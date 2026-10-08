# Experiment Review — chưa chọn K

> File này chỉ tổng hợp bằng chứng train/validation. Không phải quyết định model cuối.
> Test vẫn khóa và không được dùng ở bước này.

## Nguyên tắc đọc

- Không chọn K chỉ vì silhouette cao nhất.
- Phải đọc cùng lúc silhouette validation, stability ARI, cluster size, inertia/elbow và khả năng diễn giải profile.
- Inertia không dùng để so trực tiếp giữa hai preprocessing vì không gian/scale khác nhau.
- Các rank dưới đây chỉ giúp rà soát từng tiêu chí riêng, **không được cộng thành điểm tổng**.

## raw

| k | validation_silhouette_mean | ari_mean | ari_min | min_cluster_share_mean | silhouette_generalization_gap_abs |
|---|---|---|---|---|---|
| 2 | 0.6103 | 1.0000 | 1.0000 | 0.1780 | 0.1118 |
| 3 | 0.4312 | 0.9427 | 0.8536 | 0.0909 | 0.0293 |
| 4 | 0.3826 | 0.9159 | 0.7864 | 0.0178 | 0.0489 |
| 5 | 0.3155 | 0.9581 | 0.8686 | 0.0152 | 0.0947 |
| 6 | 0.3043 | 0.9186 | 0.8470 | 0.0038 | 0.0868 |
| 7 | 0.3039 | 0.8712 | 0.6002 | 0.0038 | 0.0879 |
| 8 | 0.2883 | 0.9189 | 0.7886 | 0.0038 | 0.0658 |

### Candidate cần xem profile trước khi freeze

Dựa trên bảng trên, nhóm phải chọn một shortlist nhỏ để profile median chi tiêu + Channel/Region. Không tự động freeze K trong bước review này.

## log1p_standardscaler

| k | validation_silhouette_mean | ari_mean | ari_min | min_cluster_share_mean | silhouette_generalization_gap_abs |
|---|---|---|---|---|---|
| 2 | 0.3066 | 0.9970 | 0.9848 | 0.4473 | 0.0310 |
| 3 | 0.2165 | 0.9078 | 0.7982 | 0.3038 | 0.0116 |
| 4 | 0.1540 | 0.9152 | 0.7916 | 0.1254 | 0.0520 |
| 5 | 0.1623 | 0.6775 | 0.3574 | 0.0860 | 0.0353 |
| 6 | 0.1601 | 0.5671 | 0.3932 | 0.0602 | 0.0332 |
| 7 | 0.1446 | 0.5836 | 0.3581 | 0.0451 | 0.0422 |
| 8 | 0.1404 | 0.6329 | 0.3594 | 0.0284 | 0.0478 |

### Candidate cần xem profile trước khi freeze

Dựa trên bảng trên, nhóm phải chọn một shortlist nhỏ để profile median chi tiêu + Channel/Region. Không tự động freeze K trong bước review này.
