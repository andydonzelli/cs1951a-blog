import pandas as pd
import glob
import time
import csv
import datetime
from argparse import ArgumentParser
import mysql.connector as mysql

#files = glob.glob('*.csv')
#df = pd.concat([pd.read_csv(f) for f in files],ignore_index=True)
parser = ArgumentParser()
parser.add_argument("-i", "--infile", dest="infile", help="Input .csv file")
parser.add_argument("-o", "--outfile", dest="outfile", help="Output .csv file")
args = parser.parse_args()

stripped_rows = []
with open(args.infile, 'r') as infile, open(args.outfile, 'w') as outfile:
    fieldnames = ['DATE_TIME', 'COMPANY', 'LAT', 'LONG']
    reader = csv.reader(infile)
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    #csv_reader = csv.reader(infile,delimiter=',')
    #stripped_rows.append(next(csv_reader))
    for row in reader:
        if row[0] == "tripduration":
            #print("header")
            continue
        else:
            dt_time = row[1]
            if '/' in dt_time:
                date_obj = datetime.datetime.strptime(
                dt_time, "%m/%d/%Y %H:%M:%S").timetuple()
            else:
                date_obj = datetime.datetime.strptime(
                dt_time, "%Y-%m-%d %H:%M:%S").timetuple()
            unix_date = time.mktime(date_obj)
            company = "citi"
            lat = row[5]
            long = row[6]
            entry = [unix_date,company,lat,long]
            writer.writerow({'DATE_TIME' : unix_date, 'COMPANY' : company, 'LAT' : lat, 'LONG' : long})
            #stripped_rows.append(entry)
            #print(entry)
    print("Processing finished")


"""
mydb = mysql.connect(host="localhost",user="root",password="Brown2020Troy")
mycursor = mydb.cursor()

#DELEE TABLE IF IT EXISTS
#mycursor.execute('DROP TABLE IF EXISTS rides')
mycursor.execute('DROP DATABASE IF EXISTS citi;')
mycursor.execute("CREATE DATABASE citi")

#need either create user with username and password beforehand or add execute for adding user
mydb = mysql.connect(host="localhost",user="root",password="password",database="citi")
mycursor = mydb.cursor()
mycursor.execute("CREATE TABLE rides (id int NOT NULL AUTO_INCREMENT PRIMARY KEY, date_time float, company varchar(255),lat float,longi float);")

#print(stripped_rows)
for row in stripped_rows[1:]:
    query = "INSERT INTO rides (date_time,company,lat,longi) VALUES (%s, %s, %s, %s)"
    values = (row[0],row[1],row[2],row[3])
    mycursor.execute(query,values)

#mycursor.close()
mydb.commit()
"""

#print(mycursor.rowcount,"records inserted")
