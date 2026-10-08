import pandas as pd
import pytest

from ml.src.experiments import DEFAULT_K_VALUES, PREPROCESSING_MODES
from ml.src.review_experiments import build_review_table, validate_evidence


def make_evidence() -> pd.DataFrame:
    rows = []
    for mode_index, mode in enumerate(PREPROCESSING_MODES):
        for k in DEFAULT_K_VALUES:
            rows.append(
                {
                    "preprocessing": mode,
                    "k": k,
                    "run_count": 10,
                    "train_inertia_mean": 1000.0 / k + mode_index,
                    "train_inertia_std": 1.0,
                    "validation_inertia_mean": 400.0 / k + mode_index,
                    "validation_inertia_std": 1.5,
                    "train_silhouette_mean": 0.40 + 0.01 * k,
                    "train_silhouette_std": 0.01,
                    "validation_silhouette_mean": 0.35 + 0.01 * k,
                    "validation_silhouette_std": 0.02,
                    "min_cluster_share_mean": 1.0 / (k + 1),
                    "min_cluster_share_min": 0.5 / (k + 1),
                    "max_cluster_share_mean": 0.5,
                    "n_iter_mean": 5.0,
                    "pair_count": 45,
                    "ari_mean": 0.90 - 0.01 * k,
                    "ari_std": 0.01,
                    "ari_min": 0.80 - 0.01 * k,
                    "ari_max": 1.0,
                }
            )
    return pd.DataFrame(rows)


def test_validate_evidence_accepts_complete_protocol() -> None:
    validate_evidence(make_evidence())


def test_validate_evidence_rejects_missing_candidate() -> None:
    frame = make_evidence().iloc[:-1].copy()
    with pytest.raises(ValueError, match="không phủ đúng protocol"):
        validate_evidence(frame)


def test_build_review_table_adds_independent_ranks_without_total_score() -> None:
    review = build_review_table(make_evidence())
    assert len(review) == 14
    assert "validation_silhouette_rank" in review.columns
    assert "stability_ari_rank" in review.columns
    assert "smallest_cluster_share_rank" in review.columns
    assert "total_score" not in review.columns
    assert "silhouette_generalization_gap_abs" in review.columns
