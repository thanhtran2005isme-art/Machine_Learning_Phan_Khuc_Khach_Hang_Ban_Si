from __future__ import annotations

import argparse
import json
from itertools import combinations
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score, silhouette_score
from sklearn.preprocessing import StandardScaler

try:
    from .audit_data import SPENDING_COLUMNS
    from .data_paths import (
        EXPERIMENT_AGGREGATE_CSV,
        EXPERIMENT_BASELINE_DESCRIPTIVE_CSV,
        EXPERIMENT_BASELINE_K2_CSV,
        EXPERIMENT_DATA_DIR,
        EXPERIMENT_FIGURES_DIR,
        EXPERIMENT_METADATA_JSON,
        EXPERIMENT_RUNS_CSV,
        EXPERIMENT_SELECTION_EVIDENCE_CSV,
        EXPERIMENT_STABILITY_CSV,
        TRAIN_CSV,
        VALIDATION_CSV,
    )
except ImportError:
    from audit_data import SPENDING_COLUMNS
    from data_paths import (
        EXPERIMENT_AGGREGATE_CSV,
        EXPERIMENT_BASELINE_DESCRIPTIVE_CSV,
        EXPERIMENT_BASELINE_K2_CSV,
        EXPERIMENT_DATA_DIR,
        EXPERIMENT_FIGURES_DIR,
        EXPERIMENT_METADATA_JSON,
        EXPERIMENT_RUNS_CSV,
        EXPERIMENT_SELECTION_EVIDENCE_CSV,
        EXPERIMENT_STABILITY_CSV,
        TRAIN_CSV,
        VALIDATION_CSV,
    )

PREPROCESSING_MODES = ("raw", "log1p_scale")
DEFAULT_K_VALUES = tuple(range(2, 9))
DEFAULT_SEEDS = tuple(range(10))
DEFAULT_N_INIT = 20
DEFAULT_MAX_ITER = 300
BASELINE_SEED = 42


