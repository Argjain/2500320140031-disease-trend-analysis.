# 14 ArgJain DiseaseTrendAnalysis BuildPlan

DISEASE TREND ANALYSIS

STEP 14 — Master Engineering Build Plan & Roadmap


## 1. Project Summary & Architectural Objective

The Disease Trend Analysis project delivers an end-to-end, interactive epidemiological web application built for public health officers, hospital administrators, epidemiologists, and policy makers in India. Operating on a 5-year observation baseline (2020–2024) across 10 representative Indian states, the solution analyzes morbidity and mortality across 5 high-impact contagious diseases: Dengue, Malaria, Tuberculosis, COVID-19, and Typhoid. The platform addresses 10 core Operational Questions (OQ-01..10) by integrating a normalized SQLite repository, cached query loaders, automated data cleaning, pure mathematical analysis routines, Tailwind-styled metric cards, and responsive Plotly visual analytics.


## 2. Master Build Tasks Register (BUILD-01 to BUILD-14)

Engineering implementation tasks ordered sequentially from infrastructure to deployment:


## 3. Definition of Done (DoD) & Standard Operating Commands

* Complete Functional Coverage: All 15 Business Requirements (BR-01..15) and 10 OQs demonstrable in live demo.
* Test Suite Execution: Automated pytest suite executes with 100% pass rate and zero critical computational regressions.
* Sub-Second Rendering: All charts and KPI metrics render within 2.0 seconds upon filter modification.
* Relational Integrity: SQLite database enforces all PK, FK, and domain CHECK constraints with zero orphaned rows.
* Documentary Completeness: All 18 formal project step deliverables finalized and organized in the docs/ folder.
* Public Hosting Availability: Application deployed to Streamlit Community Cloud with public HTTPS URL.

### Standard Operational CLI Commands

# 1. Environment initialization
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

# 2. Re-generate synthetic data repository
python src/generate_data.py

# 3. Execute automated test suite
python -m pytest tests/ -q --tb=short

# 4. Launch interactive Streamlit application
streamlit run app.py


## 4. Viva Voce Defense Preparation (10 Anticipated Questions)

Concise architectural justifications for formal academic evaluation:

14_ArgJain_DiseaseTrendAnalysis_BuildPlan.docx | v1.0 | ABES Engineering College | November 2026


---
### 📋 Embedded Data Tables


#### Table 1

| Project ID & Title | P-01 / Disease Trend Analysis |
| --- | --- |
| Domain | Healthcare Data Analytics |
| Engineering Lead / Student | Arg Jain (Roll No. 2500320140031) |
| Academic Program | MCA 2nd Year (Data Analytics Specialization) |
| Institution | ABES Engineering College, Ghaziabad |
| Faculty Mentor | Ms. Kalpana Dwivedi |
| Document Version | v1.0 |
| Actionable Build Tasks | 14 Engineering Tasks (BUILD-01 to BUILD-14) |
| Target Environment | Python 3.12 / Streamlit 1.35 / SQLite / Streamlit Cloud |
| Release Date | November 2026 |



#### Table 2

