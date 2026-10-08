"""Train the frozen Gate 5 model, evaluate held-out test once, export artifacts.

This entry point intentionally has no --force or rerun option. A CLAIMED
evaluation requires manual incident review; it must not silently read test twice.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

from ml.src.audit_data import SPENDING_COLUMNS
from ml.src.data_paths import PROJECT_ROOT, TEST_CSV, TRAIN_CSV, VALIDATION_CSV
from ml.src.experiments import feature_matrix, load_split, safe_silhouette
from ml.src.freeze_selection import SELECTION_FILE, sha256


MODELS_DIR = PROJECT_ROOT / "models"
MODEL_JSON = MODELS_DIR / "model.json"
MODEL_JOBLIB = MODELS_DIR / "model.joblib"
FINAL_EVALUATION_JSON = MODELS_DIR / "final_evaluation.json"


def validate_frozen_selection(selection: dict) -> None:
    expected = {
        "status": "FROZEN",
        "decision": "D011",
        "preprocessing": "log1p_standardscaler",
        "k": 2,
        "random_state": 42,
        "n_init": 10,
        "max_iter": 300,
        "algorithm": "lloyd",
        "fit_scope": "train_plus_validation_after_freeze",
        "test_used_for_selection": False,
        "feature_columns": list(SPENDING_COLUMNS),
    }
    for key, value in expected.items():
        if selection.get(key) != value:
            raise ValueError(f"Frozen selection không đúng D011: {key}")
    sources = selection.get("evidence", {})
    if set(sources) != {
        "selection_evidence", "review_table", "train", "validation",
        "train_median_profile", "validation_median_profile",
    }:
        raise ValueError("Thiếu nguồn bằng chứng selection.")
    for name, info in sources.items():
        relative = Path(info["path"])
        if relative.is_absolute() or ".." in relative.parts or "test" in relative.name.lower():
            raise ValueError(f"Nguồn selection không được truy cập final test: {name}")
        if sha256(PROJECT_ROOT / relative) != info["sha256"]:
            raise ValueError(f"Evidence đã thay đổi sau freeze: {name}")


def fit_frozen_model(train_validation: pd.DataFrame, selection: dict):
    """Fit on 352 development rows, never on final test."""
    raw = feature_matrix(train_validation)
    scaler = StandardScaler()
    transformed = scaler.fit_transform(np.log1p(raw))
    model = KMeans(
        n_clusters=selection["k"],
        random_state=selection["random_state"],
        n_init=selection["n_init"],
        max_iter=selection["max_iter"],
        algorithm=selection["algorithm"],
    ).fit(transformed)
    return scaler, model, transformed


def predict_portable(raw: np.ndarray, exported: dict) -> np.ndarray:
    """Reference inference matching Node's future log1p/scale/nearest center."""
    if raw.ndim != 2 or raw.shape[1] != len(exported["feature_columns"]):
        raise ValueError("Input phải có đúng 6 cột chi tiêu.")
    if not np.isfinite(raw).all() or (raw < 0).any():
        raise ValueError("Chi tiêu phải hữu hạn và không âm.")
    scaled = (np.log1p(raw) - np.array(exported["scaler_mean"])) / np.array(exported["scaler_scale"])
    centers = np.array(exported["cluster_centers"])
    return np.argmin(np.sum((scaled[:, None, :] - centers[None, :, :]) ** 2, axis=2), axis=1)


def build_export(train_validation: pd.DataFrame, selection: dict, scaler, model) -> dict:
    features = list(SPENDING_COLUMNS)
    labels = model.labels_
    cluster_rows = []
    for idx in range(selection["k"]):
        members = train_validation.loc[labels == idx, features]
        cluster_rows.append({
            "cluster": idx,
            "count": len(members),
            "share": len(members) / len(train_validation),
            "median_spending": {name: float(members[name].median()) for name in features},
        })

    # Names are descriptive labels based on development data only.
    grocery = max(cluster_rows, key=lambda r: r["median_spending"]["Grocery"]
                  + r["median_spending"]["Detergents_Paper"])["cluster"]
    for row in cluster_rows:
        row["profile_name"] = (
            "Tạp hóa / chất tẩy rửa" if row["cluster"] == grocery
            else "Thiên về hàng tươi / đông lạnh"
        )

    return {
        "schema_version": 1,
        "selection_decision": selection["decision"],
        "preprocessing": selection["preprocessing"],
        "feature_columns": features,
        "k": selection["k"],
        "random_state": selection["random_state"],
        "n_init": selection["n_init"],
        "max_iter": selection["max_iter"],
        "algorithm": selection["algorithm"],
        "training_scope": "train_plus_validation",
        "training_count": len(train_validation),
        "transform": "(log1p(input) - scaler_mean) / scaler_scale",
        "distance": "argmin squared Euclidean distance to cluster_centers; first index resolves ties",
        "scaler_mean": scaler.mean_.tolist(),
        "scaler_scale": scaler.scale_.tolist(),
        "cluster_centers": model.cluster_centers_.tolist(),
        "cluster_profiles": cluster_rows,
        "test_used_for_training": False,
    }


