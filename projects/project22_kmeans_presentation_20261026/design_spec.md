<!-- ppt-master-schema: design-spec/v1 -->
# Project 22: K-Means Customer Segmentation - Design Spec

## I. Project Information

| Item | Value |
| --- | --- |
| Project Name | Project 22: Phân Khúc Khách Hàng Bán Sỉ Với K-Means |
| Canvas Format | PPT 16:9 |
| Page Count | 15 |
| Primary Language | vi |
| Target Audience | Giảng viên và đồng nghiệp đánh giá dự án học thuật Machine Learning |
| Communication Intent | Trình bày hoàn chỉnh quy trình phân khúc khách hàng từ dữ liệu thô đến ứng dụng web, chứng minh hiểu biết về K-Means, leakage, và ML pipeline |
| Desired Audience Outcome | Hiểu rõ bài toán, phương pháp, kết quả và ứng dụng thực tế; công nhận chất lượng học thuật và kỹ thuật của dự án |
| Core Message / Ask / Action | K-Means D011 (log1p + StandardScaler, K=2) là giải pháp ổn định và có ý nghĩa kinh doanh, được triển khai thành công với full CI/CD testing |
| Delivery Context | Trình bày học thuật trực tiếp 12-15 phút với demo thực tế, có vấn đáp |
| Artifact Afterlife | Tài liệu tham khảo cho giảng viên chấm điểm và lưu trữ thành tích dự án |
| Reading Mode | presentation |
| Content Strategy | Cân bằng giữa chi tiết kỹ thuật và trực quan; số liệu và kết quả phải chính xác từ artifacts thực tế |
| Design Style | Modern technical với data visualization rõ ràng, màu sắc chuyên nghiệp, thể hiện tính học thuật và công nghệ |
| AI Image Acquisition Path | none |
| Generation Mode | continuous |
| Spec Refinement | disabled |
| Speaker Notes | enabled — explicit request for presentation preparation |
| Custom Animations | enabled — presentation mode with data reveal and transition effects |
| Narration Audio | disabled |
| Created Date | 2026-10-26 |

## II. Canvas Specification

| Property | Value |
| --- | --- |
| Format | ppt169 |
| Dimensions | 1280 × 720 |
| viewBox | `0 0 1280 720` |
| Margins | 60px sides, 50px top/bottom |
| Content Area | 1160 × 620 |

## III. Visual Theme

### Theme Style

- **Mode**: custom
- **Visual style**: custom
- **Theme**: Clean technical design với data visualization mạnh mẽ
- **Tone**: Professional, academic, data-driven, trustworthy

- **Mode behavior**: Presentation mode với cấu trúc rõ ràng: mỗi slide tập trung vào một insight chính, sử dụng visualization để support arguments, progressive disclosure cho complex data, và clear takeaway messages
- **Visual style behavior**: Modern technical aesthetic với geometric shapes sạch sẽ, data charts prominent, subtle gradients cho depth, consistent card-based containers, icon-supported headings, và generous whitespace. Color usage follows data visualization best practices.

### Color Scheme

| Role | HEX | Purpose |
| --- | --- | --- |
| Background | #FFFFFF | Slide background white cho clarity |
| Secondary background | #F8F9FA | Subtle gray cho cards và containers |
| Primary | #2563EB | Primary blue cho headings, emphasis, cluster 0 |
| Accent | #10B981 | Green accent cho success states, cluster 1 |
| Secondary accent | #8B5CF6 | Purple cho highlights và secondary data |
| Body text | #1F2937 | Dark gray cho body text |
| Secondary text | #6B7280 | Medium gray cho captions, labels |
| Divider | #E5E7EB | Light gray cho rules, borders |

## IV. Typography System

### Font Plan

| Role | Character (Reference) | Primary | English if non-English | Fallback tail |
| --- | --- | --- | --- | --- |
| Title | Modern sans-serif, clean geometric | Inter | Inter | system-ui, -apple-system, sans-serif |
| Body | Readable sans-serif | Inter | Inter | system-ui, -apple-system, sans-serif |

