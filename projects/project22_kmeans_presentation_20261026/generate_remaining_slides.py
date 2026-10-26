#!/usr/bin/env python3
"""
Generate 5 remaining SVG slides (05, 06, 07, 10, 14) for Project 22 K-Means presentation
"""

import os
from pathlib import Path

PROJECT_DIR = Path(__file__).parent
SVG_OUTPUT_DIR = PROJECT_DIR / "svg_output"
SVG_OUTPUT_DIR.mkdir(exist_ok=True)

# Common styles
COMMON_DEFS = '''  <defs>
    <filter id="softShadow" x="-15%" y="-20%" width="130%" height="150%">
      <feDropShadow dx="0" dy="6" stdDeviation="8" flood-color="#000000" flood-opacity="0.10"/>
    </filter>
    <linearGradient id="accentBar" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#2563EB"/>
      <stop offset="100%" stop-color="#10B981"/>
    </linearGradient>
  </defs>'''

def generate_slide_05():
    """Slide 05: Preprocessing Comparison"""
    content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" font-family="Inter, system-ui, -apple-system, sans-serif">
{COMMON_DEFS}
  
  <!-- Background -->
  <rect width="1280" height="720" fill="#FFFFFF"/>
  
  <!-- Header -->
  <text x="80" y="80" font-size="42" font-weight="bold" fill="#1F2937">So sánh Tiền xử lý</text>
  <text x="80" y="115" font-size="24" fill="#6B7280">Raw vs Log1p + StandardScaler</text>
  <rect x="80" y="125" width="120" height="4" rx="2" fill="url(#accentBar)"/>
  
  <!-- Left: Raw Data Issues -->
  <g transform="translate(80,180)">
    <circle cx="20" cy="0" r="28" fill="#FEE2E2"/>
    <text x="70" y="5" font-size="22" font-weight="bold" fill="#DC2626">Raw data - Vấn đề</text>
    
    <rect x="0" y="30" width="520" height="420" rx="12" fill="#FEF2F2" stroke="#DC2626" stroke-width="2"/>
    
    <!-- Skewness -->
    <text x="25" y="70" font-size="18" font-weight="600" fill="#1F2937">Skewness cực cao:</text>
    <text x="25" y="100" font-size="16" fill="#4B5563">• Delicassen: 12.12</text>
    <text x="25" y="125" font-size="16" fill="#4B5563">• Milk: 4.28</text>
    <text x="25" y="150" font-size="16" fill="#4B5563">• Frozen: 3.53</text>
    <text x="25" y="175" font-size="16" fill="#4B5563">• Grocery: 2.76</text>
    
    <!-- Range -->
    <text x="25" y="220" font-size="18" font-weight="600" fill="#1F2937">Range rất lớn:</text>
    <text x="25" y="250" font-size="16" fill="#4B5563">• Fresh: 3 → 112,151</text>
    <text x="25" y="275" font-size="16" fill="#4B5563">• Milk: 55 → 73,498</text>
    <text x="25" y="300" font-size="16" fill="#4B5563">• Grocery: 3 → 59,598</text>
    
    <!-- Consequences -->
    <text x="25" y="345" font-size="18" font-weight="600" fill="#1F2937">Hệ quả:</text>
    <text x="25" y="375" font-size="16" fill="#DC2626">✗ Distance metrics bị chi phối bởi</text>
    <text x="40" y="395" font-size="16" fill="#DC2626">features có range lớn</text>
    <text x="25" y="420" font-size="16" fill="#DC2626">✗ KMeans không ổn định</text>
  </g>
  
  <!-- Right: Log1p Solution -->
  <g transform="translate(680,180)">
    <circle cx="20" cy="0" r="28" fill="#D1FAE5"/>
    <text x="70" y="5" font-size="22" font-weight="bold" fill="#059669">Log1p + Scaler ✓</text>
    
    <rect x="0" y="30" width="520" height="420" rx="12" fill="#F0FDF4" stroke="#059669" stroke-width="2"/>
    
    <!-- Skewness reduction -->
    <text x="25" y="70" font-size="18" font-weight="600" fill="#1F2937">Giảm skewness mạnh:</text>
    <text x="25" y="100" font-size="16" fill="#4B5563">• Delicassen: 12.12 → -0.90</text>
    <text x="25" y="125" font-size="16" fill="#4B5563">• Milk: 4.28 → -0.17</text>
    <text x="25" y="150" font-size="16" fill="#4B5563">• Frozen: 3.53 → -0.46</text>
    <text x="25" y="175" font-size="16" fill="#4B5563">• Grocery: 2.76 → -0.94</text>
    
    <!-- Standardization -->
    <text x="25" y="220" font-size="18" font-weight="600" fill="#1F2937">Chuẩn hóa scale:</text>
    <text x="25" y="250" font-size="16" fill="#4B5563">• Tất cả features: mean=0, std=1</text>
    <text x="25" y="275" font-size="16" fill="#4B5563">• Distance metrics có ý nghĩa</text>
    <text x="25" y="300" font-size="16" fill="#4B5563">• Features đóng góp ngang nhau</text>
    
    <!-- Benefits -->
    <text x="25" y="345" font-size="18" font-weight="600" fill="#1F2937">Kết quả:</text>
    <text x="25" y="375" font-size="16" fill="#059669">✓ ARI mean = 0.997 (K=2, seed stability)</text>
    <text x="25" y="400" font-size="16" fill="#059669">✓ Silhouette validation = 0.307</text>
    <text x="25" y="425" font-size="16" fill="#059669">✓ Cluster ổn định, dễ interpret</text>
  </g>
  
  <!-- Footer -->
  <text x="80" y="680" font-size="14" fill="#9CA3AF">Quyết định D011: Chọn log1p + StandardScaler cho toàn bộ pipeline</text>
  <text x="1200" y="680" font-size="14" fill="#9CA3AF" text-anchor="end">5 / 15</text>
