"""Gate 10.2 evidence and leakage regression, no final held-out evaluation."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from sklearn.metrics import adjusted_rand_score, silhouette_score

from ml.src.data_paths import PROJECT_ROOT, TRAIN_CSV, VALIDATION_CSV
from ml.src.development_extension import create_extension
from ml.src.final_profile import frozen_predict, load_development


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


@pytest.fixture(scope="module")
def actual(tmp_path_factory):
    path = tmp_path_factory.mktemp("development-extension")
    meta = create_extension(output=path)
    data = json.loads((path / "analysis.json").read_text(encoding="utf-8"))
    return path, meta, data


def test_only_352_real_development_rows_and_frozen_labels(actual):
    _, meta, data = actual
    frame, model, provenance = load_development(PROJECT_ROOT, TRAIN_CSV, VALIDATION_CSV)
    label, _ = frozen_predict(frame, model)
    points = data["points"]
    assert len(points) == 352
    assert [p["index"] for p in points] == list(range(352))
    assert [p["split"] for p in points] == ["train"] * 264 + ["validation"] * 88
    assert [p["kmeans"] for p in points] == label.tolist()
    assert all(np.isfinite([p["pc1"], p["pc2"]]).all() for p in points)
    assert all(set(p) == {"index","split","pc1","pc2","kmeans","hierarchical"} for p in points)
    assert meta["provenance"] == provenance
    assert meta["test_used"] is False and meta["serving_model_changed"] is False


def test_pca_valid_and_ward_6d_comparison(actual):
    _, _, data = actual
    p = data["pca"]
    assert len(p["explained_variance_ratio"]) == 2
    assert all(0 < v < 1 for v in p["explained_variance_ratio"])
    assert sum(p["explained_variance_ratio"]) <= 1 + 1e-9
    components = np.asarray(p["components"])
    assert components.shape == (2, 6)
    np.testing.assert_allclose(components @ components.T, np.eye(2), atol=1e-9)
    r = data["comparison"]
    assert r["fit_space"] == "frozen 6D log1p+StandardScaler"
    assert r["frozen_counts"] == [162,190]
    assert sum(r["hierarchical_counts"]) == 352 and min(r["hierarchical_counts"]) > 0
    labels = np.asarray([x["kmeans"] for x in data["points"]])
    ward = np.asarray([x["hierarchical"] for x in data["points"]])
    assert r["contingency"] == [[int(np.count_nonzero((labels == i) & (ward == j)))
                                for j in (0,1)] for i in (0,1)]
    assert np.isclose(r["ari"], adjusted_rand_score(labels, ward), atol=1e-12)
    frame, model, _ = load_development(PROJECT_ROOT, TRAIN_CSV, VALIDATION_CSV)
    X = (np.log1p(frame[model["feature_columns"]].to_numpy())-model["scaler_mean"])/model["scaler_scale"]
    assert np.isclose(r["silhouette_kmeans"], silhouette_score(X, labels), atol=1e-12)
    assert np.isclose(r["silhouette_hierarchical"], silhouette_score(X, ward), atol=1e-12)


def test_deterministic_and_untouched_frozen_artifacts(tmp_path, actual):
    first, metadata, _ = actual
    frozen_files = [PROJECT_ROOT / ("models/" + f) for f in
                    ("selection.json","model.json","model.joblib","final_evaluation.json")]
    before = [sha(p) for p in frozen_files]
    second = tmp_path / "second"
    assert create_extension(output=second) == metadata
    assert (first/"analysis.json").read_bytes() == (second/"analysis.json").read_bytes()
    assert (first/"metadata.json").read_bytes() == (second/"metadata.json").read_bytes()
    assert sha(first/"analysis.json") == metadata["files"]["analysis.json"]["sha256"]
    assert before == [sha(p) for p in frozen_files]


def test_reject_corrupt_split_before_any_output(tmp_path):
    bad = tmp_path/"train.csv"
    bad.write_bytes(TRAIN_CSV.read_bytes() + b"corrupt\n")
    target = tmp_path/"no-export"
    with pytest.raises(ValueError, match="checksum"):
        create_extension(train=bad, output=target)
    assert not target.exists()


def test_no_test_split_access_and_no_production_fit(tmp_path, monkeypatch):
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import StandardScaler
    real_read = pd.read_csv
    seen = []
    def spy(path, *args, **kwargs):
        seen.append(Path(path).name)
        if Path(path).name == "test.csv":
            raise AssertionError("Final test read forbidden")
        return real_read(path, *args, **kwargs)
    def blocked(*args, **kwargs):
        raise AssertionError("Production refit forbidden")
    monkeypatch.setattr(pd,"read_csv",spy)
    monkeypatch.setattr(KMeans,"fit",blocked)
    monkeypatch.setattr(KMeans,"fit_predict",blocked)
    monkeypatch.setattr(StandardScaler,"fit",blocked)
    monkeypatch.setattr(StandardScaler,"fit_transform",blocked)
    create_extension(output=tmp_path/"safe")
    assert seen == ["train.csv", "validation.csv"]
