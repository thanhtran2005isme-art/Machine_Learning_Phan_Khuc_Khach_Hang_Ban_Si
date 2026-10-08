# Gate 9.6 — Final Requirement Closure / Code Freeze

**CI VERIFIED.** Không đồng nghĩa đồ án đã nộp đủ hồ sơ học thuật.

## 1. Ma trận yêu cầu 88 mục sau cập nhật

| Trạng thái | Số mục |
|---|---:|
| **PASS** | **57** |
| **PARTIAL** | **16** |
| **MISSING** | **9** |
| **NOT REQUIRED** | **6** |
| **Tổng** | **88** |

Bảng truy vết chi tiết kèm file/API/evidence/lý do từng mục:
[Gate9.6 Markdown](GATE9_6_REQUIREMENTS_MATRIX.md), [CSV](GATE9_6_REQUIREMENTS_MATRIX.csv). Bản Gate9.1 được giữ lại làm baseline lịch sử (**43/29/10/6**).

- **Đã đạt chức năng theo scope kiểm thử:** web 3 màn hình, form 6 biến, API Strict, Elbow/Silhouette/ARI/K explorer, final-profile 352, median chart, Channel/Region, khoảng cách/outliers, Data/Model Card, SHA integrity; không có P0/P1 được CI phát hiện trong phạm vi kiểm thử.
- **Chưa đóng theo đúng đề:** báo cáo 15–25 trang, slide 10–12, phân công và nhật ký 6 tuần / minh chứng đóng góp hai thành viên, giảng viên checkpoint, đối chiếu nguồn bài giảng, khai báo sử dụng AI và xác minh nguyên gốc, nghiệm thu Chrome bằng mắt trên Windows10 cá nhân. Những mục này không bị tùy tiện chuyển PASS.
- **PARTIAL kỹ thuật:** không tái-fit **final** D011 + re-eval final test sau one-shot; giữ quyết định K2 và checksum bất biến. Metadata candidate lịch sử có đường dẫn cá nhân, còn profile serving K2 cuối dùng path tương đối/checksum. Python requirements là range chứ chưa khóa cụ thể toàn bộ transient wheels, cần chú ý khi tái lập lâu dài.

## 2. Cold reproducibility Linux + Windows — SUCCESS

[Gate 9.6 Cold ML CI #37816077339](https://github.com/thanhtran2005isme-art/Machine_Learning_Phan_Khuc_Khach_Hang_Ban_Si/actions/runs/37816077339)

Hai jobs Ubuntu và Windows đều **SUCCESS** từ checkout sạch:

1. Cài `ml/requirements.txt`, tải UCI dataset, xác minh raw SHA-256.
2. Tái tạo **264 train + 88 validation**, xác minh SHA trong frozen `models/selection.json`.
3. Chạy lại đúng **140 train-only KMeans experiments** (Raw/Log × K2–8 × 10 seed), tính **630 pairwise ARI** trong **thư mục tạm**.
4. Đối chiếu schema/khóa/metric với `runs.csv`, `stability_pairs.csv`, `selection_evidence.csv` và **14 review candidates** gốc.
5. Chạy unit tests cho experiment, review, frozen development profile (sklearn joblib ↔ JSON trên 352 development).
6. Xác nhận **không tạo/đọc `test.csv`**, không sửa `models/`, original experiment evidence hoặc `reports/data/final_profile/`.

Bắt được lỗi Windows Python CP1252 (chỉ khi in tiếng Việt), khắc phục bằng `PYTHONUTF8=1`, `PYTHONIOENCODING=utf-8` và phân tách step fail-fast. Sau đó **hai OS đều PASS**. Đây không phải chạy lại final test.

## 3. Full code/API/browser regression — SUCCESS

| Gate trên source Gate9.6 | CI run | Kết quả |
|---|---|---|
| Gate6 API/Frontend | [37816077328](https://github.com/thanhtran2005isme-art/Machine_Learning_Phan_Khuc_Khach_Hang_Ban_Si/actions/runs/37816077328) | 15/15 Node serving, **14/14 Fastify**, FE/BE build, compiled HTTP smoke, npm audit **0** |
| Gate7 Linux E2E/parity | [37816077510](https://github.com/thanhtran2005isme-art/Machine_Learning_Phan_Khuc_Khach_Hang_Ban_Si/actions/runs/37816077510) | **40/40 Playwright**, Python↔Node parity PASS, audit 0 |
| Gate8 Windows | [37816077345](https://github.com/thanhtran2005isme-art/Machine_Learning_Phan_Khuc_Khach_Hang_Ban_Si/actions/runs/37816077345) | Windows clean `npm ci`, 15/15 Node, 14/14 API, **40/40 Chromium**, parity, audit 0, `run.bat --ci` FE HTTP200/modelReady/K2 prediction PASS |
| Gate9.6 ML replay | [37816077339](https://github.com/thanhtran2005isme-art/Machine_Learning_Phan_Khuc_Khach_Hang_Ban_Si/actions/runs/37816077339) | **Linux PASS + Windows PASS**, original 140 + 630 train/validation evidence |

**Bảo mật bổ sung:** `GET /api/model-info` không còn trả `detail` có thể lộ local path khi không load được model; Fastify integration test có kiểm tra phản hồi 503 không chứa đường dẫn nội bộ.

Đối chiếu Git giữa Gate9.5 `7cf0a746492637d48f60531228fe8c615366b962` và mốc code Gate9.6 đã test: **không file nào trong `models/` hay `reports/data/final_profile/` bị đổi**, không có held-out `data/processed/test.csv` trong Git tree. GitHub Windows runner là Windows Server, không phải Windows10 máy cá nhân.

## 4. Scope kiểm soát, lệnh nghiệm thu máy người dùng

```powershell
git status -sb
git pull --ff-only origin main
npm ci
npm run test:gate6
npm audit --audit-level=moderate
```

Nhấp đúp `run.bat` để mở 2 server, truy cập `http://localhost:5173`, vào 3 màn hình; thử 6 feature hợp lệ, thiếu/âm/ngoài khoảng train; khám phá K2–8, biểu đồ Dashboard; đảm bảo K phục vụ **luôn 2**. E2E trên máy local nếu cần theo `docs/GATE9_4_FRONTEND.md`.

**Kỷ luật freeze:** D011 K2 (seed 42), `model.json/joblib`, `selection.json`, `final_evaluation.json` và `reports/data/final_profile/` là evidence không được chỉnh sửa. Không gọi `ml:freeze` hoặc `ml:finalize`.

Sau Gate9.6, ngừng thêm tính năng ngoài đề; chỉ sửa lỗi có bằng chứng và chạy lại gates. Báo cáo/slide/nhóm là phần việc riêng, không được tuyên bố đã hoàn tất.
