from iot_pm.schemas import SensorReading,utc_now
from iot_pm.ml.alerts import score_rules

def test_hot_vibrating_motor():
    x=SensorReading(machine_id="a",timestamp=utc_now(),temperature_c=98,vibration_mm_s=7,pressure_bar=8,rpm=1800,operating_hours=120)
    alert=score_rules(x)
    assert alert.severity=="high"
    assert len(alert.reasons)==2

def test_healthy_motor():
    x=SensorReading(machine_id="a",timestamp=utc_now(),temperature_c=66,vibration_mm_s=2,pressure_bar=8,rpm=1700,operating_hours=120)
    assert score_rules(x).severity=="low"
