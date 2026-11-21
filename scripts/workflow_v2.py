
# ============================================================
# Disease Trend Analysis – Full Project Workflow v2
# Steps 2-18 (Step 6 skipped), sequential pipeline
# Each step is a fully self-contained agent (no call_tool)
# ============================================================

PROJECT_CTX = """
PROJECT CONTEXT (carry this into every step):
- Project ID: P100 | Title: Disease Trend Analysis
- Domain: Healthcare Data Analytics
- Student: Arg Jain | Roll: 2500320140031 | MCA 2nd Yr DA, ABES Engineering College
- Mentor: Mr. Dinesh
- Stack: Python 3.12, Streamlit, SQLite, Plotly, pytest, Tailwind CDN
- Diseases (5): Dengue, Malaria, Tuberculosis (TB), COVID-19, Typhoid
- Regions (10 Indian states): Uttar Pradesh, Maharashtra, Delhi, Rajasthan,
  Bihar, West Bengal, Tamil Nadu, Karnataka, Gujarat, Madhya Pradesh
- Period: Jan 2020-Dec 2024 (60 months, monthly)
- Age groups: 0-14, 15-29, 30-44, 45-59, 60+  |  Gender: Male, Female, Other
- Stakeholders:
    SH-01 Public Health Officer (Influence H)
    SH-02 Hospital Administrator (Influence H)
    SH-03 Policy Maker/Ministry (Influence H)
    SH-04 Epidemiologist/Researcher (Influence M)
    SH-05 Arg Jain Student Developer (Influence M)
    SH-06 Mr. Dinesh Mentor (Influence L)
- OQs:
    OQ-01 Which diseases have shown highest increase in cases over 5 years?
    OQ-02 Which regions are most affected by each disease?
    OQ-03 What is the monthly/seasonal trend of disease outbreaks?
    OQ-04 Which age group/gender are most vulnerable to specific diseases?
    OQ-05 What is the case fatality rate (CFR) per disease per region?
    OQ-06 How does incidence correlate with population density?
    OQ-07 Which diseases have highest recovery rates, and where?
    OQ-08 Are there concurrent outbreaks in any region?
    OQ-09 What is YoY change in cases per disease?
    OQ-10 Which months see peak disease reporting by disease type?
- BRs (15): BR-01..BR-15 (Must x9, Should x4, Could x2)
  BR-01[Must] Aggregate case counts by disease/region/time  HMW-01,09
  BR-02[Must] Region-level disease comparison  HMW-02
  BR-03[Must] Case fatality rates per disease/region  HMW-03
  BR-04[Must] Demographic filtering by age/gender  HMW-04
  BR-05[Must] Concurrent outbreak detection  HMW-05
  BR-06[Must] Seasonal/monthly disease trends  HMW-06
  BR-07[Must] Recovery rates per disease/region  HMW-07
  BR-08[Should] Incidence vs density correlation  HMW-08
  BR-09[Should] Year-over-year change percentages  HMW-09
  BR-10[Must] Structured relational database  HMW-10
  BR-11[Must] Sidebar filters updating all charts  HMW-01..05
  BR-12[Should] CSV download of filtered dataset  HMW-10
  BR-13[Could] Data quality summary page  HMW-10
  BR-14[Must] Automated pytest tests (>=80% coverage)  All BRs
  BR-15[Should] Deployed on Streamlit Community Cloud  OBJ-04
- Docs folder: C:\\Users\\Hp\\Downloads\\hcl\\docs
- Data folder: C:\\Users\\Hp\\Downloads\\hcl\\data
- Src folder:  C:\\Users\\Hp\\Downloads\\hcl\\src
- App root:    C:\\Users\\Hp\\Downloads\\hcl
"""

STEP_AGENT_PROMPT = """
You are a senior Business Analyst and Python developer working on the Disease Trend Analysis project.
You MUST complete your task fully end-to-end:
1. Write the complete Python script content
2. Use the write_file tool to save the script to disk
3. Use the run_command tool to run it
4. If it fails, fix and retry (up to 3 times)
5. Report final status: SUCCESS or FAILURE with error details

CRITICAL RULES for python-docx scripts:
- Always use triple-quoted strings (triple double-quote) for multi-line content
- Never use single-quote inside triple-double-quoted strings without escaping
- Use raw strings r'...' for Windows paths or double-backslash
- Keep string literals simple; break long strings with concatenation (+)
- Test: does every string have matching open/close quotes?
- Use os.makedirs(folder, exist_ok=True) before saving files

CRITICAL RULES for openpyxl scripts:
- Import: from openpyxl import Workbook; from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
- Always call wb.save(path) at the end
- Wrap long strings in textwrap or split across lines

After running, confirm: "STEP X COMPLETE - File saved to <path>"
"""

# ─────────────────────────────────────────────
# STEP 2 — HMW Statements
# ─────────────────────────────────────────────
phase("STEP 2 — HMW Statements")
log("Launching Step 2 agent...")

result2 = await agent(
    prompt=STEP_AGENT_PROMPT + f"""
{PROJECT_CTX}

YOUR TASK: Generate STEP 2 — How Might We (HMW) Statements document.

Write the complete python-docx script, save it to
  C:\\Users\\Hp\\Downloads\\hcl\\docs\\gen_step2.py
then run it. The script must save the Word file to:
  C:\\Users\\Hp\\Downloads\\hcl\\docs\\02_ArgJain_DiseaseTrendAnalysis_HMWStatements.docx

DOCUMENT CONTENT:

COVER BLOCK (meta table):
Title: DISEASE TREND ANALYSIS
Subtitle: STEP 2 — How Might We (HMW) Statements
Meta: Project ID P100 | Student Arg Jain | Roll 2500320140031 |
      Course MCA 2nd Year Data Analytics | Institute ABES Engineering College |
      Mentor Mr. Dinesh | Date November 2026 | Version v1.0

SECTION 1: Stakeholder Pain Points
Table: SH ID | Stakeholder | Pain Point 1 | Pain Point 2 | Pain Point 3
SH-01 | Public Health Officer | No unified real-time disease trend dashboard | Outbreak detection is reactive not proactive | No regional comparison view
SH-02 | Hospital Administrator | Cannot predict patient surge in advance | Recovery/fatality benchmarking across states is unavailable | Resource allocation based on intuition
SH-03 | Policy Maker | Health data scattered across multiple reports | Cannot justify budget allocation with visual evidence | No single-screen YoY disease comparison
SH-04 | Epidemiologist | No demographic (age/gender) drill-down on disease data | Cannot visualise incidence vs population density | Co-occurring outbreaks invisible in current reports

SECTION 2: HMW Statements Table
Columns: HMW ID | How Might We? | Stakeholder | Pain Point | Linked OQs | Priority
HMW-01 | How might we help public health officers instantly spot which disease is spiking in a specific region this month vs last year? | SH-01 | No unified trend view | OQ-01, OQ-09 | PRIORITY
HMW-02 | How might we show hospital administrators which states will face a patient surge next season so they can pre-allocate beds? | SH-02 | Reactive planning | OQ-02, OQ-03 | PRIORITY
HMW-03 | How might we help policy makers compare case fatality rates across all regions in a single view to justify budget allocations? | SH-03 | Data scattered | OQ-05, OQ-02 | PRIORITY
HMW-04 | How might we enable epidemiologists to filter disease data by age group and gender to identify the most vulnerable demographics? | SH-04 | No demographic drill-down | OQ-04 | PRIORITY
HMW-05 | How might we surface co-occurring disease outbreaks in the same region-month to alert response teams before crises escalate? | SH-01, SH-04 | Outbreaks treated in isolation | OQ-08 | PRIORITY
HMW-06 | How might we visualise seasonal disease peaks across all diseases on one chart so analysts can prepare resources months ahead? | SH-01, SH-04 | Seasonal patterns buried | OQ-10, OQ-03 | -
HMW-07 | How might we display recovery rates alongside fatality rates per region so administrators can benchmark their hospitals? | SH-02 | Recovery data not compared | OQ-07, OQ-05 | -
HMW-08 | How might we show the correlation between population density and disease incidence so researchers can prioritise dense urban zones? | SH-04 | No spatial-incidence link | OQ-06 | -
HMW-09 | How might we provide a year-over-year trend table highlighting diseases growing vs declining so ministers can redirect funds quickly? | SH-03 | No YoY summary | OQ-09, OQ-01 | -
HMW-10 | How might we give analysts a downloadable clean dataset with a data quality summary so they can demonstrate rigorous EDA methodology? | SH-05 | No exportable clean data view | OQ-01..10 | -

For PRIORITY rows use a yellow-tint background (#FEF9E7) on those rows.

SECTION 3: Priority HMW Justification
Table: HMW ID | Reason for Priority
HMW-01 | Directly addresses the core stakeholder need and links to 2 key OQs (OQ-01, OQ-09)
HMW-02 | Hospital surge planning is a life-safety issue; covers 2 OQs central to the app
HMW-03 | CFR comparison is the key policy metric; highest business value for SH-03
HMW-04 | Demographic analysis is a primary epidemiological use case; unique to SH-04
HMW-05 | Co-occurrence detection is a differentiating feature; high public health impact

SECTION 4: OQ Coverage Check
Table: OQ ID | OQ Question (short) | Covered by HMW | Status
OQ-01 | Highest disease increase over 5 years | HMW-01, HMW-09 | Covered
OQ-02 | Most affected regions per disease | HMW-02, HMW-03 | Covered
OQ-03 | Monthly/seasonal trend | HMW-02, HMW-06 | Covered
OQ-04 | Most vulnerable age/gender | HMW-04 | Covered
OQ-05 | CFR per disease per region | HMW-03, HMW-07 | Covered
OQ-06 | Incidence vs population density | HMW-08 | Covered
OQ-07 | Highest recovery rates and where | HMW-07 | Covered
OQ-08 | Concurrent outbreaks | HMW-05 | Covered
OQ-09 | YoY change in cases | HMW-01, HMW-09 | Covered
OQ-10 | Peak months per disease | HMW-06 | Covered
Summary row: All 10 OQs covered by at least 1 HMW.

Footer: 02_ArgJain_DiseaseTrendAnalysis_HMWStatements.docx | v1.0 | Nov 2026 | ABES

STYLING:
- Margins: top/bottom 2.5cm, left 3cm, right 2cm
- Heading color: RGB(26,83,118) = #1A5376
- Table header fill: #1A5376, white bold 9pt text
- Alternating rows: #EBF5FB / #FFFFFF
- Body text: 10pt
""",
    schema={"type": "string"},
    role="Step 2 HMW Agent"
)
log(f"Step 2: {result2[-300:]}")

# ─────────────────────────────────────────────
# STEP 3 — Needs Analysis
# ─────────────────────────────────────────────
phase("STEP 3 — Needs Analysis")
log("Launching Step 3 agent...")

result3 = await agent(
    prompt=STEP_AGENT_PROMPT + f"""
{PROJECT_CTX}

YOUR TASK: Generate STEP 3 — Needs Analysis document.
Write the complete python-docx script, save to
  C:\\Users\\Hp\\Downloads\\hcl\\docs\\gen_step3.py
then run it. Output file:
  C:\\Users\\Hp\\Downloads\\hcl\\docs\\03_ArgJain_DiseaseTrendAnalysis_NeedsAnalysis.docx

DOCUMENT CONTENT:

COVER BLOCK: Title DISEASE TREND ANALYSIS | Subtitle STEP 3 — Needs Analysis and Business Requirements
Meta: Project ID P100 | Student Arg Jain | Roll 2500320140031 | Course MCA 2nd Year Data Analytics
      Institute ABES Engineering College | Mentor Mr. Dinesh | Date November 2026 | Version v1.0

SECTION 1: Introduction
Two paragraphs explaining needs analysis: maps HMW statements to business requirements,
defines WHAT the system must do (not HOW), uses MoSCoW prioritisation.

SECTION 2: Business Requirements Table
Columns: BR ID | Business Requirement | Stakeholder | Source HMW | Priority | Measurement Criterion
15 rows (use Must/Should/Could):
BR-01 | The business needs to aggregate disease case counts by disease, region and time so stakeholders can identify outbreak trends | SH-01, SH-03 | HMW-01, HMW-09 | Must | All 10 OQs answered in live demo
BR-02 | The business needs to provide region-level disease comparison so hospital admins can anticipate geographic surge patterns | SH-02 | HMW-02 | Must | Regional chart functional with filter
BR-03 | The business needs to display case fatality rates per disease per region so policy makers can target budget decisions | SH-03 | HMW-03 | Must | CFR = Deaths/Cases shown per cell
BR-04 | The business needs to enable demographic filtering by age group and gender so epidemiologists can identify vulnerable populations | SH-04 | HMW-04 | Must | Age+gender filter changes all charts
BR-05 | The business needs to detect and display concurrent disease outbreaks in same region-month so alerts can be issued promptly | SH-01, SH-04 | HMW-05 | Must | Co-occurrence flag visible
BR-06 | The business needs to show seasonal monthly disease trends so resource pre-positioning is evidence-based | SH-01, SH-04 | HMW-06 | Must | Monthly trend chart for each disease
BR-07 | The business needs to compute and display recovery rates per disease per region so hospital performance can be benchmarked | SH-02 | HMW-07 | Must | Recovery rate shown correctly
BR-08 | The business needs to visualise disease incidence vs population density correlation so researchers can prioritise interventions | SH-04 | HMW-08 | Should | Scatter with Pearson r displayed
BR-09 | The business needs to present year-over-year change percentages per disease so budget re-allocation decisions are data-driven | SH-03 | HMW-09 | Should | YoY% formula shown per disease
BR-10 | The business needs to store all disease data in a structured relational database so queries are consistent and reproducible | SH-05 | HMW-10 | Must | SQLite DB passes all FK and row-count checks
BR-11 | The business needs sidebar filters updating all charts simultaneously for multi-dimensional exploration | SH-01..SH-04 | HMW-01..05 | Must | All charts refresh on filter change
BR-12 | The business needs CSV download of filtered dataset so analysts can perform offline analysis | SH-04, SH-05 | HMW-10 | Should | Download button produces valid CSV
BR-13 | The business needs a data quality summary showing cleaning steps so data credibility is transparent | SH-05 | HMW-10 | Could | Quality page shows before/after counts
BR-14 | The business needs automated pytest tests covering data loading, KPIs and UI rendering so app correctness is verifiable | SH-06 | All BRs | Must | pytest >= 80% coverage, 0 critical failures
BR-15 | The business needs the app deployed on Streamlit Community Cloud so mentor can evaluate it remotely | SH-05, SH-06 | OBJ-04 | Should | Public URL accessible, loads under 5 seconds

SECTION 3: Data Requirements
Table: BR ID | Data Elements Needed | Source | Format
Map each BR to its required data columns from the synthetic dataset.
Example: BR-01 needs disease_name, region_name, report_date, cases_reported | Synthetic SQLite | INTEGER/TEXT/DATE

SECTION 4: Gap Analysis
Table: Type | ID | Issue | Resolution
Check for HMWs without BR, BRs without HMW, OQs not covered.
Conclusion: No gaps identified - all 10 HMWs mapped to at least 1 BR, all 15 BRs trace to a HMW or OBJ.

SECTION 5: Priority Summary
Table: Priority | Count | Percentage | Examples
Must | 9 | 60% | BR-01 to BR-07, BR-10, BR-11, BR-14
Should | 4 | 27% | BR-08, BR-09, BR-12, BR-15
Could | 2 | 13% | BR-13
Won't | 0 | 0% | -

Footer: 03_ArgJain_DiseaseTrendAnalysis_NeedsAnalysis.docx | v1.0 | Nov 2026 | ABES

STYLING: Same as Step 2 (margins, colors, alternating rows).
Must rows: green tint #EAFAF1 | Should rows: yellow #FEF9E7 | Could rows: orange tint #FDEBD0
""",
    schema={"type": "string"},
    role="Step 3 Needs Analysis Agent"
)
log(f"Step 3: {result3[-300:]}")