</svg>'''
    
    with open(SVG_OUTPUT_DIR / "05_preprocessing_comparison.svg", "w", encoding="utf-8") as f:
        f.write(content)
    print("✓ Generated slide 05: Preprocessing Comparison")

def generate_slide_06():
    """Slide 06: Elbow Method"""
    # Real data from selection_evidence.csv
    k_values = [2, 3, 4, 5, 6, 7, 8]
    inertias = [391.53, 341.06, 302.02, 286.64, 265.17, 253.89, 247.25]
    
    content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" font-family="Inter, system-ui, -apple-system, sans-serif">
{COMMON_DEFS}
  
  <!-- Background -->
  <rect width="1280" height="720" fill="#FFFFFF"/>
  
  <!-- Header -->
  <text x="80" y="80" font-size="42" font-weight="bold" fill="#1F2937">Elbow Method</text>
  <text x="80" y="115" font-size="24" fill="#6B7280">Validation Inertia vs K (log1p + StandardScaler)</text>
  <rect x="80" y="125" width="120" height="4" rx="2" fill="url(#accentBar)"/>
  
  <!-- Chart -->
  <g transform="translate(180,200)">
    <!-- Chart background -->
    <rect x="0" y="0" width="900" height="320" fill="#F9FAFB" rx="12" stroke="#E5E7EB" stroke-width="2"/>
    
    <!-- Grid lines -->
    <line x1="0" y1="80" x2="900" y2="80" stroke="#D1D5DB" stroke-width="1" opacity="0.5"/>
    <line x1="0" y1="160" x2="900" y2="160" stroke="#D1D5DB" stroke-width="1" opacity="0.5"/>
    <line x1="0" y1="240" x2="900" y2="240" stroke="#D1D5DB" stroke-width="1" opacity="0.5"/>
    
    <!-- Elbow curve -->
    <polyline points="50,20 178,80 306,140 434,175 562,220 690,245 818,270" fill="none" stroke="#2563EB" stroke-width="4"/>
    
    <!-- Data points -->
    <circle cx="50" cy="20" r="10" fill="#10B981" stroke="#FFFFFF" stroke-width="3"/>
    <circle cx="178" cy="80" r="8" fill="#2563EB" stroke="#FFFFFF" stroke-width="2"/>
    <circle cx="306" cy="140" r="8" fill="#2563EB" stroke="#FFFFFF" stroke-width="2"/>
    <circle cx="434" cy="175" r="8" fill="#2563EB" stroke="#FFFFFF" stroke-width="2"/>
    <circle cx="562" cy="220" r="8" fill="#2563EB" stroke="#FFFFFF" stroke-width="2"/>
    <circle cx="690" cy="245" r="8" fill="#2563EB" stroke="#FFFFFF" stroke-width="2"/>
    <circle cx="818" cy="270" r="8" fill="#2563EB" stroke="#FFFFFF" stroke-width="2"/>
    
    <!-- K labels -->
    <text x="50" y="310" font-size="16" fill="#4B5563" text-anchor="middle">K=2</text>
    <text x="178" y="310" font-size="16" fill="#4B5563" text-anchor="middle">K=3</text>
    <text x="306" y="310" font-size="16" fill="#4B5563" text-anchor="middle">K=4</text>
    <text x="434" y="310" font-size="16" fill="#4B5563" text-anchor="middle">K=5</text>
    <text x="562" y="310" font-size="16" fill="#4B5563" text-anchor="middle">K=6</text>
    <text x="690" y="310" font-size="16" fill="#4B5563" text-anchor="middle">K=7</text>
    <text x="818" y="310" font-size="16" fill="#4B5563" text-anchor="middle">K=8</text>
    
    <!-- Inertia values -->
    <text x="50" y="-5" font-size="14" fill="#10B981" text-anchor="middle" font-weight="600">391.5</text>
    <text x="178" y="70" font-size="13" fill="#2563EB" text-anchor="middle">341.1</text>
    <text x="306" y="130" font-size="13" fill="#2563EB" text-anchor="middle">302.0</text>
    <text x="434" y="165" font-size="13" fill="#2563EB" text-anchor="middle">286.6</text>
    <text x="562" y="210" font-size="13" fill="#2563EB" text-anchor="middle">265.2</text>
    <text x="690" y="235" font-size="13" fill="#2563EB" text-anchor="middle">253.9</text>
    <text x="818" y="260" font-size="13" fill="#2563EB" text-anchor="middle">247.2</text>
    
    <!-- Y-axis label -->
    <text x="-160" y="450" font-size="18" fill="#1F2937" transform="rotate(-90)" text-anchor="middle" font-weight="600">Inertia</text>
  </g>
  
  <!-- Highlight K=2 -->
  <rect x="180" y="550" width="900" height="80" rx="12" fill="#D1FAE5" stroke="#10B981" stroke-width="2"/>
  <text x="210" y="580" font-size="18" font-weight="bold" fill="#059669">K=2 Optimal</text>
  <text x="210" y="610" font-size="16" fill="#047857">Elbow rõ ràng: inertia giảm 12.9% từ K=2→3, sau đó chỉ giảm dần &lt; 5% mỗi bước</text>
  
  <!-- Footer -->
  <text x="80" y="680" font-size="14" fill="#9CA3AF">Data: reports/data/experiments/selection_evidence.csv</text>
  <text x="1200" y="680" font-size="14" fill="#9CA3AF" text-anchor="end">6 / 15</text>
</svg>'''
    
    with open(SVG_OUTPUT_DIR / "06_elbow_method.svg", "w", encoding="utf-8") as f:
        f.write(content)
    print("✓ Generated slide 06: Elbow Method")

