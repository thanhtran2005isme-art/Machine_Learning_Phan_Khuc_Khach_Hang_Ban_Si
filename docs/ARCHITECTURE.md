# Kiến trúc Project 22

## Stack đã chốt

- **Frontend:** React + TypeScript + Vite
- **Backend:** Node.js + TypeScript + Fastify
- **Machine Learning:** Python + pandas + NumPy + scikit-learn
- **Serving model:** Backend Node.js sẽ chỉ nạp artifact đã đóng băng; không huấn luyện lại ở mỗi request.

## Phân tách trách nhiệm

```text
frontend/
  React + TypeScript
  UI / dashboard / form phân khúc

backend/
  Node.js + TypeScript
  API / validation / đọc artifact / serving

ml/
  Python
  download / audit / split / EDA / thí nghiệm / train / evaluate / export

data/
  raw + processed (tái tạo bằng script, không commit CSV sinh ra)

models/
  artifact mô hình sau khi chọn K và đóng băng

reports/
  bảng, metric, figure sinh từ pipeline
```

## Trạng thái hiện tại

### Đã dựng

- React skeleton.
- Node/Fastify skeleton với `GET /api/health`.
- Python data download.
- Schema/domain validation.
- Data quality audit.
- Train/validation/test split cố định và có manifest.
- Unit test cho validation/split.

### Chưa làm có chủ đích

- `log1p` / `StandardScaler`.
- EDA kết luận trên validation/test.
- Baseline clustering.
- K-Means.
- Chọn K.
- Model artifact.
- `POST /api/segment`.
- Dashboard thực nghiệm.

Các phần trên chỉ bắt đầu sau khi pipeline dữ liệu được chạy và kiểm tra PASS.
