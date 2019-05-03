import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
from matplotlib import rc

# Set custom font
font_files = font_manager.findSystemFonts(fontpaths=os.getcwd() + '../fonts')
font_list = font_manager.createFontList(font_files)
font_manager.fontManager.ttflist.extend(font_list)
mpl.rcParams['font.family'] = 'Product Sans'
# Read in csv as pandas dataframe
df = pd.read_csv('heatmap.csv')
# Reshape pandas dataframe into into pivot table
pt = df.pivot(index='Feature', columns='Ride Service', values='Probability')
# Set up the matplotlib figure
fig, ax = plt.subplots(figsize=(16, 12))
# Generate a custom colormap
cmap = sns.light_palette("#0F9D58", as_cmap=True, reverse=True)
# Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(pt, fmt="g", cmap=cmap, vmin=0, vmax=1, linewidths=1)
# Add title with bold font and padding
title = "Regression $\it{p}$-values of Weather Features"
plt.title(title, fontweight="bold", pad=40, size=40)
fig.canvas.set_window_title(title)
# Add label to colorbar
ax.collections[0].colorbar.set_label(
    "$\it{p}$-value", fontweight="bold", labelpad=60, size=35, rotation=270)
# Increase size of color bar labels
ax.collections[0].colorbar.ax.tick_params(labelsize=26) 
# Turn off ticks
plt.tick_params(top=False, bottom=False, left=False,
                right=False, labelleft=True, labelbottom=True)
for label in ax.collections[0].colorbar.ax.yaxis.get_ticklines():
    label.set_visible(False)
# Make axis labels bold and have more padding
for axis in [ax.xaxis, ax.yaxis]:
    axis.label.set_weight("bold")
    axis.label.set_size(35)
ax.xaxis.labelpad = 30
ax.yaxis.labelpad = 15
plt.tick_params(axis='both', which='major', labelsize=26)
#Make figure
fig.tight_layout()
fig.savefig("heatmap.svg", dpi=1200)
plt.show()
