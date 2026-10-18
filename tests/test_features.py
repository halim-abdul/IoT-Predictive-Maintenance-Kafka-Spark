import pandas as pd
import pytest
from iot_pm.features import build_features, FEATURE_NAMES

def test_feature_order_and_values():
    f = build_features(pd.DataFrame([dict(temperature_c=75,vibration_mm_s=3,pressure_bar=10,rpm=2000,operating_hours=100)]))
    assert list(f) == list(FEATURE_NAMES)
    assert f.loc[0, "thermal_load"] == 150
    assert f.loc[0, "vibration_energy"] == 9
    assert f.loc[0, "pressure_deviation"] == 2

def test_missing_feature():
    with pytest.raises(ValueError):
        build_features(pd.DataFrame({"rpm":[2]}))
