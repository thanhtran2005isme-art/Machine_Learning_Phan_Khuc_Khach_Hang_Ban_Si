# AI HANDOFF — Project 22

> Cập nhật: 2026-10-08. Branch: main. Gate 5 đã freeze **cấu hình lựa chọn** trên evidence train/validation; final test và model export chưa chạy.

## Phạm vi và kiến trúc
- Dataset UCI Wholesale Customers 440 dòng; split train=264, validation=88, final test=88.
- Chỉ sáu biến chi tiêu: Fresh, Milk, Grocery, Frozen, Detergents_Paper, Delicassen được fit.
- Channel và Region chỉ profiling sau fit; backend Fastify/TypeScript, frontend React/Vite chưa triển khai serving.
- D010: raw hoặc log1p_standardscaler; K=2..8; seed=42..51; n_init=10; max_iter=300; algorithm=lloyd.
- Baseline A thống kê train; baseline B raw K=2 seed=42.
- Scaler và K-Means chỉ fit trên train; validation chỉ transform/predict; **final test giữ kín**.
- Gate 5 chọn **log1p_standardscaler K=3 seed42**, n_init=10, max_iter=300, lloyd; frozen config `models/selection_frozen.json`; chưa final test/refit/export hay BE/FE.

## Giai đoạn trước có bằng chứng
- Gate B data audit PASS: 440 dòng, 8 cột, missing 0, duplicate 0; split 264/88/88.
- Gate C backend/frontend skeleton và build PASS theo log 2026-10-05.
- EDA train-only: cả sáu feature giảm absolute skewness sau log1p; vẫn giữ outlier.
- Có hai script experiment lịch sử: `ml/src/experiment.py` (Gate D trước merge) và `ml/src/experiments.py` (Gate 4 review). D010 là protocol chung, dùng script `experiments.py` cho review mới.
- Gate 4 trước phiên nghiệm thu: commit `bffb471`. Không reset/pull đè thay đổi.

## Gate 4 — Stability, review và profiling
- Experiment: 14 candidate × 10 seed = 140 runs; mỗi candidate có 45 cặp ARI, tổng 630.
- `ml/src/experiments.py` sinh `runs.csv`, `aggregate.csv`, `stability.csv`, `stability_pairs.csv`, `selection_evidence.csv`, metadata và 4 PNG.
- `ml/src/review_experiments.py` xác minh evidence/metadata, tính ranking riêng theo silhouette, ARI, cluster share và train/validation gap; không gộp điểm/chọn K.
- `ml/src/profile_candidate.py` tính median đơn vị gốc, Channel/Region hậu phân cụm, centroid inverse-transform, distance/outlier IQR, train/validation share và CSV/JSON/2 PNG cho từng candidate.
- Shortlist chỉ phục vụ nghiên cứu tiếp; chưa là quyết định lựa chọn cuối.

## Kiểm chứng Gate 4 cuối cùng (2026-10-08)
- `python -m pytest ml/tests -q` → **96 passed in 31.47s**.
- 140 K-Means runs, 14 candidate, 630 ARI pairs đủ/không trùng; review và 3 profile chạy thành công.
- Independent verification: median gốc, inverse centroid, Euclidean distance, IQR outliers, categorical shares, CSV/PNG pixel consistency, negative tests, metadata và leakage isolation.
- Tái chạy 11 experiment/review artifacts + 42 profile artifacts → hash SHA-256 không đổi.
- Shortlist nghiên cứu: raw K=2, log1p_standardscaler K=2 và K=3 (seed=42). Chưa chọn K cuối.
- Báo cáo và các con số chi tiết: `docs/GATE4_VERIFICATION.md`.

## Gate 5 — model selection (2026-10-08)

- D011 FROZEN: `log1p_standardscaler`, K=3, seed42, n_init10, max_iter300, lloyd.
- Silhouette train/validation=0.2049/0.2165, ARI mean/min=0.9078/0.7982. Clusters train=91/73/100, validation=40/24/24.
- Median gốc train/validation cho thấy ba nhóm Grocery/Detergents cao, chi tiêu thấp, Fresh/Frozen cao; xem `docs/GATE5_SELECTION.md`.
- Raw K2 và log K2 là đối chứng; K3 giữ tính diễn giải để đổi lấy giảm silhouette/ARI. Chỉ dùng 6 chi tiêu để quyết định.
- `models/selection_frozen.json` là **frozen selection config**, không phải fitted model artifact. Chưa chạy final test hay xuất model.

## Những điều cần duy trì
- Tuyệt đối không đọc `data/processed/test.csv` trong Gate 4.
- Không chọn K theo riêng silhouette; không so inertia khác preprocessing vì khác scale.
- Median chi tiêu đơn vị gốc là diễn giải chính; centroid chỉ tham khảo.
- Gate 4 lịch sử không freeze; Gate 5 đã freeze cấu hình tại D011. Không sửa backend/frontend.

## Tiếp theo
1. Khôi phục phiên Codex local, đối chiếu `git status` và `origin/main` trước khi chạy lệnh.
2. Validate frozen config và kiểm tra các test Gate 4, đảm bảo Gate 5 không làm thay đổi protocol đã dùng lựa chọn.
3. Refit pipeline đã freeze trên train+validation, không dùng test cho fit hay điều chỉnh.
4. Đánh giá final test **một lần duy nhất**; lưu metric, provenance và không điều chỉnh K/preprocessing sau khi xem test.
5. Xuất fitted model artifact kèm metadata/scaler/centroids/feature order, verify load và prediction reproducibility.
6. Ghi báo cáo test/export, cập nhật history/handoff và commit; BE/FE để gate sau.
