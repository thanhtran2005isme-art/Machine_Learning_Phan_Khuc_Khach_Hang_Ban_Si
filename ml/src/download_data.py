from __future__ import annotations

import argparse
import hashlib
import json
import urllib.request
import zipfile
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path

try:
    from .data_paths import RAW_CSV, RAW_DIR, RAW_METADATA
except ImportError:
    from data_paths import RAW_CSV, RAW_DIR, RAW_METADATA

SOURCE_PAGE = "https://archive.ics.uci.edu/dataset/292/wholesale%2Bcustomers"
DOWNLOAD_URL = "https://archive.ics.uci.edu/static/public/292/wholesale%2Bcustomers.zip"
DOI = "https://doi.org/10.24432/C5030X"
LICENSE = "CC BY 4.0"
EXPECTED_FILENAME = "Wholesale customers data.csv"
EXPECTED_ROWS = 440


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def download_dataset(force: bool = False) -> Path:
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    if RAW_CSV.exists() and not force:
        print(f"[download] Đã có dữ liệu: {RAW_CSV}")
        return RAW_CSV

    request = urllib.request.Request(
        DOWNLOAD_URL,
        headers={"User-Agent": "Project22-Wholesale-Customer-Segmentation/1.0"},
    )
    print(f"[download] Đang tải từ UCI: {DOWNLOAD_URL}")
    with urllib.request.urlopen(request, timeout=60) as response:
        archive_bytes = response.read()

    with zipfile.ZipFile(BytesIO(archive_bytes)) as archive:
        candidates = [
            name for name in archive.namelist()
            if Path(name).name == EXPECTED_FILENAME
        ]
        if len(candidates) != 1:
            raise RuntimeError(
                f"Không tìm thấy duy nhất tệp '{EXPECTED_FILENAME}' trong archive. "
                f"Các tệp hiện có: {archive.namelist()}"
            )
        csv_bytes = archive.read(candidates[0])

    RAW_CSV.write_bytes(csv_bytes)
    metadata = {
        "dataset": "Wholesale customers",
        "uci_dataset_id": 292,
        "source_page": SOURCE_PAGE,
        "download_url": DOWNLOAD_URL,
        "doi": DOI,
        "license": LICENSE,
        "downloaded_at_utc": datetime.now(timezone.utc).isoformat(),
        "raw_file": RAW_CSV.name,
        "raw_file_size_bytes": len(csv_bytes),
        "raw_file_sha256": sha256_bytes(csv_bytes),
        "archive_sha256": sha256_bytes(archive_bytes),
        "expected_rows": EXPECTED_ROWS,
    }
    RAW_METADATA.write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"[download] Đã lưu: {RAW_CSV}")
    print(f"[download] SHA256: {metadata['raw_file_sha256']}")
    return RAW_CSV


def main() -> None:
    parser = argparse.ArgumentParser(description="Tải Wholesale customers từ UCI.")
    parser.add_argument("--force", action="store_true", help="Tải lại dù tệp raw đã tồn tại.")
    args = parser.parse_args()
    download_dataset(force=args.force)


if __name__ == "__main__":
    main()
