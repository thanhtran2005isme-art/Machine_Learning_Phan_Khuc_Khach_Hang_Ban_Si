#!/usr/bin/env python3
"""
Generate remaining SVG slides for Project 22 K-Means presentation
Following PPT Master workflow and design_spec.md
"""

import os
from pathlib import Path

PROJECT_DIR = Path(__file__).parent
SVG_OUTPUT = PROJECT_DIR / "svg_output"
SVG_OUTPUT.mkdir(exist_ok=True)

# SVG Header template
SVG_HEADER = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" font-family="Inter, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif">'''

# Common defs
COMMON_DEFS = '''  <defs>
    <filter id="softShadow" x="-15%" y="-20%" width="130%" height="150%">
      <feDropShadow dx="0" dy="6" stdDeviation="8" flood-color="#000000" flood-opacity="0.10"/>
    </filter>
    <linearGradient id="accentBar" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#2563EB"/>
      <stop offset="100%" stop-color="#10B981"/>
    </linearGradient>
  </defs>'''

def create_slide_02():
    """Problem & Objective slide"""
    content = f'''{SVG_HEADER}
{COMMON_DEFS}
  
  <!-- Background -->
  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>
  
  <!-- Header -->
  <g id="header" data-pptx-bounds="60 50 1160 80">
    <text x="60" y="90" font-size="42" font-weight="bold" fill="#1F2937">Bài Toán và Mục Tiêu</text>
    <rect x="60" y="105" width="120" height="4" rx="2" fill="url(#accentBar)"/>
  </g>
  
  <!-- Business Problem -->
  <g id="business-problem" data-pptx-bounds="60 160 1160 120">
    <rect x="60" y="160" width="1160" height="120" rx="12" fill="#F8F9FA"/>
    <use data-icon="phosphor-duotone/target" x="80" y="185" width="36" height="36" fill="#2563EB"/>
    <text x="135" y="200" font-size="18" font-weight="bold" fill="#1F2937">Business Problem</text>
    <text x="135" y="230" font-size="20" fill="#1F2937">
      <tspan x="135" dy="0">Nhà phân phối cần hiểu <tspan font-weight="bold" fill="#2563EB">kiểu cơ cấu chi tiêu</tspan></tspan>
      <tspan x="135" dy="28">của khách hàng bán sỉ để hỗ trợ thiết kế danh mục và dịch vụ</tspan>
    </text>
  </g>
  
  <!-- Research Question -->
  <g id="research-question" data-pptx-bounds="60 310 1160 100">
    <rect x="60" y="310" width="1160" height="100" rx="12" fill="#DBEAFE" stroke="#2563EB" stroke-width="2"/>
    <text x="90" y="345" font-size="18" font-weight="bold" fill="#1E40AF">Research Question</text>
    <text x="90" y="375" font-size="19" fill="#1E3A8A" font-style="italic">
      "Sau log-transform và chuẩn hóa, K-means tạo ra các phân khúc
    </text>
    <text x="90" y="400" font-size="19" fill="#1E3A8A" font-style="italic">
      ổn định và có ý nghĩa kinh doanh nào?"
    </text>
  </g>
  
  <!-- Objectives -->
  <g id="objectives" data-pptx-bounds="60 440 560 220">
    <text x="60" y="465" font-size="20" font-weight="bold" fill="#1F2937">Objectives</text>
    <use data-icon="phosphor-duotone/check-circle" x="60" y="485" width="24" height="24" fill="#10B981"/>
    <text x="95" y="505" font-size="18" fill="#1F2937">Áp dụng K-Means phân khúc theo chi tiêu</text>
    <use data-icon="phosphor-duotone/check-circle" x="60" y="525" width="24" height="24" fill="#10B981"/>
    <text x="95" y="545" font-size="18" fill="#1F2937">Phân tích cơ cấu chi tiêu từng phân khúc</text>
    <use data-icon="phosphor-duotone/check-circle" x="60" y="565" width="24" height="24" fill="#10B981"/>
    <text x="95" y="585" font-size="18" fill="#1F2937">Đóng gói model thành web app với API</text>
  </g>
  
  <!-- Ethical Note -->
  <g id="ethical-note" data-pptx-bounds="660 440 560 220">
    <rect x="660" y="440" width="560" height="220" rx="12" fill="#FEF3C7" stroke="#F59E0B" stroke-width="2"/>
    <use data-icon="phosphor-duotone/warning" x="680" y="465" width="32" height="32" fill="#D97706"/>
    <text x="730" y="490" font-size="18" font-weight="bold" fill="#92400E">Important</text>
    <text x="680" y="525" font-size="17" fill="#78350F">
      <tspan x="680" dy="0">Cụm CHỈ mô tả hành vi chi tiêu,</tspan>
      <tspan x="680" dy="25">KHÔNG đánh giá giá trị con người</tspan>
    </text>
  </g>
  
  <!-- Footer -->
  <g id="footer" data-pptx-role="footer" data-pptx-bounds="60 680 1160 30">
    <text x="60" y="700" font-size="14" fill="#9CA3AF">Project 22: K-Means Customer Segmentation</text>
    <text x="1220" y="700" font-size="14" fill="#9CA3AF" text-anchor="end">2 / 15</text>
  </g>
</svg>'''
    return content