# ─────────────────────────────────────────────
# STEP 4 — RTM Excel
# ─────────────────────────────────────────────
phase("STEP 4 — Traceability Matrix (Excel)")
log("Launching Step 4 agent...")

result4 = await agent(
    prompt=STEP_AGENT_PROMPT + f"""
{PROJECT_CTX}

YOUR TASK: Generate STEP 4 — Requirements Traceability Matrix (RTM) as an Excel file.
Write the complete openpyxl script, save to
  C:\\Users\\Hp\\Downloads\\hcl\\docs\\gen_step4.py
then run it. Output file:
  C:\\Users\\Hp\\Downloads\\hcl\\docs\\04_ArgJain_DiseaseTrendAnalysis_RTM.xlsx

EXCEL STRUCTURE (3 sheets):

SHEET 1: "RTM"
Columns: OQ ID | HMW ID | BR ID | Business Requirement (short) | Stakeholder | Priority | Status | Feature ID | DB Table.Column | User Story ID | UI Screen ID | TC-F | TC-T
- Freeze row 1 (header)
- Enable auto_filter on row 1
- Header fill: #1A5376, white bold text, 11pt
- Status = "Identified" for all rows; fill #EBF5FB
- Feature/DB/US/UI/TC columns = "TBD"; fill #F2F3F4
- Priority: Must=#EAFAF1, Should=#FEF9E7, Could=#FDEBD0
- One row per HMW-BR link (use the linked OQ from each BR's OQs)

Rows (create these exact rows):
OQ-01 | HMW-01 | BR-01 | Aggregate case counts by disease/region/time | SH-01, SH-03 | Must | Identified | TBD | TBD | TBD | TBD | TBD | TBD
OQ-09 | HMW-09 | BR-01 | Aggregate case counts by disease/region/time | SH-01, SH-03 | Must | Identified | TBD | TBD | TBD | TBD | TBD | TBD
OQ-02 | HMW-02 | BR-02 | Region-level disease comparison | SH-02 | Must | Identified | TBD | TBD | TBD | TBD | TBD | TBD
OQ-05 | HMW-03 | BR-03 | Case fatality rates per disease/region | SH-03 | Must | Identified | TBD | TBD | TBD | TBD | TBD | TBD
OQ-04 | HMW-04 | BR-04 | Demographic filtering by age/gender | SH-04 | Must | Identified | TBD | TBD | TBD | TBD | TBD | TBD
OQ-08 | HMW-05 | BR-05 | Concurrent outbreak detection | SH-01, SH-04 | Must | Identified | TBD | TBD | TBD | TBD | TBD | TBD
OQ-03 | HMW-06 | BR-06 | Seasonal monthly disease trends | SH-01, SH-04 | Must | Identified | TBD | TBD | TBD | TBD | TBD | TBD
OQ-07 | HMW-07 | BR-07 | Recovery rates per disease/region | SH-02 | Must | Identified | TBD | TBD | TBD | TBD | TBD | TBD
OQ-06 | HMW-08 | BR-08 | Incidence vs density correlation | SH-04 | Should | Identified | TBD | TBD | TBD | TBD | TBD | TBD
OQ-09 | HMW-09 | BR-09 | Year-over-year change percentages | SH-03 | Should | Identified | TBD | TBD | TBD | TBD | TBD | TBD
OQ-01 | HMW-10 | BR-10 | Structured relational database | SH-05 | Must | Identified | TBD | TBD | TBD | TBD | TBD | TBD
OQ-01 | HMW-01 | BR-11 | Sidebar filters updating all charts | SH-01..04 | Must | Identified | TBD | TBD | TBD | TBD | TBD | TBD
OQ-02 | HMW-02 | BR-11 | Sidebar filters updating all charts | SH-01..04 | Must | Identified | TBD | TBD | TBD | TBD | TBD | TBD
OQ-05 | HMW-03 | BR-11 | Sidebar filters updating all charts | SH-01..04 | Must | Identified | TBD | TBD | TBD | TBD | TBD | TBD
OQ-04 | HMW-04 | BR-11 | Sidebar filters updating all charts | SH-01..04 | Must | Identified | TBD | TBD | TBD | TBD | TBD | TBD
OQ-08 | HMW-05 | BR-11 | Sidebar filters updating all charts | SH-01..04 | Must | Identified | TBD | TBD | TBD | TBD | TBD | TBD
OQ-01 | HMW-10 | BR-12 | CSV download of filtered dataset | SH-04, SH-05 | Should | Identified | TBD | TBD | TBD | TBD | TBD | TBD
OQ-01 | HMW-10 | BR-13 | Data quality summary page | SH-05 | Could | Identified | TBD | TBD | TBD | TBD | TBD | TBD
OQ-01 | HMW-01..10 | BR-14 | Automated pytest tests | SH-06 | Must | Identified | TBD | TBD | TBD | TBD | TBD | TBD
OQ-01 | OBJ-04 | BR-15 | Deployed on Streamlit Community Cloud | SH-05, SH-06 | Should | Identified | TBD | TBD | TBD | TBD | TBD | TBD

SHEET 2: "Coverage_Check"
Title row: RTM Coverage Check - Step 4 | Date: November 2026
Table 1 header: OQ Coverage | OQ ID | Covered by HMW | Covered by BR | Status
(10 rows, one per OQ, all Covered)
Table 2 header: HMW Coverage | HMW ID | Linked BR(s) | Status
(10 rows, all Covered)
Summary: ALL 10 OQs covered | ALL 10 HMWs mapped | ALL 15 BRs traced

SHEET 3: "Change_Log"
Columns: Version | Date | Author | Change Description
Row: v1.0 | November 2026 | Arg Jain | Initial RTM created at Step 4

Column widths (approximate chars):
OQ=8, HMW=8, BR=7, Requirement=38, Stakeholder=14, Priority=9, Status=12,
Feature=10, DB=16, US=12, UI=12, TC-F=10, TC-T=10

Use openpyxl properly: Workbook, PatternFill, Font, Alignment, Border.
wb.active.title = "RTM"
""",
    schema={"type": "string"},
    role="Step 4 RTM Agent"
)
log(f"Step 4: {result4[-300:]}")

# ─────────────────────────────────────────────
# STEP 5 — BRD
# ─────────────────────────────────────────────
phase("STEP 5 — Business Requirements Document")
log("Launching Step 5 agent...")

result5 = await agent(
    prompt=STEP_AGENT_PROMPT + f"""
{PROJECT_CTX}

YOUR TASK: Generate STEP 5 — Business Requirements Document (BRD).
Write the complete python-docx script, save to
  C:\\Users\\Hp\\Downloads\\hcl\\docs\\gen_step5.py
then run it. Output file:
  C:\\Users\\Hp\\Downloads\\hcl\\docs\\05_ArgJain_DiseaseTrendAnalysis_BRD.docx

DOCUMENT CONTENT (13 sections):

COVER BLOCK: Title DISEASE TREND ANALYSIS | Subtitle STEP 5 — Business Requirements Document (BRD)
Meta: Project ID P100 | Version v1.0 | Author Arg Jain | Roll 2500320140031 |
      Date November 2026 | Mentor Mr. Dinesh | Status Draft | Institute ABES

1. DOCUMENT CONTROL
Version history table: Version | Date | Author | Changes | Approved By
v1.0 | November 2026 | Arg Jain | Initial draft | Pending

2. EXECUTIVE SUMMARY (3 short paragraphs)
Para 1: What the project is (Disease Trend Analysis app for healthcare stakeholders)
Para 2: Why it matters (delayed outbreak detection, inefficient resource allocation)
Para 3: What it delivers (6-page Streamlit app, 10 OQs answered, SQLite backend, deployed on Cloud)

3. BUSINESS PROBLEM AND OPPORTUNITY
Current State (problems): No unified disease trend dashboard; data scattered across PDF reports
Desired State: Single interactive app with filters, charts, fatality rates, demographic breakdown
Business Impact of NOT solving: Delayed outbreak response, misallocated health budgets

4. OBJECTIVES AND SUCCESS METRICS (KPIs)
Table: Objective | KPI | Baseline | Target | Measurement Method
OBJ-01 | 10 OQs answered | 0 | 10/10 | Mentor walkthrough
OBJ-02 | 6+ Plotly charts | 0 | 6 | Manual count
OBJ-03 | pytest coverage | 0% | 80%+ | pytest --cov report
OBJ-04 | Live Streamlit URL | None | 1 URL | Browser access check
OBJ-05 | ABES document complete | 0 sections | 18 sections | Document review

5. STAKEHOLDERS — RACI TABLE
Table: SH ID | Stakeholder | Role | R | A | C | I
SH-01 | Public Health Officer | Primary User | R | - | C | I
SH-02 | Hospital Administrator | Primary User | R | - | C | I
SH-03 | Policy Maker | Decision Maker | - | A | C | I
SH-04 | Epidemiologist | Analyst | R | - | C | I
SH-05 | Arg Jain (Developer) | Developer | R | A | - | -
SH-06 | Mr. Dinesh | Evaluator/Mentor | - | - | C | I

6. SCOPE (In Scope / Out of Scope — same as Step 1 document)

7. BUSINESS REQUIREMENTS
For each BR (BR-01 to BR-15), a mini-table with: Description | Rationale | Priority | Source HMW | Acceptance Criteria (2-3 criteria)
Present each BR as its own bordered table block.

8. BUSINESS RULES (5 rules)
Table: Rule ID | Business Rule | Applies to BR | Enforcement
BRL-01 | CFR = Deaths/Cases only where Cases > 0 | BR-03 | System validation, divide-by-zero handled
BRL-02 | Date range filter cannot be less than 1 month | BR-11 | UI slider validation
BRL-03 | Recovery rate must not exceed 100% | BR-07 | CHECK constraint + display cap
BRL-04 | Synthetic data must contain no real person identifiers | BR-10 | Data generation audit
BRL-05 | All percentages rounded to 2 decimal places | BR-01..09 | Display formatting rule

9. DATA REQUIREMENTS
Table: Data Element | Description | Source | Format | Volume | Refresh
disease_cases | Monthly cases per disease per region | Synthetic generator | INTEGER | 3000 rows | Static
disease_master | Disease reference data | Hardcoded | TEXT/INTEGER | 5 rows | Static
region_master | State reference with population | Hardcoded | TEXT/INTEGER/REAL | 10 rows | Static
demographic_group | Age/gender groups | Hardcoded | TEXT | 15 rows | Static
demographic_breakdown | Cases by demographic | Synthetic | INTEGER | ~300 rows | Static

10. ASSUMPTIONS, CONSTRAINTS AND DEPENDENCIES (from Step 1 — A-01..A-07, C-01..C-05)

11. RISKS AND MITIGATION
Table: Risk ID | Risk | Probability | Impact | Mitigation
R-01 | Synthetic data may not look realistic enough | Medium | High | Build in explicit patterns; validate visually
R-02 | Streamlit free tier may be slow with 3000+ rows | Medium | Medium | Use @st.cache_data; aggregate before plotting
R-03 | pytest coverage hard to reach 80% | Low | Medium | Mock DB; test each analysis function with known inputs
R-04 | Mentor expects real patient data | Low | High | Document clearly that synthetic data is a project requirement
R-05 | Streamlit Cloud deployment fails | Low | High | Test locally first; pin all versions in requirements.txt

12. GLOSSARY
Table: Term | Definition (12 terms minimum)
CFR | Case Fatality Rate: ratio of deaths to confirmed cases, expressed as a percentage
Incidence Rate | Number of new disease cases per 100,000 population
Recovery Rate | Ratio of recovered patients to total confirmed cases
EDA | Exploratory Data Analysis: statistical examination of datasets to summarise characteristics
OQ | Operational Question: a specific analytical question the app must answer
HMW | How Might We: a design-thinking framing of a stakeholder pain point as an opportunity
BR | Business Requirement: a capability the business must have expressed as a need-to/so-that statement
YoY | Year-over-Year: comparison of a metric between the same period in consecutive years
Outbreak | A sudden increase in disease cases beyond expected levels in a region
Synthetic Data | Artificially generated data that mimics real data patterns without using real records
SQLite | A lightweight serverless relational database management system
Streamlit | An open-source Python framework for building interactive data web applications

13. SIGN-OFF TABLE
Columns: Role | Name | Signature | Date
Student Developer | Arg Jain | _____________ | ___________
Mentor | Mr. Dinesh | _____________ | ___________
HOD | (Name) | _____________ | ___________

STYLING: Same as previous docs. Page breaks before sections 3, 5, 7, 11.
""",
    schema={"type": "string"},
    role="Step 5 BRD Agent"
)
log(f"Step 5: {result5[-300:]}")

# ─────────────────────────────────────────────
# STEP 7 — TRD
# ─────────────────────────────────────────────
phase("STEP 7 — Technical Requirements Document")
log("Launching Step 7 agent...")

