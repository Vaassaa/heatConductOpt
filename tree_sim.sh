#Main bash script that executes all simulations (all SWC, all loc) for specified type of tree
#!/bin/bash
#Input vars
tree="$1" # tree: smrk, buk, modrin
opt="$2" # which swc
loc=("loc1" "loc2" "loc3") # all locations
mod="$3" 
# model complexity
# 1 ... conduction only
# 2 ... conduction + convection
# 3 ... conduction + source
# 4 ... conduction + convection + source

case "$opt" in
	low)
	swc="low"
	;;
	mid)
	swc="mid"
	;;
	high)
	swc="high"
	;;
	all)
	swc=("low" "mid" "high")
	;;
esac
#Cycle through each swc and loc
for key_loc in "${loc[@]}"; do
  echo "Starting simulation for $tree location: $key_loc"
  ./prepData.sh $tree "$key_loc" # prepares input data
	for key_swc in "${swc[@]}"; do
  	./prepSimConf.sh "$key_swc" # prepares simulations for given swc
	python3 heatConductOpt.py "$tree" "$key_loc" "$key_swc" "$mod" # performs model calibration
	python3 genPlotMulti.py "$tree" "$key_loc" "$key_swc" # generates figures
  	echo "Finished simulation for key: $key_swc"
 	done 
  echo "Finished simulation for key: $key_loc"
  echo "--------------------------------------"
done
