# PROJECT 22 — Phân khúc khách hàng bán sỉ theo cơ cấu chi tiêu

> Học phần: **Học máy cơ bản**  
> Chủ đề: **Bài 8 — K-means, phân khúc và chọn K**  
> Dữ liệu: **Wholesale customers**  
> Hình thức: **Nhóm 02 sinh viên**  
> Thời gian: **06 tuần**

---

## 1. Mục tiêu đề tài

Nhà phân phối muốn hiểu các **kiểu cơ cấu chi tiêu của khách hàng bán sỉ** để hỗ trợ thiết kế danh mục và dịch vụ. Cụm chỉ được dùng như một công cụ mô tả hành vi chi tiêu, **không được dùng như nhãn đánh giá giá trị con người**.

### Câu hỏi nghiên cứu

> Sau `log-transform` và chuẩn hóa, K-means tạo ra các phân khúc ổn định và có ý nghĩa kinh doanh nào?

### Mục tiêu học tập bắt buộc

- Vận dụng đúng kiến thức về **K-means, phân khúc và chọn K**.
- Giải thích được giả định, ưu điểm và hạn chế của K-means.
- Xây dựng pipeline có thể chạy lại từ dữ liệu thô đến kết quả.
- Giữ **test độc lập**, không dùng test để chọn mô hình hoặc tham số.
- So sánh với baseline đơn giản.
- Phân tích kết quả và các trường hợp bất thường thay vì chỉ đưa ra một metric.
- Đóng gói mô hình thành **ứng dụng web có API**.
- Có validation đầu vào, model card và thông tin giới hạn của mô hình.
- Hai thành viên có đóng góp cân bằng, thể hiện bằng Git history, nhật ký và phần vấn đáp.

---

## 2. Đặc tả bài toán Machine Learning

| Thành phần | Yêu cầu |
|---|---|
| Loại bài toán | Phân cụm không giám sát — Unsupervised Clustering |
| Đơn vị quan sát | Một khách hàng bán sỉ |
| Feature chính | Chi tiêu năm ở 6 nhóm hàng |
| `Channel` / `Region` | **Không đưa vào fit K-means chính**; chỉ dùng để profiling sau khi đã có cụm |
| Đầu ra | Mã cụm, khoảng cách tới tâm cụm, hồ sơ cụm |
| Metric chính | Inertia, silhouette, độ ổn định qua seed, kích thước cụm, khả năng diễn giải |

### Nguyên tắc quan trọng

`Channel` và `Region` **không phải ground truth** và không được dùng để chọn `K`.

Không được kết luận theo kiểu:

```text
K = 2 giống Channel nhất nên chọn K = 2.
```

Cách đúng:

```text
6 biến chi tiêu
      ↓
log1p + scale
      ↓
K-means
      ↓
Cluster ID
      ↓
Ghép Channel/Region trở lại
      ↓
Profiling và mô tả cụm
```

---

## 3. Dữ liệu

### Nguồn chính thức

- UCI Machine Learning Repository:  
  https://archive.ics.uci.edu/dataset/292/wholesale%2Bcustomers
- DOI / mô tả dữ liệu:  
  https://doi.org/10.24432/C5030X
- Giấy phép: **CC BY 4.0**

### Quy mô theo đề bài

- **440 khách hàng**.
- **6 biến chi tiêu chính**.
- Dữ liệu được đề xuất dùng `log1p` vì phân phối chi tiêu lệch.
- Sau `log1p`, dùng `StandardScaler`.

### Hồ sơ dữ liệu bắt buộc phải có

Trong thư mục `data/` cần có tối thiểu:

1. `data/README.md`
   - Nguồn dữ liệu.
   - Ngày tải.
   - Tệp sử dụng.
   - Checksum hoặc phiên bản.
   - Giấy phép / điều khoản.
   - Cách trích dẫn.

2. Data dictionary
   - Tên biến.
   - Kiểu dữ liệu.
   - Đơn vị.
   - Vai trò: feature / target / ID / profiling.
   - Thời điểm biến trở nên có sẵn.

3. Báo cáo chất lượng dữ liệu
   - Missing values.
   - Duplicate.
   - Ngoại lệ.
   - Phân phối các biến.
   - Dòng bị loại và lý do loại.