- **Title stack**: Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif
- **Body stack**: Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif

### Font Size Hierarchy

| Purpose | Anchor Size (px) |
| --- | ---: |
| Body | 24 |
| Title | 48 |
| Subtitle | 32 |
| Annotation | 18 |

## V. Layout Principles

### Deck-wide Direction

- **Hierarchy direction**: Top-down with left-to-right flow; titles prominent at top, main content in central region, supporting details below
- **Composition tendency**: Balanced layouts with clear focal points; data visualizations as primary elements; text supporting rather than competing; generous margins maintain breathing room
- **Cross-page continuity**: Consistent header treatment with project identifier; recurring icon style; stable color coding for clusters; progressive data revelation maintaining context
- **Spacing posture**: Open and breathing; technical content needs clarity not density
- **Spacing anchors**: page margin 60px; block gap 32px; column gutter 40px; corner radius 8px; body leading 1.5

## VI. Icon Usage Specification

- **Primary bundled library**: phosphor-duotone
- **Brand-logo library**: none

| Icon Path | Suitable Scenarios |
| --- | --- |
| phosphor-duotone/chart-line | Data analysis, metrics, trends |
| phosphor-duotone/chart-pie-slice | Clustering, segmentation, distribution |
| phosphor-duotone/database | Dataset, data storage |
| phosphor-duotone/git-branch | Pipeline, workflow |
| phosphor-duotone/code | Technical implementation, API |
| phosphor-duotone/check-circle | Success, validation, testing |
| phosphor-duotone/warning | Limitations, warnings |
| phosphor-duotone/users-three | Customer segments, clusters |
| phosphor-duotone/stack | Technology stack, architecture |
| phosphor-duotone/target | Goal, objective |

## VII. Visualization Reference List

| Page | Family | Template | Usage |
| --- | --- | --- | --- |
| P05 | chart | grouped_bar_chart | Compare preprocessing methods (Raw vs Log1p) |
| P06 | chart | line_chart | Show Elbow curve for K selection |
| P07 | chart | column_chart | Display silhouette scores across K values |
| P08 | chart | radar_chart | Compare cluster profiles across 6 spending features |
| P09 | table | record_table | Present Channel/Region distribution by cluster |

## VIII. Image Resource List

| Filename | Dimensions | Ratio | Purpose | Type | Image pattern | Crop Policy | Acquire Via | Status | Reference | text_policy | page_role |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

## IX. Content Outline

### Part 1: Introduction & Context

#### Slide 01 - Cover

- **Audience move**: Unaware → Oriented to project scope and presentation structure
- **Relationships**: Title → Subtitle → Authors/Date form clear hierarchy; project identifier anchors context
- **Composition**: Centered heroic title with clean geometry, subtle gradient background suggesting data flow, project badge/identifier in corner
- **Title**: Phân Khúc Khách Hàng Bán Sỉ Với K-Means Clustering
- **Core message**: This is a complete ML project from data to deployment
- **Content**:
  · Project 22 — Machine Learning Fundamentals
  · K-Means Customer Segmentation
  · UCI Wholesale Customers Dataset
  · Full Pipeline: Data → Model → Web Application
  · 440 customers, 6 spending features, K=2 final solution

#### Slide 02 - Problem & Objective

- **Audience move**: Oriented → Understanding the business problem and research question
- **Relationships**: Problem statement → Research question → Objectives flow as nested elaboration; important constraint highlighted separately
- **Composition**: Problem statement prominent in upper region, research question as focal callout, objectives as structured list, ethical constraint emphasized in distinct container
- **Title**: Bài Toán và Mục Tiêu
- **Core message**: Understand customer spending patterns to support business decisions, not to judge human worth
- **Content**:
  · **Business Problem**: Nhà phân phối cần hiểu kiểu cơ cấu chi tiêu của khách hàng bán sỉ
  · **Research Question**: "Sau log-transform và chuẩn hóa, K-means tạo ra các phân khúc ổn định và có ý nghĩa kinh doanh nào?"
  · **Objectives**:
    - Áp dụng K-Means để phân khúc dựa trên hành vi chi tiêu
    - Phân tích cơ cấu chi tiêu từng phân khúc
    - Đóng gói model thành ứng dụng web với API
  · **Important**: Cụm CHỈ mô tả hành vi chi tiêu, KHÔNG đánh giá giá trị con người

