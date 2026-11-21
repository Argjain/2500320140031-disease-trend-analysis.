import os
import docx
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

os.makedirs(r'c:\Users\Hp\Downloads\hcl\docs', exist_ok=True)
doc = Document()

for sec in doc.sections:
    sec.top_margin = Cm(2.5)
    sec.bottom_margin = Cm(2.5)
    sec.left_margin = Cm(3.0)
    sec.right_margin = Cm(2.0)

PRIMARY_COLOR = RGBColor(0x1A, 0x53, 0x76)
HEX_PRIMARY = '1A5376'
HEX_ALT_ROW = 'EBF5FB'
HEX_HEADER = 'D6EAF8'
HEX_MUST = 'EAFAF1'
HEX_SHOULD = 'FEF9E7'
HEX_COULD = 'FDEBD0'

def shade_cell(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hex_color)
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_heading_1(text):
    h = doc.add_heading(text, level=1)
    for r in h.runs:
        r.font.color.rgb = PRIMARY_COLOR
        r.font.name = 'Calibri'
        r.font.bold = True
    return h

def add_heading_2(text):
    h = doc.add_heading(text, level=2)
    for r in h.runs:
        r.font.color.rgb = RGBColor(0x2E, 0x86, 0xAB)
        r.font.name = 'Calibri'
        r.font.bold = True
    return h

def format_table(table, col_widths, headers, data, priority_col=None):
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = table.rows[0]
    for i, col_name in enumerate(headers):
        c = hdr.cells[i]
        shade_cell(c, HEX_PRIMARY)
        set_cell_margins(c)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(col_name)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        run.font.size = Pt(9)
        run.font.name = 'Calibri'

    for r_idx, row_data in enumerate(data):
        row = table.rows[r_idx + 1]
        priority_val = row_data[priority_col] if priority_col is not None else None
        
        if priority_val == 'Must':
            row_fill = HEX_MUST
        elif priority_val == 'Should':
            row_fill = HEX_SHOULD
        elif priority_val == 'Could':
            row_fill = HEX_COULD
        else:
            row_fill = HEX_ALT_ROW if r_idx % 2 == 0 else 'FFFFFF'

        for c_idx, val in enumerate(row_data):
            cell = row.cells[c_idx]
            shade_cell(cell, row_fill)
            set_cell_margins(cell)
            p = cell.paragraphs[0]
            run = p.add_run(str(val))
            run.font.size = Pt(8.5)
            run.font.name = 'Calibri'

    for row in table.rows:
        for idx, width in enumerate(col_widths):
            row.cells[idx].width = width

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# COVER BLOCK
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
p_title = doc.add_paragraph()
p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
run_t = p_title.add_run('DISEASE TREND ANALYSIS')
run_t.font.size = Pt(22)
run_t.font.bold = True
run_t.font.color.rgb = PRIMARY_COLOR

p_sub = doc.add_paragraph()
p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
run_sub = p_sub.add_run('STEP 5 — Business Requirements Document (BRD)')
run_sub.font.size = Pt(14)
run_sub.font.bold = True
run_sub.font.color.rgb = RGBColor(0x2E, 0x86, 0xAB)

doc.add_paragraph()

meta_data = [
    ('Project ID & Title', 'P100 | Disease Trend Analysis'),
    ('Domain', 'Healthcare Data Analytics'),
    ('Student Author', 'Arg Jain (Roll No. 2500320140031)'),
    ('Academic Program', 'MCA 2nd Year (Data Analytics)'),
    ('Institution', 'ABES Engineering College, Ghaziabad'),
    ('Faculty Mentor', 'Mr. Dinesh'),
    ('Document Version', 'v1.0 (Baseline Release)'),
    ('Release Date', 'November 2026'),
    ('Target Environment', 'Python 3.12 / Streamlit Community Cloud'),
    ('Document Status', 'Approved for Architecture & Engineering'),
]

t_meta = doc.add_table(rows=len(meta_data), cols=2)
t_meta.style = 'Table Grid'
t_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
for idx, (k, v) in enumerate(meta_data):
    r = t_meta.rows[idx]
    shade_cell(r.cells[0], 'D6EAF8')
    p0 = r.cells[0].paragraphs[0]
    rn0 = p0.add_run(k)
    rn0.font.bold = True
    rn0.font.size = Pt(9)
    p1 = r.cells[1].paragraphs[0]
    rn1 = p1.add_run(v)
    rn1.font.size = Pt(9)
for r in t_meta.rows:
    r.cells[0].width = Cm(5.0)
    r.cells[1].width = Cm(11.0)

