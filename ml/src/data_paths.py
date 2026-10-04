from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
REPORTS_DATA_DIR = PROJECT_ROOT / "reports" / "data"

RAW_CSV = RAW_DIR / "Wholesale customers data.csv"
RAW_METADATA = RAW_DIR / "metadata.json"
TRAIN_CSV = PROCESSED_DIR / "train.csv"
VALIDATION_CSV = PROCESSED_DIR / "validation.csv"
TEST_CSV = PROCESSED_DIR / "test.csv"
SPLIT_MANIFEST = PROCESSED_DIR / "split_manifest.json"
DATA_QUALITY_JSON = REPORTS_DATA_DIR / "data_quality.json"
DESCRIPTIVE_STATS_CSV = REPORTS_DATA_DIR / "descriptive_stats.csv"