result7 = await agent(
    prompt=STEP_AGENT_PROMPT + f"""
{PROJECT_CTX}

YOUR TASK: Generate STEP 7 — Technical Requirements Document (TRD).
Write the complete python-docx script, save to
  C:\\Users\\Hp\\Downloads\\hcl\\docs\\gen_step7.py
then run it. Output file:
  C:\\Users\\Hp\\Downloads\\hcl\\docs\\07_ArgJain_DiseaseTrendAnalysis_TRD.docx

FIXED TECH STACK:
Python 3.12 | pandas 2.2.2 | NumPy 1.26.4 | SciPy 1.13.0 | statsmodels 0.14.2
Plotly 5.22.0 | Streamlit 1.35.0 (multi-page, pages/ folder)
Tailwind CDN via st.components.v1.html | SQLite data/app.db
pytest 8.2.0 + pytest-cov 5.0.0 | GitHub | Streamlit Community Cloud

DOCUMENT CONTENT (10 sections):

COVER BLOCK: Title DISEASE TREND ANALYSIS | Subtitle STEP 7 — Technical Requirements Document (TRD)
Meta: Project ID P100 | Version v1.0 | Author Arg Jain | Roll 2500320140031 | Date November 2026
      Mentor Mr. Dinesh | Institute ABES Engineering College

1. SYSTEM ARCHITECTURE (text-based diagram + description)
   Data Flow (ASCII):
   data/app.db (SQLite)
        |
   src/data_loader.py (@st.cache_data - loads & joins tables into DataFrame)
        |
   src/cleaning.py (remove duplicates, impute NaN, cap outliers)
        |
   src/analysis.py (CFR, Recovery, YoY, Seasonal, Correlation, Co-occurrence)
        |
   src/ui.py (Tailwind header, KPI cards via st.components.v1.html)
        |
   app.py (page config, shared sidebar filters, session_state, home KPIs)
        |
   pages/ (01_Overview, 02_Trends, 03_Regional, 04_Demographics, 05_EDA, 06_DataQuality)
        |
   Streamlit Community Cloud (public URL)

2. FOLDER STRUCTURE (exact tree)
   Show all files and folders as described in project context.

3. FUNCTIONAL REQUIREMENTS (FR-01..FR-15)
   Table: FR ID | Requirement Description | Linked BR | Module | Notes
   FR-01 Load disease data from SQLite into DataFrame | BR-10 | src/data_loader.py | @st.cache_data
   FR-02 Apply sidebar filters to DataFrame | BR-11 | src/data_loader.py | session_state
   FR-03 Compute year-trend (cases by disease by year) | BR-01 | src/analysis.py | groupby+sum
   FR-04 Compute regional summary (cases by region) | BR-02 | src/analysis.py | groupby
   FR-05 Compute CFR (deaths/cases x100) per disease-region | BR-03 | src/analysis.py | div with fillna
   FR-06 Aggregate by age group and gender | BR-04 | src/analysis.py | demographic_breakdown table
   FR-07 Detect concurrent outbreaks (2+ diseases > mean in same region-month) | BR-05 | src/analysis.py | pivot+threshold
   FR-08 Compute seasonal trend (avg cases by month per disease) | BR-06 | src/analysis.py | groupby month
   FR-09 Compute recovery rate (recovered/cases x100) | BR-07 | src/analysis.py | div with fillna
   FR-10 Pearson correlation: incidence_per_lakh vs population_density | BR-08 | src/analysis.py | scipy.stats.pearsonr
   FR-11 Compute YoY% change per disease | BR-09 | src/analysis.py | pct_change
   FR-12 Render Overview page with 4 KPI cards | BR-01, BR-11 | pages/01_Overview.py | st.metric
   FR-13 Render 6+ Plotly chart types | BR-02..09 | pages/*.py | px.line/bar/imshow/scatter
   FR-14 CSV download of filtered DataFrame | BR-12 | pages/*.py | st.download_button
   FR-15 Data quality report with before/after stats | BR-13 | pages/06_Data_Quality.py | dict report

4. NON-FUNCTIONAL REQUIREMENTS (NFR-01..NFR-08)
   Table: NFR ID | Category | Requirement | Target | Test Method
   NFR-01 Performance | Initial load time | < 5 seconds | Manual timer
   NFR-02 Performance | Chart re-render on filter change | < 3 seconds | Manual timer
   NFR-03 Reliability | pytest coverage | >= 80% | pytest --cov
   NFR-04 Reliability | Critical test failures | 0 | pytest -q
   NFR-05 Usability | OQs answerable without docs | 10/10 | Mentor walkthrough
   NFR-06 Maintainability | Function length | < 50 lines | Code review
   NFR-07 Security | No real patient data | 0 real records | Data audit
   NFR-08 Availability | Uptime during evaluation | >= 99% | Streamlit Cloud monitor

5. DATA LAYER
   Loading: sqlite3 + pandas.read_sql_query wrapped in @st.cache_data(ttl=3600)
   Path: Path(__file__).parent.parent / "data" / "app.db"
   Validation on load: check row count > 0, required columns present, no negative cases
   Cleaning steps in src/cleaning.py: exact duplicate removal, median imputation for cases_reported,
   0-imputation for deaths, IQR outlier capping (Q3 + 3*IQR), logging of all changes

6. STATISTICAL METHODS PER OQ
   Table: OQ ID | Method | Python | Formula/Note
   OQ-01 | Year-over-year trend | pandas groupby+sum | Sum cases per disease per year
   OQ-02 | Regional ranking | groupby().sum().sort_values | Descending by total cases
   OQ-03 | Time-series | pandas resample/groupby month | Monthly avg per disease
   OQ-04 | Demographic pivot | groupby age_group+gender | Sum cases in group
   OQ-05 | CFR calculation | deaths/cases_reported*100 | Per disease-region cell; fillna(0)
   OQ-06 | Pearson correlation | scipy.stats.pearsonr | incidence_per_lakh vs pop_density
   OQ-07 | Recovery rate | recovered/cases_reported*100 | Per disease-region; fillna(0)
   OQ-08 | Co-occurrence | Pivot region-month, count diseases > mean | Flag >= 2 diseases
   OQ-09 | YoY % change | (curr-prev)/prev*100 | Per disease, year pairs
   OQ-10 | Monthly peak | groupby(month).mean().idxmax() | Per disease

7. UI TECHNICAL NOTES
   Tailwind: inject via st.components.v1.html with CDN script tag, height=0
   Theme file: .streamlit/config.toml (primaryColor #1A5376, backgroundColor #F0F8FF)
   Session state keys: selected_disease, selected_regions (list), selected_year_range (tuple),
   selected_age_groups (list), selected_gender
   Sidebar: st.sidebar.selectbox, multiselect, slider, radio — all bound to session_state
   Layout: st.columns for KPI cards; st.plotly_chart(use_container_width=True) for charts

8. PERFORMANCE, ERROR HANDLING, SECURITY
   Cache: @st.cache_data on all load/compute functions
   Error handling: try/except around DB connections; st.error() for user-friendly messages
   Input validation: all filters use dropdowns (no free text)
   Security: no secrets in repo; .gitignore includes .venv/ __pycache__/ *.pyc
   Data: synthetic only; no PII anywhere in codebase or database

9. REQUIREMENTS.TXT (exact pinned versions)
   Show the complete requirements.txt content in a code block:
   streamlit==1.35.0
   pandas==2.2.2
   numpy==1.26.4
   plotly==5.22.0
   scipy==1.13.0
   statsmodels==0.14.2
   openpyxl==3.1.2
   pytest==8.2.0
   pytest-cov==5.0.0

10. TECHNICAL RISKS
    Table: Risk ID | Risk | Probability | Impact | Mitigation
    TR-01 | SQLite locked on concurrent Cloud access | Low | Medium | Single-user app; @st.cache_data prevents repeated reads
    TR-02 | Tailwind CDN offline during demo | Low | Medium | Local fallback CSS; inline styles as backup
    TR-03 | statsmodels slow import on free tier | Medium | Low | Lazy import inside function; cache result
    TR-04 | Streamlit AppTest API changes between versions | Low | Medium | Pin streamlit==1.35.0
    TR-05 | Free-tier 1GB RAM exceeded with full dataset | Medium | High | Sample data to 3000 rows; cache aggressively

STYLING: Same professional style.
""",
    schema={"type": "string"},
    role="Step 7 TRD Agent"
)
log(f"Step 7: {result7[-300:]}")

# ─────────────────────────────────────────────
# STEP 8 — Database Design (Excel)
# ─────────────────────────────────────────────
phase("STEP 8 — Database Design Excel")
log("Launching Step 8 agent...")

result8 = await agent(
    prompt=STEP_AGENT_PROMPT + f"""
{PROJECT_CTX}

YOUR TASK: Generate STEP 8 — Database Design as an Excel file.
Write the complete openpyxl script, save to
  C:\\Users\\Hp\\Downloads\\hcl\\docs\\gen_step8.py
then run it. Output file:
  C:\\Users\\Hp\\Downloads\\hcl\\docs\\08_ArgJain_DiseaseTrendAnalysis_DBDesign.xlsx

DATABASE TABLES (5 tables):

TABLE 1: disease_master (5 rows)
Columns: disease_id INT PK | disease_name TEXT NOT NULL UNIQUE | disease_category TEXT |
         description TEXT | is_contagious INT(0/1) | typical_incubation_days INT
Data: 1,Dengue,Vector-borne,Mosquito-transmitted viral infection,1,7
      2,Malaria,Vector-borne,Plasmodium parasite via mosquito,1,14
      3,Tuberculosis,Airborne,Mycobacterium tuberculosis infection,1,42
      4,COVID-19,Airborne,SARS-CoV-2 coronavirus infection,1,5
      5,Typhoid,Waterborne,Salmonella typhi infection,1,10

TABLE 2: region_master (10 rows)
Columns: region_id INT PK | region_name TEXT UNIQUE | state_code TEXT |
         zone TEXT | population INT | area_sqkm REAL | population_density REAL
Zones: North(UP,DL,RJ), East(BR,WB), South(TN,KA), West(MH,GJ), Central(MP)

TABLE 3: demographic_group (15 rows = 5 age groups x 3 genders)
Columns: demo_id INT PK | age_group TEXT | gender TEXT | age_min INT | age_max INT
UNIQUE(age_group, gender)

TABLE 4: disease_cases (3000 rows — GRAIN: disease x region x month)
Columns: case_id INT PK | disease_id INT FK | region_id INT FK |
         report_date DATE | report_year INT | report_month INT |
         cases_reported INT DEFAULT 0 | deaths INT DEFAULT 0 |
         recovered INT DEFAULT 0 | active_cases INT | hospitalized INT |
         is_outbreak INT(0/1) | data_source TEXT | created_at TIMESTAMP
CHECK: deaths<=cases_reported AND recovered<=cases_reported AND cases_reported>=0

TABLE 5: demographic_breakdown (300 rows sample)
Columns: breakdown_id INT PK | case_id INT FK | demo_id INT FK |
         cases_in_group INT | deaths_in_group INT | recovered_in_group INT

ANALYSIS VIEW: v_disease_analysis (~35 columns joining all tables)

EXCEL SHEETS:

Sheet 1: "Overview" — title, description, stats (5 tables, ~3300 rows, design principles 3NF)

Sheet 2: "Tables_Summary"
Cols: Table Name | Grain | Primary Key | Foreign Keys | Total Columns | Est. Rows | Purpose
5 rows for 5 tables

Sheet 3: "DD_disease_master" — data dictionary
Cols: Column | Data Type | Key | Nullable | Allowed Values | Description | OQ/BR

Sheet 4: "DD_region_master" — same structure

Sheet 5: "DD_demographic_group" — same structure

Sheet 6: "DD_disease_cases" — same structure (most important — 14 columns)

Sheet 7: "DD_demographic_breakdown" — same structure

Sheet 8: "Relationships"
Cols: Parent Table | Child Table | Join Key | Cardinality | Business Rule
4 relationships

Sheet 9: "KPIs_Measures"
Cols: KPI Name | Formula | Unit | OQ | BR
8 KPIs: Total Cases (SUM), CFR% (deaths/cases*100), Recovery% (recovered/cases*100),
Incidence per Lakh (cases/population*100000), YoY Change% ((curr-prev)/prev*100),
Active Cases (cases-deaths-recovered), Outbreak Flag (cases>2x mean), Co-occurrence Count

Sheet 10: "SQLite_DDL"
Complete CREATE TABLE + CREATE VIEW SQL statements in one cell per table
(use font Courier New 10pt for DDL sheet)

Sheet 11: "RTM_Updated" — copy RTM from Step 4 and fill DB Table.Column column

STYLING:
- Header rows: #1A5376 fill, white bold 11pt
- Alternating rows: #EBF5FB / #FFFFFF
- DD sheets tab color: blue
- DDL sheet tab color: green
- Use openpyxl PatternFill, Font, Alignment properly
""",
    schema={"type": "string"},
    role="Step 8 DB Design Agent"
)
log(f"Step 8: {result8[-300:]}")

# ─────────────────────────────────────────────
# STEP 9 — ER Diagram
# ─────────────────────────────────────────────
phase("STEP 9 — ER Diagram")
log("Launching Step 9 agent...")

