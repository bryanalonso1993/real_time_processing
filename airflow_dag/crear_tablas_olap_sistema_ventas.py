#!/usr/env bin python
from airflow.utils.dates import days_ago
from datetime import datetime
from airflow import DAG

# Operador MySQL para crear los esquemas
from airflow.operators.mysql_operator import MySqlOperator

default_args = {
    'owner': 'Bryan Alonso'
}

with DAG(
    dag_id="crear_tablas_olap_sistema_ventas",
    description="Realizar operaciones en Mysql para crear las tablas OLAP para el sistema de ventas",
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval="@daily",
    tags=["pipeline", "mysql", "olap"]
) as dag:
    task_A = MySqlOperator(
        task_id="create_table_cantidad_pedidos_region",
        mysql_conn_id="mysql_local_connector",
        sql = '''
            CREATE TABLE IF NOT EXISTS `cantidad_pedidos_region` (
              `region` varchar(255) NOT NULL,
              `categoria` varchar(255) DEFAULT NULL,
              `cantidad` int DEFAULT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
        '''
    )

task_A
