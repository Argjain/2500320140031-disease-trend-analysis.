# 18 ArgJain DiseaseTrendAnalysis Presentation

DISEASE TREND ANALYSIS

STEP 18 — ABES Presentation Slide Deck & Speaker Script


## 1. Five-Minute Presentation Pacing Roadmap

The 11-slide presentation is engineered for strict adherence to a 5-minute academic evaluation window. Each slide is budgeted for approximately 25 to 30 seconds of spoken remarks:


## 2. Slide-by-Slide Visual Layout & Verbatim Speaker Scripts


### SLIDE 1: Title & Project Attribution

ON-SCREEN SLIDE CONTENT (Max 6 Lines):

* PROJECT TITLE: Disease Trend Analysis (Project ID: P-01)
* DOMAIN: Healthcare Data Analytics / Public Health Surveillance
* CANDIDATE: Arg Jain | University Roll No. 2500320140031
* ACADEMIC PROGRAM: MCA 2nd Year (Data Analytics Specialization)
* INSTITUTION: ABES Engineering College, Ghaziabad (AKTU Code 032)
* FACULTY MENTOR: Ms. Kalpana Dwivedi | Date: November 2026
VERBATIM SPEAKER SCRIPT (~30 Seconds):

"Good morning, respected external examiner and faculty mentor Ms. Kalpana Dwivedi. My name is Arg Jain, Roll No. 2500320140031. Today, I am proud to present Project P-01: 'Disease Trend Analysis', an interactive public health surveillance intelligence platform developed as part of my MCA 2nd Year Data Analytics curriculum at ABES Engineering College."


### SLIDE 2: Business Problem & Top 2 HMW Statements

ON-SCREEN SLIDE CONTENT (Max 6 Lines):

* THE PROBLEM: Public health authorities lack a unified, interactive visual platform to monitor disease trends across states, time, and demographics.
* THE IMPACT: Results in delayed outbreak detection, inefficient ICU bed allocation, and misdirected health budgets.
* HMW-01 [Priority]: How might we help health officers instantly spot which disease is spiking in a region vs. last year?
* HMW-03 [Priority]: How might we help policy makers compare Case Fatality Rates (CFR) across states in a single glance to justify targeted emergency budgets?
VERBATIM SPEAKER SCRIPT (~30 Seconds):

"In our problem analysis, we discovered that Indian epidemiological surveillance data is severely fragmented across static monthly bulletins, causing multi-week delays in emergency intervention. Applying design thinking, we framed top opportunities: HMW-01 addresses instant outbreak detection compared to previous baselines, while HMW-03 provides policy makers a single-glance Case Fatality Rate matrix to justify targeted healthcare budgets."


### SLIDE 3: Key Stakeholders & Governance

ON-SCREEN SLIDE CONTENT (Max 6 Lines):

* SH-01: Public Health Officer (High Influence) — Deploys rapid field containment teams and issues regional health advisories.
* SH-02: Hospital Administrator (High Influence) — Anticipates seasonal surges to pre-allocate hospital beds, ICU units, and oxygen supplies.
* SH-03: Policy Maker / Ministry (High Influence) — Evaluates mortality severity to authorize emergency containment budgets.
* SH-04: Epidemiologist / Researcher (Medium Influence) — Investigates demographic vulnerability profiles and urban crowding correlations.
* GOVERNANCE: System satisfies the decision needs of all 4 operational personas through role-specific filtering.
VERBATIM SPEAKER SCRIPT (~30 Seconds):

"The system serves three high-influence stakeholders: Public Health Officers who deploy containment teams, Hospital Administrators who manage critical-care bed surge capacity, and Policy Makers who approve emergency health financing. Each persona interacts with customized analytical views through our unified interactive dashboard."


### SLIDE 4: End-to-End Requirements Traceability (RTM)

ON-SCREEN SLIDE CONTENT (Max 6 Lines):

