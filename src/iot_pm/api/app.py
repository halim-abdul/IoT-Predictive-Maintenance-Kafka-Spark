"""FastAPI service exposing rule-based scores and liveness."""
from fastapi import FastAPI
from iot_pm.schemas import SensorReading, MaintenanceAlert
from iot_pm.ml.alerts import score_rules

app=FastAPI(title="Industrial IoT Predictive Maintenance",version="0.1.0",description="Research API; rule scores are not calibrated failure probabilities")

@app.get("/health")
def health():
    return {"status":"ok","model":"rules-v1"}

@app.post("/alerts/score",response_model=MaintenanceAlert)
def score(reading:SensorReading):
    return score_rules(reading)

@app.get("/models")
def models():
    return {"available":["rules-v1"],"trained_model_loaded":False,"disclaimer":"synthetic demo only"}
