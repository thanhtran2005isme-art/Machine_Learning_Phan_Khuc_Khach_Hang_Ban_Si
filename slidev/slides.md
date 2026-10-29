---
theme: default
background: https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?auto=format&fit=crop&w=1920&q=80
title: "Phân Khúc Khách Hàng Bán Sỉ — Project 22"
info: |
  ## Project 22: Phân Khúc Khách Hàng Bán Sỉ
  Đồ án kết thúc học phần Học Máy Cơ Bản
  K-Means Clustering & Serving Pipeline
class: text-center
highlighter: shiki
drawings:
  persist: false
transition: slide-left
mdc: true
---

# PHÂN KHÚC KHÁCH HÀNG BÁN SỈ
### THEO CƠ CẤU CHI TIÊU HẰNG NĂM

<div class="mt-4 flex justify-center items-center gap-2">
  <span class="px-3 py-1 rounded-full text-xs font-semibold bg-blue-600/30 text-blue-300 border border-blue-400/40">Học Máy Cơ Bản</span>
  <span class="px-3 py-1 rounded-full text-xs font-semibold bg-emerald-600/30 text-emerald-300 border border-emerald-400/40">Project 22 — K-Means Clustering</span>
  <span class="px-3 py-1 rounded-full text-xs font-semibold bg-purple-600/30 text-purple-300 border border-purple-400/40">UCI Wholesale Customers</span>
</div>

<div class="mt-8 grid grid-cols-2 gap-6 max-w-xl mx-auto text-left text-sm bg-black/40 backdrop-blur-md p-5 rounded-xl border border-white/10 shadow-2xl">
  <div>
    <div class="text-gray-400 text-xs uppercase tracking-wider mb-1">Giảng viên hướng dẫn</div>
    <div class="font-bold text-base text-white">PGS.TS. NGUYỄN VĂN HẬU</div>
    <div class="text-gray-300 text-xs mt-1">Lớp học phần: 12523W.1</div>
  </div>
  <div>
    <div class="text-gray-400 text-xs uppercase tracking-wider mb-1">Nhóm thực hiện</div>
    <div class="font-bold text-base text-white">Nhóm 02 sinh viên</div>
    <div class="text-gray-300 text-xs mt-1">Phân công: ML Pipeline & Web Serving</div>
  </div>
</div>

<div class="mt-8 text-xs text-gray-400">
  Nhấn phím Space hoặc phím mũi tên phải để chuyển slide <carbon:arrow-right class="inline" />
</div>

<!--
Xin chào Thầy và các bạn. Hôm nay nhóm xin trình bày đồ án kết thúc học phần Học Máy Cơ Bản: Project 22 — Phân khúc khách hàng bán sỉ theo cơ cấu chi tiêu hằng năm dựa trên tập dữ liệu UCI Wholesale Customers.
-->

---
transition: slide-left
---

# 1. Bối Cảnh, Mục Tiêu & Ranh Giới Đạo Đức

<div class="grid grid-cols-2 gap-6 mt-4">
  <div class="space-y-4">
    <div class="p-4 rounded-xl bg-blue-500/10 border border-blue-500/20">
      <div class="flex items-center gap-2 font-bold text-blue-400 mb-2">
        <span class="text-base">🏢</span> Bối Cảnh Thực Tiễn
      </div>
      <p class="text-xs text-gray-300 leading-relaxed">
        Nhà phân phối bán sỉ cần thấu hiểu các <b>mẫu hình cơ cấu chi tiêu</b> thực tế của khách hàng (nhà hàng, khách sạn, tiệm bán lẻ) để tối ưu hóa danh mục sản phẩm, kế hoạch giao vận kho bãi và chính sách dịch vụ.
      </p>
    </div>

    <div class="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/20">
      <div class="flex items-center gap-2 font-bold text-emerald-400 mb-2">
        <span class="text-base">❓</span> Câu Hỏi Nghiên Cứu Then Chốt
      </div>
      <blockquote class="text-xs italic text-gray-200 border-l-2 border-emerald-400 pl-3 py-1">
        "Sau khi áp dụng log-transform và chuẩn hóa, K-Means tạo ra các phân khúc khách hàng nào ổn định về mặt thống kê và có ý nghĩa thực tế trong kinh doanh?"
      </blockquote>
    </div>
  </div>

  <div class="space-y-4">
    <div class="p-4 rounded-xl bg-purple-500/10 border border-purple-500/20">
      <div class="flex items-center gap-2 font-bold text-purple-400 mb-2">
        <span class="text-base">🎯</span> Mục Tiêu Học Thuật Cốt Lõi
      </div>
      <ul class="text-xs text-gray-300 space-y-1.5 list-disc pl-4">
        <li>Vận dụng thuật toán K-Means, phân tích giả định và giới hạn khoảng cách Euclidean.</li>
        <li>Bảo đảm <b>tập kiểm thử độc lập 100%</b>, tuyệt đối không gây rò rỉ dữ liệu (data leakage).</li>
        <li>So sánh đa chiều: Baseline, Elbow, Silhouette, độ ổn định qua seed (ARI).</li>
        <li>Đóng gói Serving API & Web App sản xuất, nạp artifact đóng băng (không train lại theo request).</li>
      </ul>
    </div>

    <div class="p-4 rounded-xl bg-rose-500/10 border border-rose-500/30">
      <div class="flex items-center gap-2 font-bold text-rose-400 mb-1">
        <span class="text-base">⚖️</span> Ranh Giới Đạo Đức AI & Sử Dụng Trung Tính
      </div>
      <p class="text-xs text-gray-300 leading-relaxed">
        Phân cụm là công cụ <b>mô tả hành vi chi tiêu</b> thuần túy. Tuyệt đối <b>không</b> dùng nhãn cụm để định giá giá trị con người, không phân biệt đối xử hoặc từ chối phục vụ khách hàng.
      </p>
    </div>
  </div>
</div>

<!--
Slide này xác lập bài toán: giải quyết bài toán phân khúc khách hàng bán sỉ dựa trên cơ cấu chi tiêu. Chúng tôi đặc biệt tuân thủ nguyên tắc đạo đức AI: cụm chỉ mang tính mô tả trung tính, không định giá hay phân loại giá trị con người.
-->

---
transition: slide-left
---

