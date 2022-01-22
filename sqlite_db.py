import sqlite3
from datetime import datetime, timedelta
from traceback import print_tb


class Query:
    def __init__(self, path: str):
        self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()

    def __enter__(self):
        return self.connection, self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        if (self.connection):
            self.connection.close()
            print("Соединение с SQLite закрыто")

        if exc_type:
            print_tb(exc_tb)
            print(f'{exc_type} - {exc_val}')

        return True


def init_db():
    with Query('sqlite_products.db') as quer:
        conn, curs = quer
        sqlite_create_table_query = '''CREATE TABLE IF NOT EXISTS products (
                                        url TEXT NOT NULL,
                                        price REAL NOT NULL,
                                        date datetime);'''

        curs.execute(sqlite_create_table_query)
        conn.commit()


def add_str_db(url: str, price: float, date):
    with Query('sqlite_products.db') as quer:
        conn, curs = quer
        date = date.strftime('%Y-%m-%d %H:%M')
        curs.execute("INSERT INTO products VALUES(?, ?, ?);", (url, price, date))
        conn.commit()


def del_str_db(url: str):
    with Query('sqlite_products.db') as quer:
        conn, curs = quer
        curs.execute(f'DELETE FROM products WHERE url= "{url}";')
        conn.commit()


def ret_prod_from_db(url: str):
    with Query('sqlite_products.db') as quer:
        conn, curs = quer
        curs.execute(f'SELECT * FROM products WHERE url = "{url}";')
        return curs.fetchall()

if __name__ == '__main__':
    init_db()
    url = 'https://sbermegamarket.ru/catalog/details/smartfon-xiaomi-redmi-note-10-pro-128gb-glacier-blue-100028274010/'
    import random

    for i in range(100):
        add_str_db(f'{url}-{i//10}', 10000 + random.randint(0, 5000), datetime.now() + timedelta(days=random.randint(1,150), hours=9, minutes=30))

    #del_str_db(4)
    #a = ret_prod_from_db(6)
    #print(a)