import os
import docx
from docx import Document
from docx.shared import Pt, RGBColor, Cm, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

os.makedirs(r'c:\Users\Hp\Downloads\hcl\docs', exist_ok=True)
doc = Document()

# Set margins
for sec in doc.sections:
    sec.top_margin = Cm(2.5)
    sec.bottom_margin = Cm(2.5)
    sec.left_margin = Cm(3.0)
    sec.right_margin = Cm(2.0)

PRIMARY_COLOR = RGBColor(0x1A, 0x53, 0x76) # Deep Blue
HEX_PRIMARY = '1A5376'
HEX_ALT_ROW = 'EBF5FB'
HEX_HEADER = 'D6EAF8'
HEX_MUST = 'EAFAF1'
HEX_SHOULD = 'FEF9E7'
HEX_COULD = 'FDEBD0'

def shade_cell(cell, hex_color):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hex_color)
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_styled_heading(document, text, level=1):
    h = document.add_heading(text, level=level)
    h.alignment = WD_ALIGN_PARAGRAPH.LEFT
    for r in h.runs:
        r.font.color.rgb = PRIMARY_COLOR
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
            if c_idx in [0, 2, 4, 5]:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT

    for row in table.rows:
        for idx, width in enumerate(col_widths):
            row.cells[idx].width = width

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# COVER / TITLE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
p_title = doc.add_paragraph()
p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
run_t = p_title.add_run('DISEASE TREND ANALYSIS')
run_t.font.size = Pt(20)
run_t.font.bold = True
run_t.font.color.rgb = PRIMARY_COLOR

p_sub = doc.add_paragraph()
p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
run_sub = p_sub.add_run('STEP 3 — Needs Analysis & Business Requirements (BR)')
run_sub.font.size = Pt(13)
run_sub.font.bold = True
run_sub.font.color.rgb = RGBColor(0x2E, 0x86, 0xAB)

doc.add_paragraph()

meta_info = [
    ('Project ID', 'P100'),
    ('Project Title', 'Disease Trend Analysis'),
    ('Domain', 'Healthcare Data Analytics'),
    ('Student Name', 'Arg Jain'),
    ('Roll Number', '2500320140031'),
    ('Academic Program', 'MCA 2nd Year (Data Analytics Specialization)'),
    ('Institution', 'ABES Engineering College, Ghaziabad'),
    ('Faculty Mentor', 'Mr. Dinesh'),
    ('Document Version', 'v1.0'),
    ('Date', 'November 2026'),
]

t_meta = doc.add_table(rows=len(meta_info), cols=2)
t_meta.style = 'Table Grid'
t_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
for idx, (k, v) in enumerate(meta_info):
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
# 1. INTRODUCTION & PURPOSE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
add_styled_heading(doc, '1. Introduction & Methodology', level=1)
p_intro = doc.add_paragraph(
    'A Needs Analysis bridges user pain points discovered during design thinking (Step 2 HMW Statements) '
    'and functional architecture. For every HMW statement, we ask: "What does the stakeholder NEED to make this possible?" '
    'Each requirement is formally expressed in the standardized business requirement syntax: '
    '"The business needs to <capability> so that <benefit>." '
    'Importantly, this document focuses strictly on WHAT capabilities the business requires, '
    'completely agnostic of technical implementation (no SQL, Streamlit, or programming constructs).'
)
p_intro.runs[0].font.size = Pt(10)
doc.add_paragraph()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 2. BUSINESS REQUIREMENTS TABLE (BR-01 to BR-15)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
add_styled_heading(doc, '2. Business Requirements Register', level=1)
p_desc = doc.add_paragraph(
    'The 15 business requirements below have been prioritized using MoSCoW methodology '
    '(9 Must Have = 60%, 4 Should Have = 27%, 2 Could Have = 13%). '
    'Every requirement is directly traceable back to its originating HMW statement.'
)
p_desc.runs[0].font.size = Pt(10)

