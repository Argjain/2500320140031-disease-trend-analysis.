
# ============================================================
# Disease Trend Analysis – Full Project Workflow
# Steps 2-18 (Step 6 skipped), sequential pipeline
# ============================================================

PROJECT_CTX = """
PROJECT CONTEXT (carry forward to ALL steps):
- Project ID: P-01 | Title: Disease Trend Analysis
- Domain: Healthcare Data Analytics
- Student: Arg Jain | Roll: 2500320140031 | MCA 2nd Yr DA, ABES
- Mentor: Ms. Kalpana Dwivedi
- Stack: Python 3.12, Streamlit, SQLite, Plotly, pytest, Tailwind CDN
- Diseases: Dengue, Malaria, Tuberculosis (TB), COVID-19, Typhoid (5)
- Regions (10 Indian states): Uttar Pradesh, Maharashtra, Delhi,
  Rajasthan, Bihar, West Bengal, Tamil Nadu, Karnataka, Gujarat,
  Madhya Pradesh
- Period: Jan 2020 – Dec 2024 (60 months, monthly granularity)
- Age groups: 0-14, 15-29, 30-44, 45-59, 60+
- Gender: Male, Female, Other
- Stakeholders: SH-01 Public Health Officer (H), SH-02 Hospital Admin (H),
  SH-03 Policy Maker/Ministry (H), SH-04 Epidemiologist/Researcher (M),
  SH-05 Arg Jain Student Developer (M), SH-06 Ms. Kalpana Dwivedi Mentor (L)
- OQs (OQ-01..OQ-10):
  OQ-01: Which diseases have shown highest increase in cases over 5 years?
  OQ-02: Which regions are most affected by each disease?
  OQ-03: What is the monthly/seasonal trend of disease outbreaks?
  OQ-04: Which age group/gender are most vulnerable?
  OQ-05: What is the case fatality rate (CFR) per disease per region?
  OQ-06: How does incidence correlate with population density?
  OQ-07: Which diseases have highest recovery rates, and where?
  OQ-08: Are there concurrent outbreaks in any region?
  OQ-09: What is year-over-year change in cases per disease?
  OQ-10: Which months see peak disease reporting by disease type?
- Objectives OBJ-01..OBJ-05 (all by Dec 2026)
- Docs folder: c:\\Users\\Hp\\Downloads\\hcl\\docs
- Data folder: c:\\Users\\Hp\\Downloads\\hcl\\data
- App folder:  c:\\Users\\Hp\\Downloads\\hcl
"""

HMW_CONTENT = """
HMW STATEMENTS (Step 2 output):
HMW-01 [PRIORITY]: How might we help public health officers instantly spot
  which disease is spiking in a specific region this month vs last year?
  Stakeholder: SH-01 | Pain: No unified trend view | OQ: OQ-01, OQ-09
HMW-02 [PRIORITY]: How might we show hospital administrators which states will
  likely face a patient surge in the next season so they can pre-allocate beds?
  Stakeholder: SH-02 | Pain: Reactive not proactive planning | OQ: OQ-02, OQ-03
HMW-03 [PRIORITY]: How might we help policy makers compare case fatality rates
  across regions in a single glance to justify targeted budget allocations?
  Stakeholder: SH-03 | Pain: Data scattered across reports | OQ: OQ-05, OQ-02
HMW-04 [PRIORITY]: How might we enable epidemiologists to filter disease data
  by age group and gender to identify the most vulnerable demographic segments?
  Stakeholder: SH-04 | Pain: No demographic drill-down | OQ: OQ-04
HMW-05 [PRIORITY]: How might we surface co-occurring disease outbreaks in the
  same region and time window to alert response teams before crises escalate?
  Stakeholder: SH-01, SH-04 | Pain: Outbreaks treated in isolation | OQ: OQ-08
HMW-06: How might we visualise seasonal disease peaks across all diseases on
  one chart so analysts can prepare resources months in advance?
  Stakeholder: SH-01, SH-04 | Pain: Seasonal patterns buried | OQ: OQ-10, OQ-03
HMW-07: How might we display recovery rates alongside fatality rates per region
  so administrators can benchmark their hospitals against peer states?
  Stakeholder: SH-02 | Pain: Recovery data not compared | OQ: OQ-07, OQ-05
HMW-08: How might we show the correlation between population density and disease
  incidence on a scatter chart so researchers can prioritise dense urban zones?
  Stakeholder: SH-04 | Pain: No spatial-incidence link | OQ: OQ-06
HMW-09: How might we provide a year-over-year trend table that highlights which
  diseases are growing vs declining so ministers can redirect funds quickly?
  Stakeholder: SH-03 | Pain: No YoY summary | OQ: OQ-09, OQ-01
HMW-10: How might we give student developers a clean download of the cleaned
  dataset with a data quality summary so they can demonstrate EDA methodology?
  Stakeholder: SH-05 | Pain: No exportable clean data view | OQ: All
"""

BR_CONTENT = """
BUSINESS REQUIREMENTS (Step 3 output):
BR-01 [Must]: The business needs to aggregate disease case counts by disease,
  region and time period so that stakeholders can identify outbreak trends.
  Source: HMW-01, HMW-09 | Measure: All 10 OQs answered in live demo
BR-02 [Must]: The business needs to provide region-level disease comparison so
  that hospital admins can anticipate geographic surge patterns.
  Source: HMW-02 | Measure: Regional bar/map chart functional with filter
BR-03 [Must]: The business needs to display case fatality rates per disease per
  region so that policy makers can target budget decisions.
  Source: HMW-03 | Measure: CFR = Deaths/Cases shown per cell in heatmap
BR-04 [Must]: The business needs to enable demographic filtering (age, gender)
  per disease so that epidemiologists can identify vulnerable populations.
  Source: HMW-04 | Measure: Age+gender filter changes all charts correctly
BR-05 [Must]: The business needs to detect and display concurrent disease
  outbreaks in the same region-month so that alerts can be issued promptly.
  Source: HMW-05 | Measure: Co-occurrence flag visible in overlap analysis
BR-06 [Must]: The business needs to show seasonal (monthly) disease trends so
  that resource pre-positioning decisions are evidence-based.
  Source: HMW-06 | Measure: Monthly trend chart renderable for each disease
BR-07 [Must]: The business needs to compute and display recovery rates per
  disease per region so that hospital performance can be benchmarked.
  Source: HMW-07 | Measure: Recovery rate = Recovered/Cases shown correctly
BR-08 [Should]: The business needs to visualise disease incidence vs population
  density correlation so that researchers can prioritise interventions.
  Source: HMW-08 | Measure: Scatter chart with Pearson r displayed
BR-09 [Should]: The business needs to present year-over-year change percentages
  per disease so that budget re-allocation decisions are data-driven.
  Source: HMW-09 | Measure: YoY% = (This year - Last year)/Last year * 100
BR-10 [Must]: The business needs to store all disease data in a structured
  relational database so that queries are consistent and reproducible.
  Source: HMW-10 | Measure: SQLite DB passes all FK and row-count checks
BR-11 [Must]: The business needs to provide sidebar filters (disease, region,
  year, demographic) that update all charts simultaneously so that multi-
  dimensional exploration is seamless.
  Source: HMW-01..HMW-05 | Measure: All charts refresh on filter change
BR-12 [Should]: The business needs to allow CSV download of the filtered
  dataset so that analysts can perform their own offline analysis.
  Source: HMW-10 | Measure: Download button produces valid CSV
BR-13 [Could]: The business needs to display a data quality summary (missing
  values, duplicates, outliers fixed) so that data credibility is transparent.
  Source: HMW-10 | Measure: Quality page shows before/after counts
BR-14 [Must]: The business needs automated pytest tests covering data loading,
  KPI formulas, and UI rendering so that app correctness is verifiable.
  Source: All BRs | Measure: pytest passes >= 80% coverage, 0 critical fails
BR-15 [Should]: The business needs the app deployed on Streamlit Community
  Cloud with a public URL so that the mentor can evaluate it remotely.
  Source: OBJ-04 | Measure: Public URL accessible, loads < 5 s
"""

phase("Step 2 – HMW Statements")
log("Generating HMW document (Step 2)...")
step2_result = await agent(
    prompt=f"""
{PROJECT_CTX}

You are a senior Business Analyst. Generate the STEP 2 – How Might We document.

Write a Python script using python-docx (v1.2.0) to create a professional Word document.
Save it to: c:\\Users\\Hp\\Downloads\\hcl\\docs\\02_ArgJain_DiseaseTrendAnalysis_HMWStatements.docx

The document must contain:
1. Cover block: title 'DISEASE TREND ANALYSIS', subtitle 'STEP 2 – How Might We (HMW) Statements', all meta fields (Project ID P-01, Student Arg Jain, Roll 2500320140031, Course MCA 2nd Year Data Analytics, Institute ABES Engineering College, Mentor Ms. Kalpana Dwivedi, Date November 2026)

2. Section 1: Stakeholder Pain Points – table with columns: SH ID | Stakeholder | Pain Point 1 | Pain Point 2 | Pain Point 3
   Rows for SH-01 through SH-04 (each with 2-3 specific, realistic pain points for disease trend monitoring)

3. Section 2: HMW Statements Table with columns: HMW ID | How Might We...? | Stakeholder | Pain Point Addressed | Linked OQ(s) | Priority
   Include exactly these 10 HMWs (mark top 5 as PRIORITY):
   HMW-01 [PRIORITY]: How might we help public health officers instantly spot which disease is spiking in a specific region this month vs last year? | SH-01 | No unified real-time trend view | OQ-01, OQ-09
   HMW-02 [PRIORITY]: How might we show hospital administrators which states will face a patient surge next season so they can pre-allocate beds? | SH-02 | Reactive not proactive planning | OQ-02, OQ-03
   HMW-03 [PRIORITY]: How might we help policy makers compare case fatality rates across regions in a single glance to justify targeted budget allocations? | SH-03 | Data scattered across reports | OQ-05, OQ-02
   HMW-04 [PRIORITY]: How might we enable epidemiologists to filter disease data by age group and gender to identify the most vulnerable demographic segments? | SH-04 | No demographic drill-down | OQ-04
   HMW-05 [PRIORITY]: How might we surface co-occurring disease outbreaks in the same region-time window to alert response teams before crises escalate? | SH-01, SH-04 | Outbreaks treated in isolation | OQ-08
   HMW-06: How might we visualise seasonal disease peaks across all diseases on one chart so analysts can prepare resources months in advance? | SH-01, SH-04 | Seasonal patterns buried | OQ-10, OQ-03
   HMW-07: How might we display recovery rates alongside fatality rates per region so administrators can benchmark their hospitals against peer states? | SH-02 | Recovery data not compared | OQ-07, OQ-05
   HMW-08: How might we show the correlation between population density and disease incidence on a scatter chart so researchers can prioritise dense urban zones? | SH-04 | No spatial-incidence link | OQ-06
   HMW-09: How might we provide a year-over-year trend table that highlights which diseases are growing vs declining so ministers can redirect funds quickly? | SH-03 | No YoY summary | OQ-09, OQ-01
   HMW-10: How might we give analysts a clean downloadable dataset with a data quality summary so they can demonstrate rigorous EDA methodology? | SH-05 | No exportable clean data view | OQ-01..OQ-10

4. Section 3: Priority HMW Justifications – table: HMW ID | Priority Reason (1 line each) for the 5 PRIORITY ones

5. Section 4: Coverage Check – table: OQ ID | Covered by HMW (list HMW IDs). Every OQ must be covered. 
   Footer note confirming all 10 OQs covered.

6. Document footer with file name, version, date, institute.

STYLING REQUIREMENTS (must follow exactly):
- Page margins: top/bottom 2.5cm, left 3cm, right 2cm
- Heading color: RGB(26, 83, 118) = #1A5376
- Table header background: #1A5376, white bold text, 9pt
- Alternating row colors: #EBF5FB and #FFFFFF
- Body text: 10pt Calibri
- Table text: 8.5-9pt
- Priority rows: shade with #FEF9E7 (yellow tint) instead of alternating
- Document footer: 8pt grey centered

Write ONLY the Python script. Use only python-docx. No external libraries except os.
Run the script immediately after writing it. 
Output the script content and confirm: SAVED: <path>
""",
    schema={"type": "string"},
    role="Step 2 – HMW Document Writer"
)
log(f"Step 2 agent result: {step2_result[:200]}")

# Extract and run the script
step2_script_result = await call_tool("run_command", CommandLine="""python -c "
import subprocess, re, sys, os, textwrap

script_text = open(r'c:\\\\Users\\\\Hp\\\\Downloads\\\\hcl\\\\docs\\\\gen_step2.py').read()
" """, WaitMsBeforeAsync=5000, toolSummary="Check step2 script")

phase("Step 2 – Write & Run Script")
# Write the step2 script from agent output
write2 = await call_tool("write_file",
    Path=r"c:\Users\Hp\Downloads\hcl\docs\gen_step2_raw.txt",
    Content=step2_result
)
log("Step 2 raw content written.")

phase("Step 3 – Needs Analysis")
log("Generating Needs Analysis document (Step 3)...")