> Không đưa dữ liệu lớn hoặc dữ liệu bị hạn chế vào Git. Nếu cần, cung cấp script tải hoặc hướng dẫn tái tạo.

---

## 4. Quy tắc chống Data Leakage — bắt buộc

Đây là phần có trọng số rất cao trong rubric và không được làm sai.

### Đúng

```text
Raw data
   ↓
Split
   ├── Train
   ├── Validation
   └── Test

Train
   ↓
Fit preprocessing
   ↓
Fit scaler
   ↓
Fit K-means
```

### Sai

```text
Full data
   ↓
StandardScaler.fit()
   ↓
Split train / validation / test
```

### Quy tắc không thương lượng

- Tách `train / validation / test` **trước mọi bước học từ dữ liệu**.
- Imputer, scaler, encoder, feature selection, PCA hoặc resampling phải fit đúng phần train.
- Test chỉ dùng **một lần** để báo cáo cuối.
- Không chọn `K`, threshold, hyperparameter hoặc mô hình dựa trên test.
- Ghi lại `random_state`.
- Ghi lại phiên bản môi trường.
- Nếu dữ liệu có cấu trúc theo thời gian / người / phiên / hóa đơn thì phải split theo đúng nhóm tương ứng.

---

## 5. Pipeline tối thiểu theo đề

Toàn bộ project phải thực hiện được luồng sau:

1. Đóng băng định nghĩa bài toán, thời điểm dự đoán và tiêu chí đánh giá trước khi xem test.
2. Tải dữ liệu bằng script.
3. Kiểm tra schema, số dòng, khóa và chất lượng dữ liệu.
4. EDA **trên train**.
5. Xây dựng baseline.
6. Chạy mô hình chính K-means với `K = 2..8`.
7. Chạy nhiều `n_init` / `random_state`.
8. Chọn tham số bằng validation hoặc cách đánh giá phù hợp.
9. Lưu toàn bộ pipeline và cấu hình.
10. Đánh giá đúng một lần trên test.
11. Phân tích kết quả, giới hạn, out-of-domain.
12. Đưa model/pipeline đã lưu vào API và web.

---

## 6. Baseline bắt buộc

Cần có ít nhất hai mốc tham chiếu:

### Baseline A — không chia cụm

Phân tích thống kê toàn bộ tập dữ liệu mà chưa sử dụng clustering.

### Baseline B — K-means mặc định với K = 2

Dùng `K=2` như baseline đơn giản để so với các candidate sau.

Sau đó mới thực hiện đầy đủ:

```text
K = 2
K = 3
K = 4
K = 5
K = 6
K = 7
K = 8
```

---

## 7. Bốn thí nghiệm bắt buộc

### Thí nghiệm 1 — Raw vs `log1p + StandardScaler`

So sánh ít nhất hai nhánh:

```text
Nhánh A: Raw → K-means
Nhánh B: log1p → StandardScaler → K-means
```

Mục tiêu:

- Cho thấy tác động của phân phối lệch.
- Cho thấy việc chuẩn hóa ảnh hưởng thế nào đến khoảng cách Euclidean.
- Không chỉ nói “log vì đề yêu cầu”, mà phải có bằng chứng bằng số liệu và biểu đồ.

### Thí nghiệm 2 — Elbow và Silhouette cho K = 2..8

Với mỗi `K` cần lưu:

- Inertia.
- Silhouette score.
- Kích thước từng cụm.
- Cấu hình chạy.

Cần có tối thiểu:

- Elbow plot.
- Silhouette theo K.

> Không được chọn K chỉ dựa trên một metric duy nhất.

### Thí nghiệm 3 — Độ ổn định qua ít nhất 10 seed

Yêu cầu tối thiểu:

```text
seed 0
seed 1
seed 2
...
seed 9
```

Hoặc nhiều hơn.

Nên tổng hợp:

- Silhouette mean / std.
- Inertia mean / std.
- Biến thiên kích thước cụm.
- Mức ổn định gán cụm nếu có cách đo phù hợp.

Mục tiêu là trả lời:

> Khi khởi tạo khác nhau, kết luận có còn ổn định hay không?

### Thí nghiệm 4 — Profiling sau khi có cụm

Sau khi clustering:

