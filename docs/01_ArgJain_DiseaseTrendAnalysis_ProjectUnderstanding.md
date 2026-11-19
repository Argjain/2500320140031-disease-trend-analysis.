# 01 ArgJain DiseaseTrendAnalysis ProjectUnderstanding

DISEASE TREND ANALYSIS

STEP 1 — Project Understanding Document


## 1. Problem Statement

Healthcare authorities and public health analysts in India lack a unified, interactive visual platform to monitor disease occurrence trends across regions, time periods, and demographic groups, resulting in delayed outbreak detection, inefficient resource allocation, and missed opportunities for preventive intervention.


## 2. Intended Audience / Users

The application serves multiple user personas with varying frequency of use and analytical needs:


## 3. Stakeholder Register


## 4. Operational Questions (OQ-01 to OQ-10)

The following 10 questions represent the core analytical capabilities the app must deliver. Every OQ has been verified as answerable from the planned synthetic dataset.

Data Coverage Check: All 10 OQs are fully answerable from the planned synthetic dataset (disease, region, date, demographics, case/death/recovery counts).


## 5. Objectives (SMART)


## 6. Project Scope


### 6.1 In Scope

* Synthetic disease incidence dataset: 5 diseases (Dengue, Malaria, Tuberculosis, COVID-19, Typhoid), 10 Indian states, monthly data January 2020 to December 2024, with demographic breakdown by age group and gender.
* Exploratory Data Analysis (EDA): descriptive statistics, trend analysis, year-over-year change, correlation analysis.
* Interactive Plotly visualisations: time-series line chart, regional bar chart, choropleth map (state level), heatmap, scatter plot (incidence vs. density), pie chart (disease share).
* Multi-page Streamlit app with Tailwind-style CSS theming and sidebar filters.
* SQLite relational database as the data backend with structured schema.
* pytest test suite with at least 15 test cases and at least 80% code coverage.
* ABES-format Project Document (Word) covering all 18 project steps.
* ABES slide deck for final mentor presentation.
* Deployment on Streamlit Community Cloud (free tier) with shareable public URL.

### 6.2 Out of Scope

* Real or live patient data or any integration with hospital information systems (privacy/regulatory constraints).
* Predictive modelling or Machine Learning-based disease forecasting.
* Mobile application development (iOS or Android).
* User authentication, login system, or role-based access control.
* Real-time data ingestion, REST API integration, or external live data feeds.
* Multi-language (non-English) user interface support.
* Automated email or SMS alerting to stakeholders.

## 7. Assumptions and Constraints


### 7.1 Assumptions


### 7.2 Constraints


## 8. Success Criteria (Measurable)

File: 01_ArgJain_DiseaseTrendAnalysis_ProjectUnderstanding.docx  |  v1.0  |  Nov 2026  |  ABES Engineering College


---
### 📋 Embedded Data Tables


#### Table 1

| Project ID | P-01 |
| --- | --- |
| Project Title | Disease Trend Analysis |
| Domain | Healthcare Data Analytics |
| Student Name | Arg Jain |
| Roll Number | 2500320140031 |
| Course | MCA 2nd Year — Data Analytics |
| Institute | ABES Engineering College, Ghaziabad |
| Mentor | Ms. Kalpana Dwivedi |
| Document Version | v1.0 |
| Date | November 2026 |



#### Table 2

| User Type | Description | Frequency of Use | Primary Goal |
| --- | --- | --- | --- |
| Public Health Officer | State/district health dept official monitoring outbreak signals | Daily / Weekly | Spot emerging disease spikes and deploy response teams |
| Epidemiologist / Researcher | Medical researcher analysing disease spread patterns | Weekly | Identify risk factors, correlations, seasonal patterns |
| Hospital Administrator | Admin managing bed capacity & medical supplies | Weekly / Monthly | Anticipate patient surge and allocate resources proactively |
| Policy Maker / Health Minister | Senior official deciding on public health budgets | Monthly | Evidence-based budget approvals and policy decisions |
| MCA Data Analytics Student | Developer and academic user demonstrating the project | As needed | Demonstrate EDA skills; satisfy academic submission requirements |



#### Table 3

| SH ID | Stakeholder | Role | Interest | Influence | Key Decision Made with App |
| --- | --- | --- | --- | --- | --- |
| SH-01 | Public Health Officer | Primary User | Monitor & control disease outbreaks | H | Deploy field response teams; issue public health alerts |
| SH-02 | Hospital Administrator | Primary User | Manage hospital capacity efficiently | H | Allocate beds, medicines, and ICU resources ahead of surge |
| SH-03 | Policy Maker / Health Ministry | Decision Maker | Assess severity; justify budget allocation | H | Approve emergency health budgets; enforce containment measures |
| SH-04 | Epidemiologist / Researcher | Analyst | Understand disease dynamics and risk factors | M | Design targeted intervention studies; publish research findings |
| SH-05 | Arg Jain (Student Developer) | Developer & User | Demonstrate data analytics competency | M | Academic submission and project evaluation decisions |
| SH-06 | Ms. Kalpana Dwivedi (Mentor) | Evaluator | Ensure academic quality and correctness | L | Grade the project; approve for final submission |



#### Table 4

