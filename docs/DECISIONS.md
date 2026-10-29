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

- **Trạng thái:** Accepted/FROZEN, 2026-10-08, trước final test.
- **Quyết định:** `log1p_standardscaler`, K=2, `random_state=42`, `n_init=10`, `max_iter=300`, `algorithm=lloyd`; chỉ sáu biến chi tiêu.
- **Lý do:** seed ARI 0.9970, validation silhouette 0.3066, train cluster share tối thiểu 44.70%, profile nhất quán; ARI sau refit train+validation K2=0.8893 so với K3=0.3343. Raw K2 bị các điểm xa chi phối rõ rệt.
- **Hệ quả:** `models/selection.json` đã freeze trước khi mở test. Sau đó fit lại trên 352 mẫu development, đánh giá test 88 mẫu đúng một lần (silhouette 0.238890), xuất `models/model.json` và `models/model.joblib` từ cùng fitted model. Không mở lại test hoặc thay K dựa trên test.
- **Nguồn:** `docs/GATE5_MODEL_SELECTION.md`; `models/final_evaluation.json` status COMPLETE. `models/selection_frozen.json` K3 và `docs/GATE5_SELECTION.md` phản ánh đề xuất cũ đã rút trước test, **không phải cấu hình serving**.

## D012 — Gate 6 serving qua frozen JSON, giao diện không retrain

- **Trạng thái:** Accepted, 2026-10-08.
- **Quyết định:** Fastify nạp và kiểm tra SHA-256 `models/model.json` theo `models/final_evaluation.json`; đối chiếu `models/selection.json` D011. Suy luận log1p → StandardScaler → Euclidean nearest centroid; lỗi checksum/schema trả service unavailable. Dashboard lấy experiment evidence và metadata final evaluation (read-only); không đọc final test CSV.
- **Lý do:** cùng mô hình với Python, phù hợp serving Node.js đã chọn; không tạo pipeline huấn luyện trực tuyến hay dữ liệu giả.
- **Hệ quả:** API chỉ nhận sáu số không âm hữu hạn; outside observed train ranges cảnh báo nhưng không tự clip. Frontend ba màn hình React đọc API. Không sửa artifact Gate 5.



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

## D012 — PCA/Ward là phân tích mở rộng, không phải model selection
- **Status:** Accepted (optional coursework extension).
- **Reason:** Đề cho phép PCA2D và so sánh Hierarchical; cần mô hình diễn giải có bằng chứng nhưng tránh nhìn 2D rồi suy diễn hiệu quả 6D.
- **Decision:** frozen D011 K2 serving duy nhất; PCA fit 352 development sau biến đổi frozen D011 chỉ để vẽ; Ward fit 352 development trong không gian Euclidean 6D, không dùng Channel/Region, final test hoặc 2D points để tạo nhãn.
- **Consequences:** benchmark chỉ mô tả trên development, không chọn lại D011; ARI/contingency không phụ thuộc tên cụm; artifact mới có SHA và không thay models/.
- **Evidence:** docs/GATE10_2_PCA_HIERARCHICAL.md và Gate 10.2 CI.
