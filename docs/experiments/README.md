# Experiments and reproducibility

1. Run `python -m iot_pm.simulation.generator --records 5000 --output data/sample/sensors.csv`.
2. Run `python -m iot_pm.ml.cli --input data/sample/sensors.csv`.
3. Record Python version, random seed, data source and holdout split.
4. Compare rule baseline, class-weighted random forest and an unsupervised detector.
5. Report mean and uncertainty across independent assets and temporal holdouts.
6. Perform ablations removing wear-derived features and test under shifted noise.
7. Never tune on the final evaluation set.

All exploratory notebooks use synthetic data unless otherwise explicitly stated.