| OQ ID | Operational Question | Stakeholder(s) | Data Required | Answerable |
| --- | --- | --- | --- | --- |
| OQ-01 | Which diseases have shown the highest increase in reported cases over the last 5 years? | SH-01, SH-03 | Disease name, year, case count | YES |
| OQ-02 | Which geographic regions (states) are most affected by each disease? | SH-01, SH-02 | Region, disease name, case count | YES |
| OQ-03 | What is the monthly/seasonal trend of disease outbreaks? | SH-01, SH-04 | Date (month/year), disease, case count | YES |
| OQ-04 | Which age group and gender are most vulnerable to specific diseases? | SH-04, SH-03 | Age group, gender, disease, case count | YES |
| OQ-05 | What is the case fatality rate (CFR) for each disease across regions? | SH-02, SH-03 | Cases, deaths, disease, region | YES |
| OQ-06 | How does disease incidence correlate with population density? | SH-04 | Region, population (density derived), case count | YES |
| OQ-07 | Which diseases have the highest recovery rates, and in which regions? | SH-02, SH-01 | Cases, recoveries, disease, region | YES |
| OQ-08 | Are there concurrent disease outbreaks (co-occurring epidemics) in any region? | SH-01, SH-04 | Date, region, multiple disease case counts | YES |
| OQ-09 | What is the year-over-year (YoY) percentage change in reported cases per disease? | SH-03, SH-01 | Year, disease, case count | YES |
| OQ-10 | Which months see peak disease reporting, and does this vary by disease type? | SH-01, SH-04 | Month, disease, case count | YES |



#### Table 5

| OBJ ID | Objective Statement | Measurable Target | Time-Bound |
| --- | --- | --- | --- |
| OBJ-01 | Build a Streamlit app that answers all 10 OQs using synthetic epidemiological data covering 5 diseases, 10 Indian states, over 5 years (2020-2024). | 10/10 OQs demonstrable in live walkthrough | Dec 2026 |
| OBJ-02 | Provide 6 or more interactive Plotly visualisations (line, bar, heatmap, scatter, pie, choropleth) with filters for disease, region, year, and demographic. | At least 6 chart types; each loads in under 5 seconds | Dec 2026 |
| OBJ-03 | Achieve 80% or higher pytest coverage with 15 or more test cases and zero critical test failures at submission. | pytest --cov report: coverage >= 80%, 0 critical failures | Dec 2026 |
| OBJ-04 | Deploy the app on Streamlit Community Cloud with the public URL accessible during the final evaluation window. | Live URL accessible; 99% uptime over last 2 weeks of semester | Dec 2026 |
| OBJ-05 | Produce a complete ABES-format Project Document covering all 18 steps and a slide deck with full traceability to Business Requirements. | 18-section document and presentation deck submitted and approved by mentor | Dec 2026 |



#### Table 6

| Assumption ID | Assumption Statement |
| --- | --- |
| A-01 | Synthetic data generated using Python (Faker, NumPy, Pandas) will simulate realistic disease trends without using any real patient data. |
| A-02 | Region refers to 10 selected Indian states: Uttar Pradesh, Maharashtra, Delhi, Rajasthan, Bihar, West Bengal, Tamil Nadu, Karnataka, Gujarat, Madhya Pradesh. |
| A-03 | Diseases covered are Dengue, Malaria, Tuberculosis (TB), COVID-19, and Typhoid, representing major public health concerns in India. |
| A-04 | Dataset spans January 2020 to December 2024 (60 months) with monthly granularity. |
| A-05 | Age groups defined as: 0-14, 15-29, 30-44, 45-59, 60 and above. Gender categories: Male, Female, Other. |
| A-06 | Stable internet access is available for Streamlit Community Cloud deployment and evaluation. |
| A-07 | The mentor will evaluate the app via the public Streamlit URL during the final two weeks of the semester. |



#### Table 7

| Constraint ID | Category | Constraint Statement |
| --- | --- | --- |
| C-01 | Timeline | Project must be fully completed and submitted by end of MCA Semester (December 2026). |
| C-02 | Technology | Only free and open-source tools permitted: Python 3.10+, Streamlit, SQLite, Plotly, pytest. |
| C-03 | Data Privacy | No real personal health data may be used at any stage; synthetic data only. |
| C-04 | Hosting | App must run within Streamlit Community Cloud free-tier limits (1 GB RAM, shared CPU). |
| C-05 | Team Size | Individual project: all work must be performed solely by Arg Jain. |



#### Table 8

| SC ID | Success Criterion | Measurement Method | Target Value |
| --- | --- | --- | --- |
| SC-01 | All 10 Operational Questions are answerable through the app UI | Live mentor walkthrough demonstration | 10 out of 10 OQs answered |
| SC-02 | App loads and renders all charts within acceptable response time | Manual timer measurement on Streamlit Cloud URL | Under 5 seconds initial load |
| SC-03 | pytest test suite passes with sufficient coverage and no critical failures | pytest --cov report output at submission | 80% or higher coverage, 0 critical failures |
| SC-04 | Project document is complete and covers all 18 steps with traceability | Mentor document review against ABES template checklist | All 18 sections completed and approved |
| SC-05 | Final presentation is evaluated positively by the mentor | Mentor evaluation rubric score from viva/presentation | 70% or higher marks |
| SC-06 | Application remains accessible during evaluation window without downtime | Streamlit Community Cloud URL availability check | 99% uptime during final 2 weeks of semester |

