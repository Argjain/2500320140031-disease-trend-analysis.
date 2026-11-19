# 04 ArgJain DiseaseTrendAnalysis RTM

> Official Project Spreadsheet Artifact: `04_ArgJain_DiseaseTrendAnalysis_RTM.xlsx`


## 📊 Sheet: RTM (21 rows)

| OQ ID | HMW ID | Req ID (BR) | Requirement Description | Stakeholder (SH) | Priority | Status | Feature ID | DB Table.Column | User Story ID | UI Screen ID | Test Case (TC-F) | Test Case (TC-T) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OQ-01 | HMW-01 | BR-01 | Aggregate disease case counts by disease, region and time period | SH-01, SH-03 | Must | Identified | FR-03, FR-12 | disease_cases.cases_reported, report_date | US-04, US-09 | UI-01, UI-02 | TC-F-01, TC-F-04 | TC-T-02, TC-T-07 |
| OQ-09 | HMW-09 | BR-01 | Aggregate disease case counts by disease, region and time period | SH-01, SH-03 | Must | Identified | FR-03, FR-12 | disease_cases.cases_reported, report_date | US-04, US-09 | UI-01, UI-02 | TC-F-01, TC-F-04 | TC-T-02, TC-T-07 |
| OQ-02 | HMW-02 | BR-02 | Provide region-level disease comparison across all states | SH-02 | Must | Identified | FR-04 | region_master.region_name, disease_cases.cases_reported | US-06 | UI-01, UI-03 | TC-F-03, TC-F-08 | TC-T-03, TC-T-07 |
| OQ-05 | HMW-03 | BR-03 | Display Case Fatality Rates (CFR) across diseases and regions | SH-03 | Must | Identified | FR-05 | disease_cases.deaths, disease_cases.cases_reported | US-07, US-12 | UI-01, UI-03 | TC-F-09 | TC-T-05, TC-T-09 |
| OQ-04 | HMW-04 | BR-04 | Demographic filtering and breakdown by age group and gender | SH-04 | Must | Identified | FR-06 | demographic_breakdown.cases_in_group, demo_id | US-13 | UI-04 | TC-F-10, TC-F-11 | TC-T-03 |
| OQ-08 | HMW-05 | BR-05 | Detect concurrent multi-disease outbreaks in same region-month | SH-01, SH-04 | Must | Identified | FR-07 | disease_cases.is_outbreak, cases_reported | US-15 | UI-05 | TC-F-13 | TC-T-13 |
| OQ-03 | HMW-06 | BR-06 | Seasonal and monthly disease outbreak cycle profiling | SH-01, SH-04 | Must | Identified | FR-08 | disease_cases.report_month, cases_reported | US-08, US-11 | UI-02 | TC-F-05, TC-F-07 | TC-T-07 |
| OQ-10 | HMW-06 | BR-06 | Identify peak transmission months across all diseases | SH-01, SH-04 | Must | Identified | FR-08 | disease_cases.report_month, cases_reported | US-08, US-11 | UI-02 | TC-F-05, TC-F-07 | TC-T-07 |
| OQ-07 | HMW-07 | BR-07 | Compute and display recovery rates per disease and region | SH-02 | Must | Identified | FR-09 | disease_cases.recovered, cases_reported | US-12 | UI-03 | TC-F-19 | TC-T-05, TC-T-10 |
| OQ-06 | HMW-08 | BR-08 | Evaluate disease incidence vs population density correlation | SH-04 | Should | Identified | FR-10 | region_master.population_density, cases_reported | US-14 | UI-05 | TC-F-12 | TC-T-14 |
| OQ-09 | HMW-09 | BR-09 | Calculate year-over-year percentage change per disease | SH-03 | Should | Identified | FR-11 | disease_cases.report_year, cases_reported | US-05, US-10 | UI-01, UI-02 | TC-F-06 | TC-T-11 |
| OQ-01..10 | HMW-10 | BR-10 | Store disease intelligence in structured SQLite relational database | SH-05 | Must | Identified | FR-01 | Entire Schema (app.db all 5 tables) | US-01 | All Screens | TC-F-17 | TC-T-01, 04, 06 |
| OQ-01 | HMW-01 | BR-11 | Multidimensional sidebar filters updating all visuals concurrently | SH-01..04 | Must | Identified | FR-02 | Sidebar Filter Dimensions across all tables | US-03 | Sidebar (All) | TC-F-02, TC-F-18 | TC-T-16 |
| OQ-02 | HMW-02 | BR-11 | Multidimensional sidebar filters updating all visuals concurrently | SH-01..04 | Must | Identified | FR-02 | Sidebar Filter Dimensions across all tables | US-03 | Sidebar (All) | TC-F-02, TC-F-18 | TC-T-16 |
| OQ-05 | HMW-03 | BR-11 | Multidimensional sidebar filters updating all visuals concurrently | SH-01..04 | Must | Identified | FR-02 | Sidebar Filter Dimensions across all tables | US-03 | Sidebar (All) | TC-F-02, TC-F-18 | TC-T-16 |
| OQ-04 | HMW-04 | BR-11 | Multidimensional sidebar filters updating all visuals concurrently | SH-01..04 | Must | Identified | FR-02 | Sidebar Filter Dimensions across all tables | US-03 | Sidebar (All) | TC-F-02, TC-F-18 | TC-T-16 |
| OQ-08 | HMW-05 | BR-11 | Multidimensional sidebar filters updating all visuals concurrently | SH-01..04 | Must | Identified | FR-02 | Sidebar Filter Dimensions across all tables | US-03 | Sidebar (All) | TC-F-02, TC-F-18 | TC-T-16 |
| OQ-01..10 | HMW-10 | BR-12 | Export filtered analytical datasets to CSV for offline analysis | SH-04, SH-05 | Should | Identified | FR-14 | v_disease_analysis (all 35 columns) | US-16 | UI-06 | TC-F-14 | TC-T-16 |
| OQ-01..10 | HMW-10 | BR-13 | Transparent data quality audit summary showing cleaning steps | SH-05 | Could | Identified | FR-15 | Data Pipeline Audit Metadata | US-02, US-17 | UI-06 | TC-F-15 | TC-T-08 |
| OQ-01..10 | All HMWs | BR-14 | Automated pytest test suite with >=80% coverage and zero failures | SH-06 | Must | Identified | All Features | All Tables & Constraints | All Stories | All Screens | TC-F-01..20 | All TC-T-01..18 |
| OQ-01..10 | OBJ-04 | BR-15 | Cloud deployment on Streamlit Community Cloud with public URL | SH-05, SH-06 | Should | Identified | All Features | data/app.db deployment asset | All Stories | All Screens | TC-F-01, TC-F-20 | TC-T-18 |



