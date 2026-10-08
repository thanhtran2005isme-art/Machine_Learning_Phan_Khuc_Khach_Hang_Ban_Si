from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

try:
    from .audit_data import SPENDING_COLUMNS
    from .data_paths import PROFILE_DATA_DIR, PROFILE_FIGURES_DIR, TRAIN_CSV, VALIDATION_CSV
    from .experiments import (
        DEFAULT_K_VALUES,
        DEFAULT_MAX_ITER,
        DEFAULT_N_INIT,
        DEFAULT_SEEDS,
        PREPROCESSING_MODES,
        load_split,
        prepare_matrices,
    )
    from .review_experiments import load_metadata
    from .data_paths import EXPERIMENT_METADATA_JSON
except ImportError:
    from audit_data import SPENDING_COLUMNS
    from data_paths import PROFILE_DATA_DIR, PROFILE_FIGURES_DIR, TRAIN_CSV, VALIDATION_CSV
    from experiments import (
        DEFAULT_K_VALUES,
        DEFAULT_MAX_ITER,
        DEFAULT_N_INIT,
        DEFAULT_SEEDS,
        PREPROCESSING_MODES,
        load_split,
        prepare_matrices,
    )
    from review_experiments import load_metadata
    from data_paths import EXPERIMENT_METADATA_JSON

PROFILE_ONLY_COLUMNS = ("Channel", "Region")


def validated_labels(labels: np.ndarray, sample_count: int, k: int | None = None) -> np.ndarray:
    """Reject malformed cluster labels instead of silently truncating floats."""
    array = np.asarray(labels)
    if array.ndim != 1 or len(array) != sample_count or sample_count == 0:
        raise ValueError("Nhãn cụm sai kích thước hoặc không phải vector.")
    if array.dtype.kind not in "iu" or array.dtype.kind == "b":
        raise ValueError("Nhãn cụm phải là số nguyên.")
    if (array < 0).any() or (k is not None and (array >= k).any()):
        raise ValueError("Nhãn cụm ngoài phạm vi centroid.")
    return array.astype(int, copy=False)


def fit_candidate(
    train_df: pd.DataFrame,
    validation_df: pd.DataFrame,
    *,
    preprocessing: str,
    k: int,
    seed: int,
    n_init: int = DEFAULT_N_INIT,
) -> tuple[KMeans, np.ndarray, np.ndarray, StandardScaler | None, np.ndarray, np.ndarray]:
    if preprocessing not in PREPROCESSING_MODES:
        raise ValueError(f"preprocessing phải thuộc {PREPROCESSING_MODES}")
    if isinstance(k, (bool, np.bool_)) or not isinstance(k, (int, np.integer)) or k not in DEFAULT_K_VALUES:
        raise ValueError(f"k phải thuộc {DEFAULT_K_VALUES}")
    if (not isinstance(seed, (int, np.integer)) or isinstance(seed, (bool, np.bool_)) or seed < 0
            or not isinstance(n_init, (int, np.integer)) or isinstance(n_init, (bool, np.bool_)) or n_init < 1):
        raise ValueError("Seed phải nguyên không âm và n_init >= 1.")

    train_values, validation_values, scaler = prepare_matrices(
        train_df, validation_df, preprocessing
    )
    model = KMeans(
        n_clusters=k,
        random_state=seed,
        n_init=n_init,
        max_iter=DEFAULT_MAX_ITER,
        algorithm="lloyd",
    )
    train_labels = model.fit_predict(train_values)
    validation_labels = model.predict(validation_values)
    return model, train_labels, validation_labels, scaler, train_values, validation_values


def cluster_median_profile(df: pd.DataFrame, labels: np.ndarray) -> pd.DataFrame:
    labels = validated_labels(labels, len(df))
    labeled = df[list(SPENDING_COLUMNS)].copy()
    labeled.insert(0, "cluster", labels.astype(int))
    medians = labeled.groupby("cluster", as_index=False)[list(SPENDING_COLUMNS)].median()
    counts = labeled.groupby("cluster", as_index=False).size().rename(columns={"size": "count"})
    counts["share"] = counts["count"] / len(labeled)
    return counts.merge(medians, on="cluster", how="left").sort_values("cluster").reset_index(drop=True)


