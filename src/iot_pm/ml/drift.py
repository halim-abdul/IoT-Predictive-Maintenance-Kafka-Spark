"""Simple drift indicators for numerical telemetry monitoring."""
import numpy as np
import pandas as pd

def population_stability_index(reference, current, bins=10):
    a=np.asarray(reference,dtype=float)
    b=np.asarray(current,dtype=float)
    a,b=a[np.isfinite(a)],b[np.isfinite(b)]
    if not len(a) or not len(b):
        raise ValueError("Drift computation requires nonempty samples")
    edges=np.unique(np.quantile(a,np.linspace(0,1,bins+1)))
    if len(edges)<2:
        return 0.0 if np.allclose(b,a[0]) else float("inf")
    edges[0],edges[-1]=-np.inf,np.inf
    x=np.histogram(a,bins=edges)[0]/len(a)
    y=np.histogram(b,bins=edges)[0]/len(b)
    x,y=np.clip(x,1e-6,None),np.clip(y,1e-6,None)
    return float(np.sum((y-x)*np.log(y/x)))
