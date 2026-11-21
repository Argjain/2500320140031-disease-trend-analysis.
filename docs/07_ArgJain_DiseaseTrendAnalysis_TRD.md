# 07 ArgJain DiseaseTrendAnalysis TRD

DISEASE TREND ANALYSIS

STEP 7 — Technical Requirements Document (TRD)


## 1. System Architecture & End-to-End Data Pipeline

The Disease Trend Analysis system is designed following a modular multi-tier data analytics architecture. The pipeline cleanly separates the relational storage tier, caching data ingestion layer, idempotent data cleaning engine, vectorized statistical analytics module, Tailwind UI component rendering layer, and reactive multi-page presentation screens.


### 1.1 Architecture Flowchart (Mermaid Representation)

graph TD
    A[data/app.db (SQLite)] -->|SQL Query| B[src/data_loader.py (@st.cache_data)]
    B -->|Raw DataFrame| C[src/cleaning.py (Impute, Dedupe, Cap Outliers)]
    C -->|Cleaned DataFrame + Quality Report| D[src/analysis.py (CFR, YoY, Seasonality, Stats)]
    D -->|Aggregated Data & Metrics| E[app.py (Shared Sidebar Filters & Session State)]
    E -->|Filtered State & Slices| F1[pages/01_Overview.py (KPI Cards & Bar Chart)]
    E -->|Filtered State & Slices| F2[pages/02_Trends.py (Time-series & Heatmap)]
    E -->|Filtered State & Slices| F3[pages/03_Regional_Analysis.py (CFR & Recovery)]
    E -->|Filtered State & Slices| F4[pages/04_Demographics.py (Age & Gender Stacked)]
    E -->|Filtered State & Slices| F5[pages/05_EDA_Statistics.py (Correlation & Outbreak)]
    E -->|Filtered State & Slices| F6[pages/06_Data_Quality.py (Audit & CSV Export)]
    G[src/ui.py (Tailwind CDN in iframe)] -.->|CSS Classes & Cards| F1 & F2 & F3 & F4 & F5 & F6


### 1.2 Pipeline Component Responsibilities

1. Relational Persistence (data/app.db): SQLite database enforcing PK/FK relationships, domain check constraints, and denormalized analytical views.
2. Ingestion & Cache (src/data_loader.py): Connects using sqlite3, executes indexed analytical queries, and caches results via @st.cache_data(ttl=3600).
3. Cleaning Pipeline (src/cleaning.py): Drops exact duplicate rows, imputes missing counts via median/zero, caps extreme outlier spikes, and generates an audit dictionary.
4. Analytical Engine (src/analysis.py): Pure Python/pandas/SciPy mathematical functions computing epidemiological metrics with zero UI dependencies.
5. UI Component Library (src/ui.py): Renders Tailwind CSS styled KPI stat cards, alert callouts, and header components through Streamlit iframe components.
6. Presentation Tier (app.py and pages/): Native Streamlit multi-page layout rendering Plotly interactive visualizations with responsive column grids.


## 2. Folder Structure & Physical Organization

2500320140031-disease-trend-analysis/
├── app.py                     # Main application entry point & shared session state
├── requirements.txt           # Pinned dependency manifest
├── BUILD_PLAN.md              # Machine-actionable build roadmap
├── README.md                  # Installation, testing & deployment guide
├── .gitignore                 # Excludes .venv, __pycache__, temporary caches
├── .streamlit/
│   └── config.toml            # Application theme (colors, fonts, layout settings)
├── src/
│   ├── __init__.py            # Package initializer
│   ├── data_loader.py         # SQLite connection & cached queries
│   ├── cleaning.py            # Data sanitization, imputation & outlier bounds
│   ├── analysis.py            # Epidemiological & statistical analysis routines
│   ├── ui.py                  # Tailwind iframe components & visual cards
│   └── generate_data.py       # Deterministic synthetic data generator (seed 42)
├── pages/
│   ├── 01_Overview.py         # Executive KPI dashboard & regional case rankings
│   ├── 02_Trends.py           # Longitudinal time-series & seasonal heatmaps
│   ├── 03_Regional_Analysis.py# Cross-state CFR benchmarking & recovery rates
│   ├── 04_Demographics.py      # Age cohort & gender distribution profiles
│   ├── 05_EDA_Statistics.py   # Density scatter correlation & co-occurrence surveillance
│   └── 06_Data_Quality.py     # Pipeline cleaning audit ledger & raw CSV export
├── data/
│   ├── app.db                 # SQLite relational database file
│   ├── disease_cases.csv      # Flat CSV export of primary fact table
│   ├── region_master.csv      # State reference metadata & census population
│   ├── disease_master.csv     # Disease taxonomic taxonomy & incubation stats
│   ├── demographic_group.csv  # Age & gender cohort master definitions
│   └── disease_trend_analysis_data.xlsx # Multi-tab complete spreadsheet
├── tests/
│   ├── __init__.py            # Test suite package initializer
│   ├── test_data.py           # Database schema, row count & FK constraint tests
│   ├── test_analysis.py       # Pure mathematical assertions on analytical formulas
│   └── test_app.py            # Streamlit AppTest integration & UI smoke tests
└── docs/                      # All 18 formal project step deliverables (.docx, .xlsx)


