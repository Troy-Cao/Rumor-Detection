#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks--node=2
#SBATCH --time=0-00:20:00

module load Python/3.7.3-spartan_gcc-8.1.0

time mpiexec python3 main_Pool.py -i /home/troycao/bigTwitter.json