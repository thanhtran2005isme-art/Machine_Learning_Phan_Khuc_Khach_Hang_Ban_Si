# Model card — D011 frozen K-Means K=2 / Project 22

> **Đã đóng băng**. Đây là báo cáo mô tả thuật toán/phạm vi sử dụng, không phải đề nghị retrain hoặc công cụ quyết định quyền lợi của khách hàng.

## Nhận diện và cấu hình

| Trường | Giá trị (frozen artifacts) |
|---|---|
| Quyết định | `D011`, `models/selection.json` status `FROZEN` |
| Thuật toán | `sklearn.cluster.KMeans`, `algorithm='lloyd'` |
| Tiền xử lý | `log1p` cho 6 chi tiêu → `StandardScaler` |
| Số cụm | **K=2** |
| Seed | `random_state=42` |
| Số khởi tạo | `n_init=10` |
| Vòng lặp tối đa | `max_iter=300` |
| Fit cuối | **352 development** = 264 train + 88 validation, sau khi chọn K |
| Final test | **88** mẫu độc lập, đánh giá **một lần** sau freeze |
| 6 input | Fresh, Milk, Grocery, Frozen, Detergents_Paper, Delicassen |
| Không tham gia fit | Channel, Region; chỉ dùng mô tả sau phân cụm |
| Checksum model.json | `5057db0e290c93043abe4add3abf440e64864dc8d187a8d0b22d18621acd3b28` |
| Checksum model.joblib | `f2f7874807456e6fdbade0be4c1eb124a8245e922dbf5ca6f070a9e040f2c816` |

## Vì sao chọn D011 K2

| Phép đo trước final test | Raw K2 | Log1p + Scaler K2 | Log1p + Scaler K3 |
|---|---:|---:|---:|
| Validation silhouette mean, 10 seeds | 0.6103 | 0.3066 | 0.2165 |
| ARI seed stability mean | 1.0000 | **0.9970** | 0.9078 |
| Tỷ trọng cụm nhỏ nhất trên train | 17.80% | **44.70%** | 27.65% |
| ARI train-fit so với refit trên 352 (trước test) | — | **0.8893** | **0.3343** |
| Top 1% ảnh hưởng inertia train | 25.33% | **10.06%** | 10.43% |

**Raw K=2 có silhouette cao hơn**; không giấu/chỉnh metric. Tuy nhiên, kết quả raw bị ảnh hưởng mạnh hơn bởi các điểm xa, tỷ trọng cụm kém cân bằng. D011 K2 log+scaled duy trì hai xu hướng chi tiêu sau refit lên 352 tốt hơn phương án K3. K3 có thể mô tả chi tiết nhóm chi tiêu thấp hơn ở train nhưng profile không giữ ổn định tương tự khi refit. **Đây là lựa chọn đa tiêu chí** trên development, không phải chứng minh K2 tối ưu tuyệt đối. Inertia Raw và scaled **không** so sánh trực tiếp độ lớn.

## Kết quả đã freeze

| Chỉ số | Development 352 | Final test 88 (one-shot) |
|---|---:|---:|
| Silhouette | 0.289158 | **0.238890** |
| Inertia / row trong không gian log1p+scaled | 4.163875 | **4.505144** |
| Cluster counts | 162 / 190 | 45 / 43 |
| Cụm nhỏ nhất | 46.02% | 48.86% |

Final test thấp hơn development về silhouette (~0.0503); **không dùng kết quả test để đổi K**, seed, preprocessing hoặc tên cụm. Không có nhãn sự thật ⇒ không báo accuracy/precision/recall/F1.

## Profile cuối — 352 development

| Median gốc, m.u. | Cụm 0 (162) | Cụm 1 (190) |
|---|---:|---:|
| Fresh | 6410.5 | 9727.5 |
| Milk | 7226 | 1626 |
| Grocery | 10842.5 | 2175.5 |
| Frozen | 1153 | 2194.5 |
| Detergents_Paper | 4084.5 | 279.5 |
| Delicassen | 1508.5 | 662 |

