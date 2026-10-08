import numpy as np
import pandas as pd

from ml.src.audit_data import SPENDING_COLUMNS
from ml.src.experiments import (
    DEFAULT_K_VALUES,
    DEFAULT_SEEDS,
    feature_matrix,
    pairwise_ari,
    prepare_matrices,
    run_single_model,
)


def make_frame(rows: int = 40, offset: float = 0.0) -> pd.DataFrame:
    data = {
        "Channel": [1 + (i % 2) for i in range(rows)],
        "Region": [1 + (i % 3) for i in range(rows)],
    }
    for j, feature in enumerate(SPENDING_COLUMNS):
        data[feature] = [
            float(50 + offset + j * 20 + i * (j + 1) + (500 if i >= rows // 2 else 0))
            for i in range(rows)
        ]
    return pd.DataFrame(data)


def test_protocol_defaults_cover_k_2_to_8_and_at_least_10_seeds() -> None:
    assert DEFAULT_K_VALUES == tuple(range(2, 9))
    assert len(DEFAULT_SEEDS) >= 10


def test_feature_matrix_uses_only_six_spending_columns() -> None:
    frame = make_frame()
    values = feature_matrix(frame)
    assert values.shape == (40, 6)
    assert "Channel" not in SPENDING_COLUMNS
    assert "Region" not in SPENDING_COLUMNS


def test_log1p_scaler_is_fit_on_train_only() -> None:
    train = make_frame(rows=20, offset=0.0)
    validation = make_frame(rows=10, offset=1_000_000.0)
    train_values, validation_values, scaler = prepare_matrices(
        train, validation, "log1p_scale"
    )
    assert scaler is not None

    expected_mean = np.log1p(feature_matrix(train)).mean(axis=0)
    np.testing.assert_allclose(scaler.mean_, expected_mean)
    np.testing.assert_allclose(train_values.mean(axis=0), np.zeros(6), atol=1e-10)
    assert not np.allclose(validation_values.mean(axis=0), np.zeros(6), atol=1e-3)


def test_pairwise_ari_is_label_permutation_invariant() -> None:
    labels_a = np.array([0, 0, 1, 1, 2, 2])
    labels_b = np.array([2, 2, 0, 0, 1, 1])
    result = pairwise_ari([labels_a, labels_b])
    assert result["pair_count"] == 1
    assert result["ari_mean"] == 1.0
    assert result["ari_min"] == 1.0


def test_single_model_returns_finite_train_validation_metrics() -> None:
    train = make_frame(rows=60)
    validation = make_frame(rows=30, offset=10.0)
    train_values, validation_values, _ = prepare_matrices(
        train, validation, "log1p_scale"
    )
    row, labels = run_single_model(
        train_values,
        validation_values,
        preprocessing="log1p_scale",
        k=2,
        seed=0,
        n_init=5,
    )
    assert len(labels) == 60
    assert np.isfinite(float(row["train_inertia"]))
    assert np.isfinite(float(row["validation_inertia"]))
    assert np.isfinite(float(row["train_silhouette"]))
    assert np.isfinite(float(row["validation_silhouette"]))
    assert 0.0 < float(row["train_min_cluster_share"]) <= 0.5
