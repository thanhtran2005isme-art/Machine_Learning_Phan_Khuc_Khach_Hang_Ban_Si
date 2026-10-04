# Bước tiếp theo sau skeleton + data pipeline

Không chạy K-Means ngay cho đến khi các cổng dưới đây PASS.

## Gate A — môi trường

```powershell
npm install
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r ml/requirements.txt
```

## Gate B — dữ liệu

```powershell
python ml/src/prepare_data.py
python -m pytest ml/tests -q
```

Cần xác nhận:

- raw có đúng 440 dòng;
- đúng 8 cột kỳ vọng;
- không missing/NaN/inf;
- không giá trị chi tiêu âm;
- Channel chỉ thuộc {1,2};
- Region chỉ thuộc {1,2,3};
- train/validation/test không chồng lấn;
- số dòng 264/88/88;
- manifest ghi seed và checksum;
- chưa có preprocessing học từ full data.

## Gate C — skeleton web/backend

Terminal 1:

```powershell
npm run dev:backend
```

Terminal 2:

```powershell
npm run dev:frontend
```

Mở `http://localhost:5173` và xác nhận backend báo `status=ok`, `modelReady=false`.

## Sau khi A/B/C PASS

Bước kế tiếp là **EDA chỉ trên train**:

1. Phân bố 6 biến chi tiêu.
2. Skewness và biểu đồ trước/sau `log1p` (chỉ fit/quyết định trên train).
3. Median/IQR của train.
4. Kiểm tra outlier để mô tả, chưa tự động loại.
5. Đóng băng kế hoạch baseline và thí nghiệm trước khi dùng test.

Sau EDA mới bắt đầu baseline và K-Means K=2..8.
