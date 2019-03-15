import csv
import sqlite3
from argparse import ArgumentParser
import subprocess

''' SYNOPSIS
        python3 csv_to_sqlite.py -c csv_file -d db_file
'''
parser = ArgumentParser()
requiredNamed = parser.add_argument_group('Required (named) arguments')
requiredNamed.add_argument("-d", "--database", dest="database", help="Database file", required=True)
requiredNamed.add_argument("-c", "--csv_file", dest="csvfile", help="Source .csv file", required=True)
args = parser.parse_args()


''' DESCRIPTION
        Creates "core" table in the SQLite database file, and populates it with the data
        in the CSV file.
'''

# Use `wc` (with Bash) to obtain number of lines in file.
def GetNumRows(file):
    p = subprocess.Popen("wc -l core_master.csv".split(), stdout=subprocess.PIPE)
    output, _ = p.communicate()
    num_rows = int(output.split()[0])
    return num_rows - 2  # Ignore headers and final newline.



# Connect to DB file, drop table if exists, create new table with our headers.
db = sqlite3.connect(args.database)
c = db.cursor()
c.execute('DROP TABLE IF EXISTS "rides";')
c.execute('CREATE TABLE rides(id INT PRIMARY KEY, date_time FLOAT, company STRING, lat FLOAT, long FLOAT);')
db.commit()

# Add each row of the CSV to the DB.
id_count = 0
num_rows = GetNumRows(args.csvfile)
print("CSV file contains %d rows... this may take a while!")
print("Note: this thing takes a while to start up, probably because of memory allocation."
      " If you don't see anything else within 2 minutes, you can start being concerned.")

csv_data = csv.reader(open(args.csvfile))
next(csv_data)  # Skip header.
for row in csv_data:
    c.execute('''INSERT INTO rides
                    VALUES (?,?,?,?,?)''', [str(id_count)] + row)
    id_count += 1
    if id_count % 1000000 == 0:
        print("...Processed [%d/%d] rows" % (id_count, num_rows))
db.commit()
c.close()

print ("Done")