- Tính **median chi tiêu** của từng nhóm hàng theo cluster.
- Phân tích kích thước cụm.
- Ghép `Channel` và `Region` trở lại để profiling.
- Tuyệt đối không dùng `Channel` / `Region` để fit hoặc làm ground truth chọn K.

---

## 8. Tiêu chí chọn K

Không chọn K theo kiểu:

```text
Silhouette cao nhất → chọn ngay.
```

Quyết định chọn K phải xem đồng thời:

- Inertia / Elbow.
- Silhouette.
- Stability qua nhiều seed.
- Kích thước các cụm.
- Có cụm quá nhỏ / bất thường hay không.
- Khả năng diễn giải hồ sơ cụm.
- Ý nghĩa kinh doanh.

### Quy trình đúng

```text
Train
  ↓
K = 2..8
  ↓
Nhiều seed
  ↓
Validation evidence
  ↓
Chọn K
  ↓
Đóng băng quyết định
  ↓
Final test đúng một lần
```

---

## 9. Phân tích cụm

Mỗi cluster cần tối thiểu:

- Số khách hàng.
- Tỷ trọng trên tổng tập.
- Median của 6 biến chi tiêu.
- Khoảng cách phân bố tới centroid.
- Channel profile.
- Region profile.
- Mô tả hành vi chi tiêu trung tính, không miệt thị hoặc xếp hạng giá trị con người.

Ví dụ cách mô tả hợp lý:

```text
Cluster A có median chi tiêu cao hơn ở một số nhóm hàng,
trong khi các nhóm còn lại ở mức thấp hoặc trung bình.
```

Không nên dùng các tên như:

```text
Khách xấu
Khách kém
Khách vô giá trị
```

---

## 10. Đầu ra mô hình

Mỗi khách hàng mới cần có tối thiểu:

```text
Cluster ID
Distance to centroid
Cluster profile
```

Khoảng cách tới centroid giúp nhận biết khách hàng có phải mẫu điển hình của cluster hay là trường hợp nằm xa tâm cụm.

---

## 11. Lưu model / pipeline

Training và serving phải tách biệt.

### Offline training

```text
Data
 ↓
Preprocessing
 ↓
K-means
 ↓
Evaluation
 ↓
Freeze decision
 ↓
Save pipeline/model
```

### Online serving

```text
API request
 ↓
Load saved pipeline
 ↓
Validate input
 ↓
Transform bằng pipeline đã fit
 ↓
Gán cluster
 ↓
Trả JSON
```

**Không huấn luyện lại K-means ở mỗi request.**

Artifact nên lưu:

- Pipeline đã fit.
- K cuối cùng.
- Centroid.
- Cấu hình / seed.
- Version môi trường.
- Metadata / model card.

---

## 12. Web/API bắt buộc

Ứng dụng phải chạy local và có API.

### API chính

```http
POST /api/segment
```

API phải có:

- JSON request / response.
- Schema rõ ràng.
- Validation.
- HTTP status code hợp lý.
- Ví dụ request / response.
- Test tối thiểu.
- Không âm thầm sửa input sai.

### Validation đầu vào

Ứng dụng cần kiểm tra:

- Thiếu feature.
- Sai kiểu dữ liệu.
- Giá trị âm nếu không hợp lệ.
- Giá trị vượt xa miền dữ liệu training.
- `NaN` / `inf`.

Nếu input bất thường cần trả lỗi hoặc cảnh báo rõ ràng thay vì tự đổi dữ liệu mà người dùng không biết.

---

## 13. Web tối thiểu 03 màn hình

### Màn hình 1 — Giới thiệu / phạm vi

Hiển thị:

- Bài toán.
- Dataset.
- Mục tiêu.
- Phương pháp.
- Giới hạn sử dụng.

### Màn hình 2 — Phân khúc khách hàng mới

Form nhập 6 biến chi tiêu theo đúng data dictionary.

Kết quả hiển thị:

- Cluster ID.
- Khoảng cách tới centroid.
- Hồ sơ cluster.
- Cảnh báo nếu input ngoài miền.

### Màn hình 3 — Dashboard & Model Card

Nên có:

- Elbow chart.
- Silhouette chart.
- Stability qua seed.
- Cluster size.
- Cluster profile.
- Channel / Region profile.
- Thông tin model.
- Giới hạn mô hình.

---

