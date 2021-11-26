import os
import pickle
from checker import Checker
from typing import List


if os.path.exists('urls_data.pickle'):
    with open('urls_data.pickle', 'rb') as f:
        checker_objects = pickle.load(f)
else:
    checker_objects: List[Checker] = []

def create(url: str, check_delay, ascend:bool):
    check_obj = Checker(url, check_delay, ascend)
    checker_objects.append(check_obj)

    with open('urls_data.pickle', 'wb') as f:
        pickle.dump(checker_objects, f)


def clear():
    with open('urls_data.pickle', 'wb') as f:
        pickle.dump([], f)


def show_notification(prices):
    return f'  old price: {prices[1]}, new price: {prices[0]}'


def show_list() -> str:
    res = ''
    for num, checker in enumerate(checker_objects):
        res += f'{num+1})\n price:{checker.price}\nprev price: {checker.prev_price}\n check delay: {checker.check_delay}\n url: {checker.url}+\n\n'
    return res


def del_ch_obj(num: int):
    del checker_objects[num-1]
    with open('urls_data.pickle', 'wb') as f:
        pickle.dump(checker_objects, f)

def ch_set_delay(num:int, delay:str):
    obj = checker_objects.pop(num - 1)
    obj.delay(delay)
    checker_objects.append(obj)
    with open('urls_data.pickle', 'wb') as f:
        pickle.dump(checker_objects, f)