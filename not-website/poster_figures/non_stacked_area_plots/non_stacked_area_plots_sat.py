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
x = ['0:00', '1:00', '2:00', '3:00', '4:00', '5:00', '6:00', '7:00', '8:00', '9:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00', '0:00 (Sun)']
citi_hourly_rides_mon = [43.77777777777778, 31.88888888888889, 15.555555555555555, 8.88888888888889, 6.666666666666667, 6.444444444444445, 10.88888888888889, 27.22222222222222, 54.111111111111114, 102.0, 135.55555555555554, 169.88888888888889, 207.11111111111111, 215.11111111111111, 222.66666666666666, 226.44444444444446, 203.55555555555554, 190.55555555555554, 176.33333333333334, 149.77777777777777, 101.11111111111111, 74.77777777777777, 66.22222222222223, 55.77777777777778, 43.888888888888886]
green_hourly_rides_mon = [1780.111111111111, 1649.111111111111, 1460.111111111111, 1157.3333333333333, 712.8888888888889, 303.44444444444446, 166.22222222222223, 156.77777777777777, 214.22222222222223, 292.55555555555554, 389.6666666666667, 492.55555555555554, 559.1111111111111, 598.8888888888889, 715.5555555555555, 880.2222222222222, 974.7777777777778, 1063.0, 1263.111111111111, 1388.111111111111, 1330.7777777777778, 1394.7777777777778, 1604.888888888889, 1806.3333333333333, 1934.888888888889]
lyft_hourly_rides_mon = [105.88888888888889, 102.0, 115.55555555555556, 115.77777777777777, 109.88888888888889, 99.88888888888889, 75.55555555555556, 50.888888888888886, 29.555555555555557, 16.555555555555557, 15.0, 19.22222222222222, 27.444444444444443, 32.888888888888886, 40.77777777777778, 41.666666666666664, 52.666666666666664, 62.111111111111114, 69.77777777777777, 74.66666666666667, 54.77777777777778, 67.11111111111111, 77.22222222222223, 97.66666666666667, 99.44444444444444]
uber_hourly_rides_mon = [298.0, 215.33333333333334, 140.0, 103.66666666666667, 79.66666666666667, 88.66666666666667, 109.33333333333333, 135.66666666666666, 166.77777777777777, 202.66666666666666, 225.55555555555554, 244.55555555555554, 249.66666666666666, 287.55555555555554, 328.55555555555554, 337.6666666666667, 361.3333333333333, 392.44444444444446, 385.6666666666667, 401.6666666666667, 315.44444444444446, 354.1111111111111, 381.1111111111111, 363.6666666666667, 361.1111111111111]
yellow_hourly_rides_mon = [1500.111111111111, 1446.888888888889, 1192.888888888889, 907.8888888888889, 614.0, 261.55555555555554, 206.11111111111111, 227.11111111111111, 299.1111111111111, 342.6666666666667, 369.0, 369.44444444444446, 371.0, 411.55555555555554, 392.44444444444446, 387.22222222222223, 330.1111111111111, 375.3333333333333, 440.8888888888889, 515.6666666666666, 468.6666666666667, 539.5555555555555, 698.5555555555555, 1090.4444444444443, 1672.3333333333333]

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
title = "Average rides per hour on Saturdays in Brooklyn"
plt.title(title, fontweight="bold", pad=40, size=45)
fig.canvas.set_window_title(title)

ax.set(ylim=[0, 2000])
leg = plt.legend(loc='upper right', fontsize=30) #  bbox_to_anchor=(.37, 1)
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
fig.savefig("non_stacked_area_plots_sat.svg", dpi=1200)
plt.show()
