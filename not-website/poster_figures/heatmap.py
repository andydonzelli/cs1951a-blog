import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager

# Set custom font
font_files = font_manager.findSystemFonts(fontpaths=os.getcwd() + '/fonts')
font_list = font_manager.createFontList(font_files)
font_manager.fontManager.ttflist.extend(font_list)
mpl.rcParams['font.family'] = 'Metropolis'
# Read in csv as pandas dataframe
df = pd.read_csv('heatmap.csv')
# Reshape pandas dataframe into into pivot table
pt = df.pivot(index='Feature', columns='Ride Service', values='Probability')
# Set up the matplotlib figure
fig, ax = plt.subplots(figsize=(10, 5))
# Generate a custom diverging colormap
cmap = sns.light_palette("#0F9D58", as_cmap=True)
# Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(pt, fmt="g", cmap=cmap, vmin=0, vmax=1, linewidths=1)
# Add title with bold font and padding
title = "Regression Probabilities of Weather Features"
plt.title(title, fontweight="bold", pad=15, size=20)
fig.canvas.set_window_title(title)
# Add label to colorbar
ax.collections[0].colorbar.set_label(
    "Probability", fontweight="bold", labelpad=25, size=14, rotation=270)
# Turn off ticks
plt.tick_params(top=False, bottom=False, left=False,
                right=False, labelleft=True, labelbottom=True)
for label in ax.collections[0].colorbar.ax.yaxis.get_ticklines():
    label.set_visible(False)
# Make axis labels bold and have more padding
for axis in [ax.xaxis, ax.yaxis]:
    axis.label.set_weight("bold")
    axis.label.set_size(14)
    axis.labelpad = 15
fig.tight_layout()
fig.savefig("heatmap.png", format='png', dpi=600)
plt.show()