br_headers = ['BR ID', 'Business Requirement', 'Stakeholder', 'Source HMW', 'Priority', 'Measurement Criterion']
br_data = [
    [
        'BR-01',
        'The business needs to aggregate disease case counts by disease entity, geographical region, and temporal period so that health officers can detect emerging outbreak trends early.',
        'SH-01, SH-03',
        'HMW-01, HMW-09',
        'Must',
        'Verified in demo: user can select any combination of disease, state, and year to see correct aggregated case counts matching raw sums.'
    ],
    [
        'BR-02',
        'The business needs to compare disease burden across states on a common scale so that hospital administrators can anticipate inter-state patient surge patterns.',
        'SH-02',
        'HMW-02',
        'Must',
        'Regional ranking display accurately orders all 10 states by total incidence for any selected disease.'
    ],
    [
        'BR-03',
        'The business needs to compute and display Case Fatality Rates (CFR) across diseases and regions so that policy makers can identify high-mortality zones and justify emergency resource deployment.',
        'SH-03',
        'HMW-03',
        'Must',
        'CFR percentage matches (Deaths / Cases * 100) across all disease-region pairs; 0 division handled gracefully without error.'
    ],
    [
        'BR-04',
        'The business needs to segment disease morbidity by age bracket and gender cohort so that epidemiologists can identify demographic vulnerability profiles.',
        'SH-04',
        'HMW-04',
        'Must',
        'Demographic breakdown displays distribution across 5 age groups and 3 gender categories with totals reconciling to overall cases.'
    ],
    [
        'BR-05',
        'The business needs to detect and flag concurrent outbreaks where multiple diseases cross threshold levels simultaneously in the same region and time frame so that response teams avoid overwhelmed local healthcare capacity.',
        'SH-01, SH-04',
        'HMW-05',
        'Must',
        'Co-occurrence analysis correctly identifies region-months having two or more diseases exceeding 1.5x regional historical mean.'
    ],
    [
        'BR-06',
        'The business needs to profile monthly and seasonal variations in disease incidence so that medical supply chains can pre-position therapeutics ahead of peak months.',
        'SH-01, SH-04',
        'HMW-06',
        'Must',
        'Seasonal profile reveals peak transmission months for each disease (e.g., monsoon peak for vector-borne diseases).'
    ],
    [
        'BR-07',
        'The business needs to compute recovery percentages per disease and region so that hospital networks can benchmark clinical recovery efficacy against regional averages.',
        'SH-02',
        'HMW-07',
        'Must',
        'Recovery rate matches (Recoveries / Cases * 100); all reported values fall between 0.0% and 100.0%.'
    ],
    [
        'BR-08',
        'The business needs to evaluate the correlation between disease incidence rate and population density so that researchers can quantify the impact of urban crowding on transmission.',
        'SH-04',
        'HMW-08',
        'Should',
        'Displays scatter correlation with calculated Pearson correlation coefficient (r) and statistical p-value.'
    ],
    [
        'BR-09',
        'The business needs to calculate year-over-year (YoY) percentage changes in reported cases per disease so that ministries can assess multi-year disease growth or containment.',
        'SH-03',
        'HMW-09',
        'Should',
        'YoY percentage change table accurately computes ((Cases_Yr - Cases_Yr-1) / Cases_Yr-1 * 100) for all consecutive year pairs.'
    ],
    [
        'BR-10',
        'The business needs to maintain disease intelligence in a standardized, relational data store so that analytical queries are consistent, auditable, and reproducible.',
        'SH-05',
        'HMW-10',
        'Must',
        'Relational data repository passes primary key, foreign key, not null, and non-negative integrity validations.'
    ],
    [
        'BR-11',
        'The business needs synchronized multidimensional filtering (disease, region, year, age, gender) that updates all visual perspectives concurrently so that analytical exploration is fluid.',
        'SH-01..04',
        'HMW-01..05',
        'Must',
        'Applying a filter instantly cascades to all operational views and charts without page reload or state loss.'
    ],
    [
        'BR-12',
        'The business needs to export filtered analytical datasets into standard spreadsheet formats so that researchers can conduct specialized external epidemiological modeling.',
        'SH-04, SH-05',
        'HMW-10',
        'Should',
        'Export action produces a valid, non-empty CSV/Excel file containing exactly the subset of records active in the current filter state.'
    ],
    [
        'BR-13',
        'The business needs a transparent data quality accounting ledger showing cleaning interventions (missing values imputed, duplicates removed, outliers bounded) so that data integrity is demonstrable.',
        'SH-05',
        'HMW-10',
        'Could',
        'Data quality screen itemizes initial row count, duplicates purged, nulls resolved, and outliers capped.'
    ],
    [
        'BR-14',
        'The business needs comprehensive automated verification test suites covering data ingestion, KPI calculations, and interface responsiveness so that operational errors are caught prior to evaluation.',
        'SH-06',
        'All HMWs',
        'Must',
        'Test suite executes with >= 80% coverage and zero critical calculation failures.'
    ],
    [
        'BR-15',
        'The business needs the analytical platform hosted on an accessible cloud platform with public access so that evaluating mentors and external reviewers can inspect the system remotely.',
        'SH-05, SH-06',
        'OBJ-04',
        'Should',
        'Platform URL is publicly reachable over HTTPS with 99% availability during evaluation period.'
    ],
]

