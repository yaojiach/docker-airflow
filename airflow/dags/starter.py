from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2018, 6, 1),
    'email': ['airflow@airflow.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
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