step3_result = await agent(
    prompt=f"""
{PROJECT_CTX}
{HMW_CONTENT}

You are a senior Business Analyst. Generate the STEP 3 – Needs Analysis document.

Write a complete Python script using python-docx (v1.2.0) to create a professional Word document.
Save it to: c:\\Users\\Hp\\Downloads\\hcl\\docs\\03_ArgJain_DiseaseTrendAnalysis_NeedsAnalysis.docx

The document must contain:

COVER BLOCK:
- Title: 'DISEASE TREND ANALYSIS'  
- Subtitle: 'STEP 3 – Needs Analysis & Business Requirements'
- Meta table: Project ID P-01, Student Arg Jain, Roll 2500320140031, Course MCA 2nd Year Data Analytics, Institute ABES Engineering College, Mentor Ms. Kalpana Dwivedi, Document Version v1.0, Date November 2026

SECTION 1: Introduction (2-3 sentences explaining needs analysis purpose)

SECTION 2: Business Requirements Table
Columns: BR ID | Business Requirement | Stakeholder | Source HMW | Priority | Measurement Criterion
Include ALL 15 BRs below:
BR-01 [Must] The business needs to aggregate disease case counts by disease, region and time period so that stakeholders can identify outbreak trends. | SH-01, SH-03 | HMW-01, HMW-09 | All 10 OQs answered in live demo
BR-02 [Must] The business needs to provide region-level disease comparison so that hospital admins can anticipate geographic surge patterns. | SH-02 | HMW-02 | Regional bar/map chart functional with filter
BR-03 [Must] The business needs to display case fatality rates per disease per region so that policy makers can target budget decisions. | SH-03 | HMW-03 | CFR = Deaths/Cases shown per cell in heatmap
BR-04 [Must] The business needs to enable demographic filtering (age group and gender) per disease so that epidemiologists can identify vulnerable populations. | SH-04 | HMW-04 | Age+gender filter changes all charts correctly
BR-05 [Must] The business needs to detect and display concurrent disease outbreaks in the same region-month so that alerts can be issued promptly. | SH-01, SH-04 | HMW-05 | Co-occurrence flag visible in overlap analysis
BR-06 [Must] The business needs to show seasonal monthly disease trends so that resource pre-positioning is evidence-based. | SH-01, SH-04 | HMW-06 | Monthly trend chart renderable for each disease
BR-07 [Must] The business needs to compute and display recovery rates per disease per region so that hospital performance can be benchmarked. | SH-02 | HMW-07 | Recovery rate = Recovered/Cases shown correctly
BR-08 [Should] The business needs to visualise disease incidence vs population density correlation so that researchers can prioritise interventions. | SH-04 | HMW-08 | Scatter chart with Pearson r displayed
BR-09 [Should] The business needs to present year-over-year change percentages per disease so that budget re-allocation decisions are data-driven. | SH-03 | HMW-09 | YoY% = (This yr - Last yr)/Last yr * 100 shown
BR-10 [Must] The business needs to store all disease data in a structured relational database so that queries are consistent and reproducible. | SH-05 | HMW-10 | SQLite DB passes all FK and row-count checks
BR-11 [Must] The business needs sidebar filters (disease, region, year, demographic) that update all charts simultaneously for multi-dimensional exploration. | SH-01..SH-04 | HMW-01..05 | All charts refresh on filter change < 3 s
BR-12 [Should] The business needs CSV download of the filtered dataset so that analysts can perform offline analysis. | SH-04, SH-05 | HMW-10 | Download button produces valid non-empty CSV
BR-13 [Could] The business needs a data quality summary (missing values, duplicates, outliers fixed) so that data credibility is transparent. | SH-05 | HMW-10 | Quality page shows before/after counts
BR-14 [Must] The business needs automated pytest tests covering data loading, KPI formulas, and UI rendering so that app correctness is verifiable. | SH-06 | All BRs | pytest >= 80% coverage, 0 critical failures
BR-15 [Should] The business needs the app deployed on Streamlit Community Cloud with a public URL so that the mentor can evaluate it remotely. | SH-05, SH-06 | OBJ-04 | Public URL accessible, loads < 5 s

SECTION 3: Data Requirements Table
Columns: BR ID | Data Element(s) Needed | Source | Format
Map each BR to the data columns it needs from the synthetic dataset.

SECTION 4: Gap Analysis Table
Columns: Type | ID | Issue | Resolution
Check for: HMWs with no BR, BRs with no HMW, OQs not covered. If none, state "No gaps identified."

SECTION 5: Priority Summary - count Must/Should/Could/Won't BRs with percentages.

Footer: file name, version, date, institute.

STYLING (same as Step 1):
- Page margins: top/bottom 2.5cm, left 3cm, right 2cm
- Heading color: RGB(26, 83, 118)
- Table header: #1A5376 background, white bold 9pt text
- Alternating rows: #EBF5FB / #FFFFFF
- Must rows: use a subtle green-tint #EAFAF1
- Body text: 10pt
- Table text: 8.5-9pt

Output ONLY the complete Python script using python-docx. No other libraries except os.
Make sure all strings are properly escaped (no unterminated strings).
Use triple-quoted strings for long text.
""",
    schema={"type": "string"},
    role="Step 3 – Needs Analysis Writer"
)
log(f"Step 3 agent returned {len(step3_result)} chars")

write3 = await call_tool("write_file",
    Path=r"c:\Users\Hp\Downloads\hcl\docs\gen_step3_raw.txt",
    Content=step3_result
)

phase("Steps 2 & 3 – Execute Scripts")
# Have a worker agent extract and run scripts from raw outputs
exec_agent = agent("""
You are a Python execution expert. I will give you raw text output from an agent that wrote
a python-docx script. Your job is to:
1. Extract the Python script from the raw text (remove any explanation text)
2. Fix any syntax errors (unterminated strings, missing quotes etc.)
3. Save it to the given path
4. Run it with run_command
5. Report SAVED: <path> or any error

Important rules for fixing scripts:
- All string literals must be properly terminated
- Use triple-quoted strings for multi-line content
- Escape backslashes in Windows paths: use r-strings or double backslash
- Never use unterminated string literals

For Step 2 script: save to c:\\Users\\Hp\\Downloads\\hcl\\docs\\gen_step2.py
For Step 3 script: save to c:\\Users\\Hp\\Downloads\\hcl\\docs\\gen_step3.py
""", role="Script Executor")

step2_raw = open(r"c:\Users\Hp\Downloads\hcl\docs\gen_step2_raw.txt").read()
step3_raw = open(r"c:\Users\Hp\Downloads\hcl\docs\gen_step3_raw.txt").read()

exec2 = await exec_agent(
    f"Extract, fix, save and run the Step 2 python-docx script. Here is the raw output:\n\n{step2_raw[:8000]}",
    {"type": "string"}
)
log(f"Step 2 execution: {exec2[:300]}")

exec3 = await exec_agent(
    f"Extract, fix, save and run the Step 3 python-docx script. Here is the raw output:\n\n{step3_raw[:8000]}",
    {"type": "string"}
)
log(f"Step 3 execution: {exec3[:300]}")
del exec_agent

phase("Step 4 – Traceability Matrix (Excel RTM)")
log("Generating RTM Excel (Step 4)...")

step4_result = await agent(
    prompt=f"""
{PROJECT_CTX}
{HMW_CONTENT}
{BR_CONTENT}

You are a senior Business Analyst. Generate STEP 4 – Requirements Traceability Matrix (RTM) as an Excel file.

Write a complete Python script using openpyxl to create the Excel file.
Save to: c:\\Users\\Hp\\Downloads\\hcl\\docs\\04_ArgJain_DiseaseTrendAnalysis_RTM.xlsx

The Excel must have these sheets:

SHEET 1: "RTM" (main traceability matrix)
Columns (with auto-filter enabled):
OQ ID | HMW ID | BR ID | Business Requirement (short) | Stakeholder | Priority | Status | Feature ID | DB Table.Column | User Story ID | UI Screen ID | Test Case (TC-F) | Test Case (TC-T)

Create ONE ROW per HMW-BR link. Where a BR links to multiple HMWs, repeat the row for each HMW.
Status = "Identified" for all rows in this step.
Feature ID, DB Table.Column, User Story ID, UI Screen ID, TC-F, TC-T = "TBD" (will fill in later steps)

Include rows for all 15 BRs × their source HMWs:
BR-01: HMW-01, HMW-09 → 2 rows
BR-02: HMW-02 → 1 row
BR-03: HMW-03 → 1 row
BR-04: HMW-04 → 1 row
BR-05: HMW-05 → 1 row
BR-06: HMW-06 → 1 row
BR-07: HMW-07 → 1 row
BR-08: HMW-08 → 1 row
BR-09: HMW-09 → 1 row (note: also linked from BR-01's HMW-09 row)
BR-10: HMW-10 → 1 row
BR-11: HMW-01, HMW-02, HMW-03, HMW-04, HMW-05 → 5 rows
BR-12: HMW-10 → 1 row
BR-13: HMW-10 → 1 row
BR-14: All HMWs (use "HMW-01..10") → 1 row
BR-15: (source OBJ-04) → 1 row (HMW: "OBJ-04")

Linked OQ column: add OQ IDs that each BR addresses (from context above)

STYLING for RTM sheet:
- Row 1: Header row - dark blue fill #1A5376, white bold text, 12pt, freeze row 1
- Priority column: Must = green fill #EAFAF1, Should = yellow #FEF9E7, Could = orange #FDEBD0
- Status column: "Identified" = light blue #EBF5FB
- TBD cells: light grey #F2F3F4
- Column widths: OQ 8, HMW 8, BR ID 6, Requirement 35, Stakeholder 12, Priority 8, Status 10, Feature 10, DB 15, US 10, UI 10, TC-F 10, TC-T 10
- Alternating row shading for readability
- Bold borders on header row

SHEET 2: "Coverage_Check"
Title row: "RTM Coverage Check – Step 4"
Table 1: OQ Coverage: OQ ID | OQ Question | HMW(s) | BR(s) | Covered?
Table 2: HMW Coverage: HMW ID | BR(s) | Covered?
Table 3: BR Coverage: BR ID | HMW(s) | Covered?
Summary row: Total OQs: 10, All covered: YES | Total HMWs: 10, All covered: YES | Total BRs: 15, All have HMW: YES

SHEET 3: "Change_Log"
Columns: Version | Date | Changed By | Section | Change Description
Row 1: v1.0 | November 2026 | Arg Jain | Initial | RTM created at Step 4 with OQ, HMW, BR columns populated

Apply openpyxl PatternFill, Font, Alignment, Border objects properly.
Make sure auto_filter is applied to the RTM sheet header row.

Output ONLY the complete Python script. Use only openpyxl and os.
Make sure ALL strings are properly terminated. Use triple-quoted strings for safety.
""",
    schema={"type": "string"},
    role="Step 4 – RTM Excel Generator"
)
log(f"Step 4 agent returned {len(step4_result)} chars")

write4 = await call_tool("write_file",
    Path=r"c:\Users\Hp\Downloads\hcl\docs\gen_step4_raw.txt",
    Content=step4_result
)

phase("Step 4 – Execute RTM Script")
exec4_agent = agent("""You are a Python execution expert. Extract the Python script from raw text, 
fix any syntax errors, save to the specified path, and run it. Report SAVED or errors.""",
role="Step 4 Executor")

step4_raw = open(r"c:\Users\Hp\Downloads\hcl\docs\gen_step4_raw.txt").read()
exec4 = await exec4_agent(
    f"Extract, fix, save to c:\\Users\\Hp\\Downloads\\hcl\\docs\\gen_step4.py and run:\n\n{step4_raw[:9000]}",
    {"type": "string"}
)
log(f"Step 4 RTM execution: {exec4[:300]}")
del exec4_agent