doc.add_paragraph()
doc.add_page_break()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 1. DOCUMENT CONTROL
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
add_heading_1('1. Document Control & Revision History')
p_dc = doc.add_paragraph('This document is maintained under formal configuration management guidelines:')
p_dc.runs[0].font.size = Pt(10)

doc_ctrl_data = [
    ['v0.1', '14-Nov-2026', 'Arg Jain', 'Initial requirements gathering from Step 1-3 deliverables', 'Self-Review'],
    ['v0.9', '16-Nov-2026', 'Arg Jain', 'Integrated RACI, Business Rules, and Data Requirements', 'Mentor Review'],
    ['v1.0', '18-Nov-2026', 'Arg Jain', 'Formal baseline document for academic submission and build plan', 'Mr. Dinesh'],
]
t_dc = doc.add_table(rows=len(doc_ctrl_data) + 1, cols=5)
format_table(t_dc, [Cm(1.8), Cm(2.5), Cm(2.5), Cm(6.2), Cm(3.0)], ['Version', 'Date', 'Author', 'Summary of Changes', 'Reviewer'], doc_ctrl_data)
doc.add_paragraph()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 2. EXECUTIVE SUMMARY
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
add_heading_1('2. Executive Summary')
p_es1 = doc.add_paragraph(
    'In contemporary public health administration across India, epidemiological data often resides in disparate, '
    'siloed departmental systems and static PDF bulletins. This structural fragmentation creates severe latency '
    'in detecting seasonal and localized outbreaks of endemic diseases such as Dengue, Malaria, Tuberculosis, '
    'COVID-19, and Typhoid. Decision-makers frequently face a multi-week lag between field transmission spikes '
    'and executive intervention, resulting in avoidable hospital bed crises and delayed therapeutic provisioning.'
)
p_es1.runs[0].font.size = Pt(10)

p_es2 = doc.add_paragraph(
    'The Disease Trend Analysis platform (Project P100) delivers a unified, interactive analytical cockpit '
    'engineered specifically for public health officers, hospital administrators, epidemiologists, and ministerial policy makers. '
    'By integrating historical epidemiological time series across 10 major Indian states over a 5-year observation period (2020–2024), '
    'the application surfaces critical trajectory indicators: Case Fatality Rates (CFR), regional burden benchmarks, '
    'demographic risk vectors, seasonal transmission waves, and co-occurring outbreak warnings.'
)
p_es2.runs[0].font.size = Pt(10)

p_es3 = doc.add_paragraph(
    'Built entirely on an open-source data analytics stack (Python, SQLite, Streamlit, Plotly, pytest) and deployed '
    'on cloud infrastructure, the solution satisfies all 10 Operational Questions (OQ-01 through OQ-10) with sub-second '
    'visual response times. This document formally establishes the business baseline, stakeholder alignment, '
    'and functional boundary for downstream engineering execution.'
)
p_es3.runs[0].font.size = Pt(10)
doc.add_paragraph()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 3. BUSINESS PROBLEM & STRATEGIC OPPORTUNITY
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
add_heading_1('3. Business Problem & Opportunity Analysis')

add_heading_2('3.1 Current State Deficiencies')
bullet_points_curr = [
    'Static Reporting Latency: Epidemiological surveillance is published as monthly retrospective PDF summaries, preventing real-time tactical intervention.',
    'Fragmented Demographic Visibility: Co-morbidity and vulnerability indicators across age cohorts and gender brackets are not cross-filterable with geographical hotspots.',
    'Absence of Co-occurrence Warnings: Syndromic overlap (e.g., concurrent Dengue and Malaria surges during post-monsoon weeks) is evaluated in departmental silos.',
]
for bp in bullet_points_curr:
    p = doc.add_paragraph(style='List Bullet')
    r = p.add_run(bp)
    r.font.size = Pt(9.5)

add_heading_2('3.2 Desired State Capabilities')
bullet_points_des = [
    'Single-Pane Epidemiological Cockpit: Real-time visual dashboard rendering multidimensional case aggregates, fatality ratios, and recovery metrics.',
    'Granular Micro-Demographic Profiling: Instant filtering by disease entity, state boundary, calendar year, age cohort, and gender identity.',
    'Automated Multi-Disease Overlap Surveillance: Early flagging of regions where multiple contagious entities simultaneously exceed statistical thresholds.',
]
for bp in bullet_points_des:
    p = doc.add_paragraph(style='List Bullet')
    r = p.add_run(bp)
    r.font.size = Pt(9.5)

