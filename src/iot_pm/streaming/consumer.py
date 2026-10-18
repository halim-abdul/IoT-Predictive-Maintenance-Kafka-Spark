"""Diagnostic Kafka consumer for alert events."""
import json
from kafka import KafkaConsumer
from iot_pm.config import settings

def consume(topic: str | None = None):
    consumer = KafkaConsumer(topic or settings.kafka_alert_topic, bootstrap_servers=settings.kafka_bootstrap_servers.split(","), group_id=settings.kafka_consumer_group+"-diagnostic", auto_offset_reset="latest", value_deserializer=lambda b: json.loads(b.decode()))
    try:
        for message in consumer:
            yield message.value
    finally:
        consumer.close()

if __name__ == "__main__":
    for event in consume():
        print(json.dumps(event, indent=2))