# 2. Dữ Liệu & Đặc Tả Bài Toán Machine Learning

<div class="grid grid-cols-3 gap-4 mt-3">
  <div class="col-span-1 p-4 rounded-xl bg-slate-800/60 border border-slate-700 space-y-3">
    <div class="font-bold text-sm text-cyan-300 border-b border-slate-700 pb-2">
      📊 Nguồn & Quy Mô Dữ Liệu
    </div>
    <div class="text-xs space-y-2 text-gray-300">
      <div><b>Bộ dữ liệu:</b> UCI Wholesale Customers</div>
      <div><b>Định danh DOI:</b> <code>10.24432/C5030X</code></div>
      <div><b>Giấy phép:</b> Creative Commons CC BY 4.0</div>
      <div><b>Quy mô:</b> <b>440 quan sát</b> (khách hàng)</div>
      <div><b>Chất lượng:</b> <b>0 missing values</b>, không trùng lặp</div>
      <div><b>Đơn vị:</b> <i>Monetary Units (m.u.)</i> / năm</div>
    </div>
    <div class="p-2 rounded bg-amber-500/10 border border-amber-500/30 text-[11px] text-amber-200">
      *Lưu ý: UCI không xác định mệnh giá VND hay USD, chỉ dùng chuẩn monetary units (m.u.).
    </div>
  </div>

  <div class="col-span-2 space-y-3">
    <div class="p-3.5 rounded-xl bg-slate-800/60 border border-slate-700">
      <div class="font-bold text-sm text-blue-300 mb-2">
        📦 6 Biến Chi Tiêu Chính (Đầu vào mô hình phân cụm)
      </div>
      <div class="grid grid-cols-3 gap-2 text-xs">
        <div class="p-2 rounded bg-slate-900/60 border border-slate-700/50">
          <span class="text-emerald-400 font-bold">1. Fresh:</span> Hàng tươi sống
        </div>
        <div class="p-2 rounded bg-slate-900/60 border border-slate-700/50">
          <span class="text-emerald-400 font-bold">2. Milk:</span> Sữa & chế phẩm sữa
        </div>
        <div class="p-2 rounded bg-slate-900/60 border border-slate-700/50">
          <span class="text-emerald-400 font-bold">3. Grocery:</span> Hàng tạp hóa tổng hợp
        </div>
        <div class="p-2 rounded bg-slate-900/60 border border-slate-700/50">
          <span class="text-emerald-400 font-bold">4. Frozen:</span> Thực phẩm đông lạnh
        </div>
        <div class="p-2 rounded bg-slate-900/60 border border-slate-700/50">
          <span class="text-emerald-400 font-bold">5. Detergents_Paper:</span> Bột giặt & giấy
        </div>
        <div class="p-2 rounded bg-slate-900/60 border border-slate-700/50">
          <span class="text-emerald-400 font-bold">6. Delicassen:</span> Đồ nguội chế biến sẵn
        </div>
      </div>
    </div>

    <div class="p-3.5 rounded-xl bg-rose-500/10 border border-rose-500/30">
      <div class="font-bold text-sm text-rose-300 mb-1">
        🛡️ Vai Trò Của Channel & Region — Ràng Buộc Bất Biến
      </div>
      <div class="text-xs text-gray-300 space-y-1 leading-relaxed">
        <p>• <b>Channel</b> (1: Horeca - 298 mẫu; 2: Retail - 142 mẫu) và <b>Region</b> (1: Lisbon - 77; 2: Oporto - 47; 3: Other - 316).</p>
        <p class="text-amber-300 font-semibold">• Ràng buộc học thuật: Tuyệt đối KHÔNG đưa Channel/Region vào fit K-Means và KHÔNG dùng làm ground-truth để chọn K!</p>
        <p>• Chỉ ghép lại để <b>profiling và phân tích chéo</b> sau khi đã hình thành các cụm thuần túy từ 6 biến chi tiêu.</p>
      </div>
    </div>
  </div>
</div>

<!--
Về dữ liệu: 440 khách hàng bán sỉ từ UCI. Có 6 biến chi tiêu năm. Channel và Region chỉ được dùng để profiling sau khi phân cụm, không đưa vào quá trình fit K-Means.
-->

---
transition: slide-left
---

# 3. Quy Tắc Chống Rò Rỉ Dữ Liệu (Anti-Leakage Pipeline)

<div class="text-xs text-gray-300 mb-3">
  Nguyên tắc không thương lượng: <b>Chia tập dữ liệu TRƯỚC mọi bước học từ dữ liệu</b> (fit transformer, fit scaler, fit K-Means).
</div>

<div class="grid grid-cols-3 gap-4 mb-4">
  <div class="p-3.5 rounded-xl bg-blue-950/40 border border-blue-500/40 text-center">
    <div class="text-xs font-bold text-blue-400 uppercase tracking-wider">Tập Train (60%)</div>
    <div class="text-2xl font-black text-white my-1">264</div>
    <div class="text-[11px] text-gray-300">Dùng học tham số tiền xử lý & fit các mô hình thử nghiệm</div>
  </div>
  <div class="p-3.5 rounded-xl bg-purple-950/40 border border-purple-500/40 text-center">
    <div class="text-xs font-bold text-purple-400 uppercase tracking-wider">Tập Validation (20%)</div>
    <div class="text-2xl font-black text-white my-1">88</div>
    <div class="text-[11px] text-gray-300">Đánh giá Silhouette, Elbow, Stability để chọn mô hình D011</div>
  </div>
  <div class="p-3.5 rounded-xl bg-emerald-950/40 border border-emerald-500/40 text-center">
    <div class="text-xs font-bold text-emerald-400 uppercase tracking-wider">Tập Test Độc Lập (20%)</div>
    <div class="text-2xl font-black text-white my-1">88</div>
    <div class="text-[11px] text-gray-300">Khóa hoàn toàn. Đánh giá ĐÚNG 1 LẦN DUY NHẤT sau khi freeze!</div>
  </div>
</div>

