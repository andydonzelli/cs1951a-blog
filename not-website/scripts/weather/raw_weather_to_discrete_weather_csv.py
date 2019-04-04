'''
Takes raw weather csv and writes a weather csv with
discrete categorized values of sunny, windy, rainy or cloudy conditions
binned by hours.
Assumes input file is hourly weather
'''
import sqlite3
import csv
from argparse import ArgumentParser

''' SYNOPSIS
        python3 raw_weather_to_discrete_weather_csv.py [-i input file] [-o output file]
'''

parser = ArgumentParser()
parser.add_argument("-i", "--infile", dest="infile", help="Input .csv file")
parser.add_argument("-o", "--outfile", dest="outfile", help="Output .csv file")
args = parser.parse_args()

#Hyperparameters
rain_threshold = 0.8 #mm/hr 
wind_threshold = 4.0 #m/s
cloud_threshold = 0.4 #percentage

'''
Below the cloud threshold of 0.4 we will assume weather conditions are sunny
with the additional conditions that the rain and wind thresholds are not met
'''
bin_count = 0
with open(args.infile, 'r') as infile,open(args.outfile,'w') as outfile:
    fieldnames = ['bin_time','unix_time','sunny','windy','rainy','cloudy','temperature','dew_point',
                'uv_index','precip_intensity','wind_speed','cloud_cover','apparent_temperature']
    reader = csv.DictReader(infile)
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in reader:
        if float(row['precipIntensity']) >= rain_threshold:
            writer.writerow({'bin_time':bin_count,'unix_time':row['time'],'sunny':0,'windy':0,
            'rainy':1,'cloudy':0,'temperature':row['temperature'],'dew_point':row['dewPoint'],
            'uv_index':row['uvIndex'],'precip_intensity':row['precipIntensity'],
            'wind_speed':row['windSpeed'],'cloud_cover':row['cloudCover'],
            'apparent_temperature':row['apparentTemperature']})
        elif float(row['windSpeed']) >= wind_threshold:
            writer.writerow({'bin_time':bin_count,'unix_time':row['time'],'sunny':0,'windy':1,
            'rainy':0,'cloudy':0,'temperature':row['temperature'],'dew_point':row['dewPoint'],
            'uv_index':row['uvIndex'],'precip_intensity':row['precipIntensity'],
            'wind_speed':row['windSpeed'],'cloud_cover':row['cloudCover'],
            'apparent_temperature':row['apparentTemperature']})
        elif float(row['cloudCover']) >= cloud_threshold:
            writer.writerow({'bin_time':bin_count,'unix_time':row['time'],'sunny':0,'windy':0,
            'rainy':0,'cloudy':1,'temperature':row['temperature'],'dew_point':row['dewPoint'],
            'uv_index':row['uvIndex'],'precip_intensity':row['precipIntensity'],
            'wind_speed':row['windSpeed'],'cloud_cover':row['cloudCover'],
            'apparent_temperature':row['apparentTemperature']})
        else:
            writer.writerow({'bin_time':bin_count,'unix_time':row['time'],'sunny':1,'windy':0,
            'rainy':0,'cloudy':0,'temperature':row['temperature'],'dew_point':row['dewPoint'],
            'uv_index':row['uvIndex'],'precip_intensity':row['precipIntensity'],
            'wind_speed':row['windSpeed'],'cloud_cover':row['cloudCover'],
            'apparent_temperature':row['apparentTemperature']})
        bin_count += 1
print("FINISHED!!!")
