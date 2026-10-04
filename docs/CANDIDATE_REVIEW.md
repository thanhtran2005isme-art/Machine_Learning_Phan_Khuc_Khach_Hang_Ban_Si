# Review experiment và profiling candidate — Project 22

Tài liệu này mô tả bước **sau khi `ml/src/experiments.py` chạy PASS** và **trước khi freeze preprocessing + K**.

## 1. Nguyên tắc

Không chọn K tự động từ một metric duy nhất. Quyết định phải xem đồng thời:

- elbow / inertia trên train;
- silhouette trên train và validation;
- stability qua seed bằng pairwise ARI;
- tỷ lệ cluster nhỏ nhất/lớn nhất;
- mức nhất quán train ↔ validation;
- khả năng diễn giải profile theo median chi tiêu;
- `Channel`/`Region` chỉ dùng mô tả sau clustering.

Test vẫn khóa trong toàn bộ bước này.

## 2. Review evidence

Sau khi chạy experiment:

```powershell
python ml/src/experiments.py
```

chạy:

```powershell
python ml/src/review_experiments.py
```

hoặc:

```powershell
npm run ml:review
```

Script kiểm tra protocol có đủ:

- 2 preprocessing: `raw`, `log1p_scale`;
- K = 2..8;
- ít nhất 10 run/seed mỗi tổ hợp;
- metric bắt buộc không NaN/inf;
- `experiment_metadata.json` phải xác nhận `test_used=false` và `selection_status=NOT_SELECTED`.

Artifact:

```text
reports/data/experiments/review_table.csv
reports/EXPERIMENT_REVIEW.md
```

`review_table.csv` có các rank riêng cho silhouette, ARI và cluster share. **Không có total score** và không được cộng rank để auto-select K.

## 3. Shortlist candidate

Sau review, chọn một shortlist nhỏ (thường 1–3 candidate) để profile. Shortlist chưa phải model cuối.

Ví dụ:

```powershell
python ml/src/profile_candidate.py --preprocessing log1p_scale --k 3 --seed 0
```

hoặc:

```powershell
npm run ml:profile -- --preprocessing log1p_scale --k 3 --seed 0
```

`K=3` ở ví dụ trên chỉ minh họa cú pháp; không phải K được đề xuất trước khi đọc evidence thật.

## 4. Candidate profiling tạo gì?

Mỗi candidate tạo thư mục riêng:

```text
reports/data/profiles/<preprocessing>_k<K>_seed<seed>/
reports/figures/profiles/<preprocessing>_k<K>_seed<seed>/
```

Bảng chính:

- median chi tiêu train theo cluster, đơn vị gốc;
- median chi tiêu validation theo cluster;
- Channel profile train/validation;
- Region profile train/validation;
- distance-to-centroid summary train/validation;
- centroid back-transform về đơn vị gốc để tham chiếu;
- median ratio so với overall train median;
- metadata xác nhận `test_used=false`.

Hình:

- `median_ratio.png`;
- `cluster_sizes.png`.

## 5. Vai trò Channel/Region

K-Means **không fit bằng Channel hoặc Region**.

Luồng đúng:

```text
6 spending features
      ↓
preprocessing
      ↓
K-Means fit train
      ↓
cluster label
      ↓
ghép Channel/Region
      ↓
profiling mô tả
```

Không dùng Channel/Region làm ground truth để chọn K.

## 6. Median là profile chính

Dữ liệu chi tiêu lệch và có outlier, do đó profile kinh doanh chính dùng **median theo cluster trong đơn vị gốc**. Centroid inverse-transform chỉ là thông tin tham chiếu, đặc biệt ở nhánh `log1p_scale`.

## 7. Khi nào được freeze?

Chỉ freeze preprocessing + K sau khi:

1. experiment protocol đủ 140 runs;
2. review đa tiêu chí xong;
3. shortlist đã được profile;
4. profile có khả năng diễn giải và không tạo cluster bất thường chỉ vì outlier;
5. quyết định + lý do được ghi vào `docs/DECISIONS.md`;
6. metadata selection được cập nhật rõ ràng.

Sau freeze mới được mở final test đúng một lần.
