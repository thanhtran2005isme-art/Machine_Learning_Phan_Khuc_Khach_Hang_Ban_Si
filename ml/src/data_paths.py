from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
REPORTS_DATA_DIR = PROJECT_ROOT / "reports" / "data"
REPORTS_FIGURES_DIR = PROJECT_ROOT / "reports" / "figures"
EDA_DATA_DIR = REPORTS_DATA_DIR / "eda"
EDA_FIGURES_DIR = REPORTS_FIGURES_DIR / "eda"

RAW_CSV = RAW_DIR / "Wholesale customers data.csv"
RAW_METADATA = RAW_DIR / "metadata.json"
TRAIN_CSV = PROCESSED_DIR / "train.csv"
VALIDATION_CSV = PROCESSED_DIR / "validation.csv"
TEST_CSV = PROCESSED_DIR / "test.csv"
SPLIT_MANIFEST = PROCESSED_DIR / "split_manifest.json"
DATA_QUALITY_JSON = REPORTS_DATA_DIR / "data_quality.json"
DESCRIPTIVE_STATS_CSV = REPORTS_DATA_DIR / "descriptive_stats.csv"

EDA_SUMMARY_RAW_CSV = EDA_DATA_DIR / "train_summary_raw.csv"
EDA_SUMMARY_LOG1P_CSV = EDA_DATA_DIR / "train_summary_log1p.csv"
EDA_SKEWNESS_CSV = EDA_DATA_DIR / "train_skewness.csv"
EDA_IQR_OUTLIERS_CSV = EDA_DATA_DIR / "train_iqr_outliers.csv"
EDA_PREPROCESSING_COMPARISON_CSV = EDA_DATA_DIR / "preprocessing_comparison.csv"
EDA_METADATA_JSON = EDA_DATA_DIR / "eda_metadata.json"
