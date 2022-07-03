import requests
from datetime import datetime
from pytz import timezone
from time import time
from time import sleep

started_time = datetime.fromtimestamp(1600001700)
started_time = started_time.astimezone(timezone('US/Pacific'))
start_time_pacific = started_time.strftime("%B %d, %I:%M %p")
print("New Year Event On " + start_time_pacific)

current_time = int(round(time(), 0))
new_year_time = (current_time - 1600001700)
quotient = (new_year_time / 446400)
five_quotient = (300 / 446400)
str_new_year_time = str(quotient)
str_new_year_time_list = str_new_year_time.split(".")
string_before_dec = str_new_year_time_list[0]
int_before_dec = int(string_before_dec)
x = quotient - int_before_dec
print(int_before_dec)
print(five_quotient)
print(x)

if x <= five_quotient:
    print("Send Isaac Message")
else:
    print("Didn't send Isaac a message")