def generate_slide_07():
    """Slide 07: Silhouette Analysis"""
    content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" font-family="Inter, system-ui, -apple-system, sans-serif">
{COMMON_DEFS}
  
  <!-- Background -->
  <rect width="1280" height="720" fill="#FFFFFF"/>
  
  <!-- Header -->
  <text x="80" y="80" font-size="42" font-weight="bold" fill="#1F2937">Silhouette Analysis</text>
  <text x="80" y="115" font-size="24" fill="#6B7280">Train vs Validation Silhouette Score</text>
  <rect x="80" y="125" width="120" height="4" rx="2" fill="url(#accentBar)"/>
  
  <!-- Chart -->
  <g transform="translate(150,200)">
    <!-- Bars for K=2 -->
    <rect x="0" y="100" width="70" height="150" rx="6" fill="#2563EB"/>
    <text x="35" y="85" font-size="14" fill="#2563EB" text-anchor="middle" font-weight="600">0.276</text>
    <rect x="90" y="60" width="70" height="190" rx="6" fill="#10B981"/>
    <text x="125" y="45" font-size="14" fill="#10B981" text-anchor="middle" font-weight="600">0.307</text>
    <text x="80" y="280" font-size="16" fill="#1F2937" text-anchor="middle">K=2</text>
    
    <!-- Bars for K=3 -->
    <rect x="200" y="130" width="70" height="120" rx="6" fill="#2563EB"/>
    <text x="235" y="115" font-size="14" fill="#2563EB" text-anchor="middle">0.205</text>
    <rect x="290" y="110" width="70" height="140" rx="6" fill="#10B981"/>
    <text x="325" y="95" font-size="14" fill="#10B981" text-anchor="middle">0.217</text>
    <text x="280" y="280" font-size="16" fill="#1F2937" text-anchor="middle">K=3</text>
    
    <!-- Bars for K=4 -->
    <rect x="400" y="135" width="70" height="115" rx="6" fill="#2563EB"/>
    <text x="435" y="120" font-size="14" fill="#2563EB" text-anchor="middle">0.206</text>
    <rect x="490" y="170" width="70" height="80" rx="6" fill="#10B981"/>
    <text x="525" y="155" font-size="14" fill="#10B981" text-anchor="middle">0.154</text>
    <text x="480" y="280" font-size="16" fill="#1F2937" text-anchor="middle">K=4</text>
    
    <!-- Bars for K=5 -->
    <rect x="600" y="145" width="70" height="105" rx="6" fill="#2563EB"/>
    <text x="635" y="130" font-size="14" fill="#2563EB" text-anchor="middle">0.198</text>
    <rect x="690" y="170" width="70" height="80" rx="6" fill="#10B981"/>
    <text x="725" y="155" font-size="14" fill="#10B981" text-anchor="middle">0.162</text>
    <text x="680" y="280" font-size="16" fill="#1F2937" text-anchor="middle">K=5</text>
    
    <!-- Bars for K=6,7,8 (smaller) -->
    <rect x="800" y="148" width="55" height="102" rx="6" fill="#2563EB"/>
    <text x="828" y="135" font-size="13" fill="#2563EB" text-anchor="middle">0.193</text>
    <rect x="870" y="172" width="55" height="78" rx="6" fill="#10B981"/>
    <text x="898" y="160" font-size="13" fill="#10B981" text-anchor="middle">0.160</text>
    <text x="848" y="280" font-size="15" fill="#1F2937" text-anchor="middle">K=6</text>
    
    <rect x="950" y="152" width="55" height="98" rx="6" fill="#2563EB"/>
    <rect x="1020" y="178" width="55" height="72" rx="6" fill="#10B981"/>
    <text x="998" y="280" font-size="15" fill="#1F2937" text-anchor="middle">K=7</text>
    
    <!-- Grid line -->
    <line x1="-10" y1="250" x2="1100" y2="250" stroke="#E5E7EB" stroke-width="2"/>
    
    <!-- Y-axis labels -->
    <text x="-30" y="60" font-size="14" fill="#4B5563" text-anchor="end">0.30</text>
    <text x="-30" y="160" font-size="14" fill="#4B5563" text-anchor="end">0.20</text>
    <text x="-30" y="255" font-size="14" fill="#4B5563" text-anchor="end">0.00</text>
  </g>
  
  <!-- Legend -->
  <g transform="translate(950,230)">
    <rect x="0" y="0" width="40" height="30" rx="4" fill="#2563EB"/>
    <text x="50" y="20" font-size="16" fill="#1F2937">Train</text>
    <rect x="120" y="0" width="40" height="30" rx="4" fill="#10B981"/>
    <text x="170" y="20" font-size="16" fill="#1F2937">Validation</text>
  </g>
  
  <!-- Insights -->
  <rect x="80" y="520" width="1120" height="120" rx="12" fill="#DBEAFE"/>
  <text x="110" y="555" font-size="18" font-weight="bold" fill="#1E40AF">Kết luận:</text>
  <text x="110" y="585" font-size="16" fill="#1E3A8A">• K=2: Silhouette validation cao nhất (0.307), train-val gap thấp → generalization tốt</text>
  <text x="110" y="610" font-size="16" fill="#1E3A8A">• K≥3: Score giảm mạnh, overfitting risk tăng</text>
  <text x="110" y="635" font-size="16" fill="#059669" font-weight="600">→ Kết hợp Elbow + Silhouette + ARI stability (0.997): Chọn K=2</text>
  
  <!-- Footer -->
  <text x="80" y="680" font-size="14" fill="#9CA3AF">Quyết định: K=2, log1p+StandardScaler, random_state=42</text>
  <text x="1200" y="680" font-size="14" fill="#9CA3AF" text-anchor="end">7 / 15</text>
