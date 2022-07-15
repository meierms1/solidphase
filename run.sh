#!/bin/bash
#SBATCH -J AP_HTPB_Spheres           # job name
#SBATCH -o AP_HTPB_Spheres_%j # output file name (%j expands)
#SBATCH -N 1                 # total number of nodes 
#SBATCH -n 128               # total number of mpi tasks requested
#SBATCH -t 46:00:00          # run time (hh:mm:ss) - 1.5 hours
#SBATCH --mail-user=meierdo@uccs.edu
#SBATCH --mail-type=begin    # email me when the job starts
#SBATCH --mail-type=end      # email me when the job finishes

mpirun -np 128 ../../../alamo/bin/alamo-2d-g++ input plot_file = /mmfs1/home/mmeierdo/output_${SLURM_JOB_ID}
