import csv
import sqlite3
from datetime import datetime
from argparse import ArgumentParser


def main():
    ''' SYNOPSIS
        python clean_yellow_taxi_csvs.py [-c csv file(s)]
    '''
    parser = ArgumentParser()
    parser.add_argument("-c", "--csv_file", nargs='+',
                        dest="csvfile", help="Input .csv file")
    args = parser.parse_args()

    ''' DESCRIPTION
            Cleans yellow taxi csvs
    '''

    for file_csv in args.csvfile:
        file_csv_cleaned = file_csv.replace('.csv', '_cleaned.csv')
        with open(file_csv, 'r') as infile, open(file_csv_cleaned, 'w') as outfile:
            csv_data = csv.reader(infile)
            next(csv_data)  # skip header
            next(csv_data)  # skip missing row
            writer = csv.DictWriter(outfile, fieldnames=[
                                    'DATE_TIME', 'COMPANY', 'LAT', 'LONG'])
            writer.writeheader()
            for row in csv_data:
                pickup_time_str = row[1]
                unix_timestamp = datetime.strptime(
                    pickup_time_str, "%Y-%m-%d %H:%M:%S").timestamp()
                company = "yellow_taxi"
                lat = row[6]
                long = row[5]
                if lat != "0":
                    writer.writerow({'DATE_TIME': unix_timestamp,
                                     'COMPANY': company, 'LAT': lat, 'LONG': long})
        print(f"Cleaned csv file: {file_csv} Output: {file_csv_cleaned}")
    print("Done")


if __name__ == '__main__':
    main()
