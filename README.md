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

You can enter the date directly in the CLI:

```shell
$ ./transtimezone.py 2022-10-28 10:00
```

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
Entered Time is: 2022:11:22 11:00:00 EST (-0500)
+----------------------------------------------------------------------------+
| Universal Coordinated Time:      2022:11:22 16:00:00 UTC   (+0000)         |
| Central European Time:           2022:11:22 17:00:00 CET   (+0100)         |
| New York Time:                   2022:11:22 11:00:00 EST   (-0500)         |
| Los Angeles Time:                2022:11:22 08:00:00 PST   (-0800)         |
| Cuba time:                       2022:11:22 11:00:00 CST   (-0500)         |
| Zulu time (or US Navy Time):     2022:11:22 16:00:00 UTC   (+0000)         |
| Sydney Time:                     2022:11:23 03:00:00 AEDT  (+1100)         |
| Tokyo (Japan) Time:              2022:11:23 01:00:00 JST   (+0900)         |
| Dubai (Gulf) time:               2022:11:22 20:00:00 +04   (+0400)         |
+----------------------------------------------------------------------------+

```

TODO: provide the option to add one or more timezones, maybe from a list, as the
corresponding BASH script currently allows
