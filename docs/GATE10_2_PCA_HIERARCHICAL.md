# Gate 10.2 — PCA 2D và Hierarchical Ward, Project 22

## Nguồn dữ liệu và phạm vi
- Chỉ dùng UCI Wholesale Customers; train 264 và validation 88 được tạo lại theo frozen SHA từ models/selection.json, kiểm tra bởi ml/src/final_profile.py::load_development.
- Không dùng test.csv; không đọc/chạy lại final test một lần đã khóa. Channel/Region chỉ dùng hậu phân cụm, không đưa vào fit PCA/Ward.
- Tính log1p cho sáu nhóm chi tiêu, sau đó transform bằng mean/scale đã đóng băng của D011. Không fit lại KMeans hoặc StandardScaler.
- PCA(n_components=2, svd_solver=full) FIT trên 352 development đã transform, chỉ để trực quan hóa. Không thay 6D bằng 2D ở API gán cụm.
- Ward AgglomerativeClustering(n_clusters=2, linkage=ward, metric=euclidean) FIT trên cùng 6D, tính ARI/contingency/silhouette theo 352 development. Đây là benchmark mô tả, không lựa chọn lại mô hình đã freeze.

## Kết quả phân tích thực tế
| Chỉ số | Frozen D011 KMeans | Hierarchical Ward |
|---|---:|---:|
| Số cụm | 2 | 2 |
| Kích thước cụm | 162 / 190 | 194 / 158 |
| Silhouette 6D trên 352 development | 0.2891582149 | 0.2626204724 |

- ARI = 0.6872488321 (không phụ thuộc hoán vị ID).
- Contingency matrix (hàng KMeans 0,1 × cột Ward 0,1): [[17,145],[177,13]].
- PCA PC1 explained variance 44.9266445%, PC2 26.9998676%, cộng 71.9265121%. Khoảng cách 2D không thay thế khoảng cách/metric trong 6D; silhouette không chứng minh hiệu quả kinh doanh.

## Artifact và bảo vệ integrity
- ml/src/development_extension.py tải dữ liệu phát triển đã kiểm SHA, tính offline rồi xuất reports/data/development_extension/analysis.json (352 điểm thật: index, split, pc1, pc2, kmeans, hierarchical) và metadata.json (SHA + frozen provenance).
- CI offline gate10-2-evidence.yml: Linux chạy pytest test_development_extension.py và test_final_profile.py, tạo 2 lần so bytes, xác minh không có test.csv và không sửa frozen artifacts; lưu artifact và commit **chỉ phần dữ liệu** lên feature branch.
- Backend/development-extension.mjs kiểm SHA, source hashes với frozen selection, cấu trúc 352 điểm, orthogonality PCA, số lượng cụm, silhouette D011 và tự tính ARI từ contingency. API GET /api/development-extension trả evidence read-only, lỗi trả 503 không lộ đường dẫn, không vô hiệu hóa phân khúc D011.
- Frontend/DevelopmentAnalytics.tsx hiển thị scatter có đủ 352 điểm, lọc train/validation, đổi màu nhãn KMeans/Ward, % phương sai, so silhouette, ARI và ma trận, các hệ số PCA. Giao diện không fit/đoán dữ liệu.

## Chạy lại development-only
1. Cài môi trường: python -m pip install -r ml/requirements.txt
2. Tải/audit UCI: python -m ml.src.download_data
3. Tạo train và validation: python -m ml.src.prepare_development_only
4. Chạy test: python -m pytest ml/tests/test_development_extension.py -q
5. Xuất: python -m ml.src.development_extension
6. API/UI: npm ci; npm run test:gate6; mở run.bat, vào Dashboard.

Tuyệt đối không dùng ml:freeze, ml:finalize hoặc final test để chọn lại mô hình. Việc đánh giá trong tài liệu này chỉ chứng minh phạm vi phát triển.

## Trạng thái
- Offline CI run 38037496861: SUCCESS, artifact thật đã commit SHA fb7ebf11.
- Gate 10 pull request CI Linux/Windows phải xem job cuối cùng để xác nhận trước merge; không tự nhận PASS khi chưa có kết quả.

## Đối chiếu số học giữa hệ điều hành

- Git giữ đúng SHA-256 của artifact gốc, API không chấp nhận artifact bị sửa.
- Replay PCA trên runner khác có thể lệch khoảng 1e-15 do SVD/BLAS floating point; không yêu cầu SHA artifact mới giống byte-for-byte giữa các môi trường.
- ml/src/verify_development_extension.py so sánh ngữ nghĩa: provenance/hash gốc chính xác, frozen labels và Ward partition giống nhau (ARI=1), PCA components/points so với hai dấu trục với tolerance 1e-8 và chỉ số trong 1e-10.
- Windows parity test yêu cầu PYTHON=python để dùng đúng môi trường setup-python, thay vì Windows py -3 launcher có thể trỏ sang Python không có joblib.
