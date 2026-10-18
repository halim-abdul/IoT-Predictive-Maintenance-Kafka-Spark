#!/usr/bin/env bash
set -euo pipefail
for topic in industrial.sensors industrial.alerts; do
  docker compose exec -T kafka /opt/kafka/bin/kafka-topics.sh --bootstrap-server kafka:9092 --create --if-not-exists --topic "$topic" --partitions 3 --replication-factor 1
done
