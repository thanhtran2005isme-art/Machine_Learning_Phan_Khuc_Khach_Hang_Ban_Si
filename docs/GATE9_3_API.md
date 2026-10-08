# Gate 9.3 — Read-only verified final development profiles API

**Trạng thái:** Core CI Gate 6 run `37810418640` PASS (15 Node-native tests, 11 Fastify tests, both builds and production smoke). Browser/Windows CI pending at time of writing; update this document only after receiving final results.

## Endpoint

`GET /api/dashboard` **giữ nguyên contract của Gate 6**:

- `selection_decision`, `k`, `preprocessing`.
- `experiments`: 14 K candidates từ bằng chứng train/validation, không thay K của serving.
- `training`, `final_test`: metadata Gate 5 frozen (không đọc hoặc đánh giá lại final test).
- `profiles`: 2 hồ sơ với median chi tiêu từ `model.json`.
- `metric_note`: ghi chú so sánh inertia.

**Mới trong Gate 9.3:** `final_profile`, dữ liệu cho Gate 9.4:

| Trường | Kiểu | Ý nghĩa |
|---|---|---|
| `source_scope` | string | `train_plus_validation` |
| `development_count` | number | 352 development samples |
| `model_sha256`, `selection_sha256` | hex string | Provenance D011 |
| `feature_columns` | string[6] | Sáu biến chi tiêu, theo đúng thứ tự model |
| `profiling_only_columns` | string[2] | Channel/Region; không dùng fit |
| `cluster_summary` | array[2] | `cluster_id, name, count, share, median_spending` |
| `cluster_sizes` | array[2] | `cluster_id, count, share` |
| `median_ratio` | array[2] | `cluster_id, values` (6 ratios vs median toàn bộ development) |
| `channel_profile` | array[4] | `cluster_id, channel, count, within_cluster_share` |
| `region_profile` | array[6] | `cluster_id, region, count, within_cluster_share` |
| `distance_summary` | array[2] | Count, min/mean/median/p90/p95/max, q1/q3, upper IQR fence, outlier count, inertia/member |
| `outliers` | object | Quy tắc IQR, `count=16`, top 1% count/share of inertia |
| `inertia_per_row` | number | 4.163874729781235; phải khớp Gate 5 development |
| `distance_space` | string | Euclidean trong không gian `log1p + StandardScaler` đã freeze |
| `median_ratio_denominator` | string | Median của 352 development cho từng feature |
| `evidence_sha256` | object | SHA-256 của đúng 6 CSV Gate 9.2 |
| `read_only`, `test_used` | boolean | `true` / `false` |

Ví dụ phân đoạn response (lược các trường đang có và các hàng dữ liệu còn lại):

```json
{
  "selection_decision": "D011",
  "k": 2,
  "preprocessing": "log1p_standardscaler",
  "final_profile": {
    "source_scope": "train_plus_validation",
    "development_count": 352,
    "cluster_sizes": [
      {"cluster_id": 0, "count": 162, "share": 0.460227272727},
      {"cluster_id": 1, "count": 190, "share": 0.539772727273}
    ],
    "outliers": {
      "rule": "distance > cluster Q3 + 1.5*IQR; descriptive flag, no removal",
      "count": 16,
      "top_1pct_count": 4,
      "top_1pct_inertia_share": 0.09722438407028816
    },
    "test_used": false,
    "read_only": true
  }
}
```

## Integrity & fail-closed policy

- `backend/final-profile.mjs` chỉ đọc `reports/data/final_profile/profile_metadata.json` và **6 CSV whitelist**, tên file/path được đối chiếu chính xác. Không tin path tự do trong metadata.
- Mỗi yêu cầu `GET /api/dashboard` kiểm tra SHA-256 của sáu CSV. Chấp nhận chuyển CRLF/LF thuần túy do Git checkout; từ chối chỉnh sửa nội dung khác.
- Đối chiếu metadata với model D011: model SHA, selection SHA, K2, preprocessing, 352 development, 264 train + 88 validation, chính sách no fit/no test.
- Đối chiếu count/share/median với frozen model, tổng Channel/Region từng cụm, median ratio denominator, các quantiles/outliers và weighted inertia với `models/final_evaluation.json`.
- Tính toán ở đây **chỉ parse, verify và tổng hợp read-only**; không đọc `test.csv`, không gọi Python, sklearn hay fit.
- Thiếu file/checksum/schema/provenance không hợp lệ → HTTP **503** `{"status":"not_ready","message":"Dashboard evidence unavailable or failed integrity validation"}`, không trả số liệu không xác minh.
- Lỗi dashboard không làm `/api/health`, `/api/model-info`, `POST /api/segment` thất bại nếu frozen serving model vẫn hợp lệ.
- Không trả đường dẫn filesystem, thông tin bí mật hoặc raw file nội bộ trong error response.

## Kiểm thử

```powershell
npm ci
npm run test:serving
npm run test:backend
npm run build
npm run test:smoke
```

Bộ core Gate 9.3 gồm 10 native tests mới, 2 Fastify integration tests mới và browser E2E bổ sung. Trường hợp kiểm tra: happy path, semantics frozen, corrupt/rehashed tampering, missing CSV, wrong header, path traversal, metadata SHA mismatch, hot mutation và LF/CRLF. Chạy Gate6/7/8 CI để kiểm tra hồi quy.

**Tiếp theo Gate 9.4:** FE sử dụng trực tiếp `final_profile` cho chart median ratio, cluster sizes, Channel/Region và khoảng cách. Không cho UI lựa chọn K thay đổi frozen serving model.