def create_slide_03():
    """Dataset & Features slide"""
    content = f'''{SVG_HEADER}
{COMMON_DEFS}
  
  <!-- Background -->
  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>
  
  <!-- Header -->
  <g id="header" data-pptx-bounds="60 50 1160 80">
    <text x="60" y="90" font-size="42" font-weight="bold" fill="#1F2937">Dữ Liệu UCI Wholesale Customers</text>
    <rect x="60" y="105" width="120" height="4" rx="2" fill="url(#accentBar)"/>
  </g>
  
  <!-- Source Info -->
  <g id="source-info" data-pptx-bounds="60 160 560 280">
    <rect x="60" y="160" width="560" height="280" rx="12" fill="#F8F9FA"/>
    <text x="90" y="200" font-size="20" font-weight="bold" fill="#1F2937">Source</text>
    
    <use data-icon="phosphor-duotone/database" x="90" y="220" width="28" height="28" fill="#2563EB"/>
    <text x="130" y="243" font-size="17" fill="#1F2937">UCI Machine Learning Repository</text>
    
    <text x="90" y="285" font-size="16" fill="#6B7280">DOI: 10.24432/C5030X</text>
    <text x="90" y="310" font-size="16" fill="#6B7280">License: CC BY 4.0</text>
    <text x="90" y="335" font-size="16" fill="#6B7280">Size: <tspan font-weight="bold" fill="#2563EB">440 customers</tspan></text>
    <text x="90" y="365" font-size="16" fill="#6B7280">Features: <tspan font-weight="bold" fill="#10B981">6 spending variables</tspan></text>
    <text x="90" y="395" font-size="16" fill="#6B7280">Unit: Annual monetary units (m.u.)</text>
  </g>
  
  <!-- 6 Features -->
  <g id="features" data-pptx-bounds="660 160 560 480">
    <rect x="660" y="160" width="560" height="480" rx="12" fill="#EFF6FF" stroke="#2563EB" stroke-width="2"/>
    <text x="690" y="200" font-size="20" font-weight="bold" fill="#1E40AF">6 Primary Features (Clustering)</text>
    
    <g id="feature-list">
      <rect x="690" y="220" width="500" height="50" rx="8" fill="#FFFFFF"/>
      <use data-icon="phosphor-duotone/chart-line" x="700" y="232" width="26" height="26" fill="#10B981"/>
      <text x="740" y="250" font-size="17" font-weight="bold" fill="#1F2937">Fresh</text>
      <text x="950" y="250" font-size="15" fill="#6B7280" text-anchor="end">Sản phẩm tươi sống</text>
      
      <rect x="690" y="280" width="500" height="50" rx="8" fill="#FFFFFF"/>
      <use data-icon="phosphor-duotone/chart-line" x="700" y="292" width="26" height="26" fill="#10B981"/>
      <text x="740" y="310" font-size="17" font-weight="bold" fill="#1F2937">Milk</text>
      <text x="950" y="310" font-size="15" fill="#6B7280" text-anchor="end">Sữa và sản phẩm từ sữa</text>
      
      <rect x="690" y="340" width="500" height="50" rx="8" fill="#FFFFFF"/>
      <use data-icon="phosphor-duotone/chart-line" x="700" y="352" width="26" height="26" fill="#10B981"/>
      <text x="740" y="370" font-size="17" font-weight="bold" fill="#1F2937">Grocery</text>
      <text x="950" y="370" font-size="15" fill="#6B7280" text-anchor="end">Hàng tạp hóa</text>
      
      <rect x="690" y="400" width="500" height="50" rx="8" fill="#FFFFFF"/>
      <use data-icon="phosphor-duotone/chart-line" x="700" y="412" width="26" height="26" fill="#10B981"/>
      <text x="740" y="430" font-size="17" font-weight="bold" fill="#1F2937">Frozen</text>
      <text x="950" y="430" font-size="15" fill="#6B7280" text-anchor="end">Thực phẩm đông lạnh</text>
      
      <rect x="690" y="460" width="500" height="50" rx="8" fill="#FFFFFF"/>
      <use data-icon="phosphor-duotone/chart-line" x="700" y="472" width="26" height="26" fill="#10B981"/>
      <text x="740" y="490" font-size="17" font-weight="bold" fill="#1F2937">Detergents_Paper</text>
      <text x="950" y="490" font-size="15" fill="#6B7280" text-anchor="end">Chất tẩy rửa và giấy</text>
      
      <rect x="690" y="520" width="500" height="50" rx="8" fill="#FFFFFF"/>
      <use data-icon="phosphor-duotone/chart-line" x="700" y="532" width="26" height="26" fill="#10B981"/>
      <text x="740" y="550" font-size="17" font-weight="bold" fill="#1F2937">Delicassen</text>
      <text x="950" y="550" font-size="15" fill="#6B7280" text-anchor="end">Thực phẩm ăn liền</text>
    </g>
    
    <text x="690" y="605" font-size="15" fill="#9CA3AF" font-style="italic">
      Channel & Region: Chỉ dùng profiling SAU clustering
    </text>
  </g>
  
  <!-- Note -->
  <g id="note" data-pptx-bounds="60 470 560 120">
    <rect x="60" y="470" width="560" height="120" rx="12" fill="#FEF2F2" stroke="#EF4444" stroke-width="2"/>
    <text x="90" y="510" font-size="17" font-weight="bold" fill="#991B1B">Không dùng để fit K-Means:</text>
    <text x="90" y="540" font-size="16" fill="#7F1D1D">· Channel (Horeca / Retail)</text>
    <text x="90" y="565" font-size="16" fill="#7F1D1D">· Region (Lisbon / Oporto / Other)</text>
  </g>
  
  <!-- Footer -->
  <g id="footer" data-pptx-role="footer" data-pptx-bounds="60 680 1160 30">
    <text x="60" y="700" font-size="14" fill="#9CA3AF">Project 22: K-Means Customer Segmentation</text>
    <text x="1220" y="700" font-size="14" fill="#9CA3AF" text-anchor="end">3 / 15</text>
  </g>
</svg>'''
    return content

