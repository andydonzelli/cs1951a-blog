# Obtain per-hour Brooklyn weather information for the two months (Aug + Sept 2014), and 
# write this to a CSV file.

# Uses the DarkSky API for data, and the darkskylib python package to help manage that
# interaction.

from darksky import forecast
import csv

key = 'e2e4a964619ef646b0a52d025659eb08'        # Secret API key!
BROOKLYN = 40.649013, -73.943782                # Midpoint of Brooklyn

t = 1406865600      # Start with Unix time of midnight Aug 1, 2014


fieldnames = ['time','precipIntensity', 'temperature', 'apparentTemperature', \
              'dewPoint', 'windSpeed', 'cloudCover', 'uvIndex' ]

with open('hourly_weather.csv', 'w') as weather_file:
                
    writer = csv.DictWriter(weather_file, fieldnames=fieldnames, extrasaction='ignore', \
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)

    writer.writeheader()

    while t < 1412136000:     # Stop once we hit midnight of Oct. 1

        with forecast(key, *BROOKLYN, time=t, units='us', \
                      exclude='currently,minutely,daily') as data:

            for hourData in data.hourly:
                # The DictWriter only writes fields we have specified
                writer.writerow(hourData._data)

            t += 86400  # Add 1 day's worth of seconds to the time.