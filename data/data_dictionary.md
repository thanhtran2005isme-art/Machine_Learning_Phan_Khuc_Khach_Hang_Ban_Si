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
