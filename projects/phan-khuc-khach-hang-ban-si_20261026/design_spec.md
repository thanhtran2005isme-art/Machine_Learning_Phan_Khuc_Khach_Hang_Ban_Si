<!-- ppt-master-schema: design-spec/v1 -->
# Phân Khúc Khách Hàng Bán Sì - Design Spec

## I. Project Information

| Item | Value |
| --- | --- |
| Project Name | Phân Khúc Khách Hàng Bán Sì (Project 22) |
| Canvas Format | PPT 16:9 (1280x720) |
| Page Count | 14 |
| Primary Language | vi |
| Target Audience | Ban lãnh đạo, quản trị thương mại và đội điều hành cần hiểu nhóm khách hàng bán sì để xây dựng chiến lược chăm sóc |
| Communication Intent | Báo cáo và minh bạch hóa kết quả mô hình phân cụm khách hàng bán sì (K-Means K=2, log1p + StandardScaler), giải thích cơ chế lựa chọn và phần công mức độ tin cậy, đồng thời đưa ra khuyến nghị nghiệp vụ |
| Audience Outcome | Người nghe nắm được 2 nhóm khách hàng chính, hiểu tại sao chọn K=2, tin cậy vào các chỉ số đánh giá và biết giới hạn của mô hình |
| Core Message / Ask / Action | Mô hình K=2 (log1p + StandardScaler) đã đóng băng chia 440 khách hàng bán sì thành 2 nhóm rõ ràng: "Tạp hóa / chất tẩy rửa" và "Thiên về hàng tươi / đông lạnh"; đánh giá độc lập trên 88 mẫu silhouette 0.239 |
| Delivery Context | Trình bày trực tiếp (presenter-led), nội bộMeeting; secondary: lưu trữ để đánh giá và tái sử dụng sau này |
| Artifact Afterlife | Kiểm duyệt, lưu trữ, chuyển giao cho đội nghiệp vụ |
| Reading Mode | balanced |
| Content Strategy | Dựa trên verified artifacts, không phát minh chỉ số |
| Design Style | custom (minimalist, data-journalism) |
| AI Image Acquisition Path | not applicable |
| Generation Mode | continuous |
| Spec Refinement | disabled |
| Speaker Notes | disabled — workflow default |
| Custom Animations | disabled |

## II. Canvas Specification

- **Format**: PPT 16:9, viewBox `0 0 1280 720`
- **All 14 pages share one canvas**

## III. Visual Theme

- **Core palette**: `#0B3C5D` (navy chính), `#14537C` (navy phụ), `#2E86AB` (xanh accent), `#F4A259` (vàng accent), `#E9ECEF` (nền nhạt), `#1A1A1A` (văn bản chính), `#6B7280` (văn bản phụ), `#CBD5E1` (divider)
- **Style**: minimalist data-journalism, không sombra, không phát光, khoảng trống rộng, mỗi trang nhấn một chủ đích
- **Chart/table styling**: stroke divider `#CBD5E1`, text `#1A1A1A`, legend top

## IV. Typography System

- **Font family**: Arial, "Microsoft YaHei", sans-serif (heading + body)
- **Body**: 24 px
- **Cover title / hero**: 44 px
- **Chapter title**: 40 px
- **Page title / KPI hero**: 36 px
- **Subtitle**: 32 px
- **Lead / subheading**: 30 px
- **Annotation**: 18 px
- **Footnote / page number**: 16 px

## V. Layout Principles

- Mọi trang dùng viewBox `0 0 1280 720`, margin左右 80 px, nội dung tập trung trong 1120 px
- Trang cover (P01): anchor, tiêu đề lớn ở giữa, motto dưới
- Trang nội dung (P02–P13): tiêu đề trên cùng bên trái, nội dung lưới 2 cột hoặc bảng/charts tập trung
- Trang đóng (P14): breathing, takeaway lớn, ít chữ
- Bảng median và metric cards căn giữa, chữ số đậm để dễ đọc
- Không dùng bóng đổ, không dùng phát光, không dùng ảnh AI

## VI. Icon Usage Specification

- **Library**: none (không dùng thư viện icon cơ sở)
- **Inventory**: none
- **Stroke width**: not applicable
- Real brand marks (nếu có) dùng đúng supplied mark; tại đây không có brand mark bên ngoài

## VII. Visualization Reference List

- P05: `chart/column_chart`? Không — dùng bảng so sánh (table) thay vì chart catalog
- P11: so sánh 6 chi tiêu giữa hai cụm → `chart/radar_chart` hoặc `chart/column_chart` grouped
- Các trang metric (P07, P08): KPI cards, không dùng chart catalog
- Các trang profile (P09, P10): bảng median 6 biến, không dùng chart catalog

## VIII. Image Resource List

- source: none | placement: none | render: none | crop: none
- Không dùng ảnh; toàn bộ hình vẽ bằng SVG carrier (hình tròn, hình chữ nhật, đường kẻ)

## IX. Content Outline

### Slide 1 (P01) — Cover
- **Core message**: Dự án 22 — phân cụm khách hàng bán sỉ bằng K-Means K=2 (log1p + StandardScaler)
- **Content**: Tiêu đề chính, phụ đề "Machine Learning Phân Khúc Khách Hàng Bán Sì", ngày 2026-10-08, mã quyết định D011, nguồn UCI Wholesale Customers
- **Audience move**: Nhận diện dự án, mục đích và bối cảnh
- **Relationships**: none

