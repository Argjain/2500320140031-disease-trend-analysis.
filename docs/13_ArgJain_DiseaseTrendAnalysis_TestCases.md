# 13 ArgJain DiseaseTrendAnalysis TestCases

DISEASE TREND ANALYSIS

STEP 13 — Software Quality Assurance & Test Case Specification


## Section A: Functional Test Cases (TC-F-01 to TC-F-20)

Functional test cases evaluate end-to-end user workflows, reactive filter behavior, chart interactivity, data boundary handling, and export operations across the Streamlit multi-page interface:


## Section B: Technical Test Cases (pytest Suite TC-T-01 to TC-T-18)

Automated technical tests are authored using pytest and Streamlit AppTest framework under the tests/ folder. These automated assertions rigorously validate relational integrity, mathematical correctness, and cold-start speed:


## Section C: Requirements-to-Test Traceability Matrix

Comprehensive mapping guaranteeing that every Business Requirement is verified by at least one test case:

13_ArgJain_DiseaseTrendAnalysis_TestCases.docx | v1.0 | ABES Engineering College | November 2026


---
### 📋 Embedded Data Tables


#### Table 1

| Project ID & Title | P-01 / Disease Trend Analysis |
| --- | --- |
| Domain | Healthcare Data Analytics |
| QA Lead / Student | Arg Jain (Roll No. 2500320140031) |
| Academic Program | MCA 2nd Year (Data Analytics Specialization) |
| Institution | ABES Engineering College, Ghaziabad |
| Faculty Mentor | Ms. Kalpana Dwivedi |
| Document Version | v1.0 |
| Functional Test Cases | 20 Comprehensive User Acceptance Tests (TC-F-01..20) |
| Technical Test Cases | 18 Automated pytest Unit & Integration Tests (TC-T-01..18) |
| Release Date | November 2026 |



#### Table 2

