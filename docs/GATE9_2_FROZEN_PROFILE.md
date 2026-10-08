# Gate 9.2 — Frozen final K=2 development profiling

**Trạng thái:** Source và tests đã thêm; chỉ đánh dấu COMPLETE sau khi Linux CI chạy PASS và CSV/JSON đầu ra được xác minh, commit.

## Mục tiêu

- Đọc **duy nhất** train 264 + validation 88 để phân tích mô hình cuối, **không đọc test CSV**.
- Model canonical: `models/model.json` D011, `log1p + StandardScaler`, K=2, fit 352 development trước đó.
- **Không gọi** `fit`, `fit_transform`, `ml:freeze`, `ml:finalize`, không thay sklearn model/centroids/scaler.
- Dữ liệu phân khúc: `cluster_summary.csv` với size, share và median 6 chi tiêu; `median_ratio.csv` so overall development; `cluster_sizes.csv`.
- Channel/Region: `channel_profile.csv`, `region_profile.csv`, chỉ mô tả hậu phân cụm; count/share chính xác mỗi cluster.
- Distance: `distance_summary.csv` theo khoảng cách Euclidean trong không gian scaled đã lưu (min/mean/median/p90/p95/max, outlier > Q3+1.5IQR và mean inertia).
- `profile_metadata.json`: checksum model, selection và hai split, chính sách không fit/no-test và SHA-256 mỗi artifact; không có đường dẫn tuyệt đối cá nhân.

## Reproducible development-only run

Trên máy đã có `data/processed/train.csv` và `validation.csv` **đúng frozen SHA**:

```powershell
python -m pip install -r ml/requirements.txt
python -m pytest ml/tests/test_final_profile.py -q
python -m ml.src.final_profile
```

Ở máy sạch, chỉ cần raw UCI + 2 development splits (không tạo test.csv trong Gate 9.2):

```powershell
python -m ml.src.download_data
python -m ml.src.prepare_development_only
python -m pytest ml/tests/test_final_profile.py -q
python -m ml.src.final_profile
```

## Verification gates

- Source SHA / development split checksums phải khớp evidence D011; khi sai **fail closed**.
- Trên chính 352 mẫu: Python sklearn joblib `predict/transform` và portable JSON nearest-centroid phải cho cùng nhãn và distance.
- Cluster sizes cuối phải khớp model.json: **162/190**; median của sáu biến phải trùng model.json.
- Category profile tính tổng bằng 352, share trong mỗi cluster cộng bằng 1.
- Lặp lại output cho checksum không đổi. Tampering/missing data và mọi hành vi fit bị phát hiện.
- CI upload artifact và commit vào `reports/data/final_profile/` chỉ sau khi tests thành công.
- **Không** sử dụng kết quả của final test đã đóng ở Gate 5.

## Handoff Gate 9.3

API chỉ đọc `reports/data/final_profile/profile_metadata.json` và các file CSV có checksum khớp. Không nhầm với `reports/data/profiles/log1p_standardscaler_k2_seed42/` vốn là candidate **264 train-only**.
