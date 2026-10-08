> **LƯU TRỮ LỊCH SỬ — QUYẾT ĐỊNH K=3 DƯỚI ĐÂY ĐÃ RÚT TRƯỚC FINAL TEST. KHÔNG DÙNG ĐỂ SERVING.** Quyết định có hiệu lực là **D011 K=2 `log1p_standardscaler`**, đã freeze ở `models/selection.json`; minh chứng và lý do điều chỉnh tại [GATE5_MODEL_SELECTION.md](GATE5_MODEL_SELECTION.md) và [MODEL_CARD.md](MODEL_CARD.md). Nội dung còn lại giữ nguyên để truy vết quá trình trước test.

# Gate 5 — Model Selection (2026-10-08)

**Decision D011: FROZEN CONFIG — `log1p_standardscaler`, K=3, seed=42, n_init=10, max_iter=300, lloyd.** Đây là quyết định trên train/validation. Final test chưa được mở, final fit và model artifact chưa thực hiện.

## Evidence từ 140 runs / 630 ARI pairs

Các metric là trung bình theo 10 seed (42..51); cluster sizes, số IQR outlier và top 1% inertia lấy seed 42. Silhouette/ARI có thể đối chiếu như evidence, nhưng inertia raw và scaled không thể so trực tiếp.

| Evidence | Raw K=2 | Log1p+Scaler K=2 | Log1p+Scaler K=3 |
|---|---:|---:|---:|
| Silhouette train | 0.4985 | 0.2756 | 0.2049 |
| Silhouette validation | 0.6103 | 0.3066 | 0.2165 |
| Validation − train | +0.1118 | +0.0310 | +0.0116 |
| ARI mean | 1.0000 | 0.9970 | 0.9078 |
| ARI min | 1.0000 | 0.9848 | 0.7982 |
| Train cluster sizes | 217/47 | 118/146 | 91/73/100 |
| Validation cluster sizes | 81/7 | 46/42 | 40/24/24 |
| Max abs cluster share gap | 9.85 pp | 7.58 pp | 10.98 pp |
| IQR distance outliers (train) | 23 | 13 | 8 |
| Top 1% train inertia contribution | 25.33% | 10.06% | 10.43% |

Không có cluster train dưới 5% trong shortlist. K=3 có ARI thấp hơn và một số seed cho phân hoạch khác hơn (ARI min=0.7982), nhưng không tạo cụm quá nhỏ. K=2 log có silhouette tốt hơn khoảng 0.0901 và stability ổn định hơn.

## Median profile gốc: vì sao K=3 có ý nghĩa kinh doanh

Tất cả số là median của sáu biến chi tiêu **trong đơn vị gốc của dataset**. Không quy đổi thành doanh thu thực tế hay tiền tệ ngoài dataset.

| K=3 cluster | Split | N | Fresh | Milk | Grocery | Frozen | Detergents_Paper | Delicassen |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| 0 — Grocery/Detergents cao | Train | 91 | 5963 | 7184 | 11757 | 1031 | 4595 | 1468 |
| 0 — Grocery/Detergents cao | Validation | 40 | 5339.5 | 8652.5 | 12473 | 946 | 6207 | 915.5 |
| 1 — Chi tiêu thấp | Train | 73 | 6987 | 1042 | 1902 | 982 | 187 | 406 |
| 1 — Chi tiêu thấp | Validation | 24 | 5970 | 1246.5 | 1925.5 | 1274.5 | 263.5 | 344.5 |
| 2 — Fresh/Frozen cao | Train | 100 | 16293 | 2754 | 3271 | 4078 | 461 | 1140.5 |
| 2 — Fresh/Frozen cao | Validation | 24 | 13699.5 | 2401 | 2506 | 4521 | 396 | 1337.5 |

- **Cluster 0:** cao nổi bật về Grocery và Detergents_Paper trên cả hai split.
- **Cluster 1:** thấp ở Milk, Grocery, Frozen và Detergents_Paper trên cả hai split.
- **Cluster 2:** Fresh/Frozen vượt trội; Fresh median ~2.33× cluster 1 ở train và ~2.29× ở validation, Frozen ~4.15× / ~3.55×. Đây là khác biệt có thể dùng để thiết kế cách phục vụ khách sỉ theo danh mục hàng.
- Các profile cùng giữ hướng phân biệt giữa train và validation. Kích thước cluster 0/2 biến động khoảng 10–11 điểm phần trăm, cần theo dõi sau triển khai.

## Vì sao không chọn hai ứng viên K=2

- **Raw K=2:** ưu thế silhouette và ARI nhưng bị chi phối mạnh bởi quy mô chi tiêu; hai cluster lệch, nhóm nhỏ validation chỉ có 7 mẫu; 1% điểm xa nhất đóng góp 25.33% train inertia.
- **Log K=2:** rất ổn định, cân bằng và là baseline tốt. Tuy nhiên chỉ có hai nhóm đối lập về Grocery/Detergents; K=3 biểu diễn thêm nhóm Fresh/Frozen cao tách khỏi nhóm chi tiêu thấp, đồng thời cả ba nhóm nhất quán về đặc trưng chính trên validation.
- **Trade-off được chấp nhận:** K=3 giảm silhouette validation và ARI để đổi lấy tính diễn giải kinh doanh theo ba mẫu hình sản phẩm. Đây là quyết định đa tiêu chí, không tạo tổng điểm giả và không dựa vào Channel/Region.

## Cấu hình và thứ tự thực hiện sau freeze

1. `models/selection_frozen.json` lưu selection duy nhất: log1p+StandardScaler, sáu feature theo thứ tự cố định, K3, seed42, n_init10, max_iter300, lloyd.
2. Khi runtime có lại, chạy regression và validate frozen config. **Không điều chỉnh cấu hình theo final test.**
3. Refit scaler và K-Means trên **train+validation (352 mẫu)** theo cấu hình đã freeze; khi đó cluster ID có thể đổi so với profiling trên train, cần profile lại theo model final để gán tên cụm.
4. Chỉ sau khi refit/config đã cố định, đọc **final test 88 mẫu đúng một lần**, transform/predict và tính metric độc lập. Lưu log/artifact và cấm dùng kết quả test để chọn lại K, seed, features, cutoff.
5. Xuất fitted pipeline/model artifact (scaler, centers, feature order, versions, metadata) và xác minh load/predict. BE/FE để sau.

**Provenance:** Gate 4 Git commit `26476baacb5c6dbd185293f10c81ea9a7eff90df`; evidence paths: `reports/data/experiments/selection_evidence.csv`, `reports/data/experiments/review_table.csv`, và `reports/data/profiles/{raw_k2_seed42,log1p_standardscaler_k2_seed42,log1p_standardscaler_k3_seed42}/{train_median_profile.csv,validation_median_profile.csv}`.

**Runtime status:** Không có test mới được chạy trong phiên Gate 5 vì phiên Codex local đã kết thúc. Chưa đọc final test, chưa tạo fitted model artifact; chỉ freeze **selection configuration**.