#### Slide 03 - Dataset & Features

- **Audience move**: Understanding problem → Concrete knowledge of data characteristics
- **Relationships**: Source metadata links to data characteristics; six features cluster as primary variables; Channel/Region marked as secondary profiling-only variables
- **Composition**: Two-column layout with source info left, feature breakdown right; visual distinction between primary features (clustered) and secondary attributes (separated)
- **Title**: Dữ Liệu UCI Wholesale Customers
- **Core message**: 440 customers, 6 spending features are what we cluster on
- **Content**:
  · **Source**: UCI Machine Learning Repository
  · **License**: CC BY 4.0
  · **Size**: 440 customers
  · **6 Primary Features** (annual monetary units):
    - Fresh — sản phẩm tươi sống
    - Milk — sữa và sản phẩm từ sữa
    - Grocery — hàng tạp hóa
    - Frozen — thực phẩm đông lạnh
    - Detergents_Paper — chất tẩy rửa và giấy
    - Delicassen — thực phẩm ăn liền
  · **Channel & Region**: Chỉ dùng profiling SAU clustering, KHÔNG fit K-Means

### Part 2: Methodology

#### Slide 04 - ML Pipeline & Anti-Leakage

- **Audience move**: Know the data → Understand the rigorous methodology preventing data leakage
- **Relationships**: Pipeline steps flow left-to-right showing temporal order; split-before-preprocessing is the critical anti-leakage gate
- **Composition**: Horizontal flowchart with clear split point emphasized; leakage prevention highlighted as primary insight; seed and ratio values shown as anchoring details
- **Title**: Pipeline Machine Learning & Tránh Data Leakage
- **Core message**: Split BEFORE any learning = clean test results
- **Content**:
  · **Critical Rule**: Split train/validation/test TRƯỚC mọi preprocessing học từ dữ liệu
  · **Pipeline Flow**:
    1. Raw UCI data (440 customers)
    2. **SPLIT** → 264 train / 88 validation / 88 test (60/20/20, seed 42)
    3. Fit preprocessing on train only (log1p + StandardScaler)
    4. Transform validation/test using fitted parameters
    5. K-Means clustering on train
    6. Evaluate on validation
    7. Test used ONCE for final report
  · **Result**: Test độc lập, không dùng để chọn K hay tham số

#### Slide 05 - Preprocessing Comparison

- **Audience move**: Understand pipeline → See concrete evidence for preprocessing choice
- **Relationships**: Two preprocessing paths contrast in parallel; metrics compare their outcomes; winner emerges from evidence
- **Composition**: Side-by-side comparison with Raw left, Log1p+StandardScaler right; metrics table below showing superiority; visual cue (check/x) indicating selection
- **Title**: So Sánh Tiền Xử Lý: Raw vs Log1p + StandardScaler
- **Core message**: Log transformation essential for this skewed spending data
- **Content**:
  · **Baseline B**: Raw data → K-Means
    - Bị chi phối bởi outliers (chi tiêu cực lớn)
    - Khoảng cách Euclidean không công bằng giữa features
    - Silhouette và stability thấp hơn
  · **Selected Method**: log1p + StandardScaler → K-Means
    - Giảm ảnh hưởng outliers
    - Chuẩn hóa scale giữa 6 features
    - Silhouette validation tốt hơn rõ rệt
    - Stability cao qua 10 seeds
  · **Evidence**: 140 experiments (Raw/Log1p × K=2..8 × seed 42..51)
- **Visualization**: grouped_bar_chart comparing metrics

#### Slide 06 - Elbow Analysis

