# Reproducible research notebook guide

Run `pip install -e '.[api,dev]'`, then `jupyter lab`. All notebooks import functions from `iot_pm` and generate fixed-seed synthetic telemetry (no external datasets or network required). They progressively examine sensor distributions, telemetry cleaning, engineered features, anomalies, classifier evaluation, threshold tradeoffs, time-to-failure labels, drift, alert routing and overall experiments.

The notebooks provide exploratory visualizations and code examples, not claims of benchmark performance.