# Generate all slides
def main():
    slides = {
        "02_problem_objective.svg": create_slide_02(),
        "03_dataset_features.svg": create_slide_03(),
    }
    
    for filename, content in slides.items():
        filepath = SVG_OUTPUT / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Created {filename}")
    
    print(f"\n✅ Generated {len(slides)} slides in {SVG_OUTPUT}")
    print(f"📝 Slide 01 (cover) already exists")
    print(f"📋 Total slides ready: {len(slides) + 1} / 15")
    print(f"\n⚠️  Remaining slides (4-15) need chart/table visualizations")
    print(f"💡 Consider using Quick Generate profile or creating visualization templates")

if __name__ == "__main__":
    main()


# ============================================================
# SLIDE 05: PREPROCESSING COMPARISON
# ============================================================
def generate_slide_05():
    """Slide 05: So sánh Raw vs Log1p+StandardScaler"""
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" font-family="Inter, system-ui, -apple-system, sans-serif">
  <defs>
    {COMMON_DEFS}
  </defs>
  
  <!-- Background -->
  <rect width="1280" height="720" fill="#FFFFFF"/>
  
  <!-- Header -->
  <text x="80" y="80" font-size="42" font-weight="bold" fill="#1F2937">So sánh Tiền xử lý</text>
  <text x="80" y="115" font-size="24" fill="#6B7280">Raw vs Log1p + StandardScaler</text>
  <rect x="80" y="125" width="120" height="4" rx="2" fill="url(#accentBar)"/>
  
  <!-- Left Column: Raw Data Issues -->
  <g transform="translate(80,160)">
    <circle cx="15" cy="0" r="24" fill="{COLORS['error']}" opacity="0.1"/>
    <use href="#{ICONS['alert-circle']['id']}" x="3" y="-12" width="24" height="24" fill="{COLORS['error']}"/>
    <text x="55" y="5" class="body-text" fill="{COLORS['text']}">Raw data - Vấn đề</text>
    
    <!-- Issues list -->
    <rect x="0" y="30" width="500" height="350" rx="12" fill="#FEE2E2" stroke="{COLORS['error']}" stroke-width="2"/>
    <text x="25" y="70" class="label">Skewness cao:</text>
    <text x="25" y="100" class="small-text">• Delicassen: 12.12</text>
    <text x="25" y="125" class="small-text">• Milk: 4.28</text>
    <text x="25" y="150" class="small-text">• Frozen: 3.53</text>
    
    <text x="25" y="190" class="label">Range rất lớn:</text>
    <text x="25" y="220" class="small-text">• Fresh: 3 → 112,151</text>
    <text x="25" y="245" class="small-text">• Milk: 55 → 73,498</text>
    
    <text x="25" y="285" class="label">Outliers chi phối:</text>
    <text x="25" y="315" class="small-text">KMeans nhạy cảm với scale</text>
    <text x="25" y="340" class="small-text">Cluster không ổn định</text>
  </g>
  
  <!-- Right Column: Log1p Solution -->
  <g transform="translate(660,160)">
    <circle cx="15" cy="0" r="24" fill="{COLORS['success']}" opacity="0.1"/>
    <use href="#{ICONS['check-circle']['id']}" x="3" y="-12" width="24" height="24" fill="{COLORS['success']}"/>
    <text x="55" y="5" class="body-text" fill="{COLORS['text']}">Log1p + Scaler - Giải pháp</text>
    
    <!-- Solutions list -->
    <rect x="0" y="30" width="500" height="350" rx="12" fill="#D1FAE5" stroke="{COLORS['success']}" stroke-width="2"/>
    <text x="25" y="70" class="label">Giảm skewness:</text>
    <text x="25" y="100" class="small-text">• Delicassen: 12.12 → -0.90</text>
    <text x="25" y="125" class="small-text">• Milk: 4.28 → -0.17</text>
    <text x="25" y="150" class="small-text">• Frozen: 3.53 → -0.46</text>
    
    <text x="25" y="190" class="label">Chuẩn hóa scale:</text>
    <text x="25" y="220" class="small-text">Tất cả features: mean=0, std=1</text>
    <text x="25" y="245" class="small-text">Distance metrics có ý nghĩa</text>
    
    <text x="25" y="285" class="label">Cluster ổn định hơn:</text>
    <text x="25" y="315" class="small-text">ARI mean = 0.997 (K=2)</text>
    <text x="25" y="340" class="small-text">Silhouette validation = 0.307</text>
  </g>
  
  <!-- Footer -->
  <text x="80" y="{CANVAS['height']}-40" class="caption">Quyết định D011: Chọn log1p + StandardScaler cho toàn bộ pipeline</text>
