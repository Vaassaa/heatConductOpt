"""
Python script that generates bar plot of soil conductivity for 
one type of tree, location and all soil moisture scenarios
    Author: Vaclav Steinbach
    Date: 01.04.2025
    Disseration Work
"""
import matplotlib.pyplot as plt
import h5py
import numpy as np
import sys

# Input vars
tree = sys.argv[1]
loc = sys.argv[2]

fig_name = tree+"_"+loc
# This script uses h5py data structure
with h5py.File("simul.h5", "r") as h5file:
    conduct_lowSWC = np.array(h5file["opt_out_"+tree+"_"+loc+"_lowSWC"])
    conduct_midSWC = np.array(h5file["opt_out_"+tree+"_"+loc+"_midSWC"])
    conduct_highSWC = np.array(h5file["opt_out_"+tree+"_"+loc+"_highSWC"])

swc = ("lowSWC", "midSWC", "highSWC")
soil_conduct = {
    'Conduct - Org': (conduct_lowSWC[0], conduct_midSWC[0], conduct_highSWC[0]),
    'Conduct - Min': (conduct_lowSWC[1], conduct_midSWC[1], conduct_highSWC[1]),
    }

x = np.arange(len(swc))  # the label locations
width = 0.25  # the width of the bars
multiplier = 0

fig, ax = plt.subplots(layout='constrained')

for attribute, measurement in soil_conduct.items():
    offset = width * multiplier
    rects = ax.bar(x + offset, measurement, width, label=attribute)
    ax.bar_label(rects, padding=3)
    multiplier += 1

ax.set_ylabel('Soil Conductivity (W.K^-1.m^-1)')
ax.set_title('Comparison of soil conductivity by soil moisture - '+tree+' - '+loc)
ax.set_xticks(x + width, swc)
ax.legend(loc='upper left', ncols=3)
save_folder = 'optOut/'
plt.savefig(save_folder+fig_name, dpi=300, transparent=True)
plt.show()

