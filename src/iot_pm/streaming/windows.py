"""Spark windowed aggregation utilities."""
def rolling_health(stream, window_duration="5 minutes", watermark="2 minutes"):
    from pyspark.sql.functions import window, avg, max as spark_max, count
    return (stream.withWatermark("event_time",watermark)
            .groupBy("machine_id",window("event_time",window_duration))
            .agg(avg("temperature_c").alias("mean_temperature_c"),
                 avg("vibration_mm_s").alias("mean_vibration_mm_s"),
                 spark_max("vibration_mm_s").alias("peak_vibration_mm_s"),
                 count("*").alias("n_events")))
