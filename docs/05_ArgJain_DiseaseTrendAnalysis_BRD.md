# 05 ArgJain DiseaseTrendAnalysis BRD

DISEASE TREND ANALYSIS

STEP 5 — Business Requirements Document (BRD)


## 1. Document Control & Revision History

This document is maintained under formal configuration management guidelines:


## 2. Executive Summary

In contemporary public health administration across India, epidemiological data often resides in disparate, siloed departmental systems and static PDF bulletins. This structural fragmentation creates severe latency in detecting seasonal and localized outbreaks of endemic diseases such as Dengue, Malaria, Tuberculosis, COVID-19, and Typhoid. Decision-makers frequently face a multi-week lag between field transmission spikes and executive intervention, resulting in avoidable hospital bed crises and delayed therapeutic provisioning.

The Disease Trend Analysis platform (Project P-01) delivers a unified, interactive analytical cockpit engineered specifically for public health officers, hospital administrators, epidemiologists, and ministerial policy makers. By integrating historical epidemiological time series across 10 major Indian states over a 5-year observation period (2020–2024), the application surfaces critical trajectory indicators: Case Fatality Rates (CFR), regional burden benchmarks, demographic risk vectors, seasonal transmission waves, and co-occurring outbreak warnings.

Built entirely on an open-source data analytics stack (Python, SQLite, Streamlit, Plotly, pytest) and deployed on cloud infrastructure, the solution satisfies all 10 Operational Questions (OQ-01 through OQ-10) with sub-second visual response times. This document formally establishes the business baseline, stakeholder alignment, and functional boundary for downstream engineering execution.


## 3. Business Problem & Opportunity Analysis


### 3.1 Current State Deficiencies

* Static Reporting Latency: Epidemiological surveillance is published as monthly retrospective PDF summaries, preventing real-time tactical intervention.
* Fragmented Demographic Visibility: Co-morbidity and vulnerability indicators across age cohorts and gender brackets are not cross-filterable with geographical hotspots.
* Absence of Co-occurrence Warnings: Syndromic overlap (e.g., concurrent Dengue and Malaria surges during post-monsoon weeks) is evaluated in departmental silos.

### 3.2 Desired State Capabilities

* Single-Pane Epidemiological Cockpit: Real-time visual dashboard rendering multidimensional case aggregates, fatality ratios, and recovery metrics.
* Granular Micro-Demographic Profiling: Instant filtering by disease entity, state boundary, calendar year, age cohort, and gender identity.
* Automated Multi-Disease Overlap Surveillance: Early flagging of regions where multiple contagious entities simultaneously exceed statistical thresholds.

### 3.3 Cost of Inaction

* Sub-optimal Health Budget Allocation: Health funds allocated evenly rather than targeted toward high-CFR districts experiencing accelerating growth.
* Emergency Department Overcrowding: Inability to anticipate 60-day seasonal surges causes catastrophic ICU bed and oxygen shortages.

## 4. Project Objectives & Success Metrics (KPIs)

Performance against charter objectives will be audited using quantitative criteria:


## 5. Stakeholder Governance & RACI Framework

RACI mapping across the project development lifecycle (R = Responsible, A = Accountable, C = Consulted, I = Informed):


## 6. Scope Specification


### 6.1 In-Scope Capabilities

* Synthetic epidemiological dataset spanning 5 diseases (Dengue, Malaria, Tuberculosis, COVID-19, Typhoid) across 10 Indian states from Jan 2020 to Dec 2024 (60 months).
* Normalized SQLite relational database schema (3 master tables, 1 primary fact table, 1 demographic fact table, 1 denormalized analytical view).
* Exploratory Data Analysis (EDA) engine computing case sums, CFR %, recovery %, YoY % delta, monthly cyclical indices, and Pearson density correlation.
* Interactive Streamlit web application styled with Tailwind CSS visual design patterns and synchronized sidebar filtering.
* Data export capability to standard CSV format and transparent data quality auditing ledger.
* Automated test suite (pytest) covering database integrity, calculation formulas, and UI responsiveness.
* Deployment to Streamlit Community Cloud with public HTTPS URL for evaluator access.

### 6.2 Out-of-Scope Capabilities

