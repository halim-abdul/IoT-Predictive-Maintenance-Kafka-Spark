from fastapi.testclient import TestClient
from iot_pm.api.app import app

def test_health():
    r=TestClient(app).get("/health")
    assert r.status_code==200 and r.json()["status"]=="ok"

def test_api_validation():
    r=TestClient(app).post("/alerts/score",json={"machine_id":"m"})
    assert r.status_code==422

def test_models_are_labeled():
    assert TestClient(app).get("/models").json()["trained_model_loaded"] is False
