import pytest
import pytest_asyncio

# internal imports
from easydict_nicegui.backends.sqlite_backend import search_async, SQLiteBackend

# type anotations
adb: SQLiteBackend


@pytest_asyncio.fixture
async def adb(tmp_path):
    file_db = tmp_path / "test.db"
    file_db.touch()
    async_db = SQLiteBackend(file_db)
    await async_db.db_init()
    try:
        yield async_db
    finally:
        await async_db.conn.close()


@pytest.fixture
def dummy_data():
    return """
test_eng	test_cze	note	special	author
eng	cze	note	special	author
english	czech	notes	specials	authors
    """.strip()

@pytest.fixture
def dummy_file(tmp_path, dummy_data):
    file = tmp_path / "test.db"
    file.write_text(dummy_data)
    return file


async def test_prepare_db(adb):
    table_name = "test"
    sql = (
        f"SELECT count(*) FROM sqlite_master WHERE type='table' AND name=?",
        [f"{table_name}"],
    )

    async with adb.conn.execute(*sql) as cursor:
        results = await cursor.fetchall()  # result format is here [(0,)]
        assert results[0][0] == 0  # should find 0 match, table wasn't created yet

    await adb.prepare_db(table_name)  # create table

    async with adb.conn.execute(*sql) as cursor:
        results = await cursor.fetchall()
        assert results[0][0] == 1  # should find 1 match


async def test_fill_db(adb, dummy_file, dummy_data):
    await adb.prepare_db("eng_cze") # create table
    await adb.fill_db(dummy_file)  # fill table with dummy data from dummy file
    sql = "SELECT * FROM eng_cze" # get all data from table
    dummy_data = dummy_data.split("\n") # split dummy data by new line
    dummy_data = [tuple(row.split("\t")) for row in dummy_data] # every line is now tuple
    async with adb.conn.execute(sql) as cursor:
        index = 0
        async for row in cursor: # one row is tuple of columns
            assert row == dummy_data[index]
            index += 1
