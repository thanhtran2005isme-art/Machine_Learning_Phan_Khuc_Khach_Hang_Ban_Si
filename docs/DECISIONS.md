# Decisions — các quyết định cần nhớ

File này lưu **quyết định và lý do**, không phải nhật ký mọi commit.

## D001 — Frontend dùng React + TypeScript + Vite

- **Trạng thái:** Accepted
- **Lý do:** phù hợp yêu cầu web, tách frontend rõ với backend, setup nhẹ và dễ demo local.
- **Hệ quả:** UI/dashboard/form nằm trong `frontend/`; không dùng Next.js ở giai đoạn hiện tại.

## D002 — Backend dùng Node.js + TypeScript + Fastify

- **Trạng thái:** Accepted
- **Lý do:** người dùng chốt Node.js backend; Fastify gọn, phù hợp API local và test injection.
- **Hệ quả:** API/validation/serving nằm trong `backend/`.

## D003 — ML vẫn dùng Python + scikit-learn

- **Trạng thái:** Accepted
- **Lý do:** đây là bài học máy; scikit-learn phù hợp K-Means, Pipeline, StandardScaler, metric và tái lập thí nghiệm.
- **Hệ quả:** Node không thay Python ở bước train/evaluate.

## D004 — Training và serving tách biệt

- **Trạng thái:** Accepted
- **Lý do:** đề yêu cầu app nạp model/pipeline đã lưu, không train lại mỗi request.
- **Hệ quả:** Python đóng băng artifact; Node chỉ load và serve artifact.

## D005 — Split mặc định 60/20/20 với seed 42

- **Trạng thái:** Accepted for implementation, có thể xem xét lại trước khi thí nghiệm nếu có lý do học thuật.
- **Lý do:** tách rõ train/validation/test và tái lập được.
- **Lưu ý:** 60/20/20 là quyết định của nhóm, **không phải tỷ lệ bắt buộc của đề**.
- **Hệ quả:** hiện kỳ vọng 264/88/88 cho 440 dòng.

## D006 — Channel/Region chỉ dùng profiling

- **Trạng thái:** Non-negotiable theo đề.
- **Lý do:** không được dùng hai biến này làm ground truth hoặc feature fit chính để chọn K.
- **Hệ quả:** K-Means chính chỉ dùng 6 biến chi tiêu.

## D007 — Outlier chỉ phát hiện/báo cáo ở data audit

- **Trạng thái:** Accepted ở giai đoạn hiện tại.
- **Lý do:** không được tự ý xóa/winsorize trước khi có thiết kế thí nghiệm và bằng chứng.
- **Hệ quả:** audit có IQR report nhưng không tự động loại record.

## D008 — Raw/processed data tái tạo, reports/models cuối được track

- **Trạng thái:** Accepted
- **Lý do:** raw/split có thể tái tạo bằng script; assignment cần evidence/model artifacts cho bàn giao.
- **Hệ quả:** `.gitignore` bỏ qua `data/raw/*`, `data/processed/*`; không bỏ qua toàn bộ `reports/` và `models/`.

## D009 — Tài liệu continuity cho AI theo mô hình handoff + history

- **Trạng thái:** Accepted
- **Lý do:** phiên ChatGPT mới cần hiểu nhanh phiên trước mà không đọc toàn bộ chat hoặc lịch sử Git.
- **Cấu trúc:** `AGENTS.md` → `docs/AI_HANDOFF.md` → `ARCHITECTURE.md` / `DECISIONS.md` / task docs → `history/` → Git.
- **Hệ quả:** mỗi phiên có thay đổi đáng kể phải cập nhật handoff và history.

## D010 — Cố định protocol baseline/K-Means trước lựa chọn mô hình

- **Trạng thái:** Accepted, 2026-10-08.
- **Quyết định:** baseline A thống kê train; baseline B raw K=2 seed42; grid raw / log1p + StandardScaler × K=2..8 × seed42..51 với `n_init=10`, `algorithm=lloyd`.
- **Lý do:** đủ 140 cấu hình không trùng, so sánh và tái lập; dựa trên EDA train nhưng chưa chọn trước phương pháp.
- **Hệ quả:** chỉ fit trên train; validation chỉ transform/predict; test giữ kín; so sánh inertia chỉ trong cùng không gian, dùng silhouette/ARI/cluster size/profile để đánh giá. Xem `docs/EXPERIMENTS.md`.

## D011 — Chọn cấu hình K-Means sau Gate 5 (đã freeze)

- **Trạng thái:** Accepted/FROZEN, 2026-10-08; quyết định chỉ dựa trên train/validation, chưa đọc final test.
- **Preprocessing:** `log1p` sáu biến chi tiêu, sau đó `StandardScaler`.
- **Model:** `KMeans(n_clusters=3, random_state=42, n_init=10, max_iter=300, algorithm="lloyd")`.
- **Features đúng thứ tự:** `Fresh`, `Milk`, `Grocery`, `Frozen`, `Detergents_Paper`, `Delicassen`. `Channel` và `Region` chỉ dành cho profiling sau fit.
- **Lý do:** K=3 cho ba kiểu chi tiêu khác biệt và nhất quán train/validation (Grocery/Detergents cao; chi tiêu thấp; Fresh/Frozen cao). Silhouette validation=0.2165, ARI mean=0.9078, cluster train=91/73/100; không có cụm <5%. Chấp nhận độ phân tách/stability thấp hơn log K=2 (silhouette validation=0.3066, ARI=0.9970) để giữ phân khúc Fresh/Frozen riêng biệt có ý nghĩa kinh doanh.
- **Loại raw K=2:** ảnh hưởng điểm xa lớn (top 1% đóng góp 25.33% train inertia), cụm lệch 217/47; các giá trị inertia không so sánh giữa không gian raw và scaled.
- **Policy sau freeze:** fit lại scaler và K-Means trên `train+validation` (352 dòng) theo đúng config đã chốt, sau đó mới được mở final test (88 dòng) để đánh giá một lần, không dùng để chỉnh cấu hình. Lưu pipeline và metadata/model artifact. Nếu test yếu, ghi nhận kết quả; không chọn lại từ test.
- **Nguồn bằng chứng:** `docs/GATE5_SELECTION.md` và `models/selection_frozen.json`. `experiment_metadata.json` Gate 4 giữ `selection_status=NOT_SELECTED` để phản ánh trạng thái lịch sử tại lúc chạy 140 thí nghiệm.
- **Chưa thực hiện tại thời điểm freeze:** chưa mở test, chưa chạy final refit/evaluation, chưa xuất fitted model artifact, chưa sửa BE/FE.

## Cách thêm quyết định mới

Dùng mẫu:

```markdown
## D0XX — Tên quyết định

- **Trạng thái:** Proposed / Accepted / Superseded
- **Bối cảnh:** vấn đề cần quyết định
- **Quyết định:** đã chọn gì
- **Lý do:** vì sao
- **Hệ quả:** ảnh hưởng code/test/report
- **Thay thế:** D0YY nếu supersede quyết định cũ
```
