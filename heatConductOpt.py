"""
Python script for calibration of heat equations coefficients
using measured temperature data from forest location
of AMALIA pilot site in parallel.
    Author: Vaclav Steinbach
    Date: 18.03.2025
    Dissertation work
"""
import subprocess  # for executing bash script 
import numpy as np # general maths 
import pandas as pd # data manipulation
from scipy.optimize import differential_evolution # optimalization
import tempfile # paralelization
import shutil # for removing of dirs
import os # subroutines
import h5py # for storing simulation data
import sys # inputs

# Input vars
tree = sys.argv[1]
loc = sys.argv[2]
swc = sys.argv[3]
mod = int(sys.argv[4]) # model complexity
# Define the path for data files
PATH = "optData/"
out_FOL = "optOut/"
# Specify the data file to use
FILE = "monitoring_"+swc+".dat"
filename = "opt_out_"+tree+"_"+loc+"_"+swc+"SWC"

def getError(out_dir):
    """
    Reads the values of objective function and computes optimalization error.
    """
    error_file = os.path.join(out_dir, "objfnc.val")
    with open(error_file, "r") as file:
        lines = file.readlines()

    # Filter out comments and extract numeric values
    objfnc_val = [float(line.strip()) for line in lines if not line.strip().startswith("#")]
    print("Object function values:\n", objfnc_val)

    val_arr = np.array(objfnc_val)
    # Compute the sum of squared errors and return its square root
    error = np.sqrt(np.sum(val_arr**2))
    return error
    

def runDrutes(par):
    """
    Executes the DRUtES simulation with a given set of parameters.
    A unique temporary working directory is created for each run.
    """
    # Define the model complexity
    match mod:
        case 1: # conduction only model
            therm_conduct1 = par[0]  # Thermal conductivity of organic part
            therm_conduct2 = par[1]  # Thermal conductivity of mineral part
        case 2: # conduction + convection
            therm_conduct1 = par[0]  
            therm_conduct2 = par[1]  
            therm_convect1 = par[2] # Thermal convection of organic part
            therm_convect2 = par[3] # Thermal convection of mineral part
        case 3: # conduction + source
            therm_conduct1 = par[0]  
            therm_conduct2 = par[1]  
            therm_source1= par[2] # Thermal source or sink of organic part
            therm_source2 = par[3] # Thermal source or sink of mineral part
        case 4: # all terms 
            therm_conduct1 = par[0]
            therm_conduct2 = par[1] 
            therm_convect1 = par[2]
            therm_convect2 = par[3]
            therm_source1= par[4]
            therm_source2 = par[5] 

    # Create a unique temporary directory for this simulation run
    temp_dir = tempfile.mkdtemp(prefix="drutes_run_")

    # Build the command to run the shell script
    match mod:
        case 1:
            cmd = ["bash", "run_drutes.sh", temp_dir,
            str(therm_conduct1), 
            str(therm_conduct2),
            str(0.0),
            str(0.0),
            str(0.0),
            str(0.0)]
        case 2: 
            cmd = ["bash", "run_drutes.sh", temp_dir,
            str(therm_conduct1), 
            str(therm_conduct2),
            str(therm_convect1),
            str(therm_convect2),
            str(0.0),
            str(0.0)]
        case 3:
            cmd = ["bash", "run_drutes.sh", temp_dir,
            str(therm_conduct1), 
            str(therm_conduct2),
            str(0.0),
            str(0.0),
            str(therm_source1),
            str(therm_source2)]
        case 4:
            cmd = ["bash", "run_drutes.sh", temp_dir,
            str(therm_conduct1), 
            str(therm_conduct2),
            str(therm_convect1),
            str(therm_convect2),
            str(therm_source1),
            str(therm_source2)]

    # Run the shell command (Simulation)
    subprocess.run(cmd, check=True)

    # The simulation output in a subfolder 'out'
    out_dir = os.path.join(temp_dir, "out")
    error = getError(out_dir)
    
    # Simulation progress print
    print("Tree:", tree)
    print("Location:", loc)
    print("Soil Moisture scenario:", swc)
    print("Optimalization error: ", error)

    match mod:
        case 1:
            print("Thermal conductivity (organic):  ", therm_conduct1)
            print("Thermal conductivity (mineral): ", therm_conduct2)
        case 2: 
            print("Thermal conductivity (organic):  ", therm_conduct1)
            print("Thermal conductivity (mineral): ", therm_conduct2)
            print("Thermal convection (organic):", therm_convect1)
            print("Thermal convection (mineral):", therm_convect2)
        case 3:
            print("Thermal conductivity (organic):  ", therm_conduct1)
            print("Thermal conductivity (mineral): ", therm_conduct2)
            print("Thermal source (organic):", therm_source1)
            print("Thermal source (mineral):", therm_source2)
        case 4:    
            print("Thermal conductivity (organic):  ", therm_conduct1)
            print("Thermal conductivity (mineral): ", therm_conduct2)
            print("Thermal convection (organic):", therm_convect1)
            print("Thermal convection (mineral):", therm_convect2)
            print("Thermal source (organic):", therm_source1)
            print("Thermal source (mineral):", therm_source2)
    
    # Count the iterations (calls of runDrutes)
    runDrutes.call_count += 1
    print(f"Iteration: {runDrutes.call_count}\n")
    
    # Remove the temporary directory 
    shutil.rmtree(temp_dir, ignore_errors=True)
    return error

