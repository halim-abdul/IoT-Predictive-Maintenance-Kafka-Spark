PYTHON ?= python
.PHONY: install test lint demo simulate api dashboard up down
install:
	$(PYTHON) -m pip install -e '.[stream,api,dashboard,dev]'
test:
	$(PYTHON) -m pytest -q
lint:
	ruff check src tests
demo:
	$(PYTHON) -m iot_pm.simulation.generator --records 1000 --output data/sample/sensors.csv
simulate:
	$(PYTHON) -m iot_pm.streaming.producer --count 100
api:
	uvicorn iot_pm.api.app:app --reload
dashboard:
	streamlit run src/iot_pm/dashboard/app.py
up:
	docker compose up -d --build
down:
	docker compose down
