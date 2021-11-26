# modules
import webbrowser
from win10toast_click import ToastNotifier
from typing import Tuple
from checker_functions import Price


def show_notification(url: str, prices: Tuple[Price, Price]):
    # initialization
    toaster = ToastNotifier()

    toaster.show_toast(
        f"The price has changed: new: {prices[0]}, old: {prices[1]}",  # title
        "Click to open URL! >>",  # message
        icon_path=None,  # 'icon_path'
        duration=10,  # for how many seconds toast should be visible; None = leave notification in Notification Center
        threaded=True,
        # True = run other code in parallel; False = code execution will wait till notification disappears
        callback_on_click=lambda: open_url(url)  # click notification to run function
    )


def open_url(page_url: str):
    try:
        webbrowser.open_new_tab(page_url)
        print('Opening URL...')
    except:
        print('Failed to open URL. Unsupported variable type.')


if __name__ == '__main__':
    page_url = 'https://sbermegamarket.ru/catalog/details/smartfon-xiaomi-redmi-note-10-pro-128gb-glacier-blue-100028274010/'
    show_notification(page_url, (123, 145))
