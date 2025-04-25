"""
Python script for construction of intial temperature function
    Author: Vaclav Steinbach
    Date: 26.03.2025
    Dissertation work
"""
import pandas as pd
import sys
# Mesh values from drutes
z_values = [-0.5, -0.23, -0.15, -0.08, 0.0]
# Input vars
tree = sys.argv[1]
loc = sys.argv[2]

dat_fol = "dataIN"
PATH = dat_fol+"/"+tree+"/"
out_FOLD = "optData/"

# load Topsoil buk data
FILE = "output_"+loc+"_"+tree+"_topsoil.csv"
topsoil_buk_df = pd.read_csv(PATH + FILE)
grouped_topsoil_buk_df = topsoil_buk_df.groupby('tag')
topsoil_buk_highSWC_df = grouped_topsoil_buk_df.get_group('high_SWC')
topsoil_buk_midSWC_df = grouped_topsoil_buk_df.get_group('mid_SWC')
topsoil_buk_lowSWC_df = grouped_topsoil_buk_df.get_group('low_SWC')

# load Subsoil buk data
FILE = "output_"+loc+"_"+tree+"_subsoil.csv"
subsoil_buk_df = pd.read_csv(PATH + FILE)
grouped_subsoil_buk_df = subsoil_buk_df.groupby('tag')
subsoil_buk_highSWC_df = grouped_subsoil_buk_df.get_group('high_SWC')
subsoil_buk_midSWC_df = grouped_subsoil_buk_df.get_group('mid_SWC')
subsoil_buk_lowSWC_df = grouped_subsoil_buk_df.get_group('low_SWC')

# Construct initial function for each SWC
T_values_lowSWC = [
        subsoil_buk_lowSWC_df['T_n23cm'].iloc[0],
        subsoil_buk_lowSWC_df['T_n23cm'].iloc[0],
        subsoil_buk_lowSWC_df['T_n10cm'].iloc[0],
        topsoil_buk_lowSWC_df['T_n8cm'].iloc[0],
        topsoil_buk_lowSWC_df['T_0cm'].iloc[0]]

T_values_midSWC = [
        subsoil_buk_midSWC_df['T_n23cm'].iloc[0],
        subsoil_buk_midSWC_df['T_n23cm'].iloc[0],
        subsoil_buk_midSWC_df['T_n10cm'].iloc[0],
        topsoil_buk_midSWC_df['T_n8cm'].iloc[0],
        topsoil_buk_midSWC_df['T_0cm'].iloc[0]]

T_values_highSWC = [
        subsoil_buk_highSWC_df['T_n23cm'].iloc[0],
        subsoil_buk_highSWC_df['T_n23cm'].iloc[0],
        subsoil_buk_highSWC_df['T_n10cm'].iloc[0],
        topsoil_buk_highSWC_df['T_n8cm'].iloc[0],
        topsoil_buk_highSWC_df['T_0cm'].iloc[0]]

# Combine z values and the corresponding T values
intialTemp_lowSWC = pd.DataFrame({
    'z': z_values,
    'T': T_values_lowSWC})

intialTemp_midSWC = pd.DataFrame({
    'z': z_values,
    'T': T_values_midSWC})

intialTemp_highSWC = pd.DataFrame({
    'z': z_values,
    'T': T_values_highSWC})

# Save to a .in file with '#' header / comment in fortran
filename = out_FOLD+'heaticond1D_low.in'
with open(filename, 'w') as f:
    f.write("# z\tT\n")       
    intialTemp_lowSWC.to_csv(f, sep='\t', index=False, header=False)

filename = out_FOLD+'heaticond1D_mid.in'
with open(filename, 'w') as f:
    f.write("# z\tT\n")       
    intialTemp_midSWC.to_csv(f, sep='\t', index=False, header=False)

filename = out_FOLD+'heaticond1D_high.in'
with open(filename, 'w') as f:
    f.write("# z\tT\n")       
    intialTemp_highSWC.to_csv(f, sep='\t', index=False, header=False)
