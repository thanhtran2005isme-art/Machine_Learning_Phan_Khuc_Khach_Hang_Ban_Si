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

## D011 — Chọn K=2 log1p + StandardScaler và freeze (Gate 5)

- **Trạng thái:** Accepted, 2026-10-08, trước final test.
- **Quyết định:** `log1p_standardscaler`, K=2, `random_state=42`, `n_init=10`, `max_iter=300`, `algorithm=lloyd`; chỉ fit 6 feature chi tiêu. Cấu hình cuối tại `models/selection.json` có SHA-256 evidence train/validation.
- **Lý do:** K2 log ổn định seed (ARI 0.9970), silhouette validation 0.3066, min train share 44.70%, profile Grocery/Detergents và Fresh/Frozen nhất quán; refit trên 352 development cho phân hoạch ARI 0.8893 so với mô hình train-only. Dù K3 mô tả 3 profile tốt trên train/validation, ARI khi refit K3 chỉ 0.3343 và hai nhóm Grocery cao chồng lấn về diễn giải. Raw K2 silhouette 0.6103 nhưng validation 81/7, top 1% inertia 25.33%.
- **Hệ quả:** Freeze trước khi mở test; refit `log1p` + scaler + KMeans trên train+validation (352), sau đó đánh giá final test 88 **một lần** và xuất chính mô hình đã đánh giá thành joblib/JSON. Final test không đổi cấu hình, không fit, không chọn policy. Kết quả test chỉ báo cáo, không quay lại model selection. BE/FE thuộc gate sau.
- **Chi tiết bằng chứng:** `docs/GATE5_MODEL_SELECTION.md`. Freeze K3 sơ bộ đã được rút trước khi mở test và lưu tại `models/selection_k3_retracted_pretest.json` để kiểm toán; quyết định cuối là K2. Channel/Region chỉ hậu phân cụm; không dùng làm nhãn chọn K; không loại outlier.
- **Kết quả sau freeze (chỉ báo cáo, không điều chỉnh quyết định):** final test độc lập đúng một lần 88 dòng, silhouette 0.238890, inertia/row 4.505144, cụm 45/43; evaluation `COMPLETE`. Artifact `models/model.json` và `models/model.joblib` lấy từ mô hình fit development 352 dòng. SHA-256 lưu trong `models/final_evaluation.json`; không đánh giá lại test.

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
