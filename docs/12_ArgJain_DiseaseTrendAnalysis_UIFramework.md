# 12 ArgJain DiseaseTrendAnalysis UIFramework

DISEASE TREND ANALYSIS

STEP 12 — User Interface (UI) Architecture & Wireframes


## 1. Application Screen Inventory (UI-01 to UI-06)

The application interface is structured into six dedicated analytical screens conforming to standard Streamlit multi-page routing conventions under the pages/ directory:


## 2. Comprehensive ASCII Wireframes


### 2.1 Wireframe: UI-01 Executive Overview Dashboard

+---------------------------------------------------------------------------------------------------+
|  [H1] DISEASE TREND ANALYSIS — EXECUTIVE COCKPIT (pages/01_Overview.py)                           |
+----------------------+----------------------------------------------------------------------------+
| SIDEBAR FILTERS      | [ROW 1: 4 TAILWIND KPI STAT CARDS]                                         |
|                      | +------------------+ +------------------+ +---------------+ +-------------+ |
| Disease:             | | Total Cases      | | Total Deaths     | | Recoveries    | | CFR %       | |
| [ All Diseases    v] | | 1,428,520        | | 31,427           | | 1,328,940     | | 2.20%       | |
|                      | | [+14.2% YoY]     | | [-2.1% YoY]      | | [93.0% Rate]  | | [Stable]    | |
| States:              | +------------------+ +------------------+ +---------------+ +-------------+ |
| [ All 10 States   v] |                                                                            |
|                      | [ROW 2: REGIONAL BURDEN RANKING — Plotly Horizontal Bar Chart]             |
| Observation Years:   |  Maharashtra   |████████████████████████████████████████  320,410          |
| [2020 ====== 2024]   |  Delhi         |██████████████████████████████            241,120          |
|                      |  Uttar Pradesh |████████████████████████                  198,340          |
| Age Cohort:          |  West Bengal   |████████████████                          142,500          |
| [ All Ages        v] |  Bihar         |████████████                              110,230          |
|                      |                                                                            |
| Gender Identity:     | [ROW 3: INSIGHT CALLOUT BOX — Tailwind Blue]                               |
| (o) All  ( ) M  ( )F | "Maharashtra and Delhi account for 39.3% of cumulative national morbidity."|
|                      |                                                                            |
| [ Reset Filters ]    | [ROW 4: STATE-LEVEL CFR BENCHMARK TABLE — Interactive St.DataFrame]        |
|                      | State Name    | Cases    | Deaths | Recoveries | CFR (%) | Trend Badge |
| Active Filters: 0    | Maharashtra   | 320,410  | 7,690  | 298,120    | 2.40%   | High Risk   |
+----------------------+----------------------------------------------------------------------------+


### 2.2 Wireframe: UI-02 Longitudinal Trends & Seasonality

+---------------------------------------------------------------------------------------------------+
|  [H1] LONGITUDINAL & SEASONAL TRENDS (pages/02_Trends.py)                                          |
+----------------------+----------------------------------------------------------------------------+
| SIDEBAR FILTERS      | [SECTION 1: 60-MONTH LONGITUDINAL TIME SERIES — Plotly Line with Hover]    |
| (Same Persistent     | Cases                                                                      |
|  Session State)      |  50k|                   ▲ (2021 COVID Delta Wave Peak)                     |
|                      |  30k|                  / \                                                 |
|                      |  10k|   _/\_/\_      _/   \_      _/\_/\_ (Annual Monsoon Dengue Surges)   |
|                      |   0 +-------------------------------------------------------------> Time   |
|                      |     2020         2021         2022         2023         2024               |
|                      |                                                                            |
|                      | [SECTION 2: MULTI-YEAR OVERLAPPING YoY WAVES (Months 1 to 12)]             |
|                      |   Lines: ── 2020  ── 2021  ── 2022  ── 2023  ── 2024                       |
|                      |                                                                            |
|                      | [SECTION 3: 12-MONTH CYCLICAL TRANSMISSION HEATMAP — Plotly Imshow]        |
|                      | Disease       | Jan | Feb | Mar | Apr | May | Jun | Jul | Aug | Sep | Oct...|
|                      | Dengue        | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [█] | [█] | [█] | [▓]  |
|                      | Malaria       | [ ] | [ ] | [ ] | [ ] | [ ] | [░] | [█] | [█] | [█] | [░]  |
|                      | Tuberculosis  | [▓] | [▓] | [▓] | [▓] | [▓] | [▓] | [▓] | [▓] | [▓] | [▓]  |
+----------------------+----------------------------------------------------------------------------+