## 3. Functional Requirements Register

Engineering implementation specifications mapped directly to source Business Requirements:


## 4. Non-Functional Requirements (NFR-01 to NFR-08)

System quality attributes and architectural service level objectives:


## 5. Data Ingestion, Caching & Cleaning Pipeline


### 5.1 Relational Data Ingestion & Caching Strategy

Data loading is orchestrated via src/data_loader.py using standard library sqlite3. To optimize Streamlit Cloud runtime performance, the primary loading function is wrapped in Streamlit's cache manager: @st.cache_data(ttl=3600, show_spinner="Loading epidemiological repository..."). The loader connects to Path(__file__).parent.parent / "data" / "app.db", executes a validated multi-table JOIN across disease_cases, disease_master, and region_master, and returns a high-performance pandas DataFrame.


### 5.2 Data Sanitization Pipeline (src/cleaning.py)

The cleaning module executes four idempotent operations upon raw DataFrame ingestion:
1. Deduplication: Invokes df.drop_duplicates() to purge redundant transactional case rows introduced during batch ingestion.
2. Missing Value Imputation: Imputes missing cases_reported using median disease-state values. Imputes missing deaths with 0.
3. Outlier Capping (Winsorization): Identifies extreme typographical errors using Interquartile Range (IQR). Cases exceeding Q3 + 3.0 * IQR are capped to boundary values.
4. Audit Metric Accounting: Returns a quality report dictionary capturing original_rows, duplicates_removed, nulls_filled, outliers_capped, and final_rows.


## 6. Statistical & Mathematical Formulation per Operational Question

Formal mathematical definition and algorithmic approach for resolving each Operational Question:


## 7. User Interface Framework & Tailwind Styling


### 7.1 Theme Configuration (.streamlit/config.toml)

[theme]
primaryColor = "#1A5376"            # Deep Navy Blue
backgroundColor = "#F0F8FF"         # Clean Alice Blue
secondaryBackgroundColor = "#E8F4FD"# Soft Sky Blue (Sidebar & Containers)
textColor = "#2C3E50"                # High-contrast Slate Grey
font = "sans serif"                  # Modern sans-serif typography


### 7.2 Tailwind CSS Injection via iframe Architecture

While Streamlit does not natively compile external CSS frameworks into its shadow DOM, our architecture injects Tailwind CSS (via CDN) into isolated Streamlit HTML components: st.components.v1.html(..., height=...). This pattern is leveraged in src/ui.py for two signature UI elements:
1. Global Application Header: Displays an executive gradient header banner with program title and subtitle.
2. Executive KPI Summary Cards: Generates responsive card layouts utilizing Tailwind utility classes (e.g., "bg-white rounded-xl shadow-md p-4 border-t-4 border-blue-900 text-center") rendering icons, metric labels, prominent numerical values, and percentage deltas.


### 7.3 Persistent Sidebar Filter State Architecture

All filter widgets (Disease selectbox, State multiselect, Year slider, Age multiselect, Gender radio) are bound to Streamlit session state keys (st.session_state.selected_disease, etc.). When navigating between pages (01_Overview through 06_Data_Quality), session state remains persistent, ensuring that user filtering context is maintained seamlessly across analytical perspectives.


## 8. Performance Optimization, Fault Tolerance & Security


### 8.1 Performance Optimization Strategy

* Vectorized DataFrame Operations: All percentage ratios and groupings execute via C-optimized pandas vectorized methods, avoiding slow Python iterrows() loops.
* Granular Memory Management: Downcast numerical metrics (e.g., integer year to int16, case counts to int32) to maintain entire dataset memory footprint under 25 MB.
* Selective Plotly Figure Rendering: Restrict rendered data points per chart to aggregated state/month levels rather than raw row-level vectors, guaranteeing 60 fps rendering.

### 8.2 Exception Handling & Graceful Degradation

* Database Connection Safeguards: Wrap all sqlite3 operations in structured try/except blocks. If database file is missing, app renders st.error() with guidance to run src/generate_data.py.
* Zero Division Protection: All ratio formulas (deaths/cases, recovered/cases) apply pandas .fillna(0.0) and numpy division guards to prevent NaN/Infinity display errors.
* Empty Query State Handling: If narrow sidebar filter combinations yield 0 matching rows, pages render an informative st.warning("No case data matching selected filters.") rather than crashing.

