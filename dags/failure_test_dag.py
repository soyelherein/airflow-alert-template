from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime,timedelta

default_args = {
    'owner': 'dev_team',
    'email': ["youremail@airflow.com"],  # Change to your email
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

def fail_task():
    raise Exception("This task is designed to fail and trigger alert email.")

with DAG(
    'failure_test_dag',
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

    task_fail = PythonOperator(
        task_id='fail_task',
        python_callable=fail_task,
    )
