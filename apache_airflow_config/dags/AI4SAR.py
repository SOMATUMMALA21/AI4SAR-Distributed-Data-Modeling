from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash_operator import BashOperator
from data_retriever import retrieve_and_publish_sar_data
from train_model import train_model
from upload_model import upload_model_to_huggingface
from airflow.operators.python_operator import PythonOperator

default_args = {
    "owner": "sotummal",
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="AI4SAR_staging_workflow",
    default_args=default_args,
    description="This is a staging workflow to periodiclaly gather and publish data from public APIs",
    start_date=datetime(2021, 1, 1),
    schedule_interval="@monthly"
) as dag:
    
    task1 = PythonOperator(
        task_id="retrieve_and_publish_sar_data",
        python_callable=retrieve_and_publish_sar_data,
        op_kwargs={} # can change in the future if requires arguments
    )

    task2 = PythonOperator(
        task_id="train_model",
        python_callable=train_model,
        op_kwargs={} # can change in the future if requires arguments
    )

    task3 = PythonOperator(
        task_id="upload_model_to_huggingface",
        python_callable=upload_model_to_huggingface,
        op_kwargs={} # can change in the future if requires arguments
    )

    task1 >> task2 >> task3