def categorical_profile(df: pd.DataFrame, labels: np.ndarray, column: str) -> pd.DataFrame:
    if column not in PROFILE_ONLY_COLUMNS:
        raise ValueError(f"Profiling categorical chỉ hỗ trợ {PROFILE_ONLY_COLUMNS}")
    if column not in df:
        raise ValueError("Thiếu cột profiling hoặc labels sai kích thước.")
    labels = validated_labels(labels, len(df))
    labeled = pd.DataFrame({"cluster": labels.astype(int), column: df[column].to_numpy()})
    counts = (
        labeled.groupby(["cluster", column], as_index=False)
        .size()
        .rename(columns={"size": "count"})
    )
    totals = counts.groupby("cluster")["count"].transform("sum")
    counts["share_within_cluster"] = counts["count"] / totals
    return counts.sort_values(["cluster", column]).reset_index(drop=True)


def distance_summary(values: np.ndarray, labels: np.ndarray, model: KMeans) -> pd.DataFrame:
    values = np.asarray(values)
    if values.ndim != 2 or not np.issubdtype(values.dtype, np.number) or not np.isfinite(values).all():
        raise ValueError("Distance yêu cầu ma trận feature số hữu hạn.")
    labels = validated_labels(labels, len(values), len(model.cluster_centers_))
    distances = model.transform(values)
    assigned = distances[np.arange(len(values)), labels]
    frame = pd.DataFrame({"cluster": labels.astype(int), "distance_to_centroid": assigned})
    rows: list[dict[str, float | int]] = []
    for cluster, group in frame.groupby("cluster"):
        series = group["distance_to_centroid"]
        q1, q3 = series.quantile([0.25, 0.75])
        threshold = q3 + 1.5 * (q3 - q1)
        rows.append(
            {
                "cluster": int(cluster),
                "count": int(len(series)),
                "mean": float(series.mean()),
                "median": float(series.median()),
                "p90": float(series.quantile(0.90)),
                "p95": float(series.quantile(0.95)),
                "max": float(series.max()),
                "iqr_outlier_threshold": float(threshold),
                "iqr_outlier_count": int((series > threshold).sum()),
            }
        )
    return pd.DataFrame(rows).sort_values("cluster").reset_index(drop=True)


def backtransform_centers(
    centers: np.ndarray,
    preprocessing: str,
    scaler: StandardScaler | None,
) -> np.ndarray:
    if preprocessing == "raw":
        return centers.copy()
    if preprocessing != "log1p_standardscaler" or scaler is None:
        raise ValueError("log1p_standardscaler cần scaler đã fit trên train.")
    log_centers = scaler.inverse_transform(centers)
    return np.expm1(log_centers)


def centroid_table(model: KMeans, preprocessing: str, scaler: StandardScaler | None) -> pd.DataFrame:
    original_units = backtransform_centers(model.cluster_centers_, preprocessing, scaler)
    frame = pd.DataFrame(original_units, columns=SPENDING_COLUMNS)
    frame.insert(0, "cluster", np.arange(len(frame), dtype=int))
    return frame


def median_ratio_table(train_profile: pd.DataFrame, train_df: pd.DataFrame) -> pd.DataFrame:
    overall = train_df[list(SPENDING_COLUMNS)].median().astype(float)
    if (overall == 0).any():
        raise ValueError("Không thể tạo median ratio vì overall median có feature bằng 0.")
    ratios = train_profile[["cluster", *SPENDING_COLUMNS]].copy()
    for feature in SPENDING_COLUMNS:
        ratios[feature] = ratios[feature] / float(overall[feature])
    return ratios


