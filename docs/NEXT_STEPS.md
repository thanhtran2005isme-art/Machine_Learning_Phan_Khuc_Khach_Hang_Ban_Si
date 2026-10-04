# Bước tiếp theo — kiểm chứng EDA train-only

EDA đã được dựng trong code tại commit `5a64acb075b065c61bb547f02a88e599a452e1a6`, nhưng chưa được đánh dấu PASS cho đến khi chạy thật trên máy local.

## 1. Pull bản mới nhất

```powershell
git pull origin main
```

## 2. Khóa nốt Gate C

Hai kiểm tra còn thiếu bằng chứng:

```powershell
npm run test:backend
npm run build
```

Backend/frontend runtime đã được xác nhận chạy local; hai lệnh trên cần PASS để đánh dấu Gate C hoàn chỉnh.

## 3. Chạy EDA chỉ trên train

```powershell
python ml/src/eda.py
```

hoặc:

```powershell
npm run eda:train
```

Script phải in rõ:

```text
[eda] Scope: TRAIN ONLY — 264 dòng
```

và xác nhận chưa fit StandardScaler/K-Means.

## 4. Chạy test ML/data sau khi thêm EDA

```powershell
python -m pytest ml/tests -q
```

Không ghi số test PASS trước khi có output thật.

## 5. Artifact cần xuất hiện

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

## 6. Những gì được phép kết luận sau EDA

Chỉ dựa trên train:

- phân phối 6 biến chi tiêu;
- skewness raw và sau `log1p`;
- median/IQR;
- outlier IQR để mô tả;
- correlation;
- mức thay đổi hình dạng phân phối sau `log1p`.

Không được:

- đọc test để chọn preprocessing;
- dùng Channel/Region làm feature K-Means;
- tự động xóa outlier;
- fit scaler trên full dataset;
- chọn K trong EDA.

## 7. Sau khi EDA PASS

Đóng băng thiết kế thí nghiệm trước K-Means:

1. baseline thống kê không clustering;
2. baseline K=2;
3. raw vs `log1p + StandardScaler`;
4. K=2..8;
5. ít nhất 10 seed;
6. validation evidence để chọn K;
7. final test chỉ sau khi quyết định đã freeze.

Chi tiết EDA: `docs/EDA.md`.
