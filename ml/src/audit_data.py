from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

try:
    from .data_paths import DATA_QUALITY_JSON, DESCRIPTIVE_STATS_CSV, RAW_CSV, REPORTS_DATA_DIR
except ImportError:
    from data_paths import DATA_QUALITY_JSON, DESCRIPTIVE_STATS_CSV, RAW_CSV, REPORTS_DATA_DIR

EXPECTED_COLUMNS = [
    "Channel",
    "Region",
    "Fresh",
    "Milk",
    "Grocery",
    "Frozen",
    "Detergents_Paper",
    "Delicassen",
]
SPENDING_COLUMNS = [
    "Fresh",
    "Milk",
    "Grocery",
    "Frozen",
    "Detergents_Paper",
    "Delicassen",
]
EXPECTED_ROWS = 440
ALLOWED_CHANNEL = {1, 2}
ALLOWED_REGION = {1, 2, 3}


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def load_raw_dataset(path: Path = RAW_CSV) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(
            f"Chưa có dữ liệu raw tại {path}. Chạy: python ml/src/download_data.py"
        )
    df = pd.read_csv(path)
    df.columns = [str(column).strip() for column in df.columns]
    return df


def validation_errors(df: pd.DataFrame, strict_rows: bool = True) -> list[str]:
    errors: list[str] = []
    actual_columns = list(df.columns)

    if actual_columns != EXPECTED_COLUMNS:
        errors.append(
            "Schema không đúng. "
            f"Expected={EXPECTED_COLUMNS}; actual={actual_columns}"
        )
        return errors

    if strict_rows and len(df) != EXPECTED_ROWS:
        errors.append(f"Số dòng phải là {EXPECTED_ROWS}, hiện tại là {len(df)}.")

    for column in EXPECTED_COLUMNS:
        if not pd.api.types.is_numeric_dtype(df[column]):
            errors.append(f"Cột {column} phải là kiểu số.")

    if df[EXPECTED_COLUMNS].isna().any().any():
        errors.append("Dữ liệu có missing value trong schema bắt buộc.")

    numeric = df[EXPECTED_COLUMNS].to_numpy(dtype=float, copy=False)
    if not np.isfinite(numeric).all():
        errors.append("Dữ liệu chứa NaN hoặc +/-inf.")

    for column in SPENDING_COLUMNS:
        negative_count = int((df[column] < 0).sum())
        if negative_count:
            errors.append(f"Cột {column} có {negative_count} giá trị âm.")

    channel_values = set(df["Channel"].dropna().astype(int).unique().tolist())
    region_values = set(df["Region"].dropna().astype(int).unique().tolist())
    if not channel_values.issubset(ALLOWED_CHANNEL):
        errors.append(f"Channel ngoài miền cho phép {sorted(ALLOWED_CHANNEL)}: {sorted(channel_values)}")
    if not region_values.issubset(ALLOWED_REGION):
        errors.append(f"Region ngoài miền cho phép {sorted(ALLOWED_REGION)}: {sorted(region_values)}")

    return errors


def iqr_outlier_summary(series: pd.Series) -> dict[str, float | int]:
    q1 = float(series.quantile(0.25))
    q3 = float(series.quantile(0.75))
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    count = int(((series < lower) | (series > upper)).sum())
    return {
        "q1": q1,
        "q3": q3,
        "iqr": iqr,
        "lower_fence": lower,
        "upper_fence": upper,
        "outlier_count": count,
    }


def build_audit_report(df: pd.DataFrame, source_path: Path | None = None) -> dict:
    duplicate_mask = df.duplicated(keep=False)
    report = {
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "column_names": list(df.columns),
        "missing_by_column": {column: int(value) for column, value in df.isna().sum().items()},
        "duplicate_rows": int(df.duplicated().sum()),
        "duplicate_row_indices": [int(index) for index in df.index[duplicate_mask].tolist()],
        "negative_counts": {
            column: int((df[column] < 0).sum()) for column in SPENDING_COLUMNS
        },
        "channel_counts": {
            str(key): int(value) for key, value in df["Channel"].value_counts().sort_index().items()
        },
        "region_counts": {
            str(key): int(value) for key, value in df["Region"].value_counts().sort_index().items()
        },
        "iqr_outliers": {
            column: iqr_outlier_summary(df[column]) for column in SPENDING_COLUMNS
        },
        "policy": {
            "drop_outliers_automatically": False,
            "reason": "Outlier được ghi nhận để phân tích; không tự động loại trước thí nghiệm.",
            "channel_region_usage": "profiling_only",
        },
    }
    if source_path is not None and source_path.exists():
        report["source_file"] = source_path.name
        report["source_sha256"] = file_sha256(source_path)
    return report


def audit_dataset(path: Path = RAW_CSV, strict_rows: bool = True) -> dict:
    df = load_raw_dataset(path)
    errors = validation_errors(df, strict_rows=strict_rows)
    if errors:
        joined = "\n- ".join(errors)
        raise ValueError(f"Data validation thất bại:\n- {joined}")

    report = build_audit_report(df, source_path=path)
    REPORTS_DATA_DIR.mkdir(parents=True, exist_ok=True)
    DATA_QUALITY_JSON.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    df[SPENDING_COLUMNS].describe(percentiles=[0.25, 0.5, 0.75]).T.to_csv(
        DESCRIPTIVE_STATS_CSV,
        encoding="utf-8",
    )
    print(f"[audit] PASS: {len(df)} dòng, {len(df.columns)} cột")
    print(f"[audit] Missing: {sum(report['missing_by_column'].values())}")
    print(f"[audit] Duplicate rows: {report['duplicate_rows']}")
    print(f"[audit] Báo cáo: {DATA_QUALITY_JSON}")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Kiểm tra schema và chất lượng dữ liệu raw.")
    parser.add_argument(
        "--allow-row-count-mismatch",
        action="store_true",
        help="Không fail chỉ vì số dòng khác 440 (chỉ dùng để chẩn đoán).",
    )
    args = parser.parse_args()
    audit_dataset(strict_rows=not args.allow_row_count_mismatch)


if __name__ == "__main__":
    main()
