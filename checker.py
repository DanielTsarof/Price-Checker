import datetime
from checker_functions import Price, get_domain, aliexpress_price, ozon_price, sbermarket_price
from typing import Tuple

# keys: domains, values: price get functions
price_get_functions = {'aliexpress.ru': aliexpress_price,
                       'www.ozon.ru': ozon_price,
                       'sbermegamarket.ru': sbermarket_price
                       }


class Checker():
    '''Class representing product, it's url, and time interval for price checking.'''

    @staticmethod
    def _set_delay(delay: str):
        '''
        converts the str object in format dd-hh-mm
        itno datetime.timedelta object
        '''
        times = list(
            map(lambda x: int(x), delay.split('-'))
        )
        return datetime.timedelta(days=times[0], hours=times[1], minutes=times[2])

    def __init__(self, url: str, check_delay, decline_only: bool = False):
        self.url = url
        self.check_delay = self._set_delay(check_delay)
        self.domain = get_domain(url)
        self.get_price = price_get_functions[self.domain]
        self.price = self.get_price(url)
        self.prev_price = None
        self.next_check = datetime.datetime.now() + self.check_delay
        self.decline_only = decline_only

    def delay(self, delay: str):
        self.check_delay = self._set_delay(delay)

    def check_price(self) -> Tuple[Price, Price]:
        '''Checks if product price has changed
        '''
        current_price = self.get_price(self.url) # - Price('rub',100)
        self.price, self.prev_price = current_price, self.price
        if current_price < self.prev_price:
            return self.price, self.prev_price
        if current_price > self.prev_price and self.decline_only is False:
            return self.price, self.prev_price

    def check_time(self):
        '''returns True fi current time > time for the next check else False.
        '''
        if datetime.datetime.now() > self.next_check:
            self.next_check = datetime.datetime.now() + self.check_delay
            return True
        return False

    def __repr__(self):
        return f'Checker(current price = {self.price},prev price = {self.prev_price},' \
               f' delay = {self.check_delay}, next check = {self.next_check}, url = {self.url})'


if __name__ == '__main__':
    stuff1 = Checker(
        'https://sbermegamarket.ru/catalog/details/smartfon-xiaomi-redmi-note-10-pro-128gb-glacier-blue-100028274010/',
        '01-10-30')

    print(stuff1)
    print(stuff1.check_time())
    print(stuff1.check_price())
