from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

default_args = {
    'owner': 'dev_team',
    'email': [],  # Change to your email
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=1),
}

def fail_task():
    raise Exception("This task is designed to fail and trigger alert email.")

with DAG(
    'failure_test_dag',
    default_args=default_args,
    description='A DAG that fails to test email alerts',
    schedule_interval=None,
    start_date=days_ago(1),
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
