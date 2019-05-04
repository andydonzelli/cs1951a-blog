import sys
import csv
from uszipcode import Zipcode
from uszipcode import SearchEngine

search = SearchEngine(simple_zipcode=True)

def get_zip_code(ride_lat, ride_lng):
    result = search.by_coordinates(ride_lat, ride_lng)
    if len(result) != 0:
        return result[0].zipcode
    else:
        return -1

if __name__ == '__main__':
    csv_path = sys.argv[1]
    procssed_csv_path = csv_path.replace('rides_part', 'processed_rides_part')
    reader = csv.reader(open(csv_path, 'r'))
    writer = csv.writer(open(procssed_csv_path, 'w'))
    for row in reader:
        ride_date_time, ride_company, ride_lat, ride_lng = row
        ride_zip = get_zip_code(float(ride_lat), float(ride_lng))
        if ride_zip != -1:
            writer.writerow([ride_date_time, ride_company, ride_lat, ride_lng, ride_zip])
    print(f'{procssed_csv_path} done')
    sys.exit(0)