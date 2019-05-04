'''
Modify database, specifically rides table to have an additional column
of time binned by hour
'''
import sqlite3
import csv
from argparse import ArgumentParser

'''SYNOPSIS
python3 add_bin_time_to_rides -i [csv file] -d [db file] -t [table name]
table name should correspond to name of an existing weather table
'''

parser = ArgumentParser()
parser.add_argument("-i","--infile",dest="infile",help="Input .csv file")
parser.add_argument("-d", "--dbfile", dest="dbfile", help="Input .db file")
parser.add_argument("-t","--table_name",dest="tname",help="table name")
args = parser.parse_args()

conn = sqlite3.connect(args.dbfile)
c = conn.cursor()

query_to_sort_and_get_ride_time = 'SELECT DATE_TIME FROM rides ORDER BY DATE_TIME ASC LIMIT 1'
query_to_sort_and_get_weather_time = 'SELECT unix_time from {table} ORDER BY unix_time ASC LIMIT 1'.format(table=args.tname)

#c.execute(query_to_sort_and_get_ride_time)
#print(c.fetchone()[0])
#earliest_ride_time = float((c.fetchone())[0])

c.execute(query_to_sort_and_get_weather_time)
earliest_weather_time = float((c.fetchone())[0])
latest_weather_time = float(((c.execute('SELECT unix_time from {table} ORDER BY unix_time DESC LIMIT 1'.format
                    (table=args.tname))).fetchone())[0])
# print(earliest_weather_time,latest_weather_time)

#MODIFY EXISTING RIDE TABLE, ADD BIN_TIME COLUMN
'''
#ADD bin_time column to rides table
try:
    c.execute('ALTER TABLE rides ADD COLUMN bin_time integer');
except:
    print("Bin column already exists, skipping creating it")

with open(args.infile, 'r') as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        id = row["id"]
        time = float(row["date_time"])
        if time < earliest_weather_time or time > latest_weather_time:
            continue
        bin = int((time - earliest_weather_time)/3600)
        #print("bin",bin)
        c.execute('UPDATE rides set bin_time={value} where id={row_id}'.format(value=bin,row_id=id))
'''
c.execute("DROP TABLE IF EXISTS binned_rides")
c.execute("CREATE TABLE binned_rides \
        (id integer PRIMARY KEY, date_time float, \
        company string, lat float, lng float, zip_code string,bin_time integer)")

#CREATE NEW TABLE INSTEAD OF UPDATING OLD RIDES TABLE
with open(args.infile, 'r') as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        id = row["id"]
        time = float(row["date_time"])
        if time < earliest_weather_time or time > latest_weather_time:
            continue
        bin = int((time - earliest_weather_time)/3600)
        c.execute('INSERT INTO binned_rides (id,date_time,company,lat,lng,zip_code,bin_time) \
        VALUES (?,?,?,?,?,?,?);',
        (row['id'],row['date_time'],row['company'],row['lat'],row['lng'],row['zip_code'],bin))

print("FINISHED")
conn.commit()
conn.close()
