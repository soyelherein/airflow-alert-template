import os
from airflow.utils.email import send_email_smtp
from airflow.utils.session import provide_session
from airflow import configuration
from jinja2 import Template
from airflow.utils.log.logging_mixin import LoggingMixin

log = LoggingMixin().log

@provide_session
def failure_callback(context, session=None):
    """
    Custom Airflow failure callback to send templated HTML email alerts.
    """
    # Get template paths from Airflow config
    template_path = configuration.conf.get(
        'email',
        'html_content_template',
        fallback=None
    )
    subject_template_path = configuration.conf.get(
        'email',
        'subject_template',
        fallback="🚨 Airflow Alert: {{ task.task_id }} failed"
    )

    # Verify the template file exists
    if not template_path or not os.path.exists(template_path):
        raise FileNotFoundError(f"Email template not found: {template_path}")

    # Load HTML template
    with open(template_path, 'r') as f:
        template_str = f.read()

    with open(subject_template_path, 'r') as f:
        subject_template_str = f.read()

    email_template = Template(template_str)
    subject_template = Template(subject_template_str)

    # Render templates with the context
    try:
        html_content = email_template.render(**context, session=session)
        subject = subject_template.render(**context)
    except Exception as e:
        log.error("Error rendering email templates: %s", e)
        raise

    # Extract recipient(s)
    task = context.get("task")
    to_emails = task.email if task and task.email else ["your.email@example.com"]
    if isinstance(to_emails, str):
        to_emails = [to_emails]

    # Send the email
    try:
        send_email_smtp(to=to_emails, subject=subject, html_content=html_content)
        log.info("Failure alert email sent to: %s", to_emails)
    except Exception as e:
        log.error("Failed to send email: %s", e)
        raise
