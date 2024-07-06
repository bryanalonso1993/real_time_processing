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
    dag_id="crear_tablas_sistema_ventas",
    description="Realizar operaciones en Mysql para crear las tablas para el sistema de ventas",
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval="@daily",
    tags=["pipeline", "mysql"]
) as dag:
    task_A = MySqlOperator(
        task_id="create_table_cliente",
        mysql_conn_id="mysql_local_connector",
        sql = '''
            CREATE TABLE IF NOT EXISTS `cliente` (
              `id_cliente` int NOT NULL AUTO_INCREMENT,
              `uuid_cliente` varchar(50) NOT NULL,
              `nombre_cliente` varchar(255) DEFAULT NULL,
              `edad` int DEFAULT NULL,
              `genero` varchar(10) DEFAULT NULL,
              PRIMARY KEY (`id_cliente`,`uuid_cliente`),
              UNIQUE KEY `uuid_cliente` (`uuid_cliente`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        '''
    )

    task_B = MySqlOperator(
        task_id="create_table_pedido",
        mysql_conn_id="mysql_local_connector",
        sql='''
            CREATE TABLE IF NOT EXISTS `pedido` (
              `id_pedido` int NOT NULL AUTO_INCREMENT,
              `uuid_pedido` varchar(50) NOT NULL,
              `estado` varchar(20) DEFAULT NULL,
              `region` varchar(255) DEFAULT NULL,
              `categoria` varchar(255) DEFAULT NULL,
              `cantidad` int DEFAULT NULL,
              `descuento` float DEFAULT NULL,
              PRIMARY KEY (`id_pedido`,`uuid_pedido`),
              UNIQUE KEY `uuid_pedido` (`uuid_pedido`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        '''
    )

    task_C = MySqlOperator(
        task_id="create_table_producto",
        mysql_conn_id="mysql_local_connector",
        sql='''
            CREATE TABLE IF NOT EXISTS `producto` (
              `id_producto` int NOT NULL AUTO_INCREMENT,
              `uuid_producto` varchar(50) NOT NULL,
              `nombre_producto` varchar(255) DEFAULT NULL,
              `precio` float DEFAULT NULL,
              `igv` float DEFAULT NULL,
              PRIMARY KEY (`id_producto`,`uuid_producto`),
              UNIQUE KEY `uuid_producto` (`uuid_producto`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        '''
    )
    
    task_D = MySqlOperator(
        task_id="create_table_fecha",
        mysql_conn_id="mysql_local_connector",
        sql='''
            CREATE TABLE IF NOT EXISTS `fecha` (
              `id_fecha` int NOT NULL AUTO_INCREMENT,
              `uuid_fecha` varchar(50) NOT NULL,
              `fec_pedido` date DEFAULT NULL,
              `fec_prime` date DEFAULT NULL,
              `fec_vto` date DEFAULT NULL,
              `fec_mora` date DEFAULT NULL,
              `anio` int DEFAULT NULL,
              `mes` int DEFAULT NULL,
              `dia` int DEFAULT NULL,
              `mes_nombre` varchar(50) DEFAULT NULL,
              `trimestre` smallint DEFAULT NULL,
              `semestre` smallint DEFAULT NULL,
              PRIMARY KEY (`id_fecha`,`uuid_fecha`),
              UNIQUE KEY `uuid_fecha` (`uuid_fecha`)
            ) ENGINE=InnoDB AUTO_INCREMENT=14753 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        '''
    )

    task_E = MySqlOperator(
        task_id="create_table_sistema_ventas",
        mysql_conn_id="mysql_local_connector",
        sql='''
            CREATE TABLE IF NOT EXISTS `sistema_ventas` (
              `id_venta` int NOT NULL AUTO_INCREMENT,
              `cliente_id_cliente` varchar(50) NOT NULL,
              `pedido_id_pedido` varchar(50) NOT NULL,
              `fecha_id_fecha` varchar(50) NOT NULL,
              `producto_id_producto` varchar(50) NOT NULL,
              PRIMARY KEY (`id_venta`),
              KEY `cliente_id_cliente` (`cliente_id_cliente`),
              KEY `pedido_id_pedido` (`pedido_id_pedido`),
              KEY `fecha_id_fecha` (`fecha_id_fecha`),
              KEY `producto_id_producto` (`producto_id_producto`),
              CONSTRAINT `sistema_ventas_ibfk_1` FOREIGN KEY (`cliente_id_cliente`) REFERENCES `cliente` (`uuid_cliente`),
              CONSTRAINT `sistema_ventas_ibfk_2` FOREIGN KEY (`pedido_id_pedido`) REFERENCES `pedido` (`uuid_pedido`),
              CONSTRAINT `sistema_ventas_ibfk_3` FOREIGN KEY (`fecha_id_fecha`) REFERENCES `fecha` (`uuid_fecha`),
              CONSTRAINT `sistema_ventas_ibfk_4` FOREIGN KEY (`producto_id_producto`) REFERENCES `producto` (`uuid_producto`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        '''
    )

task_A >> task_B >> task_C >> task_D >> task_E
