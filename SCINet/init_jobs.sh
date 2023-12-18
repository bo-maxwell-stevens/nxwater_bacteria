#!/bin/bash

# Remove previous models
rm -rf MicrobeModels3/ 
rm std-out/*

# Create base directory if it doesn't exist
mkdir -p MicrobeModels3

# Extracting microbial names from the CSV
MICROBES=$(awk -F, 'NR==1 {for(i=1;i<=NF;i++) if ($i ~ /^Bacteria|^Fungi/) print $i}' brute_force_df.csv)

# Loop through each microbe, create its directory and submit the job
for MICROBE in $MICROBES; do
    mkdir -p MicrobeModels3/$MICROBE
    sbatch submit_single_microbe_job.slurm $MICROBE
done