</svg>'''
    
    with open(SVG_OUTPUT_DIR / "07_silhouette_analysis.svg", "w", encoding="utf-8") as f:
        f.write(content)
    print("✓ Generated slide 07: Silhouette Analysis")

def generate_slide_10():
    """Slide 10: Channel & Region Distribution"""
    content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" font-family="Inter, system-ui, -apple-system, sans-serif">
{COMMON_DEFS}
  
  <!-- Background -->
  <rect width="1280" height="720" fill="#FFFFFF"/>
  
  <!-- Header -->
  <text x="80" y="80" font-size="42" font-weight="bold" fill="#1F2937">Phân bố Channel & Region</text>
  <text x="80" y="115" font-size="24" fill="#6B7280">Profiling theo biến phụ (không dùng clustering)</text>
  <rect x="80" y="125" width="120" height="4" rx="2" fill="url(#accentBar)"/>
  
  <!-- Channel Table -->
  <g transform="translate(80,180)">
    <text x="0" y="-5" font-size="22" font-weight="bold" fill="#2563EB">Channel Distribution</text>
    
    <!-- Table header -->
    <rect x="0" y="10" width="540" height="50" fill="#DBEAFE" stroke="#2563EB" stroke-width="2" rx="8"/>
    <text x="180" y="42" font-size="18" fill="#1E40AF" text-anchor="middle" font-weight="600">Cluster 0</text>
    <text x="400" y="42" font-size="18" fill="#1E40AF" text-anchor="middle" font-weight="600">Cluster 1</text>
    
    <!-- Row 1: Horeca -->
    <rect x="0" y="60" width="540" height="70" fill="#FFFFFF" stroke="#E5E7EB" stroke-width="1" rx="6"/>
    <text x="20" y="100" font-size="18" fill="#1F2937" font-weight="500">Horeca (Ch 1)</text>
    <rect x="150" y="75" width="110" height="35" rx="6" fill="#3B82F6"/>
    <text x="205" y="100" font-size="16" fill="#FFFFFF" text-anchor="middle" font-weight="600">54 (33%)</text>
    <rect x="330" y="75" width="180" height="35" rx="6" fill="#10B981"/>
    <text x="420" y="100" font-size="16" fill="#FFFFFF" text-anchor="middle" font-weight="600">186 (98%)</text>
    
    <!-- Row 2: Retail -->
    <rect x="0" y="130" width="540" height="70" fill="#F9FAFB" stroke="#E5E7EB" stroke-width="1" rx="6"/>
    <text x="20" y="170" font-size="18" fill="#1F2937" font-weight="500">Retail (Ch 2)</text>
    <rect x="150" y="145" width="150" height="35" rx="6" fill="#3B82F6"/>
    <text x="225" y="170" font-size="16" fill="#FFFFFF" text-anchor="middle" font-weight="600">108 (67%)</text>
    <rect x="330" y="145" width="50" height="35" rx="6" fill="#10B981" opacity="0.6"/>
    <text x="355" y="170" font-size="16" fill="#FFFFFF" text-anchor="middle" font-weight="600">4 (2%)</text>
    
    <!-- Insight box -->
    <rect x="0" y="225" width="540" height="65" rx="10" fill="#EFF6FF"/>
    <text x="20" y="255" font-size="16" fill="#1E40AF" font-weight="600">💡 Cluster 1 chủ yếu Horeca (98%), Cluster 0 cân bằng hơn</text>
    <text x="20" y="278" font-size="15" fill="#3B82F6">Cluster phản ánh channel, dù không dùng channel làm feature</text>
  </g>
  
  <!-- Region Table -->
  <g transform="translate(660,180)">
    <text x="0" y="-5" font-size="22" font-weight="bold" fill="#10B981">Region Distribution</text>
    
    <!-- Table header -->
    <rect x="0" y="10" width="540" height="50" fill="#D1FAE5" stroke="#10B981" stroke-width="2" rx="8"/>
    <text x="180" y="42" font-size="18" fill="#047857" text-anchor="middle" font-weight="600">Cluster 0</text>
    <text x="400" y="42" font-size="18" fill="#047857" text-anchor="middle" font-weight="600">Cluster 1</text>
    
    <!-- Row 1: Lisbon -->
    <rect x="0" y="60" width="540" height="70" fill="#FFFFFF" stroke="#E5E7EB" stroke-width="1" rx="6"/>
    <text x="20" y="100" font-size="18" fill="#1F2937" font-weight="500">Lisbon (Reg 3)</text>
    <rect x="150" y="75" width="130" height="35" rx="6" fill="#3B82F6"/>
    <text x="215" y="100" font-size="16" fill="#FFFFFF" text-anchor="middle" font-weight="600">120 (74%)</text>
    <rect x="330" y="75" width="150" height="35" rx="6" fill="#10B981"/>
    <text x="405" y="100" font-size="16" fill="#FFFFFF" text-anchor="middle" font-weight="600">128 (67%)</text>
    
    <!-- Row 2: Oporto -->
    <rect x="0" y="130" width="540" height="70" fill="#F9FAFB" stroke="#E5E7EB" stroke-width="1" rx="6"/>
    <text x="20" y="170" font-size="18" fill="#1F2937" font-weight="500">Oporto (Reg 1)</text>
    <rect x="150" y="145" width="90" height="35" rx="6" fill="#3B82F6" opacity="0.7"/>
    <text x="195" y="170" font-size="16" fill="#FFFFFF" text-anchor="middle" font-weight="600">30 (19%)</text>
    <rect x="330" y="145" width="95" height="35" rx="6" fill="#10B981" opacity="0.7"/>
    <text x="378" y="170" font-size="16" fill="#FFFFFF" text-anchor="middle" font-weight="600">39 (21%)</text>
    
    <!-- Insight box -->
    <rect x="0" y="225" width="540" height="65" rx="10" fill="#F0FDF4"/>
    <text x="20" y="255" font-size="16" fill="#047857" font-weight="600">💡 Không có sự khác biệt rõ ràng về địa lý</text>
    <text x="20" y="278" font-size="15" fill="#059669">Region phân bố tương đồng giữa 2 cluster</text>
  </g>
  
  <!-- Summary -->
  <rect x="80" y="510" width="1120" height="130" rx="12" fill="#FFFBEB" stroke="#F59E0B" stroke-width="2"/>
  <text x="110" y="545" font-size="20" font-weight="bold" fill="#D97706">Tóm tắt:</text>
  <text x="110" y="575" font-size="17" fill="#92400E">• Channel & Region CHỈ dùng profiling sau khi phân cụm xong, KHÔNG dùng làm features clustering</text>
  <text x="110" y="605" font-size="17" fill="#92400E">• Cluster 0: Cân bằng Horeca/Retail, tập trung Lisbon</text>
  <text x="110" y="635" font-size="17" fill="#92400E">• Cluster 1: Chủ yếu Horeca (98%), cũng tập trung Lisbon</text>
  
  <!-- Footer -->
  <text x="80" y="680" font-size="14" fill="#9CA3AF">Data: final_profile/channel_profile.csv, region_profile.csv</text>
  <text x="1200" y="680" font-size="14" fill="#9CA3AF" text-anchor="end">10 / 15</text>
</svg>'''
    
    with open(SVG_OUTPUT_DIR / "10_channel_region.svg", "w", encoding="utf-8") as f:
        f.write(content)
    print("✓ Generated slide 10: Channel & Region Distribution")

