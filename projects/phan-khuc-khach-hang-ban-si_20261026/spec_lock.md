<!-- ppt-master-schema: spec-lock/v1 -->
# Execution Lock

## canvas
- viewBox: 0 0 1280 720
- format: PPT 16:9

## communication
- primary_language: vi
- audience: Ban lãnh đạo, quản trị thương mại và đội điều hành cần hiểu nhóm khách hàng bán sì để xây dựng chiến lược chăm sóc
- objective: Báo cáo và minh bạch hóa kết quả mô hình phân cụm khách hàng bán sì (K-Means K=2, log1p + StandardScaler), giải thích cơ chế lựa chọn và phần công mức độ tin cậy, đồng thời đưa ra khuyến nghị nghiệp vụ; người nghe nắm được 2 nhóm khách hàng chính, hiểu tại sao chọn K=2, tin cậy vào các chỉ số đánh giá và biết giới hạn của mô hình
- core_message: Mô hình K=2 (log1p + StandardScaler) đã đóng băng chia 440 khách hàng bán sì thành 2 nhóm rõ ràng: "Tạp hóa / chất tẩy rửa" và "Thiên về hàng tươi / đông lạnh"; đánh giá độc lập trên 88 mẫu silhouette 0.239
- consumption_mode: presentation

## mode
- mode: custom
- mode_references: pyramid, narrative
- mode_behavior: Mở bằng kết luận (2 nhóm khách hàng), phát triển bằng bằng chứng lựa chọn K=2 và kết quả kiểm thử, kết thúc bằng khuyến nghị nghiệp vụ

## visual_style
- visual_style: custom
- visual_style_behavior: Minimalist data-journalism, palette navy/xanh/vàng, không sombra, không phát光, chữ Arial/Microsoft YaHei, khoảng trống rộng, mỗi trang chỉ nhấn một chủ đích

## colors
- primary: #0B3C5D
- secondary: #14537C
- accent: #2E86AB
- accent_warm: #F4A259
- surface_light: #E9ECEF
- text_primary: #1A1A1A
- text_secondary: #6B7280
- divider: #CBD5E1

## typography
- font_family: Arial, "Microsoft YaHei", sans-serif
- title_family: Arial, "Microsoft YaHei", sans-serif
- body_family: Arial, "Microsoft YaHei", sans-serif
- body: 24
- title: 44
- subtitle: 32
- lead: 30
- annotation: 18
- footnote: 16
- page_title: 34
- kpi_value: 46
- kpi_label: 15
- caption: 13
- footer: 11

## icons
- library: none
- inventory: none

## page_rhythm
- P01: anchor
- P02: dense
- P03: dense
- P04: dense
- P05: dense
- P06: anchor
- P07: anchor
- P08: anchor
- P09: anchor
- P10: anchor
- P11: anchor
- P12: dense
- P13: dense
- P14: breathing

## pptx_structure
- mode: flat

## forbidden
- `mask`, `<style>`, `class`, external CSS, `<foreignObject>`, `textPath`, `@font-face`, `<animate*>`, `<set>`, `<script>` / event attributes, `<iframe>`
- HTML named entities in text; write typography as raw Unicode and escape XML reserved characters
- Không dùng ảnh AI (user)
- Không vẽ lại centroid hay coi cụm là nhãn đúng/sai (user)
- Không dùng Channel/Region làm ground truth chọn K (user)
