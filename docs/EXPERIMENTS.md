# Gate D — Baseline và K-Means K=2..8

## Protocol cố định (trước khi chọn mô hình)

- Train: 264 khách hàng; validation: 88; test: 88 **chưa đọc**.
- Feature fit: `Fresh`, `Milk`, `Grocery`, `Frozen`, `Detergents_Paper`, `Delicassen`.
- `Channel`, `Region` chỉ dùng profiling sau khi phân cụm.
- Baseline A: thống kê từng feature train (không clustering).
- Baseline B: K-Means **raw**, K=2, `random_state=42`, `n_init=10`, `algorithm=lloyd`.
- Grid: `raw` và `log1p + StandardScaler`; K=2,3,4,5,6,7,8; seed=42..51: **2 × 7 × 10 = 140 runs**.
- `StandardScaler.fit_transform` chỉ trên train; `StandardScaler.transform` trên validation.
- `KMeans.fit_predict` chỉ trên train; `KMeans.predict` trên validation.
- Không xóa outlier; không chọn K/preprocessing/seed trong bước tạo grid; test giữ kín.

Sáu feature train đều giảm độ lệch tuyệt đối sau `log1p` theo `reports/data/eda/train_skewness.csv`; đây là bằng chứng EDA cho việc **thử** nhánh log, không thay thế việc so sánh hai nhánh.

## Chỉ số

- Inertia train: tổng bình phương khoảng cách từ từng điểm train đến tâm cụm do model train tìm được; kiểm tra bằng `model.inertia_`.
- Inertia validation: tổng bình phương khoảng cách từ **validation đã transform** đến tâm cụm train được gán bởi `predict`; không fit lại tâm. Inertia raw và inertia scaled có đơn vị khác nhau, **không so sánh trực tiếp trị tuyệt đối giữa hai nhánh**.
- Silhouette train: tính trên train và nhãn do fit; silhouette validation: tính trên tập validation và nhãn do predict (không refit). Cần 2 đến n−1 nhãn cụm khác nhau. Trường hợp không xác định ghi `null` và lý do, không tự điền 0.
- Cluster sizes: số mẫu và tỷ trọng mỗi cụm, cho cả train và validation (có thể có 0 mẫu ở một cụm validation); tổng số mẫu và tổng tỷ trọng phải đúng.
- Stability: `adjusted_rand_score` cho từng cặp trong 10 seed trên **cùng train**, 45 cặp cho mỗi cặp (preprocessing, K). ARI không phụ thuộc hoán vị ID cụm.
- Profiling: median 6 biến chi tiêu theo cụm trên đơn vị gốc, tỷ trọng `Channel`/`Region` chỉ tính **sau phân cụm**.

## Chạy và kiểm chứng

```powershell
python ml/src/prepare_data.py  # chỉ khi chưa có split hợp lệ
python ml/src/experiment.py
python -m pytest ml/tests -q
```

Có thể chạy qua npm: `npm run ml:experiments`. Các artifact thật:

```text
reports/data/experiments/baseline_a_train.csv
reports/data/experiments/baseline_b.json
reports/data/experiments/runs.csv
reports/data/experiments/cluster_sizes.csv
reports/data/experiments/cluster_profiles.csv
reports/data/experiments/seed_summary.csv
reports/data/experiments/stability.csv
reports/data/experiments/metadata.json

reports/figures/experiments/inertia_train.png
reports/figures/experiments/inertia_validation.png
reports/figures/experiments/silhouette_train.png
reports/figures/experiments/silhouette_validation.png
```

Đồ thị thể hiện mean ± SD qua 10 seed. Với inertia, mỗi nhánh có một trục riêng để tránh so sánh độ lớn giữa hai không gian đặc trưng.

Metadata có SHA256 của **train và validation**, phiên bản scikit-learn, số runs, n_init, phương pháp đánh giá, số silhouette không xác định và đường dẫn artifact. File CSV/JSON được xuất không kèm timestamp để có thể so sánh tái lập byte-to-byte trên cùng môi trường.

## Ranh giới giai đoạn

Gate D chỉ thiết lập baseline và evidence của grid. Bước kế tiếp mới diễn giải train/validation, cân nhắc trade-off giữa silhouette, stability, size, khả năng giải thích cụm và lựa chọn K. Chỉ khi quyết định được đóng băng mới tiến tới final test độc lập. Backend/frontend và serving không thuộc gate này.