- **Audience move**: See preprocessing evidence → Understand K selection via inertia analysis
- **Relationships**: K values span horizontal axis; inertia decreases as K increases; elbow point suggests optimal K range
- **Composition**: Line chart prominent in center; K=2..8 clearly marked on axis; elbow region highlighted; interpretation callout positioned nearby
- **Title**: Elbow Method — Chọn K Từ Inertia
- **Core message**: Elbow suggests K=2-3 range as optimal tradeoff
- **Content**:
  · **Inertia per row** decreases with increasing K
  · **Elbow point** visible around K=2-3
  · Diminishing returns beyond K=3
  · Must combine with other metrics (silhouette, stability, interpretability)
  · Log1p + StandardScaler preprocessing used
- **Visualization**: line_chart showing inertia trend

#### Slide 07 - Silhouette Analysis

- **Audience move**: See inertia evidence → Understand K selection via cohesion metric
- **Relationships**: K values contrast via silhouette scores; K=2 emerges as strongest; validation scores shown separately from train
- **Composition**: Bar chart with K on x-axis, silhouette score on y-axis; K=2 bar highlighted; reference line at score threshold; validation scores emphasized
- **Title**: Silhouette Score — Độ Gắn Kết Cụm
- **Core message**: K=2 achieves best silhouette on validation
- **Content**:
  · **Validation Silhouette Scores** (Log1p + StandardScaler):
    - K=2: 0.3066 ✓ (highest)
    - K=3: 0.2847
    - K=4: 0.2654
    - K=5-8: declining
  · **Stability**: Seed ARI = 0.9970 cho K=2 (rất ổn định)
  · K=2 vượt trội cả về cohesion và stability
- **Visualization**: column_chart comparing silhouette scores

### Part 3: Results & Analysis

#### Slide 08 - Final Model D011

- **Audience move**: Understand selection process → Know the frozen model configuration
- **Relationships**: Configuration parameters group as technical specification; rationale supports decision; status confirms freeze point
- **Composition**: Configuration details in structured card; rationale as supporting evidence; freeze status badge prominent
- **Title**: Model Cuối Cùng — D011 (FROZEN)
- **Core message**: K=2 with log1p + StandardScaler is the official frozen model
- **Content**:
  · **Configuration**:
    - Preprocessing: log1p + StandardScaler
    - K: 2 clusters
    - Algorithm: lloyd
    - n_init: 10, max_iter: 300
    - Random state: 42
  · **Decision Date**: 2026-10-08 (BEFORE opening test)
  · **Rationale**:
    - Validation silhouette: 0.3066
    - Seed ARI: 0.9970 (high stability)
    - Balanced cluster sizes (44.70% minimum share)
    - Refit ARI train+val: 0.8893 vs K3's 0.3343
  · **Final Test** (88 samples, ONE time only):
    - Silhouette: 0.2389
    - Cluster sizes: 45 / 43 (balanced)

#### Slide 09 - Cluster Profiles

- **Audience move**: Know the model → Understand what the two clusters represent
- **Relationships**: Two clusters contrast across six features; median values show spending patterns; profiles interpreted in business context
- **Composition**: Radar chart comparing clusters across six dimensions; median tables positioned adjacent; cluster characteristics summarized in callouts
- **Title**: Hồ Sơ Hai Cụm (352 Development Samples)
- **Core message**: Two distinct spending patterns emerge clearly
- **Content**:
  · **Cluster 0** (162 khách, 46%): Chi Tiêu Cao
    - Fresh: 5693.5 m.u.
    - Milk: 4339.5 m.u.
    - Grocery: 4621.5 m.u.
    - Frozen: 1945.5 m.u.
    - Detergents_Paper: 1731.5 m.u.
    - Delicassen: 910.0 m.u.
    - **Pattern**: Chi tiêu cao ở hầu hết nhóm hàng
  · **Cluster 1** (190 khách, 54%): Chi Tiêu Vừa Phải
    - Fresh: 3276.0 m.u.
    - Milk: 2056.5 m.u.
    - Grocery: 1841.0 m.u.
    - Frozen: 1051.0 m.u.
    - Detergents_Paper: 296.5 m.u.
    - Delicassen: 612.5 m.u.
    - **Pattern**: Chi tiêu thấp hơn, đặc biệt rõ ở Detergents_Paper
