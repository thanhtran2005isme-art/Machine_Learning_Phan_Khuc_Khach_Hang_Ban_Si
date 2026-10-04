# AI HANDOFF — trạng thái hiện tại

> Cập nhật: 2026-10-05  
> Branch: `main`  
> Trạng thái: Gate B PASS, Gate C PASS, EDA PASS; experiment/review/profile code đã dựng, đang chờ chạy local để có evidence thật.

## 1. Mục tiêu hiện tại

Foundation, data pipeline, web/backend skeleton và EDA train-only đã PASS bằng log thật. EDA định lượng đã được đọc và protocol baseline + K-Means đã được đóng băng. **Test cuối vẫn khóa; chưa chọn preprocessing/K cuối.**

Đã có code cho:

- experiment harness raw vs `log1p + StandardScaler`;
- K=2..8;
- >=10 seed;
- inertia/silhouette/stability ARI/cluster size;
- review đa tiêu chí không auto-select;
- candidate profiling bằng median chi tiêu + Channel/Region.

Việc tiếp theo là chạy experiment thật, review evidence, profile shortlist rồi mới freeze preprocessing + K.

## 2. Stack đã chốt

- Frontend: React + TypeScript + Vite.
- Backend: Node.js + TypeScript + Fastify + Zod.
- ML: Python + pandas + NumPy + scikit-learn + matplotlib.
- Test: Vitest cho backend, pytest cho ML/data.
- Node yêu cầu `>=20`.

## 3. Trạng thái đã kiểm chứng bằng log thật

### Gate B — DATA ✅ PASS

```text
python ml/src/prepare_data.py
[audit] PASS: 440 dòng, 8 cột
[audit] Missing: 0
[audit] Duplicate rows: 0
[split] PASS: train=264, validation=88, test=88, seed=42

python -m pytest ml/tests -q
7 passed in 0.59s
```

Raw SHA256:

```text
c3d018c643565b85cee733c4a2ac76dd76e080e857cb23f0ccfcc2e15a6c17ef
```

### Gate C — web/backend ✅ PASS

```text
GET /api/health -> 200, status=ok, modelReady=false
GET /api/model-info -> 503, status=not_ready
npm run dev:frontend -> Vite ready at http://localhost:5173/

npm run test:backend
Test Files 1 passed
Tests 2 passed

npm run build
frontend PASS
backend PASS
```

### EDA train-only ✅ PASS

```text
python ml/src/eda.py
[eda] Scope: TRAIN ONLY — 264 dòng
[eda] Features: Fresh, Milk, Grocery, Frozen, Detergents_Paper, Delicassen
[eda] Chưa fit StandardScaler, chưa chạy K-Means, không dùng validation/test để ra quyết định.

python -m pytest ml/tests -q
11 passed in 7.72s
```

## 4. EDA evidence đã đọc và chốt

Raw skewness → log1p skewness:

- Fresh: `2.5483 -> -1.7618`
- Milk: `4.2825 -> -0.1716`
- Grocery: `2.7562 -> -0.9354`
- Frozen: `3.5343 -> -0.4632`
- Detergents_Paper: `2.9365 -> -0.1562`
- Delicassen: `12.1154 -> -0.8954`

Kết luận hợp lệ:

- cả 6 feature raw lệch phải mạnh;
- `log1p` giảm absolute skewness ở cả 6 feature;
- Fresh vẫn còn lệch đáng kể sau log1p, không được nói dữ liệu đã “normal”;
- outlier IQR giữ nguyên, chưa xóa/clip/winsorize;
- nhánh chính cần được xem xét là `log1p + StandardScaler`, nhưng raw vẫn giữ làm đối chứng bắt buộc.

## 5. Experiment protocol đã dựng

File chính:

- `ml/src/experiments.py`
- `ml/tests/test_experiments.py`
- `docs/EXPERIMENT_PROTOCOL.md`

Protocol:

```text
preprocessing = raw, log1p_scale
K = 2..8
seed = 0..9
n_init = 20
max_iter = 300
algorithm = lloyd
```

Tổng chính: `2 x 7 x 10 = 140` K-Means runs.

Metric:

- train/validation inertia;
- train/validation silhouette;
- pairwise ARI stability trên train assignments;
- cluster size/share;
- n_iter.

Metadata phải giữ:

```text
test_used=false
selection_status=NOT_SELECTED
```

## 6. Review + candidate profiling đã dựng

Commit code: `2271c2197b66a0d297bab5003bf4dddfe0ce9322` (`feat(ml): add experiment review and candidate profiling`).

File mới:

- `ml/src/review_experiments.py`
- `ml/src/profile_candidate.py`
- `ml/tests/test_review_experiments.py`
- `ml/tests/test_profile_candidate.py`
- `docs/CANDIDATE_REVIEW.md`

Script review:

```powershell
python ml/src/review_experiments.py
```

- kiểm tra đủ 14 candidate rows (2 preprocessing x 7 K);
- mỗi candidate >=10 runs;
- metric hữu hạn;
- metadata xác nhận test chưa dùng;
- tạo rank riêng cho silhouette / ARI / cluster share;
- **không tạo total score, không auto-select K**.

Script profiling:

```powershell
python ml/src/profile_candidate.py --preprocessing <raw|log1p_scale> --k <2..8> --seed <seed>
```

Tạo:

- train/validation median profile theo cluster;
- Channel/Region profile sau clustering;
- train/validation distance summary;
- centroid inverse-transform về đơn vị gốc để tham chiếu;
- median ratio plot;
- cluster size plot;
- metadata `test_used=false`, `not_final_model=true`.

## 7. Ràng buộc học thuật không được phá

- 6 biến chi tiêu là feature chính.
- `Channel`/`Region` profiling only.
- Split trước preprocessing.
- Scaler chỉ fit train.
- Validation chỉ transform/predict bằng object fit train.
- Test không dùng để chọn preprocessing/K/seed.
- Không auto-select K theo silhouette hoặc một điểm tổng tự chế.
- Median trong đơn vị gốc là profile diễn giải chính.
- Backend không train model ở request time.

## 8. Chưa được phép ghi PASS / chưa làm

Chưa có log local thật cho code mới nhất:

- `python -m pytest ml/tests -q` sau khi thêm experiment/review/profile tests;
- `python ml/src/experiments.py`;
- `python ml/src/review_experiments.py`;
- chưa có `selection_evidence.csv` thật;
- chưa shortlist candidate;
- chưa chạy candidate profiling;
- chưa freeze preprocessing + K;
- chưa mở final test;
- chưa export final serving artifact;
- chưa có `POST /api/segment` thực;
- dashboard/model card chưa hoàn chỉnh.

## 9. Bước tiếp theo

1. `git pull origin main`.
2. `python -m pytest ml/tests -q`.
3. `python ml/src/experiments.py`.
4. `python ml/src/review_experiments.py`.
5. Đọc `reports/data/experiments/review_table.csv` + `selection_evidence.csv`.
6. Chọn shortlist nhỏ dựa trên đa tiêu chí; chưa freeze.
7. Chạy `profile_candidate.py` cho shortlist.
8. Review profile median + Channel/Region + cluster size rồi mới ghi quyết định vào `docs/DECISIONS.md`.
9. Sau freeze mới được mở final test đúng một lần.

## 10. File nên đọc tiếp

- `docs/EXPERIMENT_PROTOCOL.md`
- `docs/CANDIDATE_REVIEW.md`
- `docs/DECISIONS.md`
- `docs/ARCHITECTURE.md`
- `docs/history/2026-10.md`

Nếu handoff khác code/git, tin code + test + git và sửa lại handoff.
