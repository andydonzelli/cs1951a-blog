import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
from matplotlib import rc
sns.set(font_scale=2)

# Set custom font
font_files = font_manager.findSystemFonts(fontpaths=os.getcwd() + '../fonts')
font_list = font_manager.createFontList(font_files)
font_manager.fontManager.ttflist.extend(font_list)
mpl.rcParams['font.family'] = 'Product Sans'
# Read in csv as pandas dataframe
df = pd.read_csv('r2_heatmap.csv')
# Reshape pandas dataframe into into pivot table
pt = df.pivot(index='zxc', columns='Ride Service', values='R^2')
# Set up the matplotlib figure
fig, ax = plt.subplots(figsize=(16, 3))
# Generate a custom colormap
cmap = sns.light_palette("#4285F4", as_cmap=True)
# Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(pt, fmt="g", cmap=cmap, vmin=0, vmax=0.2512, linewidths=1, annot=True, cbar=False, annot_kws={"color": "#FFFFFF"}, cbar_kws={"orientation": "horizontal", "fraction": 0.2, "pad":0.6})
# Add title with bold font and padding
title = "$R{^2}$ values for each ride service"
plt.title(title, fontweight="bold", pad=20, size=40)
fig.canvas.set_window_title(title)
# Turn off ticks
plt.tick_params(top=False, bottom=False, left=False,
                right=False, labelleft=False, labelbottom=True)
# Make axis labels bold and have more padding
for axis in [ax.xaxis, ax.yaxis]:
    axis.label.set_weight("bold")
    axis.label.set_size(35)
    axis.label.set_visible(False)
ax.xaxis.labelpad = 30
ax.yaxis.labelpad = 15
plt.tick_params(axis='both', which='major', labelsize=26)
#Make figure
fig.tight_layout()
fig.savefig("r2_heatmap.svg", dpi=1200)
plt.show()
