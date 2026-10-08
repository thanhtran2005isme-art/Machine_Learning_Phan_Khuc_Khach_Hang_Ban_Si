"""Read the frozen joblib only. No training, no split data, and no final test access."""

from __future__ import annotations
import json
from pathlib import Path

import joblib
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
frozen = joblib.load(ROOT / "models" / "model.joblib")
export = json.loads((ROOT / "models" / "model.json").read_text(encoding="utf-8"))

features = ["Fresh", "Milk", "Grocery", "Frozen", "Detergents_Paper", "Delicassen"]
assert frozen["feature_columns"] == export["feature_columns"] == features

raw = np.array([
    [0, 0, 0, 0, 0, 0],
    [6410.5, 7226, 10842.5, 1153, 4084.5, 1508.5],
    [9727.5, 1626, 2175.5, 2194.5, 279.5, 662],
    [1, 100, 10000, 0, 10, 500],
    [100000, 500, 50, 60000, 1, 250],
    [1e7, 1e6, 1e8, 1e5, 1e6, 1e4],
], dtype=float)
scaled = frozen["scaler"].transform(np.log1p(raw))
labels = frozen["model"].predict(scaled)
distances = frozen["model"].transform(scaled)
print(json.dumps({"features": features, "inputs": raw.tolist(),
                  "labels": labels.tolist(), "distances": distances.tolist()}, allow_nan=False))
