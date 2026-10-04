# AI HANDOFF — trạng thái hiện tại

> Cập nhật: 2026-10-04  
> Branch: `main`  
> Repo HEAD trước khi ghi nhận Gate B: `9054074729ecfbba5722077c50515482e2a183be`

## 1. Mục tiêu hiện tại

Skeleton project + pipeline dữ liệu đã được dựng. **Gate B — dữ liệu đã PASS bằng log chạy thật trên Windows 10.** Tiếp theo cần hoàn tất Gate C cho Node/React, sau đó làm **EDA chỉ trên train**. Chưa bắt đầu K-Means.

## 2. Stack đã chốt

- Frontend: React + TypeScript + Vite.
- Backend: Node.js + TypeScript + Fastify + Zod.
- ML: Python + pandas + NumPy + scikit-learn.
- Test: Vitest cho backend, pytest cho ML/data.
- Node yêu cầu `>=20` theo `package.json`.

## 3. Đã hoàn thành trong code

- Root npm workspace cho `frontend` và `backend`.
- React/Vite skeleton.
- Fastify backend skeleton.
- `GET /api/health` trả `modelReady: false`.
- `GET /api/model-info` trả 503 `not_ready` trước khi model được đóng băng.
- Backend skeleton tests đã được viết.
- Python scripts cho download/audit/split/prepare data.
- Data README + data dictionary.
- Kiểm tra schema/domain, missing, finite, negative values và outlier report.
- Split mặc định 60/20/20, seed 42, trước preprocessing học từ dữ liệu.
- Unit tests cho data validation/split.
- Raw/processed data sinh tự động không commit; `reports/` và `models/` được phép track artifact cuối.

## 4. Kiểm chứng local đã có bằng chứng thật

### Gate B — DATA: PASS

Máy chạy: Windows 10 (`10.0.19045.6456`).

Lệnh đã chạy:

```powershell
python ml/src/prepare_data.py
python -m pytest ml/tests -q
```

Kết quả `prepare_data.py`:

```text
[download] Đã tải dữ liệu UCI thành công
SHA256: c3d018c643565b85cee733c4a2ac76dd76e080e857cb23f0ccfcc2e15a6c17ef
[audit] PASS: 440 dòng, 8 cột
[audit] Missing: 0
[audit] Duplicate rows: 0
[split] PASS: train=264, validation=88, test=88, seed=42
[split] Chưa fit scaler/log transform/model ở bước này.
[data pipeline] HOÀN TẤT
```

Kết quả pytest:

```text
....... [100%]
7 passed in 0.59s
```

Kết luận được phép ghi:

- raw dataset đúng 440 dòng, 8 cột;
- missing = 0;
- duplicate rows = 0;
- split đúng 264/88/88, seed 42;
- data pipeline chưa fit `log1p`, `StandardScaler` hoặc K-Means;
- 7 ML/data tests PASS.

Không suy diễn thêm các kết quả chưa xuất hiện trong log người dùng.

### Gate A — môi trường

- Python đủ khả năng chạy pipeline và pytest thực tế.
- Log cài venv/requirements không được lưu trong handoff hiện tại, nên không tuyên bố toàn Gate A PASS chỉ từ bằng chứng trên.

### Gate C — web/backend skeleton: CHƯA KIỂM CHỨNG

Cần chạy:

```powershell
npm install
npm run test:backend
npm run build
```

Sau đó chạy backend/frontend và kiểm tra `/api/health`.

## 5. Gate cần đạt trước K-Means

### Gate A — môi trường

- Node/npm install thành công.
- Python venv và requirements cài thành công.

### Gate B — dữ liệu ✅ PASS

Đã có log thật xác nhận pipeline + pytest như mục 4.

### Gate C — web/backend skeleton

- Backend test PASS.
- Frontend/backend build PASS.
- Backend chạy local.
- Frontend chạy local.
- `/api/health` trả `status=ok`, `modelReady=false`.
- `/api/model-info` chưa khả dụng là hành vi đúng ở giai đoạn này.

## 6. Quyết định học thuật phải giữ

- Feature chính: 6 biến chi tiêu.
- `Channel`/`Region`: profiling only.
- Split trước preprocessing.
- Test giữ độc lập, chỉ dùng kết luận cuối.
- Outlier hiện chỉ báo cáo, chưa tự động xóa/winsorize.
- Tỷ lệ 60/20/20 là quyết định triển khai, không phải yêu cầu bắt buộc nguyên văn của đề.

## 7. Chưa làm có chủ đích

- EDA hoàn chỉnh trên train.
- Baseline thống kê/K=2.
- Thí nghiệm raw vs `log1p + StandardScaler`.
- K-Means K=2..8.
- Stability >=10 seed.
- Chọn K.
- Final independent test.
- Export serving artifact.
- `POST /api/segment`.
- Dashboard thực nghiệm/model card hoàn chỉnh.

## 8. Bước tiếp theo

1. Chạy `npm install`.
2. Chạy `npm run test:backend`.
3. Chạy `npm run build`.
4. Chạy backend + frontend, kiểm tra `/api/health` và giao diện skeleton.
5. Nếu Gate C PASS, cập nhật handoff/history bằng log thật.
6. Xây EDA **chỉ trên `data/processed/train.csv`**: distribution, skewness, median/IQR, outlier description, trước/sau `log1p`.
7. Đóng băng kế hoạch thí nghiệm trước khi nhìn test.
8. Sau đó mới bắt đầu baseline và K-Means.

## 9. File nên đọc tiếp

- `docs/NEXT_STEPS.md`
- `docs/ARCHITECTURE.md`
- `docs/DECISIONS.md`
- `data/README.md`
- `docs/history/2026-10.md`

## 10. Lệnh xem lịch sử gần nhất

```bash
git log --oneline -20
```

Nếu handoff khác với code/git, tin code + git và sửa lại handoff.