## 14. Cấu trúc repository đề xuất

```text
Machine_Learning_Phan_Khuc_Khach_Hang_Ban_Si/
│
├── app/
│   ├── main.py
│   ├── schemas.py
│   ├── service.py
│   ├── templates/
│   └── static/
│
├── data/
│   ├── README.md
│   ├── raw/
│   └── processed/
│
├── models/
│   ├── pipeline.joblib
│   └── metadata.json
│
├── notebooks/
│   └── eda_train.ipynb
│
├── reports/
│   ├── figures/
│   └── tables/
│
├── src/
│   ├── download_data.py
│   ├── data.py
│   ├── features.py
│   ├── train.py
│   ├── evaluate.py
│   └── experiment.py
│
├── tests/
│   ├── test_data.py
│   ├── test_preprocessing.py
│   ├── test_model.py
│   └── test_api.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

Đây là cấu trúc triển khai đề xuất. Có thể thay đổi nếu vẫn đảm bảo đầy đủ yêu cầu của đề và khả năng tái lập.

---

## 15. Các bước thực hiện chi tiết

### Bước 0 — Khởi tạo project

- Tạo repository.
- Tạo môi trường Python.
- Tạo `requirements.txt` hoặc lock file.
- Tạo `.gitignore`.
- Chốt cấu trúc thư mục.
- Ghi version Python và thư viện.

Ví dụ môi trường local:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Cài dependency khi đã có `requirements.txt`:

```bash
pip install -r requirements.txt
```

### Bước 1 — Tải dữ liệu bằng script

Mục tiêu:

```bash
python src/download_data.py
```

Script cần:

- Tải đúng nguồn.
- Lưu vào `data/raw/`.
- Không sửa tay dữ liệu raw.
- Ghi checksum hoặc thông tin version nếu có.

### Bước 2 — Kiểm tra dữ liệu

Kiểm tra:

- Schema.
- Số dòng.
- Kiểu dữ liệu.
- Missing.
- Duplicate.
- Giá trị âm / không hợp lệ.
- Ngoại lệ.

Tạo report chất lượng dữ liệu.

### Bước 3 — Split trước preprocessing

Tạo train / validation / test trước các bước học từ dữ liệu.

Lưu seed và tỷ lệ split trong config hoặc metadata.

### Bước 4 — EDA chỉ trên train

EDA phải phục vụ quyết định kỹ thuật, không chỉ để trang trí.

Cần xem:

- Phân phối từng feature.
- Skewness.
- Outlier.
- Tương quan tham khảo.
- Mức thay đổi sau `log1p`.
- Lý do cần scaling.

### Bước 5 — Xây dựng preprocessing

Nhánh chính:

```text
Input
 ↓
log1p
 ↓
