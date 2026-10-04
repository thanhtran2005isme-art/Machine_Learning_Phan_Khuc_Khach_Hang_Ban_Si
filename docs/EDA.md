# EDA trên train — Project 22

## 1. Mục tiêu

EDA ở giai đoạn này chỉ dùng để hiểu **6 biến chi tiêu trên `train.csv`** và tạo bằng chứng cho quyết định tiền xử lý trước khi chạy K-Means.

Không dùng validation/test để chọn preprocessing, không chọn K và chưa fit mô hình trong bước này.

## 2. Phạm vi dữ liệu

Nguồn duy nhất của script chính:

```text
data/processed/train.csv
```

Sáu biến được phân tích:

- `Fresh`
- `Milk`
- `Grocery`
- `Frozen`
- `Detergents_Paper`
- `Delicassen`

`Channel` và `Region` không phải feature của K-Means chính. Hai cột này được giữ nguyên trong split để profiling sau khi clustering, nhưng không được đưa vào các bảng/biểu đồ feature chính của EDA này.

## 3. EDA tạo gì?

### Bảng

```text
reports/data/eda/train_summary_raw.csv
reports/data/eda/train_summary_log1p.csv
reports/data/eda/train_skewness.csv
reports/data/eda/train_iqr_outliers.csv
reports/data/eda/preprocessing_comparison.csv
reports/data/eda/eda_metadata.json
```

### Hình

```text
reports/figures/eda/train_distributions_raw.png
reports/figures/eda/train_distributions_log1p.png
reports/figures/eda/train_boxplots_raw.png
reports/figures/eda/train_boxplots_log1p.png
reports/figures/eda/train_correlation_raw.png
reports/figures/eda/train_correlation_log1p.png
```

## 4. Vì sao so sánh raw với log1p?

Đề bài yêu cầu thí nghiệm so sánh dữ liệu thô với nhánh `log1p + StandardScaler`. EDA này chỉ tạo bằng chứng mô tả cho phần `raw` và `log1p`:

- phân phối trước/sau log;
- skewness trước/sau log;
- median/IQR;
- outlier theo quy tắc IQR;
- khoảng giá trị trước/sau log;
- correlation trước/sau log.

`log1p` là biến đổi xác định nên bước EDA có thể tính trực tiếp trên train. **StandardScaler chưa được fit ở đây**; scaler chỉ được fit đúng phạm vi train khi bước thí nghiệm/mô hình bắt đầu.

## 5. Chính sách outlier

EDA chỉ **phát hiện và báo cáo** outlier. Không tự động:

- xóa dòng;
- winsorize;
- clip;
- thay thế giá trị.

Nếu sau này muốn xử lý outlier, phải thiết kế thành một thí nghiệm riêng và có bằng chứng trên validation trước khi dùng test.

## 6. Cách chạy

Sau khi `python ml/src/prepare_data.py` đã PASS:

```powershell
python ml/src/eda.py
```

hoặc:

```powershell
npm run eda:train
```

Sau đó chạy test:

```powershell
python -m pytest ml/tests -q
```

## 7. Điều kiện để đóng EDA

Chỉ đánh dấu EDA PASS khi có log chạy thật xác nhận:

- script đọc `train.csv` thành công;
- artifact bảng/hình được sinh;
- test ML/data PASS;
- metadata ghi `scope=train_only`;
- chưa fit `StandardScaler`;
- chưa chạy K-Means;
- chưa dùng validation/test để ra quyết định.

## 8. Sau EDA

Khi EDA đã được kiểm chứng, bước kế tiếp là đóng băng thiết kế thí nghiệm:

1. baseline thống kê không clustering;
2. baseline K-Means `K=2`;
3. so sánh raw với `log1p + StandardScaler`;
4. K-Means `K=2..8`;
5. stability qua ít nhất 10 seed;
6. chọn K bằng bằng chứng validation;
7. chỉ sau khi đóng băng quyết định mới dùng final test.
