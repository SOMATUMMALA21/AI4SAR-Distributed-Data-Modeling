import os
import pickle
from huggingface_hub import HfApi, HfFolder
from skops import card, hub_utils
from pathlib import Path
from sklearn.metrics import accuracy_score, f1_score
import matplotlib.pyplot as plt
import pandas as pd

def upload_model_to_huggingface(model_dir='output/model', model_file='model.pkl', testing_data_file='output/testing/accuracy.pkl', repo_id='REPLACE_ME'):
    # Check if model file exists
    model_path = os.path.join(model_dir, model_file)
    if not os.path.exists(model_path):
        print(f"Model file {model_file} not found in {model_dir}")
        return

    # Load the model
    with open(model_path, 'rb') as f:
        model = pickle.load(f)

    # Load testing data
    if not os.path.exists(testing_data_file):
        print(f"Testing data file {testing_data_file} not found")
        return

    with open(testing_data_file, 'rb') as f:
        test_data = pickle.load(f)

    accuracy = test_data['accuracy']
    y_test = pd.DataFrame(test_data['y_test'])
    y_pred = test_data['y_pred']

    # Initialize Hugging Face API
    api = HfApi()
    token = HfFolder.get_token()

    if token is None:
        print("Hugging Face token not found. Please log in using 'huggingface-cli login'")
        return

    # Create local repository
    local_repo = "AI4SAR-model"
    hub_utils.init(
        model=model_path,
        requirements=["scikit-learn"],
        dst=local_repo,
        task="tabular-classification",
        data=y_test
    )

    # Create model card
    model_card = card.Card(model, metadata=card.metadata_from_config(Path(local_repo) / "config.json"))
    model_card.add(
        model_description="RandomForestClassifier model for tabular classification.",
        eval_method="Evaluated using test split."
    )
    model_card.add_metrics(
        accuracy=accuracy_score(y_test, y_pred),
        f1_score=f1_score(y_test, y_pred, average='weighted')
    )

    # Create confusion matrix plot
    from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix
    cm = confusion_matrix(y_test, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=model.classes_)
    disp.plot()
    plot_path = Path(local_repo) / "confusion_matrix.png"
    plt.savefig(plot_path, bbox_inches='tight')
    model_card.add_plot(confusion_matrix=str(plot_path))

    # Save the model card
    model_card.save(Path(local_repo) / "README.md")

    # Upload the repository to Hugging Face Hub
    try:
        hub_utils.push(
            repo_id=repo_id,
            source=local_repo,
            token=token,
            commit_message="Uploading RandomForestClassifier model and evaluation data.",
            create_remote=True,
        )
        print(f"Successfully uploaded model and evaluation data to {repo_id}.")
    except Exception as e:
        print(f"Failed to upload model: {e}")
