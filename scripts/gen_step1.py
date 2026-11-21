
from docx import Document
from docx.shared import Pt, RGBColor, Inches, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import os

os.makedirs(r'c:\Users\Hp\Downloads\hcl\docs', exist_ok=True)

doc = Document()

# --- Page margins ---
for section in doc.sections:
    section.top_margin    = Cm(2.5)
    section.bottom_margin = Cm(2.5)
    section.left_margin   = Cm(3)
    section.right_margin  = Cm(2)

def set_col_widths(table, widths):
    for row in table.rows:
        for i, cell in enumerate(row.cells):
            if i < len(widths):
                cell.width = widths[i]

def shade_cell(cell, fill_hex):
    tc   = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd  = OxmlElement('w:shd')
    shd.set(qn('w:val'),   'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'),  fill_hex)
    tcPr.append(shd)

def add_heading(doc, text, level=1):
    h = doc.add_heading(text, level=level)
    h.alignment = WD_ALIGN_PARAGRAPH.LEFT
    for run in h.runs:
        run.font.color.rgb = RGBColor(0x1A, 0x53, 0x76)
    return h

def header_row(table, cols):
    row = table.rows[0]
    for i, col in enumerate(cols):
        if i < len(row.cells):
            cell = row.cells[i]
            shade_cell(cell, '1A5376')
            p = cell.paragraphs[0]
            run = p.add_run(col)
            run.font.bold  = True
            run.font.color.rgb = RGBColor(0xFF,0xFF,0xFF)
            run.font.size  = Pt(9)
            p.alignment    = WD_ALIGN_PARAGRAPH.CENTER

def add_table(doc, headers, rows, col_widths=None):
    t = doc.add_table(rows=1+len(rows), cols=len(headers))
    t.style = 'Table Grid'
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    header_row(t, headers)
    for ri, row_data in enumerate(rows):
        tr = t.rows[ri+1]
        fill = 'EBF5FB' if ri % 2 == 0 else 'FFFFFF'
        for ci, val in enumerate(row_data):
            if ci < len(tr.cells):
                cell = tr.cells[ci]
                shade_cell(cell, fill)
                p = cell.paragraphs[0]
                run = p.add_run(str(val))
                run.font.size = Pt(8.5)
    if col_widths:
        set_col_widths(t, col_widths)
    doc.add_paragraph()
    return t

# ═══════════════════════════════════════════════
# COVER BLOCK
# ═══════════════════════════════════════════════
title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = title.add_run('DISEASE TREND ANALYSIS')
run.font.bold = True
run.font.size = Pt(18)
run.font.color.rgb = RGBColor(0x1A,0x53,0x76)

sub = doc.add_paragraph()
sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
run2 = sub.add_run('STEP 1 — Project Understanding Document')
run2.font.size = Pt(13)
run2.font.bold = True
run2.font.color.rgb = RGBColor(0x21,0x8E,0xBE)

doc.add_paragraph()

meta_data = [
    ('Project ID',       'P100'),
    ('Project Title',    'Disease Trend Analysis'),
    ('Domain',           'Healthcare Data Analytics'),
    ('Student Name',     'Arg Jain'),
    ('Roll Number',      '2500320140031'),
    ('Course',           'MCA 2nd Year — Data Analytics'),
    ('Institute',        'ABES Engineering College, Ghaziabad'),
    ('Mentor',           'Mr. Dinesh'),
    ('Document Version', 'v1.0'),
    ('Date',             'November 2026'),
]
t = doc.add_table(rows=len(meta_data), cols=2)
t.style = 'Table Grid'
for i,(k,v) in enumerate(meta_data):
    r = t.rows[i]
    c0 = r.cells[0]
    shade_cell(c0, 'D6EAF8')
    rn = c0.paragraphs[0].add_run(k)
    rn.font.bold = True
    rn.font.size = Pt(9)
    c1 = r.cells[1]
    c1.paragraphs[0].add_run(v).font.size = Pt(9)
set_col_widths(t, [Cm(5), Cm(10)])
doc.add_paragraph()
doc.add_page_break()

# ═══════════════════════════════════════════════
# 1. PROBLEM DESCRIPTION & PROBLEM STATEMENT
# ═══════════════════════════════════════════════
add_heading(doc, '1. Problem Description & Problem Statement', 1)

