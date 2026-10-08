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

## Gate 9.2 — COMPLETE, CI verified
- `ml/src/final_profile.py`: read frozen model + 264 train/88 validation only, reject wrong SHA, predict-only final K2 352-profile.
- `ml/src/prepare_development_only.py`: build only train/validation from raw UCI on clean runner; no held-out test.csv created.
- `ml/tests/test_final_profile.py`: 8 tests (frozen sklearn parity, independent medians/channel/region, determinism, tamper/leakage/no-fit guards).
- `docs/GATE9_2_FROZEN_PROFILE.md`: specification and evidence. CI `.github/workflows/gate9-2-frozen-profile.yml` will commit verified profile CSV/JSON after PASS.
- GitHub Actions `37797274530` SUCCESS: 8/8 Python tests, 352 development sklearn/JSON parity, reproducibility SHA, category counts; no final test split and no fit.
- Derived outputs committed in `74ddfb24bc771e048c1c025e6591e692e9d3de53`: 6 CSV + profile_metadata.json in `reports/data/final_profile/`. Frozen models unchanged.
- Model K2 final cluster sizes **162/190**, Channel/Region totals 352, distance outliers IQR 5/11, inertia/row 4.163874729781235.
- **Next: Gate 9.3** API loads only verified profile files and exposes stable validated JSON contract, no profile retraining.

## Gate 9.3 — Backend verified final profile
- `backend/final-profile.mjs`: validate model D011 + selected metadata, SHA256 per CSV including LF/CRLF compatibility, CSV shape, summary/size/Channel/Region/ratio/distance consistency against frozen artifacts. Every dashboard request verifies files, no fit/train/test access.
- `GET /api/dashboard` backwards compatible with Gate 6, adds `final_profile`. Invalid files → 503; health/segment stay operational. See `docs/GATE9_3_API.md`.
- Gate9.3 final verification: Gate6 CI `37810673033` (15 Node / 11 API / build / smoke), Gate7 CI `37810673011` (22 Playwright), Windows CI `37810672975` (clean install, audit 0, parity, 22 E2E, batch HTTP) all SUCCESS.
- Next: Gate9.4 FE charts/table candidate explorer sourced only from verified API.

## Gate 9.4 — COMPLETE, verified on Linux + Windows
- React Dashboard now shows final K2 352 development cluster sizes, six-feature median ratios (and frozen raw medians), Channel and Region composition, P95/max centroid distance and IQR outlier count, all from verified `GET /api/dashboard.final_profile`.
- Experiment explorer browses K2–8 × Raw/Log1p, reveals train inertia/validation silhouette/ARI/min share **without changing frozen serving K2**.
- UI fails closed when profile is missing/invalid; data labels/tables accessible, responsive 320px. New E2E covers chart accuracy against API, explorer isolation, outage, mobile overflow.
- CI runs: Gate6 `37812065997` SUCCESS; Gate7 `37812066044` SUCCESS **34/34 E2E**; Windows Gate8 `37812066198` SUCCESS **34/34 E2E**, clean install, audit, batch smoke. No models/ or final_profile/ changes.
- [Technical acceptance details](GATE9_4_FRONTEND.md). Next: Gate 9.5 explanations/data+model card and 9.6 final requirements closure, no re-fit/test.

## Gate 9.5 — source-grounded interpretability COMPLETE (CI VERIFIED)
- Added `docs/DATA_CARD.md`, `docs/MODEL_CARD.md`, `docs/GATE9_5_API_EXAMPLES.md` and `docs/GATE9_5_INTERPRETATION.md`. Source UCI annual **monetary units (m.u.)**, no named currency, dataset DOI/license and raw checksum. Correct time of applicability only after 6 annual spending features are available.
- `GET /api/model-info` backwards-compatibly adds `data_card`/`model_card` based on frozen D011 metadata, selection rationale, conditions and safe-use limits. Intro, segment and dashboard now reflect cards/units from API.
- CI runs Gate6 `37813391195` SUCCESS (15 Node, 13 Fastify, TS/Vite build, HTTP smoke), Gate7 `37813391072` SUCCESS (40 E2E Linux), Windows `37813391303` SUCCESS (40 E2E Windows, clean install, npm audit 0, batch smoke). Frozen artifacts unchanged, no ML final test rerun.
- Historical K3 proposal doc now prominently superseded pre-test; old candidate paths historical only. Next Gate9.6: full 88-ID requirement evidence re-audit and cold reproducibility with zero final-test reevaluation.
