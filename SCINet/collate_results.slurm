#!/bin/bash
#SBATCH --job-name=collate_rf
#SBATCH --output=std-out/collate.out
#SBATCH --error=std-out/collate.err
#SBATCH --ntasks=96
#SBATCH --time=24:00:00
#SBATCH --partition=short
#SBATCH --mem-per-cpu=3G
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=bo.stevens@usda.gov 

module load miniconda
source activate /home/bo.stevens/.conda/envs/rf_env

# Execute Python script with the microbe as an argument
python collate_results.py
