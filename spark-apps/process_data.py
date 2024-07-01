#!/usr/env bin pyspark
from pyspark.sql import SparkSession
from datetime import datetime
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, LongType, NullType
from pyspark.sql.functions import from_json, col

# ./bin/spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1 /opt/spark-apps/process_data.py

# fecha de ejecucion
date_now = datetime.now().strftime("%Y-%m-%d")

print(f"Fecha de ejecucion { date_now }")

# instancia de Spark
spark = SparkSession.builder.appName("Time Series Procesor").getOrCreate()

# Subscribe multiple topics

# topics = "oltp.netflix.Gender,oltp.netflix.Movie,oltp.netflix.Movie_Gender,oltp.netflix.Participant,oltp.netflix.Person"

topics = "oltp.datapath.cliente"

df = spark \
    .read \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", topics) \
    .load()

json_schema = StructType([
    StructField("before", NullType()),
    StructField("after", StructType([
        StructField("id_cliente", IntegerType()),
        StructField("uuid_cliente", StringType()),
        StructField("nombre_cliente", StringType()),
        StructField("edad", IntegerType()),
        StructField("genero", StringType())
    ])),
    StructField("source", StructType([
        StructField("version", StringType()),
        StructField("connector", StringType()),
        StructField("name", StringType()),
        StructField("ts_ms", LongType()),
        StructField("snapshot", StringType()),
        StructField("db", StringType()),
        StructField("sequence", NullType()),
        StructField("table", StringType()),
        StructField("server_id", IntegerType()),
        StructField("gtid", NullType()),
        StructField("file", StringType()),
        StructField("pos", IntegerType()),
        StructField("row", IntegerType()),
        StructField("thread", NullType()),
        StructField("query", NullType())
    ])),
    StructField("op", StringType()),
    StructField("ts_ms", LongType()),
    StructField("transaction", NullType())
])

df_values = df.selectExpr("CAST(value AS STRING) AS json").select(from_json(col("json"), json_schema).alias("data")).select("data.*")

processed_df = df_values.select("after.*").groupBy("nombre_cliente").count()

print("Esto es una prueba de Spark")

print(processed_df.show())

spark.stop()
