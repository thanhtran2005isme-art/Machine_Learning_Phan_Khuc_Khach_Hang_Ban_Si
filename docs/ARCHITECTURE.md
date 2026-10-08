# Kiến trúc Project 22

## 1. Stack đã chốt

- **Frontend:** React + TypeScript + Vite
- **Backend:** Node.js + TypeScript + Fastify
- **Validation:** Zod
- **Machine Learning:** Python + pandas + NumPy + scikit-learn
- **Serving model:** Backend Node.js chỉ nạp artifact đã đóng băng; không huấn luyện lại ở mỗi request.

## 2. Phân tách trách nhiệm

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
  bảng, metric, figure và bằng chứng tái lập

docs/
  handoff / kiến trúc / quyết định / troubleshooting / history
```

## 3. Luồng dữ liệu và ML mục tiêu

```text
UCI Wholesale Customers
        ↓
download + checksum
        ↓
audit schema / quality
        ↓
split train / validation / test
        ↓
EDA trên train
        ↓
raw vs log1p + StandardScaler
        ↓
KMeans K=2..8 + nhiều seed
        ↓
validation evidence
        ↓
freeze K / preprocessing / config
        ↓
final test độc lập một lần
        ↓
export artifact
        ↓
Node.js API serving
        ↓
React UI/dashboard
```

## 4. Ranh giới leakage

- Split xảy ra trước mọi preprocessing học tham số từ dữ liệu.
- Scaler/model chỉ fit trên phần được phép của từng giai đoạn.
- Test không được dùng để chọn K, scaler, seed hay policy.
- `Channel` và `Region` không đi vào fit K-Means chính; chỉ ghép lại sau clustering để profiling.

## 5. Kiến trúc serving dự kiến

Python là nguồn huấn luyện/đánh giá chính. Sau khi mô hình được chọn và đóng băng:

```text
Python training
   ├── pipeline/joblib phục vụ tái lập học thuật
   └── serving artifact JSON/metadata
                         ↓
                   Node.js backend
                         ↓
                  POST /api/segment
                         ↓
                      React UI
```

Node.js không được tự ý train K-Means mỗi request.

## 6. Trạng thái hiện tại

### Đã dựng

- React skeleton.
- Node/Fastify skeleton với `GET /api/health` và placeholder `GET /api/model-info`.
- Python data download/audit/split/prepare.
- Data quality validation.
- Train/validation/test split cố định + manifest.
- Unit tests cho data split/validation và backend skeleton.
- EDA train-only cùng baseline A/B, 140 thí nghiệm K-Means train/validation, profiling và stability.

### Gate 5 đã hoàn thành

- D011 chọn `log1p_standardscaler`, K=2 sau so sánh train/validation và kiểm tra refit trên 352 dòng.
- `models/selection.json` freeze trước final test; model fit train+validation; đánh giá final test 88 dòng đúng một lần (`status=COMPLETE`).
- Artifact serving JSON và Python joblib đã xuất và kiểm tra checksum; portable inference khớp sklearn.

### Chưa làm có chủ đích

- `POST /api/segment`.
- Dashboard thực nghiệm/model card.

## 7. Kiến trúc tài liệu để tiếp tục qua nhiều phiên AI

```text
AGENTS.md
   ↓
docs/AI_HANDOFF.md
   ├── ARCHITECTURE.md
   ├── DECISIONS.md
   ├── NEXT_STEPS.md
   └── TROUBLESHOOTING.md
          ↓
   docs/history/YYYY-MM.md
          ↓
       Git history
```

Nguyên tắc: handoff giữ hiện tại; history giữ quá khứ; Git giữ diff tuyệt đối.
