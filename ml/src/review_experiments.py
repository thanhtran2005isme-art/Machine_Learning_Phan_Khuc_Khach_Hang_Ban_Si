from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

try:
    from .audit_data import SPENDING_COLUMNS
    from .data_paths import (
        EXPERIMENT_METADATA_JSON,
        EXPERIMENT_REVIEW_CSV,
        EXPERIMENT_REVIEW_MD,
        EXPERIMENT_SELECTION_EVIDENCE_CSV,
    )
    from .experiments import DEFAULT_K_VALUES, DEFAULT_N_INIT, DEFAULT_SEEDS, PREPROCESSING_MODES
except ImportError:
    from audit_data import SPENDING_COLUMNS
    from data_paths import (
        EXPERIMENT_METADATA_JSON,
        EXPERIMENT_REVIEW_CSV,
        EXPERIMENT_REVIEW_MD,
        EXPERIMENT_SELECTION_EVIDENCE_CSV,
    )
    from experiments import DEFAULT_K_VALUES, DEFAULT_N_INIT, DEFAULT_SEEDS, PREPROCESSING_MODES

REQUIRED_COLUMNS = {
    "preprocessing",
    "k",
    "run_count",
    "train_inertia_mean",
    "train_inertia_std",
    "validation_inertia_mean",
    "validation_inertia_std",
    "train_silhouette_mean",
    "train_silhouette_std",
    "validation_silhouette_mean",
    "validation_silhouette_std",
    "min_cluster_share_mean",
    "min_cluster_share_min",
    "ari_mean",
    "ari_std",
    "ari_min",
    "ari_max",
    "pair_count",
}


def load_evidence(path: Path = EXPERIMENT_SELECTION_EVIDENCE_CSV) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(
            f"Chưa có {path}. Chạy python ml/src/experiments.py trước."
        )
    frame = pd.read_csv(path)
    validate_evidence(frame)
    return frame


def validate_evidence(frame: pd.DataFrame) -> None:
    missing = sorted(REQUIRED_COLUMNS - set(frame.columns))
    if missing:
        raise ValueError(f"selection_evidence thiếu cột bắt buộc: {missing}")

    expected_pairs = {
        (mode, k) for mode in PREPROCESSING_MODES for k in DEFAULT_K_VALUES
    }
    try:
        if frame["k"].isna().any() or not np.isfinite(pd.to_numeric(frame["k"], errors="coerce")).all():
            raise ValueError("K không hợp lệ")
        if (frame["k"].astype(float) % 1 != 0).any():
            raise ValueError("K phải nguyên")
        actual_pairs = {
            (str(row.preprocessing), int(row.k))
            for row in frame[["preprocessing", "k"]].itertuples(index=False)
        }
    except (TypeError, ValueError) as exc:
        raise ValueError("Evidence chứa K hoặc preprocessing không hợp lệ.") from exc
    if actual_pairs != expected_pairs:
        missing_pairs = sorted(expected_pairs - actual_pairs)
        extra_pairs = sorted(actual_pairs - expected_pairs)
        raise ValueError(
            "Evidence không phủ đúng protocol 2 preprocessing x K=2..8. "
            f"missing={missing_pairs}; extra={extra_pairs}"
        )

    if len(frame) != len(expected_pairs):
        raise ValueError("Evidence có dòng trùng preprocessing/K.")

    numeric_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column != "preprocessing"
    ]
    try:
        numeric = frame[numeric_columns].apply(pd.to_numeric, errors="raise")
        values = numeric.to_numpy(dtype=float)
    except (ValueError, TypeError) as exc:
        raise ValueError("Evidence chứa metric không phải số.") from exc
    if not np.isfinite(values).all():
        raise ValueError("Evidence chứa NaN hoặc +/-inf ở metric bắt buộc.")
    if not (numeric["run_count"] == len(DEFAULT_SEEDS)).all():
        raise ValueError("Mỗi preprocessing/K phải có đúng 10 seed runs.")
    if not (numeric["pair_count"] == 45).all():
        raise ValueError("Mỗi candidate phải có chính xác 45 cặp seed ARI.")
    for metric in ("train_inertia_mean", "validation_inertia_mean", "train_inertia_std", "validation_inertia_std", "train_silhouette_std", "validation_silhouette_std", "ari_std"):
        if (numeric[metric] < 0).any():
            raise ValueError(f"Metric {metric} không được âm.")
    for metric in ("train_silhouette_mean", "validation_silhouette_mean", "ari_mean", "ari_min", "ari_max"):
        if not numeric[metric].between(-1, 1).all():
            raise ValueError(f"Metric {metric} ngoài [-1, 1].")
    for metric in ("min_cluster_share_mean", "min_cluster_share_min"):
        if not numeric[metric].between(0, 1).all():
            raise ValueError(f"Metric {metric} ngoài [0, 1].")
    if (numeric["ari_min"] > numeric["ari_mean"]).any() or (numeric["ari_mean"] > numeric["ari_max"]).any():
        raise ValueError("ARI min/mean/max không nhất quán.")


