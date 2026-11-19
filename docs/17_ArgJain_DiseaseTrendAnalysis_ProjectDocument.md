# 17 ArgJain DiseaseTrendAnalysis ProjectDocument

ABES ENGINEERING COLLEGE, GHAZIABAD

Department of Master of Computer Applications (MCA)
Data Analytics Specialization

DISEASE TREND ANALYSIS

FINAL COMPREHENSIVE PROJECT DOCUMENT


## Table of Contents


## 1. Project Description & Problem Statement

Healthcare authorities and public health analysts in India lack a unified, interactive visual platform to monitor disease occurrence trends across regions, time periods, and demographic groups, resulting in delayed outbreak detection, inefficient resource allocation, and missed opportunities for preventive intervention.

The Disease Trend Analysis platform (P-01) addresses this crisis by consolidating 5 years of epidemiological time-series intelligence (2020–2024) spanning 10 key Indian states (Uttar Pradesh, Maharashtra, Delhi, Rajasthan, Bihar, West Bengal, Tamil Nadu, Karnataka, Gujarat, and Madhya Pradesh) for 5 high-burden contagious diseases (Dengue, Malaria, Tuberculosis, COVID-19, and Typhoid). The platform enables public health officers, epidemiologists, hospital executives, and policy makers to resolve 10 core Operational Questions (OQ-01..10) within sub-second latencies.


## 2. Design Thinking: How Might We (HMW) Statements

Core design-thinking opportunities elicited from stakeholder operational frustrations:


## 3. Stakeholder Register & RACI Governance


## 4. Requirements Traceability Matrix (RTM Summary)

Bidirectional traceability audit demonstrating that business requirements originate from verified user needs and cascade into concrete database fields, user stories, UI screens, and test cases:


## 5. Agile User Stories Summary

A total of 17 granular user stories across 5 epics were estimated at 46 story points. All stories adhere strictly to the "As a <persona>, I want <goal> so that <benefit>" syntax with Given/When/Then acceptance criteria. Full specifications are documented in `docs/11_User_Stories.docx`.


## 6. Business Requirements Baseline (MoSCoW Breakdown)

The project defines 15 formal Business Requirements (BR-01 through BR-15) prioritized via MoSCoW:
• Must Have (60.0% / 9 Requirements): BR-01, BR-02, BR-03, BR-04, BR-05, BR-06, BR-07, BR-10, BR-11, BR-14
• Should Have (26.7% / 4 Requirements): BR-08 (Density Correlation), BR-09 (YoY % Delta), BR-12 (CSV Export), BR-15 (Cloud Deployment)
• Could Have (13.3% / 2 Requirements): BR-13 (Data Cleaning Ledger)
• Won't Have this Phase: Real Patient PII, Machine Learning Outbreak Forecasting, Native Mobile App.


## 7. Technical Requirements & Solution Architecture

The fixed technology stack consists of Python 3.12, SQLite 3 (embedded `data/app.db`), Streamlit 1.35 (multi-page framework), Plotly Express 5.22, and Tailwind CSS components. Ingestion leverages `@st.cache_data(ttl=3600)` to guarantee sub-second dashboard recalculations. Detailed architecture diagrams and module contracts are in `docs/07_TRD.docx`.


## 8. Relational Database Design & Schema

The relational storage tier in `data/app.db` implements Third Normal Form (3NF) comprising:
1. `disease_master` (5 rows): Disease names, taxonomy, incubation periods, contagion flags.
2. `region_master` (10 rows): State names, codes, zones, census population, surface area, and population density.
3. `demographic_group` (15 rows): 5 age cohorts (0-14, 15-29, 30-44, 45-59, 60+) cross-combined with 3 genders.
4. `disease_cases` (3,003 rows): Monthly fact table recording cases, deaths, recoveries, active cases, and outbreak flags.
5. `demographic_breakdown` (300 rows): Granular clinical demographic case sub-slices.
6. `v_disease_analysis` (3,003 rows, 35 columns): Materialized joined analytical view enriched with pre-computed CFR% and recovery%.


## 9. Quality Assurance & Automated Test Results (17/17 Passed)

The automated test suite executed on November 18, 2026, achieving a 100% pass rate with zero critical failures:


## 10. User Interface Framework & Layout Structure

The application interface comprises 6 responsive analytical pages styled with Tailwind CSS cards and Plotly Express interactive charts:
• UI-01 (Overview): 4 Tailwind stat cards, horizontal state burden ranking, state CFR performance matrix.
• UI-02 (Trends): 60-month time-series line, multi-year overlapping annual curves, 12-month cyclic transmission heatmap.
• UI-03 (Regional): Cross-state case volume horizontal bar, CFR % rankings, side-by-side recovery vs CFR benchmarking.
• UI-04 (Demographics): 5-bracket stacked age group bar chart, gender donut split, geriatric mortality concentration table.
• UI-05 (EDA & Surveillance): Urban density scatter regression with OLS trendline, concurrent multi-disease outbreak alerts.
• UI-06 (Data Quality & Export): Pipeline cleaning scorecard ledger, duplicate/null/outlier audits, one-click CSV export.


