from inspect import get_annotations
from bookkeeper.repository.abstract_repository import AbstractRepository, T

import sqlite3
from typing import Any

class SQLiteRepository(AbstractRepository[T]):
    def __init__(self, db_file: str, cls: type) -> None:
        self.db_file = db_file
        self.table_name = cls.__name__.lower()
        self.fields = get_annotations(cls, eval_str=True)
        self.fields.pop('pk')
        self.cls = cls

        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            res = cur.execute('SELECT name FROM sqlite_master')
            db_tables = [t[0].lower() for t in res.fetchall()]

            if self.table_name not in db_tables:

                col_names = ', '.join(self.fields.keys())
                query = f'CREATE TABLE {self.table_name} (' \
                    f'"pk" INTEGER PRIMARY KEY AUTOINCREMENT, {col_names})'
                cur.execute(query)
        con.close()

    def add(self, obj: T) -> int:
        if getattr(obj, 'pk', None) != 0:
            raise ValueError(f'trying to add object {obj} with filled `pk` attribute')
        names = ', '.join(self.fields.keys())
        p = ', '.join("?" * len(self.fields))
        values = [getattr(obj, x) for x in self.fields]
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(
                f'INSERT INTO {self.table_name} ({names}) VALUES({p})',
                values
                )
            obj.pk = cur.lastrowid
        con.close()
        return obj.pk

    # def r():
    #     return

    def get(self, pk: int) -> T | None:
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute(
                f'SELECT * FROM {self.table_name} WHERE ROWID=={pk}'
            )
            result = cur.fetchall()
        con.close()

        if not result:
            return None
        else:
            obj_res = self.cls(result)
            obj_res.pk = result[0][0]
            return obj_res

    def grt_all(self, wher: dict[str, Any] | None = None) -> list[T]:

        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            if wher is None:
                result = cur.execute(
                    f'SELECT * FROM {self.table_name}'
                ).fetchall()
            else:
                fields = " AND ".join([f"{f} LIKE ?" for f in wher.keys()])
                result = cur.execute(
                    f'SELECT ROWID, * FROM {self.table_name} ' + f'WHERE {fields}',
                    list(wher.values())).fetchall()
        con.close()
        return result

    def update(self, obj: T) -> None:
        if obj.pk == 0:
            raise ValueError('attempt to update object with unknown primary key')
        fields = ", ".join([f"{f}=?" for f in self.fields.keys()])
        values = [getattr(obj, f) for f in self.fields]
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute(
                f'UPDATE {self.table_name} SET {fields} WHERE ROWID=={obj.pk}', values
            )
        con.close()

    def delete(self, pk: int) -> None:
        if pk == 0:
            raise ValueError('attempt to delete object with unknown primary key')
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            if not cur.execute(f'SELECT * FROM {self.table_name} WHERE ROWID=={pk}').fetchall():
                raise KeyError
            else:
                cur.execute(f'DELETE FROM {self.table_name} WHERE ROWID=={pk}')
        con.close()

