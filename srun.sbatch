#!/bin/bash

#SBATCH -o /home/user/projects/eee/run/%j.out
srun cset proc --set=user --exec stress-ng -- --cpu 1 --cpu-method pi --cpu-ops $1
