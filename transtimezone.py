#!/usr/bin/env python3

# SPDX-FileCopyrightText: Carlo Piana
#
# SPDX-License-Identifier: Apache-2.0

from datetime import datetime 
# from pytz import common_timezones
from pytz import timezone, UnknownTimeZoneError
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
    """Function that asks for timezones and proposes fuzzy matches."""

    count = 0
    max_attempts = 3
    
    while count < max_attempts:
        try:
            # Detect user's local timezone for prompt suggestion
            local_tz = detect_local_timezone()
            
            input_tz = input(f"\nEnter timezone (or leave blank for {local_tz}): > ").strip()
            
            # If user provides empty input, use detected local timezone
            if not input_tz:
                print(f"Using {local_tz} as default")
                return timezone(local_tz)
            
            # Try exact match first
            try:
                return timezone(input_tz)
            except:
                pass
            
            # No exact match, fuzzy search for alternatives
            matches = fuzzy_timezone_match(input_tz)
            
            if matches:
                print(f"\nNo exact match for '{input_tz}'. Did you mean one of these?")
                print("Showing top 10 suggestions:\n")
                
                display_names = {}
                for tz in all_timezones:
                    if tz.lower() in [m.lower() for m in matches]:
                        name_parts = tz.split('/')[-1].replace('_', ' ')
                        display_names[tz] = name_parts
                
                for idx, tz in enumerate(matches, 1):
                    print(f"  {idx}. {tz} ({display_names.get(tz, tz).title()})" if tz in display_names else f"  {idx}. {tz}")
                
                # Ask user to select from suggestions
                while True:
                    selection = input(f"\nEnter number (1-{len(matches)}) or try again: ").strip()
                    try:
                        sel_idx = int(selection) - 1
                        if 0 <= sel_idx < len(matches):
                            return timezone(matches[sel_idx])
                        else:
                            print(f"Please enter a number between 1 and {len(matches)}")
                    except ValueError:
                        # User wants to retry their input
                        break
            
            print(f"\nCould not find timezone matching '{input_tz}'")
            count += 1
            if count < max_attempts:
                print(f"Attempt {count} of {max_attempts}\n")
        
        except KeyboardInterrupt:
            print("\nCancelling... Using UTC")
            return timezone('UTC')
    
    # If user failed all attempts, default to UTC with message
    print(f"\nUnable to parse timezone after {max_attempts} attempts. Using UTC.")
    return timezone('UTC')

def parseTimezone(input_tz, allow_fuzzy=True):
    """Parse timezone with optional fuzzy matching.
    
    Args:
        input_tz: Timezone string or identifier
        allow_fuzzy: If True, attempt fuzzy matching on failure
    
    Returns:
        pytz timezone object
    
    Behaviors:
        - Exact match returns immediately
        - Fuzzy matching searches by city/region name and common abbreviations
        - Provides helpful output when no match found
    """
    if not input_tz:
        return timezone('UTC')
    
    # Try exact match first
    try:
        return timezone(input_tz)
    except UnknownTimeZoneError:
        pass
    
    # Attempt fuzzy matching if enabled
    if allow_fuzzy:
        matches = fuzzy_timezone_match(input_tz)
        
        if len(matches) == 1:
            print(f"Using best match for '{input_tz}': {matches[0]}")
            return timezone(matches[0])
        elif len(matches) > 1:
            # Multiple matches - list them and ask user to select
            print(f"\nMultiple matches for '{input_tz}', please choose one:")
            for idx, tz in enumerate(matches, 1):
                print(f"  {idx}. {tz}")
            
            while True:
                try:
                    selection = input(f"\nEnter number (1-{len(matches)}): ").strip()
                    sel_idx = int(selection) - 1
                    if 0 <= sel_idx < len(matches):
                        return timezone(matches[sel_idx])
                    else:
                        print(f"Please enter a number between 1 and {len(matches)}")
                except ValueError:
                    print("Invalid input. Please enter a number.")
    
    # No match found
    matches = fuzzy_timezone_match(input_tz)
    
    if not matches:
        raise ValueError(f"No matching timezone found for '{input_tz}' after fuzzy search")
    
    print(f"\nNo exact match for '{input_tz}'. Closest suggestions:")
    for idx, tz in enumerate(matches[:5], 1):
        print(f"  {idx}. {tz}")
    
    raise ValueError(f"'{input_tz}' is not a valid timezone identifier")

def regmatch(input):
    '''Searches for a partial match in the list of pytz.timezone
    and proposes the ones relevant'''

    pattern = r'.*'+input+'.*'
    results = []
    
    for i in all_timezones:
        match = re.findall(pattern, i, re.IGNORECASE)
        if match :
            results.append(i)
                        
    return results