### Slide 2 (P02) — Agenda
- **Core message**: 14 khía cạnh từ dữ liệu, tiền xử lý, chọn mô hình đến khuyến nghị
- **Content**: Danh mục 14 mục theo thứ tự trình bày
- **Audience move**: Biết lộ trình và những gì sẽ được thảo luận
- **Relationships**: none

### Slide 3 (P03) — Dữ liệu & nguồn
- **Core message**: 440 khách hàng bán sỉ, UCI Wholesale Customers, 6 chi tiêu hàng năm, không giá trị thiếu, không trùng
- **Content**: Bảng: số dòng 440, 8 cột (Channel, Region + 6 chi tiêu), Channel 1=298/2=142, Region 1=77/2=47/3=316, nguồn DOI 10.24432/C5030X
- **Audience move**: Nắm được nguồn dữ liệu và độ tin cậy
- **Relationships**: none

### Slide 4 (P04) — Tiền xử lý & chia dữ liệu
- **Core message**: log1p cho 6 chi tiêu rồi StandardScaler; split 264 train / 88 validation / 88 test
- **Content**: Luồng xử lý, kích thước mỗi split, split xảy ra trước preprocessing học từ dữ liệu
- **Audience move**: Hiểu chuỗi xử lý và cách tránh rò rỉ dữ liệu
- **Relationships**: none

### Slide 5 (P05) — Chọn mô hình: tại sao K=2
- **Core message**: K=2 log1p+scaled cân bằng nhất (silhouette, ổn định ARI, tỷ trọng cụm lớn)
- **Content**: Bảng so sánh Raw K2 / Log+Scale K2 / Log+Scale K3 theo silhouette validation, ARI mean/min, tỷ trọng cụm nhỏ nhất, top 1% đóng góp inertia
- **Audience move**: Hiểu tại sao không chọn Raw K2 hay K3
- **Relationships**: none

### Slide 6 (P06) — Quy trình đóng băng D011
- **Core message**: Freeze trước khi đánh giá test; test 88 mẫu chỉ đánh giá một lần, không tham gia fit
- **Content**: Luồng D011, checksum artifact, final_evaluation.json status COMPLETE
- **Audience move**: Tin cậy vào việc mô hình đã đóng băng và test độc lập
- **Relationships**: none

### Slide 7 (P07) — Kết quả phát triển (352 mẫu)
- **Core message**: Silhouette 0.289, inertia/row 4.16, cụm 162 / 190 (46.0% / 54.0%)
- **Content**: Metric cards: silhouette, inertia/row, cluster 0/1, tỉ trọng cụm nhỏ nhất
- **Audience move**: Nắm kết quả trên tập phát triển trước khi xem test
- **Relationships**: none

### Slide 8 (P08) — Kiểm thử độc lập (88 mẫu)
- **Core message**: Silhouette 0.239, inertia/row 4.51, cụm 45 / 43, tỉ trọng cụm nhỏ nhất 48.9%; không dùng để đổi K
- **Content**: Metric cards: silhouette test, inertia/row, cluster 45/43, min cluster share
- **Audience move**: Hiểu kết quả ngoài mẫu và ràng buộc không chọn lại K
- **Relationships**: none

### Slide 9 (P09) — Cụm 0: Tạp hóa / chất tẩy rửa
- **Core message**: 162 khách (46.0%), median Grocery cao nhất, xu hướng Milk/Detergents_Paper
- **Content**: Bảng median 6 chi tiêu (Fresh, Milk, Grocery, Frozen, Detergents_Paper, Delicassen), đơn vị gốc
- **Audience move**: Nhận diện đặc điểm cụm 0
- **Relationships**: none

### Slide 10 (P10) — Cụm 1: Thiên về hàng tươi / đông lạnh
- **Core message**: 190 khách (54.0%), median Fresh cao nhất, xu hướng Fresh/Frozen
- **Content**: Bảng median 6 chi tiêu, đơn vị gốc
- **Audience move**: Nhận diện đặc điểm cụm 1
- **Relationships**: none

### Slide 11 (P11) — So sánh hai cụm
- **Core message**: Hai cụm phân biệt rõ trên Grocery/Milk/Detergents (cụm 0) vs Fresh/Frozen (cụm 1)
- **Content**: Biểu đồ so sánh 6 chi tiêu giữa hai cụm (median đơn vị gốc)
- **Audience move**: Thấy rõ đường phân ranh giữa hai nhóm khách
- **Relationships**: none

### Slide 12 (P12) — Hạn chế & giả định
- **Core message**: Không có nhãn thật, không retrain, chỉ profiling sau clustering, không phải OOD probability
- **Content**: Danh sách hạn chế: không có accuracy/precision/recall/F1, không suy ra doanh/lợi nhuận, K-Means nhạy cảm với outlier/preprocessing
- **Audience move**: Hiểu ranh giới và mức độ tin cậy
- **Relationships**: none

### Slide 13 (P13) — Khuyến nghị nghiệp vụ
- **Core message**: Chăm sát khác theo nhóm: cụm 0 tập trung tạp hóa/chất tẩy rửa; cụm 1 tập trung hàng tươi/đông lạnh
- **Content**: 4–5 khuyến nghị nghiệp vụ cụ thể
- **Audience move**: Nhận hành động tiếp theo cho mỗi nhóm
- **Relationships**: none

### Slide 14 (P14) — Tóm tắt & đóng
- **Core message**: 2 nhóm khách hàng, K=2 đã đóng băng, kiểm thử độc lập silhouette 0.239
- **Content**: Takeaway chính, liên hệ, lời cảm ơn
- **Audience move**: Giữ lấy kết luận và biết ai để hỏi thêm
- **Relationships**: none

## X. Speaker Notes Requirements

- **Generation**: disabled
