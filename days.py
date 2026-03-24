from enum import Enum

import calendar
import datetime


today = datetime.date.today()
tomorrow = today + datetime.timedelta(1)
print(f"{today.strftime('%A')}, {today.day}/{today.month}/{today.year}")




