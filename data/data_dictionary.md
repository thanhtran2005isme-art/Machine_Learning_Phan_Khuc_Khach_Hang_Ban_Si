# Data Dictionary — Wholesale customers

| Biến | Kiểu | Đơn vị / ý nghĩa | Vai trò trong Project 22 |
|---|---|---|---|
| `Fresh` | Integer | Chi tiêu năm cho sản phẩm tươi, monetary units | Feature chính |
| `Milk` | Integer | Chi tiêu năm cho sản phẩm sữa, monetary units | Feature chính |
| `Grocery` | Integer | Chi tiêu năm cho hàng tạp hóa, monetary units | Feature chính |
| `Frozen` | Integer | Chi tiêu năm cho sản phẩm đông lạnh, monetary units | Feature chính |
| `Detergents_Paper` | Integer | Chi tiêu năm cho chất tẩy rửa và giấy, monetary units | Feature chính |
| `Delicassen` | Integer | Chi tiêu năm cho delicatessen, monetary units | Feature chính |
| `Channel` | Categorical (mã số) | Kênh khách hàng | **Profiling only**; không fit K-Means, không chọn K |
| `Region` | Categorical (mã số) | Khu vực khách hàng | **Profiling only**; không fit K-Means, không chọn K |

## Thời điểm sẵn có

Các biến trên nằm trong bản ghi khách hàng của dataset. Trong bài này không có trục thời gian để chia theo thời gian; nhóm dùng random split cố định trước preprocessing. Nếu về sau bổ sung dữ liệu có thời gian/người/phiên/hóa đơn, chiến lược split phải được xem xét lại theo đúng nhóm/thời gian để tránh leakage.

## Ghi chú

Trang UCI có thể mô tả vai trò metadata của `Channel`/`Region` khác cách sử dụng trong học phần. Trong **Project 22**, vai trò phải theo đề: chỉ dùng để profiling sau phân cụm.

## Chuẩn đơn vị và điều kiện sử dụng (Gate 9.5)

- Sáu feature = **mức chi tiêu hằng năm**, đơn vị **monetary units (m.u.)** theo UCI; **không phải VND hay loại tiền đã được công bố**. Tài liệu UCI: https://archive.ics.uci.edu/dataset/292/wholesale%2Bcustomers.
- Đầu vào thực tế chỉ sẵn có **sau khi** đã ghi nhận đầy đủ sáu chi tiêu trong kỳ năm. Dataset không có ngày giao dịch/khóa năm, không dự đoán chi tiêu tương lai hoặc điểm phân loại khách chưa có chi tiêu.
- `Channel`: 1 = Horeca (hotel/restaurant/café), 2 = Retail (bán lẻ).
- `Region`: 1 = Lisbon, 2 = Oporto, 3 = Other. Mã được ghi trong tài liệu dữ liệu UCI qua các bản sử dụng học thuật, xem https://search.r-project.org/CRAN/refmans/tclust/html/wholesale.html.
- Cả hai biến phân loại **chỉ mô tả** sau KMeans. Metadata UCI gắn `Region` role `Target` nhưng Project22 không học giám sát và không được dùng Region làm nhãn/chọn K.
- Chi tiết lineage, hạn chế, raw checksum, giấy phép tại [DATA_CARD.md](../docs/DATA_CARD.md).