# 1.1 Context & Background
add_heading(doc, '1.1 Epidemiological Context & Background in India', 2)
p_bg1 = doc.add_paragraph(
    'India presents one of the most complex public health landscapes globally, characterized by vast geographic, '
    'climatic, and demographic diversity across its 28 states and 8 union territories. The country continuously '
    'battles a dual burden of endemic communicable diseases. Vector-borne illnesses like Dengue and Malaria exhibit '
    'extreme seasonal transmission surges coinciding with the southwest monsoon (July to October). Simultaneously, '
    'chronic and airborne infections such as Tuberculosis and respiratory viruses like COVID-19 exert an unrelenting '
    'strain on critical care infrastructure, particularly within densely populated urban epicenters.'
)
p_bg1.runs[0].font.size = Pt(10)

p_bg2 = doc.add_paragraph(
    'Furthermore, water-borne enteric infections such as Typhoid repeatedly challenge municipal sanitation networks, '
    'causing localized flare-ups that overlap with mosquito breeding cycles. Despite the collection of extensive health '
    'records by district surveillance units, public health analysts and administrative decision-makers struggle to '
    'extract actionable insights in real time due to fragmented data storage, static tabular reporting formats, and lack of '
    'integrated multi-dimensional analytics.'
)
p_bg2.runs[0].font.size = Pt(10)

# 1.2 Formal Problem Statement
add_heading(doc, '1.2 Formal Problem Statement', 2)
p_ps = doc.add_paragraph()
r_ps_lbl = p_ps.add_run('Formal Problem Statement: ')
r_ps_lbl.bold = True
r_ps_lbl.font.color.rgb = RGBColor(0x0F, 0x2B, 0x48)
r_ps = p_ps.add_run(
    'Healthcare authorities, district epidemiologists, hospital administrators, and state policy makers in India '
    'lack a unified, interactive, and multi-dimensional visual analytics platform to monitor disease occurrence trends, '
    'fatality severity, clinical recovery rates, and demographic risk profiles across states and longitudinal timelines. '
    'This analytical deficit directly results in delayed outbreak signal detection (by 2 to 4 weeks), reactive rather '
    'than predictive medical supply allocation, unmitigated mortality spikes, and suboptimal execution of preventive public health interventions.'
)
r_ps.font.size = Pt(10)
r_ps.font.italic = True
r_ps.font.color.rgb = RGBColor(0x1A, 0x53, 0x76)

# 1.3 Key Operational Deficiencies & Pain Points
add_heading(doc, '1.3 Key Operational Challenges & Deficiencies', 2)
p_def = doc.add_paragraph(
    'Comprehensive stakeholder consultations and domain analysis reveal five critical deficiencies in existing '
    'public health data workflows:'
)
p_def.runs[0].font.size = Pt(10)

prob_headers = ['Deficiency ID', 'Core Challenge & Operational Defect', 'Public Health Impact', 'Severity']
prob_rows = [
    ('DEF-01',
     'Data Siloing & Tabular Reporting\nHealth data is stored across disconnected spreadsheets and static monthly PDF registers without relational schema linkages.',
     'Inability to perform cross-state or cross-disease comparative analysis; high latency in publishing surveillance summaries.',
     'High'),
    ('DEF-02',
     'Delayed Outbreak Signal Detection\nSurveillance teams rely on retrospective monthly roll-ups rather than continuous trend anomaly and rolling-average tracking.',
     'Outbreak containment protocols are initiated 2–4 weeks late, allowing localized disease clusters to escalate into statewide epidemics.',
     'Critical'),
    ('DEF-03',
     'Demographic & Risk Group Blindspots\nMorbidity counts are reported as aggregate state totals without simultaneous cross-tabulation by age cohorts and gender.',
     'High-risk groups (e.g. pediatric cases in Dengue or geriatric vulnerability in COVID-19) remain undetected until mortality rates spike.',
     'High'),
    ('DEF-04',
     'Reactive Resource Misallocation\nHospital ICU beds, oxygen cylinders, ventilators, and emergency medications are dispatched only after hospital wards overflow.',
     'Severe regional supply shortages in surge districts, accompanied by medical stock idling in unaffected neighboring districts.',
     'Critical'),
    ('DEF-05',
     'Absence of Clinical Quality Benchmarking\nMetrics such as Case Fatality Rate (CFR %) and Clinical Recovery Efficacy % are rarely normalized or benchmarked across states.',
     'Inability to evaluate healthcare system efficiency or identify districts suffering from sub-standard clinical triage and delayed treatment.',
     'Medium'),
]
add_table(doc, prob_headers, prob_rows, [Cm(2.2), Cm(6.5), Cm(5.8), Cm(2.0)])

