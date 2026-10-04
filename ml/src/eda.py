from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

try:
    from .audit_data import (
        EXPECTED_COLUMNS,
        SPENDING_COLUMNS,
        file_sha256,
        iqr_outlier_summary,
        validation_errors,
    )
    from .data_paths import (
        EDA_DATA_DIR,
        EDA_FIGURES_DIR,
        EDA_IQR_OUTLIERS_CSV,
        EDA_METADATA_JSON,
        EDA_PREPROCESSING_COMPARISON_CSV,
        EDA_SKEWNESS_CSV,
        EDA_SUMMARY_LOG1P_CSV,
        EDA_SUMMARY_RAW_CSV,
        PROJECT_ROOT,
        TRAIN_CSV,
    )
except ImportError:
    from audit_data import (
        EXPECTED_COLUMNS,
        SPENDING_COLUMNS,
        file_sha256,
        iqr_outlier_summary,
        validation_errors,
    )
    from data_paths import (
        EDA_DATA_DIR,
        EDA_FIGURES_DIR,
        EDA_IQR_OUTLIERS_CSV,
        EDA_METADATA_JSON,
        EDA_PREPROCESSING_COMPARISON_CSV,
        EDA_SKEWNESS_CSV,
        EDA_SUMMARY_LOG1P_CSV,
        EDA_SUMMARY_RAW_CSV,
        PROJECT_ROOT,
        TRAIN_CSV,
    )


def load_train_dataset(path: Path = TRAIN_CSV) -> pd.DataFrame:
    """Đọc đúng train split đã tạo trước preprocessing."""
    if not path.exists():
        raise FileNotFoundError(
            f"Chưa có train split tại {path}. Chạy: python ml/src/prepare_data.py"
        )

    frame = pd.read_csv(path)
    frame.columns = [str(column).strip() for column in frame.columns]
    errors = validation_errors(frame, strict_rows=False)
    if errors:
        joined = "\n- ".join(errors)
        raise ValueError(f"Train split không hợp lệ:\n- {joined}")
    if list(frame.columns) != EXPECTED_COLUMNS:
        raise ValueError("Train split không giữ đúng schema/cột kỳ vọng.")
    return frame


def spending_frame(frame: pd.DataFrame) -> pd.DataFrame:
    """Chỉ lấy 6 biến chi tiêu dùng cho mô hình chính."""
    return frame[SPENDING_COLUMNS].astype(float).copy()


def log1p_features(frame: pd.DataFrame) -> pd.DataFrame:
    """Biến đổi log1p xác định, không học tham số từ validation/test."""
    values = spending_frame(frame)
    if (values < 0).any().any():
        raise ValueError("Không thể log1p vì dữ liệu chi tiêu có giá trị âm.")
    return np.log1p(values)


def build_summary_table(values: pd.DataFrame) -> pd.DataFrame:
    summary = values.describe(percentiles=[0.25, 0.5, 0.75]).T
    summary = summary.rename(
        columns={"25%": "q1", "50%": "median", "75%": "q3"}
    )
    summary["iqr"] = summary["q3"] - summary["q1"]
    summary.insert(0, "feature", summary.index)
    return summary[
        ["feature", "count", "mean", "std", "min", "q1", "median", "q3", "max", "iqr"]
    ].reset_index(drop=True)


def build_skewness_table(frame: pd.DataFrame) -> pd.DataFrame:
    raw = spending_frame(frame)
    logged = log1p_features(frame)
    rows: list[dict[str, float | str]] = []
    for feature in SPENDING_COLUMNS:
        raw_skew = float(raw[feature].skew())
        log_skew = float(logged[feature].skew())
        rows.append(
            {
                "feature": feature,
                "raw_skewness": raw_skew,
                "log1p_skewness": log_skew,
                "raw_abs_skewness": abs(raw_skew),
                "log1p_abs_skewness": abs(log_skew),
                "abs_skewness_reduction": abs(raw_skew) - abs(log_skew),
            }
        )
    return pd.DataFrame(rows)


