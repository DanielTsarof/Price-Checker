import sqlite3
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
                                        id INTEGER,
                                        url TEXT NOT NULL,
                                        price REAL NOT NULL,
                                        date datetime);'''

        curs.execute(sqlite_create_table_query)
        conn.commit()


def add_str_db(id: int, url: str, price: float, date):
    with Query('sqlite_products.db') as quer:
        conn, curs = quer
        curs.execute("INSERT INTO products VALUES(?, ?, ?, ?);", (id, url, price, date))
        conn.commit()


def del_str_db(id: int):
    with Query('sqlite_products.db') as quer:
        conn, curs = quer
        curs.execute(f"DELETE FROM products WHERE id= {id};")
        conn.commit()


def ret_prod_from_db(id: int):
    with Query('sqlite_products.db') as quer:
        conn, curs = quer
        curs.execute(f"SELECT * FROM products WHERE id = {id};")
        return curs.fetchall()

if __name__ == '__main__':
    init_db()
    url = 'https://sbermegamarket.ru/catalog/details/smartfon-xiaomi-redmi-note-10-pro-128gb-glacier-blue-100028274010/'
    import random

    #for i in range(100):
    #    add_str_db(i // 10, url, 10000 + random.randint(0, 5000), f'{random.randint(1, 31)}-{random.randint(1, 12)}-21')
    del_str_db(4)
    a = ret_prod_from_db(6)
    print(a)