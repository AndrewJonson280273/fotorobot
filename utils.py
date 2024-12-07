import sqlite3
from PyQt6.QtWidgets import *


class Database:
    def __init__(self, fname="database.sqlite"):
        self.file_name = fname

    def execute(self, sql):
        # Выполнение запроса и получение всех результатов
        self.con = sqlite3.connect(self.file_name)
        self.cur = self.con.cursor()
        result = self.cur.execute(sql).fetchall()
        self.con.close()

        return result

    def execute_some(self, sql, count):
        # Выполнение запроса и получение всех результатов
        self.con = sqlite3.connect(self.file_name)
        self.cur = self.con.cursor()
        result = self.cur.execute(sql).fetchmany(count)
        self.con.close()
        return result

    def commit(self, sql):
        # Выполнение запроса и получение всех результатов
        self.con = sqlite3.connect(self.file_name)
        self.cur = self.con.cursor()
        self.cur.execute(sql)
        self.con.commit()
        # self.con.close()

    def insert(self, table, columns, values):
        self.commit(f"INSERT INTO {table}({columns}) VALUES({values})")

    def add_element(self, params: dict, table):
        columns = params.keys()
        columns_sql = ",".join(columns)
        # image = params.pop("image")
        for param, value in params.items():
            if param == "image":
                params["image"] = '"' + value + '"'
            else:
                id = self.execute(f'SELECT id FROM {param} WHERE name = "{value}"')
                id = id[0][0]

                params[param] = id

        values = [str(i) for i in params.values()]
        values_sql = ",".join(values)
        self.insert(table, columns_sql, values_sql)

    def get_all_elements(self, table):
        return self.execute(f"SELECT * FROM {table}")