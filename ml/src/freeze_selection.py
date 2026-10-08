"""Gate 5: freeze the decision using train/validation evidence only."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

from ml.src.audit_data import SPENDING_COLUMNS
from ml.src.data_paths import (
    EXPERIMENT_REVIEW_CSV,
    EXPERIMENT_SELECTION_EVIDENCE_CSV,
    PROFILE_DATA_DIR,
    PROJECT_ROOT,
    TRAIN_CSV,
    VALIDATION_CSV,
)
from ml.src.review_experiments import build_review_table, validate_evidence


SELECTION_FILE = PROJECT_ROOT / "models" / "selection.json"
SELECTED_PREPROCESSING = "log1p_standardscaler"
SELECTED_K = 2
SELECTED_SEED = 42


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def freeze_selection(output: Path = SELECTION_FILE) -> dict:
    """Write once; do not inspect or access the final test split."""
    if output.exists():
        raise FileExistsError(f"Selection đã freeze: {output}")

    evidence = pd.read_csv(EXPERIMENT_SELECTION_EVIDENCE_CSV)
    validate_evidence(evidence)
    review = pd.read_csv(EXPERIMENT_REVIEW_CSV)
    expected = build_review_table(evidence)
    pd.testing.assert_frame_equal(
        review, expected, check_exact=False, rtol=1e-10, atol=1e-10
    )

    candidate = evidence.loc[
        (evidence["preprocessing"] == SELECTED_PREPROCESSING)
        & (evidence["k"] == SELECTED_K)
    ]
    if len(candidate) != 1 or int(candidate.iloc[0]["run_count"]) != 10:
        raise ValueError("Selection thiếu evidence 10 seed của candidate đã chọn.")

    profile_dir = PROFILE_DATA_DIR / "log1p_standardscaler_k2_seed42"
    train_profile_path = profile_dir / "train_median_profile.csv"
    validation_profile_path = profile_dir / "validation_median_profile.csv"
    train_profile = pd.read_csv(train_profile_path)
    validation_profile = pd.read_csv(validation_profile_path)
    for frame, count in ((train_profile, 264), (validation_profile, 88)):
        if (
            len(frame) != SELECTED_K
            or set(frame["cluster"]) != set(range(SELECTED_K))
            or int(frame["count"].sum()) != count
            or not np.isclose(frame["share"].sum(), 1.0)
            or frame[list(SPENDING_COLUMNS)].isna().any().any()
        ):
            raise ValueError("Median profile không hợp lệ; chưa thể freeze.")

    paths = {
        "selection_evidence": EXPERIMENT_SELECTION_EVIDENCE_CSV,
        "review_table": EXPERIMENT_REVIEW_CSV,
        "train": TRAIN_CSV,
        "validation": VALIDATION_CSV,
        "train_median_profile": train_profile_path,
        "validation_median_profile": validation_profile_path,
    }
    selection = {
        "schema_version": 1,
        "status": "FROZEN",
        "decision": "D011",
        "date": "2026-10-08",
        "preprocessing": SELECTED_PREPROCESSING,
        "k": SELECTED_K,
        "random_state": SELECTED_SEED,
        "n_init": 10,
        "max_iter": 300,
        "algorithm": "lloyd",
        "feature_columns": list(SPENDING_COLUMNS),
        "fit_scope": "train_plus_validation_after_freeze",
        "test_used_for_selection": False,
        "evidence": {
            name: {"path": str(path.relative_to(PROJECT_ROOT)).replace("\\", "/"),
                   "sha256": sha256(path)}
            for name, path in paths.items()
        },
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("x", encoding="utf-8") as handle:
        json.dump(selection, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    return selection


if __name__ == "__main__":
    frozen = freeze_selection()
    print(f"[Gate 5] FROZEN: {frozen['preprocessing']}, K={frozen['k']}, seed={frozen['random_state']}")
    print("[Gate 5] Selection used train/validation only; final test remains sealed.")