def build_iqr_outlier_table(frame: pd.DataFrame) -> pd.DataFrame:
    values = spending_frame(frame)
    rows: list[dict[str, float | int | str]] = []
    for feature in SPENDING_COLUMNS:
        summary = iqr_outlier_summary(values[feature])
        count = int(summary["outlier_count"])
        rows.append(
            {
                "feature": feature,
                **summary,
                "outlier_percent": (count / len(values) * 100.0) if len(values) else 0.0,
            }
        )
    return pd.DataFrame(rows)


def build_preprocessing_comparison(frame: pd.DataFrame) -> pd.DataFrame:
    raw = spending_frame(frame)
    logged = log1p_features(frame)
    skewness = build_skewness_table(frame).set_index("feature")

    rows: list[dict[str, float | str]] = []
    for feature in SPENDING_COLUMNS:
        rows.append(
            {
                "feature": feature,
                "raw_min": float(raw[feature].min()),
                "raw_max": float(raw[feature].max()),
                "raw_range": float(raw[feature].max() - raw[feature].min()),
                "log1p_min": float(logged[feature].min()),
                "log1p_max": float(logged[feature].max()),
                "log1p_range": float(logged[feature].max() - logged[feature].min()),
                "raw_skewness": float(skewness.loc[feature, "raw_skewness"]),
                "log1p_skewness": float(skewness.loc[feature, "log1p_skewness"]),
                "abs_skewness_reduction": float(
                    skewness.loc[feature, "abs_skewness_reduction"]
                ),
            }
        )
    return pd.DataFrame(rows)


def _save_distribution_grid(values: pd.DataFrame, path: Path, title: str) -> None:
    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    for axis, feature in zip(axes.flat, SPENDING_COLUMNS, strict=True):
        axis.hist(values[feature].to_numpy(), bins=24)
        axis.set_title(feature)
        axis.set_xlabel("Giá trị")
        axis.set_ylabel("Tần suất")
    fig.suptitle(title)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(path, dpi=160, bbox_inches="tight")
    plt.close(fig)


def _save_boxplot_grid(values: pd.DataFrame, path: Path, title: str) -> None:
    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    for axis, feature in zip(axes.flat, SPENDING_COLUMNS, strict=True):
        axis.boxplot(values[feature].to_numpy())
        axis.set_title(feature)
        axis.set_xticks([1])
        axis.set_xticklabels([feature])
        axis.set_ylabel("Giá trị")
    fig.suptitle(title)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(path, dpi=160, bbox_inches="tight")
    plt.close(fig)


def _save_correlation(values: pd.DataFrame, path: Path, title: str) -> None:
    correlation = values.corr(numeric_only=True)
    fig, axis = plt.subplots(figsize=(9, 7))
    image = axis.imshow(correlation.to_numpy(), vmin=-1, vmax=1)
    axis.set_xticks(range(len(SPENDING_COLUMNS)))
    axis.set_yticks(range(len(SPENDING_COLUMNS)))
    axis.set_xticklabels(SPENDING_COLUMNS, rotation=45, ha="right")
    axis.set_yticklabels(SPENDING_COLUMNS)
    axis.set_title(title)
    fig.colorbar(image, ax=axis, label="Correlation")

    for row in range(len(SPENDING_COLUMNS)):
        for column in range(len(SPENDING_COLUMNS)):
            axis.text(
                column,
                row,
                f"{correlation.iloc[row, column]:.2f}",
                ha="center",
                va="center",
                fontsize=8,
            )

    fig.tight_layout()
    fig.savefig(path, dpi=160, bbox_inches="tight")
    plt.close(fig)


def _relative_display_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(PROJECT_ROOT.resolve())).replace("\\", "/")
    except ValueError:
        return str(path)


