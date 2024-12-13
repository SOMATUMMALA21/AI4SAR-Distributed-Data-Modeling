import pandas as pd
from sodapy import Socrata
import os
import joblib

def retrieve_and_publish_sar_data():
    # Initialize Socrata client
    client = Socrata("data.ny.gov", None)

    # Fetch data from API(Note: replace with your own api ID and token)
    results = client.get("u6hu-h7p5", limit=2000) # REPLACE_ME

    # Convert results to DataFrame
    results_df = pd.DataFrame.from_records(results)

    # Define output folders
    output_data_folder = "output/data"
    output_preprocessed_folder = "output/preprocessed"
    os.makedirs(output_data_folder, exist_ok=True)
    os.makedirs(output_preprocessed_folder, exist_ok=True)

    # Save initial CSV file
    raw_output_file = os.path.join(output_data_folder, "magicwand.csv")
    results_df.to_csv(raw_output_file, index=False)

    # Drop unwanted columns
    columns_to_drop = [
        'incident_start_date',
        'incident_start_time',
        'incident_closed_date',
        'incident_closed_time',
        'location',
    ]
    results_df.drop(columns=columns_to_drop, inplace=True, errors='ignore')

    # Save preprocessed CSV file
    preprocessed_output_file = os.path.join(output_preprocessed_folder, "preprocessed.csv")
    results_df.to_csv(preprocessed_output_file, index=False)

    # Save preprocessed DataFrame using joblib
    preprocessed_joblib_file = os.path.join(output_preprocessed_folder, "preprocessed.pkl")
    joblib.dump(results_df, preprocessed_joblib_file)

    print(f"Data saved to {preprocessed_output_file} and {preprocessed_joblib_file}")
