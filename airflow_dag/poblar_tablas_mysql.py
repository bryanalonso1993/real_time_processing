#!/usr/env bin python
from airflow.utils.dates import days_ago
from datetime import datetime
from airflow import DAG

# Operador MySQL para crear los esquemas
from airflow.operators.mysql_operator import MySqlOperator
from airflow.operators.python import PythonOperator
import pandas as pd

DATAFILE_PEDIDOS = "/opt/airflow/repository/DATA_PEDIDOS.xlsx"

default_args = {
    'owner': 'Bryan Alonso'
}

def read_xlsx_file():
    df = pd.read_excel(DATAFILE_PEDIDOS, header=0, date_format=True)
    return df

def data_wrangling(ti):
    df = ti.xcom_pull(task_ids="read_xlsx_file")
    df = df.drop(['TELE', 'DIR', 'TIPVTA', 'FECFACTURA'], axis=1)
    df = df.drop(df[(df.EDAD > 100)].index)
    return df

def print_df(ti):
    df = ti.xcom_pull(task_ids="data_wrangling")
    print(df.head())

with DAG(
    dag_id="poblar_base_datos",
    description="pipeline para poblar la base de datos",
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval="@once",
    tags=['pipeline', 'mysql', 'dataset', 'sistema_ventas']
) as dag:
    task_A = PythonOperator(
        task_id="read_xlsx_file",
        python_callable=read_xlsx_file
    )

    task_B = PythonOperator(
        task_id="clean_dataframe",
        python_callable=data_wrangling
    )

    task_C = PythonOperator(
        task_id="print_df",
        python_callable=print_df
    )

task_A >> task_B >> task_C
