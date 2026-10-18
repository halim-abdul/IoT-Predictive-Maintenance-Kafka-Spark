"""Publish well-formed synthetic industrial events to Kafka."""
import argparse
import json
import time
from kafka import KafkaProducer
from iot_pm.config import settings
from iot_pm.simulation.generator import simulate

def publish(count: int = 100, interval: float = 1.0, machines: int = 5) -> int:
    producer = KafkaProducer(bootstrap_servers=settings.kafka_bootstrap_servers.split(","), value_serializer=lambda v: json.dumps(v).encode(), retries=5, acks="all")
    sent = 0
    try:
        # count=0 produces indefinitely in batches, for demo streaming.
        while count == 0 or sent < count:
            batch = simulate(n=min(100, (count-sent) if count else 100), machines=machines, seed=42+sent)
            for event in batch.to_dict("records"):
                event["timestamp"] = event["timestamp"].isoformat()
                producer.send(settings.kafka_sensor_topic, key=event["machine_id"].encode(), value=event)
                sent += 1
                time.sleep(max(interval, 0))
            producer.flush()
    finally:
        producer.close()
    return sent

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--count", type=int, default=100)
    p.add_argument("--interval", type=float, default=0.1)
    p.add_argument("--machines", type=int, default=5)
    args = p.parse_args()
    print("Published", publish(args.count,args.interval,args.machines), "events")
if __name__ == "__main__":
    main()
