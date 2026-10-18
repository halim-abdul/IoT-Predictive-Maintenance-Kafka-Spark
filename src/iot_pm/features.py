"""Feature engineering used consistently for training and inference."""
import numpy as np
import pandas as pd

NUMERIC_FEATURES = ("temperature_c", "vibration_mm_s", "pressure_bar", "rpm", "operating_hours")

def validate_columns(df: pd.DataFrame) -> None:
    missing = set(NUMERIC_FEATURES) - set(df.columns)
    if missing:
        raise ValueError(f"Missing sensor columns: {sorted(missing)}")

def build_features(df: pd.DataFrame) -> pd.DataFrame:
    validate_columns(df)
    result = df.loc[:, NUMERIC_FEATURES].copy()
    for name in NUMERIC_FEATURES:
        result[name] = pd.to_numeric(result[name], errors="coerce")
    result["thermal_load"] = result["temperature_c"] * result["rpm"] / 1000
    result["vibration_energy"] = np.square(result["vibration_mm_s"])
    result["pressure_deviation"] = (result["pressure_bar"] - 8.0).abs()
    return result.replace([np.inf, -np.inf], np.nan)

FEATURE_NAMES = (*NUMERIC_FEATURES, "thermal_load", "vibration_energy", "pressure_deviation")
