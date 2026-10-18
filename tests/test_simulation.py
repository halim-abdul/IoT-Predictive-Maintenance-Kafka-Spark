import pytest
from iot_pm.simulation.generator import simulate

def test_determinism():
    a, b = simulate(50, seed=14), simulate(50, seed=14)
    assert a.equals(b)

def test_different_seed():
    assert not simulate(30, seed=1).equals(simulate(30, seed=2))

def test_bounds_and_shape():
    df = simulate(101, machines=4)
    assert len(df) == 101
    assert df["machine_id"].nunique() == 4
    assert (df["vibration_mm_s"] >= 0).all()

def test_invalid_size():
    with pytest.raises(ValueError):
        simulate(0)
