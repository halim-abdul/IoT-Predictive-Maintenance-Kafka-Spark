"""Isolation Forest anomaly detection; scores rescaled for demo display."""
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from iot_pm.features import build_features

def fit_anomaly_model(frame: pd.DataFrame, contamination: float = .05, seed: int = 42):
    if not 0 < contamination < .5:
        raise ValueError("contamination must be between 0 and 0.5")
    model = Pipeline([("imputer",SimpleImputer(strategy="median")),("forest",IsolationForest(n_estimators=200,contamination=contamination,random_state=seed))])
    model.fit(build_features(frame))
    return model

def anomaly_raw_score(model, frame: pd.DataFrame):
    return -model.decision_function(build_features(frame))

def anomaly_flags(model, frame: pd.DataFrame):
    return model.predict(build_features(frame)) == -1
