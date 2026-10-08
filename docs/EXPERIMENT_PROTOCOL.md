# Experiment Protocol — Project 22

## 1. Trạng thái

Protocol này được đóng băng **sau khi EDA train-only đã chạy PASS** và **trước khi xem kết quả test cuối**.

Mục tiêu: thực hiện baseline và thí nghiệm K-Means theo đúng yêu cầu đề, không leakage và không chọn K bằng một metric duy nhất.

## 2. Bằng chứng EDA dùng để chốt preprocessing

EDA chỉ dùng `data/processed/train.csv` với 264 dòng và 6 biến chi tiêu.

### Skewness raw → log1p

| Feature | Raw skewness | log1p skewness | Giảm absolute skewness |
|---|---:|---:|---:|
| Fresh | 2.5483 | -1.7618 | 0.7865 |
| Milk | 4.2825 | -0.1716 | 4.1109 |
| Grocery | 2.7562 | -0.9354 | 1.8208 |
| Frozen | 3.5343 | -0.4632 | 3.0711 |
| Detergents_Paper | 2.9365 | -0.1562 | 2.7803 |
| Delicassen | 12.1154 | -0.8954 | 11.2200 |

Kết luận được phép rút ra từ train:

- cả 6 biến raw đều lệch phải mạnh;
- `log1p` làm giảm **absolute skewness của cả 6 biến**;
- `Fresh` vẫn còn lệch đáng kể sau log1p (`-1.7618`), nên không được tuyên bố dữ liệu đã trở thành phân phối chuẩn;
- `Milk`, `Frozen`, `Detergents_Paper` trở nên gần đối xứng hơn rõ rệt;
- `Delicassen` có cải thiện lớn nhất về absolute skewness.

### Outlier IQR trên train

| Feature | Outlier | Tỷ lệ |
|---|---:|---:|
| Fresh | 10 | 3.79% |
| Milk | 21 | 7.95% |
| Grocery | 20 | 7.58% |
| Frozen | 23 | 8.71% |
| Detergents_Paper | 19 | 7.20% |
| Delicassen | 14 | 5.30% |

Chính sách: **không tự động xóa, clip hay winsorize outlier**. Outlier được giữ lại và dùng trong thí nghiệm chính; nếu muốn xử lý riêng phải tạo experiment khác.

### Mean lớn hơn median ở cả 6 biến

Ví dụ train:

- Fresh: mean `13032.03`, median `9195.5`;
- Milk: mean `5691.95`, median `3327.5`;
- Grocery: mean `7251.80`, median `4164.5`;
- Frozen: mean `3056.25`, median `1610.0`;
- Detergents_Paper: mean `2497.66`, median `700.0`;
- Delicassen: mean `1542.44`, median `983.5`.

Điều này nhất quán với phân phối lệch phải của dữ liệu raw.

## 3. Hai nhánh preprocessing bắt buộc

### Nhánh A — RAW

```text
6 biến chi tiêu gốc
        ↓
      K-Means
```

Mục đích: baseline/đối chứng theo yêu cầu raw-vs-preprocessed.

### Nhánh B — LOG1P + SCALE

```text
6 biến chi tiêu
        ↓
      log1p
        ↓
StandardScaler.fit(TRAIN)
        ↓
transform TRAIN + VALIDATION
        ↓
      K-Means
```

`StandardScaler` **chỉ fit trên train**. Validation chỉ được `transform` bằng tham số train.

Đây là nhánh preprocessing chính cần được xem xét nghiêm túc vì EDA train cho thấy log1p giảm absolute skewness trên toàn bộ 6 feature. Tuy nhiên nhánh cuối chỉ được chốt cùng với bằng chứng clustering/validation, không chỉ dựa vào EDA.

## 4. Baseline

### Baseline A — không clustering

Bảng mô tả train theo 6 feature:

- mean;
- median;
- std;
- Q1/Q3;
- IQR.

### Baseline B — K=2 đơn giản

- 6 biến raw;
- `K=2`;
- `random_state=42`;
- `n_init=10`;
- đánh giá train và validation;
- chỉ là mốc tham chiếu, không phải model cuối.

## 5. Candidate K

Bắt buộc chạy:

```text
K = 2, 3, 4, 5, 6, 7, 8
```

Không thử K ngoài khoảng này trong protocol chính trước khi hoàn tất yêu cầu đề.

## 6. Stability

Mỗi tổ hợp preprocessing/K chạy tối thiểu 10 seed:

```text
seed = 42..51
```

Mỗi K-Means dùng:

- `n_init=10`;
- `max_iter=300`;
- `algorithm="lloyd"`.

Độ ổn định chính được đo bằng **pairwise Adjusted Rand Index (ARI)** trên assignment của train giữa các seed. ARI phù hợp vì không bị ảnh hưởng bởi việc đổi tên cluster ID giữa các lần chạy.

## 7. Metric thu thập

Mỗi run lưu:

- train inertia;
- validation inertia theo centroid đã fit trên train;
- train silhouette;
- validation silhouette;
- kích thước từng cluster train;
- tỷ lệ cluster nhỏ nhất/lớn nhất;
- số vòng lặp K-Means;
- seed, K, preprocessing.

Mỗi K/preprocessing tổng hợp:

- mean/std inertia;
- mean/std silhouette;
- mean/min pairwise ARI;
- biến thiên cluster size.

## 8. Quy tắc chọn preprocessing và K

**Không tự động chọn K theo silhouette cao nhất.**

Quyết định phải xem đồng thời:

1. Elbow/inertia trên train.
2. Silhouette train và validation.
3. Stability qua seed bằng ARI.
4. Kích thước cluster có hợp lý hay có cluster quá nhỏ/bất thường.
5. Khả năng diễn giải cluster profile.
6. Sự nhất quán giữa train và validation.

Không có cutoff cluster-size cứng trong protocol chính; tỷ lệ cluster nhỏ được report như bằng chứng để phân tích, tránh đặt ngưỡng tùy ý sau khi xem kết quả.

## 9. Validation và test

Trong giai đoạn này chỉ đọc:

```text
train.csv
validation.csv
```

**Không đọc `test.csv`.**

Test chỉ được dùng sau khi:

- chọn preprocessing;
- chọn K;
- chốt các tham số serving;
- ghi quyết định vào docs/DECISIONS.md;
- freeze model-selection protocol.

## 10. Artifact của experiment harness

Sau khi chạy:

```powershell
python ml/src/experiments.py
```

hoặc:

```powershell
npm run ml:experiment
```

sẽ sinh:

```text
reports/data/experiments/
  baseline_descriptive.csv
  baseline_k2.csv
  runs.csv
  aggregate.csv
  stability.csv
  stability_pairs.csv
  selection_evidence.csv
  experiment_metadata.json

reports/figures/experiments/
  elbow_train.png
  validation_silhouette.png
  stability_ari.png
  min_cluster_share.png
```

`experiment_metadata.json` phải ghi:

```text
test_used = false
selection_status = NOT_SELECTED
```

## 11. Sau khi experiment chạy PASS

1. Đọc `selection_evidence.csv`.
2. Phân tích raw vs `log1p+scale`.
3. Phân tích K=2..8.
4. Kiểm tra stability và cluster size.
5. Profile candidate K tốt nhất bằng median + Channel/Region sau clustering.
6. Chọn/freeze preprocessing + K bằng validation evidence.
7. Chỉ sau đó mới mở final test đúng một lần.
