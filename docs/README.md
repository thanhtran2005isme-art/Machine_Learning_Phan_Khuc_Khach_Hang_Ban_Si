# Tài liệu dự án

Thư mục `docs/` được tổ chức để một phiên ChatGPT/AI mới có thể hiểu nhanh phiên trước đã làm gì mà không phải đọc toàn bộ lịch sử.

## Sơ đồ

```text
AGENTS.md
   │
   ▼
docs/AI_HANDOFF.md       ← trạng thái hiện tại, đọc đầu tiên sau AGENTS
   │
   ├── docs/ARCHITECTURE.md    ← hệ thống được chia như thế nào
   ├── docs/DECISIONS.md       ← tại sao chọn cách làm hiện tại
   ├── docs/NEXT_STEPS.md      ← gate/task tiếp theo của giai đoạn hiện tại
   └── docs/TROUBLESHOOTING.md ← lỗi đã gặp, nguyên nhân, cách xử lý
             │
             ▼
      docs/history/YYYY-MM.md  ← nhật ký chi tiết theo tháng
             │
             ▼
          Git history          ← nguồn sự thật tuyệt đối về commit/diff
```

## Thứ tự đọc cho phiên mới

1. `../AGENTS.md`
2. `AI_HANDOFF.md`
3. `ARCHITECTURE.md`
4. `DECISIONS.md`
5. Tài liệu liên quan task (`NEXT_STEPS.md`, `../data/README.md`, ...)
6. `TROUBLESHOOTING.md` nếu có lỗi
7. `history/YYYY-MM.md` và `git log` khi cần chi tiết

## Vai trò từng file

| File | Vai trò | Tần suất cập nhật |
|---|---|---|
| `AI_HANDOFF.md` | Trạng thái hiện tại và bước kế tiếp | Mỗi phiên có thay đổi đáng kể |
| `ARCHITECTURE.md` | Kiến trúc và ranh giới module | Khi kiến trúc thay đổi |
| `DECISIONS.md` | Quyết định + lý do + hệ quả | Khi có quyết định mới |
| `NEXT_STEPS.md` | Checklist/gate gần nhất | Khi chuyển giai đoạn |
| `TROUBLESHOOTING.md` | Lỗi đáng nhớ + cách xử lý | Khi gặp/sửa lỗi |
| `history/YYYY-MM.md` | Nhật ký thay đổi theo ngày/commit | Mỗi phiên/commit đáng kể |

## Quy tắc chống trùng lặp

- `AI_HANDOFF.md` chỉ giữ **hiện tại**.
- `history/` giữ **quá khứ chi tiết**.
- `DECISIONS.md` giữ **lý do ra quyết định**, không phải nhật ký mọi thay đổi.
- `TROUBLESHOOTING.md` chỉ giữ lỗi có giá trị tái sử dụng.
- Git lưu diff tuyệt đối; tài liệu chỉ giải thích ý nghĩa của diff.
