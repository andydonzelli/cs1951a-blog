#!/usr/bin/env python

''' Creates 'nyc_zip_code_info.csv' a CSV file with headers ['ZIP_CODE', 'LAT', 'LNG', 'BOROUGH', 'NEIGHBOURHOOD'] in same directory.

    Requries the following files in same directory as script:
        - 'opendatasoft_ny_zip_code_info.csv' from https://public.opendatasoft.com/explore/dataset/us-zip-code-latitude-and-longitude/download/?format=csv&refine.state=NY&timezone=America/New_York&use_labels_for_header=true
        - 'us_zip_codes.csv' from https://gist.github.com/abatko/ee7b24db82a6f50cfce02afafa1dfd1e
'''

from bs4 import BeautifulSoup
import requests
import sqlite3
import csv


def main():
    scrape()

def scrape():
    page_link = 'https://www.health.ny.gov/statistics/cancer/registry/appendix/neighborhoods.htm'
    page_response = requests.get(page_link, timeout=5)
    page_content = BeautifulSoup(page_response.content, 'html.parser')

    table = page_content.find('table')
    rows = table.find_all('tr')

    zips = []
    zips_to_boroughs_dict = {}
    zips_to_neighbourhoods_dict = {}

    current_borough = None
    current_neighbourhood = None
    current_zip_codes = None

    for row in rows[1:]:
        cols = row.findAll('td')
        if len(cols) == 3:
            current_borough = cols[0].get_text()
            current_neighbourhood = cols[1].get_text()
            current_zip_codes = list(map(str.strip, cols[2].get_text().split(',')))
        else:
            current_neighbourhood = cols[0].get_text()
            current_zip_codes = list(map(str.strip, cols[1].get_text().split(',')))

        for zip_code in current_zip_codes:
            zips.append(zip_code)
            zips_to_boroughs_dict[zip_code] = current_borough
            zips_to_neighbourhoods_dict[zip_code] = current_neighbourhood

    zips_to_lats_dict, zips_to_longs_dict = get_nyc_zip_coordinates(zips)
    create_output_csv(zips, zips_to_lats_dict, zips_to_longs_dict,
                      zips_to_boroughs_dict, zips_to_neighbourhoods_dict)


def get_nyc_zip_coordinates(zips):
    us_zips_lats_dict_primary = None
    us_zips_longs_dict_primary = None
    us_zips_lats_dict_secondary = None
    us_zips_longs_dict_secondary = None

    with open('opendatasoft_ny_zip_code_info.csv', 'r') as csv_file:
        reader_primary = csv.reader(csv_file, delimiter=';')
        us_zips_lats_dict_primary = {rows[0]: rows[3] for rows in reader_primary}
    with open('opendatasoft_ny_zip_code_info.csv', 'r') as csv_file:
        reader_primary = csv.reader(csv_file, delimiter=';')
        us_zips_longs_dict_primary = {rows[0]: rows[4] for rows in reader_primary}
    with open('us_zip_codes.csv', 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        us_zips_lats_dict_secondary = {rows[0]: rows[1] for rows in reader}
    with open('us_zip_codes.csv', 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        us_zips_longs_dict_secondary = {rows[0]: rows[2] for rows in reader}

    zips_to_lats_dict = {}
    zips_to_longs_dict = {}
    for zip_code in zips:
        if zip_code in us_zips_lats_dict_primary:
            zips_to_lats_dict[zip_code] = us_zips_lats_dict_primary[zip_code]
            zips_to_longs_dict[zip_code] = us_zips_longs_dict_primary[zip_code]
        else:
            zips_to_lats_dict[zip_code] = us_zips_lats_dict_secondary[zip_code]
            zips_to_longs_dict[zip_code] = us_zips_longs_dict_secondary[zip_code]
    
    return zips_to_lats_dict, zips_to_longs_dict


def create_output_csv(zips, zips_to_lats_dict, zips_to_longs_dict, zips_to_boroughs_dict, zips_to_neighbourhoods_dict):
    zips.sort()
    output_csv = 'nyc_zip_code_info.csv'
    with open(output_csv, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=['ZIP_CODE', 'LAT', 'LNG', 'BOROUGH', 'NEIGHBOURHOOD'])
        writer.writeheader()
        for zip_code in zips:
            writer.writerow({'ZIP_CODE': zip_code, 'LAT': zips_to_lats_dict[zip_code], 'LNG': zips_to_longs_dict[zip_code],
                             'BOROUGH': zips_to_boroughs_dict[zip_code], 'NEIGHBOURHOOD': zips_to_neighbourhoods_dict[zip_code]})
    print(f'Ouput CSV: {output_csv}')


if __name__ == '__main__':
    main()
