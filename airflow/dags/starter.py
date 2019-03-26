from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta


# Utility function
sender = 'me@amazon.com'
receiver = 'you@amazon.com'
server = 'smtp.amazon.com'
password = 'password'

def send_mail(
    send_from, 
    send_to,
    subject, 
    message, 
    cc=None,
    server="localhost", 
    use_tls=True,
    port=587,
    username='',
    password=''
    ):
    """Compose and send email with provided info and attachments.

    Arguments:
        send_from (str): from name
        send_to (str): to name
        subject (str): message title
        message (str): message body
        files (list[str]): list of file paths to be attached to email
        cc (str): cc name
        server (str): mail server host name
        use_tls (bool): use TLS mode
        port (int): port number
        username (str): server auth username
        password (str): server auth password
    """
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.base import MIMEBase
    from email.mime.text import MIMEText
    from email.utils import formatdate
    from email import encoders

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = send_to
    if cc:
        msg['Cc'] = cc
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(message))

    smtp = smtplib.SMTP(server, port)
    if use_tls:
        smtp.ehlo()
        smtp.starttls()
    smtp.ehlo()
    smtp.login(username, password)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.quit()

def failed_mail_callback(ctx):
    title = 'Airflow alert: {task} failed.'.format(**ctx)
    body = """
    Airflow alert: {task} failed
    """.format(**ctx)
    send_mail(
        sender,
        receiver,
        title,
        body,
        server=server,
        username=sender,
        password=password
    )

def retry_mail_callback(ctx):
    title = 'Airflow alert: {task} retrying.'.format(**ctx)
    body = """
    Airflow alert: {task} retrying
    """.format(**ctx)
    send_mail(
        sender,
        receiver,
        title,
        body,
        server=server,
        username=sender,
        password=password
    )


# Define DAG

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2018, 6, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'end_date': datetime(2018, 6, 8),
}

dag = DAG('starter', default_args=default_args, schedule_interval=timedelta(1))

# t1, t2 and t3 are examples of tasks created by instantiating operators
t1 = BashOperator(task_id='print_date_push_xcom', bash_command='date', xcom_push=True, dag=dag)

t2 = BashOperator(
    task_id='pull_from_xcom',
    bash_command="echo {{ ti.xcom_pull(task_ids='print_date') }}",
    dag=dag
    )

templated_command = '''
    {% for i in range(5) %}
        echo '{{ ds }}'
        echo '{{ macros.ds_add(ds, 7)}}'
        echo '{{ params.my_param }}'
    {% endfor %}
'''

t3 = BashOperator(
    task_id='templated',
    bash_command=templated_command,
    params={'my_param': 'Parameter I passed in'},
    dag=dag,
)

t2.set_upstream(t1)
t3.set_upstream(t1)
