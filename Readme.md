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
 => [internal] load .dockerignore                                          
```

2) 