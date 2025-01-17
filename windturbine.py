from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.python import BranchPythonOperator
from airflow.operators.email import EmailOperator
from airflow.sensors.filesystem import FileSensor
from airflow.utils.task_group import TaskGroup
from datetime import datetime, timedelta
import json
import os

default_args = {
    'depends_on_past': False,
    'email': [''], #adicionar email para envio de mensagem/alerta
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_dalay': timedelta(seconds=10)
    }

dag = DAG('windturbine', description='Dados da Turbina', schedule_interval=None, 
          start_date=datetime(2023,3,5), catchup=False, default_args=default_args,
          default_view='graph', doc_md="## Dag para registrar dados de turbina eólica")

group_check_temp = TaskGroup("group_checL_temp", dag=dag)
group_database = TaskGroup("group_database", dag=dag)

file_sensor_task = FileSensor(
    task_id = 'file_sensor_task',
    filepath = Variable.get('path_file'),
    fs_conn_id = 'fs_default',
    poke_interval = 10,
    dag=dag
    )

def process_file(**kwarg):
    with open(Variable.get('path_file')) as f:
        data = json.load(f)
        kwarg['ti'].xcom_psuh(key='idtemp', value=data['idtemp'])
        kwarg['ti'].xcom_psuh(key='powerfactor', value=data['powerfactor'])
        kwarg['ti'].xcom_psuh(key='hydraulicpressure', value=data['hydraulicpressure'])
        kwarg['ti'].xcom_psuh(key='temperature', value=data['temperature'])
        kwarg['ti'].xcom_psuh(key='timestamp', value=data['timestamp'])
    os.remove(Variable.get('path_file'))

get_data = PythonOperator(
    task_id = 'get_data',
    python_callable = process_file,
    provide_context = True,
    dag=dag
)

create_table = PostgresOperator(task_id="create_table", postgres_conn_id="postgres",
                                sql='''create table if not exists
                                sensors (idtemp varcharm powerfactor varchar,
                                hydraulicpressure varchar, temperature varchar,
                                timestamp varchar);
                                ''',
                                task_group=group_database,
                                dag=dag)

insert_data = PostgresOperator(task_id='insert_data',
                               postgres_conn_id='postgres',
                               parameters=(
                               '{{ ti.xcom_pull(task_ids="get_data",key="idtemp") }}',
                               '{{ ti.xcom_pull(task_ids="get_data",key="powerfactor") }}',
                               '{{ ti.xcom_pull(task_ids="get_data",key="hydraulicpressure") }}',
                               '{{ ti.xcom_pull(task_ids="get_data",key="temperature") }}',
                               '{{ ti.xcom_pull(task_ids="get_data",key="timestamp") }}'
                               ),
                               sql = '''INSERT INTO sensors (idtemp, powerfactor, 
                               hydraulicpressure, temperature, timestamp)
                               VALUES (%s, %s, %s, %s, %s);''',
                               task_group = group_database,
                               dag=dag)