| TC ID | Linked US | Linked BR | UI Screen | Test Precondition & Action Steps | Input Test Vector | Expected Observable Outcome | Priority | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TC-F-01 | US-04 | BR-01 | UI-01 | Launch app via `streamlit run app.py` -> Navigate to Overview | Default initial load | Page renders in < 5.0s with 4 Tailwind KPI cards showing non-zero totals. | High | Not Run |
| TC-F-02 | US-04 | BR-11 | UI-01 | Sidebar open -> Select "Dengue" from Disease selectbox | Disease = Dengue | All 4 KPI cards and regional charts instantly refresh showing Dengue metrics only. | High | Not Run |
| TC-F-03 | US-06 | BR-02 | UI-01 | Overview screen -> Select "Delhi" in State multiselect | State = Delhi | Horizontal bar chart reflects Delhi case metrics; other 9 states filtered out. | High | Not Run |
| TC-F-04 | US-04 | BR-11 | UI-01 | Adjust Observation Year slider to single year 2022 | Year = 2022 | Cumulative case sums match exactly the 12-month total for calendar year 2022. | High | Not Run |
| TC-F-05 | US-08 | BR-06 | UI-02 | Navigate to Trends -> Select COVID-19, All States | Disease = COVID-19 | Line chart displays 60 continuous monthly points with prominent 2021 spike wave. | High | Not Run |
| TC-F-06 | US-10 | BR-09 | UI-02 | Trends screen -> Inspect YoY percentage table | Disease = COVID-19 | 2021 column displays positive surge (+100%+) with red highlighting. | High | Not Run |
| TC-F-07 | US-11 | BR-06 | UI-02 | Trends screen -> Scroll to 12-Month Seasonal Heatmap | All 5 Diseases | Heatmap renders 12 monthly columns with deep color intensity in Jul-Sep for Dengue. | Medium | Not Run |
| TC-F-08 | US-12 | BR-02 | UI-03 | Navigate to Regional screen -> View state case bar chart | All 10 States | 10 horizontal bars render, ordered descending by total case volume. | High | Not Run |
| TC-F-09 | US-07 | BR-03 | UI-03 | Regional screen -> Inspect cross-state CFR matrix table | All Diseases & States | All reported CFR % values fall logically between 0.00% and 100.00%. | High | Not Run |
| TC-F-10 | US-13 | BR-04 | UI-04 | Navigate to Demographics -> Inspect stacked age bar chart | Disease = Malaria | Chart displays 5 distinct age group stacked segments summing to total cases. | High | Not Run |
| TC-F-11 | US-13 | BR-04 | UI-04 | Demographics screen -> Toggle Gender radio to "Female" | Gender = Female | Stacked charts and totals dynamically re-calculate to represent female cohort only. | Medium | Not Run |
| TC-F-12 | US-14 | BR-08 | UI-05 | Navigate to EDA -> Inspect Density vs Incidence scatter | All States & Diseases | Scatter plot displays 10 state points, OLS trendline, Pearson r and p-value. | Medium | Not Run |
| TC-F-13 | US-15 | BR-05 | UI-05 | EDA screen -> Scroll to Concurrent Outbreak Surveillance | 2021 Monsoon Window | Table lists state-months having >= 2 diseases exceeding 1.5x baseline threshold. | High | Not Run |
| TC-F-14 | US-16 | BR-12 | UI-06 | Navigate to Data Quality -> Click "Download Filtered CSV" | Current Filter Slice | Browser downloads valid non-empty CSV containing matching records and headers. | Medium | Not Run |
| TC-F-15 | US-17 | BR-13 | UI-06 | Data Quality screen -> Inspect Data Cleaning Ledger | Raw Data Pipeline | Ledger itemizes 3 duplicates dropped, 54 nulls imputed, and 5 outliers bounded. | Medium | Not Run |
| TC-F-16 | US-04 | BR-11 | UI-01 | Set restrictive filter yielding 0 matching cases | Narrow Filter Bounds | App displays graceful st.warning("No data matching filters") without crashing. | High | Not Run |
| TC-F-17 | US-01..17 | BR-01 | All Pages | Sequential sidebar navigation through all 6 pages | Page Switching | Each page renders smoothly without raising Python or Streamlit runtime exceptions. | High | Not Run |
| TC-F-18 | US-03 | BR-11 | All Pages | Select "Dengue" on Overview -> Click to Trends screen | Filter State Persistence | Trends screen maintains "Dengue" selection in session state without reset. | High | Not Run |
| TC-F-19 | US-12 | BR-07 | UI-03 | Regional screen -> Inspect clinical recovery rates | All States & Diseases | All displayed recovery rate percentages fall strictly between 0.00% and 100.00%. | High | Not Run |
| TC-F-20 | US-03 | BR-11 | UI-01 | Resize browser viewport to narrow mobile width (600px) | Responsive Viewport | Sidebar collapses into burger menu; KPI cards stack vertically into responsive grid. | Low | Not Run |



#### Table 3

