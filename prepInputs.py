"""
Python scritpt for preparation of simulation 
and optimalization input data
    Author: Vaclav Steinbach
    Date: 25.10.2024
    Dissertation work
"""
import pandas as pd  # for data manipulation
import os
import sys
# Input vars
tree = sys.argv[1]
loc = sys.argv[2]

dat_fol = "dataIN"
PATH = dat_fol+"/"+tree+"/"
out_FOLD = "optData/"

# Topsoil buk data
FILE = "output_"+loc+"_"+tree+"_topsoil.csv"
topsoil_buk_df = pd.read_csv(PATH + FILE)
grouped_topsoil_buk_df = topsoil_buk_df.groupby('tag')
topsoil_buk_highSWC_df = grouped_topsoil_buk_df.get_group('high_SWC')
topsoil_buk_midSWC_df = grouped_topsoil_buk_df.get_group('mid_SWC')
topsoil_buk_lowSWC_df = grouped_topsoil_buk_df.get_group('low_SWC')

#  Look at the structure of topsoil data
# print("TOPSOIL BUK DATA")
# Set option to display all columns
# pd.set_option('display.max_columns', None)
# topsoil_buk_lowSWC_df.info()
# print(topsoil_buk_lowSWC_df.head(10))

# Subsoil buk data
FILE = "output_"+loc+"_"+tree+"_subsoil.csv"
subsoil_buk_df = pd.read_csv(PATH + FILE)
grouped_subsoil_buk_df = subsoil_buk_df.groupby('tag')
subsoil_buk_highSWC_df = grouped_subsoil_buk_df.get_group('high_SWC')
subsoil_buk_midSWC_df = grouped_subsoil_buk_df.get_group('mid_SWC')
subsoil_buk_lowSWC_df = grouped_subsoil_buk_df.get_group('low_SWC')

#  Convert the DTM data to seconds for simulation
time_lowSWC = pd.to_datetime(topsoil_buk_lowSWC_df['DTM'], format='mixed')
epoch = pd.Timestamp(time_lowSWC.iloc[0])
time_lowSWC_sec = pd.DataFrame()
time_lowSWC_sec['seconds'] = (time_lowSWC - epoch).dt.total_seconds()

time_midSWC = pd.to_datetime(topsoil_buk_midSWC_df['DTM'], format='mixed')
epoch = pd.Timestamp(time_midSWC.iloc[0])
time_midSWC_sec = pd.DataFrame()
time_midSWC_sec['seconds'] = (time_midSWC - epoch).dt.total_seconds()

time_highSWC = pd.to_datetime(topsoil_buk_highSWC_df['DTM'], format='mixed')
epoch = pd.Timestamp(time_highSWC.iloc[0])
time_highSWC_sec = pd.DataFrame()
time_highSWC_sec['seconds'] = (time_highSWC - epoch).dt.total_seconds()

# Get the values for upper boundary condition
selected_data_top_lowSWC_BC = topsoil_buk_lowSWC_df['T_0cm']
selected_data_top_midSWC_BC = topsoil_buk_midSWC_df['T_0cm']
selected_data_top_highSWC_BC = topsoil_buk_highSWC_df['T_0cm']
bc_low = pd.concat([time_lowSWC_sec, selected_data_top_lowSWC_BC],axis=1)
bc_mid = pd.concat([time_midSWC_sec, selected_data_top_midSWC_BC],axis=1)
bc_high = pd.concat([time_highSWC_sec, selected_data_top_highSWC_BC],axis=1)

# Save the upper boundary condition files
bc_low.to_csv(out_FOLD+'102_low.bc', index=False, header=False, sep='\t')
bc_mid.to_csv(out_FOLD+'102_mid.bc', index=False, header=False, sep='\t') 
bc_high.to_csv(out_FOLD+'102_high.bc', index=False, header=False, sep='\t')

#  Select the data for monitoring file for each SWC
selected_data_top_lowSWC = topsoil_buk_lowSWC_df[['T_n8cm']]
selected_data_sub_lowSWC_10 = subsoil_buk_lowSWC_df[['T_n10cm']]
selected_data_sub_lowSWC_23 = subsoil_buk_lowSWC_df[['T_n23cm']]
monitoring_low = pd.concat([time_lowSWC_sec,
                            selected_data_top_lowSWC, 
                            selected_data_sub_lowSWC_10,
                            selected_data_sub_lowSWC_23], axis=1)

selected_data_top_midSWC = topsoil_buk_midSWC_df[['T_n8cm']]
selected_data_sub_midSWC = subsoil_buk_midSWC_df[['T_n10cm', 'T_n23cm']]
monitoring_mid = pd.concat([time_midSWC_sec, selected_data_top_midSWC, selected_data_sub_midSWC], axis=1)

selected_data_top_highSWC = topsoil_buk_highSWC_df[['T_n8cm']]
selected_data_sub_highSWC_10 = subsoil_buk_highSWC_df[['T_n10cm']]
selected_data_sub_highSWC_23 = subsoil_buk_highSWC_df[['T_n23cm']]
monitoring_high = pd.concat([time_highSWC_sec,
                             selected_data_top_highSWC,
                             selected_data_sub_highSWC_10,
                             selected_data_sub_highSWC_23], axis=1)
# Standart deviations data
std_top_lowSWC = topsoil_buk_lowSWC_df[['SD_Tn8cm']]
std_sub_lowSWC = subsoil_buk_lowSWC_df[['SD_Tn10cm', 'SD_Tn23cm']]
std_low = pd.concat([std_top_lowSWC, std_sub_lowSWC], axis=1)

std_data_top_midSWC = topsoil_buk_midSWC_df[['SD_Tn8cm']]
std_data_sub_midSWC = subsoil_buk_midSWC_df[['SD_Tn10cm', 'SD_Tn23cm']]
std_mid = pd.concat([std_data_top_midSWC, std_data_sub_midSWC], axis=1)

std_data_top_highSWC = topsoil_buk_highSWC_df[['SD_Tn8cm']]
std_data_sub_highSWC = subsoil_buk_highSWC_df[['SD_Tn10cm', 'SD_Tn23cm']]
std_high = pd.concat([std_data_top_highSWC, std_data_sub_highSWC], axis=1)

# Save the STD data
std_low.to_csv(out_FOLD+'std_low.dat', index=False, sep='\t')
std_mid.to_csv(out_FOLD+'std_mid.dat', index=False, sep='\t')
std_high.to_csv(out_FOLD+'std_high.dat', index=False, sep='\t')

# Save the monitoring data 
monitoring_low.to_csv(out_FOLD+'monitoring_low.dat', index=False, sep='\t')
monitoring_mid.to_csv(out_FOLD+'monitoring_mid.dat', index=False, sep='\t')
monitoring_high.to_csv(out_FOLD+'monitoring_high.dat', index=False, sep='\t')
# Adds '#' at the beginning of the first line / comment
filenames = ["monitoring_low.dat", "monitoring_mid.dat", "monitoring_high.dat", "std_low.dat", "std_mid.dat", "std_high.dat"] 
for i in range(len(filenames)): 
    filename = out_FOLD + filenames[i]  
    with open(filename, 'r') as file:
        lines = file.readlines()

    # Write the modified contents back to the file
    with open(filename, 'w') as file:
        file.write('#' + lines[0])
        file.writelines(lines[1:])