<div class="grid grid-cols-2 gap-4 text-xs">
  <div class="p-3.5 rounded-xl bg-emerald-500/10 border border-emerald-500/30">
    <div class="font-bold text-emerald-300 flex items-center gap-1.5 mb-1.5">
      ✅ Quy Trình Chuẩn (Đúng Khoa Học)
    </div>
    <div class="text-gray-300 space-y-1">
      <div>1. Tách thô 440 dòng thành <code>Train (264) / Val (88) / Test (88)</code>.</div>
      <div>2. Fit <code>StandardScaler</code> CHỈ trên Train.</div>
      <div>3. Transform Validation bằng mean & std của Train để chọn cấu hình.</div>
      <div>4. Freeze cấu hình D011 → Refit trên 352 (Train+Val) → Test 88 một lần.</div>
    </div>
  </div>

  <div class="p-3.5 rounded-xl bg-rose-500/10 border border-rose-500/30">
    <div class="font-bold text-rose-300 flex items-center gap-1.5 mb-1.5">
      ❌ Sai Lầm Nghiêm Trọng Cần Tránh (Data Leakage)
    </div>
    <div class="text-gray-300 space-y-1">
      <div>• Fit <code>StandardScaler</code> trên toàn bộ 440 dòng trước khi split.</div>
      <div>• Nhìn kết quả tập Test để điều chỉnh K hoặc tham số tiền xử lý.</div>
      <div>• Sử dụng Channel/Region để ép thuật toán chọn K=2.</div>
      <div>• Rò rỉ phân phối tập kiểm thử vào không gian đặc trưng huấn luyện.</div>
    </div>
  </div>
</div>

<!--
Quy tắc chống rò rỉ dữ liệu là trọng tâm rubric: chia tập train/val/test trước mọi bước transform. Test 88 dòng được khóa hoàn toàn và chỉ đánh giá đúng một lần sau khi đóng băng quyết định D011.
-->

---
transition: slide-left
---

# 4. EDA & Tiền Xử Lý: Biến Đổi Log1p (Thí Nghiệm 1)

<div class="grid grid-cols-2 gap-4">
  <div>
    <div class="font-bold text-xs text-amber-300 mb-1 flex items-center gap-1">
      📉 Phân Phối Chi Tiêu Gốc: Lệch Phải Cực Nặng
    </div>
    <img src="/images/train_distributions_raw.png" class="rounded-lg border border-slate-700 h-44 w-full object-contain bg-slate-900/80" />
    <div class="mt-2 text-[11px] text-gray-300 leading-tight">
      <b>Skewness trên Train:</b> Fresh (2.56), Milk (4.05), Grocery (3.59), Frozen (5.91), Detergents_Paper (3.63), <b>Delicassen (11.15)</b>.
      Khoảng cách Euclidean bị chi phối bởi các khách hàng cực lớn.
    </div>
  </div>

  <div>
    <div class="font-bold text-xs text-emerald-300 mb-1 flex items-center gap-1">
      📈 Sau Biến Đổi $log(1+x)$ & StandardScaler
    </div>
    <img src="/images/train_distributions_log1p.png" class="rounded-lg border border-slate-700 h-44 w-full object-contain bg-slate-900/80" />
    <div class="mt-2 text-[11px] text-gray-300 leading-tight">
      <b>Hiệu quả:</b> Đưa phân phối 6 biến về dạng chuông gần đối xứng (skewness dao động quanh -0.8 đến 0.4).
      Sau đó <code>StandardScaler</code> chuẩn hóa mean=0, std=1, giúp khoảng cách Euclidean công bằng giữa các chiều.
    </div>
  </div>
</div>

<div class="mt-3 p-2.5 rounded-lg bg-blue-950/40 border border-blue-500/30 text-xs flex justify-between items-center text-gray-300">
  <span><b>Kết luận Thí nghiệm 1:</b> Không dùng biến đổi "vì đề yêu cầu" mà dựa trên bằng chứng số liệu phân phối và độ co cụm không gian.</span>
  <span class="text-blue-400 font-semibold text-[11px]">Bằng chứng: <code>reports/data/eda/train_skewness.csv</code></span>
</div>

<!--
Thí nghiệm 1 so sánh Raw và Log1p. Phân phối gốc lệch phải cực nặng với skewness lên tới 11.15 ở Delicassen. Biến đổi log1p và StandardScaler giúp khoảng cách Euclidean trong K-Means phản ánh đúng tương quan tỷ trọng thay vì bị áp đảo bởi giá trị ngoại lệ.
-->

---
transition: slide-left
---

# 5. Thiết Kế Thí Nghiệm & Baseline Tham Chiếu

<div class="grid grid-cols-3 gap-4 mt-2">
  <div class="p-3.5 rounded-xl bg-slate-800/80 border border-slate-700">
    <div class="font-bold text-xs text-gray-300 uppercase tracking-wider mb-2">Baseline A — Không Chia Cụm</div>
    <div class="text-xs text-gray-300 space-y-2">
      <p>Thống kê mô tả toàn bộ tập dữ liệu (mean, median, IQR 6 biến) làm mốc tham chiếu tổng thể.</p>
      <div class="p-2 rounded bg-black/40 font-mono text-[11px] text-cyan-300">
        Inertia tham chiếu = Tổng phương sai toàn bộ mẫu
      </div>
      <p class="text-[11px] text-gray-400">Giúp trả lời: Liệu việc phân nhóm có thực sự giảm phương sai nội bộ hay không?</p>
    </div>
  </div>

  <div class="p-3.5 rounded-xl bg-slate-800/80 border border-slate-700">
    <div class="font-bold text-xs text-rose-300 uppercase tracking-wider mb-2">Baseline B — K=2 Trên Dữ Liệu Raw</div>
    <div class="text-xs text-gray-300 space-y-2">
      <p>K-Means mặc định K=2 trên dữ liệu thô (chưa log, chưa scale).</p>
      <div class="p-2 rounded bg-black/40 font-mono text-[11px] text-amber-300">
        Val Silhouette = 0.6103<br>
        Min Cluster Share = 17.80%
      </div>
      <p class="text-[11px] text-gray-400"><b>Ảo tưởng Silhouette:</b> Điểm cao do vài ngoại lệ gom thành cụm nhỏ rời rạc, không mang giá trị kinh doanh.</p>
    </div>
  </div>

  <div class="p-3.5 rounded-xl bg-blue-950/40 border border-blue-500/40">
    <div class="font-bold text-xs text-blue-300 uppercase tracking-wider mb-2">Lưới Thí Nghiệm Đầy Đủ</div>
    <div class="text-xs text-gray-300 space-y-1.5">
      <div>• <b>2 nhánh tiền xử lý:</b> Raw vs. Log1p+StandardScaler</div>
      <div>• <b>Phạm vi K:</b> Duyệt $K \in [2, 8]$</div>
      <div>• <b>10 random seeds:</b> 0..9 để đo độ ổn định ARI</div>
      <div>• <b>Tổng cộng:</b> 140 runs huấn luyện + 630 cặp so sánh ARI</div>
      <div class="p-2 rounded bg-emerald-500/10 border border-emerald-500/20 text-emerald-300 text-[11px] mt-2">
        Mọi metric ghi nhận tại: <code>reports/data/experiments/</code>
      </div>
    </div>
  </div>
