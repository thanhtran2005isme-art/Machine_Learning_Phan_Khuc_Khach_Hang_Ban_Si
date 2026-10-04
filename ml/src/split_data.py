from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

try:
    from .audit_data import EXPECTED_COLUMNS, load_raw_dataset, validation_errors
    from .data_paths import PROCESSED_DIR, RAW_CSV, SPLIT_MANIFEST, TEST_CSV, TRAIN_CSV, VALIDATION_CSV
except ImportError:
    from audit_data import EXPECTED_COLUMNS, load_raw_dataset, validation_errors
    from data_paths import PROCESSED_DIR, RAW_CSV, SPLIT_MANIFEST, TEST_CSV, TRAIN_CSV, VALIDATION_CSV

DEFAULT_SEED = 42
DEFAULT_TRAIN_RATIO = 0.60
DEFAULT_VALIDATION_RATIO = 0.20
DEFAULT_TEST_RATIO = 0.20


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def split_indices(
    n_rows: int,
    seed: int = DEFAULT_SEED,
    train_ratio: float = DEFAULT_TRAIN_RATIO,
    validation_ratio: float = DEFAULT_VALIDATION_RATIO,
    test_ratio: float = DEFAULT_TEST_RATIO,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    if n_rows <= 0:
        raise ValueError("n_rows phải > 0.")
    if not np.isclose(train_ratio + validation_ratio + test_ratio, 1.0):
        raise ValueError("Tổng train/validation/test ratio phải bằng 1.0.")
    if min(train_ratio, validation_ratio, test_ratio) <= 0:
        raise ValueError("Mọi split ratio phải > 0.")

    rng = np.random.default_rng(seed)
    indices = rng.permutation(n_rows)
    train_end = int(n_rows * train_ratio)
    validation_end = train_end + int(n_rows * validation_ratio)

    train_idx = indices[:train_end]
    validation_idx = indices[train_end:validation_end]
    test_idx = indices[validation_end:]
    return train_idx, validation_idx, test_idx


def assert_disjoint_and_complete(
    train_idx: np.ndarray,
    validation_idx: np.ndarray,
    test_idx: np.ndarray,
    n_rows: int,
) -> None:
    train_set = set(map(int, train_idx))
    validation_set = set(map(int, validation_idx))
    test_set = set(map(int, test_idx))

    if train_set & validation_set or train_set & test_set or validation_set & test_set:
        raise AssertionError("Split bị chồng lấn index.")
    combined = train_set | validation_set | test_set
    if combined != set(range(n_rows)):
        raise AssertionError("Split không bao phủ chính xác toàn bộ dữ liệu.")


def split_dataset(
    path: Path = RAW_CSV,
    seed: int = DEFAULT_SEED,
    train_ratio: float = DEFAULT_TRAIN_RATIO,
    validation_ratio: float = DEFAULT_VALIDATION_RATIO,
    test_ratio: float = DEFAULT_TEST_RATIO,
) -> dict:
    df = load_raw_dataset(path)
    errors = validation_errors(df, strict_rows=True)
    if errors:
        joined = "\n- ".join(errors)
        raise ValueError(f"Không thể split vì dữ liệu raw không hợp lệ:\n- {joined}")

    train_idx, validation_idx, test_idx = split_indices(
        len(df),
        seed=seed,
        train_ratio=train_ratio,
        validation_ratio=validation_ratio,
        test_ratio=test_ratio,
    )
    assert_disjoint_and_complete(train_idx, validation_idx, test_idx, len(df))

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    splits = {
        "train": (TRAIN_CSV, df.iloc[train_idx].reset_index(drop=True)),
        "validation": (VALIDATION_CSV, df.iloc[validation_idx].reset_index(drop=True)),
        "test": (TEST_CSV, df.iloc[test_idx].reset_index(drop=True)),
    }
    for _, (output_path, split_df) in splits.items():
        split_df.to_csv(output_path, index=False, encoding="utf-8")

    manifest = {
        "source_file": path.name,
        "source_sha256": file_sha256(path),
        "seed": seed,
        "strategy": "random_split_before_any_learned_preprocessing",
        "stratified": False,
        "stratification_note": "Channel/Region chỉ dùng profiling, không dùng làm ground truth để điều khiển split/chọn K.",
        "ratios": {
            "train": train_ratio,
            "validation": validation_ratio,
            "test": test_ratio,
        },
        "counts": {
            "train": len(train_idx),
            "validation": len(validation_idx),
            "test": len(test_idx),
        },
        "source_row_indices": {
            "train": [int(value) for value in train_idx],
            "validation": [int(value) for value in validation_idx],
            "test": [int(value) for value in test_idx],
        },
        "columns": EXPECTED_COLUMNS,
        "preprocessing_applied": False,
        "files": {
            name: {
                "path": str(output_path.relative_to(PROCESSED_DIR.parent.parent)).replace('\\', '/'),
                "sha256": file_sha256(output_path),
            }
            for name, (output_path, _) in splits.items()
        },
    }
    SPLIT_MANIFEST.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(
        "[split] PASS: "
        f"train={len(train_idx)}, validation={len(validation_idx)}, test={len(test_idx)}, seed={seed}"
    )
    print("[split] Chưa fit scaler/log transform/model ở bước này.")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Tách train/validation/test trước preprocessing học từ dữ liệu.")
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--train", type=float, default=DEFAULT_TRAIN_RATIO)
    parser.add_argument("--validation", type=float, default=DEFAULT_VALIDATION_RATIO)
    parser.add_argument("--test", type=float, default=DEFAULT_TEST_RATIO)
    args = parser.parse_args()
    split_dataset(
        seed=args.seed,
        train_ratio=args.train,
        validation_ratio=args.validation,
        test_ratio=args.test,
    )


if __name__ == "__main__":
    main()
