''' This script takes a CSV file that includes a timestamp column, and creates a new CSV file
which instead has a unix_time column.
'''

import datetime
import time
import csv
from argparse import ArgumentParser

''' SYNOPSIS
        python csv2csv_date_to_unix.py [-i input file] [-o output file]
'''
parser = ArgumentParser()
parser.add_argument("-i", "--infile", dest="infile", help="Input .csv file")
parser.add_argument("-o", "--outfile", dest="outfile", help="Output .csv file")
args = parser.parse_args()

''' DESCRIPTION 
        Converts timestamp to unix time
        Format:     8/1/14 8:08
'''
with open(args.infile, 'r') as infile, open(args.outfile, 'w') as outfile:
    fieldnames = ['DATE_TIME', 'COMPANY', 'LAT', 'LONG']
    reader = csv.DictReader(infile)
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in reader:
        stamp = row.get('DATE_TIME')
        date_obj = datetime.datetime.strptime(
            stamp, "%m/%d/%y %H:%M").timetuple()
        unix_date = time.mktime(date_obj)
        writer.writerow({'DATE_TIME' : unix_date, 'COMPANY' : row['COMPANY'], 'LAT' : row['LAT'], 'LONG' : row['LONG']})
print("DONE")