# 1.4 Proposed Solution & Project Value Proposition
add_heading(doc, '1.4 Proposed Solution & Project Scope (P100)', 2)
p_sol = doc.add_paragraph(
    'Project P100 ("Disease Trend Analysis Intelligence Cockpit") resolves these operational challenges by delivering '
    'a high-performance, interactive multi-page web application built using Python, Streamlit, SQLite 3NF relational data marts, '
    'and Plotly Express. The platform synthesizes 5 years of historical health surveillance records (60 continuous calendar '
    'months: January 2020 to December 2024), covering 3,000 monthly state-disease observations across 5 critical diseases '
    'and 10 representative Indian states. By providing instant multi-faceted sidebar filtering, real-time KPI card tracking, '
    '12-month cyclic seasonality heatmaps, demographic pyramid breakdowns, urban density regression modeling, and automated '
    'concurrent surge alerting, the system empowers public health officials with data-driven decision superiority.'
)
p_sol.runs[0].font.size = Pt(10)
doc.add_paragraph()

# ═══════════════════════════════════════════════
# 2. INTENDED AUDIENCE / USERS
# ═══════════════════════════════════════════════
add_heading(doc, '2. Intended Audience / Users', 1)
p2 = doc.add_paragraph(
    'The application serves multiple user personas with varying frequency of use and analytical needs:'
)
p2.runs[0].font.size = Pt(10)

aud_headers = ['User Type', 'Description', 'Frequency of Use', 'Primary Goal']
aud_rows = [
    ('Public Health Officer',
     'State/district health dept official monitoring outbreak signals',
     'Daily / Weekly',
     'Spot emerging disease spikes and deploy response teams'),
    ('Epidemiologist / Researcher',
     'Medical researcher analysing disease spread patterns',
     'Weekly',
     'Identify risk factors, correlations, seasonal patterns'),
    ('Hospital Administrator',
     'Admin managing bed capacity & medical supplies',
     'Weekly / Monthly',
     'Anticipate patient surge and allocate resources proactively'),
    ('Policy Maker / Health Minister',
     'Senior official deciding on public health budgets',
     'Monthly',
     'Evidence-based budget approvals and policy decisions'),
    ('MCA Data Analytics Student',
     'Developer and academic user demonstrating the project',
     'As needed',
     'Demonstrate EDA skills; satisfy academic submission requirements'),
]
add_table(doc, aud_headers, aud_rows, [Cm(3.5), Cm(5.5), Cm(3), Cm(5)])

# ═══════════════════════════════════════════════
# 3. STAKEHOLDERS
# ═══════════════════════════════════════════════
add_heading(doc, '3. Stakeholder Register', 1)
sh_headers = ['SH ID', 'Stakeholder', 'Role', 'Interest', 'Influence', 'Key Decision Made with App']
sh_rows = [
    ('SH-01', 'Public Health Officer', 'Primary User',
     'Monitor & control disease outbreaks', 'H',
     'Deploy field response teams; issue public health alerts'),
    ('SH-02', 'Hospital Administrator', 'Primary User',
     'Manage hospital capacity efficiently', 'H',
     'Allocate beds, medicines, and ICU resources ahead of surge'),
    ('SH-03', 'Policy Maker / Health Ministry', 'Decision Maker',
     'Assess severity; justify budget allocation', 'H',
     'Approve emergency health budgets; enforce containment measures'),
    ('SH-04', 'Epidemiologist / Researcher', 'Analyst',
     'Understand disease dynamics and risk factors', 'M',
     'Design targeted intervention studies; publish research findings'),
    ('SH-05', 'Arg Jain (Student Developer)', 'Developer & User',
     'Demonstrate data analytics competency', 'M',
     'Academic submission and project evaluation decisions'),
    ('SH-06', 'Mr. Dinesh (Mentor)', 'Evaluator',
     'Ensure academic quality and correctness', 'L',
     'Grade the project; approve for final submission'),
]
add_table(doc, sh_headers, sh_rows, [Cm(1.5), Cm(3), Cm(2.5), Cm(4), Cm(1.5), Cm(5)])

