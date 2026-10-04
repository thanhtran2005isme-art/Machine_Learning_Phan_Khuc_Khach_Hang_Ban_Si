import numpy as np
import pandas as pd

from ml.src.audit_data import SPENDING_COLUMNS
from ml.src.profile_candidate import (
    backtransform_centers,
    categorical_profile,
    cluster_median_profile,
    fit_candidate,
    median_ratio_table,
)


def make_frame(rows: int = 60, offset: float = 0.0) -> pd.DataFrame:
    data = {
        "Channel": [1 + (i % 2) for i in range(rows)],
        "Region": [1 + (i % 3) for i in range(rows)],
    }
    for j, feature in enumerate(SPENDING_COLUMNS):
        data[feature] = [
            float(100 + offset + j * 10 + i * (j + 1) + (800 if i >= rows // 2 else 0))
            for i in range(rows)
        ]
    return pd.DataFrame(data)


def test_fit_candidate_uses_only_six_spending_features() -> None:
    train = make_frame(60)
    validation = make_frame(30, offset=5.0)
    model, train_labels, validation_labels, scaler, _, _ = fit_candidate(
        train,
        validation,
        preprocessing="log1p_scale",
        k=2,
        seed=0,
        n_init=5,
    )
    assert model.n_features_in_ == 6
    assert scaler is not None
    assert len(train_labels) == 60
    assert len(validation_labels) == 30


def test_channel_profile_shares_sum_to_one_per_cluster() -> None:
    frame = make_frame(12)
    labels = np.array([0] * 6 + [1] * 6)
    profile = categorical_profile(frame, labels, "Channel")
    sums = profile.groupby("cluster")["share_within_cluster"].sum()
    np.testing.assert_allclose(sums.to_numpy(), np.ones(len(sums)))


def test_cluster_median_profile_keeps_original_units() -> None:
    frame = make_frame(12)
    labels = np.array([0] * 6 + [1] * 6)
    profile = cluster_median_profile(frame, labels)
    assert set(profile.columns) == {"cluster", "count", "share", *SPENDING_COLUMNS}
    assert profile["count"].sum() == 12
    assert profile.loc[0, "Fresh"] == frame.loc[:5, "Fresh"].median()


def test_backtransform_log1p_scale_centers_returns_original_space() -> None:
    train = make_frame(60)
    validation = make_frame(30)
    model, _, _, scaler, _, _ = fit_candidate(
        train,
        validation,
        preprocessing="log1p_scale",
        k=2,
        seed=0,
        n_init=5,
    )
    restored = backtransform_centers(model.cluster_centers_, "log1p_scale", scaler)
    assert restored.shape == (2, 6)
    assert np.isfinite(restored).all()
    assert (restored >= 0).all()


def test_median_ratio_table_uses_train_overall_median() -> None:
    frame = make_frame(12)
    labels = np.array([0] * 6 + [1] * 6)
    profile = cluster_median_profile(frame, labels)
    ratios = median_ratio_table(profile, frame)
    assert ratios.shape == (2, 7)
    assert (ratios[list(SPENDING_COLUMNS)] > 0).all().all()