t_br = doc.add_table(rows=len(br_data) + 1, cols=6)
format_table(
    t_br,
    [Cm(1.8), Cm(5.5), Cm(2.2), Cm(2.2), Cm(1.8), Cm(3.5)],
    br_headers,
    br_data,
    priority_col=4
)

doc.add_paragraph()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 3. DATA REQUIREMENTS PER BR
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
add_styled_heading(doc, '3. Data Elements Required per Requirement', level=1)
p_dr = doc.add_paragraph('Each business requirement depends on specific data attributes from the healthcare data model:')
p_dr.runs[0].font.size = Pt(10)

dr_headers = ['BR ID', 'Required Data Entities & Attributes', 'Domain Type', 'Granularity']
dr_data = [
    ['BR-01', 'Disease Name, State/Region Name, Report Date, Report Year, Case Count', 'Epidemiological / Geospatial', 'Monthly per State & Disease'],
    ['BR-02', 'State Name, State Code, Geographic Zone, Case Count, Normalised Incidence', 'Geospatial / Clinical', 'Aggregated per State'],
    ['BR-03', 'Disease Name, Region Name, Cases Reported, Deaths Reported, CFR Calculated', 'Clinical Outcome', 'Monthly per Disease-Region cell'],
    ['BR-04', 'Age Group (0-14, 15-29, 30-44, 45-59, 60+), Gender (Male, Female, Other), Cases', 'Demographic Cohort', 'Demographic breakdown per Case record'],
    ['BR-05', 'Date (Year-Month), Region Name, Multiple Disease Case Counts, Historical Baseline', 'Outbreak Surveillance', 'Monthly Region-level Multi-disease index'],
    ['BR-06', 'Report Month (1-12), Disease Name, Monthly Aggregated Case Count, 5-Yr Mean', 'Seasonal / Temporal', 'Monthly cyclic series (Jan–Dec)'],
    ['BR-07', 'Cases Reported, Recovered Count, Recovery Percentage, Region, Disease', 'Clinical Outcome', 'Monthly per State & Disease'],
    ['BR-08', 'State Population, State Area (sq. km), Population Density, Incidence per Lakh', 'Demographic / Spatial', 'Annual State-level derived metric'],
    ['BR-09', 'Disease Name, Annual Total Cases for 2020, 2021, 2022, 2023, 2024, YoY % Delta', 'Temporal / Trend', 'Annual per Disease'],
    ['BR-10', 'Primary Keys, Foreign Keys, Timestamp, Audit Source, Integrity Rules', 'Relational Schema', 'Table / View Level'],
    ['BR-11', 'Filter Dimensions: Disease List, State Multi-select, Year Range, Demographics', 'Analytical State', 'Session State UI bindings'],
    ['BR-12', 'Full Filtered Record Set in tabular format with Column Headers', 'Export Data Stream', 'Filtered row-level records'],
    ['BR-13', 'Raw Row Count, Clean Row Count, Duplicates Count, Null Count, Outlier Count', 'Data Quality Audit', 'Data Pipeline Metadata'],
    ['BR-14', 'Test Vectors: Known inputs, Expected outputs, Assertion thresholds', 'Quality Assurance', 'Unit & Integration Test Suite'],
    ['BR-15', 'Deployment Package, Pinned Dependency Manifest, Entry Point Script', 'DevOps / Release', 'Cloud Repository Asset'],
]