### 2.3 Wireframe: UI-05 Advanced EDA & Outbreak Surveillance

+---------------------------------------------------------------------------------------------------+
|  [H1] ADVANCED EDA & SURVEILLANCE SURGE DETECTOR (pages/05_EDA_Statistics.py)                     |
+----------------------+----------------------------------------------------------------------------+
| SIDEBAR FILTERS      | [SECTION 1: URBAN CROWDING & DENSITY REGRESSION — Plotly Scatter + OLS]    |
| (Same Persistent     | Incidence/Lakh                                                             |
|  Session State)      |       ▲                                                                    |
|                      |   120 |                                       * Delhi (Density: 22,198)    |
|                      |    80 |                             * MH                                   |
|                      |    40 |                * WB     * TN                                       |
|                      |     0 +----------------------------------------------------> Density       |
|                      |         Pearson r = 0.84 | p-value < 0.001 | Strong Positive Correlation   |
|                      |                                                                            |
|                      | [SECTION 2: CONCURRENT OUTBREAK ANOMALY DETECTOR (>=2 Diseases in Surge)]  |
|                      | State       | Month-Year  | Surging Diseases           | Combined Caseload |
|                      | Delhi       | August 2021 | COVID-19, Dengue           | 14,890 (Alert)    |
|                      | Maharashtra | Sept 2022   | Dengue, Malaria, Typhoid   | 18,220 (Critical) |
+----------------------+----------------------------------------------------------------------------+


## 3. Global Layout Architecture & Color Palette

The visual system implements a healthcare-optimized corporate palette balancing high contrast, clinical trustworthiness, and accessible data visualization:


## 4. Visualization Selection Matrix per Operational Question

Theoretical justification for chart selection aligned with data visualization best practices:


## 5. Reusable UI Components Library (src/ui.py)

To guarantee design consistency across all six pages, common UI widgets are encapsulated inside src/ui.py. These methods programmatically construct Tailwind CSS HTML markup and render it via Streamlit's component engine:
1. inject_tailwind(): Silent pre-initialization of Tailwind CDN scripts.
2. render_header(title, subtitle): Generates responsive executive gradient banners.
3. render_kpi_card(label, value, delta, icon, color): Builds responsive metric tiles with percentage indicators.
4. render_insight_box(title, text, alert_type): Standardizes qualitative clinical takeaway callouts.

12_ArgJain_DiseaseTrendAnalysis_UIFramework.docx | v1.0 | ABES Engineering College | November 2026


---
### 📋 Embedded Data Tables


#### Table 1

| Project ID & Title | P-01 / Disease Trend Analysis |
| --- | --- |
| Domain | Healthcare Data Analytics |
| UI/UX Architect | Arg Jain (Roll No. 2500320140031) |
| Academic Program | MCA 2nd Year (Data Analytics Specialization) |
| Institution | ABES Engineering College, Ghaziabad |
| Faculty Mentor | Ms. Kalpana Dwivedi |
| Document Version | v1.0 |
| UI Tech Stack | Streamlit 1.35 Multi-Page + Tailwind CSS (CDN in iframe) + Plotly 5.22 |
| Total Application Screens | 6 Dedicated Analytical Screens (UI-01 to UI-06) |
| Release Date | November 2026 |



#### Table 2

