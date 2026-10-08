# Gate 5 — Model selection và freeze (2026-10-08)

## Cơ sở lựa chọn: chỉ train/validation

Đã đối chiếu toàn bộ 14 dòng `reports/data/experiments/selection_evidence.csv`
và `review_table.csv`, sau đó đọc profile median của ba shortlist. Mỗi candidate
có 10 seed và 45 ARI pair. Bảng dưới dùng silhouette/ARI **mean qua 10 seed**;
size/outlier và profile thuộc **seed 42**.

| Tiêu chí | Raw K=2 | Log1p+Scaler K=2 | Log1p+Scaler K=3 |
|---|---:|---:|---:|
| Silhouette train / validation | 0.4985 / 0.6103 | 0.2756 / 0.3066 | 0.2049 / 0.2165 |
| Gap tuyệt đối validation–train | 0.1118 | 0.0310 | 0.0116 |
| ARI mean / min | 1.0000 / 1.0000 | 0.9970 / 0.9848 | 0.9078 / 0.7982 |
| Cluster counts train | 217 / 47 | 118 / 146 | 91 / 73 / 100 |
| Cluster counts validation | 81 / 7 | 46 / 42 | 40 / 24 / 24 |
| Smallest cluster train | 17.80% | 44.70% | 27.65% |
| Max gap tỷ trọng train–validation | 9.85 điểm % | 7.58 điểm % | 10.98 điểm % |
| Train IQR distance outliers | 23 | 13 | 8 |
| Top 1% đóng góp vào inertia train | 25.33% | 10.06% | 10.43% |

Inertia tuyệt đối giữa raw và log/scaled có đơn vị khác nhau. **Chỉ so inertia
trong cùng nhánh:** log K=2 có train mean 1116.61, validation mean 391.53;
log K=3 có train mean 945.90, validation mean 341.06. Mức giảm của K=3 là
15.29% trên train và 12.89% trên validation; kết quả giảm inertia khi tăng K
không tự nó chứng minh K=3 tốt hơn.

## Median spending, đơn vị gốc

| Candidate/cluster | N train / val | Fresh train → val | Milk train → val | Grocery train → val | Frozen train → val | Detergents train → val | Delicassen train → val |
|---|---:|---:|---:|---:|---:|---:|---:|
| Log K2, 0 | 118 / 46 | 8562 → 5588 | 6949 → 7968 | 10391 → 11443 | 1265 → 1071 | 3774 → 5219 | 1667 → 1352 |
| Log K2, 1 | 146 / 42 | 9518 → 9270 | 1606 → 1532 | 2242 → 2036 | 2062 → 2191 | 270 → 281 | 645 → 614 |
| **Log K3, 0** | **91 / 40** | 5963 → 5340 | 7184 → 8653 | 11757 → 12473 | 1031 → 946 | 4595 → 6207 | 1468 → 916 |
| **Log K3, 1** | **73 / 24** | 6987 → 5970 | 1042 → 1247 | 1902 → 1926 | 982 → 1275 | 187 → 264 | 406 → 345 |
| **Log K3, 2** | **100 / 24** | 16293 → 13700 | 2754 → 2401 | 3271 → 2506 | 4078 → 4521 | 461 → 396 | 1141 → 1338 |

K3 tạo ba nhóm riêng biệt, duy trì **thứ tự tương đối về mặt hàng đặc trưng**
trên validation:

1. K3/0: Grocery, Milk và Detergents_Paper cao → **tạp hóa/chất tẩy rửa**.
2. K3/1: phần lớn nhóm hàng ở mức thấp → **chi tiêu thấp**.
3. K3/2: Fresh và Frozen nổi bật → **hàng tươi/đông lạnh**.

K=2 log giữ một nhóm grocery/detergents, nhưng nhóm kia chưa mô tả được
khác biệt giữa khách có chi tiêu thấp và khách thiên Fresh/Frozen. Đối chiếu
nhãn train K2×K3 (không coi cluster ID là tên cố định): K2/0 → K3/0,1,2 =
89/0/29; K2/1 → 2/73/71. Validation lần lượt = 40/0/6 và 0/24/18.
Do đó K3 tạo khác biệt định hướng hàng hóa đáng kể thay vì chỉ chia cụm
theo mức độ chi tiêu tổng.