def fuzzy_timezone_match(search_text):
    """Fuzzy match timezone search text against pytz timezones.
    
    Handles: partial matches, case-insensitivity, common abbreviations, 
             city names extracted from timezone IDs.
    
    Args:
        search_text: User's timezone input (e.g., "new york", "nyc", "sydney")
    
    Returns:
        List of best matching timezone identifiers, ranked by relevance
    """
    if not search_text:
        return []
    
    search_lower = search_text.lower().strip()
    results = {}
    
    # Build a ranking score for each timezone
    for tz in all_timezones:
        name_parts = tz.split('/')  # e.g., ['America', 'New_York']
        
        # Score components:
        base_score = 0
        
        # Exact substring match (case-insensitive) - highest priority
        if search_lower in tz.lower():
            base_score += 100
        
        # Match against the last part of timezone (city/region name)
        for part in reversed(name_parts):
            if search_lower == part.lower():
                base_score += 100
            elif search_lower in part.lower():
                base_score += 50
        
        # Handle common abbreviations and slang
        abbr_map = {
            'nyc': ['america/new_york', 'us/eastern'],
            'ny': ['america/new_york'],
            'la': ['america/los_angeles', 'pacific/chatham'],
            'sf': ['america/los_angeles'],
            'sydney': ['australia/sydney'],
            'london': ['europe/london'],
            'tokyo': ['asia/tokyo'],
            'paris': ['europe/paris'],
            'berlin': ['europe/berlin'],
            'moscow': ['europe/moscow'],
            'dubai': ['asia/dubai'],
            'singapore': ['asia/singapore'],
            'hongkong': [' asia/hong_kong', 'asia/macau'],
            'hk': ['asia/hong_kong'],
            'abeja': ['europe/london'],
            'cet': ['utc+1', 'utc-2'],
            'est': ['utc-5', 'america/new_york', 'america/toronto'],
            'pst': ['utc-8', 'america/los_angeles'],
            'pacific time': ['america/los_angeles'],
            'california': ['america/los_angeles'],
        }
        
        if search_lower in abbr_map:
            for mapped_tz in abbr_map[search_lower]:
                if mapped_tz and mapped_tz.strip():  # Only non-empty entries
                    mapped_tz_stripped = mapped_tz.strip().lower()
                    if mapped_tz_stripped == tz.lower():
                        base_score += 90
                        
        # Additional heuristic for "LA" specifically targeting Los Angeles
        if search_lower == 'la':
            if 'los_angeles' in tz.lower():
                base_score += 150
        
        # Fuzzy matching using character overlap
        tz_display = name_parts[-1].replace('_', ' ').lower()
        search_words = set(search_lower.split())
        tz_words = set(tz_display.split())
        
        if search_words & tz_words:  # Has common words
            base_score += 20
        
        # Normalize underscores and spaces for matching
        tz_normalized = tz.lower().replace('_', ' ')
        if ' '.join(search_lower.split()) in tz_normalized:
            base_score += 30
        
        # Exact match on city name (case-sensitive)
        if any(search_text == part for part in name_parts):
            base_score += 150
        
        if base_score > 0:
            results[tz] = base_score
    
    # Sort by score descending
    sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)
    
    # Limit to top 10 results
    return [tz for tz, _ in sorted_results[:15]]
    