* Real or identifiable patient electronic health records (EHR) due to statutory HIPAA/DISHA data protection regulations.
* Machine learning predictive forecasting models (e.g., ARIMA, Prophet, LSTM) — deferred to academic semester 3/4.
* Native mobile application development (iOS/Android).
* User identity management, role-based access control (RBAC), and authentication gateways.
* Automated SMS or email outbound emergency broadcasting pipelines.
* Multi-lingual internationalization (platform standard is Indian English).

## 7. Detailed Business Requirements Register

Each requirement is itemized with operational rationale and formal acceptance criteria:

BR-01: Multi-dimensional Incidence Aggregation [Must]

BR-02: Comparative Regional Burden Benchmarking [Must]

BR-03: Case Fatality Rate (CFR) Intelligence [Must]

BR-04: Vulnerable Demographic Cohort Profiling [Must]

BR-05: Automated Co-occurring Outbreak Surveillance [Must]

BR-06: Seasonal Wave & Cyclic Profiling [Must]

BR-07: Clinical Recovery Benchmarking [Must]

BR-08: Urban Crowding & Density Correlation [Should]

BR-09: Multi-Year Year-over-Year (YoY) Trajectory [Should]

BR-10: Relational Data Integrity Architecture [Must]

BR-11: Synchronized Multidimensional Filtering [Must]

BR-12: Analytical Data Export Capability [Should]

BR-13: Transparent Data Quality Ledger [Could]

BR-14: Automated Quality Assurance Test Suite [Must]

BR-15: High-Availability Public Cloud Deployment [Should]


## 8. Business Rules Catalog

The platform strictly enforces the following domain validation rules:


## 9. Data Requirements & Model Entities

The data pipeline ingests, validates, and maintains the following entities:


## 10. Assumptions, Constraints & Dependencies


### 10.1 Foundational Assumptions


### 10.2 Operational Constraints


## 11. Risk Management & Mitigation Framework

Identified technical and operational risks along with pre-planned mitigation strategies:


## 12. Glossary of Terms & Acronyms


## 13. Formal Sign-off & Milestone Acceptance

By signing below, the stakeholders confirm that the Business Requirements Document (BRD v1.0) accurately represents project scope, operational requirements, and success criteria. Engineering work on Technical Requirements (Step 7) and Database Design (Step 8) is authorized to proceed.

05_ArgJain_DiseaseTrendAnalysis_BRD.docx | v1.0 | ABES Engineering College | November 2026


---
### 📋 Embedded Data Tables


#### Table 1

| Project ID & Title | P-01 / Disease Trend Analysis |
| --- | --- |
| Domain | Healthcare Data Analytics |
| Student Author | Arg Jain (Roll No. 2500320140031) |
| Academic Program | MCA 2nd Year (Data Analytics) |
| Institution | ABES Engineering College, Ghaziabad |
| Faculty Mentor | Ms. Kalpana Dwivedi |
| Document Version | v1.0 (Baseline Release) |
| Release Date | November 2026 |
| Target Environment | Python 3.12 / Streamlit Community Cloud |
| Document Status | Approved for Architecture & Engineering |



#### Table 2

| Version | Date | Author | Summary of Changes | Reviewer |
| --- | --- | --- | --- | --- |
| v0.1 | 14-Nov-2026 | Arg Jain | Initial requirements gathering from Step 1-3 deliverables | Self-Review |
| v0.9 | 16-Nov-2026 | Arg Jain | Integrated RACI, Business Rules, and Data Requirements | Mentor Review |
| v1.0 | 18-Nov-2026 | Arg Jain | Formal baseline document for academic submission and build plan | Ms. Kalpana Dwivedi |



#### Table 3

| Obj ID | KPI Name | Metric Description | Baseline | Target | Verification |
| --- | --- | --- | --- | --- | --- |
| OBJ-01 | OQ Resolution Completeness | App answers all 10 defined operational questions through intuitive UI | 0 OQs | 10 / 10 OQs (100%) | Interactive mentor walkthrough |
| OBJ-02 | Visual Analytical Diversity | Interactive Plotly charts (Line, Bar, Heatmap, Scatter, Demographics, Quality) | 0 charts | >= 6 Distinct Chart Types | UI inspection |
| OBJ-03 | Engine Latency & Performance | End-to-end page render and filter recalculation speed | N/A | < 5.0s Initial, < 2.0s Filter | Automated timer logging |
| OBJ-04 | Test Suite Integrity | Automated pytest test suite line & branch coverage | 0% | >= 80% Coverage (0 critical bugs) | pytest-cov execution report |
| OBJ-05 | Cloud Availability | Continuous operational uptime on Streamlit Community Cloud | Local only | >= 99.0% Uptime over eval period | Cloud host monitoring |