# ═══════════════════════════════════════════════
# 4. OPERATIONAL QUESTIONS
# ═══════════════════════════════════════════════
add_heading(doc, '4. Operational Questions (OQ-01 to OQ-10)', 1)
p4 = doc.add_paragraph(
    'The following 10 questions represent the core analytical capabilities the app must deliver. '
    'Every OQ has been verified as answerable from the planned synthetic dataset.'
)
p4.runs[0].font.size = Pt(10)
doc.add_paragraph()

oq_headers = ['OQ ID', 'Operational Question', 'Stakeholder(s)', 'Data Required', 'Answerable']
oq_rows = [
    ('OQ-01', 'Which diseases have shown the highest increase in reported cases over the last 5 years?',
     'SH-01, SH-03', 'Disease name, year, case count', 'YES'),
    ('OQ-02', 'Which geographic regions (states) are most affected by each disease?',
     'SH-01, SH-02', 'Region, disease name, case count', 'YES'),
    ('OQ-03', 'What is the monthly/seasonal trend of disease outbreaks?',
     'SH-01, SH-04', 'Date (month/year), disease, case count', 'YES'),
    ('OQ-04', 'Which age group and gender are most vulnerable to specific diseases?',
     'SH-04, SH-03', 'Age group, gender, disease, case count', 'YES'),
    ('OQ-05', 'What is the case fatality rate (CFR) for each disease across regions?',
     'SH-02, SH-03', 'Cases, deaths, disease, region', 'YES'),
    ('OQ-06', 'How does disease incidence correlate with population density?',
     'SH-04', 'Region, population (density derived), case count', 'YES'),
    ('OQ-07', 'Which diseases have the highest recovery rates, and in which regions?',
     'SH-02, SH-01', 'Cases, recoveries, disease, region', 'YES'),
    ('OQ-08', 'Are there concurrent disease outbreaks (co-occurring epidemics) in any region?',
     'SH-01, SH-04', 'Date, region, multiple disease case counts', 'YES'),
    ('OQ-09', 'What is the year-over-year (YoY) percentage change in reported cases per disease?',
     'SH-03, SH-01', 'Year, disease, case count', 'YES'),
    ('OQ-10', 'Which months see peak disease reporting, and does this vary by disease type?',
     'SH-01, SH-04', 'Month, disease, case count', 'YES'),
]
add_table(doc, oq_headers, oq_rows, [Cm(1.5), Cm(6.5), Cm(2.5), Cm(5), Cm(2)])

p_check = doc.add_paragraph()
run = p_check.add_run(
    'Data Coverage Check: All 10 OQs are fully answerable from the planned synthetic dataset '
    '(disease, region, date, demographics, case/death/recovery counts).'
)
run.font.bold = True
run.font.size = Pt(9)
run.font.color.rgb = RGBColor(0x1E,0x8B,0x4C)
doc.add_paragraph()

# ═══════════════════════════════════════════════
# 5. OBJECTIVES (SMART)
# ═══════════════════════════════════════════════
add_heading(doc, '5. Objectives (SMART)', 1)
obj_headers = ['OBJ ID', 'Objective Statement', 'Measurable Target', 'Time-Bound']
obj_rows = [
    ('OBJ-01',
     'Build a Streamlit app that answers all 10 OQs using synthetic epidemiological data covering 5 diseases, 10 Indian states, over 5 years (2020-2024).',
     '10/10 OQs demonstrable in live walkthrough',
     'Dec 2026'),
    ('OBJ-02',
     'Provide 6 or more interactive Plotly visualisations (line, bar, heatmap, scatter, pie, choropleth) with filters for disease, region, year, and demographic.',
     'At least 6 chart types; each loads in under 5 seconds',
     'Dec 2026'),
    ('OBJ-03',
     'Achieve 80% or higher pytest coverage with 15 or more test cases and zero critical test failures at submission.',
     'pytest --cov report: coverage >= 80%, 0 critical failures',
     'Dec 2026'),
    ('OBJ-04',
     'Deploy the app on Streamlit Community Cloud with the public URL accessible during the final evaluation window.',
     'Live URL accessible; 99% uptime over last 2 weeks of semester',
     'Dec 2026'),
    ('OBJ-05',
     'Produce a complete ABES-format Project Document covering all 18 steps and a slide deck with full traceability to Business Requirements.',
     '18-section document and presentation deck submitted and approved by mentor',
     'Dec 2026'),
]
add_table(doc, obj_headers, obj_rows, [Cm(1.5), Cm(9), Cm(4.5), Cm(2)])

