import pytest
from pydantic import ValidationError
from iot_pm.schemas import SensorReading, utc_now

def example():
    return dict(machine_id="motor-001",timestamp=utc_now(),temperature_c=70,vibration_mm_s=2,pressure_bar=8,rpm=1800,operating_hours=20)

def test_valid_sample():
    assert SensorReading(**example()).machine_id == "motor-001"

def test_reject_negative_vibration():
    with pytest.raises(ValidationError):
        SensorReading(**(example() | {"vibration_mm_s": -0.1}))

def test_reject_invalid_failure_label():
    with pytest.raises(ValidationError):
        SensorReading(**(example() | {"failure": 2}))