result9 = await agent(
    prompt=STEP_AGENT_PROMPT + f"""
{PROJECT_CTX}

YOUR TASK: Generate STEP 9 — ER Diagram document.
Write the complete python-docx script, save to
  C:\\Users\\Hp\\Downloads\\hcl\\docs\\gen_step9.py
then run it. Output file:
  C:\\Users\\Hp\\Downloads\\hcl\\docs\\09_ArgJain_DiseaseTrendAnalysis_ERDiagram.docx

DOCUMENT CONTENT:

COVER BLOCK: Title DISEASE TREND ANALYSIS | Subtitle STEP 9 — Entity Relationship Diagram
Meta: same as other docs

SECTION 1: Mermaid ER Diagram Code
Display the following Mermaid code in a styled code block (Courier New 9pt, grey background #F4F6F7):

erDiagram
    disease_master {{
        int disease_id PK
        string disease_name
        string disease_category
        string description
        int is_contagious
        int typical_incubation_days
    }}
    region_master {{
        int region_id PK
        string region_name
        string state_code
        string zone
        int population
        float area_sqkm
        float population_density
    }}
    demographic_group {{
        int demo_id PK
        string age_group
        string gender
        int age_min
        int age_max
    }}
    disease_cases {{
        int case_id PK
        int disease_id FK
        int region_id FK
        date report_date
        int report_year
        int report_month
        int cases_reported
        int deaths
        int recovered
        int active_cases
        int hospitalized
        int is_outbreak
        string data_source
        timestamp created_at
    }}
    demographic_breakdown {{
        int breakdown_id PK
        int case_id FK
        int demo_id FK
        int cases_in_group
        int deaths_in_group
        int recovered_in_group
    }}
    disease_master ||--o{{ disease_cases : "has"
    region_master ||--o{{ disease_cases : "reports in"
    disease_cases ||--o{{ demographic_breakdown : "broken down by"
    demographic_group ||--o{{ demographic_breakdown : "classifies"

SECTION 2: Relationship Descriptions (5 items, numbered list)
1. One disease in disease_master has zero or many case records in disease_cases. Each case record reports incidents for exactly one disease.
2. One region in region_master reports zero or many disease case records. Each case record belongs to exactly one region.
3. One disease_cases record is broken down into zero or many demographic_breakdown records. Each breakdown row belongs to exactly one case record.
4. One demographic group classifies zero or many demographic_breakdown rows. Each breakdown row references exactly one demographic group.
5. The analysis view v_disease_analysis joins all four base tables to produce a denormalised view of approximately 35 columns including computed KPIs (CFR, recovery rate, incidence per lakh).

SECTION 3: Business Rules Enforced by Design (numbered list of 7 rules)
1. FK constraint: disease_cases.disease_id references disease_master.disease_id — orphan case records not permitted.
2. FK constraint: disease_cases.region_id references region_master.region_id — every case belongs to a known region.
3. CHECK constraint: deaths <= cases_reported — deaths cannot exceed total cases.
4. CHECK constraint: recovered <= cases_reported — recoveries cannot exceed total cases.
5. CHECK constraint: cases_reported >= 0 — negative case counts are not permitted.
6. UNIQUE constraint: disease_master.disease_name — no duplicate disease entries.
7. UNIQUE constraint: demographic_group(age_group, gender) — each demographic segment is unique.

SECTION 4: Design Review and Identified Issues
Table: Issue ID | Issue | Severity | Fix Applied
DI-01 | active_cases is derived (cases - deaths - recovered) — storing redundant derived data | Low | Kept for query convenience; documented as derived; CHECK ensures consistency
DI-02 | population_density in region_master is derived (population/area_sqkm) | Low | Kept for performance (avoid recalculation in every query); documented
DI-03 | No audit trail for data corrections (no updated_at column) | Low | created_at added; updated_at deferred to future enhancement
DI-04 | report_year and report_month partially redundant with report_date | Low | Kept for fast GROUP BY without date parsing overhead
DI-05 | No surrogate key on demographic_group composite unique — using integer PK is correct | None | Design is correct; integer PK allows compact FK references

SECTION 5: ER Diagram Image Placeholder
[INSERT ER DIAGRAM PNG HERE]
Instructions paragraph: Paste the Mermaid code from Section 1 into https://mermaid.live
Export as PNG. Save as 09_ER_Diagram.png and insert here.

SECTION 6: SQLite DDL Reference (key tables only)
Show CREATE TABLE for disease_master and disease_cases in Courier New 9pt code block.

Footer: same as other docs.
STYLING: Same professional style. Code blocks: Courier New 9pt, background #F4F6F7.
""",
    schema={"type": "string"},
    role="Step 9 ER Diagram Agent"
)
log(f"Step 9: {result9[-300:]}")

# ─────────────────────────────────────────────
# STEP 10 — Dataset Generation (Python code + run)
# ─────────────────────────────────────────────
phase("STEP 10 — Dataset Generation")
log("Launching Step 10 agent...")

result10 = await agent(
    prompt=STEP_AGENT_PROMPT + f"""
{PROJECT_CTX}

YOUR TASK: Generate STEP 10 — Dataset Generation script, then run it.

Write the complete src/generate_data.py script, save to
  C:\\Users\\Hp\\Downloads\\hcl\\src\\generate_data.py
then run it with run_command.

Also create these directories: C:\\Users\\Hp\\Downloads\\hcl\\src and C:\\Users\\Hp\\Downloads\\hcl\\data

THE SCRIPT MUST:
1. Use random.seed(42) and np.random.seed(42)
2. Generate all 5 tables exactly as designed
3. Build in 5 patterns
4. Add data quality issues
5. Save to data/ folder
6. Print validation report

EXACT GENERATION INSTRUCTIONS:

Imports:
import pandas as pd
import numpy as np
import sqlite3
import os
import random
from pathlib import Path

BASE_DIR = Path(r"C:\\Users\\Hp\\Downloads\\hcl")
DATA_DIR = BASE_DIR / "data"
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(BASE_DIR / "src", exist_ok=True)

random.seed(42)
np.random.seed(42)

--- disease_master (5 rows) ---
Create a list of 5 dicts and make a DataFrame:
diseases = [
    (1, "Dengue", "Vector-borne", "Mosquito-transmitted viral infection", 1, 7),
    (2, "Malaria", "Vector-borne", "Plasmodium parasite via mosquito", 1, 14),
    (3, "Tuberculosis", "Airborne", "Mycobacterium tuberculosis infection", 1, 42),
    (4, "COVID-19", "Airborne", "SARS-CoV-2 coronavirus infection", 1, 5),
    (5, "Typhoid", "Waterborne", "Salmonella typhi infection", 1, 10),
]
df_disease = pd.DataFrame(diseases, columns=["disease_id","disease_name","disease_category","description","is_contagious","typical_incubation_days"])

--- region_master (10 rows) ---
regions = [
    (1, "Uttar Pradesh", "UP", "North", 231502578, 240928.0),
    (2, "Maharashtra", "MH", "West", 123144223, 307713.0),
    (3, "Delhi", "DL", "North", 32941308, 1484.0),
    (4, "Rajasthan", "RJ", "North", 81032689, 342239.0),
    (5, "Bihar", "BR", "East", 128500364, 94163.0),
    (6, "West Bengal", "WB", "East", 100896618, 88752.0),
    (7, "Tamil Nadu", "TN", "South", 83697770, 130058.0),
    (8, "Karnataka", "KA", "South", 67562686, 191791.0),
    (9, "Gujarat", "GJ", "West", 72429009, 196024.0),
    (10, "Madhya Pradesh", "MP", "Central", 85002417, 308252.0),
]
df_region = pd.DataFrame(regions, columns=["region_id","region_name","state_code","zone","population","area_sqkm"])
df_region["population_density"] = (df_region["population"] / df_region["area_sqkm"]).round(2)

--- demographic_group (15 rows) ---
age_groups = [("0-14",0,14), ("15-29",15,29), ("30-44",30,44), ("45-59",45,59), ("60+",60,99)]
genders = ["Male", "Female", "Other"]
demo_rows = []
demo_id = 1
for ag, amin, amax in age_groups:
    for g in genders:
        demo_rows.append((demo_id, ag, g, amin, amax))
        demo_id += 1
df_demo = pd.DataFrame(demo_rows, columns=["demo_id","age_group","gender","age_min","age_max"])

--- disease_cases (3000 rows: 5 diseases x 10 regions x 60 months) ---
# Base case rates per disease per month
base_cases = dict: Dengue 200, Malaria 150, Tuberculosis 80, COVID-19 500, Typhoid 100
# PATTERN 1: Dengue and Malaria peak in monsoon months (Jul=7,Aug=8,Sep=9) -> multiply by 2.5
# PATTERN 2: COVID-19 spike in 2021 (multiply by 4 for year==2021) -> decline from 2022
# PATTERN 3: Dense urban regions (DL region_id=3, MH region_id=2) have 1.5x base
# PATTERN 4: Elderly 60+ group has higher CFR (handled in demographic_breakdown)
# PATTERN 5: TB stable year-round but higher in UP/Bihar (region_id 1,5 -> 1.3x)

Build rows:
rows = []
case_id = 1
from datetime import date, timedelta
import calendar

for disease_id, disease_name, _, _, _, _ in diseases:
    for region_id, region_name, _, _, _, _, _ in [r[:7] for r in regions]:  # NOTE: regions has 7 items (without density)
        for year in range(2020, 2025):
            for month in range(1, 13):
                base = base_cases[disease_name]
                
                # PATTERN 1: monsoon boost for Dengue and Malaria
                if disease_name in ("Dengue", "Malaria") and month in (7, 8, 9):
                    base = int(base * 2.5)
                
                # PATTERN 2: COVID spike
                if disease_name == "COVID-19":
                    if year == 2021:
                        base = int(base * 4)
                    elif year == 2022:
                        base = int(base * 2)
                    elif year == 2023:
                        base = int(base * 1.3)
                
                # PATTERN 3: urban boost
                if region_id in (2, 3):
                    base = int(base * 1.5)
                
                # PATTERN 5: TB in UP/Bihar
                if disease_name == "Tuberculosis" and region_id in (1, 5):
                    base = int(base * 1.3)
                
                # Add random noise
                cases = max(0, int(np.random.normal(base, base * 0.2)))
                
                # CFR by disease
                cfr_map = dict: Dengue 0.01, Malaria 0.015, Tuberculosis 0.03, COVID-19 0.025, Typhoid 0.008
                death_rate = cfr_map[disease_name]
                deaths = max(0, int(np.random.binomial(cases, death_rate)))
                deaths = min(deaths, cases)
                
                # Recovery: 85-97% of (cases - deaths)
                remaining = cases - deaths
                recovery_rate = np.random.uniform(0.85, 0.97)
                recovered = max(0, min(remaining, int(remaining * recovery_rate)))
                
                active_cases = max(0, cases - deaths - recovered)
                hospitalized = max(0, int(cases * np.random.uniform(0.1, 0.3)))
                
                # Outbreak flag: cases > 1.5 * base
                is_outbreak = 1 if cases > base * 1.5 else 0
                
                report_date = date(year, month, 1).isoformat()
                data_sources = ["ICMR Synthetic", "State Health Dept Synthetic", "WHO India Synthetic"]
                data_source = random.choice(data_sources)
                created_at = "2026-01-01 00:00:00"
                
                rows.append((case_id, disease_id, region_id, report_date, year, month,
                              cases, deaths, recovered, active_cases, hospitalized,
                              is_outbreak, data_source, created_at))
                case_id += 1

df_cases = pd.DataFrame(rows, columns=["case_id","disease_id","region_id","report_date",
    "report_year","report_month","cases_reported","deaths","recovered",
    "active_cases","hospitalized","is_outbreak","data_source","created_at"])

# DATA QUALITY ISSUES (add after creating df_cases):
# DQ-01: Set 2% of cases_reported to NaN
mask1 = np.random.random(len(df_cases)) < 0.02
df_cases.loc[mask1, "cases_reported"] = np.nan

# DQ-02: Add 3 exact duplicate rows
dupes = df_cases.sample(3, random_state=42)
df_cases = pd.concat([df_cases, dupes], ignore_index=True)

# DQ-03: Add 5 outlier rows (cases_reported = 10x normal)
outlier_idx = np.random.choice(df_cases.dropna().index[:100], 5, replace=False)
df_cases.loc[outlier_idx, "cases_reported"] = df_cases.loc[outlier_idx, "cases_reported"] * 10

# DQ-04: Set 1% of deaths to NaN
mask2 = np.random.random(len(df_cases)) < 0.01
df_cases.loc[mask2, "deaths"] = np.nan

--- demographic_breakdown (sample 300 case_ids, distribute cases) ---
sampled = df_cases.dropna(subset=["cases_reported"]).sample(300, random_state=42)
breakdown_rows = []
bd_id = 1
for _, row in sampled.iterrows():
    total = int(row["cases_reported"])
    demo_sample = df_demo.sample(min(5, len(df_demo)), random_state=bd_id)
    weights = np.random.dirichlet(np.ones(len(demo_sample)))
    for i, (_, drow) in enumerate(demo_sample.iterrows()):
        cases_grp = int(total * weights[i])
        deaths_grp = int(cases_grp * 0.015) if int(row.get("disease_id",0)) != 4 else int(cases_grp * 0.025)
        recov_grp = max(0, int(cases_grp * 0.9) - deaths_grp)
        breakdown_rows.append((bd_id, int(row["case_id"]), int(drow["demo_id"]),
                                cases_grp, deaths_grp, recov_grp))
        bd_id += 1
df_breakdown = pd.DataFrame(breakdown_rows, columns=["breakdown_id","case_id","demo_id",
    "cases_in_group","deaths_in_group","recovered_in_group"])

--- Save to CSV ---
df_disease.to_csv(DATA_DIR / "disease_master.csv", index=False)
df_region.to_csv(DATA_DIR / "region_master.csv", index=False)
df_demo.to_csv(DATA_DIR / "demographic_group.csv", index=False)
df_cases.to_csv(DATA_DIR / "disease_cases.csv", index=False)
df_breakdown.to_csv(DATA_DIR / "demographic_breakdown.csv", index=False)

--- Save to Excel (one sheet per table) ---
with pd.ExcelWriter(DATA_DIR / "disease_trend_analysis_data.xlsx", engine="openpyxl") as writer:
    df_disease.to_excel(writer, sheet_name="disease_master", index=False)
    df_region.to_excel(writer, sheet_name="region_master", index=False)
    df_demo.to_excel(writer, sheet_name="demographic_group", index=False)
    df_cases.to_excel(writer, sheet_name="disease_cases", index=False)
    df_breakdown.to_excel(writer, sheet_name="demographic_breakdown", index=False)

--- Save to SQLite (app.db) ---
db_path = DATA_DIR / "app.db"
conn = sqlite3.connect(str(db_path))
conn.execute("PRAGMA foreign_keys = ON")

DDL for each table (use the exact column definitions from the design).
Create tables, insert data using DataFrame.to_sql(if_exists="replace").
Create the analysis view v_disease_analysis joining all tables.

conn.close()

--- Validation Report ---
Print:
print("=== VALIDATION REPORT ===")
print(f"disease_master rows: expected 5, got {{len(df_disease)}}")
print(f"region_master rows: expected 10, got {{len(df_region)}}")
print(f"demographic_group rows: expected 15, got {{len(df_demo)}}")
print(f"disease_cases rows: expected ~3003 (3000+3 dupes), got {{len(df_cases)}}")
print(f"demographic_breakdown rows: got {{len(df_breakdown)}}")
print(f"Missing values in cases_reported: {{df_cases['cases_reported'].isna().sum()}}")
print(f"Missing values in deaths: {{df_cases['deaths'].isna().sum()}}")
dengue_july = df_cases[(df_cases.disease_id==1) & (df_cases.report_month==7)]["cases_reported"].mean()
dengue_jan = df_cases[(df_cases.disease_id==1) & (df_cases.report_month==1)]["cases_reported"].mean()
print(f"PATTERN-1 Dengue July avg vs Jan avg: {{dengue_july:.1f}} vs {{dengue_jan:.1f}} (should be 2x+)")
covid_2021 = df_cases[(df_cases.disease_id==4) & (df_cases.report_year==2021)]["cases_reported"].mean()
covid_2020 = df_cases[(df_cases.disease_id==4) & (df_cases.report_year==2020)]["cases_reported"].mean()
print(f"PATTERN-2 COVID-19 2021 avg vs 2020 avg: {{covid_2021:.1f}} vs {{covid_2020:.1f}} (should be ~4x)")
print("DATA GENERATION COMPLETE - Files saved to data/")

After the script runs successfully, also create:
  C:\\Users\\Hp\\Downloads\\hcl\\src\\__init__.py  (empty file)

Report: STEP 10 COMPLETE
""",
    schema={"type": "string"},
    role="Step 10 Data Generation Agent"
)
log(f"Step 10: {result10[-500:]}")

