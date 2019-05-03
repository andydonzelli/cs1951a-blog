import csv
import sqlite3
from argparse import ArgumentParser

''' SYNOPSIS
        python uber_csv_to_db.py [-d database] [-c csv file(s)]
'''
parser = ArgumentParser()
parser.add_argument("-d", "--database", dest="database", help="Input database")
parser.add_argument("-c", "--csv_file", nargs='+', dest="csvfile", help="Input .csv file")
args = parser.parse_args()

''' DESCRIPTION
        Creates uber table in a database from given .csv file
'''

db = sqlite3.connect(args.database)
c = db.cursor()

c.execute('DROP TABLE IF EXISTS "uber";')
c.execute('CREATE TABLE uber(date_time FLOAT, company STRING, lat FLOAT, long FLOAT);')
db.commit()

for file_csv in args.csvfile:
    csv_data = csv.reader(open(file_csv))
    next(csv_data)
    for row in csv_data:
        c.execute('''INSERT INTO uber
                     VALUES (?,?,?,?)''', row)
    db.commit()
c.close()
print ("Done")