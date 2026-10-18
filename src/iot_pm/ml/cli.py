"""Command-line training on sensor CSV."""
import argparse
import json
import pandas as pd
from iot_pm.ml.failure import train_classifier,save_classifier

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--input",default="data/sample/sensors.csv")
    p.add_argument("--output",default="artifacts/failure_model.joblib")
    args=p.parse_args()
    model,metrics=train_classifier(pd.read_csv(args.input))
    save_classifier(model,args.output)
    print(json.dumps(metrics,indent=2))
if __name__=="__main__":
    main()