</div>

<div class="mt-4 p-3 rounded-xl bg-slate-900 border border-slate-700 text-xs">
  <div class="font-bold text-cyan-300 mb-1">Quy Tắc Đánh Giá Đa Chiều (Không Dùng Điểm Đơn Lẻ)</div>
  <div class="grid grid-cols-4 gap-2 text-center text-gray-300 text-[11px]">
    <div class="p-1.5 rounded bg-slate-800">1. Inertia / Elbow Plot</div>
    <div class="p-1.5 rounded bg-slate-800">2. Silhouette Score</div>
    <div class="p-1.5 rounded bg-slate-800">3. Độ ổn định qua seed (ARI)</div>
    <div class="p-1.5 rounded bg-slate-800">4. Kích thước & Khả năng diễn giải</div>
  </div>
</div>

<!--
Chúng tôi thiết lập Baseline A (không chia cụm) và Baseline B (K=2 dữ liệu thô). Điểm thú vị là Baseline B có Silhouette 0.6103 rất cao, nhưng đây là ảo tưởng do các điểm ngoại lệ chi phối. Lưới thí nghiệm 140 runs giúp chúng tôi có cái nhìn toàn diện.
-->

---
transition: slide-left
---

# 6. Lựa Chọn K: Đồ Thị Elbow & Silhouette (Thí Nghiệm 2)

<div class="grid grid-cols-2 gap-4">
  <div>
    <div class="font-bold text-xs text-blue-300 mb-1 flex items-center gap-1">
      📉 Đồ Thị Elbow — Quán Tính (Inertia) Trên Train
    </div>
    <img src="/images/elbow_train.png" class="rounded-lg border border-slate-700 h-44 w-full object-contain bg-slate-900/80" />
    <div class="mt-2 text-[11px] text-gray-300">
      Độ dốc quán tính giảm mạnh nhất từ $K=2$ sang $K=3$, sau đó giảm đều đặn từ $K=4$ đến $K=8$.
      Điểm "khuỷu tay" rõ nét nhất xuất hiện tại vùng $K=2$ và $K=3$.
    </div>
  </div>

  <div>
    <div class="font-bold text-xs text-purple-300 mb-1 flex items-center gap-1">
      📊 Hệ Số Silhouette Trên Tập Validation (88 Mẫu)
    </div>
    <img src="/images/validation_silhouette.png" class="rounded-lg border border-slate-700 h-44 w-full object-contain bg-slate-900/80" />
    <div class="mt-2 text-[11px] text-gray-300">
      Với <code>log1p_standardscaler</code>: <b>K=2 đạt Silhouette trung bình cao nhất (0.3066)</b>, tiếp đến là $K=3$ (0.2165).
      Từ $K \ge 4$, Silhouette giảm sâu ($< 0.16$).
    </div>
  </div>
</div>

<div class="mt-3 overflow-x-auto">
  <table class="w-full text-xs text-left text-gray-300 border border-slate-700 rounded-lg overflow-hidden">
    <thead class="bg-slate-800 text-gray-200 text-[11px] uppercase">
      <tr>
        <th class="p-1.5">Số Cụm (K)</th>
        <th class="p-1.5">Val Silhouette Mean</th>
        <th class="p-1.5">ARI Mean (Ổn định)</th>
        <th class="p-1.5">ARI Min</th>
        <th class="p-1.5">Min Cluster Share</th>
        <th class="p-1.5">Gen Gap Abs</th>
      </tr>
    </thead>
    <tbody class="divide-y divide-slate-800 text-[11px]">
      <tr class="bg-emerald-950/30 text-emerald-300 font-bold">
        <td class="p-1.5">K = 2 (Đề xuất D011)</td>
        <td class="p-1.5">0.3066</td>
        <td class="p-1.5">0.9970</td>
        <td class="p-1.5">0.9848</td>
        <td class="p-1.5">44.73%</td>
        <td class="p-1.5">0.0310</td>
      </tr>
      <tr>
        <td class="p-1.5">K = 3</td>
        <td class="p-1.5">0.2165</td>
        <td class="p-1.5">0.9078</td>
        <td class="p-1.5">0.7982</td>
        <td class="p-1.5">30.38%</td>
        <td class="p-1.5">0.0116</td>
      </tr>
      <tr>
        <td class="p-1.5">K = 4</td>
        <td class="p-1.5">0.1540</td>
        <td class="p-1.5">0.9152</td>
        <td class="p-1.5">0.7916</td>
        <td class="p-1.5">12.54%</td>
        <td class="p-1.5">0.0520</td>
      </tr>
    </tbody>
  </table>
</div>

<!--
Thí nghiệm 2: Elbow và Silhouette trên tập Validation. K=2 cho Silhouette 0.3066, tỷ lệ cụm nhỏ nhất lên tới 44.73%, độ lệch giữa train và val chỉ 0.0310, vượt trội hoàn toàn so với K>=4.
-->

---
transition: slide-left
---

# 7. Độ Ổn Định Qua Seed & Quyết Định Đóng Băng D011 (Thí Nghiệm 3)

