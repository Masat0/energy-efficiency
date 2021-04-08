#!/bin/bash

#количество итераций для одной частоты, одного объема работ и количества ядер

e=$1
for f in 1.2 2.6;
  do
    cpupower frequency-set -g userspace -d "$f"GHz -u "$f"GHz
    echo "userspace "$f"GHz"
#
    for o in 50000 100000 500000 1000000 5000000;
    	do
        for n in $(seq 1 2);
      		do
       			for i in $(seq 1 $e);
          		do
          			test=$(sbatch -n $n srun.sbatch $o &)
            		echo $test
            		sleep 30
            	done;
        done;
    done;
  done;


