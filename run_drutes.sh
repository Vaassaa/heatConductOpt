# Bash script for rewriting .conf file for parameter optimalization
#!/bin/bash

WORKDIR="$1"
shift
rm -rf "$WORKDIR"
cp -a drutes_temp "$WORKDIR"
cd "$WORKDIR"

# replace vars in chosen .conf with cmd arguments
# add -e 's/!var/'$k'/g' for each var
conduct1=$1
conduct2=$2
convect1=$3
convect2=$4
src1=$5
src2=$6
sed -e 's/!conduct1/'$conduct1'/g' -e 's/!conduct2/'$conduct2'/g' -e 's/!convect1/'$convect1'/g' -e 's/!convect2/'$convect2'/g' -e 's/!source1/'$src1'/g' -e 's/!source2/'$src2'/g' drutes.conf/heat/heat.conf.temp > drutes.conf/heat/heat.conf

# run drutes simulation and discard the terminal output
bin/drutes > /dev/null

# run drutes simulation with output
#bin/drutes


