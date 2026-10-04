# AI HANDOFF — trạng thái hiện tại

> Cập nhật: 2026-10-04  
> Branch: `main`  
> Trạng thái gần nhất: Gate B PASS; Gate C runtime đã được kiểm chứng một phần bằng log thật.

## 1. Mục tiêu hiện tại

Skeleton project + pipeline dữ liệu đã được dựng. **Gate B — dữ liệu đã PASS bằng log chạy thật trên Windows 10.** Backend và frontend skeleton cũng đã chạy local thành công; API health/model-info phản hồi đúng thiết kế. Còn thiếu bằng chứng `npm run test:backend` và `npm run build` trước khi đánh dấu toàn bộ Gate C PASS. Sau đó làm **EDA chỉ trên train**. Chưa bắt đầu K-Means.

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

Kết quả:

```text
[download] Đã tải dữ liệu UCI thành công
SHA256: c3d018c643565b85cee733c4a2ac76dd76e080e857cb23f0ccfcc2e15a6c17ef
[audit] PASS: 440 dòng, 8 cột
[audit] Missing: 0
[audit] Duplicate rows: 0
[split] PASS: train=264, validation=88, test=88, seed=42
[split] Chưa fit scaler/log transform/model ở bước này.
[data pipeline] HOÀN TẤT
....... [100%]
7 passed in 0.59s
```

Kết luận: Gate B PASS; chưa fit `log1p`, `StandardScaler` hoặc K-Means.

### Gate C — runtime skeleton: PASS một phần

Bằng chứng terminal người dùng:

```text
curl http://127.0.0.1:3001/api/health
{"status":"ok","service":"wholesale-customer-segmentation-api","modelReady":false}

curl http://127.0.0.1:3001/api/model-info
{"status":"not_ready","message":"Mô hình chưa được huấn luyện. Hoàn tất pipeline dữ liệu và thí nghiệm K-Means trước."}

npm run dev:frontend
VITE v6.4.3 ready
Local: http://localhost:5173/
```

Được phép kết luận:

- backend đang chạy local và `/api/health` phản hồi đúng;
- `modelReady=false` đúng thiết kế;
- `/api/model-info` chưa sẵn sàng đúng thiết kế trước khi huấn luyện model;
- frontend Vite đã khởi động thành công tại `http://localhost:5173/`.

**Chưa được đánh dấu toàn bộ Gate C PASS** vì chưa có log thật cho:

```powershell
npm run test:backend
npm run build
```

### Gate A — môi trường

- Python đủ khả năng chạy pipeline và pytest thực tế.
- Node/Vite/Fastify đủ khả năng chạy runtime local thực tế.
- Không suy diễn thêm các bước cài môi trường không có log lưu lại.

## 5. Gate cần đạt trước K-Means

### Gate A — môi trường

Môi trường Python/Node đã đủ để chạy pipeline và runtime; lưu log cài đặt chỉ khi cần audit chi tiết.

### Gate B — dữ liệu ✅ PASS

Đã có log thật xác nhận pipeline + pytest.

### Gate C — web/backend skeleton ⏳ CÒN 2 KIỂM TRA

Đã xác nhận:

- backend chạy local ✅
- frontend chạy local ✅
- `/api/health` đúng ✅
- `/api/model-info` đúng trạng thái chưa có model ✅

Còn cần:

- `npm run test:backend` PASS;
- `npm run build` PASS.

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

1. Chạy `npm run test:backend`.
2. Chạy `npm run build`.
3. Nếu cả hai PASS, đánh dấu Gate C hoàn tất.
4. Xây EDA **chỉ trên `data/processed/train.csv`**: distribution, skewness, median/IQR, outlier description, trước/sau `log1p`.
5. Đóng băng kế hoạch thí nghiệm trước khi nhìn test.
6. Sau đó mới bắt đầu baseline và K-Means.

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
