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
    return async_db


@pytest.fixture
def dummy_data():
    return """
test_eng	test_cze	note	special	author
eng	cze	note	special	author
english	czech	notes	specials	authors
    """.strip()

async def test_prepare_db(adb):
    table_name = "test"
    sql = (f"SELECT count(*) FROM sqlite_master WHERE type='table' AND name=?", [f"{table_name}"])
    
    async with adb.conn.execute(*sql) as cursor:
        results = await cursor.fetchall() # result format is here [(0,)]
        assert results[0][0] == 0 # should find 0 match, table wasn't created yet
    
    await adb.prepare_db(table_name) # create table
    
    async with adb.conn.execute(*sql) as cursor:
        results = await cursor.fetchall()
        assert results[0][0] == 1 # should find 1 match

    await adb.conn.close() # close whole connection


# async def test_fill_db(adb, dummy_data):