add_heading_2('3.3 Cost of Inaction')
bullet_points_cost = [
    'Sub-optimal Health Budget Allocation: Health funds allocated evenly rather than targeted toward high-CFR districts experiencing accelerating growth.',
    'Emergency Department Overcrowding: Inability to anticipate 60-day seasonal surges causes catastrophic ICU bed and oxygen shortages.',
]
for bp in bullet_points_cost:
    p = doc.add_paragraph(style='List Bullet')
    r = p.add_run(bp)
    r.font.size = Pt(9.5)

doc.add_paragraph()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 4. OBJECTIVES & SUCCESS METRICS (KPIs)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
add_heading_1('4. Project Objectives & Success Metrics (KPIs)')
p_obj = doc.add_paragraph('Performance against charter objectives will be audited using quantitative criteria:')
p_obj.runs[0].font.size = Pt(10)

kpi_data = [
    ['OBJ-01', 'OQ Resolution Completeness', 'App answers all 10 defined operational questions through intuitive UI', '0 OQs', '10 / 10 OQs (100%)', 'Interactive mentor walkthrough'],
    ['OBJ-02', 'Visual Analytical Diversity', 'Interactive Plotly charts (Line, Bar, Heatmap, Scatter, Demographics, Quality)', '0 charts', '>= 6 Distinct Chart Types', 'UI inspection'],
    ['OBJ-03', 'Engine Latency & Performance', 'End-to-end page render and filter recalculation speed', 'N/A', '< 5.0s Initial, < 2.0s Filter', 'Automated timer logging'],
    ['OBJ-04', 'Test Suite Integrity', 'Automated pytest test suite line & branch coverage', '0%', '>= 80% Coverage (0 critical bugs)', 'pytest-cov execution report'],
    ['OBJ-05', 'Cloud Availability', 'Continuous operational uptime on Streamlit Community Cloud', 'Local only', '>= 99.0% Uptime over eval period', 'Cloud host monitoring'],
]
t_kpi = doc.add_table(rows=len(kpi_data) + 1, cols=6)
format_table(t_kpi, [Cm(1.8), Cm(3.2), Cm(4.5), Cm(1.5), Cm(2.5), Cm(2.5)], ['Obj ID', 'KPI Name', 'Metric Description', 'Baseline', 'Target', 'Verification'], kpi_data)
doc.add_paragraph()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 5. STAKEHOLDER RACI MATRIX
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
add_heading_1('5. Stakeholder Governance & RACI Framework')
p_raci = doc.add_paragraph('RACI mapping across the project development lifecycle (R = Responsible, A = Accountable, C = Consulted, I = Informed):')
p_raci.runs[0].font.size = Pt(10)

raci_data = [
    ['SH-01', 'Public Health Officer', 'Primary User', 'C', 'I', 'R', 'I', 'Validates outbreak threshold models'],
    ['SH-02', 'Hospital Administrator', 'Primary User', 'C', 'I', 'R', 'I', 'Advises surge and bed capacity KPIs'],
    ['SH-03', 'Policy Maker / Ministry', 'Executive User', 'I', 'A', 'I', 'A', 'Approves strategic metrics & budget views'],
    ['SH-04', 'Epidemiologist / Researcher', 'Expert Analyst', 'C', 'I', 'R', 'I', 'Reviews statistical correlations & CFR formulas'],
    ['SH-05', 'Arg Jain', 'Lead Developer (Student)', 'R', 'A', 'R', 'R', 'Owns end-to-end design, code, and deployment'],
    ['SH-06', 'Mr. Dinesh', 'Faculty Evaluator (Mentor)', 'A', 'A', 'A', 'A', 'Evaluates academic rigor and signs off release'],
]
t_raci = doc.add_table(rows=len(raci_data) + 1, cols=8)
format_table(t_raci, [Cm(1.5), Cm(3.0), Cm(2.2), Cm(1.0), Cm(1.0), Cm(1.0), Cm(1.0), Cm(5.3)], ['SH ID', 'Stakeholder Name', 'Role', 'Req', 'Des', 'Bld', 'Dep', 'Key Responsibilities'], raci_data)
doc.add_paragraph()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 6. SCOPE SPECIFICATION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
add_heading_1('6. Scope Specification')

