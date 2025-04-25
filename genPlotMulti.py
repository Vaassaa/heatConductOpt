"""
Python scritpt for ploting the comparison of simulated
versus measured temperatures evolution of soil in forest 
location of AMALIA pilot site
    Author: Vaclav Steinbach
    Date: 19.12.2024
    Dissertation work
"""
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import sys
import matplotlib.ticker as ticker
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
# Input vars
tree = sys.argv[1]
loc = sys.argv[2]
swc = sys.argv[3]
PATH_to_measured = "optData/"
out_FOLD = "optOut/simOut/"
FILE_of_measured = "monitoring_"+swc+".dat"
FILE_of_std = "std_"+swc+".dat"
fig_name = "Comparison_"+tree+"_"+loc+"_"+swc+"SWC.png"

# Switch for title
if swc == "low":
    title = 'Low soil water content'
elif swc == "mid":
    title = 'Medium soil water content'
elif swc == "high":
    title = 'High soil water content'
else:
    print("Value not recognized...")

# print('Monitoring data are in this format:')
measured_data = pd.read_csv(PATH_to_measured+FILE_of_measured, sep='\t')
# print(measured_data)
std_data = pd.read_csv(PATH_to_measured+FILE_of_std, sep='\t')

# Get simulated data
PATH_to_simulated = "drutes_run/out/"
FILE_of_simulated_obspt1 = "obspt_heat-1.out"
FILE_of_simulated_obspt2 = "obspt_heat-2.out"
FILE_of_simulated_obspt3 = "obspt_heat-3.out"

# If the simulation has already been done, use this! 
# PATH_to_simulated = "optOut/simOut/"
# FILE_of_simulated_obspt1 = "obspt1_"+swc+".out"
# FILE_of_simulated_obspt2 = "obspt2_"+swc+".out"
# FILE_of_simulated_obspt3 = "obspt3_"+swc+".out"

# Observation point 1 (-8cm)
obspt1 = pd.read_csv(PATH_to_simulated+FILE_of_simulated_obspt1,
                   skiprows=10,  # metadata
                   sep='\s+', # white space separator
                   header=None)
# Name the simulated data
obspt1.columns = ['time', 'temperature', 'heat_flux', 'cumulative_flux']

# Observation point 2 (-15cm)
obspt2 = pd.read_csv(PATH_to_simulated+FILE_of_simulated_obspt2,
                   skiprows=10,  # metadata
                   sep='\s+', # white space separator
                   header=None)
# Name the simulated data
obspt2.columns = ['time', 'temperature', 'heat_flux', 'cumulative_flux']

# Observation point 3 (-23cm)
obspt3 = pd.read_csv(PATH_to_simulated+FILE_of_simulated_obspt3,
                   skiprows=10,  # metadata
                   sep='\s+', # white space separator
                   header=None)
# Name the simulated data
obspt3.columns = ['time', 'temperature', 'heat_flux', 'cumulative_flux']

# Save the simulated outputs
obspt1.to_csv(out_FOLD+"obspt1_"+swc+".out", index=False, sep='\t')
obspt2.to_csv(out_FOLD+"obspt2_"+swc+".out", index=False, sep='\t')
obspt3.to_csv(out_FOLD+"obspt3_"+swc+".out", index=False, sep='\t')

selected_data_obspt1 = obspt1[['time', 'temperature']]
selected_data_obspt2 = obspt2[['temperature']]
selected_data_obspt3 = obspt3[['temperature']]
simulated_data = pd.concat([selected_data_obspt1, selected_data_obspt2, selected_data_obspt3], axis=1)
simulated_data.columns = ['seconds', 'T_n8cm', 'T_n10cm', 'T_n23cm']

# Create a figure with 3 subplots arranged in a 3x1 grid.
fig, axs = plt.subplots(3, 1, figsize=(6,8), sharex=True)
# Define a formatter for the x-axis to show scientific notation (e.g., 175e3)
formatter = ticker.FuncFormatter(lambda x, pos: f"{x/1000:.0f}e3")

# -------------------------
# Subplot 1: Depth -8 cm
# -------------------------
# Plot measured data with a dashed line and fill for std area.
axs[0].plot(measured_data['#seconds'], measured_data['T_n8cm'],
            linestyle='--', color='forestgreen', label='Measured')
axs[0].fill_between(measured_data['#seconds'],
                    measured_data['T_n8cm'] - std_data['#SD_Tn8cm'],
                    measured_data['T_n8cm'] + std_data['#SD_Tn8cm'],
                    color='forestgreen', alpha=0.2)
# Plot simulated data with a solid line.
axs[0].plot(simulated_data['seconds'], simulated_data['T_n8cm'],
            linestyle='-', color='forestgreen', label='Simulated')
axs[0].grid(True, which='both')
# Add minor ticks to the Y axis
axs[0].yaxis.set_minor_locator(ticker.AutoMinorLocator())
axs[0].tick_params(which='minor', length=4)
# --------------------------
# Subplot 2: Depth -15 cm
# --------------------------
axs[1].plot(measured_data['#seconds'], measured_data['T_n10cm'],
            linestyle='--', color='darkorange', label='Measured')
axs[1].fill_between(measured_data['#seconds'],
                    measured_data['T_n10cm'] - std_data['SD_Tn10cm'],
                    measured_data['T_n10cm'] + std_data['SD_Tn10cm'],
                    color='darkorange', alpha=0.2)
axs[1].plot(simulated_data['seconds'], simulated_data['T_n10cm'],
            linestyle='-', color='darkorange', label='Simulated')
axs[1].set_ylabel('Soil temperature [°C]')
axs[1].grid(True, which='both')
axs[1].yaxis.set_minor_locator(ticker.AutoMinorLocator())
axs[1].tick_params(which='minor', length=4)

# -------------------------
# Subplot 3: Depth -23 cm
# -------------------------
axs[2].plot(measured_data['#seconds'], measured_data['T_n23cm'],
            linestyle='--', color='sienna', label='Measured')
axs[2].fill_between(measured_data['#seconds'],
                    measured_data['T_n23cm'] - std_data['SD_Tn23cm'],
                    measured_data['T_n23cm'] + std_data['SD_Tn23cm'],
                    color='sienna', alpha=0.2)
axs[2].plot(simulated_data['seconds'], simulated_data['T_n23cm'],
            linestyle='-', color='sienna', label='Simulated')
axs[2].grid(True, which='both')
axs[2].yaxis.set_minor_locator(ticker.AutoMinorLocator())
axs[2].tick_params(which='minor', length=4)
axs[2].set_xlabel('Simulation time [seconds]')
axs[2].xaxis.set_major_formatter(formatter)
# Custom legend entries for better clarity
custom_lines = [
    Line2D([0], [0], color='black', linestyle='--', label='Measured'),
    Line2D([0], [0], color='black', linestyle='-', label='Simulated'),
    Line2D([0], [0], color='forestgreen', linestyle='-', label='-8 cm'),
    Line2D([0], [0], color='darkorange', linestyle='-', label='-15 cm'),
    Line2D([0], [0], color='sienna', linestyle='-', label='-23 cm')
]
# Add legend
fig.legend(handles=custom_lines, 
           loc='lower center', ncol=5)
fig.suptitle(title, fontsize=16)

# Adjust layout to leave room for the legend
plt.subplots_adjust(bottom=0.1)
# Check the file names!
save_folder = 'optOut/'
plt.savefig(save_folder+fig_name, dpi=300, transparent=True)
# plt.show()
