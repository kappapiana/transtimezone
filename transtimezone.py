#!/usr/bin/env python3

# SPDX-FileCopyrightText: Carlo Piana
#
# SPDX-License-Identifier: Apache-2.0

import pytz
import datetime
import argparse
import re

# Define the most relevant timezones
translates_to = {"UTC": "Universal Coordinated Time",
                 "CET": "Central European Time",
                 "America/New_York": "New York Time",
                 "America/Los_Angeles": "Los Angeles Time",
                 "Australia/Sydney": "Sydney Time",
                 "Asia/Tokyo": "Tokyo (Japan) Time",
                 "Europe/London": "London time, (GMT or BST)"}

def regmatch(input):
    ''' searches for a partial match in the file of
    cities and proposes the ones relevant'''

    pattern = r'.*'+input+'.*'

    with open("tz.asc") as f: 
        find = re.findall(pattern, f.read(), re.IGNORECASE)
    
    for i in find:
        print(i)

def asker():
    count = 0 # We need a counter
    while True: # Cycle until counter is met
        try:
            input_tz = input('\nenter the timezone, if unsure, leave blank, we\'ll use UTC after three times :> ')
            tz = pytz.timezone(input_tz)
            return tz
            break
        except:
            if count < 2 : # Ask Three Time then quit.
                if input_tz == "":
                    print(f"\n*** no valid time zone is provided *** "
                        f"please use a valid one, such as:\n")
                    for timezone, timename in translates_to.items():
                        print(f"- {timezone}, ({timename})")
                else:
                    print(f"You have written {input_tz}, do you mean one of the following?")
                    regmatch(input_tz)

                count = count + 1
            else:
                tz = pytz.timezone("UTC")
                print(f"\nNo valid timezone has been provided")
                print(f"after 3 times. We are using ***UTC***\n")
                return tz
                break
    print(tz)

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
parser.add_argument("-o", "--tozone", type=str, help="Add the timezone if you know \
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
    tz = asker()

else:
    try: 
        tz = pytz.timezone(args.timezone)
    except:
        tz = asker()

localized_from_date = tz.localize(from_date)
print("\nEntered Time is:", localized_from_date.strftime("%Y:%m:%d %H:%M:%S %Z (%z)"))

if args.tozone: 
    try: 
        translated_to = localized_from_date.astimezone(pytz.timezone(args.tozone))
        time_true = translated_to.strftime("%Y:%m:%d %H:%M:%S %Z ")
        zone_true = translated_to.strftime("(%z)")
        print("\n+--------------------------selected Time-------------------------------------+")
        print(f"|\n| Translates To {args.tozone + ':':<21} {time_true:<25} {zone_true :13}|\n|")

        print("+---------------------------Other Times--------------------------------------+")
    except:
        timezone_to = str(asker()) #use the asking function
        translated_to = localized_from_date.astimezone(pytz.timezone(timezone_to))
        time_true = translated_to.strftime("%Y:%m:%d %H:%M:%S %Z ")
        zone_true = translated_to.strftime("(%z)")
        print("\n+--------------------------selected Time-------------------------------------+")
        print(f"| {'':<75}|")
        print(f"| Translates To {timezone_to + ':':<21} {time_true:<25} {zone_true :13}|")
        print(f"| {'':<75}|")
        print("+---------------------------Other Times--------------------------------------+")
    
else:
    print("+----------------------------------------------------------------------------+")
    print(f"| {'':<75}|")
    print("| If these times do not provide the desidered timezone, try -o [timezone to] |")
    print(f"| {'':<75}|")

for timezone, timename in translates_to.items():

    translated_to = localized_from_date.astimezone(pytz.timezone(timezone))
    time_true = translated_to.strftime("%Y:%m:%d %H:%M:%S %Z ")
    zone_true = translated_to.strftime("(%z)")
    print(f"| {timename + ':':<35} {time_true:<25} {zone_true :13}|")

print("+----------------------------------------------------------------------------+")
