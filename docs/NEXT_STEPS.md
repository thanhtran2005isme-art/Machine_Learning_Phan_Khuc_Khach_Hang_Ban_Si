# Next Steps — Sau Gate 6 (2026-10-08)

## Đã hoàn thành

- Gate 3/4: baseline, K-Means, stability, profiling và review.
- Gate 5: D011 chọn `log1p_standardscaler`, K=2, seed42; `models/selection.json` là frozen config cuối. Refit development 352, test 88 đánh giá đúng một lần, `models/final_evaluation.json` COMPLETE; serving artifacts `models/model.json`/`model.joblib` bất biến.
- Gate 6: Fastify API đọc frozen JSON, React 3 màn hình, production smoke và GitHub CI PASS; `run.bat` chạy cả hai app.
- Lưu ý `models/selection_frozen.json` K3 là lịch sử chọn sơ bộ đã rút **trước final test**; không dùng cho serving.

## Gate 7 (đang kiểm thử)

1. Browser E2E Playwright desktop + mobile, navigation, form happy/negative, dashboard, API outage.
2. Parity Python sklearn joblib ↔ Node JSON trên synthetic inputs, không đọc lại final test.
3. Audit npm dependencies và cập nhật khi đủ bằng chứng, sau đó full regression & CI.
4. Cập nhật Gate 7 evidence/handoff/history, bàn giao sau khi thực tế PASS.

## Sau Gate 7

- Gate 8 final code audit: clean install, deploy readiness và kiểm thử thủ công Chrome Windows; báo cáo/slide để giai đoạn sau.
- Không chạy `ml:freeze`, `ml:finalize` hoặc thay D011 vì final test.