#### Table 4

| SH ID | Stakeholder Name | Role | Req | Des | Bld | Dep | Key Responsibilities |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SH-01 | Public Health Officer | Primary User | C | I | R | I | Validates outbreak threshold models |
| SH-02 | Hospital Administrator | Primary User | C | I | R | I | Advises surge and bed capacity KPIs |
| SH-03 | Policy Maker / Ministry | Executive User | I | A | I | A | Approves strategic metrics & budget views |
| SH-04 | Epidemiologist / Researcher | Expert Analyst | C | I | R | I | Reviews statistical correlations & CFR formulas |
| SH-05 | Arg Jain | Lead Developer (Student) | R | A | R | R | Owns end-to-end design, code, and deployment |
| SH-06 | Ms. Kalpana Dwivedi | Faculty Evaluator (Mentor) | A | A | A | A | Evaluates academic rigor and signs off release |



#### Table 5

| Requirement Description | The business needs to aggregate disease case counts by disease entity, geographical region, and temporal period so that health officers can detect emerging outbreak trends early. |
| --- | --- |
| Business Rationale | Without consolidated multidimensional grouping, analysts cannot observe state-level or seasonal shifts. |
| Source HMW Link | HMW-01, HMW-09 |
| Acceptance Criteria | 1. User can aggregate cases across any combination of 5 diseases, 10 states, and 5 years. 2. Aggregated totals match raw SQL sums. 3. Renders within 1.5 seconds. |



#### Table 6

| Requirement Description | The business needs to compare disease burden across states on a common scale so that hospital administrators can anticipate inter-state patient surge patterns. |
| --- | --- |
| Business Rationale | Allows cross-state allocation of mobile intensive care units and consumable medical supplies. |
| Source HMW Link | HMW-02 |
| Acceptance Criteria | 1. Displays horizontal ranking of all 10 states sorted descending by case volume. 2. Filter changes update state rankings instantly. |



#### Table 7

| Requirement Description | The business needs to compute and display Case Fatality Rates (CFR) across diseases and regions so that policy makers can identify high-mortality zones and justify emergency resource deployment. |
| --- | --- |
| Business Rationale | High incidence with low CFR indicates managed caseload; high CFR demands acute medical intervention. |
| Source HMW Link | HMW-03 |
| Acceptance Criteria | 1. CFR calculated strictly as (Deaths / Cases * 100). 2. Handled safely for zero case counts (returns 0.0%). 3. Displayed in disease-by-region heatmap matrix. |



#### Table 8

| Requirement Description | The business needs to segment disease morbidity by age bracket and gender cohort so that epidemiologists can identify demographic vulnerability profiles. |
| --- | --- |
| Business Rationale | Enables targeted immunization and public messaging (e.g., pediatric vs elderly outreach). |
| Source HMW Link | HMW-04 |
| Acceptance Criteria | 1. Visual breakdown across 5 age groups (0-14, 15-29, 30-44, 45-59, 60+) and 3 genders. 2. Sum of demographic slices equals total reported cases within 10% sampling variance. |



#### Table 9

| Requirement Description | The business needs to detect and flag concurrent outbreaks where multiple diseases cross threshold levels simultaneously in the same region and time frame so that response teams avoid overwhelmed local healthcare capacity. |
| --- | --- |
| Business Rationale | Syndromic convergence can collapse local hospital triage capacity rapidly. |
| Source HMW Link | HMW-05 |
| Acceptance Criteria | 1. Algorithmic trigger flags any state-month where >= 2 diseases exceed 1.5x monthly historical baseline. 2. High-risk region-months presented in dedicated alert view. |



#### Table 10