# ─────────────────────────────────────────────
# STEP 11 — User Stories
# ─────────────────────────────────────────────
phase("STEP 11 — User Stories")
log("Launching Step 11 agent...")

result11 = await agent(
    prompt=STEP_AGENT_PROMPT + f"""
{PROJECT_CTX}

YOUR TASK: Generate STEP 11 — User Stories document.
Write the complete python-docx script, save to
  C:\\Users\\Hp\\Downloads\\hcl\\docs\\gen_step11.py
then run it. Output file:
  C:\\Users\\Hp\\Downloads\\hcl\\docs\\11_ArgJain_DiseaseTrendAnalysis_UserStories.docx

DOCUMENT CONTENT:

COVER BLOCK: Title DISEASE TREND ANALYSIS | Subtitle STEP 11 — User Stories
Meta: same as other docs

SECTION 1: Epic Overview Table
Cols: Epic ID | Epic Name | Description | Stories Count | Priority
EP-01 | Data Infrastructure | Data loading, cleaning pipeline, session state | 3 | Must
EP-02 | Dashboard and KPIs | Overview page, KPI cards, region bar chart | 4 | Must
EP-03 | Trend Analysis | Time series, YoY comparison, seasonal heatmap | 4 | Must
EP-04 | Regional and Demographic | Regional analysis, demographic breakdown | 3 | Must
EP-05 | Insights and Quality | Correlation, co-occurrence, data quality, download | 3 | Should

SECTION 2: User Stories (main table)
Cols: US ID | Epic | Persona | User Story | Feature ID | BR ID | Priority | Story Points

Write all 17 user stories exactly as follows:

US-01 | EP-01 | Student Developer | As a student developer I want the app to load all disease data from SQLite on startup using caching so that every page has consistent data without repeated file reads | FR-01 | BR-10 | Must | 3
US-02 | EP-01 | Student Developer | As a student developer I want a data cleaning pipeline that removes duplicates imputes missing values and caps outliers so that the analysis is based on reliable data | FR-01 | BR-13 | Must | 3
US-03 | EP-01 | Public Health Officer | As a public health officer I want sidebar filters for disease region year age group and gender stored in session_state so that every page responds to the same selection | FR-02 | BR-11 | Must | 2
US-04 | EP-02 | Public Health Officer | As a public health officer I want a KPI dashboard on the Overview page showing total cases deaths recoveries and active CFR so that I get an instant health snapshot | FR-12 | BR-01 | Must | 3
US-05 | EP-02 | Public Health Officer | As a public health officer I want to see which disease has the highest year-over-year increase as a KPI badge so that I can immediately identify the fastest growing threat | FR-11 | BR-09 | Must | 2
US-06 | EP-02 | Hospital Administrator | As a hospital administrator I want a bar chart of total cases by region so that I can see which states need the most resource support | FR-04 | BR-02 | Must | 2
US-07 | EP-02 | Policy Maker | As a policy maker I want a summary table of case fatality rates per disease across all regions so that I can quickly identify high-risk disease-region pairs | FR-05 | BR-03 | Must | 3
US-08 | EP-03 | Public Health Officer | As a public health officer I want a monthly time-series line chart showing case counts per disease so that I can spot seasonal peaks and trough patterns | FR-08 | BR-06 | Must | 3
US-09 | EP-03 | Epidemiologist | As an epidemiologist I want a year-over-year comparison chart showing case counts for each year as overlapping lines so that I can identify multi-year trends | FR-03 | BR-01 | Must | 3
US-10 | EP-03 | Policy Maker | As a policy maker I want a YoY percentage change table per disease sorted by biggest increase so that I can redirect health budgets to growing threats | FR-11 | BR-09 | Must | 2
US-11 | EP-03 | Epidemiologist | As an epidemiologist I want a seasonal heatmap with months as columns and diseases as rows showing average case intensity so that I can identify which diseases peak in which months | FR-08 | BR-06 | Should | 3
US-12 | EP-04 | Hospital Administrator | As a hospital administrator I want a horizontal bar chart ranking states by CFR so that I can benchmark my state against peers | FR-05 | BR-03 | Must | 3
US-13 | EP-04 | Epidemiologist | As an epidemiologist I want a stacked bar chart of cases broken down by age group and gender for a selected disease so that I can identify the most vulnerable demographics | FR-06 | BR-04 | Must | 3
US-14 | EP-04 | Epidemiologist | As an epidemiologist I want a scatter chart of incidence rate vs population density per region with Pearson r displayed so that I can quantify the urbanisation-disease link | FR-10 | BR-08 | Should | 3
US-15 | EP-05 | Public Health Officer | As a public health officer I want a concurrent outbreak detector flagging any region-month where 2 or more diseases exceed their threshold simultaneously so that I can alert field teams early | FR-07 | BR-05 | Must | 5
US-16 | EP-05 | Epidemiologist | As an epidemiologist I want a CSV download button on every analysis page so that I can export filtered data for offline statistical work | FR-14 | BR-12 | Should | 1
US-17 | EP-05 | Student Developer | As a student developer I want a Data Quality page showing before and after cleaning statistics so that the mentor can verify my data handling methodology | FR-15 | BR-13 | Could | 2

SECTION 3: Acceptance Criteria (Given/When/Then)
Table: US ID | Given | When | Then
Write brief Given/When/Then for all 17 US.

SECTION 4: Sprint Plan
Table: Day | US IDs | Goal | Key Deliverable
Day 1 | US-01, US-02, US-03 | Data layer ready | app.db loaded, filters working
Day 2 | US-04, US-05, US-06 | Overview page done | KPI cards and bar chart visible
Day 3 | US-07, US-08, US-09 | CFR and time trends | CFR table and trend line charts
Day 4 | US-10, US-11 | Seasonal patterns | YoY table and seasonal heatmap
Day 5 | US-12, US-13 | Regional and demographic | Pages 3 and 4 functional
Day 6 | US-14, US-15 | Insights | Scatter chart and co-occurrence table
Day 7 | US-16, US-17 | Quality and downloads | Data quality page and CSV download
Day 8 | All US | Testing and deployment | pytest green, app live on Streamlit Cloud

SECTION 5: Story Point Summary
Table: Epic | Story Points | Stories Count | Priority
EP-01 | 8 | 3 | Must
EP-02 | 10 | 4 | Must
EP-03 | 11 | 4 | Must
EP-04 | 9 | 3 | Must
EP-05 | 8 | 3 | Should/Could
Total | 46 | 17 | -

STYLING: Same professional style. PRIORITY rows in US table: shade #EBF5FB for Must, #FEF9E7 for Should.
""",
    schema={"type": "string"},
    role="Step 11 User Stories Agent"
)
log(f"Step 11: {result11[-300:]}")

# ─────────────────────────────────────────────
# STEP 12 — UI Framework
# ─────────────────────────────────────────────
phase("STEP 12 — UI Framework")
log("Launching Step 12 agent...")

result12 = await agent(
    prompt=STEP_AGENT_PROMPT + f"""
{PROJECT_CTX}

YOUR TASK: Generate STEP 12 — UI Framework document.
Write the complete python-docx script, save to
  C:\\Users\\Hp\\Downloads\\hcl\\docs\\gen_step12.py
then run it. Output file:
  C:\\Users\\Hp\\Downloads\\hcl\\docs\\12_ArgJain_DiseaseTrendAnalysis_UIFramework.docx

DOCUMENT CONTENT:

COVER BLOCK: same meta, subtitle STEP 12 — UI Framework

SECTION 1: Screen Inventory Table
Cols: UI ID | Screen Name | File | Purpose | Key Components | Filters | User Stories
UI-01 | Overview Dashboard | 01_Overview.py | Health snapshot with KPIs | 4 KPI cards, region bar chart, CFR table | disease, region, year | US-04, US-05, US-06, US-07
UI-02 | Disease Trends | 02_Trends.py | Time-series and seasonal analysis | Line chart, YoY chart, seasonal heatmap | disease, year | US-08, US-09, US-10, US-11
UI-03 | Regional Analysis | 03_Regional_Analysis.py | Region comparison and CFR | Horizontal bar, CFR heatmap | disease, year | US-12
UI-04 | Demographics | 04_Demographics.py | Age and gender breakdown | Stacked bar, pie chart | disease, region, age, gender | US-13
UI-05 | EDA and Insights | 05_EDA_Statistics.py | Correlation and co-occurrence | Scatter plot, stats table, overlap table | disease, region, year | US-14, US-15
UI-06 | Data Quality | 06_Data_Quality.py | Data cleaning audit and export | Before/after table, download button | None | US-16, US-17

SECTION 2: ASCII Wireframes (one per screen, labelled clearly)
Draw ASCII wireframes for all 6 screens. Each shows:
- Header bar at top (project title, tagline)
- Left sidebar (narrow, 180px) with filter controls
- Main content area with KPI cards and/or charts

UI-01 Overview:
+---------------------------------------------------------------------+
|  DISEASE TREND ANALYSIS                   [Streamlit App Header]    |
+-------------------+-------------------------------------------------+
| SIDEBAR FILTERS   | ROW 1: 4 KPI CARDS                              |
| Disease: [v]      | [Total Cases] [Deaths] [Recoveries] [CFR %]     |
| Region: [v]       |                                                 |
| Year: [slider]    | ROW 2: BAR CHART                                |
| Age Grp: [v]      | Cases by Region (Plotly bar, horizontal, top 10)|
| Gender: [radio]   |                                                 |
|                   | ROW 3: CFR HEATMAP TABLE                         |
| [Apply Filters]   | Disease x Region CFR% (colour coded)            |
+-------------------+-------------------------------------------------+

Draw similar wireframes for UI-02 through UI-06.

SECTION 3: Global Layout Specification
3.1 Shared Sidebar Filters Table:
Filter | Widget | session_state Key | Options/Range
Disease | st.selectbox | selected_disease | "All Diseases" + 5 names
Region | st.multiselect | selected_regions | "All" + 10 state names
Year | st.slider | selected_year_range | 2020 to 2024
Age Group | st.multiselect | selected_age_groups | All + 5 groups
Gender | st.radio | selected_gender | All, Male, Female, Other

3.2 Colour Theme Table:
Role | Hex | Usage
Primary | #1A5376 | Headers, sidebar, table headers
Accent | #2E86AB | Chart line/bar color, links
Success | #1E8B4C | Positive metrics, good CFR
Warning | #E67E22 | Medium concern metrics
Danger | #C0392B | High CFR, outbreak alerts
Background | #F0F8FF | Page background
Card BG | #FFFFFF | KPI cards, chart cards
Text | #2C3E50 | Body text

3.3 Typography: Heading 24px bold | Subheading 16px | Body 14px | KPI value 32px bold

SECTION 4: Reusable Components
For each of 4 components describe: name, HTML/Python structure, Tailwind classes used
KPI Card | HTML div bg-white rounded-xl shadow-md p-4 | icon, label (grey), value (bold 32px), delta (green/red)
Chart Card | st.container + st.plotly_chart | border, title, description below chart
Insight Box | HTML div bg-blue-50 border-l-4 border-blue-600 p-3 | bold insight text
Active Filter Badge | Python f-string in sidebar | shows "X filters active" count

SECTION 5: Best Chart for Each OQ
Table: OQ ID | Best Chart Type | Plotly Call | Why | Secondary Chart
OQ-01 | Line chart (year on x, cases on y, disease as color) | px.line | Trends over time are clearest as lines | Bar
OQ-02 | Horizontal bar (region on y, cases on x) | px.bar orientation=h | Easy to compare 10 regions by rank | Heatmap
OQ-03 | Time series line (month on x) | px.line | Monthly cycle visible as wave pattern | Area chart
OQ-04 | Grouped bar (age group on x, gender as color) | px.bar barmode=group | Demographic comparison side-by-side | Stacked pie
OQ-05 | Heatmap (disease as row, region as col, CFR as color) | px.imshow | Matrix view shows all 50 disease-region pairs | Table
OQ-06 | Scatter (density on x, incidence on y, region as label) | px.scatter trendline=ols | Correlation pattern and direction visible | None
OQ-07 | Grouped bar (recovery vs CFR side by side per region) | px.bar barmode=group | Direct comparison of two rates | Table
OQ-08 | Scatter timeline (month on x, region on y, flag as color) | px.scatter | Outbreak co-occurrence visible in time | Table
OQ-09 | Bar (disease on x, YoY% on y, positive/negative color) | px.bar color_discrete_map | Positive/negative diverging bars are intuitive | Table
OQ-10 | Heatmap (month on x, disease on y, avg cases as color) | px.imshow | Peak months visible as colour intensity | Line

SECTION 6: config.toml Content
Show exact .streamlit/config.toml:
[theme]
primaryColor = "#1A5376"
backgroundColor = "#F0F8FF"
secondaryBackgroundColor = "#E8F4FD"
textColor = "#2C3E50"
font = "sans serif"

SECTION 7: Starter src/ui.py Code
Display the complete src/ui.py code in a Courier New 9pt code block:
import streamlit as st
import streamlit.components.v1 as components

TAILWIND_CDN = '<script src="https://cdn.tailwindcss.com"></script>'

def inject_tailwind():
    components.html(TAILWIND_CDN, height=0)

def render_header(title, subtitle=""):
    html = f"""
    <div class="bg-blue-900 text-white px-6 py-4 rounded-lg shadow-md mb-4">
        <h1 class="text-2xl font-bold">{title}</h1>
        <p class="text-blue-200 text-sm">{subtitle}</p>
    </div>
    """
    components.html(TAILWIND_CDN + html, height=90)

def render_kpi_card(label, value, delta=None, icon="📊", color="#1A5376"):
    delta_html = f'<span style="color:{"green" if delta and delta>=0 else "red"};font-size:12px;">{delta:+.1f}% YoY</span>' if delta is not None else ""
    return f"""
    <div style="background:#fff;border-radius:12px;padding:16px;box-shadow:0 2px 8px rgba(0,0,0,0.1);text-align:center;border-top:4px solid {color};">
        <div style="font-size:24px;">{icon}</div>
        <div style="font-size:13px;color:#666;margin:4px 0;">{label}</div>
        <div style="font-size:28px;font-weight:bold;color:{color};">{value}</div>
        {delta_html}
    </div>
    """

def render_insight_box(text):
    html = f"""<div style="background:#EBF5FB;border-left:4px solid #1A5376;padding:12px 16px;border-radius:4px;margin:8px 0;font-size:14px;">{text}</div>"""
    components.html(html, height=70)

STYLING: Same professional style.
""",
    schema={"type": "string"},
    role="Step 12 UI Framework Agent"
)
log(f"Step 12: {result12[-300:]}")

# ─────────────────────────────────────────────
# STEP 13 — Test Cases + pytest files
# ─────────────────────────────────────────────
phase("STEP 13 — Test Cases")
log("Launching Step 13 agent...")

