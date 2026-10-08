# Troubleshooting

Chỉ ghi lỗi có giá trị tái sử dụng. Mỗi mục cần có **triệu chứng → nguyên nhân → cách xử lý → cách xác minh**.

## T001 — PowerShell chặn activate virtual environment

**Triệu chứng**

```powershell
.\.venv\Scripts\Activate.ps1
```

bị chặn bởi ExecutionPolicy.

**Cách xử lý trong terminal hiện tại**

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\.venv\Scripts\Activate.ps1
```

Không cần thay policy toàn máy nếu không cần thiết.

**Xác minh**

```powershell
python --version
python -m pip --version
```

đều trỏ vào môi trường `.venv`.

---

## T002 — `/api/model-info` trả 503 / `modelReady=false` (giai đoạn skeleton cũ)

**Triệu chứng**

- `/api/health`: `modelReady: false`.
- `/api/model-info`: HTTP 503 `not_ready`.

**Nguyên nhân**

Đây từng là hành vi **đúng ở giai đoạn skeleton**. Từ Gate 6, mô hình đã được freeze, endpoint này thông thường trả 200. HTTP 503 hiện nay nghĩa là artifact thiếu/hỏng, SHA-256 không khớp hoặc metadata freeze bị lệch.

**Không sửa bằng cách** hard-code model giả hoặc train model trong request.

**Xác minh**

Trong Gate 6, kiểm tra `models/model.json`, `models/selection.json`, `models/final_evaluation.json`, rồi chạy `npm run test:backend`. Không tự chạy lại final test, không ghi đè frozen model. Test thiếu artifact phải kỳ vọng HTTP 503.

---

## T003 — Artifact trong `reports/` hoặc `models/` không được Git theo dõi

**Lịch sử**

Commit `ed41b6a97a38b4f44cfe5ea61218831a6db0fac5` đã sửa `.gitignore` để chỉ ignore raw/split data tái tạo, còn `reports/` và `models/` có thể track artifact cuối.

**Xác minh**

```bash
git check-ignore -v reports/<file>
git check-ignore -v models/<file>
```

Artifact cuối không nên bị rule tổng quát chặn.

---

## T004 — Frontend build dùng TypeScript project build không phù hợp skeleton

**Lịch sử**

Commit `ef25d72c8afa21b287cf2c0490bb57d44b0cf896` đổi script frontend từ:

```text
tsc -b && vite build
```

sang:

```text
tsc --noEmit && vite build
```

và chuyển Vite/TypeScript/plugin React sang `devDependencies`.

**Xác minh**

```powershell
npm run build
```

Chỉ ghi PASS vào handoff/history sau khi có output chạy thật.

---

## Mẫu mục mới

```markdown
## T0XX — Tên lỗi

**Ngày / commit:** ...

**Triệu chứng**
...

**Nguyên nhân gốc**
...

**Cách xử lý**
...

**Cách xác minh**
...

**File liên quan**
...
```
