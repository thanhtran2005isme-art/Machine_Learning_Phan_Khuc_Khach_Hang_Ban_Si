Về kiến trúc công nghệ: Nhóm tuân thủ nguyên tắc tách biệt Training và Serving.
Huấn luyện offline bằng Python scikit-learn; sau khi đóng băng, toàn bộ tham số được xuất ra file JSON kèm mã băm SHA-256.
Phần phục vụ trực tuyến chạy trên Node.js Fastify thuần, xác thực checksum model mỗi khi khởi động, đảm bảo tốc độ suy luận cực nhanh và an toàn tuyệt đối.