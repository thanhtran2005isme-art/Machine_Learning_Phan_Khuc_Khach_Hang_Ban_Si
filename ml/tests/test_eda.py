import json

import pandas as pd

from ml.src.audit_data import EXPECTED_COLUMNS, SPENDING_COLUMNS
from ml.src.eda import (
    build_iqr_outlier_table,
    build_skewness_table,
    generate_eda_outputs,
    log1p_features,
)


def make_train_frame(rows: int = 24) -> pd.DataFrame:
    data = {
        "Channel": [1 + (index % 2) for index in range(rows)],
        "Region": [1 + (index % 3) for index in range(rows)],
        "Fresh": [index * index + 1 for index in range(rows)],
        "Milk": [2 ** (index / 4) for index in range(rows)],
        "Grocery": [100 + index * 11 for index in range(rows)],
        "Frozen": [50 + (index % 5) * 30 for index in range(rows)],
        "Detergents_Paper": [20 + index * 7 for index in range(rows)],
        "Delicassen": [10 + index * index * 2 for index in range(rows)],
    }
    return pd.DataFrame(data)[EXPECTED_COLUMNS]


def test_log1p_keeps_only_six_model_features() -> None:
    transformed = log1p_features(make_train_frame())
    assert list(transformed.columns) == SPENDING_COLUMNS
    assert "Channel" not in transformed.columns
    assert "Region" not in transformed.columns


def test_skewness_table_compares_raw_and_log1p() -> None:
    table = build_skewness_table(make_train_frame())
    assert table["feature"].tolist() == SPENDING_COLUMNS
    assert {
        "raw_skewness",
        "log1p_skewness",
        "abs_skewness_reduction",
    }.issubset(table.columns)


def test_iqr_outliers_are_reported_without_dropping_rows() -> None:
    frame = make_train_frame()
    original_rows = len(frame)
    frame.loc[0, "Fresh"] = 1_000_000
    table = build_iqr_outlier_table(frame)

    fresh = table.loc[table["feature"] == "Fresh"].iloc[0]
    assert int(fresh["outlier_count"]) >= 1
    assert len(frame) == original_rows


def test_generate_eda_outputs_writes_tables_figures_and_metadata(tmp_path) -> None:
    data_dir = tmp_path / "data"
    figures_dir = tmp_path / "figures"
    outputs = generate_eda_outputs(
        make_train_frame(),
        data_dir=data_dir,
        figures_dir=figures_dir,
    )

    for path in outputs["tables"].values():
        assert path.exists()
        assert path.stat().st_size > 0
    for path in outputs["figures"].values():
        assert path.exists()
        assert path.stat().st_size > 0

    metadata = json.loads((data_dir / "eda_metadata.json").read_text(encoding="utf-8"))
    assert metadata["scope"] == "train_only"
    assert metadata["model_features"] == SPENDING_COLUMNS
    assert metadata["standard_scaler_fitted"] is False
    assert metadata["kmeans_fitted"] is False
    assert metadata["validation_used_for_decision"] is False
    assert metadata["test_used_for_decision"] is False