add_heading_2('6.1 In-Scope Capabilities')
in_scope_items = [
    'Synthetic epidemiological dataset spanning 5 diseases (Dengue, Malaria, Tuberculosis, COVID-19, Typhoid) across 10 Indian states from Jan 2020 to Dec 2024 (60 months).',
    'Normalized SQLite relational database schema (3 master tables, 1 primary fact table, 1 demographic fact table, 1 denormalized analytical view).',
    'Exploratory Data Analysis (EDA) engine computing case sums, CFR %, recovery %, YoY % delta, monthly cyclical indices, and Pearson density correlation.',
    'Interactive Streamlit web application styled with Tailwind CSS visual design patterns and synchronized sidebar filtering.',
    'Data export capability to standard CSV format and transparent data quality auditing ledger.',
    'Automated test suite (pytest) covering database integrity, calculation formulas, and UI responsiveness.',
    'Deployment to Streamlit Community Cloud with public HTTPS URL for evaluator access.',
]
for item in in_scope_items:
    p = doc.add_paragraph(style='List Bullet')
    r = p.add_run(item)
    r.font.size = Pt(9.5)

add_heading_2('6.2 Out-of-Scope Capabilities')
out_scope_items = [
    'Real or identifiable patient electronic health records (EHR) due to statutory HIPAA/DISHA data protection regulations.',
    'Machine learning predictive forecasting models (e.g., ARIMA, Prophet, LSTM) — deferred to academic semester 3/4.',
    'Native mobile application development (iOS/Android).',
    'User identity management, role-based access control (RBAC), and authentication gateways.',
    'Automated SMS or email outbound emergency broadcasting pipelines.',
    'Multi-lingual internationalization (platform standard is Indian English).',
]
for item in out_scope_items:
    p = doc.add_paragraph(style='List Bullet')
    r = p.add_run(item)
    r.font.size = Pt(9.5)

doc.add_paragraph()
doc.add_page_break()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 7. BUSINESS REQUIREMENTS DETAIL (BR-01 to BR-15)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
add_heading_1('7. Detailed Business Requirements Register')
p_br_intro = doc.add_paragraph('Each requirement is itemized with operational rationale and formal acceptance criteria:')
p_br_intro.runs[0].font.size = Pt(10)

