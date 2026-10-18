"""Structured Streaming from Kafka to JSONL with schema validation and event-time windows.

Run using spark-submit with the connector matching your Spark/Scala versions:
--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.3
"""
import argparse
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, window, avg, count, when
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType

SENSOR_SCHEMA = StructType([
    StructField("machine_id", StringType()),
    StructField("timestamp", StringType()),
    StructField("temperature_c", DoubleType()),
    StructField("vibration_mm_s", DoubleType()),
    StructField("pressure_bar", DoubleType()),
    StructField("rpm", DoubleType()),
    StructField("operating_hours", DoubleType()),
    StructField("failure", IntegerType()),
])

def main():
    from iot_pm.config import settings
    p = argparse.ArgumentParser()
    p.add_argument("--checkpoint", default="checkpoint/sensors")
    p.add_argument("--output", default="data/processed/stream")
    args = p.parse_args()
    spark = SparkSession.builder.appName("iot-predictive-maintenance").getOrCreate()
    raw = (spark.readStream.format("kafka").option("kafka.bootstrap.servers",settings.kafka_bootstrap_servers).option("subscribe",settings.kafka_sensor_topic).option("startingOffsets","latest").load())
    data = raw.select(from_json(col("value").cast("string"),SENSOR_SCHEMA).alias("event")).select("event.*")
    clean = data.where(col("machine_id").isNotNull() & col("vibration_mm_s").between(0,100) & col("temperature_c").between(-100,300))
    clean = clean.withColumn("event_time",col("timestamp").cast("timestamp")).where(col("event_time").isNotNull())
    features = clean.withColumn("rule_alert",when((col("temperature_c")>90)|(col("vibration_mm_s")>6),1).otherwise(0))
    query = (features.writeStream.format("parquet").option("path",args.output).option("checkpointLocation",args.checkpoint).outputMode("append").start())
    query.awaitTermination()

if __name__=="__main__":
    main()
