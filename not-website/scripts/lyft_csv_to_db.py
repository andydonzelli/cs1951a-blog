''' Code modified from Matt's csv_to_db.py file to import Lyft data. '''

import csv
import sqlite3
from datetime import datetime
from argparse import ArgumentParser

''' SYNOPSIS
        python lyft_csv_to_db.py [-d database] [-c csv file(s)]
'''
parser = ArgumentParser()
parser.add_argument("-d", "--database", dest="database", help="Input database")
parser.add_argument("-c", "--csv_file", nargs='+', dest="csvfile", help="Input .csv file")
args = parser.parse_args()

''' DESCRIPTION
        Creates lyft table in a database from given .csv file
'''


# Converts a datetime stamp to unix time. If no string format is given, it expects
# a timestamp like: '9/4/2014 9:51'. 
def GetUnixTime(s, str_format='%m/%d/%Y %H:%M'):
    dt = datetime.strptime(row[0], str_format)   # Assumes format like
    secs_since_epoch = int(dt.strftime('%s'))
    return secs_since_epoch



db = sqlite3.connect(args.database)
c = db.cursor()

c.execute('DROP TABLE IF EXISTS "lyft_rides";')
c.execute('CREATE TABLE lyft_rides(date_time FLOAT, company STRING, lat FLOAT, long FLOAT);')
db.commit()

for file_csv in args.csvfile:
    csv_data = csv.reader(open(file_csv))
    next(csv_data)      # skip header
    for row in csv_data:
        unix_time = GetUnixTime(row[0])
        lat = row[1]
        long = row[2]
        c.execute("INSERT INTO lyft_rides VALUES ('%d','lyft','%s','%s')" % (unix_time,lat, long))
    db.commit()
c.close()
print('Done')