Raw K2 chủ yếu phân biệt Fresh cao (median 30624 so với 7005 trên train),
validation chỉ có 7 khách ở nhóm Fresh cao và top 1% điểm xa đóng góp 25.33%
inertia. Nó có silhouette tốt nhưng ít cân bằng và bị chi phối mạnh hơn bởi
điểm xa. Không so inertia raw với log trên hai scale.

`Channel` và `Region` chỉ là hậu phân cụm. Với K3, Channel 2 chiếm 74.7%
train và 90.0% validation của cluster grocery/detergents; nhóm chi tiêu thấp
và Fresh/Frozen phần lớn Channel 1. Đây là kiểm tra mô tả, **không phải nhãn
thật hay tiêu chí fit/chọn K**. Region không được dùng để chọn mô hình.

## Kiểm tra độ ổn định khi refit (phát triển, không đụng test)

Một kiểm tra bổ sung trước final test dùng hai mô hình có cùng cấu hình seed=42:
(a) fit trên train 264 rồi predict toàn bộ 352 development, (b) fit lại scaler
và KMeans trên train+validation 352 rồi predict 352 mẫu. Đo ARI giữa hai
phân hoạch **trên cùng 352 dòng** (không tính dựa vào nhãn Channel/Region):

| Cấu hình | ARI train-fit vs refit 352 | Profile sau refit 352 |
|---|---:|---|
| **Log K2** | **0.8893** | 162 khách thiên Grocery/Milk/Detergents; 190 khách thiên Fresh/Frozen; hướng profile giữ nguyên |
| Log K3 | 0.3343 | 176 khách thiên Fresh/Frozen, nhưng **hai cụm còn lại đều có Grocery/Detergents cao**, không duy trì ba nhóm thấp / tạp hóa / Fresh rõ rệt |

K3 đạt ARI seed stability 0.9078 **trên train cố định**, nhưng không bảo đảm
ổn định khi dữ liệu dùng để fit tăng thêm 88 dòng. Kiểm tra refit cho thấy
ý nghĩa nhóm K3 dễ biến đổi, nên không chọn K3 cho artifact fit 352.
Đây là phân tích phát triển trước test, khác với đánh giá final test.

## Quyết định D011 và đánh đổi

**Chọn `log1p_standardscaler`, K=2, random_state=42, n_init=10,
max_iter=300, algorithm=lloyd.** ARI 0.9970 qua seed, silhouette validation
0.3066, min train share 44.70%, gap train/validation share 7.58 điểm %,
outlier 13, top 1% inertia 10.06%. Hai nhóm chính thiên
Grocery/Milk/Detergents và thiên Fresh/Frozen có profile consistent trên
train/validation và sau refit 352. So với K3, bỏ sự phân biệt nhóm chi tiêu
thấp chi tiết hơn, đổi lại cấu trúc ổn định hơn khi đưa vào artifact cuối.
Không mặc định K2 luôn tốt hơn: kết luận có phạm vi trên dataset/split này.

Seed 42 theo protocol D010; không tối ưu seed dựa vào test. Không xóa
outlier. Không dùng Channel/Region làm ground truth. Độ tin cậy profiling
vẫn giới hạn bởi validation 88 dòng; profile không chứng minh doanh thu/
lợi nhuận thực tế sẽ tăng.

**Biên bản điều chỉnh trước test:** bản freeze K3 sơ bộ được lưu ở
`models/selection_k3_retracted_pretest.json` để kiểm toán. Preflight trên
352 development phát hiện biến đổi profile, nên rút bản này **trước bất kỳ
lần đọc final test nào**. `models/selection.json` là quyết định D011 cuối K2;
không được thay đổi sau khi đánh giá test.