<div class="grid grid-cols-2 gap-4">
  <div>
    <div class="font-bold text-xs text-cyan-300 mb-1 flex items-center gap-1">
      🎲 Độ Ổn Định Adjusted Rand Index (ARI) Qua 10 Seeds
    </div>
    <img src="/images/stability_ari.png" class="rounded-lg border border-slate-700 h-44 w-full object-contain bg-slate-900/80" />
    <div class="mt-2 text-[11px] text-gray-300">
      Đo lường tính bất biến của phân cụm khi thay đổi khởi tạo tâm cụm ngẫu nhiên (seed 0..9).
      $K=2$ đạt độ đồng thuận <b>ARI = 0.9970 (gần như tuyệt đối)</b>, trong khi $K \ge 5$ độ ổn định tụt xuống dưới 0.6.
    </div>
  </div>

  <div class="space-y-3">
    <div class="p-3 rounded-xl bg-slate-800/80 border border-slate-700">
      <div class="font-bold text-xs text-emerald-400 mb-1 flex items-center gap-1.5">
        📋 Hồ Sơ Quyết Định Đóng Băng D011
      </div>
      <div class="text-xs space-y-1.5 text-gray-300 font-mono">
        <div>• Quyết định: <span class="text-emerald-300 font-bold">D011 (models/selection.json)</span></div>
        <div>• Tiền xử lý: <span class="text-blue-300">log1p_standardscaler</span></div>
        <div>• Số cụm K: <span class="text-purple-300 font-bold">2</span> | Seed: <span class="text-gray-200">42</span></div>
        <div>• Thuật toán: <span class="text-gray-200">Lloyd</span> | n_init: <span class="text-gray-200">10</span> | max_iter: <span class="text-gray-200">300</span></div>
        <div>• Phạm vi refit: <span class="text-amber-300">352 (Train 264 + Val 88)</span></div>
      </div>
    </div>

    <div class="p-3 rounded-xl bg-blue-950/40 border border-blue-500/30">
      <div class="font-bold text-xs text-blue-300 mb-1">
        Lý Do Lựa Chọn K=2 Thay Vì K=3
      </div>
      <ul class="text-[11px] text-gray-300 space-y-1 list-disc pl-4">
        <li><b>Chất lượng hình học:</b> Silhouette $0.3066$ cao hơn đáng kể so với $0.2165$ ($K=3$).</li>
        <li><b>Độ ổn định:</b> ARI $0.9970$ so với $0.9078$ (ít nhạy cảm với nhiễu).</li>
        <li><b>Cân bằng quy mô:</b> Tỷ lệ cụm nhỏ nhất $44.73\%$ vs $30.38\%$.</li>
        <li><b>Ý nghĩa kinh doanh:</b> Phân định rõ 2 trụ cột phân phối: Hàng tươi & Hàng bách hóa.</li>
      </ul>
    </div>
  </div>
</div>

<!--
Thí nghiệm 3: Kiểm tra độ ổn định qua 10 seed. K=2 đạt ARI 0.9970, cực kỳ ổn định. Do đó, nhóm quyết định đóng băng cấu hình D011: K=2, log1p + StandardScaler, seed 42, thuật toán Lloyd.
-->

---
transition: slide-left
---

# 8. Đánh Giá Độc Lập Trên Tập Test (Final Evaluation)

<div class="text-xs text-gray-300 mb-3">
  Mô hình D011 được refit trên toàn bộ <b>352 mẫu phát triển</b> và đánh giá <b>DUY NHẤT MỘT LẦN</b> trên <b>88 mẫu Test độc lập</b> đã khóa.
</div>

<div class="grid grid-cols-2 gap-6">
  <div class="p-4 rounded-xl bg-slate-800/80 border border-slate-700 space-y-3">
    <div class="font-bold text-sm text-cyan-300 border-b border-slate-700 pb-2">
      🧪 Kết Quả Đánh Giá Đối Soát
    </div>
    <div class="grid grid-cols-2 gap-3 text-center">
      <div class="p-3 rounded-lg bg-black/40 border border-slate-700">
        <div class="text-[11px] text-gray-400">Tập Phát Triển (352 dòng)</div>
        <div class="text-xl font-bold text-white mt-1">0.2892</div>
        <div class="text-[10px] text-gray-400">Silhouette Score</div>
        <div class="text-[11px] text-cyan-300 font-mono mt-1">Inertia: 4.1639 / dòng</div>
      </div>
      <div class="p-3 rounded-lg bg-emerald-950/40 border border-emerald-500/40">
        <div class="text-[11px] text-emerald-300 font-semibold">Tập Test Độc Lập (88 dòng)</div>
        <div class="text-xl font-bold text-emerald-400 mt-1">0.2389</div>
        <div class="text-[10px] text-gray-400">Silhouette Score</div>
        <div class="text-[11px] text-emerald-300 font-mono mt-1">Inertia: 4.5051 / dòng</div>
      </div>
    </div>
    <div class="text-xs text-gray-300 leading-relaxed pt-1">
      • Độ suy giảm Silhouette (Generalization Gap) chỉ là <b>0.0503</b>, cho thấy mô hình không bị quá khớp (overfitting) và duy trì tính khái quát hóa xuất sắc trên dữ liệu chưa từng thấy.
    </div>
  </div>

  <div class="p-4 rounded-xl bg-slate-800/80 border border-slate-700 space-y-3">
    <div class="font-bold text-sm text-purple-300 border-b border-slate-700 pb-2">
      🎯 Phân Bố Cụm Trên Tập Kiểm Thử (88 Mẫu)
    </div>
    <div class="grid grid-cols-2 gap-3 text-center">
      <div class="p-3 rounded-lg bg-blue-950/40 border border-blue-500/30">
        <div class="text-xs text-blue-300 font-semibold">Cụm 0 (Tạp hóa / Bách hóa)</div>
        <div class="text-2xl font-black text-white mt-1">45 <span class="text-sm font-normal text-gray-400">(51.1%)</span></div>
        <div class="text-[10px] text-gray-400 mt-1">Mẫu kiểm thử</div>
      </div>
      <div class="p-3 rounded-lg bg-emerald-950/40 border border-emerald-500/30">
        <div class="text-xs text-emerald-300 font-semibold">Cụm 1 (Tươi sống / Horeca)</div>
        <div class="text-2xl font-black text-white mt-1">43 <span class="text-sm font-normal text-gray-400">(48.9%)</span></div>
        <div class="text-[10px] text-gray-400 mt-1">Mẫu kiểm thử</div>
      </div>
    </div>
    <div class="p-2.5 rounded bg-emerald-500/10 border border-emerald-500/30 text-xs text-emerald-200">
      <b>Tỷ lệ cụm nhỏ nhất: 48.86%</b> — Cấu trúc phân khúc vô cùng cân bằng, không có hiện tượng tạo cụm rác hay cụm thiểu số.
    </div>
    <div class="text-[10px] text-gray-400">
      *Chứng thực toàn vẹn: SHA-256 khớp 100% trong <code>models/final_evaluation.json</code>.
    </div>
  </div>
