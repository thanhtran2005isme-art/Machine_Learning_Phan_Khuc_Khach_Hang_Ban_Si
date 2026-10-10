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

## Gate 9.6 — FINAL CODE CI VERIFIED

- Cold Linux/Windows `37816077339`: raw UCI SHA, train/val frozen 264/88 SHA, original 140-run grid & 630 ARI pairs + 14 candidate review reproduced in temp; no test.csv, no frozen model change. Fixed Python Windows cp1252 console via UTF-8 CI env.
- Gate6 `37816077328`: 15 Node, 14 Fastify, build/smoke, audit0. Gate7 `37816077510`: 40 E2E Linux. Gate8 `37816077345`: 40 E2E Windows, clean install, batch smoke, audit0.
- API 503 no longer leaks internal model-loading paths; added regression.
- Gate9.6 matrix `docs/GATE9_6_REQUIREMENTS_MATRIX.csv` + MD = **57 PASS /16 PARTIAL /9 MISSING /6 NOT REQUIRED**, includes deferred report/slides/team evidence honestly. [Final acceptance](GATE9_6_FINAL.md).
- Stop adding features; next manual Windows10 demonstration + real group evidence/reports, when user requests. NEVER rerun final holdout/refit D011.


## Gate 10.1 - feature branch CI verified (not merged)
- Experimental read-only evidence detail, seed variability, descriptive outliers, customer explanation, CSV/browser PDF print and teaching Lloyd panel. See docs/GATE10_1_ANALYSIS.md.
- Do not claim these changes are on main until PR merged. Gate 10.1 CI 38020099636 SUCCESS: 15 native + 14 API tests; 46 Playwright desktop/mobile; build, security audit and Python-Node parity PASS at code SHA 43e808fe. PCA/Hierarchical deferred to development-only offline evidence gate.

## Gate 10.2 — PCA 2D và Hierarchical Ward (feature PR #1)
- Offline Python ml/src/development_extension.py: 352 development, frozen mean/scale, PCA(2D) và Ward K2 6D, không refit KMeans, không đọc final test.
- CI offline 38037496861 PASS; verified analysis.json 352 điểm commit data fb7ebf11. PC1=0.44926644, PC2=0.26999868; KMeans silhouette 0.28915821, Ward 0.26262047, ARI 0.68724883, sizes KMeans 162/190 Ward 194/158.
- Read-only API GET /api/development-extension + strict SHA/source/count/ARI validation, React dashboard toggles colors and development split, no fake points.
- Feature branch feat/gate10-analysis-explain-export, PR #1 still not merged. Linux/Windows PR CI jobs must be checked before merge. Frozen model/selection/test and final_profile unchanged.
- Full method + command: docs/GATE10_2_PCA_HIERARCHICAL.md.


## Gate 10.3 — UI refresh on feature PR #1 (CI latest status must be verified)
- Updated frontend App.tsx, index.css, AnalysisExtensions.tsx, DevelopmentAnalytics.tsx, added E2E UX/responsive/screenshot tests. Desktop sidebar, mobile nav, verified frozen model status, customer form completion and comparison bars, PCA point selection, dashboard jump anchors. All data from API; no new dependencies.
- Screenshots from test browser written as GitHub Actions artifacts. See docs/GATE10_3_UI_UX.md for scope and manual UI review checklist.
- Feature branch only (not main); Gate10 GitHub Actions latest run must be inspected before marking PASS. No ML/backend/frozen data touched in this gate.
