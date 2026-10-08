# Gate 9.5 — Diễn giải, đơn vị, model/data card

**Trạng thái: COMPLETE — CI VERIFIED, 2026-10-09.**

**Phạm vi:** không có tính năng ML mới; chỉ công bố **nguồn, đơn vị, cấu hình, điều kiện đầu vào và giới hạn suy luận** cho API/UI, cùng tài liệu dữ liệu/mô hình. Không làm báo cáo hoặc slide.

## Audit nguồn gốc

- **UCI ID292** nói rõ chi tiêu **hằng năm**, đơn vị **monetary units (m.u.)**; không khẳng định VND. DOI `10.24432/C5030X`, giấy phép CC BY 4.0. Xem [DATA_CARD](DATA_CARD.md).
- **Model D011** KMeans K2 log1p + StandardScaler, `random_state=42`, `n_init=10`, `max_iter=300`, Lloyd, fit 352, final test một lần 88; thông tin đọc model đã freeze. Xem [MODEL_CARD](MODEL_CARD.md).
- K2 được chọn không chỉ theo silhouette; so sánh cân bằng nhóm, seed stability, outlier và sự ổn định khi refit từ 264 lên 352 trước test. Không phóng đại performance.
- Vùng cảnh báo **min/max feature train 264**, khác outlier **Q3+1.5 IQR theo distance 352**. Cả hai không là xác suất lỗi.
- Chưa có timestamps từng hóa đơn hoặc dữ liệu live; chỉ phân khúc khi có đủ 6 khoản chi tiêu năm. Không áp dụng cho khách chưa có các feature này.
- Có ví dụ request + **response JSON 200 hoàn chỉnh**, được tính từ artifact frozen, tại [GATE9_5_API_EXAMPLES](GATE9_5_API_EXAMPLES.md).

## Source changes

- `GET /api/model-info`: hai object bổ sung `data_card`, `model_card`, không đổi response cũ (backward compatible).
- Giới thiệu: card dữ liệu ngắn, nguồn UCI, đơn vị, năm, ngày đủ điều kiện sử dụng.
- Phân khúc: không nhầm VND, nhắc tính trung tính và khoảng cách không phải confidence.
- Dashboard Model card: seed, n_init, max_iter, Lloyd, lý do K2 và limitations từ API, không hardcode experiment fake data.
- `data/README.md` / `data/data_dictionary.md`: cập nhật unit, thời điểm dùng, mã Channel/Region và thông tin download timestamp.
- Kiểm thử Fastify + smoke + Playwright desktop/mobile đối chiếu response và UI, giữ nguyên previous tests.

## Giới hạn & yêu cầu còn lại

- Model/data cards là **tài liệu kỹ thuật**, chưa thay thế báo cáo 15–25 trang, slide 10–12, nhật ký/phân công đóng góp 2 người bắt buộc khi nộp; người dùng đang hoãn phần này.
- Cold rebuild đầy đủ pipeline ML, phép kiểm từng mục còn thiếu của ma trận 88 thuộc **Gate 9.6**. Không chạy lại final test.
- Thao tác nhấp đúp trên đúng Windows10 của người dùng không thể xác minh từ GitHub CI Windows Server.
- Tài liệu học phần/slide bài giảng do giảng viên cung cấp chưa thấy trong repository, **không tạo trích dẫn giả**.

## Tham khảo

- UCI dataset ID292: https://archive.ics.uci.edu/dataset/292/wholesale%2Bcustomers
- UCI Cardoso (2013): https://doi.org/10.24432/C5030X
- scikit-learn KMeans: https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html
- scikit-learn clustering/metrics: https://scikit-learn.org/stable/modules/clustering.html
- Frozen selection facts: `docs/GATE5_MODEL_SELECTION.md`

## Bằng chứng CI đã nghiệm thu

- [Gate 6 / BE, FE run 37813391195](https://github.com/thanhtran2005isme-art/Machine_Learning_Phan_Khuc_Khach_Hang_Ban_Si/actions/runs/37813391195): SUCCESS, **15/15 Node native serving**, **13/13 Fastify API tests**, TS/Vite builds và compiled production HTTP smoke PASS.
- [Gate 7 / Browser run 37813391072](https://github.com/thanhtran2005isme-art/Machine_Learning_Phan_Khuc_Khach_Hang_Ban_Si/actions/runs/37813391072): SUCCESS, **40/40 E2E desktop/mobile Chromium Linux**, Python ↔ Node frozen sklearn parity PASS, dependency audit 0 vulnerabilities tại thời điểm chạy.
- [Gate 8 / Windows run 37813391303](https://github.com/thanhtran2005isme-art/Machine_Learning_Phan_Khuc_Khach_Hang_Ban_Si/actions/runs/37813391303): SUCCESS, Windows clean install, audit 0 vulnerabilities, 15 Node + 13 API, **40/40 browser tests**, `run.bat --ci` FE HTTP200, Backend modelReady true, K2 prediction 0.
- Bằng chứng local Git diff của Gate 9.5 phải xác nhận `models/` + `reports/data/final_profile/` không đổi. Nhánh chính sau biên bản này chỉ có code UI/API và docs.
- CI Windows là runner Windows Server, **không** thay thế manual thao tác nhấp đúp trên Windows10 cá nhân.

## Historical evidence clarification

- `docs/GATE5_SELECTION.md` ghi quyết định K3 trước final test; đã được gắn **banner SUPERSEDED PRE-TEST**. Văn bản dưới banner lưu nguyên lịch sử cho kiểm toán; quyết định phục vụ thực tế là D011 K2.
- `reports/data/profiles/log1p_standardscaler_k2_seed42/profile_metadata.json` là candidate **train 264** và chứa đường dẫn local `C:\\Users\\...` từ máy tác giả. Đây là **metadata lịch sử**, không dùng để phục vụ web hiện tại; giữ bất biến, không sửa checksum hồi tố. Hồ sơ cuối đang dùng `reports/data/final_profile/` có path tương đối + checksum (Gate9.2).