</div>

<!--
Trên tập test độc lập 88 dòng, đánh giá duy nhất một lần: Silhouette đạt 0.2389, tỷ lệ cụm 45/43 cực kỳ cân bằng (48.86%). Generalization gap chỉ 0.0503 chứng minh mô hình tổng quát hóa rất tốt.
-->

---
transition: slide-left
---

# 9. Hồ Sơ Phân Khúc & Ý Nghĩa Kinh Doanh (Thí Nghiệm 4)

<div class="grid grid-cols-2 gap-4">
  <div class="p-3.5 rounded-xl bg-blue-950/30 border border-blue-500/30">
    <div class="flex justify-between items-center mb-2">
      <span class="font-bold text-sm text-blue-300">Cụm 0: "Tạp Hóa & Hóa Phẩm"</span>
      <span class="px-2 py-0.5 rounded text-xs bg-blue-500/20 text-blue-300">162 KH (46.0%)</span>
    </div>
    <div class="text-xs text-gray-300 space-y-1.5">
      <div><b>Trung vị chi tiêu (Medians m.u.):</b></div>
      <div class="grid grid-cols-3 gap-1 font-mono text-[11px] text-gray-200 bg-black/40 p-2 rounded">
        <div>Grocery: <b class="text-cyan-300">10,843</b></div>
        <div>Milk: <b class="text-cyan-300">7,226</b></div>
        <div>Det_Paper: <b class="text-cyan-300">4,085</b></div>
        <div>Fresh: 6,411</div>
        <div>Frozen: 1,153</div>
        <div>Delicassen: 1,509</div>
      </div>
      <div><b>Đặc tính kinh doanh:</b></div>
      <ul class="text-[11px] text-gray-300 list-disc pl-4 space-y-0.5">
        <li>Chi tiêu cực cao ở hàng khô, bách hóa, sữa và chất tẩy rửa.</li>
        <li><b>Kênh phân phối (Channel):</b> <b>66.7% là Bán lẻ (Retail)</b>, 33.3% là Horeca.</li>
        <li>Khoảng cách tâm cụm: Trung vị 1.75, 5 điểm ngoại lệ IQR.</li>
      </ul>
    </div>
  </div>

  <div class="p-3.5 rounded-xl bg-emerald-950/30 border border-emerald-500/30">
    <div class="flex justify-between items-center mb-2">
      <span class="font-bold text-sm text-emerald-300">Cụm 1: "Hàng Tươi Sống & Đông Lạnh"</span>
      <span class="px-2 py-0.5 rounded text-xs bg-emerald-500/20 text-emerald-300">190 KH (54.0%)</span>
    </div>
    <div class="text-xs text-gray-300 space-y-1.5">
      <div><b>Trung vị chi tiêu (Medians m.u.):</b></div>
      <div class="grid grid-cols-3 gap-1 font-mono text-[11px] text-gray-200 bg-black/40 p-2 rounded">
        <div>Fresh: <b class="text-emerald-300">9,728</b></div>
        <div>Frozen: <b class="text-emerald-300">2,195</b></div>
        <div>Delicassen: 662</div>
        <div>Grocery: 2,176</div>
        <div>Milk: 1,626</div>
        <div>Det_Paper: 280</div>
      </div>
      <div><b>Đặc tính kinh doanh:</b></div>
      <ul class="text-[11px] text-gray-300 list-disc pl-4 space-y-0.5">
        <li>Ưu tiên hàng tươi sống và đông lạnh; tiêu thụ chất tẩy rửa rất thấp.</li>
        <li><b>Kênh phân phối (Channel):</b> <b>97.9% là Horeca</b> (Khách sạn/Nhà hàng/Cafe)!</li>
        <li>Khoảng cách tâm cụm: Trung vị 1.57, 11 điểm ngoại lệ IQR.</li>
      </ul>
    </div>
  </div>
</div>

<div class="mt-3 p-3 rounded-xl bg-slate-900 border border-slate-700">
  <div class="font-bold text-xs text-amber-300 mb-1">💡 Chiến Lược Kinh Doanh Thực Tế Cho Nhà Phân Phối</div>
  <div class="grid grid-cols-2 gap-4 text-xs text-gray-300">
    <div>• <b>Với Nhóm Cụm 0 (Bán lẻ):</b> Xây dựng chính sách chiết khấu bậc thang theo số lượng hàng khô, combo Bách hóa + Giấy tẩy rửa, tối ưu chu kỳ giao định kỳ theo tuần.</div>
    <div>• <b>Với Nhóm Cụm 1 (Horeca):</b> Đầu tư chuỗi cung ứng lạnh chuyên dụng (Cold Chain), cam kết giao tươi trong ngày, đảm bảo vệ sinh an toàn thực phẩm.</div>
  </div>
</div>

<!--
Thí nghiệm 4 là phân tích hồ sơ cụm. Cụm 0 là khách hàng tạp hóa/bán lẻ chi tiêu mạnh vào Grocery, Milk, Detergents_Paper. Cụm 1 là nhóm Horeca chiếm tới 97.9% kênh Horeca, chi tiêu chủ lực vào Fresh và Frozen.
-->

---
transition: slide-left
---

# 10. Mở Rộng: PCA 2D & Đối Chiếu Phân Cụm Thứ Bậc (Ward)