- **Cụm 0:** xu hướng cao hơn ở Grocery/Milk/Detergents_Paper. Mã `0` không có thứ hạng giá trị.
- **Cụm 1:** xu hướng cao hơn ở Fresh/Frozen. Mã `1` không mang nghĩa tốt/xấu hơn.
- Channel/Region chỉ hậu phân cụm, không đủ để kết luận tác động hay quan hệ nhân quả, và không phải nhãn đúng/sai.
- Outlier khoảng cách Euclidean trong feature space đã scale, theo ngưỡng **Q3 + 1.5×IQR tính riêng cho từng cụm**: **5** (cụm 0) và **11** (cụm 1). Cờ chỉ mang tính mô tả trên development, **không loại mẫu, không phải OOD probability**.
- 4 quan sát có khoảng cách lớn nhất (top 1% development) đóng góp ~**9.72%** tổng squared distance. Đây là chỉ số tập trung outlier, không có nghĩa 9.72% khách là ngoại lệ.
- Không được gộp **IQR theo chi tiêu raw**, **IQR khoảng cách**, và **cảnh báo từng feature ngoài min/max train** thành cùng một loại lỗi.

## Giả định, hạn chế và cách dùng

**Dùng để:** khám phá nhóm chi tiêu của những khách đã có sáu khoản chi tiêu hằng năm theo cùng định nghĩa m.u.; trình bày khuynh hướng và hình thành giả thuyết nghiệp vụ **cần kiểm chứng**.

**Không dùng để:** quyết định từ chối/phân biệt khách, suy ra doanh thu/lợi nhuận, tín nhiệm, giá trị cá nhân hoặc dự báo nhu cầu khi chưa có dữ liệu năm. Cụm không phải phân loại có nhãn, không có xác suất, calibration hay confidence score.

K-Means tối thiểu hóa tổng bình phương khoảng cách tới centroid trong không gian numeric đã scale, nhạy cảm với preprocessing/outlier và giả định những cụm có thể biểu diễn bằng centroid/Euclidean. Khoảng cách càng nhỏ chỉ có nghĩa gần centroid hơn **trong biểu diễn đó**; không tự suy ra khả năng đáp ứng, chất lượng hay độ đúng nhãn.

Khi triển khai ngoài môi trường bài học: kiểm tra ánh xạ 6 biến và kỳ chi tiêu, sự đồng nhất đơn vị, tình trạng dữ liệu, drift/outlier, tính dễ diễn giải với người dùng mới. Không có bằng chứng production performance hoặc effect size kinh doanh.

## Quy trình kiểm chứng

- Serving JSON: `backend/model.mjs` kiểm tra SHA-256 và frozen D011, chỉ `log1p(x)`, transform với scaler đã lưu, Euclidean nearest centroid; không fit.
- Reference sklearn: `models/model.joblib`. Gate9.2 đã kiểm tra parity trên **352 development**, Gate7/8 so sánh synthetic inputs. 
- Dashboard: `GET /api/dashboard.final_profile` đọc sáu CSV predict-only kèm checksum và đối chiếu median/count/inertia; không tái đánh giá test.
- Các kiểm thử Gate 6–9.5 kiểm API/schema/UI; **không được** chạy `ml/src/finalize_model.py` nữa.
- **Lịch sử K3** (`models/selection_frozen.json`, `models/selection_k3_retracted_pretest.json`) rút **trước** final test; source-of-truth phục vụ chỉ có D011 K2.

## Nguồn

- Project experiment audit: `docs/GATE5_MODEL_SELECTION.md`, `models/selection.json`, `models/model.json`, `models/final_evaluation.json`.
- [scikit-learn KMeans](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html); [scikit-learn Clustering guide (Silhouette/ARI)](https://scikit-learn.org/stable/modules/clustering.html).
- [UCI Wholesale customers](https://archive.ics.uci.edu/dataset/292/wholesale%2Bcustomers), [DOI](https://doi.org/10.24432/C5030X).
