# Modeling methodology

## Tasks
- Supervised failure probability: random forest with median imputation and class weighting
- Unsupervised anomaly detection: Isolation Forest; negative decision function is an uncalibrated anomaly score
- RUL: random forest regression using future *observed failure times*; right-censored units have unknown targets
- Rules: auditable temperature, vibration, pressure and RPM gates

## Evaluation precautions
Group by machine for holdout evaluation; never let recordings from the same machine leak across train and test sets. For deployments, additionally use time-forward validation with an embargo. Threshold selection must happen only on validation data, never on test data. Track PR-AUC, recall at alert budget, false alarms per machine-day, latency and predictive lead time. ROC-AUC alone hides class imbalance.

## Limits
Synthetic failures are generated algorithmically from correlated sensor signals and therefore cannot establish real-world generalization. RUL predictions require run-to-failure data with censoring accounted for in a real study; current baseline drops right-censored examples and can be biased. No real hardware, industrial validation, calibrated risk, or uptime guarantee is claimed.
