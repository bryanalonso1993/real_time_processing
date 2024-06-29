#!/usr/env bin pyspark
from pyspark.sql import SparkSession
from datetime import datetime

# ./bin/spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1 /opt/spark-apps/process_data.py

# fecha de ejecucion
date_now = datetime.now().strftime("%Y-%m-%d")

print(f"Fecha de ejecucion { date_now }")

spark = SparkSession.builder.appName("Time Series Procesor").getOrCreate()

# Subscribe multiple topics
topics = "oltp.netflix.Gender,oltp.netflix.Movie,oltp.netflix.Movie_Gender,oltp.netflix.Participant,oltp.netflix.Person"

# topics = "oltp.netflix.Movie"

df = spark \
    .read \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", topics) \
    .load()

df.show()

df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)").show()

spark.stop()

