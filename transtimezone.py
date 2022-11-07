#!/usr/bin/env python3

# import datetime
import pytz
import datetime
import argparse


def parsedate(year, date):
    print(f"date is {date}")


parser = argparse.ArgumentParser()
parser.add_argument("date", type=str, nargs="?", help="The date in YYYY-MM-DD format")
parser.add_argument("time", type=str, nargs="?", default="00:00", help="The time in HH:MM format (if not provided, defaults to 00:00)")
parser.add_argument("-t", "--timezone", type=str, help="Add the timezone if you know what it is")
args = parser.parse_args()

print(args.date, args.time, args.timezone)

if args.date == None :
    print("No date has been entered")

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
        print(date)
        input_day = date[0]
        print(input_day)
        input_day_elements = input_day.split('-')

        year, month, day = [int(element) for element in input_day_elements]
        hour = 00
        minutes = 00

if args.timezone == None :

    input_tz = input('enter the timezone, if unsure, leave blank :> ')
    tz = pytz.timezone(input_tz)
else:
    tz = pytz.timezone(args.timezone)

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
