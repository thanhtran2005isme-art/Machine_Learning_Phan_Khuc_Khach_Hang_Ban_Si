# Gate 9.2 — Frozen final K=2 development profiling

**Trạng thái: COMPLETE — CI VERIFIED, đã xuất CSV/JSON và commit vào GitHub.** [Run 37797274530](https://github.com/thanhtran2005isme-art/Machine_Learning_Phan_Khuc_Khach_Hang_Ban_Si/actions/runs/37797274530): 8/8 tests PASS; artifacts lặp lại SHA-256 giống nhau.

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

## Số liệu nghiệm thu thực tế (352 development, không phải final test)

- Cluster 0: **162 / 352 = 46,02%** — median: Fresh 6410,5; Milk 7226; Grocery 10842,5; Frozen 1153; Detergents_Paper 4084,5; Delicassen 1508,5.
- Cluster 1: **190 / 352 = 53,98%** — median: Fresh 9727,5; Milk 1626; Grocery 2175,5; Frozen 2194,5; Detergents_Paper 279,5; Delicassen 662.
- Outliers **khoảng cách** (IQR Q3+1,5 IQR theo từng cụm): cluster 0 = 5, cluster 1 = 11, tổng **16**; chỉ gắn cờ, không xóa.
- Inertia development trên mỗi quan sát (model đã frozen): **4.163874729781235**; trùng giá trị trong metadata Gate 5.
- Top 1% mẫu có khoảng cách lớn nhất: 4/352; chiếm **9,7224%** tổng squared distance.
- Channel, Region (chỉ diễn giải): tổng mỗi bảng = 352; share trong từng cluster cộng bằng 1. CSV xem tại `reports/data/final_profile/`.
- 6 CSV + `profile_metadata.json` được kiểm tra checksum và commit bởi GitHub Actions; metadata không chứa đường dẫn tuyệt đối máy cá nhân.
- Source phục vụ Gate 9.3: `reports/data/final_profile/profile_metadata.json`, liên kết SHA-256 đến sáu CSV, D011 K2/model hash.

## Kiểm thử CI đã xác minh

- Linux runner, Python 3.12: `python -m pip install -r ml/requirements.txt`, tải UCI, **chỉ chuẩn bị train/validation**; kiểm tra `test.csv` không tồn tại.
- **8 passed in 1.46s**, bao gồm toàn bộ 352 mẫu sklearn.joblib ↔ portable JSON, median/size/category, no-fit guard, không đọc test split, corruption/missing và tái lập.
- Tạo profile hai lần trên cùng frozen state cho SHA-256 file không đổi; checks count=162/190 và Channel/Region đều 352.
- Run: https://github.com/thanhtran2005isme-art/Machine_Learning_Phan_Khuc_Khach_Hang_Ban_Si/actions/runs/37797274530
- Generated commit: `74ddfb24bc771e048c1c025e6591e692e9d3de53`. Không sửa bất kỳ file nào trong `models/`.
- **Giới hạn:** đây là hậu phân cụm trên 352 development samples; không có phân tích test, không phải model mới; Gate 9.3/9.4 vẫn cần hiển thị dữ liệu qua API/web.