* RTM-01: OQ-01 -> HMW-01 -> BR-01 -> US-04 -> disease_cases.cases_reported -> UI-01 -> TC-F-01, TC-T-02
* RTM-02: OQ-02 -> HMW-02 -> BR-02 -> US-06 -> region_master.region_name -> UI-01 -> TC-F-03, TC-T-03
* RTM-03: OQ-05 -> HMW-03 -> BR-03 -> US-07 -> disease_cases.deaths -> UI-03 -> TC-F-09, TC-T-09
* RTM-04: OQ-08 -> HMW-05 -> BR-05 -> US-15 -> disease_cases.is_outbreak -> UI-05 -> TC-F-13, TC-T-13
* AUDIT STATUS: 100% of 10 OQs, 10 HMWs, and 15 BRs trace end-to-end to verified code and passing tests.
VERBATIM SPEAKER SCRIPT (~30 Seconds):

"To ensure professional engineering rigor, we maintained a 100% complete Requirements Traceability Matrix. As visible on this slide, every stakeholder need directly maps to a Business Requirement, an Agile User Story, a physical SQLite database column, a dedicated UI screen, and both functional and technical automated test cases."


### SLIDE 5: Data Architecture & Quality Interventions

ON-SCREEN SLIDE CONTENT (Max 6 Lines):

* DATASET VOLUME: 3,003 records in disease_cases fact table (5 diseases, 10 states, 60 months: 2020–2024).
* RELATIONAL SCHEMA: 5 base tables in SQLite (`data/app.db`) + 1 joined view (`v_disease_analysis`, 35 columns).
* EMBEDDED CLINICAL PATTERNS: Monsoon Dengue surge, COVID-19 2021 spike, urban density incidence correlation.
* PIPELINE CLEANING 1: 3 exact duplicate reporting rows purged via `df.drop_duplicates()`.
* PIPELINE CLEANING 2: 54 missing case values imputed using group median per disease entity.
* PIPELINE CLEANING 3: 5 typographic extreme spikes (> 3.0*IQR) bounded via Winsorization capping.
VERBATIM SPEAKER SCRIPT (~30 Seconds):

"Our data layer models 60 months of epidemiological history across 10 Indian states. We embedded authentic clinical patterns, including post-monsoon vector-borne surges and the 2021 pandemic wave. Our cleaning pipeline automatically purges 3 duplicate rows, imputes 54 null values using disease medians, and bounds 5 extreme outliers to certify data integrity."


### SLIDE 6: Solution Architecture & Technical Flow

ON-SCREEN SLIDE CONTENT (Max 6 Lines):

* DATA TIER: SQLite 3 relational repository (`data/app.db`) enforcing PK/FK and non-negative CHECK constraints.
* INGESTION & CACHE: `src/data_loader.py` with `@st.cache_data(ttl=3600)` enabling sub-second query execution.
* ANALYTICAL ENGINE: Pure Python modules in `src/analysis.py` computing CFR%, recovery%, YoY%, and Pearson r.
* UI & STYLING: Streamlit 1.35 multi-page architecture + Tailwind CSS components injected via iframe.
* DEPLOYMENT: Streamlit Community Cloud with public HTTPS URL (zero cloud hosting licensing cost).
VERBATIM SPEAKER SCRIPT (~30 Seconds):

"Our technical architecture follows a modular decoupled pipeline: SQLite stores normalized records; `@st.cache_data` memoizes database projections in memory; pure Python functions compute mathematical ratios; and Tailwind CSS is injected into Streamlit to deliver a modern corporate visual experience with zero cloud hosting expense."


### SLIDE 7: Interactive Dashboard Screens

ON-SCREEN SLIDE CONTENT (Max 6 Lines):

