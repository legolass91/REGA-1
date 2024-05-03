import os
import sqlite3
from sqlite3 import IntegrityError

class DB:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def __enter__(self):
        self.connection = sqlite3.connect(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'main.db'))
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.commit()
        self.connection.close()

    def create_schema(self):
        query = '''
            CREATE TABLE IF NOT EXISTS accounts
            (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_id INTEGER NOT NULL,
                first_name TEXT,
                last_name TEXT,
                username TEXT,
                password TEXT,
                email TEXT,
                region TEXT,
                birth_day INTEGER,
                birth_month INTEGER,
                birth_year INTEGER,
                score INTEGER,
                active BOOLEAN
            )
            '''
        self.cursor.execute(query)
        # query = '''
        #     CREATE TABLE IF NOT EXISTS accounts
        #     (
        #         id INTEGER PRIMARY KEY AUTOINCREMENT,
        #         account_id INTEGER NOT NULL,
        #         first_name TEXT,
        #         last_name TEXT,
        #         username TEXT,
        #         password TEXT,
        #         email TEXT,
        #         region TEXT,
        #         birth_day INTEGER,
        #         birth_month INTEGER,
        #         birth_year INTEGER,
        #         score INTEGER,
        #         active BOOLEAN,
        #         FOREIGN KEY (account_id) REFERENCES proxy_data(id)
        #         FOREIGN KEY (account_id) REFERENCES cookies_data(id)
        #
        #     )
        #     '''
        # self.cursor.execute(query)
        # query = '''
        #     CREATE TABLE IF NOT EXISTS proxy_data
        #     (
        #         id INTEGER PRIMARY KEY,
        #         proxy_data1 TEXT,
        #         proxy_data2 TEXT,
        #         proxy_region
        #     );
        #     '''
        # self.cursor.execute(query)
        # query = '''
        #     CREATE TABLE IF NOT EXISTS cookies_data
        #     (
        #         id INTEGER PRIMARY KEY,
        #         cookies_data1 TEXT,
        #         cookies_data2 TEXT,
        #     );
        #     '''
        # self.cursor.execute(query)

    def create_new_account(self, account_id, first_name, last_name, username, password, email, region, birth_day, birth_month, birth_year):
        query = '''
            INSERT INTO accounts(account_id, first_name, last_name, username, password, email, region, birth_day, birth_month, birth_year)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        self.cursor.execute(query, (account_id, first_name, last_name, username, password, email, region, birth_day, birth_month, birth_year))

    def write_proxy_data(self):
        pass

    def write_cookies_data(self):
        pass