StandardScaler
```

Fit transformer/scaler bằng train.

Validation và test chỉ gọi `transform()` bằng transformer đã fit.

### Bước 6 — Chạy baseline

- Toàn bộ train không clustering để làm thống kê cơ sở.
- K-means với `K=2` làm baseline.

Lưu kết quả vào bảng để so sánh.

### Bước 7 — Chạy thí nghiệm K = 2..8

Với mỗi K:

- Chạy nhiều seed.
- Ghi inertia.
- Ghi silhouette.
- Ghi cluster size.
- Ghi runtime/config nếu cần.

### Bước 8 — So sánh raw với log1p + scale

Chạy cùng điều kiện đánh giá để đảm bảo so sánh công bằng.

### Bước 9 — Stability analysis

Dùng tối thiểu 10 seed.

Tạo bảng tổng hợp mean/std và biểu đồ phù hợp.

### Bước 10 — Chọn K bằng validation evidence

Chọn K dựa trên tổng hợp:

- Elbow.
- Silhouette.
- Stability.
- Cluster size.
- Khả năng diễn giải.

Ghi rõ lý do lựa chọn trong report.

### Bước 11 — Đóng băng quyết định

Sau khi chốt:

- Preprocessing.
- K.
- Seed / config.
- Tiêu chí đánh giá.

Không quay lại test để tối ưu.

### Bước 12 — Final test đúng một lần

Chỉ dùng test để đưa ra kết luận cuối.

Tách rõ trong báo cáo:

```text
Validation result → dùng để lựa chọn
Test result       → dùng để kết luận cuối
```

### Bước 13 — Profile cluster

Tạo:

- Median chi tiêu theo cluster.
- Cluster size.
- Channel profile.
- Region profile.
- Phân tích distance tới centroid.

### Bước 14 — Phân tích lỗi / giới hạn

Với clustering, cần xem các trường hợp như:

- Điểm rất xa centroid.
- Cluster rất nhỏ.
- Khách hàng nằm gần ranh giới nhiều centroid.
- Cluster thay đổi mạnh qua seed.
- Outlier.
- Input ngoài miền training.
- K có metric đẹp nhưng khó diễn giải.

### Bước 15 — Lưu model/pipeline

Mục tiêu cuối:

```text
models/pipeline.joblib
models/metadata.json
```

Ứng dụng web chỉ load artifact đã lưu.

### Bước 16 — Xây API

Stack khuyến nghị trong đề:

- Python.
- pandas.
- scikit-learn.
- Flask hoặc FastAPI.
- HTML/CSS/JS hoặc React/Vue.

SQLite chỉ dùng nếu thật sự cần.

### Bước 17 — Xây Web

Hoàn thiện tối thiểu 3 màn hình đúng yêu cầu.

### Bước 18 — Test

Test tối thiểu nên bao gồm:

- Data schema.
- Preprocessing.
- Model artifact.
- API happy path.
- API thiếu trường.
- API sai kiểu dữ liệu.
- API input bất hợp lệ.
- API input ngoài miền.

### Bước 19 — Kiểm tra tái lập trên máy sạch

Một thành viên hoặc máy khác phải có thể làm theo README và chạy lại project.

Mục tiêu cần đạt:

```text
setup → data → train → evaluate → app
```

mà không cần sửa đường dẫn cá nhân.

---

## 16. Lệnh chạy mục tiêu

> Các lệnh dưới đây là giao diện chạy **dự kiến của project**. Khi code được triển khai, cần bảo đảm README và code thực tế đồng nhất.

### Tải dữ liệu

```bash
python src/download_data.py
```

### Train / chạy thí nghiệm

```bash
python src/train.py
```

### Evaluate

```bash
python src/evaluate.py
```

### Chạy test

```bash
pytest
```

### Chạy web nếu dùng FastAPI

```bash
uvicorn app.main:app --reload
```

Sau đó mở:

```text
http://127.0.0.1:8000
```

API docs mặc định nếu dùng FastAPI:

```text
http://127.0.0.1:8000/docs
```

---

## 17. Model Card cần có

Model card nên mô tả:

- Tên model.
- Phiên bản.
- Dataset.
- Ngày train.
- Feature sử dụng.
- Feature không sử dụng để fit (`Channel`, `Region`).
- Preprocessing.
- K cuối cùng.
- Random seed / cấu hình.
- Metric validation.
- Metric final test.
- Hạn chế.
- Miền dữ liệu training.
- Cảnh báo khi sử dụng.
- Mục đích phù hợp và không phù hợp.

---

## 18. Yêu cầu báo cáo

Báo cáo bắt buộc:

- **15–25 trang**, không tính phụ lục.
- Có PDF và file nguồn DOCX hoặc LaTeX.
- Biểu đồ phải đọc được.

### Đề cương bắt buộc

1. Tóm tắt.
2. Bối cảnh và câu hỏi nghiên cứu.
3. Dữ liệu và giấy phép.
4. Thời điểm dự đoán và leakage.
5. Phương pháp.
6. Thiết kế thí nghiệm.
7. Kết quả.
8. Phân tích lỗi.
9. Web/API.
10. Đạo đức và giới hạn.
11. Kết luận.
12. Tài liệu tham khảo.
13. Phụ lục tái lập.

---

## 19. Yêu cầu slide và demo

- **10–12 slide**.
- Demo trực tiếp **5–7 phút**.
- Tổng phần trình bày khoảng **12–15 phút** và có vấn đáp.

Nội dung slide nên tập trung:

1. Bài toán.
2. Dataset.
3. Leakage/split.
4. EDA chính.
5. Raw vs log1p+scale.
6. K=2..8.
7. Elbow + silhouette.
8. Stability.
9. K được chọn và lý do.
10. Cluster profile.
11. Web/API demo.
12. Hạn chế và kết luận.

---

## 20. Kế hoạch 06 tuần

### Tuần 1

- Chốt câu hỏi nghiên cứu.
- Chốt thời điểm dự đoán.
- Xác nhận nguồn / giấy phép.
- Tạo repo và backlog.

Đầu ra:

- Project brief 1–2 trang.
- Data README.
- Schema.
- Baseline plan.

### Tuần 2

- Tải / làm sạch dữ liệu.
- EDA trên train.
- Hoàn thiện split.
- Baseline.

Đầu ra:

- Script dữ liệu.
- Notebook EDA.
- Baseline chạy được.
- Checkpoint giảng viên.

### Tuần 3

- Pipeline mô hình chính.
- Validation / đánh giá.
- Theo dõi thí nghiệm.

Đầu ra:

- Bảng thí nghiệm vòng 1.
- Model candidate.
- Test preprocessing.

### Tuần 4

- Hoàn tất thí nghiệm.
- Chọn mô hình / cấu hình.
- Final test.
- Phân tích lỗi.

Đầu ra:

- Bảng kết quả đóng băng.
- Figures.
- Model card nháp.

### Tuần 5

- Đóng gói API và web.
- Tích hợp model.
- Test input và lỗi.

Đầu ra:

- Web demo end-to-end.
- API docs.
- Test.
- Checkpoint demo.

### Tuần 6

- Hoàn thiện báo cáo.
- Hoàn thiện slide.
- Rehearsal.
- Tái lập trên môi trường sạch.

Đầu ra:

- Release cuối.
- Báo cáo.
- Slide.
- Biên bản phân công.

---

## 21. Phân công hai thành viên

Yêu cầu của đề:

- Mỗi người phải có đóng góp đáng kể ở **cả data/model và web/report**.
- Không chia cứng một người chỉ code, một người chỉ viết báo cáo.
- Pull request / commit message cần mô tả công việc.
- Nhật ký tuần cần ghi:
  - Người thực hiện.
  - Giờ ước lượng.
  - Kết quả.
  - Vấn đề gặp phải.
- Cả hai phải hiểu toàn bộ pipeline.
- Cả hai phải trả lời được về:
  - Leakage.
  - Metric.
  - K-means.
  - Chọn K.
  - API.

---

## 22. Rubric 100 điểm

| Tiêu chí | Điểm |
|---|---:|
| Bài toán & phạm vi | 8 |
| Dữ liệu & EDA | 12 |
| Split, leakage & tái lập | 15 |
| Mô hình & thí nghiệm | 18 |
| Đánh giá & phân tích lỗi | 18 |
| Web/API | 12 |
| Mã nguồn & bàn giao | 7 |
| Báo cáo, trình bày & nhóm | 10 |
| **Tổng** | **100** |

### Các điều kiện có thể làm mất điểm nghiêm trọng

- Không tái lập được kết quả.
- Không có test độc lập.
- Có data leakage nghiêm trọng chưa sửa.

Các lỗi trên có thể khiến bài bị giới hạn tối đa **50/100** theo đề.

Nếu không có Web/API chạy được thì mất toàn bộ điểm mục Web/API.

Vi phạm nguồn dữ liệu / điều khoản hoặc sao chép sẽ xử lý theo quy chế học vụ.

---

## 23. Cổng kiểm tra trước khi nộp

### Dữ liệu

- [ ] Nguồn truy cập được.
- [ ] License / citation rõ.
- [ ] Có script tái tạo.
- [ ] Không chứa dữ liệu nhạy cảm thật.
- [ ] Có data dictionary.
- [ ] Có quality report.

### Đánh giá

- [ ] Split hợp lệ.
- [ ] Baseline có đầy đủ.
- [ ] Validation và test tách rõ.
- [ ] Test chỉ dùng cho kết luận cuối.
- [ ] Có bảng metric.
- [ ] Có phân tích lỗi / giới hạn.

### Thí nghiệm

- [ ] Raw vs log1p+scale.
- [ ] K=2..8.
- [ ] Elbow.
- [ ] Silhouette.
- [ ] Ít nhất 10 seed.
- [ ] Stability analysis.
- [ ] Profile median.
- [ ] Channel/Region chỉ dùng sau clustering.

### Kỹ thuật

- [ ] Có hướng dẫn ngắn chạy train/evaluate/app.
- [ ] Không có absolute path của máy cá nhân.
- [ ] Có requirements/lock.
- [ ] Có random seed.
- [ ] Có model artifact.
- [ ] Có metadata/model card.

### Web/API

- [ ] Web chạy local.
- [ ] Có ít nhất 3 màn hình.
- [ ] `POST /api/segment` chạy.
- [ ] JSON schema rõ.
- [ ] Input xấu không làm sập ứng dụng.
- [ ] Có warning ngoài miền.
- [ ] Không retrain model mỗi request.

### Học thuật

- [ ] Mọi bảng/hình có nguồn khi cần.
- [ ] Không sao chép.
- [ ] Ghi rõ công cụ AI và cách kiểm chứng nếu có.
- [ ] Báo cáo đúng cấu trúc.
- [ ] Slide/demo hoàn chỉnh.
- [ ] Hai thành viên đều hiểu toàn bộ pipeline.

---

## 24. Các câu hỏi vấn đáp cần chuẩn bị

### Vì sao cần `log1p`?

Cần giải thích dựa trên phân phối lệch của dữ liệu chi tiêu và ảnh hưởng của giá trị rất lớn lên khoảng cách Euclidean của K-means.

### Silhouette cao nhất có đủ để chọn K không?

Không. Cần xem đồng thời elbow/inertia, stability, kích thước cluster và khả năng diễn giải.

### `Channel` và `Region` dùng ở đâu?

Chỉ dùng để **profiling sau clustering**, không đưa vào fit chính và không dùng làm ground truth chọn K.

### Vì sao scaler chỉ fit trên train?

Để tránh thông tin từ validation/test đi vào preprocessing, gây data leakage.

### Vì sao test chỉ dùng một lần?

Nếu dùng test nhiều lần để chọn K hoặc cấu hình, test đã trở thành validation và kết quả cuối sẽ bị lạc quan.

### Khách mới được gán cụm thế nào?

Dùng **đúng preprocessing đã fit** và centroid/model đã lưu; không fit lại scaler hoặc K-means bằng khách mới.

---

## 25. Phần mở rộng — chỉ làm khi phần bắt buộc đã hoàn chỉnh

Có thể làm thêm:

- PCA 2D để trực quan.
- So sánh hierarchical clustering.

Tuy nhiên:

- Kết quả chính vẫn phải là **K-means**.
- Phần mở rộng không bù cho lỗi split, leakage hoặc web/API không chạy.
- Không bắt buộc cloud.
- Không bắt buộc mobile app.
- Không bắt buộc deep learning.
- Không bắt buộc thu thập thêm dữ liệu.

---

## 26. Definition of Done

Project chỉ nên coi là **hoàn thành** khi thỏa toàn bộ luồng:

```text
UCI Wholesale Customers
          ↓
