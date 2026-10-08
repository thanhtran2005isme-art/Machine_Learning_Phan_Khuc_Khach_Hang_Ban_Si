# Gate 6 — Frozen model serving và React web

**Source baseline:** Gate 5 D011 `models/selection.json`: `log1p_standardscaler`, K=2. Serving JSON `models/model.json`; checksum lưu `models/final_evaluation.json` (COMPLETE). Không gọi `ml:freeze` hoặc `ml:finalize`.

## Khởi chạy

```powershell
npm ci
npm run test:serving
npm run test:backend
npm run build
npm run dev:backend
# Terminal khác
npm run dev:frontend
```

Mở http://localhost:5173 (Vite proxy đến http://127.0.0.1:3001). Không yêu cầu database hoặc Python runtime trong serving.

## API

- `GET /api/health`: 200, `status: "ok"`, `modelReady: boolean`.
- `GET /api/model-info`: 200 (K, preprocessing, artifact SHA, reference ranges 264 train samples, 2 median profiles, limitations); 503 khi artifact thiếu/hỏng.
- `GET /api/dashboard`: 200 (14 experiment rows, training/final evaluation metadata, profiles); 503 khi evidence hỏng.
- `POST /api/segment`: body phải là JSON object **chỉ** có sáu trường số hữu hạn, không âm, theo tên `Fresh, Milk, Grocery, Frozen, Detergents_Paper, Delicassen`. Ví dụ:

```json
{"Fresh":6410.5,"Milk":7226,"Grocery":10842.5,"Frozen":1153,"Detergents_Paper":4084.5,"Delicassen":1508.5}
```

Response 200 gồm `cluster_id`, `distance_to_centroid`, `distances_to_centroids`, `profile` (median chi tiêu đơn vị gốc), `warnings`, `distance_space`. Không trả xác suất vì K-Means không dự đoán xác suất. Input sai trả 400 `invalid_input`; model thiếu/hỏng trả 503 `not_ready`. Không âm thầm điền, clip hay ép kiểu dữ liệu sai.

## Chống leakage & integrity

- Chỉ đọc model JSON, selection và evaluation metadata + evidence experiment/EDA; **không đọc `data/processed/test.csv`**.
- Verify SHA256 model bytes theo frozen evaluation và kiểm tra model metadata K2/D011. Nếu mismatch: fail closed, `modelReady=false`.
- Inference: per feature `(log1p(x) - scaler_mean)/scaler_scale`, squared Euclidean tới 2 centroids; chỉ số nhỏ nhất thắng tie.
- Warnings nếu ngoài min/max **của 264 mẫu train EDA** (không phải absolute domain của toàn bộ dataset). Vẫn dự đoán, không đổi input.
- Các biểu đồ inertia phải so sánh *trong cùng preprocessing*, không so magnitude giữa raw và logscale.

## Test & nghiệm thu

- `npm run test:serving`: node built-in tests cho checksum, independent distance, bad inputs và dashboard data.
- `npm run test:backend`: Fastify injection happy path, strict validation, thiếu model, JSON metadata và 14 runs.
- `npm run build`: TypeScript backend/frontend và Vite.
- Manual E2E: nhập 6 số → API → cluster/profile; thử thiếu 1 số, âm, sai kiểu, cực lớn; thử tắt backend; xem dashboard chart/profile.
- Không tuyên bố PASS cho môi trường nào chưa có log. Không được mở lại final test để phục vụ Gate 6.