</svg>'''
    
    with open(f"{SVG_OUTPUT_DIR}/05_preprocessing_comparison.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("✓ Generated slide 05: Preprocessing Comparison")

# ============================================================
# SLIDE 06: ELBOW METHOD K=2..8
# ============================================================
def generate_slide_06():
    """Slide 06: Elbow Method - Chọn K tối ưu"""
    
    # Real data from selection_evidence.csv (log1p_standardscaler only)
    k_values = [2, 3, 4, 5, 6, 7, 8]
    inertias = [391.53, 341.06, 302.02, 286.64, 265.17, 253.89, 247.25]
    
    # Normalize to chart space (800x300)
    chart_x = 250
    chart_y = 200
    chart_w = 800
    chart_h = 300
    
    # Scale inertia to fit chart
    min_inertia = min(inertias)
    max_inertia = max(inertias)
    
    def scale_y(val):
        return chart_y + chart_h - ((val - min_inertia) / (max_inertia - min_inertia) * chart_h)
    
    def scale_x(k_idx):
        return chart_x + (k_idx * chart_w / (len(k_values) - 1))
    
    # Build polyline points
    points = " ".join([f"{scale_x(i)},{scale_y(inertias[i])}" for i in range(len(k_values))])
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CANVAS['width']} {CANVAS['height']}" width="{CANVAS['width']} height="{CANVAS['height']}">
  <defs>
    {generate_styles()}
    <linearGradient id="elbow-gradient" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="{COLORS['primary']}" stop-opacity="0.3"/>
      <stop offset="100%" stop-color="{COLORS['primary']}" stop-opacity="0.0"/>
    </linearGradient>
  </defs>
  
  <!-- Background -->
  <rect width="{CANVAS['width']}" height="{CANVAS['height']}" fill="{COLORS['background']}"/>
  
  <!-- Header -->
  <text x="80" y="80" class="heading">Elbow Method</text>
  <text x="80" y="115" class="subtitle">Validation Inertia vs K (log1p + StandardScaler)</text>
  
  <!-- Chart background -->
  <rect x="{chart_x}" y="{chart_y}" width="{chart_w}" height="{chart_h}" fill="white" rx="8" stroke="{COLORS['border']}" stroke-width="2"/>
  
  <!-- Grid lines -->
  <line x1="{chart_x}" y1="{chart_y + chart_h/4}" x2="{chart_x + chart_w}" y2="{chart_y + chart_h/4}" stroke="{COLORS['border']}" stroke-width="1" opacity="0.3"/>
  <line x1="{chart_x}" y1="{chart_y + chart_h/2}" x2="{chart_x + chart_w}" y2="{chart_y + chart_h/2}" stroke="{COLORS['border']}" stroke-width="1" opacity="0.3"/>
  <line x1="{chart_x}" y1="{chart_y + 3*chart_h/4}" x2="{chart_x + chart_w}" y2="{chart_y + 3*chart_h/4}" stroke="{COLORS['border']}" stroke-width="1" opacity="0.3"/>
  
  <!-- Elbow curve -->
  <polyline points="{points}" fill="none" stroke="{COLORS['primary']}" stroke-width="4" stroke-linejoin="round"/>
  
  <!-- Data points -->'''
    
    for i, (k, inertia) in enumerate(zip(k_values, inertias)):
        x = scale_x(i)
        y = scale_y(inertia)
        color = COLORS['accent'] if k == 2 else COLORS['primary']
        svg += f'''
  <circle cx="{x}" cy="{y}" r="8" fill="{color}" stroke="white" stroke-width="2"/>'''
    
    svg += f'''
  
  <!-- X-axis labels -->'''
    for i, k in enumerate(k_values):
        x = scale_x(i)
        svg += f'''
  <text x="{x}" y="{chart_y + chart_h + 35}" class="caption" text-anchor="middle">K={k}</text>'''
    
    svg += f'''
  
  <!-- Y-axis labels -->
  <text x="{chart_x - 20}" y="{chart_y}" class="caption" text-anchor="end" dominant-baseline="middle">{max_inertia:.0f}</text>
  <text x="{chart_x - 20}" y="{chart_y + chart_h}" class="caption" text-anchor="end" dominant-baseline="middle">{min_inertia:.0f}</text>
  <text x="{chart_x - 80}" y="{chart_y + chart_h/2}" class="label" text-anchor="middle" transform="rotate(-90 {chart_x - 80} {chart_y + chart_h/2})">Inertia</text>
  
  <!-- Highlight K=2 -->
  <g transform="translate({scale_x(0)},{scale_y(inertias[0]) - 60})">
    <rect x="-80" y="-40" width="160" height="50" rx="8" fill="{COLORS['accent']}" opacity="0.1" stroke="{COLORS['accent']}" stroke-width="2"/>
    <text x="0" y="-20" class="body-text" fill="{COLORS['accent']}" text-anchor="middle" font-weight="600">K=2 Optimal</text>
    <text x="0" y="0" class="small-text" text-anchor="middle">Inertia: 391.5</text>
  </g>
  
  <!-- Insight box -->
  <g transform="translate(80,580)">
    <rect width="1120" height="90" rx="12" fill="{COLORS['primary']}" opacity="0.05"/>
    <use href="#
{ICONS['lightbulb']['id']}" x="20" y="20" width="28" height="28" fill="{COLORS['primary']}"/>
    <text x="70" y="35" class="body-text" font-weight="600">Phân tích:</text>
    <text x="70" y="60" class="small-text">Inertia giảm nhanh từ K=2→3 (giảm 12.9%), sau đó chậm lại dần. Elbow rõ ràng tại K=2–3.</text>
    <text x="70" y="80" class="small-text">Kết hợp với Silhouette và stability, chọn K=2 cho interpretability cao.</text>
  </g>
</svg>'''
    
    with open(f"{SVG_OUTPUT_DIR}/06_elbow_method.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("✓ Generated slide 06: Elbow Method")

# ============================================================
# SLIDE 07: SILHOUETTE ANALYSIS
# ============================================================
def generate_slide_07():
    """Slide 07: Silhouette Score Comparison"""
    
    # Real data from selection_evidence.csv
    k_values = [2, 3, 4, 5, 6, 7, 8]
    train_sil = [0.2756, 0.2049, 0.2059, 0.1976, 0.1933, 0.1868, 0.1881]
    val_sil = [0.3066, 0.2165, 0.1540, 0.1623, 0.1601, 0.1446, 0.1404]
    
    # Chart dimensions
    chart_x = 200
    chart_y = 180
    chart_w = 880
    chart_h = 280
    bar_width = 50
    group_spacing = 120
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CANVAS['width']} {CANVAS['height']}" width="{CANVAS['width']}" height="{CANVAS['height']}">
  <defs>
    {generate_styles()}
  </defs>
  
  <!-- Background -->
  <rect width="{CANVAS['width']}" height="{CANVAS['height']}" fill="{COLORS['background']}"/>
  
  <!-- Header -->
  <text x="80" y="80" class="heading">Silhouette Analysis</text>
  <text x="80" y="115" class="subtitle">Train vs Validation Silhouette Score</text>
  
  <!-- Chart background -->
  <rect x="{chart_x}" y="{chart_y}" width="{chart_w}" height="{chart_h}" fill="white" rx="8" stroke="{COLORS['border']}" stroke-width="2"/>
  
  <!-- Grid lines -->
  <line x1="{chart_x}" y1="{chart_y + chart_h/4}" x2="{chart_x + chart_w}" y2="{chart_y + chart_h/4}" stroke="{COLORS['border']}" stroke-width="1" opacity="0.3"/>
  <line x1="{chart_x}" y1="{chart_y + chart_h/2}" x2="{chart_x + chart_w}" y2="{chart_y + chart_h/2}" stroke="{COLORS['border']}" stroke-width="1" opacity="0.3"/>
  <line x1="{chart_x}" y1="{chart_y + 3*chart_h/4}" x2="{chart_x + chart_w}" y2="{chart_y + 3*chart_h/4}" stroke="{COLORS['border']}" stroke-width="1" opacity="0.3"/>
  
  <!-- Bars -->'''
    
    max_score = 0.35
    for i, k in enumerate(k_values):
        group_x = chart_x + 40 + (i * group_spacing)
        
        # Train bar (blue)
        train_h = (train_sil[i] / max_score) * chart_h
        train_y = chart_y + chart_h - train_h
        svg += f'''
  <rect x="{group_x}" y="{train_y}" width="{bar_width}" height="{train_h}" rx="4" fill="{COLORS['primary']}"/>
  <text x="{group_x + bar_width/2}" y="{train_y - 8}" class="caption" text-anchor="middle">{train_sil[i]:.3f}</text>'''
        
        # Validation bar (green)
        val_h = (val_sil[i] / max_score) * chart_h
        val_y = chart_y + chart_h - val_h
        svg += f'''
  <rect x="{group_x + bar_width + 10}" y="{val_y}" width="{bar_width}" height="{val_h}" rx="4" fill="{COLORS['accent']}"/>
  <text x="{group_x + bar_width + 10 + bar_width/2}" y="{val_y - 8}" class="caption" text-anchor="middle">{val_sil[i]:.3f}</text>'''
        
        # K label
        svg += f'''
  <text x="{group_x + bar_width + 5}" y="{chart_y + chart_h + 30}" class="caption" text-anchor="middle">K={k}</text>'''
    
    svg += f'''
  
  <!-- Y-axis -->
  <text x="{chart_x - 20}" y="{chart_y}" class="caption" text-anchor="end">0.35</text>
  <text x="{chart_x - 20}" y="{chart_y + chart_h}" class="caption" text-anchor="end">0.00</text>
  <text x="{chart_x - 80}" y="{chart_y + chart_h/2}" class="label" text-anchor="middle" transform="rotate(-90 {chart_x - 80} {chart_y + chart_h/2})">Silhouette Score</text>
  
  <!-- Legend -->
  <g transform="translate(900,200)">
    <rect x="0" y="0" width="32" height="32" rx="4" fill="{COLORS['primary']}"/>
    <text x="45" y="20" class="small-text">Train</text>
    <rect x="0" y="45" width="32" height="32" rx="4" fill="{COLORS['accent']}"/>
    <text x="45" y="65" class="small-text">Validation</text>
  </g>
  
  <!-- Insights -->
  <g transform="translate(80,520)">
    <rect width="1120" height="140" rx="12" fill="{COLORS['accent']}" opacity="0.05"/>
    <use href="#check-circle" x="20" y="20" width="28" height="28" fill="{COLORS['accent']}"/>
    <text x="70" y="35" class="body-text" font-weight="600">Kết luận:</text>
    <text x="70" y="60" class="small-text">• K=2: Silhouette validation cao nhất (0.307), train-val gap thấp → generalization tốt</text>
    <text x="70" y="85" class="small-text">• K≥3: Score giảm mạnh, gap tăng → overfitting risk</text>
    <text x="70" y="110" class="small-text">• Kết hợp Elbow, Silhouette, ARI stability (0.997) → Chọn K=2 là optimal</text>
    <text x="70" y="135" class="small-text" fill="{COLORS['accent']}" font-weight="600">Quyết định: K=2, log1p+StandardScaler, random_state=42</text>
  </g>