def store_simulation(sim_key, simulation_data, filename="simul.h5"):
    """
    Stores simulation ouputs into a structured database
    """
    with h5py.File(filename, "a") as h5file:
        h5file.create_dataset(sim_key, data=simulation_data)

# Define bounds for the optimization parameters
conduct_bnd = (0.001, 15.0)  # Bounds for thermal conductivity parameters
convect_bnd = (-3.0, 3.0) # bounds for thermal convection parameter
source_bnd = (-1.0, 1.0) # bounds for source parameter
match mod:
    case 1:
        bounds = [conduct_bnd, conduct_bnd] 
    case 2:
        bounds = [conduct_bnd, conduct_bnd, convect_bnd, convect_bnd]
    case 3:
        bounds = [conduct_bnd, conduct_bnd, source_bnd, source_bnd]
    case 4:
        bounds = [conduct_bnd, conduct_bnd, convect_bnd, convect_bnd, source_bnd, source_bnd]

# Initialize a counter attribute for runDrutes
runDrutes.call_count = 0

# Load monitoring data for computation of error
monitoring_data = pd.read_csv(PATH + FILE, sep='\t')

# Run differential evolution optimization in parallel.
# The workers=-1 setting uses all available CPU cores.
result = differential_evolution(runDrutes, bounds, 
                                workers=-1, 
                                updating='deferred',
                                tol=1e-4,
                                atol = 1e-4,
                                maxiter=10000)

# Output the optimized parameter values and error
print("Optimized values:\n", result.x, '\n', result.fun)

# Write output file with calibrated parameters based on model complexity
match mod:
    case 1:
        with open(out_FOL + filename + ".txt", 'w') as file:
            file.write('#conduct1 conduct2\n')
            file.write(' '.join(f"{x:.5f}" for x in result.x) + '\n')
            file.write('#error\n')
            file.write(f"{result.fun:.5f}")
    case 2:
        with open(out_FOL + filename + ".txt", 'w') as file:
            file.write('#conduct1 conduct2 convect1 convect2\n')
            file.write(' '.join(f"{x:.5f}" for x in result.x) + '\n')
            file.write('#error\n')
            file.write(f"{result.fun:.5f}")
    case 3:
        with open(out_FOL + filename + ".txt", 'w') as file:
            file.write('#conduct1 conduct2 source1 source2\n')
            file.write(' '.join(f"{x:.5f}" for x in result.x) + '\n')
            file.write('#error\n')
            file.write(f"{result.fun:.5f}")
    case 4:
        with open(out_FOL + filename + ".txt", 'w') as file:
            file.write('#conduct1 conduct2 convect1 convect2 source1 source2\n')
            file.write(' '.join(f"{x:.5f}" for x in result.x) + '\n')
            file.write('#error\n')
            file.write(f"{result.fun:.5f}")

# Store the calibrated params into a database
sim_key = filename
# store_simulation(sim_key, result.x)

# Prepare commands for final simulation
optimal_dir = "drutes_run"  # This folder will now contain the final simulation run.
match mod:
    case 1:
        cmd_final = ["bash",
                     "run_drutes.sh",
                     optimal_dir,
                     str(result.x[0]),
                     str(result.x[1]),
                     str(0.0),
                     str(0.0),
                     str(0.0),
                     str(0.0)]
    case 2:
        cmd_final = ["bash",
                     "run_drutes.sh",
                     optimal_dir,
                     str(result.x[0]),
                     str(result.x[1]),
                     str(result.x[2]),
                     str(result.x[3]),
                     str(0.0),
                     str(0.0)]
    case 3:
        cmd_final = ["bash",
                     "run_drutes.sh",
                     optimal_dir,
                     str(result.x[0]),
                     str(result.x[1]),
                     str(0.0),
                     str(0.0),
                     str(result.x[2]),
                     str(result.x[3])]
    case 4:
        cmd_final = ["bash",
                     "run_drutes.sh",
                     optimal_dir,
                     str(result.x[0]),
                     str(result.x[1]),
                     str(result.x[2]),
                     str(result.x[3]),
                     str(result.x[4]),
                     str(result.x[5])]

# Run the simulation with the optimilized parameters
subprocess.run(cmd_final, check=True)
print(f"Final simulation run stored in '{optimal_dir}'.")