def generate_eda_outputs(
    frame: pd.DataFrame,
    data_dir: Path = EDA_DATA_DIR,
    figures_dir: Path = EDA_FIGURES_DIR,
    source_path: Path | None = None,
) -> dict:
    """Sinh toàn bộ EDA artifact từ một DataFrame đã xác định là train."""
    errors = validation_errors(frame, strict_rows=False)
    if errors:
        joined = "\n- ".join(errors)
        raise ValueError(f"Không thể chạy EDA vì train không hợp lệ:\n- {joined}")

    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    raw = spending_frame(frame)
    logged = log1p_features(frame)

    table_paths = {
        "summary_raw": data_dir / EDA_SUMMARY_RAW_CSV.name,
        "summary_log1p": data_dir / EDA_SUMMARY_LOG1P_CSV.name,
        "skewness": data_dir / EDA_SKEWNESS_CSV.name,
        "iqr_outliers": data_dir / EDA_IQR_OUTLIERS_CSV.name,
        "preprocessing_comparison": data_dir / EDA_PREPROCESSING_COMPARISON_CSV.name,
        "metadata": data_dir / EDA_METADATA_JSON.name,
    }
    figure_paths = {
        "distributions_raw": figures_dir / "train_distributions_raw.png",
        "distributions_log1p": figures_dir / "train_distributions_log1p.png",
        "boxplots_raw": figures_dir / "train_boxplots_raw.png",
        "boxplots_log1p": figures_dir / "train_boxplots_log1p.png",
        "correlation_raw": figures_dir / "train_correlation_raw.png",
        "correlation_log1p": figures_dir / "train_correlation_log1p.png",
    }

    build_summary_table(raw).to_csv(table_paths["summary_raw"], index=False, encoding="utf-8")
    build_summary_table(logged).to_csv(
        table_paths["summary_log1p"], index=False, encoding="utf-8"
    )
    build_skewness_table(frame).to_csv(table_paths["skewness"], index=False, encoding="utf-8")
    build_iqr_outlier_table(frame).to_csv(
        table_paths["iqr_outliers"], index=False, encoding="utf-8"
    )
    build_preprocessing_comparison(frame).to_csv(
        table_paths["preprocessing_comparison"], index=False, encoding="utf-8"
    )

    _save_distribution_grid(raw, figure_paths["distributions_raw"], "Train — phân phối dữ liệu thô")
    _save_distribution_grid(
        logged,
        figure_paths["distributions_log1p"],
        "Train — phân phối sau log1p",
    )
    _save_boxplot_grid(raw, figure_paths["boxplots_raw"], "Train — boxplot dữ liệu thô")
    _save_boxplot_grid(logged, figure_paths["boxplots_log1p"], "Train — boxplot sau log1p")
    _save_correlation(raw, figure_paths["correlation_raw"], "Train — tương quan dữ liệu thô")
    _save_correlation(
        logged,
        figure_paths["correlation_log1p"],
        "Train — tương quan sau log1p",
    )

    metadata = {
        "scope": "train_only",
        "rows": int(len(frame)),
        "model_features": SPENDING_COLUMNS,
        "excluded_from_model_features": ["Channel", "Region"],
        "comparison": ["raw", "log1p"],
        "standard_scaler_fitted": False,
        "kmeans_fitted": False,
        "validation_used_for_decision": False,
        "test_used_for_decision": False,
        "outlier_policy": "report_only_no_automatic_removal",
        "notes": [
            "EDA chỉ mô tả train split.",
            "log1p là biến đổi xác định; bước này chưa fit StandardScaler.",
            "Không chọn K trong bước EDA.",
        ],
        "tables": {key: _relative_display_path(path) for key, path in table_paths.items() if key != "metadata"},
        "figures": {key: _relative_display_path(path) for key, path in figure_paths.items()},
    }
    if source_path is not None and source_path.exists():
        metadata["source_file"] = _relative_display_path(source_path)
        metadata["source_sha256"] = file_sha256(source_path)

    table_paths["metadata"].write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return {
        "metadata": metadata,
        "tables": table_paths,
        "figures": figure_paths,
    }


def run_eda() -> dict:
    frame = load_train_dataset(TRAIN_CSV)
    print(f"[eda] Scope: TRAIN ONLY — {len(frame)} dòng")
    print(f"[eda] Features: {', '.join(SPENDING_COLUMNS)}")
    outputs = generate_eda_outputs(
        frame,
        data_dir=EDA_DATA_DIR,
        figures_dir=EDA_FIGURES_DIR,
        source_path=TRAIN_CSV,
    )
    print(f"[eda] Bảng: {EDA_DATA_DIR}")
    print(f"[eda] Hình: {EDA_FIGURES_DIR}")
    print("[eda] Chưa fit StandardScaler, chưa chạy K-Means, không dùng validation/test để ra quyết định.")
    return outputs


def main() -> None:
    run_eda()


if __name__ == "__main__":
    main()