def load_split(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(
            f"Không tìm thấy split tại {path}. Chạy python ml/src/prepare_data.py trước."
        )
    df = pd.read_csv(path)
    missing = [column for column in SPENDING_COLUMNS if column not in df.columns]
    if missing:
        raise ValueError(f"Thiếu feature bắt buộc: {missing}")
    return df


def feature_matrix(df: pd.DataFrame) -> np.ndarray:
    values = df[SPENDING_COLUMNS].to_numpy(dtype=float, copy=True)
    if not np.isfinite(values).all():
        raise ValueError("Feature chứa NaN hoặc +/-inf.")
    if (values < 0).any():
        raise ValueError("Feature chi tiêu có giá trị âm; không thể áp dụng log1p an toàn.")
    return values


def prepare_matrices(
    train_df: pd.DataFrame,
    validation_df: pd.DataFrame,
    mode: str,
) -> tuple[np.ndarray, np.ndarray, StandardScaler | None]:
    train_raw = feature_matrix(train_df)
    validation_raw = feature_matrix(validation_df)

    if mode == "raw":
        return train_raw, validation_raw, None
    if mode != "log1p_scale":
        raise ValueError(f"Preprocessing mode không hỗ trợ: {mode}")

    train_log = np.log1p(train_raw)
    validation_log = np.log1p(validation_raw)
    scaler = StandardScaler()
    train_transformed = scaler.fit_transform(train_log)
    validation_transformed = scaler.transform(validation_log)
    return train_transformed, validation_transformed, scaler


def safe_silhouette(values: np.ndarray, labels: np.ndarray) -> float:
    unique_labels = np.unique(labels)
    if len(unique_labels) < 2 or len(unique_labels) >= len(values):
        return float("nan")
    return float(silhouette_score(values, labels))


def assigned_inertia(
    values: np.ndarray,
    labels: np.ndarray,
    centers: np.ndarray,
) -> float:
    residuals = values - centers[labels]
    return float(np.square(residuals).sum())


def cluster_size_stats(labels: np.ndarray) -> tuple[str, int, int, float, float]:
    unique, counts = np.unique(labels, return_counts=True)
    ordered = {int(label): int(count) for label, count in zip(unique, counts, strict=True)}
    minimum = int(counts.min())
    maximum = int(counts.max())
    total = int(counts.sum())
    return (
        json.dumps(ordered, sort_keys=True),
        minimum,
        maximum,
        minimum / total,
        maximum / total,
    )


def run_single_model(
    train_values: np.ndarray,
    validation_values: np.ndarray,
    *,
    preprocessing: str,
    k: int,
    seed: int,
    n_init: int = DEFAULT_N_INIT,
    max_iter: int = DEFAULT_MAX_ITER,
) -> tuple[dict[str, float | int | str], np.ndarray]:
    model = KMeans(
        n_clusters=k,
        random_state=seed,
        n_init=n_init,
        max_iter=max_iter,
        algorithm="lloyd",
    )
    train_labels = model.fit_predict(train_values)
    validation_labels = model.predict(validation_values)

    sizes_json, minimum, maximum, min_share, max_share = cluster_size_stats(train_labels)
    row: dict[str, float | int | str] = {
        "preprocessing": preprocessing,
        "k": k,
        "seed": seed,
        "n_init": n_init,
        "train_inertia": float(model.inertia_),
        "validation_inertia": assigned_inertia(
            validation_values, validation_labels, model.cluster_centers_
        ),
        "train_silhouette": safe_silhouette(train_values, train_labels),
        "validation_silhouette": safe_silhouette(validation_values, validation_labels),
        "train_cluster_sizes": sizes_json,
        "train_min_cluster_size": minimum,
        "train_max_cluster_size": maximum,
        "train_min_cluster_share": min_share,
        "train_max_cluster_share": max_share,
        "validation_distinct_clusters": int(len(np.unique(validation_labels))),
        "n_iter": int(model.n_iter_),
    }
    return row, train_labels


def pairwise_ari(labelings: list[np.ndarray]) -> dict[str, float | int]:
    if len(labelings) < 2:
        return {
            "pair_count": 0,
            "ari_mean": float("nan"),
            "ari_std": float("nan"),
            "ari_min": float("nan"),
            "ari_max": float("nan"),
        }
    scores = [
        adjusted_rand_score(left, right)
        for left, right in combinations(labelings, 2)
    ]
    values = np.asarray(scores, dtype=float)
    return {
        "pair_count": int(len(values)),
        "ari_mean": float(values.mean()),
        "ari_std": float(values.std(ddof=0)),
        "ari_min": float(values.min()),
        "ari_max": float(values.max()),
    }


def aggregate_runs(runs: pd.DataFrame) -> pd.DataFrame:
    return (
        runs.groupby(["preprocessing", "k"], as_index=False)
        .agg(
            run_count=("seed", "count"),
            train_inertia_mean=("train_inertia", "mean"),
            train_inertia_std=("train_inertia", "std"),
            validation_inertia_mean=("validation_inertia", "mean"),
            validation_inertia_std=("validation_inertia", "std"),
            train_silhouette_mean=("train_silhouette", "mean"),
            train_silhouette_std=("train_silhouette", "std"),
            validation_silhouette_mean=("validation_silhouette", "mean"),
            validation_silhouette_std=("validation_silhouette", "std"),
            min_cluster_share_mean=("train_min_cluster_share", "mean"),
            min_cluster_share_min=("train_min_cluster_share", "min"),
            max_cluster_share_mean=("train_max_cluster_share", "mean"),
            n_iter_mean=("n_iter", "mean"),
        )
        .sort_values(["preprocessing", "k"])
        .reset_index(drop=True)
    )


def baseline_descriptive(train_df: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, float | str]] = []
    for feature in SPENDING_COLUMNS:
        series = train_df[feature].astype(float)
        rows.append(
            {
                "feature": feature,
                "mean": float(series.mean()),
                "median": float(series.median()),
                "std": float(series.std(ddof=1)),
                "q1": float(series.quantile(0.25)),
                "q3": float(series.quantile(0.75)),
                "iqr": float(series.quantile(0.75) - series.quantile(0.25)),
            }
        )
    return pd.DataFrame(rows)


