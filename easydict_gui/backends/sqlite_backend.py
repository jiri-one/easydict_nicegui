from pathlib import Path
import sqlite3
import re
from typing import Iterator

# internal imports
from .backend import DBBackend, Result


class SQLiteBackend(DBBackend):
    @staticmethod
    def regexp(expr, item):
        """Helper function for search with regex"""
        reg = re.compile(expr)
        return reg.search(item) is not None

    def __init__(self):
        try:
            # TODO: import it from settings, not hardcode it
            db_file = Path(__file__).parent.parent / "dict_data/easydict.db"
            if not db_file.exists():
                raise FileNotFoundError()
        except FileNotFoundError:
            print(f"DB file {db_file} not found.")
            exit()
        conn_file = sqlite3.connect(db_file)
        self.conn = sqlite3.connect(':memory:')
        conn_file.backup(self.conn)
        self.conn.create_function("REGEXP", 2, self.regexp)
        self.cursor = self.conn.cursor()

    def prepare_db(self, db_name: str):
        """It creates a table in the database.
        A method that is not (yet) used in production."""
        sql = f"""CREATE TABLE if not exists {db_name}
                  (eng TEXT, cze TEXT, notes TEXT,
                   special TEXT, author TEXT)
                """
        self.cursor.execute(sql)

    def fill_db(self, raw_file: str | Path = None):
        """Filling the database with data.
        A method that is not (yet) used in production."""
        if not raw_file:
            raw_file = Path(__file__).parent.parent / "data/en-cs.txt"
            if not raw_file.exists():
                raise FileNotFoundError()

        data = []
        with open(raw_file) as file:
            for line in file:
                line_list = line.split("\t")
                data.append(
                    (
                        line_list[0],
                        line_list[1],
                        line_list[2],
                        line_list[3],
                        str(line_list[4]).replace(
                            "\n", ""
                        ),  # sometimes there are some unnecessary new lines
                    )
                )
        self.cursor.executemany("INSERT INTO eng_cze VALUES (?,?,?,?,?)", data)
        # save data
        self.conn.commit()

    def search_in_db(
        self, word, lang, fulltext: bool = None
    ) -> Iterator[Result] | None:
        if fulltext:
            sql = (f"SELECT * FROM eng_cze WHERE {lang} LIKE ?", [f"%{word}%"])
        else:
            sql = (f"SELECT * FROM eng_cze WHERE {lang} REGEXP ?", [rf"\b{word}\b"])
        self.cursor.execute(*sql)
        results = self.cursor.fetchall()
        if not results:
            return None
        for result in iter(results):
            yield Result(*result)
            # yield dict(zip(("eng", "cze", "notes", "special", "author"), result))
