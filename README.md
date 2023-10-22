<!--
SPDX-FileCopyrightText: 2022 Carlo Piana

SPDX-License-Identifier: CC0-1.0
-->

[![REUSE status](https://api.reuse.software/badge/github.com/kappapiana/transtimezone)](https://api.reuse.software/info/github.com/kappapiana/transtimezone)

# transtimezone

Quick translate times between timezones

The basic idea is to have a quick way to find out what time it is in different
places of the world when announcing, for instance, a virtual meeting. Many
people say stupid things like "let's meet 3pm Pacific", which should rather be
announced "let's meet at 15:00 PST (UTC-8)". Trying to educate to use a more
sensible way to announce time, short of all using UTC (and I wonder why this is
not the default option), it is gracious to at least announce the local time for
some countries/cities. The one provided here are only an example.

With this script you can enter a sensible date and have multiple dates in
different timezones.

If you just want to know what time it is in different timezones, just go for 

```shell
./transtimezone.py 2022-10-28 10:00
```

You can enter the date directly in the CLI, using the `YYYY-MM-DD` convention (as
you always should):

```shell
$ ./transtimezone.py
```

And it will take the system date 

It will ask the timezone.

Using the `-t` or `--timezone` flag, you can specify the timezone right from the
start:

```shell
$ ./transtimezone.py 2022-10-28 10:00 -t CET

```

If you just want to use your current one, omit the flag and avoid entering
anything when prompted: the script will use the local timezone as obtained from
the system.

If you omit any parameter, the program will ask to enter the date and time
string. Remeber that it must be entered in the ISO format `YYYY-MM-DD HH:MM`.

At the end, you will have a list of times

```
Entered date is 2023-10-22 13:29 UTC - +0000
+------------------------------------- Times----------------------------------------+
| Timezone:                 TIME:                     Comment:                      |
|                                                                                   |
| CET:                      2023:10:22 15:29:28 CEST  Central European Time         |
| America/New_York:         2023:10:22 09:29:28 EDT   New York Time                 |
| America/Los_Angeles:      2023:10:22 06:29:28 PDT   Los Angeles Time              |
| Australia/Sydney:         2023:10:23 00:29:28 AEDT  Sydney Time                   |
| Asia/Tokyo:               2023:10:22 22:29:28 JST   Tokyo (Japan) Time            |
| Europe/London:            2023:10:22 14:29:28 BST   London time, (GMT or BST)     |
| UTC:                      2023:10:22 13:29:28 UTC   Universal Time                |
| America/Chicago:          2023:10:22 08:29:28 CDT   Chicago Time (lakes)          |
| America/Anchorage:        2023:10:22 05:29:28 AKDT  Alaska Time                   |
|                                                                                   |
+-----------------------------------------------------------------------------------+

```
You have the option to request a specific timezone to which the date is translated
in addition to the default ones. Just enter it with the `-o` flag 

You can also add more timezones-to by adding timezone and a comment in
`listzones.asc`. See current example.