## Ranh giới freeze và one-shot final test

`models/selection.json` chứa quyết định K2 và SHA-256 của evidence, review,
median profile và hai split phát triển. Freeze xong mới cho phép chạy
`ml/src/finalize_model.py`: fit `log1p`+scaler+KMeans trên **train+validation
(352 mẫu)** rồi xuất `model.joblib` cùng `model.json` để Node đọc sau này.
Đánh giá **test 88 mẫu đúng một lần** trên mô hình đã fit; test tuyệt đối
không tham gia fit, đặt tên segment, chọn K, seed hay policy.

Trước khi mở test, script tạo `models/final_evaluation.json` ở trạng thái
`CLAIMED` để từ chối chạy lại nếu bị ngắt. Chỉ `COMPLETE` chứng minh đánh giá
đã kết thúc; khi `CLAIMED` kéo dài phải kiểm tra thủ công, không tự chạy lại.
Không sửa selection hoặc thử candidate khác từ kết quả final test.

## Kết quả Gate 5 đã thực thi (2026-10-08)

**D011 được freeze trước final test; Gate 5 đã COMPLETE.** Đây là biên bản chạy
thật, không phải lệnh cần chạy lại:

- Preflight PASS: 14 evidence và 14 review rows; checksum 6 nguồn hợp lệ;
  train/validation 352 dòng không trùng; portable prediction khớp sklearn.
- `python -m pytest ml/tests -q`: **100 passed in 30.70s**.
- `python -m ml.src.finalize_model`: **exit 0**, một lần, `status=COMPLETE`.
- `npm run build`: frontend Vite/TypeScript và backend TypeScript PASS.
- `npm run test:backend`: **2 passed**, API skeleton giữ `/api/model-info` 503.
- Kiểm chứng artifact sau chạy PASS: SHA-256 khớp biên bản, JSON portable
  suy luận trùng sklearn trên 352 development rows; không mở test lần nữa.

| Chỉ số | Development refit (352) | Final test độc lập (88) |
|---|---:|---:|
| Silhouette | 0.289158 | **0.238890** |
| Inertia / row (log1p+scaled) | 4.163875 | **4.505144** |
| Cluster 0/1 | 162 / 190 | **45 / 43** |
| Smallest cluster share | 46.02% | 48.86% |

Profile của model cuối (median đơn vị gốc) giữ hai xu hướng:

- Cluster 0 (162): Grocery=10842.5, Milk=7226, Detergents_Paper=4084.5,
  Fresh=6410.5, Frozen=1153 → thiên **tạp hóa/chất tẩy rửa**.
- Cluster 1 (190): Fresh=9727.5, Frozen=2194.5, Grocery=2175.5,
  Milk=1626, Detergents_Paper=279.5 → thiên **hàng tươi/đông lạnh**.

Các profile đặt tên dựa vào development, **không dùng test để đặt tên**.
Silhouette test thấp hơn development khoảng 0.0503; đây là chỉ số đánh giá
ngoài mẫu, không được dùng quay lại chọn K. Phân cụm không có nhãn thật để
đánh giá accuracy và chưa có bằng chứng hiệu quả kinh doanh.

| Artifact | SHA-256 |
|---|---|
| `models/selection.json` | `f256dc6a04a5a8eddb0fc854e940bda25a4276b86b184d6155c4cee2a1ed8c64` |
| `models/model.json` | `5057db0e290c93043abe4add3abf440e64864dc8d187a8d0b22d18621acd3b28` |
| `models/model.joblib` | `f2f7874807456e6fdbade0be4c1eb124a8245e922dbf5ca6f070a9e040f2c816` |

`models/final_evaluation.json` là biên bản kết quả: `COMPLETE`,
`test_evaluated_once=true`, `test_used_for_selection=false`, test 88 dòng.
**Không chạy lại `ml:freeze` hoặc `ml:finalize`.** Cả hai entry point đều
chặn ghi đè để bảo vệ quyết định và test độc lập. Backend/frontend thuộc Gate 6.
