#### Real time processing

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

2) Desplegar la aplicación con docker compose

```
@bryanalonso1993 ➜ /workspaces/real_time_processing (main) $ docker compose up -d 
WARN[0000] /workspaces/real_time_processing/docker-compose.yaml: `version` is obsolete 
[+] Running 88/6
 ✔ mysql Pulled                                                                                                                                                                                                              47.9s 
 ✔ akhq Pulled                                                                                                                                                                                                               56.0s 
 ✔ debezium Pulled                                                                                                                                                                                                           75.7s 
 ✔ zookeeper Pulled                                                                                                                                                                                                          65.7s 
 ✔ jupyter Pulled                                                                                                                                                                                                            84.6s 
 ✔ kafka Pulled                                                                                                                                                                                                              65.7s 
[+] Running 11/11
 ✔ Network real_time_processing_net_deployment    Created                                                                                                                                                                     0.1s 
 ✔ Volume "real_time_processing_mysql_data"       Created                                                                                                                                                                     0.0s 
 ✔ Volume "real_time_processing_jupyter_storage"  Created                                                                                                                                                                     0.0s 
 ✔ Container jupyter-notebook                     Started                                                                                                                                                                     2.5s 
 ✔ Container mysql-container                      Started                                                                                                                                                                     2.4s 
 ✔ Container spark-master                         Started                                                                                                                                                                     2.5s 
 ✔ Container zookeeper                            Started                                                                                                                                                                     2.5s 
 ✔ Container spark-worker                         Started                                                                                                                                                                     3.7s 
 ✔ Container kafka                                Started                                                                                                                                                                     3.2s 
 ✔ Container ui-kafka                             Started                                                                                                                                                                     4.3s 
 ✔ Container debezium                             Started   
```

3) En Jupyter se encuentra el script para poblar las tablas.

```

```

4) Crear el conector de Debezium

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

