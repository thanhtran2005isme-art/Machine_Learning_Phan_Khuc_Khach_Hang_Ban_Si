# Gate 9.4 — Frontend Dashboard đúng evidence K-Means

**Trạng thái: COMPLETE / CI VERIFIED — 2026-10-08.**

Mã nguồn: `frontend/src/App.tsx`, `frontend/src/index.css`; bộ kiểm thử: `e2e/customer-flow.spec.ts`.

## Phạm vi triển khai

Giữ nguyên 3 màn hình Giới thiệu, Phân khúc khách hàng, Dashboard. Dashboard lấy `GET /api/dashboard` từ Fastify Gate 9.3 (Backend tự kiểm tra SHA-256 của 6 CSV Gate 9.2 trên mỗi request). Không chạy Python, không fit, không đọc train/test tại Frontend.

| Thành phần giao diện | Nguồn dữ liệu | Nguyên tắc hiển thị |
|---|---|---|
| Elbow, validation silhouette, ARI theo K=2–8 | `experiments` (14 rows: Raw và Log1p/StandardScaler) | Chỉ so sánh inertia trong **cùng preprocessing** |
| Candidate K explorer | `experiments`: inertia, silhouette, ARI, min cluster share | Chọn K2–8 **chỉ xem thí nghiệm**, không thay model serving |
| Quy mô hai cụm | `final_profile.cluster_sizes` | 162/190, 46,02%/53,98% trên 352 development |
| Biểu đồ median 6 biến | `final_profile.median_ratio` | Tỷ lệ với median chung 352 development; đường mốc 1,0; card median gốc từ `cluster_summary` |
| Phân bố Channel | `final_profile.channel_profile` | Bar 100% theo cụm và bảng counts/shares; chỉ profiling |
| Phân bố Region | `final_profile.region_profile` | Bar 100% theo cụm và bảng counts/shares; chỉ profiling |
| Khoảng cách và ngoại lệ | `final_profile.distance_summary` + `outliers` | Biểu đồ P95 và max, bảng median/P95/max/IQR counts; tổng 16 mẫu chỉ gắn cờ |
| Model card | `modelInfo` + `final_profile` | D011/K2, train+validation, SHA model, kiểm chứng 6 CSV |

**Đơn vị:** Chi tiêu tính theo đơn vị tiền tệ gốc từ dataset UCI Wholesale Customers (monetary units); tỷ lệ median không có đơn vị. Không được suy diễn các biến là VND. Khoảng cách Euclidean trong feature space log1p+StandardScaler không phải xác suất hay độ tin cậy.

**Phân biệt 3 phạm vi:** Profile cuối **352 development**; Elbow/Silhouette/ARI là evidence chọn K bằng train/validation trước freeze; `final_test` chỉ là metadata của lần đánh giá test duy nhất trước đó. Không dùng kết quả test để chọn lại K hoặc cập nhật serving.

**Fail closed:** UI kiểm tra sự tồn tại/cấu trúc profile có `read_only=true`, `test_used=false`, 352 mẫu và K2. Nếu API trả 200 nhưng thiếu profile, hiển thị lỗi rõ và không vẽ charts giả. Nếu Backend trả 503 (checksum mismatch hoặc thiếu file), UI giữ trạng thái lỗi; không có fallback giả. Backend chịu trách nhiệm integrity/semantic validation.

**Accessibility/responsive:** Các bar chart có nhãn `role=img` chứa giá trị; bảng Channel/Region/distance có caption và header; chọn K có `aria-pressed`; tài liệu có label và màu phân biệt, không chỉ phụ thuộc màu. Layout được test ở chiều rộng **320px**, bảng có scroll nội bộ, không có horizontal overflow toàn trang.

## Kiểm thử thực tế

- [Gate 6 run 37812065997](https://github.com/thanhtran2005isme-art/Machine_Learning_Phan_Khuc_Khach_Hang_Ban_Si/actions/runs/37812065997) — **SUCCESS**, 15/15 Node serving, 11/11 Fastify, TS/Vite builds, production HTTP smoke.
- [Gate 7 run 37812066044](https://github.com/thanhtran2005isme-art/Machine_Learning_Phan_Khuc_Khach_Hang_Ban_Si/actions/runs/37812066044) — **SUCCESS**, **34/34 Chromium desktop/mobile-emulated E2E**, Python↔Node parity, npm security audit PASS.
- [Gate 8 Windows run 37812066198](https://github.com/thanhtran2005isme-art/Machine_Learning_Phan_Khuc_Khach_Hang_Ban_Si/actions/runs/37812066198) — **SUCCESS**, Windows clean install, 0 vulnerabilities, full Gate6 regression, parity, **34/34 Chromium desktop/mobile-emulated E2E**, `run.bat --ci` FE HTTP 200, modelReady true, K2 API prediction.
- Sáu test Gate9.4 mới (mỗi test chạy ở desktop và mobile): chart median/size đối chiếu API, Channel/Region, distance/outliers, explorer K2–8/Raw/Log, API thiếu final profile, 320px overflow.
- Một lượt test E2E đầu bị lỗi **assertion test string** (32/34, mã nguồn biểu đồ đúng); đã sửa matcher theo định dạng nhãn hai cụm và chạy lại toàn bộ **34/34** trên Linux và Windows. Không bỏ test để xanh CI.

## Không thay đổi

- Bất kỳ file nào trong `models/`, `reports/data/final_profile/`.
- Fit lại scaler/KMeans, đánh giá lại final test, sử dụng Channel/Region khi fit, hay thay API phục vụ `POST /api/segment`.
- Không thêm npm dependencies, không thay đổi workflow CI, không tạo report/slides.

## Chạy local

```powershell
git pull --ff-only origin main
npm ci
npm run test:gate6
```

Nhấp đúp `run.bat`, vào `http://localhost:5173` → Dashboard; thử Raw/Log1p, K2–8, xem tất cả biểu đồ. Để chạy E2E trên Windows:

```powershell
npm install --no-save --package-lock=false @playwright/test@1.56.1
npx playwright install chromium
npm run test:e2e
```

GitHub Windows runner không thay thế thao tác nhấp đúp và cảm nhận UX trên Windows10 của người dùng. **Gate 9.5** sẽ rà soát diễn giải và dữ liệu/model card theo đề; **Gate 9.6** làm full requirement regression & release closure.