<div class="grid grid-cols-2 gap-4 mt-1">
  <div class="p-3.5 rounded-xl bg-slate-800/80 border border-slate-700 space-y-2">
    <div class="font-bold text-xs text-cyan-300 flex items-center gap-1.5">
      🔮 Trực Quan Hóa Bằng PCA 2 Chiều
    </div>
    <div class="text-xs text-gray-300 space-y-1.5">
      <div class="grid grid-cols-2 gap-2 text-center my-2">
        <div class="p-2 rounded bg-black/40">
          <div class="text-[10px] text-gray-400">Phương sai PC1</div>
          <div class="text-base font-bold text-cyan-300">44.93%</div>
        </div>
        <div class="p-2 rounded bg-black/40">
          <div class="text-[10px] text-gray-400">Phương sai PC2</div>
          <div class="text-base font-bold text-cyan-300">27.00%</div>
        </div>
      </div>
      <p>• <b>Tổng phương sai giải thích: 71.93%</b> — Giữ lại phần lớn thông tin cấu trúc của không gian 6 chiều gốc.</p>
      <p>• <b>Vai trò kỹ thuật:</b> PCA chỉ phục vụ trực quan hóa 2D trên Dashboard, <b>tuyệt đối không thay thế 6 biến gốc</b> khi suy luận.</p>
    </div>
  </div>

  <div class="p-3.5 rounded-xl bg-slate-800/80 border border-slate-700 space-y-2">
    <div class="font-bold text-xs text-purple-300 flex items-center gap-1.5">
      🌲 Đối Chiếu Phân Cụm Thứ Bậc (Hierarchical Ward)
    </div>
    <div class="text-xs text-gray-300 space-y-1.5">
      <div class="grid grid-cols-2 gap-2 text-center my-2">
        <div class="p-2 rounded bg-black/40">
          <div class="text-[10px] text-gray-400">Silhouette 6D Ward</div>
          <div class="text-base font-bold text-purple-300">0.2626</div>
        </div>
        <div class="p-2 rounded bg-black/40">
          <div class="text-[10px] text-gray-400">ARI (KMeans ↔ Ward)</div>
          <div class="text-base font-bold text-emerald-400">0.6872</div>
        </div>
      </div>
      <p>• <b>Quy mô cụm Ward:</b> 194 / 158 mẫu (so với KMeans: 162 / 190 mẫu).</p>
      <p>• <b>Ma trận liên kết (Contingency):</b> Khớp chính xác <b>322 / 352 mẫu (91.5%)</b> giữa hai thuật toán độc lập.</p>
      <p class="text-[11px] text-emerald-300">→ Chứng minh cấu trúc 2 phân khúc là đặc trưng tự nhiên có sẵn của tập dữ liệu.</p>
    </div>
  </div>
</div>

<div class="mt-3 p-3 rounded-xl bg-blue-950/40 border border-blue-500/30 text-xs text-gray-300 flex justify-between items-center">
  <span><b>Bằng chứng phát triển:</b> Tính toán offline, kiểm định SHA-256 qua CI <code>Gate 10.2</code>, phục vụ qua API đọc độc lập.</span>
  <span class="text-cyan-300 font-mono text-[11px]">reports/data/development_extension/analysis.json</span>
</div>

<!--
Phần mở rộng: PCA 2 chiều giải thích 71.93% phương sai dữ liệu. Khi so sánh với thuật toán Hierarchical Clustering Ward, ARI đạt 0.6872 và độ trùng khớp nhãn lên tới 91.5%, chứng minh sự tồn tại vững chắc của 2 phân khúc.
-->

---
transition: slide-left
---

# 11. Kiến Trúc Triển Khai Web & Production Serving

<div class="grid grid-cols-3 gap-4 mt-2">
  <div class="p-3.5 rounded-xl bg-slate-800/80 border border-slate-700 space-y-2">
    <div class="font-bold text-xs text-blue-300 uppercase tracking-wider flex items-center gap-1">
      ⚡ Backend Serving Fastify
    </div>
    <div class="text-xs text-gray-300 space-y-1.5">
      <div>• <b>Node-native engine:</b> Nạp trực tiếp <code>models/model.json</code>, không phụ thuộc runtime Python khi online.</div>
      <div>• <b>Kiểm định SHA-256:</b> Từ chối phục vụ ngay nếu file model hoặc artifact bị giả mạo.</div>
      <div>• <b>Không train theo request:</b> Dùng mean/scale & centroid đã đóng băng D011.</div>
      <div>• <b>Endpoints:</b> <code>/api/segment</code>, <code>/api/dashboard</code>, <code>/api/model-info</code>, <code>/api/ready</code>.</div>
    </div>
  </div>

  <div class="p-3.5 rounded-xl bg-slate-800/80 border border-slate-700 space-y-2">
    <div class="font-bold text-xs text-emerald-300 uppercase tracking-wider flex items-center gap-1">
      💻 Frontend React 3 Màn Hình
    </div>
    <div class="text-xs text-gray-300 space-y-1.5">
      <div>• <b>1. Giới thiệu & Phạm vi:</b> Bối cảnh, Data Card, giới hạn mô hình.</div>
      <div>• <b>2. Phân khúc khách hàng:</b> Form nhập 6 biến, kiểm tra ngoài miền, giải thích cụm & khoảng cách.</div>
      <div>• <b>3. Dashboard & Model Card:</b> Trực quan hóa Elbow, Silhouette, PCA 2D tương tác và Ward benchmark.</div>
      <div>• <b>Batch CSV:</b> Hỗ trợ tải file CSV tối đa 100 dòng.</div>
    </div>
  </div>

  <div class="p-3.5 rounded-xl bg-slate-800/80 border border-slate-700 space-y-2">
    <div class="font-bold text-xs text-purple-300 uppercase tracking-wider flex items-center gap-1">
      🧪 Kiểm Thử Toàn Diện (CI/CD)
    </div>
    <div class="text-xs text-gray-300 space-y-1.5">
      <div>• <b>Python Parity Test:</b> Kiểm tra khớp số học 100% giữa scikit-learn và Node.js.</div>
      <div>• <b>Vitest Unit/API:</b> 16/16 test Fastify endpoints.</div>
      <div>• <b>Playwright E2E:</b> <b>64/64 test PASS</b> trên cả Desktop và Mobile Chromium.</div>
      <div>• <b>Chống crash:</b> Xử lý nghiêm ngặt lỗi mạng, 503 retry và bảo vệ công thức CSV.</div>
    </div>
  </div>
</div>

<div class="mt-4 p-3 rounded-xl bg-slate-900 border border-slate-700 text-xs">
  <div class="font-bold text-cyan-300 mb-1 flex items-center gap-1.5">
    ⚙️ Luồng Dữ Liệu Suy Luận Thực Tế (Online Inference Flow)
  </div>
  <div class="flex items-center justify-between text-[11px] text-gray-300 font-mono bg-black/40 p-2.5 rounded">
    <span class="text-amber-300">Client Input (6 số)</span>
    <span>➔</span>
    <span class="text-blue-300">Validate Schema & Min/Max Bounds</span>
    <span>➔</span>
    <span class="text-purple-300">log1p(x)</span>
    <span>➔</span>
    <span class="text-purple-300">StandardScaler (frozen)</span>
    <span>➔</span>
    <span class="text-emerald-300">Euclidean Centroid Distance</span>
    <span>➔</span>
    <span class="text-cyan-300">Cluster ID & Profile Response</span>
  </div>
