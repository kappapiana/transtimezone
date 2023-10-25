#!/usr/bin/env python3

# SPDX-FileCopyrightText: Carlo Piana
#
# SPDX-License-Identifier: Apache-2.0

from datetime import datetime 
# from pytz import common_timezones
from pytz import timezone
from pytz import all_timezones
import argparse
import re
import os

# some variables used in the script
script_dir = os.path.abspath( os.path.dirname( __file__ ) )
timezone_file = str(script_dir + "/listzones.asc")

# Define the most relevant timezones to us, hardcoded
translates_to = {"CET": "Central European Time",
                 "America/New_York": "New York Time",
                 "America/Los_Angeles": "Los Angeles Time",
                 "Australia/Sydney": "Sydney Time",
                 "Asia/Tokyo": "Tokyo (Japan) Time",
                 "Europe/London": "London time, (GMT or BST)"}
 
# Optional, load timezones from config file
if os.path.isfile(timezone_file):
    with open(timezone_file) as f:
        mylist = f.read().splitlines() # otherwise uses newline
        for line in mylist:
            if not (line.startswith("#") or line == ""): #allow comments and blank lines
                (k, v) = line.split(":")
                translates_to[k] = v


class TimezoneChooser:
    """create the to-timezones, add more"""
    def __init__(self): 
        # self.timezone = timezone
        # self.name = name 
        self.dictionary = translates_to

    def addEntry(self, timezone, name):
        self.dictionary[timezone] = name
        # return self.dictionary


class DateExtractor:
    def __init__(self, date_time_string, format='%Y-%m-%d %H:%M:%S', tz=""):
        self.date_time_string = date_time_string
        self.utc = timezone("UTC")
        if tz == "":
            self.tz_obj = timezone("UTC")
        else: 
            self.tz_obj = tz
        if (type(self.date_time_string)) is str :
            # self.date_obj = datetime.strptime(self.date_time_string, format)
            self.date_obj = datetime.strptime(self.date_time_string, format)
        else:
            self.date_obj = self.date_time_string 

    def pass_dataobject(self):
        """pass data object to functions as UTC"""
        localized_date = self.tz_obj.localize(self.date_obj)
        utc_date = localized_date.astimezone(self.utc)
        return utc_date 

class OutLen:
    def __init__(self):
        self.len_part = 1
    
    def maxlength(self, length):
        """takes the value, compares with previous
        if larger, takes it"""
        if length > self.len_part:
            self.len_part = length
        
def asker():
    """the function that asks for timezones and proposes to select from a match"""

    count = 0 
    while True: # Cycle until counter is met
        try:
            input_tz = input("\nenter the timezone, if unsure, " 
                             "\nleave blank, we\'ll use UTC after three times :> "
                             )
            tz = timezone(input_tz)
            return tz
            break
        except:
            if count < 2 : # Ask Three Times then quit.
                list_matches = regmatch(input_tz)
                for i in list_matches[0:15]:
                    print(i)

                print(
                    f"\nYou have written \"{input_tz}\", do you mean one of the following "
                    "(first 15 matches)?")
                
                # 
                count = count + 1
            else:
                tz = timezone("UTC")
                return tz
                break

def parseTimezone(input_tz):
    """checks if timezone has been correctly input, if not
    it asks for timezone via asker()function"""
 
    try: 
        tz = timezone(input_tz)
    except: 
        print(f"{input_tz} is not valid")
        tz = (asker())
    
    return tz

def regmatch(input):
    ''' searches for a partial match in the list of pytz.timezone
    and proposes the ones relevant'''

    pattern = r'.*'+input+'.*'
    results = []
    
    for i in all_timezones:
        match = re.findall(pattern, i, re.IGNORECASE)
        if match :
            results.append(i)
                        
    return results
    
