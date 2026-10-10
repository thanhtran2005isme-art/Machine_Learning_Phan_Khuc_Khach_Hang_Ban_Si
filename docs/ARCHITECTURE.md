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

### Machine Learning / Gate 3–5

- Data audit, split 264/88/88, train-only EDA, baseline, 140 K-Means runs và 630 ARI comparisons đã hoàn thành.
- D011: model cuối `log1p_standardscaler` + K=2, fit development 352 khách, final test 88 khách đánh giá đúng một lần và đã COMPLETE.
- `models/selection.json`, `models/model.json`, `models/model.joblib` canonical; checksum và frozen metadata được giữ nguyên.

### Serving Web & API / Gate 6–7

- Fastify `GET /api/health`, `GET /api/model-info`, `GET /api/dashboard`, `POST /api/segment` đã hoàn thiện; không chạy train khi request.
- React/Vite ba màn hình Giới thiệu, Phân khúc và Dashboard đã kết nối API thực.
- Gate 6 CI: TypeScript/Vite build + 5 native tests + 9 API tests + production HTTP smoke PASS.
- Gate 7 CI: 18 Playwright E2E desktop/mobile PASS; Python sklearn joblib ↔ Node portable parity PASS trên 6 synthetic vectors; security audit sau nâng Vitest5 không còn advisory được npm báo. Xem `docs/GATE7_VERIFICATION.md`.
- Chưa thực hiện manual Chrome Windows thật hoặc deployment công khai.

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

## Gate 10.2 — Kiến trúc PCA/Ward development-only
- Ngoài luồng inference, Python offline dùng frozen D011 scaler và chỉ 352 dòng train+validation kiểm SHA. PCA hai chiều để chiếu hình, Agglomerative Ward so sánh 6D, không chọn lại mô hình.
- Artifact read-only: reports/data/development_extension/analysis.json và metadata.json; backend endpoint GET /api/development-extension xác minh SHA/provenance và trả 503 độc lập khi thiếu evidence.
- Frontend trực quan hóa scatter/contingency/ARI; API /api/segment vẫn dùng KMeans D011 và không fit trên request; final test độc lập không được truy cập.