t_dr = doc.add_table(rows=len(dr_data) + 1, cols=4)
format_table(t_dr, [Cm(1.8), Cm(7.2), Cm(4.0), Cm(3.5)], dr_headers, dr_data)

doc.add_paragraph()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 4. TRACEABILITY & GAP ANALYSIS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
add_styled_heading(doc, '4. Traceability & Gap Analysis', level=1)
p_gap = doc.add_paragraph(
    'To guarantee end-to-end alignment, a bidirectional traceability audit was conducted '
    'between HMW statements, Business Requirements, and the 10 Operational Questions:'
)
p_gap.runs[0].font.size = Pt(10)

gap_headers = ['Audit Check', 'Evaluation Finding', 'Status', 'Remediation / Justification']
gap_data = [
    [
        'HMW without BR',
        'All 10 HMW statements (HMW-01 through HMW-10) have at least one corresponding Business Requirement.',
        'PASSED',
        'None needed. Complete coverage verified.'
    ],
    [
        'BR without HMW',
        'Requirements BR-01 through BR-13 trace directly to HMW-01..10. BR-14 traces to overall QA objectives. BR-15 traces to project objective OBJ-04.',
        'PASSED',
        'All 15 BRs justified by user need or project charter objectives.'
    ],
    [
        'OQ Coverage',
        'All 10 Operational Questions (OQ-01 through OQ-10) are directly supported by one or more Must-Have BRs.',
        'PASSED',
        'Every OQ is verifiable through specific business requirement acceptance criteria.'
    ],
    [
        'MoSCoW Balance',
        'Must: 9 (60.0%), Should: 4 (26.7%), Could: 2 (13.3%), Won\'t: 0 (0.0%).',
        'PASSED',
        'Adheres exactly to software engineering best practices (~60% Must requirements).'
    ],
]

t_gap = doc.add_table(rows=len(gap_data) + 1, cols=4)
format_table(t_gap, [Cm(3.0), Cm(6.5), Cm(2.5), Cm(4.5)], gap_headers, gap_data)

doc.add_paragraph()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 5. MOSCOW PRIORITY SUMMARY
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
add_styled_heading(doc, '5. MoSCoW Priority Distribution', level=1)
p_moscow = doc.add_paragraph(
    'The requirements prioritization ensures delivery of a robust Minimum Viable Product (MVP) '
    'while clearly defining subsequent enhancements:'
)
p_moscow.runs[0].font.size = Pt(10)

moscow_headers = ['MoSCoW Level', 'Count', 'Percentage', 'Requirements Included', 'Strategic Purpose']
moscow_data = [
    ['Must Have', '9', '60.0%', 'BR-01, BR-02, BR-03, BR-04, BR-05, BR-06, BR-07, BR-10, BR-11, BR-14', 'Core analytical capabilities required to answer all 10 OQs; non-negotiable for project evaluation.'],
    ['Should Have', '4', '26.7%', 'BR-08, BR-09, BR-12, BR-15', 'High-value analytical enhancements (correlation, YoY tables, CSV export, cloud hosting).'],
    ['Could Have', '2', '13.3%', 'BR-13', 'Desirable quality features (visual data cleaning ledger) included if schedule permits.'],
    ['Won\'t Have', '0', '0.0%', 'Real patient PII, Predictive AI forecasting, Mobile app, User authentication', 'Formally deferred to Phase 2 (post-semester).'],
]

t_moscow = doc.add_table(rows=len(moscow_data) + 1, cols=5)
format_table(t_moscow, [Cm(2.5), Cm(1.5), Cm(2.0), Cm(4.5), Cm(6.0)], moscow_headers, moscow_data)

doc.add_paragraph()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FOOTER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
p_foot = doc.add_paragraph()
p_foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
rn_f = p_foot.add_run('03_ArgJain_DiseaseTrendAnalysis_NeedsAnalysis.docx | v1.0 | ABES Engineering College | November 2026')
rn_f.font.size = Pt(8)
rn_f.font.color.rgb = RGBColor(0x88, 0x88, 0x88)

save_path = r'c:\Users\Hp\Downloads\hcl\docs\03_ArgJain_DiseaseTrendAnalysis_NeedsAnalysis.docx'
doc.save(save_path)
print(f'SAVED: {save_path}')
