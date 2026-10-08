<<<<<<< HEAD
# Bước tiếp theo — sau Gate D baseline + K-Means

Gate B data, Gate C skeleton, EDA train-only và **Gate D baseline/grid K-Means đã chạy thật**. Bản thí nghiệm đã tạo đủ 140 runs trên train/validation, 0 silhouette validation không xác định. Xem `docs/EXPERIMENTS.md`.

## Đã cố định và thực hiện

- Data split 264 train / 88 validation / 88 test, seed 42.
- Feature K-Means đúng 6 biến chi tiêu; `Channel`/`Region` chỉ profiling sau fit.
- Baseline A thống kê train; Baseline B raw K=2 seed42.
- Raw và `log1p + StandardScaler`; K=2..8; seed42..51; `n_init=10`, `algorithm=lloyd`.
- Fit scaler/K-Means trên train; validation chỉ transform/predict; **test chưa đọc**.
- Inertia/silhouette train/validation; cluster size/proportion, profiling và 45 cặp ARI cho mỗi preprocessing/K.
- CSV, JSON và 4 PNG tại `reports/data/experiments/` và `reports/figures/experiments/`.

## Việc tiếp theo (ngoài phạm vi Gate D)

1. Đọc `reports/data/experiments/seed_summary.csv`, `stability.csv`, `cluster_sizes.csv`, `cluster_profiles.csv` và 4 biểu đồ.
2. So sánh hiệu quả, độ ổn định, phân bổ kích thước cụm và ý nghĩa nghiệp vụ giữa K/preprocessing; inertia chỉ so sánh trong cùng không gian.
3. Lập luận lựa chọn K/preprocessing dựa trên train + validation và khóa config trước final test; không chọn chỉ theo silhouette cao nhất.
4. Chạy final test độc lập **sau khi freeze**, đánh giá và xuất model artifact.
5. Sau cùng mới thực hiện serving backend / frontend theo kế hoạch riêng.

## Lệnh kiểm chứng Gate D

```powershell
python ml/src/experiment.py
python -m pytest ml/tests -q
```

Không mở `data/processed/test.csv` hoặc dùng test chọn K/tham số trong các bước 1–3. Không tự động loại outlier, không dùng Channel/Region làm nhãn thật.
=======
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
>>>>>>> fcfd75fb02b6ead0eabf976c16e7684e4a186254
