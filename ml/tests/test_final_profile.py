"""Gate 9.2 regression: only the historical development split, no fit/final test."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import pytest

from ml.src.data_paths import PROJECT_ROOT, TRAIN_CSV, VALIDATION_CSV
from ml.src.final_profile import build_tables, frozen_predict, generate_profile, load_development


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@pytest.fixture(scope="module")
def dev():
    return load_development(PROJECT_ROOT, TRAIN_CSV, VALIDATION_CSV)


def test_development_frozen_counts_medians_and_categories(dev):
    frame, model, provenance = dev
    labels, distances = frozen_predict(frame, model)
    assert len(frame) == 352 and set(labels) == {0, 1}
    assert np.bincount(labels, minlength=2).tolist() == [162, 190]
    assert np.isfinite(distances).all() and (distances >= 0).all()
    tables, info = build_tables(frame, model)
    assert info["cluster_counts"] == {"0": 162, "1": 190}
    assert sum(info["cluster_counts"].values()) == 352
    assert info["inertia_per_row"] > 0
    for i in (0, 1):
        members = frame.loc[labels == i]
        summary = tables["cluster_summary.csv"].iloc[i]
        assert summary["count"] == len(members)
        assert np.isclose(summary["share"], len(members) / 352, atol=1e-12)
        for feature in model["feature_columns"]:
            assert np.isclose(summary[feature], members[feature].median(), atol=1e-10)
    for source in ["Channel", "Region"]:
        table = tables[source.lower() + "_profile.csv"]
        assert table["count"].sum() == 352
        for cluster in (0, 1):
            counts = table.loc[table["cluster"] == cluster]
            assert counts["count"].sum() == int((labels == cluster).sum())
            assert np.isclose(counts["within_cluster_share"].sum(), 1, atol=1e-12)
    assert provenance["model_sha256"] and provenance["selection_sha256"]


def test_exact_frozen_joblib_matches_portable_on_all_development(dev):
    frame, model, _ = dev
    pipeline = joblib.load(PROJECT_ROOT / "models/model.joblib")
    raw = frame[model["feature_columns"]].to_numpy(dtype=float)
    x = pipeline["scaler"].transform(np.log1p(raw))
    expected_labels = pipeline["model"].predict(x)
    expected_distances = pipeline["model"].transform(x)
    labels, chosen = frozen_predict(frame, model)
    np.testing.assert_array_equal(labels, expected_labels)
    np.testing.assert_allclose(
        chosen, expected_distances[np.arange(len(labels)), labels], atol=1e-8, rtol=1e-8
    )


def test_deterministic_metadata_and_artifacts(dev, tmp_path):
    before = [file_sha(PROJECT_ROOT / p) for p in
              ("models/model.json", "models/model.joblib", "models/selection.json",
               "models/final_evaluation.json")]
    first, second = tmp_path / "first", tmp_path / "second"
    m1 = generate_profile(output=first)
    m2 = generate_profile(output=second)
    assert m1 == m2
    assert m1["status"] == "COMPLETE"
    assert m1["model_fit_performed"] is False
    assert m1["scaler_fit_performed"] is False
    assert m1["test_used"] is False
    assert m1["source_rows"] == {"train": 264, "validation": 88}
    for name, meta in m1["files"].items():
        data1, data2 = (first / name).read_bytes(), (second / name).read_bytes()
        assert data1 == data2
        assert hashlib.sha256(data1).hexdigest() == meta["sha256"]
    assert (first / "profile_metadata.json").read_bytes() == (second / "profile_metadata.json").read_bytes()
    after = [file_sha(PROJECT_ROOT / p) for p in
             ("models/model.json", "models/model.joblib", "models/selection.json",
              "models/final_evaluation.json")]
    assert before == after


def test_corrupted_development_split_fails_closed(tmp_path):
    corrupted = tmp_path / "train.csv"
    corrupted.write_bytes(TRAIN_CSV.read_bytes() + b"bad-extra-row\n")
    with pytest.raises(ValueError, match="checksum"):
        generate_profile(train=corrupted, output=tmp_path / "out")
    assert not (tmp_path / "out").exists()


def test_missing_validation_does_not_write_artifacts(tmp_path):
    with pytest.raises(FileNotFoundError):
        generate_profile(validation=tmp_path / "missing.csv", output=tmp_path / "out")
    assert not (tmp_path / "out").exists()


def test_model_tampering_is_detected(tmp_path):
    source = PROJECT_ROOT / "models"
    destination = tmp_path / "models"
    destination.mkdir()
    for name in ("model.json", "selection.json", "final_evaluation.json"):
        (destination / name).write_bytes((source / name).read_bytes())
    obj = json.loads((destination / "model.json").read_text(encoding="utf-8"))
    obj["cluster_centers"][0][0] += 0.5
    (destination / "model.json").write_text(json.dumps(obj), encoding="utf-8")
    with pytest.raises(ValueError, match="checksum"):
        generate_profile(root=tmp_path, train=TRAIN_CSV, validation=VALIDATION_CSV,
                         output=tmp_path / "out")
    assert not (tmp_path / "out").exists()


def test_does_not_access_test_split(monkeypatch, tmp_path):
    real_reader = pd.read_csv
    seen = []
    def guarded_reader(path, *args, **kwargs):
        seen.append(Path(path).name)
        if Path(path).name.lower() == "test.csv":
            raise AssertionError("Gate 9.2 must never read held-out test data")
        return real_reader(path, *args, **kwargs)
    monkeypatch.setattr(pd, "read_csv", guarded_reader)
    generate_profile(output=tmp_path / "output")
    assert seen == ["train.csv", "validation.csv"]


def test_no_model_or_scaler_fit_used(monkeypatch, tmp_path):
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import StandardScaler
    def blocked(*_args, **_kwargs):
        raise AssertionError("No training/refit is allowed in Gate 9.2")
    monkeypatch.setattr(KMeans, "fit", blocked)
    monkeypatch.setattr(KMeans, "fit_predict", blocked)
    monkeypatch.setattr(StandardScaler, "fit", blocked)
    monkeypatch.setattr(StandardScaler, "fit_transform", blocked)
    generate_profile(output=tmp_path / "profile")
    assert (tmp_path / "profile/cluster_summary.csv").exists()
