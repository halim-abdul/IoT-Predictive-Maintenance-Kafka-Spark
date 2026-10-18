"""Auditable rule-based alert baseline; not a calibrated failure probability."""
from iot_pm.schemas import MaintenanceAlert, SensorReading

def score_rules(reading: SensorReading):
    reasons=[]
    if reading.temperature_c >= 90: reasons.append("temperature >= 90 C")
    if reading.vibration_mm_s >= 6: reasons.append("vibration >= 6 mm/s")
    if reading.pressure_bar < 5: reasons.append("pressure < 5 bar")
    if reading.rpm < 1200: reasons.append("rpm < 1200")
    score = min(1.0, len(reasons)*0.28)
    severity = "critical" if score>=.84 else "high" if score>=.56 else "medium" if score>=.28 else "low"
    return MaintenanceAlert(machine_id=reading.machine_id,timestamp=reading.timestamp,anomaly_score=score,severity=severity,reasons=reasons or ["No threshold violations detected"])
