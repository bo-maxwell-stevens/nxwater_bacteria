#!/bin/bash
#SBATCH --job-name=microbe_rf
#SBATCH --output=std-out/microbe_rf_%j.out
#SBATCH --error=std-out/microbe_rf_%j.err
#SBATCH --ntasks=1
#SBATCH --time=01:00:00
#SBATCH --partition=short
#SBATCH --mem-per-cpu=2G

module load miniconda
source activate /home/bo.stevens/.conda/envs/rf_env

# Execute Python script with the microbe as an argument
python run_rf.py $1