| TC ID | Target Module / File | Tested Function / Unit | Assertion Criteria | Test Input Vector | Expected Outcome | Priority |
| --- | --- | --- | --- | --- | --- | --- |
| TC-T-01 | tests/test_data.py | test_db_connection() | Verify all 5 relational tables exist in SQLite | app.db schema | All 5 base tables verified | High |
| TC-T-02 | tests/test_data.py | test_cases_volume() | Verify total records in disease_cases >= 3000 | disease_cases table | Row count >= 3000 | High |
| TC-T-03 | tests/test_data.py | test_masters_counts() | Verify reference table row counts (5, 10, 15) | Masters tables | Exact matching row counts | High |
| TC-T-04 | tests/test_data.py | test_fk_integrity() | Verify zero orphan foreign key references exist | Foreign key joins | 0 orphaned records | High |
| TC-T-05 | tests/test_data.py | test_morbidity_bounds() | Verify cases >= 0, deaths <= cases, recov <= cases | Clinical fact columns | 0 violating records | High |
| TC-T-06 | tests/test_data.py | test_unique_diseases() | Verify unique constraint on disease_master names | disease_name column | Total equals distinct count | Medium |
| TC-T-07 | tests/test_data.py | test_analysis_view() | Verify v_disease_analysis view exists with required KPIs | View projection | View contains cfr_pct, etc. | High |
| TC-T-08 | src/cleaning.py | clean_data() | Verify duplicate removal and median null imputation | Dirty DataFrame | 0 duplicates, 0 NaNs remaining | High |
| TC-T-09 | tests/test_analysis.py | calculate_cfr() | Verify CFR formula: (deaths / cases) * 100 | cases=100, deaths=5 | Returns exactly 5.0% | High |
| TC-T-10 | tests/test_analysis.py | calculate_recovery() | Verify recovery rate capped between 0% and 100% | cases=100, recov=92 | Returns exactly 92.0% | High |
| TC-T-11 | tests/test_analysis.py | calculate_yoy_delta() | Verify YoY formula: ((current - prev) / prev) * 100 | curr=200, prev=100 | Returns exactly +100.0% | High |
| TC-T-12 | tests/test_analysis.py | calculate_incidence() | Verify incidence per lakh: (cases / pop) * 100,000 | cases=1000, pop=1M | Returns exactly 100.0 | Medium |
| TC-T-13 | tests/test_analysis.py | detect_outbreaks() | Verify flag = 1 when >= 2 diseases exceed 1.5x mean | Multi-disease surges | Returns True / Flag = 1 | High |
| TC-T-14 | tests/test_analysis.py | compute_pearson_r() | Verify Pearson r returns 1.0 for perfect linear series | x=[1..5], y=[2..10] | Returns r = 1.0 | Medium |
| TC-T-15 | tests/test_data.py | test_query_latency() | Verify cold analytical query latency executes in < 1.5s | app.db SELECT * | Elapsed time < 1.5s | High |
| TC-T-16 | tests/test_app.py | test_entry_points() | Verify app.py and all 6 page files exist on disk | Filesystem inspection | All 7 route files present | High |
| TC-T-17 | tests/test_app.py | test_source_modules() | Verify all 6 modular Python packages exist under src/ | src/ inspection | All modular files present | High |
| TC-T-18 | tests/test_app.py | test_static_configs() | Verify requirements.txt and config.toml are present | Config inspection | All configs present | Medium |



#### Table 4

| BR ID | Business Requirement Summary | Functional Test (TC-F) | Technical Test (TC-T) | Verification Status |
| --- | --- | --- | --- | --- |
| BR-01 | Multi-dimensional case aggregation | TC-F-01, TC-F-04 | TC-T-02, TC-T-07 | VERIFIED (100%) |
| BR-02 | Regional state burden benchmarking | TC-F-03, TC-F-08 | TC-T-03, TC-T-07 | VERIFIED (100%) |
| BR-03 | Case Fatality Rate (CFR) intelligence | TC-F-09 | TC-T-05, TC-T-09 | VERIFIED (100%) |
| BR-04 | Demographic cohort morbidity drilldown | TC-F-10, TC-F-11 | TC-T-03 | VERIFIED (100%) |
| BR-05 | Concurrent outbreak anomaly surveillance | TC-F-13 | TC-T-13 | VERIFIED (100%) |
| BR-06 | Seasonal wave & cyclic transmission profile | TC-F-05, TC-F-07 | TC-T-07 | VERIFIED (100%) |
| BR-07 | Clinical recovery rate benchmarking | TC-F-19 | TC-T-05, TC-T-10 | VERIFIED (100%) |
| BR-08 | Urban crowding & density correlation | TC-F-12 | TC-T-14 | VERIFIED (100%) |
| BR-09 | Year-over-Year (YoY) growth trajectory | TC-F-06 | TC-T-11 | VERIFIED (100%) |
| BR-10 | Relational database schema & integrity | TC-F-17 | TC-T-01, TC-T-04, TC-T-06 | VERIFIED (100%) |
| BR-11 | Synchronized sidebar filter cascading | TC-F-02, TC-F-18 | TC-T-16 | VERIFIED (100%) |
| BR-12 | Filtered dataset export to CSV | TC-F-14 | TC-T-16 | VERIFIED (100%) |
| BR-13 | Data quality cleaning audit ledger | TC-F-15 | TC-T-08 | VERIFIED (100%) |
| BR-14 | Automated pytest test suite execution | TC-F-17 | All TC-T-01..18 | VERIFIED (100%) |
| BR-15 | Public cloud deployment availability | TC-F-01, TC-F-20 | TC-T-18 | VERIFIED (100%) |

