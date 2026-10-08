# Next Steps — Sau Gate 6 (2026-10-08)

## Đã hoàn thành

- Gate 3/4: baseline, K-Means, stability, profiling và review.
- Gate 5: D011 chọn `log1p_standardscaler`, K=2, seed42; `models/selection.json` là frozen config cuối. Refit development 352, test 88 đánh giá đúng một lần, `models/final_evaluation.json` COMPLETE; serving artifacts `models/model.json`/`model.joblib` bất biến.
- Gate 6: Fastify API đọc frozen JSON, React 3 màn hình, production smoke và GitHub CI PASS; `run.bat` chạy cả hai app.
- Lưu ý `models/selection_frozen.json` K3 là lịch sử chọn sơ bộ đã rút **trước final test**; không dùng cho serving.

## Gate 7 — COMPLETE trong CI

- Python sklearn ↔ Node parity 1/1 PASS trên 6 synthetic vectors, không đọc lại final test.
- Playwright Chromium desktop và mobile emulation 18/18 PASS; happy/negative UI, API outage, dashboard, responsive.
- Audit dependencies sau nâng Vitest5: 0 vulnerabilities được npm báo; `package-lock.json` cập nhật có regression.
- Gate 6 và Gate 7 GitHub CI SUCCESS: `37789072881` và `37789072891`.
- Xem `docs/GATE7_VERIFICATION.md` để biết evidence và giới hạn (chưa manual Windows).

## Sau Gate 7

- Gate 8 final code audit: clean install, deploy readiness và kiểm thử thủ công Chrome Windows; báo cáo/slide để giai đoạn sau.
- Không chạy `ml:freeze`, `ml:finalize` hoặc thay D011 vì final test.

## Gate 8 — Windows CI đã nghiệm thu

- Windows Server 2025 run `37791339124` SUCCESS: clean `npm ci`, security audit 0, Gate6 regression, parity, Playwright 20/20, `run.bat --ci` HTTP health/API/web PASS.
- Bug async stale prediction đã sửa. `run.bat` siết version Node >=20 và dependencies consistency.
- Xem `docs/GATE8_VERIFICATION.md`; model K2 bất biến. Không làm report/slide.

## Bước tiếp theo nhỏ nhất

- Kiểm tra trực tiếp double-click `run.bat` và màn hình trên Windows10 của người dùng (CI Windows Server 2025 không thay thế).
- Sau nghiệm thu local, không cần mở rộng code ngoài scope Project 22 trừ khi tìm thấy lỗi mới.

## Gate 9.1 — Traceability complete

- Xem `docs/GATE9_1_REQUIREMENTS_MATRIX.md` (đọc theo trang đề 2–7) và bản máy đọc `docs/GATE9_1_REQUIREMENTS_MATRIX.csv`.
- Ma trận 88 mục: 43 PASS / 29 PARTIAL / 10 MISSING / 6 NOT REQUIRED. Không đổi trạng thái khi chưa có evidence mới.
- Tiếp theo: Gate 9.2 frozen-profile 352 development **predict-only**; không đọc test hay refit model.

## Gate 9.2 — COMPLETE: frozen K2 development profiles

- CI `37797274530` SUCCESS 8/8 tests; generated Git commit `74ddfb24` contains 6 validated profile CSVs and `profile_metadata.json`.
- Cluster 0: 162; cluster 1: 190; Channel/Region, medians and distance metrics verified against frozen D011, no fit/test read. See `docs/GATE9_2_FROZEN_PROFILE.md`.
- **Next Gate 9.3:** API expose profile/evidence with checksum validation; then Gate 9.4 charts/dashboard. No model retrain or final test.

## Gate 9.3 — Verified API implemented
- `GET /api/dashboard` now includes checksum-verified `final_profile`: cluster summary, sizes, six-variable median ratios, Channel/Region distribution, centroid distance/outlier metrics and provenance.
- Core Gate6 CI `37810418640` PASS (15 Node / 11 API tests / builds / smoke); see `docs/GATE9_3_API.md`.
- Next Gate9.4 UI: read these real arrays to build profile chart, cluster sizes, candidate K explorer and model card, plus desktop/mobile E2E.

## Gate 9.3 — COMPLETE, Windows CI verified

- New `final_profile` in `GET /api/dashboard`, backward-compatible; six CSV SHA256 checks on every read plus D011 provenance and semantic validation. 503 if missing/corrupt, segment endpoint independent.
- CI: Gate6 `37810673033` SUCCESS, Gate7 `37810673011` SUCCESS (22 Playwright), Windows `37810672975` SUCCESS (clean install, 22 E2E, real batch smoke).
- **Next: Gate 9.4 Frontend** — median/size/categorical/distance visualizations and candidate K explorer, consuming verified API only. No ML retrain.

## Gate 9.4 — COMPLETE / Frontend Dashboard

- Candidate K2–8/Raw vs Log1p explorer read-only; verified final K2 cluster-size, median ratio and exact raw median, Channel/Region distribution, centroid distances/outliers rendered from `GET /api/dashboard.final_profile`.
- Browser E2E **34/34 PASS** on Linux `37812066044` and Windows `37812066198`. Backend build/regression `37812065997` PASS. See `docs/GATE9_4_FRONTEND.md`.
- **Next Gate 9.5**: interpretation of monetary units/time of prediction, model/data card, complete API response example, limits and final outlier interpretation. Then **Gate 9.6**: requirement matrix re-audit and final cold reproducibility without using held-out final test.

## Gate 9.5 — COMPLETE, CI verified

- Data/model cards and complete sample API response, UCI m.u. monetary units, prediction timing and outlier/metric caveats in UI+API. See `docs/GATE9_5_INTERPRETATION.md`.
- Source-grounded API/UI assertions and browser tests all passed: Gate6 `37813391195`, Gate7 `37813391072` 40/40, Windows `37813391303` 40/40, batch startup, audit 0.
- Next Gate9.6: re-audit 88 requirement IDs, clean reproducibility without reading final test or replacing frozen artifacts; no report/slides yet.

## Gate 9.6 — CODE FREEZE CI VERIFIED

- 88 requirement snapshot updated (57/16/9/6): `docs/GATE9_6_REQUIREMENTS_MATRIX.md`.
- Train/validation cold rerun on Linux/Windows: 140 runs + 630 ARI, match frozen evidence, no test use (CI `37816077339`). All source regression gates `37816077328`, `37816077510`, `37816077345` SUCCESS, Windows 40/40 browser.
- 503 model path disclosure fixed. Model artifacts unchanged; release snapshot to be pinned after final docs commit.
- Remaining outside feature build: manual Windows10 verification, journal/group attribution, report/slides, course slide bibliography. Follow `docs/GATE9_6_FINAL.md`.
