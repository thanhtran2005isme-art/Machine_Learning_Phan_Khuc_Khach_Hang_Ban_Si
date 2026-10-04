# AGENTS.md — Quy tắc đọc và bàn giao dự án cho AI

File này là điểm vào đầu tiên cho ChatGPT/Codex/AI agent khi mở một phiên làm việc mới.

## Thứ tự đọc bắt buộc

1. `AGENTS.md` — quy tắc làm việc và thứ tự đọc.
2. `docs/AI_HANDOFF.md` — trạng thái hiện tại, việc vừa làm, việc kế tiếp, test đã/chưa chạy.
3. `docs/ARCHITECTURE.md` — kiến trúc hệ thống và ranh giới trách nhiệm.
4. `docs/DECISIONS.md` — các quyết định quan trọng và lý do.
5. Tài liệu liên quan trực tiếp đến task hiện tại, ví dụ `docs/NEXT_STEPS.md`, `data/README.md`.
6. `docs/TROUBLESHOOTING.md` nếu task liên quan lỗi môi trường/chạy local.
7. `docs/history/YYYY-MM.md` của tháng hiện tại nếu cần bối cảnh chi tiết.
8. `git log --oneline -20` và diff/commit liên quan khi cần sự thật tuyệt đối về lịch sử mã nguồn.

Không cần đọc toàn bộ lịch sử dự án mỗi lần. `AI_HANDOFF.md` phải đủ ngắn để nắm trạng thái nhanh; chi tiết cũ chuyển vào `docs/history/`.

## Nguồn sự thật ưu tiên

Khi tài liệu và code mâu thuẫn, ưu tiên theo thứ tự:

1. Code + test hiện tại.
2. Git commit/diff.
3. `docs/AI_HANDOFF.md`.
4. `docs/DECISIONS.md` / `docs/ARCHITECTURE.md`.
5. Lịch sử cũ.

Không được khẳng định test PASS nếu chưa thực sự chạy hoặc chưa có log xác nhận.

## Quy tắc cập nhật sau mỗi phiên làm việc có thay đổi

Mỗi phiên có sửa code/tài liệu đáng kể phải cập nhật tối thiểu:

- `docs/AI_HANDOFF.md`: trạng thái mới, việc đã làm, test, blocker, bước kế tiếp.
- `docs/history/YYYY-MM.md`: ghi ngày, commit, file thay đổi, sửa gì, tại sao, cách kiểm chứng.

Chỉ cập nhật thêm khi có liên quan:

- `docs/DECISIONS.md`: khi có quyết định kiến trúc/quy trình mới hoặc thay đổi quyết định cũ.
- `docs/TROUBLESHOOTING.md`: khi gặp lỗi đáng nhớ và đã xác định nguyên nhân/cách xử lý.
- `docs/ARCHITECTURE.md`: khi thay đổi stack, luồng dữ liệu, ranh giới module hoặc serving.

## Quy tắc cho AI_HANDOFF.md

Giữ khoảng dưới 250 dòng nếu có thể. Chỉ giữ thông tin cần cho phiên kế tiếp:

- branch/baseline gần nhất;
- mục tiêu hiện tại;
- đã hoàn thành;
- chưa hoàn thành;
- test/command đã chạy và kết quả;
- quyết định cần nhớ;
- blocker;
- 3–7 bước tiếp theo.

Chi tiết cũ chuyển sang `docs/history/YYYY-MM.md`, không nhồi toàn bộ lịch sử vào handoff.

## Quy ước commit

Ưu tiên Conventional Commits:

- `feat(scope): ...`
- `fix(scope): ...`
- `test(scope): ...`
- `docs(scope): ...`
- `refactor(scope): ...`
- `chore(scope): ...`

Mỗi entry lịch sử nên lưu SHA đầy đủ hoặc SHA ngắn đủ nhận dạng. Nếu entry được viết trong chính commit đang tạo và chưa biết SHA, ghi `PENDING` rồi phiên sau đối chiếu bằng `git log`; Git là nguồn sự thật tuyệt đối.

## Các ràng buộc học thuật không được phá

- Đây là Project 22 — K-Means phân khúc khách hàng bán sỉ.
- 6 biến chi tiêu là feature chính.
- `Channel` và `Region` chỉ dùng profiling sau clustering, không dùng fit chính hay ground truth chọn K.
- Split phải xảy ra trước preprocessing học từ dữ liệu.
- Test độc lập, không dùng để chọn K/tham số.
- Phải so sánh raw với `log1p + StandardScaler`, K=2..8, stability ít nhất 10 seed và profiling cụm.
- Backend không train lại model ở mỗi request; serving dùng artifact đã đóng băng.

## Khi kết thúc một task

Trước khi báo xong, AI phải trả lời được 6 câu:

1. Đã sửa file nào?
2. Vì sao sửa?
3. Có làm thay đổi kiến trúc/quyết định không?
4. Đã chạy command/test nào và kết quả thật là gì?
5. Commit nào chứa thay đổi?
6. Người/AI tiếp theo phải làm gì?