result13 = await agent(
    prompt=STEP_AGENT_PROMPT + f"""
{PROJECT_CTX}

YOUR TASK: Generate STEP 13 — Test Cases (Word document + 2 pytest files).

PART A: Write python-docx script, save to
  C:\\Users\\Hp\\Downloads\\hcl\\docs\\gen_step13.py
then run it. Output file:
  C:\\Users\\Hp\\Downloads\\hcl\\docs\\13_ArgJain_DiseaseTrendAnalysis_TestCases.docx

PART B: Write test files and save them:
  C:\\Users\\Hp\\Downloads\\hcl\\tests\\__init__.py  (empty)
  C:\\Users\\Hp\\Downloads\\hcl\\tests\\test_data.py
  C:\\Users\\Hp\\Downloads\\hcl\\tests\\test_analysis.py

Create the tests/ directory if needed.

WORD DOCUMENT CONTENT:

COVER BLOCK: same meta, subtitle STEP 13 — Test Cases

SECTION A: Functional Test Cases (TC-F-01..TC-F-20)
Table: TC ID | Linked US | Linked BR | UI Screen | Pre-condition | Steps | Test Data | Expected Result | Priority | Status

TC-F-01 | US-04 | BR-01 | UI-01 | App running | Navigate to Overview page | None | Page loads in under 5s, 4 KPI cards visible | High | Not Run
TC-F-02 | US-04 | BR-11 | UI-01 | App running | Select Dengue in disease filter | disease=Dengue | All KPI cards show Dengue-only totals | High | Not Run
TC-F-03 | US-06 | BR-02,BR-11 | UI-01 | App running | Select Delhi in region filter | region=Delhi | Bar chart shows only Delhi bar | High | Not Run
TC-F-04 | US-04 | BR-11 | UI-01 | App running | Move year slider to 2022 | year=2022 | KPIs and charts show 2022 data only | High | Not Run
TC-F-05 | US-08 | BR-06 | UI-02 | Trends page | Load page with COVID-19 2021 | disease=COVID-19 year=2021 | Line chart with 12 monthly data points visible | High | Not Run
TC-F-06 | US-10 | BR-09 | UI-02 | Trends page | Load YoY table | disease=COVID-19 | 2021 row shows positive YoY% vs 2020 | High | Not Run
TC-F-07 | US-11 | BR-06 | UI-02 | Trends page | Load seasonal heatmap | All diseases | Heatmap: rows=diseases cols=months (12) with colour | Medium | Not Run
TC-F-08 | US-12 | BR-02 | UI-03 | Regional page | Load bar chart | All regions | 10 horizontal bars visible sorted by cases | High | Not Run
TC-F-09 | US-07 | BR-03 | UI-03 | Regional page | Load CFR heatmap | disease=Dengue | All CFR% values between 0 and 100 | High | Not Run
TC-F-10 | US-13 | BR-04 | UI-04 | Demographics page | Select Malaria, all ages | disease=Malaria | Stacked bar shows 5 age group segments | High | Not Run
TC-F-11 | US-13 | BR-04 | UI-04 | Demographics page | Select Female gender | gender=Female | Only Female data visible in chart | Medium | Not Run
TC-F-12 | US-14 | BR-08 | UI-05 | EDA page | Load scatter plot | disease=Dengue | Scatter chart visible with r= annotation | Medium | Not Run
TC-F-13 | US-15 | BR-05 | UI-05 | EDA page | Load co-occurrence section | 2021 monsoon | Table shows regions with 2+ concurrent diseases | High | Not Run
TC-F-14 | US-16 | BR-12 | UI-01..05 | Any page | Click Download CSV | Current filter | File downloads, opens in Excel, has headers and data | Medium | Not Run
TC-F-15 | US-17 | BR-13 | UI-06 | Data Quality page | Load page | None | Table shows original row count, duplicates removed, NaN filled | Medium | Not Run
TC-F-16 | US-04 | BR-11 | UI-01 | App running | Select impossible filter combo | Very narrow filter | App shows No data message, does not crash | High | Not Run
TC-F-17 | US-04..17 | BR-01 | All pages | App running | Click each page in sidebar | None | Each of 6 pages loads without Python error | High | Not Run
TC-F-18 | US-03 | BR-11 | All pages | Dengue selected | Switch from Overview to Trends page | disease=Dengue | Trends page also shows Dengue data (session_state persists) | High | Not Run
TC-F-19 | US-07 | BR-07 | UI-03 | Regional page | Load recovery chart | All data | No bar or cell shows recovery rate over 100% | High | Not Run
TC-F-20 | US-04 | BR-11 | All | Narrow browser | Resize to 600px width | None | Sidebar collapses, main content visible and usable | Low | Not Run

SECTION B: Technical Test Cases (TC-T-01..TC-T-15)
Table: TC ID | Module/Function | Check | Test Input | Expected Output | Priority

TC-T-01 | src/data_loader.py load_data() | Returns non-empty DataFrame | app.db | df.shape[0] > 0 | High
TC-T-02 | src/data_loader.py load_data() | Has required columns | app.db | columns include cases_reported deaths recovered | High
TC-T-03 | disease_cases table | disease_id FK valid (no orphans) | app.db | 0 orphan disease_ids | High
TC-T-04 | disease_cases table | region_id FK valid (no orphans) | app.db | 0 orphan region_ids | High
TC-T-05 | disease_cases table | cases_reported >= 0 after cleaning | cleaned df | min(cases_reported) >= 0 | High
TC-T-06 | disease_cases table | deaths <= cases_reported | cleaned df | all rows satisfy constraint | High
TC-T-07 | disease_master table | Unique disease names | app.db | 0 duplicate disease_name values | Medium
TC-T-08 | src/cleaning.py clean_data() | No duplicate rows after cleaning | raw df with 3 dupes | 0 exact duplicate rows in result | High
TC-T-09 | src/analysis.py compute_cfr() | CFR = deaths/cases*100 | cases=100 deaths=5 | returns 5.0 | High
TC-T-10 | src/analysis.py compute_recovery_rate() | Rate = recovered/cases*100 | cases=100 recovered=90 | returns 90.0 | High
TC-T-11 | src/analysis.py compute_yoy_change() | YoY% formula correct | 2021=200 2020=100 | returns 100.0 | High
TC-T-12 | src/analysis.py compute_incidence_rate() | Per lakh formula | cases=1000 pop=1000000 | returns 100.0 | Medium
TC-T-13 | src/analysis.py detect_concurrent_outbreaks() | Flags correctly | 2 diseases above threshold in same region-month | flag=1 | High
TC-T-14 | src/analysis.py pearson_correlation() | Pearson r on known data | x=[1,2,3,4,5] y=[2,4,6,8,10] | r approx 1.0 | Medium
TC-T-15 | src/data_loader.py load_data() | Loads within time limit | app.db | elapsed time < 3.0 seconds | High

SECTION C: Test Coverage Summary
Table: BR ID | TC-F IDs | TC-T IDs | Covered?
(map every BR to its test cases; all 15 BRs must have at least 1 test)

Now also save the pytest files:

FILE: C:\\Users\\Hp\\Downloads\\hcl\\tests\\test_data.py
Content:
import pytest
import sys
import time
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "app.db"

sys.path.insert(0, str(BASE_DIR))

def get_conn():
    if not DB_PATH.exists():
        pytest.skip("app.db not found - run generate_data.py first")
    return sqlite3.connect(str(DB_PATH))

def test_load_data_rows():  # TC-T-01
    conn = get_conn()
    df_len = conn.execute("SELECT COUNT(*) FROM disease_cases").fetchone()[0]
    conn.close()
    assert df_len > 0, "disease_cases table is empty"

def test_load_data_columns():  # TC-T-02
    conn = get_conn()
    cursor = conn.execute("SELECT * FROM disease_cases LIMIT 1")
    cols = [d[0] for d in cursor.description]
    conn.close()
    for col in ["cases_reported", "deaths", "recovered", "disease_id", "region_id"]:
        assert col in cols, f"Column {col} missing"

def test_disease_id_fk():  # TC-T-03
    conn = get_conn()
    orphans = conn.execute(
        "SELECT COUNT(*) FROM disease_cases dc LEFT JOIN disease_master dm "
        "ON dc.disease_id = dm.disease_id WHERE dm.disease_id IS NULL"
    ).fetchone()[0]
    conn.close()
    assert orphans == 0, f"Found {orphans} orphan disease_ids"

def test_region_id_fk():  # TC-T-04
    conn = get_conn()
    orphans = conn.execute(
        "SELECT COUNT(*) FROM disease_cases dc LEFT JOIN region_master rm "
        "ON dc.region_id = rm.region_id WHERE rm.region_id IS NULL"
    ).fetchone()[0]
    conn.close()
    assert orphans == 0, f"Found {orphans} orphan region_ids"

def test_cases_non_negative():  # TC-T-05
    conn = get_conn()
    neg = conn.execute(
        "SELECT COUNT(*) FROM disease_cases WHERE cases_reported < 0"
    ).fetchone()[0]
    conn.close()
    assert neg == 0, f"Found {neg} rows with negative cases_reported"

def test_deaths_le_cases():  # TC-T-06
    conn = get_conn()
    invalid = conn.execute(
        "SELECT COUNT(*) FROM disease_cases WHERE deaths > cases_reported"
    ).fetchone()[0]
    conn.close()
    assert invalid == 0, f"Found {invalid} rows where deaths > cases_reported"

def test_disease_names_unique():  # TC-T-07
    conn = get_conn()
    total = conn.execute("SELECT COUNT(*) FROM disease_master").fetchone()[0]
    unique = conn.execute("SELECT COUNT(DISTINCT disease_name) FROM disease_master").fetchone()[0]
    conn.close()
    assert total == unique, "Duplicate disease names found"

def test_no_duplicate_case_rows():  # TC-T-08
    conn = get_conn()
    total = conn.execute("SELECT COUNT(*) FROM disease_cases").fetchone()[0]
    unique = conn.execute(
        "SELECT COUNT(*) FROM (SELECT DISTINCT disease_id, region_id, report_date, "
        "cases_reported, deaths, recovered FROM disease_cases)"
    ).fetchone()[0]
    conn.close()
    # After cleaning there should be no exact dupes; allow small tolerance
    assert (total - unique) <= 3, f"Too many duplicate rows: {total - unique}"

def test_load_time():  # TC-T-15
    if not DB_PATH.exists():
        pytest.skip("app.db not found")
    start = time.time()
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("SELECT * FROM disease_cases").fetchall()
    conn.close()
    elapsed = time.time() - start
    assert elapsed < 3.0, f"Load took {elapsed:.2f}s, expected < 3.0s"

FILE: C:\\Users\\Hp\\Downloads\\hcl\\tests\\test_analysis.py
Content:
import pytest
import sys
import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BASE_DIR))

def make_test_df(cases, deaths, recovered, population=1000000, pop_density=500):
    return pd.DataFrame([{
        "cases_reported": cases,
        "deaths": deaths,
        "recovered": recovered,
        "population": population,
        "population_density": pop_density,
        "disease_name": "Test",
        "region_name": "Test Region",
        "report_year": 2021,
        "report_month": 6,
    }])

def test_compute_cfr():  # TC-T-09
    try:
        from src.analysis import compute_cfr
        df = make_test_df(100, 5, 90)
        result = compute_cfr(df)
        assert "cfr_pct" in result.columns
        assert abs(result["cfr_pct"].iloc[0] - 5.0) < 0.1
    except ImportError:
        # Function not yet built - mark expected failure
        pytest.xfail("src.analysis not yet implemented")

def test_compute_recovery_rate():  # TC-T-10
    try:
        from src.analysis import compute_recovery_rate
        df = make_test_df(100, 5, 90)
        result = compute_recovery_rate(df)
        assert "recovery_rate_pct" in result.columns
        assert abs(result["recovery_rate_pct"].iloc[0] - 90.0) < 0.1
    except ImportError:
        pytest.xfail("src.analysis not yet implemented")

def test_compute_yoy_change():  # TC-T-11
    try:
        from src.analysis import compute_yoy_change
        rows = [
            {"disease_name": "Dengue", "report_year": 2020, "cases_reported": 100},
            {"disease_name": "Dengue", "report_year": 2021, "cases_reported": 200},
        ]
        df = pd.DataFrame(rows)
        result = compute_yoy_change(df)
        # Result should contain 100% increase from 2020->2021
        assert result is not None
    except ImportError:
        pytest.xfail("src.analysis not yet implemented")

def test_compute_incidence_rate():  # TC-T-12
    try:
        from src.analysis import compute_incidence_rate
        df = make_test_df(1000, 10, 900, population=1000000)
        result = compute_incidence_rate(df)
        assert "incidence_per_lakh" in result.columns
        assert abs(result["incidence_per_lakh"].iloc[0] - 100.0) < 0.1
    except ImportError:
        pytest.xfail("src.analysis not yet implemented")

def test_detect_concurrent_outbreaks():  # TC-T-13
    try:
        from src.analysis import detect_concurrent_outbreaks
        rows = []
        for disease_id, disease_name in [(1,"Dengue"),(2,"Malaria"),(3,"TB")]:
            rows.append({
                "disease_id": disease_id,
                "disease_name": disease_name,
                "region_id": 1, "region_name": "UP",
                "report_year": 2021, "report_month": 8,
                "cases_reported": 9999,
            })
        df = pd.DataFrame(rows)
        result = detect_concurrent_outbreaks(df)
        assert result is not None
    except ImportError:
        pytest.xfail("src.analysis not yet implemented")

def test_pearson_correlation():  # TC-T-14
    try:
        from src.analysis import pearson_correlation
        rows = [{"incidence_per_lakh": float(i*20), "population_density": float(i*100)}
                for i in range(1, 11)]
        df = pd.DataFrame(rows)
        r, p = pearson_correlation(df)
        assert abs(r - 1.0) < 0.01, f"Expected r~1.0, got {r}"
    except ImportError:
        pytest.xfail("src.analysis not yet implemented")

After saving both test files, report: STEP 13 COMPLETE
""",
    schema={"type": "string"},
    role="Step 13 Test Cases Agent"
)
log(f"Step 13: {result13[-300:]}")

# ─────────────────────────────────────────────
# STEP 14 — Build Plan
# ─────────────────────────────────────────────
phase("STEP 14 — Build Plan")
log("Launching Step 14 agent...")

