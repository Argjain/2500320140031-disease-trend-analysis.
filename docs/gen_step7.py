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

def format_table(table, col_widths, headers, data):
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

def add_code_block(code_text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.5)
    p.paragraph_format.right_indent = Cm(0.5)
    run = p.add_run(code_text)
    run.font.name = 'Consolas'
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor(0x2C, 0x3E, 0x50)

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
run_sub = p_sub.add_run('STEP 7 — Technical Requirements Document (TRD)')
run_sub.font.size = Pt(14)
run_sub.font.bold = True
run_sub.font.color.rgb = RGBColor(0x2E, 0x86, 0xAB)

doc.add_paragraph()

meta_data = [
    ('Project ID & Title', 'P-01 | Disease Trend Analysis'),
    ('Domain', 'Healthcare Data Analytics'),
    ('Student Architect', 'Arg Jain (Roll No. 2500320140031)'),
    ('Academic Program', 'MCA 2nd Year (Data Analytics Specialization)'),
    ('Institution', 'ABES Engineering College, Ghaziabad'),
    ('Faculty Mentor', 'Ms. Kalpana Dwivedi'),
    ('Document Version', 'v1.0 (Baseline Architecture)'),
    ('Technical Stack', 'Python 3.12 | Streamlit 1.35 | SQLite | Plotly 5.22 | pytest 8.2'),
    ('Deployment Target', 'Streamlit Community Cloud (Free Tier)'),
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
# 1. SYSTEM ARCHITECTURE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
add_heading_1('1. System Architecture & End-to-End Data Pipeline')
p_arch = doc.add_paragraph(
    'The Disease Trend Analysis system is designed following a modular multi-tier data analytics architecture. '
    'The pipeline cleanly separates the relational storage tier, caching data ingestion layer, idempotent data cleaning engine, '
    'vectorized statistical analytics module, Tailwind UI component rendering layer, and reactive multi-page presentation screens.'
)
p_arch.runs[0].font.size = Pt(10)

add_heading_2('1.1 Architecture Flowchart (Mermaid Representation)')
code_mermaid = (
    "graph TD\n"
    "    A[data/app.db (SQLite)] -->|SQL Query| B[src/data_loader.py (@st.cache_data)]\n"
    "    B -->|Raw DataFrame| C[src/cleaning.py (Impute, Dedupe, Cap Outliers)]\n"
    "    C -->|Cleaned DataFrame + Quality Report| D[src/analysis.py (CFR, YoY, Seasonality, Stats)]\n"
    "    D -->|Aggregated Data & Metrics| E[app.py (Shared Sidebar Filters & Session State)]\n"
    "    E -->|Filtered State & Slices| F1[pages/01_Overview.py (KPI Cards & Bar Chart)]\n"
    "    E -->|Filtered State & Slices| F2[pages/02_Trends.py (Time-series & Heatmap)]\n"
    "    E -->|Filtered State & Slices| F3[pages/03_Regional_Analysis.py (CFR & Recovery)]\n"
    "    E -->|Filtered State & Slices| F4[pages/04_Demographics.py (Age & Gender Stacked)]\n"
    "    E -->|Filtered State & Slices| F5[pages/05_EDA_Statistics.py (Correlation & Outbreak)]\n"
    "    E -->|Filtered State & Slices| F6[pages/06_Data_Quality.py (Audit & CSV Export)]\n"
    "    G[src/ui.py (Tailwind CDN in iframe)] -.->|CSS Classes & Cards| F1 & F2 & F3 & F4 & F5 & F6\n"
)
add_code_block(code_mermaid)

add_heading_2('1.2 Pipeline Component Responsibilities')
p_pipe = doc.add_paragraph(
    '1. Relational Persistence (data/app.db): SQLite database enforcing PK/FK relationships, domain check constraints, and denormalized analytical views.\n'
    '2. Ingestion & Cache (src/data_loader.py): Connects using sqlite3, executes indexed analytical queries, and caches results via @st.cache_data(ttl=3600).\n'
    '3. Cleaning Pipeline (src/cleaning.py): Drops exact duplicate rows, imputes missing counts via median/zero, caps extreme outlier spikes, and generates an audit dictionary.\n'
    '4. Analytical Engine (src/analysis.py): Pure Python/pandas/SciPy mathematical functions computing epidemiological metrics with zero UI dependencies.\n'
    '5. UI Component Library (src/ui.py): Renders Tailwind CSS styled KPI stat cards, alert callouts, and header components through Streamlit iframe components.\n'
    '6. Presentation Tier (app.py and pages/): Native Streamlit multi-page layout rendering Plotly interactive visualizations with responsive column grids.'
)
p_pipe.runs[0].font.size = Pt(9.5)
doc.add_paragraph()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 2. FOLDER & CODEBASE STRUCTURE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
add_heading_1('2. Folder Structure & Physical Organization')
code_tree = (
    "2500320140031-disease-trend-analysis/\n"
    "├── app.py                     # Main application entry point & shared session state\n"
    "├── requirements.txt           # Pinned dependency manifest\n"
    "├── BUILD_PLAN.md              # Machine-actionable build roadmap\n"
    "├── README.md                  # Installation, testing & deployment guide\n"
    "├── .gitignore                 # Excludes .venv, __pycache__, temporary caches\n"
    "├── .streamlit/\n"
    "│   └── config.toml            # Application theme (colors, fonts, layout settings)\n"
    "├── src/\n"
    "│   ├── __init__.py            # Package initializer\n"
    "│   ├── data_loader.py         # SQLite connection & cached queries\n"
    "│   ├── cleaning.py            # Data sanitization, imputation & outlier bounds\n"
    "│   ├── analysis.py            # Epidemiological & statistical analysis routines\n"
    "│   ├── ui.py                  # Tailwind iframe components & visual cards\n"
    "│   └── generate_data.py       # Deterministic synthetic data generator (seed 42)\n"
    "├── pages/\n"
    "│   ├── 01_Overview.py         # Executive KPI dashboard & regional case rankings\n"
    "│   ├── 02_Trends.py           # Longitudinal time-series & seasonal heatmaps\n"
    "│   ├── 03_Regional_Analysis.py# Cross-state CFR benchmarking & recovery rates\n"
    "│   ├── 04_Demographics.py      # Age cohort & gender distribution profiles\n"
    "│   ├── 05_EDA_Statistics.py   # Density scatter correlation & co-occurrence surveillance\n"
    "│   └── 06_Data_Quality.py     # Pipeline cleaning audit ledger & raw CSV export\n"
    "├── data/\n"
    "│   ├── app.db                 # SQLite relational database file\n"
    "│   ├── disease_cases.csv      # Flat CSV export of primary fact table\n"
    "│   ├── region_master.csv      # State reference metadata & census population\n"
    "│   ├── disease_master.csv     # Disease taxonomic taxonomy & incubation stats\n"
    "│   ├── demographic_group.csv  # Age & gender cohort master definitions\n"
    "│   └── disease_trend_analysis_data.xlsx # Multi-tab complete spreadsheet\n"
    "├── tests/\n"
    "│   ├── __init__.py            # Test suite package initializer\n"
    "│   ├── test_data.py           # Database schema, row count & FK constraint tests\n"
    "│   ├── test_analysis.py       # Pure mathematical assertions on analytical formulas\n"
    "│   └── test_app.py            # Streamlit AppTest integration & UI smoke tests\n"
    "└── docs/                      # All 18 formal project step deliverables (.docx, .xlsx)\n"
)
add_code_block(code_tree)
doc.add_paragraph()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 3. FUNCTIONAL REQUIREMENTS (FR-01 to FR-15)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
add_heading_1('3. Functional Requirements Register')
p_fr = doc.add_paragraph('Engineering implementation specifications mapped directly to source Business Requirements:')
p_fr.runs[0].font.size = Pt(10)

fr_headers = ['FR ID', 'Technical Requirement', 'Linked BR', 'Target Module', 'Implementation Method']
fr_data = [
    ['FR-01', 'Load multi-table joined disease dataset from SQLite with caching', 'BR-10', 'src/data_loader.py', 'sqlite3 connection + @st.cache_data(ttl=3600)'],
    ['FR-02', 'Synchronize global sidebar filter selections across all sub-pages', 'BR-11', 'app.py / src/data_loader.py', 'st.session_state filter binding with persistent state keys'],
    ['FR-03', 'Compute multi-year annual and monthly case frequency aggregations', 'BR-01', 'src/analysis.py', 'df.groupby([\'disease_name\', \'report_year\'])[\'cases_reported\'].sum()'],
    ['FR-04', 'Generate sorted state-level case burden rankings', 'BR-02', 'src/analysis.py', 'Groupby region_name, sort descending, render px.bar(orientation=\'h\')'],
    ['FR-05', 'Calculate matrix of Case Fatality Rates (CFR) across state-disease pairs', 'BR-03', 'src/analysis.py', '(deaths / cases_reported * 100).fillna(0.0), render px.imshow'],
    ['FR-06', 'Disaggregate cases across 5 age brackets and 3 gender identities', 'BR-04', 'src/analysis.py', 'Pivot table on demographic_breakdown, render px.bar(barmode=\'stack\')'],
    ['FR-07', 'Identify co-occurring outbreak anomalies across regional temporal cells', 'BR-05', 'src/analysis.py', 'Flag cells where count(diseases > 1.5 * historical_mean) >= 2'],
    ['FR-08', 'Construct 12-month cyclical transmission profiles per disease', 'BR-06', 'src/analysis.py', 'Groupby report_month (1-12) mean cases, render px.imshow & px.line'],
    ['FR-09', 'Compute clinical recovery percentages per state and disease', 'BR-07', 'src/analysis.py', '(recovered / cases_reported * 100).clip(0, 100), render px.bar'],
    ['FR-10', 'Calculate Pearson correlation coefficient between density and incidence', 'BR-08', 'src/analysis.py', 'scipy.stats.pearsonr(incidence_per_lakh, population_density)'],
    ['FR-11', 'Generate year-over-year percentage delta matrix across consecutive years', 'BR-09', 'src/analysis.py', 'Annual sum pivot table + pct_change(axis=1) * 100'],
    ['FR-12', 'Render responsive executive KPI cards (Cases, Deaths, Recoveries, CFR)', 'BR-01, BR-11', 'pages/01_Overview.py', 'render_kpi_card() HTML generation inside st.columns(4)'],
    ['FR-13', 'Render 6 interactive, responsive Plotly visual analytics chart types', 'BR-02..09', 'pages/*.py', 'Plotly Express (px.line, px.bar, px.imshow, px.scatter, px.pie)'],
    ['FR-14', 'Generate downloadable filtered CSV extract via one-click UI trigger', 'BR-12', 'pages/06_Data_Quality.py', 'st.download_button(data=df.to_csv(index=False), mime=\'text/csv\')'],
    ['FR-15', 'Render visual data cleaning accounting ledger (initial vs clean metrics)', 'BR-13', 'pages/06_Data_Quality.py', 'Tabular render of quality_report dictionary metrics'],
]
t_fr = doc.add_table(rows=len(fr_data) + 1, cols=5)
format_table(t_fr, [Cm(1.8), Cm(5.2), Cm(1.8), Cm(3.5), Cm(4.7)], fr_headers, fr_data)
doc.add_paragraph()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 4. NON-FUNCTIONAL REQUIREMENTS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
add_heading_1('4. Non-Functional Requirements (NFR-01 to NFR-08)')
p_nfr = doc.add_paragraph('System quality attributes and architectural service level objectives:')
p_nfr.runs[0].font.size = Pt(10)

nfr_headers = ['NFR ID', 'Category', 'Target Objective', 'Target Threshold', 'Verification Method']
nfr_data = [
    ['NFR-01', 'Performance', 'Initial application cold-start and database load', '< 5.0 seconds', 'Automated timer on Streamlit Community Cloud URL'],
    ['NFR-02', 'Performance', 'Visual chart re-render upon sidebar filter mutation', '< 2.0 seconds', 'Manual browser developer tools profiling'],
    ['NFR-03', 'Reliability', 'Automated test suite code coverage', '>= 80.0% Line Coverage', 'pytest --cov=src execution report'],
    ['NFR-04', 'Reliability', 'Critical computational or rendering regression failures', '0 Failures', 'pytest -q test execution output'],
    ['NFR-05', 'Usability', 'All 10 OQs resolvable without requiring external documentation', '10 / 10 OQs (100%)', 'Interactive mentor usability audit walkthrough'],
    ['NFR-06', 'Maintainability', 'Maximum functional code complexity per method', '< 50 lines of code', 'Static analysis code review inspection'],
    ['NFR-07', 'Data Privacy', 'Absolute elimination of real patient personal identifiers (PII)', '0 PII records (100% Synthetic)', 'Synthetic dataset schema validation audit'],
    ['NFR-08', 'Availability', 'Public platform availability during semester evaluation window', '>= 99.0% Uptime', 'Uptime monitoring over final 2 academic weeks'],
]
t_nfr = doc.add_table(rows=len(nfr_data) + 1, cols=5)
format_table(t_nfr, [Cm(1.8), Cm(2.8), Cm(6.0), Cm(3.2), Cm(3.2)], nfr_headers, nfr_data)
doc.add_paragraph()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 5. DATA INGESTION, CACHING & CLEANING SPECIFICATION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
add_heading_1('5. Data Ingestion, Caching & Cleaning Pipeline')

add_heading_2('5.1 Relational Data Ingestion & Caching Strategy')
p_ing = doc.add_paragraph(
    'Data loading is orchestrated via src/data_loader.py using standard library sqlite3. '
    'To optimize Streamlit Cloud runtime performance, the primary loading function is wrapped in Streamlit\'s cache manager: '
    '@st.cache_data(ttl=3600, show_spinner="Loading epidemiological repository..."). '
    'The loader connects to Path(__file__).parent.parent / "data" / "app.db", executes a validated multi-table JOIN across '
    'disease_cases, disease_master, and region_master, and returns a high-performance pandas DataFrame.'
)
p_ing.runs[0].font.size = Pt(9.5)

add_heading_2('5.2 Data Sanitization Pipeline (src/cleaning.py)')
p_cln = doc.add_paragraph(
    'The cleaning module executes four idempotent operations upon raw DataFrame ingestion:\n'
    '1. Deduplication: Invokes df.drop_duplicates() to purge redundant transactional case rows introduced during batch ingestion.\n'
    '2. Missing Value Imputation: Imputes missing cases_reported using median disease-state values. Imputes missing deaths with 0.\n'
    '3. Outlier Capping (Winsorization): Identifies extreme typographical errors using Interquartile Range (IQR). Cases exceeding Q3 + 3.0 * IQR are capped to boundary values.\n'
    '4. Audit Metric Accounting: Returns a quality report dictionary capturing original_rows, duplicates_removed, nulls_filled, outliers_capped, and final_rows.'
)
p_cln.runs[0].font.size = Pt(9.5)
doc.add_paragraph()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 6. STATISTICAL & ANALYTICAL FORMULATION PER OQ
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
add_heading_1('6. Statistical & Mathematical Formulation per Operational Question')
p_stat = doc.add_paragraph('Formal mathematical definition and algorithmic approach for resolving each Operational Question:')
p_stat.runs[0].font.size = Pt(10)

stat_headers = ['OQ ID', 'Analytical Question', 'Mathematical Formulation', 'Python Implementation', 'Visualization Engine']
stat_data = [
    ['OQ-01', '5-Year Case Growth', 'Delta = Sum(Cases_2024) - Sum(Cases_2020)', 'df.groupby([\'disease\', \'year\']).sum()', 'px.line (Multi-series time trend)'],
    ['OQ-02', 'Geographic Hotspots', 'Rank(State) = Descending(Sum(Cases))', 'df.groupby(\'region\').sum().sort_values()', 'px.bar (Horizontal ranked bar chart)'],
    ['OQ-03', 'Monthly Cyclical Trend', 'Index(m) = Mean(Cases in month m, 2020-2024)', 'df.groupby(\'report_month\').mean()', 'px.line (12-month cyclic transmission wave)'],
    ['OQ-04', 'Demographic Cohorts', 'Cases(age, gender) / Total_Cases * 100', 'df.pivot_table(index=\'age\', cols=\'gender\')', 'px.bar (Stacked demographic bar chart)'],
    ['OQ-05', 'Case Fatality Rate', 'CFR = (Deaths / Cases_Reported) * 100', '(df[\'deaths\'] / df[\'cases\'] * 100).fillna(0)', 'px.imshow (Disease x Region CFR heatmap)'],
    ['OQ-06', 'Density Correlation', 'r = Cov(Incidence, Density) / (Sigma_x * Sigma_y)', 'scipy.stats.pearsonr(inc_rate, pop_density)', 'px.scatter (Trendline OLS regression)'],
    ['OQ-07', 'Clinical Recovery Rate', 'Recov% = (Recovered / Cases_Reported) * 100', '(df[\'recovered\'] / df[\'cases\'] * 100).clip(0,100)', 'px.bar (Grouped Recovery vs CFR comparison)'],
    ['OQ-08', 'Concurrent Outbreaks', 'Flag = 1 if Count(Diseases > 1.5 * Mean) >= 2', 'df.groupby([\'region\',\'date\']).apply(check_surge)', 'px.scatter (Alert timeline bubble chart)'],
    ['OQ-09', 'YoY Growth Trajectory', 'YoY% = (Cases_t - Cases_t-1) / Cases_t-1 * 100', 'annual_pivot.pct_change(axis=1) * 100', 'st.dataframe (Diverging colored table)'],
    ['OQ-10', 'Peak Transmission Month', 'Peak_Month = ArgMax_m(Mean(Cases_m))', 'df.groupby(\'report_month\')[\'cases\'].mean().idxmax()', 'px.imshow (Month x Disease intensity heatmap)'],
]
t_stat = doc.add_table(rows=len(stat_data) + 1, cols=5)
format_table(t_stat, [Cm(1.5), Cm(3.2), Cm(4.8), Cm(4.2), Cm(3.3)], stat_headers, stat_data)
doc.add_paragraph()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 7. UI ARCHITECTURE, TAILWIND STYLING & THEMING
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
add_heading_1('7. User Interface Framework & Tailwind Styling')

add_heading_2('7.1 Theme Configuration (.streamlit/config.toml)')
code_toml = (
    "[theme]\n"
    "primaryColor = \"#1A5376\"            # Deep Navy Blue\n"
    "backgroundColor = \"#F0F8FF\"         # Clean Alice Blue\n"
    "secondaryBackgroundColor = \"#E8F4FD\"# Soft Sky Blue (Sidebar & Containers)\n"
    "textColor = \"#2C3E50\"                # High-contrast Slate Grey\n"
    "font = \"sans serif\"                  # Modern sans-serif typography\n"
)
add_code_block(code_toml)

add_heading_2('7.2 Tailwind CSS Injection via iframe Architecture')
p_tw = doc.add_paragraph(
    'While Streamlit does not natively compile external CSS frameworks into its shadow DOM, our architecture '
    'injects Tailwind CSS (via CDN) into isolated Streamlit HTML components: st.components.v1.html(..., height=...). '
    'This pattern is leveraged in src/ui.py for two signature UI elements:\n'
    '1. Global Application Header: Displays an executive gradient header banner with program title and subtitle.\n'
    '2. Executive KPI Summary Cards: Generates responsive card layouts utilizing Tailwind utility classes '
    '(e.g., "bg-white rounded-xl shadow-md p-4 border-t-4 border-blue-900 text-center") rendering icons, metric labels, '
    'prominent numerical values, and percentage deltas.'
)
p_tw.runs[0].font.size = Pt(9.5)

add_heading_2('7.3 Persistent Sidebar Filter State Architecture')
p_sb = doc.add_paragraph(
    'All filter widgets (Disease selectbox, State multiselect, Year slider, Age multiselect, Gender radio) '
    'are bound to Streamlit session state keys (st.session_state.selected_disease, etc.). '
    'When navigating between pages (01_Overview through 06_Data_Quality), session state remains persistent, '
    'ensuring that user filtering context is maintained seamlessly across analytical perspectives.'
)
p_sb.runs[0].font.size = Pt(9.5)
doc.add_paragraph()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 8. PERFORMANCE, ERROR HANDLING & APPLICATION SECURITY
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
add_heading_1('8. Performance Optimization, Fault Tolerance & Security')

add_heading_2('8.1 Performance Optimization Strategy')
bullet_perf = [
    'Vectorized DataFrame Operations: All percentage ratios and groupings execute via C-optimized pandas vectorized methods, avoiding slow Python iterrows() loops.',
    'Granular Memory Management: Downcast numerical metrics (e.g., integer year to int16, case counts to int32) to maintain entire dataset memory footprint under 25 MB.',
    'Selective Plotly Figure Rendering: Restrict rendered data points per chart to aggregated state/month levels rather than raw row-level vectors, guaranteeing 60 fps rendering.',
]
for bp in bullet_perf:
    p = doc.add_paragraph(style='List Bullet')
    r = p.add_run(bp)
    r.font.size = Pt(9.5)

add_heading_2('8.2 Exception Handling & Graceful Degradation')
bullet_err = [
    'Database Connection Safeguards: Wrap all sqlite3 operations in structured try/except blocks. If database file is missing, app renders st.error() with guidance to run src/generate_data.py.',
    'Zero Division Protection: All ratio formulas (deaths/cases, recovered/cases) apply pandas .fillna(0.0) and numpy division guards to prevent NaN/Infinity display errors.',
    'Empty Query State Handling: If narrow sidebar filter combinations yield 0 matching rows, pages render an informative st.warning("No case data matching selected filters.") rather than crashing.',
]
for be in bullet_err:
    p = doc.add_paragraph(style='List Bullet')
    r = p.add_run(be)
    r.font.size = Pt(9.5)

add_heading_2('8.3 Security & Statutory Compliance')
bullet_sec = [
    'Zero Identifiable Health Data (PII): Entire repository operates on synthetically generated epidemiological records; completely compliant with HIPAA, DISHA, and DPDP 2023 regulations.',
    'Zero Credential Footprint: App uses local embedded SQLite storage and free public hosting; zero cloud access keys, database passwords, or JWT secrets exist in repository history.',
    'File System Isolation: Database access is strictly read-only during application runtime; all analytical views are generated in-memory without write back.',
]
for bs in bullet_sec:
    p = doc.add_paragraph(style='List Bullet')
    r = p.add_run(bs)
    r.font.size = Pt(9.5)

doc.add_paragraph()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 9. PINNED DEPENDENCY MANIFEST (requirements.txt)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
add_heading_1('9. Pinned Dependency Manifest (requirements.txt)')
p_req = doc.add_paragraph('To prevent cloud deployment build breakages caused by upstream library releases, all dependencies are strictly pinned:')
p_req.runs[0].font.size = Pt(10)

code_req = (
    "streamlit==1.35.0\n"
    "pandas==2.2.2\n"
    "numpy==1.26.4\n"
    "plotly==5.22.0\n"
    "scipy==1.13.0\n"
    "statsmodels==0.14.2\n"
    "openpyxl==3.1.2\n"
    "python-docx==1.2.0\n"
    "pytest==8.2.0\n"
    "pytest-cov==5.0.0\n"
)
add_code_block(code_req)
doc.add_paragraph()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 10. TECHNICAL RISK REGISTER & REMEDIATION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
add_heading_1('10. Technical Risk Register & Remediation')
p_trisk = doc.add_paragraph('Identified technical risks and pre-engineered architectural mitigations:')
p_trisk.runs[0].font.size = Pt(10)

trisk_headers = ['Risk ID', 'Technical Risk Factor', 'Probability', 'Impact', 'Architectural Remediation']
trisk_data = [
    ['TR-01', 'SQLite Concurrency Locking on Cloud', 'Low', 'Medium', 'Application executes strictly read-only SELECT queries; @st.cache_data prevents repeated file reads.'],
    ['TR-02', 'Tailwind CDN Outage during Evaluation', 'Low', 'Low', 'src/ui.py includes inline CSS fallbacks so KPI cards render cleanly even without external CDN connection.'],
    ['TR-03', 'Cold-Start Latency on Streamlit Cloud', 'Medium', 'Medium', 'Aggregated summaries pre-indexed in SQLite views; @st.cache_data ensures instant subsequent page loads.'],
    ['TR-04', 'Plotly Library Memory Overhead', 'Low', 'Medium', 'Chart rendering leverages Plotly Express with native WebGL rendering for responsive performance.'],
    ['TR-05', 'Relative Path Resolution Failure on Cloud', 'Medium', 'High', 'All file lookups use Path(__file__).resolve().parent rather than fragile working directory paths.'],
]
t_trisk = doc.add_table(rows=len(trisk_data) + 1, cols=5)
format_table(t_trisk, [Cm(1.8), Cm(4.5), Cm(1.8), Cm(1.8), Cm(7.1)], trisk_headers, trisk_data)

doc.add_paragraph()
p_foot = doc.add_paragraph()
p_foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
rn_f = p_foot.add_run('07_ArgJain_DiseaseTrendAnalysis_TRD.docx | v1.0 | ABES Engineering College | November 2026')
rn_f.font.size = Pt(8)
rn_f.font.color.rgb = RGBColor(0x88, 0x88, 0x88)

save_path = r'c:\Users\Hp\Downloads\hcl\docs\07_ArgJain_DiseaseTrendAnalysis_TRD.docx'
doc.save(save_path)
print(f'SAVED: {save_path}')
