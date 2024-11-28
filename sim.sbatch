#!/bin/bash
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=48
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=3700
#SBATCH --time=12:00:00

MY_NUM_THREADS=$SLURM_CPUS_PER_TASK
export OMP_NUM_THREADS=$MY_NUM_THREADS

module purge
module load GCC/13.2.0 SciPy-bundle/2023.11

# Run $SLURM_NTASKS tasks in parallel
MY_PARALLEL_OPTS="-N 1 --delay 2 -j $SLURM_NTASKS --joblog parallel-${SLURM_JOBID}.log"
MY_SRUN_OPTS="-N 1 -n 1 --exclusive"
MY_EXEC='python "$HOME/alpha_sim_results/simulation_cluster.py" {1} constant'
parallel $MY_PARALLEL_OPTS srun $MY_SRUN_OPTS $MY_EXEC ::: {0..100}
