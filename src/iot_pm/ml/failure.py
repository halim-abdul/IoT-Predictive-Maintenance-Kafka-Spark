"""Train and score a calibrated failure risk classifier."""
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import average_precision_score, roc_auc_score, classification_report, confusion_matrix
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GroupShuffleSplit, train_test_split
from iot_pm.features import build_features, FEATURE_NAMES

def train_classifier(frame: pd.DataFrame, *, seed: int = 42):
    if "failure" not in frame:
        raise ValueError("A failure label is required for supervised learning")
    X = build_features(frame)
    y = frame["failure"].astype(int)
    if y.nunique() < 2:
        raise ValueError("Need examples of both failure classes")
    if "machine_id" in frame and frame["machine_id"].nunique() >= 4:
        idx_train, idx_test = next(GroupShuffleSplit(test_size=.25,random_state=seed).split(X,y,groups=frame["machine_id"]))
    else:
        idx_train,idx_test = train_test_split(np.arange(len(X)),test_size=.25,random_state=seed,stratify=y)
    model = Pipeline([("imputer",SimpleImputer(strategy="median")),("classifier",RandomForestClassifier(n_estimators=150,min_samples_leaf=3,class_weight="balanced_subsample",random_state=seed,n_jobs=-1))])
    model.fit(X.iloc[idx_train],y.iloc[idx_train])
    proba = model.predict_proba(X.iloc[idx_test])[:,1]
    yt = y.iloc[idx_test]
    metrics = {"average_precision":float(average_precision_score(yt,proba)),"roc_auc":float(roc_auc_score(yt,proba)) if yt.nunique()==2 else None,"positive_rate_test":float(yt.mean()),"n_test":len(idx_test)}
    return model,metrics

def save_classifier(model, path: str):
    target = Path(path)
    target.parent.mkdir(parents=True,exist_ok=True)
    joblib.dump(model,target)

def load_classifier(path: str):
    # Only load joblib artifacts from trusted authors. pickle-based formats can execute code.
    return joblib.load(path)

def failure_probability(model, frame: pd.DataFrame):
    return model.predict_proba(build_features(frame))[:,1]
