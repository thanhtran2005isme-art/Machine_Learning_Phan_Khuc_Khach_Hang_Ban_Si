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

## 5. Kiến trúc serving thực tế

Python đã huấn luyện/đánh giá và đóng băng model ở Gate 5. Backend ở Gate 6 đọc JSON serving tại startup, xác minh checksum và D011; không retrain:

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

- API `POST /api/segment`, `GET /api/dashboard`, `GET /api/model-info` đã có source và validation.
- React 3 màn hình đã có source và kết nối API; xem Gate 6 CI/local test evidence để xác nhận runtime.

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

## Gate 6 — Ranh giới tích hợp

- `backend/model.mjs` đọc `models/model.json` SHA256 phải khớp `models/final_evaluation.json`; `models/selection.json` bắt buộc D011 K2. Bản K3 `models/selection_frozen.json` là lưu trữ lịch sử, không dùng runtime.
- API nhận đúng sáu biến chi tiêu số không âm, không coercion; trả cụm, distances trong không gian scaled và hồ sơ median gốc.
- Dữ liệu dashboard là artifacts K sweep đã commit; final evaluation metadata chỉ hiển thị, không tính lại test.
- Frontend Vite /api proxy tới Fastify 127.0.0.1:3001. Không có database.