phase("Step 5 – BRD")
log("Generating BRD document (Step 5)...")
step5_result = await agent(
    prompt=f"""
{PROJECT_CTX}
{HMW_CONTENT}
{BR_CONTENT}

You are a senior Business Analyst. Generate STEP 5 – Business Requirements Document (BRD).

Write a complete Python script using python-docx (v1.2.0) to create the Word document.
Save to: c:\\Users\\Hp\\Downloads\\hcl\\docs\\05_ArgJain_DiseaseTrendAnalysis_BRD.docx

The BRD must contain these 13 sections with professional content:

COVER BLOCK: Title 'DISEASE TREND ANALYSIS', Subtitle 'STEP 5 – Business Requirements Document (BRD)', meta table (Project ID P-01, Version v1.0, Author Arg Jain, Roll 2500320140031, Date November 2026, Mentor Ms. Kalpana Dwivedi, Status Draft, Institute ABES Engineering College Ghaziabad)

1. DOCUMENT CONTROL
   - Version history table: Version | Date | Author | Changes | Approved by
     v1.0 | Nov 2026 | Arg Jain | Initial draft | Pending

2. EXECUTIVE SUMMARY (3-4 professional paragraphs)
   - What the project is, why it matters, what it delivers

3. BUSINESS PROBLEM AND OPPORTUNITY
   - Current state (pain): 2 bullet problems
   - Desired state (opportunity): 2 bullet opportunities  
   - Business impact of NOT solving: 2 bullet consequences

4. OBJECTIVES AND SUCCESS METRICS (KPIs)
   Table: Objective | KPI | Baseline | Target | Measurement Method
   At least 5 rows from OBJ-01..05

5. STAKEHOLDERS – RACI TABLE
   Rows: each stakeholder SH-01..SH-06
   Columns: SH ID | Stakeholder | Role | Responsible | Accountable | Consulted | Informed
   (R/A/C/I format with project phase notes)

6. SCOPE
   6.1 In Scope: 9 bullet points
   6.2 Out of Scope: 7 bullet points

7. BUSINESS REQUIREMENTS (the core section)
   For EACH of the 15 BRs (BR-01..BR-15) write a sub-section with:
   - BR ID and short title as heading
   - Description: full "The business needs to X so that Y" statement
   - Rationale: why this matters (1-2 sentences)
   - Priority: Must/Should/Could
   - Source HMW: HMW ID(s)
   - Acceptance Criteria: 2-3 testable criteria
   
   Present as a styled table per BR: Field | Detail

8. BUSINESS RULES (5-7 rules)
   Table: BR Rule ID | Business Rule | Applies to BR | Enforcement
   Examples: 
   BRL-01: CFR must be calculated as Deaths/Cases only where Cases > 0 | BR-03 | System validation
   BRL-02: Date range filter cannot be less than 1 month | BR-11 | UI validation
   BRL-03: Recovery rate must not exceed 100% | BR-07 | Data validation
   BRL-04: Synthetic data must have no real person identifiers | BR-10 | Data generation rule
   BRL-05: All percentages must be rounded to 2 decimal places | BR-01..09 | Display rule

9. DATA REQUIREMENTS
   Table: Data Element | Description | Source | Format | Refresh Frequency | Volume
   At least 8 rows covering: disease_cases, fatality_counts, recovery_counts, demographic_data, region_data, population_data, date_period, disease_master

10. ASSUMPTIONS, CONSTRAINTS AND DEPENDENCIES
    Table: ID | Type | Statement | Impact
    Include all 7 assumptions (A-01..A-07) and 5 constraints (C-01..C-05) from Step 1

11. RISKS AND MITIGATION
    Table: Risk ID | Risk | Probability | Impact | Mitigation
    5 realistic risks: synthetic data not realistic, app slow on free tier, 
    test coverage hard to reach 80%, deployment fails, mentor expects real data

12. GLOSSARY
    Table: Term | Definition
    At least 12 terms: CFR, Incidence Rate, Recovery Rate, Outbreak, YoY, 
    Epidemiology, EDA, OQ, HMW, BR, Stakeholder, Synthetic Data

13. SIGN-OFF TABLE
    Columns: Role | Name | Signature | Date
    Rows: Student Developer (Arg Jain), Mentor (Ms. Kalpana Dwivedi), HOD (blank)

STYLING (professional, consistent with Step 1):
- Same color scheme: #1A5376 headings, #EBF5FB/#FFFFFF alternating rows
- Table headers: #1A5376 dark blue, white bold 9pt
- Must BRs: green tint #EAFAF1 background on description cell
- Should BRs: yellow tint #FEF9E7
- Body text: 10pt Calibri
- Section numbers bold, slightly larger
- Page break before major sections 3, 5, 7, 11

Output ONLY the complete Python script. Use python-docx only (plus os).
Use triple-quoted strings for all multi-line text to avoid syntax errors.
Ensure the script is complete and runnable.
""",
    schema={"type": "string"},
    role="Step 5 – BRD Writer"
)
log(f"Step 5 BRD agent returned {len(step5_result)} chars")

write5 = await call_tool("write_file",
    Path=r"c:\Users\Hp\Downloads\hcl\docs\gen_step5_raw.txt",
    Content=step5_result
)

phase("Step 5 – Execute BRD Script")
exec5_agent = agent("You are a Python execution expert. Extract, fix, save and run python-docx scripts. Report SAVED or errors clearly.",
role="Step 5 Executor")
step5_raw = open(r"c:\Users\Hp\Downloads\hcl\docs\gen_step5_raw.txt").read()
exec5 = await exec5_agent(
    f"Extract, fix syntax errors, save to c:\\Users\\Hp\\Downloads\\hcl\\docs\\gen_step5.py and run:\n\n{step5_raw[:9000]}",
    {"type": "string"}
)
log(f"Step 5 execution: {exec5[:300]}")
del exec5_agent

phase("Step 7 – TRD")
log("Generating TRD document (Step 7)...")
step7_result = await agent(
    prompt=f"""
{PROJECT_CTX}
{BR_CONTENT}

You are a Solution Architect. Generate STEP 7 – Technical Requirements Document (TRD).

Write a complete Python script using python-docx (v1.2.0) to create the Word document.
Save to: c:\\Users\\Hp\\Downloads\\hcl\\docs\\07_ArgJain_DiseaseTrendAnalysis_TRD.docx

FIXED TECH STACK:
- Python 3.12, pandas, NumPy, SciPy/statsmodels, Plotly 5.x
- Streamlit 1.35+ (multi-page with pages/ folder)
- Tailwind CDN via st.components.v1.html for header and KPI cards
- SQLite at data/app.db in the repo
- pytest + streamlit.testing.v1.AppTest
- GitHub for version control
- Streamlit Community Cloud for deployment

The TRD must contain these 10 sections:

COVER BLOCK: Same meta as previous docs, subtitle 'STEP 7 – Technical Requirements Document (TRD)'

1. SYSTEM ARCHITECTURE
   ASCII diagram showing:
   data/app.db (SQLite) -> src/data_loader.py (pandas + cache) -> src/cleaning.py 
   -> src/analysis.py (stats) -> pages/01_Overview.py ... pages/06_DataQuality.py
   -> app.py (Streamlit entry, shared sidebar filters via st.session_state)
   Also: Mermaid-style flowchart described in text (since Word can't render Mermaid)

2. FOLDER STRUCTURE
   Show exact folder tree:
   project-root/
     app.py
     requirements.txt
     .streamlit/config.toml
     pages/
       01_Overview.py
       02_Trends.py
       03_Regional_Analysis.py
       04_Demographics.py
       05_EDA_Statistics.py
       06_Data_Quality.py
     src/
       __init__.py
       data_loader.py
       cleaning.py
       analysis.py
       ui.py
     data/
       app.db
       disease_cases.csv
       region_master.csv
       disease_master.csv
       demographic_breakdown.csv
     tests/
       __init__.py
       test_data.py
       test_analysis.py
       test_app.py
     docs/  (all step documents)

3. FUNCTIONAL REQUIREMENTS
   Table: FR ID | Requirement | Linked BR | Linked US (TBD) | Module | Description
   FR-01..FR-15 mapping to BRs:
   FR-01: Load disease case data from SQLite | BR-10 | src/data_loader.py
   FR-02: Filter data by disease, region, year, demographic | BR-11 | src/data_loader.py
   FR-03: Compute case counts by disease and year trend | BR-01 | src/analysis.py
   FR-04: Compute regional disease comparison | BR-02 | src/analysis.py
   FR-05: Compute case fatality rate per disease per region | BR-03 | src/analysis.py
   FR-06: Filter and aggregate by age group and gender | BR-04 | src/analysis.py
   FR-07: Detect co-occurring outbreaks (2+ diseases, same region-month) | BR-05 | src/analysis.py
   FR-08: Compute monthly seasonal trend per disease | BR-06 | src/analysis.py
   FR-09: Compute recovery rates per disease per region | BR-07 | src/analysis.py
   FR-10: Compute incidence-density Pearson correlation | BR-08 | src/analysis.py
   FR-11: Compute year-over-year percentage change | BR-09 | src/analysis.py
   FR-12: Display Overview KPI dashboard (4 KPI cards) | BR-01, BR-11 | pages/01_Overview.py
   FR-13: Render all 6 Plotly chart types | BR-02..BR-09 | pages/*.py
   FR-14: Enable CSV download of filtered dataset | BR-12 | pages/*.py
   FR-15: Display data quality summary report | BR-13 | pages/06_Data_Quality.py

4. NON-FUNCTIONAL REQUIREMENTS
   Table: NFR ID | Category | Requirement | Target | Test Method
   NFR-01: Performance | App initial load time | < 5 seconds | Manual timer
   NFR-02: Performance | Chart re-render on filter change | < 3 seconds | Manual timer
   NFR-03: Reliability | pytest coverage | >= 80% | pytest --cov report
   NFR-04: Reliability | 0 critical test failures at submission | 0 failures | pytest -q
   NFR-05: Usability | All 10 OQs answerable without documentation | 10/10 | Mentor walkthrough
   NFR-06: Maintainability | Each function < 50 lines | < 50 lines | Code review
   NFR-07: Security | No real patient data anywhere | 0 real records | Data audit
   NFR-08: Availability | App uptime during evaluation | >= 99% | Streamlit Cloud monitor

5. DATA LAYER
   - Loading: sqlite3 + pandas read_sql, wrapped in @st.cache_data(ttl=3600)
   - Validation checks on load: row count, column names, FK integrity
   - Cleaning steps in src/cleaning.py: handle NaN (median imputation for numeric, mode for categorical), remove exact duplicates, cap outliers at 3 IQR, log all changes

6. STATISTICAL METHODS PER OQ
   Table: OQ ID | Statistical Method | Python Function | Formula
   OQ-01: Trend comparison | pandas groupby + pct_change | year-over-year sum
   OQ-02: Regional ranking | groupby().sum().sort_values | descending rank
   OQ-03: Time series decomposition | statsmodels seasonal_decompose | additive model
   OQ-04: Demographic breakdown | groupby(['age_group','gender']).sum | pivot table
   OQ-05: CFR | deaths / cases * 100 | per disease-region cell
   OQ-06: Pearson correlation | scipy.stats.pearsonr | incidence_rate vs pop_density
   OQ-07: Recovery rate | recovered / cases * 100 | per disease-region cell
   OQ-08: Co-occurrence | count diseases per region-month where cases > threshold | flag
   OQ-09: YoY change | (current_yr - prev_yr) / prev_yr * 100 | per disease
   OQ-10: Monthly peak | groupby('month').sum().idxmax() | per disease

7. UI TECHNICAL NOTES
   - Tailwind CDN injected via st.components.v1.html in src/ui.py
   - KPI cards: HTML div with Tailwind classes (bg-blue-50, rounded-xl, shadow)
   - Theme: .streamlit/config.toml: primaryColor #1A5376, backgroundColor #F0F8FF
   - Shared filters: st.session_state keys: selected_disease, selected_region, selected_year, selected_age, selected_gender
   - st.sidebar for all filters; filters persist across pages via session_state
   - Responsive: Streamlit's native column layout (col1, col2, col3)

8. PERFORMANCE, ERROR HANDLING, SECURITY
   - @st.cache_data on all data loading functions
   - try/except around DB connections with st.error fallback
   - Input validation: filters must match allowed values (dropdown, not text input)
   - No secrets or API keys in repo; .gitignore: .venv/, __pycache__/, *.pyc

9. REQUIREMENTS.TXT (pinned versions)
   Show the exact requirements.txt content:
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
    5 risks: SQLite concurrency on Cloud (L/M), Tailwind CDN offline (L/M), 
    statsmodels import slow (M/L), Streamlit AppTest API changes (L/M), 
    free-tier memory limit on large dataset (M/H)

STYLING: Same professional style as previous docs.
Output ONLY complete Python script. Triple-quoted strings. No syntax errors.
""",
    schema={"type": "string"},
    role="Step 7 – TRD Writer"
)
log(f"Step 7 TRD returned {len(step7_result)} chars")
write7 = await call_tool("write_file",
    Path=r"c:\Users\Hp\Downloads\hcl\docs\gen_step7_raw.txt",
    Content=step7_result
)

phase("Step 7 – Execute TRD Script")
exec7_agent = agent("Python execution expert: extract, fix, save and run python-docx scripts.",
role="Step 7 Executor")
step7_raw = open(r"c:\Users\Hp\Downloads\hcl\docs\gen_step7_raw.txt").read()
exec7 = await exec7_agent(
    f"Extract, fix, save to c:\\Users\\Hp\\Downloads\\hcl\\docs\\gen_step7.py and run:\n\n{step7_raw[:9000]}",
    {"type": "string"}
)
log(f"Step 7 execution: {exec7[:300]}")
del exec7_agent

phase("Step 8 – Database Design")
log("Generating DB Design Excel + RTM update (Step 8)...")

