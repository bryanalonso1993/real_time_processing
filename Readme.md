#### Real time processing

##### Requisitos Previos:

1) Crear imagen customizada de Apache Spark

```
@bryanalonso1993 ➜ /workspaces/real_time_processing (main) $ ls
Readme.md  docker-compose.yaml  dumps  register-mysql.json  spark_custom_image
@bryanalonso1993 ➜ /workspaces/real_time_processing (main) $ cd spark_custom_image/
@bryanalonso1993 ➜ /workspaces/real_time_processing/spark_custom_image (main) $ ls
Dockerfile  start-spark.sh
@bryanalonso1993 ➜ /workspaces/real_time_processing/spark_custom_image (main) $ docker build -t apache-spark:v1 .
[+] Building 162.3s (13/13) FINISHED                                                                                                                                     docker:default
 => [internal] load build definition from Dockerfile                                                                                                                               0.2s
 => => transferring dockerfile: 1.44kB                                                                                                                                             0.0s
 => [internal] load metadata for docker.io/library/openjdk:11.0.11-jre-slim-buster                                                                                                 0.7s
 => [auth] library/openjdk:pull token for registry-1.docker.io                                                                                                                     0.0s
```
2) Crear la imagen de apache airflow

```
@bryanalonso1993 ➜ /workspaces/real_time_processing (main) $ cd airflow_custom_image/
@bryanalonso1993 ➜ /workspaces/real_time_processing/airflow_custom_image (main) $ ls
Dockerfile  requirements.txt start.sh
@bryanalonso1993 ➜ /workspaces/real_time_processing/airflow_custom_image (main) $ docker build -t apache-airflow:v1 .
[+] Building 0.7s (12/12) FINISHED                                                                                   docker:default
                                                                       0.0s
```

3) Desplegar la aplicación con docker compose.

```
@bryanalonso1993 ➜ /workspaces/real_time_processing (main) $ docker compose up -d
WARN[0000] /workspaces/real_time_processing/docker-compose.yaml: `version` is obsolete 
[+] Running 88/6
 ✔ jupyter Pulled                                                                                                             86.5s 
 ✔ mysql Pulled                                                                                                               54.2s 
 ✔ zookeeper Pulled                                                                                                           63.9s 
 ✔ kafka Pulled                                                                                                               64.0s 
 ✔ akhq Pulled                                                                                                                63.7s 
 ✔ debezium Pulled                                                                                                            74.6s 
[+] Running 9/9
 ✔ Container spark-master        Started                                                                                       4.3s 
 ✔ Container jupyter-notebook    Started                                                                                       4.3s 
 ✔ Container airflow-standalone  Started                                                                                       4.3s 
 ✔ Container mysql-container     Started                                                                                       4.1s 
 ✔ Container zookeeper           Started                                                                                       4.1s 
 ✔ Container kafka               Started                                                                                       4.5s 
 ✔ Container spark-worker        Started                                                                                       4.8s 
 ✔ Container debezium            Started                                                                                       5.5s 
 ✔ Container ui-kafka            Started  
```

4) En el contenedor de airflow creamos un usuario con el rol Admin.

```
@bryanalonso1993 ➜ /workspaces/real_time_processing (main) $ docker exec -it airflow-standalone bash
airflow@477716bfad36:/opt/airflow$ 
airflow@477716bfad36:/opt/airflow$ 
airflow@477716bfad36:/opt/airflow$ airflow users create --username bryan --firstname Bryan --lastname Almeyda --email balmeyda@uni.pe --role Admin --password claro123
/home/airflow/.local/lib/python3.11/site-packages/flask_limiter/extension.py:333 UserWarning: Using the in-memory storage for tracking rate limits as no storage was explicitly specified. This is not recommended for production use. See: https://flask-limiter.readthedocs.io#configuring-a-storage-backend for documentation about configuring the storage backend.
[2024-07-06T12:34:20.495-0500] {override.py:1516} INFO - Added user bryan
User "bryan" created with role "Admin"
airflow@477716bfad36:/opt/airflow$ 
```

5) Crear la conexión desde Airflow a la base de datos.

<img title="Crear registro pelicula" alt="Alt text" src="./img/conexion_mysql_airflow.png">


6) Crear variable que determina la tabla a poblar.

<img title="Crear registro pelicula" alt="Alt text" src="./img/crear_variable_airflow.png">


7) Ejecutar el DAG crear_tablas_sistema_ventas en irflow. 

<img title="Crear tabla sistema de ventas" alt="Alt text" src="./img/crear_tabla_sistema_ventas.png">

8) Crear el conector de Debezium.

```
@bryanalonso1993 ➜ /workspaces/real_time_processing (main) $ curl -i -X POST -H "Accept:application/json" -H "Content-Type:application/json" http://localhost:8083/connectors/ -d @register-mysql.json
HTTP/1.1 201 Created
Date: Sun, 30 Jun 2024 22:36:49 GMT
Location: http://localhost:8083/connectors/mysql-connector
Content-Type: application/json
Content-Length: 566
Server: Jetty(9.4.52.v20230823)

{"name":"mysql-connector","config":{"connector.class":"io.debezium.connector.mysql.MySqlConnector","tasks.max":"1","database.hostname":"mysql-container","database.port":"3306","database.user":"root","database.password":"Changeme123","database.server.id":"184054","database.server.name":"datapath","database.include.list":"datapath","schema.history.internal.kafka.bootstrap.servers":"kafka:9092","schema.history.internal.kafka.topic":"schema-changes.datapath","include.schema.changes":"true","topic.prefix":"oltp","name":"mysql-connector"},"tasks":[],"type":"source"}
```
 
