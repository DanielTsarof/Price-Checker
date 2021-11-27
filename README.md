# Price-Checker
price checker windows application

This application monitors the prices of selected products and displays a notification if the price has changed.

To configure the application, run the settings file, it has a simple gui. To track some product add it's url
in the big text field (aliexpress, ozon and sbrmegamarket are currently supported). Then add a check delay in 
the small text field in format days-hours-minutes (like 00-10-30) and click "Создать" (Create) button. Click
on "Просмотреть" (manage) button to show all created checker objects in the big text field. Use check-box if
you want to recieve notifications only if price is decreased. After creating  the objects tun the __main__ 
file to monitor prices.

Нou can send commands to the small text field using the "Команда" (Command) button. Supported commands:

  del <number>  - delete checker object with given number
  set <number> <delay>  - change check delay of the object with given number
  !clear  - delete all created checker objects

To add new marketplace support you need:
  1. add new function in the checker_functions file that assepts product url and return Price class (price, currency).
  2.import this function to the checker file and add couple (marketplace_domain, checker_function) to the price_checker_functions dict. 
  
  if something doesn't work try to change user agen in get_html function
  
  # This is the early build. Application is not fully tested yet.
