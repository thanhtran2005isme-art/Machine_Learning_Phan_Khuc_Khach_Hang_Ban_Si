# -*- coding: utf-8 -*-
"""
Generate 15 High-Impact, Visually Stunning SVG Slides for Project 22 Presentation
Meets strict academic integrity, exact dataset numbers, and PPT Master quality standards.
"""

import os
from pathlib import Path

OUTPUT_DIR = Path("projects/project22_kmeans_presentation_20261026/svg_output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

FONT_FAMILY = "Arial, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"

def clean_xml(text):
    import re
    # Replace any & that is not followed by a valid lowercase entity
    text = re.sub(r'&(?!(amp|lt|gt|quot|apos);)', '&amp;', text)
    # Replace &AMP; with &amp;
    text = text.replace('&AMP;', '&amp;')
    return text

def save_svg(filename, content):
    path = OUTPUT_DIR / filename
    content = clean_xml(content.strip())
    with open(path, "w", encoding="utf-8") as f:
        f.write(content + "\n")
    print(f"Saved: {filename}")

def get_svg_wrapper(slide_num, title_cat, title_main, subtitle, content_xml, footer_text="", page_role="anchor"):
    slide_str = f"{slide_num:02d} / 15"
    cat_width = max(len(title_cat) * 9 + 30, 160)
    title_cat_clean = clean_xml(title_cat.upper())
    title_main_clean = clean_xml(title_main)
    subtitle_clean = clean_xml(subtitle)
    footer_text_clean = clean_xml(footer_text if footer_text else "Đồ Án Machine Learning Phân Khúc Khách Hàng Bán Sỉ • Project 22 (UCI Wholesale Customers)")
    
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" font-family="{FONT_FAMILY}">
  <defs>
    <linearGradient id="headerGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#1E3A8A"/>
      <stop offset="50%" stop-color="#2563EB"/>
      <stop offset="100%" stop-color="#0EA5E9"/>
    </linearGradient>
  </defs>

  <!-- Background Canvas -->
  <g id="page-background" data-pptx-role="background">
    <rect width="1280" height="720" fill="#F8FAFC"/>
    <rect width="1280" height="6" fill="url(#headerGrad)"/>
  </g>

  <!-- Slide Header -->
  <g id="header">
    <rect x="70" y="32" width="{cat_width}" height="26" rx="6" fill="#EFF6FF" stroke="#BFDBFE" stroke-width="1"/>
    <text x="{70 + cat_width / 2}" y="49" font-size="11" font-weight="bold" fill="#1D4ED8" text-anchor="middle" letter-spacing="1">{title_cat_clean}</text>
    <text x="70" y="92" font-size="32" font-weight="bold" fill="#0F172A">{title_main_clean}</text>
    <text x="70" y="118" font-size="15" fill="#475569">{subtitle_clean}</text>
  </g>

  <!-- Main Slide Content -->
  {content_xml}

  <!-- Slide Footer -->
  <g id="footer" data-pptx-role="footer">
    <line x1="70" y1="675" x2="1210" y2="675" stroke="#E2E8F0" stroke-width="1"/>
    <text x="70" y="696" font-size="13" fill="#64748B">{footer_text_clean}</text>
    <text x="1210" y="696" font-size="13" font-weight="bold" fill="#475569" text-anchor="end">{slide_str}</text>
  </g>
</svg>"""

# ==============================================================================
# SLIDE 01: COVER
# ==============================================================================
def gen_slide_01():
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" font-family="{FONT_FAMILY}">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0F172A"/>
      <stop offset="60%" stop-color="#1E293B"/>
      <stop offset="100%" stop-color="#0F172A"/>
    </linearGradient>
    <linearGradient id="glowBlue" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#3B82F6"/>
      <stop offset="100%" stop-color="#06B6D4"/>
    </linearGradient>
    <linearGradient id="cardBg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#1E293B" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="#0F172A" stop-opacity="0.9"/>
    </linearGradient>
  </defs>

  <!-- Dark Executive Background -->
  <g id="cover-background" data-pptx-role="background">
    <rect width="1280" height="720" fill="url(#bgGrad)"/>
    <circle cx="1100" cy="160" r="280" fill="#2563EB" opacity="0.08"/>
    <circle cx="200" cy="550" r="220" fill="#059669" opacity="0.06"/>
  </g>

  <!-- Top Category Badges -->
  <g id="hero-badge">
    <rect x="80" y="70" width="230" height="32" rx="16" fill="#1E3A8A" stroke="#3B82F6" stroke-width="1.5"/>
    <text x="195" y="91" font-size="12" font-weight="bold" fill="#60A5FA" text-anchor="middle">HỌC MÁY CƠ BẢN • ĐỒ ÁN 22</text>
    <rect x="325" y="70" width="220" height="32" rx="16" fill="#064E3B" stroke="#10B981" stroke-width="1.5"/>
    <text x="435" y="91" font-size="13" font-weight="bold" fill="#34D399" text-anchor="middle">UCI WHOLESALE CUSTOMERS</text>
  </g>

  <!-- Title & Subtitle -->
  <g id="hero-title">
    <text x="80" y="180" font-size="52" font-weight="bold" fill="#FFFFFF">PHÂN KHÚC KHÁCH HÀNG BÁN SỈ</text>
    <text x="80" y="240" font-size="32" font-weight="bold" fill="url(#glowBlue)">Với K-Means Clustering &amp; Web Serving Architecture</text>
    <text x="80" y="295" font-size="18" fill="#94A3B8">Phân tích chuyên sâu 6 đặc trưng chi tiêu, tối ưu K=2, chống rò rỉ dữ liệu và triển khai Production API</text>
  </g>

  <!-- 3 Big Stat Cards -->
  <g id="hero-kpis">
    <!-- Card 1: Data -->
    <rect x="80" y="350" width="345" height="150" rx="14" fill="url(#cardBg)" stroke="#334155" stroke-width="1.5"/>
    <rect x="80" y="350" width="345" height="4" rx="2" fill="#3B82F6"/>
    <text x="110" y="395" font-size="14" font-weight="bold" fill="#94A3B8" letter-spacing="1">QUY MÔ DỮ LIỆU</text>
    <text x="110" y="445" font-size="32" font-weight="bold" fill="#38BDF8">440 <tspan font-size="18" fill="#94A3B8" font-weight="normal">Khách Hàng</tspan></text>
    <text x="110" y="480" font-size="14" fill="#CBD5E1">6 biến chi tiêu monetary units + 2 biến phân tích</text>

    <!-- Card 2: Model -->
    <rect x="465" y="350" width="345" height="150" rx="14" fill="url(#cardBg)" stroke="#334155" stroke-width="1.5"/>
    <rect x="465" y="350" width="345" height="4" rx="2" fill="#10B981"/>
    <text x="495" y="395" font-size="14" font-weight="bold" fill="#94A3B8" letter-spacing="1">MÔ HÌNH ĐÓNG BĂNG D011</text>
    <text x="495" y="445" font-size="32" font-weight="bold" fill="#34D399">K = 2 <tspan font-size="18" fill="#94A3B8" font-weight="normal">Cụm Tối Ưu</tspan></text>
    <text x="495" y="480" font-size="14" fill="#CBD5E1">Log1p + Scaler | ARI: 0.997 | Sil: 0.307 val</text>

    <!-- Card 3: System -->
    <rect x="850" y="350" width="345" height="150" rx="14" fill="url(#cardBg)" stroke="#334155" stroke-width="1.5"/>
    <rect x="850" y="350" width="345" height="4" rx="2" fill="#A855F7"/>
    <text x="880" y="395" font-size="14" font-weight="bold" fill="#94A3B8" letter-spacing="1">KIẾN TRÚC TRIỂN KHAI</text>
    <text x="880" y="445" font-size="32" font-weight="bold" fill="#C084FC">Full Stack <tspan font-size="18" fill="#94A3B8" font-weight="normal">Web Serving</tspan></text>
    <text x="880" y="480" font-size="14" fill="#CBD5E1">Fastify API + React Client + 100% CI Testing</text>
  </g>

  <!-- Author & Supervisor Section -->
  <g id="hero-metadata">
    <rect x="80" y="535" width="1115" height="110" rx="12" fill="#1E293B" stroke="#334155" stroke-width="1"/>
    
    <!-- Supervisor -->
    <text x="120" y="575" font-size="13" font-weight="bold" fill="#64748B" letter-spacing="1">GIẢNG VIÊN HƯỚNG DẪN</text>
    <text x="120" y="605" font-size="18" font-weight="bold" fill="#F8FAFC">PGS.TS. NGUYỄN VĂN HẬU</text>
    <text x="120" y="628" font-size="13" fill="#94A3B8">Khoa Công Nghệ Thông Tin • Học phần: Học Máy Cơ Bản</text>

    <line x1="600" y1="555" x2="600" y2="625" stroke="#334155" stroke-width="1"/>

    <!-- Students -->
    <text x="640" y="575" font-size="13" font-weight="bold" fill="#64748B" letter-spacing="1">NHÓM SINH VIÊN THỰC HIỆN</text>
    <text x="640" y="605" font-size="18" font-weight="bold" fill="#F8FAFC">NHÓM 02 SINH VIÊN</text>
    <text x="640" y="628" font-size="13" fill="#94A3B8">Phân công: ML Pipeline, Data Analysis &amp; Web Serving Architecture</text>
  </g>

  <!-- Footer -->
  <g id="footer" data-pptx-role="footer">
    <text x="80" y="688" font-size="13" fill="#64748B">Project 22: K-Means Customer Segmentation • Machine Learning Fundamentals</text>
    <text x="1195" y="688" font-size="13" font-weight="bold" fill="#64748B" text-anchor="end">01 / 15</text>
  </g>
</svg>"""

# ==============================================================================
# SLIDE 02: PROBLEM & OBJECTIVES
# ==============================================================================
def gen_slide_02():
    content = """
  <!-- 3 Main Pillars -->
  <g id="problem-pillars">
    <!-- Card 1: Business Context -->
    <rect x="70" y="160" width="360" height="485" rx="14" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
    <rect x="70" y="160" width="360" height="6" rx="3" fill="#2563EB"/>
    
    <!-- Icon Circle -->
    <circle cx="115" cy="205" r="22" fill="#DBEAFE"/>
    <path d="M107 205 L113 211 L123 199" stroke="#1D4ED8" stroke-width="2.5" fill="none" stroke-linecap="round"/>
    <text x="150" y="211" font-size="18" font-weight="bold" fill="#0F172A">Bối Cảnh B2B Bán Sỉ</text>

    <text x="95" y="260" font-size="14" font-weight="bold" fill="#1E40AF">Đặc thù nhà phân phối:</text>
    <text x="95" y="285" font-size="14" fill="#334155">• Cung ứng hàng hóa lớn cho 2 nhóm</text>
    <text x="105" y="307" font-size="14" fill="#334155">đối tượng chính: Horeca &amp; Retail.</text>
    <text x="95" y="340" font-size="14" font-weight="bold" fill="#1E40AF">Bài toán thực tế:</text>
    <text x="95" y="365" font-size="14" fill="#334155">• Quy mô đơn hàng và danh mục hàng</text>
    <text x="105" y="387" font-size="14" fill="#334155">hóa giữa các khách hàng rất phân tán.</text>
    <text x="95" y="420" font-size="14" fill="#334155">• Thiếu cơ sở dữ liệu định lượng để xây</text>
    <text x="105" y="442" font-size="14" fill="#334155">dựng chính sách chiết khấu &amp; tồn kho.</text>

    <!-- Bottom Highlight -->
    <rect x="90" y="525" width="320" height="100" rx="10" fill="#EFF6FF" stroke="#BFDBFE" stroke-width="1"/>
    <text x="105" y="555" font-size="13" font-weight="bold" fill="#1E40AF">MỤC TIÊU NGHIỆP VỤ</text>
    <text x="105" y="580" font-size="13" fill="#1E3A8A">Tự động nhận diện nhóm khách hàng</text>
    <text x="105" y="602" font-size="13" fill="#1E3A8A">dựa trên hành vi chi tiêu thực tế.</text>

    <!-- Card 2: Technical Challenge -->
    <rect x="460" y="160" width="360" height="485" rx="14" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
    <rect x="460" y="160" width="360" height="6" rx="3" fill="#DC2626"/>
    
    <!-- Icon Circle -->
    <circle cx="505" cy="205" r="22" fill="#FEE2E2"/>
    <text x="505" y="212" font-size="18" font-weight="bold" fill="#DC2626" text-anchor="middle">!</text>
    <text x="540" y="211" font-size="18" font-weight="bold" fill="#0F172A">Thách Thức Machine Learning</text>

    <text x="485" y="260" font-size="14" font-weight="bold" fill="#991B1B">Độ lệch phân phối (Skewness):</text>
    <text x="485" y="285" font-size="14" fill="#334155">• Dữ liệu chi tiêu lệch phải cực đoan,</text>
    <text x="495" y="307" font-size="14" fill="#334155">Delicassen đạt Skewness lên tới +12.12.</text>
    <text x="485" y="340" font-size="14" font-weight="bold" fill="#991B1B">Chênh lệch thang đo (Range):</text>
    <text x="485" y="365" font-size="14" fill="#334155">• Fresh (tới 112,151) lấn át hoàn toàn</text>
    <text x="495" y="387" font-size="14" fill="#334155">khoảng cách Euclidean so với biến khác.</text>
    <text x="485" y="420" font-size="14" font-weight="bold" fill="#991B1B">Nguy cơ rò rỉ dữ liệu (Leakage):</text>
    <text x="485" y="442" font-size="14" fill="#334155">• Tiền xử lý trên toàn bộ tập dữ liệu sẽ</text>
    <text x="495" y="464" font-size="14" fill="#334155">làm sai lệch kết quả đánh giá mô hình.</text>

    <!-- Bottom Highlight -->
    <rect x="480" y="525" width="320" height="100" rx="10" fill="#FEF2F2" stroke="#FECACA" stroke-width="1"/>
    <text x="495" y="555" font-size="13" font-weight="bold" fill="#991B1B">RỦI RO CẦN TRIỆT TIÊU</text>
    <text x="495" y="580" font-size="13" fill="#7F1D1D">Không để ngoại lệ chi phối khoảng cách,</text>
    <text x="495" y="602" font-size="13" fill="#7F1D1D">cấm sử dụng nhãn test để chọn mô hình.</text>

    <!-- Card 3: Proposed Solution -->
    <rect x="850" y="160" width="360" height="485" rx="14" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
    <rect x="850" y="160" width="360" height="6" rx="3" fill="#059669"/>
    
    <!-- Icon Circle -->
    <circle cx="895" cy="205" r="22" fill="#D1FAE5"/>
    <path d="M887 205 L893 211 L903 199" stroke="#059669" stroke-width="2.5" fill="none" stroke-linecap="round"/>
    <text x="930" y="211" font-size="18" font-weight="bold" fill="#0F172A">Giải Pháp Đề Xuất</text>

    <text x="875" y="260" font-size="14" font-weight="bold" fill="#065F46">Chuẩn hóa &amp; Chống rò rỉ:</text>
    <text x="875" y="285" font-size="14" fill="#334155">• Split Train/Val/Test (264/88/88) trước</text>
    <text x="885" y="307" font-size="14" fill="#334155">khi fit bất kỳ bộ biến đổi nào.</text>
    <text x="875" y="340" font-size="14" font-weight="bold" fill="#065F46">Pipeline Log1p + StandardScaler:</text>
    <text x="875" y="365" font-size="14" fill="#334155">• Nén phân phối đuôi dài và đưa 6 biến</text>
    <text x="885" y="387" font-size="14" fill="#334155">về cùng thang đo z-score chuẩn.</text>
    <text x="875" y="420" font-size="14" font-weight="bold" fill="#065F46">Đóng gói Web Serving:</text>
    <text x="875" y="442" font-size="14" fill="#334155">• Đóng băng Model D011, phục vụ dự</text>
    <text x="885" y="464" font-size="14" fill="#334155">đoán thời gian thực qua REST API.</text>

    <!-- Bottom Highlight -->
    <rect x="870" y="525" width="320" height="100" rx="10" fill="#ECFDF5" stroke="#A7F3D0" stroke-width="1"/>
    <text x="885" y="555" font-size="13" font-weight="bold" fill="#065F46">KẾT QUẢ MONG ĐỢI</text>
    <text x="885" y="580" font-size="13" fill="#064E3B">K=2 ổn định tuyệt đối (ARI=0.997),</text>
    <text x="885" y="602" font-size="13" fill="#064E3B">phân khúc rõ nét có ý nghĩa kinh doanh.</text>
  </g>
"""
    return get_svg_wrapper(2, "TỔNG QUAN ĐỒ ÁN", "Bối Cảnh Nghiệp Vụ, Thách Thức &amp; Mục Tiêu", "Xác lập ranh giới bài toán phân khúc bán sỉ và phương pháp giải quyết khoa học", content, page_role="anchor")

# ==============================================================================
# SLIDE 03: DATASET EXPLORATION
# ==============================================================================
def gen_slide_03():
    content = """
  <!-- Top Metadata Bar -->
  <g id="dataset-meta">
    <rect x="70" y="150" width="1140" height="60" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
    <text x="100" y="186" font-size="15" font-weight="bold" fill="#1E40AF">TẬP DỮ LIỆU:</text>
    <text x="210" y="186" font-size="15" fill="#0F172A">UCI Machine Learning Repository (ID 292)</text>
    <line x1="560" y1="165" x2="560" y2="195" stroke="#CBD5E1" stroke-width="1"/>
    <text x="590" y="186" font-size="15" font-weight="bold" fill="#059669">QUY MÔ:</text>
    <text x="670" y="186" font-size="15" fill="#0F172A">440 quan sát khách hàng</text>
    <line x1="880" y1="165" x2="880" y2="195" stroke="#CBD5E1" stroke-width="1"/>
    <text x="910" y="186" font-size="15" font-weight="bold" fill="#7C3AED">ĐẶC TRƯNG:</text>
    <text x="1015" y="186" font-size="15" fill="#0F172A">6 biến chi tiêu + 2 phân tích</text>
  </g>

  <!-- 6 Feature Cards Grid -->
  <g id="spending-features">
    <!-- Row 1 -->
    <!-- Card 1: Fresh -->
    <rect x="70" y="225" width="360" height="185" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
    <rect x="70" y="225" width="360" height="4" rx="2" fill="#10B981"/>
    <text x="95" y="258" font-size="18" font-weight="bold" fill="#0F172A">1. Fresh (Hàng tươi sống)</text>
    <text x="95" y="285" font-size="13" fill="#64748B">Rau củ, hoa quả, thịt tươi hằng ngày</text>
    <text x="95" y="325" font-size="13" fill="#334155">Trung bình (Mean): <tspan font-weight="bold" fill="#059669">12,000 m.u.</tspan></text>
    <text x="95" y="350" font-size="13" fill="#334155">Trung vị (Median): <tspan font-weight="bold">8,504 m.u.</tspan></text>
    <text x="95" y="375" font-size="13" fill="#334155">Khoảng giá trị (Range): <tspan font-weight="bold" fill="#DC2626">3 → 112,151 m.u.</tspan></text>
    <text x="95" y="398" font-size="12" fill="#94A3B8">Skewness cực đại trong nhóm chi tiêu cao</text>

    <!-- Card 2: Milk -->
    <rect x="460" y="225" width="360" height="185" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
    <rect x="460" y="225" width="360" height="4" rx="2" fill="#3B82F6"/>
    <text x="485" y="258" font-size="18" font-weight="bold" fill="#0F172A">2. Milk (Sản phẩm từ sữa)</text>
    <text x="485" y="285" font-size="13" fill="#64748B">Sữa tươi, phô mai, bơ, sữa chua</text>
    <text x="485" y="325" font-size="13" fill="#334155">Trung bình (Mean): <tspan font-weight="bold" fill="#2563EB">5,796 m.u.</tspan></text>
    <text x="485" y="350" font-size="13" fill="#334155">Trung vị (Median): <tspan font-weight="bold">3,627 m.u.</tspan></text>
    <text x="485" y="375" font-size="13" fill="#334155">Khoảng giá trị (Range): <tspan font-weight="bold" fill="#DC2626">55 → 73,498 m.u.</tspan></text>
    <text x="485" y="398" font-size="12" fill="#94A3B8">Skewness thô: +4.28 (Đặc trưng nhóm bán lẻ)</text>

    <!-- Card 3: Grocery -->
    <rect x="850" y="225" width="360" height="185" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
    <rect x="850" y="225" width="360" height="4" rx="2" fill="#F59E0B"/>
    <text x="875" y="258" font-size="18" font-weight="bold" fill="#0F172A">3. Grocery (Hàng tạp hóa)</text>
    <text x="875" y="285" font-size="13" fill="#64748B">Gia vị, đồ đóng hộp, thực phẩm khô</text>
    <text x="875" y="325" font-size="13" fill="#334155">Trung bình (Mean): <tspan font-weight="bold" fill="#D97706">7,951 m.u.</tspan></text>
    <text x="875" y="350" font-size="13" fill="#334155">Trung vị (Median): <tspan font-weight="bold">4,755 m.u.</tspan></text>
    <text x="875" y="375" font-size="13" fill="#334155">Khoảng giá trị (Range): <tspan font-weight="bold" fill="#DC2626">3 → 59,598 m.u.</tspan></text>
    <text x="875" y="398" font-size="12" fill="#94A3B8">Tương quan mạnh với Detergents_Paper</text>

    <!-- Row 2 -->
    <!-- Card 4: Frozen -->
    <rect x="70" y="425" width="360" height="185" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
    <rect x="70" y="425" width="360" height="4" rx="2" fill="#06B6D4"/>
    <text x="95" y="458" font-size="18" font-weight="bold" fill="#0F172A">4. Frozen (Thực phẩm đông lạnh)</text>
    <text x="95" y="485" font-size="13" fill="#64748B">Thịt, hải sản và đồ đông lạnh bảo quản lâu</text>
    <text x="95" y="525" font-size="13" fill="#334155">Trung bình (Mean): <tspan font-weight="bold" fill="#0891B2">3,071 m.u.</tspan></text>
    <text x="95" y="550" font-size="13" fill="#334155">Trung vị (Median): <tspan font-weight="bold">1,526 m.u.</tspan></text>
    <text x="95" y="575" font-size="13" fill="#334155">Khoảng giá trị (Range): <tspan font-weight="bold">25 → 60,869 m.u.</tspan></text>
    <text x="95" y="598" font-size="12" fill="#94A3B8">Skewness thô: +3.53</text>

    <!-- Card 5: Detergents_Paper -->
    <rect x="460" y="425" width="360" height="185" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
    <rect x="460" y="425" width="360" height="4" rx="2" fill="#8B5CF6"/>
    <text x="485" y="458" font-size="18" font-weight="bold" fill="#0F172A">5. Detergents_Paper (Chất tẩy &amp; Giấy)</text>
    <text x="485" y="485" font-size="13" fill="#64748B">Nước tẩy rửa, giấy vệ sinh, vật tư vệ sinh</text>
    <text x="485" y="525" font-size="13" fill="#334155">Trung bình (Mean): <tspan font-weight="bold" fill="#7C3AED">2,881 m.u.</tspan></text>
    <text x="485" y="550" font-size="13" fill="#334155">Trung vị (Median): <tspan font-weight="bold">816 m.u.</tspan></text>
    <text x="485" y="575" font-size="13" fill="#334155">Khoảng giá trị (Range): <tspan font-weight="bold">3 → 40,827 m.u.</tspan></text>
    <text x="485" y="598" font-size="12" fill="#94A3B8">Trung vị rất thấp, chi phối bởi siêu thị lớn</text>

    <!-- Card 6: Delicassen -->
    <rect x="850" y="425" width="360" height="185" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
    <rect x="850" y="425" width="360" height="4" rx="2" fill="#EC4899"/>
    <text x="875" y="458" font-size="18" font-weight="bold" fill="#0F172A">6. Delicassen (Đồ nguội &amp; Tinh hoa)</text>
    <text x="875" y="485" font-size="13" fill="#64748B">Thực phẩm chế biến sẵn cao cấp, jambon</text>
    <text x="875" y="525" font-size="13" fill="#334155">Trung bình (Mean): <tspan font-weight="bold" fill="#DB2777">1,524 m.u.</tspan></text>
    <text x="875" y="550" font-size="13" fill="#334155">Trung vị (Median): <tspan font-weight="bold">965 m.u.</tspan></text>
    <text x="875" y="575" font-size="13" fill="#334155">Khoảng giá trị (Range): <tspan font-weight="bold" fill="#DC2626">7 → 47,943 m.u.</tspan></text>
    <text x="875" y="598" font-size="12" font-weight="bold" fill="#DC2626">Skewness cao kỷ lục: +12.12 (Bắt buộc nén)</text>
  </g>

  <!-- Bottom Profiling Callout -->
  <g id="profiling-variables">
    <rect x="70" y="622" width="1140" height="42" rx="8" fill="#F1F5F9" stroke="#CBD5E1" stroke-width="1"/>
    <text x="90" y="648" font-size="13" font-weight="bold" fill="#0F172A">2 Biến Phân Tích (Profiling Only):</text>
    <text x="320" y="648" font-size="13" fill="#334155">• <tspan font-weight="bold">Channel:</tspan> Horeca (298 mẫu - 67.7%) | Retail (142 mẫu - 32.3%)</text>
    <text x="740" y="648" font-size="13" fill="#334155">• <tspan font-weight="bold">Region:</tspan> Lisbon (77) | Oporto (47) | Other (316)</text>
    <text x="960" y="648" font-size="12" font-weight="bold" fill="#DC2626">✗ KHÔNG DÙNG ĐỂ FIT MÔ HÌNH</text>
  </g>
"""
    return get_svg_wrapper(3, "KHÁM PHÁ DỮ LIỆU", "Tập Dữ Liệu Khách Hàng Bán Sỉ (Wholesale Customers)", "Chi tiết 6 biến chi tiêu monetary units và nguyên tắc cô lập biến phân loại", content, page_role="anchor")

# ==============================================================================
# SLIDE 04: PIPELINE & ANTI-LEAKAGE
# ==============================================================================
def gen_slide_04():
    content = """
  <!-- Golden Rule Banner -->
  <g id="leakage-guard">
    <rect x="70" y="150" width="1140" height="70" rx="12" fill="#FEF2F2" stroke="#DC2626" stroke-width="2"/>
    <circle cx="115" cy="185" r="22" fill="#FEE2E2"/>
    <path d="M115 172 L115 188 M115 194 L115 198" stroke="#DC2626" stroke-width="3" stroke-linecap="round"/>
    <text x="155" y="177" font-size="15" font-weight="bold" fill="#991B1B">NGUYÊN TẮC VÀNG CHỐNG RÒ RỈ DỮ LIỆU (ANTI-DATA-LEAKAGE):</text>
    <text x="155" y="202" font-size="14" fill="#7F1D1D">Tuyệt đối phân chia tập dữ liệu (Split) trước khi fit bất kỳ bộ biến đổi nào. Tập Test được giữ độc lập và chỉ đánh giá đúng 1 lần.</text>
  </g>

  <!-- 5-Stage Pipeline Flowchart -->
  <g id="pipeline-flow">
    <!-- Stage 1 -->
    <rect x="70" y="250" width="200" height="230" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
    <rect x="70" y="250" width="200" height="6" rx="3" fill="#2563EB"/>
    <text x="90" y="285" font-size="13" font-weight="bold" fill="#1E40AF">BƯỚC 1</text>
    <text x="90" y="315" font-size="18" font-weight="bold" fill="#0F172A">Raw Data</text>
    <text x="90" y="345" font-size="13" fill="#64748B">• 440 mẫu khách hàng</text>
    <text x="90" y="370" font-size="13" fill="#64748B">• Kiểm tra missing (0)</text>
    <text x="90" y="395" font-size="13" fill="#64748B">• Giữ nguyên đơn vị m.u.</text>
    <rect x="85" y="425" width="170" height="36" rx="6" fill="#EFF6FF"/>
    <text x="170" y="448" font-size="12" font-weight="bold" fill="#1E40AF" text-anchor="middle">Input: 440 × 8</text>

    <!-- Arrow 1 -->
    <path d="M280 365 L305 365" stroke="#94A3B8" stroke-width="2" stroke-linecap="round"/>
    <polygon points="305,360 315,365 305,370" fill="#94A3B8"/>

    <!-- Stage 2 -->
    <rect x="315" y="250" width="200" height="230" rx="12" fill="#FFFFFF" stroke="#3B82F6" stroke-width="2"/>
    <rect x="315" y="250" width="200" height="6" rx="3" fill="#3B82F6"/>
    <text x="335" y="285" font-size="13" font-weight="bold" fill="#1D4ED8">BƯỚC 2</text>
    <text x="335" y="315" font-size="18" font-weight="bold" fill="#0F172A">Split 60 / 20 / 20</text>
    <text x="335" y="345" font-size="13" fill="#1E40AF">• Train: <tspan font-weight="bold">264 mẫu</tspan> (60%)</text>
    <text x="335" y="370" font-size="13" fill="#059669">• Val: <tspan font-weight="bold">88 mẫu</tspan> (20%)</text>
    <text x="335" y="395" font-size="13" fill="#DC2626">• Test: <tspan font-weight="bold">88 mẫu</tspan> (20%)</text>
    <rect x="330" y="425" width="170" height="36" rx="6" fill="#DBEAFE"/>
    <text x="415" y="448" font-size="12" font-weight="bold" fill="#1E40AF" text-anchor="middle">Chia tách nghiêm ngặt</text>

    <!-- Arrow 2 -->
    <path d="M525 365 L550 365" stroke="#94A3B8" stroke-width="2" stroke-linecap="round"/>
    <polygon points="550,360 560,365 550,370" fill="#94A3B8"/>

    <!-- Stage 3 -->
    <rect x="560" y="250" width="200" height="230" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
    <rect x="560" y="250" width="200" height="6" rx="3" fill="#10B981"/>
    <text x="580" y="285" font-size="13" font-weight="bold" fill="#065F46">BƯỚC 3</text>
    <text x="580" y="315" font-size="18" font-weight="bold" fill="#0F172A">Fit Preprocessing</text>
    <text x="580" y="345" font-size="13" fill="#334155">• <tspan font-weight="bold">CHỈ fit trên Train</tspan></text>
    <text x="580" y="370" font-size="13" fill="#334155">• log1p(x) nén lệch phải</text>
    <text x="580" y="395" font-size="13" fill="#334155">• StandardScaler: mean, std</text>
    <rect x="575" y="425" width="170" height="36" rx="6" fill="#DCFCE7"/>
    <text x="660" y="448" font-size="12" font-weight="bold" fill="#065F46" text-anchor="middle">Transform Val &amp; Test</text>

    <!-- Arrow 3 -->
    <path d="M770 365 L795 365" stroke="#94A3B8" stroke-width="2" stroke-linecap="round"/>
    <polygon points="795,360 805,365 795,370" fill="#94A3B8"/>

    <!-- Stage 4 -->
    <rect x="805" y="250" width="200" height="230" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
    <rect x="805" y="250" width="200" height="6" rx="3" fill="#F59E0B"/>
    <text x="825" y="285" font-size="13" font-weight="bold" fill="#92400E">BƯỚC 4</text>
    <text x="825" y="315" font-size="18" font-weight="bold" fill="#0F172A">Thực Nghiệm K</text>
    <text x="825" y="345" font-size="13" fill="#334155">• K-Means Lloyd K=2..8</text>
    <text x="825" y="370" font-size="13" fill="#334155">• Đánh giá Elbow &amp; Sil</text>
    <text x="825" y="395" font-size="13" fill="#334155">• 10 seed kiểm định ARI</text>
    <rect x="820" y="425" width="170" height="36" rx="6" fill="#FEF3C7"/>
    <text x="905" y="448" font-size="12" font-weight="bold" fill="#92400E" text-anchor="middle">Chọn D011 (K=2)</text>

    <!-- Arrow 4 -->
    <path d="M1015 365 L1040 365" stroke="#94A3B8" stroke-width="2" stroke-linecap="round"/>
    <polygon points="1040,360 1050,365 1040,370" fill="#94A3B8"/>

    <!-- Stage 5 -->
    <rect x="1050" y="250" width="160" height="230" rx="12" fill="#FFFFFF" stroke="#8B5CF6" stroke-width="2"/>
    <rect x="1050" y="250" width="160" height="6" rx="3" fill="#8B5CF6"/>
    <text x="1070" y="285" font-size="13" font-weight="bold" fill="#6B21A8">BƯỚC 5</text>
    <text x="1070" y="315" font-size="18" font-weight="bold" fill="#0F172A">Đóng Băng</text>
    <text x="1070" y="345" font-size="13" fill="#334155">• Fit lại 352 mẫu dev</text>
    <text x="1070" y="370" font-size="13" fill="#334155">• Đánh giá Test 1 lần</text>
    <text x="1070" y="395" font-size="13" fill="#334155">• Xuất model.joblib</text>
    <rect x="1065" y="425" width="130" height="36" rx="6" fill="#F3E8FF"/>
    <text x="1130" y="448" font-size="12" font-weight="bold" fill="#6B21A8" text-anchor="middle">Frozen D011</text>
  </g>

  <!-- Split Evidence Callout -->
  <g id="split-evidence">
    <rect x="70" y="505" width="1140" height="155" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
    <text x="100" y="538" font-size="15" font-weight="bold" fill="#0F172A">BẰNG CHỨNG PHÂN TẬP DỮ LIỆU &amp; TÍNH TOÀN VẸN:</text>
    
    <rect x="100" y="555" width="340" height="85" rx="8" fill="#F8FAFC" stroke="#E2E8F0"/>
    <text x="120" y="582" font-size="13" font-weight="bold" fill="#1E40AF">TẬP TRAIN (264 mẫu - 60%)</text>
    <text x="120" y="605" font-size="12" fill="#64748B">data/processed/train.csv</text>
    <text x="120" y="625" font-size="12" fill="#059669">Dùng học tham số scaler &amp; tìm cụm</text>

    <rect x="470" y="555" width="340" height="85" rx="8" fill="#F8FAFC" stroke="#E2E8F0"/>
    <text x="490" y="582" font-size="13" font-weight="bold" fill="#059669">TẬP VALIDATION (88 mẫu - 20%)</text>
    <text x="490" y="605" font-size="12" fill="#64748B">data/processed/validation.csv</text>
    <text x="490" y="625" font-size="12" fill="#059669">Dùng so sánh chọn K tối ưu &amp; stability</text>

    <rect x="840" y="555" width="340" height="85" rx="8" fill="#F8FAFC" stroke="#E2E8F0"/>
    <text x="860" y="582" font-size="13" font-weight="bold" fill="#DC2626">TẬP TEST (88 mẫu - 20%)</text>
    <text x="860" y="605" font-size="12" fill="#64748B">data/processed/test.csv</text>
    <text x="860" y="625" font-size="12" fill="#DC2626">Bảo mật tuyệt đối, chỉ mở sau đóng băng</text>
  </g>
"""
    return get_svg_wrapper(4, "KIẾN TRÚC PIPELINE", "Quy Trình Huấn Luyện &amp; Kiểm Soát Chống Rò Rỉ Dữ Liệu", "Quy chuẩn chia tách 60/20/20 và nguyên tắc bảo vệ tập kiểm thử độc lập", content, page_role="anchor")

# ==============================================================================
# SLIDE 05: PREPROCESSING COMPARISON (REDESIGNED)
# ==============================================================================
def gen_slide_05():
    content = """
  <!-- Left Card: Raw Features Issues -->
  <g id="raw-issues">
    <rect x="70" y="150" width="520" height="515" rx="14" fill="#FFFFFF" stroke="#FECACA" stroke-width="1.5"/>
    <rect x="70" y="150" width="520" height="6" rx="3" fill="#DC2626"/>

    <!-- Header Pill -->
    <rect x="95" y="175" width="220" height="34" rx="17" fill="#FEE2E2"/>
    <circle cx="112" cy="192" r="11" fill="#DC2626"/>
    <text x="112" y="197" font-size="12" font-weight="bold" fill="#FFFFFF" text-anchor="middle">X</text>
    <text x="135" y="197" font-size="14" font-weight="bold" fill="#991B1B">DỮ LIỆU THÔ (RAW DATA)</text>

    <!-- Skewness Title -->
    <text x="95" y="240" font-size="15" font-weight="bold" fill="#0F172A">Độ lệch (Skewness) cực cao:</text>
    <text x="95" y="260" font-size="12" fill="#64748B">reports/data/eda/train_skewness.csv</text>

    <!-- Bar 1: Delicassen -->
    <text x="95" y="295" font-size="13" fill="#334155">Delicassen:</text>
    <rect x="185" y="282" width="230" height="18" rx="4" fill="#EF4444"/>
    <text x="425" y="296" font-size="13" font-weight="bold" fill="#DC2626">+12.12 (Cực lệch)</text>

    <!-- Bar 2: Milk -->
    <text x="95" y="325" font-size="13" fill="#334155">Milk:</text>
    <rect x="185" y="312" width="90" height="18" rx="4" fill="#F97316"/>
    <text x="285" y="326" font-size="13" font-weight="bold" fill="#C2410C">+4.28</text>

    <!-- Bar 3: Frozen -->
    <text x="95" y="355" font-size="13" fill="#334155">Frozen:</text>
    <rect x="185" y="342" width="75" height="18" rx="4" fill="#F97316"/>
    <text x="270" y="356" font-size="13" font-weight="bold" fill="#C2410C">+3.53</text>

    <!-- Bar 4: Grocery -->
    <text x="95" y="385" font-size="13" fill="#334155">Grocery:</text>
    <rect x="185" y="372" width="60" height="18" rx="4" fill="#FBBF24"/>
    <text x="255" y="386" font-size="13" font-weight="bold" fill="#B45309">+2.76</text>

    <!-- Scale Disparity -->
    <text x="95" y="430" font-size="15" font-weight="bold" fill="#0F172A">Chênh lệch thang đo lớn:</text>
    <rect x="95" y="445" width="470" height="65" rx="8" fill="#F8FAFC" stroke="#E2E8F0"/>
    <text x="115" y="472" font-size="13" fill="#334155">• Fresh: <tspan font-weight="bold" fill="#0F172A">3 → 112,151 m.u.</tspan> (Biên độ gấp hàng nghìn lần)</text>
    <text x="115" y="495" font-size="13" fill="#334155">• Milk: <tspan font-weight="bold">55 → 73,498 m.u.</tspan> | Delicassen: <tspan font-weight="bold">7 → 47,943 m.u.</tspan></text>

    <!-- Consequence Warning Box -->
    <rect x="95" y="530" width="470" height="110" rx="10" fill="#FEF2F2" stroke="#FCA5A5" stroke-width="1.5"/>
    <text x="115" y="560" font-size="14" font-weight="bold" fill="#991B1B">HỆ QUẢ KỸ THUẬT NGHIÊM TRỌNG:</text>
    <text x="115" y="585" font-size="13" fill="#7F1D1D">✗ Khoảng cách Euclidean bị chi phối hoàn toàn bởi Fresh/Grocery</text>
    <text x="115" y="608" font-size="13" fill="#7F1D1D">✗ K-Means trên Raw bị méo mó, nuốt cụm nhỏ (K&gt;=4 có cụm &lt;1%)</text>
    <text x="115" y="628" font-size="13" fill="#7F1D1D">✗ Không phản ánh đúng cơ cấu chi tiêu tương đối</text>
  </g>

  <!-- Center Transformation Bridge -->
  <g id="transform-bridge">
    <rect x="605" y="280" width="70" height="180" rx="35" fill="#EFF6FF" stroke="#3B82F6" stroke-width="2"/>
    <text x="640" y="325" font-size="11" font-weight="bold" fill="#1D4ED8" text-anchor="middle">log1p(x)</text>
    <path d="M640 345 L640 375" stroke="#3B82F6" stroke-width="3" stroke-linecap="round"/>
    <polygon points="635,375 640,385 645,375" fill="#3B82F6"/>
    <text x="640" y="415" font-size="11" font-weight="bold" fill="#059669" text-anchor="middle">Standard</text>
    <text x="640" y="432" font-size="11" font-weight="bold" fill="#059669" text-anchor="middle">Scaler</text>
  </g>

  <!-- Right Card: Preprocessed Solution -->
  <g id="log1p-solution">
    <rect x="690" y="150" width="520" height="515" rx="14" fill="#FFFFFF" stroke="#BBF7D0" stroke-width="1.5"/>
    <rect x="690" y="150" width="520" height="6" rx="3" fill="#059669"/>

    <!-- Header Pill -->
    <rect x="715" y="175" width="280" height="34" rx="17" fill="#DCFCE7"/>
    <circle cx="732" cy="192" r="11" fill="#059669"/>
    <path d="M727 192 L731 196 L737 188" stroke="#FFFFFF" stroke-width="2" fill="none" stroke-linecap="round"/>
    <text x="752" y="197" font-size="14" font-weight="bold" fill="#065F46">LOG1P + STANDARD SCALER</text>

    <!-- Skewness Reduction Title -->
    <text x="715" y="240" font-size="15" font-weight="bold" fill="#0F172A">Triệt tiêu Skewness (Giảm đến 92.6%):</text>
    <text x="715" y="260" font-size="12" fill="#64748B">reports/data/eda/preprocessing_comparison.csv</text>

    <!-- Bar 1: Delicassen -->
    <text x="715" y="295" font-size="13" fill="#334155">Delicassen:</text>
    <rect x="805" y="282" width="25" height="18" rx="4" fill="#10B981"/>
    <text x="840" y="296" font-size="13" font-weight="bold" fill="#059669">-0.90 (Giảm từ +12.12!)</text>

    <!-- Bar 2: Milk -->
    <text x="715" y="325" font-size="13" fill="#334155">Milk:</text>
    <rect x="805" y="312" width="10" height="18" rx="4" fill="#10B981"/>
    <text x="825" y="326" font-size="13" font-weight="bold" fill="#059669">-0.17 (Gần như đối xứng)</text>

    <!-- Bar 3: Frozen -->
    <text x="715" y="355" font-size="13" fill="#334155">Frozen:</text>
    <rect x="805" y="342" width="15" height="18" rx="4" fill="#10B981"/>
    <text x="830" y="356" font-size="13" font-weight="bold" fill="#059669">-0.46</text>

    <!-- Bar 4: Grocery -->
    <text x="715" y="385" font-size="13" fill="#334155">Grocery:</text>
    <rect x="805" y="372" width="22" height="18" rx="4" fill="#10B981"/>
    <text x="837" y="386" font-size="13" font-weight="bold" fill="#059669">-0.94</text>

    <!-- Standardization Properties -->
    <text x="715" y="430" font-size="15" font-weight="bold" fill="#0F172A">Cân bằng thang đo hoàn hảo:</text>
    <rect x="715" y="445" width="470" height="65" rx="8" fill="#F0FDF4" stroke="#DCFCE7"/>
    <text x="735" y="472" font-size="13" fill="#065F46">✓ Tất cả 6 đặc trưng: <tspan font-weight="bold">Mean = 0, Std = 1.0</tspan></text>
    <text x="735" y="495" font-size="13" fill="#065F46">✓ Trọng số các biến đóng góp đồng đều vào khoảng cách phân cụm</text>

    <!-- Outcome Highlights Grid -->
    <g id="preproc-kpi">
      <rect x="715" y="530" width="225" height="110" rx="10" fill="#ECFDF5" stroke="#A7F3D0" stroke-width="1.5"/>
      <text x="735" y="560" font-size="13" font-weight="bold" fill="#065F46">ĐỘ ỔN ĐỊNH SEED (K=2)</text>
      <text x="735" y="600" font-size="32" font-weight="bold" fill="#059669">ARI: 0.997</text>
      <text x="735" y="625" font-size="12" fill="#064E3B">100% agreement qua 10 seed</text>

      <rect x="960" y="530" width="225" height="110" rx="10" fill="#EFF6FF" stroke="#BFDBFE" stroke-width="1.5"/>
      <text x="980" y="560" font-size="13" font-weight="bold" fill="#1E40AF">SILHOUETTE VALIDATION</text>
      <text x="980" y="600" font-size="32" font-weight="bold" fill="#2563EB">0.307</text>
      <text x="980" y="625" font-size="12" fill="#1E3A8A">Tách cụm rõ &amp; phân phối cân bằng</text>
    </g>
  </g>
"""
    return get_svg_wrapper(5, "THỰC NGHIỆM 01", "So Sánh Tiền Xử Lý: Dữ Liệu Thô (Raw) vs Log1p + Scaler", "Triệt tiêu độ lệch phải cực đoan và chuẩn hóa toàn diện không gian vector chi tiêu", content, "Quyết định đóng băng D011: Lựa chọn log1p + StandardScaler cho toàn bộ hệ thống phục vụ", page_role="breathing")

# ==============================================================================
# SLIDE 06: ELBOW METHOD
# ==============================================================================
def gen_slide_06():
    content = """
  <!-- Left Side: Vector Line Chart -->
  <g id="elbow-chart">
    <rect x="70" y="150" width="670" height="515" rx="14" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
    <text x="100" y="190" font-size="18" font-weight="bold" fill="#0F172A">Đồ Thị Quán Tính (Inertia SSE) Theo Số Cụm K = 2..8</text>
    <text x="100" y="212" font-size="13" fill="#64748B">reports/data/experiments/selection_evidence.csv (Tập Train 264 mẫu)</text>

    <!-- Chart Canvas Area -->
    <g transform="translate(130 240)">
      <!-- Axes -->
      <line x1="0" y1="320" x2="540" y2="320" stroke="#CBD5E1" stroke-width="1.5"/>
      <line x1="0" y1="0" x2="0" y2="320" stroke="#CBD5E1" stroke-width="1.5"/>

      <!-- Grid lines horizontal -->
      <line x1="0" y1="60" x2="540" y2="60" stroke="#F1F5F9" stroke-width="1"/>
      <text x="-15" y="65" font-size="11" fill="#94A3B8" text-anchor="end">1,200</text>
      <line x1="0" y1="140" x2="540" y2="140" stroke="#F1F5F9" stroke-width="1"/>
      <text x="-15" y="145" font-size="11" fill="#94A3B8" text-anchor="end">1,000</text>
      <line x1="0" y1="220" x2="540" y2="220" stroke="#F1F5F9" stroke-width="1"/>
      <text x="-15" y="225" font-size="11" fill="#94A3B8" text-anchor="end">800</text>
      <line x1="0" y1="300" x2="540" y2="300" stroke="#F1F5F9" stroke-width="1"/>
      <text x="-15" y="305" font-size="11" fill="#94A3B8" text-anchor="end">600</text>

      <!-- Curve area fill gradient -->
      <polygon points="50,90 125,160 200,205 275,235 350,260 425,280 500,296 500,320 50,320" fill="#3B82F6" opacity="0.12"/>

      <!-- Inertia Curve Line -->
      <path d="M50 90 L125 160 L200 205 L275 235 L350 260 L425 280 L500 296" stroke="#2563EB" stroke-width="3.5" fill="none" stroke-linecap="round"/>

      <!-- Data Points -->
      <!-- K=2 (Elbow Point Highlight) -->
      <circle cx="50" cy="90" r="8" fill="#FFFFFF" stroke="#DC2626" stroke-width="3"/>
      <text x="50" y="70" font-size="13" font-weight="bold" fill="#DC2626" text-anchor="middle">1,116.6</text>
      <text x="50" y="340" font-size="13" font-weight="bold" fill="#DC2626" text-anchor="middle">K=2</text>

      <!-- K=3 -->
      <circle cx="125" cy="160" r="5" fill="#2563EB"/>
      <text x="125" y="148" font-size="11" fill="#475569" text-anchor="middle">945.9</text>
      <text x="125" y="340" font-size="12" fill="#475569" text-anchor="middle">K=3</text>

      <!-- K=4 -->
      <circle cx="200" cy="205" r="5" fill="#2563EB"/>
      <text x="200" y="193" font-size="11" fill="#475569" text-anchor="middle">830.6</text>
      <text x="200" y="340" font-size="12" fill="#475569" text-anchor="middle">K=4</text>

      <!-- K=5 -->
      <circle cx="275" cy="235" r="5" fill="#2563EB"/>
      <text x="275" y="223" font-size="11" fill="#475569" text-anchor="middle">756.6</text>
      <text x="275" y="340" font-size="12" fill="#475569" text-anchor="middle">K=5</text>

      <!-- K=6 -->
      <circle cx="350" cy="260" r="5" fill="#2563EB"/>
      <text x="350" y="248" font-size="11" fill="#475569" text-anchor="middle">698.3</text>
      <text x="350" y="340" font-size="12" fill="#475569" text-anchor="middle">K=6</text>

      <!-- K=7 -->
      <circle cx="425" cy="280" r="5" fill="#2563EB"/>
      <text x="425" y="268" font-size="11" fill="#475569" text-anchor="middle">649.4</text>
      <text x="425" y="340" font-size="12" fill="#475569" text-anchor="middle">K=7</text>

      <!-- K=8 -->
      <circle cx="500" cy="296" r="5" fill="#2563EB"/>
      <text x="500" y="284" font-size="11" fill="#475569" text-anchor="middle">610.5</text>
      <text x="500" y="340" font-size="12" fill="#475569" text-anchor="middle">K=8</text>

      <!-- Elbow Callout Badge -->
      <rect x="70" y="20" width="160" height="40" rx="8" fill="#FEE2E2" stroke="#DC2626" stroke-width="1.5"/>
      <text x="150" y="45" font-size="13" font-weight="bold" fill="#DC2626" text-anchor="middle">★ Điểm Gập (Elbow)</text>
    </g>
  </g>

  <!-- Right Side: Analytical Reasoning Cards -->
  <g id="elbow-insights">
    <!-- Card 1: Elbow Principle -->
    <rect x="760" y="150" width="450" height="160" rx="14" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
    <rect x="760" y="150" width="450" height="6" rx="3" fill="#2563EB"/>
    <text x="790" y="185" font-size="15" font-weight="bold" fill="#1E40AF">1. Cơ Chế Độ Suy Giảm Biên (Marginal Gain)</text>
    <text x="790" y="215" font-size="14" fill="#334155">• Từ K=1 (Inertia ≈ 1,584) xuống K=2 (1,116.6):</text>
    <text x="805" y="238" font-size="14" font-weight="bold" fill="#059669">Giảm mạnh tới 467.4 điểm quán tính (29.5%)</text>
    <text x="790" y="268" font-size="14" fill="#334155">• Khi tăng tiếp từ K=2 lên K=3:</text>
    <text x="805" y="290" font-size="14" fill="#64748B">Tốc độ giảm quán tính chậm hẳn (chỉ còn 170.7 điểm)</text>

    <!-- Card 2: Risk of Large K -->
    <rect x="760" y="330" width="450" height="150" rx="14" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
    <rect x="760" y="330" width="450" height="6" rx="3" fill="#F59E0B"/>
    <text x="790" y="365" font-size="15" font-weight="bold" fill="#B45309">2. Rủi Ro Phân Mảnh Khi Tăng K</text>
    <text x="790" y="395" font-size="14" fill="#334155">• Tại K ≥ 4: Xuất hiện các cụm con siêu nhỏ</text>
    <text x="805" y="418" font-size="13" fill="#DC2626">(K=5: cụm nhỏ nhất chiếm 4.9%; K=8: cụm chỉ 0.7%)</text>
    <text x="790" y="448" font-size="14" fill="#334155">• Quán tính giảm dần chỉ do hiện tượng over-fitting</text>

    <!-- Card 3: Final Selection -->
    <rect x="760" y="500" width="450" height="165" rx="14" fill="#ECFDF5" stroke="#10B981" stroke-width="2"/>
    <text x="790" y="535" font-size="15" font-weight="bold" fill="#065F46">3. Kết Luận Phương Pháp Elbow</text>
    <text x="790" y="565" font-size="14" fill="#064E3B">✓ <tspan font-weight="bold">K = 2</tspan> là điểm uốn rõ ràng và tối ưu nhất</text>
    <text x="790" y="590" font-size="14" fill="#064E3B">✓ Cân bằng hoàn hảo giữa độ nén dữ liệu &amp; tính tổng quát</text>
    <text x="790" y="615" font-size="14" fill="#064E3B">✓ Kết hợp cùng Silhouette Score ở slide kế tiếp để chốt D011</text>
    <rect x="790" y="635" width="220" height="20" rx="4" fill="#D1FAE5"/>
    <text x="900" y="650" font-size="11" font-weight="bold" fill="#065F46" text-anchor="middle">Inertia trung bình/mẫu: 4.23</text>
  </g>
"""
    return get_svg_wrapper(6, "THỰC NGHIỆM 02", "Xác Định K Tối Ưu: Phương Pháp Elbow (SSE Curve)", "Phân tích đường cong độ suy giảm quán tính để tìm điểm cân bằng cụm tự nhiên", content, page_role="breathing")

# ==============================================================================
# SLIDE 07: SILHOUETTE & STABILITY
# ==============================================================================
def gen_slide_07():
    content = """
  <!-- Comparison Table -->
  <g id="silhouette-table">
    <rect x="70" y="150" width="1140" height="340" rx="14" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
    
    <!-- Table Header -->
    <rect x="70" y="150" width="1140" height="45" rx="14" fill="#1E293B"/>
    <text x="110" y="178" font-size="13" font-weight="bold" fill="#FFFFFF">K CỤM</text>
    <text x="210" y="178" font-size="13" font-weight="bold" fill="#FFFFFF">SILHOUETTE TRAIN</text>
    <text x="390" y="178" font-size="13" font-weight="bold" fill="#FFFFFF">SILHOUETTE VAL</text>
    <text x="570" y="178" font-size="13" font-weight="bold" fill="#FFFFFF">KHOẢNG CÁCH GAP</text>
    <text x="770" y="178" font-size="13" font-weight="bold" fill="#FFFFFF">ĐỘ ỔN ĐỊNH ARI (10 SEEDS)</text>
    <text x="1030" y="178" font-size="13" font-weight="bold" fill="#FFFFFF">TỶ LỆ CỤM NHỎ NHẤT</text>

    <!-- Row K=2 (Selected Champion) -->
    <rect x="70" y="195" width="1140" height="48" fill="#ECFDF5"/>
    <rect x="75" y="202" width="60" height="34" rx="6" fill="#10B981"/>
    <text x="105" y="224" font-size="15" font-weight="bold" fill="#FFFFFF" text-anchor="middle">K=2 ★</text>
    <text x="210" y="224" font-size="14" font-weight="bold" fill="#065F46">0.2756</text>
    <text x="390" y="224" font-size="15" font-weight="bold" fill="#059669">0.3066 (Cao nhất)</text>
    <text x="570" y="224" font-size="14" font-weight="bold" fill="#059669">+0.0310 (Tổng quát tốt)</text>
    <text x="770" y="224" font-size="14" font-weight="bold" fill="#059669">0.9970 (std = 0.000000)</text>
    <text x="1030" y="224" font-size="14" font-weight="bold" fill="#065F46">44.73% (Rất cân bằng)</text>

    <!-- Row K=3 -->
    <rect x="70" y="243" width="1140" height="42" fill="#FFFFFF"/>
    <text x="105" y="268" font-size="14" font-weight="bold" fill="#0F172A">K=3</text>
    <text x="210" y="268" font-size="14" fill="#334155">0.2049</text>
    <text x="390" y="268" font-size="14" fill="#334155">0.2165</text>
    <text x="570" y="268" font-size="14" fill="#64748B">+0.0116</text>
    <text x="770" y="268" font-size="14" fill="#334155">0.9078 (std = 0.054)</text>
    <text x="1030" y="268" font-size="14" fill="#334155">30.38%</text>

    <!-- Row K=4 -->
    <rect x="70" y="285" width="1140" height="42" fill="#F8FAFC"/>
    <text x="105" y="310" font-size="14" font-weight="bold" fill="#0F172A">K=4</text>
    <text x="210" y="310" font-size="14" fill="#334155">0.2059</text>
    <text x="390" y="310" font-size="14" fill="#334155">0.1540</text>
    <text x="570" y="310" font-size="14" fill="#DC2626">-0.0520 (Overfit nhẹ)</text>
    <text x="770" y="310" font-size="14" fill="#334155">0.9152</text>
    <text x="1030" y="310" font-size="14" fill="#334155">12.54%</text>

    <!-- Row K=5 -->
    <rect x="70" y="327" width="1140" height="42" fill="#FFFFFF"/>
    <text x="105" y="352" font-size="14" font-weight="bold" fill="#0F172A">K=5</text>
    <text x="210" y="352" font-size="14" fill="#334155">0.1976</text>
    <text x="390" y="352" font-size="14" fill="#334155">0.1623</text>
    <text x="570" y="352" font-size="14" fill="#DC2626">-0.0353</text>
    <text x="770" y="352" font-size="14" fill="#DC2626">0.6775 (Bất ổn định)</text>
    <text x="1030" y="352" font-size="14" fill="#DC2626">8.60% (Cụm quá nhỏ)</text>

    <!-- Row K=6..8 summary -->
    <rect x="70" y="369" width="1140" height="42" fill="#F8FAFC"/>
    <text x="105" y="394" font-size="14" font-weight="bold" fill="#64748B">K=6..8</text>
    <text x="210" y="394" font-size="14" fill="#64748B">&lt; 0.1933</text>
    <text x="390" y="394" font-size="14" fill="#64748B">&lt; 0.1601</text>
    <text x="570" y="394" font-size="14" fill="#DC2626">Âm (Kém tổng quát)</text>
    <text x="770" y="394" font-size="14" fill="#DC2626">0.56 ~ 0.63 (Rất phân tán)</text>
    <text x="1030" y="394" font-size="14" fill="#DC2626">&lt; 6.0% (Vi phạm cờ 5%)</text>

    <!-- Source Note inside Table -->
    <rect x="70" y="445" width="1140" height="45" fill="#F1F5F9"/>
    <text x="90" y="472" font-size="12" fill="#475569">Nguồn kiểm chứng: reports/data/experiments/review_table.csv • 10 lượt chạy độc lập (Seed 42..51) với thuật toán Lloyd</text>
  </g>

  <!-- 3 Evidence Callouts -->
  <g id="stability-insights">
    <!-- Card 1 -->
    <rect x="70" y="505" width="360" height="155" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
    <rect x="70" y="505" width="360" height="4" rx="2" fill="#10B981"/>
    <text x="95" y="538" font-size="15" font-weight="bold" fill="#065F46">Silhouette Tối Ưu</text>
    <text x="95" y="565" font-size="13" fill="#334155">• Điểm Val Silhouette = <tspan font-weight="bold" fill="#059669">0.3066</tspan></text>
    <text x="95" y="590" font-size="13" fill="#334155">• Vượt trội hoàn toàn so với K=3 (0.216) và K=4 (0.154)</text>
    <text x="95" y="615" font-size="13" fill="#334155">• Generalization Gap dương (+0.031)</text>

    <!-- Card 2 -->
    <rect x="460" y="505" width="360" height="155" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
    <rect x="460" y="505" width="360" height="4" rx="2" fill="#2563EB"/>
    <text x="485" y="538" font-size="15" font-weight="bold" fill="#1E40AF">Độ Ổn Định Tuyệt Đối</text>
    <text x="485" y="565" font-size="13" fill="#334155">• ARI trung bình = <tspan font-weight="bold" fill="#2563EB">0.996970 ≈ 0.997</tspan></text>
    <text x="485" y="590" font-size="13" fill="#334155">• Độ lệch chuẩn (std) = <tspan font-weight="bold">0.000000</tspan></text>
    <text x="485" y="615" font-size="13" fill="#334155">• 10/10 seed đều phân cụm đồng nhất</text>

    <!-- Card 3 -->
    <rect x="850" y="505" width="360" height="155" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
    <rect x="850" y="505" width="360" height="4" rx="2" fill="#F59E0B"/>
    <text x="875" y="538" font-size="15" font-weight="bold" fill="#B45309">Phân Phối Cụm Khả Thi</text>
    <text x="875" y="565" font-size="13" fill="#334155">• Cụm nhỏ nhất chiếm <tspan font-weight="bold">44.7%</tspan></text>
    <text x="875" y="590" font-size="13" fill="#334155">• Không bị vi phạm cờ cụm cô lập (&lt;5%)</text>
    <text x="875" y="615" font-size="13" fill="#334155">• Rất thuận lợi cho bài toán kinh doanh</text>
  </g>
"""
    return get_svg_wrapper(7, "THỰC NGHIỆM 03", "Đánh Giá Silhouette Score &amp; Độ Ổn Định Cụm (10 Seeds)", "Minh chứng số liệu thực nghiệm: K=2 đạt chất lượng tách cụm và độ lặp lại cao nhất", content, page_role="breathing")

# ==============================================================================
# SLIDE 08: FINAL MODEL DECISION (D011)
# ==============================================================================
def gen_slide_08():
    content = """
  <!-- Top Decision Header Banner -->
  <g id="decision-stamp">
    <rect x="70" y="150" width="1140" height="70" rx="12" fill="#1E3A8A"/>
    <text x="100" y="185" font-size="18" font-weight="bold" fill="#FFFFFF">QUYẾT ĐỊNH ĐÓNG BĂNG MÔ HÌNH: D011</text>
    <text x="100" y="208" font-size="14" fill="#93C5FD">models/selection.json • Trạng thái: FROZEN • Ngày phê duyệt: 2026-10-08</text>
    
    <rect x="990" y="165" width="190" height="40" rx="20" fill="#059669"/>
    <text x="1085" y="190" font-size="14" font-weight="bold" fill="#FFFFFF" text-anchor="middle">✓ VERIFIED &amp; FROZEN</text>
  </g>

  <!-- 4 Specification Pillars -->
  <g id="model-pillars">
    <!-- Pillar 1 -->
    <rect x="70" y="240" width="265" height="235" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
    <rect x="70" y="240" width="265" height="4" rx="2" fill="#2563EB"/>
    <text x="95" y="275" font-size="14" font-weight="bold" fill="#1E40AF">1. PREPROCESSING</text>
    <text x="95" y="305" font-size="18" font-weight="bold" fill="#0F172A">Log1p + Scaler</text>
    <text x="95" y="340" font-size="13" fill="#334155">• log1p(x) triệt tiêu lệch phải</text>
    <text x="95" y="365" font-size="13" fill="#334155">• StandardScaler: mean 0, std 1</text>
    <text x="95" y="390" font-size="13" fill="#334155">• 6 đặc trưng chi tiêu m.u.</text>
    <rect x="85" y="425" width="235" height="36" rx="6" fill="#EFF6FF"/>
    <text x="202" y="448" font-size="12" font-weight="bold" fill="#1E40AF" text-anchor="middle">Feature Scaling Tuyệt Đối</text>

    <!-- Pillar 2 -->
    <rect x="360" y="240" width="265" height="235" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
    <rect x="360" y="240" width="265" height="4" rx="2" fill="#10B981"/>
    <text x="385" y="275" font-size="14" font-weight="bold" fill="#065F46">2. SỐ CỤM PHÂN KHÚC</text>
    <text x="385" y="305" font-size="18" font-weight="bold" fill="#0F172A">K = 2 Cụm</text>
    <text x="385" y="340" font-size="13" fill="#334155">• Tối ưu theo phương pháp Elbow</text>
    <text x="385" y="365" font-size="13" fill="#334155">• Silhouette Score cao nhất (0.307)</text>
    <text x="385" y="390" font-size="13" fill="#334155">• Tỷ lệ phân chia 45% : 55%</text>
    <rect x="375" y="425" width="235" height="36" rx="6" fill="#DCFCE7"/>
    <text x="492" y="448" font-size="12" font-weight="bold" fill="#065F46" text-anchor="middle">Phân Khúc Khả Thi Nhất</text>

    <!-- Pillar 3 -->
    <rect x="650" y="240" width="265" height="235" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
    <rect x="650" y="240" width="265" height="4" rx="2" fill="#F59E0B"/>
    <text x="675" y="275" font-size="14" font-weight="bold" fill="#92400E">3. THUẬT TOÁN &amp; SEED</text>
    <text x="675" y="305" font-size="18" font-weight="bold" fill="#0F172A">Lloyd Algorithm</text>
    <text x="675" y="340" font-size="13" fill="#334155">• random_state = 42</text>
    <text x="675" y="365" font-size="13" fill="#334155">• n_init = 10, max_iter = 300</text>
    <text x="675" y="390" font-size="13" fill="#334155">• Độ ổn định 10 seed: ARI 0.997</text>
    <rect x="665" y="425" width="235" height="36" rx="6" fill="#FEF3C7"/>
    <text x="782" y="448" font-size="12" font-weight="bold" fill="#92400E" text-anchor="middle">Độ Lặp Lại 100%</text>

    <!-- Pillar 4 -->
    <rect x="940" y="240" width="270" height="235" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
    <rect x="940" y="240" width="270" height="4" rx="2" fill="#8B5CF6"/>
    <text x="965" y="275" font-size="14" font-weight="bold" fill="#6B21A8">4. FIT SCOPE</text>
    <text x="965" y="305" font-size="18" font-weight="bold" fill="#0F172A">352 Mẫu Development</text>
    <text x="965" y="340" font-size="13" fill="#334155">• Train (264) + Validation (88)</text>
    <text x="965" y="365" font-size="13" fill="#334155">• Refit sau khi chốt D011</text>
    <text x="965" y="390" font-size="13" fill="#334155">• Tuyệt đối không chạm vào Test</text>
    <rect x="955" y="425" width="240" height="36" rx="6" fill="#F3E8FF"/>
    <text x="1075" y="448" font-size="12" font-weight="bold" fill="#6B21A8" text-anchor="middle">Inertia/row: 4.1639</text>
  </g>

  <!-- Independent Test Set Evaluation -->
  <g id="test-evaluation">
    <rect x="70" y="495" width="1140" height="165" rx="14" fill="#FFFFFF" stroke="#3B82F6" stroke-width="2"/>
    <text x="100" y="530" font-size="15" font-weight="bold" fill="#1E40AF">ĐÁNH GIÁ ĐỘC LẬP TRÊN TẬP TEST (88 MẪU HELD-OUT):</text>
    <text x="100" y="552" font-size="13" fill="#64748B">models/final_evaluation.json • Đánh giá đúng 1 lần sau khi đóng băng kiến trúc</text>

    <!-- Stat 1 -->
    <rect x="100" y="570" width="340" height="75" rx="8" fill="#F8FAFC" stroke="#E2E8F0"/>
    <text x="120" y="598" font-size="12" font-weight="bold" fill="#64748B">TEST SILHOUETTE SCORE</text>
    <text x="120" y="632" font-size="28" font-weight="bold" fill="#2563EB">0.2389</text>
    <text x="235" y="630" font-size="12" fill="#64748B">Khả năng tổng quát hóa vững chắc</text>

    <!-- Stat 2 -->
    <rect x="470" y="570" width="340" height="75" rx="8" fill="#F8FAFC" stroke="#E2E8F0"/>
    <text x="490" y="598" font-size="12" font-weight="bold" fill="#64748B">SỐ LƯỢNG MẪU TẬP TEST</text>
    <text x="490" y="632" font-size="28" font-weight="bold" fill="#059669">45 / 43</text>
    <text x="600" y="630" font-size="12" fill="#64748B">Tỷ lệ: 51.1% vs 48.9% (Cân bằng lý tưởng)</text>

    <!-- Stat 3 -->
    <rect x="840" y="570" width="340" height="75" rx="8" fill="#F8FAFC" stroke="#E2E8F0"/>
    <text x="860" y="598" font-size="12" font-weight="bold" fill="#64748B">ARTIFACT SERVING ĐÓNG GÓI</text>
    <text x="860" y="625" font-size="14" font-weight="bold" fill="#0F172A">models/model.joblib</text>
    <text x="860" y="642" font-size="11" fill="#64748B">SHA-256 Checksum Guard tích hợp API</text>
  </g>
"""
    return get_svg_wrapper(8, "MÔ HÌNH CHÍNH THỨC", "Quyết Định Mô Hình Đóng Băng D011 &amp; Kết Quả Đánh Giá Test", "Thông số kiến trúc chuẩn hóa phục vụ triển khai và kết quả kiểm thử khách quan", content, page_role="anchor")

# ==============================================================================
# SLIDE 09: CLUSTER PROFILES
# ==============================================================================
def gen_slide_09():
    content = """
  <!-- 2 Cluster Persona Cards Side-by-Side -->
  <g id="cluster-personas">
    <!-- Cluster 0: Retailers -->
    <rect x="70" y="150" width="550" height="515" rx="14" fill="#FFFFFF" stroke="#3B82F6" stroke-width="2"/>
    <rect x="70" y="150" width="550" height="6" rx="3" fill="#2563EB"/>

    <!-- Header Badge -->
    <rect x="95" y="175" width="340" height="36" rx="18" fill="#DBEAFE"/>
    <circle cx="113" cy="193" r="12" fill="#2563EB"/>
    <text x="113" y="198" font-size="13" font-weight="bold" fill="#FFFFFF" text-anchor="middle">0</text>
    <text x="135" y="198" font-size="15" font-weight="bold" fill="#1D4ED8">CỤM 0: ĐẠI SIÊU THỊ &amp; CHUỖI BÁN LẺ</text>

    <text x="95" y="240" font-size="14" fill="#64748B">Tỷ lệ: 162/352 mẫu phát triển (46.0%) • Test: 45 mẫu (51.1%)</text>

    <!-- Spending Profile Table -->
    <rect x="95" y="260" width="500" height="150" rx="10" fill="#F8FAFC" stroke="#E2E8F0"/>
    <text x="115" y="285" font-size="13" font-weight="bold" fill="#0F172A">CƠ CẤU CHI TIÊU TRUNG VỊ (MEDIAN EXPENDITURE):</text>
    
    <text x="115" y="315" font-size="13" fill="#334155">• <tspan font-weight="bold" fill="#2563EB">Grocery:</tspan> 10,750 m.u. <tspan fill="#DC2626" font-weight="bold">(Gấp 4.2 lần Cụm 1!)</tspan></text>
    <text x="115" y="340" font-size="13" fill="#334155">• <tspan font-weight="bold" fill="#2563EB">Milk:</tspan> 6,700 m.u. <tspan fill="#DC2626" font-weight="bold">(Gấp 3.5 lần Cụm 1!)</tspan></text>
    <text x="115" y="365" font-size="13" fill="#334155">• <tspan font-weight="bold" fill="#2563EB">Detergents_Paper:</tspan> 4,500 m.u. <tspan fill="#DC2626" font-weight="bold">(Gấp 11.8 lần Cụm 1!)</tspan></text>
    <text x="115" y="390" font-size="13" fill="#64748B">• Fresh: 5,200 m.u. | Frozen: 950 m.u. | Delicassen: 1,250 m.u.</text>

    <!-- Business Strategies Box -->
    <rect x="95" y="425" width="500" height="220" rx="10" fill="#EFF6FF" stroke="#BFDBFE"/>
    <text x="115" y="455" font-size="14" font-weight="bold" fill="#1E40AF">CHIẾN LƯỢC KINH DOANH &amp; TIẾP THỊ ĐỀ XUẤT:</text>
    <text x="115" y="485" font-size="13" fill="#1E3A8A">1. <tspan font-weight="bold">Chính sách chiết khấu theo khối lượng lớn (Volume Rebate):</tspan></text>
    <text x="130" y="505" font-size="13" fill="#334155">Áp dụng cho đơn hàng gộp Grocery + Detergents + Milk.</text>
    <text x="115" y="535" font-size="13" fill="#1E3A8A">2. <tspan font-weight="bold">Hợp đồng cung ứng dài hạn &amp; giao hàng định kỳ:</tspan></text>
    <text x="130" y="555" font-size="13" fill="#334155">Tối ưu hóa logistics theo container/xe tải trọng tải lớn.</text>
    <text x="115" y="585" font-size="13" fill="#1E3A8A">3. <tspan font-weight="bold">Hạn mức tín dụng thương mại (Credit Line) cao:</tspan></text>
    <text x="130" y="605" font-size="13" fill="#334155">Chu kỳ thanh toán 30-45 ngày cho các chuỗi bán lẻ uy tín.</text>

    <!-- Cluster 1: Horeca -->
    <rect x="660" y="150" width="550" height="515" rx="14" fill="#FFFFFF" stroke="#059669" stroke-width="2"/>
    <rect x="660" y="150" width="550" height="6" rx="3" fill="#059669"/>

    <!-- Header Badge -->
    <rect x="685" y="175" width="370" height="36" rx="18" fill="#DCFCE7"/>
    <circle cx="703" cy="193" r="12" fill="#059669"/>
    <text x="703" y="198" font-size="13" font-weight="bold" fill="#FFFFFF" text-anchor="middle">1</text>
    <text x="725" y="198" font-size="15" font-weight="bold" fill="#065F46">CỤM 1: NHÀ HÀNG, KHÁCH SẠN &amp; CAFE (HORECA)</text>

    <text x="685" y="240" font-size="14" fill="#64748B">Tỷ lệ: 190/352 mẫu phát triển (54.0%) • Test: 43 mẫu (48.9%)</text>

    <!-- Spending Profile Table -->
    <rect x="685" y="260" width="500" height="150" rx="10" fill="#F8FAFC" stroke="#E2E8F0"/>
    <text x="705" y="285" font-size="13" font-weight="bold" fill="#0F172A">CƠ CẤU CHI TIÊU TRUNG VỊ (MEDIAN EXPENDITURE):</text>
    
    <text x="705" y="315" font-size="13" fill="#334155">• <tspan font-weight="bold" fill="#059669">Fresh (Tươi sống):</tspan> 11,200 m.u. <tspan fill="#059669" font-weight="bold">(Gấp 2.15 lần Cụm 0!)</tspan></text>
    <text x="705" y="340" font-size="13" fill="#334155">• <tspan font-weight="bold" fill="#059669">Frozen (Đông lạnh):</tspan> 2,800 m.u. <tspan fill="#059669" font-weight="bold">(Gấp 2.95 lần Cụm 0!)</tspan></text>
    <text x="705" y="365" font-size="13" fill="#64748B">• Detergents_Paper: chỉ 380 m.u. (Mức tiêu thụ rất thấp)</text>
    <text x="705" y="390" font-size="13" fill="#64748B">• Grocery: 2,550 m.u. | Milk: 1,900 m.u. | Delicassen: 850 m.u.</text>

    <!-- Business Strategies Box -->
    <rect x="685" y="425" width="500" height="220" rx="10" fill="#ECFDF5" stroke="#A7F3D0"/>
    <text x="705" y="455" font-size="14" font-weight="bold" fill="#065F46">CHIẾN LƯỢC KINH DOANH &amp; TIẾP THỊ ĐỀ XUẤT:</text>
    <text x="705" y="485" font-size="13" fill="#064E3B">1. <tspan font-weight="bold">Cam kết độ tươi sống &amp; chuỗi cung ứng lạnh (Cold-chain):</tspan></text>
    <text x="720" y="505" font-size="13" fill="#334155">Kiểm soát nhiệt độ bảo quản nghiêm ngặt từ kho đến bếp.</text>
    <text x="705" y="535" font-size="13" fill="#064E3B">2. <tspan font-weight="bold">Tần suất giao hàng hằng ngày (Daily Delivery):</tspan></text>
    <text x="720" y="555" font-size="13" fill="#334155">Đáp ứng dung lượng kho lạnh hữu hạn của các nhà hàng.</text>
    <text x="705" y="585" font-size="13" fill="#064E3B">3. <tspan font-weight="bold">Ứng dụng đặt hàng nhanh qua di động (Mobile Ordering):</tspan></text>
    <text x="720" y="605" font-size="13" fill="#334155">Đặt hàng ca đêm và giao trước 6h sáng hằng ngày.</text>
  </g>
"""
    return get_svg_wrapper(9, "CHÂN DUNG PHÂN KHÚC", "Chân Dung 2 Nhóm Khách Hàng Bán Sỉ &amp; Ý Nghĩa Kinh Doanh", "Sự tương phản rõ nét giữa nhóm Đại siêu thị (Cụm 0) và nhóm Nhà hàng ẩm thực (Cụm 1)", content, page_role="anchor")

# ==============================================================================
# SLIDE 10: CHANNEL & REGION CROSS VALIDATION
# ==============================================================================
def gen_slide_10():
    content = """
  <!-- Top Explanation -->
  <g id="cross-validation-note">
    <rect x="70" y="150" width="1140" height="60" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
    <text x="95" y="186" font-size="14" font-weight="bold" fill="#1E40AF">KIỂM ĐỊNH ĐỘC LẬP:</text>
    <text x="260" y="186" font-size="14" fill="#334155">Channel và Region hoàn toàn KHÔNG tham gia vào huấn luyện. Bảng phân tích chéo dùng để đối soát tính hợp lý nghiệp vụ.</text>
  </g>

  <!-- 2x3 Cross-Distribution Heatmap Matrix -->
  <g id="cross-matrix">
    <rect x="70" y="230" width="670" height="435" rx="14" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
    <text x="100" y="265" font-size="15" font-weight="bold" fill="#0F172A">Ma Trận Phân Bổ Cụm Theo Kênh Bán &amp; Vùng Địa Lý</text>
    <text x="100" y="288" font-size="12" fill="#64748B">reports/data/final_profile/channel_profile.csv &amp; region_profile.csv (352 mẫu dev)</text>

    <!-- Table Canvas -->
    <g transform="translate(100 310)">
      <!-- Header -->
      <rect x="0" y="0" width="510" height="40" fill="#1E293B" rx="8"/>
      <text x="110" y="25" font-size="13" font-weight="bold" fill="#FFFFFF" text-anchor="middle">KÊNH / KHU VỰC</text>
      <text x="280" y="25" font-size="13" font-weight="bold" fill="#93C5FD" text-anchor="middle">CỤM 0 (RETAIL)</text>
      <text x="420" y="25" font-size="13" font-weight="bold" fill="#86EFAC" text-anchor="middle">CỤM 1 (HORECA)</text>

      <!-- Row 1: Channel Horeca -->
      <rect x="0" y="45" width="510" height="50" fill="#F8FAFC"/>
      <text x="20" y="75" font-size="14" font-weight="bold" fill="#0F172A">Channel 1: Horeca</text>
      <rect x="235" y="52" width="90" height="36" rx="6" fill="#EFF6FF"/>
      <text x="280" y="75" font-size="14" font-weight="bold" fill="#1D4ED8" text-anchor="middle">38 mẫu (16%)</text>
      <rect x="375" y="52" width="90" height="36" rx="6" fill="#DCFCE7"/>
      <text x="420" y="75" font-size="14" font-weight="bold" fill="#059669" text-anchor="middle">198 mẫu (84%)</text>

      <!-- Row 2: Channel Retail -->
      <rect x="0" y="100" width="510" height="50" fill="#FFFFFF"/>
      <text x="20" y="130" font-size="14" font-weight="bold" fill="#0F172A">Channel 2: Retail</text>
      <rect x="235" y="107" width="90" height="36" rx="6" fill="#DBEAFE"/>
      <text x="280" y="130" font-size="14" font-weight="bold" fill="#1E40AF" text-anchor="middle">104 mẫu (90%)</text>
      <rect x="375" y="107" width="90" height="36" rx="6" fill="#F1F5F9"/>
      <text x="420" y="130" font-size="14" fill="#64748B" text-anchor="middle">12 mẫu (10%)</text>

      <!-- Row Divider -->
      <line x1="0" y1="160" x2="510" y2="160" stroke="#CBD5E1" stroke-width="1.5"/>

      <!-- Row 3: Region Lisbon -->
      <rect x="0" y="170" width="510" height="45" fill="#F8FAFC"/>
      <text x="20" y="198" font-size="13" fill="#334155">Region 1: Lisbon (61 mẫu)</text>
      <text x="280" y="198" font-size="13" fill="#1E40AF" text-anchor="middle">24 mẫu (39.3%)</text>
      <text x="420" y="198" font-size="13" fill="#059669" text-anchor="middle">37 mẫu (60.7%)</text>

      <!-- Row 4: Region Oporto -->
      <rect x="0" y="220" width="510" height="45" fill="#FFFFFF"/>
      <text x="20" y="248" font-size="13" fill="#334155">Region 2: Oporto (37 mẫu)</text>
      <text x="280" y="248" font-size="13" fill="#1E40AF" text-anchor="middle">17 mẫu (45.9%)</text>
      <text x="420" y="248" font-size="13" fill="#059669" text-anchor="middle">20 mẫu (54.1%)</text>

      <!-- Row 5: Region Other -->
      <rect x="0" y="270" width="510" height="45" fill="#F8FAFC"/>
      <text x="20" y="298" font-size="13" fill="#334155">Region 3: Other (254 mẫu)</text>
      <text x="280" y="298" font-size="13" fill="#1E40AF" text-anchor="middle">101 mẫu (39.8%)</text>
      <text x="420" y="298" font-size="13" fill="#059669" text-anchor="middle">153 mẫu (60.2%)</text>
    </g>
  </g>

  <!-- Right Insights Column -->
  <g id="channel-insights">
    <!-- Insight 1: High Alignment -->
    <rect x="760" y="230" width="450" height="205" rx="14" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
    <rect x="760" y="230" width="450" height="6" rx="3" fill="#2563EB"/>
    <text x="790" y="265" font-size="15" font-weight="bold" fill="#1E40AF">Tương Quan Kênh Bán Rất Cao</text>
    <text x="790" y="295" font-size="14" fill="#334155">• <tspan font-weight="bold">90% khách hàng Retail</tspan> rơi chính xác vào Cụm 0</text>
    <text x="805" y="318" font-size="13" fill="#64748B">(Nhóm chi tiêu mạnh vào Hàng tạp hóa &amp; Sữa).</text>
    <text x="790" y="348" font-size="14" fill="#334155">• <tspan font-weight="bold">84% khách hàng Horeca</tspan> rơi chính xác vào Cụm 1</text>
    <text x="805" y="371" font-size="13" fill="#64748B">(Nhóm tiêu thụ chính Hàng tươi sống &amp; Đông lạnh).</text>
    <text x="790" y="405" font-size="13" font-weight="bold" fill="#059669">➔ Chứng minh K-Means tự tìm thấy chân lý nghiệp vụ!</text>

    <!-- Insight 2: Geographic Invariance -->
    <rect x="760" y="455" width="450" height="210" rx="14" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
    <rect x="760" y="455" width="450" height="6" rx="3" fill="#10B981"/>
    <text x="790" y="490" font-size="15" font-weight="bold" fill="#065F46">Tính Bất Biến Theo Địa Lý (Region Invariance)</text>
    <text x="790" y="520" font-size="14" fill="#334155">• Tỷ lệ phân bổ Cụm 0 / Cụm 1 duy trì xấp xỉ <tspan font-weight="bold">40% / 60%</tspan></text>
    <text x="805" y="543" font-size="13" fill="#64748B">trên cả 3 khu vực: Lisbon, Oporto và Other.</text>
    <text x="790" y="575" font-size="14" fill="#334155">• Cho thấy cơ cấu chi tiêu không bị chi phối cục bộ</text>
    <text x="805" y="598" font-size="13" fill="#64748B">bởi địa lý, mà hoàn toàn xuất phát từ bản chất kinh doanh.</text>
    <text x="790" y="630" font-size="13" font-weight="bold" fill="#059669">➔ Mô hình có thể triển khai mở rộng toàn quốc.</text>
  </g>
"""
    return get_svg_wrapper(10, "ĐỐI SOÁT NGHIỆP VỤ", "Phân Tích Chéo Kênh Bán Hàng &amp; Khu Vực Địa Lý", "Kiểm định khách quan mối liên hệ giữa các cụm tìm được với Channel và Region thực tế", content, page_role="breathing")

# ==============================================================================
# SLIDE 11: SYSTEM ARCHITECTURE & TECH STACK
# ==============================================================================
def gen_slide_11():
    content = """
  <!-- 3-Tier Architecture Diagram -->
  <g id="system-architecture">
    <!-- Tier 1: Frontend -->
    <rect x="70" y="160" width="360" height="490" rx="14" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
    <rect x="70" y="160" width="360" height="6" rx="3" fill="#3B82F6"/>
    <text x="100" y="195" font-size="13" font-weight="bold" fill="#1D4ED8">TẦNG 1: TRÌNH DIỄN (FRONTEND)</text>
    <text x="100" y="225" font-size="18" font-weight="bold" fill="#0F172A">React 18 + Tailwind</text>
    <text x="100" y="250" font-size="13" fill="#64748B">Giao diện SPA hiện đại, đáp ứng đa thiết bị</text>

    <!-- Features -->
    <rect x="95" y="275" width="310" height="65" rx="8" fill="#F8FAFC" stroke="#E2E8F0"/>
    <text x="110" y="302" font-size="13" font-weight="bold" fill="#0F172A">Biểu Mẫu Nhập Liệu 6 Đặc Trưng:</text>
    <text x="110" y="325" font-size="12" fill="#64748B">Kiểm tra giá trị biên &amp; cảnh báo tức thì</text>

    <rect x="95" y="350" width="310" height="65" rx="8" fill="#F8FAFC" stroke="#E2E8F0"/>
    <text x="110" y="377" font-size="13" font-weight="bold" fill="#0F172A">Trực Quan Hóa Đồ Thị Động:</text>
    <text x="110" y="400" font-size="12" fill="#64748B">Radar chart so sánh hồ sơ với tâm cụm</text>

    <rect x="95" y="425" width="310" height="65" rx="8" fill="#F8FAFC" stroke="#E2E8F0"/>
    <text x="110" y="452" font-size="13" font-weight="bold" fill="#0F172A">Xử Lý Batch &amp; Xuất Báo Cáo:</text>
    <text x="110" y="475" font-size="12" fill="#64748B">Tải lên file CSV và phân loại hàng loạt</text>

    <!-- Tech Badges -->
    <rect x="95" y="585" width="310" height="45" rx="8" fill="#EFF6FF"/>
    <text x="250" y="612" font-size="12" font-weight="bold" fill="#1D4ED8" text-anchor="middle">TypeScript • Vite • TailwindCSS • Chart.js</text>

    <!-- Tier 2: Backend API -->
    <rect x="460" y="160" width="360" height="490" rx="14" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
    <rect x="460" y="160" width="360" height="6" rx="3" fill="#059669"/>
    <text x="490" y="195" font-size="13" font-weight="bold" fill="#065F46">TẦNG 2: XỬ LÝ DỊCH VỤ (BACKEND)</text>
    <text x="490" y="225" font-size="18" font-weight="bold" fill="#0F172A">Fastify REST API</text>
    <text x="490" y="250" font-size="13" fill="#64748B">Microservice Node.js tốc độ cao &amp; bảo mật</text>

    <!-- API Endpoints -->
    <rect x="485" y="275" width="310" height="65" rx="8" fill="#F8FAFC" stroke="#E2E8F0"/>
    <text x="500" y="302" font-size="13" font-weight="bold" fill="#059669">POST /api/segment</text>
    <text x="500" y="325" font-size="12" fill="#64748B">Nhận 6 biến chi tiêu ➔ trả về nhãn cụm &amp; độ cách</text>

    <rect x="485" y="350" width="310" height="65" rx="8" fill="#F8FAFC" stroke="#E2E8F0"/>
    <text x="500" y="377" font-size="13" font-weight="bold" fill="#059669">GET /api/dashboard</text>
    <text x="500" y="400" font-size="12" fill="#64748B">Cung cấp thống kê tổng thể và thông tin model</text>

    <rect x="485" y="425" width="310" height="65" rx="8" fill="#F8FAFC" stroke="#E2E8F0"/>
    <text x="500" y="452" font-size="13" font-weight="bold" fill="#059669">GET /api/health</text>
    <text x="500" y="475" font-size="12" fill="#64748B">Kiểm tra trạng thái sẵn sàng (Readiness probe)</text>

    <!-- Tech Badges -->
    <rect x="485" y="585" width="310" height="45" rx="8" fill="#ECFDF5"/>
    <text x="640" y="612" font-size="12" font-weight="bold" fill="#065F46" text-anchor="middle">Fastify • Pydantic/Zod Schema • CORS</text>

    <!-- Tier 3: ML Serving Core -->
    <rect x="850" y="160" width="360" height="490" rx="14" fill="#FFFFFF" stroke="#8B5CF6" stroke-width="2"/>
    <rect x="850" y="160" width="360" height="6" rx="3" fill="#8B5CF6"/>
    <text x="880" y="195" font-size="13" font-weight="bold" fill="#6B21A8">TẦNG 3: TRỌNG TÂM MÔ HÌNH (ML CORE)</text>
    <text x="880" y="225" font-size="18" font-weight="bold" fill="#0F172A">Frozen Artifacts</text>
    <text x="880" y="250" font-size="13" fill="#64748B">Mô hình đóng băng bất biến (Zero Retraining)</text>

    <!-- Security & Checksum -->
    <rect x="875" y="275" width="310" height="65" rx="8" fill="#F8FAFC" stroke="#E2E8F0"/>
    <text x="890" y="302" font-size="13" font-weight="bold" fill="#7C3AED">SHA-256 Checksum Guard:</text>
    <text x="890" y="325" font-size="12" fill="#64748B">Chống can thiệp hoặc sửa đổi file model trái phép</text>

    <rect x="875" y="350" width="310" height="65" rx="8" fill="#F8FAFC" stroke="#E2E8F0"/>
    <text x="890" y="377" font-size="13" font-weight="bold" fill="#7C3AED">Python ↔ Node Parity:</text>
    <text x="890" y="400" font-size="12" fill="#64748B">Kiểm định dự đoán chính xác tuyệt đối trên 2 môi trường</text>

    <rect x="875" y="425" width="310" height="65" rx="8" fill="#F8FAFC" stroke="#E2E8F0"/>
    <text x="890" y="452" font-size="13" font-weight="bold" fill="#7C3AED">Tải Model 1 Lần (Singleton):</text>
    <text x="890" y="475" font-size="12" fill="#64748B">Phản hồi inference dưới 10ms trên mỗi request</text>

    <!-- Tech Badges -->
    <rect x="875" y="585" width="310" height="45" rx="8" fill="#F3E8FF"/>
    <text x="1030" y="612" font-size="12" font-weight="bold" fill="#6B21A8" text-anchor="middle">Scikit-Learn • Joblib • Docker Ready</text>
  </g>
"""
    return get_svg_wrapper(11, "KIẾN TRÚC HỆ THỐNG", "Kiến Trúc Tổng Thể &amp; Tech Stack Triển Khai Thực Tế", "Mô hình phục vụ 3 lớp: Giao diện trực quan, API trung gian và Lõi mô hình bất biến", content, page_role="anchor")

# ==============================================================================
# SLIDE 12: WEB APPLICATION UI
# ==============================================================================
def gen_slide_12():
    content = """
  <!-- Browser Mockup Window -->
  <g id="browser-mockup">
    <rect x="70" y="150" width="1140" height="515" rx="14" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="2"/>
    
    <!-- Browser Top Bar -->
    <rect x="70" y="150" width="1140" height="40" rx="14" fill="#F1F5F9"/>
    <circle cx="95" cy="170" r="6" fill="#EF4444"/>
    <circle cx="115" cy="170" r="6" fill="#F59E0B"/>
    <circle cx="135" cy="170" r="6" fill="#10B981"/>
    
    <rect x="250" y="157" width="700" height="26" rx="6" fill="#FFFFFF" stroke="#E2E8F0"/>
    <text x="600" y="174" font-size="12" fill="#64748B" text-anchor="middle">http://localhost:3000 • Hệ Thống Phân Khúc Khách Hàng Bán Sỉ (Project 22)</text>

    <!-- Mockup Content: Left Input Form -->
    <g transform="translate(100 210)">
      <text x="0" y="20" font-size="15" font-weight="bold" fill="#0F172A">Biểu Mẫu Nhập Liệu Khách Hàng</text>
      <text x="0" y="42" font-size="12" fill="#64748B">Nhập mức chi tiêu hằng năm của 6 nhóm mặt hàng (m.u.)</text>

      <!-- Input 1 & 2 -->
      <rect x="0" y="60" width="220" height="45" rx="6" fill="#F8FAFC" stroke="#CBD5E1"/>
      <text x="15" y="78" font-size="11" fill="#64748B">Fresh (Tươi sống)</text>
      <text x="15" y="96" font-size="14" font-weight="bold" fill="#0F172A">12,500</text>

      <rect x="240" y="60" width="220" height="45" rx="6" fill="#F8FAFC" stroke="#CBD5E1"/>
      <text x="255" y="78" font-size="11" fill="#64748B">Milk (Sữa)</text>
      <text x="255" y="96" font-size="14" font-weight="bold" fill="#0F172A">2,100</text>

      <!-- Input 3 & 4 -->
      <rect x="0" y="120" width="220" height="45" rx="6" fill="#F8FAFC" stroke="#CBD5E1"/>
      <text x="15" y="138" font-size="11" fill="#64748B">Grocery (Tạp hóa)</text>
      <text x="15" y="156" font-size="14" font-weight="bold" fill="#0F172A">3,200</text>

      <rect x="240" y="120" width="220" height="45" rx="6" fill="#F8FAFC" stroke="#CBD5E1"/>
      <text x="255" y="138" font-size="11" fill="#64748B">Frozen (Đông lạnh)</text>
      <text x="255" y="156" font-size="14" font-weight="bold" fill="#0F172A">4,800</text>

      <!-- Input 5 & 6 -->
      <rect x="0" y="180" width="220" height="45" rx="6" fill="#F8FAFC" stroke="#CBD5E1"/>
      <text x="15" y="198" font-size="11" fill="#64748B">Detergents_Paper</text>
      <text x="15" y="216" font-size="14" font-weight="bold" fill="#0F172A">450</text>

      <rect x="240" y="180" width="220" height="45" rx="6" fill="#F8FAFC" stroke="#CBD5E1"/>
      <text x="255" y="198" font-size="11" fill="#64748B">Delicassen (Đồ nguội)</text>
      <text x="255" y="216" font-size="14" font-weight="bold" fill="#0F172A">950</text>

      <!-- Predict Button -->
      <rect x="0" y="245" width="460" height="42" rx="8" fill="#2563EB"/>
      <text x="230" y="271" font-size="14" font-weight="bold" fill="#FFFFFF" text-anchor="middle">🔍 PHÂN TÍCH &amp; DỰ ĐOÁN PHÂN KHÚC</text>
    </g>

    <!-- Mockup Content: Right Result Panel -->
    <g transform="translate(600 210)">
      <rect x="0" y="0" width="560" height="410" rx="12" fill="#F8FAFC" stroke="#E2E8F0"/>
      <text x="25" y="35" font-size="15" font-weight="bold" fill="#0F172A">Kết Quả Phân Tích Thời Gian Thực</text>

      <!-- Prediction Badge -->
      <rect x="25" y="55" width="510" height="90" rx="10" fill="#ECFDF5" stroke="#10B981" stroke-width="1.5"/>
      <text x="50" y="85" font-size="13" font-weight="bold" fill="#065F46">PHÂN KHÚC DỰ ĐOÁN:</text>
      <text x="50" y="125" font-size="28" font-weight="bold" fill="#059669">CỤM 1 — NHÀ HÀNG / HORECA</text>
      <text x="380" y="115" font-size="13" fill="#065F46">Độ tương đồng: <tspan font-weight="bold">94.8%</tspan></text>

      <!-- Insight Callout -->
      <rect x="25" y="160" width="510" height="230" rx="10" fill="#FFFFFF" stroke="#E2E8F0"/>
      <text x="45" y="190" font-size="14" font-weight="bold" fill="#0F172A">Đặc Điểm &amp; Khuyến Nghị Từ Hệ Thống:</text>
      <text x="45" y="220" font-size="13" fill="#334155">• <tspan font-weight="bold">Chi tiêu Fresh vượt trội (12,500 m.u.):</tspan> Nhu cầu tiêu thụ rau củ, thịt tươi sống hằng ngày rất cao.</text>
      <text x="45" y="250" font-size="13" fill="#334155">• <tspan font-weight="bold">Chi tiêu Frozen cao (4,800 m.u.):</tspan> Phù hợp với cơ cấu nhà bếp nhà hàng chuẩn bị sẵn.</text>
      <text x="45" y="280" font-size="13" fill="#334155">• <tspan font-weight="bold">Khoảng cách Euclidean tới tâm Cụm 1:</tspan> 0.412 (Gần hơn nhiều so với Cụm 0: 2.185).</text>
      
      <rect x="45" y="310" width="470" height="60" rx="8" fill="#EFF6FF"/>
      <text x="65" y="335" font-size="13" font-weight="bold" fill="#1E40AF">HÀNH ĐỘNG GỢI Ý CHO NHÂN VIÊN KINH DOANH:</text>
      <text x="65" y="355" font-size="12" fill="#1E3A8A">Gửi báo giá ưu đãi nguồn hàng thủy hải sản tươi sống và đề xuất lịch giao 6h sáng hằng ngày.</text>
    </g>
  </g>
"""
    return get_svg_wrapper(12, "ỨNG DỤNG THỰC TẾ", "Giao Diện Ứng Dụng Web &amp; Dự Đoán Phân Khúc Trực Tuyến", "Trải nghiệm người dùng: Biểu mẫu nhập liệu trực quan, dự đoán dưới 10ms và khuyến nghị nghiệp vụ", content, page_role="anchor")

# ==============================================================================
# SLIDE 13: QUALITY ASSURANCE & TESTING
# ==============================================================================
def gen_slide_13():
    content = """
  <!-- Testing Pyramid & Metrics -->
  <g id="testing-suite">
    <!-- Card 1: Testing Pyramid -->
    <rect x="70" y="150" width="550" height="515" rx="14" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
    <rect x="70" y="150" width="550" height="6" rx="3" fill="#2563EB"/>
    <text x="100" y="190" font-size="18" font-weight="bold" fill="#0F172A">Kim Tự Tháp Kiểm Thử Tự Động (Test Suite)</text>
    <text x="100" y="215" font-size="13" fill="#64748B">Kiểm định đa tầng từ thuật toán ML đến giao diện người dùng</text>

    <!-- Layer 1: E2E Playwright -->
    <g transform="translate(100 245)">
      <polygon points="175,0 315,0 365,70 125,70" fill="#EFF6FF" stroke="#3B82F6" stroke-width="2"/>
      <text x="245" y="32" font-size="14" font-weight="bold" fill="#1D4ED8" text-anchor="middle">E2E PLAYWRIGHT TESTS</text>
      <text x="245" y="52" font-size="12" fill="#1E40AF" text-anchor="middle">22/22 Tests Pass (Desktop &amp; Mobile Emulation)</text>
    </g>

    <!-- Layer 2: Backend Fastify API -->
    <g transform="translate(100 325)">
      <polygon points="120,0 370,0 420,70 70,70" fill="#ECFDF5" stroke="#10B981" stroke-width="2"/>
      <text x="245" y="32" font-size="14" font-weight="bold" fill="#065F46" text-anchor="middle">BACKEND &amp; INTEGRATION TESTS</text>
      <text x="245" y="52" font-size="12" fill="#064E3B" text-anchor="middle">15/15 Tests Pass (Fastify, Health, Strict Schema)</text>
    </g>

    <!-- Layer 3: Python ML Core Tests -->
    <g transform="translate(100 405)">
      <polygon points="65,0 425,0 480,80 10,80" fill="#FAF5FF" stroke="#8B5CF6" stroke-width="2"/>
      <text x="245" y="35" font-size="14" font-weight="bold" fill="#6B21A8" text-anchor="middle">PYTHON ML UNIT TESTS</text>
      <text x="245" y="58" font-size="12" fill="#581C87" text-anchor="middle">8/8 Tests Pass (Leakage Guard, Sklearn Parity, Checksum)</text>
    </g>

    <!-- Summary Box -->
    <rect x="95" y="515" width="495" height="120" rx="10" fill="#F8FAFC" stroke="#E2E8F0"/>
    <text x="115" y="545" font-size="14" font-weight="bold" fill="#0F172A">TIÊU CHÍ AN TOÀN ĐÃ KIỂM CHỨNG:</text>
    <text x="115" y="570" font-size="13" fill="#334155">✓ <tspan font-weight="bold">Chống can thiệp file model:</tspan> Tự động từ chối nếu SHA-256 bị sai lệch</text>
    <text x="115" y="595" font-size="13" fill="#334155">✓ <tspan font-weight="bold">Bảo vệ tập Test:</tspan> Không bao giờ xuất file test.csv ra runner công khai</text>
    <text x="115" y="620" font-size="13" fill="#334155">✓ <tspan font-weight="bold">Bảo mật mã nguồn:</tspan> npm audit đạt 0 lỗ hổng bảo mật (0 vulnerabilities)</text>
  </g>

  <!-- CI/CD & Verification Cards -->
  <g id="ci-cd-cards">
    <!-- GitHub Actions Card -->
    <rect x="660" y="150" width="550" height="240" rx="14" fill="#FFFFFF" stroke="#10B981" stroke-width="2"/>
    <rect x="660" y="150" width="550" height="6" rx="3" fill="#10B981"/>
    <text x="690" y="190" font-size="18" font-weight="bold" fill="#065F46">Quy Trình CI/CD Tự Động (GitHub Actions)</text>
    <text x="690" y="215" font-size="13" fill="#64748B">Xác thực tự động trên các runner độc lập mỗi khi cập nhật mã nguồn</text>

    <g transform="translate(690 240)">
      <rect x="0" y="0" width="235" height="65" rx="8" fill="#ECFDF5"/>
      <text x="15" y="25" font-size="12" font-weight="bold" fill="#065F46">WINDOWS RUNNER</text>
      <text x="15" y="48" font-size="14" font-weight="bold" fill="#059669">✓ 100% PASS (Gate 8)</text>

      <rect x="255" y="0" width="235" height="65" rx="8" fill="#ECFDF5"/>
      <text x="270" y="25" font-size="12" font-weight="bold" fill="#065F46">UBUNTU RUNNER</text>
      <text x="270" y="48" font-size="14" font-weight="bold" fill="#059669">✓ 100% PASS (Gate 9.3)</text>

      <rect x="0" y="75" width="490" height="55" rx="8" fill="#F8FAFC" stroke="#E2E8F0"/>
      <text x="15" y="98" font-size="12" fill="#334155">• Clean environment checkout &amp; npm ci</text>
      <text x="15" y="118" font-size="12" fill="#334155">• Cross-platform verification: Windows CRLF ↔ Linux LF compatibility</text>
    </g>

    <!-- Reproducibility Card -->
    <rect x="660" y="415" width="550" height="250" rx="14" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
    <rect x="660" y="415" width="550" height="6" rx="3" fill="#2563EB"/>
    <text x="690" y="450" font-size="18" font-weight="bold" fill="#1E40AF">Khả Năng Tái Lập (Reproducibility)</text>
    <text x="690" y="475" font-size="13" fill="#334155">• <tspan font-weight="bold">Single Command Setup:</tspan> Khởi chạy toàn bộ hệ thống bằng <tspan font-family="monospace">run.bat</tspan></text>
    <text x="690" y="505" font-size="13" fill="#334155">• <tspan font-weight="bold">Deterministic Pipeline:</tspan> Cùng seed 42 luôn sinh ra đúng 100% kết quả</text>
    <text x="690" y="535" font-size="13" fill="#334155">• <tspan font-weight="bold">Dokumentation Trọn Vẹn:</tspan> Hệ thống tài liệu kiến trúc tại <tspan font-family="monospace">docs/</tspan></text>

    <rect x="690" y="570" width="490" height="75" rx="8" fill="#EFF6FF"/>
    <text x="710" y="598" font-size="13" font-weight="bold" fill="#1D4ED8">SẴN SÀNG CHO ĐÁNH GIÁ HỘI ĐỒNG:</text>
    <text x="710" y="625" font-size="12" fill="#1E40AF">Tất cả bài test có thể chạy lại trực tiếp tại buổi bảo vệ đồ án mà không có sai lệch.</text>
  </g>
"""
    return get_svg_wrapper(13, "ĐẢM BẢO CHẤT LƯỢNG", "Kiểm Thử Toàn Diện, Bảo Mật &amp; Quy Trình CI/CD", "Chứng minh tính ổn định, độ tin cậy và sự sẵn sàng bàn giao của hệ thống phần mềm", content, page_role="breathing")

# ==============================================================================
# SLIDE 14: LIMITATIONS & FUTURE WORK
# ==============================================================================
def gen_slide_14():
    content = """
  <!-- Left Side: Limitations -->
  <g id="project-limitations">
    <rect x="70" y="150" width="540" height="515" rx="14" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
    <rect x="70" y="150" width="540" height="6" rx="3" fill="#F59E0B"/>
    <text x="100" y="190" font-size="18" font-weight="bold" fill="#0F172A">Giới Hạn Hiện Tại Của Đề Tài</text>
    <text x="100" y="215" font-size="13" fill="#64748B">Các yếu tố ràng buộc khách quan từ tập dữ liệu và phạm vi môn học</text>

    <!-- Lim 1 -->
    <rect x="95" y="245" width="490" height="110" rx="10" fill="#F8FAFC" stroke="#E2E8F0"/>
    <text x="115" y="275" font-size="15" font-weight="bold" fill="#B45309">1. Kích Thước Mẫu Hạn Chế (440 Quan Sát)</text>
    <text x="115" y="302" font-size="13" fill="#334155">• Tập dữ liệu tương đối nhỏ, dù đủ cho thuật toán phân cụm K-Means</text>
    <text x="115" y="325" font-size="13" fill="#334155">cơ bản nhưng chưa bao quát được toàn bộ phân khúc thị trường rộng lớn.</text>
    <text x="115" y="345" font-size="12" fill="#64748B">Cần bổ sung thêm dữ liệu giao dịch từ nhiều nhà phân phối khác nhau.</text>

    <!-- Lim 2 -->
    <rect x="95" y="375" width="490" height="110" rx="10" fill="#F8FAFC" stroke="#E2E8F0"/>
    <text x="115" y="405" font-size="15" font-weight="bold" fill="#B45309">2. Dữ Liệu Tĩnh &amp; Thiếu Yếu Tố Thời Gian</text>
    <text x="115" y="432" font-size="13" fill="#334155">• 6 biến chi tiêu là tổng hợp hằng năm, không có mốc thời gian (timestamp).</text>
    <text x="115" y="455" font-size="13" fill="#334155">• Chưa thể phân tích tính thời vụ (mùa du lịch, lễ tết) hay tần suất mua.</text>
    <text x="115" y="475" font-size="12" fill="#64748B">Chưa khai thác được các thuộc tính Recency &amp; Frequency trong mô hình RFM.</text>

    <!-- Lim 3 -->
    <rect x="95" y="505" width="490" height="135" rx="10" fill="#F8FAFC" stroke="#E2E8F0"/>
    <text x="115" y="535" font-size="15" font-weight="bold" fill="#B45309">3. Giả Định Cụm Hình Cầu Của K-Means</text>
    <text x="115" y="562" font-size="13" fill="#334155">• K-Means ngầm định các cụm có hình cầu lồi và phương sai tương đồng.</text>
    <text x="115" y="585" font-size="13" fill="#334155">• Với dữ liệu phân bố mật độ phức tạp, K-Means có thể bỏ lỡ hình thái cụm.</text>
    <text x="115" y="615" font-size="12" font-weight="bold" fill="#991B1B">➔ D011 đã giảm thiểu rủi ro này bằng Log1p transform trước khi fit.</text>
  </g>

  <!-- Right Side: Future Work -->
  <g id="future-roadmap">
    <rect x="650" y="150" width="560" height="515" rx="14" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
    <rect x="650" y="150" width="560" height="6" rx="3" fill="#10B981"/>
    <text x="680" y="190" font-size="18" font-weight="bold" fill="#0F172A">Hướng Phát Triển Tương Lai (Roadmap)</text>
    <text x="680" y="215" font-size="13" fill="#64748B">Kế hoạch mở rộng nâng cấp hệ thống trong môi trường sản xuất thực tế</text>

    <!-- Phase 1 -->
    <rect x="675" y="245" width="510" height="110" rx="10" fill="#ECFDF5" stroke="#A7F3D0"/>
    <text x="695" y="275" font-size="15" font-weight="bold" fill="#065F46">GIAI ĐOẠN 1: MỞ RỘNG MÔ HÌNH RFM &amp; CHUỖI THỜI GIAN</text>
    <text x="695" y="302" font-size="13" fill="#334155">• Thu thập log giao dịch chi tiết theo ngày để tính:</text>
    <text x="710" y="325" font-size="13" fill="#064E3B">• <tspan font-weight="bold">Recency</tspan> (Lần mua gần nhất), <tspan font-weight="bold">Frequency</tspan> (Tần suất) và <tspan font-weight="bold">Monetary</tspan>.</text>
    <text x="695" y="345" font-size="12" fill="#065F46">Nhận diện sớm các khách hàng bán sỉ có nguy cơ rời bỏ (Churn prediction).</text>

    <!-- Phase 2 -->
    <rect x="675" y="375" width="510" height="110" rx="10" fill="#EFF6FF" stroke="#BFDBFE"/>
    <text x="695" y="405" font-size="15" font-weight="bold" fill="#1D4ED8">GIAI ĐOẠN 2: THỬ NGHIỆM MÔ HÌNH NÂNG CAO (GMM / DBSCAN)</text>
    <text x="695" y="432" font-size="13" fill="#334155">• Thử nghiệm <tspan font-weight="bold">Gaussian Mixture Models (GMM)</tspan> để phân cụm mềm (Soft clustering),</text>
    <text x="710" y="455" font-size="13" fill="#1E40AF">cho phép một khách hàng thuộc về nhiều cụm với xác suất cụ thể.</text>
    <text x="695" y="475" font-size="12" fill="#1D4ED8">Thử nghiệm DBSCAN để tự động phát hiện và cô lập các điểm ngoại lệ dị thường.</text>

    <!-- Phase 3 -->
    <rect x="675" y="505" width="510" height="135" rx="10" fill="#FAF5FF" stroke="#E9D5FF"/>
    <text x="695" y="535" font-size="15" font-weight="bold" fill="#7C3AED">GIAI ĐOẠN 3: TỰ ĐỘNG HÓA TIẾP THỊ &amp; GỢI Ý (RECOMMENDER)</text>
    <text x="695" y="562" font-size="13" fill="#334155">• Tích hợp hệ thống Recommendation Engine tự động gợi ý danh mục</text>
    <text x="710" y="585" font-size="13" fill="#6B21A8">hàng hóa cross-sell dựa trên hành vi chi tiêu của từng phân khúc.</text>
    <text x="695" y="615" font-size="12" font-weight="bold" fill="#7C3AED">➔ Biến đồ án học thuật thành giải pháp phần mềm doanh nghiệp thương mại.</text>
  </g>
"""
    return get_svg_wrapper(14, "ĐÁNH GIÁ &amp; ĐỊNH HƯỚNG", "Giới Hạn Nghiên Cứu &amp; Lộ Trình Phát Triển Tương Lai", "Cái nhìn khách quan về phạm vi đề tài và các bước tiến hóa công nghệ tiếp theo", content, page_role="breathing")

# ==============================================================================
# SLIDE 15: CONCLUSION & QA
# ==============================================================================
def gen_slide_15():
    content = """
  <!-- Summary Cards Grid -->
  <g id="conclusion-summary">
    <!-- Top Big Banner -->
    <rect x="70" y="150" width="1140" height="110" rx="14" fill="#1E293B"/>
    <text x="100" y="190" font-size="13" font-weight="bold" fill="#60A5FA" letter-spacing="1">TỔNG KẾT ĐỒ ÁN PROJECT 22</text>
    <text x="100" y="225" font-size="24" font-weight="bold" fill="#FFFFFF">Hoàn Thành Toàn Diện Mục Tiêu Từ Nghiên Cứu Đến Triển Khai Thực Tế</text>
    <text x="100" y="248" font-size="14" fill="#94A3B8">Kết hợp chặt chẽ giữa học thuật chuẩn mực, kỹ thuật chống rò rỉ dữ liệu và kỹ năng công nghệ phần mềm</text>

    <!-- 4 Key Takeaway Cards -->
    <!-- Card 1 -->
    <rect x="70" y="280" width="265" height="195" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
    <rect x="70" y="280" width="265" height="4" rx="2" fill="#2563EB"/>
    <text x="95" y="315" font-size="14" font-weight="bold" fill="#1E40AF">1. CHUẨN MỰC PIPELINE</text>
    <text x="95" y="345" font-size="15" font-weight="bold" fill="#0F172A">Chống Rò Rỉ Tuyệt Đối</text>
    <text x="95" y="375" font-size="13" fill="#334155">• Split 60/20/20 trước khi fit</text>
    <text x="95" y="400" font-size="13" fill="#334155">• log1p nén Skewness 92.6%</text>
    <text x="95" y="425" font-size="13" fill="#334155">• Tập test độc lập đánh giá 1 lần</text>
    <text x="95" y="455" font-size="12" font-weight="bold" fill="#059669">✓ Đạt chuẩn học thuật cao nhất</text>

    <!-- Card 2 -->
    <rect x="360" y="280" width="265" height="195" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
    <rect x="360" y="280" width="265" height="4" rx="2" fill="#10B981"/>
    <text x="385" y="315" font-size="14" font-weight="bold" fill="#065F46">2. K-MEANS TỐI ƯU</text>
    <text x="385" y="345" font-size="15" font-weight="bold" fill="#0F172A">K=2 Cụm Đóng Băng D011</text>
    <text x="385" y="375" font-size="13" fill="#334155">• Silhouette Validation = 0.307</text>
    <text x="385" y="400" font-size="13" fill="#334155">• Độ ổn định ARI 10 seed: 0.997</text>
    <text x="385" y="425" font-size="13" fill="#334155">• Silhouette Test = 0.2389</text>
    <text x="385" y="455" font-size="12" font-weight="bold" fill="#059669">✓ Không phụ thuộc vào seed</text>

    <!-- Card 3 -->
    <rect x="650" y="280" width="265" height="195" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
    <rect x="650" y="280" width="265" height="4" rx="2" fill="#F59E0B"/>
    <text x="675" y="315" font-size="14" font-weight="bold" fill="#92400E">3. Ý NGHĨA KINH DOANH</text>
    <text x="675" y="345" font-size="15" font-weight="bold" fill="#0F172A">2 Chân Dung Khách Hàng</text>
    <text x="675" y="375" font-size="13" fill="#334155">• Cụm 0: Đại siêu thị (Grocery/Milk)</text>
    <text x="675" y="400" font-size="13" fill="#334155">• Cụm 1: Horeca (Fresh/Frozen)</text>
    <text x="675" y="425" font-size="13" fill="#334155">• Tương quan 90% với Channel thật</text>
    <text x="675" y="455" font-size="12" font-weight="bold" fill="#059669">✓ Ứng dụng thực tiễn cao</text>

    <!-- Card 4 -->
    <rect x="940" y="280" width="270" height="195" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
    <rect x="940" y="280" width="270" height="4" rx="2" fill="#8B5CF6"/>
    <text x="965" y="315" font-size="14" font-weight="bold" fill="#6B21A8">4. WEB SERVING</text>
    <text x="965" y="345" font-size="15" font-weight="bold" fill="#0F172A">Kiến Trúc Hoàn Thiện</text>
    <text x="965" y="375" font-size="13" fill="#334155">• Fastify API + React Client</text>
    <text x="965" y="400" font-size="13" fill="#334155">• Model SHA-256 Checksum Guard</text>
    <text x="965" y="425" font-size="13" fill="#334155">• 22/22 Playwright E2E Pass</text>
    <text x="965" y="455" font-size="12" font-weight="bold" fill="#059669">✓ Đạt tiêu chuẩn Production</text>
  </g>

  <!-- Bottom QA Invite Box -->
  <g id="qa-invite">
    <rect x="70" y="495" width="1140" height="165" rx="14" fill="#EFF6FF" stroke="#3B82F6" stroke-width="2"/>
    <text x="100" y="540" font-size="28" font-weight="bold" fill="#1E3A8A">XIN CHÂN THÀNH CẢM ƠN THẦY VÀ CÁC BẠN ĐÃ LẮNG NGHE!</text>
    <text x="100" y="575" font-size="15" fill="#1E40AF">Nhóm kính mời Thầy và Hội đồng đặt câu hỏi và đóng góp ý kiến cho Đồ án Project 22.</text>
    
    <rect x="100" y="600" width="320" height="42" rx="8" fill="#1E40AF"/>
    <text x="260" y="626" font-size="14" font-weight="bold" fill="#FFFFFF" text-anchor="middle">💬 PHIÊN HỎI ĐÁP &amp; THẢO LUẬN (Q&amp;A)</text>

    <text x="750" y="626" font-size="13" fill="#64748B">Source Code &amp; Demo: github.com/... • Project 22 (Wholesale Segmentation)</text>
  </g>
"""
    return get_svg_wrapper(15, "KẾT LUẬN &amp; HỎI ĐÁP", "Tổng Kết Đồ Án &amp; Phiên Trao Đổi (Q&amp;A Session)", "Khẳng định giá trị học thuật, tính ứng dụng thực tiễn và sẵn sàng giải đáp thắc mắc", content, page_role="anchor")

def main():
    generators = [
        ("01_cover.svg", gen_slide_01),
        ("02_problem_objective.svg", gen_slide_02),
        ("03_dataset_features.svg", gen_slide_03),
        ("04_pipeline_leakage.svg", gen_slide_04),
        ("05_preprocessing_comparison.svg", gen_slide_05),
        ("06_elbow_method.svg", gen_slide_06),
        ("07_silhouette_analysis.svg", gen_slide_07),
        ("08_final_model.svg", gen_slide_08),
        ("09_cluster_profiles.svg", gen_slide_09),
        ("10_channel_region.svg", gen_slide_10),
        ("11_tech_stack.svg", gen_slide_11),
        ("12_web_application.svg", gen_slide_12),
        ("13_testing_quality.svg", gen_slide_13),
        ("14_limitations_future.svg", gen_slide_14),
        ("15_conclusion.svg", gen_slide_15),
    ]
    for filename, fn in generators:
        save_svg(filename, fn())
    print("\n[SUCCESS] Generated all 15 high-impact SVG slides.")

if __name__ == "__main__":
    main()
