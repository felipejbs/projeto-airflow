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