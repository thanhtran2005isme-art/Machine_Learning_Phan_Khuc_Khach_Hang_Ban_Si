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

## Trạng thái nghiệm thu

- Chưa ghi PASS trước log CI thực tế.
- Không khẳng định đã kiểm thử trên Chrome Windows người dùng nếu mới chạy GitHub Actions Ubuntu.
- Nếu CI fail: phân loại source bug, test bug hoặc môi trường, sửa rồi chạy lại.