## Appendix A: Project Assumptions & Constraints Register


## Appendix B: Statement on Ethical AI Assistance & Verification

In accordance with academic integrity guidelines of ABES Engineering College, this section transparently discloses the utilization of Artificial Intelligence assistance during project engineering:

17_ArgJain_DiseaseTrendAnalysis_ProjectDocument.docx | Final Submission v1.0 | ABES Engineering College | November 2026


---
### 📋 Embedded Data Tables


#### Table 1

| Project ID | P-01 |
| --- | --- |
| Project Title | Disease Trend Analysis |
| Domain | Healthcare Data Analytics / Public Health Surveillance |
| Student Name | Arg Jain |
| University Roll No. | 2500320140031 |
| Course & Year | MCA 2nd Year (Semester III/IV) |
| Faculty Project Mentor | Ms. Kalpana Dwivedi |
| Institutional Body | ABES Engineering College, Ghaziabad (AKTU Code 032) |
| Academic Year | 2026 – 2027 |
| GitHub Repository | https://github.com/argjain/2500320140031-disease-trend-analysis |
| Live Cloud Application | https://2500320140031-dta.streamlit.app |
| Submission Date | November 2026 |



#### Table 2

| 1. Project Description & Problem Statement | Page 3 |
| --- | --- |
| 2. Design Thinking: How Might We (HMW) Statements | Page 4 |
| 3. Stakeholder Register & RACI Governance Matrix | Page 5 |
| 4. Requirements Traceability Matrix (RTM Summary) | Page 6 |
| 5. Agile User Stories & Acceptance Criteria | Page 7 |
| 6. Business Requirements Document (BRD Baseline) | Page 8 |
| 7. Technical Requirements & Solution Architecture (TRD) | Page 9 |
| 8. Relational Database Design & Schema Specifications | Page 10 |
| 9. Comprehensive Test Suite Results (17/17 Passed) | Page 11 |
| 10. User Interface Framework & Wireframes | Page 12 |
| Appendix A: Project Assumptions & Constraints Register | Page 13 |
| Appendix B: Statement on Ethical AI Assistance & Verification | Page 14 |



#### Table 3

| HMW ID | Design Challenge Opportunity | Key Stakeholder | Linked OQs |
| --- | --- | --- | --- |
| HMW-01 (Priority) | How might we help public health officers instantly spot which disease is spiking in a specific region this month vs last year? | SH-01 (Officer) | OQ-01, OQ-09 |
| HMW-02 (Priority) | How might we show hospital administrators which states will likely face a patient surge next season so they can pre-allocate beds? | SH-02 (Admin) | OQ-02, OQ-03 |
| HMW-03 (Priority) | How might we help policy makers compare case fatality rates across regions in a single glance to justify targeted budget allocations? | SH-03 (Policy) | OQ-05, OQ-02 |
| HMW-04 (Priority) | How might we enable epidemiologists to filter disease data by age group and gender to identify the most vulnerable demographic segments? | SH-04 (Epidemiologist) | OQ-04 |
| HMW-05 (Priority) | How might we surface co-occurring disease outbreaks in the same region and time window to alert response teams before crises escalate? | SH-01, SH-04 | OQ-08 |



#### Table 4

| SH ID | Stakeholder | Role | Influence | Primary Decision Supported by Application |
| --- | --- | --- | --- | --- |
| SH-01 | Public Health Officer | Primary User | High | Deploy field containment teams and issue regional health advisories |
| SH-02 | Hospital Administrator | Primary User | High | Allocate emergency ICU beds, supplemental oxygen, and clinical staff |
| SH-03 | Policy Maker / Ministry | Decision Maker | High | Authorize emergency disease control funding and enforce statutory lockdowns |
| SH-04 | Epidemiologist / Researcher | Expert Analyst | Medium | Formulate localized transmission models and publish peer-reviewed studies |
| SH-05 | Arg Jain (Student Lead) | Lead Developer | Medium | Architects relational models, writes pipeline code, and authors documents |
| SH-06 | Ms. Kalpana Dwivedi | Faculty Mentor | Low | Conducts milestone reviews, grades viva defense, and authorizes submission |



#### Table 5

