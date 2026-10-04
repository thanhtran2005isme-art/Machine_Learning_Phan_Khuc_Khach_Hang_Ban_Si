# Bước tiếp theo — sau khi EDA train-only đã PASS

Gate B (data) và Gate C (web/backend skeleton) đã có log chạy thật và được phép đánh dấu PASS. EDA train-only cũng đã chạy thành công với 264 dòng train và 11 pytest PASS.

## Trạng thái đã khóa

- Dataset raw: 440 dòng, 8 cột.
- Split: train 264 / validation 88 / test 88, seed 42.
- EDA chỉ dùng train.
- 6 feature chính: `Fresh`, `Milk`, `Grocery`, `Frozen`, `Detergents_Paper`, `Delicassen`.
- `Channel`/`Region`: profiling only.
- Chưa fit `StandardScaler` trên full data.
- Chưa chạy/chọn K-Means.
- Test vẫn khóa cho đánh giá cuối.

## Bước 1 — đọc artifact EDA thật

Trên máy local, kiểm tra:

```text
reports/data/eda/train_skewness.csv
reports/data/eda/train_iqr_outliers.csv
reports/data/eda/preprocessing_comparison.csv
reports/data/eda/train_summary_raw.csv
reports/data/eda/train_summary_log1p.csv

reports/figures/eda/train_distributions_raw.png
reports/figures/eda/train_distributions_log1p.png
reports/figures/eda/train_boxplots_raw.png
reports/figures/eda/train_boxplots_log1p.png
reports/figures/eda/train_correlation_raw.png
reports/figures/eda/train_correlation_log1p.png
```

Mục tiêu:

- ghi skewness raw và sau `log1p` cho từng feature;
- ghi median/IQR trên train;
- mô tả outlier theo IQR nhưng chưa tự động loại;
- quan sát correlation để hiểu cấu trúc dữ liệu, không dùng correlation để tạo ground truth;
- kết luận bằng bằng chứng xem `log1p` có giảm lệch đáng kể hay không.

## Bước 2 — đóng băng protocol thí nghiệm trước K-Means

Phải ghi rõ trước khi nhìn test:

### Baseline A

Không clustering — thống kê toàn bộ train để làm mốc mô tả.

### Baseline B

K-Means `K=2` với cấu hình seed/n_init được ghi rõ.

### Thí nghiệm preprocessing bắt buộc

```text
Nhánh A: Raw -> K-Means
Nhánh B: log1p -> StandardScaler -> K-Means
```

`StandardScaler` phải fit trong phạm vi train của nhánh thí nghiệm, không fit trên full dataset.

### Candidate K

```text
K = 2, 3, 4, 5, 6, 7, 8
```

### Stability

Ít nhất 10 seed khác nhau cho mỗi candidate cần đánh giá độ ổn định.

### Metric / evidence

- inertia;
- silhouette;
- silhouette mean/std qua seed;
- inertia mean/std qua seed;
- cluster sizes;
- độ ổn định gán cụm nếu triển khai metric phù hợp;
- khả năng diễn giải profile;
- median profile của 6 feature;
- `Channel`/`Region` chỉ ghép lại sau clustering để profiling.

## Bước 3 — triển khai code baseline/experiment

Dự kiến thêm:

```text
ml/src/features.py
ml/src/baseline.py
ml/src/experiment.py
ml/src/stability.py
ml/src/profile_clusters.py
ml/tests/test_features.py
ml/tests/test_experiment.py
```

Artifact dự kiến:

```text
reports/data/experiments/
reports/figures/experiments/
```

## Bước 4 — validation rồi mới freeze

Sau khi candidate được chạy trên đúng protocol:

1. dùng evidence train/validation để chọn preprocessing + K;
2. ghi lý do chọn K, không dựa vào một metric duy nhất;
3. freeze preprocessing/K/config;
4. chỉ sau khi freeze mới mở test đúng một lần cho báo cáo cuối.

## Không được làm ở bước kế tiếp

- Không nhìn test để chọn K.
- Không dùng `Channel`/`Region` làm nhãn hoặc target.
- Không tự động xóa outlier chỉ vì IQR flag.
- Không chọn K chỉ vì silhouette cao nhất.
- Không train model trong Node.js request.

## Lệnh nền tảng đã PASS

```powershell
python ml/src/prepare_data.py
python ml/src/eda.py
python -m pytest ml/tests -q
npm run test:backend
npm run build
```

Bước kế tiếp thực tế: **đọc số liệu EDA thật rồi mới commit protocol thí nghiệm và code baseline/K-Means.**
