from airflow import DAG
from airflow.operators.python.operator import PythonOperator
from airflow.operators.python.operator import BranchPythonOperator
from airflow.operators.email.operator import EmailOperator
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
