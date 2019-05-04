import pandas as pd
import sqlite3
import sys
from argparse import ArgumentParser


def main():
    ''' SYNOPSIS
        python create_locations_table [-d core_rides.db] [-c nyc_zip_code_info.csv]
    '''
    parser = ArgumentParser()
    parser.add_argument("-d", "--db_file", dest="core_rides_db", help="core_rides.db file", required=True)
    parser.add_argument("-c", "--csv_file", dest="nyc_zip_code_info_csv", help="nyc_zip_code_info.csv file", required=True)
    if len(sys.argv) < 2:
        parser.print_usage()
        sys.exit(1)
    args = parser.parse_args()

    conn = sqlite3.connect(args.core_rides_db)
    df = pd.read_csv(args.nyc_zip_code_info_csv)
    df['NEIGHBOURHOOD'] = df['NEIGHBOURHOOD'].str.strip() #Trim's whitespace in column
    df.to_sql('locations', conn, if_exists='append', index=False)
    conn.close()


if __name__ == '__main__':
    main()