| Requirement Description | The business needs to profile monthly and seasonal variations in disease incidence so that medical supply chains can pre-position therapeutics ahead of peak months. |
| --- | --- |
| Business Rationale | Vector-borne illnesses exhibit predictable monsoon peaks requiring 60-day advance procurement. |
| Source HMW Link | HMW-06 |
| Acceptance Criteria | 1. Cyclic curve maps average incidence across calendar months 1 through 12. 2. Vector-borne peaks clearly discernible in monsoon window (July–September). |



#### Table 11

| Requirement Description | The business needs to compute recovery percentages per disease and region so that hospital networks can benchmark clinical recovery efficacy against regional averages. |
| --- | --- |
| Business Rationale | Highlights clinical management successes and identifies protocols worth standardizing. |
| Source HMW Link | HMW-07 |
| Acceptance Criteria | 1. Recovery rate computed as (Recovered / Cases * 100). 2. All values constrained between 0.0% and 100.0%. 3. Displayed alongside CFR in regional comparison view. |



#### Table 12

| Requirement Description | The business needs to evaluate the correlation between disease incidence rate and population density so that researchers can quantify the impact of urban crowding on transmission. |
| --- | --- |
| Business Rationale | Validates epidemiological models linking rapid urbanization to contagious disease velocity. |
| Source HMW Link | HMW-08 |
| Acceptance Criteria | 1. Scatter plot plots Incidence per Lakh against Population Density (persons/sq km). 2. Calculates Pearson correlation coefficient (r) and two-tailed p-value. |



#### Table 13

| Requirement Description | The business needs to calculate year-over-year (YoY) percentage changes in reported cases per disease so that ministries can assess multi-year disease growth or containment. |
| --- | --- |
| Business Rationale | Essential for evaluating effectiveness of multi-year public health programs. |
| Source HMW Link | HMW-09 |
| Acceptance Criteria | 1. Computes ((Cases_Yr - Cases_Yr-1) / Cases_Yr-1 * 100) across consecutive years. 2. Displays diverging color indicators (Green for decline, Red for growth). |



#### Table 14

| Requirement Description | The business needs to maintain disease intelligence in a standardized, relational data store so that analytical queries are consistent, auditable, and reproducible. |
| --- | --- |
| Business Rationale | Guarantees referential integrity, eliminates orphaned records, and ensures reproducibility. |
| Source HMW Link | HMW-10 |
| Acceptance Criteria | 1. Relational schema deployed in SQLite. 2. Foreign key constraints enforce parent-child relations. 3. Check constraints enforce non-negative values. |



#### Table 15

| Requirement Description | The business needs synchronized multidimensional filtering (disease, region, year, age, gender) that updates all visual perspectives concurrently so that analytical exploration is fluid. |
| --- | --- |
| Business Rationale | Analysts should never experience state desynchronization across tabs or views. |
| Source HMW Link | HMW-01..05 |
| Acceptance Criteria | 1. Centralized filter controls persist across application pages. 2. Modifying a filter cascades to all KPI cards and charts simultaneously. |



#### Table 16

| Requirement Description | The business needs to export filtered analytical datasets into standard spreadsheet formats so that researchers can conduct specialized external epidemiological modeling. |
| --- | --- |
| Business Rationale | Facilitates offline analysis in R, SPSS, or advanced statistical modeling packages. |
| Source HMW Link | HMW-10 |
| Acceptance Criteria | 1. One-click CSV export button available on data screen. 2. Output matches current filter slice and opens cleanly in Microsoft Excel. |



#### Table 17

| Requirement Description | The business needs a transparent data quality accounting ledger showing cleaning interventions (missing values imputed, duplicates removed, outliers bounded) so that data integrity is demonstrable. |
| --- | --- |
| Business Rationale | Builds stakeholder trust in the validity and reliability of published findings. |
| Source HMW Link | HMW-10 |
| Acceptance Criteria | 1. Dedicated Data Quality screen displays pre-cleaning and post-cleaning metrics. 2. Counts of nulls filled, duplicates purged, and outliers bounded are explicitly shown. |



#### Table 18

| Requirement Description | The business needs comprehensive automated verification test suites covering data ingestion, KPI calculations, and interface responsiveness so that operational errors are caught prior to evaluation. |
| --- | --- |
| Business Rationale | Prevents computational regressions and validates data integrity before academic presentation. |
| Source HMW Link | All HMWs |
| Acceptance Criteria | 1. pytest test suite executes cleanly. 2. Line and calculation coverage >= 80% with 0 critical failures. |



