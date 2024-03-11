from airflow import DAG
from datetime import datetime, timedelta

from airflow.operators.python_operator import PythonOperator

from extract_scripts import parse_ISRID

default_args = {
    "owner": "sotummal",
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    default_args=default_args,
    dag_id="AI4SAR_staging_workflow",
    description="This is a data staging workflow for the ISRID dataset.",
    start_date=datetime(2024, 1, 1), # Can be changed
    schedule_interval="@weekly" # A weekly cadence should be good enough as the dataset is not updated very frequently
) as dag:
    task1 = PythonOperator(
        task_id="greet_task",
        python_callable=parse_ISRID,
    )

    task1