def parsedate(get_date, get_time="00:00"):
        """ parses the provided date and transforms it to date elements
        returns a datetime object (todo) """

        year, month, day = [int(element) for element in get_date.split('-')]
        hour, minutes = [int(element) for element in get_time.split(':')]

        return datetime(year, month, day, hour, minutes)

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
            # print(input_day, input_hour)
            print(f"You have entered {input_day} {input_hour}")
            input_date = parsedate(input_day, input_hour)
            break
        except:
            print("you have entered a wrong data, see the reference it \
                   must be YYYY-MM-DD HH:MM")

    return input_date

def input_parser():
    '''Parser from commandline'''

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
    input_args = parser.parse_args()

    return input_args

def find_from_date(args):
    '''This finds the date from which the computation is made
    '''
    if args.date is None: # no input for date, use system date as UTC
        date_system = DateExtractor(datetime.utcnow())
        date_utc = DateExtractor.pass_dataobject(date_system)
        string_date = date_utc.strftime("%Y-%m-%d %H:%M %Z - %z")
        print(f"Entered date is {string_date}")
        from_date = date_utc

    else:
        tz = parseTimezone(args.timezone)
        print(f"Timezone is {tz}")
        
        try:
            date_time_string = (f"{args.date} {args.time}")
            insert_date = DateExtractor(date_time_string, "%Y-%m-%d %H:%M", tz)
            from_date = insert_date.pass_dataobject()
            # print(tz)
            # print(from_date.astimezone(tz))

        except:
            print("You have entered a wrong data, see the reference "
                "it must be YYYY-MM-DD HH:MM")
            
            date_time_string = typedate()
            insert_date = DateExtractor(date_time_string, "%Y-%m-%d %H:%M")
            from_date = insert_date.pass_dataobject()
            # 
            # create_list()
    return from_date

def translate_everything(from_date, tz_maxlen, timetrue_maxlen, timename_maxlen):

    list_results = []
    # instantiate class
    list_timezones = TimezoneChooser()

    for tz, timename in list_timezones.dictionary.items():
        translated_to = from_date.astimezone(timezone(tz))
        time_true = translated_to.strftime("%Y:%m:%d %H:%M:%S %Z ")
        list_results.append([tz, timename, time_true])

        tz_maxlen.maxlength(len(tz))
        timetrue_maxlen.maxlength(len(time_true))
        timename_maxlen.maxlength(len(timename))

    return list_results

def create_output(args, from_date):    
    ''' this is actually the bit that calculates and outputs times'''

    if args.tozone:
        """Check if there is a desired to-time and adds it
        to dictionary"""

        #check if valid,or ask
        timezone_parsed = parseTimezone(args.tozone) 
        #we need the string, not the object
        timezone_to = str(timezone_parsed) 
        
        list_timezones.addEntry(timezone_to, "*** THIS the time you WANT ***")

    tz_maxlen = OutLen()
    timetrue_maxlen = OutLen()
    timename_maxlen = OutLen()

    list_results = translate_everything(from_date, tz_maxlen, timetrue_maxlen, timename_maxlen)
    
    total_space = tz_maxlen.len_part + timetrue_maxlen.len_part + timename_maxlen.len_part + 2
    half_space = int(total_space / 2)

# The initial decoration
#  
    print(f"+{'-' * half_space}Times{'-' * half_space}+")
    print(
            f"| {'Timezone:':{tz_maxlen.len_part + 1}} {'TIME:':<{timetrue_maxlen.len_part + 1}}"
            f"{'Comment:' :<{timename_maxlen.len_part}} |"
          )
    print(f"| {'':<{total_space + 1}} |")

# Generate list of results from the list generated by translate_everything()
# and print out
 
    for i in list_results:
        for a in i:
            tz = i[0]
            time_true = i[1]
            timename = i[2] 
        print(
            f"| {tz + ':':{tz_maxlen.len_part + 1}} {time_true:<{timetrue_maxlen.len_part + 1}}"
            f"{timename :<{timename_maxlen.len_part}} |"
            )

# The final decoration

    print(f"| {'':{total_space}}  |")
    print(f"+-{'-' * total_space}--+")


def main():

    args = input_parser()

    from_date = find_from_date(args)

    create_output(args, from_date)
    
if __name__ == '__main__':
    main() 
