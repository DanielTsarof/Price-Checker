from work_functions import checker_objects, show_list, clear, ch_set_delay
import win_notifications
from work_functions import checker_objects
import time
import pickle

if __name__ == '__main__':

    print(show_list())
    # ch_set_delay(1, '00-03-00')
    # main loop
    while True:
        for obj in checker_objects:
            if obj.check_time():
                print(obj)
                try:
                    prices = obj.check_price()
                    print(obj, prices)
                except:
                    prices = None
                if prices:

                    print(obj.url)
                    with open('urls_data.pickle', 'wb') as f:
                        pickle.dump(checker_objects, f)
                    win_notifications.show_notification(obj.url, prices)
        time.sleep(1)
        print('b')
        # break
