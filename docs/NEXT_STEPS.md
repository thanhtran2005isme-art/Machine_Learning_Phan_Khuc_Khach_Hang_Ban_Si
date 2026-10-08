# Next Steps — Sau Gate 5 Selection Freeze

- Đã freeze D011: `log1p_standardscaler`, K=3, seed=42, `n_init=10`, `max_iter=300`, `algorithm=lloyd` trên sáu biến chi tiêu; xem `docs/GATE5_SELECTION.md` và `models/selection_frozen.json`.
- Quyết định dựa trên train/validation; **final test chưa đọc**, fitted model chưa có. Gate 5 chưa thể xác nhận PASS end-to-end vì runtime local Codex đã hết hiệu lực.
- Khi local hoạt động lại, kiểm tra `git status --short --branch`, `git pull --ff-only origin main` khi working tree sạch, `python -m pytest ml/tests -q`.
- Validate config; refit **train+validation**; hoàn tất output và metadata. Chỉ **sau đó** mới đánh giá final test đúng một lần. Không dùng test để sửa config.
- Xuất fitted model/pipeline và JSON provenance; test load/predict, đối chiếu centroid, cluster profiling gắn đúng cluster ID cuối.
- Viết báo cáo final test, cập nhật `docs/AI_HANDOFF.md` và `docs/history/2026-10.md`, kiểm tra commit/push. BE/FE chỉ thực hiện tại gate sau.
