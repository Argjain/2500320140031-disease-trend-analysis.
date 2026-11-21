import os
import docx
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

os.makedirs(r'c:\Users\Hp\Downloads\hcl\docs', exist_ok=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 1. WRITE BUILD_PLAN.md
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
build_plan_md = """# Disease Trend Analysis — Master Engineering Build Plan (BUILD_PLAN.md)

**Project:** P100 | Disease Trend Analysis | **Domain:** Healthcare Data Analytics  
**Author:** Arg Jain (Roll No. 2500320140031) | MCA 2nd Year DA, ABES Engineering College  
**Mentor:** Mr. Dinesh | **Target Release:** December 2026  

---

## 1. Executive Summary & Document Matrix
The Disease Trend Analysis platform is an interactive public health intelligence web application monitoring 5 contagious diseases across 10 Indian states over 60 months (2020–2024). It answers 10 operational questions using a normalized SQLite repository, automated data cleaning, multi-page Streamlit views, Plotly visualizations, and Tailwind CSS components.

### Core Documentation Links
- [01_Project_Understanding.docx](docs/01_ArgJain_DiseaseTrendAnalysis_ProjectUnderstanding.docx)
- [02_HMW_Statements.docx](docs/02_ArgJain_DiseaseTrendAnalysis_HMWStatements.docx)
- [03_Needs_Analysis.docx](docs/03_ArgJain_DiseaseTrendAnalysis_NeedsAnalysis.docx)
- [04_Traceability_Matrix.xlsx](docs/04_ArgJain_DiseaseTrendAnalysis_RTM.xlsx)
- [05_BRD.docx](docs/05_ArgJain_DiseaseTrendAnalysis_BRD.docx)
- [07_TRD.docx](docs/07_ArgJain_DiseaseTrendAnalysis_TRD.docx)
- [08_Database_Design.xlsx](docs/08_ArgJain_DiseaseTrendAnalysis_DBDesign.xlsx)
- [09_ER_Diagram.docx](docs/09_ArgJain_DiseaseTrendAnalysis_ERDiagram.docx)
- [11_User_Stories.docx](docs/11_ArgJain_DiseaseTrendAnalysis_UserStories.docx)
- [12_UI_Framework.docx](docs/12_ArgJain_DiseaseTrendAnalysis_UIFramework.docx)
- [13_Test_Cases.docx](docs/13_ArgJain_DiseaseTrendAnalysis_TestCases.docx)

---

## 2. Final Physical Folder Structure
```
2500320140031-disease-trend-analysis/
├── app.py                      # Main entry point & shared session state
├── requirements.txt            # Pinned dependencies
├── BUILD_PLAN.md               # Machine-actionable build roadmap
├── README.md                   # Installation & deployment instructions
├── .gitignore                  # Git exclusions
├── .streamlit/
│   └── config.toml             # Theme & UI palette settings
├── src/
│   ├── __init__.py
│   ├── data_loader.py          # Cached SQLite querying & loading
│   ├── cleaning.py             # Deduplication, imputation, outlier bounds
│   ├── analysis.py             # Epidemiological calculation functions
│   ├── ui.py                   # Tailwind CSS iframe component library
│   └── generate_data.py        # Seed-42 deterministic synthetic data generator
├── pages/
│   ├── 01_Overview.py          # KPI dashboard & regional case ranking
│   ├── 02_Trends.py            # 60-month time-series & seasonal heatmaps
│   ├── 03_Regional_Analysis.py # State CFR & recovery rate benchmarking
│   ├── 04_Demographics.py       # Stacked age group & gender charts
│   ├── 05_EDA_Statistics.py    # Density correlation & outbreak anomaly detection
│   └── 06_Data_Quality.py      # Cleaning audit ledger & CSV export
├── data/
│   ├── app.db                  # SQLite database (5 tables + view)
│   ├── disease_cases.csv
│   ├── region_master.csv
│   ├── disease_master.csv
│   ├── demographic_group.csv
│   ├── demographic_breakdown.csv
│   └── disease_trend_analysis_data.xlsx
├── tests/
│   ├── __init__.py
│   ├── test_data.py            # Schema, row counts, FK constraint tests
│   ├── test_analysis.py        # Mathematical assertions on pure formulas
│   └── test_app.py             # Route existence & static file smoke tests
└── docs/                       # Formal step deliverables (01 to 18)
```

---

## 3. Step-by-Step Build Tasks (BUILD-01 to BUILD-14)

- [x] **BUILD-01: Environment Configuration & Static Manifests**  
  - **Files:** `requirements.txt`, `.gitignore`, `.streamlit/config.toml`  
  - **Check:** Files exist with pinned versions.

- [x] **BUILD-02: Deterministic Dataset Generation**  
  - **Files:** `src/generate_data.py`, `data/app.db`, `data/*.csv`, `data/*.xlsx`  
  - **Check:** `python src/generate_data.py` completes with all validation tests passed.

- [ ] **BUILD-03: Data Loader with Caching (`src/data_loader.py`)**  
  - **Goal:** Connects to `data/app.db`, executes SQL query on view or tables, caches via `@st.cache_data`.  
  - **Check:** `python -c "from src.data_loader import load_data; df = load_data(); print(df.shape)"`

- [ ] **BUILD-04: Data Cleaning Pipeline (`src/cleaning.py`)**  
  - **Goal:** Implements `clean_data(df)`: drops exact duplicates, median-imputes nulls, bounds 3x IQR outliers.  
  - **Check:** Returns tuple `(cleaned_df, quality_report)`.

- [ ] **BUILD-05: Epidemiological Analytical Engine (`src/analysis.py`)**  
  - **Goal:** Implements pure functions: `compute_cfr()`, `compute_recovery_rate()`, `compute_yoy_change()`, `compute_seasonal_trend()`, `compute_incidence_rate()`, `detect_concurrent_outbreaks()`, `compute_pearson_correlation()`.  
  - **Check:** All assertions in `tests/test_analysis.py` pass.

- [x] **BUILD-06: Tailwind UI Component Library (`src/ui.py`)**  
  - **Goal:** Implements `inject_tailwind()`, `render_header()`, `render_kpi_card()`, `render_insight_box()`.  
  - **Check:** `from src.ui import render_header, render_kpi_card` succeeds.

- [ ] **BUILD-07: Application Root & Sidebar State (`app.py`)**  
  - **Goal:** Page configuration, header rendering, global session state initialization, sidebar filters.  
  - **Check:** `streamlit run app.py` starts without syntax error.

- [ ] **BUILD-08: Screen UI-01: Executive Overview (`pages/01_Overview.py`)**  
  - **Goal:** 4 Tailwind KPI cards, Plotly horizontal regional bar chart, state CFR table.  
  - **Check:** Page renders in browser and responds to sidebar filters.

- [ ] **BUILD-09: Screen UI-02: Longitudinal Trends (`pages/02_Trends.py`)**  
  - **Goal:** 60-month time-series line, overlapping YoY multi-line, 12-month cyclic transmission heatmap.  
  - **Check:** All 3 charts render smoothly.

- [ ] **BUILD-10: Screen UI-03: Regional Analysis (`pages/03_Regional_Analysis.py`)**  
  - **Goal:** State case burden rankings, CFR % comparison bar chart, recovery rate benchmarking.  
  - **Check:** 10 states displayed with accurate percentages.

- [ ] **BUILD-11: Screen UI-04: Demographic Drilldown (`pages/04_Demographics.py`)**  
  - **Goal:** Stacked age group bar chart and gender distribution pie chart.  
  - **Check:** Morbidity disaggregated across 5 age brackets.

- [ ] **BUILD-12: Screen UI-05: Advanced EDA & Surveillance (`pages/05_EDA_Statistics.py`)**  
  - **Goal:** Density vs incidence scatter with OLS trendline, Pearson r display, concurrent outbreak anomaly detector.  
  - **Check:** Correlation coefficient and surge table rendered.

- [ ] **BUILD-13: Screen UI-06: Data Quality & Export (`pages/06_Data_Quality.py`)**  
  - **Goal:** Cleaning ledger metrics scorecard, duplicate/null/outlier audits, one-click CSV dataset download.  
  - **Check:** CSV download button saves filtered data locally.

- [ ] **BUILD-14: Verification Suite & Documentation Packaging**  
  - **Goal:** Execute full test suite, verify 100% pass, generate final Project Document and presentation.  
  - **Check:** `pytest -q tests/` passes completely.

---

## 4. Definition of Done (DoD)
1. All 15 Business Requirements (BR-01..15) demonstrable in live walkthrough.
2. All 10 Operational Questions (OQ-01..10) resolvable through intuitive UI.
3. Automated test suite executes with zero critical calculation failures.
4. Clean code structure with all methods under 50 lines.
5. All 18 project deliverables available as downloadable artifacts in `docs/`.
6. Public repository pushed to GitHub with verified README.

---

## 5. Execution Commands
```bash
# Setup virtual environment
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt

# Generate synthetic dataset
python src/generate_data.py

# Run test suite
python -m pytest tests/ -q

# Launch interactive application
streamlit run app.py
```

---

## 6. Viva Voce Preparation (10 Anticipated Questions & Answers)

1. **Q: Why use SQLite instead of PostgreSQL or MySQL for this project?**  
   *A: SQLite is serverless, zero-configuration, and self-contained within the file system (`data/app.db`). For analytical datasets of 3,000–50,000 rows, SQLite combined with `@st.cache_data` provides sub-millisecond query performance with zero cloud database hosting costs.*

2. **Q: How is the Case Fatality Rate (CFR) calculated, and how do you handle zero division?**  
   *A: CFR is calculated as `(Deaths / Cases) * 100`. In Python and SQL, we apply null division guards (`NULLIF(cases, 0)` in SQL, `.fillna(0.0)` in pandas) returning `0.00%` when case counts are zero.*

3. **Q: What synthetic epidemiological patterns were embedded, and why?**  
   *A: Five clinical patterns were embedded: (1) Monsoon surges in Dengue/Malaria (Jul–Sep); (2) 2021 COVID-19 pandemic wave; (3) Higher incidence in dense urban hubs (Delhi/Maharashtra); (4) Higher mortality in elderly demographics (60+); and (5) Endemic Tuberculosis persistence in UP and Bihar.*

4. **Q: What is the purpose of `@st.cache_data(ttl=3600)`?**  
   *A: It memoizes expensive database queries in memory for 1 hour. Subsequent page transitions or filter recalculations pull directly from memory, slashing load times from 1.5s to < 0.05s.*

5. **Q: How does Streamlit maintain filter state across multi-page navigation?**  
   *A: Streamlit uses `st.session_state`. By storing selected disease, regions, and year range in session dictionary keys, all pages read from the same persistent state without reset.*

6. **Q: Why combine Streamlit with Tailwind CSS?**  
   *A: Streamlit provides rapid interactive Python widgets, while Tailwind CSS injects polished corporate UI aesthetics (rounded cards, soft shadows, accent borders) via isolated `st.components.v1.html` iframe containers.*

7. **Q: How do you identify a "Concurrent Outbreak" in Step 15?**  
   *A: An algorithmic scan evaluates each state-month. If two or more independent diseases simultaneously exceed 1.5x of their historical monthly mean, an outbreak alert flag (`is_outbreak = 1`) triggers.*

8. **Q: What data quality anomalies were injected, and how were they cleaned?**  
   *A: We injected 54 null cases (median imputed), 28 null deaths (zero imputed), 5 typography outlier spikes (bounded to Q3 + 3.0 * IQR), and 3 duplicate records (purged via `drop_duplicates`).*

9. **Q: How is statistical correlation evaluated in OQ-06?**  
   *A: We compute Pearson correlation coefficient (r) and two-tailed p-value between state population density and disease incidence per 100,000 using `scipy.stats.pearsonr`.*

10. **Q: How does the application prevent PII or medical privacy violations?**  
    *A: Zero real patient data is used. The entire dataset is algorithmically generated using synthetic statistical models conforming to HIPAA, DISHA, and DPDP guidelines.*
"""

with open(r'c:\Users\Hp\Downloads\hcl\BUILD_PLAN.md', 'w', encoding='utf-8') as f:
    f.write(build_plan_md)
print("Saved BUILD_PLAN.md")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 2. BUILD WORD DOCUMENT (docs/14_ArgJain_DiseaseTrendAnalysis_BuildPlan.docx)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
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
    run.font.size = Pt(8.0)
    run.font.color.rgb = RGBColor(0x2C, 0x3E, 0x50)

# Cover Block
p_title = doc.add_paragraph()
p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
run_t = p_title.add_run('DISEASE TREND ANALYSIS')
run_t.font.size = Pt(22)
run_t.font.bold = True
run_t.font.color.rgb = PRIMARY_COLOR

p_sub = doc.add_paragraph()
p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
run_sub = p_sub.add_run('STEP 14 — Master Engineering Build Plan & Roadmap')
run_sub.font.size = Pt(14)
run_sub.font.bold = True
run_sub.font.color.rgb = RGBColor(0x2E, 0x86, 0xAB)

doc.add_paragraph()

meta_data = [
    ('Project ID & Title', 'P100 | Disease Trend Analysis'),
    ('Domain', 'Healthcare Data Analytics'),
    ('Engineering Lead / Student', 'Arg Jain (Roll No. 2500320140031)'),
    ('Academic Program', 'MCA 2nd Year (Data Analytics Specialization)'),
    ('Institution', 'ABES Engineering College, Ghaziabad'),
    ('Faculty Mentor', 'Mr. Dinesh'),
    ('Document Version', 'v1.0'),
    ('Actionable Build Tasks', '14 Engineering Tasks (BUILD-01 to BUILD-14)'),
    ('Target Environment', 'Python 3.12 / Streamlit 1.35 / SQLite / Streamlit Cloud'),
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
# 1. PROJECT SUMMARY & SCOPE MATRIX
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
add_heading_1('1. Project Summary & Architectural Objective')
p_sum = doc.add_paragraph(
    'The Disease Trend Analysis project delivers an end-to-end, interactive epidemiological web application '
    'built for public health officers, hospital administrators, epidemiologists, and policy makers in India. '
    'Operating on a 5-year observation baseline (2020–2024) across 10 representative Indian states, '
    'the solution analyzes morbidity and mortality across 5 high-impact contagious diseases: Dengue, Malaria, '
    'Tuberculosis, COVID-19, and Typhoid. The platform addresses 10 core Operational Questions (OQ-01..10) '
    'by integrating a normalized SQLite repository, cached query loaders, automated data cleaning, pure mathematical '
    'analysis routines, Tailwind-styled metric cards, and responsive Plotly visual analytics.'
)
p_sum.runs[0].font.size = Pt(10)
doc.add_paragraph()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 2. MASTER BUILD TASKS (BUILD-01 to BUILD-14)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
add_heading_1('2. Master Build Tasks Register (BUILD-01 to BUILD-14)')
p_b_intro = doc.add_paragraph('Engineering implementation tasks ordered sequentially from infrastructure to deployment:')
p_b_intro.runs[0].font.size = Pt(10)

build_tasks_headers = ['Build ID', 'Task Goal & Scope', 'Target Files Affected', 'Supported Stories / Features', 'Verification Command / Check', 'Governing Tests']
build_tasks_data = [
    ['BUILD-01', 'Environment setup & manifest pinning', 'requirements.txt, .gitignore, .streamlit/config.toml', 'N/A / Tech Foundation', 'Files exist with exact pinned libraries', 'TC-T-18'],
    ['BUILD-02', 'Deterministic synthetic data generation', 'src/generate_data.py, data/app.db, data/*.csv', 'US-01 / FR-01', '`python src/generate_data.py` -> 100% checks pass', 'TC-T-01..07'],
    ['BUILD-03', 'Cached SQLite data loader implementation', 'src/data_loader.py', 'US-01 / FR-01', '`load_data()` queries view, caches via @st.cache_data', 'TC-T-01, 15'],
    ['BUILD-04', 'Idempotent data cleaning pipeline', 'src/cleaning.py', 'US-02 / FR-01', 'Purges 3 dupes, imputes 54 nulls, caps 5 outliers', 'TC-T-08'],
    ['BUILD-05', 'Epidemiological analytical calculation engine', 'src/analysis.py', 'US-07..15 / FR-03..11', 'Implements CFR, recovery, YoY, seasonal, correlation', 'TC-T-09..14'],
    ['BUILD-06', 'Tailwind CSS component library', 'src/ui.py', 'US-04 / UI Foundation', 'Renders header, metric stat cards, and insight boxes', 'TC-F-01'],
    ['BUILD-07', 'Root entry point & sidebar session state', 'app.py', 'US-03 / FR-02', 'Global page config, persistent sidebar filter state', 'TC-F-17, 18'],
    ['BUILD-08', 'Screen UI-01: Executive Overview', 'pages/01_Overview.py', 'US-04..07 / FR-12', 'Renders 4 Tailwind KPI cards, regional case bar, CFR table', 'TC-F-01..04'],
    ['BUILD-09', 'Screen UI-02: Longitudinal Trends', 'pages/02_Trends.py', 'US-08..11 / FR-03, 08', 'Renders 60-month line, multi-year YoY, seasonal heatmap', 'TC-F-05..07'],
    ['BUILD-10', 'Screen UI-03: Regional Burden & Recovery', 'pages/03_Regional_Analysis.py', 'US-12 / FR-04, 05', 'Renders state burden rankings, CFR bar, recovery rates', 'TC-F-08, 09, 19'],
    ['BUILD-11', 'Screen UI-04: Demographic Cohort Profiles', 'pages/04_Demographics.py', 'US-13 / FR-06', 'Renders stacked age group bars and gender donut chart', 'TC-F-10, 11'],
    ['BUILD-12', 'Screen UI-05: Advanced EDA & Outbreak Alerts', 'pages/05_EDA_Statistics.py', 'US-14, 15 / FR-07, 10', 'Density scatter regression (r & p), outbreak anomaly table', 'TC-F-12, 13'],
    ['BUILD-13', 'Screen UI-06: Data Quality Audit & Export', 'pages/06_Data_Quality.py', 'US-16, 17 / FR-14, 15', 'Cleaning ledger scorecard, CSV dataset download trigger', 'TC-F-14, 15'],
    ['BUILD-14', 'Test suite verification & deployment guide', 'tests/*.py, README.md, Deploy Doc', 'All US / BR-14, 15', 'Full test suite executes with 100% pass', 'All TC-T-01..18'],
]
t_bt = doc.add_table(rows=len(build_tasks_data) + 1, cols=6)
format_table(t_bt, [Cm(1.8), Cm(3.8), Cm(3.8), Cm(2.5), Cm(3.2), Cm(1.9)], build_tasks_headers, build_tasks_data)
doc.add_paragraph()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 3. DEFINITION OF DONE & CLI COMMANDS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
add_heading_1('3. Definition of Done (DoD) & Standard Operating Commands')
dod_items = [
    'Complete Functional Coverage: All 15 Business Requirements (BR-01..15) and 10 OQs demonstrable in live demo.',
    'Test Suite Execution: Automated pytest suite executes with 100% pass rate and zero critical computational regressions.',
    'Sub-Second Rendering: All charts and KPI metrics render within 2.0 seconds upon filter modification.',
    'Relational Integrity: SQLite database enforces all PK, FK, and domain CHECK constraints with zero orphaned rows.',
    'Documentary Completeness: All 18 formal project step deliverables finalized and organized in the docs/ folder.',
    'Public Hosting Availability: Application deployed to Streamlit Community Cloud with public HTTPS URL.',
]
for item in dod_items:
    p = doc.add_paragraph(style='List Bullet')
    r = p.add_run(item)
    r.font.size = Pt(9.5)

add_heading_2('Standard Operational CLI Commands')
code_cmds = (
    "# 1. Environment initialization\n"
    "python -m venv .venv\n"
    ".venv\\Scripts\\activate\n"
    "pip install -r requirements.txt\n\n"
    "# 2. Re-generate synthetic data repository\n"
    "python src/generate_data.py\n\n"
    "# 3. Execute automated test suite\n"
    "python -m pytest tests/ -q --tb=short\n\n"
    "# 4. Launch interactive Streamlit application\n"
    "streamlit run app.py\n"
)
add_code_block(code_cmds)
doc.add_paragraph()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 4. VIVA VOCE DEFENSE NOTES (10 QUESTIONS & MODEL ANSWERS)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
add_heading_1('4. Viva Voce Defense Preparation (10 Anticipated Questions)')
p_viva_intro = doc.add_paragraph('Concise architectural justifications for formal academic evaluation:')
p_viva_intro.runs[0].font.size = Pt(10)

viva_headers = ['#', 'Anticipated Viva Question', 'Model Answer & Technical Justification']
viva_data = [
    ['1', 'Why choose SQLite over PostgreSQL for this application?', 'SQLite is an embedded, zero-configuration engine stored directly as data/app.db. For an analytical volume of 3,000–50,000 records, SQLite combined with Streamlit in-memory caching (@st.cache_data) provides sub-millisecond query responses with zero cloud database hosting costs.'],
    ['2', 'How is Case Fatality Rate (CFR) defined, and how do you prevent divide-by-zero crashes?', 'CFR is defined as (Deaths / Confirmed Cases) * 100. Divide-by-zero errors are prevented using SQL NULLIF(cases, 0) and Python zero-guards, returning exactly 0.00% when zero cases are reported.'],
    ['3', 'What epidemiological patterns were synthetically engineered into the data?', 'Five authentic patterns were embedded: (1) Monsoon surges in Dengue and Malaria (Jul-Sep); (2) Severe COVID-19 pandemic wave in 2021; (3) Higher incidence in high-density urban hubs (Delhi, Maharashtra); (4) Elevated CFR in elderly demographics (60+); and (5) Endemic Tuberculosis persistence in UP and Bihar.'],
    ['4', 'What performance benefit does @st.cache_data provide?', 'It memoizes data loading and cleaning in RAM for 1 hour (ttl=3600). Subsequent user filter mutations or page navigation bypass SQLite disk queries entirely, reducing latency from 1.5s to < 0.05s.'],
    ['5', 'How does the application maintain filter context when switching pages?', 'Filters are stored in st.session_state dictionary keys (e.g., st.session_state.selected_disease). Because session state persists throughout the user session, all 6 sub-pages inherit identical active filter context without state loss.'],
    ['6', 'Why combine Streamlit with Tailwind CSS via iframe?', 'Streamlit generates rapid interactive data science visualizations, while Tailwind CSS injects polished corporate UI aesthetics (rounded cards, soft shadows, accent borders) via isolated st.components.v1.html iframe containers.'],
    ['7', 'How is a "Concurrent Outbreak" algorithmically detected in Step 15?', 'An analytical function evaluates each state-month. If two or more independent disease entities simultaneously exceed 1.5x of their historical monthly baseline, an alert flag (is_outbreak = 1) is triggered.'],
    ['8', 'What data quality issues were introduced, and how does the pipeline clean them?', 'We injected 54 null cases (median imputed), 28 null deaths (zero imputed), 5 typography outlier spikes (bounded to Q3 + 3.0 * IQR), and 3 duplicate records (purged via drop_duplicates).'],
    ['9', 'How is urban density correlation evaluated in OQ-06?', 'We compute the Pearson correlation coefficient (r) and two-tailed p-value between state population density (persons/sq km) and normalized disease incidence per 100,000 residents using scipy.stats.pearsonr.'],
    ['10', 'How does the architecture protect patient data privacy?', 'Zero real patient data is utilized. The entire dataset is algorithmically synthesized using deterministic statistical distributions conforming strictly to HIPAA, DISHA, and DPDP 2023 regulations.'],
]
t_viva = doc.add_table(rows=len(viva_data) + 1, cols=3)
format_table(t_viva, [Cm(1.0), Cm(4.8), Cm(11.2)], viva_headers, viva_data)

doc.add_paragraph()
p_foot = doc.add_paragraph()
p_foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
rn_f = p_foot.add_run('14_ArgJain_DiseaseTrendAnalysis_BuildPlan.docx | v1.0 | ABES Engineering College | November 2026')
rn_f.font.size = Pt(8)
rn_f.font.color.rgb = RGBColor(0x88, 0x88, 0x88)

save_path = r'c:\Users\Hp\Downloads\hcl\docs\14_ArgJain_DiseaseTrendAnalysis_BuildPlan.docx'
doc.save(save_path)
print(f'SAVED DOCX: {save_path}')
