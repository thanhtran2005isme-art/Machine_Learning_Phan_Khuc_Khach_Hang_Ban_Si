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
