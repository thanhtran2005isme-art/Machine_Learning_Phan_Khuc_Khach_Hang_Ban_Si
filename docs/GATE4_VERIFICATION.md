# Gate 4 — Independent verification (2026-10-08)

**Kết quả: PASS trong phạm vi stability, review và profiling.** Chưa chọn K, chưa freeze, chưa đọc final test, chưa thay đổi BE/FE. Protocol D010 giữ nguyên.

## Regression và isolation

- `python -m pytest ml/tests -q` → **96 passed in 31.47s** (lần cuối).
- Integration test chạy `run_experiments()` với output nằm trong thư mục tạm, guard giới hạn `load_split` chỉ `train.csv` và `validation.csv`, đồng thời từ chối pandas đọc `test.csv`. Kết quả: đúng 140 runs, 630 ARI pairs và metadata `test_used=false`, `selection_status=NOT_SELECTED`.
- `python ml/src/experiments.py` → thành công, 140 runs; `python ml/src/review_experiments.py` → thành công, đủ 14 candidates. So sánh SHA-256 trước/sau trên **11 CSV/PNG/Markdown**: **0 file đổi**.
- Ba lệnh `profile_candidate.py` (raw K=2, log1p_standardscaler K=2/K=3, seed=42) đều thành công. So sánh SHA-256 trước/sau trên **42 profile CSV/JSON/PNG**: **0 file đổi**.
- Cùng config fit 2 lần cho nhãn train/validation giống nhau và centroid đúng tolerance `rtol=atol=1e-12`.

## Đối chiếu độc lập

1. **Median:** tự tính `np.median` trực tiếp trên sáu biến chi tiêu gốc cho từng nhãn train/validation; so khớp `train_median_profile.csv` và `validation_median_profile.csv` (`atol=1e-7`). Count và share tổng đúng 264/88 và 1.0.
2. **Centroid:** với log branch, tự tính `expm1(centers * scaler.scale_ + scaler.mean_)` và so với `centroids_original_units.csv` (`rtol=1e-10`, `atol=1e-8`). Scaler mean/transform độc lập chỉ từ train; raw giữ nguyên đơn vị.
3. **Distance/outlier:** tự tính `sqrt(sum((X - centers[labels])**2))`, không dùng `model.transform`; đối chiếu mean, median, P90, P95, max, IQR threshold và outlier counts cho train/validation. Count/share/cluster gap và cờ `<5%` đúng CSV.
4. **Channel/Region:** kiểm tra frequency và within-cluster share bằng bảng chéo độc lập; hai trường chỉ xuất hiện hậu phân cụm.
5. **Biểu đồ:** tái dựng `median_ratio.png` và `cluster_sizes.png` từ CSV, so sánh từng pixel RGB với ba cặp PNG có sẵn: trùng khớp, không rỗng.
6. **Negative tests:** từ chối cột thiếu, giá trị chữ, NaN, Inf, giá trị âm; K/seed/n_init sai; nhãn không nguyên, âm, vượt K, sai chiều dài; distance input lỗi; metadata thiếu/hỏng/sai protocol; ARI pair thiếu/trùng/đảo, metric ngoài phạm vi. Validation evidence không cho phép NaN/Inf, min share đảo ngược.
7. **Reproducibility:** hash artifacts và trực tiếp so sánh fit như mô tả ở trên.
8. **Leakage:** thay đổi mạnh validation không thay đổi train labels, scaler train hoặc model centers. Test integration chỉ mở train/validation, output nằm trong thư mục tạm và metadata khẳng định chưa chọn/freeze.

## Kết quả shortlist thực tế

Metrics silhouette/ARI là trung bình của 10 seeds; counts/outliers/inertia concentration thuộc seed 42. `top 1% inertia` là phần tỷ trọng tổng bình phương khoảng cách do 1% điểm có khoảng cách lớn nhất đóng góp trên **train**, một phép đo độ nhạy outlier (không loại quan sát).

| Candidate | Train counts | Validation counts | Min train share | Max train/val share gap | Train distance-IQR outliers | Top 1% inertia | Sil. train/val | ARI mean |
|---|---|---|---:|---:|---:|---:|---|---:|
| raw K=2 | 217 / 47 | 81 / 7 | 17.80% | 9.85% | 23 | 25.33% | 0.4985 / 0.6103 | 1.0000 |
| log1p_standardscaler K=2 | 118 / 146 | 46 / 42 | 44.70% | 7.58% | 13 | 10.06% | 0.2756 / 0.3066 | 0.9970 |
| log1p_standardscaler K=3 | 91 / 73 / 100 | 40 / 24 / 24 | 27.65% | 10.98% | 8 | 10.43% | 0.2049 / 0.2165 | 0.9078 |

Không candidate nào trong ba profile có cụm train dưới 5%. Raw K=2 có silhouette cao nhưng top 1% điểm đóng góp hơn 1/4 inertia, cần xem cùng khả năng diễn giải và độ nhạy outlier. Ba candidate là **shortlist nghiên cứu**, chưa phải quyết định chọn K.

## Sửa lỗi Gate 4

- `ml/src/profile_candidate.py`: reject nhãn phân số/NaN/Inf/sai shape, nhãn âm hoặc vượt centroid range trong distance; validate chặt kiểu K, seed, n_init; validate ma trận distance hữu hạn.
- `ml/src/review_experiments.py`: reject min-cluster-share min > mean; kiểm tra metadata `max_iter`, seed count, data scope, profiling-only columns, scaler fit scope và preprocessing metadata.
- `ml/tests/test_gate4_independent.py`: bổ sung independent evidence tests, negative cases, deterministic PNG comparison, fit reproducibility và full grid leakage guard trong thư mục tạm.

Không xóa/clip outlier, không điều chỉnh config D010 để cải thiện metric, không đổi kiến trúc. Kiểm thử có một lần FAIL do test sai giả định về nhãn không liên tiếp; đã sửa test đúng theo trách nhiệm hàm và lần chạy cuối đạt 96 PASS.
