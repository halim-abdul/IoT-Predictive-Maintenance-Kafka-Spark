import numpy as np
import pytest
from iot_pm.simulation.generator import simulate
from iot_pm.ml.anomaly import fit_anomaly_model,anomaly_flags
from iot_pm.ml.rul import make_rul_targets
from iot_pm.ml.failure import train_classifier

def test_anomaly_shapes():
    df=simulate(80)
    m=fit_anomaly_model(df)
    assert len(anomaly_flags(m,df))==80

def test_rul_targets_nonnegative():
    df=simulate(250)
    r=make_rul_targets(df)
    assert (r.dropna()>=0).all()

def test_failure_training():
    df=simulate(600)
    m,metrics=train_classifier(df)
    assert metrics["n_test"]>0
    assert 0<=metrics["average_precision"]<=1
