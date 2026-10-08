"""Gate 5 selection freeze and final test isolation tests."""

from __future__ import annotations

import json

import numpy as np
import pandas as pd
import pytest

from ml.src.audit_data import SPENDING_COLUMNS
from ml.src import finalize_model as final
from ml.src.freeze_selection import freeze_selection, sha256


def test_selection_freezes_once_without_access_to_test(tmp_path, monkeypatch):
    output = tmp_path / "selection.json"
    frozen = freeze_selection(output)
    assert frozen["status"] == "FROZEN"
    assert frozen["k"] == 2
    assert frozen["test_used_for_selection"] is False
    assert set(frozen["evidence"]) == {
        "selection_evidence", "review_table", "train", "validation",
        "train_median_profile", "validation_median_profile",
    }
    with pytest.raises(FileExistsError):
        freeze_selection(output)


def test_portable_predict_validates_and_matches_sklearn():
    rng = np.random.default_rng(57)
    three_profiles = np.array([
        [5000, 7000, 12000, 1000, 6000, 1400],
        [6000, 1100, 1500, 900, 150, 400],
        [16000, 2400, 3000, 5000, 450, 1100],
    ])
    raw = np.vstack([np.exp(rng.normal(np.log(profile), 0.14, (50, 6))) for profile in three_profiles])
    frame = pd.DataFrame(raw, columns=SPENDING_COLUMNS)
    config = {"k": 2, "random_state": 42, "n_init": 10, "max_iter": 300, "algorithm": "lloyd",
              "preprocessing": "log1p_standardscaler", "decision": "D011"}
    scaler, model, _ = final.fit_frozen_model(frame, config)
    exported = final.build_export(frame, config, scaler, model)
    np.testing.assert_array_equal(final.predict_portable(raw, exported), model.predict(scaler.transform(np.log1p(raw))))
    with pytest.raises(ValueError):
        final.predict_portable(np.array([[-1., 1., 1., 1., 1., 1.]]), exported)
    with pytest.raises(ValueError):
        final.predict_portable(np.ones((2, 5)), exported)


def test_final_test_is_read_after_claim_exactly_once(tmp_path, monkeypatch):
    rng = np.random.default_rng(8)
    prototype = np.array([
        [5000, 7000, 12000, 1000, 6000, 1400],
        [6000, 1100, 1500, 900, 150, 400],
        [16000, 2400, 3000, 5000, 450, 1100],
    ])
    samples = np.vstack([
        np.exp(rng.normal(np.log(prototype[i % 3]), 0.16, size=(1, 6)))
        for i in range(440)
    ])
    train, val, test = np.split(samples, [264, 352])
    root = tmp_path
    data_dir = root / "data" / "processed"
    model_dir = root / "models"
    data_dir.mkdir(parents=True)
    model_dir.mkdir()
    for name, values in (("train", train), ("validation", val), ("test", test)):
        pd.DataFrame(values, columns=SPENDING_COLUMNS).to_csv(data_dir / (name + ".csv"), index=False)

    sources = {}
    for name in ("selection_evidence", "review_table", "train", "validation",
                 "train_median_profile", "validation_median_profile"):
        path = data_dir / (name + ".csv")
        if not path.exists():
            path.write_text("placeholder\n", encoding="utf-8")
        sources[name] = {"path": str(path.relative_to(root)).replace("\\", "/"), "sha256": sha256(path)}
    selected = {
        "status": "FROZEN", "decision": "D011", "preprocessing": "log1p_standardscaler",
        "k": 2, "random_state": 42, "n_init": 10, "max_iter": 300, "algorithm": "lloyd",
        "fit_scope": "train_plus_validation_after_freeze", "test_used_for_selection": False,
        "feature_columns": list(SPENDING_COLUMNS), "evidence": sources,
    }
    selection_path = model_dir / "selection.json"
    selection_path.write_text(json.dumps(selected), encoding="utf-8")
    monkeypatch.setattr(final, "PROJECT_ROOT", root)
    monkeypatch.setattr(final, "SELECTION_FILE", selection_path)
    monkeypatch.setattr(final, "TRAIN_CSV", data_dir / "train.csv")
    monkeypatch.setattr(final, "VALIDATION_CSV", data_dir / "validation.csv")
    monkeypatch.setattr(final, "TEST_CSV", data_dir / "test.csv")
    monkeypatch.setattr(final, "MODELS_DIR", model_dir)
    monkeypatch.setattr(final, "MODEL_JSON", model_dir / "model.json")
    monkeypatch.setattr(final, "MODEL_JOBLIB", model_dir / "model.joblib")
    monkeypatch.setattr(final, "FINAL_EVALUATION_JSON", model_dir / "final_evaluation.json")

    observed_reads = []
    real_loader = final.load_split

    def guarded_loader(path):
        if path == final.TEST_CSV:
            assert json.loads(final.FINAL_EVALUATION_JSON.read_text())["status"] == "CLAIMED"
        observed_reads.append(path)
        return real_loader(path)

    monkeypatch.setattr(final, "load_split", guarded_loader)
    completed = final.finalize_model()
    assert completed["status"] == "COMPLETE"
    assert completed["test_evaluated_once"] is True
    assert completed["training"]["rows"] == 352
    assert completed["final_test"]["rows"] == 88
    assert observed_reads.count(final.TEST_CSV) == 1
    with pytest.raises(FileExistsError):
        final.finalize_model()
    assert observed_reads.count(final.TEST_CSV) == 1


def test_selection_rejects_changed_training_evidence(tmp_path):
    evidence = tmp_path / "train.csv"
    evidence.write_text("original", encoding="utf-8")
    config = {
        "status": "FROZEN", "decision": "D011", "preprocessing": "log1p_standardscaler",
        "k": 2, "random_state": 42, "n_init": 10, "max_iter": 300, "algorithm": "lloyd",
        "fit_scope": "train_plus_validation_after_freeze", "test_used_for_selection": False,
        "feature_columns": list(SPENDING_COLUMNS),
        "evidence": {name: {"path": "train.csv", "sha256": sha256(evidence)}
                     for name in ("selection_evidence", "review_table", "train", "validation",
                                  "train_median_profile", "validation_median_profile")},
    }
    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(final, "PROJECT_ROOT", tmp_path)
        final.validate_frozen_selection(config)
        evidence.write_text("changed", encoding="utf-8")
        with pytest.raises(ValueError, match="đã thay đổi"):
            final.validate_frozen_selection(config)