detailed_brs = [
    ('BR-01', 'Multi-dimensional Incidence Aggregation', 'The business needs to aggregate disease case counts by disease entity, geographical region, and temporal period so that health officers can detect emerging outbreak trends early.', 'Without consolidated multidimensional grouping, analysts cannot observe state-level or seasonal shifts.', 'Must', 'HMW-01, HMW-09', '1. User can aggregate cases across any combination of 5 diseases, 10 states, and 5 years.\n2. Aggregated totals match raw SQL sums.\n3. Renders within 1.5 seconds.'),
    ('BR-02', 'Comparative Regional Burden Benchmarking', 'The business needs to compare disease burden across states on a common scale so that hospital administrators can anticipate inter-state patient surge patterns.', 'Allows cross-state allocation of mobile intensive care units and consumable medical supplies.', 'Must', 'HMW-02', '1. Displays horizontal ranking of all 10 states sorted descending by case volume.\n2. Filter changes update state rankings instantly.'),
    ('BR-03', 'Case Fatality Rate (CFR) Intelligence', 'The business needs to compute and display Case Fatality Rates (CFR) across diseases and regions so that policy makers can identify high-mortality zones and justify emergency resource deployment.', 'High incidence with low CFR indicates managed caseload; high CFR demands acute medical intervention.', 'Must', 'HMW-03', '1. CFR calculated strictly as (Deaths / Cases * 100).\n2. Handled safely for zero case counts (returns 0.0%).\n3. Displayed in disease-by-region heatmap matrix.'),
    ('BR-04', 'Vulnerable Demographic Cohort Profiling', 'The business needs to segment disease morbidity by age bracket and gender cohort so that epidemiologists can identify demographic vulnerability profiles.', 'Enables targeted immunization and public messaging (e.g., pediatric vs elderly outreach).', 'Must', 'HMW-04', '1. Visual breakdown across 5 age groups (0-14, 15-29, 30-44, 45-59, 60+) and 3 genders.\n2. Sum of demographic slices equals total reported cases within 10% sampling variance.'),
    ('BR-05', 'Automated Co-occurring Outbreak Surveillance', 'The business needs to detect and flag concurrent outbreaks where multiple diseases cross threshold levels simultaneously in the same region and time frame so that response teams avoid overwhelmed local healthcare capacity.', 'Syndromic convergence can collapse local hospital triage capacity rapidly.', 'Must', 'HMW-05', '1. Algorithmic trigger flags any state-month where >= 2 diseases exceed 1.5x monthly historical baseline.\n2. High-risk region-months presented in dedicated alert view.'),
    ('BR-06', 'Seasonal Wave & Cyclic Profiling', 'The business needs to profile monthly and seasonal variations in disease incidence so that medical supply chains can pre-position therapeutics ahead of peak months.', 'Vector-borne illnesses exhibit predictable monsoon peaks requiring 60-day advance procurement.', 'Must', 'HMW-06', '1. Cyclic curve maps average incidence across calendar months 1 through 12.\n2. Vector-borne peaks clearly discernible in monsoon window (July–September).'),
    ('BR-07', 'Clinical Recovery Benchmarking', 'The business needs to compute recovery percentages per disease and region so that hospital networks can benchmark clinical recovery efficacy against regional averages.', 'Highlights clinical management successes and identifies protocols worth standardizing.', 'Must', 'HMW-07', '1. Recovery rate computed as (Recovered / Cases * 100).\n2. All values constrained between 0.0% and 100.0%.\n3. Displayed alongside CFR in regional comparison view.'),
    ('BR-08', 'Urban Crowding & Density Correlation', 'The business needs to evaluate the correlation between disease incidence rate and population density so that researchers can quantify the impact of urban crowding on transmission.', 'Validates epidemiological models linking rapid urbanization to contagious disease velocity.', 'Should', 'HMW-08', '1. Scatter plot plots Incidence per Lakh against Population Density (persons/sq km).\n2. Calculates Pearson correlation coefficient (r) and two-tailed p-value.'),
    ('BR-09', 'Multi-Year Year-over-Year (YoY) Trajectory', 'The business needs to calculate year-over-year (YoY) percentage changes in reported cases per disease so that ministries can assess multi-year disease growth or containment.', 'Essential for evaluating effectiveness of multi-year public health programs.', 'Should', 'HMW-09', '1. Computes ((Cases_Yr - Cases_Yr-1) / Cases_Yr-1 * 100) across consecutive years.\n2. Displays diverging color indicators (Green for decline, Red for growth).'),
    ('BR-10', 'Relational Data Integrity Architecture', 'The business needs to maintain disease intelligence in a standardized, relational data store so that analytical queries are consistent, auditable, and reproducible.', 'Guarantees referential integrity, eliminates orphaned records, and ensures reproducibility.', 'Must', 'HMW-10', '1. Relational schema deployed in SQLite.\n2. Foreign key constraints enforce parent-child relations.\n3. Check constraints enforce non-negative values.'),
    ('BR-11', 'Synchronized Multidimensional Filtering', 'The business needs synchronized multidimensional filtering (disease, region, year, age, gender) that updates all visual perspectives concurrently so that analytical exploration is fluid.', 'Analysts should never experience state desynchronization across tabs or views.', 'Must', 'HMW-01..05', '1. Centralized filter controls persist across application pages.\n2. Modifying a filter cascades to all KPI cards and charts simultaneously.'),
    ('BR-12', 'Analytical Data Export Capability', 'The business needs to export filtered analytical datasets into standard spreadsheet formats so that researchers can conduct specialized external epidemiological modeling.', 'Facilitates offline analysis in R, SPSS, or advanced statistical modeling packages.', 'Should', 'HMW-10', '1. One-click CSV export button available on data screen.\n2. Output matches current filter slice and opens cleanly in Microsoft Excel.'),
    ('BR-13', 'Transparent Data Quality Ledger', 'The business needs a transparent data quality accounting ledger showing cleaning interventions (missing values imputed, duplicates removed, outliers bounded) so that data integrity is demonstrable.', 'Builds stakeholder trust in the validity and reliability of published findings.', 'Could', 'HMW-10', '1. Dedicated Data Quality screen displays pre-cleaning and post-cleaning metrics.\n2. Counts of nulls filled, duplicates purged, and outliers bounded are explicitly shown.'),
    ('BR-14', 'Automated Quality Assurance Test Suite', 'The business needs comprehensive automated verification test suites covering data ingestion, KPI calculations, and interface responsiveness so that operational errors are caught prior to evaluation.', 'Prevents computational regressions and validates data integrity before academic presentation.', 'Must', 'All HMWs', '1. pytest test suite executes cleanly.\n2. Line and calculation coverage >= 80% with 0 critical failures.'),
    ('BR-15', 'High-Availability Public Cloud Deployment', 'The business needs the analytical platform hosted on an accessible cloud platform with public access so that evaluating mentors and external reviewers can inspect the system remotely.', 'Enables seamless grading, mentor verification, and external stakeholder evaluation.', 'Should', 'OBJ-04', '1. Platform deployed on Streamlit Community Cloud.\n2. URL accessible via standard web browser without special VPN or login credentials.'),
]