def parse_datetime_flexible(date_input, time_input=None):
    """Parse date/time with multiple format support.
    
    Accepts formats:
    - "HH:MM" or "H:MM" → uses current date
    - "HH:MM AM/PM" → uses current date 
    - YYYY-MM-DD HH:MM (ISO format)
    - MM/DD/YYYY HH:MM or MM/DD/YYYY  
    - DD Mon YYYY HH:MM with AM/PM
    
    Handles: single-digit hours, AM/PM, date/time only input
    """
    combined_input = None
    
    # Combine if needed
    if time_input and ' at ' not in str(date_input).lower():
        combined_input = f"{date_input} {time_input}"
    
    # Try parsing the combined input first (if provided)
    if combined_input:
        try:
            return parse_datetime_flexible(combined_input, None)
        except ValueError:
            pass
    
    date_str = str(date_input).strip()
    
    # Handle "H AM/PM" or "H PM" style format (e.g., "9am", "3pm")
    am_pm_pattern = r'^(\d{1,2})\s*(am|pm)$'
    ampm_match = re.match(am_pm_pattern, date_str, re.IGNORECASE)
    if ampm_match:
        try:
            hour = int(ampm_match.group(1))
            ampm_lower = ampm_match.group(2).lower()
            
            # Normalize to lowercase for comparison (am or pm)
            if ampm_lower.startswith('p'):
                if hour != 12:
                    hour += 12
            elif ampm_lower.startswith('a'):
                if hour == 12:
                    hour = 0
            
            now = datetime.now()
            return now.replace(hour=hour, minute=0, second=0, microsecond=0)
        except (ValueError, TypeError):
            pass
    
    # Handle HH:MM or H:MM format with optional AM/PM
    time_pattern = r'^(\d{1,2}):?(\d{2})\s*(am|pm)?$'
    simple_match = re.match(time_pattern, date_str, re.IGNORECASE)
    
    if simple_match:
        try:
            hour = int(simple_match.group(1))
            minute = int(simple_match.group(2)) if simple_match.group(2) else 0
            
            ampm_part = simple_match.group(3)
            if ampm_part:
                ampm_lower = ampm_part.lower()
                # Normalize to lowercase for comparison (am or pm)
                if ampm_lower.startswith('p'):
                    if hour != 12:
                        hour += 12
                elif ampm_lower.startswith('a'):
                    if hour == 12:
                        hour = 0
            
            now = datetime.now()
            return now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        except (ValueError, TypeError):
            pass
    
    formats_to_try = [
        ("%Y-%m-%d %H:%M", "ISO format (YYYY-MM-DD HH:MM)"),
        ("%Y-%m-%d %H:%M:%S", "ISO with seconds"),
        ("%Y-%m-%d", "Date only (defaults to 00:00)"),
        ("%m/%d/%Y %H:%M", "US format (MM/DD/YYYY HH:MM)"),
        ("%m/%d/%Y", "US date only"),
        ("%d %b %Y %H:%M", "European (DD Mon YYYY HH:MM)"),
        ("%d %b %Y", "European date only"),
    ]
    
    for fmt, desc in formats_to_try:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    
    # Try AM/PM formats with case variations and "at" keyword
    am_pm_formats = [
        "%b %d, %Y at %-I:%M%p",
        "%b %d, %Y %-I:%M%p",
        "%b %d, %Y at %-I%M%p",
        "%b %d, %Y %-I%M%p",
    ]
    
    for fmt in am_pm_formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    
    # Try flexible parsing for AM/PM variants like "3pm", "3:00pm"
    am_pm_pattern = r'.{0,1}\s*(\d{1,2}):?(\d{2})?\s*([ap]m)'
    am_match = re.search(am_pm_pattern, date_str, re.IGNORECASE)
    if am_match:
        hour_part = date_str.replace("at", "").strip()
        try:
            hour, minute = am_match.group(1), am_match.group(2)
            
            # Extract the rest of the date before the time
            before_time = hour_part[:am_match.start()]
            after_time = hour_part[am_match.end():]
            
            for fmt in ["%b %d, %Y", "%Y-%m-%d", "%m/%d/%Y"]:
                try:
                    base_dt = datetime.strptime(before_time.strip(), fmt)
                    # Normalize to 24-hour format
                    am_or_pm = am_match.group(3).lower()[:1]
                    hour_int = int(hour_part.lstrip(re.search(r'\.*\s*(\d+)\s*\...', before_time).group().split()[0]) if re.search(r'\d+', before_time) else hour or 12)
                    hour_int = int(am_match.group(1)) if am_match.group(1) else 12
                    
                    if am_or_pm == 'p' and hour_int != 12:
                        hour_int += 12
                    elif am_or_pm == 'a' and hour_int == 12:
                        hour_int = 0
                    
                    return base_dt.replace(hour=hour_int, minute=int(minute or 0))
                except ValueError:
                    continue
        
        except (AttributeError, TypeError):
            pass
    
    # Try parsing "3pm" at end of string
    end_am_pm_match = re.match(r'(.+?)\s*(\d{1,2}):?(\d{2})?\s*([ap]m)\s*$', date_str, re.IGNORECASE)
    if end_am_pm_match:
        base_str, hour, minute, ampm = end_am_pm_match.groups()
        try:
            for fmt in ["%b %d, %Y", "%Y-%m-%d", "%m/%d/%Y"]:
                try:
                    base_dt = datetime.strptime(base_str.strip(), fmt)
                    hour_int = int(hour or 12)
                    if ampm.lower() == 'p' and hour_int != 12:
                        hour_int += 12
                    elif ampm.lower() == 'a' and hour_int == 12:
                        hour_int = 0
                    return base_dt.replace(hour=hour_int, minute=int(minute or 0))
                except ValueError:
                    continue
        except (ValueError, AttributeError):
            pass
    
    # Try parsing "at 3pm" format within the string
    at_am_pm_match = re.search(r'\sat\s*(\d{1,2}):?(\d{2})?\s*([ap]m)\s*$', date_str, re.IGNORECASE)
    if at_am_pm_match:
        before_time = re.sub(r'\sat\s*\d+:?\d*\s*[ap]m\s*$', '', date_str, flags=re.IGNORECASE).strip()
        hour, minute, ampm = at_am_pm_match.groups()
        try:
            for fmt in ["%b %d, %Y", "%Y-%m-%d", "%m/%d/%Y"]:
                try:
                    base_dt = datetime.strptime(before_time, fmt)
                    hour_int = int(hour or 12)
                    if ampm.lower() == 'p' and hour_int != 12:
                        hour_int += 12
                    elif ampm.lower() == 'a' and hour_int == 12:
                        hour_int = 0
                    return base_dt.replace(hour=hour_int, minute=int(minute or 0))
                except ValueError:
                    continue
        except (ValueError, AttributeError):
            pass
    
    raise ValueError(f"Unable to parse date/time from '{date_input}' with time component '{time_input}'. Try formats like '2023-10-28 15:00' or 'Oct 28, 2023 at 3pm'.")

