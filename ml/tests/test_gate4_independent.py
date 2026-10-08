"""Independent Gate 4 audit. Only train/validation splits are opened."""

from __future__ import annotations

import json
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from PIL import Image

from ml.src.audit_data import SPENDING_COLUMNS
from ml.src.data_paths import (
    EXPERIMENT_METADATA_JSON,
    EXPERIMENT_RUNS_CSV,
    EXPERIMENT_SELECTION_EVIDENCE_CSV,
    EXPERIMENT_STABILITY_PAIRS_CSV,
    PROFILE_DATA_DIR,
    PROFILE_FIGURES_DIR,
    TRAIN_CSV,
    VALIDATION_CSV,
)
from ml.src.experiments import DEFAULT_K_VALUES, DEFAULT_SEEDS, feature_matrix, prepare_matrices
import ml.src.experiments as experiment_module
from ml.src.profile_candidate import (
    categorical_profile,
    cluster_median_profile,
    distance_summary,
    fit_candidate,
    save_cluster_size_plot,
    save_profile_plot,
)
from ml.src.review_experiments import load_metadata, validate_evidence, validate_stability_pairs


CANDIDATES = (("raw", 2, 42), ("log1p_standardscaler", 2, 42), ("log1p_standardscaler", 3, 42))
FEATURES = list(SPENDING_COLUMNS)


@pytest.fixture(scope="module")
def splits() -> tuple[pd.DataFrame, pd.DataFrame]:
    return pd.read_csv(TRAIN_CSV), pd.read_csv(VALIDATION_CSV)


@pytest.fixture(scope="module", params=CANDIDATES, ids=[f"{p}_k{k}" for p, k, _ in CANDIDATES])
def candidate(request, splits):
    mode, k, seed = request.param
    train, validation = splits
    model, labels_t, labels_v, scaler, x_t, x_v = fit_candidate(
        train, validation, preprocessing=mode, k=k, seed=seed
    )
    name = f"{mode}_k{k}_seed{seed}"
    directory = PROFILE_DATA_DIR / name
    figures = PROFILE_FIGURES_DIR / name
    return (train, validation, model, labels_t, labels_v, scaler, x_t, x_v, directory, figures, mode, k)


def _csv(directory: Path, name: str) -> pd.DataFrame:
    return pd.read_csv(directory / f"{name}.csv").sort_values("cluster").reset_index(drop=True)


def test_medians_in_original_units_and_cluster_shares(candidate):
    train, validation, _, labels_t, labels_v, _, _, _, directory, _, _, k = candidate
    for split, labels, prefix in ((train, labels_t, "train"), (validation, labels_v, "validation")):
        table = _csv(directory, f"{prefix}_median_profile")
        expected = sorted(set(labels))
        assert table.cluster.tolist() == expected
        assert int(table["count"].sum()) == len(split)
        np.testing.assert_allclose(table["share"].sum(), 1, atol=1e-12)
        for row in table.itertuples(index=False):
            members = split.loc[labels == row.cluster, FEATURES].to_numpy(dtype=float)
            np.testing.assert_allclose([getattr(row, f) for f in FEATURES],
                                       np.median(members, axis=0), rtol=0, atol=1e-7)
            assert row.count == len(members)
            np.testing.assert_allclose(row.share, len(members) / len(split), atol=1e-12)
    quality = _csv(directory, "cluster_quality")
    assert quality.cluster.tolist() == list(range(k))
    assert quality.train_count.sum() == len(train)
    assert quality.validation_count.sum() == len(validation)
    np.testing.assert_allclose(quality.train_share, np.bincount(labels_t, minlength=k) / len(train))
    np.testing.assert_allclose(quality.validation_share, np.bincount(labels_v, minlength=k) / len(validation))
    assert (quality.small_train_cluster_below_5pct.to_numpy() == (quality.train_share < .05).to_numpy()).all()
    np.testing.assert_allclose(quality.abs_train_validation_share_gap,
                               np.abs(quality.train_share - quality.validation_share))