DB_SCHEMA = """
DATABASE SCHEMA (use exactly these tables and columns):

TABLE 1: disease_master (master)
disease_id INTEGER PK | disease_name TEXT NOT NULL UNIQUE | disease_category TEXT | 
description TEXT | is_contagious INTEGER (0/1) | typical_incubation_days INTEGER
Rows: 5 (Dengue, Malaria, TB, COVID-19, Typhoid)

TABLE 2: region_master (master)
region_id INTEGER PK | region_name TEXT NOT NULL UNIQUE | state_code TEXT |
zone TEXT (North/South/East/West/Central) | population INTEGER NOT NULL |
area_sqkm REAL | population_density REAL (computed: population/area)
Rows: 10 Indian states

TABLE 3: demographic_group (master)
demo_id INTEGER PK | age_group TEXT NOT NULL | gender TEXT NOT NULL |
age_min INTEGER | age_max INTEGER
UNIQUE(age_group, gender)
Rows: 5 age groups × 3 genders = 15 rows

TABLE 4: disease_cases (main fact table - GRAIN: one row per disease × region × month × demographic group)
case_id INTEGER PK | disease_id INTEGER FK(disease_master) | region_id INTEGER FK(region_master) |
demo_id INTEGER FK(demographic_group) | report_date DATE NOT NULL |
report_year INTEGER | report_month INTEGER |
cases_reported INTEGER NOT NULL DEFAULT 0 |
deaths INTEGER NOT NULL DEFAULT 0 |
recovered INTEGER NOT NULL DEFAULT 0 |
active_cases INTEGER (cases - deaths - recovered) |
hospitalized INTEGER | is_outbreak INTEGER (0/1) |
data_source TEXT | created_at TIMESTAMP
CHECK: deaths <= cases_reported, recovered <= cases_reported, cases_reported >= 0
Rows: 5 diseases × 10 regions × 60 months × 15 demo groups = 45,000 rows (use subset ~300 for realism)
Actually: 5 × 10 × 60 = 3000 rows (aggregate at region-month-disease level, not demographic)
Plus: demographic_breakdown as separate table

TABLE 5: demographic_breakdown (fact - GRAIN: disease × region × month × demographic)  
breakdown_id INTEGER PK | case_id INTEGER FK(disease_cases) |
demo_id INTEGER FK(demographic_group) |
cases_in_group INTEGER | deaths_in_group INTEGER | recovered_in_group INTEGER
Rows: 3000 × subset of demographics = ~9000 rows (but generate ~300 for manageability)

ANALYSIS VIEW: v_disease_analysis (JOIN of all tables)
~35 columns including all KPIs: cfr_pct, recovery_rate_pct, incidence_per_lakh,
yoy_change_pct, is_concurrent_outbreak
"""

step8_result = await agent(
    prompt=f"""
{PROJECT_CTX}
{BR_CONTENT}
{DB_SCHEMA}

You are a Data Architect. Generate STEP 8 – Database Design as an Excel file.

Write a complete Python script using openpyxl to create the Excel file.
Save to: c:\\Users\\Hp\\Downloads\\hcl\\docs\\08_ArgJain_DiseaseTrendAnalysis_DBDesign.xlsx

The Excel must have these sheets:

SHEET 1: "Overview"
Title: Disease Trend Analysis – Database Design (Step 8)
Brief description of design approach (3-4 lines)
Key stats: 5 tables, ~3300 rows in fact table, 35+ columns in analysis view
Design principles: 3NF normalized, referential integrity via FK, CHECK constraints

SHEET 2: "Tables_Summary"
Columns: Table Name | Grain | Primary Key | Foreign Keys | Total Columns | Est. Rows | Purpose
5 rows for 5 tables

SHEET 3: "DD_disease_master" (data dictionary for disease_master)
Columns: Column Name | Data Type | Key | Nullable | Allowed Values | Description | OQ/BR Supported
All columns of disease_master table

SHEET 4: "DD_region_master"
Same structure for region_master

SHEET 5: "DD_demographic_group"
Same structure for demographic_group

SHEET 6: "DD_disease_cases"
Same structure for disease_cases (main fact table - most important sheet)

SHEET 7: "DD_demographic_breakdown"
Same structure for demographic_breakdown

SHEET 8: "Relationships"
Columns: Parent Table | Child Table | Join Key | Cardinality | Business Rule
4 relationships: disease_master→disease_cases, region_master→disease_cases,
demographic_group→disease_cases, disease_cases→demographic_breakdown

SHEET 9: "KPIs_Measures"
Columns: KPI/Measure Name | Formula | Unit | OQ Supported | BR Supported
At least 8 KPIs: Total Cases, CFR%, Recovery Rate%, Incidence per Lakh, YoY Change%,
Active Cases, Outbreak Flag, Co-occurrence Count

SHEET 10: "SQLite_DDL"
Complete CREATE TABLE statements for all 5 tables plus CREATE VIEW for v_disease_analysis
Include: PRIMARY KEY, FOREIGN KEY, NOT NULL, CHECK, UNIQUE constraints
Include: CREATE INDEX statements for performance

SHEET 11: "RTM_Updated"
Copy the RTM from Step 4 and fill in the DB Table.Column column for each BR

STYLING for all sheets:
- Header row: dark blue #1A5376, white bold text
- Alternating rows: #EBF5FB / #FFFFFF  
- Column widths appropriate to content
- Sheet tabs: color the data dictionary sheets blue, DDL sheet green

Output ONLY the complete Python script using openpyxl and os.
Use triple-quoted strings. Ensure no syntax errors.
""",
    schema={"type": "string"},
    role="Step 8 – DB Design Excel Generator"
)
log(f"Step 8 DB Design returned {len(step8_result)} chars")
write8 = await call_tool("write_file",
    Path=r"c:\Users\Hp\Downloads\hcl\docs\gen_step8_raw.txt",
    Content=step8_result
)

phase("Step 8 – Execute DB Design Script")
exec8_agent = agent("Python execution expert: extract, fix, save and run openpyxl scripts.",
role="Step 8 Executor")
step8_raw = open(r"c:\Users\Hp\Downloads\hcl\docs\gen_step8_raw.txt").read()
exec8 = await exec8_agent(
    f"Extract, fix syntax, save to c:\\Users\\Hp\\Downloads\\hcl\\docs\\gen_step8.py and run:\n\n{step8_raw[:9000]}",
    {"type": "string"}
)
log(f"Step 8 execution: {exec8[:300]}")
del exec8_agent

phase("Step 9 – ER Diagram")
log("Generating ER Diagram document (Step 9)...")

step9_result = await agent(
    prompt=f"""
{PROJECT_CTX}
{DB_SCHEMA}

You are a Data Architect. Generate STEP 9 – ER Diagram document.

Write a complete Python script using python-docx (v1.2.0).
Save to: c:\\Users\\Hp\\Downloads\\hcl\\docs\\09_ArgJain_DiseaseTrendAnalysis_ERDiagram.docx

The document must contain:

COVER BLOCK: same meta, subtitle 'STEP 9 – Entity-Relationship Diagram'

SECTION 1: Mermaid ER Diagram Code
Display this exact Mermaid erDiagram code in a styled code block (monospace font, light grey background):

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
        real area_sqkm
        real population_density
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
    region_master ||--o{{ disease_cases : "reports"
    disease_cases ||--o{{ demographic_breakdown : "broken down by"
    demographic_group ||--o{{ demographic_breakdown : "classifies"

SECTION 2: Relationship Descriptions
One paragraph per relationship (5 total including view):
- "One disease in disease_master has zero or many case records in disease_cases. Each case record reports incidents for exactly one disease."
- "One region in region_master reports zero or many disease case records. Each case record belongs to exactly one region."
- "One disease_cases record is broken down into zero or many demographic_breakdown records. Each breakdown row belongs to exactly one case record."
- "One demographic group classifies zero or many demographic_breakdown rows. Each breakdown row references exactly one demographic group."
- "The analysis view v_disease_analysis joins all four base tables to produce a denormalised view of approximately 35 columns for query convenience."

SECTION 3: Business Rules Enforced by Design
Numbered list of 7 business rules:
1. A disease case record must reference a valid disease (FK constraint: disease_cases.disease_id → disease_master.disease_id)
2. A case record must belong to a valid region (FK: disease_cases.region_id → region_master.region_id)
3. Deaths and recoveries cannot exceed total reported cases (CHECK: deaths <= cases_reported AND recovered <= cases_reported)
4. Cases reported must be non-negative (CHECK: cases_reported >= 0)
5. Each disease must have a unique name (UNIQUE: disease_master.disease_name)
6. Each demographic group is uniquely identified by age_group + gender combination (UNIQUE: demographic_group(age_group, gender))
7. Population density in region_master must be non-negative (CHECK: population_density >= 0)

SECTION 4: Design Review and Issues
Table: Issue ID | Issue | Severity | Fix Applied
Review these points:
Issue 1: active_cases in disease_cases is derived (cases - deaths - recovered) → store as computed or add CHECK | Medium | Added CHECK constraint; computed on load
Issue 2: population_density in region_master is derived (population/area_sqkm) → redundant | Low | Kept for query performance; documented as derived
Issue 3: demographic_breakdown is a bridge resolving disease_cases to demographic_group (the many-to-many between a case record and demographics is naturally one-to-many via demo_id) | Low | No change needed; correct cardinality
Issue 4: No audit trail for data corrections | Low | created_at timestamp added; future enhancement for updated_at
Issue 5: report_date with report_year and report_month columns are partially redundant | Low | Kept for fast filtering; documented

SECTION 5: ER Diagram Image Placeholder
Add a placeholder paragraph: "[INSERT ER DIAGRAM PNG HERE - Generated from mermaid.live]"
Instructions: "Paste the Mermaid code from Section 1 into https://mermaid.live, export as PNG, 
and insert it in this placeholder. File name: 09_ER_Diagram.png"

SECTION 6: SQLite DDL Reference (abbreviated)
Show CREATE TABLE statements for disease_master and disease_cases as example (monospace font).

Footer: file name, version, date, institute.

STYLING: Same as previous docs. 
Code blocks: monospace Courier New 9pt, light grey background #F8F9FA.
Output ONLY the complete Python script. No syntax errors. Triple-quoted strings.
""",
    schema={"type": "string"},
    role="Step 9 – ER Diagram Writer"
)
log(f"Step 9 ER Diagram returned {len(step9_result)} chars")
write9 = await call_tool("write_file",
    Path=r"c:\Users\Hp\Downloads\hcl\docs\gen_step9_raw.txt",
    Content=step9_result
)

phase("Step 9 – Execute ER Diagram Script")
exec9_agent = agent("Python execution expert: extract, fix, save and run python-docx scripts.",
role="Step 9 Executor")
step9_raw = open(r"c:\Users\Hp\Downloads\hcl\docs\gen_step9_raw.txt").read()
exec9 = await exec9_agent(
    f"Extract, fix, save to c:\\Users\\Hp\\Downloads\\hcl\\docs\\gen_step9.py and run:\n\n{step9_raw[:9000]}",
    {"type": "string"}
)
log(f"Step 9 execution: {exec9[:300]}")
del exec9_agent

phase("Step 10 – Dataset Generation")
log("Generating dataset generation Python script (Step 10)...")

