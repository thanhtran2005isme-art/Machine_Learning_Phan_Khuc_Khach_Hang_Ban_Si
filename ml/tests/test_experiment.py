import itertools
import json

import numpy as np
import pandas as pd
import pytest
from sklearn.metrics import silhouette_score

from ml.src.audit_data import EXPECTED_COLUMNS, SPENDING_COLUMNS
from ml.src.experiment import (
    K_VALUES,
    PREPROCESSING,
    SEEDS,
    baseline_a,
    evaluate_candidate,
    prepare_features,
    run_experiments,
    squared_distance_inertia,
)


def make_data(n=80, offset=0):
    rng = np.random.default_rng(123 + offset)
    groups = np.arange(n) % 4
    baseline = np.array([[70, 50, 10, 20, 40, 15], [300, 240, 90, 65, 200, 110],
                         [2000, 400, 900, 200, 160, 300], [400, 3000, 2000, 1500, 1000, 800]])
    values = baseline[groups] * rng.lognormal(mean=0, sigma=0.2, size=(n, 6))
    frame = pd.DataFrame(values, columns=SPENDING_COLUMNS)
    frame.insert(0, "Region", 1 + np.arange(n) % 3)
    frame.insert(0, "Channel", 1 + np.arange(n) % 2)
    return frame[EXPECTED_COLUMNS]


@pytest.fixture(scope="module")
def experiment_outputs(tmp_path_factory):
    tmp = tmp_path_factory.mktemp("experiment")
    train, validation = make_data(), make_data(40, offset=1)
    outputs = run_experiments(train, validation, tmp / "data", tmp / "figures")
    return train, validation, outputs


def test_baseline_a_uses_all_six_train_features_without_clustering():
    train = make_data()
    summary = baseline_a(train)
    assert summary["feature"].tolist() == SPENDING_COLUMNS
    assert (summary["count"] == len(train)).all()
    for feature in SPENDING_COLUMNS:
        value = summary.set_index("feature").loc[feature]
        assert value["mean"] == pytest.approx(train[feature].mean())
        assert value["median"] == pytest.approx(train[feature].median())


def test_log_scaler_fits_only_train_and_ignores_profile_columns():
    train, validation = make_data(), make_data(40, offset=1)
    train_scaled, validation_scaled, scaler = prepare_features(train, validation, "log1p_standardscaler")
    assert scaler is not None
    np.testing.assert_allclose(scaler.mean_, np.log1p(train[SPENDING_COLUMNS]).mean(axis=0))
    np.testing.assert_allclose(train_scaled.mean(axis=0), 0, atol=1e-12)
    np.testing.assert_allclose(validation_scaled, scaler.transform(np.log1p(validation[SPENDING_COLUMNS].to_numpy())))

    altered_validation = validation.copy()
    altered_validation.loc[:, SPENDING_COLUMNS] *= 10_000
    other_train, _, other_scaler = prepare_features(train, altered_validation, "log1p_standardscaler")
    np.testing.assert_array_equal(train_scaled, other_train)
    np.testing.assert_array_equal(scaler.mean_, other_scaler.mean_)

    altered_train = train.copy()
    altered_train["Channel"] = 2
    altered_train["Region"] = 3
    raw_a, _, _ = prepare_features(train, validation, "raw")
    raw_b, _, _ = prepare_features(altered_train, validation, "raw")
    np.testing.assert_array_equal(raw_a, raw_b)


def test_metrics_match_independent_reference_and_repeat_exactly():
    train, validation = make_data(), make_data(40, offset=1)
    a, b, _ = prepare_features(train, validation, "log1p_standardscaler")
    result, labels, model = evaluate_candidate(a, b, "log1p_standardscaler", 4, 42)
    assert result["inertia_train"] == pytest.approx(model.inertia_)
    assert result["inertia_validation"] == pytest.approx(
        squared_distance_inertia(b, model.predict(b), model.cluster_centers_)
    )
    assert result["silhouette_train"] == pytest.approx(silhouette_score(a, labels["train"]))
    assert result["silhouette_validation"] == pytest.approx(silhouette_score(b, labels["validation"]))

    repeated, other_labels, other_model = evaluate_candidate(a, b, "log1p_standardscaler", 4, 42)
    assert repeated == result
    np.testing.assert_array_equal(other_labels["train"], labels["train"])
    np.testing.assert_array_equal(other_labels["validation"], labels["validation"])
    np.testing.assert_array_equal(other_model.cluster_centers_, model.cluster_centers_)


