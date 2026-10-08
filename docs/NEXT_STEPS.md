# Next Steps — Sau Gate 5 (2026-10-08)

## Gate 5 đã đóng

- D011: `log1p_standardscaler`, K=2, seed=42; quyết định tại `models/selection.json`.
- Đã fit model trên train+validation (352 dòng), final test độc lập **một lần** 88 dòng; `models/final_evaluation.json` có `status=COMPLETE`.
- Model cho Gate 6: `models/model.json` (portable) và `models/model.joblib` (Python reference). Checksum trong `docs/GATE5_MODEL_SELECTION.md`.
- Đã PASS: ML 100 tests; frontend/backend build; backend 2 tests; artifact verification.

**Không chạy lại** `python -m ml.src.freeze_selection` hoặc `python -m ml.src.finalize_model`; kết quả đã frozen. Không chọn lại K hay tham số dựa trên final test.

## Gate 6 — Chỉ bắt đầu khi được giao

1. Xác định contract Node: 6 spending features đúng thứ tự, input hữu hạn, không âm.
2. Đọc `models/model.json`; suy luận `log1p → (x-mean)/scale → argmin squared Euclidean distance`; không train khi request.
3. Test Node vs Python portable trên development hoặc synthetic (không đánh giá lại final test), bao gồm input lỗi/biên và cấu hình mô hình.
4. Tích hợp route inference/model-info, Zod validation, sau đó frontend demo/dashboard.
5. Quality gates end-to-end; cập nhật kiến trúc, handoff và history khi triển khai.

Lý do lựa chọn Raw K2 / Log K2 / Log K3 và biên bản final test xem `docs/GATE5_MODEL_SELECTION.md`.
