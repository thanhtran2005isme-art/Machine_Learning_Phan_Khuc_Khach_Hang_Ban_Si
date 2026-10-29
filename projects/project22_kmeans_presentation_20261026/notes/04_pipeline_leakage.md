Quy tắc chống rò rỉ dữ liệu (Anti-Data Leakage) là trọng tâm hàng đầu của đồ án.
Chúng tôi chia tập dữ liệu ngay từ đầu thành: Train 264 mẫu (60%), Validation 88 mẫu (20%), và Test độc lập 88 mẫu (20%).
Mọi bước học từ dữ liệu gồm fit Scaler và fit K-Means chỉ diễn ra trên tập Train.
Tập Test được niêm phong hoàn toàn và chỉ được đánh giá đúng một lần sau khi đóng băng quyết định mô hình.