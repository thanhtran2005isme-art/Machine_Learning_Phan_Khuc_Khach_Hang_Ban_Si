# AI HANDOFF — trạng thái hiện tại

> Cập nhật: 2026-10-04  
> Branch: `main`  
> EDA implementation commit: `5a64acb075b065c61bb547f02a88e599a452e1a6`

## 1. Mục tiêu hiện tại

Skeleton + data pipeline đã hoạt động. Gate B đã PASS bằng log chạy thật. Backend/frontend runtime đã chạy local đúng thiết kế nhưng Gate C còn thiếu log `npm run test:backend` và `npm run build`.

**Pipeline EDA train-only đã được dựng trong code, nhưng chưa được phép ghi PASS cho đến khi người dùng pull và chạy thật.** K-Means chưa bắt đầu.

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

### EDA train-only — đã dựng, chờ chạy local

Commit: `5a64acb075b065c61bb547f02a88e599a452e1a6` (`feat(ml): add train-only EDA pipeline`).

File chính:

- `ml/src/eda.py`
- `ml/tests/test_eda.py`
- `ml/src/data_paths.py`
- `docs/EDA.md`
- `package.json` có script `eda:train`.

EDA chỉ dùng 6 biến chi tiêu và mặc định chỉ đọc:

```text
data/processed/train.csv
```

Artifact dự kiến:

```text
reports/data/eda/
  train_summary_raw.csv
  train_summary_log1p.csv
  train_skewness.csv
  train_iqr_outliers.csv
  preprocessing_comparison.csv
  eda_metadata.json

reports/figures/eda/
  train_distributions_raw.png
  train_distributions_log1p.png
  train_boxplots_raw.png
  train_boxplots_log1p.png
  train_correlation_raw.png
  train_correlation_log1p.png
```

EDA hiện chỉ so sánh raw với `log1p`, báo cáo skewness/median/IQR/outlier/correlation. **Chưa fit StandardScaler và chưa chạy K-Means.**

## 4. Kiểm chứng local đã có bằng chứng thật

### Gate B — DATA ✅ PASS

Windows 10 `10.0.19045.6456`.

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

### Gate C — runtime skeleton ✅ một phần

Đã có log thật:

```text
GET /api/health -> status=ok, modelReady=false
GET /api/model-info -> status=not_ready
npm run dev:frontend -> Vite ready at http://localhost:5173/
```

Còn thiếu log thật:

```powershell
npm run test:backend
npm run build
```

### EDA — ⏳ code đã dựng, chưa kiểm chứng local

Chưa có output thật cho:

```powershell
python ml/src/eda.py
python -m pytest ml/tests -q
```

Do đó chưa được ghi EDA PASS và chưa được kết luận dữ liệu có mức skewness nào.

## 5. Ràng buộc học thuật phải giữ

- Feature chính: 6 biến chi tiêu.
- `Channel`/`Region`: profiling only.
- Split trước preprocessing.
- Test giữ độc lập, không dùng chọn K/tham số.
- Outlier chỉ báo cáo, chưa tự động xóa/winsorize.
- EDA ra quyết định trên train; validation/test không dùng ở bước này.
- `log1p` được mô tả trên train; `StandardScaler` chỉ fit trong bước thí nghiệm đúng phạm vi train.
- Không chọn K từ EDA.

## 6. Chưa làm

- Chạy/kiểm chứng EDA thật trên 264 dòng train.
- Đóng băng thiết kế baseline/thí nghiệm.
- Baseline không clustering và K=2.
- Raw vs `log1p + StandardScaler` trong thí nghiệm K-Means.
- K=2..8, stability >=10 seed.
- Chọn K bằng validation.
- Final independent test.
- Export serving artifact.
- `POST /api/segment`.
- Dashboard/model card hoàn chỉnh.

## 7. Bước tiếp theo

1. `git pull origin main`.
2. Chạy `npm run test:backend` và `npm run build`; lưu output thật.
3. Chạy `python ml/src/eda.py` hoặc `npm run eda:train`.
4. Chạy `python -m pytest ml/tests -q` và lưu số test PASS thật.
5. Kiểm tra các bảng/hình trong `reports/data/eda` và `reports/figures/eda`.
6. Chỉ sau khi EDA PASS mới diễn giải skewness/raw-vs-log1p và đóng băng kế hoạch thí nghiệm.
7. Sau đó mới làm baseline và K-Means.

## 8. File nên đọc tiếp

- `docs/EDA.md`
- `docs/NEXT_STEPS.md`
- `docs/ARCHITECTURE.md`
- `docs/DECISIONS.md`
- `data/README.md`
- `docs/history/2026-10.md`

Nếu handoff khác code/git, tin code + git và sửa lại handoff.
