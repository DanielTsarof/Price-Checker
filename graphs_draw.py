import matplotlib.pyplot as plt
import matplotlib.dates
from sqlite_db import ret_prod_from_db
from datetime import datetime


def draw_graph(url):
    data = ret_prod_from_db(url)
    if data:
        data = dict(
            sorted(
                [(datetime.strptime(x[2], '%Y-%m-%d %H:%M'), x[1]) for x in data],
                key=lambda a: a[0]))
    else:
        raise ValueError

    print(type(data))
    print(matplotlib.dates.date2num(
        list(
            data.keys())
    )
    )

    plt.plot(list(data.keys()), list(data.values()))
    plt.gcf().autofmt_xdate()
    plt.xlabel('datetime')
    plt.ylabel('price')

    plt.show()


if __name__ == '__main__':
    from pprint import pprint

    draw_graph('https://sbermegamarket.ru/catalog/details/smartfon-xiaomi-redmi-note-10-pro-128gb-glacier-blue-100028274010/-1')

    print(datetime.now())
