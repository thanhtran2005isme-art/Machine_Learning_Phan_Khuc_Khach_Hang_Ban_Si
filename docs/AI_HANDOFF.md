# AI HANDOFF — trạng thái hiện tại

> Cập nhật: 2026-10-05  
> Branch: `main`  
> EDA implementation commit: `5a64acb075b065c61bb547f02a88e599a452e1a6`

## 1. Mục tiêu hiện tại

Skeleton project, data pipeline, web/backend skeleton và EDA train-only đã được dựng và kiểm chứng bằng log chạy thật trên Windows 10. **Gate B PASS, Gate C PASS, EDA runtime PASS. K-Means chưa bắt đầu.**

Bước tiếp theo là đọc các artifact EDA thật, ghi nhận kết luận preprocessing dựa trên train, rồi đóng băng protocol thí nghiệm baseline + K-Means trước khi dùng validation/test.

## 2. Stack đã chốt

- Frontend: React + TypeScript + Vite.
- Backend: Node.js + TypeScript + Fastify + Zod.
- ML: Python + pandas + NumPy + scikit-learn + matplotlib.
- Test: Vitest cho backend, pytest cho ML/data.
- Node yêu cầu `>=20` theo `package.json`.

## 3. Đã hoàn thành trong code

### Foundation / data

- Root npm workspace cho `frontend` và `backend`.
- React/Vite skeleton.
- Fastify backend skeleton.
- `GET /api/health` trả `modelReady: false`.
- `GET /api/model-info` trả 503 `not_ready` trước khi model được đóng băng.
- Python download/audit/split/prepare data.
- Data README + data dictionary.
- Split 60/20/20, seed 42, trước preprocessing học từ dữ liệu.
- Unit tests data validation/split.

### EDA train-only

Commit code: `5a64acb075b065c61bb547f02a88e599a452e1a6` (`feat(ml): add train-only EDA pipeline`).

File chính:

- `ml/src/eda.py`
- `ml/tests/test_eda.py`
- `ml/src/data_paths.py`
- `docs/EDA.md`
- `package.json` có script `eda:train`.

EDA mặc định chỉ đọc `data/processed/train.csv`, chỉ dùng 6 biến chi tiêu và sinh artifact dưới:

```text
reports/data/eda/
reports/figures/eda/
```

EDA hiện so sánh raw với `log1p`, báo cáo skewness/median/IQR/outlier/correlation. **Chưa fit StandardScaler và chưa chạy K-Means.**

## 4. Kiểm chứng local đã có bằng chứng thật

### Gate B — DATA ✅ PASS

```text
python ml/src/prepare_data.py
[audit] PASS: 440 dòng, 8 cột
[audit] Missing: 0
[audit] Duplicate rows: 0
[split] PASS: train=264, validation=88, test=88, seed=42

python -m pytest ml/tests -q
....... [100%]
7 passed in 0.59s
```

Raw SHA256:

```text
c3d018c643565b85cee733c4a2ac76dd76e080e857cb23f0ccfcc2e15a6c17ef
```

### Gate C — web/backend skeleton ✅ PASS

Runtime đã xác nhận:

```text
GET /api/health -> 200, status=ok, modelReady=false
GET /api/model-info -> 503, status=not_ready
npm run dev:frontend -> Vite ready at http://localhost:5173/
```

Test/build đã xác nhận ngày 2026-10-05:

```text
npm run test:backend
Test Files  1 passed (1)
Tests       2 passed (2)

npm run build
frontend: tsc --noEmit && vite build -> PASS
backend: tsc -p tsconfig.json -> PASS
```

Kết luận: Gate C PASS đầy đủ.

### EDA train-only ✅ PASS runtime

```text
python ml/src/eda.py
[eda] Scope: TRAIN ONLY — 264 dòng
[eda] Features: Fresh, Milk, Grocery, Frozen, Detergents_Paper, Delicassen
[eda] Chưa fit StandardScaler, chưa chạy K-Means, không dùng validation/test để ra quyết định.

python -m pytest ml/tests -q
........... [100%]
11 passed in 7.72s
```

EDA đã sinh bảng/hình local. **Chưa được ghi kết luận định lượng về skewness, outlier hay correlation vào handoff cho đến khi đọc artifact EDA thật.**

## 5. Ràng buộc học thuật phải giữ

- Feature chính: 6 biến chi tiêu.
- `Channel`/`Region`: profiling only.
- Split trước preprocessing.
- Test giữ độc lập, không dùng chọn K/tham số.
- Outlier chỉ báo cáo, chưa tự động xóa/winsorize.
- EDA ra quyết định trên train; validation/test không dùng ở bước này.
- `StandardScaler` chỉ fit trong pipeline thí nghiệm đúng phạm vi train.
- Không chọn K từ EDA.
- Backend không train model ở request time.

## 6. Chưa làm

- Chưa đọc/ghi kết luận định lượng từ artifact EDA thật.
- Chưa đóng băng protocol baseline/thí nghiệm.
- Baseline không clustering.
- Baseline K=2.
- Raw vs `log1p + StandardScaler` trong thí nghiệm K-Means.
- K=2..8, stability >=10 seed.
- Chọn K bằng validation.
- Final independent test.
- Export serving artifact.
- `POST /api/segment`.
- Dashboard/model card hoàn chỉnh.

## 7. Bước tiếp theo

1. Đọc `reports/data/eda/train_skewness.csv`, `train_iqr_outliers.csv`, `preprocessing_comparison.csv` và các figure EDA.
2. Ghi kết luận EDA dựa trên train, không nhìn validation/test để quyết định preprocessing.
3. Nếu bằng chứng ủng hộ, chốt nhánh chính `log1p + StandardScaler`; vẫn giữ nhánh raw để thí nghiệm bắt buộc.
4. Đóng băng protocol: baseline A, baseline K=2, K=2..8, >=10 seed, inertia/silhouette/stability/cluster size/profile.
5. Viết code baseline/experiment.
6. Sau đó mới dùng validation để so sánh candidate; test tiếp tục khóa.

## 8. File nên đọc tiếp

- `docs/EDA.md`
- `docs/NEXT_STEPS.md`
- `docs/ARCHITECTURE.md`
- `docs/DECISIONS.md`
- `data/README.md`
- `docs/history/2026-10.md`

Nếu handoff khác code/git, tin code + test + git và sửa lại handoff.
