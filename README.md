# Setup of soil heat conductivity calibration from monitoring data
Input variables:
- **Trees** $tree: smrk, buk, modrin
- **Locations** $loc: loc1, loc2, loc3
- **Scenarios** $swc: low, mid, high
Input data in form of .csv files containing temperature evolution for each tree type and locations has to be provided in a folowing format:
dataIN/
├── buk
│   ├── output_loc1_buk_subsoil.csv
│   ├── output_loc1_buk_topsoil.csv
│   ├── output_loc2_buk_subsoil.csv
│   ├── output_loc2_buk_topsoil.csv
│   ├── output_loc3_buk_subsoil.csv
│   └── output_loc3_buk_topsoil.csv
├── modrin
│   ├── output_loc1_modrin_subsoil.csv
│   ├── output_loc1_modrin_topsoil.csv
│   ├── output_loc2_modrin_subsoil.csv
│   ├── output_loc2_modrin_topsoil.csv
│   ├── output_loc3_modrin_subsoil.csv
│   └── output_loc3_modrin_topsoil.csv
└── smrk
    ├── output_loc1_smrk_subsoil.csv
    ├── output_loc1_smrk_topsoil.csv
    ├── output_loc2_smrk_subsoil.csv
    ├── output_loc2_smrk_topsoil.csv
    ├── output_loc3_smrk_subsoil.csv
    └── output_loc3_smrk_topsoil.csv

User has two ways to obtain calibration results
## Manual
1. Prepare simulation input data for desired tree type and location
`./prepData.sh tree loc`
    - `prepInputs tree loc`
    - `prepInitTemp tree loc`
    - `calcHeatCapacity tree loc`
2. Prepare DRUtES configurations for each soil moisture scenario
`./prepSimConf.sh swc`
3. Perform model calibration
`python3 heatConductOpt.py tree loc swc`
4. Visualize simulated data
`python3 genPlotMulti.py tree loc swc` 
5. Repeat step 2. - 4. for each scenario
6. Clean configurations between each location  
`./cleanTree`

## Semi-Automatic
Executes model calibration for given tree type, soil moisture scenario and model complexity
`./tree_sim.sh tree opt mod`
- opt:
    - low - all loc low swc only
    - mid - all loc mid swc only
    - high - all loc high swc only
    - all - all loc all swc
- mod:
    - 1 - conduction only
    - 2 - conduction + convection
    - 3 - conduction + source
    - 4 - conduction + convection + source

Both ways should yield