for br_id, title, desc, rat, prio, hmw, ac in detailed_brs:
    p_b = doc.add_paragraph()
    r_b = p_b.add_run(f'{br_id}: {title} [{prio}]')
    r_b.font.bold = True
    r_b.font.size = Pt(11)
    r_b.font.color.rgb = PRIMARY_COLOR
    
    br_table_data = [
        ['Requirement Description', desc],
        ['Business Rationale', rat],
        ['Source HMW Link', hmw],
        ['Acceptance Criteria', ac],
    ]
    t = doc.add_table(rows=len(br_table_data), cols=2)
    t.style = 'Table Grid'
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for idx, (k, v) in enumerate(br_table_data):
        row = t.rows[idx]
        shade_cell(row.cells[0], 'D6EAF8')
        set_cell_margins(row.cells[0])
        p0 = row.cells[0].paragraphs[0]
        rn0 = p0.add_run(k)
        rn0.font.bold = True
        rn0.font.size = Pt(8.5)
        
        fill = HEX_MUST if prio == 'Must' and idx == 0 else (HEX_ALT_ROW if idx % 2 == 0 else 'FFFFFF')
        shade_cell(row.cells[1], fill)
        set_cell_margins(row.cells[1])
        p1 = row.cells[1].paragraphs[0]
        rn1 = p1.add_run(v)
        rn1.font.size = Pt(8.5)
    for row in t.rows:
        row.cells[0].width = Cm(4.5)
        row.cells[1].width = Cm(11.5)
    doc.add_paragraph()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 8. BUSINESS RULES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
add_heading_1('8. Business Rules Catalog')
p_brules = doc.add_paragraph('The platform strictly enforces the following domain validation rules:')
p_brules.runs[0].font.size = Pt(10)

b_rules_data = [
    ['BRL-01', 'CFR Calculation Integrity', 'Case Fatality Rate is strictly (Deaths / Cases * 100). If Cases = 0, CFR must return 0.00%. CFR can never exceed 100.00%.', 'BR-03', 'Engine / Calculation Layer'],
    ['BRL-02', 'Recovery Ceiling Constraint', 'Reported recoveries cannot exceed total cases. Recovery Rate = (Recovered / Cases * 100) constrained between 0.00% and 100.00%.', 'BR-07', 'Data Ingestion & UI Layer'],
    ['BRL-03', 'Temporal Filter Bounds', 'Date range selections cannot be inverted (Start Year cannot exceed End Year). Minimum selectable span is 1 calendar month.', 'BR-11', 'Sidebar UI Validation'],
    ['BRL-04', 'Outbreak Threshold Logic', 'A localized outbreak flag (is_outbreak = 1) triggers when monthly cases exceed 1.5x of the 5-year monthly historical mean for that state.', 'BR-05', 'Analytical Model Layer'],
    ['BRL-05', 'Synthetic Data Privacy Firewall', 'Under no circumstances may real patient names, Aadhaar numbers, or contact identifiers be stored or rendered. Synthetic data only.', 'BR-10', 'Data Architecture Governance'],
    ['BRL-06', 'Decimal Precision Standard', 'All published percentage metrics (CFR, Recovery Rate, YoY Change) must be formatted to exactly two decimal places (0.00%).', 'BR-01..09', 'Presentation Layer'],
]
t_brules = doc.add_table(rows=len(b_rules_data) + 1, cols=5)
format_table(t_brules, [Cm(1.8), Cm(3.5), Cm(6.5), Cm(1.8), Cm(2.4)], ['Rule ID', 'Rule Name', 'Operational Definition', 'Governs', 'Enforcement Point'], b_rules_data)
doc.add_paragraph()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 9. DATA REQUIREMENTS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
add_heading_1('9. Data Requirements & Model Entities')
p_dreq = doc.add_paragraph('The data pipeline ingests, validates, and maintains the following entities:')
p_dreq.runs[0].font.size = Pt(10)