def test_inverse_centroids_and_train_only_scaling(candidate):
    train, validation, model, _, _, scaler, x_t, x_v, directory, _, mode, _ = candidate
    if mode == "raw":
        expected = model.cluster_centers_
        np.testing.assert_array_equal(x_t, train[FEATURES].to_numpy(dtype=float))
        np.testing.assert_array_equal(x_v, validation[FEATURES].to_numpy(dtype=float))
    else:
        logtrain = np.log1p(train[FEATURES].to_numpy(dtype=float))
        logvalidation = np.log1p(validation[FEATURES].to_numpy(dtype=float))
        np.testing.assert_allclose(scaler.mean_, logtrain.mean(axis=0), atol=1e-12)
        np.testing.assert_allclose(x_t, (logtrain - scaler.mean_) / scaler.scale_, atol=1e-12)
        np.testing.assert_allclose(x_v, (logvalidation - scaler.mean_) / scaler.scale_, atol=1e-12)
        expected = np.expm1(model.cluster_centers_ * scaler.scale_ + scaler.mean_)
    centroid = _csv(directory, "centroids_original_units")
    np.testing.assert_allclose(centroid[FEATURES].to_numpy(), expected, rtol=1e-10, atol=1e-8)
    assert model.n_features_in_ == 6
    assert model._n_threads >= 1


def test_euclidean_distance_and_iqr_outliers_independently(candidate):
    _, _, model, labels_t, labels_v, _, x_t, x_v, directory, _, _, _ = candidate
    for prefix, values, labels in (("train", x_t, labels_t), ("validation", x_v, labels_v)):
        recorded = _csv(directory, f"{prefix}_distance_summary")
        # Independent Euclidean norm; avoid model.transform and production distance_summary.
        d = np.sqrt(np.sum(np.square(values - model.cluster_centers_[labels]), axis=1))
        assert len(d) == len(labels) and np.isfinite(d).all() and (d >= 0).all()
        for row in recorded.itertuples(index=False):
            values_cluster = pd.Series(d[labels == row.cluster])
            q1, q3 = values_cluster.quantile([.25, .75])
            threshold = q3 + 1.5 * (q3 - q1)
            assert row.count == len(values_cluster)
            for field, expected in (("mean", values_cluster.mean()), ("median", values_cluster.median()),
                                    ("p90", values_cluster.quantile(.90)), ("p95", values_cluster.quantile(.95)),
                                    ("max", values_cluster.max()), ("iqr_outlier_threshold", threshold)):
                np.testing.assert_allclose(getattr(row, field), expected, rtol=1e-10, atol=1e-8)
            assert row.iqr_outlier_count == int((values_cluster > threshold).sum())
        assert int(recorded["count"].sum()) == len(labels)
        # Quantify the influence of the largest 1% of observations on inertia.
        squared = np.sort(d ** 2)
        tail = squared[-max(1, int(np.ceil(len(squared) * .01))):]
        assert 0 <= tail.sum() / squared.sum() <= 1


def test_channel_region_descriptive_only(candidate):
    train, validation, _, labels_t, labels_v, _, _, _, directory, _, _, _ = candidate
    for split, labels, prefix in ((train, labels_t, "train"), (validation, labels_v, "validation")):
        for column in ("Channel", "Region"):
            reported = _csv(directory, f"{prefix}_{column.lower()}_profile")
            independent = pd.crosstab(labels, split[column].to_numpy())
            for row in reported.itertuples(index=False):
                assert row.count == independent.loc[row.cluster, getattr(row, column)]
                np.testing.assert_allclose(row.share_within_cluster,
                                           row.count / independent.loc[row.cluster].sum())