step10_code = await agent(
    prompt=f"""
{PROJECT_CTX}
{DB_SCHEMA}

You are a Python data engineer. Generate STEP 10 – the complete dataset generation script.

Write the COMPLETE src/generate_data.py script (save to c:\\Users\\Hp\\Downloads\\hcl\\src\\generate_data.py).
Also create the directories: c:\\Users\\Hp\\Downloads\\hcl\\src and c:\\Users\\Hp\\Downloads\\hcl\\data

The script must:
1. Use random seed 42 for reproducibility
2. Generate synthetic data for all 5 database tables
3. Build in 3-5 realistic patterns (list them in comments)
4. Add data quality issues (2-3% missing, 2-3 duplicates, a few outliers)
5. Save outputs: data/disease_cases.csv, data/region_master.csv, 
   data/disease_master.csv, data/demographic_group.csv, 
   data/demographic_breakdown.csv, data/disease_trend_analysis_data.xlsx (all sheets),
   data/app.db (SQLite with all DDL + data)
6. Print a validation report at the end

EXACT DATA TO GENERATE:

disease_master (5 rows):
(1, 'Dengue', 'Vector-borne', 'Mosquito-transmitted viral infection', 1, 7)
(2, 'Malaria', 'Vector-borne', 'Plasmodium parasite infection via mosquito', 1, 14)
(3, 'Tuberculosis', 'Airborne', 'Mycobacterium tuberculosis bacterial infection', 1, 42)
(4, 'COVID-19', 'Airborne', 'SARS-CoV-2 coronavirus infection', 1, 5)
(5, 'Typhoid', 'Waterborne', 'Salmonella typhi bacterial infection', 1, 10)

region_master (10 rows - Indian states with realistic populations):
(1, 'Uttar Pradesh', 'UP', 'North', 231502578, 240928, 960.9)
(2, 'Maharashtra', 'MH', 'West', 123144223, 307713, 400.2)
(3, 'Delhi', 'DL', 'North', 32941308, 1484, 22198.3)
(4, 'Rajasthan', 'RJ', 'North', 81032689, 342239, 236.8)
(5, 'Bihar', 'BR', 'East', 128500364, 94163, 1364.9)
(6, 'West Bengal', 'WB', 'East', 100896618, 88752, 1136.9)
(7, 'Tamil Nadu', 'TN', 'South', 83697770, 130058, 643.6)
(8, 'Karnataka', 'KA', 'South', 67562686, 191791, 352.3)
(9, 'Gujarat', 'GJ', 'West', 72429009, 196024, 369.5)
(10, 'Madhya Pradesh', 'MP', 'Central', 85002417, 308252, 275.8)

demographic_group (15 rows = 5 age groups × 3 genders):
age groups: '0-14', '15-29', '30-44', '45-59', '60+'
genders: 'Male', 'Female', 'Other'
demo_id 1-15, age_min/max corresponding to age group

disease_cases (GRAIN: disease × region × month, 3000 rows = 5×10×60):
For each combination of disease_id (1-5), region_id (1-10), report_date (Jan 2020 - Dec 2024):
- cases_reported: realistic values by disease (Dengue: 50-800, Malaria: 30-600, TB: 10-200, COVID-19: 100-5000, Typhoid: 20-400)
- COVID-19 spike in 2020-2021 (multiply by 3-5x for those years)
- Dengue/Malaria peak in monsoon months (Jul-Sep): multiply by 2-3x
- TB relatively stable year-round
- deaths: 0.5-3% of cases (COVID higher at 2-5%)
- recovered: 85-97% of cases
- active_cases = cases - deaths - recovered (can be 0)
- hospitalized: 10-30% of cases
- is_outbreak: 1 if cases > 2x regional average for that month, else 0
- data_source: 'ICMR Synthetic', 'State Health Dept Synthetic', or 'WHO India Synthetic' (random)

PATTERNS TO BUILD IN (add as comments and ensure data reflects them):
PATTERN-1: Dengue and Malaria peak in monsoon months (July-September) - visible in OQ-10
PATTERN-2: COVID-19 shows massive spike in 2021, decline from 2022 - visible in OQ-01, OQ-09
PATTERN-3: Dense urban regions (Delhi, Maharashtra) have higher incidence rates per lakh - OQ-06
PATTERN-4: Elderly (60+) have higher CFR for all diseases - OQ-04, OQ-05
PATTERN-5: TB shows consistent burden in UP and Bihar vs lower in Kerala proxy states - OQ-02

DATA QUALITY ISSUES TO ADD (fix in cleaning.py, document here):
DQ-01: 2% of cases_reported values set to NaN (introduce after generation)
DQ-02: 3 exact duplicate rows added to disease_cases
DQ-03: 5 outlier rows where cases_reported is 10x normal (typos simulation)
DQ-04: 1% of deaths values set to NaN

demographic_breakdown (~300 rows):
Sample 300 case_ids from disease_cases
For each sampled case_id, distribute cases across 3-5 demographic groups
Ensure sum of cases_in_group ≈ cases_reported (allow ±10% for realism)

SQLite app.db:
Create all tables with DDL (FK constraints, CHECK constraints)
PRAGMA foreign_keys = ON
Insert all data
Create analysis view v_disease_analysis joining all tables

VALIDATION REPORT to print:
- Row counts per table (expected vs actual)
- FK integrity check (any orphan records)
- Range check (any cases < 0, deaths > cases, etc.)
- Duplicate check
- Missing value count per column
- Pattern verification: "Dengue July avg > Dengue January avg: TRUE/FALSE"

The script must be COMPLETE and RUNNABLE. Use:
import pandas as pd
import numpy as np
import sqlite3
import os
from pathlib import Path

random.seed(42) and np.random.seed(42) at top.

After generating, print: "DATA GENERATION COMPLETE. Files saved to data/"

Output ONLY the complete Python script. No other text.
""",
    schema={"type": "string"},
    role="Step 10 – Dataset Generator"
)
log(f"Step 10 script returned {len(step10_code)} chars")

# Save and run the script
write10 = await call_tool("write_file",
    Path=r"c:\Users\Hp\Downloads\hcl\src\generate_data.py",
    Content=step10_code
)

phase("Step 10 – Run Data Generation")
exec10 = await call_tool("run_command",
    CommandLine=r"cd c:\Users\Hp\Downloads\hcl && python src\generate_data.py 2>&1",
    WaitMsBeforeAsync=60000,
    toolSummary="Run dataset generation script"
)
log(f"Step 10 run result: {str(exec10)[:500]}")

phase("Step 11 – User Stories")
log("Generating User Stories document (Step 11)...")

step11_result = await agent(
    prompt=f"""
{PROJECT_CTX}
{BR_CONTENT}
Features from TRD: FR-01..FR-15 (data loading, filtering, 10 OQ analysis functions, 6 pages, download, data quality)

You are a Product Owner. Generate STEP 11 – User Stories document.

Write a complete Python script using python-docx (v1.2.0).
Save to: c:\\Users\\Hp\\Downloads\\hcl\\docs\\11_ArgJain_DiseaseTrendAnalysis_UserStories.docx

The document must contain:

COVER BLOCK: same meta, subtitle 'STEP 11 – User Stories'

SECTION 1: Epic Overview Table
Epic ID | Epic Name | Description | Stories Count | Priority
EP-01 | Data Infrastructure | Data loading, DB setup, cleaning pipeline | 3 | Must
EP-02 | Dashboard & KPIs | Overview page with KPI cards and filters | 4 | Must
EP-03 | Trend Analysis | Time series, YoY, seasonal analysis | 4 | Must
EP-04 | Regional & Demographic | Regional maps, demographic breakdown | 3 | Must
EP-05 | Insights & Quality | Correlation, co-occurrence, data quality page | 3 | Should

SECTION 2: User Stories Table (main table)
Columns: US ID | Epic | Persona | User Story | Feature ID | BR ID | Priority | Story Points

Write exactly 17 user stories:

EPIC EP-01 – Data Infrastructure:
US-01 | EP-01 | Student Developer | As a student developer, I want the app to load all disease data from SQLite on startup so that every page has consistent data without repeated file reads. | FR-01 | BR-10 | Must | 3
US-02 | EP-01 | Student Developer | As a student developer, I want a data cleaning pipeline that removes duplicates, imputes missing values, and flags outliers so that the analysis is based on reliable data. | FR-01 | BR-13 | Must | 3
US-03 | EP-01 | Student Developer | As a student developer, I want sidebar filters (disease, region, year, demographic) stored in session_state so that every page responds to the same selection without reload. | FR-02 | BR-11 | Must | 2

EPIC EP-02 – Dashboard & KPIs:
US-04 | EP-02 | Public Health Officer | As a public health officer, I want a KPI dashboard on the Overview page showing total cases, deaths, recoveries, and active cases for my selection so that I get an instant health snapshot. | FR-12 | BR-01 | Must | 3
US-05 | EP-02 | Public Health Officer | As a public health officer, I want to see which disease has the highest year-over-year increase as a KPI badge so that I can immediately identify the fastest-growing threat. | FR-11 | BR-09 | Must | 2
US-06 | EP-02 | Hospital Administrator | As a hospital administrator, I want a bar chart of total cases by region so that I can see which states need the most resource support. | FR-04 | BR-02 | Must | 2
US-07 | EP-02 | Policy Maker | As a policy maker, I want a summary table of case fatality rates per disease across all regions on the overview page so that I can quickly identify high-risk disease-region pairs. | FR-05 | BR-03 | Must | 3

EPIC EP-03 – Trend Analysis:
US-08 | EP-03 | Public Health Officer | As a public health officer, I want a monthly time-series line chart showing case counts per disease so that I can spot seasonal peaks and trough patterns. | FR-08 | BR-06 | Must | 3
US-09 | EP-03 | Epidemiologist | As an epidemiologist, I want a year-over-year comparison chart showing case counts for each year as overlapping lines so that I can identify multi-year trends. | FR-03 | BR-01 | Must | 3
US-10 | EP-03 | Policy Maker | As a policy maker, I want a YoY percentage change table per disease sorted by biggest increase so that I can redirect health budgets to growing threats. | FR-11 | BR-09 | Must | 2
US-11 | EP-03 | Epidemiologist | As an epidemiologist, I want a seasonal heatmap (months as columns, diseases as rows, cases as cell colour intensity) so that I can identify which diseases peak in which months. | FR-08 | BR-06 | Should | 3

EPIC EP-04 – Regional & Demographic:
US-12 | EP-04 | Hospital Administrator | As a hospital administrator, I want a choropleth-style bar chart ranking states by CFR so that I can benchmark my state against peers and prioritise improvement areas. | FR-05 | BR-03 | Must | 3
US-13 | EP-04 | Epidemiologist | As an epidemiologist, I want a stacked bar chart of cases broken down by age group and gender for a selected disease so that I can identify the most vulnerable demographics. | FR-06 | BR-04 | Must | 3
US-14 | EP-04 | Epidemiologist | As an epidemiologist, I want a scatter chart of disease incidence rate vs population density per region with Pearson r displayed so that I can quantify the urbanisation-disease link. | FR-10 | BR-08 | Should | 3

EPIC EP-05 – Insights & Quality:
US-15 | EP-05 | Public Health Officer | As a public health officer, I want a concurrent outbreak detector that flags any region-month where 2 or more diseases exceed their average threshold simultaneously so that I can alert field teams early. | FR-07 | BR-05 | Must | 5
US-16 | EP-05 | Epidemiologist | As an epidemiologist, I want a CSV download button on every analysis page so that I can export filtered data for my own offline statistical work. | FR-14 | BR-12 | Should | 1
US-17 | EP-05 | Student Developer | As a student developer, I want a Data Quality page showing before/after cleaning statistics (rows removed, NaNs filled, outliers capped) so that the mentor can verify my data handling methodology. | FR-15 | BR-13 | Could | 2

SECTION 3: Acceptance Criteria (Given/When/Then)
For each US, provide acceptance criteria. Present as a compact table per epic:
Columns: US ID | Given | When | Then

Write full Given/When/Then for all 17 stories.

SECTION 4: Sprint Plan
Table: Day | Tasks (US IDs) | Goal | Deliverable
Day 1: US-01, US-02, US-03 | Data layer ready | app.db loaded, filters work
Day 2: US-04, US-05, US-06 | Overview page done | KPI cards and bar chart
Day 3: US-07, US-08, US-09 | CFR and trends | Trend page functional
Day 4: US-10, US-11 | Seasonal patterns | Heatmap and YoY table
Day 5: US-12, US-13 | Regional and demographic | Pages 3 and 4
Day 6: US-14, US-15 | Insights | Scatter and co-occurrence
Day 7: US-16, US-17 | Quality and download | Data quality page
Day 8: Testing, fixes, deployment | All tests pass | pytest green, app live

SECTION 5: Story Point Summary
Total story points per epic, priority breakdown.

STYLING: Same professional style.
Output ONLY the complete Python script. Triple-quoted strings. No syntax errors.
""",
    schema={"type": "string"},
    role="Step 11 – User Stories Writer"
)
log(f"Step 11 returned {len(step11_result)} chars")
write11 = await call_tool("write_file",
    Path=r"c:\Users\Hp\Downloads\hcl\docs\gen_step11_raw.txt",
    Content=step11_result
)

phase("Step 11 – Execute Script")
exec11_agent = agent("Python execution expert: extract, fix, save and run python-docx scripts.",
role="Step 11 Executor")
step11_raw = open(r"c:\Users\Hp\Downloads\hcl\docs\gen_step11_raw.txt").read()
exec11 = await exec11_agent(
    f"Extract, fix, save to c:\\Users\\Hp\\Downloads\\hcl\\docs\\gen_step11.py and run:\n\n{step11_raw[:9000]}",
    {"type": "string"}
)
log(f"Step 11 execution: {exec11[:300]}")
del exec11_agent

phase("Step 12 – UI Framework")
log("Generating UI Framework document (Step 12)...")