def save_profile_plot(ratios: pd.DataFrame, output_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(10, 5.5))
    x = np.arange(len(SPENDING_COLUMNS))
    for row in ratios.itertuples(index=False):
        values = [float(getattr(row, feature)) for feature in SPENDING_COLUMNS]
        ax.plot(x, values, marker="o", label=f"Cluster {int(row.cluster)}")
    ax.axhline(1.0, linewidth=1, linestyle="--", label="Overall train median")
    ax.set_xticks(x)
    ax.set_xticklabels(SPENDING_COLUMNS, rotation=25, ha="right")
    ax.set_ylabel("Cluster median / overall train median")
    ax.set_title("Candidate cluster profile — median spending ratio")
    ax.grid(alpha=0.25)
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)


def save_cluster_size_plot(profile: pd.DataFrame, output_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.bar(profile["cluster"].astype(str), profile["share"])
    ax.set_xlabel("Cluster")
    ax.set_ylabel("Share of train")
    ax.set_title("Candidate cluster sizes — train")
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)


def profile_candidate(
    *,
    preprocessing: str,
    k: int,
    seed: int,
    n_init: int = DEFAULT_N_INIT,
    train_path: Path = TRAIN_CSV,
    validation_path: Path = VALIDATION_CSV,
    experiment_metadata_path: Path = EXPERIMENT_METADATA_JSON,
) -> dict:
    meta = load_metadata(experiment_metadata_path)
    if (preprocessing not in PREPROCESSING_MODES or k not in DEFAULT_K_VALUES
            or seed not in DEFAULT_SEEDS or n_init != meta["n_init"]):
        raise ValueError("Candidate config không khớp grid seed=42..51/n_init=10/K=2..8.")
    train_df = load_split(train_path)
    validation_df = load_split(validation_path)

    model, train_labels, validation_labels, scaler, train_values, validation_values = fit_candidate(
        train_df,
        validation_df,
        preprocessing=preprocessing,
        k=k,
        seed=seed,
        n_init=n_init,
    )

    candidate_name = f"{preprocessing}_k{k}_seed{seed}"
    data_dir = PROFILE_DATA_DIR / candidate_name
    figure_dir = PROFILE_FIGURES_DIR / candidate_name
    data_dir.mkdir(parents=True, exist_ok=True)
    figure_dir.mkdir(parents=True, exist_ok=True)

    train_profile = cluster_median_profile(train_df, train_labels)
    validation_profile = cluster_median_profile(validation_df, validation_labels)
    cluster_sizes = pd.DataFrame({"cluster": range(k)}).merge(
        train_profile[["cluster", "count", "share"]], on="cluster", how="left"
    ).rename(columns={"count": "train_count", "share": "train_share"}).merge(
        validation_profile[["cluster", "count", "share"]].rename(
            columns={"count": "validation_count", "share": "validation_share"}),
        on="cluster", how="left"
    ).fillna(0)
    cluster_sizes["small_train_cluster_below_5pct"] = cluster_sizes["train_share"] < 0.05
    cluster_sizes["abs_train_validation_share_gap"] = (
        cluster_sizes["train_share"] - cluster_sizes["validation_share"]
    ).abs()
    ratios = median_ratio_table(train_profile, train_df)

    artifacts: dict[str, Path] = {
        "train_median_profile": data_dir / "train_median_profile.csv",
        "validation_median_profile": data_dir / "validation_median_profile.csv",
        "train_channel_profile": data_dir / "train_channel_profile.csv",
        "train_region_profile": data_dir / "train_region_profile.csv",
        "validation_channel_profile": data_dir / "validation_channel_profile.csv",
        "validation_region_profile": data_dir / "validation_region_profile.csv",
        "train_distance_summary": data_dir / "train_distance_summary.csv",
        "validation_distance_summary": data_dir / "validation_distance_summary.csv",
        "centroids_original_units": data_dir / "centroids_original_units.csv",
        "train_median_ratio": data_dir / "train_median_ratio.csv",
        "cluster_quality": data_dir / "cluster_quality.csv",
        "metadata": data_dir / "profile_metadata.json",
        "profile_plot": figure_dir / "median_ratio.png",
        "size_plot": figure_dir / "cluster_sizes.png",
    }

    train_profile.to_csv(artifacts["train_median_profile"], index=False, encoding="utf-8")
    validation_profile.to_csv(artifacts["validation_median_profile"], index=False, encoding="utf-8")
    cluster_sizes.to_csv(artifacts["cluster_quality"], index=False, encoding="utf-8")
    categorical_profile(train_df, train_labels, "Channel").to_csv(
        artifacts["train_channel_profile"], index=False, encoding="utf-8"
    )
    categorical_profile(train_df, train_labels, "Region").to_csv(
        artifacts["train_region_profile"], index=False, encoding="utf-8"
    )
    categorical_profile(validation_df, validation_labels, "Channel").to_csv(
        artifacts["validation_channel_profile"], index=False, encoding="utf-8"
    )
    categorical_profile(validation_df, validation_labels, "Region").to_csv(
        artifacts["validation_region_profile"], index=False, encoding="utf-8"
    )
    distance_summary(train_values, train_labels, model).to_csv(
        artifacts["train_distance_summary"], index=False, encoding="utf-8"
    )
    distance_summary(validation_values, validation_labels, model).to_csv(
        artifacts["validation_distance_summary"], index=False, encoding="utf-8"
    )
    centroid_table(model, preprocessing, scaler).to_csv(
        artifacts["centroids_original_units"], index=False, encoding="utf-8"
    )
    ratios.to_csv(artifacts["train_median_ratio"], index=False, encoding="utf-8")
    save_profile_plot(ratios, artifacts["profile_plot"])
    save_cluster_size_plot(train_profile, artifacts["size_plot"])

    metadata = {
        "scope": "train_and_validation_only",
        "test_used": False,
        "selection_status": "CANDIDATE_PROFILE_ONLY",
        "not_final_model": True,
        "candidate": {
            "preprocessing": preprocessing,
            "k": k,
            "seed": seed,
            "n_init": n_init,
            "max_iter": DEFAULT_MAX_ITER,
        },
        "feature_columns": list(SPENDING_COLUMNS),
        "profiling_only_columns": list(PROFILE_ONLY_COLUMNS),
        "fit_scope": "train_only",
        "train_count": len(train_df),
        "validation_count": len(validation_df),
        "validation_clusters_present": int(len(np.unique(validation_labels))),
        "small_train_clusters_below_5pct": int(cluster_sizes["small_train_cluster_below_5pct"].sum()),
        "experiment_metadata": str(experiment_metadata_path),
        "validation_policy": "predict_only_with_train-fitted preprocessing/model",
        "interpretation_policy": (
            "Use median spending in original units as the primary cluster profile; Channel/Region are descriptive only and never ground truth."
        ),
        "centroid_note": (
            "For log1p_standardscaler, centroids are inverse-transformed to original units for reference; median profiles remain the preferred interpretation."
        ),
        "artifacts": {key: str(path) for key, path in artifacts.items() if key != "metadata"},
    }
    artifacts["metadata"].write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(
        f"[profile] Candidate={preprocessing}, K={k}, seed={seed}; TRAIN={len(train_df)}, VALIDATION={len(validation_df)}, TEST=NOT TOUCHED"
    )
    print(f"[profile] Data: {data_dir}")
    print(f"[profile] Figures: {figure_dir}")
    print("[profile] Channel/Region chỉ dùng profiling sau khi cluster labels đã được tạo.")
    print("[profile] Đây chưa phải final model; chưa mở test và chưa freeze lựa chọn.")
    return metadata


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Profile một candidate K-Means bằng median + Channel/Region; không đọc test."
    )
    parser.add_argument("--preprocessing", choices=PREPROCESSING_MODES, required=True)
    parser.add_argument("--k", type=int, choices=DEFAULT_K_VALUES, required=True)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEEDS[0])
    parser.add_argument("--n-init", type=int, default=DEFAULT_N_INIT)
    args = parser.parse_args()
    profile_candidate(
        preprocessing=args.preprocessing,
        k=args.k,
        seed=args.seed,
        n_init=args.n_init,
    )


if __name__ == "__main__":
    main()
