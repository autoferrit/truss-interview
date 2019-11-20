#!/usr/bin/env python3

import csv
import sys
from datetime import datetime as dt

import pytz
from pytz import timezone

# read it as bytes so we can process through different encodings
content = sys.stdin.buffer.read()
# coerce it to utf-8, replacing invalid utf-8 sequences with the replace code
clean_content = content.decode('utf-8', errors='replace').splitlines()
# grab the header
header, *tail = clean_content
# read in the records
reader = csv.reader(tail)

def fix_timestamp(record):
    """Make sure timestamps are in EST/ISO8601 format"""
    pdt = timezone('US/Pacific')
    est = timezone('US/Eastern')
    from_fmt = '%m/%d/%y %I:%M:%S %p'

    # create datetime object
    date_obj = dt.strptime(record, from_fmt)
    # inject tz as PDT since there is no existing tz info
    date_obj.replace(tzinfo=pdt)

    # convert to EST in ISO8601 format
    return date_obj.astimezone(est).isoformat()

def fix_zip(record):
    """Make sure zipcode is proper format."""
    return str(record[:5].rjust(5, '0'))

def time_to_seconds(ts):
    """Convert H:M:S.m to total seconds."""
    hour, minute, second = [float(t) for t in ts.split(':')]

    return (hour * 60.0 + minute) * 60.0 + second

def write(text):
    """Write to stdout."""
    sys.stdout.write(f'{text}\n')

write(header)

for line in reader:
    # timestamp
    timestamp = fix_timestamp(line[0])

    # address
    address = f'"{line[1]}"'

    # zip
    zip = fix_zip(line[2])

    # full name
    fullname = f'"{line[3].upper()}"'

    # foo
    footime = time_to_seconds(line[4])

    # bar
    bartime = time_to_seconds(line[5])

    # total
    total = str(footime + bartime)

    # notes
    notes = f'"{line[7]}"'

    write(','.join([timestamp, address, zip, fullname, str(footime), str(bartime), total, notes]))