def save_line_plot(
    frame: pd.DataFrame,
    *,
    y_column: str,
    title: str,
    ylabel: str,
    output_path: Path,
) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))
    for preprocessing, group in frame.groupby("preprocessing"):
        ordered = group.sort_values("k")
        ax.plot(ordered["k"], ordered[y_column], marker="o", label=preprocessing)
    ax.set_title(title)
    ax.set_xlabel("K")
    ax.set_ylabel(ylabel)
    ax.set_xticks(list(DEFAULT_K_VALUES))
    ax.grid(alpha=0.25)
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)


def run_experiments(
    train_path: Path = TRAIN_CSV,
    validation_path: Path = VALIDATION_CSV,
    *,
    k_values: tuple[int, ...] = DEFAULT_K_VALUES,
    seeds: tuple[int, ...] = DEFAULT_SEEDS,
    n_init: int = DEFAULT_N_INIT,
) -> dict:
    if len(seeds) < 10:
        raise ValueError("Thiết kế bắt buộc ít nhất 10 seed để đánh giá stability.")
    if tuple(k_values) != DEFAULT_K_VALUES:
        raise ValueError("Protocol chính yêu cầu K = 2..8.")

    train_df = load_split(train_path)
    validation_df = load_split(validation_path)
    EXPERIMENT_DATA_DIR.mkdir(parents=True, exist_ok=True)
    EXPERIMENT_FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    baseline_descriptive(train_df).to_csv(
        EXPERIMENT_BASELINE_DESCRIPTIVE_CSV, index=False, encoding="utf-8"
    )

    transformed: dict[str, tuple[np.ndarray, np.ndarray]] = {}
    scaler_metadata: dict[str, dict | None] = {}
    for mode in PREPROCESSING_MODES:
        train_values, validation_values, scaler = prepare_matrices(
            train_df, validation_df, mode
        )
        transformed[mode] = (train_values, validation_values)
        scaler_metadata[mode] = (
            None
            if scaler is None
            else {
                "mean": [float(value) for value in scaler.mean_],
                "scale": [float(value) for value in scaler.scale_],
                "fit_scope": "train_only_after_log1p",
            }
        )

    baseline_train, baseline_validation = transformed["raw"]
    baseline_k2, _ = run_single_model(
        baseline_train,
        baseline_validation,
        preprocessing="raw",
        k=2,
        seed=BASELINE_SEED,
        n_init=n_init,
    )
    pd.DataFrame([baseline_k2]).to_csv(
        EXPERIMENT_BASELINE_K2_CSV, index=False, encoding="utf-8"
    )

    run_rows: list[dict[str, float | int | str]] = []
    labels_by_key: dict[tuple[str, int], list[np.ndarray]] = {}

    for mode in PREPROCESSING_MODES:
        train_values, validation_values = transformed[mode]
        for k in k_values:
            labels_by_key[(mode, k)] = []
            for seed in seeds:
                row, train_labels = run_single_model(
                    train_values,
                    validation_values,
                    preprocessing=mode,
                    k=k,
                    seed=seed,
                    n_init=n_init,
                )
                run_rows.append(row)
                labels_by_key[(mode, k)].append(train_labels)

    runs = pd.DataFrame(run_rows)
    aggregate = aggregate_runs(runs)

    stability_rows: list[dict[str, float | int | str]] = []
    for (mode, k), labelings in labels_by_key.items():
        stability_rows.append(
            {
                "preprocessing": mode,
                "k": k,
                **pairwise_ari(labelings),
            }
        )
    stability = pd.DataFrame(stability_rows).sort_values(["preprocessing", "k"])
    evidence = aggregate.merge(stability, on=["preprocessing", "k"], how="left")

    runs.to_csv(EXPERIMENT_RUNS_CSV, index=False, encoding="utf-8")
    aggregate.to_csv(EXPERIMENT_AGGREGATE_CSV, index=False, encoding="utf-8")
    stability.to_csv(EXPERIMENT_STABILITY_CSV, index=False, encoding="utf-8")
    evidence.to_csv(EXPERIMENT_SELECTION_EVIDENCE_CSV, index=False, encoding="utf-8")

    save_line_plot(
        aggregate,
        y_column="train_inertia_mean",
        title="Elbow evidence — train inertia mean",
        ylabel="Mean train inertia",
        output_path=EXPERIMENT_FIGURES_DIR / "elbow_train.png",
    )
    save_line_plot(
        aggregate,
        y_column="validation_silhouette_mean",
        title="Validation silhouette across K",
        ylabel="Mean validation silhouette",
        output_path=EXPERIMENT_FIGURES_DIR / "validation_silhouette.png",
    )
    save_line_plot(
        evidence,
        y_column="ari_mean",
        title="Seed stability across K",
        ylabel="Mean pairwise ARI",
        output_path=EXPERIMENT_FIGURES_DIR / "stability_ari.png",
    )
    save_line_plot(
        aggregate,
        y_column="min_cluster_share_mean",
        title="Smallest cluster share across K",
        ylabel="Mean smallest-cluster share",
        output_path=EXPERIMENT_FIGURES_DIR / "min_cluster_share.png",
    )

    metadata = {
        "scope": "train_and_validation_only",
        "test_used": False,
        "test_policy": "Do not read test until preprocessing and K are frozen.",
        "feature_columns": list(SPENDING_COLUMNS),
        "profiling_only_columns": ["Channel", "Region"],
        "preprocessing_modes": {
            "raw": "No learned preprocessing; six spending columns in original units.",
            "log1p_scale": "np.log1p then StandardScaler fit on train only; validation uses transform only.",
        },
        "k_values": list(k_values),
        "seeds": list(seeds),
        "seed_count": len(seeds),
        "n_init": n_init,
        "max_iter": DEFAULT_MAX_ITER,
        "stability_metric": "mean pairwise Adjusted Rand Index on train assignments across seeds",
        "selection_status": "NOT_SELECTED",
        "selection_rule": (
            "Review validation silhouette, elbow/inertia, ARI stability, cluster sizes and interpretability together. "
            "Do not auto-select K from one metric."
        ),
        "baseline": {
            "descriptive_no_clustering": str(EXPERIMENT_BASELINE_DESCRIPTIVE_CSV.name),
            "k2": {
                "preprocessing": "raw",
                "seed": BASELINE_SEED,
                "note": "Simple reproducible K=2 reference; not the final model decision.",
            },
        },
        "scaler_metadata": scaler_metadata,
    }
    EXPERIMENT_METADATA_JSON.write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"[experiment] TRAIN={len(train_df)}; VALIDATION={len(validation_df)}; TEST=NOT TOUCHED")
    print(f"[experiment] Features: {', '.join(SPENDING_COLUMNS)}")
    print(f"[experiment] Preprocessing: {', '.join(PREPROCESSING_MODES)}")
    print(f"[experiment] K: {min(k_values)}..{max(k_values)}")
    print(f"[experiment] Seeds: {len(seeds)} ({min(seeds)}..{max(seeds)})")
    print(f"[experiment] Runs: {len(runs)}")
    print(f"[experiment] Evidence: {EXPERIMENT_SELECTION_EVIDENCE_CSV}")
    print("[experiment] Chưa chọn K và chưa đọc test. Hãy review evidence trước khi freeze quyết định.")
    return metadata


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Chạy baseline + K-Means K=2..8, >=10 seed trên train/validation; không đọc test."
    )
    parser.add_argument("--n-init", type=int, default=DEFAULT_N_INIT)
    args = parser.parse_args()
    run_experiments(n_init=args.n_init)


if __name__ == "__main__":
    main()