#### Table 19

| Requirement Description | The business needs the analytical platform hosted on an accessible cloud platform with public access so that evaluating mentors and external reviewers can inspect the system remotely. |
| --- | --- |
| Business Rationale | Enables seamless grading, mentor verification, and external stakeholder evaluation. |
| Source HMW Link | OBJ-04 |
| Acceptance Criteria | 1. Platform deployed on Streamlit Community Cloud. 2. URL accessible via standard web browser without special VPN or login credentials. |



#### Table 20

| Rule ID | Rule Name | Operational Definition | Governs | Enforcement Point |
| --- | --- | --- | --- | --- |
| BRL-01 | CFR Calculation Integrity | Case Fatality Rate is strictly (Deaths / Cases * 100). If Cases = 0, CFR must return 0.00%. CFR can never exceed 100.00%. | BR-03 | Engine / Calculation Layer |
| BRL-02 | Recovery Ceiling Constraint | Reported recoveries cannot exceed total cases. Recovery Rate = (Recovered / Cases * 100) constrained between 0.00% and 100.00%. | BR-07 | Data Ingestion & UI Layer |
| BRL-03 | Temporal Filter Bounds | Date range selections cannot be inverted (Start Year cannot exceed End Year). Minimum selectable span is 1 calendar month. | BR-11 | Sidebar UI Validation |
| BRL-04 | Outbreak Threshold Logic | A localized outbreak flag (is_outbreak = 1) triggers when monthly cases exceed 1.5x of the 5-year monthly historical mean for that state. | BR-05 | Analytical Model Layer |
| BRL-05 | Synthetic Data Privacy Firewall | Under no circumstances may real patient names, Aadhaar numbers, or contact identifiers be stored or rendered. Synthetic data only. | BR-10 | Data Architecture Governance |
| BRL-06 | Decimal Precision Standard | All published percentage metrics (CFR, Recovery Rate, YoY Change) must be formatted to exactly two decimal places (0.00%). | BR-01..09 | Presentation Layer |



#### Table 21

| Entity Name | Description & Business Role | Source Origin | Volume / Cardinality | Structural Nature |
| --- | --- | --- | --- | --- |
| disease_master | Master table containing disease reference metadata (category, contagion flag, incubation period) | Curated Medical Reference | Static Table (5 records) | Relational PK: disease_id |
| region_master | Geographic master containing state names, state codes, regional zones, population census, and land area | Census & Geospatial Reference | Static Table (10 states) | Relational PK: region_id |
| demographic_group | Classification master cross-combining 5 age cohorts with 3 gender identities | Demographic Reference | Static Table (15 segments) | Relational PK: demo_id |
| disease_cases | Primary transactional fact table containing monthly incident cases, deaths, recoveries, and active cases | State Epidemiological Reporting | Monthly Grain (3,000+ records) | Foreign Keys to disease & region |
| demographic_breakdown | Secondary fact table itemizing case counts across age and gender segments for sampled cases | Clinical Triage Records | Fact Grain (~300 records) | Foreign Keys to case_id & demo_id |
| v_disease_analysis | Denormalized joined analytical view combining all master and fact attributes with calculated KPIs | Relational Engine View | Materialized Query View (35+ columns) | Dynamic SQL View |



#### Table 22

| ID | Assumption Category | Detailed Assumption Statement |
| --- | --- | --- |
| A-01 | Synthetic Data Realism | Algorithmic synthetic generation (Faker + NumPy) reproduces authentic epidemiological dynamics (seasonal waves, COVID spike, urban density correlation) with high fidelity. |
| A-02 | Geographic Representation | Ten selected states (UP, MH, DL, RJ, BR, WB, TN, KA, GJ, MP) provide a statistically balanced representation of Northern, Southern, Eastern, Western, and Central Indian healthcare dynamics. |
| A-03 | Temporal Granularity | A 5-year observation window (2020 to 2024) with monthly time buckets is sufficient to capture longitudinal trends, seasonal cyclicity, and pandemic waves. |
| A-04 | Evaluation Accessibility | The evaluation panel will possess standard modern web browsers with unrestricted HTTPS access to public cloud services (share.streamlit.io). |