def test_median_ratio_csv_matches_actual_plot_and_cluster_sizes(candidate, tmp_path):
    train, _, _, labels_t, _, _, _, _, directory, figures, _, _ = candidate
    median_csv = _csv(directory, "train_median_profile")
    ratio_csv = _csv(directory, "train_median_ratio")
    size_csv = _csv(directory, "cluster_quality")
    np.testing.assert_allclose(ratio_csv[FEATURES],
                               median_csv[FEATURES].to_numpy() / train[FEATURES].median().to_numpy(),
                               rtol=1e-12, atol=1e-12)
    assert len(ratio_csv) == len(np.unique(labels_t))
    assert (size_csv.train_share >= 0).all()
    regenerated_ratio = tmp_path / "median_ratio.png"
    regenerated_sizes = tmp_path / "cluster_sizes.png"
    save_profile_plot(ratio_csv, regenerated_ratio)
    save_cluster_size_plot(median_csv, regenerated_sizes)
    for expected, actual in ((figures / "median_ratio.png", regenerated_ratio),
                             (figures / "cluster_sizes.png", regenerated_sizes)):
        with Image.open(expected) as recorded, Image.open(actual) as regenerated:
            assert recorded.size == regenerated.size
            assert recorded.width >= 600 and recorded.height >= 400
            np.testing.assert_array_equal(np.asarray(recorded.convert("RGB")),
                                          np.asarray(regenerated.convert("RGB")))


@pytest.mark.parametrize("bad", [np.array([0., 1., 1.]), np.array([0, -1, 1]),
                                  np.array([0, 1]),
                                  np.array([0, np.nan, 1]), np.array([0, np.inf, 1]),
                                  np.array([0, "foo", 1]), np.array([[0], [1], [1]])])
def test_malformed_labels_are_rejected(bad):
    frame = pd.DataFrame({feature: [10., 20., 30.] for feature in FEATURES})
    with pytest.raises((ValueError, TypeError)):
        cluster_median_profile(frame, bad)
    with pytest.raises((ValueError, TypeError)):
        categorical_profile(frame.assign(Channel=[1, 2, 1]), bad, "Channel")


@pytest.mark.parametrize("bad", [np.array([0., 1., 1.]), np.array([0, 1]),
                                  np.array([0, -1, 1]), np.array([0, 2, 1]),
                                  np.array([0, np.nan, 1])])
def test_malformed_distance_labels_are_rejected(bad, splits):
    train, validation = splits
    model, _, _, _, _, _ = fit_candidate(train, validation, preprocessing="raw", k=2, seed=42)
    with pytest.raises((ValueError, TypeError)):
        distance_summary(np.ones((3, 6)), bad, model)


@pytest.mark.parametrize("bad", [1, 9, 2.0, True, "3"])
def test_invalid_k_is_rejected(bad, splits):
    with pytest.raises(ValueError):
        fit_candidate(*splits, preprocessing="raw", k=bad, seed=42)


@pytest.mark.parametrize("field,bad", [("seed", -1), ("seed", 1.2), ("seed", True),
                                         ("n_init", 0), ("n_init", 1.2), ("n_init", True)])
def test_invalid_seed_and_n_init_are_rejected(field, bad, splits):
    kwargs = dict(preprocessing="raw", k=2, seed=42, n_init=10)
    kwargs[field] = bad
    with pytest.raises(ValueError):
        fit_candidate(*splits, **kwargs)


@pytest.mark.parametrize("mutation", ["missing", "text", "nan", "inf", "negative"])
def test_invalid_spending_data_is_rejected(mutation, splits):
    frame = splits[0].copy()
    if mutation == "missing":
        frame = frame.drop(columns=[FEATURES[0]])
    else:
        frame[FEATURES[0]] = frame[FEATURES[0]].astype(object)
        frame.loc[0, FEATURES[0]] = {"text": "invalid", "nan": np.nan,
                                      "inf": np.inf, "negative": -10}[mutation]
    with pytest.raises(ValueError):
        feature_matrix(frame)
    with pytest.raises(ValueError):
        prepare_matrices(frame, splits[1], "log1p_standardscaler")


