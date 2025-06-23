from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime,timedelta

from airflow.utils.email import send_email
from airflow.utils.db import provide_session
from jinja2 import Template
from random import random
from utils.email_callback import failure_callback


default_args = {
    'owner': 'dev_team',
    'email': ["youremail@airflow.com"],  # Change to your email
    'email_on_failure': False,
    'email_on_retry': False,
    'on_failure_callback': failure_callback,
    'on_retry_callback': failure_callback,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}


def randomly_fail():
    if random() < 0.8:  # 50% chance to fail
        raise Exception("🔴 Task failed randomly!")
    else:
        print("✅ Task succeeded.")

with DAG(
    'failure_test_dag_callback',
    default_args=default_args,
    description='A DAG that fails to test email alerts',
    schedule=None,
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=['test', 'alert'],
    params={
        "recovery_tip": "Check the failure message and logs. Restart the task after fixing the issue.",
    },
) as dag:

    randomly_fail = PythonOperator(
        task_id='fail_task',
        python_callable=randomly_fail,
    )
