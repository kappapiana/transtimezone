#!/usr/bin/env python3

# SPDX-FileCopyrightText: Carlo Piana
#
# SPDX-License-Identifier: Apache-2.0

import pytz
import datetime
import argparse


def parsedate(year, time="00:00"):
    '''
    parses the provided date and transforms it to date elements
    returns a datetime object (todo)
    '''

    year, month, day = [int(element) for element in year.split('-')]
    hour, minutes = [int(element) for element in time.split(':')]

    return datetime.datetime(year, month, day, hour, minutes)


parser = argparse.ArgumentParser()
parser.add_argument("date", type=str, nargs="?", help="The date in YYYY-MM-DD format")
parser.add_argument("time", type=str, nargs="?", default="00:00", help="The time in HH:MM format (if not provided, defaults to 00:00)")
parser.add_argument("-t", "--timezone", type=str, help="Add the timezone if you know what it is")
args = parser.parse_args()

print(args.date, args.time, args.timezone)

if args.date is None:
    print("No date has been entered")

    input_hour = "00:00"
    date = input('enter the date as YYYY-MM-DD hh:mm :> ').split(' ')
    input_day = date[0]
    if len(date) == 2:
        input_hour = date[1]
    elif len(date) < 2 :
        print(f"you have entered only {len(date)} elements\nwe use midnight")
    from_date = parsedate(input_day, input_hour)

else:
    from_date = parsedate(args.date, args.time)


if args.timezone is None:

    input_tz = input('enter the timezone, if unsure, leave blank :> ')
    tz = pytz.timezone(input_tz)
else:
    tz = pytz.timezone(args.timezone)

localized_from_date = tz.localize(from_date)
print("Entered Time is:", localized_from_date.strftime("%Y:%m:%d %H:%M:%S %Z (%z)"))
print(f"+----------------------------------------------------------------------------+")


translates_to = {"UTC": "Universal Coordinated Time",
                 "CET": "Central European Time",
                 "America/New_York": "New York Time",
                 "America/Los_Angeles": "Los Angeles Time",
                 "Cuba": "Cuba time"}

for timezone, timename in translates_to.items():

    translated_to = localized_from_date.astimezone(pytz.timezone(timezone))
    time_true = translated_to.strftime("%Y:%m:%d %H:%M:%S %Z (%z)")
    print(f"| {timename + ':':<32} {time_true :42}|")

print(f"+----------------------------------------------------------------------------+")
# convert UTC timezone to 'US/Central'



# print(pytz.all_timezones)
