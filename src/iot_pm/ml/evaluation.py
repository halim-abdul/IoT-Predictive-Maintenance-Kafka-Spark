"""Methods for threshold selection and alert classification diagnostics."""
import numpy as np
from sklearn.metrics import precision_recall_curve, precision_score, recall_score, f1_score

def select_threshold(y_true, probs, min_recall=.8):
    if not 0 <= min_recall <= 1:
        raise ValueError("min_recall outside [0,1]")
    precision,recall,thresholds = precision_recall_curve(y_true,probs)
    eligible=[(float(precision[i]),float(thresholds[i])) for i in range(len(thresholds)) if recall[i]>=min_recall]
    return max(eligible, default=(0.0,0.5))[1]

def classification_at_threshold(y_true,probs,threshold=.5):
    y_pred=(np.asarray(probs)>=threshold).astype(int)
    return {"precision":float(precision_score(y_true,y_pred,zero_division=0)),"recall":float(recall_score(y_true,y_pred,zero_division=0)),"f1":float(f1_score(y_true,y_pred,zero_division=0))}
