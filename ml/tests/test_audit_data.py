import pandas as pd

from ml.src.audit_data import EXPECTED_COLUMNS, build_audit_report, validation_errors


def make_valid_frame(rows: int = 440) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Channel": [1 + (i % 2) for i in range(rows)],
            "Region": [1 + (i % 3) for i in range(rows)],
            "Fresh": [100 + i for i in range(rows)],
            "Milk": [200 + i for i in range(rows)],
            "Grocery": [300 + i for i in range(rows)],
            "Frozen": [400 + i for i in range(rows)],
            "Detergents_Paper": [500 + i for i in range(rows)],
            "Delicassen": [600 + i for i in range(rows)],
        }
    )[EXPECTED_COLUMNS]


def test_valid_frame_has_no_validation_errors() -> None:
    assert validation_errors(make_valid_frame()) == []


def test_negative_spending_is_rejected() -> None:
    frame = make_valid_frame()
    frame.loc[0, "Fresh"] = -1
    errors = validation_errors(frame)
    assert any("Fresh" in error and "giá trị âm" in error for error in errors)


def test_channel_outside_domain_is_rejected() -> None:
    frame = make_valid_frame()
    frame.loc[0, "Channel"] = 99
    errors = validation_errors(frame)
    assert any("Channel ngoài miền" in error for error in errors)


def test_audit_does_not_drop_outliers() -> None:
    frame = make_valid_frame()
    frame.loc[0, "Fresh"] = 1_000_000
    report = build_audit_report(frame)
    assert report["rows"] == 440
    assert report["policy"]["drop_outliers_automatically"] is False
    assert report["iqr_outliers"]["Fresh"]["outlier_count"] >= 1
