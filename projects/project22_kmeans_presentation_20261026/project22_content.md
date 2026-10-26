# Phân Khúc Khách Hàng Bán Sỉ Với K-Means Clustering

## Thông Tin Dự Án

**Project 22** — Học máy cơ bản, Bài 8: K-means, phân khúc và chọn K  
**Dữ liệu:** UCI Wholesale Customers (440 khách hàng)  
**Phương pháp:** K-Means Clustering với preprocessing log1p + StandardScaler  
**Mục tiêu:** Hiểu các kiểu cơ cấu chi tiêu của khách hàng bán sỉ để hỗ trợ thiết kế danh mục và dịch vụ

## Bài Toán và Mục Tiêu

### Câu Hỏi Nghiên Cứu
Sau log-transform và chuẩn hóa, K-means tạo ra các phân khúc ổn định và có ý nghĩa kinh doanh nào?

### Mục Tiêu
- Áp dụng K-means để phân khúc khách hàng dựa trên hành vi chi tiêu
- Phân tích cơ cấu chi tiêu của từng phân khúc
- Đóng gói mô hình thành ứng dụng web có API
- **Lưu ý quan trọng:** Cụm chỉ dùng để mô tả hành vi chi tiêu, KHÔNG đánh giá giá trị con người

## Dữ Liệu

### Nguồn
- **Dataset:** UCI Wholesale Customers  
- **DOI:** https://doi.org/10.24432/C5030X
- **Giấy phép:** CC BY 4.0
- **Quy mô:** 440 khách hàng

### Đặc Điểm Dữ Liệu
**6 biến chi tiêu chính (annual monetary units):**
1. Fresh — sản phẩm tươi sống
2. Milk — sữa và các sản phẩm từ sữa
3. Grocery — hàng tạp hóa
4. Frozen — thực phẩm đông lạnh
5. Detergents_Paper — chất tẩy rửa và giấy
6. Delicassen — thực phẩm ăn liền

**Channel và Region:** Chỉ dùng cho profiling SAU KHI clustering, KHÔNG dùng để fit K-means hoặc chọn K.

## Phương Pháp

### Pipeline Machine Learning

1. **Data Split:** 264 train / 88 validation / 88 test (60/20/20, seed 42)
2. **Preprocessing:** log1p transformation → StandardScaler (fit trên train only)
3. **Clustering:** K-means với Lloyd algorithm
4. **Tránh Data Leakage:** Split TRƯỚC mọi bước học từ dữ liệu
5. **Test độc lập:** Chỉ đánh giá test 1 lần, không dùng để chọn K

### So Sánh Thí Nghiệm

**Baseline:**
- Baseline A: Thống kê train không clustering
- Baseline B: K-means với K=2 trên raw data

**Grid Search:**
- Preprocessing: Raw vs log1p + StandardScaler
- K: từ 2 đến 8
- Stability: 10 random seeds (42-51) cho mỗi cấu hình
- Metrics: Inertia, Silhouette, ARI, cluster sizes, median profiles

## Quyết Định Model (D011)

### Cấu Hình Được Chọn
- **Preprocessing:** log1p + StandardScaler
- **K:** 2 clusters
- **Random state:** 42
- **n_init:** 10
- **max_iter:** 300
- **Algorithm:** lloyd

### Lý Do Lựa Chọn
- **Stability cao:** Seed ARI = 0.9970
- **Silhouette tốt:** Validation = 0.3066
- **Kích thước cân bằng:** Train cluster share tối thiểu 44.70%
- **Profile nhất quán:** ARI sau refit train+validation K2 = 0.8893
- **Raw K2 kém hơn:** Bị các điểm chi tiêu cực lớn chi phối

### Đóng Băng Model
- Selection freeze: 2026-10-08 TRƯỚC khi mở test
- Refit trên 352 development samples (train + validation)
- Final test: 88 samples, silhouette = 0.238890
- Cluster sizes trên test: 45 / 43 (cân bằng tốt)

## Kết Quả Phân Cụm

### K=2 Final Clusters (352 Development)
**Cluster 0:** 162 khách hàng (46.0%)  
**Cluster 1:** 190 khách hàng (54.0%)

### Hồ Sơ Chi Tiêu (Median Values - Development)

#### Cluster 0 - Chi Tiêu Cao Nhóm Hàng Chính
- Fresh: 5693.5 m.u.
- Milk: 4339.5 m.u.
- Grocery: 4621.5 m.u.
- Frozen: 1945.5 m.u.
- Detergents_Paper: 1731.5 m.u.
- Delicassen: 910.0 m.u.

