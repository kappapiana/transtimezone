#!/usr/bin/env python3

from datetime import datetime 
from pytz import timezone
import argparse

# Define the most relevant timezones
translates_to = {"UTC": "Universal Coordinated Time",
                 "CET": "Central European Time",
                 "America/New_York": "New York Time",
                 "America/Los_Angeles": "Los Angeles Time",
                 "Australia/Sydney": "Sydney Time",
                 "Asia/Tokyo": "Tokyo (Japan) Time",
                 "Europe/London": "London time, (GMT or BST)"}


class DateExtractor:
    def __init__(self, date_time_string, format='%Y-%m-%d %H:%M:%S', tz="UTC"):
        self.date_time_string = date_time_string
        self.timezone = timezone(tz)
        self.utc_tz = timezone("UTC")

        if (type(self.date_time_string)) is str :
            self.date_obj = datetime.strptime(self.date_time_string, format)
                # print(f"**ERROR**: {self.date_time_string} is bad time or date")
        else:
            self.date_obj = self.date_time_string 

    def pass_dataobject(self):
        """pass data object to functions as UTC"""
        localized_date = self.timezone.localize(self.date_obj)
        utc_date = localized_date.astimezone(self.utc_tz)
        return utc_date 
        
def asker():
    try:
        input_tz = input('\nenter the timezone, if unsure, leave blank, we\'ll use UTC after three times :> ')
        tz = timezone(input_tz)
        return tz
    except:
        print("error asker")

def parseTimezone():

    if args.timezone:
        try: 
            tz = timezone(args.timezone)
        except: 
            print(f"{args.timezone} is not valid")
            try:
                tz = (asker())
            except:
                print("we quit")
    else: 
        tz = timezone(asker())

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
        # print(f"the entered date is {date}")

        input_day = date[0]
        if len(date) == 2:  # two elements are expected in the list
            input_hour = date[1]
        elif len(date) < 2:
            print(f"you have entered only {len(date)} "
                  f"elements\nwe use midnight")
        try:
            # print(input_day, input_hour)
            input_date = parsedate(input_day, input_hour)
            break
        except:
            print("you have entered a wrong data, see the reference it \
                   must be YYYY-MM-DD HH:MM")

    return input_date


# Parser from commandline:

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


def main():

    if args.date is None: # no input for date, use system date as UTC
        date_system = DateExtractor(datetime.utcnow())
        date_utc = DateExtractor.pass_dataobject(date_system)
        print(date_utc.strftime("%Y-%m-%d %H:%M %Z - %z"))

    else:
        tz = parseTimezone()
        
        try:
            date_time_string = (f"{args.date} {args.time}")
            insert_date = DateExtractor(date_time_string, "%Y-%m-%d %H:%M")
            from_date = insert_date.pass_dataobject()
            print(from_date)

        except:
            print("You have entered a wrong data, see the reference "
                "it must be YYYY-MM-DD HH:MM")
            
            date_time_string = typedate()
            insert_date = DateExtractor(date_time_string, "%Y-%m-%d %H:%M")
            from_date = insert_date.pass_dataobject()
            # print(from_date)

        
        

    
# Main function:

if __name__ == '__main__':
    main() 

# rubbish

# timezonez = timezone("CET")
# date_from = DateExtractor.pass_dataobject(date_system)
# print(date_from.astimezone(timezonez)) 


# insert_date = DateExtractor("2023-10-15 23:01", '%Y-%m-%d %H:%M', "CET")

# from_date = insert_date.pass_dataobject()

# todate_timezone = "CET"
# to_date_tz = timezone(todate_timezone)
# to_date = from_date.astimezone(to_date_tz)

# print(f"utc date is {from_date}")
# print(f"destination date is {to_date}")

# print(type(local_date))
# local_date.strftime("%Y-%m-%d %H:%M")
# print(datetime.strftime(DateExtractor.pass_dataobject(insert_date), '%Y-%m-%d %H:%M'))
# print(DateExtractor.extract_stringtime(insert_date))

