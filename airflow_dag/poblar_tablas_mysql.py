#!/usr/env bin python
from airflow.utils.dates import days_ago
from airflow import DAG

from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.hooks.base_hook import BaseHook
from airflow.models import Variable

from sqlalchemy import create_engine
from datetime import datetime
import pandas as pd
import numpy as np
import uuid


DATAFILE_PEDIDOS = "/opt/airflow/repository/DATA_PEDIDOS.xlsx"

default_args = {
    'owner': 'Bryan Alonso'
}

def leer_xlsx():
    df = pd.read_excel(DATAFILE_PEDIDOS, header=0, date_format=True)
    return df.to_json()

def limpiar_dataframe(ti):
    json_data = ti.xcom_pull(task_ids='leer_xlsx')
    df = pd.read_json(json_data)
    df = df.drop(['TELE', 'DIR', 'TIPVTA', 'FECFACTURA'], axis=1)
    df = df.drop(df[(df.EDAD > 100)].index)
    return df.to_json()

def crear_df_pedido(ti):
    json_data = ti.xcom_pull(task_ids='limpiar_dataframe')
    df = pd.read_json(json_data)
    df_pedido = df[['ESTADO', 'REGION', 'CATE', 'CANT','DSCTO']]
    df_pedido['uuid'] = np.array([str(uuid.uuid4()) for _ in range(len(df_pedido.index))])
    df_pedido = df_pedido.rename(columns={ 'ESTADO':'estado', 'REGION': 'region', 'CATE': 'categoria', 'uuid': 'uuid_pedido', 'CANT': 'cantidad', 'DSCTO': 'descuento' })
    return df_pedido.to_json()

def insertar_df_pedido_mysql(ti):
    json_data = ti.xcom_pull(task_ids='crear_df_pedido')
    df = pd.read_json(json_data)
    mysql_conn = BaseHook.get_connection('mysql_local_connector')
    cnx_string = f'mysql+pymysql://{mysql_conn.login}:{mysql_conn.password}@{mysql_conn.host}:{mysql_conn.port}/{mysql_conn.schema}'
    engine = create_engine(cnx_string)
    df.to_sql(name='pedido', con=engine, if_exists='append', index=False)

def crear_df_producto(ti):
    json_data = ti.xcom_pull(task_ids='leer_xlsx')
    df = pd.read_json(json_data)
    df_producto = df[['NOMPRO', 'PRECIO', 'IGV']]
    df_producto['uuid'] = np.array([str(uuid.uuid4()) for _ in range(len(df_producto.index))])
    df_producto = df_producto.rename(columns={ 'NOMPRO': 'nombre_producto', 'PRECIO': 'precio', 'IGV':'igv', 'uuid': 'uuid_producto' })
    return df_producto.to_json()

def insertar_df_producto_mysql(ti):
    json_data = ti.xcom_pull(task_ids='crear_df_producto')
    df = pd.read_json(json_data)
    mysql_conn = BaseHook.get_connection('mysql_local_connector')
    cnx_string = f'mysql+pymysql://{mysql_conn.login}:{mysql_conn.password}@{mysql_conn.host}:{mysql_conn.port}/{mysql_conn.schema}'
    engine = create_engine(cnx_string)
    df.to_sql(name='producto', con=engine, if_exists='append', index=False)

def determinar_flujo_a_cargar():
    transform_action = Variable.get("tabla_elegida", default_var=None)
    print(f" el flujo escogido es el siguiente: { transform_action }")
    if transform_action == 'pedido':
        return "crear_df_pedido"
    else:
        return "crear_df_producto"

with DAG(
    dag_id = "poblar_base_datos",
    description = "pipeline para poblar la base de datos",
    default_args = default_args,
    start_date = days_ago(1),
    schedule_interval = "@once",
    tags=['pipeline', 'mysql', 'dataset', 'sistema_ventas']
) as dag:
    task_A = PythonOperator(
        task_id="leer_xlsx",
        python_callable=leer_xlsx
    )

    task_B = PythonOperator(
        task_id="limpiar_dataframe",
        python_callable=limpiar_dataframe
    )
    
    task_filter = BranchPythonOperator(
        task_id="determinar_flujo_a_cargar",
        python_callable=determinar_flujo_a_cargar
    )

    task_C = PythonOperator(
        task_id="crear_df_pedido",
        python_callable=crear_df_pedido
    )

    task_D = PythonOperator(
        task_id="crear_df_producto",
        python_callable=crear_df_producto
    )

    task_E = PythonOperator(
        task_id="insertar_df_pedido_mysql",
        python_callable=insertar_df_pedido_mysql
    )

    task_F = PythonOperator(
        task_id="insertar_df_producto_mysql",
        python_callable=insertar_df_producto_mysql
    )

task_A >> task_B >> task_filter >> [task_C, task_D]

task_C >> task_E

task_D >> task_F
