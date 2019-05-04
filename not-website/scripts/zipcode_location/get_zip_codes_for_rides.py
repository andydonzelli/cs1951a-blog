import csv
import sqlite3
import sys
from argparse import ArgumentParser
import traceback
from uszipcode import Zipcode
from uszipcode import SearchEngine
import time
import os

search = SearchEngine(simple_zipcode=True)

def main():
    ''' SYNOPSIS
        python get_zip_codes_for_rides.py [-d core_rides.db]

        Assumes a table "new_rides" exists with the following schema in the database:
        CREATE TABLE IF NOT EXISTS "new_rides" (
          "ID" INT PRIMARY KEY,
          "DATE_TIME" FLOAT,
          "COMPANY" STRING,
          "LAT" FLOAT,
          "LNG" FLOAT,
          "ZIP_CODE" STRING,
          FOREIGN KEY("ZIP_CODE") REFERENCES locations("ZIP_CODE")
        );
    '''
    parser = ArgumentParser()
    parser.add_argument("-d", "--db_file", dest="core_rides_db",
                        help="core_rides_v2.db file", required=True)
    if len(sys.argv) < 2:
        parser.print_usage()
        sys.exit(1)
    args = parser.parse_args()
 
    # exact zips that are in locations table, pre allocated into a set for speed purposes
    # nyc_zips = {"10001", "10002", "10003", "10004", "10005", "10006", "10007", "10009", "10010", "10011", "10012", "10013", "10014",
    #             "10016", "10017", "10018", "10019", "10020", "10021", "10022", "10023", "10024", "10025", "10026", "10027", "10028",
    #             "10029", "10030", "10031", "10032", "10033", "10034", "10035", "10036", "10037", "10038", "10039", "10040", "10044",
    #             "10065", "10075", "10128", "10280", "10301", "10302", "10303", "10304", "10305", "10306", "10307", "10308", "10309",
    #             "10310", "10312", "10314", "10451", "10452", "10453", "10454", "10455", "10456", "10457", "10458", "10459", "10460",
    #             "10461", "10462", "10463", "10464", "10465", "10466", "10467", "10468", "10469", "10470", "10471", "10472", "10473",
    #             "10474", "10475", "11004", "11005", "11101", "11102", "11103", "11104", "11105", "11106", "11201", "11203", "11204",
    #             "11205", "11206", "11207", "11208", "11209", "11210", "11211", "11212", "11213", "11214", "11215", "11216", "11217",
    #             "11218", "11219", "11220", "11221", "11222", "11223", "11224", "11225", "11226", "11228", "11229", "11230", "11231",
    #             "11232", "11233", "11234", "11235", "11236", "11237", "11238", "11239", "11354", "11355", "11356", "11357", "11358",
    #             "11359", "11360", "11361", "11362", "11363", "11364", "11365", "11366", "11367", "11368", "11369", "11370", "11372",
    #             "11373", "11374", "11375", "11377", "11378", "11379", "11385", "11411", "11412", "11413", "11414", "11415", "11416",
    #             "11417", "11418", "11419", "11420", "11421", "11422", "11423", "11426", "11427", "11428", "11429", "11432", "11433",
    #             "11434", "11435", "11436", "11691", "11692", "11693", "11694", "11695", "11697"}
    conn = create_connection(args.core_rides_db)
    if conn is not None:
        rides_cursor = conn.cursor()
        statement = "SELECT * FROM rides;"
        rides_cursor.execute(statement)
        row_batch = []
        count = 0
        t0 = time.time()
        for row in rides_cursor:
            insert_cursor = conn.cursor()
            ride_id, ride_date_time, ride_company, ride_lat, ride_lng = row
            ride_zip_code = get_zip_code(ride_lat, ride_lng)
            new_row = (ride_id, ride_date_time, ride_company, ride_lat, ride_lng, ride_zip_code)
            row_batch.append(new_row)
            count += 1
            if count == 500:
                t1 = time.time()
                print(t1-t0)
                t0 = t1
                insert_cursor.execute("BEGIN TRANSACTION;")
                insert_cursor.executemany("INSERT INTO new_rides VALUES(?,?,?,?,?,?)", row_batch)
                insert_cursor.execute("COMMIT;")
                row_batch = []
                count = 0
                print(process.memory_percent())
        conn.commit()
        conn.close()


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Exception:
        print(traceback.print_exc())
    return None


def get_zip_code(ride_lat, ride_lng):
    result = search.by_coordinates(ride_lat, ride_lng)
    return result[0].zipcode


if __name__ == '__main__':
    main()
