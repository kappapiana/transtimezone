#!/usr/bin/env python3

# SPDX-FileCopyrightText: Carlo Piana
#
# SPDX-License-Identifier: Apache-2.0

import pytz
import datetime
import argparse


def parsedate(get_date, get_time="00:00"):
    """ parses the provided date and transforms it to date elements
    returns a datetime object (todo) """

    year, month, day = [int(element) for element in get_date.split('-')]
    hour, minutes = [int(element) for element in get_time.split(':')]

    return datetime.datetime(year, month, day, hour, minutes)


def typedate():
    """function to enter manually (not from CLI)"""

    input_hour = "00:00"  # sets default date in case of no input

    while True:  # goes on until the dummy gets it right
        date = input('enter the date as YYYY-MM-DD hh:mm :> ').split(' ')

        input_day = date[0]
        if len(date) == 2:  # two elements are expected in the list
            input_hour = date[1]
        elif len(date) < 2:
            print(f"you have entered only {len(date)} "
                  f"elements\nwe use midnight")
        try:
            input_date = parsedate(input_day, input_hour)
            break
        except:
            print("you have entered a wrong data, see the reference it \
                   must be YYYY-MM-DD HH:MM")

    return input_date


parser = argparse.ArgumentParser()
parser.add_argument("date", type=str, nargs="?",
                    help="The date in YYYY-MM-DD format")
parser.add_argument("time", type=str, nargs="?", default="00:00",
                    help="The time in HH:MM format (if not provided, \
                    defaults to 00:00)")
parser.add_argument("-t", "--timezone", type=str, help="Add the timezone if you know \
                    what it is")
args = parser.parse_args()

if args.date is None:
    print("No date has been entered")
    from_date = typedate()

else:
    try:
        from_date = parsedate(args.date, args.time)
    except:
        print("You have entered a wrong data, see the reference "
              "it must be YYYY-MM-DD HH:MM")
        from_date = typedate()

if args.timezone is None:

    try:
        input_tz = input('\nenter the timezone, if unsure, leave blank, we\'ll use the system one :> ')
        tz = pytz.timezone(input_tz)
    except:
        tz = pytz.timezone(datetime.datetime.now().astimezone().tzname())
        print(f"\n*** no time zone is provided, "
              f"we are using the current system one, {tz} ***\n")

else:
    tz = pytz.timezone(args.timezone)

localized_from_date = tz.localize(from_date)
print("Entered Time is:", localized_from_date.strftime("%Y:%m:%d %H:%M:%S %Z (%z)"))


translates_to = {"UTC": "Universal Coordinated Time",
                 "CET": "Central European Time",
                 "America/New_York": "New York Time",
                 "America/Los_Angeles": "Los Angeles Time",
                 "Cuba": "Cuba time",
                 "Zulu": "Zulu time (or US Navy Time)",
                 "Australia/Sydney": "Sydney Time",
                 "Asia/Tokyo": "Tokyo (Japan) Time",
		 "Asia/Dubai": "Dubai (Gulf) time"}

print("+----------------------------------------------------------------------------+")
for timezone, timename in translates_to.items():

    translated_to = localized_from_date.astimezone(pytz.timezone(timezone))
    time_true = translated_to.strftime("%Y:%m:%d %H:%M:%S %Z ")
    zone_true = translated_to.strftime("(%z)")
    print(f"| {timename + ':':<32} {time_true:<25} {zone_true :16}|")

print("+----------------------------------------------------------------------------+")
