import os
import pickle
from checker import Checker
from typing import List

# List of Checker objects
if os.path.exists('urls_data.pickle'):
    with open('urls_data.pickle', 'rb') as f:
        checker_objects = pickle.load(f)
else:
    checker_objects: List[Checker] = []

# functions for working with list of Checker objects

def create(url: str, check_delay, ascend:bool):
    '''Creates new Checker object, than adds it to the list and saves list.
    '''
    check_obj = Checker(url, check_delay, ascend)
    checker_objects.append(check_obj)

    with open('urls_data.pickle', 'wb') as f:
        pickle.dump(checker_objects, f)


def clear():
    '''Clears the list of checker objects
    '''
    with open('urls_data.pickle', 'wb') as f:
        pickle.dump([], f)


def show_notification(prices):
    return f'  old price: {prices[1]}, new price: {prices[0]}'


def show_list() -> str:
    '''returns List of saved objects as str.
    '''
    res = ''
    for num, checker in enumerate(checker_objects):
        res += f'{num+1})\n price:{checker.price}\nprev price: {checker.prev_price}\n check delay: {checker.check_delay}\n url: {checker.url}+\n\n'
    return res


def del_ch_obj(num: int):
    '''deletes object from list woth a given number
    '''
    del checker_objects[num-1]
    with open('urls_data.pickle', 'wb') as f:
        pickle.dump(checker_objects, f)

def ch_set_delay(num:int, delay:str):
    '''changes check_delay of object with a given number
    '''
    obj = checker_objects.pop(num - 1)
    obj.delay(delay)
    checker_objects.append(obj)
    with open('urls_data.pickle', 'wb') as f:
        pickle.dump(checker_objects, f)