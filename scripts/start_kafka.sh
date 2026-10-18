#!/usr/bin/env bash
set -euo pipefail
docker compose up -d kafka
echo "Kafka host endpoint: localhost:9092"
