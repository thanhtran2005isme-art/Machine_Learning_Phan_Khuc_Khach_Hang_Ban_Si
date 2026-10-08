# Gate 7 — Kiểm thử Web/API/Model tích hợp

**Source:** Gate 5 D011 `models/model.json` K=2 immutable; không chạy lại `ml:finalize`, không mở `data/processed/test.csv`.

## Checklist

1. Playwright headless Chromium desktop và Pixel 5 emulation: intro, navigation, form happy path, input thiếu/âm, out-of-train warning, reset, dashboard 14 candidates/raw-vs-log charts, API 503 và responsive overflow.
2. Backend Fastify & Node-native regression test từ Gate 6 không suy giảm.
3. Python joblib sklearn → Node JSON portable parity trên sáu trường hợp tổng hợp chỉ dùng model đã lưu; không đọc dữ liệu test.
4. TypeScript/Vite/backend builds và production HTTP smoke Gate 6.
5. Dependency audit chi tiết trong CI; chỉ nâng dependency nếu cập nhật lockfile và kiểm thử đi kèm, không `npm audit fix --force` mù.
6. Browser test artifacts chỉ upload khi fail; tuyệt đối không để screenshot giả làm evidence.

## Chạy trên máy dev Windows

```powershell
npm ci
npm install --no-save --package-lock=false @playwright/test@1.56.1
npx playwright install chromium
npm run test:parity
npm run test:e2e
npm run test:gate6
```

Các lệnh `test:e2e` tự khởi chạy BE/FE ở 3001/5173 khi cổng trống; khi đang chạy `run.bat` có thể dùng lại server, cần bảo đảm server chạy bản code mới. `npm install --no-save` chỉ dùng Playwright test runner, **không sửa package-lock.json**, không cần Playwright ở runtime demo. Test parity cần Python đã cài scikit-learn, joblib và numpy.

## Trạng thái nghiệm thu — CI Verified (2026-10-08)

**Gate 7 CI:** [run 37789072891](https://github.com/thanhtran2005isme-art/Machine_Learning_Phan_Khuc_Khach_Hang_Ban_Si/actions/runs/37789072891) SUCCESS.

- `npm ci`: PASS.
- `npm audit --audit-level=moderate`: PASS, **0 vulnerabilities** theo dữ liệu npm tại thời điểm chạy.
- `npm run build`: PASS cho backend TypeScript và frontend TypeScript/Vite.
- `npm run test:parity`: 1/1 PASS, 6 vectors tổng hợp so sánh nhãn cụm và khoảng cách Python sklearn vs Node JSON.
- `npm run test:e2e`: **18/18 PASS** trên desktop Chromium + Pixel 5 Chromium emulation (9 kịch bản × 2 viewport).
- Audit sau cài Playwright test runner cũng báo 0 moderate/high/critical.
- **Gate 6 regression:** [run 37789072881](https://github.com/thanhtran2005isme-art/Machine_Learning_Phan_Khuc_Khach_Hang_Ban_Si/actions/runs/37789072881) SUCCESS.
- Đã nâng `backend` Vitest từ dòng major 3 lên `^5.0.3`; `package-lock.json` được npm CI trial tạo và thử nghiệm cùng Gate 6, sau đó commit; xóa workflow trial. Không dùng `--force`.
- Artifact model Gate 5 không thay đổi, không chạy final evaluation, không đọc final test CSV.

**Giới hạn nghiệm thu:** Chromium ở CI Linux, mobile chỉ là chế độ giả lập thiết bị; chưa thử thao tác trên thiết bị vật lý hoặc Windows Chrome của người dùng. Không khẳng định đã tối ưu production security toàn hệ sinh thái chỉ vì audit hiện tại bằng 0.

**Next:** Gate 8 — final clean-environment/code audit và nghiệm thu Windows/browser thực; không mở rộng ML hoặc làm báo cáo trong bước này.
