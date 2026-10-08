"""Train-only K-Means experiments; validation is transformed and predicted only.

The independent test split is intentionally absent from this module.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sklearn
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score, silhouette_score
from sklearn.preprocessing import StandardScaler

try:
    from .audit_data import EXPECTED_COLUMNS, SPENDING_COLUMNS, validation_errors
    from .data_paths import (
        EXPERIMENT_DATA_DIR,
        EXPERIMENT_FIGURES_DIR,
        PROJECT_ROOT,
        TRAIN_CSV,
        VALIDATION_CSV,
    )
except ImportError:
    from audit_data import EXPECTED_COLUMNS, SPENDING_COLUMNS, validation_errors
    from data_paths import (
        EXPERIMENT_DATA_DIR,
        EXPERIMENT_FIGURES_DIR,
        PROJECT_ROOT,
        TRAIN_CSV,
        VALIDATION_CSV,
    )

PREPROCESSING = ("raw", "log1p_standardscaler")
K_VALUES = tuple(range(2, 9))
SEEDS = tuple(range(42, 52))
N_INIT = 10


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(PROJECT_ROOT.resolve()).as_posix()
    except ValueError:
        return str(path)


def load_split(path: Path) -> pd.DataFrame:
    if not path.is_file():
        raise FileNotFoundError(f"Missing split: {path}. Run python ml/src/prepare_data.py")
    frame = pd.read_csv(path)
    if list(frame.columns) != EXPECTED_COLUMNS:
        raise ValueError(f"Unexpected split schema: {path}")
    errors = validation_errors(frame, strict_rows=False)
    if errors:
        raise ValueError(f"Invalid split {path}: {'; '.join(errors)}")
    return frame


def baseline_a(frame: pd.DataFrame) -> pd.DataFrame:
    """Descriptive train-only baseline, without fitting any estimator."""
    summary = frame.loc[:, SPENDING_COLUMNS].describe().T
    summary.index.name = "feature"
    summary = summary.reset_index().rename(
        columns={"25%": "q1", "50%": "median", "75%": "q3"}
    )
    return summary.loc[:, ["feature", "count", "mean", "std", "min", "q1", "median", "q3", "max"]]


def prepare_features(
    train: pd.DataFrame, validation: pd.DataFrame, method: str
) -> tuple[np.ndarray, np.ndarray, StandardScaler | None]:
    if method not in PREPROCESSING:
        raise ValueError(f"Unknown preprocessing: {method}")
    x_train = train.loc[:, SPENDING_COLUMNS].to_numpy(dtype=np.float64, copy=True)
    x_validation = validation.loc[:, SPENDING_COLUMNS].to_numpy(dtype=np.float64, copy=True)
    if not np.isfinite(x_train).all() or not np.isfinite(x_validation).all():
        raise ValueError("Non-finite input features")
    if method == "raw":
        return x_train, x_validation, None
    if (x_train < 0).any() or (x_validation < 0).any():
        raise ValueError("log1p requires non-negative expenditures")
    # The scaler learns only from train. Validation may only call transform.
    scaler = StandardScaler()
    return scaler.fit_transform(np.log1p(x_train)), scaler.transform(np.log1p(x_validation)), scaler


def squared_distance_inertia(
    values: np.ndarray, labels: np.ndarray, centers: np.ndarray
) -> float:
    residual = values - centers[labels]
    return float(np.einsum("ij,ij->", residual, residual))


def _silhouette(values: np.ndarray, labels: np.ndarray) -> tuple[float | None, str]:
    clusters = np.unique(labels).size
    if not 2 <= clusters <= len(values) - 1:
        return None, "undefined_requires_2_to_n_minus_1_predicted_clusters"
    score = float(silhouette_score(values, labels))
    if not np.isfinite(score) or not -1 <= score <= 1:
        raise AssertionError("Invalid silhouette")
    return score, "ok"


def evaluate_candidate(
    x_train: np.ndarray, x_validation: np.ndarray, method: str, k: int, seed: int
) -> tuple[dict, dict[str, np.ndarray], KMeans]:
    model = KMeans(n_clusters=k, random_state=seed, n_init=N_INIT, algorithm="lloyd")
    labels_train = model.fit_predict(x_train)
    labels_validation = model.predict(x_validation)
    inertia_train = squared_distance_inertia(x_train, labels_train, model.cluster_centers_)
    inertia_validation = squared_distance_inertia(x_validation, labels_validation, model.cluster_centers_)
    if not np.isclose(inertia_train, model.inertia_, rtol=1e-9, atol=1e-6):
        raise AssertionError("Train inertia disagrees with sklearn")
    if not np.isfinite([inertia_train, inertia_validation]).all() or min(inertia_train, inertia_validation) < 0:
        raise AssertionError("Invalid inertia")
    silhouette_train, status_train = _silhouette(x_train, labels_train)
    silhouette_validation, status_validation = _silhouette(x_validation, labels_validation)
    if status_train != "ok":
        raise AssertionError("Train silhouette is undefined")
    result = {
        "preprocessing": method,
        "k": k,
        "seed": seed,
        "n_init": N_INIT,
        "inertia_train": inertia_train,
        "inertia_validation": inertia_validation,
        "silhouette_train": silhouette_train,
        "silhouette_validation": silhouette_validation,
        "silhouette_validation_status": status_validation,
        "train_clusters_present": int(np.unique(labels_train).size),
        "validation_clusters_present": int(np.unique(labels_validation).size),
    }
    return result, {"train": labels_train, "validation": labels_validation}, model


def _sizes_and_profiles(
    frame: pd.DataFrame, labels: np.ndarray, method: str, k: int, seed: int, split: str
) -> tuple[list[dict], list[dict]]:
    sizes = np.bincount(labels, minlength=k)
    if sizes.sum() != len(frame):
        raise AssertionError("Cluster sizes do not cover split")
    size_rows, profile_rows = [], []
    for cluster in range(k):
        count = int(sizes[cluster])
        base = {"preprocessing": method, "k": k, "seed": seed, "split": split, "cluster": cluster}
        size_rows.append({**base, "count": count, "proportion": count / len(frame)})
        if count == 0:
            continue
        members = frame.loc[labels == cluster]
        profile = {**base, "count": count}
        for feature in SPENDING_COLUMNS:
            profile[f"median_{feature}"] = float(members[feature].median())
        # Channel/Region are used only here, after K-Means fit and prediction.
        for channel in (1, 2):
            profile[f"channel_{channel}_rate"] = float((members["Channel"] == channel).mean())
        for region in (1, 2, 3):
            profile[f"region_{region}_rate"] = float((members["Region"] == region).mean())
        profile_rows.append(profile)
    return size_rows, profile_rows


def _summary(runs: pd.DataFrame, stability: pd.DataFrame) -> pd.DataFrame:
    metrics = ["inertia_train", "inertia_validation", "silhouette_train", "silhouette_validation"]
    summary = runs.groupby(["preprocessing", "k"], sort=True)[metrics].agg(["mean", "std"])
    summary.columns = [f"{metric}_{stat}" for metric, stat in summary.columns]
    summary = summary.reset_index()
    return summary.merge(stability, on=["preprocessing", "k"], validate="one_to_one")


def _draw_metric(summary: pd.DataFrame, metric: str, split: str, output: Path) -> None:
    column = f"{metric}_{split}"
    if metric == "inertia":
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        panels = zip(axes, PREPROCESSING, strict=True)
    else:
        fig, axis = plt.subplots(figsize=(8, 5))
        panels = ((axis, None),)

    for axis, panel_method in panels:
        methods = (panel_method,) if panel_method else PREPROCESSING
        for method in methods:
            table = summary.loc[summary["preprocessing"] == method]
            y = table[f"{column}_mean"].to_numpy(dtype=float)
            std = table[f"{column}_std"].fillna(0).to_numpy(dtype=float)
            x = table["k"].to_numpy(dtype=int)
            axis.plot(x, y, marker="o", label=method)
            axis.fill_between(x, y - std, y + std, alpha=0.18)
        axis.set_xticks(K_VALUES)
        axis.set_xlabel("K")
        axis.set_ylabel(f"{metric} ({split})")
        axis.grid(alpha=0.2)
        axis.legend()
        if panel_method:
            axis.set_title(panel_method)
        if metric == "silhouette":
            axis.set_ylim(-1, 1)
    fig.suptitle(f"{metric.capitalize()} - {split} (mean ± SD of 10 seeds)")
    fig.tight_layout()
    fig.savefig(output, dpi=160, bbox_inches="tight")
    plt.close(fig)


def run_experiments(
    train: pd.DataFrame,
    validation: pd.DataFrame,
    data_dir: Path = EXPERIMENT_DATA_DIR,
    figures_dir: Path = EXPERIMENT_FIGURES_DIR,
    train_path: Path | None = None,
    validation_path: Path | None = None,
) -> dict:
    """Run the fixed 2 x 7 x 10 grid without touching an independent test split."""
    for split_name, frame in (("train", train), ("validation", validation)):
        if list(frame.columns) != EXPECTED_COLUMNS:
            raise ValueError(f"Invalid {split_name} schema")
        errors = validation_errors(frame, strict_rows=False)
        if errors:
            raise ValueError(f"Invalid {split_name}: {'; '.join(errors)}")
        if len(frame) <= max(K_VALUES):
            raise ValueError(f"Insufficient {split_name} rows for K=8")

    grid = list(itertools.product(PREPROCESSING, K_VALUES, SEEDS))
    if len(grid) != 140 or len(set(grid)) != len(grid):
        raise AssertionError("Experiment grid must contain 140 distinct configurations")

    run_rows, size_rows, profile_rows, stability_rows = [], [], [], []
    reference_b = None
    for method in PREPROCESSING:
        x_train, x_validation, _ = prepare_features(train, validation, method)
        for k in K_VALUES:
            assignments = []
            for seed in SEEDS:
                row, labels, _ = evaluate_candidate(x_train, x_validation, method, k, seed)
                run_rows.append(row)
                assignments.append(labels["train"])
                for name, frame in (("train", train), ("validation", validation)):
                    sizes, profiles = _sizes_and_profiles(frame, labels[name], method, k, seed, name)
                    size_rows.extend(sizes)
                    profile_rows.extend(profiles)
                if (method, k, seed) == ("raw", 2, 42):
                    reference_b = row.copy()
            scores = [
                adjusted_rand_score(first, second)
                for first, second in itertools.combinations(assignments, 2)
            ]
            stability_rows.append(
                {"preprocessing": method, "k": k, "seed_pairs": len(scores),
                 "mean_pairwise_ari_train": float(np.mean(scores)),
                 "std_pairwise_ari_train": float(np.std(scores, ddof=1)),
                 "min_pairwise_ari_train": float(np.min(scores))}
            )

    runs = pd.DataFrame(run_rows)
    sizes = pd.DataFrame(size_rows)
    profiles = pd.DataFrame(profile_rows)
    stability = pd.DataFrame(stability_rows)
    summary = _summary(runs, stability)
    if len(runs) != 140 or runs.duplicated(["preprocessing", "k", "seed"]).any():
        raise AssertionError("Incomplete or duplicate runs")
    totals = sizes.groupby(["preprocessing", "k", "seed", "split"], sort=True).agg(
        count=("count", "sum"), proportion=("proportion", "sum")
    ).reset_index()
    for split_name, n in (("train", len(train)), ("validation", len(validation))):
        split_totals = totals.loc[totals["split"] == split_name]
        if not (split_totals["count"] == n).all() or not np.allclose(split_totals["proportion"], 1):
            raise AssertionError(f"Invalid cluster sizes for {split_name}")

    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)
    tables = {
        "baseline_a_train": data_dir / "baseline_a_train.csv",
        "runs": data_dir / "runs.csv",
        "cluster_sizes": data_dir / "cluster_sizes.csv",
        "cluster_profiles": data_dir / "cluster_profiles.csv",
        "seed_summary": data_dir / "seed_summary.csv",
        "stability": data_dir / "stability.csv",
    }
    for name, table in (
        ("baseline_a_train", baseline_a(train)), ("runs", runs),
        ("cluster_sizes", sizes), ("cluster_profiles", profiles),
        ("seed_summary", summary), ("stability", stability),
    ):
        table.to_csv(tables[name], index=False, encoding="utf-8", float_format="%.15g")

    figures = {
        f"{metric}_{split}": figures_dir / f"{metric}_{split}.png"
        for metric in ("inertia", "silhouette") for split in ("train", "validation")
    }
    for metric in ("inertia", "silhouette"):
        for split in ("train", "validation"):
            _draw_metric(summary, metric, split, figures[f"{metric}_{split}"])

    if reference_b is None:
        raise AssertionError("Baseline B not produced")
    baseline_b_path = data_dir / "baseline_b.json"
    baseline_b_path.write_text(json.dumps(reference_b, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    metadata = {
        "scope": "fit_train_transform_predict_validation_only",
        "model_features": SPENDING_COLUMNS,
        "excluded_from_fit": ["Channel", "Region"],
        "preprocessing": list(PREPROCESSING),
        "k_values": list(K_VALUES), "seeds": list(SEEDS),
        "n_init": N_INIT, "algorithm": "lloyd", "sklearn_version": sklearn.__version__,
        "rows": {"train": len(train), "validation": len(validation)},
        "runs_expected": 140, "runs_actual": len(runs),
        "scaler_fit_split": "train_only", "kmeans_fit_split": "train_only",
        "validation_policy": "transform_and_predict_only",
        "test_accessed": False, "k_selected": False,
        "inertia_definition": "sum of squared distances to fitted train centroids in each preprocessing space",
        "validation_silhouette_definition": "silhouette on validation points using predicted labels; null when fewer than 2 predicted clusters",
        "undefined_validation_silhouette_runs": int(runs["silhouette_validation"].isna().sum()),
        "stability_definition": "pairwise ARI on train assignments across 45 seed pairs per preprocessing/K",
        "input_sha256": {
            name: _sha256(path) for name, path in (("train", train_path), ("validation", validation_path))
            if path is not None and path.is_file()
        },
        "tables": {name: _relative(path) for name, path in tables.items()},
        "figures": {name: _relative(path) for name, path in figures.items()},
        "baseline_b": _relative(baseline_b_path),
    }
    metadata_path = data_dir / "metadata.json"
    metadata_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8")
    return {"runs": runs, "sizes": sizes, "summary": summary, "metadata": metadata,
            "tables": tables, "figures": figures, "baseline_b": baseline_b_path, "metadata_path": metadata_path}


def main() -> None:
    train = load_split(TRAIN_CSV)
    validation = load_split(VALIDATION_CSV)
    outputs = run_experiments(
        train, validation, train_path=TRAIN_CSV, validation_path=VALIDATION_CSV
    )
    print(f"[experiment] 140 runs: {len(outputs['runs'])}; train={len(train)}, validation={len(validation)}")
    print(f"[experiment] Undefined validation silhouettes: {outputs['metadata']['undefined_validation_silhouette_runs']}")
    print(f"[experiment] CSV/JSON: {EXPERIMENT_DATA_DIR}")
    print(f"[experiment] Figures: {EXPERIMENT_FIGURES_DIR}")
    print("[experiment] Test split untouched; no K selected.")


if __name__ == "__main__":
    main()