# ═══════════════════════════════════════════════
# 6. SCOPE
# ═══════════════════════════════════════════════
add_heading(doc, '6. Project Scope', 1)

add_heading(doc, '6.1 In Scope', 2)
in_scope = [
    'Synthetic disease incidence dataset: 5 diseases (Dengue, Malaria, Tuberculosis, COVID-19, Typhoid), 10 Indian states, monthly data January 2020 to December 2024, with demographic breakdown by age group and gender.',
    'Exploratory Data Analysis (EDA): descriptive statistics, trend analysis, year-over-year change, correlation analysis.',
    'Interactive Plotly visualisations: time-series line chart, regional bar chart, choropleth map (state level), heatmap, scatter plot (incidence vs. density), pie chart (disease share).',
    'Multi-page Streamlit app with Tailwind-style CSS theming and sidebar filters.',
    'SQLite relational database as the data backend with structured schema.',
    'pytest test suite with at least 15 test cases and at least 80% code coverage.',
    'ABES-format Project Document (Word) covering all 18 project steps.',
    'ABES slide deck for final mentor presentation.',
    'Deployment on Streamlit Community Cloud (free tier) with shareable public URL.',
]
for item in in_scope:
    p = doc.add_paragraph(style='List Bullet')
    p.add_run(item).font.size = Pt(9.5)
doc.add_paragraph()

add_heading(doc, '6.2 Out of Scope', 2)
out_scope = [
    'Real or live patient data or any integration with hospital information systems (privacy/regulatory constraints).',
    'Predictive modelling or Machine Learning-based disease forecasting.',
    'Mobile application development (iOS or Android).',
    'User authentication, login system, or role-based access control.',
    'Real-time data ingestion, REST API integration, or external live data feeds.',
    'Multi-language (non-English) user interface support.',
    'Automated email or SMS alerting to stakeholders.',
]
for item in out_scope:
    p = doc.add_paragraph(style='List Bullet')
    p.add_run(item).font.size = Pt(9.5)
doc.add_paragraph()

# ═══════════════════════════════════════════════
# 7. ASSUMPTIONS & CONSTRAINTS
# ═══════════════════════════════════════════════
add_heading(doc, '7. Assumptions and Constraints', 1)

add_heading(doc, '7.1 Assumptions', 2)
assumptions = [
    ('A-01', 'Synthetic data generated using Python (Faker, NumPy, Pandas) will simulate realistic disease trends without using any real patient data.'),
    ('A-02', 'Region refers to 10 selected Indian states: Uttar Pradesh, Maharashtra, Delhi, Rajasthan, Bihar, West Bengal, Tamil Nadu, Karnataka, Gujarat, Madhya Pradesh.'),
    ('A-03', 'Diseases covered are Dengue, Malaria, Tuberculosis (TB), COVID-19, and Typhoid, representing major public health concerns in India.'),
    ('A-04', 'Dataset spans January 2020 to December 2024 (60 months) with monthly granularity.'),
    ('A-05', 'Age groups defined as: 0-14, 15-29, 30-44, 45-59, 60 and above. Gender categories: Male, Female, Other.'),
    ('A-06', 'Stable internet access is available for Streamlit Community Cloud deployment and evaluation.'),
    ('A-07', 'The mentor will evaluate the app via the public Streamlit URL during the final two weeks of the semester.'),
]
t_a = doc.add_table(rows=len(assumptions)+1, cols=2)
t_a.style = 'Table Grid'
header_row(t_a, ['Assumption ID', 'Assumption Statement'])
for i,(aid,atext) in enumerate(assumptions):
    fill = 'EBF5FB' if i%2==0 else 'FFFFFF'
    r = t_a.rows[i+1]
    shade_cell(r.cells[0], fill)
    r.cells[0].paragraphs[0].add_run(aid).font.size = Pt(9)
    shade_cell(r.cells[1], fill)
    r.cells[1].paragraphs[0].add_run(atext).font.size = Pt(9)
