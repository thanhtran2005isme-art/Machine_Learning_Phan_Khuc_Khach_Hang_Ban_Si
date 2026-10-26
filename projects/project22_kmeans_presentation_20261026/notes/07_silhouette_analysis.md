Tiếp tục thí nghiệm 2 với hệ số Silhouette trên cả tập Train và Validation.
Với log1p + StandardScaler, K=2 đạt Silhouette Validation cao nhất là 0.307, tiếp đến K=3 đạt 0.217. Từ K>=4 trở đi, Silhouette giảm sâu dưới 0.16.
Độ chênh lệch giữa Train và Validation ở K=2 rất thấp, chứng minh mô hình tổng quát hóa rất tốt và không bị quá khớp.