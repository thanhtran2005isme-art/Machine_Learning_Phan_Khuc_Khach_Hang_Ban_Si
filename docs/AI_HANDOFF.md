# AI HANDOFF — trạng thái hiện tại

> Cập nhật: 2026-10-05  
> Branch: `main`

## 1. Mục tiêu hiện tại

Foundation, data pipeline, web/backend skeleton và EDA train-only đã PASS bằng log thật. EDA định lượng đã được đọc và ghi nhận. **Experiment protocol baseline + K-Means đã được đóng băng và experiment harness đã được code, nhưng chưa được chạy local sau commit mới.**

Test cuối vẫn đang khóa; chưa chọn K cuối.

## 2. Stack đã chốt

- Frontend: React + TypeScript + Vite.
- Backend: Node.js + TypeScript + Fastify + Zod.
- ML: Python + pandas + NumPy + scikit-learn + matplotlib.
- Test: Vitest cho backend, pytest cho ML/data.

## 3. Trạng thái đã kiểm chứng

### Gate B — DATA ✅ PASS

- raw: 440 dòng, 8 cột;
- missing 0;
- duplicate 0;
- split: train 264 / validation 88 / test 88, seed 42;
- raw SHA256: `c3d018c643565b85cee733c4a2ac76dd76e080e857cb23f0ccfcc2e15a6c17ef`;
- data tests ban đầu: `7 passed in 0.59s`.

### Gate C — web/backend ✅ PASS

- `/api/health` -> 200, `modelReady=false`;
- `/api/model-info` -> 503, `not_ready` đúng thiết kế;
- frontend Vite chạy local;
- backend tests: `2 passed`;
- frontend/backend build PASS.

### EDA train-only ✅ PASS

- `python ml/src/eda.py` chạy trên 264 dòng train;
- ML/data tests sau EDA: `11 passed in 7.72s`;
- chưa fit StandardScaler trong EDA;
- chưa dùng validation/test để ra quyết định EDA.

## 4. Kết luận EDA định lượng

Raw skewness đều dương và lớn:

- Fresh `2.5483` -> log1p `-1.7618`;
- Milk `4.2825` -> `-0.1716`;
- Grocery `2.7562` -> `-0.9354`;
- Frozen `3.5343` -> `-0.4632`;
- Detergents_Paper `2.9365` -> `-0.1562`;
- Delicassen `12.1154` -> `-0.8954`.

`log1p` giảm absolute skewness ở cả 6 biến. `Fresh` vẫn lệch đáng kể sau log1p nên không được tuyên bố dữ liệu đã trở thành normal.

IQR outlier trên train:

- Fresh 10 (3.79%);
- Milk 21 (7.95%);
- Grocery 20 (7.58%);
- Frozen 23 (8.71%);
- Detergents_Paper 19 (7.20%);
- Delicassen 14 (5.30%).

Chính sách giữ nguyên: **không tự động xóa/clip/winsorize outlier**.

## 5. Protocol thí nghiệm đã đóng băng

Tài liệu: `docs/EXPERIMENT_PROTOCOL.md`.

Hai nhánh:

1. `raw` — 6 biến chi tiêu gốc -> K-Means.
2. `log1p_scale` — `log1p` -> `StandardScaler.fit(train)` -> transform train/validation -> K-Means.

Candidate:

- K = 2..8;
- seeds = 0..9 (10 seed);
- `n_init=20`;
- `max_iter=300`;
- stability = pairwise Adjusted Rand Index trên train assignments;
- train/validation inertia;
- train/validation silhouette;
- cluster-size evidence;
- không auto-select K từ một metric.

Test không được đọc ở giai đoạn này.

## 6. Experiment harness đã code — CHỜ CHẠY LOCAL

File chính:

- `ml/src/experiments.py`;
- `ml/tests/test_experiments.py`;
- `ml/src/data_paths.py`;
- `docs/EXPERIMENT_PROTOCOL.md`;
- `package.json` có `ml:experiment`.

Experiment chỉ import/use train + validation, không dùng `test.csv`.

Artifact dự kiến:

```text
reports/data/experiments/
  baseline_descriptive.csv
  baseline_k2.csv
  runs.csv
  aggregate.csv
  stability.csv
  selection_evidence.csv
  experiment_metadata.json

reports/figures/experiments/
  elbow_train.png
  validation_silhouette.png
  stability_ari.png
  min_cluster_share.png
```

`experiment_metadata.json` phải ghi `test_used=false` và `selection_status=NOT_SELECTED`.

## 7. Chưa làm

- Chưa chạy harness mới trên máy local.
- Chưa biết kết quả inertia/silhouette/stability thực tế.
- Chưa profile candidate K.
- Chưa chọn/freeze preprocessing + K cuối.
- Chưa mở final test.
- Chưa export model/serving artifact.
- Chưa có `POST /api/segment`.
- Dashboard/model card chưa hoàn chỉnh.

## 8. Bước tiếp theo

1. `git pull origin main`.
2. `python -m pytest ml/tests -q`.
3. `python ml/src/experiments.py` hoặc `npm run ml:experiment`.
4. Kiểm tra terminal phải nói `TEST=NOT TOUCHED` và `Chưa chọn K`.
5. Đọc `reports/data/experiments/selection_evidence.csv`.
6. Chỉ dựa trên train/validation để so raw vs log1p_scale và K=2..8.
7. Profile 1–2 candidate K tốt nhất bằng median + Channel/Region.
8. Freeze quyết định trước khi mở test.

## 9. File nên đọc tiếp

- `docs/EXPERIMENT_PROTOCOL.md`
- `docs/EDA.md`
- `docs/NEXT_STEPS.md`
- `docs/DECISIONS.md`
- `docs/history/2026-10.md`

Nếu handoff khác code/test/git, tin code + test + git và sửa handoff.