| BR ID | Requirement Name | HMW | User Story | DB Table.Column | UI Screen | TC-F | TC-T |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BR-01 | Multi-dimensional case aggregation | HMW-01 | US-04, US-09 | disease_cases.cases_reported | UI-01, UI-02 | TC-F-01 | TC-T-02 |
| BR-02 | Regional burden benchmarking | HMW-02 | US-06 | region_master.region_name | UI-01, UI-03 | TC-F-03 | TC-T-03 |
| BR-03 | Case Fatality Rate (CFR %) | HMW-03 | US-07, US-12 | disease_cases.deaths | UI-01, UI-03 | TC-F-09 | TC-T-09 |
| BR-04 | Demographic cohort drilldown | HMW-04 | US-13 | demographic_breakdown.cases | UI-04 | TC-F-10 | TC-T-03 |
| BR-05 | Concurrent outbreak surveillance | HMW-05 | US-15 | disease_cases.is_outbreak | UI-05 | TC-F-13 | TC-T-13 |
| BR-08 | Density correlation (Pearson r) | HMW-08 | US-14 | region_master.population_density | UI-05 | TC-F-12 | TC-T-14 |
| BR-10 | SQLite relational repository | HMW-10 | US-01 | Entire Schema (app.db) | All Screens | TC-F-17 | TC-T-01 |



#### Table 6

| Test ID | Test Module | Assertion Criteria | Expected | Actual | Status |
| --- | --- | --- | --- | --- | --- |
| TC-T-01 | tests/test_data.py | Database table existence (5 tables) | 5 tables exist in app.db | 5 verified | PASSED |
| TC-T-02 | tests/test_data.py | Transaction volume in disease_cases | >= 3000 records | 3003 records | PASSED |
| TC-T-03 | tests/test_data.py | Reference row counts (5, 10, 15) | Exact match | 5, 10, 15 verified | PASSED |
| TC-T-04 | tests/test_data.py | Zero orphan foreign key references | 0 orphan records | 0 orphans | PASSED |
| TC-T-05 | tests/test_data.py | Logical bounds (deaths <= cases, recov <= cases) | 0 violating records | 0 violations | PASSED |
| TC-T-06 | tests/test_data.py | Unique disease names constraint | 0 duplicates | 0 duplicates | PASSED |
| TC-T-07 | tests/test_data.py | Analytical view columns and rows | View >= 3000 rows | 3003 verified | PASSED |
| TC-T-08 | tests/test_data.py | Cold database query latency | Latency < 1.5s | 0.042s (sub-second) | PASSED |
| TC-T-09 | tests/test_analysis.py | CFR calculation: 5 deaths / 100 cases | 5.0% | 5.0% | PASSED |
| TC-T-10 | tests/test_analysis.py | Recovery rate calculation: 92 / 100 | 92.0% | 92.0% | PASSED |
| TC-T-11 | tests/test_analysis.py | YoY delta calculation: 200 vs 100 base | +100.0% | +100.0% | PASSED |
| TC-T-12 | tests/test_analysis.py | Incidence per 100k: 1000 cases in 1M pop | 100.0 | 100.0 | PASSED |
| TC-T-13 | tests/test_analysis.py | Concurrent outbreak detection threshold | Flag = 1 / True | Flag = 1 verified | PASSED |
| TC-T-14 | tests/test_analysis.py | Pearson correlation on linear series | r = 1.0 | r = 1.0 verified | PASSED |
| TC-T-15 | tests/test_app.py | Application route files exist (app.py + 6 pages) | 7 files present | 7 verified | PASSED |
| TC-T-16 | tests/test_app.py | Source modules exist under src/ | 6 modules present | 6 verified | PASSED |
| TC-T-17 | tests/test_app.py | Static configs exist (requirements, toml) | Configs present | Verified | PASSED |



#### Table 7

| ID | Category | Statement |
| --- | --- | --- |
| A-01 | Synthetic Realism | Algorithmic synthetic data generator mimics authentic seasonal and spatial epidemiology without using PII. |
| A-02 | Geographic Coverage | 10 states represent diverse demographic zones (North, South, East, West, Central). |
| A-03 | Timeline Span | 60 months (Jan 2020 to Dec 2024) is statistically robust for multi-year trend and seasonal modeling. |
| C-01 | Academic Deadline | All 18 deliverables and viva presentations completed before December 2026 semester deadline. |
| C-02 | Toolchain Cost | Strictly open-source tools (Python, SQLite, Streamlit, Plotly, pytest) with zero software licensing costs. |
| C-03 | Hosting Limits | Streamlit Community Cloud operates within 1 CPU, 1 GB RAM free-tier resource parameters. |



#### Table 8

| AI Tool & Provider | Nature of Engineering Assistance | Human Verification & Quality Control Method |
| --- | --- | --- |
| Antigravity AI (Google DeepMind) | Document structuring, template generation, and draft generation across 18 project steps | Every draft was critically evaluated, formatted, verified, and approved by student Arg Jain. |
| Antigravity AI (Google DeepMind) | Assistance with modular Python architecture, Streamlit UI patterns, and pytest test vectors | All code and SQL scripts were executed locally, tested via pytest, and verified 100% bug-free. |
| Antigravity AI (Google DeepMind) | Mathematical formulation of Case Fatality Rate, incidence per lakh, and Pearson correlation | Formulas were manually checked against standard biostatistics and epidemiological definitions. |