step12_result = await agent(
    prompt=f"""
{PROJECT_CTX}
{BR_CONTENT}
User Stories: US-01..US-17 as defined in Step 11.
Pages: 01_Overview.py, 02_Trends.py, 03_Regional_Analysis.py, 04_Demographics.py, 05_EDA_Statistics.py, 06_Data_Quality.py

You are a UI/UX Designer. Generate STEP 12 – UI Framework document.

Write a complete Python script using python-docx (v1.2.0).
Save to: c:\\Users\\Hp\\Downloads\\hcl\\docs\\12_ArgJain_DiseaseTrendAnalysis_UIFramework.docx

The document must contain:

COVER BLOCK: same meta, subtitle 'STEP 12 – UI Framework'

SECTION 1: Screen Inventory Table
Columns: UI ID | Screen Name | File | Purpose | Key Components | Filters Used | User Stories
UI-01 | Overview / KPI Dashboard | 01_Overview.py | Health snapshot with KPI cards | 4 KPI cards, bar chart, CFR table | disease, region, year | US-04, US-05, US-06, US-07
UI-02 | Disease Trends | 02_Trends.py | Time-series and seasonal analysis | Line chart, YoY chart, heatmap | disease, year | US-08, US-09, US-10, US-11
UI-03 | Regional Analysis | 03_Regional_Analysis.py | Region comparison and CFR ranking | Horizontal bar chart, CFR heatmap | disease, year | US-12
UI-04 | Demographics | 04_Demographics.py | Age group and gender breakdown | Stacked bar, pie chart | disease, region, age, gender | US-13
UI-05 | EDA & Insights | 05_EDA_Statistics.py | Correlation, co-occurrence, stats | Scatter plot, overlap table, stats summary | disease, region, year | US-14, US-15
UI-06 | Data Quality | 06_Data_Quality.py | Data cleaning audit and download | Before/after table, download button | None | US-16, US-17

SECTION 2: ASCII Wireframes (one per screen)
For each screen, draw an ASCII wireframe showing:
- Top: Tailwind header bar (project title, disease, breadcrumb)
- Left sidebar (160px): filter controls
- Main area: KPI cards row + charts grid

Example format for UI-01 Overview:
+------------------------------------------------------------------+
|  DISEASE TREND ANALYSIS                    [Streamlit Header]    |
+------------------+-----------------------------------------------+
| FILTERS          | KPI CARDS (4 cards, 2x2 grid)                 |
| Disease: [v]     |  +----------+ +----------+ +--------+ +------+|
| Region:  [v]     |  |Total     | |Deaths    | |Recovrd | |CFR % ||
| Year:    [v]     |  |Cases     | |          | |        | |      ||
| Age:     [v]     |  |[number]  | |[number]  | |[number]| |[n%]  ||
| Gender:  [v]     |  +----------+ +----------+ +--------+ +------+|
|                  |                                               |
| [Apply Filters]  | BAR CHART: Cases by Region (Plotly bar)      |
|                  | [interactive bar chart, 10 bars]             |
+------------------+ CFR TABLE: Disease x Region heatmap          |
                   | [colour-coded table]                         |
                   +-----------------------------------------------+

Draw similar wireframes for all 6 screens.

SECTION 3: Global Layout Specification
3.1 Shared Sidebar Filters (table): Filter Name | Widget | session_state key | Options
disease_filter | st.selectbox | selected_disease | All Diseases + 5 disease names
region_filter | st.multiselect | selected_regions | All Regions + 10 state names
year_filter | st.slider | selected_year_range | 2020-2024
age_filter | st.multiselect | selected_age_groups | All + 5 age groups
gender_filter | st.radio | selected_gender | All, Male, Female, Other

3.2 Colour Theme:
Primary: #1A5376 (deep blue)
Accent: #2E86AB (medium blue)
Success: #1E8B4C (green - good metrics)
Warning: #E67E22 (orange - attention)
Danger: #C0392B (red - critical)
Background: #F0F8FF (alice blue)
Card background: #FFFFFF
Text: #2C3E50

3.3 Typography: Heading: Poppins 24px bold | Subheading: 16px medium | Body: 14px | KPI value: 32px bold

SECTION 4: Reusable Components
For each component, describe its structure and Tailwind classes:
4.1 KPI Card: HTML div, classes bg-white rounded-xl shadow-md p-4, with icon, label, value, delta
4.2 Chart Card: st.container with custom CSS border and title, plotly chart inside
4.3 Insight Box: HTML div, classes bg-blue-50 border-l-4 border-blue-500 p-3, for key findings
4.4 Filter Badge: Shows active filter count in sidebar

SECTION 5: Best Chart for Each OQ
Table: OQ ID | Best Chart Type | Plotly Function | Why This Chart | Secondary Chart
OQ-01: Line chart | px.line | Shows trend over time | Bar chart
OQ-02: Horizontal bar | px.bar(orientation='h') | Easy region ranking | Heatmap
OQ-03: Time series line | px.line | Monthly patterns clear | Area chart
OQ-04: Grouped bar | px.bar(barmode='group') | Demographic comparison | Pie chart
OQ-05: Heatmap | px.imshow | Disease x Region CFR matrix | Table
OQ-06: Scatter | px.scatter | Correlation with trendline | No secondary
OQ-07: Grouped bar | px.bar | Recovery vs CFR side by side | Table
OQ-08: Scatter timeline | px.scatter | Outbreak flags per month | Table
OQ-09: Bar with delta | px.bar | YoY% positive/negative colour | Table
OQ-10: Heatmap | px.imshow | Month x Disease peak matrix | Line chart

SECTION 6: config.toml Theme
Show the exact .streamlit/config.toml content:
[theme]
primaryColor = "#1A5376"
backgroundColor = "#F0F8FF"
secondaryBackgroundColor = "#E8F4FD"
textColor = "#2C3E50"
font = "sans serif"

SECTION 7: Starter src/ui.py Code
Show the complete src/ui.py code with:
- inject_tailwind() function using st.components.v1.html with Tailwind CDN
- render_header(title, subtitle) function
- render_kpi_card(label, value, delta, icon, color) function using HTML
- render_insight_box(text) function

Present code in a code block (Courier New 9pt, grey background #F8F9FA).

Footer: file name, version, date, institute.
STYLING: Same professional style.
Output ONLY the complete Python script. Triple-quoted strings. No syntax errors.
""",
    schema={"type": "string"},
    role="Step 12 – UI Framework Writer"
)
log(f"Step 12 returned {len(step12_result)} chars")
write12 = await call_tool("write_file",
    Path=r"c:\Users\Hp\Downloads\hcl\docs\gen_step12_raw.txt",
    Content=step12_result
)

phase("Step 12 – Execute Script")
exec12_agent = agent("Python execution expert: extract, fix, save and run python-docx scripts.",
role="Step 12 Executor")
step12_raw = open(r"c:\Users\Hp\Downloads\hcl\docs\gen_step12_raw.txt").read()
exec12 = await exec12_agent(
    f"Extract, fix, save to c:\\Users\\Hp\\Downloads\\hcl\\docs\\gen_step12.py and run:\n\n{step12_raw[:9000]}",
    {"type": "string"}
)
log(f"Step 12 execution: {exec12[:300]}")
del exec12_agent

phase("Step 13 – Test Cases")
log("Generating Test Cases document + pytest files (Step 13)...")

step13_result = await agent(
    prompt=f"""
{PROJECT_CTX}
{BR_CONTENT}
User Stories: US-01..US-17
UI Screens: UI-01..UI-06

You are a QA Engineer. Generate STEP 13 – Test Cases.

PART A: Write a complete Python script using python-docx to create the test cases document.
Save to: c:\\Users\\Hp\\Downloads\\hcl\\docs\\13_ArgJain_DiseaseTrendAnalysis_TestCases.docx

PART B: Write test files (output as separate code blocks after the docx script):
- c:\\Users\\Hp\\Downloads\\hcl\\tests\\test_data.py
- c:\\Users\\Hp\\Downloads\\hcl\\tests\\test_analysis.py

The Word document must contain:

COVER BLOCK: same meta, subtitle 'STEP 13 – Test Cases'

SECTION A: Functional Test Cases (TC-F-01..TC-F-20)
Table: TC ID | Linked US | Linked BR | UI Screen | Pre-condition | Test Steps | Test Data | Expected Result | Priority | Status

Write 20 functional test cases covering:
TC-F-01: App loads without error on Overview page | US-04 | BR-01 | UI-01 | App running | Navigate to Overview | None | Page loads in < 5s, 4 KPI cards visible | High | Not Run
TC-F-02: Disease filter changes KPI values | US-04 | BR-11 | UI-01 | App running | Select 'Dengue' | disease=Dengue | All KPI cards show Dengue-only totals | High | Not Run
TC-F-03: Region filter changes bar chart | US-06 | BR-02, BR-11 | UI-01 | App running | Select 'Delhi' | region=Delhi | Bar chart shows only Delhi bar | High | Not Run
TC-F-04: Year slider filters data to 2022 | US-04 | BR-11 | UI-01 | App running | Slide year to 2022 | year=2022 | KPIs and charts show 2022 data only | High | Not Run
TC-F-05: Trends page shows monthly line chart | US-08 | BR-06 | UI-02 | Trends page open | Load page | disease=COVID-19, year=2021 | Line chart with 12 monthly points visible | High | Not Run
TC-F-06: YoY table shows correct increase for COVID-19 2021 | US-10 | BR-09 | UI-02 | Trends page | Load YoY table | disease=COVID-19 | 2021 shows positive YoY% vs 2020 | High | Not Run
TC-F-07: Seasonal heatmap loads with 12 columns | US-11 | BR-06 | UI-02 | Trends page | Load heatmap | All diseases | Heatmap: rows=diseases, cols=months (12) | Medium | Not Run
TC-F-08: Regional analysis shows 10 regions in bar chart | US-12 | BR-02 | UI-03 | Regional page open | Load bar chart | All regions | 10 horizontal bars visible | High | Not Run
TC-F-09: CFR table displays value between 0 and 100 | US-07 | BR-03 | UI-03 | Regional page | Load CFR heatmap | disease=Dengue | All CFR% values between 0 and 100 | High | Not Run
TC-F-10: Demographics page stacked bar has age groups | US-13 | BR-04 | UI-04 | Demographics page | Select disease=Malaria | age filter All | Stacked bar shows 5 age group segments | High | Not Run
TC-F-11: Gender filter shows Female-only data | US-13 | BR-04 | UI-04 | Demographics page | Select gender=Female | gender=Female | Only Female demographic data shown | Medium | Not Run
TC-F-12: Correlation scatter shows Pearson r value | US-14 | BR-08 | UI-05 | EDA page | Load scatter plot | disease=Dengue | Chart visible with r= value in annotation | Medium | Not Run
TC-F-13: Co-occurrence detector flags concurrent outbreak | US-15 | BR-05 | UI-05 | EDA page | Load co-occurrence section | 2021 monsoon months | Table shows regions with 2+ concurrent diseases | High | Not Run
TC-F-14: CSV download produces non-empty file | US-16 | BR-12 | UI-01..05 | Any analysis page | Click Download CSV | Current filter | File downloads, opens in Excel, has headers + data | Medium | Not Run
TC-F-15: Data quality page shows before/after stats | US-17 | BR-13 | UI-06 | Data quality page | Load page | None | Table shows original row count, duplicates removed, NaN filled | Medium | Not Run
TC-F-16: Empty result state handled gracefully | US-04 | BR-11 | UI-01 | App running | Select non-existent combo | disease+region+year with 0 cases | App shows "No data available" message, no crash | High | Not Run
TC-F-17: Navigation between pages works | US-04..17 | BR-01 | All | App running | Click each page in sidebar | None | Each page loads without error | High | Not Run
TC-F-18: Filters persist across page navigation | US-03 | BR-11 | All | App running, Dengue selected | Switch from Overview to Trends | disease=Dengue | Trends page also shows Dengue data | High | Not Run
TC-F-19: Recovery rate never exceeds 100% | US-07 | BR-07 | UI-03 | Regional page | Load recovery chart | All data | No bar or cell shows > 100% | High | Not Run
TC-F-20: Mobile/narrow view: sidebar collapses cleanly | US-03 | BR-11 | All | Narrow browser window (600px) | Load app | None | Sidebar collapses, main content visible | Low | Not Run

SECTION B: Technical Test Cases (TC-T-01..TC-T-15)
Table: TC ID | Module/Function | Check | Test Data | Expected | Priority

TC-T-01: test_data.py | load_data() | Returns non-empty DataFrame | app.db | df.shape[0] > 0 | High
TC-T-02: test_data.py | load_data() | Correct column count | app.db | >= 12 columns | High
TC-T-03: test_data.py | disease_cases table | disease_id FK valid | app.db | No orphan disease_ids | High
TC-T-04: test_data.py | disease_cases table | region_id FK valid | app.db | No orphan region_ids | High
TC-T-05: test_data.py | disease_cases table | cases_reported >= 0 | app.db | Min >= 0 | High
TC-T-06: test_data.py | disease_cases table | deaths <= cases_reported | app.db | All rows satisfy constraint | High
TC-T-07: test_data.py | disease_master table | Unique disease names | app.db | No duplicates | Medium
TC-T-08: test_data.py | disease_cases | No exact duplicate rows after cleaning | cleaned df | 0 duplicates | High
TC-T-09: test_analysis.py | compute_cfr() | Known input | cases=100, deaths=5 | Returns 5.0 | High
TC-T-10: test_analysis.py | compute_recovery_rate() | Known input | cases=100, recovered=90 | Returns 90.0 | High
TC-T-11: test_analysis.py | compute_yoy_change() | Known input | 2021=200, 2020=100 | Returns 100.0 | High
TC-T-12: test_analysis.py | compute_incidence_rate() | Known input | cases=1000, population=1000000 | Returns 100.0 | Medium
TC-T-13: test_analysis.py | detect_concurrent_outbreaks() | Flags correctly | 2 diseases > threshold in same region-month | Returns flag=1 | High
TC-T-14: test_analysis.py | pearson_correlation() | Known data | x=[1,2,3,4,5], y=[2,4,6,8,10] | r ≈ 1.0 | Medium
TC-T-15: test_data.py | load_data() | Loads within 3 seconds | app.db | time.time() delta < 3.0 | High

SECTION C: Test Coverage Summary
Table: BR ID | TC-F IDs | TC-T IDs | Covered?
Every BR must have at least 1 test.

Now also write the pytest content:

FILE: c:\\Users\\Hp\\Downloads\\hcl\\tests\\test_data.py
Write the complete pytest file for TC-T-01 through TC-T-08 and TC-T-15.
Import from src.data_loader (functions may not exist yet, so use try/except with @pytest.mark.xfail or placeholder)
Test the SQLite DB at data/app.db

FILE: c:\\Users\\Hp\\Downloads\\hcl\\tests\\test_analysis.py
Write complete pytest file for TC-T-09 through TC-T-14.
Test analysis functions with known inputs.

Output the Word script first (complete, runnable python-docx script).
Then output test_data.py content.
Then output test_analysis.py content.
Label each section clearly.
Use triple-quoted strings. No syntax errors.
""",
    schema={"type": "string"},
    role="Step 13 – Test Cases Writer"
)
log(f"Step 13 returned {len(step13_result)} chars")
write13 = await call_tool("write_file",
    Path=r"c:\Users\Hp\Downloads\hcl\docs\gen_step13_raw.txt",
    Content=step13_result
)

