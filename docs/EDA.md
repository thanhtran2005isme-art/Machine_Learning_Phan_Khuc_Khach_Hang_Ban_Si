# EDA trên train — Project 22

## 1. Mục tiêu

EDA chỉ dùng để hiểu **6 biến chi tiêu trên `train.csv`** và tạo bằng chứng cho quyết định tiền xử lý trước K-Means.

Không dùng validation/test để chọn preprocessing, không chọn K và không fit model trong bước EDA.

## 2. Phạm vi dữ liệu

Nguồn duy nhất:

```text
data/processed/train.csv
```

Train đã được kiểm chứng có `264` dòng. Sáu biến:

- `Fresh`
- `Milk`
- `Grocery`
- `Frozen`
- `Detergents_Paper`
- `Delicassen`

`Channel` và `Region` chỉ dành cho profiling sau clustering.

## 3. Trạng thái kiểm chứng

EDA đã chạy thành công trên Windows 10:

```text
[eda] Scope: TRAIN ONLY — 264 dòng
[eda] Features: Fresh, Milk, Grocery, Frozen, Detergents_Paper, Delicassen
[eda] Chưa fit StandardScaler, chưa chạy K-Means, không dùng validation/test để ra quyết định.
```

Sau khi thêm EDA, ML/data tests:

```text
11 passed in 7.72s
```

## 4. Skewness raw và sau log1p

| Feature | Raw skewness | log1p skewness | Giảm absolute skewness |
|---|---:|---:|---:|
| Fresh | 2.5483 | -1.7618 | 0.7865 |
| Milk | 4.2825 | -0.1716 | 4.1109 |
| Grocery | 2.7562 | -0.9354 | 1.8208 |
| Frozen | 3.5343 | -0.4632 | 3.0711 |
| Detergents_Paper | 2.9365 | -0.1562 | 2.7803 |
| Delicassen | 12.1154 | -0.8954 | 11.2200 |

Kết luận từ train:

- cả 6 biến raw đều lệch phải mạnh;
- `log1p` giảm absolute skewness ở **cả 6 biến**;
- `Fresh` vẫn lệch đáng kể sau log1p, nên không được nói dữ liệu đã trở thành phân phối chuẩn;
- `Milk`, `Frozen`, `Detergents_Paper` gần đối xứng hơn rõ rệt;
- `Delicassen` cải thiện lớn nhất về absolute skewness.

## 5. Median/IQR và outlier IQR

### Tóm tắt raw

| Feature | Mean | Median | Q1 | Q3 | IQR |
|---|---:|---:|---:|---:|---:|
| Fresh | 13032.03 | 9195.5 | 3361.25 | 18629.0 | 15267.75 |
| Milk | 5691.95 | 3327.5 | 1449.75 | 6578.0 | 5128.25 |
| Grocery | 7251.80 | 4164.5 | 2127.0 | 9265.5 | 7138.5 |
| Frozen | 3056.25 | 1610.0 | 742.25 | 3731.0 | 2988.75 |
| Detergents_Paper | 2497.66 | 700.0 | 234.75 | 3492.75 | 3258.0 |
| Delicassen | 1542.44 | 983.5 | 435.5 | 1877.0 | 1441.5 |

Mean lớn hơn median ở cả 6 biến, nhất quán với phân phối lệch phải raw.

### Outlier IQR

| Feature | Outlier count | Tỷ lệ |
|---|---:|---:|
| Fresh | 10 | 3.79% |
| Milk | 21 | 7.95% |
| Grocery | 20 | 7.58% |
| Frozen | 23 | 8.71% |
| Detergents_Paper | 19 | 7.20% |
| Delicassen | 14 | 5.30% |

Chính sách vẫn là **không tự động xóa/clip/winsorize outlier**.

## 6. Bằng chứng range raw → log1p

Ví dụ:

- Fresh: raw `3..112151` → log1p `1.386..11.628`;
- Milk: raw `55..73498` → log1p `4.025..11.205`;
- Grocery: raw `3..59598` → log1p `1.386..10.995`;
- Frozen: raw `25..36534` → log1p `3.258..10.506`;
- Detergents_Paper: raw `3..26701` → log1p `1.386..10.192`;
- Delicassen: raw `7..47943` → log1p `2.079..10.778`.

Điều này cho thấy log1p nén mạnh khoảng giá trị, nhưng quyết định cuối vẫn phải được kiểm chứng bằng clustering/validation.

## 7. Quyết định preprocessing sau EDA

EDA cung cấp đủ bằng chứng để **đưa `log1p + StandardScaler` thành nhánh preprocessing chính cần đánh giá**, đồng thời vẫn giữ nhánh `raw` làm đối chứng bắt buộc.

StandardScaler chưa được fit trong EDA. Ở experiment, scaler chỉ được fit trên train và validation chỉ `transform`.

Chi tiết protocol đã đóng băng tại:

```text
docs/EXPERIMENT_PROTOCOL.md
```

## 8. Artifact EDA

```text
reports/data/eda/
  train_summary_raw.csv
  train_summary_log1p.csv
  train_skewness.csv
  train_iqr_outliers.csv
  preprocessing_comparison.csv
  eda_metadata.json

reports/figures/eda/
  train_distributions_raw.png
  train_distributions_log1p.png
  train_boxplots_raw.png
  train_boxplots_log1p.png
  train_correlation_raw.png
  train_correlation_log1p.png
```

## 9. Bước tiếp theo

1. Chạy baseline mô tả không clustering.
2. Chạy baseline K=2.
3. So sánh raw với `log1p + StandardScaler`.
4. Chạy K=2..8.
5. Mỗi tổ hợp chạy ít nhất 10 seed.
6. Tổng hợp validation silhouette, inertia, stability ARI và cluster size.
7. Không đọc test cho đến khi preprocessing + K được freeze.