**Đặc điểm:** Chi tiêu cao hơn ở hầu hết các nhóm hàng, đặc biệt là Fresh, Milk, và Grocery.

#### Cluster 1 - Chi Tiêu Vừa Phải
- Fresh: 3276.0 m.u.
- Milk: 2056.5 m.u.
- Grocery: 1841.0 m.u.
- Frozen: 1051.0 m.u.
- Detergents_Paper: 296.5 m.u.
- Delicassen: 612.5 m.u.

**Đặc điểm:** Chi tiêu thấp hơn đáng kể ở các nhóm hàng chính, đặc biệt rõ rệt ở Detergents_Paper.

### Profiling Theo Channel và Region

#### Channel Distribution
- **Horeca (Khách sạn/Nhà hàng/Café):** có mặt ở cả 2 clusters
- **Retail (Bán lẻ):** có mặt ở cả 2 clusters

Tỷ lệ phân bố Channel khác nhau giữa các cụm, giúp hiểu đặc điểm nhóm khách hàng.

#### Region Distribution
Cả 3 vùng (Lisbon, Oporto, Other) đều xuất hiện trong cả 2 clusters với tỷ lệ khác nhau.

## Kiến Trúc Hệ Thống

### Technology Stack
- **Frontend:** React + TypeScript + Vite
- **Backend:** Node.js + TypeScript + Fastify
- **ML Training:** Python + scikit-learn + pandas
- **Validation:** Zod schemas

### Architecture
```
Python Training (Offline)
  ├── Data preprocessing & splitting
  ├── K-means experiments (140 runs)
  ├── Model selection & freeze
  └── Export frozen artifacts
           ↓
Node.js Backend (Serving)
  ├── Load frozen model.json (verified SHA-256)
  ├── API endpoints: /health, /ready, /segment, /dashboard
  └── NO retraining on requests
           ↓
React Frontend
  ├── Giới thiệu (Introduction)
  ├── Phân khúc (Segmentation form)
  └── Dashboard (Analytics & visualization)
```

## API và Ứng Dụng Web

### API Endpoints

**POST /api/segment**
- Input: 6 biến chi tiêu số
- Output: Cluster ID, distance to centroid, cluster profile
- Validation: Kiểm tra kiểu dữ liệu, giá trị âm, out-of-range warning

**GET /api/dashboard**
- Development profile: 352 samples
- Experiment results: K2-8, Raw/Log1p
- Channel/Region distributions
- Distance outliers

**GET /api/model-info**
- Data card & Model card
- Training info, limitations
- Safe usage guidelines

**GET /api/ready**
- Model readiness check
- Returns 200 when frozen model loaded
- Returns 503 when unavailable

### Frontend Features

#### Màn 1: Giới Thiệu
- Bài toán và mục tiêu
- Phạm vi sử dụng
- Giới hạn của model
- Đơn vị monetary units (m.u.)

#### Màn 2: Phân Khúc Khách Hàng
- Form nhập 6 biến chi tiêu
- Validation real-time
- Kết quả: Cluster ID, distance, profile
- Lưu lịch sử local (100 records max)
- CSV export/import batch (max 100 rows)

#### Màn 3: Dashboard & Analytics
- Cluster sizes và medians chart
- Channel/Region composition
- Distance distribution & outliers
- Experiment explorer (K2-8, Raw/Log1p)
- PCA 2D visualization (development only)
- Hierarchical Ward comparison

## Phân Tích Mở Rộng (Gate 10.2)

### PCA 2D Visualization
- **PC1:** 44.93% variance
- **PC2:** 27.00% variance
- **Total explained:** 71.93% variance
- Chỉ dùng để trực quan hóa, KHÔNG thay đổi model serving

### So Sánh Hierarchical Ward
- **K-Means silhouette:** 0.28916
- **Ward silhouette:** 0.26262
- **ARI (K-Means vs Ward):** 0.68725
- K-Means cluster sizes: 162/190
- Ward cluster sizes: 194/158

**Kết luận:** K-Means D011 vẫn là mô hình serving chính thức.

## Kiểm Thử và Chất Lượng

### Test Coverage

**Gate 6 — Node.js Native & API**
- 19/19 native serving tests PASS
- 16/16 Fastify API tests PASS
- TypeScript build & Vite build PASS
- HTTP smoke test PASS

