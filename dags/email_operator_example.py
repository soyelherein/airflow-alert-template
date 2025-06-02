from airflow import DAG
from airflow.operators.email import EmailOperator
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 1, 1),
    'retries': 0,
}

with DAG(
    dag_id='email_operator_example',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    tags=['email'],
) as dag:

    send_email = EmailOperator(
        task_id='send_email_task',
        to='',# Change to your email
        subject='Test Email from Airflow 2.10',
        html_content="""
        <h3>Hello from Airflow 3!</h3>
        <p>This email was sent using the <b>EmailOperator</b>.</p>
        """,
    )

    send_email
