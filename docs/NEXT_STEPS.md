# Next Steps — Gate 4

Phạm vi: **stability, evidence review và candidate profiling**. Chưa chọn/freeze mô hình, chưa mở final test, chưa sửa backend/frontend.

## Protocol D010
- Preprocessing: `raw`, `log1p_standardscaler`.
- K=2..8; seed=42..51; `n_init=10`, `max_iter=300`, `algorithm=lloyd`.
- 140 K-Means runs, 14 candidate, 45 ARI pairs/candidate, tổng 630 pairs.
- Scaler/model fit trên train; validation transform/predict; Channel/Region sau fit cho profiling.

## Lệnh kiểm chứng
```powershell
python -m pytest ml/tests -q
python ml/src/experiments.py
python ml/src/review_experiments.py
```

Đối chiếu thực tế CSV/JSON tại `reports/data/experiments/`, các PNG ở `reports/figures/experiments/` và báo cáo `reports/EXPERIMENT_REVIEW.md`.

## Shortlist và profiling
Sau khi đọc `review_table.csv` và train/validation evidence, xác định 1–3 candidate và ghi rõ rationale. Chạy từng cấu hình:
```powershell
python ml/src/profile_candidate.py --preprocessing log1p_standardscaler --k 3 --seed 42
```
K=3 chỉ là ví dụ cú pháp. Profile median 6 biến đơn vị gốc, Channel/Region hậu phân cụm, distance-to-centroid, inverse-transform, cluster size, outliers và biểu đồ.

## Gate tiếp theo (ngoài phạm vi)
Sau khi diễn giải profile mới chọn/freeze config trong `docs/DECISIONS.md`, rồi mới mở independent test đúng một lần. Chưa xuất model hay triển khai API/UI.
