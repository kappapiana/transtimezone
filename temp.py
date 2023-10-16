#!/usr/bin/env python3

from datetime import datetime 
from pytz import timezone

class DateExtractor:
    def __init__(self, date_time_string, format='%Y-%m-%d %H:%M:%S', tz="UTC"):
        self.date_time_string = date_time_string
        self.timezone = timezone(tz)

        if (type(self.date_time_string)) is str :
            self.date_obj = datetime.strptime(self.date_time_string, format)
        else:
            self.date_obj = self.date_time_string 
            
        print(type(self.date_obj))

    def pass_dataobject(self):
        """pass data object to functions"""
        
        date = self.timezone.localize(self.date_obj)
        
        return date

    def extract_stringtime(self):
        """A method to extract a date and time string for no particular reason"""

        extracted_date = datetime.date(self.date_obj)
        extracted_time = datetime.time(self.date_obj)

        try: 
            string_time = str(f"{extracted_date} {extracted_time} {self.timezone}")
        except:
            print("bugger")

        return string_time


date_system = DateExtractor(datetime.utcnow())
print(datetime.strftime(DateExtractor.pass_dataobject(date_system), '%Y-%m-%d %H:%M %Z'))

timezonez = timezone("CET")
date_from = DateExtractor.pass_dataobject(date_system)
print(date_from.astimezone(timezonez)) 


insert_date = DateExtractor("2023-10-15", '%Y-%m-%d', "Europe/Amsterdam")

from_date = insert_date.pass_dataobject()
print(datetime.time(from_date))

# print(type(local_date))
# local_date.strftime("%Y-%m-%d %H:%M")
# print(datetime.strftime(DateExtractor.pass_dataobject(insert_date), '%Y-%m-%d %H:%M'))
# print(DateExtractor.extract_stringtime(insert_date))

