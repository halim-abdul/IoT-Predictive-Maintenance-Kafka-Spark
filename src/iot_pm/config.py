"""Environment-configurable service settings."""
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    kafka_bootstrap_servers: str = "localhost:9092"
    kafka_sensor_topic: str = "industrial.sensors"
    kafka_alert_topic: str = "industrial.alerts"
    kafka_consumer_group: str = "iot-pm"
    sensor_interval_seconds: float = 1.0
    anomaly_threshold: float = 0.75
    model_path: str = "artifacts/failure_model.joblib"

settings = Settings()
