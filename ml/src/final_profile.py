"""Gate 9.2: predict-only profiles of the 352 development customers.

Only train.csv, validation.csv and the frozen Gate 5 artifacts are opened.
No fit, train, model selection, or held-out test access.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

from ml.src.audit_data import EXPECTED_COLUMNS, SPENDING_COLUMNS
from ml.src.data_paths import PROJECT_ROOT, TRAIN_CSV, VALIDATION_CSV

FEATURES = list(SPENDING_COLUMNS)
ARTIFACTS = (
    "cluster_summary.csv", "median_ratio.csv", "cluster_sizes.csv",
    "channel_profile.csv", "region_profile.csv", "distance_summary.csv",
)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def assert_frozen_hash(path: Path, expected: str) -> None:
    original = path.read_bytes()
    crlf = original.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")
    if sha(original) != expected and sha(crlf) != expected:
        raise ValueError("Frozen checksum mismatch: " + path.name)


def assert_split_hash(path: Path, expected: str) -> None:
    original = path.read_bytes()
    crlf = original.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")
    if sha(original) != expected and sha(crlf) != expected:
        raise ValueError("Frozen development split checksum mismatch: " + path.name)


def load_development(root: Path, train_path: Path, val_path: Path) -> tuple[pd.DataFrame, dict, dict]:
    evaluation = json.loads((root / "models/final_evaluation.json").read_text(encoding="utf-8"))
    selection_path = root / "models/selection.json"
    model_path = root / "models/model.json"
    assert_frozen_hash(selection_path, evaluation["selection_sha256"])
    assert_frozen_hash(model_path, evaluation["model_json_sha256"])
    selection = json.loads(selection_path.read_text(encoding="utf-8"))
    model = json.loads(model_path.read_text(encoding="utf-8"))

    if not (
        evaluation["status"] == "COMPLETE"
        and evaluation["test_used_for_selection"] is False
        and evaluation["selection_unchanged_after_test"] is True
        and evaluation["training"]["rows"] == 352
        and selection["status"] == "FROZEN"
        and selection["decision"] == model["selection_decision"] == "D011"
        and selection["preprocessing"] == model["preprocessing"] == "log1p_standardscaler"
        and selection["k"] == model["k"] == 2
        and selection["random_state"] == model["random_state"] == 42
        and selection["feature_columns"] == model["feature_columns"] == FEATURES
        and model["training_scope"] == "train_plus_validation"
        and model["training_count"] == 352
        and model["test_used_for_training"] is False
    ):
        raise ValueError("Gate 5 frozen selection, model and evaluation mismatch.")

    frames = []
    for name, path, size in (("train", train_path, 264), ("validation", val_path, 88)):
        evidence = selection["evidence"][name]
        if evidence["path"] != f"data/processed/{name}.csv":
            raise ValueError("Noncanonical development evidence path.")
        assert_split_hash(path, evidence["sha256"])
        df = pd.read_csv(path)
        if len(df) != size or list(df.columns) != EXPECTED_COLUMNS:
            raise ValueError(f"Invalid {name} split schema or size.")
        if df.isna().any().any():
            raise ValueError(f"Missing {name} values.")
        numeric = df[EXPECTED_COLUMNS].to_numpy(dtype=float)
        if not np.isfinite(numeric).all() or (df[FEATURES].to_numpy(dtype=float) < 0).any():
            raise ValueError(f"Invalid {name} numeric values.")
        if not set(df["Channel"].unique()).issubset({1, 2}) or not set(df["Region"].unique()).issubset({1, 2, 3}):
            raise ValueError(f"Invalid {name} category values.")
        frames.append(df)
    return pd.concat(frames, ignore_index=True), model, {
        "selection_sha256": evaluation["selection_sha256"],
        "model_sha256": evaluation["model_json_sha256"],
        "train_sha256": selection["evidence"]["train"]["sha256"],
        "validation_sha256": selection["evidence"]["validation"]["sha256"],
    }


def frozen_predict(frame: pd.DataFrame, model: dict) -> tuple[np.ndarray, np.ndarray]:
    raw = frame[FEATURES].to_numpy(dtype=float, copy=True)
    mean, scale = np.asarray(model["scaler_mean"], dtype=float), np.asarray(model["scaler_scale"], dtype=float)
    centers = np.asarray(model["cluster_centers"], dtype=float)
    if (
        raw.shape != (352, 6) or mean.shape != (6,) or scale.shape != (6,)
        or centers.shape != (2, 6) or not np.isfinite(raw).all()
        or not np.isfinite(mean).all() or not np.isfinite(scale).all()
        or not np.isfinite(centers).all() or np.any(scale <= 0)
    ):
        raise ValueError("Invalid frozen model dimensions or values.")
    scaled = (np.log1p(raw) - mean) / scale
    all_distances = np.sqrt(np.square(scaled[:, None, :] - centers[None, :, :]).sum(axis=2))
    labels = all_distances.argmin(axis=1)
    selected = all_distances[np.arange(352), labels]
    if set(np.unique(labels)) != {0, 1}:
        raise ValueError("Frozen development predictions do not contain both clusters.")
    return labels, selected


def category_table(frame: pd.DataFrame, labels: np.ndarray, field: str) -> pd.DataFrame:
    rows = []
    categories = sorted(set(map(int, frame[field].unique())))
    values = frame[field].to_numpy()
    for cluster in (0, 1):
        size = int((labels == cluster).sum())
        for category in categories:
            count = int(((labels == cluster) & (values == category)).sum())
            rows.append({"cluster": cluster, field: category, "count": count,
                         "within_cluster_share": count / size})
    return pd.DataFrame(rows)


def build_tables(frame: pd.DataFrame, model: dict) -> tuple[dict[str, pd.DataFrame], dict]:
    labels, distances = frozen_predict(frame, model)
    overall = frame[FEATURES].median()
    if (overall <= 0).any():
        raise ValueError("Cannot calculate median ratios with nonpositive denominator.")
    summaries, ratios, sizes, distributions = [], [], [], []
    for cluster in (0, 1):
        subset = frame.loc[labels == cluster, FEATURES]
        size = len(subset)
        share = size / 352
        medians = subset.median()
        profile = model["cluster_profiles"][cluster]
        if (
            profile["cluster"] != cluster or profile["count"] != size
            or not np.isclose(profile["share"], share, atol=1e-12, rtol=0)
            or not np.allclose([profile["median_spending"][f] for f in FEATURES],
                                medians.to_numpy(dtype=float), atol=1e-10, rtol=0)
        ):
            raise ValueError("Final profile does not match frozen 352-development model.")
        summaries.append({"cluster": cluster, "profile_name": profile["profile_name"],
                          "count": size, "share": share,
                          **{f: float(medians[f]) for f in FEATURES}})
        ratios.append({"cluster": cluster, **{f: float(medians[f] / overall[f]) for f in FEATURES}})
        sizes.append({"cluster": cluster, "count": size, "share": share})
        d = distances[labels == cluster]
        q1, q3 = np.quantile(d, [0.25, 0.75])
        high = float(q3 + 1.5 * (q3 - q1))
        distributions.append({
            "cluster": cluster, "count": size, "min": float(d.min()),
            "mean": float(d.mean()), "median": float(np.median(d)),
            "p90": float(np.percentile(d, 90)), "p95": float(np.percentile(d, 95)),
            "max": float(d.max()), "q1": float(q1), "q3": float(q3),
            "iqr_upper_fence": high, "iqr_distance_outlier_count": int((d > high).sum()),
            "inertia_per_member": float(np.square(d).mean()),
        })
    tables = {
        "cluster_summary.csv": pd.DataFrame(summaries),
        "median_ratio.csv": pd.DataFrame(ratios),
        "cluster_sizes.csv": pd.DataFrame(sizes),
        "channel_profile.csv": category_table(frame, labels, "Channel"),
        "region_profile.csv": category_table(frame, labels, "Region"),
        "distance_summary.csv": pd.DataFrame(distributions),
    }
    for fname in ("channel_profile.csv", "region_profile.csv"):
        table = tables[fname]
        if int(table["count"].sum()) != 352:
            raise AssertionError("Category counts do not reconcile.")
        for c in (0, 1):
            if not np.isclose(table.loc[table.cluster == c, "within_cluster_share"].sum(), 1, atol=1e-12):
                raise AssertionError("Category shares do not reconcile.")
    squared = np.sort(np.square(distances))[::-1]
    info = {
        "development_count": 352,
        "cluster_counts": {"0": sizes[0]["count"], "1": sizes[1]["count"]},
        "distance_outlier_count": int(sum(item["iqr_distance_outlier_count"] for item in distributions)),
        "top_1pct_count": 4,
        "top_1pct_inertia_share": float(squared[:4].sum() / squared.sum()),
        "inertia_per_row": float(np.square(distances).mean()),
    }
    return tables, info


def generate_profile(*, root: Path = PROJECT_ROOT, train: Path | None = None,
                     validation: Path | None = None, output: Path | None = None) -> dict:
    root = Path(root)
    train = Path(train) if train is not None else root / "data/processed/train.csv"
    validation = Path(validation) if validation is not None else root / "data/processed/validation.csv"
    output = Path(output) if output is not None else root / "reports/data/final_profile"
    development, model, provenance = load_development(root, train, validation)
    tables, metrics = build_tables(development, model)
    if tuple(tables) != ARTIFACTS:
        raise AssertionError("Unexpected profile artifact names.")
    payloads = {name: table.to_csv(index=False, float_format="%.12g",
                                    lineterminator="\n").encode("utf-8") for name, table in tables.items()}
    metadata = {
        "schema_version": 1, "status": "COMPLETE", "decision": "D011",
        "scope": "train_plus_validation", "source_rows": {"train": 264, "validation": 88},
        "frozen_k": 2, "frozen_preprocessing": "log1p_standardscaler",
        "model_fit_performed": False, "scaler_fit_performed": False, "test_used": False,
        "source_policy": "read train.csv and validation.csv only; no final test or re-fit",
        "feature_columns": FEATURES, "profiling_only_columns": ["Channel", "Region"],
        "distance_space": "Euclidean in frozen log1p StandardScaler space",
        "outlier_policy": "distance > cluster Q3 + 1.5*IQR; descriptive flag, no removal",
        "median_ratio_denominator": "overall 352-development median by feature",
        "provenance": provenance,
        "files": {name: {"path": "reports/data/final_profile/" + name, "sha256": sha(blob)}
                  for name, blob in payloads.items()},
        **metrics,
    }
    output.mkdir(parents=True, exist_ok=True)
    for name, blob in payloads.items():
        (output / name).write_bytes(blob)
    (output / "profile_metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2, allow_nan=False) + "\n",
        encoding="utf-8", newline="\n",
    )
    return metadata


def main() -> None:
    parser = argparse.ArgumentParser(description="Gate 9.2 frozen K2 development profiling: predict-only")
    parser.add_argument("--train", type=Path, default=TRAIN_CSV)
    parser.add_argument("--validation", type=Path, default=VALIDATION_CSV)
    parser.add_argument("--output", type=Path, default=PROJECT_ROOT / "reports/data/final_profile")
    args = parser.parse_args()
    info = generate_profile(train=args.train, validation=args.validation, output=args.output)
    print("[Gate 9.2] PROFILE COMPLETE; 352 development rows; no fit/test access")
    print("[Gate 9.2] Counts:", info["cluster_counts"], "| inertia/row:", info["inertia_per_row"])


if __name__ == "__main__":
    main()
