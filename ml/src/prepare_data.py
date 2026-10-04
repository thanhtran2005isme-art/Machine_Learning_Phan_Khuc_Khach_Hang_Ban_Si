from __future__ import annotations

import argparse

try:
    from .audit_data import audit_dataset
    from .download_data import download_dataset
    from .split_data import split_dataset
except ImportError:
    from audit_data import audit_dataset
    from download_data import download_dataset
    from split_data import split_dataset


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Pipeline dữ liệu giai đoạn 1: download -> audit -> split."
    )
    parser.add_argument("--force-download", action="store_true")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    raw_path = download_dataset(force=args.force_download)
    audit_dataset(raw_path, strict_rows=True)
    manifest = split_dataset(raw_path, seed=args.seed)

    print("\n[data pipeline] HOÀN TẤT")
    print(f"- Raw: {raw_path}")
    print(f"- Train: {manifest['counts']['train']} dòng")
    print(f"- Validation: {manifest['counts']['validation']} dòng")
    print(f"- Test: {manifest['counts']['test']} dòng")
    print("- Chưa thực hiện log1p, StandardScaler hoặc K-Means.")
    print("- Bước kế tiếp: EDA chỉ trên train, sau đó mới xây baseline/thí nghiệm K-Means.")


if __name__ == "__main__":
    main()
