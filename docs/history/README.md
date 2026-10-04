# History — nhật ký thay đổi dài hạn

Mỗi tháng dùng một file `YYYY-MM.md` để tránh `AI_HANDOFF.md` phình to.

## Mục đích

History trả lời:

- phiên trước đã sửa gì;
- commit nào chứa thay đổi;
- tại sao thay đổi;
- test/command nào đã chạy;
- còn việc gì dang dở.

Git vẫn là nguồn sự thật tuyệt đối cho diff.

## Mẫu entry

```markdown
## YYYY-MM-DD — tiêu đề ngắn

- **Commit:** `SHA` hoặc `PENDING`
- **Mục tiêu:** ...
- **File chính:** `a`, `b`, `c`
- **Thay đổi:**
  - ...
  - ...
- **Lý do:** ...
- **Kiểm chứng đã chạy:**
  - `command` → PASS / FAIL / NOT RUN
- **Kết quả:** ...
- **Còn lại:** ...
- **Tài liệu cập nhật:** AI_HANDOFF / DECISIONS / TROUBLESHOOTING / ARCHITECTURE
```

## Quy tắc

- Không ghi `PASS` nếu không có kết quả chạy thật.
- Khi một phiên có nhiều commit liên quan cùng mục tiêu, có thể ghi một entry và liệt kê nhiều SHA.
- Nếu commit hiện tại chưa có SHA vì entry được tạo trong cùng commit, ghi `PENDING`; phiên sau đối chiếu `git log` và bổ sung khi cần.
- Không copy nguyên diff dài vào history; ghi ý nghĩa của thay đổi, rồi trỏ commit.
