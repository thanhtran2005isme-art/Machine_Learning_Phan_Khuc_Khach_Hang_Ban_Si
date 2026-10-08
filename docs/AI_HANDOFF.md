# AI HANDOFF — Project 22

> Cập nhật: 2026-10-08. Branch: `main`. Gate 5 đã COMPLETE, Gate 6 đã triển khai source trên GitHub; Gate 6 CI hoàn chỉnh PASS: GitHub Actions run 37777406114 (5 Node-native tests, 9 Fastify injection tests, TypeScript/Vite build, production HTTP smoke).

## Phạm vi và nguồn sự thật

- UCI Wholesale Customers 440 dòng; train 264, validation 88, final test 88.
- Chỉ sáu biến chi tiêu: Fresh, Milk, Grocery, Frozen, Detergents_Paper, Delicassen; Channel/Region chỉ dùng profiling.
- D010: 140 runs (raw/log1p_standardscaler × K2..8 × 10 seed) và 630 ARI comparisons; Gate 4 đã có kiểm chứng độc lập (xem GATE4_VERIFICATION).
- D011: chọn `log1p_standardscaler`, K=2, seed42, n_init10, max_iter300, lloyd trên train/validation; refit 352 development; final test 88 mẫu đánh giá đúng một lần.
- Final test: silhouette 0.238890, inertia/row 4.505144, cụm 45/43. `models/final_evaluation.json` trạng thái COMPLETE. **Không chạy lại final evaluation** hoặc thay đổi freeze config.
- `models/selection.json` / `models/model.json` / `models/model.joblib` là các artifact canonical. `models/selection_frozen.json` K=3 là bản freeze sơ bộ đã rút trước test, lưu lịch sử; không được dùng serving.

## Gate 6 — Source triển khai

- `backend/model.mjs` đọc model.json lúc khởi động, kiểm tra SHA256 và trạng thái freeze/evaluation, tính log1p → scaled Euclidean → nearest K2 center; không train lại.
- `backend/src/app.ts`: `GET /api/health`, `GET /api/model-info`, `GET /api/dashboard`, `POST /api/segment`. Zod kiểm tra đúng sáu numeric không âm, strict body, HTTP 400 khi sai, 503 khi artifact unavailable.
- `frontend/src/App.tsx`: ba màn hình Giới thiệu, Phân khúc, Dashboard; dữ liệu lấy từ API thật, không tạo demo kết quả phân cụm giả.
- `backend/model.test.mjs`: test lõi suy luận với Node built-in test. `backend/src/app.test.ts`: Fastify injection tests.
- `docs/GATE6_SERVING.md` ghi API contract và lệnh kiểm thử.
- Model checksum và frozen evidence không bị thay đổi. Không đọc `data/processed/test.csv` trong Gate 6.

## Bằng chứng trước Gate 6

- Gate 5 local: Python tests 100 passed, backend tests 2 passed, frontend/backend build PASS (theo history trước).
- Gate 6: CI run 37777406114 PASS trên GitHub Actions Ubuntu/Node22: Node-native 5/5, Fastify 9/9, frontend/backend build, production HTTP smoke. Test checksum tampering PASS; LF/CRLF mismatch được xử lý mà không sửa artifact Gate 5.
- Current source ưu tiên hơn tài liệu nếu có mâu thuẫn; conflict merge K2/K3 trong AI_HANDOFF và DECISIONS đã được giải quyết ở Gate 6.

## Việc tiếp theo

1. Gate 6 CI đã PASS; kiểm tra thủ công browser E2E trên Windows nếu cần nghiệm thu giao diện.
2. Kiểm thử local bằng `npm ci`, `npm run test:backend`, `npm run test:serving`, `npm run build`.
3. Chạy backend `npm run dev:backend`, frontend `npm run dev:frontend`; kiểm thử luồng nhập đủ 6 feature → API → kết quả; negative paths.
4. Đối chiếu đại diện dự đoán Node/Python từ development fixture, không mở final test.
5. Nếu có lỗi phát hiện thì sửa và cập nhật handoff/history, không sửa frozen artifacts.


## Gate 7 — Đang triển khai (chưa xác nhận PASS)
- `e2e/customer-flow.spec.ts`: Playwright desktop/mobile web end-to-end.
- `backend/parity.test.mjs`, `ml/tests/gate7_parity_reference.py`: so sánh sklearn joblib ↔ Node JSON với dữ liệu synthetic.
- `.github/workflows/gate7.yml`: CI browser + parity + npm audit report; không train lại model, không đọc final test.
- Xem `docs/GATE7_VERIFICATION.md` và CI Gate7 trước khi kết luận.