def validate_stability_pairs(pairs: pd.DataFrame) -> None:
    required = {"preprocessing", "k", "seed_a", "seed_b", "ari"}
    if not required.issubset(pairs.columns):
        raise ValueError("Thiếu cột trong bảng 630 cặp ARI.")
    expected = {
        (mode, k, a, b)
        for mode in PREPROCESSING_MODES for k in DEFAULT_K_VALUES
        for i, a in enumerate(DEFAULT_SEEDS) for b in DEFAULT_SEEDS[i + 1:]
    }
    actual = list(pairs[["preprocessing", "k", "seed_a", "seed_b"]].itertuples(index=False, name=None))
    if len(actual) != 630 or len(set(actual)) != 630 or set(actual) != expected:
        raise ValueError("ARI pairs thiếu, trùng, đảo chiều hoặc sai seed; yêu cầu đúng 630 cặp.")
    try:
        numeric = pd.to_numeric(pairs["ari"], errors="raise")
    except (TypeError, ValueError) as exc:
        raise ValueError("ARI phải là số.") from exc
    if not np.isfinite(numeric).all() or not numeric.between(-1, 1).all():
        raise ValueError("ARI không hữu hạn hoặc ngoài [-1,1].")


def load_metadata(path: Path = EXPERIMENT_METADATA_JSON) -> dict:
    if not path.exists():
        raise FileNotFoundError(
            f"Chưa có {path}. Chạy python ml/src/experiments.py trước."
        )
    metadata = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(metadata, dict):
        raise ValueError("Experiment metadata phải là JSON object.")
    if metadata.get("test_used") is not False:
        raise ValueError("Metadata phải xác nhận test_used=false trước model selection.")
    if metadata.get("selection_status") != "NOT_SELECTED":
        raise ValueError(
            "Review script chỉ dùng trước khi freeze lựa chọn; selection_status phải là NOT_SELECTED."
        )
    if (metadata.get("k_values") != list(DEFAULT_K_VALUES)
            or metadata.get("seeds") != list(DEFAULT_SEEDS)
            or metadata.get("n_init") != DEFAULT_N_INIT
            or metadata.get("runs_actual") != 140
            or metadata.get("ari_pair_count") != 630
            or not isinstance(metadata.get("preprocessing_modes"), dict)
            or set(metadata["preprocessing_modes"]) != set(PREPROCESSING_MODES)
            or metadata.get("stability_pairs_file") != "stability_pairs.csv"
            or metadata.get("feature_columns") != list(SPENDING_COLUMNS)):
        raise ValueError("Experiment metadata không khớp protocol D010 hoặc thiếu evidence.")
    return metadata


def build_review_table(frame: pd.DataFrame) -> pd.DataFrame:
    review = frame.copy()
    review["silhouette_generalization_gap_abs"] = (
        review["train_silhouette_mean"] - review["validation_silhouette_mean"]
    ).abs()
    review["silhouette_generalization_gap_signed"] = (
        review["validation_silhouette_mean"] - review["train_silhouette_mean"]
    )
    review["validation_silhouette_rank"] = review.groupby("preprocessing")[
        "validation_silhouette_mean"
    ].rank(method="min", ascending=False)
    review["stability_ari_rank"] = review.groupby("preprocessing")["ari_mean"].rank(
        method="min", ascending=False
    )
    review["smallest_cluster_share_rank"] = review.groupby("preprocessing")[
        "min_cluster_share_mean"
    ].rank(method="min", ascending=False)
    for name, metric in (("validation_silhouette_global_rank", "validation_silhouette_mean"),
                         ("stability_ari_global_rank", "ari_mean"),
                         ("smallest_cluster_share_global_rank", "min_cluster_share_mean")):
        review[name] = review[metric].rank(method="min", ascending=False)
    review["small_cluster_below_5pct_flag"] = review["min_cluster_share_min"] < 0.05

    ordered_columns = [
        "preprocessing",
        "k",
        "run_count",
        "train_silhouette_mean",
        "validation_silhouette_mean",
        "silhouette_generalization_gap_abs",
        "silhouette_generalization_gap_signed",
        "validation_silhouette_std",
        "ari_mean",
        "ari_min",
        "ari_std",
        "min_cluster_share_mean",
        "min_cluster_share_min",
        "train_inertia_mean",
        "train_inertia_std",
        "validation_inertia_mean",
        "validation_inertia_std",
        "validation_silhouette_rank",
        "stability_ari_rank",
        "smallest_cluster_share_rank",
        "validation_silhouette_global_rank",
        "stability_ari_global_rank",
        "smallest_cluster_share_global_rank",
        "small_cluster_below_5pct_flag",
    ]
    return review[ordered_columns].sort_values(["preprocessing", "k"]).reset_index(drop=True)