phase("Step 13 – Execute Scripts")
exec13_agent = agent("""You are a Python execution expert and QA engineer.
From the raw output, extract THREE separate pieces:
1. The python-docx Word document script - save to c:\\Users\\Hp\\Downloads\\hcl\\docs\\gen_step13.py and run it
2. The test_data.py content - save to c:\\Users\\Hp\\Downloads\\hcl\\tests\\test_data.py
3. The test_analysis.py content - save to c:\\Users\\Hp\\Downloads\\hcl\\tests\\test_analysis.py
Also create c:\\Users\\Hp\\Downloads\\hcl\\tests\\__init__.py (empty file)
Report each file saved.""",
role="Step 13 Executor")
step13_raw = open(r"c:\Users\Hp\Downloads\hcl\docs\gen_step13_raw.txt").read()
exec13 = await exec13_agent(
    f"Extract all three files and run the Word script:\n\n{step13_raw[:10000]}",
    {"type": "string"}
)
log(f"Step 13 execution: {exec13[:300]}")
del exec13_agent

phase("Step 14 – Build Plan")
log("Generating Build Plan document (Step 14)...")

step14_result = await agent(
    prompt=f"""
{PROJECT_CTX}
{BR_CONTENT}
User Stories: US-01..US-17
UI Screens: UI-01..UI-06
FR-01..FR-15 from TRD
Folder structure as defined in TRD Step 7
requirements.txt: streamlit==1.35.0, pandas==2.2.2, numpy==1.26.4, plotly==5.22.0, scipy==1.13.0, statsmodels==0.14.2, openpyxl==3.1.2, pytest==8.2.0, pytest-cov==5.0.0

You are a Tech Lead. Generate STEP 14 – Build Plan.

PART A: Write a complete Python script using python-docx to create the Build Plan Word document.
Save to: c:\\Users\\Hp\\Downloads\\hcl\\docs\\14_ArgJain_DiseaseTrendAnalysis_BuildPlan.docx

PART B: Write BUILD_PLAN.md content (output separately after the docx script).
Save to: c:\\Users\\Hp\\Downloads\\hcl\\BUILD_PLAN.md

WORD DOCUMENT MUST CONTAIN:

COVER BLOCK: same meta, subtitle 'STEP 14 – Build Plan'

SECTION 1: Project Summary (10 lines)
Disease Trend Analysis app summary covering: purpose, users, tech stack, data, key features,
deployment target, test approach, success criteria.
Links row: "Documents in docs/ folder: Steps 01-13 Word/Excel files"

SECTION 2: Final Folder Structure
Exact folder tree with all files listed

SECTION 3: Build Tasks (the main section)
Table for each BUILD task: BUILD ID | Goal | Files | US IDs | Feature IDs | AI Prompt Summary | Verification Check | Tests That Must Pass

BUILD-01: Setup and project structure | requirements.txt, .gitignore, .streamlit/config.toml, app.py stub | US-01 | - | pip install -r requirements.txt | pip list shows all packages | None
BUILD-02: SQLite loader and cache | src/data_loader.py | US-01 | FR-01 | Write load_data() with @st.cache_data | python -c "from src.data_loader import load_data; df=load_data(); print(df.shape)" | TC-T-01, TC-T-02, TC-T-15
BUILD-03: Data cleaning pipeline | src/cleaning.py | US-02 | FR-01 | Write clean_data() with duplicate removal, NaN imputation, outlier capping | python -c "from src.cleaning import clean_data" | TC-T-08
BUILD-04: Session state filter setup | app.py, src/ui.py | US-03 | FR-02 | Write sidebar filters using st.session_state | streamlit run app.py - filters visible | TC-F-17, TC-F-18
BUILD-05: Analysis functions | src/analysis.py | US-07,09,10 | FR-03..FR-11 | Write all 9 analysis functions (CFR, recovery, YoY, seasonal, correlation, co-occurrence) | pytest tests/test_analysis.py -v | TC-T-09..TC-T-14
BUILD-06: Tailwind UI components | src/ui.py | US-04 | - | Write inject_tailwind(), render_kpi_card(), render_header() | streamlit run app.py - header visible | None
BUILD-07: Overview page (UI-01) | pages/01_Overview.py | US-04,05,06,07 | FR-12 | Write Overview page with 4 KPI cards and regional bar chart | Manual: 4 KPIs visible | TC-F-01..TC-F-04
BUILD-08: Trends page (UI-02) | pages/02_Trends.py | US-08,09,10,11 | FR-03,FR-08,FR-11 | Write Trends page with line chart, YoY chart, seasonal heatmap | Manual: 3 charts visible | TC-F-05..TC-F-07
BUILD-09: Regional analysis page (UI-03) | pages/03_Regional_Analysis.py | US-12 | FR-04,FR-05 | Write Regional page with horizontal bar and CFR heatmap | Manual: 10-region bar chart visible | TC-F-08,TC-F-09
BUILD-10: Demographics page (UI-04) | pages/04_Demographics.py | US-13 | FR-06 | Write Demographics page with stacked bar by age group | Manual: stacked bar with 5 segments | TC-F-10,TC-F-11
BUILD-11: EDA and Insights page (UI-05) | pages/05_EDA_Statistics.py | US-14,15 | FR-07,FR-10 | Write EDA page with scatter plot and co-occurrence table | Manual: scatter with r=, table visible | TC-F-12,TC-F-13
BUILD-12: Data quality page (UI-06) | pages/06_Data_Quality.py | US-16,17 | FR-14,FR-15 | Write Data Quality page with before/after stats and CSV download | Manual: stats table and download button | TC-F-14,TC-F-15
BUILD-13: Run all tests and fix failures | tests/ | US-01..17 | All FRs | pytest -q --cov=src tests/ | pytest report: 0 failures, >= 80% coverage | All TC-T-01..TC-T-15
BUILD-14: README and final checks | README.md | - | - | Write README with setup, run, deploy instructions | README.md renders on GitHub | None

SECTION 4: Definition of Done
Checklist (10 items):
- All 15 Must BRs demonstrable in live app
- All 10 OQs answerable in mentor walkthrough
- pytest coverage >= 80% with 0 critical failures
- App deployed at Streamlit Community Cloud URL
- All 6 pages load without errors
- Sidebar filters update all charts < 3 seconds
- CSV download works on all pages
- Data Quality page shows before/after cleaning stats
- README.md complete with setup and deploy instructions
- All 18-step documents complete in docs/ folder

SECTION 5: Commands Reference
Install: cd project-root && python -m venv .venv && .venv\\Scripts\\activate && pip install -r requirements.txt
Run app: streamlit run app.py
Run tests: pytest -q --cov=src tests/
Run data gen: python src/generate_data.py
Deploy: git push origin main (Streamlit Cloud auto-deploys)

SECTION 6: Viva Q&A Notes
Table: Question | Short Answer (2-3 lines)
10 likely viva questions with concise answers about the project design, data, analysis, testing.

BUILD_PLAN.md must be a clean Markdown file with:
# Disease Trend Analysis – Build Plan
## Project: P-01 | Student: Arg Jain | Roll: 2500320140031
Then all 14 BUILD tasks in Markdown format with checkboxes:
- [ ] BUILD-01: ...
etc.

Output the Word script first (complete, runnable). Then BUILD_PLAN.md content.
Label each section. Triple-quoted strings. No syntax errors.
""",
    schema={"type": "string"},
    role="Step 14 – Build Plan Writer"
)
log(f"Step 14 returned {len(step14_result)} chars")
write14 = await call_tool("write_file",
    Path=r"c:\Users\Hp\Downloads\hcl\docs\gen_step14_raw.txt",
    Content=step14_result
)

phase("Step 14 – Execute Scripts")
exec14_agent = agent("""Python execution expert: 
1. Extract the python-docx script, save to c:\\Users\\Hp\\Downloads\\hcl\\docs\\gen_step14.py and run it
2. Extract the BUILD_PLAN.md content, save to c:\\Users\\Hp\\Downloads\\hcl\\BUILD_PLAN.md
Report both files saved.""",
role="Step 14 Executor")
step14_raw = open(r"c:\Users\Hp\Downloads\hcl\docs\gen_step14_raw.txt").read()
exec14 = await exec14_agent(
    f"Extract and run:\n\n{step14_raw[:9000]}",
    {"type": "string"}
)
log(f"Step 14 execution: {exec14[:300]}")
del exec14_agent

phase("Step 15 – Build App Code")
log("Building complete Streamlit application (Step 15)...")

step15_result = await agent(
    prompt=f"""
{PROJECT_CTX}
requirements.txt: streamlit==1.35.0, pandas==2.2.2, numpy==1.26.4, plotly==5.22.0, scipy==1.13.0, statsmodels==0.14.2, openpyxl==3.1.2, pytest==8.2.0, pytest-cov==5.0.0

You are a senior Python developer. Build the complete Disease Trend Analysis Streamlit app.

Write ALL the following files (output each as a clearly labelled code block):

FILE 1: requirements.txt
(pinned versions as listed above, one per line)

FILE 2: .streamlit/config.toml
[theme]
primaryColor = "#1A5376"
backgroundColor = "#F0F8FF"
secondaryBackgroundColor = "#E8F4FD"
textColor = "#2C3E50"
font = "sans serif"

FILE 3: src/__init__.py
(empty)

FILE 4: src/data_loader.py
Write load_data() that:
- Connects to data/app.db using sqlite3
- Loads disease_cases joined with disease_master, region_master
- Returns a pandas DataFrame with columns: case_id, disease_name, region_name, 
  state_code, zone, population, area_sqkm, population_density,
  report_date, report_year, report_month, cases_reported, deaths, 
  recovered, active_cases, hospitalized, is_outbreak, data_source
- Uses @st.cache_data(ttl=3600)
- Has try/except for DB errors
- Uses Path(__file__).parent.parent / "data" / "app.db" for path

FILE 5: src/cleaning.py
Write clean_data(df) that:
- Removes exact duplicates
- Imputes missing cases_reported with column median
- Imputes missing deaths with 0
- Caps outliers at Q3 + 3*IQR for cases_reported
- Returns (cleaned_df, quality_report_dict) where quality_report_dict has:
  original_rows, duplicates_removed, nulls_filled, outliers_capped, final_rows

FILE 6: src/analysis.py
Write these functions (each with docstring):
- compute_cfr(df) → df with cfr_pct column (deaths/cases*100, handle div/0)
- compute_recovery_rate(df) → df with recovery_rate_pct column
- compute_yoy_change(df) → pivot: disease as rows, years as cols, YoY% values
- compute_seasonal_trend(df) → pivot: month as rows, disease as cols, avg cases
- compute_incidence_rate(df) → df with incidence_per_lakh column (cases/population*100000)
- detect_concurrent_outbreaks(df) → df of region-months where 2+ diseases > their mean
- pearson_correlation(df) → returns (r, p_value) for incidence_per_lakh vs population_density
- compute_regional_summary(df) → grouped df: region × disease with total cases, CFR, recovery

FILE 7: src/ui.py
Write these functions:
- inject_tailwind() → st.components.v1.html with Tailwind CDN script tag, height=0
- render_header(title, subtitle="") → st.components.v1.html with Tailwind-styled header
- render_kpi_card(label, value, delta=None, icon="📊", color="#1A5376") → HTML KPI card string
- render_insight_box(text) → st.components.v1.html with styled insight box

FILE 8: app.py (main entry point)
- Page config: title="Disease Trend Analysis", page_icon="🏥", layout="wide"
- inject_tailwind() call
- render_header("Disease Trend Analysis", "Healthcare Analytics Dashboard")
- Load data with load_data(), clean with clean_data()
- Sidebar with all 5 filters (disease, region, year, age, gender) using st.session_state
- Welcome message and navigation hint
- Display 4 KPI cards on home page (Total Cases, Deaths, Recoveries, CFR%)

FILE 9: pages/01_Overview.py
Complete page with:
- KPI cards (4): Total Cases, Deaths, Recoveries, Active CFR%
- Bar chart: Cases by Region (px.bar, horizontal, top 10)
- CFR heatmap table: disease vs region (px.imshow)
- Filter application from st.session_state

FILE 10: pages/02_Trends.py
Complete page with:
- Monthly time-series line chart (px.line, disease as color, month on x)
- Year-over-year comparison chart (px.line with year as color)
- Seasonal heatmap (px.imshow: months as x, diseases as y, avg cases as z)
- YoY change table (styled DataFrame)

FILE 11: pages/03_Regional_Analysis.py
Complete page with:
- Horizontal bar chart: Total cases by region
- CFR% bar chart by region
- Recovery rate comparison chart

FILE 12: pages/04_Demographics.py
Complete page with:
- Stacked bar chart by age group (px.bar barmode=stack)
- Pie chart: gender distribution
- Note: uses demographic_breakdown table if available, else uses disease_cases

FILE 13: pages/05_EDA_Statistics.py
Complete page with:
- Scatter plot: incidence rate vs population density with trendline (px.scatter, trendline='ols')
- Pearson r and p-value displayed
- Concurrent outbreak detection table
- Descriptive statistics table (df.describe())

FILE 14: pages/06_Data_Quality.py
Complete page with:
- Data quality report table (before/after cleaning)
- Outliers section
- CSV download button for full cleaned dataset

FILE 15: tests/__init__.py (empty)

FILE 16: tests/test_app.py
Basic Streamlit AppTest tests:
- test_app_starts() - app.py loads without exception
- test_overview_page() - 01_Overview.py loads

Save all files to the correct paths under c:\\Users\\Hp\\Downloads\\hcl\\

Output each file clearly labelled as:
=== FILE: <path> ===
<complete file content>
=== END FILE ===

Make sure all code is complete and runnable. Use Plotly Express (px). Handle edge cases (empty dataframes).
""",
    schema={"type": "string"},
    role="Step 15 – App Builder"
)
log(f"Step 15 app code returned {len(step15_result)} chars")
write15 = await call_tool("write_file",
    Path=r"c:\Users\Hp\Downloads\hcl\docs\gen_step15_raw.txt",
    Content=step15_result
)

