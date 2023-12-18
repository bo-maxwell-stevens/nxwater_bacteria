import os
import json
import pandas as pd
from concurrent.futures import ProcessPoolExecutor

def load_data(microbe_path, data_file):
    """Load individual data file and return the result."""
    with open(os.path.join(microbe_path, data_file), 'r') as infile:
        data = json.load(infile)
    return {
        'Microbe': data["microbe"],
        'Interaction Microbe': data.get("interaction_microbe", "BaseModel"),
        'Feature Importance': data["feature_importances"],
        'R2': data.get("r2", None)
    }

def aggregate_results(directory_path='MicrobeModels3', max_workers=None):
    """Aggregate results from files (without .json extension) into a DataFrame."""
    agg_results = []
    
    # Create a ProcessPoolExecutor to parallelize the operations
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        # Iterate through each subdirectory in the provided directory
        for microbe_dir in os.listdir(directory_path):
            microbe_path = os.path.join(directory_path, microbe_dir)
            
            # Ensure it's a directory before proceeding
            if os.path.isdir(microbe_path):
                print(f'Found directory: {microbe_path}', flush=True)
                
                data_files = [f for f in os.listdir(microbe_path) if os.path.isfile(os.path.join(microbe_path, f))]
                
                if not data_files:
                    print(f'No data files found in {microbe_path}', flush=True)
                    continue
                
                # Parallelize loading and parsing data
                for result in executor.map(load_data, [microbe_path]*len(data_files), data_files):
                    agg_results.append(result)
                
    # Convert list of dictionaries to DataFrame
    agg_results_df = pd.DataFrame(agg_results)
    
    return agg_results_df


# Calling the function and storing the results in a DataFrame
results_df = aggregate_results()
results_df = results_df.sort_values('R2', ascending = False)
results_df.to_csv('/project/akron/NxWater/brute_force/collated_results3.csv')
# results_df = results_df[results_df['R2'] > 0.724]

# results_df.to_csv('/project/akron/NxWater/brute_force/collated_results_significant.csv')