def test_grid_cluster_sizes_stability_and_artifacts(experiment_outputs):
    train, validation, outputs = experiment_outputs
    runs, sizes, summary = outputs["runs"], outputs["sizes"], outputs["summary"]
    expected = set(itertools.product(PREPROCESSING, K_VALUES, SEEDS))
    actual = set(runs[["preprocessing", "k", "seed"]].itertuples(index=False, name=None))
    assert len(runs) == 140 == len(expected) == len(actual)
    assert actual == expected
    assert len(summary) == 14
    assert (runs[["inertia_train", "inertia_validation"]] >= 0).all().all()
    assert np.isfinite(runs[["inertia_train", "inertia_validation"]]).all().all()
    for column in ("silhouette_train", "silhouette_validation"):
        defined = runs[column].dropna()
        assert ((defined >= -1) & (defined <= 1)).all()
        assert np.isfinite(defined).all()
    assert (runs["silhouette_validation"].notna() | (
        runs["silhouette_validation_status"] != "ok"
    )).all()
    for (method, k, seed, split), group in sizes.groupby(["preprocessing", "k", "seed", "split"]):
        assert len(group) == k
        assert group["count"].sum() == (len(train) if split == "train" else len(validation))
        assert group["proportion"].sum() == pytest.approx(1)
        assert ((group["proportion"] >= 0) & (group["proportion"] <= 1)).all()
    assert (summary["seed_pairs"] == 45).all()
    assert ((summary["mean_pairwise_ari_train"] >= -1) &
            (summary["mean_pairwise_ari_train"] <= 1)).all()
    for path in [*outputs["tables"].values(), *outputs["figures"].values(),
                 outputs["baseline_b"], outputs["metadata_path"]]:
        assert path.exists() and path.stat().st_size > 100
    baseline_b = json.loads(outputs["baseline_b"].read_text(encoding="utf-8"))
    assert (baseline_b["preprocessing"], baseline_b["k"], baseline_b["seed"]) == ("raw", 2, 42)
    metadata = json.loads(outputs["metadata_path"].read_text(encoding="utf-8"))
    assert metadata["test_accessed"] is False
    assert metadata["k_selected"] is False
    assert metadata["runs_actual"] == 140


def test_input_validation_and_undefined_silhouette():
    train, validation = make_data(), make_data(40, offset=1)
    train.loc[0, "Fresh"] = -1
    with pytest.raises(ValueError, match="Invalid train"):
        run_experiments(train, validation)

    # A degenerate validation prediction cannot legitimately have a silhouette.
    from ml.src.experiment import _silhouette
    score, status = _silhouette(np.zeros((10, 6)), np.zeros(10, dtype=int))
    assert score is None
    assert status.startswith("undefined_")


def test_cli_reads_only_train_and_validation(monkeypatch, tmp_path):
    from ml.src import experiment

    train, validation = make_data(), make_data(40, offset=1)
    train_path, validation_path = tmp_path / "train.csv", tmp_path / "validation.csv"
    train.to_csv(train_path, index=False)
    validation.to_csv(validation_path, index=False)
    monkeypatch.setattr(experiment, "TRAIN_CSV", train_path)
    monkeypatch.setattr(experiment, "VALIDATION_CSV", validation_path)
    reads = []
    original_read = pd.read_csv

    def guarded_read(path, *args, **kwargs):
        reads.append(str(path))
        assert str(path) in {str(train_path), str(validation_path)}
        return original_read(path, *args, **kwargs)

    monkeypatch.setattr(pd, "read_csv", guarded_read)
    monkeypatch.setattr(experiment, "run_experiments", lambda a, b, **kwargs: {
        "runs": [None] * 140, "metadata": {"undefined_validation_silhouette_runs": 0}
    })
    experiment.main()
    assert reads == [str(train_path), str(validation_path)]