- **Visualization**: radar_chart comparing spending across features
- **Native-ready**: cluster-profile=yes

#### Slide 10 - Channel & Region Profiling

- **Audience move**: Understand spending patterns → See how clusters relate to business context
- **Relationships**: Clusters distribute across Channel types and Regions; distribution percentages show non-uniform patterns; insight: clusters reflect spending behavior beyond simple Channel/Region grouping
- **Composition**: Table showing distribution matrix; percentages clearly visible; key insight highlighted as takeaway
- **Title**: Profiling Channel và Region (SAU Clustering)
- **Core message**: Clusters found via spending patterns, not Channel/Region
- **Content**:
  · **Channel Distribution**:
    - Horeca (Hotel/Restaurant/Café): có ở cả 2 clusters
    - Retail (Bán lẻ): có ở cả 2 clusters
    - Tỷ lệ khác nhau giữa clusters
  · **Region Distribution**:
    - Lisbon, Oporto, Other regions
    - Phân bố khác nhau giữa 2 clusters
  · **Key Point**: Channel/Region KHÔNG dùng để fit model hoặc chọn K; chỉ dùng để hiểu cụm sau khi tạo
- **Visualization**: record_table showing distribution
- **Native-ready**: channel-region-table=yes

### Part 4: System & Application

#### Slide 11 - Technology Stack

- **Audience move**: Understand analysis results → Know the implementation technology
- **Relationships**: Three-tier architecture flows from ML training through backend to frontend; each layer has distinct responsibilities
- **Composition**: Vertical stack diagram with ML training at bottom (foundation), backend in middle (serving), frontend at top (presentation); technologies labeled clearly; arrows show data flow
- **Title**: Kiến Trúc Hệ Thống
- **Core message**: Clean separation: Python trains offline, Node.js serves frozen model, React presents to users
- **Content**:
  · **ML Training (Python)**:
    - scikit-learn, pandas, NumPy
    - 140 experiments → Model selection
    - Export frozen artifacts
  · **Backend (Node.js)**:
    - Fastify + TypeScript
    - Load frozen model.json (SHA-256 verified)
    - NO retraining on requests
    - API: /health, /ready, /segment, /dashboard, /model-info
  · **Frontend (React)**:
    - TypeScript + Vite
    - 3 screens: Intro, Segmentation, Dashboard
    - Visualization với PCA 2D, charts
  · **Testing**:
    - 64/64 E2E tests PASS
    - Gate 6-10 CI/CD verified

#### Slide 12 - Web Application Demo

- **Audience move**: Know the architecture → See the working application
- **Relationships**: Three screens represent user journey; each screen serves distinct purpose; API connections enable data flow
- **Composition**: Three screen mockups arranged horizontally showing user flow; brief descriptions below each; call-to-action for live demo
- **Title**: Ứng Dụng Web — 3 Màn Hình Chính
- **Core message**: Full working application from input to insights
- **Content**:
  · **Screen 1: Giới Thiệu**
    - Bài toán, phạm vi, giới hạn
    - Data card & Model card
    - Đơn vị monetary units (m.u.)
  · **Screen 2: Phân Khúc Khách Hàng**
    - Form input 6 biến chi tiêu
    - Real-time validation
    - Result: Cluster ID, distance, profile
    - Lưu lịch sử local (100 records)
    - CSV batch import/export
  · **Screen 3: Dashboard & Analytics**
    - Cluster sizes, medians
    - Channel/Region composition
    - Experiment explorer (K2-8, Raw/Log1p)
    - PCA 2D visualization
    - Distance outliers
  · **Live Demo**: localhost:5173 (ready to show)

#### Slide 13 - Testing & Quality

