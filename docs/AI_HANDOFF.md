# AI HANDOFF — Project 22

> Cập nhật: 2026-10-08. Branch: main. Gate 4 đang được kiểm chứng; xem kết quả mới nhất ở cuối file.

## Phạm vi và kiến trúc
- Dataset UCI Wholesale Customers 440 dòng; split train=264, validation=88, final test=88.
- Chỉ sáu biến chi tiêu: Fresh, Milk, Grocery, Frozen, Detergents_Paper, Delicassen được fit.
- Channel và Region chỉ profiling sau fit; backend Fastify/TypeScript, frontend React/Vite chưa triển khai serving.
- D010: raw hoặc log1p_standardscaler; K=2..8; seed=42..51; n_init=10; max_iter=300; algorithm=lloyd.
- Baseline A thống kê train; baseline B raw K=2 seed=42.
- Scaler và K-Means chỉ fit trên train; validation chỉ transform/predict; **final test giữ kín**.
- Chưa freeze/ chọn model cuối, chưa export serving artifact hay làm BE/FE.

## Giai đoạn trước có bằng chứng
- Gate B data audit PASS: 440 dòng, 8 cột, missing 0, duplicate 0; split 264/88/88.
- Gate C backend/frontend skeleton và build PASS theo log 2026-10-05.
- EDA train-only: cả sáu feature giảm absolute skewness sau log1p; vẫn giữ outlier.
- Có hai script experiment lịch sử: `ml/src/experiment.py` (Gate D trước merge) và `ml/src/experiments.py` (Gate 4 review). D010 là protocol chung, dùng script `experiments.py` cho review mới.
- Git HEAD trước Gate 4: `0aa99f9`. Các sửa Gate 4 đang ở working tree; không reset/pull đè thay đổi.

## Gate 4 — Stability, review và profiling
- Experiment: 14 candidate × 10 seed = 140 runs; mỗi candidate có 45 cặp ARI, tổng 630.
- `ml/src/experiments.py` sinh `runs.csv`, `aggregate.csv`, `stability.csv`, `stability_pairs.csv`, `selection_evidence.csv`, metadata và 4 PNG.
- `ml/src/review_experiments.py` xác minh evidence/metadata, tính ranking riêng theo silhouette, ARI, cluster share và train/validation gap; không gộp điểm/chọn K.
- `ml/src/profile_candidate.py` tính median đơn vị gốc, Channel/Region hậu phân cụm, centroid inverse-transform, distance/outlier IQR, train/validation share và CSV/JSON/2 PNG cho từng candidate.
- Shortlist chỉ phục vụ nghiên cứu tiếp; chưa là quyết định lựa chọn cuối.

## Kiểm chứng phiên hiện tại
- Đã chuẩn hóa 4 unit tests dùng preprocessing cũ `log1p_scale`.
- `python -m pytest ml/tests -q` → **30 passed in 20.90s** (trước các kiểm thử âm bổ sung).
- Đã bổ sung một số ràng buộc input/evidence/metadata và đồng bộ docs D010.
- Run experiment/review/profiling và negative tests: kiểm tra trạng thái thực tế ở báo cáo history mới nhất trước khi ghi PASS.

## Những điều cần duy trì
- Tuyệt đối không đọc `data/processed/test.csv` trong Gate 4.
- Không chọn K theo riêng silhouette; không so inertia khác preprocessing vì khác scale.
- Median chi tiêu đơn vị gốc là diễn giải chính; centroid chỉ tham khảo.
- Không freeze, không sửa backend/frontend trong Gate 4.

## Tiếp theo
1. Hoàn tất pytest, đặc biệt negative tests.
2. Xác nhận 140 runs, 630 cặp ARI bằng artifact thực tế; kiểm tra NaN/Inf và tính nhất quán.
3. Chạy review đủ 14 candidate, kiểm tra rankings và gaps.
4. Chọn shortlist 1–3 dựa trên train/validation evidence và profile từng candidate.
5. Kiểm tra CSV/JSON/PNG, inverse transform, distance, cluster share/outlier.
6. Ghi báo cáo Gate 4 và history; quyết định freeze chỉ ở gate tiếp theo.