@pytest.mark.parametrize("field,value", [("test_used", True), ("selection_status", "FROZEN"),
                                           ("n_init", 11), ("seeds", [42]),
                                           ("k_values", [2]), ("runs_actual", 139),
                                           ("ari_pair_count", 629), ("feature_columns", ["Channel"]),
                                           ("max_iter", 200), ("seed_count", 9),
                                           ("scope", "train_validation_test"),
                                           ("profiling_only_columns", ["Channel", "Fresh"]),
                                           ("scaler_metadata", {})])
def test_invalid_metadata_is_rejected(field, value, tmp_path):
    original = json.loads(EXPERIMENT_METADATA_JSON.read_text(encoding="utf-8"))
    original[field] = value
    p = tmp_path / "invalid_metadata.json"
    p.write_text(json.dumps(original), encoding="utf-8")
    with pytest.raises(ValueError):
        load_metadata(p)


def test_missing_and_corrupt_metadata_rejected(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_metadata(tmp_path / "missing.json")
    corrupt = tmp_path / "bad.json"
    corrupt.write_text("not-json", encoding="utf-8")
    with pytest.raises(ValueError):
        load_metadata(corrupt)


@pytest.mark.parametrize("bad", [np.array([[1., np.nan] * 3]),
                                  np.array([[1., np.inf] * 3]),
                                  np.array([1., 2., 3.]),
                                  np.array([["bad"] * 6])])
def test_invalid_distance_matrices_are_rejected(bad, splits):
    model, _, _, _, _, _ = fit_candidate(*splits, preprocessing="raw", k=2, seed=42)
    with pytest.raises((ValueError, TypeError)):
        distance_summary(bad, np.zeros(len(bad), dtype=int), model)


def test_140_unique_runs_630_unique_ari_pairs_and_metric_domains():
    runs = pd.read_csv(EXPERIMENT_RUNS_CSV)
    expected_runs = set(product(("raw", "log1p_standardscaler"), DEFAULT_K_VALUES, DEFAULT_SEEDS))
    actual = list(runs[["preprocessing", "k", "seed"]].itertuples(index=False, name=None))
    assert len(actual) == len(set(actual)) == len(expected_runs) == 140
    assert set(actual) == expected_runs
    for field in ("train_inertia", "validation_inertia"):
        assert np.isfinite(runs[field]).all() and (runs[field] >= 0).all()
    for field in ("train_silhouette", "validation_silhouette"):
        assert np.isfinite(runs[field]).all() and runs[field].between(-1, 1).all()
    pairs = pd.read_csv(EXPERIMENT_STABILITY_PAIRS_CSV)
    validate_stability_pairs(pairs)
    evidence = pd.read_csv(EXPERIMENT_SELECTION_EVIDENCE_CSV)
    validate_evidence(evidence)
    assert len(evidence) == 14 and len(pairs) == 630


def test_pairwise_evidence_rejects_duplicates_missing_reversed_and_invalid_ari():
    frame = pd.read_csv(EXPERIMENT_STABILITY_PAIRS_CSV)
    for bad in (frame.iloc[:-1], pd.concat([frame.iloc[:-1], frame.iloc[[0]]]),
                frame.assign(seed_a=frame.seed_b, seed_b=frame.seed_a),
                frame.assign(ari=np.inf), frame.assign(ari=1.1)):
        with pytest.raises(ValueError):
            validate_stability_pairs(bad)


def test_reproducible_labels_centroids_and_predictions(splits):
    train, validation = splits
    for mode, k, seed in CANDIDATES:
        one = fit_candidate(train, validation, preprocessing=mode, k=k, seed=seed)
        two = fit_candidate(train, validation, preprocessing=mode, k=k, seed=seed)
        np.testing.assert_array_equal(one[1], two[1])
        np.testing.assert_array_equal(one[2], two[2])
        np.testing.assert_allclose(one[0].cluster_centers_, two[0].cluster_centers_, rtol=1e-12, atol=1e-12)
        np.testing.assert_allclose(one[4], two[4], rtol=1e-12, atol=1e-12)


def test_leakage_guard_validation_changes_do_not_change_fitted_model(splits):
    train, validation = splits
    perturbed = validation.copy()
    perturbed[FEATURES] = validation[FEATURES] * 100 + 200000
    for mode, k, seed in CANDIDATES:
        original = fit_candidate(train, validation, preprocessing=mode, k=k, seed=seed)
        changed = fit_candidate(train, perturbed, preprocessing=mode, k=k, seed=seed)
        np.testing.assert_array_equal(original[1], changed[1])
        np.testing.assert_allclose(original[0].cluster_centers_, changed[0].cluster_centers_, atol=1e-12)
        if mode != "raw":
            np.testing.assert_allclose(original[3].mean_, changed[3].mean_, atol=1e-12)
            np.testing.assert_allclose(original[3].scale_, changed[3].scale_, atol=1e-12)
    meta = load_metadata()
    assert meta["test_used"] is False and meta["selection_status"] == "NOT_SELECTED"


def test_full_experiment_isolated_outputs_and_no_final_test_access(monkeypatch, tmp_path):
    """Execute the 140-run harness with a path guard and temporary artifacts."""
    output_names = {
        "EXPERIMENT_BASELINE_DESCRIPTIVE_CSV": "baseline_descriptive.csv",
        "EXPERIMENT_BASELINE_K2_CSV": "baseline_k2.csv",
        "EXPERIMENT_RUNS_CSV": "runs.csv",
        "EXPERIMENT_AGGREGATE_CSV": "aggregate.csv",
        "EXPERIMENT_STABILITY_CSV": "stability.csv",
        "EXPERIMENT_STABILITY_PAIRS_CSV": "stability_pairs.csv",
        "EXPERIMENT_SELECTION_EVIDENCE_CSV": "selection_evidence.csv",
        "EXPERIMENT_METADATA_JSON": "experiment_metadata.json",
    }
    output_dir = tmp_path / "data"
    figure_dir = tmp_path / "figures"
    monkeypatch.setattr(experiment_module, "EXPERIMENT_DATA_DIR", output_dir)
    monkeypatch.setattr(experiment_module, "EXPERIMENT_FIGURES_DIR", figure_dir)
    for symbol, filename in output_names.items():
        monkeypatch.setattr(experiment_module, symbol, output_dir / filename)

    opened_splits = []
    original_loader = experiment_module.load_split
    original_reader = pd.read_csv

    def guarded_reader(filepath, *args, **kwargs):
        if isinstance(filepath, (str, Path)) and Path(filepath).name.lower() == "test.csv":
            raise AssertionError("Final test access forbidden in Gate 4")
        return original_reader(filepath, *args, **kwargs)

    def guarded_loader(path):
        path = Path(path).resolve()
        assert path in {TRAIN_CSV.resolve(), VALIDATION_CSV.resolve()}
        opened_splits.append(path)
        return original_loader(path)

    monkeypatch.setattr(pd, "read_csv", guarded_reader)
    monkeypatch.setattr(experiment_module, "load_split", guarded_loader)
    experiment_module.run_experiments()
    assert opened_splits == [TRAIN_CSV.resolve(), VALIDATION_CSV.resolve()]
    assert len(original_reader(output_dir / "runs.csv")) == 140
    assert len(original_reader(output_dir / "stability_pairs.csv")) == 630
    generated_meta = json.loads((output_dir / "experiment_metadata.json").read_text(encoding="utf-8"))
    assert generated_meta["test_used"] is False
    assert generated_meta["selection_status"] == "NOT_SELECTED"
