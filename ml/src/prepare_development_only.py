"""Recreate train and validation CSV only; held-out test is never materialized."""
from __future__ import annotations
import json
from pathlib import Path

import numpy as np

from ml.src.audit_data import load_raw_dataset, validation_errors
from ml.src.data_paths import PROJECT_ROOT, RAW_CSV, TRAIN_CSV, VALIDATION_CSV
from ml.src.final_profile import assert_split_hash, sha
from ml.src.split_data import split_indices


def materialize_development(*, raw: Path = RAW_CSV, root: Path = PROJECT_ROOT) -> None:
    quality = json.loads((root / "reports/data/data_quality.json").read_text(encoding="utf-8"))
    if sha(raw.read_bytes()) != quality["source_sha256"]:
        raise ValueError("Raw file SHA does not match audited UCI dataset.")
    frame = load_raw_dataset(raw)
    if errors := validation_errors(frame, strict_rows=True):
        raise ValueError("Raw schema validation failed: " + "; ".join(errors))
    train_indices, validation_indices, _ = split_indices(len(frame), seed=42)
    frozen = json.loads((root / "models/selection.json").read_text(encoding="utf-8"))
    parts = (("train", TRAIN_CSV, frame.iloc[train_indices]),
             ("validation", VALIDATION_CSV, frame.iloc[validation_indices]))
    for name, path, values in parts:
        expected = frozen["evidence"][name]["sha256"]
        csv_bytes = values.reset_index(drop=True).to_csv(index=False, lineterminator="\n").encode("utf-8")
        crlf = csv_bytes.replace(b"\n", b"\r\n")
        if sha(csv_bytes) != expected and sha(crlf) != expected:
            raise ValueError(f"Development {name} has changed since Gate 5 freeze.")
    for _, path, values in parts:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(values.reset_index(drop=True).to_csv(index=False, lineterminator="\n").encode("utf-8"))
    print("[Gate 9.2] Prepared train=264, validation=88; no test.csv created/read.")


if __name__ == "__main__":
    materialize_development()