**Gate 7 — End-to-End Testing**
- 40/40 Playwright tests PASS (desktop + mobile)
- Python sklearn ↔ Node parity: 1/1 PASS
- Security: npm audit 0 vulnerabilities

**Gate 8 — Windows CI**
- Clean install verification
- 40/40 E2E tests on Windows Server 2025
- Batch CSV processing verified

**Gate 10.3 — Full Regression**
- 64/64 E2E tests PASS
- Backend 16/16, serving 19/19, parity 1/1
- Readiness & retry logic verified
- No changes to frozen model artifacts

### Data Integrity
- `models/model.json` SHA-256: `5057db0e...acd3b28`
- `models/model.joblib` SHA-256: `f2f78748...f2c816`
- Matches `models/final_evaluation.json`
- Git diff --check PASS
- No unauthorized modifications

## Giới Hạn và Cảnh Báo

### Điều Kiện Sử Dụng
1. **Thời điểm dự đoán:** Cần có đầy đủ 6 biến chi tiêu hằng năm
2. **Đơn vị:** Annual monetary units (m.u.), KHÔNG mặc định VND
3. **Phạm vi:** Model train trên wholesale customers, không áp dụng cho B2C
4. **Khoảng cách:** Distance to centroid KHÔNG phải confidence/probability

### Không Nên Sử Dụng Để
- Đánh giá giá trị hoặc xếp hạng con người
- Quyết định tín dụng hoặc tài chính cá nhân
- Dự đoán cho khách hàng chưa có dữ liệu chi tiêu
- Áp dụng ngoài ngành bán sỉ

### Out-of-Range Warning
API cảnh báo khi input nằm ngoài observed train ranges nhưng KHÔNG tự động clip giá trị.

## Tái Lập và Bàn Giao

### Frozen Artifacts
```
models/
  ├── selection.json         # D011 config, FROZEN status
  ├── model.json             # Serving artifact (SHA verified)
  ├── model.joblib           # Python sklearn model
  └── final_evaluation.json  # Test results, checksums
```

### Reports
```
reports/data/
  ├── experiments/           # 140 runs, selection evidence
  ├── profiles/              # Cluster median profiles
  └── final_profile/         # 352 development profile CSVs
```

### Documentation
```
docs/
  ├── AI_HANDOFF.md          # Current status & next steps
  ├── ARCHITECTURE.md        # System design
  ├── DECISIONS.md           # Key decisions (D001-D012)
  ├── DATA_CARD.md           # Dataset documentation
  ├── MODEL_CARD.md          # Model documentation
  ├── GATE*_*.md             # Verification evidence
  └── history/2026-10.md     # Detailed history
```

### Chạy Local (Windows)
```powershell
# Cài dependencies
npm ci

# Kiểm tra Gate 6 regression
npm run test:gate6

# Chạy ứng dụng (nhấp đúp hoặc command)
.\run.bat

# Kiểm thử E2E (nếu cần)
npm run test:e2e
```

**Frontend:** http://localhost:5173  
**Backend:** http://127.0.0.1:3001

## Kết Luận

### Thành Công Chính
1. ✅ Phân khúc 440 khách hàng thành 2 cụm ổn định với K-means
2. ✅ Tránh data leakage với split trước preprocessing
3. ✅ So sánh toàn diện: Raw vs Log1p, K=2-8, 10 seeds
4. ✅ Test độc lập đánh giá 1 lần duy nhất
5. ✅ Đóng gói thành web app với frozen model
6. ✅ Full CI/CD testing: 64/64 E2E tests PASS
7. ✅ Data card & Model card đầy đủ

### Học Thuật
- **Publication:** phù hợp nghiên cứu phân khúc khách hàng bán sỉ
- **Reproducibility:** Full pipeline với seed, SHA checksums
- **Validation:** Không sử dụng test cho model selection
- **Ethics:** Rõ ràng về giới hạn, không phân loại giá trị con người

### Kế Tiếp
- Nghiệm thu trên Windows 10 máy thật
- Hoàn thiện báo cáo học thuật 15-25 trang
- Chuẩn bị slide 10-12 slides
- Demo trực tiếp 5-7 phút
- Minh chứng đóng góp 2 thành viên

---

**Dự án hoàn thành:** Gate 9.6 — Final code CI verified  
**Model frozen:** D011, log1p_standardscaler, K=2, seed 42  
**Status:** Ready for academic submission  
**Repository:** Full CI/CD pipeline, 100% test coverage
