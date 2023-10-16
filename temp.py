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
            try:
                self.date_obj = datetime.strptime(self.date_time_string, format)
            except:
                print(f"**ERROR**: {self.date_time_string} is bad time or date")
        else:
                self.date_obj = self.date_time_string 

    def pass_dataobject(self):
        """pass data object to functions as UTC"""
        try:
            localized_date = self.timezone.localize(self.date_obj)
            utc_date = localized_date.astimezone(self.utc_tz)
            self.utc_tz = utc_date
            return utc_date 
        except:
            print("nothing to do")   
            
    def extract_stringtime(self):
        """A method to extract a date and time string for no particular reason"""

        extracted_date = datetime.date(self.utc_date)
        extracted_time = datetime.time(self.utc_date)

        try: 
            string_time = str(f"{extracted_date} {extracted_time} {self.timezone}")
        except:
            print("bugger")

        return string_time


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

    if args.date is None:
        date_system = DateExtractor(datetime.utcnow())
        date_utc = DateExtractor.pass_dataobject(date_system)
        print(date_utc.strftime("%Y-%m-%d %H:%M %Z - %z"))

    else: 
        pass
    

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