phase("Step 15 – Save App Files")
exec15_agent = agent("""You are a Python file management expert. 
Parse the raw output which contains multiple files labelled as:
=== FILE: <path> ===
<content>
=== END FILE ===

For each file found:
1. Create the directory if needed
2. Save the file to its exact path under c:\\Users\\Hp\\Downloads\\hcl\\
3. Report each file saved

After saving all files, run:
cd c:\\Users\\Hp\\Downloads\\hcl && python -c "import sys; sys.path.insert(0, '.'); from src.data_loader import load_data; print('data_loader OK')"

Then try: cd c:\\Users\\Hp\\Downloads\\hcl && python -m pytest tests/ -q --tb=short 2>&1 | head -50

Report all results.""",
role="Step 15 File Saver")
step15_raw = open(r"c:\Users\Hp\Downloads\hcl\docs\gen_step15_raw.txt").read()
exec15 = await exec15_agent(
    f"Parse and save all files, then test:\n\n{step15_raw[:12000]}",
    {"type": "string"}
)
log(f"Step 15 file saving: {exec15[:500]}")
del exec15_agent

phase("Step 16 – Deployment Guide")
log("Generating Deployment Guide (Step 16)...")

step16_result = await agent(
    prompt=f"""
{PROJECT_CTX}

You are a DevOps engineer. Generate STEP 16 – Deployment Guide.

Write a complete Python script using python-docx (v1.2.0).
Save to: c:\\Users\\Hp\\Downloads\\hcl\\docs\\16_ArgJain_DiseaseTrendAnalysis_DeploymentGuide.docx

The document must contain:

COVER BLOCK: same meta, subtitle 'STEP 16 – Deployment Guide: Streamlit Community Cloud'

SECTION 1: Pre-Deployment Checklist
Table: Check ID | Item | Expected | Verified?
CHK-01: app.py at root | app.py exists in repo root | Yes
CHK-02: requirements.txt at root | Pinned versions, no conflicts | Yes
CHK-03: data/app.db committed | SQLite file in data/ folder | Yes
CHK-04: Relative paths | Path(__file__).parent used | Yes
CHK-05: No secrets in code | No API keys, passwords | Yes
CHK-06: .gitignore correct | .venv/, __pycache__/, *.pyc excluded | Yes
CHK-07: All pages in pages/ | 6 page files present | Yes
CHK-08: pytest passes | 0 critical failures | Yes
CHK-09: App runs locally | streamlit run app.py works | Yes
CHK-10: GitHub repo pushed | git push origin main done | Yes

SECTION 2: GitHub Repository Setup
Step-by-step numbered instructions:
1. Create GitHub repo named: 2500320140031-disease-trend-analysis
2. git init (if not done)
3. git remote add origin https://github.com/<username>/2500320140031-disease-trend-analysis.git
4. git add .
5. git commit -m "Initial: Disease Trend Analysis app - Arg Jain"
6. git push -u origin main
Troubleshooting box: If git push fails (file too large), show: git lfs install, git lfs track "data/app.db"

SECTION 3: Streamlit Community Cloud Deployment
Step-by-step numbered instructions with screenshots description:
1. Go to share.streamlit.io and sign in with GitHub
2. Click "Create app" button (top right)
3. Fill form: Repository = 2500320140031-disease-trend-analysis, Branch = main, Main file path = app.py
4. App URL: 2500320140031-disease-trend-analysis.streamlit.app (or similar)
5. Click Deploy - wait 2-5 minutes
6. Watch deployment log - look for "You can now view your Streamlit app in your browser"
7. Share the URL with mentor

SECTION 4: Common Deployment Failures and Fixes
Table: Error | Cause | Fix
ModuleNotFoundError: | Package missing from requirements.txt | Add package with pinned version
"No module named 'src'" | Relative import issue | Add src/__init__.py; use sys.path
app.db not found | Relative path issue | Use Path(__file__).parent.parent/"data"/"app.db"
MemoryError | Dataset too large | Reduce rows in generate_data.py; use sampling
Slow startup | No caching | Add @st.cache_data to all data functions

SECTION 5: Post-Deployment Verification
Checklist after deployment:
- Open URL: app loads in < 5 seconds
- All 6 pages accessible from sidebar
- Filters work and update charts
- CSV download works
- Data Quality page shows stats
- Share URL: copy from browser address bar

SECTION 6: Maintenance
- To update: edit code → git add . → git commit → git push → Streamlit Cloud auto-redeploys
- To view logs: Streamlit Cloud dashboard → App → Logs tab
- Free tier limits: 1 GB RAM, 1 CPU, app sleeps after 7 days inactivity (re-wakes on visit)

FOOTER: file name, version, date, institute.
STYLING: Same professional style.
Output ONLY the complete Python script. Triple-quoted strings. No syntax errors.
""",
    schema={"type": "string"},
    role="Step 16 – Deployment Guide Writer"
)
log(f"Step 16 returned {len(step16_result)} chars")
write16 = await call_tool("write_file",
    Path=r"c:\Users\Hp\Downloads\hcl\docs\gen_step16_raw.txt",
    Content=step16_result
)

phase("Step 16 – Execute Script")
exec16_agent = agent("Python execution expert: extract, fix, save and run python-docx scripts.",
role="Step 16 Executor")
step16_raw = open(r"c:\Users\Hp\Downloads\hcl\docs\gen_step16_raw.txt").read()
exec16 = await exec16_agent(
    f"Extract, fix, save to c:\\Users\\Hp\\Downloads\\hcl\\docs\\gen_step16.py and run:\n\n{step16_raw[:8000]}",
    {"type": "string"}
)
log(f"Step 16 execution: {exec16[:300]}")
del exec16_agent

phase("Steps 17 & 18 – Final Documents")
log("Generating Project Document (Step 17) and Presentation guide (Step 18)...")

steps1718 = await parallel(
    ['step17', 'step18'],
    lambda step: agent(
        prompt=f"""
{PROJECT_CTX}
{BR_CONTENT}

{'You are a Technical Writer. Generate STEP 17 – Project Document (ABES format).' if step == 'step17' else 'You are a Presentation Designer. Generate STEP 18 – Presentation outline.'}

Write a complete Python script using python-docx (v1.2.0).
Save to: c:\\Users\\Hp\\Downloads\\hcl\\docs\\{'17_ArgJain_DiseaseTrendAnalysis_ProjectDocument.docx' if step == 'step17' else '18_ArgJain_DiseaseTrendAnalysis_Presentation_Script.docx'}

{'The ABES Project Document must contain ALL 18 step summaries with cross-references. Include: Cover page (project title, student, roll, mentor, institute, date, GitHub URL placeholder, Streamlit URL placeholder), Table of Contents, then sections 1-18 each with a 1-page summary of that step. Use same professional styling. Add RACI table, traceability summary (3-4 RTM rows showing end-to-end trace), and Appendix A: Assumptions, Appendix B: AI Tools Used (mention AI-assisted document drafting, human-verified content, Streamlit app coded with AI suggestions). Keep document professional and academically formatted.' if step == 'step17' else '''The presentation script document should contain:
COVER BLOCK: Slide-by-Slide Speaker Script

For each of 11 slides, provide:
SLIDE NUMBER and TITLE
CONTENT (max 6 bullet points per slide, what appears on screen)
SPEAKER NOTES (what to say aloud, ~30 seconds worth)

Slide 1 - Title Slide: Disease Trend Analysis | Arg Jain | Roll 2500320140031 | Ms. Kalpana Dwivedi | ABES Engineering College | November 2026 | "P-01 Disease Trend Analysis"
Slide 2 - Problem + Top 2 HMW: Problem statement 1 line + HMW-01 and HMW-03 (top priority ones)
Slide 3 - Stakeholders (top 3): SH-01, SH-02, SH-03 with influence and key decision
Slide 4 - Traceability: 4 RTM rows showing HMW→BR→US→TC→UI chain
Slide 5 - Data: 3000 rows, 15 columns, Jan 2020-Dec 2024, 5 diseases, 10 states; 3 quality fixes: duplicates removed, NaN imputed, outliers capped
Slide 6 - Solution + Tech Flow: Python→SQLite→Streamlit→Plotly; 6 pages; Tailwind UI
Slide 7 - Dashboard Screenshots: Describe UI-01 KPI cards + UI-02 trend chart (actual screenshots to be inserted)
Slide 8 - Key Findings: 3 numbers with evidence (e.g. COVID-19 saw 300% spike in 2021 vs 2020, Dengue peaks 2.5x in monsoon months, Delhi CFR 3.2% vs 1.8% national avg)
Slide 9 - Testing: 15 pytest tests + 20 manual TC-F; show 3 key test rows; coverage 80%+
Slide 10 - Recommendations, Limitations, Next Steps
Slide 11 - Live Demo: App URL + GitHub URL + QR code placeholder

Also include: Preparation checklist (5 items), 5-minute timing guide per slide.'''}

STYLING: Professional ABES format. Same color scheme.
Output ONLY the complete Python script. Triple-quoted strings. No syntax errors.
""",
        schema={"type": "string"},
        role=f"{'Step 17' if step == 'step17' else 'Step 18'} Writer"
    )
)
step17_result, step18_result = steps1718
log(f"Step 17 returned {len(step17_result)} chars, Step 18 returned {len(step18_result)} chars")

write17 = await call_tool("write_file",
    Path=r"c:\Users\Hp\Downloads\hcl\docs\gen_step17_raw.txt",
    Content=step17_result
)
write18 = await call_tool("write_file",
    Path=r"c:\Users\Hp\Downloads\hcl\docs\gen_step18_raw.txt",
    Content=step18_result
)

phase("Steps 17 & 18 – Execute Scripts")
execs1718 = await parallel(
    [('17', r'c:\Users\Hp\Downloads\hcl\docs\gen_step17_raw.txt', r'c:\Users\Hp\Downloads\hcl\docs\gen_step17.py'),
     ('18', r'c:\Users\Hp\Downloads\hcl\docs\gen_step18_raw.txt', r'c:\Users\Hp\Downloads\hcl\docs\gen_step18.py')],
    lambda item: agent(
        f"Python execution expert: read file at {item[1]}, extract python-docx script, fix syntax, save to {item[2]} and run it. Report SAVED or errors.",
        schema={"type": "string"},
        role=f"Step {item[0]} Executor"
    )
)
log(f"Step 17 exec: {execs1718[0][:200]}")
log(f"Step 18 exec: {execs1718[1][:200]}")

phase("Final Summary")
log("All steps executed. Generating file inventory...")

inventory_check = await call_tool("run_command",
    CommandLine=r"Get-ChildItem c:\Users\Hp\Downloads\hcl\docs\ | Select-Object Name, Length, LastWriteTime | Format-Table -AutoSize",
    WaitMsBeforeAsync=10000,
    toolSummary="List generated documents"
)
log(f"File inventory: {str(inventory_check)[:1000]}")

data_check = await call_tool("run_command",
    CommandLine=r"Get-ChildItem c:\Users\Hp\Downloads\hcl\data\ -ErrorAction SilentlyContinue | Select-Object Name, Length | Format-Table -AutoSize",
    WaitMsBeforeAsync=10000,
    toolSummary="List data files"
)
log(f"Data files: {str(data_check)[:500]}")

src_check = await call_tool("run_command",
    CommandLine=r"Get-ChildItem c:\Users\Hp\Downloads\hcl\src\ -ErrorAction SilentlyContinue | Select-Object Name | Format-Table -AutoSize",
    WaitMsBeforeAsync=10000,
    toolSummary="List source files"
)
log(f"Source files: {str(src_check)[:500]}")

print("WORKFLOW COMPLETE")
print("All steps 2-18 (excluding 6) have been executed.")
print("Check docs/ for Word and Excel files.")
print("Check src/ for Python source files.")
print("Check data/ for SQLite database and CSV files.")
