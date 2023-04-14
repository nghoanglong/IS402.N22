from datetime import datetime
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
import pandas as pd

dag = DAG(
    dag_id="system_healthy_checking", 
    description="checking health of airflow system", 
    schedule_interval='0 * * * *', 
    start_date=datetime(2023, 3, 7), 
    catchup=False,
    max_active_runs=1
)

dummy_operator = DummyOperator(
    task_id='checking_task', 
    retries = 3, 
    dag=dag
)

