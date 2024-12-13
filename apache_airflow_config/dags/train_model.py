import pandas as pd
import numpy as np
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import make_column_transformer
from sklearn.pipeline import make_pipeline
from sklearn.utils import class_weight
import joblib

def train_model():
    # Load the preprocessed data
    preprocessed_file = 'output/preprocessed/preprocessed.pkl'
    results_df = joblib.load(preprocessed_file)

    # Load and prepare the data
    location_data_filtered = results_df[['location_found_elevation', 'situation', 'found_in_search_area']].dropna()

    # Define features (X) and target (y)
    X = location_data_filtered[['location_found_elevation', 'situation']]
    y = location_data_filtered['found_in_search_area']

    # Column transformer for scaling and encoding
    ct = make_column_transformer(
        (StandardScaler(), ['location_found_elevation']),
        (OneHotEncoder(), ['situation']),
        remainder="drop"
    )

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

    print(X_test)
    print(type(X_test))

    # create data frame that looks like X_test with fake data not X_test
    fake_data = pd.DataFrame({'location_found_elevation': [0, 0, 0], 'situation': ['fake', 'fake', 'fake']})
    print(fake_data)

    # Calculate class weights to handle class imbalance
    unique_classes = np.unique(y_train)
    class_weights = class_weight.compute_class_weight(class_weight='balanced', classes=unique_classes, y=y_train)
    class_weights_dict = dict(zip(unique_classes, class_weights))

    # Create pipeline with RandomForestClassifier using class weights
    pipe = make_pipeline(ct, RandomForestClassifier(n_estimators=100, random_state=42, class_weight=class_weights_dict))
    pipe.fit(X_train, y_train)

    # Make predictions
    y_pred = pipe.predict(X_test)

    # Evaluate the model
    accuracy = accuracy_score(y_test, y_pred)
    print(f'Accuracy: {accuracy:.2f}')
    print('Classification Report:')
    print(classification_report(y_test, y_pred))

    # Store the accuracy and the y_test and y_pred
    accuracy_map = {'accuracy': accuracy, 'y_test': y_test, 'y_pred': y_pred}
    output_testing_folder = 'output/testing'
    os.makedirs(output_testing_folder, exist_ok=True)
    with open('output/testing/accuracy.pkl', 'wb') as f:
        pickle.dump(accuracy_map, f)

    # Store the model
    output_model_folder = 'output/model'
    os.makedirs(output_model_folder, exist_ok=True)
    with open('output/model/model.pkl', 'wb') as f:
        pickle.dump(pipe, f)

    print(f"Model and accuracy data saved.")
