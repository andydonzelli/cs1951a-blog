import os
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager

# Set custom font
font_files = font_manager.findSystemFonts(fontpaths=os.getcwd() + '../fonts')
font_list = font_manager.createFontList(font_files)
font_manager.fontManager.ttflist.extend(font_list)
mpl.rcParams['font.family'] = 'Product Sans'

# Data
x = ['0:00', '1:00', '2:00', '3:00', '4:00', '5:00', '6:00', '7:00', '8:00', '9:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00', '0:00 (Tues)']
citi_hourly_rides_mon = [21.333333333333332, 9.777777777777779, 4.444444444444445, 3.375, 2.5, 12.333333333333334, 45.666666666666664, 113.55555555555556, 234.66666666666666, 179.77777777777777, 93.66666666666667,
                         91.0, 93.33333333333333, 105.44444444444444, 102.33333333333333, 108.0, 122.88888888888889, 182.11111111111111, 213.0, 179.22222222222223, 106.77777777777777, 79.88888888888889, 63.666666666666664, 41.0, 19.22222222222222]
green_hourly_rides_mon = [624.7777777777778, 401.22222222222223, 267.1111111111111, 172.88888888888889, 138.0, 114.22222222222223, 166.77777777777777, 286.6666666666667, 427.55555555555554, 462.0, 431.55555555555554, 405.0,
                          384.6666666666667, 365.3333333333333, 409.6666666666667, 453.44444444444446, 503.6666666666667, 606.0, 723.4444444444445, 776.3333333333334, 962.6666666666666, 951.6666666666666, 965.5555555555555, 821.3333333333334, 430.1111111111111]
lyft_hourly_rides_mon = [72.55555555555556, 71.33333333333333, 68.33333333333333, 58.0, 43.77777777777778, 29.444444444444443, 18.555555555555557, 11.444444444444445, 8.0, 7.555555555555555, 13.88888888888889, 18.555555555555557,
                         28.88888888888889, 27.0, 31.555555555555557, 35.111111111111114, 33.22222222222222, 36.111111111111114, 44.77777777777778, 39.77777777777778, 71.22222222222223, 70.55555555555556, 72.55555555555556, 74.11111111111111, 60.22222222222222]
uber_hourly_rides_mon = [77.77777777777777, 51.0, 44.77777777777778, 68.33333333333333, 95.88888888888889, 145.0, 178.44444444444446, 191.44444444444446, 180.11111111111111, 170.11111111111111, 146.55555555555554, 141.66666666666666,
                         140.33333333333334, 137.77777777777777, 141.77777777777777, 144.33333333333334, 162.55555555555554, 185.33333333333334, 207.11111111111111, 193.44444444444446, 255.77777777777777, 234.88888888888889, 199.33333333333334, 139.33333333333334, 56.333333333333336]
yellow_hourly_rides_mon = [573.7777777777778, 405.22222222222223, 283.55555555555554, 196.77777777777777, 188.33333333333334, 165.77777777777777, 253.44444444444446, 330.6666666666667, 328.8888888888889, 256.0, 181.88888888888889,
                           151.11111111111111, 158.66666666666666, 172.77777777777777, 168.0, 168.33333333333334, 153.22222222222223, 190.11111111111111, 250.55555555555554, 311.22222222222223, 454.77777777777777, 496.77777777777777, 565.5555555555555, 616.5555555555555, 491.44444444444446]
mycolors = ['lightgreen', '#ffd253', '#000000', '#00c8fc', '#ff14bb']
columns = ['Green Taxi', 'Yellow Taxi', 'Uber', 'Citi Bike', 'Lyft']
fig, ax = plt.subplots(figsize=(20, 10))
plt.xlim(left=0.0, right=24)
plt.ylim(bottom=0.0)
ax.fill_between(x, y1=green_hourly_rides_mon, y2=0, label=columns[0], color=mycolors[0], alpha=0.8, linewidth=1)
ax.fill_between(x, y1=yellow_hourly_rides_mon, y2=0, label=columns[1], color=mycolors[1], alpha=0.8, linewidth=1)
ax.fill_between(x, y1=uber_hourly_rides_mon, y2=0, label=columns[2], color=mycolors[2],  alpha=0.8, linewidth=1)
ax.fill_between(x, y1=citi_hourly_rides_mon, y2=0, label=columns[3], color=mycolors[3],  alpha=0.8, linewidth=1)
ax.fill_between(x, y1=lyft_hourly_rides_mon, y2=0, label=columns[4], color=mycolors[4],  alpha=0.8, linewidth=1)

# Add title with bold font and padding
title = "Average rides per hour on Mondays in Brooklyn"
plt.title(title, fontweight="bold", pad=40, size=45)
fig.canvas.set_window_title(title)

ax.set(ylim=[0, 2000])
leg = plt.legend(loc='upper right', fontsize=30) # bbox_to_anchor=(.37, 1)
leg.get_frame().set_linewidth(0.0)

# Turn off ticks
plt.tick_params(top=False, bottom=False, left=False,
                right=False, labelleft=True, labelbottom=True)

#Don't show first zero on Y axis
yticks = ax.yaxis.get_major_ticks() 
yticks[0].label1.set_visible(False)

plt.xlabel('Hour in day')
plt.ylabel('Number of rides')

for axis in [ax.xaxis, ax.yaxis]:
    axis.label.set_weight("bold")
    axis.label.set_size(38)
    axis.labelpad = 15

plt.tick_params(axis='both', which='major', labelsize=30)

for index, label in enumerate(ax.xaxis.get_ticklabels()):
    if index % 4 != 0:
        label.set_visible(False)

# Remove borders
plt.gca().spines["top"].set_alpha(0)
plt.gca().spines["bottom"].set_alpha(0)
plt.gca().spines["right"].set_alpha(0)
plt.gca().spines["left"].set_alpha(0)
fig.tight_layout()
fig.savefig("non_stacked_area_plots_mon.svg", dpi=1200)
plt.show()