### 8.3 Security & Statutory Compliance

* Zero Identifiable Health Data (PII): Entire repository operates on synthetically generated epidemiological records; completely compliant with HIPAA, DISHA, and DPDP 2023 regulations.
* Zero Credential Footprint: App uses local embedded SQLite storage and free public hosting; zero cloud access keys, database passwords, or JWT secrets exist in repository history.
* File System Isolation: Database access is strictly read-only during application runtime; all analytical views are generated in-memory without write back.

## 9. Pinned Dependency Manifest (requirements.txt)

To prevent cloud deployment build breakages caused by upstream library releases, all dependencies are strictly pinned:

streamlit==1.35.0
pandas==2.2.2
numpy==1.26.4
plotly==5.22.0
scipy==1.13.0
statsmodels==0.14.2
openpyxl==3.1.2
python-docx==1.2.0
pytest==8.2.0
pytest-cov==5.0.0


## 10. Technical Risk Register & Remediation

Identified technical risks and pre-engineered architectural mitigations:

07_ArgJain_DiseaseTrendAnalysis_TRD.docx | v1.0 | ABES Engineering College | November 2026


---
### 📋 Embedded Data Tables


#### Table 1

| Project ID & Title | P100 / Disease Trend Analysis |
| --- | --- |
| Domain | Healthcare Data Analytics |
| Student Architect | Arg Jain (Roll No. 2500320140031) |
| Academic Program | MCA 2nd Year (Data Analytics Specialization) |
| Institution | ABES Engineering College, Ghaziabad |
| Faculty Mentor | Mr. Dinesh |
| Document Version | v1.0 (Baseline Architecture) |
| Technical Stack | Python 3.12 / Streamlit 1.35 / SQLite / Plotly 5.22 / pytest 8.2 |
| Deployment Target | Streamlit Community Cloud (Free Tier) |
| Release Date | November 2026 |



#### Table 2