#### Table 23

| ID | Constraint Category | Detailed Constraint Statement |
| --- | --- | --- |
| C-01 | Academic Schedule | All 18 project steps, code artifacts, documentation, and viva presentations must be completed by December 2026. |
| C-02 | Open-Source Toolchain | Project implementation must rely strictly on free, open-source software libraries (Python, SQLite, Streamlit, Plotly, pytest) without commercial licensing costs. |
| C-03 | Free-Tier Cloud Limits | Hosting must operate within Streamlit Community Cloud free tier constraints (1 CPU, 1 GB RAM, shared memory limits). |
| C-04 | Individual Authorship | All architecture, development, QA, and documentation tasks must be completed solely by student candidate Arg Jain. |



#### Table 24

| Risk ID | Risk Title | Risk Description | Likelihood | Impact | Proactive Mitigation Strategy |
| --- | --- | --- | --- | --- | --- |
| R-01 | Synthetic Data Credibility | Evaluator perceives synthetic data as artificial or ungrounded | Medium | High | Embed verifiable historical patterns (monsoon Dengue surges, COVID 2021 spike) and document data validation tests. |
| R-02 | Cloud Resource Throttling | Streamlit Cloud 1 GB memory limit reached during complex joins | Medium | Medium | Leverage @st.cache_data decorators, pre-aggregate heavy views in SQLite, and optimize DataFrame datatypes. |
| R-03 | Testing Coverage Deficit | Unable to reach mandatory 80% pytest code coverage before deadline | Low | Medium | Modularize analysis functions into pure, standalone Python functions easily tested via parameterized pytest fixtures. |
| R-04 | Cloud Inactivity Hibernation | Streamlit Cloud puts app to sleep after 7 days of zero traffic | High | Low | Document sleep behavior in deployment guide; wake application 1 hour prior to formal academic viva demonstration. |
| R-05 | Data Integrity Corruption | Inadvertent introduction of negative cases or deaths exceeding cases | Low | High | Enforce SQLite CHECK constraints and run automated cleaning pipeline before rendering any visual chart. |



#### Table 25

| Term / Acronym | Authoritative Definition |
| --- | --- |
| CFR (Case Fatality Rate) | The proportion of deaths caused by a specific disease relative to total confirmed cases, calculated as (Deaths / Confirmed Cases * 100). |
| Incidence Rate | The frequency of new disease cases occurring in a defined population over a specified time interval, normalized per 100,000 residents. |
| Recovery Rate | The proportion of patients successfully recovered from a diagnosed disease, calculated as (Recovered / Confirmed Cases * 100). |
| EDA (Exploratory Data Analysis) | The statistical practice of examining datasets through summary statistics, distribution analysis, and interactive visual charting. |
| MoSCoW Prioritization | A prioritization framework categorizing requirements into Must Have, Should Have, Could Have, and Won't Have this time. |
| OQ (Operational Question) | A concrete analytical question that end-users need the application to answer to make informed operational decisions. |
| HMW (How Might We) | A design-thinking question format that reframes user pain points into actionable innovation opportunities. |
| BR (Business Requirement) | A formal statement defining what capability the business requires to achieve a stated operational benefit. |
| YoY (Year-over-Year) | A mathematical comparison of an identical metric across consecutive calendar years to identify growth trajectories. |
| RTM (Requirements Traceability Matrix) | A tabular grid cross-mapping requirements to source needs, user stories, database schemas, and test verification cases. |
| SQLite | A lightweight, zero-configuration, serverless, relational database management system embedded directly within the application filesystem. |
| Streamlit | An open-source Python framework designed for rapid development and deployment of data science web applications. |



#### Table 26

| Signatory Role | Full Name & Designation | Approval Status / Signature | Date |
| --- | --- | --- | --- |
| Lead Developer / Student | Arg Jain (Roll No. 2500320140031) | Submitted for Review | 18-Nov-2026 |
| Faculty Mentor / Evaluator | Ms. Kalpana Dwivedi (Assistant Professor) | Recommended for Build | 18-Nov-2026 |
| Head of Department (MCA) | Prof. (Dr.) Expert Academician | Approved for Submission | Pending |