| UI ID | Screen Title | File Route | Analytical Scope | Core Visual Components | Supported User Stories |
| --- | --- | --- | --- | --- | --- |
| UI-01 | Executive Overview & KPIs | pages/01_Overview.py | High-level epidemiological snapshot and state rankings | 4 Tailwind KPI cards, horizontal bar chart, state CFR table | US-04, US-05, US-06, US-07 |
| UI-02 | Longitudinal & Seasonal Trends | pages/02_Trends.py | Multi-year trajectory and monthly cyclic transmission | 60-month time series line, overlapping YoY lines, cyclic heatmap | US-08, US-09, US-10, US-11 |
| UI-03 | Regional Burden & Clinical Efficacy | pages/03_Regional_Analysis.py | Cross-state mortality and recovery rate benchmarking | Ranked state cases bar, CFR percentage bar, recovery vs CFR | US-12 |
| UI-04 | Demographic Cohort Drilldown | pages/04_Demographics.py | Age group and gender vulnerability profiles | Stacked age group bar chart, gender distribution donut/pie | US-13 |
| UI-05 | Advanced EDA & Surveillance | pages/05_EDA_Statistics.py | Crowding correlation and co-occurring outbreak alerts | Density vs incidence scatter (OLS line), outbreak alert table | US-14, US-15 |
| UI-06 | Data Quality Audit & Export | pages/06_Data_Quality.py | Pipeline transparency ledger and filtered dataset download | Cleaning scorecard ledger, null/dupe audits, CSV download trigger | US-16, US-17 |



#### Table 3

| Color Role | Hex Code | Visual Description | Application Point |
| --- | --- | --- | --- |
| Primary Dominant | #1A5376 | Deep Navy Blue | Application headers, table header rows, primary button fills, major axis labels |
| Secondary Accent | #2E86AB | Vibrant Sea Blue | Plotly line chart series, secondary button borders, sub-headings, filter borders |
| Clinical Success | #1E8B4C | Forest Emerald Green | High recovery percentages (>90%), negative/curbed outbreak deltas, valid status tags |
| Warning Attention | #E67E22 | Amber Ochre | Moderate CFR rates (2.0% - 4.0%), cautionary data quality indicators |
| Critical Danger | #C0392B | Crimson Red | High CFR (>4.0%), active outbreak anomaly alerts, mortality metrics |
| Background Canvas | #F0F8FF | Alice Blue Soft Grey | Global page background canvas behind visual containers |
| Card Surface | #FFFFFF | Pure Crisp White | KPI card backgrounds, Plotly chart container canvas, data tables |
| High-Contrast Text | #2C3E50 | Charcoal Slate | Primary typography body text, numerical figures, chart legends |



#### Table 4

| OQ ID | Operational Question | Primary Chart Type | Plotly Implementation | Visualization Rationale |
| --- | --- | --- | --- | --- |
| OQ-01 | 5-Year Case Increase | Multi-Series Line Chart | px.line(markers=True) | Continuous time series lines represent direction and magnitude of multi-year trajectories clearly. |
| OQ-02 | Regional State Rankings | Horizontal Bar Chart | px.bar(orientation='h') | Horizontal orientation allows clear reading of 10 long state labels without diagonal slant text. |
| OQ-03 | Monthly Cyclical Trend | Transmission Curve Line | px.line(x='month') | Connecting 12 monthly data points establishes immediate visual wave recognition. |
| OQ-04 | Demographic Cohorts | Stacked Demographic Bar | px.bar(barmode='stack') | Stacked bars illustrate total morbidity while simultaneously displaying age bracket proportions. |
| OQ-05 | Case Fatality Rate (CFR) | Bi-Dimensional Heatmap | px.imshow(color_continuous_scale) | Matrix heatmaps allow rapid cognitive scanning of 50 state-disease cells to identify dark hot spots. |
| OQ-06 | Density Correlation | Scatter Plot + Trendline | px.scatter(trendline='ols') | Scatter plotting reveals clustering and bivariate linearity; OLS regression line shows trajectory. |
| OQ-07 | Clinical Recovery Rates | Grouped Comparison Bar | px.bar(barmode='group') | Side-by-side grouped bars facilitate direct visual benchmarking between recovery and mortality. |
| OQ-08 | Concurrent Outbreaks | Bubble Scatter Alert Chart | px.scatter(size='cases') | Surfaces multi-disease overlap spikes as prominent visual clusters along the time axis. |
| OQ-09 | Year-over-Year Delta | Diverging Colored Table | st.dataframe(style.background_gradient) | Tabular representation with green/red gradient highlights negative vs positive trajectories. |
| OQ-10 | Peak Transmission Months | Monthly Intensity Heatmap | px.imshow(labels=dict(x='Month')) | 12 columns across 5 disease rows highlight the exact calendar month of maximum transmission. |

