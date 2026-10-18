"""Contract shared across producer, Spark and inference services."""
from datetime import datetime, timezone
from typing import Literal
from pydantic import BaseModel, Field, ConfigDict

class SensorReading(BaseModel):
    model_config = ConfigDict(extra="forbid")
    machine_id: str = Field(min_length=1)
    timestamp: datetime
    temperature_c: float = Field(ge=-100, le=300)
    vibration_mm_s: float = Field(ge=0, le=100)
    pressure_bar: float = Field(ge=0, le=500)
    rpm: float = Field(ge=0, le=100000)
    operating_hours: float = Field(ge=0)
    failure: int = Field(default=0, ge=0, le=1)

class MaintenanceAlert(BaseModel):
    machine_id: str
    timestamp: datetime
    anomaly_score: float = Field(ge=0, le=1)
    severity: Literal["low","medium","high","critical"]
    reasons: list[str]
    model_version: str = "baseline-heuristic-v1"

def utc_now() -> datetime:
    return datetime.now(timezone.utc)