## 📊 Sheet: Coverage_Check (26 rows)

| REQUIREMENTS TRACEABILITY COVERAGE AUDIT | Unnamed: 1 | Unnamed: 2 | Unnamed: 3 | Unnamed: 4 |
| --- | --- | --- | --- | --- |
| — | — | — | — | — |
| OQ ID | Operational Question | Linked HMW(s) | Linked BR(s) | Coverage Status |
| OQ-01 | Diseases with highest 5-year case increase | HMW-01, HMW-09 | BR-01, BR-09, BR-11 | COVERED (100%) |
| OQ-02 | Geographic states most affected per disease | HMW-02, HMW-03 | BR-02, BR-11 | COVERED (100%) |
| OQ-03 | Monthly / seasonal trend of disease outbreaks | HMW-02, HMW-06 | BR-06, BR-11 | COVERED (100%) |
| OQ-04 | Vulnerable age group and gender demographics | HMW-04 | BR-04, BR-11 | COVERED (100%) |
| OQ-05 | Case fatality rate (CFR) across diseases/regions | HMW-03, HMW-07 | BR-03, BR-11 | COVERED (100%) |
| OQ-06 | Incidence correlation with population density | HMW-08 | BR-08, BR-11 | COVERED (100%) |
| OQ-07 | Highest recovery rates and geographic spread | HMW-07 | BR-07, BR-11 | COVERED (100%) |
| OQ-08 | Concurrent disease outbreaks in same region-month | HMW-05 | BR-05, BR-11 | COVERED (100%) |
| OQ-09 | Year-over-year (YoY) percentage change in cases | HMW-01, HMW-09 | BR-09, BR-01 | COVERED (100%) |
| OQ-10 | Peak reporting months by disease type | HMW-06 | BR-06, BR-11 | COVERED (100%) |
| — | — | — | — | — |
| HMW ID | HMW Statement Summary | Primary Stakeholder | Mapped BR(s) | Traceability Status |
| HMW-01 (Priority) | Instantly spot spiking disease vs last year | SH-01 | BR-01, BR-11 | MAPPED (100%) |
| HMW-02 (Priority) | Anticipate seasonal state surge for bed allocation | SH-02 | BR-02, BR-11 | MAPPED (100%) |
| HMW-03 (Priority) | Single-glance CFR comparison across states | SH-03 | BR-03, BR-11 | MAPPED (100%) |
| HMW-04 (Priority) | Age and gender demographic drill-down | SH-04 | BR-04, BR-11 | MAPPED (100%) |
| HMW-05 (Priority) | Detect concurrent co-occurring disease outbreaks | SH-01, SH-04 | BR-05, BR-11 | MAPPED (100%) |
| HMW-06 | Visualise seasonal peaks across diseases | SH-01, SH-04 | BR-06, BR-11 | MAPPED (100%) |
| HMW-07 | Recovery rate benchmarking per region | SH-02 | BR-07, BR-11 | MAPPED (100%) |
| HMW-08 | Incidence vs population density correlation | SH-04 | BR-08, BR-11 | MAPPED (100%) |
| HMW-09 | Year-over-year trend table of growing threats | SH-03 | BR-09, BR-01 | MAPPED (100%) |
| HMW-10 | Downloadable clean dataset and quality ledger | SH-05 | BR-10, BR-12, BR-13 | MAPPED (100%) |
| — | — | — | — | — |
| AUDIT SUMMARY | 10/10 OQs Covered (100%) / 10/10 HMWs Mapped (100%) / 15/15 BRs Traced (100%) / 0 Unmapped Items | — | — | ALL CHECKS PASSED |



## 📊 Sheet: Change_Log (5 rows)

| Version | Release Date | Author / Role | Step ID | Scope of Change / Fields Updated |
| --- | --- | --- | --- | --- |
| v1.0 | 18-Nov-2026 | Arg Jain (Lead DA) | Step 4 | Initial RTM created with OQ, HMW, BR, SH, Priority, Status columns populated. Later columns marked TBD. |
| v1.1 | 18-Nov-2026 | Arg Jain (Lead DA) | Step 8 | Populated DB Table.Column mapping for all requirements. |
| v1.2 | 18-Nov-2026 | Arg Jain (Lead DA) | Step 11 | Populated User Story IDs (US-01..US-17) and Sprint Epics. |
| v1.3 | 18-Nov-2026 | Arg Jain (Lead DA) | Step 12 | Populated UI Screen IDs (UI-01..UI-06) across all requirements. |
| v1.4 | 18-Nov-2026 | Arg Jain (Lead DA) | Step 13 | FINAL RTM COMPLETE: Feature IDs, Functional (TC-F) and Technical (TC-T) test case IDs populated. |

