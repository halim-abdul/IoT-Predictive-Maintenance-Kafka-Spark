from iot_pm.schemas import SensorReading, utc_now

def test_kafka_json_roundtrip():
    v = SensorReading(machine_id="motor-001", timestamp=utc_now(),temperature_c=70,vibration_mm_s=2,pressure_bar=8,rpm=1700,operating_hours=15)
    assert SensorReading.model_validate_json(v.model_dump_json()) == v
