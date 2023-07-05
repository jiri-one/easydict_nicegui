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
    await adb.prepare_db("eng_cze")
    await adb.cursor.close()
    await adb.conn.close()


# async def test_fill_db(adb, dummy_data):
