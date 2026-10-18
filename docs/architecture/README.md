# Architecture and event contracts

Sensor simulation / edge adapters → Kafka `industrial.sensors` (keyed by machine_id) → Spark Structured Streaming → validated Parquet records → offline feature engineering and ML inference → maintenance alerts.

The source event has UTC timestamp, machine_id, temperature_c, vibration_mm_s, pressure_bar, rpm, operating_hours, and synthetic failure (training only). Production sensor input should omit any ground-truth failure label.

Use Kafka partitions for horizontal throughput; order is guaranteed *within a partition*, not globally. Spark checkpoints must be stored durably for restart safety. A restarted producer may cause duplicates; downstream storage and alert delivery should be idempotent.

## Alert routing
Score each reading using the rules or persisted ML model, group by machine, suppress duplicate alerts, and dispatch to a maintenance owner only after setting alert severity and explanation. Authentication and transport encryption are required before production deployment.

## Running
See repository root README for local installation and Docker commands. The Spark application requires the Kafka source JAR matching Spark and Scala versions; the Dockerfile is a Python demonstration base, not a preconfigured Spark runtime.
