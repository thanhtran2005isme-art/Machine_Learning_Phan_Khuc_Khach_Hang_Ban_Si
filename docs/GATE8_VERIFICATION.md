# Gate 8 — Final Code Audit và Windows clean install

**Trạng thái: CI VERIFIED / PASS** (2026-10-08).
**Nguồn:** [Windows Gate 8 workflow run 37791339124](https://github.com/thanhtran2005isme-art/Machine_Learning_Phan_Khuc_Khach_Hang_Ban_Si/actions/runs/37791339124), code commit `f94b505e4bed7eb5ac96c3f9019e328d5aa9fdad`. Docs-only changes follow and do not modify serving/ML code.

## Những gì thực tế PASS

| Kiểm tra | Bằng chứng Windows Server 2025 |
|---|---|
| Checkout Git sạch | PASS; không có `node_modules` khi khởi đầu |
| `npm ci` và dependency audit | PASS, 0 advisories được npm báo tại thời điểm chạy |
| Gate 6 regression | Node serving 5/5, Fastify API 9/9, TypeScript/Vite build, compiled HTTP smoke PASS |
| Python sklearn vs Node | Parity test 1/1 PASS trên 6 inputs tổng hợp, không dùng final test |
| Browser automation | Playwright Chromium desktop/mobile simulated 20/20 PASS |
| Luồng form | Nhập 6 biến, nhận cụm/median, invalid input, out-of-range warning, reset, dashboard |
| Race condition | Thay/xóa input trước khi API trả về không còn hiển thị kết quả cũ |
| Missing API | Frontend báo lỗi thay vì hiển thị model giả |
| Batch launcher | `cmd.exe /c run.bat --ci` khởi chạy cả FE/BE; `GET /api/health` modelReady true, FE HTTP 200, POST /api/segment trả cụm 0 hợp lệ |

## Lỗi và vấn đề đã xử lý

1. **Frontend async race:** `frontend/src/App.tsx` dùng request sequence guard; sau khi người dùng xóa/sửa form, response đến muộn không thể ghi đè state. Bổ sung Playwright regression chạy trên cả 2 device presets.
2. **Windows launcher environment:** `run.bat` kiểm tra Node.js >=20, npm và dependency hiện hành; cài lại bằng `npm ci` khi thiếu/hỏng. `--ci` chạy không có các cửa sổ interactive `cmd /k` để nghiệm thu trên runner. Nhấp đúp bình thường không đổi.
3. **CI Windows console:** dùng batch mode `--ci` để tránh runner giữ console của app lâu dài; probe frontend bằng địa chỉ thực tế `http://localhost:5173`, backend qua `http://127.0.0.1:3001`.
4. **Doc conflict:** đã dọn `<<<<<<<` / `=======` / `>>>>>>>` còn sót trong `docs/history/2026-10.md`, giữ kết luận D011 K=2 và chú thích K3 pretest là lịch sử đã rút.
5. **Giữ provenance:** `ml/src/experiment.py` và `ml/src/experiments.py` cùng các tests/evidence lịch sử không bị xóa tùy tiện; frozen artifacts trong `models/` không thay đổi.

## Ranh giới và mức độ nghiệm thu

- **Không thực hiện lại** `ml:freeze`, `ml:finalize`, final test CSV hoặc thay K.
- GitHub runner là **Windows Server 2025 (10.0.26100)**, không phải thiết bị Windows 10 19045 của người dùng. E2E mobile là Chromium emulation, không phải điện thoại thực.
- Mode `--ci` được kiểm tra tự động; cửa sổ `cmd /k` từ thao tác **nhấp đúp run.bat** cần kiểm tra cuối trên máy Windows10 thực tế. Điều kiện này không được suy diễn từ CI.
- npm audit 0 không có nghĩa tất cả rủi ro bảo mật tương lai đều không tồn tại; kiểm tra lại trước khi triển khai công khai.
- Không thêm database/cloud/mobile riêng hoặc báo cáo và slide.

## Kiểm thử nhanh trên Windows 10

Trong PowerShell tại thư mục source:

```powershell
git status -sb
git pull --ff-only origin main
npm ci
npm run test:gate6
npm audit --audit-level=moderate
```

Sau đó nhấp đúp `run.bat`, truy cập `http://localhost:5173`, thử màn hình Phân khúc và Dashboard. Nếu muốn E2E trên Chrome/Chromium máy local:

```powershell
npm install --no-save --package-lock=false @playwright/test@1.56.1
npx playwright install chromium
npm run test:e2e
```

Nếu Windows10 có lỗi, ghi terminal output và screenshot để điều tra; không reset hoặc xóa local source không cần thiết.
