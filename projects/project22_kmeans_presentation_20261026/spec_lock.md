<!-- ppt-master-schema: spec-lock/v1 -->
# Execution Lock

## canvas
- format: PPT 16:9
- viewBox: 0 0 1280 720

## communication
- primary_language: vi
- audience: Giảng viên và đồng nghiệp đánh giá dự án học thuật Machine Learning
- objective: Trình bày hoàn chỉnh quy trình phân khúc khách hàng để chứng minh hiểu biết ML pipeline và đạt đánh giá tốt
- core_message: K-Means D011 (log1p + StandardScaler, K=2) là giải pháp ổn định và có ý nghĩa kinh doanh, đã triển khai thành công với full CI/CD testing

## mode
- mode: custom
- mode_behavior: Presentation mode với cấu trúc rõ ràng mỗi slide tập trung vào một insight chính, sử dụng visualization để support arguments, progressive disclosure cho complex data, và clear takeaway messages

## visual_style
- visual_style: custom
- visual_style_behavior: Modern technical aesthetic với geometric shapes sạch sẽ, data charts prominent, subtle gradients cho depth, consistent card-based containers, icon-supported headings, generous whitespace, và color usage theo data visualization best practices

## colors
- background: #FFFFFF
- secondary_bg: #F8F9FA
- primary: #2563EB
- accent: #10B981
- secondary_accent: #8B5CF6
- body_text: #1F2937
- secondary_text: #6B7280
- divider: #E5E7EB

## typography
- title_family: Arial, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif
- body_family: Arial, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif
- font_family: Arial, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif
- body: 24
- title: 48
- subtitle: 32
- annotation: 18
- card_title: 28
- section_title: 42
- footnote: 14
- compact_metric: 15
- badge: 13
- small_label: 12
- micro_label: 11
- hero_metric: 56
- large_metric: 52

## icons
- library: phosphor-duotone
- inventory: chart-line, chart-pie-slice, database, git-branch, code, check-circle, warning, users-three, stack, target

## page_rhythm
- P01: anchor
- P02: anchor
- P03: anchor
- P04: anchor
- P05: breathing
- P06: breathing
- P07: breathing
- P08: anchor
- P09: anchor
- P10: dense
- P11: breathing
- P12: breathing
- P13: anchor
- P14: breathing
- P15: anchor

## page_visualizations
- P05: chart/grouped_bar_chart
- P06: chart/line_chart
- P07: chart/column_chart
- P08: chart/radar_chart
- P09: table/record_table

## pptx_structure
- mode: flat

## forbidden
- `mask`, `<style>`, `class`, external CSS, `<foreignObject>`, `textPath`, `@font-face`, `<animate*>`, `<set>`, `<script>` / event attributes, `<iframe>`
- HTML named entities in text; write typography as raw Unicode and escape XML reserved characters