* UI-01 (Executive Overview): 4 Tailwind KPI cards (Cases, Deaths, Recoveries, CFR), regional burden bar ranking.
* UI-02 (Longitudinal Trends): 60-month time-series line, multi-year overlapping YoY curves, 12-month seasonal heatmap.
* UI-03 (Regional Analysis): Cross-state CFR benchmarking and clinical recovery efficacy comparison bars.
* UI-04 (Demographics): 5-bracket stacked age group bar chart and gender distribution donut chart.
* UI-05 (Advanced EDA): Urban density scatter plot with OLS trendline, automated concurrent outbreak surge alerts.
* UI-06 (Data Quality): Pipeline cleaning accounting scorecard ledger and one-click filtered CSV dataset export.
VERBATIM SPEAKER SCRIPT (~30 Seconds):

"The application provides six dedicated analytical screens: UI-01 displays executive KPI cards and state rankings; UI-02 maps 60-month trends and seasonal heatmaps; UI-03 and 04 explore regional CFR and demographic vulnerability; while UI-05 surfaces statistical crowding correlations and concurrent outbreak alerts."


### SLIDE 8: Key Analytical Findings & Proofs

ON-SCREEN SLIDE CONTENT (Max 6 Lines):

* FINDING 1 (Pandemic Wave): COVID-19 surged by +279% in 2021 vs. 2020, followed by steady decline (OQ-01, OQ-09).
* FINDING 2 (Seasonal Cyclicity): Dengue cases surge by 6.04x during August monsoon months (1,401 avg) vs. January (231 avg) (OQ-03, OQ-10).
* FINDING 3 (Urban Crowding Correlation): Strong positive correlation (Pearson r = 0.84, p < 0.001) between state population density and disease incidence (OQ-06).
* FINDING 4 (Geriatric Risk): Senior cohort (60+) displays 5.5% Case Fatality Rate vs. 1.5% general population average (OQ-04).
VERBATIM SPEAKER SCRIPT (~30 Seconds):

"Our analysis revealed four statistically verifiable findings: COVID-19 experienced a 279% surge in 2021; Dengue incidence surges by over 6x during August monsoon weeks; state population density strongly correlates with infection velocity with a Pearson r of 0.84; and senior demographics face a 3.6x higher fatality rate."


### SLIDE 9: Quality Assurance & Verification Suite

ON-SCREEN SLIDE CONTENT (Max 6 Lines):

* AUTOMATED TESTS: 17/17 automated tests executed and passing with 100% success rate (zero critical failures).
* DATABASE TESTS (8 Tests): Table existence, 3,003 row volume, zero orphan FKs, and non-negative bounds verified.
* ANALYSIS TESTS (6 Tests): Known-vector validation of CFR (5.0%), Recovery (92.0%), YoY (+100%), and Pearson r (1.0).
* UI & CONFIG TESTS (3 Tests): Application routes, modular source packages, and pinned manifests verified.
* LATENCY VERIFICATION: Cold database analytical query completes in 0.042 seconds (Threshold: < 1.50s).
VERBATIM SPEAKER SCRIPT (~30 Seconds):

"Our automated QA suite executed 17 rigorous technical tests, achieving a 100% pass rate. We verified relational integrity, zero orphaned records, mathematical accuracy on known calculation vectors, and verified that cold database queries execute in just 0.042 seconds—well below our 1.5-second SLA threshold."


### SLIDE 10: Recommendations & Future Roadmap

ON-SCREEN SLIDE CONTENT (Max 6 Lines):

* STRATEGIC RECOMMENDATION: Transition synthetic pipelines to live district-level ICMR API feeds for active containment.
* SYSTEM LIMITATION 1: Synthetic data, while statistically calibrated, cannot model real-time behavioral shifts.
* SYSTEM LIMITATION 2: Free-tier cloud instances hibernate after 7 days of inactivity (re-wakes automatically upon visit).
* PHASE 2 ROADMAP 1: Deploy predictive Machine Learning forecasting (ARIMA / Prophet) for 60-day outbreak projection.
* PHASE 2 ROADMAP 2: Integrate automated WhatsApp and SMS outbound emergency dispatch alerts for field triage teams.
VERBATIM SPEAKER SCRIPT (~30 Seconds):

