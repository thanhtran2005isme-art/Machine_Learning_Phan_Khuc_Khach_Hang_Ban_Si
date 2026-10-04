# AI HANDOFF — trạng thái hiện tại

> Cập nhật: 2026-10-04  
> Branch: `main`  
> Code baseline đã xác minh trước khi tạo bộ tài liệu continuity: `ed41b6a97a38b4f44cfe5ea61218831a6db0fac5`

## 1. Mục tiêu hiện tại

Hoàn tất **skeleton project + pipeline dữ liệu**, chạy kiểm tra local qua các gate, sau đó mới làm **EDA trên train**. Chưa bắt đầu K-Means cho đến khi data pipeline và skeleton web/backend được xác nhận chạy ổn.

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
- Unit tests cho data validation/split đã được viết.
- Raw/processed data sinh tự động không commit; `reports/` và `models/` được phép track artifact cuối.

## 4. Trạng thái kiểm chứng

Các test/command dưới đây **được yêu cầu chạy trên máy local nhưng chưa có log PASS được ghi vào handoff này**:

```powershell
npm install
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r ml/requirements.txt
python ml/src/prepare_data.py
python -m pytest ml/tests -q
npm run test:backend
npm run build
```

Không được ghi PASS cho các gate này cho đến khi có output thật.

## 5. Gate cần đạt trước K-Means

### Gate A — môi trường

- Node/npm install thành công.
- Python venv và requirements cài thành công.

### Gate B — dữ liệu

Cần xác nhận:

- raw đúng 440 dòng;
- đúng 8 cột kỳ vọng;
- không missing/NaN/inf;
- không chi tiêu âm;
- `Channel ∈ {1,2}`;
- `Region ∈ {1,2,3}`;
- train/validation/test không overlap;
- kích thước 264/88/88;
- manifest có seed/checksum;
- chưa fit scaler/K-Means trên full data.

### Gate C — web/backend skeleton

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

1. Pull `main` về máy local.
2. Chạy đầy đủ Gate A/B/C và lưu output thật.
3. Nếu lỗi, ghi nguyên nhân/cách sửa vào `TROUBLESHOOTING.md` và history.
4. Nếu PASS, cập nhật handoff + history với kết quả test.
5. Xây EDA **chỉ trên `train.csv`**: distribution, skewness, median/IQR, outlier description, trước/sau `log1p`.
6. Đóng băng kế hoạch thí nghiệm trước khi nhìn test.
7. Sau đó mới bắt đầu baseline và K-Means.

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