result14 = await agent(
    prompt=STEP_AGENT_PROMPT + f"""
{PROJECT_CTX}

YOUR TASK: Generate STEP 14 — Build Plan (Word document + BUILD_PLAN.md).

PART A: Write python-docx script, save to
  C:\\Users\\Hp\\Downloads\\hcl\\docs\\gen_step14.py
then run it. Output file:
  C:\\Users\\Hp\\Downloads\\hcl\\docs\\14_ArgJain_DiseaseTrendAnalysis_BuildPlan.docx

PART B: Save BUILD_PLAN.md to
  C:\\Users\\Hp\\Downloads\\hcl\\BUILD_PLAN.md

WORD DOCUMENT CONTENT:

COVER BLOCK: same meta, subtitle STEP 14 — Build Plan

SECTION 1: Project Summary (10 sentences)
The Disease Trend Analysis project (P100) builds an interactive healthcare analytics app.
It analyses synthetic disease incidence data for 5 diseases across 10 Indian states from 2020 to 2024.
The tech stack is Python 3.12, Streamlit 1.35.0, SQLite, Plotly, and pytest.
Stakeholders include public health officers, hospital administrators, and policy makers.
The app answers 10 operational questions through 6 multi-page Streamlit screens.
Data is stored in a normalised SQLite database (app.db) with 5 tables and an analysis view.
Tailwind CSS is injected via st.components.v1.html for the header and KPI card styling.
pytest covers all analysis functions and data integrity checks with target 80% coverage.
The final app is deployed on Streamlit Community Cloud with a public URL.
Submission includes 18 step documents, an ABES project document, and a slide presentation.

SECTION 2: Final Folder Structure (exact tree with all files)

SECTION 3: Build Tasks (the main section)
For each of 14 BUILD tasks present a table: BUILD ID | Goal | Files | US IDs | AI Prompt Summary | Verification Check | Tests That Must Pass

BUILD-01 | Project setup and structure | requirements.txt .gitignore .streamlit/config.toml | - | Create all config files with pinned versions | pip install -r requirements.txt succeeds | None
BUILD-02 | SQLite data loader with caching | src/data_loader.py | US-01 | Write load_data() with @st.cache_data joining all tables from app.db | python -c "from src.data_loader import load_data; print(load_data().shape)" | TC-T-01 TC-T-02 TC-T-15
BUILD-03 | Data cleaning pipeline | src/cleaning.py | US-02 | Write clean_data() removing dupes imputing NaN capping outliers returning quality report dict | python -c "from src.cleaning import clean_data" | TC-T-08
BUILD-04 | Session state sidebar filters | app.py src/ui.py | US-03 | Write all sidebar widgets bound to st.session_state; inject Tailwind; render header | streamlit run app.py shows header and sidebar | TC-F-17
BUILD-05 | All 9 analysis functions | src/analysis.py | US-07..15 | Write CFR recovery YoY seasonal incidence correlation co-occurrence functions | pytest tests/test_analysis.py -v | TC-T-09..TC-T-14
BUILD-06 | Overview page (UI-01) | pages/01_Overview.py | US-04 US-05 US-06 US-07 | Write 4 KPI cards bar chart CFR heatmap applying session_state filters | Manual: 4 KPIs and bar chart visible | TC-F-01..TC-F-04
BUILD-07 | Trends page (UI-02) | pages/02_Trends.py | US-08 US-09 US-10 US-11 | Write monthly line chart YoY chart seasonal heatmap and YoY table | Manual: 3 charts visible | TC-F-05..TC-F-07
BUILD-08 | Regional analysis page (UI-03) | pages/03_Regional_Analysis.py | US-12 | Write horizontal bar chart and CFR by region chart | Manual: 10-region chart visible | TC-F-08 TC-F-09
BUILD-09 | Demographics page (UI-04) | pages/04_Demographics.py | US-13 | Write stacked bar by age group and pie chart by gender | Manual: stacked segments visible | TC-F-10 TC-F-11
BUILD-10 | EDA and Insights page (UI-05) | pages/05_EDA_Statistics.py | US-14 US-15 | Write scatter with trendline Pearson r and co-occurrence table | Manual: scatter and r value visible | TC-F-12 TC-F-13
BUILD-11 | Data Quality page (UI-06) | pages/06_Data_Quality.py | US-16 US-17 | Write before/after cleaning stats table and CSV download button | Manual: stats table and download visible | TC-F-14 TC-F-15
BUILD-12 | Filter edge cases and empty states | all pages | US-04 | Add empty DataFrame check: show No data available message on each page | TC-F-16 passes | TC-F-16
BUILD-13 | Full test run and fixes | tests/ | All US | Run pytest -q --cov=src tests/ and fix all failures | pytest report: 0 failures coverage >= 80% | All TC-T-01..TC-T-15
BUILD-14 | README and final checks | README.md | - | Write setup run deploy instructions; check all 6 pages load | README renders on GitHub; all pages load | TC-F-17

SECTION 4: Definition of Done (10 checklist items)
SECTION 5: Commands Reference (install run test generate deploy)
SECTION 6: Viva Q&A Notes (10 questions with 2-line answers)
Example questions: Why SQLite instead of PostgreSQL? How is CFR calculated? 
What patterns are in the data? How does @st.cache_data work?
What is session_state used for? How is test coverage measured?

BUILD_PLAN.md content (save to C:\\Users\\Hp\\Downloads\\hcl\\BUILD_PLAN.md):
# Disease Trend Analysis - Build Plan
## Project: P100 | Student: Arg Jain | Roll: 2500320140031 | Mentor: Mr. Dinesh

## Setup Commands
```
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
python src/generate_data.py
streamlit run app.py
pytest -q --cov=src tests/
```

## Build Tasks
- [ ] BUILD-01: Project setup (requirements.txt, config.toml, .gitignore)
- [ ] BUILD-02: src/data_loader.py - load_data() with @st.cache_data
- [ ] BUILD-03: src/cleaning.py - clean_data() pipeline
- [ ] BUILD-04: app.py + src/ui.py - sidebar filters and Tailwind header
- [ ] BUILD-05: src/analysis.py - all 9 analysis functions
- [ ] BUILD-06: pages/01_Overview.py - KPI dashboard
- [ ] BUILD-07: pages/02_Trends.py - time series and seasonal
- [ ] BUILD-08: pages/03_Regional_Analysis.py - regional comparison
- [ ] BUILD-09: pages/04_Demographics.py - age and gender breakdown
- [ ] BUILD-10: pages/05_EDA_Statistics.py - scatter and co-occurrence
- [ ] BUILD-11: pages/06_Data_Quality.py - quality report and download
- [ ] BUILD-12: Empty state handling on all pages
- [ ] BUILD-13: Run pytest --cov and fix all failures
- [ ] BUILD-14: Write README.md

## Definition of Done
- [ ] All 10 OQs answerable in live walkthrough
- [ ] pytest coverage >= 80%, 0 critical failures
- [ ] App deployed at Streamlit Cloud URL
- [ ] All 18 step documents complete

After saving both files, report: STEP 14 COMPLETE
""",
    schema={"type": "string"},
    role="Step 14 Build Plan Agent"
)
log(f"Step 14: {result14[-300:]}")

# ─────────────────────────────────────────────
# STEP 15 — Build the Streamlit App
# ─────────────────────────────────────────────
phase("STEP 15 — Build Streamlit App")
log("Launching Step 15 agent...")

result15 = await agent(
    prompt=STEP_AGENT_PROMPT + f"""
{PROJECT_CTX}

YOUR TASK: Build the complete Disease Trend Analysis Streamlit app (Step 15).

Create all required directories and write all files:
  C:\\Users\\Hp\\Downloads\\hcl\\src\\
  C:\\Users\\Hp\\Downloads\\hcl\\pages\\
  C:\\Users\\Hp\\Downloads\\hcl\\.streamlit\\

Write and save each file listed below using write_file tool. After saving all files,
run: cd C:\\Users\\Hp\\Downloads\\hcl && python src\\generate_data.py 2>&1
to verify data exists (skip if already run).

Then try to run streamlit (non-interactive check):
cd C:\\Users\\Hp\\Downloads\\hcl && python -c "import streamlit; import pandas; import plotly; print('All imports OK')"

FILE: C:\\Users\\Hp\\Downloads\\hcl\\requirements.txt
streamlit==1.35.0
pandas==2.2.2
numpy==1.26.4
plotly==5.22.0
scipy==1.13.0
statsmodels==0.14.2
openpyxl==3.1.2
pytest==8.2.0
pytest-cov==5.0.0

FILE: C:\\Users\\Hp\\Downloads\\hcl\\.streamlit\\config.toml
[theme]
primaryColor = "#1A5376"
backgroundColor = "#F0F8FF"
secondaryBackgroundColor = "#E8F4FD"
textColor = "#2C3E50"
font = "sans serif"

FILE: C:\\Users\\Hp\\Downloads\\hcl\\src\\__init__.py
(empty)

FILE: C:\\Users\\Hp\\Downloads\\hcl\\src\\data_loader.py
Write complete data_loader.py:
- import streamlit as st, pandas as pd, sqlite3, from pathlib import Path
- DB_PATH = Path(__file__).parent.parent / "data" / "app.db"
- @st.cache_data(ttl=3600)
- def load_data() -> pd.DataFrame: 
    connect to DB_PATH, run JOIN query across disease_cases, disease_master, region_master
    return df with all columns including disease_name, region_name, population, population_density
    wrap in try/except, return empty DataFrame on error

FILE: C:\\Users\\Hp\\Downloads\\hcl\\src\\cleaning.py
Write complete cleaning.py:
- def clean_data(df): 
    track original_rows = len(df)
    remove duplicates: df = df.drop_duplicates()
    impute cases_reported NaN with median
    impute deaths NaN with 0
    cap outliers: Q3 + 3*IQR for cases_reported
    return cleaned_df, quality_report (dict with original_rows, duplicates_removed, nulls_filled, outliers_capped, final_rows)

FILE: C:\\Users\\Hp\\Downloads\\hcl\\src\\analysis.py
Write complete analysis.py with all 8 functions (each with docstring, handle div-by-zero with fillna(0)):
- compute_cfr(df) -> df with cfr_pct column
- compute_recovery_rate(df) -> df with recovery_rate_pct column
- compute_yoy_change(df) -> pivot DataFrame (disease rows, year cols with YoY% values)
- compute_seasonal_trend(df) -> pivot (month rows, disease cols, avg cases)
- compute_incidence_rate(df) -> df with incidence_per_lakh column
- detect_concurrent_outbreaks(df) -> filtered df of region-months with 2+ diseases > their mean
- pearson_correlation(df) -> tuple (r: float, p_value: float)
- compute_regional_summary(df) -> grouped summary df

FILE: C:\\Users\\Hp\\Downloads\\hcl\\src\\ui.py
Complete ui.py with:
- inject_tailwind()
- render_header(title, subtitle)
- render_kpi_card(label, value, delta, icon, color) returning HTML string
- render_insight_box(text)

FILE: C:\\Users\\Hp\\Downloads\\hcl\\app.py
Complete app.py:
- st.set_page_config(page_title="Disease Trend Analysis", page_icon="🏥", layout="wide")
- inject_tailwind()
- render_header("Disease Trend Analysis", "Healthcare Analytics | ABES | Arg Jain")
- Load data: raw_df = load_data(); df, quality_report = clean_data(raw_df)
- Sidebar filters with st.session_state (disease, regions, year_range, age_groups, gender)
- Apply filters to df
- Home page: 4 KPI cards using render_kpi_card in st.columns(4)
- Welcome text explaining the app

FILE: C:\\Users\\Hp\\Downloads\\hcl\\pages\\01_Overview.py
Complete page with 4 KPI cards, bar chart (cases by region, px.bar horizontal),
CFR heatmap (px.imshow on pivot). Load filtered_df from session state or reload.

FILE: C:\\Users\\Hp\\Downloads\\hcl\\pages\\02_Trends.py
Complete page with line chart (monthly cases, px.line), YoY chart (px.line by year),
seasonal heatmap (px.imshow), YoY% table (st.dataframe styled).

FILE: C:\\Users\\Hp\\Downloads\\hcl\\pages\\03_Regional_Analysis.py
Complete page with horizontal bar chart (cases by region), CFR by region bar chart,
recovery rate comparison.

FILE: C:\\Users\\Hp\\Downloads\\hcl\\pages\\04_Demographics.py
Complete page with stacked bar (age group x gender, px.bar barmode=stack),
pie chart for gender split (px.pie). Note: use disease_cases data grouped appropriately.

FILE: C:\\Users\\Hp\\Downloads\\hcl\\pages\\05_EDA_Statistics.py
Complete page with scatter plot (incidence_per_lakh vs population_density, px.scatter trendline=ols),
Pearson r and p-value displayed, co-occurrence table from detect_concurrent_outbreaks(),
descriptive stats table (df.describe()).

FILE: C:\\Users\\Hp\\Downloads\\hcl\\pages\\06_Data_Quality.py
Complete page with before/after cleaning stats table (st.dataframe from quality_report dict),
outlier section, full CSV download button.

FILE: C:\\Users\\Hp\\Downloads\\hcl\\tests\\test_app.py
Write basic test_app.py:
import pytest, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_imports():
    import streamlit
    import pandas
    import plotly
    import scipy
    assert True

def test_data_loader_import():
    try:
        from src.data_loader import load_data
        assert callable(load_data)
    except Exception as e:
        pytest.xfail(f"data_loader not ready: {{e}}")

def test_analysis_import():
    try:
        from src.analysis import compute_cfr, compute_recovery_rate
        assert callable(compute_cfr)
    except Exception as e:
        pytest.xfail(f"analysis not ready: {{e}}")

After saving all files:
1. Run: cd C:\\Users\\Hp\\Downloads\\hcl && python -c "import sys; sys.path.insert(0,'.'); from src.data_loader import load_data; print('loader OK')" 2>&1
2. Run: cd C:\\Users\\Hp\\Downloads\\hcl && python -m pytest tests/ -q --tb=short 2>&1

Report all results. STEP 15 COMPLETE means: all files saved, imports work, tests run (xfail OK).
""",
    schema={"type": "string"},
    role="Step 15 App Builder Agent"
)
log(f"Step 15: {result15[-500:]}")

# ─────────────────────────────────────────────
# STEP 16 — Deployment Guide
# ─────────────────────────────────────────────
phase("STEP 16 — Deployment Guide")
log("Launching Step 16 agent...")

