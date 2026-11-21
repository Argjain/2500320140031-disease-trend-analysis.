import os
import docx
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment

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
run_sub = p_sub.add_run('STEP 11 — Agile User Stories & Acceptance Criteria')
run_sub.font.size = Pt(14)
run_sub.font.bold = True
run_sub.font.color.rgb = RGBColor(0x2E, 0x86, 0xAB)

doc.add_paragraph()

meta_data = [
    ('Project ID & Title', 'P100 | Disease Trend Analysis'),
    ('Domain', 'Healthcare Data Analytics'),
    ('Product Owner / Student', 'Arg Jain (Roll No. 2500320140031)'),
    ('Academic Program', 'MCA 2nd Year (Data Analytics Specialization)'),
    ('Institution', 'ABES Engineering College, Ghaziabad'),
    ('Faculty Mentor', 'Mr. Dinesh'),
    ('Document Version', 'v1.0'),
    ('Epics Total', '5 Epics (Data, Dashboard, Trends, Demographics, Quality)'),
    ('User Stories Count', '17 Granular Stories (All <= 0.5 Day Velocity)'),
    ('Total Story Points', '46 Points (Fibonacci scale: 1, 2, 3, 5)'),
    ('Release Date', 'November 2026'),
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
# 1. EPIC OVERVIEW
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
add_heading_1('1. Epics Hierarchy & Story Point Distribution')
p_epic_intro = doc.add_paragraph(
    'User stories are grouped into 5 cohesive functional Epics spanning the analytical product lifecycle. '
    'Estimation follows Fibonacci sizing (1 to 5 story points) where 1 story point equals approximately 1-2 hours of engineering effort:'
)
p_epic_intro.runs[0].font.size = Pt(10)

epic_data = [
    ['EP-01', 'Data Infrastructure & Ingestion', 'SQLite schema initialization, cached data loaders, cleaning pipeline, and session state initialization', 3, 8, 'Must'],
    ['EP-02', 'Executive Dashboard & KPI Cockpit', 'Executive stat cards, regional morbidity bar rankings, and state-level CFR matrices', 4, 10, 'Must'],
    ['EP-03', 'Longitudinal & Cyclical Trend Analytics', '5-year monthly time-series, overlapping YoY comparisons, and 12-month seasonal transmission heatmaps', 4, 11, 'Must'],
    ['EP-04', 'Regional Benchmarking & Demographic Drilldown', 'Horizontal state CFR comparisons, age cohort stacked bars, and gender distribution analysis', 3, 9, 'Must'],
    ['EP-05', 'Advanced Insights & Data Governance', 'Density correlation regression, multi-disease concurrent outbreak detection, data quality ledger, and CSV export', 3, 8, 'Should / Could'],
]
t_epic = doc.add_table(rows=len(epic_data) + 1, cols=6)
format_table(t_epic, [Cm(1.8), Cm(4.5), Cm(6.5), Cm(1.5), Cm(1.5), Cm(2.2)], ['Epic ID', 'Epic Name', 'Functional Scope', 'Stories', 'Points', 'Priority'], epic_data, priority_col=5)
doc.add_paragraph()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 2. COMPLETE USER STORIES REGISTER (US-01 to US-17)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
add_heading_1('2. Agile User Stories Register')
p_us_intro = doc.add_paragraph(
    'Every user story is structured in the formal agile template: "As a <persona>, I want <goal> so that <benefit>." '
    'Each story traces directly to architectural feature IDs and upstream business requirements:'
)
p_us_intro.runs[0].font.size = Pt(10)

stories_data = [
    ['US-01', 'EP-01', 'Student Developer', 'As a student developer, I want the app to load all epidemiological records from SQLite into memory on startup using cache decorators, so that repeated page visits avoid slow database reads.', 'FR-01', 'BR-10', 'Must', '3'],
    ['US-02', 'EP-01', 'Student Developer', 'As a student developer, I want an automated cleaning pipeline to purge duplicate records, impute null values, and bound extreme outliers, so that downstream statistical calculations operate on reliable data.', 'FR-01', 'BR-13', 'Must', '3'],
    ['US-03', 'EP-01', 'Public Health Officer', 'As a public health officer, I want centralized sidebar filters (disease, state, year range, age, gender) bound to session state, so that selecting a filter cascade-updates all pages consistently.', 'FR-02', 'BR-11', 'Must', '2'],
    ['US-04', 'EP-02', 'Public Health Officer', 'As a public health officer, I want four high-level KPI cards on the Overview page displaying Total Cases, Fatalities, Recoveries, and Case Fatality Rate, so that I get an immediate situation snapshot.', 'FR-12', 'BR-01', 'Must', '3'],
    ['US-05', 'EP-02', 'Public Health Officer', 'As a public health officer, I want a prominent alert badge identifying the disease with the steepest year-over-year percentage increase, so that I immediately know which threat is expanding fastest.', 'FR-11', 'BR-09', 'Must', '2'],
    ['US-06', 'EP-02', 'Hospital Administrator', 'As a hospital administrator, I want a ranked bar chart of disease cases across all 10 states, so that I can identify which regions bear the greatest clinical volume.', 'FR-04', 'BR-02', 'Must', '2'],
    ['US-07', 'EP-02', 'Policy Maker', 'As a policy maker, I want a matrix heatmap of Case Fatality Rates cross-tabulated by disease and state, so that I can spot geographic mortality hot spots requiring emergency funding.', 'FR-05', 'BR-03', 'Must', '3'],
    ['US-08', 'EP-03', 'Public Health Officer', 'As a public health officer, I want an interactive monthly time-series line chart with zoom and hover tooltips, so that I can inspect outbreak velocity over the full 60-month historical timeline.', 'FR-08', 'BR-06', 'Must', '3'],
    ['US-09', 'EP-03', 'Epidemiologist', 'As an epidemiologist, I want an overlapping year-over-year line chart where years 2020 through 2024 are plotted as distinct series across months 1-12, so that I can detect multi-year wave anomalies.', 'FR-03', 'BR-01', 'Must', '3'],
    ['US-10', 'EP-03', 'Policy Maker', 'As a policy maker, I want a formatted table displaying annual case counts and YoY percentage deltas with color-coded direction indicators, so that I can evaluate long-term public health containment trends.', 'FR-11', 'BR-09', 'Must', '2'],
    ['US-11', 'EP-03', 'Epidemiologist', 'As an epidemiologist, I want a 12-month seasonal transmission heatmap plotting calendar months on the horizontal axis and diseases on the vertical axis, so that I can pinpoint seasonal surge windows.', 'FR-08', 'BR-06', 'Should', '3'],
    ['US-12', 'EP-04', 'Hospital Administrator', 'As a hospital administrator, I want a comparative bar chart displaying regional Case Fatality Rates alongside recovery percentages, so that I can benchmark state hospital clinical efficacy.', 'FR-05', 'BR-03', 'Must', '3'],
    ['US-13', 'EP-04', 'Epidemiologist', 'As an epidemiologist, I want stacked bar charts breaking down morbidity across 5 age brackets and gender cohorts, so that I can determine demographic vulnerability profiles for targeted advisories.', 'FR-06', 'BR-04', 'Must', '3'],
    ['US-14', 'EP-05', 'Epidemiologist', 'As an epidemiologist, I want a scatter plot correlating state population density against disease incidence rate with an OLS linear trendline and Pearson r value, so that I can quantify the impact of urban crowding.', 'FR-10', 'BR-08', 'Should', '3'],
    ['US-15', 'EP-05', 'Public Health Officer', 'As a public health officer, I want an automated surveillance detector alerting whenever two or more diseases concurrently exceed 1.5x their historical mean in the same state-month, so that response teams can avert triage collapse.', 'FR-07', 'BR-05', 'Must', '5'],
    ['US-16', 'EP-05', 'Epidemiologist', 'As an epidemiologist, I want a one-click CSV export button on the Data screen, so that I can download the filtered analytical slice for offline statistical modeling in external software.', 'FR-14', 'BR-12', 'Should', '1'],
    ['US-17', 'EP-05', 'Student Developer', 'As a student developer, I want a transparent Data Quality screen displaying pre-cleaning and post-cleaning metrics (nulls filled, duplicates dropped, outliers capped), so that the mentor can evaluate data engineering rigor.', 'FR-15', 'BR-13', 'Could', '2'],
]

t_us = doc.add_table(rows=len(stories_data) + 1, cols=8)
format_table(t_us, [Cm(1.5), Cm(1.5), Cm(2.2), Cm(6.0), Cm(1.5), Cm(1.5), Cm(1.5), Cm(1.3)], ['US ID', 'Epic', 'Persona', 'User Story Narrative', 'FR ID', 'BR ID', 'Priority', 'Points'], stories_data, priority_col=6)
doc.add_paragraph()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 3. ACCEPTANCE CRITERIA (Given / When / Then)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
add_heading_1('3. Acceptance Criteria in Given-When-Then Specification')
p_ac_intro = doc.add_paragraph('Formal behavioral acceptance specifications for each user story:')
p_ac_intro.runs[0].font.size = Pt(10)

ac_data = [
    ['US-01', 'Given data/app.db exists on disk', 'When the Streamlit application initializes', 'Then all tables are queried into memory within 3.0s and cached via @st.cache_data.'],
    ['US-02', 'Given raw data contains 54 null cases and 3 duplicates', 'When the clean_data() function is executed', 'Then duplicates are removed, nulls are median-imputed, and an audit dict is generated.'],
    ['US-03', 'Given the user is on the Overview page', 'When the user selects "Dengue" in the sidebar', 'Then moving to the Trends or Regional page retains "Dengue" without resetting filters.'],
    ['US-04', 'Given the user accesses the Overview screen', 'When the page renders with active filters', 'Then 4 KPI cards display Total Cases, Deaths, Recoveries, and CFR % formatted to 2 decimals.'],
    ['US-05', 'Given multi-year disease case history', 'When the overview statistics are computed', 'Then an alert badge highlights the disease exhibiting the highest positive YoY percentage growth.'],
    ['US-06', 'Given regional case aggregation is active', 'When the regional chart is displayed', 'Then all 10 states are ranked horizontally in descending order of total incident volume.'],
    ['US-07', 'Given case and mortality totals across state-disease pairs', 'When the CFR matrix heatmap is selected', 'Then each cell renders CFR% = (deaths/cases*100) with color scaling from low to high risk.'],
    ['US-08', 'Given 60 months of historical case records', 'When the user navigates to the Trends screen', 'Then an interactive Plotly line chart renders monthly points with hover metadata.'],
    ['US-09', 'Given multiple years of monthly transmission data', 'When the user enables the YoY comparison view', 'Then years 2020-2024 are plotted as 5 separate lines across months 1-12 on one chart.'],
    ['US-10', 'Given annual aggregated case records', 'When the YoY growth table is rendered', 'Then percentage changes are displayed with green indicators for decline and red for surge.'],
    ['US-11', 'Given monthly cyclical aggregates for all 5 diseases', 'When the seasonal heatmap is generated', 'Then monsoon peak transmission for vector-borne diseases (Jul-Sep) is visually distinct.'],
    ['US-12', 'Given state-level mortality and recovery records', 'When the Regional Analysis screen is viewed', 'Then recovery rates and CFR percentages are displayed side by side per state.'],
    ['US-13', 'Given demographic breakdown table data', 'When the Demographics screen is loaded', 'Then cases are partitioned into stacked bars across 5 age groups and 3 gender categories.'],
    ['US-14', 'Given state population density and incidence rates', 'When the correlation scatter plot is generated', 'Then an OLS linear trendline renders along with computed Pearson r and p-value.'],
    ['US-15', 'Given temporal state case data across all diseases', 'When the concurrent outbreak algorithm runs', 'Then state-months where >= 2 diseases exceed 1.5x monthly mean are flagged in a table.'],
    ['US-16', 'Given the active filter state on the Data screen', 'When the user clicks the "Download CSV" button', 'Then a valid non-empty CSV containing the filtered subset is saved to the local machine.'],
    ['US-17', 'Given data cleaning execution metrics', 'When the Data Quality screen is opened', 'Then a scorecard itemizes original rows, duplicates purged, nulls filled, and outliers bounded.'],
]

t_ac = doc.add_table(rows=len(ac_data) + 1, cols=4)
format_table(t_ac, [Cm(1.8), Cm(4.5), Cm(4.5), Cm(6.2)], ['US ID', 'Given (Precondition)', 'When (User Action / Trigger)', 'Then (Expected Behavioral Outcome)'], ac_data)
doc.add_paragraph()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 4. SPRINT ROADMAP & TIMELINE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
add_heading_1('4. Sprint Roadmap & Implementation Schedule')
p_sp_intro = doc.add_paragraph('The 17 user stories are scheduled across an 8-day engineering sprint roadmap:')
p_sp_intro.runs[0].font.size = Pt(10)

sprint_data = [
    ['Day 1', 'US-01, US-02, US-03', 'EP-01 (Data Infrastructure)', 'SQLite database connection, caching loader, cleaning pipeline, and session state sidebar.'],
    ['Day 2', 'US-04, US-05, US-06, US-07', 'EP-02 (Dashboard & KPIs)', 'Overview page with 4 Tailwind KPI cards, regional case bar ranking, and initial CFR heatmap.'],
    ['Day 3', 'US-08, US-09', 'EP-03 (Longitudinal Trends)', 'Trends page with 60-month time-series line chart and multi-year overlapping YoY curves.'],
    ['Day 4', 'US-10, US-11', 'EP-03 (Seasonal Heatmaps)', 'Formatted YoY percentage delta table and 12-month cyclic transmission intensity heatmap.'],
    ['Day 5', 'US-12, US-13', 'EP-04 (Demographics & Regions)', 'Comparative regional recovery/CFR charts and stacked demographic age/gender distribution.'],
    ['Day 6', 'US-14, US-15', 'EP-05 (Advanced Insights)', 'Density correlation scatter with OLS trendline and multi-disease concurrent outbreak surveillance.'],
    ['Day 7', 'US-16, US-17', 'EP-05 (Quality & Export)', 'Data Quality audit ledger page and one-click filtered CSV dataset export mechanism.'],
    ['Day 8', 'Quality Assurance & Release', 'Full Test Suite & Deploy', 'Execute pytest verification suite (>=80% coverage), resolve regressions, and deploy to Cloud.'],
]
t_sp = doc.add_table(rows=len(sprint_data) + 1, cols=4)
format_table(t_sp, [Cm(1.8), Cm(3.5), Cm(4.5), Cm(7.2)], ['Sprint Day', 'Target Stories', 'Epic Focus', 'Key Milestone Deliverables'], sprint_data)
doc.add_paragraph()

p_foot = doc.add_paragraph()
p_foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
rn_f = p_foot.add_run('11_ArgJain_DiseaseTrendAnalysis_UserStories.docx | v1.0 | ABES Engineering College | November 2026')
rn_f.font.size = Pt(8)
rn_f.font.color.rgb = RGBColor(0x88, 0x88, 0x88)

save_path = r'c:\Users\Hp\Downloads\hcl\docs\11_ArgJain_DiseaseTrendAnalysis_UserStories.docx'
doc.save(save_path)
print(f'SAVED DOCX: {save_path}')

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ALSO UPDATE RTM with "User Story ID"
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
rtm_path = r'c:\Users\Hp\Downloads\hcl\docs\04_ArgJain_DiseaseTrendAnalysis_RTM.xlsx'
if os.path.exists(rtm_path):
    wb_rtm = load_workbook(rtm_path)
    ws_r = wb_rtm['RTM']
    
    us_mapping = {
        'BR-01': 'US-04, US-09',
        'BR-02': 'US-06',
        'BR-03': 'US-07, US-12',
        'BR-04': 'US-13',
        'BR-05': 'US-15',
        'BR-06': 'US-08, US-11',
        'BR-07': 'US-12',
        'BR-08': 'US-14',
        'BR-09': 'US-05, US-10',
        'BR-10': 'US-01',
        'BR-11': 'US-03',
        'BR-12': 'US-16',
        'BR-13': 'US-02, US-17',
        'BR-14': 'All Stories',
        'BR-15': 'All Stories',
    }
    
    for row in range(2, ws_r.max_row + 1):
        br_id = ws_r.cell(row=row, column=3).value
        if br_id in us_mapping:
            cell = ws_r.cell(row=row, column=10)
            cell.value = us_mapping[br_id]
            cell.font = Font(name='Calibri', size=10)
            cell.fill = PatternFill(start_color='FFFFFF', end_color='FFFFFF', fill_type='solid')
            cell.alignment = Alignment(horizontal='center', vertical='center')
            
    # Update Change Log
    ws_log = wb_rtm['Change_Log']
    for r in range(2, ws_log.max_row + 1):
        if ws_log.cell(row=r, column=1).value == 'v1.2':
            ws_log.cell(row=r, column=2, value='18-Nov-2026')
            ws_log.cell(row=r, column=5, value='Populated User Story IDs (US-01..US-17) and Sprint Epics.')
            
    wb_rtm.save(rtm_path)
    print(f'UPDATED RTM: {rtm_path} (User Story ID populated)')
