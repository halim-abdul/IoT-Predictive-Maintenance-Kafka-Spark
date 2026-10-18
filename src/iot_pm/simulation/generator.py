"""Controllable synthetic multivariate telemetry; not a physical digital twin."""
import argparse
from pathlib import Path
import numpy as np
import pandas as pd

def simulate(n: int = 1000, machines: int = 5, seed: int = 42) -> pd.DataFrame:
    if n <= 0 or machines <= 0:
        raise ValueError("n and machines must be positive")
    rng = np.random.default_rng(seed)
    ids = np.array([f"motor-{i:03d}" for i in range(machines)])
    machine_id = ids[np.arange(n) % machines]
    hours = np.arange(n) / machines * 0.5
    wear = np.clip(hours / max(hours.max(), 1), 0, 1)
    temperature = 65 + 22 * wear + rng.normal(0, 3, n)
    vibration = np.clip(1.5 + 4 * wear + rng.normal(0, 0.35, n), 0, None)
    pressure = np.clip(8 - 2 * wear + rng.normal(0, 0.25, n), 0, None)
    rpm = np.clip(1800 - 160 * wear + rng.normal(0, 35, n), 0, None)
    # Synthetic event: a probabilistic label derived from wear and sensor stress.
    logit = -7 + 3 * wear + .06 * (temperature - 65) + .6 * vibration
    p = 1 / (1 + np.exp(-np.clip(logit, -30, 30)))
    failure = rng.binomial(1, p)
    return pd.DataFrame({"machine_id":machine_id, "timestamp":pd.date_range("2025-01-01", periods=n, freq="s", tz="UTC"),"temperature_c":temperature.round(3),"vibration_mm_s":vibration.round(3),"pressure_bar":pressure.round(3),"rpm":rpm.round(3),"operating_hours":hours.round(3),"failure":failure})

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--records", type=int, default=1000)
    parser.add_argument("--machines", type=int, default=5)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", default="data/sample/sensors.csv")
    args = parser.parse_args()
    frame = simulate(args.records, args.machines, args.seed)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(output, index=False)
    print(f"Wrote {len(frame)} samples to {output}")

if __name__ == "__main__":
    main()
