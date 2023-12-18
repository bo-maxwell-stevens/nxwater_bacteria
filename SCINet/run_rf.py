import sys
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
import os
import time
import json

start = time.time()

def run_model_and_save(X, y, microbe_name, interaction_microbe=None):
    """Run Random Forest Grid Search and save results."""
    # Grid search parameters
    param_grid = {
        'n_estimators': [10, 50],  # You can expand this list if necessary
        'max_features': ['sqrt'],
        'max_depth': [10, 20, None]
    }

    # Initialize RandomForestRegressor and GridSearchCV
    rf = RandomForestRegressor()
    grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=5, scoring='r2')

    # Fit model
    grid_search.fit(X, y)
    best_rf = grid_search.best_estimator_

    # Extract feature importances
    feature_importances = dict(zip(X.columns, best_rf.feature_importances_))

    # Result data
    result_data = {
        "microbe": microbe_name,
        "interaction_microbe": interaction_microbe,
        "best_params": grid_search.best_params_,
        "feature_importances": feature_importances,
        "r2": grid_search.best_score_  # Add this line to save the R^2 score
    }

    # Determine filename based on interaction microbe
    if interaction_microbe:
        filename = f"{microbe_name}_With_{interaction_microbe}.json"
    else:
        filename = f"{microbe_name}_BaseModel.json"

    # Save the result as a JSON file inside the microbe's directory
    with open(os.path.join('MicrobeModels3', microbe_name, filename), 'w') as outfile:
        json.dump(result_data, outfile, indent=4)


# Fetch microbe name from arguments
microbe_name = sys.argv[1]

# Load the dataset
data = pd.read_csv('brute_force_df.csv')
# data = data[data['Sample date'] == '2021-09-23']

# Base model features and target
features_base = [microbe_name, 'Water trt target', 'N trt target']
X_base = data[features_base]
y = data['Grain 0% MC']  

# Run base model
run_model_and_save(X_base, y, microbe_name)

# Interaction models
for interaction_microbe in data.columns:
    if interaction_microbe.startswith(('Bacteria', 'Fungi')) and interaction_microbe != microbe_name:
        features_interaction = features_base + [interaction_microbe]
        X_interaction = data[features_interaction]
        run_model_and_save(X_interaction, y, microbe_name, interaction_microbe)

end = time.time()
print(end - start)