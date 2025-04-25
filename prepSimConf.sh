#Bash script that prepares instances of drutes for simulation of all SWC scenarios
if [ ! -d "allSWC" ]; then
  mkdir allSWC
  echo "Directory 'allSWC' created."
fi

# Params
swc="$1"
cp -r drutes_template allSWC/drutes_$swc

#Copy OptData to its simulation dirs
cp optData/monitoring_$swc.dat allSWC/drutes_$swc/drutes.conf/inverse_modeling/
cp optData/heaticond1D_$swc.in allSWC/drutes_$swc/drutes.conf/heat/heaticond1D.in 
cp optData/102_$swc.bc allSWC/drutes_$swc/drutes.conf/heat/102.bc
cp optData/soilHeatCapa.dat allSWC/drutes_$swc/drutes.conf/heat/

cd allSWC/drutes_$swc/drutes.conf/inverse_modeling/
sed -e 's/!swc/'$swc'/g' objfnc.conf.temp > objfnc.conf

cd ..
cd heat/

#Rewrite the calculated values of soil heat capacity
SOURCE_FILE="soilHeatCapa.dat"   # File containing the line with two variables.
TARGET_FILE="heat.conf.temp" # File where you want to insert the values.
case "$swc" in
	low)
	heatCapa_line=4
	;;
	mid)
	heatCapa_line=8
	;;
	high)
	heatCapa_line=12
	;;
esac
TARGET_LINE_org=33          # Target line for the first variable.
TARGET_LINE_min=34          # Target line for the second variable.

# Extract the specified line from the source file.
line=$(sed -n "${heatCapa_line}p" "$SOURCE_FILE")

# Split the line into two variables based on space.
read var1 var2 <<< "$line"

# Function to replace or insert a line in the target file.
replace_line() {
  local file=$1
  local line_num=$2
  local new_value=$3

  sed -i "${line_num}s/.*/$new_value/" "$file"
}

# Insert the first variable into TARGET_LINE1 and the second into TARGET_LINE2.
replace_line "$TARGET_FILE" "$TARGET_LINE_org" "$var1"
replace_line "$TARGET_FILE" "$TARGET_LINE_min" "$var2"

rm soilHeatCapa.dat
cd .. # /drutes.conf
cd .. # /drutes_!swc
cd .. # /allSWC
cd .. # /heatConductOpt_parallel
#cd /home/vstein/Documents/PhD/Code/heatConductOpt_parallel
if [ -d "drutes_temp" ]; then
  rm -r drutes_temp
  echo "Directory 'drutes_temp' destroyed."
fi
cp -r allSWC/drutes_$swc drutes_temp