##### Prueba Funcional:

9) Ejecutar DAG pobla la base de datos.

* Producto
<img title="Crear tabla sistema de ventas" alt="Alt text" src="./img/poblar_tabla_producto.png">

* Pedido
<img title="Crear tabla sistema de ventas" alt="Alt text" src="./img/poblar_tabla_pedido.png">

10) Validar UI Kafka.

<img title="Crear tabla sistema de ventas" alt="Alt text" src="./img/kafka_ui.png">

11) Procesamiento en Spark

```
    root@9360c8613bfb:/opt/spark# ./bin/spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1 /opt/spark-apps/process_data_pedido.py

    24/07/07 11:49:57 INFO DAGScheduler: Got job 1 (showString at <unknown>:0) with 1 output partitions
24/07/07 11:49:57 INFO DAGScheduler: Final stage: ResultStage 2 (showString at <unknown>:0)
24/07/07 11:49:57 INFO DAGScheduler: Parents of final stage: List(ShuffleMapStage 1)
24/07/07 11:49:57 INFO DAGScheduler: Missing parents: List()
24/07/07 11:49:57 INFO DAGScheduler: Submitting ResultStage 2 (MapPartitionsRDD[13] at showString at <unknown>:0), which has no missing parents
24/07/07 11:49:57 INFO MemoryStore: Block broadcast_1 stored as values in memory (estimated size 64.6 KiB, free 434.2 MiB)
24/07/07 11:49:57 INFO MemoryStore: Block broadcast_1_piece0 stored as bytes in memory (estimated size 26.1 KiB, free 434.2 MiB)
24/07/07 11:49:57 INFO BlockManagerInfo: Added broadcast_1_piece0 in memory on 9360c8613bfb:35729 (size: 26.1 KiB, free: 434.3 MiB)
24/07/07 11:49:57 INFO SparkContext: Created broadcast 1 from broadcast at DAGScheduler.scala:1585
24/07/07 11:49:57 INFO DAGScheduler: Submitting 1 missing tasks from ResultStage 2 (MapPartitionsRDD[13] at showString at <unknown>:0) (first 15 tasks are for partitions Vector(0))
24/07/07 11:49:57 INFO TaskSchedulerImpl: Adding task set 2.0 with 1 tasks resource profile 0
24/07/07 11:49:57 INFO TaskSetManager: Starting task 0.0 in stage 2.0 (TID 1) (9360c8613bfb, executor driver, partition 0, NODE_LOCAL, 9664 bytes) 
24/07/07 11:49:57 INFO Executor: Running task 0.0 in stage 2.0 (TID 1)
24/07/07 11:49:57 INFO ShuffleBlockFetcherIterator: Getting 1 (313.0 B) non-empty blocks including 1 (313.0 B) local and 0 (0.0 B) host-local and 0 (0.0 B) push-merged-local and 0 (0.0 B) remote blocks
24/07/07 11:49:57 INFO ShuffleBlockFetcherIterator: Started 0 remote fetches in 21 ms
24/07/07 11:49:57 INFO BlockManagerInfo: Removed broadcast_0_piece0 on 9360c8613bfb:35729 in memory (size: 25.5 KiB, free: 434.4 MiB)
24/07/07 11:49:57 INFO CodeGenerator: Code generated in 43.612415 ms
24/07/07 11:49:57 INFO Executor: Finished task 0.0 in stage 2.0 (TID 1). 5247 bytes result sent to driver
24/07/07 11:49:57 INFO TaskSetManager: Finished task 0.0 in stage 2.0 (TID 1) in 317 ms on 9360c8613bfb (executor driver) (1/1)
24/07/07 11:49:57 INFO DAGScheduler: ResultStage 2 (showString at <unknown>:0) finished in 0.368 s
24/07/07 11:49:57 INFO DAGScheduler: Job 1 is finished. Cancelling potential speculative or zombie tasks for this job
24/07/07 11:49:57 INFO TaskSchedulerImpl: Removed TaskSet 2.0, whose tasks have all completed, from pool 
24/07/07 11:49:57 INFO TaskSchedulerImpl: Killing all running tasks in stage 2: Stage finished
24/07/07 11:49:57 INFO DAGScheduler: Job 1 finished: showString at <unknown>:0, took 0.409657 s
24/07/07 11:49:57 INFO CodeGenerator: Code generated in 23.220101 ms
+-------+-----+
| region|count|
+-------+-----+
| Africa| 2957|
|Oceanía|  686|
| Europa| 2700|
|America| 5212|
|   Asia| 3197|
+-------+-----+

None
24/07/07 11:49:57 INFO SparkContext: SparkContext is stopping with exitCode 0.
24/07/07 11:49:57 INFO SparkUI: Stopped Spark web UI at http://9360c8613bfb:4040
24/07/07 11:49:57 INFO MapOutputTrackerMasterEndpoint: MapOutputTrackerMasterEndpoint stopped!

```