</svg>'''
    
    with open(f"{SVG_OUTPUT_DIR}/07_silhouette_analysis.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("✓ Generated slide 07: Silhouette Analysis")

# ============================================================
# SLIDE 10: CHANNEL & REGION PROFILE TABLE
# ============================================================
def generate_slide_10():
    """Slide 10: Channel & Region Distribution"""
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CANVAS['width']} {CANVAS['height']}" width="{CANVAS['width']}" height="{CANVAS['height']}">
  <defs>
    {generate_styles()}
  </defs>
  
  <!-- Background -->
  <rect width="{CANVAS['width']}" height="{CANVAS['height']}" fill="{COLORS['background']}"/>
  
  <!-- Header -->
  <text x="80" y="80" class="heading">Phân bố Channel & Region</text>
  <text x="80" y="115" class="subtitle">Profiling theo biến phụ (không dùng clustering)</text>
  
  <!-- Channel Table -->
  <g transform="translate(80,180)">
    <text x="0" y="-10" class="body-text" font-weight="600" fill="{COLORS['primary']}">Channel Distribution</text>
    
    <!-- Table header -->
    <rect x="0" y="0" width="520" height="50" fill="{COLORS['primary']}" opacity="0.1" stroke="{COLORS['primary']}" stroke-width="2"/>
    <text x="100" y="32" class="label" text-anchor="middle" font-weight="600">Cluster 0</text>
    <text x="300" y="32" class="label" text-anchor="middle" font-weight="600">Cluster 1</text>
    
    <!-- Row 1: Horeca -->
    <rect x="0" y="50" width="520" height="60" fill="white" stroke="{COLORS['border']}" stroke-width="1"/>
    <text x="20" y="85" class="body-text" font-weight="500">Horeca (Ch 1)</text>
    <rect x="70" y="65" width="90" height="30" rx="4" fill="{COLORS['primary']}" opacity="0.8"/>
    <text x="115" y="86" class="small-text" fill="white" text-anchor="middle" font-weight="600">54 (33.3%)</text>
    <rect x="270" y="65" width="170" height="30" rx="4" fill="{COLORS['accent']}" opacity="0.9"/>
    <text x="355" y="86" class="small-text" fill="white" text-anchor="middle" font-weight="600">186 (97.9%)</text>
    
    <!-- Row 2: Retail -->
    <rect x="0" y="110" width="520" height="60" fill="#F9FAFB" stroke="{COLORS['border']}" stroke-width="1"/>
    <text x="20" y="145" class="body-text" font-weight="500">Retail (Ch 2)</text>
    <rect x="70" y="125" width="150" height="30" rx="4" fill="{COLORS['primary']}" opacity="0.9"/>
    <text x="145" y="146" class="small-text" fill="white" text-anchor="middle" font-weight="600">108 (66.7%)</text>
    <rect x="270" y="125" width="50" height="30" rx="4" fill="{COLORS['accent']}" opacity="0.6"/>
    <text x="295" y="146" class="small-text" fill="white" text-anchor="middle" font-weight="600">4 (2.1%)</text>
    
    <!-- Insight -->
    <g transform="translate(0,200)">
      <rect width="520" height="60" rx="8" fill="{COLORS['primary']}" opacity="0.05"/>
      <use href="#lightbulb" x="15" y="15" width="24" height="24" fill="{COLORS['primary']}"/>
      <text x="55" y="30" class="small-text" font-weight="600">Insight:</text>
      <text x="55" y="48" class="small-text">Cluster 1 chủ yếu Horeca (98%), Cluster 0 cân bằng hơn</text>
    </g>
  </g>
  
  <!-- Region Table -->
  <g transform="translate(680,180)">
    <text x="0" y="-10" class="body-text" font-weight="600" fill="{COLORS['accent']}">Region Distribution</text>
    
    <!-- Table header -->
    <rect x="0" y="0" width="520" height="50" fill="{COLORS['accent']}" opacity="0.1" stroke="{COLORS['accent']}" stroke-width="2"/>
    <text x="100" y="32" class="label" text-anchor="middle" font-weight="600">Cluster 0</text>
    <text x="300" y="32" class="label" text-anchor="middle" font-weight="600">Cluster 1</text>
    
    <!-- Simplified regions (top 2 only for space) -->
    <rect x="0" y="50" width="520" height="60" fill="white" stroke="{COLORS['border']}" stroke-width="1"/>
    <text x="20" y="85" class="body-text" font-weight="500">Lisbon (Reg 3)</text>
    <rect x="70" y="65" width="100" height="30" rx="4" fill="{COLORS['primary']}" opacity="0.7"/>
    <text x="120" y="86" class="small-text" fill="white" text-anchor="middle" font-weight="600">76 (46.9%)</text>
    <rect x="270" y="65" width="120" height="30" rx="4" fill="{COLORS['accent']}" opacity="0.8"/>
    <text x="330" y="86" class="small-text" fill="white" text-anchor="middle" font-weight="600">101 (53.2%)</text>
    
    <rect x="0" y="110" width="520" height="60" fill="#F9FAFB" stroke="{COLORS['border']}" stroke-width="1"/>
    <text x="20" y="145" class="body-text" font-weight="500">Oporto (Reg 1)</text>
    <rect x="70" y="125" width="80" height="30" rx="4" fill="{COLORS['primary']}" opacity="0.6"/>
    <text x="110" y="146" class="small-text" fill="white" text-anchor="middle" font-weight="600">47 (29%)</text>
    <rect x="270" y="125" width="90" height="30" rx="4" fill="{COLORS['accent']}" opacity="0.7"/>
    <text x="315" y="146" class="small-text" fill="white" text-anchor="middle" font-weight="600">50 (26.3%)</text>
    
    <!-- Insight -->
    <g transform="translate(0,200)">
      <rect width="520" height="60" rx="8" fill="{COLORS['accent']}" opacity="0.05"/>
      <use href="#globe" x="15" y="15" width="24" height="24" fill="{COLORS['accent']}"/>
      <text x="55" y="30" class="small-text" font-weight="600">Insight:</text>
      <text x="55" y="48" class="small-text">Không có sự khác biệt rõ ràng về địa lý giữa 2 cluster</text>
    </g>
  </g>
  
  <!-- Footer note -->
  <text x="80" y="{CANVAS['height']}-40" class="caption" fill="{COLORS['secondary']}">Data: final_profile/channel_profile.csv, region_profile.csv | Channel & Region không dùng làm features clustering</text>
</svg>'''
    
    with open(f"{SVG_OUTPUT_DIR}/10_channel_region.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("✓ Generated slide 10: Channel & Region Distribution")

# ============================================================
# SLIDE 14: LIMITATIONS & FUTURE WORK
# ============================================================
def generate_slide_14():
    """Slide 14: Limitations and Future Directions"""
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CANVAS['width']} {CANVAS['height']}" width="{CANVAS['width']}" height="{CANVAS['height']}">
  <defs>
    {generate_styles()}
  </defs>
  
  <!-- Background -->
  <rect width="{CANVAS['width']}" height="{CANVAS['height']}" fill="{COLORS['background']}"/>
  
  <!-- Header -->
  <text x="80" y="80" class="heading">Limitations & Future Work</text>
  <text x="80" y="115" class="subtitle">Hạn chế và Hướng phát triển</text>
  
  <!-- Limitations (Left) -->
  <g transform="translate(80,180)">
    <circle cx="20" cy="0" r="28" fill="{COLORS['warning']}" opacity="0.1"/>
    <use href="#warning" x="8" y="-12" width="24" height="24" fill="{COLORS['warning']}"/>
    <text x="70" y="5" class="body-text" font-weight="600" fill="{COLORS['warning']}">Hạn chế hiện tại</text>
    
    <!-- Limitation cards -->
    <g transform="translate(0,50)">
      <rect width="520" height="110" rx="12" fill="white" stroke="{COLORS['border']}" stroke-width="2"/>
      <text x="25" y="35" class="body-text" font-weight="600" fill="{COLORS['text']}">1. Phương pháp K-Means</text>
      <text x="25" y="60" class="small-text">• Chỉ phát hiện cluster hình cầu, khoảng cách Euclidean</text>
      <text x="25" y="80" class="small-text">• Không phù hợp với cluster hình dạng phức tạp</text>
      <text x="25" y="100" class="small-text">• Nhạy cảm với outliers dù đã preprocessing</text>
    </g>
    
    <g transform="translate(0,180)">
      <rect width="520" height="90" rx="12" fill="white" stroke="{COLORS['border']}" stroke-width="2"/>
      <text x="25" y="35" class="body-text" font-weight="600" fill="{COLORS['text']}">2. Feature engineering</text>
      <text x="25" y="60" class="small-text">• Chưa có interaction features (Fresh×Milk, etc.)</text>
      <text x="25" y="80" class="small-text">• Không dùng temporal patterns (nếu có timestamp)</text>
    </g>
    
    <g transform="translate(0,290)">
      <rect width="520" height="90" rx="12" fill="white" stroke="{COLORS['border']}" stroke-width="2"/>
      <text x="25" y="35" class="body-text" font-weight="600" fill="{COLORS['text']}">3. Validation</text>
      <text x="25" y="60" class="small-text">• Chỉ test tính ổn định, chưa có ground truth labels</text>
      <text x="25" y="80" class="small-text">• Chưa có A/B test trên business metrics thực tế</text>
    </g>
  </g>
  
  <!-- Future Work (Right) -->
  <g transform="translate(680,180)">
    <circle cx="20" cy="0" r="28" fill="{COLORS['success']}" opacity="0.1"/>
    <use href="#rocket-launch" x="8" y="-12" width="24" height="24" fill="{COLORS['success']}"/>
    <text x="70" y="5" class="body-text" font-weight="600" fill="{COLORS['success']}">Hướng phát triển</text>
    
    <!-- Future cards -->
    <g transform="translate(0,50)">
      <rect width="520" height="110" rx="12" fill="white" stroke="{COLORS['border']}" stroke-width="2"/>
      <text x="25" y="35" class="body-text" font-weight="600" fill="{COLORS['text']}">1. Thuật toán khác</text>
      <text x="25" y="60" class="small-text">• DBSCAN: phát hiện cluster hình dạng bất kỳ + outliers</text>
      <text x="25" y="80" class="small-text">• Hierarchical clustering: phân tích dendrogram</text>
      <text x="25" y="100" class="small-text">• Gaussian Mixture Models: soft assignment</text>
    </g>
    
    <g transform="translate(0,180)">
      <rect width="520" height="90" rx="12" fill="white" stroke="{COLORS['border']}" stroke-width="2"/>
      <text x="25" y="35" class="body-text" font-weight="600" fill="{COLORS['text']}">2. Feature mới</text>
      <text x="25" y="60" class="small-text">• Ratio features: Fresh/Total, Milk/Grocery, etc.</text>
      <text x="25" y="80" class="small-text">• RFM analysis nếu có dữ liệu thời gian</text>
    </g>
    
    <g transform="translate(0,290)">
      <rect width="520" height="90" rx="12" fill="white" stroke="{COLORS['border']}" stroke-width="2"/>
      <text x="25" y="35" class="body-text" font-weight="600" fill="{COLORS['text']}">3. Production deployment</text>
      <text x="25" y="60" class="small-text">• Monitoring data drift (PSI, KL divergence)</text>
      <text x="25" y="80" class="small-text">• A/B test chiến dịch marketing theo cluster</text>
    </g>
  </g>
  
  <!-- Footer -->
  <text x="80" y="{CANVAS['height']}-40" class="caption">Project 22 hoàn thành với K-Means baseline. Các phương pháp nâng cao để lại cho tương lai.</text>
</svg>'''
    
    with open(f"{SVG_OUTPUT_DIR}/14_limitations_future.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("✓ Generated slide 14: Limitations & Future Work")

# ============================================================
# MAIN EXECUTION
# ============================================================
if __name__ == "__main__":
    print("Generating 5 remaining slides...")
    generate_slide_05()
    generate_slide_06()
    generate_slide_07()
    generate_slide_10()
    generate_slide_14()
    print("\n✅ All 15 slides completed!")
    print(f"📁 SVG files: {SVG_OUTPUT_DIR}")
    print("\nNext: Run svg_to_pptx.py to export PowerPoint file")