dreq_data = [
    ['disease_master', 'Master table containing disease reference metadata (category, contagion flag, incubation period)', 'Curated Medical Reference', 'Static Table (5 records)', 'Relational PK: disease_id'],
    ['region_master', 'Geographic master containing state names, state codes, regional zones, population census, and land area', 'Census & Geospatial Reference', 'Static Table (10 states)', 'Relational PK: region_id'],
    ['demographic_group', 'Classification master cross-combining 5 age cohorts with 3 gender identities', 'Demographic Reference', 'Static Table (15 segments)', 'Relational PK: demo_id'],
    ['disease_cases', 'Primary transactional fact table containing monthly incident cases, deaths, recoveries, and active cases', 'State Epidemiological Reporting', 'Monthly Grain (3,000+ records)', 'Foreign Keys to disease & region'],
    ['demographic_breakdown', 'Secondary fact table itemizing case counts across age and gender segments for sampled cases', 'Clinical Triage Records', 'Fact Grain (~300 records)', 'Foreign Keys to case_id & demo_id'],
    ['v_disease_analysis', 'Denormalized joined analytical view combining all master and fact attributes with calculated KPIs', 'Relational Engine View', 'Materialized Query View (35+ columns)', 'Dynamic SQL View'],
]
t_dreq = doc.add_table(rows=len(dreq_data) + 1, cols=5)
format_table(t_dreq, [Cm(3.2), Cm(5.0), Cm(2.8), Cm(2.5), Cm(2.5)], ['Entity Name', 'Description & Business Role', 'Source Origin', 'Volume / Cardinality', 'Structural Nature'], dreq_data)
doc.add_paragraph()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 10. ASSUMPTIONS, CONSTRAINTS & DEPENDENCIES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
add_heading_1('10. Assumptions, Constraints & Dependencies')

add_heading_2('10.1 Foundational Assumptions')
assump_data = [
    ['A-01', 'Synthetic Data Realism', 'Algorithmic synthetic generation (Faker + NumPy) reproduces authentic epidemiological dynamics (seasonal waves, COVID spike, urban density correlation) with high fidelity.'],
    ['A-02', 'Geographic Representation', 'Ten selected states (UP, MH, DL, RJ, BR, WB, TN, KA, GJ, MP) provide a statistically balanced representation of Northern, Southern, Eastern, Western, and Central Indian healthcare dynamics.'],
    ['A-03', 'Temporal Granularity', 'A 5-year observation window (2020 to 2024) with monthly time buckets is sufficient to capture longitudinal trends, seasonal cyclicity, and pandemic waves.'],
    ['A-04', 'Evaluation Accessibility', 'The evaluation panel will possess standard modern web browsers with unrestricted HTTPS access to public cloud services (share.streamlit.io).'],
]
t_assump = doc.add_table(rows=len(assump_data) + 1, cols=3)
format_table(t_assump, [Cm(1.8), Cm(3.5), Cm(10.7)], ['ID', 'Assumption Category', 'Detailed Assumption Statement'], assump_data)

add_heading_2('10.2 Operational Constraints')
constr_data = [
    ['C-01', 'Academic Schedule', 'All 18 project steps, code artifacts, documentation, and viva presentations must be completed by December 2026.'],
    ['C-02', 'Open-Source Toolchain', 'Project implementation must rely strictly on free, open-source software libraries (Python, SQLite, Streamlit, Plotly, pytest) without commercial licensing costs.'],
    ['C-03', 'Free-Tier Cloud Limits', 'Hosting must operate within Streamlit Community Cloud free tier constraints (1 CPU, 1 GB RAM, shared memory limits).'],
    ['C-04', 'Individual Authorship', 'All architecture, development, QA, and documentation tasks must be completed solely by student candidate Arg Jain.'],
]
t_constr = doc.add_table(rows=len(constr_data) + 1, cols=3)
format_table(t_constr, [Cm(1.8), Cm(3.5), Cm(10.7)], ['ID', 'Constraint Category', 'Detailed Constraint Statement'], constr_data)
doc.add_paragraph()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 11. RISK MANAGEMENT MATRIX
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
add_heading_1('11. Risk Management & Mitigation Framework')
p_risk = doc.add_paragraph('Identified technical and operational risks along with pre-planned mitigation strategies:')
p_risk.runs[0].font.size = Pt(10)