Download script
          ↓
Schema + quality audit
          ↓
Train / Validation / Test
          ↓
EDA on Train
          ↓
Raw vs log1p + scale
          ↓
Baseline
          ↓
KMeans K=2..8
          ↓
≥ 10 random seeds
          ↓
Elbow + Silhouette + Stability
          ↓
Choose K using validation evidence
          ↓
Freeze decision
          ↓
Final Test exactly once
          ↓
Cluster Profile + Channel/Region Profile
          ↓
Save Pipeline / Model Card
          ↓
API / Web
          ↓
Tests
          ↓
Report + Slides + Reproducibility Check
```

---

## 27. Tài liệu tham khảo tối thiểu

1. Slide học phần: **Bài 8 — K-means, phân khúc và chọn K**.
2. UCI Wholesale customers:  
   https://archive.ics.uci.edu/dataset/292/wholesale%2Bcustomers
3. DOI dữ liệu:  
   https://doi.org/10.24432/C5030X
4. Scikit-learn — K-means / clustering:  
   https://scikit-learn.org/stable/modules/clustering.html#k-means

---

## 28. Trạng thái hiện tại

Repository đang ở giai đoạn khởi tạo. README này là **đặc tả yêu cầu + roadmap triển khai** dựa trên đề Project 22.

Khi bắt đầu code, mỗi hạng mục hoàn thành cần được cập nhật lại README để đảm bảo tài liệu luôn đúng với source thực tế.
