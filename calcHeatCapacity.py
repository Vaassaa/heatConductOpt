"""
Python script for calculation of soil heat capacity 
from monitoring data
    Author: Vaclav Steinbach
    Date: 26.03.2025
    Dissertation work
"""
# For dry organic soil (from lit.)
# C_o = 0.748 MJ.Mg^-1.K^-1 = 748 J.kg^-1.K^-1 x 1135 kg.m^-3 = 848980 J.kg^-1.K^-1 
# For dry mineral soil (from lit.)
# C_m = 0.758 MJ.Mg^-1.K^-1 = 758 J.kg^-1.K^-1 x 1483 kg.m^-3 = 1124114 J.kg^-1.K^-1 
import numpy as np
import pandas as pd
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

# Subsoil buk data
FILE = "output_"+loc+"_"+tree+"_subsoil.csv"
subsoil_buk_df = pd.read_csv(PATH + FILE)
grouped_subsoil_buk_df = subsoil_buk_df.groupby('tag')
subsoil_buk_highSWC_df = grouped_subsoil_buk_df.get_group('high_SWC')
subsoil_buk_midSWC_df = grouped_subsoil_buk_df.get_group('mid_SWC')
subsoil_buk_lowSWC_df = grouped_subsoil_buk_df.get_group('low_SWC')

org_lowSWC_mean = np.mean(topsoil_buk_lowSWC_df['SWC'])
org_midSWC_mean = np.mean(topsoil_buk_midSWC_df['SWC'])
org_highSWC_mean = np.mean(topsoil_buk_highSWC_df['SWC'])

min_lowSWC_mean = np.mean(subsoil_buk_lowSWC_df['SWC'])
min_midSWC_mean = np.mean(subsoil_buk_midSWC_df['SWC'])
min_highSWC_mean = np.mean(subsoil_buk_highSWC_df['SWC'])

# Params from literature
dry_org = 848980
dry_min = 1124114
water_capa = 4200000

soilHeatCapa = [dry_org + water_capa * org_lowSWC_mean,
                dry_min + water_capa * min_lowSWC_mean,
                dry_org + water_capa * org_midSWC_mean,
                dry_min + water_capa * min_midSWC_mean,
                dry_org + water_capa * org_highSWC_mean,
                dry_min + water_capa * min_highSWC_mean]

# Write to the .dat file
filename = out_FOLD+"soilHeatCapa.dat"
with open(filename, "w") as f:
    f.write("# theta lowSWC org min\n")
    f.write(f"{org_lowSWC_mean:.5f} {min_lowSWC_mean:.5f}\n")
    f.write("# capacity lowSWC org min\n")
    f.write(f"{soilHeatCapa[0]:.0f} {soilHeatCapa[1]:.0f}\n")
    f.write("# theta midSWC org min\n")
    f.write(f"{org_midSWC_mean:.5f} {min_midSWC_mean:.5f}\n")
    f.write("# capacity midSWC org min\n")
    f.write(f"{soilHeatCapa[2]:.0f} {soilHeatCapa[3]:.0f}\n")
    f.write("# theta highSWC org min\n")
    f.write(f"{org_highSWC_mean:.5f} {min_highSWC_mean:.5f}\n")
    f.write("# capacity highSWC org min\n")
    f.write(f"{soilHeatCapa[4]:.0f} {soilHeatCapa[5]:.0f}\n")