set_col_widths(t_a, [Cm(2.5), Cm(14)])
doc.add_paragraph()

add_heading(doc, '7.2 Constraints', 2)
constraints = [
    ('C-01', 'Timeline', 'Project must be fully completed and submitted by end of MCA Semester (December 2026).'),
    ('C-02', 'Technology', 'Only free and open-source tools permitted: Python 3.10+, Streamlit, SQLite, Plotly, pytest.'),
    ('C-03', 'Data Privacy', 'No real personal health data may be used at any stage; synthetic data only.'),
    ('C-04', 'Hosting', 'App must run within Streamlit Community Cloud free-tier limits (1 GB RAM, shared CPU).'),
    ('C-05', 'Team Size', 'Individual project: all work must be performed solely by Arg Jain.'),
]
t_c = doc.add_table(rows=len(constraints)+1, cols=3)
t_c.style = 'Table Grid'
header_row(t_c, ['Constraint ID', 'Category', 'Constraint Statement'])
for i,(cid,cat,ctext) in enumerate(constraints):
    fill = 'EBF5FB' if i%2==0 else 'FFFFFF'
    r = t_c.rows[i+1]
    for ci,val in enumerate([cid,cat,ctext]):
        shade_cell(r.cells[ci], fill)
        r.cells[ci].paragraphs[0].add_run(val).font.size = Pt(9)
set_col_widths(t_c, [Cm(2.5), Cm(3), Cm(11)])
doc.add_paragraph()

# ═══════════════════════════════════════════════
# 8. SUCCESS CRITERIA
# ═══════════════════════════════════════════════
add_heading(doc, '8. Success Criteria (Measurable)', 1)
sc_headers = ['SC ID', 'Success Criterion', 'Measurement Method', 'Target Value']
sc_rows = [
    ('SC-01', 'All 10 Operational Questions are answerable through the app UI',
     'Live mentor walkthrough demonstration', '10 out of 10 OQs answered'),
    ('SC-02', 'App loads and renders all charts within acceptable response time',
     'Manual timer measurement on Streamlit Cloud URL', 'Under 5 seconds initial load'),
    ('SC-03', 'pytest test suite passes with sufficient coverage and no critical failures',
     'pytest --cov report output at submission', '80% or higher coverage, 0 critical failures'),
    ('SC-04', 'Project document is complete and covers all 18 steps with traceability',
     'Mentor document review against ABES template checklist', 'All 18 sections completed and approved'),
    ('SC-05', 'Final presentation is evaluated positively by the mentor',
     'Mentor evaluation rubric score from viva/presentation', '70% or higher marks'),
    ('SC-06', 'Application remains accessible during evaluation window without downtime',
     'Streamlit Community Cloud URL availability check', '99% uptime during final 2 weeks of semester'),
]
add_table(doc, sc_headers, sc_rows, [Cm(1.5), Cm(6.5), Cm(5), Cm(4)])

# ═══════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════
doc.add_paragraph()
foot = doc.add_paragraph()
foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = foot.add_run(
    'File: 01_ArgJain_DiseaseTrendAnalysis_ProjectUnderstanding.docx  |  v1.0  |  Nov 2026  |  ABES Engineering College'
)
run.font.size = Pt(8)
run.font.color.rgb = RGBColor(0x88,0x88,0x88)

path = r'c:\Users\Hp\Downloads\hcl\docs\01_ArgJain_DiseaseTrendAnalysis_ProjectUnderstanding.docx'
import time
saved = False
for attempt in range(5):
    try:
        doc.save(path)
        print('SAVED:', path)
        saved = True
        break
    except PermissionError:
        print(f"File {path} is currently open in an editor, retrying in 2s...")
        time.sleep(2)

if not saved:
    alt_path = r'c:\Users\Hp\Downloads\hcl\docs\01_ArgJain_DiseaseTrendAnalysis_ProjectUnderstanding_updated.docx'
    doc.save(alt_path)
    print('SAVED TO ALTERNATE PATH:', alt_path)
