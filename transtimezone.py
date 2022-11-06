#!/usr/bin/env python3

# import datetime
import pytz
import datetime

date = input('enter the date as YYYY-MM-DD hh:mm :> ').split(' ')
print(date)

if len(date) == 2:
    print("lunga")
    input_day, input_hour = [element for element in date]
    input_day_elements = input_day.split('-')
    input_hour_elements = input_hour.split(':')

    year, month, day = [int(element) for element in input_day_elements]
    hour, minutes = [int(element) for element in input_hour_elements]
else:
    print("breve")

input_tz = input('enter the timezone, if unsure, leave blank :> ')

tz = pytz.timezone(input_tz)

from_date = datetime.datetime(year, month, day, hour, minutes)


print("Current Time:", from_date.strftime("%Y-%m-%d %H:%M:%S %Z %z"))


localized_from_date = tz.localize(from_date)
print("Current Time:", localized_from_date.strftime("%Y:%m:%d %H:%M:%S %Z %z"))


translates_to = {"UTC": "Universal Coordinated Time", "CET": "Central European Time", "America/New_York": "New York Time", "America/Los_Angeles": "Los Angeles Time"}

for timezone, timename in translates_to.items():

    translated_to = localized_from_date.astimezone(pytz.timezone(timezone))
    print(timename, ":", translated_to.strftime("%Y:%m:%d %H:%M:%S %Z (%z)"))

# convert UTC timezone to 'US/Central'



# print(pytz.all_timezones)