risk_data = [
    ['R-01', 'Synthetic Data Credibility', 'Evaluator perceives synthetic data as artificial or ungrounded', 'Medium', 'High', 'Embed verifiable historical patterns (monsoon Dengue surges, COVID 2021 spike) and document data validation tests.'],
    ['R-02', 'Cloud Resource Throttling', 'Streamlit Cloud 1 GB memory limit reached during complex joins', 'Medium', 'Medium', 'Leverage @st.cache_data decorators, pre-aggregate heavy views in SQLite, and optimize DataFrame datatypes.'],
    ['R-03', 'Testing Coverage Deficit', 'Unable to reach mandatory 80% pytest code coverage before deadline', 'Low', 'Medium', 'Modularize analysis functions into pure, standalone Python functions easily tested via parameterized pytest fixtures.'],
    ['R-04', 'Cloud Inactivity Hibernation', 'Streamlit Cloud puts app to sleep after 7 days of zero traffic', 'High', 'Low', 'Document sleep behavior in deployment guide; wake application 1 hour prior to formal academic viva demonstration.'],
    ['R-05', 'Data Integrity Corruption', 'Inadvertent introduction of negative cases or deaths exceeding cases', 'Low', 'High', 'Enforce SQLite CHECK constraints and run automated cleaning pipeline before rendering any visual chart.'],
]
t_risk = doc.add_table(rows=len(risk_data) + 1, cols=6)
format_table(t_risk, [Cm(1.5), Cm(3.2), Cm(5.0), Cm(1.5), Cm(1.5), Cm(3.3)], ['Risk ID', 'Risk Title', 'Risk Description', 'Likelihood', 'Impact', 'Proactive Mitigation Strategy'], risk_data)
doc.add_paragraph()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 12. GLOSSARY OF TERMS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
add_heading_1('12. Glossary of Terms & Acronyms')
glossary_data = [
    ['CFR (Case Fatality Rate)', 'The proportion of deaths caused by a specific disease relative to total confirmed cases, calculated as (Deaths / Confirmed Cases * 100).'],
    ['Incidence Rate', 'The frequency of new disease cases occurring in a defined population over a specified time interval, normalized per 100,000 residents.'],
    ['Recovery Rate', 'The proportion of patients successfully recovered from a diagnosed disease, calculated as (Recovered / Confirmed Cases * 100).'],
    ['EDA (Exploratory Data Analysis)', 'The statistical practice of examining datasets through summary statistics, distribution analysis, and interactive visual charting.'],
    ['MoSCoW Prioritization', 'A prioritization framework categorizing requirements into Must Have, Should Have, Could Have, and Won\'t Have this time.'],
    ['OQ (Operational Question)', 'A concrete analytical question that end-users need the application to answer to make informed operational decisions.'],
    ['HMW (How Might We)', 'A design-thinking question format that reframes user pain points into actionable innovation opportunities.'],
    ['BR (Business Requirement)', 'A formal statement defining what capability the business requires to achieve a stated operational benefit.'],
    ['YoY (Year-over-Year)', 'A mathematical comparison of an identical metric across consecutive calendar years to identify growth trajectories.'],
    ['RTM (Requirements Traceability Matrix)', 'A tabular grid cross-mapping requirements to source needs, user stories, database schemas, and test verification cases.'],
    ['SQLite', 'A lightweight, zero-configuration, serverless, relational database management system embedded directly within the application filesystem.'],
    ['Streamlit', 'An open-source Python framework designed for rapid development and deployment of data science web applications.'],
]
t_gloss = doc.add_table(rows=len(glossary_data) + 1, cols=2)
format_table(t_gloss, [Cm(4.5), Cm(11.5)], ['Term / Acronym', 'Authoritative Definition'], glossary_data)
doc.add_paragraph()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 13. FORMAL SIGN-OFF & APPROVAL
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
add_heading_1('13. Formal Sign-off & Milestone Acceptance')
p_sign = doc.add_paragraph(
    'By signing below, the stakeholders confirm that the Business Requirements Document (BRD v1.0) '
    'accurately represents project scope, operational requirements, and success criteria. '
    'Engineering work on Technical Requirements (Step 7) and Database Design (Step 8) is authorized to proceed.'
)
p_sign.runs[0].font.size = Pt(10)
doc.add_paragraph()

sign_data = [
    ['Lead Developer / Student', 'Arg Jain (Roll No. 2500320140031)', 'Submitted for Review', '18-Nov-2026'],
    ['Faculty Mentor / Evaluator', 'Mr. Dinesh (Assistant Professor)', 'Recommended for Build', '18-Nov-2026'],
    ['Head of Department (MCA)', 'Prof. (Dr.) Expert Academician', 'Approved for Submission', 'Pending'],
]
t_sign = doc.add_table(rows=len(sign_data) + 1, cols=4)
format_table(t_sign, [Cm(4.0), Cm(4.5), Cm(4.5), Cm(3.0)], ['Signatory Role', 'Full Name & Designation', 'Approval Status / Signature', 'Date'], sign_data)

doc.add_paragraph()
p_foot = doc.add_paragraph()
p_foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
rn_f = p_foot.add_run('05_ArgJain_DiseaseTrendAnalysis_BRD.docx | v1.0 | ABES Engineering College | November 2026')
rn_f.font.size = Pt(8)
rn_f.font.color.rgb = RGBColor(0x88, 0x88, 0x88)

save_path = r'c:\Users\Hp\Downloads\hcl\docs\05_ArgJain_DiseaseTrendAnalysis_BRD.docx'
doc.save(save_path)
print(f'SAVED: {save_path}')
