# 03 ArgJain DiseaseTrendAnalysis NeedsAnalysis

DISEASE TREND ANALYSIS

STEP 3 — Needs Analysis & Business Requirements (BR)


## 1. Introduction & Methodology

A Needs Analysis bridges user pain points discovered during design thinking (Step 2 HMW Statements) and functional architecture. For every HMW statement, we ask: "What does the stakeholder NEED to make this possible?" Each requirement is formally expressed in the standardized business requirement syntax: "The business needs to <capability> so that <benefit>." Importantly, this document focuses strictly on WHAT capabilities the business requires, completely agnostic of technical implementation (no SQL, Streamlit, or programming constructs).


## 2. Business Requirements Register

The 15 business requirements below have been prioritized using MoSCoW methodology (9 Must Have = 60%, 4 Should Have = 27%, 2 Could Have = 13%). Every requirement is directly traceable back to its originating HMW statement.


## 3. Data Elements Required per Requirement

Each business requirement depends on specific data attributes from the healthcare data model:


## 4. Traceability & Gap Analysis

To guarantee end-to-end alignment, a bidirectional traceability audit was conducted between HMW statements, Business Requirements, and the 10 Operational Questions:


## 5. MoSCoW Priority Distribution

The requirements prioritization ensures delivery of a robust Minimum Viable Product (MVP) while clearly defining subsequent enhancements:

03_ArgJain_DiseaseTrendAnalysis_NeedsAnalysis.docx | v1.0 | ABES Engineering College | November 2026


---
### 📋 Embedded Data Tables


#### Table 1

| Project ID | P-01 |
| --- | --- |
| Project Title | Disease Trend Analysis |
| Domain | Healthcare Data Analytics |
| Student Name | Arg Jain |
| Roll Number | 2500320140031 |
| Academic Program | MCA 2nd Year (Data Analytics Specialization) |
| Institution | ABES Engineering College, Ghaziabad |
| Faculty Mentor | Ms. Kalpana Dwivedi |
| Document Version | v1.0 |
| Date | November 2026 |



#### Table 2

| BR ID | Business Requirement | Stakeholder | Source HMW | Priority | Measurement Criterion |
| --- | --- | --- | --- | --- | --- |
| BR-01 | The business needs to aggregate disease case counts by disease entity, geographical region, and temporal period so that health officers can detect emerging outbreak trends early. | SH-01, SH-03 | HMW-01, HMW-09 | Must | Verified in demo: user can select any combination of disease, state, and year to see correct aggregated case counts matching raw sums. |
| BR-02 | The business needs to compare disease burden across states on a common scale so that hospital administrators can anticipate inter-state patient surge patterns. | SH-02 | HMW-02 | Must | Regional ranking display accurately orders all 10 states by total incidence for any selected disease. |
| BR-03 | The business needs to compute and display Case Fatality Rates (CFR) across diseases and regions so that policy makers can identify high-mortality zones and justify emergency resource deployment. | SH-03 | HMW-03 | Must | CFR percentage matches (Deaths / Cases * 100) across all disease-region pairs; 0 division handled gracefully without error. |
| BR-04 | The business needs to segment disease morbidity by age bracket and gender cohort so that epidemiologists can identify demographic vulnerability profiles. | SH-04 | HMW-04 | Must | Demographic breakdown displays distribution across 5 age groups and 3 gender categories with totals reconciling to overall cases. |
| BR-05 | The business needs to detect and flag concurrent outbreaks where multiple diseases cross threshold levels simultaneously in the same region and time frame so that response teams avoid overwhelmed local healthcare capacity. | SH-01, SH-04 | HMW-05 | Must | Co-occurrence analysis correctly identifies region-months having two or more diseases exceeding 1.5x regional historical mean. |
| BR-06 | The business needs to profile monthly and seasonal variations in disease incidence so that medical supply chains can pre-position therapeutics ahead of peak months. | SH-01, SH-04 | HMW-06 | Must | Seasonal profile reveals peak transmission months for each disease (e.g., monsoon peak for vector-borne diseases). |
| BR-07 | The business needs to compute recovery percentages per disease and region so that hospital networks can benchmark clinical recovery efficacy against regional averages. | SH-02 | HMW-07 | Must | Recovery rate matches (Recoveries / Cases * 100); all reported values fall between 0.0% and 100.0%. |
| BR-08 | The business needs to evaluate the correlation between disease incidence rate and population density so that researchers can quantify the impact of urban crowding on transmission. | SH-04 | HMW-08 | Should | Displays scatter correlation with calculated Pearson correlation coefficient (r) and statistical p-value. |
| BR-09 | The business needs to calculate year-over-year (YoY) percentage changes in reported cases per disease so that ministries can assess multi-year disease growth or containment. | SH-03 | HMW-09 | Should | YoY percentage change table accurately computes ((Cases_Yr - Cases_Yr-1) / Cases_Yr-1 * 100) for all consecutive year pairs. |
| BR-10 | The business needs to maintain disease intelligence in a standardized, relational data store so that analytical queries are consistent, auditable, and reproducible. | SH-05 | HMW-10 | Must | Relational data repository passes primary key, foreign key, not null, and non-negative integrity validations. |
| BR-11 | The business needs synchronized multidimensional filtering (disease, region, year, age, gender) that updates all visual perspectives concurrently so that analytical exploration is fluid. | SH-01..04 | HMW-01..05 | Must | Applying a filter instantly cascades to all operational views and charts without page reload or state loss. |
| BR-12 | The business needs to export filtered analytical datasets into standard spreadsheet formats so that researchers can conduct specialized external epidemiological modeling. | SH-04, SH-05 | HMW-10 | Should | Export action produces a valid, non-empty CSV/Excel file containing exactly the subset of records active in the current filter state. |
| BR-13 | The business needs a transparent data quality accounting ledger showing cleaning interventions (missing values imputed, duplicates removed, outliers bounded) so that data integrity is demonstrable. | SH-05 | HMW-10 | Could | Data quality screen itemizes initial row count, duplicates purged, nulls resolved, and outliers capped. |
| BR-14 | The business needs comprehensive automated verification test suites covering data ingestion, KPI calculations, and interface responsiveness so that operational errors are caught prior to evaluation. | SH-06 | All HMWs | Must | Test suite executes with >= 80% coverage and zero critical calculation failures. |
| BR-15 | The business needs the analytical platform hosted on an accessible cloud platform with public access so that evaluating mentors and external reviewers can inspect the system remotely. | SH-05, SH-06 | OBJ-04 | Should | Platform URL is publicly reachable over HTTPS with 99% availability during evaluation period. |



