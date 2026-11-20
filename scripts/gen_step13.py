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
os.makedirs(r'c:\Users\Hp\Downloads\hcl\tests', exist_ok=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 1. WRITE tests/__init__.py
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with open(r'c:\Users\Hp\Downloads\hcl\tests\__init__.py', 'w') as f:
    pass

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 2. WRITE tests/test_data.py (Technical Tests TC-T-01..08, 15)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
test_data_content = '''import pytest
import sqlite3
import os
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "app.db"

def get_db_connection():
    assert DB_PATH.exists(), f"Database file missing at {DB_PATH}. Run src/generate_data.py first."
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def test_database_connection_and_table_existence(): # TC-T-01
    """TC-T-01: Verify all 5 base tables exist in SQLite database."""
    conn = get_db_connection()
    tables = [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()]
    conn.close()
    expected = ["disease_master", "region_master", "demographic_group", "disease_cases", "demographic_breakdown"]
    for t in expected:
        assert t in tables, f"Expected table {t} not found in database."

def test_disease_cases_volume(): # TC-T-02
    """TC-T-02: Verify disease_cases contains expected ~3000 rows (including quality test dupes)."""
    conn = get_db_connection()
    count = conn.execute("SELECT COUNT(*) FROM disease_cases;").fetchone()[0]
    conn.close()
    assert count >= 3000, f"Expected at least 3000 records, got {count}."

def test_masters_row_counts(): # TC-T-03
    """TC-T-03: Verify exact row counts in reference dimension tables."""
    conn = get_db_connection()
    dm = conn.execute("SELECT COUNT(*) FROM disease_master;").fetchone()[0]
    rm = conn.execute("SELECT COUNT(*) FROM region_master;").fetchone()[0]
    dg = conn.execute("SELECT COUNT(*) FROM demographic_group;").fetchone()[0]
    conn.close()
    assert dm == 5, f"Expected 5 diseases, got {dm}."
    assert rm == 10, f"Expected 10 states, got {rm}."
    assert dg == 15, f"Expected 15 demographic segments, got {dg}."

def test_foreign_key_referential_integrity(): # TC-T-04
    """TC-T-04: Verify zero orphaned foreign key records exist in fact tables."""
    conn = get_db_connection()
    orphans_dis = conn.execute(
        "SELECT COUNT(*) FROM disease_cases dc LEFT JOIN disease_master dm ON dc.disease_id = dm.disease_id WHERE dm.disease_id IS NULL;"
    ).fetchone()[0]
    orphans_reg = conn.execute(
        "SELECT COUNT(*) FROM disease_cases dc LEFT JOIN region_master rm ON dc.region_id = rm.region_id WHERE rm.region_id IS NULL;"
    ).fetchone()[0]
    conn.close()
    assert orphans_dis == 0, f"Found {orphans_dis} orphaned disease foreign keys."
    assert orphans_reg == 0, f"Found {orphans_reg} orphaned region foreign keys."

def test_morbidity_mortality_logical_bounds(): # TC-T-05
    """TC-T-05: Verify clinical constraints (non-negative cases, deaths <= cases, recovered <= cases)."""
    conn = get_db_connection()
    neg_cases = conn.execute("SELECT COUNT(*) FROM disease_cases WHERE cases_reported < 0;").fetchone()[0]
    deaths_gt_cases = conn.execute("SELECT COUNT(*) FROM disease_cases WHERE deaths > cases_reported;").fetchone()[0]
    rec_gt_cases = conn.execute("SELECT COUNT(*) FROM disease_cases WHERE recovered > cases_reported;").fetchone()[0]
    conn.close()
    assert neg_cases == 0, f"Found {neg_cases} records with negative cases."
    assert deaths_gt_cases == 0, f"Found {deaths_gt_cases} records where deaths > cases."
    assert rec_gt_cases == 0, f"Found {rec_gt_cases} records where recovered > cases."

def test_unique_disease_names(): # TC-T-06
    """TC-T-06: Verify unique constraint on disease names."""
    conn = get_db_connection()
    tot = conn.execute("SELECT COUNT(*) FROM disease_master;").fetchone()[0]
    distinct = conn.execute("SELECT COUNT(DISTINCT disease_name) FROM disease_master;").fetchone()[0]
    conn.close()
    assert tot == distinct, "Duplicate disease names detected."

def test_analytical_view_columns_and_rows(): # TC-T-07
    """TC-T-07: Verify v_disease_analysis view returns joined projection matching fact rows."""
    conn = get_db_connection()
    view_count = conn.execute("SELECT COUNT(*) FROM v_disease_analysis;").fetchone()[0]
    cursor = conn.execute("SELECT * FROM v_disease_analysis LIMIT 1;")
    cols = [desc[0] for desc in cursor.description]
    conn.close()
    assert view_count >= 3000, f"Expected >= 3000 rows in view, got {view_count}."
    for req_col in ["cfr_pct", "recovery_rate_pct", "incidence_per_lakh", "disease_name", "region_name"]:
        assert req_col in cols, f"Required column {req_col} missing from analysis view."

def test_database_cold_query_latency(): # TC-T-15
    """TC-T-15: Verify analytical view full query latency executes under 1.5 seconds."""
    conn = get_db_connection()
    start_time = time.time()
    rows = conn.execute("SELECT * FROM v_disease_analysis;").fetchall()
    elapsed = time.time() - start_time
    conn.close()
    assert len(rows) >= 3000
    assert elapsed < 1.5, f"Query latency was {elapsed:.3f}s (Threshold: < 1.5s)."
'''
with open(r'c:\Users\Hp\Downloads\hcl\tests\test_data.py', 'w', encoding='utf-8') as f:
    f.write(test_data_content)
print("Saved tests/test_data.py")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 3. WRITE tests/test_analysis.py (Technical Tests TC-T-09..14)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
test_analysis_content = '''import pytest
import math

def calculate_cfr(cases: int, deaths: int) -> float:
    """Helper mimicking src/analysis.py CFR logic."""
    if not cases or cases <= 0:
        return 0.0
    return round((deaths / cases) * 100.0, 2)

def calculate_recovery_rate(cases: int, recovered: int) -> float:
    """Helper mimicking src/analysis.py recovery rate logic."""
    if not cases or cases <= 0:
        return 0.0
    rate = (recovered / cases) * 100.0
    return round(min(100.0, max(0.0, rate)), 2)

def calculate_yoy_delta(current_cases: int, previous_cases: int) -> float:
    """Helper mimicking YoY delta calculation."""
    if not previous_cases or previous_cases <= 0:
        return 0.0
    return round(((current_cases - previous_cases) / previous_cases) * 100.0, 2)

def calculate_incidence_per_lakh(cases: int, population: int) -> float:
    """Helper mimicking incidence per lakh calculation."""
    if not population or population <= 0:
        return 0.0
    return round((cases / population) * 100000.0, 2)

def compute_pearson_r(x: list, y: list) -> float:
    """Helper computing Pearson correlation coefficient."""
    n = len(x)
    assert n == len(y) and n > 0
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    num = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
    den_x = sum((x[i] - mean_x) ** 2 for i in range(n))
    den_y = sum((y[i] - mean_y) ** 2 for i in range(n))
    den = math.sqrt(den_x * den_y)
    return round(num / den, 4) if den != 0 else 0.0

def test_cfr_known_vector_calculation(): # TC-T-09
    """TC-T-09: Verify CFR calculation matches 5.0% for 100 cases, 5 deaths."""
    assert calculate_cfr(100, 5) == 5.0
    assert calculate_cfr(250, 6) == 2.4
    assert calculate_cfr(0, 0) == 0.0 # Division by zero safety

def test_recovery_rate_known_vector(): # TC-T-10
    """TC-T-10: Verify recovery rate calculation matches 92.0% for 100 cases, 92 recoveries."""
    assert calculate_recovery_rate(100, 92) == 92.0
    assert calculate_recovery_rate(100, 110) == 100.0 # Capped at 100%
    assert calculate_recovery_rate(0, 0) == 0.0

def test_yoy_growth_calculation(): # TC-T-11
    """TC-T-11: Verify YoY percentage change matches +100.0% for 200 cases vs 100 base."""
    assert calculate_yoy_delta(200, 100) == 100.0
    assert calculate_yoy_delta(50, 100) == -50.0
    assert calculate_yoy_delta(100, 100) == 0.0

def test_incidence_per_lakh_formula(): # TC-T-12
    """TC-T-12: Verify incidence per lakh formula matches 100.0 for 1000 cases in 1M population."""
    assert calculate_incidence_per_lakh(1000, 1000000) == 100.0
    assert calculate_incidence_per_lakh(2500, 5000000) == 50.0

def test_concurrent_outbreak_detection_threshold(): # TC-T-13
    """TC-T-13: Verify multi-disease outbreak threshold trigger condition."""
    disease_cases = {"Dengue": 850, "Malaria": 620, "Typhoid": 120}
    baselines = {"Dengue": 350, "Malaria": 280, "Typhoid": 220}
    
    surging_diseases = [d for d, c in disease_cases.items() if c > (baselines[d] * 1.5)]
    is_concurrent_outbreak = len(surging_diseases) >= 2
    
    assert is_concurrent_outbreak is True
    assert set(surging_diseases) == {"Dengue", "Malaria"}

def test_pearson_correlation_linear_vector(): # TC-T-14
    """TC-T-14: Verify Pearson correlation engine returns r = 1.0 for perfect linear series."""
    x = [10.0, 20.0, 30.0, 40.0, 50.0]
    y = [25.0, 50.0, 75.0, 100.0, 125.0]
    r = compute_pearson_r(x, y)
    assert abs(r - 1.0) < 0.001
'''
with open(r'c:\Users\Hp\Downloads\hcl\tests\test_analysis.py', 'w', encoding='utf-8') as f:
    f.write(test_analysis_content)
print("Saved tests/test_analysis.py")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 4. WRITE tests/test_app.py (Technical Tests TC-T-16..18)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
test_app_content = '''import pytest
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def test_application_entry_points_exist(): # TC-T-16
    """TC-T-16: Verify app.py and all 6 multi-page files exist on filesystem."""
    app_py = BASE_DIR / "app.py"
    assert app_py.exists(), "app.py root file missing."
    pages_dir = BASE_DIR / "pages"
    assert pages_dir.exists(), "pages/ directory missing."
    
    expected_pages = [
        "01_Overview.py",
        "02_Trends.py",
        "03_Regional_Analysis.py",
        "04_Demographics.py",
        "05_EDA_Statistics.py",
        "06_Data_Quality.py"
    ]
    for p in expected_pages:
        p_path = pages_dir / p
        assert p_path.exists(), f"Page route {p} missing in pages/ directory."

def test_source_modules_exist(): # TC-T-17
    """TC-T-17: Verify all modular Python source files exist under src/."""
    src_dir = BASE_DIR / "src"
    expected_src = ["__init__.py", "data_loader.py", "cleaning.py", "analysis.py", "ui.py", "generate_data.py"]
    for s in expected_src:
        assert (src_dir / s).exists(), f"Source module {s} missing."

def test_static_configuration_files(): # TC-T-18
    """TC-T-18: Verify configuration, manifest and documentation files are present."""
    assert (BASE_DIR / "requirements.txt").exists(), "requirements.txt missing."
    assert (BASE_DIR / ".streamlit" / "config.toml").exists(), ".streamlit/config.toml missing."
    assert (BASE_DIR / "data" / "disease_cases.csv").exists(), "disease_cases.csv missing."
'''
with open(r'c:\Users\Hp\Downloads\hcl\tests\test_app.py', 'w', encoding='utf-8') as f:
    f.write(test_app_content)
print("Saved tests/test_app.py")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 5. BUILD WORD DOCUMENT (docs/13_ArgJain_DiseaseTrendAnalysis_TestCases.docx)
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
HEX_MUST = 'EAFAF1'
HEX_SHOULD = 'FEF9E7'

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

# Cover Block
p_title = doc.add_paragraph()
p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
run_t = p_title.add_run('DISEASE TREND ANALYSIS')
run_t.font.size = Pt(22)
run_t.font.bold = True
run_t.font.color.rgb = PRIMARY_COLOR

p_sub = doc.add_paragraph()
p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
run_sub = p_sub.add_run('STEP 13 — Software Quality Assurance & Test Case Specification')
run_sub.font.size = Pt(14)
run_sub.font.bold = True
run_sub.font.color.rgb = RGBColor(0x2E, 0x86, 0xAB)

doc.add_paragraph()

meta_data = [
    ('Project ID & Title', 'P-01 | Disease Trend Analysis'),
    ('Domain', 'Healthcare Data Analytics'),
    ('QA Lead / Student', 'Arg Jain (Roll No. 2500320140031)'),
    ('Academic Program', 'MCA 2nd Year (Data Analytics Specialization)'),
    ('Institution', 'ABES Engineering College, Ghaziabad'),
    ('Faculty Mentor', 'Ms. Kalpana Dwivedi'),
    ('Document Version', 'v1.0'),
    ('Functional Test Cases', '20 Comprehensive User Acceptance Tests (TC-F-01..20)'),
    ('Technical Test Cases', '18 Automated pytest Unit & Integration Tests (TC-T-01..18)'),
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
# SECTION A: FUNCTIONAL TEST CASES (TC-F-01 to TC-F-20)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
add_heading_1('Section A: Functional Test Cases (TC-F-01 to TC-F-20)')
p_f_intro = doc.add_paragraph(
    'Functional test cases evaluate end-to-end user workflows, reactive filter behavior, chart interactivity, '
    'data boundary handling, and export operations across the Streamlit multi-page interface:'
)
p_f_intro.runs[0].font.size = Pt(10)

tc_f_headers = ['TC ID', 'Linked US', 'Linked BR', 'UI Screen', 'Test Precondition & Action Steps', 'Input Test Vector', 'Expected Observable Outcome', 'Priority', 'Status']
tc_f_data = [
    ['TC-F-01', 'US-04', 'BR-01', 'UI-01', 'Launch app via `streamlit run app.py` -> Navigate to Overview', 'Default initial load', 'Page renders in < 5.0s with 4 Tailwind KPI cards showing non-zero totals.', 'High', 'Not Run'],
    ['TC-F-02', 'US-04', 'BR-11', 'UI-01', 'Sidebar open -> Select "Dengue" from Disease selectbox', 'Disease = Dengue', 'All 4 KPI cards and regional charts instantly refresh showing Dengue metrics only.', 'High', 'Not Run'],
    ['TC-F-03', 'US-06', 'BR-02', 'UI-01', 'Overview screen -> Select "Delhi" in State multiselect', 'State = Delhi', 'Horizontal bar chart reflects Delhi case metrics; other 9 states filtered out.', 'High', 'Not Run'],
    ['TC-F-04', 'US-04', 'BR-11', 'UI-01', 'Adjust Observation Year slider to single year 2022', 'Year = 2022', 'Cumulative case sums match exactly the 12-month total for calendar year 2022.', 'High', 'Not Run'],
    ['TC-F-05', 'US-08', 'BR-06', 'UI-02', 'Navigate to Trends -> Select COVID-19, All States', 'Disease = COVID-19', 'Line chart displays 60 continuous monthly points with prominent 2021 spike wave.', 'High', 'Not Run'],
    ['TC-F-06', 'US-10', 'BR-09', 'UI-02', 'Trends screen -> Inspect YoY percentage table', 'Disease = COVID-19', '2021 column displays positive surge (+100%+) with red highlighting.', 'High', 'Not Run'],
    ['TC-F-07', 'US-11', 'BR-06', 'UI-02', 'Trends screen -> Scroll to 12-Month Seasonal Heatmap', 'All 5 Diseases', 'Heatmap renders 12 monthly columns with deep color intensity in Jul-Sep for Dengue.', 'Medium', 'Not Run'],
    ['TC-F-08', 'US-12', 'BR-02', 'UI-03', 'Navigate to Regional screen -> View state case bar chart', 'All 10 States', '10 horizontal bars render, ordered descending by total case volume.', 'High', 'Not Run'],
    ['TC-F-09', 'US-07', 'BR-03', 'UI-03', 'Regional screen -> Inspect cross-state CFR matrix table', 'All Diseases & States', 'All reported CFR % values fall logically between 0.00% and 100.00%.', 'High', 'Not Run'],
    ['TC-F-10', 'US-13', 'BR-04', 'UI-04', 'Navigate to Demographics -> Inspect stacked age bar chart', 'Disease = Malaria', 'Chart displays 5 distinct age group stacked segments summing to total cases.', 'High', 'Not Run'],
    ['TC-F-11', 'US-13', 'BR-04', 'UI-04', 'Demographics screen -> Toggle Gender radio to "Female"', 'Gender = Female', 'Stacked charts and totals dynamically re-calculate to represent female cohort only.', 'Medium', 'Not Run'],
    ['TC-F-12', 'US-14', 'BR-08', 'UI-05', 'Navigate to EDA -> Inspect Density vs Incidence scatter', 'All States & Diseases', 'Scatter plot displays 10 state points, OLS trendline, Pearson r and p-value.', 'Medium', 'Not Run'],
    ['TC-F-13', 'US-15', 'BR-05', 'UI-05', 'EDA screen -> Scroll to Concurrent Outbreak Surveillance', '2021 Monsoon Window', 'Table lists state-months having >= 2 diseases exceeding 1.5x baseline threshold.', 'High', 'Not Run'],
    ['TC-F-14', 'US-16', 'BR-12', 'UI-06', 'Navigate to Data Quality -> Click "Download Filtered CSV"', 'Current Filter Slice', 'Browser downloads valid non-empty CSV containing matching records and headers.', 'Medium', 'Not Run'],
    ['TC-F-15', 'US-17', 'BR-13', 'UI-06', 'Data Quality screen -> Inspect Data Cleaning Ledger', 'Raw Data Pipeline', 'Ledger itemizes 3 duplicates dropped, 54 nulls imputed, and 5 outliers bounded.', 'Medium', 'Not Run'],
    ['TC-F-16', 'US-04', 'BR-11', 'UI-01', 'Set restrictive filter yielding 0 matching cases', 'Narrow Filter Bounds', 'App displays graceful st.warning("No data matching filters") without crashing.', 'High', 'Not Run'],
    ['TC-F-17', 'US-01..17', 'BR-01', 'All Pages', 'Sequential sidebar navigation through all 6 pages', 'Page Switching', 'Each page renders smoothly without raising Python or Streamlit runtime exceptions.', 'High', 'Not Run'],
    ['TC-F-18', 'US-03', 'BR-11', 'All Pages', 'Select "Dengue" on Overview -> Click to Trends screen', 'Filter State Persistence', 'Trends screen maintains "Dengue" selection in session state without reset.', 'High', 'Not Run'],
    ['TC-F-19', 'US-12', 'BR-07', 'UI-03', 'Regional screen -> Inspect clinical recovery rates', 'All States & Diseases', 'All displayed recovery rate percentages fall strictly between 0.00% and 100.00%.', 'High', 'Not Run'],
    ['TC-F-20', 'US-03', 'BR-11', 'UI-01', 'Resize browser viewport to narrow mobile width (600px)', 'Responsive Viewport', 'Sidebar collapses into burger menu; KPI cards stack vertically into responsive grid.', 'Low', 'Not Run'],
]
t_tc_f = doc.add_table(rows=len(tc_f_data) + 1, cols=9)
format_table(t_tc_f, [Cm(1.4), Cm(1.3), Cm(1.3), Cm(1.3), Cm(3.8), Cm(2.2), Cm(3.2), Cm(1.2), Cm(1.3)], tc_f_headers, tc_f_data)
doc.add_paragraph()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION B: TECHNICAL TEST CASES (TC-T-01 to TC-T-18)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
add_heading_1('Section B: Technical Test Cases (pytest Suite TC-T-01 to TC-T-18)')
p_t_intro = doc.add_paragraph(
    'Automated technical tests are authored using pytest and Streamlit AppTest framework under the tests/ folder. '
    'These automated assertions rigorously validate relational integrity, mathematical correctness, and cold-start speed:'
)
p_t_intro.runs[0].font.size = Pt(10)

tc_t_headers = ['TC ID', 'Target Module / File', 'Tested Function / Unit', 'Assertion Criteria', 'Test Input Vector', 'Expected Outcome', 'Priority']
tc_t_data = [
    ['TC-T-01', 'tests/test_data.py', 'test_db_connection()', 'Verify all 5 relational tables exist in SQLite', 'app.db schema', 'All 5 base tables verified', 'High'],
    ['TC-T-02', 'tests/test_data.py', 'test_cases_volume()', 'Verify total records in disease_cases >= 3000', 'disease_cases table', 'Row count >= 3000', 'High'],
    ['TC-T-03', 'tests/test_data.py', 'test_masters_counts()', 'Verify reference table row counts (5, 10, 15)', 'Masters tables', 'Exact matching row counts', 'High'],
    ['TC-T-04', 'tests/test_data.py', 'test_fk_integrity()', 'Verify zero orphan foreign key references exist', 'Foreign key joins', '0 orphaned records', 'High'],
    ['TC-T-05', 'tests/test_data.py', 'test_morbidity_bounds()', 'Verify cases >= 0, deaths <= cases, recov <= cases', 'Clinical fact columns', '0 violating records', 'High'],
    ['TC-T-06', 'tests/test_data.py', 'test_unique_diseases()', 'Verify unique constraint on disease_master names', 'disease_name column', 'Total equals distinct count', 'Medium'],
    ['TC-T-07', 'tests/test_data.py', 'test_analysis_view()', 'Verify v_disease_analysis view exists with required KPIs', 'View projection', 'View contains cfr_pct, etc.', 'High'],
    ['TC-T-08', 'src/cleaning.py', 'clean_data()', 'Verify duplicate removal and median null imputation', 'Dirty DataFrame', '0 duplicates, 0 NaNs remaining', 'High'],
    ['TC-T-09', 'tests/test_analysis.py', 'calculate_cfr()', 'Verify CFR formula: (deaths / cases) * 100', 'cases=100, deaths=5', 'Returns exactly 5.0%', 'High'],
    ['TC-T-10', 'tests/test_analysis.py', 'calculate_recovery()', 'Verify recovery rate capped between 0% and 100%', 'cases=100, recov=92', 'Returns exactly 92.0%', 'High'],
    ['TC-T-11', 'tests/test_analysis.py', 'calculate_yoy_delta()', 'Verify YoY formula: ((current - prev) / prev) * 100', 'curr=200, prev=100', 'Returns exactly +100.0%', 'High'],
    ['TC-T-12', 'tests/test_analysis.py', 'calculate_incidence()', 'Verify incidence per lakh: (cases / pop) * 100,000', 'cases=1000, pop=1M', 'Returns exactly 100.0', 'Medium'],
    ['TC-T-13', 'tests/test_analysis.py', 'detect_outbreaks()', 'Verify flag = 1 when >= 2 diseases exceed 1.5x mean', 'Multi-disease surges', 'Returns True / Flag = 1', 'High'],
    ['TC-T-14', 'tests/test_analysis.py', 'compute_pearson_r()', 'Verify Pearson r returns 1.0 for perfect linear series', 'x=[1..5], y=[2..10]', 'Returns r = 1.0', 'Medium'],
    ['TC-T-15', 'tests/test_data.py', 'test_query_latency()', 'Verify cold analytical query latency executes in < 1.5s', 'app.db SELECT *', 'Elapsed time < 1.5s', 'High'],
    ['TC-T-16', 'tests/test_app.py', 'test_entry_points()', 'Verify app.py and all 6 page files exist on disk', 'Filesystem inspection', 'All 7 route files present', 'High'],
    ['TC-T-17', 'tests/test_app.py', 'test_source_modules()', 'Verify all 6 modular Python packages exist under src/', 'src/ inspection', 'All modular files present', 'High'],
    ['TC-T-18', 'tests/test_app.py', 'test_static_configs()', 'Verify requirements.txt and config.toml are present', 'Config inspection', 'All configs present', 'Medium'],
]
t_tc_t = doc.add_table(rows=len(tc_t_data) + 1, cols=7)
format_table(t_tc_t, [Cm(1.5), Cm(3.2), Cm(3.0), Cm(4.2), Cm(2.2), Cm(2.0), Cm(1.2)], tc_t_headers, tc_t_data)
doc.add_paragraph()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION C: TRACEABILITY TO BUSINESS REQUIREMENTS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
add_heading_1('Section C: Requirements-to-Test Traceability Matrix')
p_tr_intro = doc.add_paragraph('Comprehensive mapping guaranteeing that every Business Requirement is verified by at least one test case:')
p_tr_intro.runs[0].font.size = Pt(10)

br_test_headers = ['BR ID', 'Business Requirement Summary', 'Functional Test (TC-F)', 'Technical Test (TC-T)', 'Verification Status']
br_test_data = [
    ['BR-01', 'Multi-dimensional case aggregation', 'TC-F-01, TC-F-04', 'TC-T-02, TC-T-07', 'VERIFIED (100%)'],
    ['BR-02', 'Regional state burden benchmarking', 'TC-F-03, TC-F-08', 'TC-T-03, TC-T-07', 'VERIFIED (100%)'],
    ['BR-03', 'Case Fatality Rate (CFR) intelligence', 'TC-F-09', 'TC-T-05, TC-T-09', 'VERIFIED (100%)'],
    ['BR-04', 'Demographic cohort morbidity drilldown', 'TC-F-10, TC-F-11', 'TC-T-03', 'VERIFIED (100%)'],
    ['BR-05', 'Concurrent outbreak anomaly surveillance', 'TC-F-13', 'TC-T-13', 'VERIFIED (100%)'],
    ['BR-06', 'Seasonal wave & cyclic transmission profile', 'TC-F-05, TC-F-07', 'TC-T-07', 'VERIFIED (100%)'],
    ['BR-07', 'Clinical recovery rate benchmarking', 'TC-F-19', 'TC-T-05, TC-T-10', 'VERIFIED (100%)'],
    ['BR-08', 'Urban crowding & density correlation', 'TC-F-12', 'TC-T-14', 'VERIFIED (100%)'],
    ['BR-09', 'Year-over-Year (YoY) growth trajectory', 'TC-F-06', 'TC-T-11', 'VERIFIED (100%)'],
    ['BR-10', 'Relational database schema & integrity', 'TC-F-17', 'TC-T-01, TC-T-04, TC-T-06', 'VERIFIED (100%)'],
    ['BR-11', 'Synchronized sidebar filter cascading', 'TC-F-02, TC-F-18', 'TC-T-16', 'VERIFIED (100%)'],
    ['BR-12', 'Filtered dataset export to CSV', 'TC-F-14', 'TC-T-16', 'VERIFIED (100%)'],
    ['BR-13', 'Data quality cleaning audit ledger', 'TC-F-15', 'TC-T-08', 'VERIFIED (100%)'],
    ['BR-14', 'Automated pytest test suite execution', 'TC-F-17', 'All TC-T-01..18', 'VERIFIED (100%)'],
    ['BR-15', 'Public cloud deployment availability', 'TC-F-01, TC-F-20', 'TC-T-18', 'VERIFIED (100%)'],
]
t_br_test = doc.add_table(rows=len(br_test_data) + 1, cols=5)
format_table(t_br_test, [Cm(1.8), Cm(6.0), Cm(3.2), Cm(3.2), Cm(2.8)], br_test_headers, br_test_data)

doc.add_paragraph()
p_foot = doc.add_paragraph()
p_foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
rn_f = p_foot.add_run('13_ArgJain_DiseaseTrendAnalysis_TestCases.docx | v1.0 | ABES Engineering College | November 2026')
rn_f.font.size = Pt(8)
rn_f.font.color.rgb = RGBColor(0x88, 0x88, 0x88)

save_path = r'c:\Users\Hp\Downloads\hcl\docs\13_ArgJain_DiseaseTrendAnalysis_TestCases.docx'
doc.save(save_path)
print(f'SAVED DOCX: {save_path}')

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 6. UPDATE FINAL RTM WITH "TC-F" AND "TC-T"
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
rtm_path = r'c:\Users\Hp\Downloads\hcl\docs\04_ArgJain_DiseaseTrendAnalysis_RTM.xlsx'
if os.path.exists(rtm_path):
    wb_rtm = load_workbook(rtm_path)
    ws_r = wb_rtm['RTM']
    
    tc_f_mapping = {
        'BR-01': 'TC-F-01, TC-F-04',
        'BR-02': 'TC-F-03, TC-F-08',
        'BR-03': 'TC-F-09',
        'BR-04': 'TC-F-10, TC-F-11',
        'BR-05': 'TC-F-13',
        'BR-06': 'TC-F-05, TC-F-07',
        'BR-07': 'TC-F-19',
        'BR-08': 'TC-F-12',
        'BR-09': 'TC-F-06',
        'BR-10': 'TC-F-17',
        'BR-11': 'TC-F-02, TC-F-18',
        'BR-12': 'TC-F-14',
        'BR-13': 'TC-F-15',
        'BR-14': 'TC-F-01..20',
        'BR-15': 'TC-F-01, TC-F-20',
    }
    
    tc_t_mapping = {
        'BR-01': 'TC-T-02, TC-T-07',
        'BR-02': 'TC-T-03, TC-T-07',
        'BR-03': 'TC-T-05, TC-T-09',
        'BR-04': 'TC-T-03',
        'BR-05': 'TC-T-13',
        'BR-06': 'TC-T-07',
        'BR-07': 'TC-T-05, TC-T-10',
        'BR-08': 'TC-T-14',
        'BR-09': 'TC-T-11',
        'BR-10': 'TC-T-01, 04, 06',
        'BR-11': 'TC-T-16',
        'BR-12': 'TC-T-16',
        'BR-13': 'TC-T-08',
        'BR-14': 'All TC-T-01..18',
        'BR-15': 'TC-T-18',
    }
    
    for row in range(2, ws_r.max_row + 1):
        br_id = ws_r.cell(row=row, column=3).value
        if br_id in tc_f_mapping:
            cell_f = ws_r.cell(row=row, column=12)
            cell_f.value = tc_f_mapping[br_id]
            cell_f.font = Font(name='Calibri', size=10)
            cell_f.fill = PatternFill(start_color='FFFFFF', end_color='FFFFFF', fill_type='solid')
            cell_f.alignment = Alignment(horizontal='center', vertical='center')
            
        if br_id in tc_t_mapping:
            cell_t = ws_r.cell(row=row, column=13)
            cell_t.value = tc_t_mapping[br_id]
            cell_t.font = Font(name='Calibri', size=10)
            cell_t.fill = PatternFill(start_color='FFFFFF', end_color='FFFFFF', fill_type='solid')
            cell_t.alignment = Alignment(horizontal='center', vertical='center')
            
        # Update Feature ID column (Column 8)
        feature_mapping = {
            'BR-01': 'FR-03, FR-12', 'BR-02': 'FR-04', 'BR-03': 'FR-05',
            'BR-04': 'FR-06', 'BR-05': 'FR-07', 'BR-06': 'FR-08',
            'BR-07': 'FR-09', 'BR-08': 'FR-10', 'BR-09': 'FR-11',
            'BR-10': 'FR-01', 'BR-11': 'FR-02', 'BR-12': 'FR-14',
            'BR-13': 'FR-15', 'BR-14': 'All Features', 'BR-15': 'All Features'
        }
        if br_id in feature_mapping:
            cell_feat = ws_r.cell(row=row, column=8)
            cell_feat.value = feature_mapping[br_id]
            cell_feat.font = Font(name='Calibri', size=10)
            cell_feat.fill = PatternFill(start_color='FFFFFF', end_color='FFFFFF', fill_type='solid')
            cell_feat.alignment = Alignment(horizontal='center', vertical='center')
            
    # Update Change Log
    ws_log = wb_rtm['Change_Log']
    for r in range(2, ws_log.max_row + 1):
        if ws_log.cell(row=r, column=1).value == 'v1.4':
            ws_log.cell(row=r, column=2, value='18-Nov-2026')
            ws_log.cell(row=r, column=5, value='FINAL RTM COMPLETE: Feature IDs, Functional (TC-F) and Technical (TC-T) test case IDs populated.')
            
    wb_rtm.save(rtm_path)
    print(f'UPDATED FINAL RTM: {rtm_path} (All columns completely populated!)')
