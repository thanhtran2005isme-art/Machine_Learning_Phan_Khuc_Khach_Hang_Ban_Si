# Dữ liệu — Wholesale customers

## 1. Nguồn chính thức

- Dataset: **Wholesale customers**
- UCI Dataset ID: **292**
- Trang nguồn: https://archive.ics.uci.edu/dataset/292/wholesale%2Bcustomers
- DOI: https://doi.org/10.24432/C5030X
- Giấy phép: **CC BY 4.0**
- Quy mô được đề bài xác định: **440 khách hàng**.

Dữ liệu mô tả mức chi tiêu hằng năm (monetary units) của khách hàng bán sỉ theo các nhóm sản phẩm.

## 2. Quy tắc sử dụng trong Project 22

Sáu biến chi tiêu dùng cho mô hình chính:

- `Fresh`
- `Milk`
- `Grocery`
- `Frozen`
- `Detergents_Paper`
- `Delicassen`

`Channel` và `Region` **không được đưa vào fit K-Means chính và không phải ground truth để chọn K**. Hai biến này chỉ được ghép lại sau khi có cụm để profiling/mô tả.

## 3. Không commit dữ liệu sinh tự động

`data/raw/` và `data/processed/` được bỏ qua trong Git (ngoại trừ `.gitkeep`). Máy mới phải tái tạo dữ liệu bằng script.

## 4. Pipeline dữ liệu hiện tại

```text
UCI ZIP
  ↓
download_data.py
  ↓
data/raw/Wholesale customers data.csv
  ↓
audit_data.py
  ├── schema / row count
  ├── missing / duplicate
  ├── miền Channel / Region
  ├── giá trị âm / finite
  └── IQR outlier report (KHÔNG tự động xóa)
  ↓
split_data.py
  ├── train      60% = 264 dòng
  ├── validation 20% = 88 dòng
  └── test       20% = 88 dòng
```

Tỷ lệ `60/20/20` là **quyết định triển khai của nhóm**, không phải tỷ lệ bắt buộc ghi trong đề. Seed mặc định là `42` và được lưu vào manifest để tái lập.

**Quan trọng:** split diễn ra trước mọi preprocessing học từ dữ liệu. Ở giai đoạn này chưa fit `StandardScaler`, chưa chọn K và chưa chạy K-Means.

## 5. Chạy từ máy mới

Từ thư mục gốc project:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r ml/requirements.txt
python ml/src/prepare_data.py
python -m pytest ml/tests -q
```

Sau khi chạy thành công sẽ có:

```text
data/raw/Wholesale customers data.csv
data/raw/metadata.json
data/processed/train.csv
data/processed/validation.csv
data/processed/test.csv
data/processed/split_manifest.json
reports/data/data_quality.json
reports/data/descriptive_stats.csv
```

## 6. Chính sách outlier

Outlier chỉ được **phát hiện và báo cáo** ở bước audit. Không tự động xóa hoặc winsorize trước khi thiết kế thí nghiệm. Việc xử lý/không xử lý outlier phải có bằng chứng và được ghi trong báo cáo.

## 7. Trích dẫn dữ liệu

Cardoso, M. (2013). *Wholesale customers* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5030X

## 8. Data card Gate 9.5 — đơn vị và thời điểm dự đoán

- **Nguồn UCI ghi đơn vị monetary units (m.u.)**, là chi tiêu **theo năm**, **không xác định cụ thể tiền tệ**, không mặc định VND. Không tự nhân tỷ giá để đưa input mới vào mô hình.
- Chỉ phân khúc đối tượng đã có dữ liệu chi tiêu cả năm ở đủ sáu nhóm. Đây không phải mô hình dự báo doanh thu hoặc phân loại khách mới chưa có giao dịch.
- `Channel` (1=Horeca, 2=Retail) và `Region` (1=Lisbon, 2=Oporto, 3=Other) chỉ dùng profiling; UCI gắn role metadata khác Project22 nhưng không tạo nhãn thật.
- File `data/raw/metadata.json` sinh local chứa `downloaded_at_utc`, SHA256 raw và archive; **không commit**. Ngày donated 2014 trên UCI không phải ngày tải thực tế.
- Raw SHA256 trong audit Git: `c3d018c643565b85cee733c4a2ac76dd76e080e857cb23f0ccfcc2e15a6c17ef`. Bản chi tiết xem [Data card](../docs/DATA_CARD.md).
