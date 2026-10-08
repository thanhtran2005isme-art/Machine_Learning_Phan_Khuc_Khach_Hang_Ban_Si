# Data card — UCI Wholesale customers / Project 22

> Dataset metadata and audit snapshot. Đây **không** phải model card hay xác nhận rằng dữ liệu phù hợp trực tiếp với doanh nghiệp Việt Nam.

## Nguồn và quyền sử dụng

| Mục | Giá trị |
|---|---|
| Dataset | **Wholesale customers**, UCI Dataset ID **292** |
| Nguồn | https://archive.ics.uci.edu/dataset/292/wholesale%2Bcustomers |
| DOI / trích dẫn | Cardoso, M. (2013). *Wholesale customers* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5030X |
| Giấy phép | **Creative Commons Attribution 4.0 International (CC BY 4.0)**; khi chia sẻ/chuyển thể giữ ghi công và đường dẫn |
| Quy mô | **440** khách hàng, mỗi dòng một khách |
| Cấu trúc | **8 cột:** 6 khoản chi tiêu, `Channel`, `Region` |
| Giai đoạn chi tiêu | **Hằng năm (annual spending)** |
| Đơn vị | **Monetary units (m.u.)**, *UCI không định danh đơn vị tiền tệ cụ thể*. Không gọi là VND, USD, EUR hay tự suy diễn hệ số quy đổi. |
| Thời điểm công bố UCI | Trang UCI ghi **donated 30/03/2014** — **không phải ngày dữ liệu được ghi nhận/thu thập, cũng không phải ngày tải của project** |
| Ngày tải thực tế | Khi tải, `ml/src/download_data.py` ghi `downloaded_at_utc` vào **`data/raw/metadata.json` trên máy chạy**, không commit vào Git; vì vậy hồ sơ này không khẳng định ngày tải cụ thể. |
| Raw CSV fingerprint | `SHA256 c3d018c643565b85cee733c4a2ac76dd76e080e857cb23f0ccfcc2e15a6c17ef` từ `reports/data/data_quality.json` |

## Dictionary và mã danh mục

| Biến | Loại | Vai trò | Mô tả |
|---|---|---|---|
| `Fresh` | Số nguyên, ≥0 | Fit | Mức chi tiêu **năm** cho hàng tươi, m.u. |
| `Milk` | Số nguyên, ≥0 | Fit | Mức chi tiêu **năm** cho sữa, m.u. |
| `Grocery` | Số nguyên, ≥0 | Fit | Mức chi tiêu **năm** cho tạp hóa, m.u. |
| `Frozen` | Số nguyên, ≥0 | Fit | Mức chi tiêu **năm** cho hàng đông lạnh, m.u. |
| `Detergents_Paper` | Số nguyên, ≥0 | Fit | Mức chi tiêu **năm** cho chất tẩy rửa/giấy, m.u. |
| `Delicassen` | Số nguyên, ≥0 | Fit | Mức chi tiêu **năm** cho delicatessen, m.u.; giữ tên cột gốc, không đổi schema |
| `Channel` | Mã số | **Profiling only** | 1=Horeca, 2=Retail; không fit hoặc chọn K |
| `Region` | Mã số | **Profiling only** | 1=Lisbon, 2=Oporto, 3=Other; không fit hoặc chọn K |

Trang UCI liệt kê `Region` dưới nhãn metadata `Target`, **nhưng Project 22 là học không giám sát và không sử dụng bất kỳ target/ground truth nào để fit hoặc chọn K**. `Channel`/`Region` chỉ được ghép lại **sau** phân cụm để diễn giải. Tài liệu mapping mã: https://search.r-project.org/CRAN/refmans/tclust/html/wholesale.html.

## Chất lượng và giới hạn quan sát

Audit tại `reports/data/data_quality.json`: **440/440** dòng, **0 missing**, **0 duplicate**, **0 giá trị âm**, Channel counts **298/142**, Region counts **77/47/316**. IQR outliers theo từng biến lần lượt Fresh=20, Milk=28, Grocery=24, Frozen=43, Detergents_Paper=30, Delicassen=27. **Không cộng số outlier theo biến để suy ra số khách riêng biệt**; một người có thể bất thường ở nhiều biến.

Tách dữ liệu trước học scaler: train 264 (60%), validation 88 (20%), final test 88 (20%), seed42. `StandardScaler` khi so sánh K fit trên train; sau chọn D011 K2 và freeze mới refit **352 train+validation**. Final test 88 đã dùng đúng một lần cho đánh giá độc lập, **không dùng lại để lựa chọn hay profiling**.

## Điều kiện nhập dữ liệu và áp dụng

- Mô hình dùng **sáu khoản chi tiêu hằng năm đã quan sát đầy đủ**. Khi chưa có lịch sử năm (khách hoàn toàn mới), hệ thống **không có đủ feature** để gán cụm một cách có căn cứ; mẫu thử nhập tay chỉ là *giả định* theo đúng đơn vị/cùng định nghĩa.
- Dataset không cung cấp dấu thời gian từng hóa đơn hoặc năm quan sát. Không coi giá trị năm là dự báo real-time, doanh thu/lợi nhuận hay chi tiêu tháng.
- API yêu cầu 6 **JSON numbers hữu hạn ≥0** (chấp nhận số thập phân trong công cụ minh họa); từ chối thiếu, âm, chuỗi, extra field. Không tự ép kiểu/điền thiếu.
- Khoảng min/max cảnh báo đầu vào xuất phát từ EDA **264 train**, không phải miền hợp lệ tuyệt đối. Dữ liệu vượt khoảng **vẫn được gán cụm** kèm cảnh báo, không clipping. Cờ này **khác** với outlier khoảng cách theo IQR của 352 development.
- Dữ liệu lịch sử từ một nhà phân phối cụ thể; **chưa có chứng cứ** mô hình khái quát sang tổ chức/tiền tệ/thời kỳ khác. Muốn sử dụng thực tế cần xác minh mapping, đơn vị, chất lượng dữ liệu và đánh giá lại trên dữ liệu triển khai (ngoài phạm vi mô hình frozen nộp đồ án).

## Tái lập, provenance

- File raw/processed không commit; tải và audit lại bằng `ml/src/download_data.py`, `ml/src/audit_data.py`, `ml/src/split_data.py`. Không chạy `ml/src/finalize_model.py` sau khi one-shot evaluation Gate5 đã COMPLETE.
- Final descriptive profiles (predict-only): `reports/data/final_profile/`, 352 development, six CSV + `profile_metadata.json` có checksum cho từng nguồn; `GET /api/dashboard.final_profile` verify trước khi phục vụ. Không được nhầm với candidate 264 train-only.
- Đề bài không ghi rõ ngày mua sắm/tần suất giao dịch hay biến target chất lượng khách; không tự suy diễn.

## Nguồn tham khảo

1. [UCI Wholesale customers](https://archive.ics.uci.edu/dataset/292/wholesale%2Bcustomers); [DOI](https://doi.org/10.24432/C5030X), CC BY 4.0.
2. [CRAN tclust — Wholesale customers data dictionary/category codes](https://search.r-project.org/CRAN/refmans/tclust/html/wholesale.html).
3. Audit của dự án: `reports/data/data_quality.json`; pipeline `ml/src/download_data.py`; frozen D011 `models/selection.json`.
