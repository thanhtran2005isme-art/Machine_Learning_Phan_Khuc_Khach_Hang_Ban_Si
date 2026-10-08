"""Gate 9.6: cold replay of TRAIN/VALIDATION evidence only (no final test).

A fresh checkout prepares 264+88 from verified UCI raw, then repeats the
original D010 140-run experiment grid and 630 pairwise ARIs in a TEMP dir.
Frozen D011 K2 artifacts and historical evidence remain read-only.
"""
from __future__ import annotations

import hashlib
import json
import tempfile
from pathlib import Path
from unittest.mock import patch

import numpy as np
import pandas as pd

from ml.src import experiments as experiment
from ml.src import review_experiments as review
from ml.src.data_paths import PROJECT_ROOT, TRAIN_CSV, VALIDATION_CSV

FROZEN_FILES = (
    "models/selection.json", "models/model.json", "models/model.joblib",
    "models/final_evaluation.json",
)
EVIDENCE_FILES = (
    "reports/data/experiments/selection_evidence.csv",
    "reports/data/experiments/review_table.csv",
    "reports/data/experiments/runs.csv",
    "reports/data/experiments/stability_pairs.csv",
)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compare_csv(original: Path, generated: Path, key: tuple[str, ...], columns: tuple[str, ...] | None = None) -> None:
    baseline = pd.read_csv(original).sort_values(list(key)).reset_index(drop=True)
    current = pd.read_csv(generated).sort_values(list(key)).reset_index(drop=True)
    if baseline.shape != current.shape:
        raise AssertionError(f"Shape drift {original.name}: {baseline.shape} != {current.shape}")
    if set(baseline.columns) != set(current.columns):
        raise AssertionError(f"Schema drift in {original.name}")
    for col in baseline.columns if columns is None else columns:
        if col in key:
            if not baseline[col].equals(current[col]):
                raise AssertionError(f"Key drift in {original.name}.{col}")
        elif pd.api.types.is_numeric_dtype(baseline[col]):
            if not np.allclose(
                baseline[col].to_numpy(dtype=float), current[col].to_numpy(dtype=float),
                rtol=1e-4, atol=1e-4, equal_nan=True,
            ):
                a = baseline[col].to_numpy(dtype=float)
                b = current[col].to_numpy(dtype=float)
                worst = int(np.argmax(np.abs(a-b)))
                raise AssertionError(
                    f"Numeric evidence drift in {original.name}.{col} row {worst}: {a[worst]} vs {b[worst]}"
                )
        elif not baseline[col].astype(str).equals(current[col].astype(str)):
            raise AssertionError(f"Text evidence drift in {original.name}.{col}")


def verify_cold_replay() -> None:
    if (PROJECT_ROOT / "data/processed/test.csv").exists():
        raise RuntimeError("Held-out test file must NOT exist during Gate 9.6 cold replay")
    quality = json.loads((PROJECT_ROOT / "reports/data/data_quality.json").read_text(encoding="utf-8"))
    raw = PROJECT_ROOT / "data/raw/Wholesale customers data.csv"
    if not raw.exists() or sha(raw) != quality["source_sha256"]:
        raise RuntimeError("Audited raw UCI checksum mismatch")
    selected = json.loads((PROJECT_ROOT / "models/selection.json").read_text(encoding="utf-8"))
    if selected["status"] != "FROZEN" or selected["decision"] != "D011" or selected["k"] != 2:
        raise RuntimeError("D011 selection mismatch")
    for name, path in (("train",TRAIN_CSV),("validation",VALIDATION_CSV)):
        actual = path.read_bytes()
        expected = selected["evidence"][name]["sha256"]
        if hashlib.sha256(actual).hexdigest() != expected and hashlib.sha256(actual.replace(b"\n",b"\r\n")).hexdigest()!=expected:
            raise RuntimeError("Frozen "+name+" split mismatch")

    protected = {p:sha(PROJECT_ROOT / p) for p in (*FROZEN_FILES,*EVIDENCE_FILES)}
    with tempfile.TemporaryDirectory(prefix="gate9-6-cold-") as temporary:
        root=Path(temporary); data=root/"experiments";figures=root/"figures"
        outputs = {
            "EXPERIMENT_DATA_DIR": data,
            "EXPERIMENT_FIGURES_DIR": figures,
            "EXPERIMENT_BASELINE_DESCRIPTIVE_CSV":data/"baseline_descriptive.csv",
            "EXPERIMENT_BASELINE_K2_CSV":data/"baseline_k2.csv",
            "EXPERIMENT_RUNS_CSV":data/"runs.csv",
            "EXPERIMENT_AGGREGATE_CSV":data/"aggregate.csv",
            "EXPERIMENT_STABILITY_CSV":data/"stability.csv",
            "EXPERIMENT_STABILITY_PAIRS_CSV":data/"stability_pairs.csv",
            "EXPERIMENT_SELECTION_EVIDENCE_CSV":data/"selection_evidence.csv",
            "EXPERIMENT_METADATA_JSON":data/"experiment_metadata.json",
        }
        with patch.multiple(experiment, **outputs):
            info=experiment.run_experiments(train_path=TRAIN_CSV,validation_path=VALIDATION_CSV)
        if info["runs_actual"]!=140 or info["ari_pair_count"]!=630 or info["test_used"] is not False:
            raise AssertionError("D010 experiment protocol incomplete / test leakage flag")
        compare_csv(PROJECT_ROOT/"reports/data/experiments/runs.csv",data/"runs.csv",
                    ("preprocessing","k","seed"))
        compare_csv(PROJECT_ROOT/"reports/data/experiments/stability_pairs.csv",data/"stability_pairs.csv",
                    ("preprocessing","k","seed_a","seed_b"))
        compare_csv(PROJECT_ROOT/"reports/data/experiments/selection_evidence.csv",
                    data/"selection_evidence.csv",("preprocessing","k"))
        with patch.multiple(
            review, EXPERIMENT_REVIEW_CSV=data/"review_table.csv",
            EXPERIMENT_REVIEW_MD=root/"EXPERIMENT_REVIEW.md"
        ):
            result=review.review_experiments(
                evidence_path=data/"selection_evidence.csv",
                metadata_path=data/"experiment_metadata.json",
            )
        if len(result)!=14: raise AssertionError("Expected 14 candidate review rows")
        compare_csv(PROJECT_ROOT/"reports/data/experiments/review_table.csv",
                    data/"review_table.csv",("preprocessing","k"))
        for p in (*FROZEN_FILES,*EVIDENCE_FILES):
            if sha(PROJECT_ROOT/p)!=protected[p]:
                raise AssertionError("Protected evidence/frozen model modified: "+p)
        if (PROJECT_ROOT/"data/processed/test.csv").exists():
            raise AssertionError("Cold replay must never materialize held-out final test")
        print("GATE9.6 PASS: UCI raw source verified, frozen 264/88 splits verified")
        print("GATE9.6 PASS: 140 experiment runs, 630 pairwise ARIs, 14 candidate evidence and review compared")
        print("GATE9.6 PASS: no test.csv read/created, no models/ or canonical evidence changed")
        print("GATE9.6 NOTE: only train/validation candidate experiments re-fit in TEMP; final D011 stays frozen")


if __name__ == "__main__":
    verify_cold_replay()
