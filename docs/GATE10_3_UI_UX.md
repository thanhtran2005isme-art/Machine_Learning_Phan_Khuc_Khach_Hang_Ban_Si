# Gate 10.3 — Professional UI/UX refresh (feature PR #1)

## Thiết kế
Tham khảo ba ảnh phong cách dashboard analytics do người dùng cung cấp. Không sao chép ảnh mẫu, không dùng ảnh stock và không tạo dữ liệu mô phỏng trong dashboard; chỉ dùng các con số JSON đã xác thực ở API.

Giữ nguyên ba màn hình:
- **Giới thiệu:** sidebar desktop / tabs mobile, model integrity status, hero CTA và preview quy mô cụm thật từ frozen model, bốn KPI 440/6/2/352. Data Card và mô phỏng Lloyd vẫn phân biệt nguồn và ví dụ.
- **Phân khúc:** label sáu nhóm chi tiêu rõ m.u., chỉ dẫn khoảng train, progress 0/6 đến 6/6, cảnh báo số không âm, kết quả khoảng cách / median / biểu đồ profile tương quan từng feature. Mỗi cặp bar có cùng thang **trong từng feature**, không so sánh bề ngang khác feature; bảng số thật vẫn có.
- **Dashboard:** KPI thật, anchor shortcuts cho experiment/PCA/profile/model, bộ lọc Raw/Log+Scale K2..8, PCA 352 điểm với tô màu Ward/KMeans, filter train/validation và chọn mẫu bằng index; so silhouette/ARI/contingency, distribution Channel/Region, metric caution được giữ nguyên.

UI hiện dùng React + CSS/SVG native, không cài thư viện UI hoặc plotting mới. Không thêm ảnh minh họa không khớp mô hình, không thêm chức năng mua hàng, không ghi dữ liệu hoặc thay thuật toán. Các tên "Cụm 0/1" chỉ định danh không xếp hạng.

## Responsive / kiểm thử
- Desktop từ ~861px: sidebar; mobile / tablet: header ngang, width 320 và 768 không overflow toàn trang.
- Các bảng có scroll riêng và không làm rộng body. Nút export CSV giữ clickable. Nút, form và PCA filter có focus ring/label; có prefers-reduced-motion.
- Không có lỗi âm thầm khi API unavailable: banner mô hình/API vẫn hiển thị; result không tự sinh.
- E2E mới kiểm tra điều hướng ba màn hình, sidebar model state, progress, PCA chọn mẫu bằng index, responsive widths 320/768.
- E2E visual review chụp đủ ba màn hình từ API thật trên desktop Chromium và Pixel 5 emulation, lưu artifacts \`gate10-ui-ubuntu\` và \`gate10-ui-windows\` từ Actions.
- **Không tuyên bố đã nghiệm thu thủ công trên Windows10 cá nhân.** CI Linux/Windows máy runner và Chrome emulation chỉ là tự động.

## Những thứ tuyệt đối giữ nguyên
\`models/*\`, \`reports/data/final_profile/*\`, \`reports/data/development_extension/*\`, final holdout one-shot, Fastify API protocol, giá trị và metric từ frozen D011.

## Nghiệm thu bằng tay
Trên nhánh PR #1 chạy \`npm ci\`, \`run.bat\`, mở http://localhost:5173. Kiểm tra trang Giới thiệu, submit ví dụ trên trang Phân khúc, qua Dashboard kiểm tra K sweep/PCA/Channel/Region, thử mobile narrow screen. Nếu cần xem ảnh tự động, vào workflow Gate10 CI → Artifacts rồi tải \`gate10-ui-ubuntu\` hoặc \`gate10-ui-windows\`.
