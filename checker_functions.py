import requests
import re
from bs4 import BeautifulSoup
from dataclasses import dataclass
from unidecode import unidecode
from functools import total_ordering


def get_html(url: str):
    response = requests.get(url, headers = {'User-agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.text, 'html5lib')
    return soup


@dataclass
@total_ordering
class Price():
    currency: str = 'None'
    value: float

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, quantity):
        if quantity < 0:
            raise ValueError('Cannot be negative')
        self._value = quantity

    def set_currency(self, high_level_domain:str):
        dom_dict = {'ru': 'rub',
                    'eu': 'eu',
                    'us': 'usd',
                    'cn':'cnu'}

        try:
            self.currency = dom_dict[high_level_domain]
        except KeyError:
            self.currency = 'unknown'

    def __repr__(self):
        return f'{self.value} {self.currency}'

    def __eq__(self, other):
        if self.value == other.value:
            return True
        return False

    def __gt__(self, other):
        if self.value > other.value:
            return True
        return False

    def __add__(self, other):
        return Price(self.currency, self.value + other.value)

    def __sub__(self, other):
        return Price(self.currency, self.value - other.value)


def get_domain(url: str):
    return re.search(r'/[\w.]+', url).group(0)[1:]


def aliexpress_price(url: str) -> Price:
    str_html_req = unidecode(str(get_html(url)('span')))
    str_price = (
        re.search(r'product-price-current">[0-9\s,-]+ \w+', str_html_req).
            group(0).split('>')[1].
            replace(' ', '').
            replace(',', '.')
    )

    currency = re.search(r'[а-яa-z]+', str_price).group(0)
    prices = str_price.replace(currency, '').split('-')
    avg_price = round(sum(map(lambda x: float(x), prices)) / len(prices))
    return Price(currency, avg_price)

def ozon_price(url: str, high_level_domain = 'ru')-> Price:
    html = unidecode(str(get_html(url)('div')))
    str_price_req = re.search(r'"finalPrice":\d+', html).group(0)
    price = float(str_price_req[str_price_req.index(':')+1:])
    res = Price(value=price)
    res.set_currency(high_level_domain)
    return res

def sbermarket_price(url: str, high_level_domain = 'ru')-> Price:
    html = unidecode(str(get_html(url)))
    str_price_req = re.search(r'price__final">[\d\s]+', html).group(0).replace(' ','')
    price = float(str_price_req[str_price_req.index('>') + 1:])
    res = Price(value=price)
    res.set_currency(high_level_domain)
    return res



if __name__ == '__main__':
    test_url_ali = 'https://aliexpress.ru/item/32903212605.html?spm=a2g0o.best.old-user.1.23ca5430Uu2qBI&pdp_ext_f=%7B%22source_from%22:' \
                   '%22channel%22,%22sku_id%22:%2210000010056870574%22%7D&_ga=2.126504461.1485445389.1637316854-2130996722.1599981946&_gac=' \
                   '1.182095573.1636626770.CjwKCAiAm7OMBhAQEiwArvGi3HB9m3jpu3qdxs9aZ9kbQRxYqkF-FVhz6HEFl1EOliqjHQUoZSkgjhoCD2MQAvD_BwE'

    test_url_ozon = 'https://www.ozon.ru/product/dispenser-dlya-napitkov-kilner-barrel-na-podstavke-1-l-151962139/?sh=vR3DiNqP'
    test_url_ozon2 = 'https://www.ozon.ru/product/14-1-noutbuk-digma-14-p416-intel-pentium-j3710-1-6-ggts-ram-4-gb-ssd-128-gb-intel-hd-graphics-405-323005792/?sh=sI8XzE04'
    #html_ali = get_html(test_url_ali)
    print(aliexpress_price(test_url_ali))

    #html = unidecode(str(get_html(test_url_ozon2)('div')))
    #print(html)
    #print(re.findall(r'"finalPrice":\d+', html))
    print(get_domain(test_url_ali))

    print(ozon_price(test_url_ozon, 'ru'))

    test_url_sber = 'https://sbermegamarket.ru/catalog/details/smartfon-xiaomi-redmi-note-10-pro-128gb-glacier-blue-100028274010/'
    print(get_domain(test_url_sber))
    #print(unidecode(str(get_html(test_url_sber))))
    html_sber = get_html(test_url_sber)
    print(sbermarket_price(test_url_sber))