# Gate 9.5 — API contract và ví dụ JSON đầy đủ

## GET /api/model-info (additive data/model cards)

Endpoint giữ nguyên `status`, `k`, `preprocessing`, `profiles`, `reference_ranges`, `reference_note` và `limitations`. Bổ sung hai object:

- `data_card`: `dataset`, `uci_id`, `source_url`, `doi`, `license`, `row_count`, `spending_period`, `spending_unit`, `currency_known`, `feature_columns`, `profiling_only_columns`, `data_available_when`, `source_policy`.
- `model_card`: `decision`, `algorithm`, `random_state`, `n_init`, `max_iter`, `preprocessing`, `k`, `selection_scope`, `fit_scope`, `fit_rows`, `held_out_test_rows`, `held_out_test_evaluated_once`, `cluster_labels`, `selection_rationale`, `assumptions`, `intended_use`, `prohibited_inferences`, `metric_cautions`, `distance_cautions`.

Số liệu/tham số đọc từ mô hình D011 đã verify; phần diễn giải là mô tả thống nhất với [model card](MODEL_CARD.md) và [data card](DATA_CARD.md). Không phải endpoint training, không thêm quyền thay K.

## POST /api/segment — request

```http
POST /api/segment HTTP/1.1
Content-Type: application/json
```

```json
{
  "Fresh": 6410.5,
  "Milk": 7226,
  "Grocery": 10842.5,
  "Frozen": 1153,
  "Detergents_Paper": 4084.5,
  "Delicassen": 1508.5
}
```

Đây là vector **median của cụm 0 đã xuất từ frozen model**, chỉ là **ví dụ diễn giải**, không phải số liệu một khách cụ thể.

## POST /api/segment — response HTTP 200 đầy đủ

Các khoảng cách sau được tính từ **scaler mean/scale và centroids trong `models/model.json` D011 K2** theo đúng công thức Node serving, không phải một prediction trên held-out test:

```json
{
  "status": "ok",
  "cluster_id": 0,
  "distance_to_centroid": 0.26018988610281957,
  "distances_to_centroids": [
    0.26018988610281957,
    2.749008929378785
  ],
  "profile": {
    "name": "Tạp hóa / chất tẩy rửa",
    "count": 162,
    "share": 0.4602272727272727,
    "median_spending": {
      "Fresh": 6410.5,
      "Milk": 7226,
      "Grocery": 10842.5,
      "Frozen": 1153,
      "Detergents_Paper": 4084.5,
      "Delicassen": 1508.5
    }
  },
  "warnings": [],
  "distance_space": "log1p + StandardScaler (Euclidean)"
}
```

Sai biệt rất nhỏ ở chữ số cuối có thể phụ thuộc môi trường floating point; **giá trị ví dụ cần được kiểm tra lại bằng HTTP smoke nếu code serving thay đổi trong tương lai**.

## Lỗi đầu vào / thiếu artifact

- HTTP **400**: `{"status":"invalid_input","message":"Cần đúng 6 giá trị chi tiêu không âm, hữu hạn (kiểu number)","errors":[...]}` (danh sách `errors` phụ thuộc trường sai). Từ chối giá trị âm/thiếu/chuỗi/field thừa, không coercion/clipping.
- HTTP **503** khi mô hình không sẵn sàng: `{"status":"not_ready","message":"Frozen model unavailable"}` ở `POST /api/segment`.
- HTTP **503** khi dashboard evidence thiếu/sai checksum: `{"status":"not_ready","message":"Dashboard evidence unavailable or failed integrity validation"}` ở `GET /api/dashboard`. Không đưa raw path/stacktrace ra client.

## Ba khác biệt quan trọng

1. Cảnh báo `warnings`: vượt min/max feature của **264 train EDA**, nhưng vẫn được gán cụm. Không phải lỗi schema, không phải model từ chối.
2. `distance_to_centroid`: Euclidean trong `log1p+scaled`, không phải confidence.
3. `GET /api/dashboard.final_profile.outliers`: **16 cờ khoảng cách IQR** theo hai cụm trên **352 development**; không quyết định logic/giá trị khách mới trong `POST /api/segment`.

Đã có /api/dashboard schema và checksum chi tiết tại [Gate9.3](GATE9_3_API.md). UI diễn giải tại [Gate9.4](GATE9_4_FRONTEND.md).

## Hướng dẫn kiểm chứng

```powershell
npm ci
npm run test:serving
npm run test:backend
npm run build
npm run test:smoke
```

Bài E2E thêm tại `e2e/customer-flow.spec.ts` đối chiếu data card, model card, cảnh báo cùng API và tính trung tính của cụm. Không dùng dữ liệu test ML hay fit khi gọi HTTP.
