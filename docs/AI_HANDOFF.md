# AI HANDOFF — Project 22

> Cập nhật: 2026-10-08. Branch `main`. Gate 3–7 đã hoàn tất theo bằng chứng hiện có. Gate 7 GitHub CI `37789072891` SUCCESS; Gate 6 regression `37789072881` SUCCESS.

## Quy tắc bất biến

- ML UCI Wholesale Customers 440 dòng; split 264/88/88; sáu chi tiêu fit: Fresh, Milk, Grocery, Frozen, Detergents_Paper, Delicassen. Channel/Region chỉ profiling.
- D011: `log1p_standardscaler`, K=2, seed42, n_init10, max_iter300, Lloyd; chọn từ train/validation. Refit 352 development, final test 88 **đã đánh giá một lần**, silhouette 0.238890 và cụm 45/43.
- `models/selection.json`, `models/model.json`, `models/model.joblib`, `models/final_evaluation.json` là canonical frozen artifacts. Không thay đổi và không chạy lại `ml:freeze`/`ml:finalize`.
- Bản K3 lịch sử `models/selection_frozen.json` đã rút trước test; tuyệt đối không dùng cho serving.

## BE/FE hiện tại

- Fastify ở `backend/src/app.ts`: /api/health, /api/model-info, /api/dashboard, /api/segment. Core `backend/model.mjs` load JSON và xác minh SHA-256, strict six numeric input. Không train theo request.
- React ở `frontend/src/App.tsx`: ba màn hình Giới thiệu, Phân khúc và Dashboard; dữ liệu backend thật.
- `run.bat` ở root khởi chạy BE/FE trên Windows. Node >=20.
- Model checksum Gate 5 dùng Windows CRLF; verifier chấp nhận raw SHA hoặc chuẩn hóa chỉ LF → CRLF, reject thay đổi nội dung khác.

## Evidence gần nhất

- Gate 6 GitHub Actions `37789072881`: Node-native serving 5/5, Fastify 9/9, build + HTTP smoke PASS (sau Vitest5).
- Gate 7 GitHub Actions `37789072891`: Playwright desktop 9/9, mobile Chromium emulation 9/9; sklearn joblib vs Node portable parity 1/1 trên 6 synthetic examples; build PASS.
- `npm audit --audit-level=moderate` sau `npm ci`: PASS, npm báo 0 vulnerabilities. `backend/package.json` Vitest5 và `package-lock.json` đã nâng có kiểm chứng.
- Không mở lại final test hay sửa model files trong Gate 6/7. Xem `docs/GATE7_VERIFICATION.md` để biết chi tiết.

## Gate 8 — CI VERIFIED / PASS

- Windows Server 2025 GitHub Actions run `37791339124`: clean checkout, `npm ci`, 0 audit advisories, Gate 6 full regression, Python sklearn ↔ Node frozen artifact parity, 20/20 Chromium desktop/mobile emulated E2E PASS.
- `run.bat --ci`: API modelReady true, frontend HTTP 200, POST /api/segment hợp lệ. Bình thường `run.bat` vẫn mở hai cửa sổ cmd; đã thêm Node version guard và automatic npm ci khi deps cũ.
- React stale API response khi người dùng sửa/xóa input đã được sửa và có regression test.
- `docs/history/2026-10.md` đã được dọn conflict merge K2/K3; lưu lịch sử K3 pretest nhưng cấu hình duy nhất phục vụ inference vẫn D011 K2.
- Tất cả model artifacts Gate 5 không thay đổi. Không chạy lại final test.
- Chi tiết chứng cứ: `docs/GATE8_VERIFICATION.md`.

## Việc tiếp theo

1. Windows 10 máy thật của người dùng: `git pull --ff-only origin main`, `npm ci`, `npm run test:gate6`, double-click `run.bat`, thử 3 màn hình.
2. Nếu cần E2E trên máy Windows cá nhân, xem lệnh Playwright trong `docs/GATE8_VERIFICATION.md`.
3. Nếu không có lỗi thực tế, dừng phát triển code theo phạm vi hiện tại; không làm report/slide khi chưa được giao.

## Gate 9.1 — Requirements traceability audited
- Đề gốc Project 22 trang 2–7: 88 dòng yêu cầu đánh giá tại `docs/GATE9_1_REQUIREMENTS_MATRIX.md` + CSV; trạng thái: PASS 43, PARTIAL 29, MISSING 10, NOT REQUIRED 6.
- Chưa sửa frozen model/Backend/Frontend; không chạy lại final test. Backlog chức năng ưu tiên 9.2→9.6; báo cáo/slide/hồ sơ 2 người vẫn bắt buộc khi nộp nhưng đang hoãn.

## Gate 9.2 — Source added, CI pending
- `ml/src/final_profile.py`: read frozen model + 264 train/88 validation only, reject wrong SHA, predict-only final K2 352-profile.
- `ml/src/prepare_development_only.py`: build only train/validation from raw UCI on clean runner; no held-out test.csv created.
- `ml/tests/test_final_profile.py`: 8 tests (frozen sklearn parity, independent medians/channel/region, determinism, tamper/leakage/no-fit guards).
- `docs/GATE9_2_FROZEN_PROFILE.md`: specification and evidence. CI `.github/workflows/gate9-2-frozen-profile.yml` will commit verified profile CSV/JSON after PASS.
- Do not mark completed until workflow results; no change to models/.
