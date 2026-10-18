"""RUL estimation from labeled run-to-failure histories; units follow time axis."""
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from iot_pm.features import build_features

def make_rul_targets(frame: pd.DataFrame, time_col="operating_hours"):
    if "machine_id" not in frame or "failure" not in frame:
        raise ValueError("RUL requires machine_id and observed failure events")
    ordered = frame.sort_values(["machine_id",time_col]).copy()
    targets = pd.Series(np.nan,index=ordered.index,dtype=float)
    for _, group in ordered.groupby("machine_id"):
        times = group[time_col].to_numpy()
        failures = group["failure"].to_numpy().astype(bool)
        for i,t in enumerate(times):
            upcoming = times[(times>=t)&failures]
            if len(upcoming):
                targets.at[group.index[i]]=max(0.0,float(upcoming[0]-t))
    return targets.reindex(frame.index)

def train_rul_model(frame: pd.DataFrame, seed=42):
    target=make_rul_targets(frame)
    valid=target.notna()
    if valid.sum()<5:
        raise ValueError("Need at least five observed run-to-failure readings")
    model=Pipeline([("imputer",SimpleImputer(strategy="median")),("regressor",RandomForestRegressor(n_estimators=150,random_state=seed,n_jobs=-1))])
    model.fit(build_features(frame.loc[valid]),target.loc[valid])
    return model

def predict_rul(model, frame: pd.DataFrame):
    return np.maximum(0, model.predict(build_features(frame)))
