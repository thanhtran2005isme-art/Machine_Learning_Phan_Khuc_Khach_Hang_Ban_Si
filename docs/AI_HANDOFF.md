# AI HANDOFF — Project 22

<<<<<<< HEAD
> Cập nhật: 2026-10-08. Branch: `main`. **Gate 5 COMPLETE**; quyết định D011 và one-shot final test đã thực thi. Xem `docs/GATE5_MODEL_SELECTION.md`.

## Phạm vi
- UCI Wholesale Customers 440 dòng: train 264, validation 88, final test 88.
- Sáu biến fit: Fresh, Milk, Grocery, Frozen, Detergents_Paper, Delicassen. Channel và Region chỉ profiling, không là feature hay ground truth.
- ML Python/scikit-learn; backend Fastify và frontend React/Vite vẫn ở trạng thái skeleton, chưa tích hợp serving.
- Gate 4: 14 candidates (raw/log1p+scaler × K=2..8), 10 seed/candidate, tổng 140 runs và 630 ARI pairs; đã kiểm chứng độc lập. Chi tiết `docs/GATE4_VERIFICATION.md`.
=======
> Cập nhật: 2026-10-08. Branch: main. Gate 5 đã freeze **cấu hình lựa chọn** trên evidence train/validation; final test và model export chưa chạy.

## Phạm vi và kiến trúc
- Dataset UCI Wholesale Customers 440 dòng; split train=264, validation=88, final test=88.
- Chỉ sáu biến chi tiêu: Fresh, Milk, Grocery, Frozen, Detergents_Paper, Delicassen được fit.
- Channel và Region chỉ profiling sau fit; backend Fastify/TypeScript, frontend React/Vite chưa triển khai serving.
- D010: raw hoặc log1p_standardscaler; K=2..8; seed=42..51; n_init=10; max_iter=300; algorithm=lloyd.
- Baseline A thống kê train; baseline B raw K=2 seed=42.
- Scaler và K-Means chỉ fit trên train; validation chỉ transform/predict; **final test giữ kín**.
- Gate 5 chọn **log1p_standardscaler K=3 seed42**, n_init=10, max_iter=300, lloyd; frozen config `models/selection_frozen.json`; chưa final test/refit/export hay BE/FE.
>>>>>>> 7defe431a81af90ba3b971c30a771ee9a490052c

## Quyết định cuối và bằng chứng
- D011 chọn **log1p + StandardScaler, K=2**, random_state=42, n_init=10, max_iter=300, algorithm=lloyd.
- Train/validation trước freeze: silhouette trung bình 0.2756/0.3066, seed ARI trung bình 0.9970, size train 118/146, validation 46/42.
- K3 tạo ba nhóm rõ khi fit train nhưng refit 352 làm thay đổi phân hoạch: ARI train-fit vs refit K3=0.3343 so với K2=0.8893; K2 giữ hai nhóm thiên Grocery/Milk/Detergents và Fresh/Frozen.
- `models/selection.json` đã **FROZEN trước khi mở test**, SHA-256 `f256dc6a04a5a8eddb0fc854e940bda25a4276b86b184d6155c4cee2a1ed8c64`.
- Bản freeze K3 sơ bộ rút trước test: `models/selection_k3_retracted_pretest.json`, lưu để audit; không phải model cuối.

## Final test một lần — COMPLETE
- Chạy `python -m ml.src.finalize_model` **một lần**, exit 0. `models/final_evaluation.json`: `status=COMPLETE`, `test_evaluated_once=true`, `test_used_for_selection=false`.
- Mô hình cuối fit train+validation 352 dòng: silhouette **0.289158**, inertia/row **4.163875**; cụm 0/1 có **162/190** khách.
- Final test 88 dòng: silhouette **0.238890**, inertia/row **4.505144**, cụm 0/1 **45/43** (nhỏ nhất 48.86%). Test không tham gia fit/chọn cấu hình.
- `models/model.json` SHA-256 `5057db0e290c93043abe4add3abf440e64864dc8d187a8d0b22d18621acd3b28`.
- `models/model.joblib` SHA-256 `f2f7874807456e6fdbade0be4c1eb124a8245e922dbf5ca6f070a9e040f2c816`.
- Portable JSON prediction khớp sklearn trên development 352 và tại thời điểm đánh giá test. Checksum selection/model khớp biên bản. **Không chạy lại final evaluation**; trạng thái COMPLETE là kết quả cuối.

## Kiểm thử thực chạy (2026-10-08)
- Preflight: 14/14 evidence rows và review hợp lệ, checksum freeze khớp, 352 dòng development không trùng, portable inference khớp; chưa mở test ở bước này.
- `python -m pytest ml/tests -q` → **100 passed in 30.70s** (trước one-shot final test).
- `npm run build` → frontend + backend PASS.
- `npm run test:backend` → **2 passed**; backend `/api/model-info` vẫn là placeholder 503 như thiết kế.
- Kiểm tra artifact sau final: PASS (checksum và suy luận trên development); lần in tên profile tiếng Việt từ script kiểm tra tạm bị `UnicodeEncodeError` do terminal cp1252, chạy lại dạng escaped ASCII PASS. Không phải lỗi model.

<<<<<<< HEAD
## Giới hạn và nguyên tắc bất biến
- Test silhouette 0.2389 được báo cáo độc lập; không dùng để chọn lại K/seed, thay preprocessing hoặc điều chỉnh model.
- KMeans không có ground-truth labels; silhouette/ARI chỉ mô tả cấu trúc và độ ổn định, chưa chứng minh tăng doanh thu.
- Không so inertia giữa raw và log+scaled; không xóa outlier; không sử dụng Channel/Region để fit hay chọn K.
- `selection.json`, `final_evaluation.json` và model artifacts là frozen evidence; không ghi đè, không re-run final test. Nếu gặp `CLAIMED`, điều tra trước bất kỳ hành động nào.

## 4 bước tiếp theo
1. Giữ artifact Gate 5, không chạy lại `ml:freeze`/`ml:finalize`.
2. Khi bắt đầu Gate 6, thiết kế contract JSON → Node.js inference cho đúng 6 biến, thứ tự log1p/scale/nearest center.
3. Viết integration tests Node đối chiếu Python portable predictions trên synthetic/development examples, validation Zod và thông báo lỗi input.
4. Chỉ sau khi Gate 6 được giao mới tích hợp API/UI và kiểm thử luồng sử dụng; chưa thực hiện trong Gate 5.
=======
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
>>>>>>> 7defe431a81af90ba3b971c30a771ee9a490052c
