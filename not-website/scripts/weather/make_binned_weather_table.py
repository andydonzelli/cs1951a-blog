'''
Takes in a discretized weather csv and creates a weather table
binned on hourly time
'''
import sqlite3
import csv
from argparse import ArgumentParser


''' SYNOPSIS
        python3 make_binned_weather_table.py [-i input file] [-o database file] [-t table_name]
        NOTE: will create database file and table if they do not exist otherwise
        otherwise will add table to existing database file
'''

parser = ArgumentParser()
parser.add_argument("-i", "--infile", dest="infile", help="Input .csv file")
parser.add_argument("-d,","--dbfile", dest="dbfile", help="Output .db file")
parser.add_argument("-t","--table_name",dest="tname",help="table name")
args = parser.parse_args()

conn = sqlite3.connect(args.dbfile)
c = conn.cursor()
ofile = args.dbfile

c.execute("DROP TABLE IF EXISTS {name}".format(name=args.tname))
c.execute("CREATE TABLE {name} \
        (bin_time integer PRIMARY KEY, unix_time integer, \
        sunny integer, windy integer, rainy integer, cloudy integer, \
        temperature float);".format(name=args.tname))

with open(args.infile, 'r') as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        #print(row)
        c.execute('INSERT INTO {name}(bin_time,unix_time,sunny,windy,rainy,cloudy,temperature) \
        VALUES (?,?,?,?,?,?,?);'.format(name=args.tname),
        (row['bin_time'],row['unix_time'],row['sunny'],row['windy'],row['rainy'],row['cloudy'],
        row['temperature']))

conn.commit()
conn.close()
print("ALL DONE!")
