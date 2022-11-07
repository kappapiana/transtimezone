#!/usr/bin/env python3

# import datetime
import pytz
import datetime
import argparse


def parsedate(year, time="00:00"):
    '''
    parses the provided date and transforms it to date elements
    returns a datetime object (todo)
    '''

    if time != "00:00":
        year, month, day = [int(element) for element in year.split('-')]
        hour, minutes = [int(element) for element in time.split(':')]
    else:
        year, month, day = [int(element) for element in input_day.split('-')]
        hour = 00
        minutes = 00

    return datetime.datetime(year, month, day, hour, minutes)

    print(f"the date you entered is {year}\nand the time is {time}")


parser = argparse.ArgumentParser()
parser.add_argument("date", type=str, nargs="?", help="The date in YYYY-MM-DD format")
parser.add_argument("time", type=str, nargs="?", default="00:00", help="The time in HH:MM format (if not provided, defaults to 00:00)")
parser.add_argument("-t", "--timezone", type=str, help="Add the timezone if you know what it is")
args = parser.parse_args()

print(args.date, args.time, args.timezone)

# parsedate(args.date, args.time)
# TODO: transform the logic here below in function,
# to be reused with parsed arguments if provided.

if args.date is None:
    print("No date has been entered")

    date = input('enter the date as YYYY-MM-DD hh:mm :> ').split(' ')
    input_day, input_hour = [element for element in date]

else:
    from_date = parsedate(args.date, args.time)


if args.timezone is None:

    input_tz = input('enter the timezone, if unsure, leave blank :> ')
    tz = pytz.timezone(input_tz)
else:
    tz = pytz.timezone(args.timezone)




print("Current Time:", from_date.strftime("%Y-%m-%d %H:%M:%S %Z %z"))


localized_from_date = tz.localize(from_date)
print("Current Time:", localized_from_date.strftime("%Y:%m:%d %H:%M:%S %Z %z"))


translates_to = {"UTC": "Universal Coordinated Time",
                 "CET": "Central European Time",
                 "America/New_York": "New York Time",
                 "America/Los_Angeles": "Los Angeles Time",
                 "Cuba": "Cuba time"}

for timezone, timename in translates_to.items():

    translated_to = localized_from_date.astimezone(pytz.timezone(timezone))
    print(timename, ":", translated_to.strftime("%Y:%m:%d %H:%M:%S %Z (%z)"))

# convert UTC timezone to 'US/Central'



# print(pytz.all_timezones)
