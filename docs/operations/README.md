# Operations runbook

## Local development
Install dependencies with `pip install -e '.[stream,api,dashboard,dev]'`. Run `pytest`. Start Kafka with `docker compose up -d kafka` then `bash scripts/create_topics.sh`; producer via `python -m iot_pm.streaming.producer --count 100`. Run API with `uvicorn iot_pm.api.app:app --reload`. Dashboard: `streamlit run src/iot_pm/dashboard/app.py`.

Spark requires a Spark distribution and a version-compatible Kafka connector; it is not automatically provisioned by the sample Python Docker image. Use `bash scripts/run_spark.sh` on a configured Spark host.

## Incident response
Record machine ID, event timestamp, raw sensor values, scoring configuration and alert ID; verify sensor calibration, look for missing Kafka offsets, check Spark checkpoint continuity, and notify a human maintenance operator. Never automatically shut down physical machines from this sample system.

## Observability
Monitor Kafka consumer lag, dropped/malformed records, Spark batch duration, checkpoint age, inference latency, API 5xx errors and per-machine false alert rates. Enforce TLS/SASL/RBAC and secret management before production use.
