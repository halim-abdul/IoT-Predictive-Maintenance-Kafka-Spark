from iot_pm.ml.drift import population_stability_index

def test_same_distribution_has_low_drift():
    x=list(range(100))
    assert abs(population_stability_index(x,x))<1e-10

def test_shift_has_high_drift():
    x=list(range(100))
    assert population_stability_index(x,[v+50 for v in x])>0