| FR ID | Technical Requirement | Linked BR | Target Module | Implementation Method |
| --- | --- | --- | --- | --- |
| FR-01 | Load multi-table joined disease dataset from SQLite with caching | BR-10 | src/data_loader.py | sqlite3 connection + @st.cache_data(ttl=3600) |
| FR-02 | Synchronize global sidebar filter selections across all sub-pages | BR-11 | app.py / src/data_loader.py | st.session_state filter binding with persistent state keys |
| FR-03 | Compute multi-year annual and monthly case frequency aggregations | BR-01 | src/analysis.py | df.groupby(['disease_name', 'report_year'])['cases_reported'].sum() |
| FR-04 | Generate sorted state-level case burden rankings | BR-02 | src/analysis.py | Groupby region_name, sort descending, render px.bar(orientation='h') |
| FR-05 | Calculate matrix of Case Fatality Rates (CFR) across state-disease pairs | BR-03 | src/analysis.py | (deaths / cases_reported * 100).fillna(0.0), render px.imshow |
| FR-06 | Disaggregate cases across 5 age brackets and 3 gender identities | BR-04 | src/analysis.py | Pivot table on demographic_breakdown, render px.bar(barmode='stack') |
| FR-07 | Identify co-occurring outbreak anomalies across regional temporal cells | BR-05 | src/analysis.py | Flag cells where count(diseases > 1.5 * historical_mean) >= 2 |
| FR-08 | Construct 12-month cyclical transmission profiles per disease | BR-06 | src/analysis.py | Groupby report_month (1-12) mean cases, render px.imshow & px.line |
| FR-09 | Compute clinical recovery percentages per state and disease | BR-07 | src/analysis.py | (recovered / cases_reported * 100).clip(0, 100), render px.bar |
| FR-10 | Calculate Pearson correlation coefficient between density and incidence | BR-08 | src/analysis.py | scipy.stats.pearsonr(incidence_per_lakh, population_density) |
| FR-11 | Generate year-over-year percentage delta matrix across consecutive years | BR-09 | src/analysis.py | Annual sum pivot table + pct_change(axis=1) * 100 |
| FR-12 | Render responsive executive KPI cards (Cases, Deaths, Recoveries, CFR) | BR-01, BR-11 | pages/01_Overview.py | render_kpi_card() HTML generation inside st.columns(4) |
| FR-13 | Render 6 interactive, responsive Plotly visual analytics chart types | BR-02..09 | pages/*.py | Plotly Express (px.line, px.bar, px.imshow, px.scatter, px.pie) |
| FR-14 | Generate downloadable filtered CSV extract via one-click UI trigger | BR-12 | pages/06_Data_Quality.py | st.download_button(data=df.to_csv(index=False), mime='text/csv') |
| FR-15 | Render visual data cleaning accounting ledger (initial vs clean metrics) | BR-13 | pages/06_Data_Quality.py | Tabular render of quality_report dictionary metrics |



#### Table 3

| NFR ID | Category | Target Objective | Target Threshold | Verification Method |
| --- | --- | --- | --- | --- |
| NFR-01 | Performance | Initial application cold-start and database load | < 5.0 seconds | Automated timer on Streamlit Community Cloud URL |
| NFR-02 | Performance | Visual chart re-render upon sidebar filter mutation | < 2.0 seconds | Manual browser developer tools profiling |
| NFR-03 | Reliability | Automated test suite code coverage | >= 80.0% Line Coverage | pytest --cov=src execution report |
| NFR-04 | Reliability | Critical computational or rendering regression failures | 0 Failures | pytest -q test execution output |
| NFR-05 | Usability | All 10 OQs resolvable without requiring external documentation | 10 / 10 OQs (100%) | Interactive mentor usability audit walkthrough |
| NFR-06 | Maintainability | Maximum functional code complexity per method | < 50 lines of code | Static analysis code review inspection |
| NFR-07 | Data Privacy | Absolute elimination of real patient personal identifiers (PII) | 0 PII records (100% Synthetic) | Synthetic dataset schema validation audit |
| NFR-08 | Availability | Public platform availability during semester evaluation window | >= 99.0% Uptime | Uptime monitoring over final 2 academic weeks |



#### Table 4

| OQ ID | Analytical Question | Mathematical Formulation | Python Implementation | Visualization Engine |
| --- | --- | --- | --- | --- |
| OQ-01 | 5-Year Case Growth | Delta = Sum(Cases_2024) - Sum(Cases_2020) | df.groupby(['disease', 'year']).sum() | px.line (Multi-series time trend) |
| OQ-02 | Geographic Hotspots | Rank(State) = Descending(Sum(Cases)) | df.groupby('region').sum().sort_values() | px.bar (Horizontal ranked bar chart) |
| OQ-03 | Monthly Cyclical Trend | Index(m) = Mean(Cases in month m, 2020-2024) | df.groupby('report_month').mean() | px.line (12-month cyclic transmission wave) |
| OQ-04 | Demographic Cohorts | Cases(age, gender) / Total_Cases * 100 | df.pivot_table(index='age', cols='gender') | px.bar (Stacked demographic bar chart) |
| OQ-05 | Case Fatality Rate | CFR = (Deaths / Cases_Reported) * 100 | (df['deaths'] / df['cases'] * 100).fillna(0) | px.imshow (Disease x Region CFR heatmap) |
| OQ-06 | Density Correlation | r = Cov(Incidence, Density) / (Sigma_x * Sigma_y) | scipy.stats.pearsonr(inc_rate, pop_density) | px.scatter (Trendline OLS regression) |
| OQ-07 | Clinical Recovery Rate | Recov% = (Recovered / Cases_Reported) * 100 | (df['recovered'] / df['cases'] * 100).clip(0,100) | px.bar (Grouped Recovery vs CFR comparison) |
| OQ-08 | Concurrent Outbreaks | Flag = 1 if Count(Diseases > 1.5 * Mean) >= 2 | df.groupby(['region','date']).apply(check_surge) | px.scatter (Alert timeline bubble chart) |
| OQ-09 | YoY Growth Trajectory | YoY% = (Cases_t - Cases_t-1) / Cases_t-1 * 100 | annual_pivot.pct_change(axis=1) * 100 | st.dataframe (Diverging colored table) |
| OQ-10 | Peak Transmission Month | Peak_Month = ArgMax_m(Mean(Cases_m)) | df.groupby('report_month')['cases'].mean().idxmax() | px.imshow (Month x Disease intensity heatmap) |



#### Table 5

| Risk ID | Technical Risk Factor | Probability | Impact | Architectural Remediation |
| --- | --- | --- | --- | --- |
| TR-01 | SQLite Concurrency Locking on Cloud | Low | Medium | Application executes strictly read-only SELECT queries; @st.cache_data prevents repeated file reads. |
| TR-02 | Tailwind CDN Outage during Evaluation | Low | Low | src/ui.py includes inline CSS fallbacks so KPI cards render cleanly even without external CDN connection. |
| TR-03 | Cold-Start Latency on Streamlit Cloud | Medium | Medium | Aggregated summaries pre-indexed in SQLite views; @st.cache_data ensures instant subsequent page loads. |
| TR-04 | Plotly Library Memory Overhead | Low | Medium | Chart rendering leverages Plotly Express with native WebGL rendering for responsive performance. |
| TR-05 | Relative Path Resolution Failure on Cloud | Medium | High | All file lookups use Path(__file__).resolve().parent rather than fragile working directory paths. |