def typedate():
    """Function to enter date/time interactively with flexible format support."""

    while True:
        user_input = input("enter the date/time (e.g., 2023-10-28 15:00, or just 09:00 for today): > ").strip()

        if not user_input:
            print("Using current time")
            return datetime.now()

        try:
            input_date = parse_datetime_flexible(user_input)
            print(f"You have entered {input_date}")
            return input_date
        except ValueError as e:
            print(f"\nError: {e}\n")

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

def detect_local_timezone():
    """Detect system's local timezone using multiple methods.
    
    Tries in order:
    1. /etc/localtime symlink on Unix systems
    2. /etc/timezone file (Linux)
    3. TZ environment variable
    4. Fallback to UTC
    """
    import os
    import platform
    
    # Method 1: Check /etc/localtime symlink path
    if os.path.exists('/etc/localtime') and os.path.islink('/etc/localtime'):
        link_target = os.readlink('/etc/localtime')
        if 'zoneinfo' in link_target:
            parts = link_target.split('zoneinfo/')
            if len(parts) > 1:
                return parts[1]
    
    # Method 2: Check /etc/timezone file (Linux standard)
    if os.path.exists('/etc/timezone'):
        with open('/etc/timezone', 'r') as f:
            tz = f.read().strip()
            try:
                timezone(tz)  # Verify it's valid
                return tz
            except UnknownTimeZoneError:
                pass
    
    # Method 3: Check TZ environment variable
    tz_env = os.environ.get('TZ')
    if tz_env:
        try:
            timezone(tz_env)  # Verify it's valid
            return tz_env
        except UnknownTimeZoneError:
            pass
    
    # Method 4: Try platform-specific detection for Mac OS X
    if platform.system() == 'Darwin':
        try:
            import subprocess
            result = subprocess.run(
                ['systemsetup', '-getlocaltimezone'],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                parts = result.stdout.strip().split(':')
                if len(parts) >= 2:
                    tz_name = ':'.join(parts[1:]).strip()
                    try:
                        timezone(tz_name)
                        return tz_name
                    except UnknownTimeZoneError:
                        pass
        except Exception:
            pass
    
    # Ultimate fallback: UTC with warning
    print("Warning: Could not detect local timezone, using UTC as default")
    return "UTC"

def find_from_date(args):
    '''This finds the date from which the computation is made
    '''
    
    # Detect and use local timezone if no explicit one provided
    tz_local = detect_local_timezone()
    
    # Parse timezone first (always needed for DateExtractor)
    tz = None
    if args.timezone:
        try:
            tz = parseTimezone(args.timezone)
            print(f"Timezone is {tz}")
        except ValueError as e:
            print(f"Warning: {e}")
    
    # Check if user provided time-only without date (e.g., just "09:00")
    is_time_only = args.date and re.match(r'(\d{1,2}):?(\d{2})?\s*(am|pm)?$', args.date, re.IGNORECASE)
    
    if args.date is None:
        # No date provided, use current datetime
        from_date = datetime.now().replace(second=0, microsecond=0)
        
    elif is_time_only:
        # Time-only input like "09:00" - parse time and use current date
        now = datetime.now().replace(second=0, microsecond=0)
        if args.date:
            time_match = re.match(r'(\d{1,2}):?(\d{2})?\s*(am|pm)?$', args.date, re.IGNORECASE)
            if time_match:
                hour = int(time_match.group(1))
                minute = int(time_match.group(2)) if time_match.group(2) else 0
                
                ampm = time_match.group(3)
                if ampm:
                    ampm_lower = ampm.lower()
                    if ampm_lower == 'p' and hour != 12:
                        hour += 12
                    elif ampm_lower == 'a' and hour == 12:
                        hour = 0
                
                if 0 <= hour <= 23:
                    from_date = now.replace(hour=hour, minute=minute)
                    # Create DateExtractor with timezone if provided
                    if tz:
                        insert_date = DateExtractor(from_date, "%Y-%m-%d %H:%M", tz)
                        from_date = insert_date.pass_dataobject()
                else:
                    from_date = now
        else:
            from_date = now
            
    else:
        # Full date input like "2023-10-28" or "2023-10-28 15:00"
        try:
            # Check if date already contains time (e.g., "2023-10-28 15:00")
            if args.time and args.time != "00:00":
                date_time_string = f"{args.date} {args.time}"
            else:
                # Use flexible parser on just the date part
                from datetime import datetime as dt
                parsed = parse_datetime_flexible(args.date)
                insert_date = DateExtractor(parsed, "%Y-%m-%d %H:%M", tz if tz else "UTC")
                from_date = insert_date.pass_dataobject()
                return from_date
            
            insert_date = DateExtractor(date_time_string, "%Y-%m-%d %H:%M", tz if tz else "UTC")
            from_date = insert_date.pass_dataobject()
        except:
            print("You have entered a wrong data format")
            date_time_string = typedate()
            if tz:
                insert_date = DateExtractor(date_time_string, "%Y-%m-%d %H:%M", tz)
            else:
                insert_date = DateExtractor(date_time_string, "%Y-%m-%d %H:%M", "UTC")
            from_date = insert_date.pass_dataobject()
    
    return from_date

def translate_everything(from_date, tz_maxlen, timetrue_maxlen, timename_maxlen, args):

    list_results = []
    # instantiate class
    list_timezones = TimezoneChooser()
    
    if args.tozone:
        """Check if there is a desired to-time and adds it
        to dictionary"""

        #check if valid,or ask
        timezone_parsed = parseTimezone(args.tozone) 
        #we need the string, not the object
        timezone_to = str(timezone_parsed) 
        
        list_timezones.addEntry(timezone_to, "*** THIS the time you WANT ***")

    for tz, timename in list_timezones.dictionary.items():
        translated_to = from_date.astimezone(timezone(tz))
        time_true = translated_to.strftime("%Y-%m-%d %H:%M %Z ")
        list_results.append([tz, time_true, timename])

        tz_maxlen.maxlength(len(tz))
        timetrue_maxlen.maxlength(len(time_true))
        timename_maxlen.maxlength(len(timename))

    return list_results

def create_output(args, from_date):    
    ''' this is actually the bit that calculates and outputs times'''

    tz_maxlen = OutLen()
    timetrue_maxlen = OutLen()
    timename_maxlen = OutLen()

    list_results = translate_everything(
                                        from_date, tz_maxlen, timetrue_maxlen, \
                                        timename_maxlen, args
                                        )
    
    total_space = int(tz_maxlen.len_part + timetrue_maxlen.len_part + timename_maxlen.len_part + 2)
    half_space = int(total_space / 2 - 2)
    other_space = int(total_space - half_space - 4)

# The initial decoration
#  
    title = "List of results"
    print(f"+{title:-^{total_space + 3}}+")
    # print(f"| {'':<{total_space + 1}} |")
    print(
            f"| {'Timezone:':{tz_maxlen.len_part + 1}} {'TIME:':<{timetrue_maxlen.len_part + 1}}"
            f"{'Comment:' :<{timename_maxlen.len_part}} |"
          )

# Generate list of results from the list generated by translate_everything()
# and print out
 
    for i in list_results:
        tz, time_true, timename = i
        print(
            f"| {tz + ':':{tz_maxlen.len_part + 1}} {time_true:<{timetrue_maxlen.len_part + 1}}"
            f"{timename :<{timename_maxlen.len_part}} |"
            )

# The final decoration

    # print(f"| {'':{total_space}}  |")
    print(f"+-{'-' * total_space}--+")


def main():

    args = input_parser()

    from_date = find_from_date(args)

    create_output(args, from_date)
    
if __name__ == '__main__':
    main() 