- **Audience move**: See the application → Trust the quality through testing evidence
- **Relationships**: Multiple test gates build confidence progressively; each gate validates different aspects; final numbers prove thoroughness
- **Composition**: Test results organized by gate; passing status prominently displayed; CI/CD badge indicating automated verification
- **Title**: Kiểm Thử và Đảm Bảo Chất Lượng
- **Core message**: Comprehensive testing across all layers proves production readiness
- **Content**:
  · **Gate 6 — Node.js Native & API**:
    - 19/19 native serving tests ✓
    - 16/16 Fastify API tests ✓
    - TypeScript & Vite build ✓
  · **Gate 7 — End-to-End**:
    - 40/40 Playwright tests ✓
    - Desktop + mobile emulation
    - Python sklearn ↔ Node parity 1/1 ✓
  · **Gate 8 — Windows CI**:
    - Clean install verification ✓
    - 40/40 E2E on Windows Server 2025 ✓
  · **Gate 10.3 — Full Regression**:
    - 64/64 E2E tests PASS ✓
    - Backend, serving, parity all verified
  · **Security**: npm audit 0 vulnerabilities
  · **Data Integrity**: SHA-256 checksums verified, no unauthorized changes

### Part 5: Limitations & Conclusion

#### Slide 14 - Limitations & Ethical Considerations

- **Audience move**: See complete system → Understand proper use boundaries and limitations
- **Relationships**: Usage conditions define when model applies; ethical guidelines prevent misuse; out-of-scope scenarios protect users
- **Composition**: Limitations grouped in structured sections; warning symbols emphasize constraints; ethical boundaries prominently highlighted
- **Title**: Giới Hạn và Cân Nhắc Đạo Đức
- **Core message**: Clear boundaries ensure responsible ML practice
- **Content**:
  · **Điều Kiện Sử Dụng**:
    - Cần đủ 6 biến chi tiêu hằng năm
    - Đơn vị annual monetary units (m.u.), KHÔNG mặc định VND
    - Áp dụng cho wholesale B2B, không phải B2C
    - Khoảng cách ≠ confidence/probability
  · **KHÔNG Nên Dùng Để**:
    - ❌ Đánh giá giá trị hoặc xếp hạng con người
    - ❌ Quyết định tín dụng/tài chính cá nhân
    - ❌ Dự đoán cho khách chưa có dữ liệu chi tiêu
    - ❌ Áp dụng ngoài ngành bán sỉ
  · **Out-of-Range Warning**:
    - API cảnh báo khi input ngoài train ranges
    - KHÔNG tự động clip giá trị
    - Distance to centroid as uncertainty signal

#### Slide 15 - Conclusion & Achievements

- **Audience move**: Understand limitations → Appreciate complete project accomplishment
- **Relationships**: Key achievements list project milestones; academic compliance shows rigor; repository readiness enables reproduction
- **Composition**: Achievement list prominent in main region; academic/technical badges showing compliance; repository link and next steps as call-to-action
- **Title**: Kết Luận và Thành Quả
- **Core message**: Complete ML project ready for academic evaluation and real-world use
- **Content**:
  · **Thành Tựu Chính**:
    ✓ Phân khúc 440 khách thành 2 cụm ổn định
    ✓ Tránh data leakage với split-first methodology
    ✓ So sánh toàn diện: Raw vs Log1p, K=2-8, 10 seeds
    ✓ Test độc lập 1 lần duy nhất
    ✓ Web app với frozen model serving
    ✓ Full CI/CD: 64/64 E2E tests PASS
    ✓ Data card & Model card đầy đủ
  · **Học Thuật**:
    - Reproducible: Full pipeline với seeds, SHA checksums
    - No test leakage: Test không dùng cho selection
    - Ethical: Rõ ràng về giới hạn, không phân loại giá trị người
  · **Technical**:
    - Gate 9.6: Final code CI verified
    - Model D011: FROZEN status
    - Repository: github.com/[project-repo]
  · **Next Steps**: Nghiệm thu Windows 10, báo cáo 15-25 trang, minh chứng 2 thành viên

## X. Speaker Notes Requirements

- **Generation**: enabled
- **Filename**: Match each SVG (e.g., `01_cover.svg` → `notes/01_cover.md`)
- **Content**: Formal presentation notes covering key talking points, data interpretations, and transition cues for 12-15 minute academic presentation with demo
- **Total duration**: 12-15 minutes
- **Notes style**: formal
- **Presentation purpose**: Academic project evaluation with technical depth and business context
