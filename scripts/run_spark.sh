#!/usr/bin/env bash
set -euo pipefail
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.3 src/iot_pm/streaming/spark_job.py --checkpoint checkpoint/sensors