</div>

<!--
Kiến trúc triển khai: Tách hoàn toàn huấn luyện và phục vụ. Fastify phục vụ API xác thực SHA-256 model đóng băng, giao diện React 3 màn hình và kiểm thử tự động 64/64 test Playwright.
-->

---
transition: slide-left
---

# 12. Tổng Kết Đồ Án, Giới Hạn & Hướng Phát Triển

<div class="grid grid-cols-2 gap-4">
  <div class="p-3.5 rounded-xl bg-emerald-950/30 border border-emerald-500/30 space-y-2">
    <div class="font-bold text-xs text-emerald-400 flex items-center gap-1">
      🏆 Thành Quả Đạt Được (100% Rubric)
    </div>
    <ul class="text-xs text-gray-300 space-y-1.5 list-disc pl-4">
      <li>Quy trình chuẩn khoa học dữ liệu: Tách độc lập Train/Val/Test, <b>không data leakage</b>.</li>
      <li>Hoàn thành đầy đủ <b>4 thí nghiệm bắt buộc</b> + 1 thí nghiệm mở rộng PCA & Hierarchical.</li>
      <li>Chọn $K=2$ dựa trên bằng chứng đa chiều (Elbow, Silhouette, ARI stability, Business logic).</li>
      <li>Đánh giá tập Test đúng 1 lần với kết quả xuất sắc: Silhouette 0.2389, tỷ lệ 45/43.</li>
      <li>Sản phẩm ứng dụng web hoàn chỉnh, có kiểm tra đầu vào, model card và API đầy đủ.</li>
    </ul>
  </div>

  <div class="p-3.5 rounded-xl bg-amber-950/30 border border-amber-500/30 space-y-2">
    <div class="font-bold text-xs text-amber-400 flex items-center gap-1">
      ⚠️ Giới Hạn Nghiên Cứu Hiện Tại
    </div>
    <ul class="text-xs text-gray-300 space-y-1.5 list-disc pl-4">
      <li><b>Yêu cầu dữ liệu:</b> Chỉ áp dụng khi khách hàng đã có đủ 6 khoản chi tiêu cả năm (chưa hỗ trợ khách mới toanh chưa có lịch sử).</li>
      <li><b>Khoảng cách tâm cụm:</b> Đo lường độ lệch so với khách hàng điển hình, <b>không phải xác suất</b> hay độ tin cậy thống kê.</li>
      <li><b>Dữ liệu tĩnh:</b> Chưa có dấu thời gian (timestamps) của từng đơn hàng cụ thể theo tuần/tháng để phân tích xu hướng dịch chuyển cụm.</li>
    </ul>
  </div>
</div>

<div class="mt-3.5 p-3 rounded-xl bg-blue-950/40 border border-blue-500/30">
  <div class="font-bold text-xs text-blue-300 mb-1 flex items-center gap-1">
    🚀 Hướng Phát Triển Tiếp Theo
  </div>
  <div class="grid grid-cols-3 gap-3 text-xs text-gray-300">
    <div class="p-2 rounded bg-slate-900/80">
      <b class="text-cyan-300">1. Dữ liệu chuỗi thời gian:</b> Thu thập chi tiêu theo từng tháng để phát hiện xu hướng chuyển dịch phân khúc của khách hàng.
    </div>
    <div class="p-2 rounded bg-slate-900/80">
      <b class="text-cyan-300">2. Phát hiện bất thường:</b> Tích hợp mô hình Isolation Forest để tự động cảnh báo các giao dịch gian lận hoặc đột biến kho bãi.
    </div>
    <div class="p-2 rounded bg-slate-900/80">
      <b class="text-cyan-300">3. Tối ưu tồn kho tự động:</b> Kết nối phân khúc khách hàng vào hệ thống ERP để tự động gợi ý đơn đặt hàng chuỗi cung ứng lạnh.
    </div>
  </div>
</div>

<!--
Tổng kết đồ án: Đáp ứng trọn vẹn toàn bộ các tiêu chí rubric học thuật. Nhóm cũng chỉ rõ các giới hạn về thời điểm sử dụng và định hướng tích hợp dữ liệu chuỗi thời gian trong tương lai.
-->

---
layout: center
class: text-center
---

# HỎI ĐÁP (Q&A) & LỜI CẢM ƠN

<div class="mt-4 text-base text-gray-300">
  Kính mời Thầy PGS.TS. Nguyễn Văn Hậu và Hội đồng đặt câu hỏi.
</div>

<div class="mt-6 grid grid-cols-3 gap-4 max-w-2xl mx-auto text-left text-xs">
  <div class="p-3 rounded-lg bg-slate-800/80 border border-slate-700">
    <div class="font-bold text-cyan-300 mb-1">1. Về Rò Rỉ Dữ Liệu?</div>
    <div class="text-gray-300 text-[11px]">Cam kết split trước tiền xử lý; tập test 88 mẫu được niêm phong và chỉ đánh giá đúng 1 lần.</div>
  </div>
  <div class="p-3 rounded-lg bg-slate-800/80 border border-slate-700">
    <div class="font-bold text-emerald-300 mb-1">2. Vì Sao Chọn K=2?</div>
    <div class="text-gray-300 text-[11px]">Dựa trên Elbow, Silhouette (0.3066), độ ổn định ARI (0.9970) và ý nghĩa kinh doanh thực tế.</div>
  </div>
  <div class="p-3 rounded-lg bg-slate-800/80 border border-slate-700">
    <div class="font-bold text-purple-300 mb-1">3. Vai Trò Channel?</div>
    <div class="text-gray-300 text-[11px]">Không đưa vào fit hay chọn K; chỉ dùng để profiling và kiểm chứng đối soát sau phân cụm.</div>
  </div>
</div>

<div class="mt-8 text-xs text-gray-400">
  Kho mã nguồn & minh chứng đầy đủ: <code>Project 22 — Wholesale Customers Segmentation</code>
</div>
