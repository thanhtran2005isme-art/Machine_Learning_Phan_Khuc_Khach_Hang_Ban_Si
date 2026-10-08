# Bước tiếp theo — sau Gate D baseline + K-Means

Gate B data, Gate C skeleton, EDA train-only và **Gate D baseline/grid K-Means đã chạy thật**. Bản thí nghiệm đã tạo đủ 140 runs trên train/validation, 0 silhouette validation không xác định. Xem `docs/EXPERIMENTS.md`.

## Đã cố định và thực hiện

- Data split 264 train / 88 validation / 88 test, seed 42.
- Feature K-Means đúng 6 biến chi tiêu; `Channel`/`Region` chỉ profiling sau fit.
- Baseline A thống kê train; Baseline B raw K=2 seed42.
- Raw và `log1p + StandardScaler`; K=2..8; seed42..51; `n_init=10`, `algorithm=lloyd`.
- Fit scaler/K-Means trên train; validation chỉ transform/predict; **test chưa đọc**.
- Inertia/silhouette train/validation; cluster size/proportion, profiling và 45 cặp ARI cho mỗi preprocessing/K.
- CSV, JSON và 4 PNG tại `reports/data/experiments/` và `reports/figures/experiments/`.

## Việc tiếp theo (ngoài phạm vi Gate D)

1. Đọc `reports/data/experiments/seed_summary.csv`, `stability.csv`, `cluster_sizes.csv`, `cluster_profiles.csv` và 4 biểu đồ.
2. So sánh hiệu quả, độ ổn định, phân bổ kích thước cụm và ý nghĩa nghiệp vụ giữa K/preprocessing; inertia chỉ so sánh trong cùng không gian.
3. Lập luận lựa chọn K/preprocessing dựa trên train + validation và khóa config trước final test; không chọn chỉ theo silhouette cao nhất.
4. Chạy final test độc lập **sau khi freeze**, đánh giá và xuất model artifact.
5. Sau cùng mới thực hiện serving backend / frontend theo kế hoạch riêng.

## Lệnh kiểm chứng Gate D

```powershell
python ml/src/experiment.py
python -m pytest ml/tests -q
```

Không mở `data/processed/test.csv` hoặc dùng test chọn K/tham số trong các bước 1–3. Không tự động loại outlier, không dùng Channel/Region làm nhãn thật.