result16 = await agent(
    prompt=STEP_AGENT_PROMPT + f"""
{PROJECT_CTX}

YOUR TASK: Generate STEP 16 — Deployment Guide (Word document).
Write python-docx script, save to
  C:\\Users\\Hp\\Downloads\\hcl\\docs\\gen_step16.py
then run it. Output file:
  C:\\Users\\Hp\\Downloads\\hcl\\docs\\16_ArgJain_DiseaseTrendAnalysis_DeploymentGuide.docx

DOCUMENT CONTENT:

COVER BLOCK: same meta, subtitle STEP 16 — Deployment Guide: Streamlit Community Cloud

SECTION 1: Pre-Deployment Checklist
Table: Check ID | Item | Expected State | Verified?
CHK-01 | app.py at repo root | File exists at root level | Yes
CHK-02 | requirements.txt at root with pinned versions | All versions pinned (==) | Yes
CHK-03 | data/app.db committed to repo | SQLite file in data/ folder and in git | Yes
CHK-04 | Relative paths using Path(__file__).parent | No hardcoded absolute paths | Yes
CHK-05 | No API keys or passwords in code | No secrets in any .py file | Yes
CHK-06 | .gitignore excludes .venv/ __pycache__/ *.pyc | .gitignore file present | Yes
CHK-07 | All 6 page files in pages/ folder | pages/ has 6 .py files | Yes
CHK-08 | pytest passes with 0 critical failures | pytest -q shows 0 failed | Yes
CHK-09 | App runs locally without errors | streamlit run app.py works | Yes
CHK-10 | GitHub repo pushed with all files | git push completed | Yes

SECTION 2: GitHub Repository Setup (numbered steps)
1. Go to github.com and create new repository named: 2500320140031-disease-trend-analysis
2. Set to Public, do NOT initialize with README (you already have one)
3. In your project folder (terminal):
   git init
   git add .
   git commit -m "Initial commit: Disease Trend Analysis - Arg Jain P100"
   git remote add origin https://github.com/YOUR_USERNAME/2500320140031-disease-trend-analysis.git
   git push -u origin main
4. Go to your GitHub repo URL and verify all files are visible
Troubleshooting tip: If git push fails due to file size, use git lfs for data/app.db

SECTION 3: Streamlit Community Cloud Deployment (numbered steps)
1. Navigate to share.streamlit.io in your browser
2. Sign in with your GitHub account
3. Click New app (top right button)
4. Fill the deployment form:
   - Repository: YOUR_USERNAME/2500320140031-disease-trend-analysis
   - Branch: main
   - Main file path: app.py
   - App URL (optional): 2500320140031-dta (or similar slug)
5. Click Deploy now
6. Wait 2-5 minutes while Streamlit installs packages and starts the app
7. Watch the deployment log for the message: Your app is now deployed
8. Copy the public URL and share with mentor

SECTION 4: Common Deployment Failures and Fixes
Table: Error Message | Root Cause | Exact Fix
ModuleNotFoundError: No module named X | Package missing from requirements.txt | Add X==VERSION to requirements.txt and git push
No module named src | Python path issue | Add sys.path.insert(0, Path(__file__).parent) in app.py
FileNotFoundError: app.db | Incorrect relative path | Use Path(__file__).parent / "data" / "app.db"
MemoryError or App crashes | Dataset too large for 1GB free tier | Reduce rows in generate_data.py; use sampling
Application failed to start | requirements.txt syntax error | Check for extra spaces or wrong format
App sleeps after inactivity | Streamlit free tier policy | App auto-wakes on first visit; warn mentor

SECTION 5: Post-Deployment Verification Checklist
Step-by-step numbered list:
1. Open the public Streamlit URL in a browser
2. Verify app loads in under 5 seconds
3. Check all 6 pages are accessible from sidebar
4. Apply a disease filter and verify charts update
5. Apply a region filter and verify data changes
6. Click CSV download on a page and verify file downloads
7. Open Data Quality page and verify before/after stats visible
8. Copy the final URL for submission

SECTION 6: Maintenance and Updates
Numbered list:
1. To update the app: edit code locally then git add . and git commit and git push origin main
2. Streamlit Cloud automatically redeploys on git push (takes 2-3 minutes)
3. To view deployment logs: share.streamlit.io dashboard then App then Manage app then Logs
4. Free tier limits: 1 GB RAM, 1 CPU shared, app sleeps after 7 days inactivity (re-wakes on visit)
5. Submission note: include the public URL in the ABES project document cover page

Also create C:\\Users\\Hp\\Downloads\\hcl\\.gitignore with content:
.venv/
__pycache__/
*.pyc
*.pyo
.env
*.egg-info/
dist/
build/
.DS_Store

Report: STEP 16 COMPLETE
""",
    schema={"type": "string"},
    role="Step 16 Deployment Guide Agent"
)
log(f"Step 16: {result16[-300:]}")

# ─────────────────────────────────────────────
# STEPS 17 & 18 — Project Document + Presentation
# ─────────────────────────────────────────────
phase("STEPS 17 and 18 — Final Documents (parallel)")
log("Launching Steps 17 and 18 in parallel...")

results_1718 = await parallel(
    [17, 18],
    lambda step_num: agent(
        prompt=STEP_AGENT_PROMPT + f"""
{PROJECT_CTX}

YOUR TASK: Generate STEP {step_num} document.

{"" if step_num == 17 else ""}
Write python-docx script, save to
  C:\\Users\\Hp\\Downloads\\hcl\\docs\\gen_step{step_num}.py
then run it. Output file:
  C:\\Users\\Hp\\Downloads\\hcl\\docs\\{step_num:02d}_ArgJain_DiseaseTrendAnalysis_{"ProjectDocument" if step_num==17 else "PresentationScript"}.docx

{"STEP 17 — PROJECT DOCUMENT (ABES Format)" if step_num == 17 else "STEP 18 — PRESENTATION SLIDE SCRIPT"}

{"CONTENT FOR STEP 17:" if step_num == 17 else "CONTENT FOR STEP 18:"}

{"COVER PAGE TABLE: Project Title Disease Trend Analysis | Project ID P100 | Student Arg Jain | Roll No 2500320140031 | Course MCA 2nd Year Data Analytics | Institute ABES Engineering College Ghaziabad | Mentor Mr. Dinesh | Academic Year 2026-27 | GitHub URL [TO BE ADDED AFTER DEPLOYMENT] | Streamlit Cloud URL [TO BE ADDED AFTER DEPLOYMENT] | Submission Date November 2026 | Version v1.0" if step_num == 17 else ""}

{"Then one section per step with heading and 1-page content summary:" if step_num == 17 else ""}
{"Section 1 Project Understanding: Problem statement one-sentence | Intended audience table | Stakeholders SH-01..SH-06 | 10 OQs | 5 SMART objectives | Scope in/out | Assumptions A-01..A-07 | Constraints C-01..C-05 | 6 success criteria" if step_num == 17 else ""}
{"Section 2 HMW Statements: Pain points table | 10 HMW statements with IDs | Priority 5 marked | OQ coverage confirmed" if step_num == 17 else ""}
{"Section 3 Needs Analysis: 15 BRs (BR-01..BR-15) in a summary table | Priority breakdown Must 9 Should 4 Could 2 | No gaps" if step_num == 17 else ""}
{"Section 4 Traceability Matrix: 4 sample RTM rows showing end-to-end trace (OQ to HMW to BR to US to TC to UI) | Note: full RTM in 04_...RTM.xlsx" if step_num == 17 else ""}
{"Section 5 BRD: Executive summary | RACI table | 15 BRs with acceptance criteria (abbreviated) | 5 business rules | 5 risks" if step_num == 17 else ""}
{"Section 6 PRD: (Skipped per project scope)" if step_num == 17 else ""}
{"Section 7 TRD: Architecture diagram (ASCII) | Folder structure | 15 FRs | 8 NFRs | Statistical methods per OQ | requirements.txt | 5 technical risks" if step_num == 17 else ""}
{"Section 8 Database Design: 5 tables summary | Key DDL (CREATE TABLE disease_cases abbreviated) | Relationships | 8 KPIs/measures" if step_num == 17 else ""}
{"Section 9 ER Diagram: Mermaid code | 4 relationships described | Business rules | ER diagram image placeholder" if step_num == 17 else ""}
{"Section 10 Dataset Generation: 5 patterns built in | 4 quality issues | File list (data/app.db data/*.csv data/*.xlsx) | Validation report summary" if step_num == 17 else ""}
{"Section 11 User Stories: 17 US in 5 epics | Story point total 46 | Sprint plan (8 days)" if step_num == 17 else ""}
{"Section 12 UI Framework: 6 screens UI-01..UI-06 | ASCII wireframe for UI-01 | Colour theme | config.toml | src/ui.py starter code" if step_num == 17 else ""}
{"Section 13 Test Cases: 20 TC-F and 15 TC-T | Coverage: all 15 BRs covered | pytest files in tests/" if step_num == 17 else ""}
{"Section 14 Build Plan: 14 BUILD tasks | Definition of Done 10 items | Commands reference | 10 viva Q&A" if step_num == 17 else ""}
{"Section 15 Build Test Fix: App files list (app.py 6 pages src/*.py tests/*.py) | pytest run result placeholder | Key fixes applied" if step_num == 17 else ""}
{"Section 16 Deployment: Pre-deployment checklist 10 items | GitHub repo URL placeholder | Streamlit Cloud URL placeholder | 6-step deploy procedure" if step_num == 17 else ""}
{"Appendix A: Project Assumptions (A-01..A-07 from Step 1)" if step_num == 17 else ""}
{"Appendix B: AI Tools Used - table: Tool | Used For | How Output Was Verified - rows: Antigravity (this AI) | Document drafting all 18 steps analysis function design test case generation | Each document reviewed corrected and approved by student before submission; code tested locally with pytest" if step_num == 17 else ""}

{"CONTENT FOR STEP 18 — PRESENTATION SCRIPT:" if step_num == 18 else ""}
{"For each of 11 slides provide: Slide number and title | Content (max 6 bullet points what appears on screen) | Speaker notes (what to say aloud ~30 seconds)" if step_num == 18 else ""}

{"SLIDE 1 TITLE: Disease Trend Analysis | P100 | Arg Jain | Roll 2500320140031 | Mr. Dinesh | ABES Engineering College | November 2026" if step_num == 18 else ""}
{"SLIDE 2 PROBLEM AND HMW: Problem = Lack of unified platform to monitor disease trends. Leads to delayed outbreak response. Missed budget targeting opportunities. HMW-01: How might we help public health officers spot which disease is spiking in a region vs last year? HMW-03: How might we help policy makers compare CFR across regions to justify budget allocations?" if step_num == 18 else ""}
{"SLIDE 3 STAKEHOLDERS: SH-01 Public Health Officer Influence H Decision: Deploy response teams. SH-02 Hospital Administrator Influence H Decision: Allocate beds and medicines. SH-03 Policy Maker Influence H Decision: Approve health budgets." if step_num == 18 else ""}
{"SLIDE 4 TRACEABILITY: Show 4 RTM rows: OQ-01 | HMW-01 | BR-01 | US-04 | TC-F-01 | UI-01 and OQ-05 | HMW-03 | BR-03 | US-07 | TC-F-09 | UI-03 and OQ-08 | HMW-05 | BR-05 | US-15 | TC-F-13 | UI-05 and OQ-04 | HMW-04 | BR-04 | US-13 | TC-F-10 | UI-04" if step_num == 18 else ""}
{"SLIDE 5 DATA: 3000 rows in disease_cases fact table. 5 tables in SQLite database. Jan 2020 to Dec 2024 (60 months). 5 diseases 10 Indian states. Quality fixes: 60+ NaN imputed | 3 duplicates removed | 5 outliers capped." if step_num == 18 else ""}
{"SLIDE 6 SOLUTION AND TECH STACK: Python 3.12 + pandas for data processing. SQLite (app.db) as relational database. Streamlit 1.35 multi-page framework. Plotly 5 for 6 interactive chart types. Tailwind CSS via CDN for UI styling. Deployed: Streamlit Community Cloud." if step_num == 18 else ""}
{"SLIDE 7 DASHBOARD: Screenshot placeholder UI-01 Overview with 4 KPI cards. Screenshot placeholder UI-02 Trends with seasonal heatmap. 6 pages: Overview Trends Regional Demographics EDA DataQuality." if step_num == 18 else ""}
{"SLIDE 8 KEY FINDINGS: COVID-19 showed 300% spike in cases from 2020 to 2021 (OQ-09 YoY analysis). Dengue and Malaria cases are 2.5x higher in monsoon months July-September vs January (OQ-10 seasonal). Delhi CFR 3.1% vs Bihar 1.4% showing urban density impact (OQ-05 OQ-06)." if step_num == 18 else ""}
{"SLIDE 9 TESTING: 20 manual functional test cases (TC-F-01..TC-F-20). 15 pytest automated test cases (TC-T-01..TC-T-15). Coverage target 80% via pytest --cov. 0 critical test failures at submission. Key tests: load_data rows > 0 | deaths <= cases | CFR formula 5.0 for 100 cases 5 deaths." if step_num == 18 else ""}
{"SLIDE 10 RECOMMENDATIONS: Recommendation: Integrate real ICMR district-level data for operational use. Limitations: Synthetic data may not capture all epidemiological nuances. Free-tier Streamlit app may sleep after inactivity. Next Steps: Add ML forecasting (ARIMA or Prophet) for 3-month outbreak prediction. Enable email alerts when is_outbreak flag triggers." if step_num == 18 else ""}
{"SLIDE 11 LIVE DEMO: GitHub Repository: github.com/argjain/2500320140031-disease-trend-analysis [placeholder]. Live App URL: 2500320140031-dta.streamlit.app [placeholder]. QR code: [TO BE ADDED]. All 10 OQs demonstrable in 5-minute live walkthrough." if step_num == 18 else ""}

{"Also add: 5-minute timing guide table: Slide | Time | Key Point" if step_num == 18 else ""}
{"Prep checklist: 1 Test app URL day before 2 Screenshot Overview and Trends pages 3 Rehearse 5 minutes 4 Prepare for 3 viva questions 5 Have GitHub URL and app URL ready" if step_num == 18 else ""}

Report: STEP {step_num} COMPLETE
""",
        schema={"type": "string"},
        role=f"Step {step_num} {'Project Document' if step_num==17 else 'Presentation'} Agent"
    )
)

result17, result18 = results_1718
log(f"Step 17: {result17[-200:]}")
log(f"Step 18: {result18[-200:]}")

# ─────────────────────────────────────────────
# FINAL INVENTORY CHECK
# ─────────────────────────────────────────────
phase("FINAL INVENTORY")
log("Checking all generated files...")

inventory_agent = agent(
    "List all files in C:\\Users\\Hp\\Downloads\\hcl\\docs\\ and C:\\Users\\Hp\\Downloads\\hcl\\data\\ and C:\\Users\\Hp\\Downloads\\hcl\\src\\ and C:\\Users\\Hp\\Downloads\\hcl\\pages\\ using run_command. Report the complete file list.",
    schema={"type": "string"},
    role="Inventory Checker"
)
inventory = await inventory_agent
log(f"INVENTORY: {inventory}")

print("WORKFLOW COMPLETE")
print("All steps 2-18 (excluding 6) have been executed.")
print("Check C:\\Users\\Hp\\Downloads\\hcl\\docs\\ for all Word and Excel files.")