def _markdown_table(frame: pd.DataFrame, columns: list[str]) -> str:
    headers = "| " + " | ".join(columns) + " |"
    separator = "|" + "|".join(["---"] * len(columns)) + "|"
    rows: list[str] = []
    for row in frame[columns].itertuples(index=False, name=None):
        formatted: list[str] = []
        for value in row:
            if isinstance(value, (float, np.floating)):
                formatted.append(f"{float(value):.4f}")
            else:
                formatted.append(str(value))
        rows.append("| " + " | ".join(formatted) + " |")
    return "\n".join([headers, separator, *rows])


def build_markdown(review: pd.DataFrame) -> str:
    sections = [
        "# Experiment Review — chưa chọn K",
        "",
        "> File này chỉ tổng hợp bằng chứng train/validation. Không phải quyết định model cuối.",
        "> Test vẫn khóa và không được dùng ở bước này.",
        "",
        "## Nguyên tắc đọc",
        "",
        "- Không chọn K chỉ vì silhouette cao nhất.",
        "- Phải đọc cùng lúc silhouette validation, stability ARI, cluster size, inertia/elbow và khả năng diễn giải profile.",
        "- Inertia không dùng để so trực tiếp giữa hai preprocessing vì không gian/scale khác nhau.",
        "- Các rank dưới đây chỉ giúp rà soát từng tiêu chí riêng, **không được cộng thành điểm tổng**.",
        "",
    ]

    columns = [
        "k",
        "validation_silhouette_mean",
        "ari_mean",
        "ari_min",
        "min_cluster_share_mean",
        "silhouette_generalization_gap_abs",
    ]
    for mode in PREPROCESSING_MODES:
        group = review[review["preprocessing"] == mode].sort_values("k")
        sections.extend(
            [
                f"## {mode}",
                "",
                _markdown_table(group, columns),
                "",
                "### Candidate cần xem profile trước khi freeze",
                "",
                "Dựa trên bảng trên, nhóm phải chọn một shortlist nhỏ để profile median chi tiêu + Channel/Region. Không tự động freeze K trong bước review này.",
                "",
            ]
        )
    return "\n".join(sections)


def review_experiments(
    evidence_path: Path = EXPERIMENT_SELECTION_EVIDENCE_CSV,
    metadata_path: Path = EXPERIMENT_METADATA_JSON,
) -> pd.DataFrame:
    evidence = load_evidence(evidence_path)
    metadata = load_metadata(metadata_path)
    pair_path = evidence_path.parent / metadata["stability_pairs_file"]
    if not pair_path.is_file():
        raise FileNotFoundError(f"Thiếu ARI pair-level evidence: {pair_path}")
    pairs = pd.read_csv(pair_path)
    validate_stability_pairs(pairs)
    for candidate in evidence.itertuples(index=False):
        p = pairs[(pairs["preprocessing"] == candidate.preprocessing) & (pairs["k"] == candidate.k)]["ari"]
        if (not np.isclose(p.mean(), candidate.ari_mean, atol=1e-10)
                or not np.isclose(p.min(), candidate.ari_min, atol=1e-10)
                or not np.isclose(p.std(ddof=0), candidate.ari_std, atol=1e-10)):
            raise ValueError("Aggregate ARI lệch so với 630 ARI pairs nguồn.")
    review = build_review_table(evidence)

    EXPERIMENT_REVIEW_CSV.parent.mkdir(parents=True, exist_ok=True)
    EXPERIMENT_REVIEW_MD.parent.mkdir(parents=True, exist_ok=True)
    review.to_csv(EXPERIMENT_REVIEW_CSV, index=False, encoding="utf-8")
    EXPERIMENT_REVIEW_MD.write_text(build_markdown(review), encoding="utf-8")

    print(f"[review] Candidates: {len(review)} (2 preprocessing x 7 K)")
    print(f"[review] CSV: {EXPERIMENT_REVIEW_CSV}")
    print(f"[review] Markdown: {EXPERIMENT_REVIEW_MD}")
    for mode in PREPROCESSING_MODES:
        group = review[review["preprocessing"] == mode]
        best_sil = group.loc[group["validation_silhouette_mean"].idxmax()]
        best_ari = group.loc[group["ari_mean"].idxmax()]
        print(
            f"[review] {mode}: silhouette cao nhất tại K={int(best_sil['k'])}; "
            f"ARI cao nhất tại K={int(best_ari['k'])}."
        )
    print("[review] Chưa chọn K. Hãy profile shortlist và review đa tiêu chí trước khi freeze.")
    return review


def main() -> None:
    review_experiments()


if __name__ == "__main__":
    main()