"We recommend transitioning this platform to live ICMR district data feeds for operational surveillance. In Phase 2, we plan to integrate ARIMA and Prophet machine learning models for 60-day predictive outbreak forecasting, and enable automated SMS dispatch notifications to hospital administrators."


### SLIDE 11: Live Demonstration & Artifact Links

ON-SCREEN SLIDE CONTENT (Max 6 Lines):

* LIVE APPLICATION URL: https://2500320140031-dta.streamlit.app
* GITHUB CODE REPOSITORY: https://github.com/Argjain/2500320140031-disease-trend-analysis.
* FULL PROJECT DOCUMENTATION: Complete 18-step deliverables available in `docs/` folder.
* DEMONSTRATION SCOPE: Resolving all 10 Operational Questions live in under 5 minutes.
* THANK YOU: Respected faculty and jury members. I am now open for viva voce questions.
VERBATIM SPEAKER SCRIPT (~30 Seconds):

"In conclusion, the platform is live and fully accessible at the URL shown on screen, backed by our public GitHub repository. All 10 Operational Questions can be demonstrated live in the running application. Thank you, respected evaluators, and I look forward to your questions."

18_ArgJain_DiseaseTrendAnalysis_Presentation.docx | ABES Presentation Deck | November 2026


---
### 📋 Embedded Data Tables


#### Table 1

| Project ID & Title | P-01 / Disease Trend Analysis |
| --- | --- |
| Domain | Healthcare Data Analytics |
| Presenter / Student | Arg Jain (Roll No. 2500320140031) |
| Academic Program | MCA 2nd Year (Data Analytics Specialization) |
| Institution | ABES Engineering College, Ghaziabad |
| Faculty Project Mentor | Ms. Kalpana Dwivedi |
| Deck Structure | 11 Formal Slides (Conforming to ABES PPT Template) |
| Total Presentation Time | 5 Minutes (30 Seconds Allocation per Slide) |
| Release Date | November 2026 |



#### Table 2

| Slide # | Slide Title | Target Time Budget | Elapsed Time | Core Focus of Spoken Remarks |
| --- | --- | --- | --- | --- |
| Slide 1 | Title & Project Attribution | 0:20 min | 0:20 | Greet evaluators, introduce project ID P-01, student credentials, and faculty mentor. |
| Slide 2 | Problem Statement & Top 2 HMWs | 0:30 min | 0:50 | State public health surveillance latency problem and introduce HMW-01 and HMW-03. |
| Slide 3 | Key Stakeholders & Influence | 0:25 min | 1:15 | Highlight Public Health Officer, Hospital Admin, and Policy Maker decision rights. |
| Slide 4 | Requirements Traceability (RTM) | 0:30 min | 1:45 | Demonstrate seamless end-to-end trace from HMW to BR, User Story, Code, and Test. |
| Slide 5 | Data Architecture & Quality Pipeline | 0:30 min | 2:15 | Present 3,000-row fact dataset, 5 clinical patterns, and 3 data cleaning interventions. |
| Slide 6 | Solution Architecture & Tech Flow | 0:30 min | 2:45 | Walk through data flow: SQLite to cached loader, cleaning, analytics, and Tailwind UI. |
| Slide 7 | Interactive Dashboard Screens | 0:30 min | 3:15 | Showcase UI-01 Overview KPI cards and UI-02 60-month longitudinal time-series lines. |
| Slide 8 | Key Analytical Findings & Proofs | 0:35 min | 3:50 | Present COVID 2021 spike (+300%), Dengue monsoon peak (6x), and density correlation. |
| Slide 9 | Quality Assurance & Test Suite (17/17) | 0:25 min | 4:15 | Announce 17/17 automated tests passing, 0 critical failures, sub-second latency. |
| Slide 10 | Recommendations & Future Scope | 0:25 min | 4:40 | Recommend district ICMR ingestion, note free-tier limitations, propose ML forecasting. |
| Slide 11 | Live Cloud Demonstration & Links | 0:20 min | 5:00 | Present live Streamlit Cloud URL, GitHub repository, and transition to jury Q&A. |

