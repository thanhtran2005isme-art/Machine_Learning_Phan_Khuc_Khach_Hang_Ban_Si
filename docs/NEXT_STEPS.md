# Bước tiếp theo — chạy experiment, review candidate, chưa mở test

Foundation, data pipeline, web/backend skeleton và EDA train-only đã PASS. Protocol K-Means đã được đóng băng trước test. Code experiment/review/profile đã có trên `main`, nhưng **chưa có log local thật cho giai đoạn mới nhất**.

## 1. Pull code mới nhất

```powershell
git pull origin main
```

## 2. Chạy toàn bộ pytest sau khi thêm experiment/review/profile

```powershell
python -m pytest ml/tests -q
```

Chỉ ghi số test PASS khi có output thật.

## 3. Chạy 140 K-Means runs

```powershell
python ml/src/experiments.py
```

hoặc:

```powershell
npm run ml:experiment
```

Terminal phải xác nhận:

```text
TRAIN=264
VALIDATION=88
TEST=NOT TOUCHED
Preprocessing: raw, log1p_scale
K: 2..8
Seeds: 10 (0..9)
Runs: 140
Chưa chọn K
```

Artifact chính:

```text
reports/data/experiments/selection_evidence.csv
reports/data/experiments/experiment_metadata.json
reports/figures/experiments/elbow_train.png
reports/figures/experiments/validation_silhouette.png
reports/figures/experiments/stability_ari.png
reports/figures/experiments/min_cluster_share.png
```

## 4. Review evidence đa tiêu chí

```powershell
python ml/src/review_experiments.py
```

hoặc:

```powershell
npm run ml:review
```

Script phải kiểm tra:

- đủ 14 candidate rows = 2 preprocessing x 7 K;
- mỗi candidate >=10 runs;
- metric hữu hạn;
- `test_used=false`;
- `selection_status=NOT_SELECTED`.

Artifact:

```text
reports/data/experiments/review_table.csv
reports/EXPERIMENT_REVIEW.md
```

Review chỉ tạo rank riêng theo từng tiêu chí. **Không có total score và không auto-select K.**

## 5. Shortlist rồi mới profile

Từ evidence, chọn shortlist nhỏ 1–3 candidate để profile. Ví dụ cú pháp:

```powershell
python ml/src/profile_candidate.py --preprocessing log1p_scale --k 3 --seed 0
```

hoặc:

```powershell
npm run ml:profile -- --preprocessing log1p_scale --k 3 --seed 0
```

`K=3` chỉ là ví dụ cú pháp, không phải quyết định trước khi đọc evidence.

Candidate profile tạo:

- median chi tiêu train/validation theo cluster, đơn vị gốc;
- Channel/Region profile sau clustering;
- distance-to-centroid summary;
- centroid back-transform để tham chiếu;
- median ratio plot;
- cluster size plot;
- metadata xác nhận test chưa dùng.

## 6. Khi nào mới được freeze preprocessing + K?

Chỉ sau khi xem đồng thời:

1. elbow/inertia;
2. validation silhouette + độ lệch train↔validation;
3. ARI stability qua seed;
4. cluster size/share;
5. median profile có ý nghĩa và không bị outlier dẫn dắt;
6. Channel/Region chỉ hỗ trợ mô tả, không làm ground truth.

Sau đó ghi quyết định vào `docs/DECISIONS.md` và cập nhật metadata selection.

## 7. Test vẫn khóa

Không được đọc `data/processed/test.csv` để:

- chọn preprocessing;
- chọn K;
- chọn seed;
- chọn cách xử lý outlier;
- sửa protocol sau khi thấy kết quả test.

Chỉ sau freeze mới mở final test đúng một lần.

## 8. Trạng thái chưa làm

- experiment local chưa PASS;
- chưa có selection evidence thật;
- chưa shortlist;
- chưa profile candidate thật;
- chưa freeze preprocessing/K;
- chưa final test;
- chưa export serving artifact;
- chưa triển khai `POST /api/segment`;
- dashboard/model card chưa hoàn chỉnh.

Chi tiết protocol: `docs/EXPERIMENT_PROTOCOL.md`.  
Chi tiết review/profile: `docs/CANDIDATE_REVIEW.md`.