#### Table 3

| BR ID | Required Data Entities & Attributes | Domain Type | Granularity |
| --- | --- | --- | --- |
| BR-01 | Disease Name, State/Region Name, Report Date, Report Year, Case Count | Epidemiological / Geospatial | Monthly per State & Disease |
| BR-02 | State Name, State Code, Geographic Zone, Case Count, Normalised Incidence | Geospatial / Clinical | Aggregated per State |
| BR-03 | Disease Name, Region Name, Cases Reported, Deaths Reported, CFR Calculated | Clinical Outcome | Monthly per Disease-Region cell |
| BR-04 | Age Group (0-14, 15-29, 30-44, 45-59, 60+), Gender (Male, Female, Other), Cases | Demographic Cohort | Demographic breakdown per Case record |
| BR-05 | Date (Year-Month), Region Name, Multiple Disease Case Counts, Historical Baseline | Outbreak Surveillance | Monthly Region-level Multi-disease index |
| BR-06 | Report Month (1-12), Disease Name, Monthly Aggregated Case Count, 5-Yr Mean | Seasonal / Temporal | Monthly cyclic series (Jan–Dec) |
| BR-07 | Cases Reported, Recovered Count, Recovery Percentage, Region, Disease | Clinical Outcome | Monthly per State & Disease |
| BR-08 | State Population, State Area (sq. km), Population Density, Incidence per Lakh | Demographic / Spatial | Annual State-level derived metric |
| BR-09 | Disease Name, Annual Total Cases for 2020, 2021, 2022, 2023, 2024, YoY % Delta | Temporal / Trend | Annual per Disease |
| BR-10 | Primary Keys, Foreign Keys, Timestamp, Audit Source, Integrity Rules | Relational Schema | Table / View Level |
| BR-11 | Filter Dimensions: Disease List, State Multi-select, Year Range, Demographics | Analytical State | Session State UI bindings |
| BR-12 | Full Filtered Record Set in tabular format with Column Headers | Export Data Stream | Filtered row-level records |
| BR-13 | Raw Row Count, Clean Row Count, Duplicates Count, Null Count, Outlier Count | Data Quality Audit | Data Pipeline Metadata |
| BR-14 | Test Vectors: Known inputs, Expected outputs, Assertion thresholds | Quality Assurance | Unit & Integration Test Suite |
| BR-15 | Deployment Package, Pinned Dependency Manifest, Entry Point Script | DevOps / Release | Cloud Repository Asset |



#### Table 4

| Audit Check | Evaluation Finding | Status | Remediation / Justification |
| --- | --- | --- | --- |
| HMW without BR | All 10 HMW statements (HMW-01 through HMW-10) have at least one corresponding Business Requirement. | PASSED | None needed. Complete coverage verified. |
| BR without HMW | Requirements BR-01 through BR-13 trace directly to HMW-01..10. BR-14 traces to overall QA objectives. BR-15 traces to project objective OBJ-04. | PASSED | All 15 BRs justified by user need or project charter objectives. |
| OQ Coverage | All 10 Operational Questions (OQ-01 through OQ-10) are directly supported by one or more Must-Have BRs. | PASSED | Every OQ is verifiable through specific business requirement acceptance criteria. |
| MoSCoW Balance | Must: 9 (60.0%), Should: 4 (26.7%), Could: 2 (13.3%), Won't: 0 (0.0%). | PASSED | Adheres exactly to software engineering best practices (~60% Must requirements). |



#### Table 5

| MoSCoW Level | Count | Percentage | Requirements Included | Strategic Purpose |
| --- | --- | --- | --- | --- |
| Must Have | 9 | 60.0% | BR-01, BR-02, BR-03, BR-04, BR-05, BR-06, BR-07, BR-10, BR-11, BR-14 | Core analytical capabilities required to answer all 10 OQs; non-negotiable for project evaluation. |
| Should Have | 4 | 26.7% | BR-08, BR-09, BR-12, BR-15 | High-value analytical enhancements (correlation, YoY tables, CSV export, cloud hosting). |
| Could Have | 2 | 13.3% | BR-13 | Desirable quality features (visual data cleaning ledger) included if schedule permits. |
| Won't Have | 0 | 0.0% | Real patient PII, Predictive AI forecasting, Mobile app, User authentication | Formally deferred to Phase 2 (post-semester). |