def _create_json(path: Path, obj: dict) -> None:
    with path.open("x", encoding="utf-8") as handle:
        json.dump(obj, handle, ensure_ascii=False, indent=2, allow_nan=False)
        handle.write("\n")


def finalize_model() -> dict:
    if any(p.exists() for p in (MODEL_JSON, MODEL_JOBLIB, FINAL_EVALUATION_JSON)):
        raise FileExistsError("Artifact hoặc final evaluation đã tồn tại; không được đọc test lần nữa.")

    selection = json.loads(SELECTION_FILE.read_text(encoding="utf-8"))
    validate_frozen_selection(selection)
    train_df = load_split(TRAIN_CSV)
    validation_df = load_split(VALIDATION_CSV)
    if len(train_df) != 264 or len(validation_df) != 88:
        raise ValueError("Split phát triển phải là train=264, validation=88.")
    development = pd.concat([train_df, validation_df], ignore_index=True)
    scaler, model, dev_features = fit_frozen_model(development, selection)
    exported = build_export(development, selection, scaler, model)
    if not np.array_equal(predict_portable(feature_matrix(development), exported), model.labels_):
        raise AssertionError("Portable JSON prediction không khớp sklearn trên development.")
    if not TEST_CSV.is_file():
        raise FileNotFoundError(f"Thiếu final test: {TEST_CSV}")

    dev_silhouette = float(silhouette_score(dev_features, model.labels_))
    dev_inertia_per_sample = float(model.inertia_ / len(development))
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    _create_json(MODEL_JSON, exported)
    with MODEL_JOBLIB.open("xb") as handle:
        joblib.dump({"scaler": scaler, "model": model, "feature_columns": list(SPENDING_COLUMNS)}, handle)

    # Durable one-shot claim is written BEFORE the very first test read.
    claim = {
        "status": "CLAIMED",
        "selection_sha256": sha256(SELECTION_FILE),
        "test_used_for_selection": False,
        "warning": "If interrupted, inspect the incident; never automatically rerun test.",
    }
    _create_json(FINAL_EVALUATION_JSON, claim)

    test_df = load_split(TEST_CSV)  # First and only evaluation of the held-out split.
    if len(test_df) != 88:
        raise ValueError("Final test phải có 88 dòng.")
    test_raw = feature_matrix(test_df)
    test_features = scaler.transform(np.log1p(test_raw))
    test_labels = model.predict(test_features)
    if not np.array_equal(predict_portable(test_raw, exported), test_labels):
        raise AssertionError("Portable JSON không khớp sklearn trên test.")
    unique, counts = np.unique(test_labels, return_counts=True)
    silhouette = safe_silhouette(test_features, test_labels)
    squared_distances = np.sum((test_features - model.cluster_centers_[test_labels]) ** 2, axis=1)
    result = {
        "status": "COMPLETE",
        "selection_sha256": claim["selection_sha256"],
        "test_used_for_selection": False,
        "test_evaluated_once": True,
        "model_json_sha256": sha256(MODEL_JSON),
        "model_joblib_sha256": sha256(MODEL_JOBLIB),
        "test_sha256": sha256(TEST_CSV),
        "training": {
            "rows": len(development),
            "scope": "train_plus_validation_after_freeze",
            "silhouette": dev_silhouette,
            "inertia_per_row": dev_inertia_per_sample,
        },
        "final_test": {
            "rows": len(test_df),
            "silhouette": None if np.isnan(silhouette) else float(silhouette),
            "inertia_per_row": float(squared_distances.mean()),
            "cluster_counts": {str(i): int(counts[unique == i][0]) if i in unique else 0
                               for i in range(selection["k"])},
            "min_cluster_share": float(counts.min() / len(test_df)),
        },
        "selection_unchanged_after_test": True,
    }
    tmp_result = FINAL_EVALUATION_JSON.with_suffix(".completed.tmp")
    _create_json(tmp_result, result)
    os.replace(tmp_result, FINAL_EVALUATION_JSON)
    return result


if __name__ == "__main__":
    output = finalize_model()
    print("[Gate 5] Independent final test: COMPLETE (one-shot)")
    print(json.dumps(output["final_test"], ensure_ascii=False, indent=2))
    print("[Gate 5] Frozen artifacts: models/model.json + models/model.joblib")