| Build ID | Task Goal & Scope | Target Files Affected | Supported Stories / Features | Verification Command / Check | Governing Tests |
| --- | --- | --- | --- | --- | --- |
| BUILD-01 | Environment setup & manifest pinning | requirements.txt, .gitignore, .streamlit/config.toml | N/A / Tech Foundation | Files exist with exact pinned libraries | TC-T-18 |
| BUILD-02 | Deterministic synthetic data generation | src/generate_data.py, data/app.db, data/*.csv | US-01 / FR-01 | `python src/generate_data.py` -> 100% checks pass | TC-T-01..07 |
| BUILD-03 | Cached SQLite data loader implementation | src/data_loader.py | US-01 / FR-01 | `load_data()` queries view, caches via @st.cache_data | TC-T-01, 15 |
| BUILD-04 | Idempotent data cleaning pipeline | src/cleaning.py | US-02 / FR-01 | Purges 3 dupes, imputes 54 nulls, caps 5 outliers | TC-T-08 |
| BUILD-05 | Epidemiological analytical calculation engine | src/analysis.py | US-07..15 / FR-03..11 | Implements CFR, recovery, YoY, seasonal, correlation | TC-T-09..14 |
| BUILD-06 | Tailwind CSS component library | src/ui.py | US-04 / UI Foundation | Renders header, metric stat cards, and insight boxes | TC-F-01 |
| BUILD-07 | Root entry point & sidebar session state | app.py | US-03 / FR-02 | Global page config, persistent sidebar filter state | TC-F-17, 18 |
| BUILD-08 | Screen UI-01: Executive Overview | pages/01_Overview.py | US-04..07 / FR-12 | Renders 4 Tailwind KPI cards, regional case bar, CFR table | TC-F-01..04 |
| BUILD-09 | Screen UI-02: Longitudinal Trends | pages/02_Trends.py | US-08..11 / FR-03, 08 | Renders 60-month line, multi-year YoY, seasonal heatmap | TC-F-05..07 |
| BUILD-10 | Screen UI-03: Regional Burden & Recovery | pages/03_Regional_Analysis.py | US-12 / FR-04, 05 | Renders state burden rankings, CFR bar, recovery rates | TC-F-08, 09, 19 |
| BUILD-11 | Screen UI-04: Demographic Cohort Profiles | pages/04_Demographics.py | US-13 / FR-06 | Renders stacked age group bars and gender donut chart | TC-F-10, 11 |
| BUILD-12 | Screen UI-05: Advanced EDA & Outbreak Alerts | pages/05_EDA_Statistics.py | US-14, 15 / FR-07, 10 | Density scatter regression (r & p), outbreak anomaly table | TC-F-12, 13 |
| BUILD-13 | Screen UI-06: Data Quality Audit & Export | pages/06_Data_Quality.py | US-16, 17 / FR-14, 15 | Cleaning ledger scorecard, CSV dataset download trigger | TC-F-14, 15 |
| BUILD-14 | Test suite verification & deployment guide | tests/*.py, README.md, Deploy Doc | All US / BR-14, 15 | Full test suite executes with 100% pass | All TC-T-01..18 |



#### Table 3

| # | Anticipated Viva Question | Model Answer & Technical Justification |
| --- | --- | --- |
| 1 | Why choose SQLite over PostgreSQL for this application? | SQLite is an embedded, zero-configuration engine stored directly as data/app.db. For an analytical volume of 3,000–50,000 records, SQLite combined with Streamlit in-memory caching (@st.cache_data) provides sub-millisecond query responses with zero cloud database hosting costs. |
| 2 | How is Case Fatality Rate (CFR) defined, and how do you prevent divide-by-zero crashes? | CFR is defined as (Deaths / Confirmed Cases) * 100. Divide-by-zero errors are prevented using SQL NULLIF(cases, 0) and Python zero-guards, returning exactly 0.00% when zero cases are reported. |
| 3 | What epidemiological patterns were synthetically engineered into the data? | Five authentic patterns were embedded: (1) Monsoon surges in Dengue and Malaria (Jul-Sep); (2) Severe COVID-19 pandemic wave in 2021; (3) Higher incidence in high-density urban hubs (Delhi, Maharashtra); (4) Elevated CFR in elderly demographics (60+); and (5) Endemic Tuberculosis persistence in UP and Bihar. |
| 4 | What performance benefit does @st.cache_data provide? | It memoizes data loading and cleaning in RAM for 1 hour (ttl=3600). Subsequent user filter mutations or page navigation bypass SQLite disk queries entirely, reducing latency from 1.5s to < 0.05s. |
| 5 | How does the application maintain filter context when switching pages? | Filters are stored in st.session_state dictionary keys (e.g., st.session_state.selected_disease). Because session state persists throughout the user session, all 6 sub-pages inherit identical active filter context without state loss. |
| 6 | Why combine Streamlit with Tailwind CSS via iframe? | Streamlit generates rapid interactive data science visualizations, while Tailwind CSS injects polished corporate UI aesthetics (rounded cards, soft shadows, accent borders) via isolated st.components.v1.html iframe containers. |
| 7 | How is a "Concurrent Outbreak" algorithmically detected in Step 15? | An analytical function evaluates each state-month. If two or more independent disease entities simultaneously exceed 1.5x of their historical monthly baseline, an alert flag (is_outbreak = 1) is triggered. |
| 8 | What data quality issues were introduced, and how does the pipeline clean them? | We injected 54 null cases (median imputed), 28 null deaths (zero imputed), 5 typography outlier spikes (bounded to Q3 + 3.0 * IQR), and 3 duplicate records (purged via drop_duplicates). |
| 9 | How is urban density correlation evaluated in OQ-06? | We compute the Pearson correlation coefficient (r) and two-tailed p-value between state population density (persons/sq km) and normalized disease incidence per 100,000 residents using scipy.stats.pearsonr. |
| 10 | How does the architecture protect patient data privacy? | Zero real patient data is utilized. The entire dataset is algorithmically synthesized using deterministic statistical distributions conforming strictly to HIPAA, DISHA, and DPDP 2023 regulations. |