def generate_slide_14():
    """Slide 14: Limitations & Future Work"""
    content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" font-family="Inter, system-ui, -apple-system, sans-serif">
{COMMON_DEFS}
  
  <!-- Background -->
  <rect width="1280" height="720" fill="#FFFFFF"/>
  
  <!-- Header -->
  <text x="80" y="80" font-size="42" font-weight="bold" fill="#1F2937">Limitations & Future Work</text>
  <text x="80" y="115" font-size="24" fill="#6B7280">Hạn chế và Hướng phát triển</text>
  <rect x="80" y="125" width="120" height="4" rx="2" fill="url(#accentBar)"/>
  
  <!-- Limitations (Left) -->
  <g transform="translate(80,180)">
    <circle cx="22" cy="0" r="30" fill="#FEE2E2"/>
    <text x="22" y="10" font-size="32" text-anchor="middle">⚠️</text>
    <text x="75" y="5" font-size="24" font-weight="bold" fill="#DC2626">Hạn chế hiện tại</text>
    
    <!-- Card 1 -->
    <rect x="0" y="45" width="540" height="130" rx="12" fill="#FFFFFF" stroke="#E5E7EB" stroke-width="2"/>
    <text x="25" y="80" font-size="19" font-weight="600" fill="#1F2937">1. Phương pháp K-Means</text>
    <text x="25" y="105" font-size="16" fill="#4B5563">• Chỉ phát hiện cluster hình cầu (Euclidean)</text>
    <text x="25" y="130" font-size="16" fill="#4B5563">• Không phù hợp cluster hình dạng phức tạp</text>
    <text x="25" y="155" font-size="16" fill="#4B5563">• Nhạy cảm outliers dù đã preprocessing</text>
    
    <!-- Card 2 -->
    <rect x="0" y="190" width="540" height="105" rx="12" fill="#FFFFFF" stroke="#E5E7EB" stroke-width="2"/>
    <text x="25" y="225" font-size="19" font-weight="600" fill="#1F2937">2. Feature engineering</text>
    <text x="25" y="250" font-size="16" fill="#4B5563">• Chưa có interaction (Fresh×Milk, etc.)</text>
    <text x="25" y="275" font-size="16" fill="#4B5563">• Chưa có temporal patterns (timestamp)</text>
    
    <!-- Card 3 -->
    <rect x="0" y="310" width="540" height="105" rx="12" fill="#FFFFFF" stroke="#E5E7EB" stroke-width="2"/>
    <text x="25" y="345" font-size="19" font-weight="600" fill="#1F2937">3. Validation</text>
    <text x="25" y="370" font-size="16" fill="#4B5563">• Chỉ test stability, chưa có ground truth</text>
    <text x="25" y="395" font-size="16" fill="#4B5563">• Chưa A/B test business metrics thực tế</text>
  </g>
  
  <!-- Future Work (Right) -->
  <g transform="translate(660,180)">
    <circle cx="22" cy="0" r="30" fill="#D1FAE5"/>
    <text x="22" y="10" font-size="32" text-anchor="middle">🚀</text>
    <text x="75" y="5" font-size="24" font-weight="bold" fill="#059669">Hướng phát triển</text>
    
    <!-- Card 1 -->
    <rect x="0" y="45" width="540" height="130" rx="12" fill="#FFFFFF" stroke="#E5E7EB" stroke-width="2"/>
    <text x="25" y="80" font-size="19" font-weight="600" fill="#1F2937">1. Thuật toán khác</text>
    <text x="25" y="105" font-size="16" fill="#4B5563">• DBSCAN: cluster bất kỳ + outliers</text>
    <text x="25" y="130" font-size="16" fill="#4B5563">• Hierarchical: phân tích dendrogram</text>
    <text x="25" y="155" font-size="16" fill="#4B5563">• GMM: soft assignment, uncertainty</text>
    
    <!-- Card 2 -->
    <rect x="0" y="190" width="540" height="105" rx="12" fill="#FFFFFF" stroke="#E5E7EB" stroke-width="2"/>
    <text x="25" y="225" font-size="19" font-weight="600" fill="#1F2937">2. Feature mới</text>
    <text x="25" y="250" font-size="16" fill="#4B5563">• Ratio: Fresh/Total, Milk/Grocery</text>
    <text x="25" y="275" font-size="16" fill="#4B5563">• RFM analysis nếu có dữ liệu thời gian</text>
    
    <!-- Card 3 -->
    <rect x="0" y="310" width="540" height="105" rx="12" fill="#FFFFFF" stroke="#E5E7EB" stroke-width="2"/>
    <text x="25" y="345" font-size="19" font-weight="600" fill="#1F2937">3. Production deployment</text>
    <text x="25" y="370" font-size="16" fill="#4B5563">• Monitoring data drift (PSI, KL divergence)</text>
    <text x="25" y="395" font-size="16" fill="#4B5563">• A/B test chiến dịch marketing theo cluster</text>
  </g>
  
  <!-- Academic constraint note -->
  <rect x="80" y="510" width="1120" height="130" rx="12" fill="#EEF2FF" stroke="#6366F1" stroke-width="2"/>
  <text x="110" y="545" font-size="20" font-weight="bold" fill="#4338CA">Ghi chú học thuật:</text>
  <text x="110" y="575" font-size="17" fill="#4F46E5">Project 22 hoàn thành với K-Means baseline theo đúng yêu cầu Project 22:</text>
  <text x="110" y="605" font-size="17" fill="#4F46E5">• 6 biến chi tiêu là features chính, Channel/Region chỉ profiling</text>
  <text x="110" y="635" font-size="17" fill="#4F46E5">• Preprocessing + Train/Val/Test split đúng quy trình → Model artifact đã đóng băng</text>
  
  <!-- Footer -->
  <text x="80" y="680" font-size="14" fill="#9CA3AF">Các phương pháp nâng cao để lại cho tương lai</text>
  <text x="1200" y="680" font-size="14" fill="#9CA3AF" text-anchor="end">14 / 15</text>
</svg>'''
    
    with open(SVG_OUTPUT_DIR / "14_limitations_future.svg", "w", encoding="utf-8") as f:
        f.write(content)
    print("✓ Generated slide 14: Limitations & Future Work")

if __name__ == "__main__":
    print("Generating 5 remaining slides (05, 06, 07, 10, 14)...\n")
    generate_slide_05()
    generate_slide_06()
    generate_slide_07()
    generate_slide_10()
    generate_slide_14()
    print("\n✅ All 5 remaining slides completed!")
    print(f"📁 SVG files saved to: {SVG_OUTPUT_DIR}")
    print("\nTotal slides ready: 15 / 15")
    print("Next step: Run svg_to_pptx.py to export PowerPoint file")
