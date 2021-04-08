#!/bin/bash

# run this scipt with root privileges, cpupower requires these privileges 
# function RANDOM return number from 0-32767

pa=9830 # 0.3
max_freq=2600000
filename=$1

cat $filename | while read ops p n; 
do 
	u=$RANDOM

if [ $u -le $pa ]; 
	then 
		/usr/bin/cpupower frequency-set -g userspace -d $max_freq -u $max_freq > /dev/null
fi;

#echo "$ops $p $n"	
	sbatch -n $n srun.sbatch $ops
	sleep $p
done;