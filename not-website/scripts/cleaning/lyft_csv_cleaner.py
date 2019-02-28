''' Code modified from Matt's csv_to_db.py file to clean Lyft data. '''

import csv
import sys
from datetime import datetime

''' SYNOPSIS
    python lyft_csv_cleaner.py  dirty.csv  clean.csv
'''

''' DESCRIPTION
    Creates a new .csv file, having changed date into unix time, and adding company column
'''


# Converts a datetime stamp to unix time. If no string format is given, it expects
# a timestamp like: '9/4/2014 9:51'. 
def GetUnixTime(s, str_format='%m/%d/%Y %H:%M'):
    dt = datetime.strptime(s, str_format)   # Assumes format like
    secs_since_epoch = int(dt.strftime('%s'))
    return secs_since_epoch


def CreateCleanCsv(dirty_csv, clean_csv):
    with open(dirty_csv, 'r') as infile, open(clean_csv, 'w') as outfile:
        csv_data = csv.reader(infile)
        next(csv_data)  # skip header
        writer = csv.DictWriter(outfile, fieldnames=[
                                'DATE_TIME', 'COMPANY', 'LAT', 'LONG'])
        writer.writeheader()
        for row in csv_data:
            unix_timestamp = GetUnixTime(row[0])
            company = "Lyft"
            lat = row[1]
            long = row[2]
            writer.writerow({   'DATE_TIME': unix_timestamp,
                                'COMPANY': company,
                                'LAT': lat,
                                'LONG': long})

    print('Finished writing to clean CSV.')

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("ERROR: Expected two arguments: dirty.csv clean.csv")
        print("ABORTING")
        sys.exit(1)
    
    CreateCleanCsv(sys.argv[1], sys.argv[2])