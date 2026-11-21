import os
from openpyxl import Workbook, load_workbook
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter

os.makedirs(r'c:\Users\Hp\Downloads\hcl\docs', exist_ok=True)
wb = Workbook()

HEX_HEADER_FILL = '1A5376'
HEX_SUBHEADER_FILL = '2E86AB'
HEX_ALT_ROW = 'EBF5FB'
HEX_WHITE = 'FFFFFF'
HEX_BORDER = 'BDC3C7'

font_title = Font(name='Calibri', size=14, bold=True, color=HEX_WHITE)
font_header = Font(name='Calibri', size=11, bold=True, color=HEX_WHITE)
font_bold = Font(name='Calibri', size=10, bold=True)
font_regular = Font(name='Calibri', size=10)
font_code = Font(name='Consolas', size=9)

align_center = Alignment(horizontal='center', vertical='center', wrap_text=True)
align_left = Alignment(horizontal='left', vertical='center', wrap_text=True)

thin_border = Border(
    left=Side(style='thin', color=HEX_BORDER),
    right=Side(style='thin', color=HEX_BORDER),
    top=Side(style='thin', color=HEX_BORDER),
    bottom=Side(style='thin', color=HEX_BORDER)
)

fill_header = PatternFill(start_color=HEX_HEADER_FILL, end_color=HEX_HEADER_FILL, fill_type='solid')
fill_sub = PatternFill(start_color=HEX_SUBHEADER_FILL, end_color=HEX_SUBHEADER_FILL, fill_type='solid')
fill_alt = PatternFill(start_color=HEX_ALT_ROW, end_color=HEX_ALT_ROW, fill_type='solid')
fill_white = PatternFill(start_color=HEX_WHITE, end_color=HEX_WHITE, fill_type='solid')

def style_table(ws, start_row, headers, data, col_widths=None):
    # Header
    for c_idx, h in enumerate(headers, start=1):
        cell = ws.cell(row=start_row, column=c_idx, value=h)
        cell.fill = fill_header
        cell.font = font_header
        cell.alignment = align_center
        cell.border = thin_border
    ws.row_dimensions[start_row].height = 26
    
    # Data
    curr_row = start_row + 1
    for r_data in data:
        row_fill = fill_alt if (curr_row % 2 == 0) else fill_white
        for c_idx, val in enumerate(r_data, start=1):
            cell = ws.cell(row=curr_row, column=c_idx, value=val)
            cell.fill = row_fill
            cell.border = thin_border
            cell.font = font_regular
            if c_idx in [1, 3, 4, 5]:
                cell.alignment = align_center
            else:
                cell.alignment = align_left
        ws.row_dimensions[curr_row].height = 20
        curr_row += 1

    if col_widths:
        for col_letter, width in col_widths.items():
            ws.column_dimensions[col_letter].width = width

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SHEET 1: Overview
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ws_over = wb.active
ws_over.title = 'Overview'
ws_over.views.sheetView[0].showGridLines = True

ws_over.merge_cells('A1:F1')
t_cell = ws_over.cell(row=1, column=1, value='DISEASE TREND ANALYSIS — RELATIONAL DATABASE ARCHITECTURE')
t_cell.fill = fill_header
t_cell.font = font_title
t_cell.alignment = align_center
ws_over.row_dimensions[1].height = 35

overview_meta = [
    ('Project ID & Title', 'P100 | Disease Trend Analysis'),
    ('Domain', 'Healthcare Data Analytics / Public Health Surveillance'),
    ('Architect', 'Arg Jain (Roll No. 2500320140031), MCA 2nd Yr DA, ABES'),
    ('Faculty Mentor', 'Mr. Dinesh'),
    ('Database Engine', 'SQLite 3 (Serverless Relational Engine with Foreign Key Support)'),
    ('Normalization Standard', 'Third Normal Form (3NF) for Base Tables + Denormalized Analytical View'),
    ('Total Entity Tables', '5 Base Tables (3 Masters + 1 Main Fact + 1 Demographic Fact)'),
    ('Analytical Views', '1 Materialized Query View (v_disease_analysis with ~35 columns)'),
    ('Observation Scope', '5 Diseases, 10 States, 60 Months (2020-2024), 5 Age Groups, 3 Genders'),
    ('Fact Table Volume', '3,003 Rows in disease_cases (including 3 audit test duplicates)'),
]

for idx, (k, v) in enumerate(overview_meta, start=3):
    c1 = ws_over.cell(row=idx, column=1, value=k)
    c1.fill = fill_sub
    c1.font = font_header
    c1.alignment = align_left
    c1.border = thin_border
    
    ws_over.merge_cells(start_row=idx, start_column=2, end_row=idx, end_column=6)
    c2 = ws_over.cell(row=idx, column=2, value=v)
    c2.fill = fill_white
    c2.font = font_regular
    c2.alignment = align_left
    c2.border = thin_border
    ws_over.row_dimensions[idx].height = 22

ws_over.column_dimensions['A'].width = 28
ws_over.column_dimensions['B'].width = 20
ws_over.column_dimensions['C'].width = 20
ws_over.column_dimensions['D'].width = 20
ws_over.column_dimensions['E'].width = 20
ws_over.column_dimensions['F'].width = 20

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SHEET 2: Tables_Summary
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ws_ts = wb.create_sheet(title='Tables_Summary')
ws_ts.views.sheetView[0].showGridLines = True

ts_headers = ['Table Name', 'Table Type', 'Granularity (Grain)', 'Primary Key', 'Foreign Keys', 'Columns Count', 'Est. Rows', 'Architectural Role']
ts_data = [
    ['disease_master', 'Master / Dimension', 'One record per disease entity', 'disease_id', 'None', 6, 5, 'Reference taxonomy & contagion metadata'],
    ['region_master', 'Master / Dimension', 'One record per Indian state', 'region_id', 'None', 7, 10, 'Geospatial attributes & census population/area'],
    ['demographic_group', 'Master / Dimension', 'One record per age cohort x gender', 'demo_id', 'None', 5, 15, 'Demographic classification matrix'],
    ['disease_cases', 'Transaction Fact', 'Disease x State x Calendar Month', 'case_id', 'disease_id, region_id', 14, 3003, 'Core incident cases, deaths, recoveries & active'],
    ['demographic_breakdown', 'Sub-fact / Bridge', 'Case Record x Demographic Group', 'breakdown_id', 'case_id, demo_id', 6, 300, 'Granular demographic distribution of cases'],
    ['v_disease_analysis', 'Analytical View', 'Denormalized joined analytical record', 'case_id (logical)', 'Inherited from fact', 35, 3000, 'Unified querying view with computed KPIs'],
]
style_table(ws_ts, 1, ts_headers, ts_data, {
    'A': 24, 'B': 18, 'C': 34, 'D': 14, 'E': 22, 'F': 14, 'G': 12, 'H': 40
})

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SHEET 3: DD_disease_master
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ws_dd1 = wb.create_sheet(title='DD_disease_master')
ws_dd1.views.sheetView[0].showGridLines = True
dd_headers = ['Column Name', 'Data Type', 'Key Type', 'Nullable', 'Allowed Values / Range', 'Description', 'OQ / BR Supported']
dd1_data = [
    ['disease_id', 'INTEGER', 'PRIMARY KEY', 'No', '1 to 5', 'Unique surrogate identifier for each disease', 'All OQs / BR-10'],
    ['disease_name', 'TEXT', 'UNIQUE', 'No', 'Dengue, Malaria, Tuberculosis, COVID-19, Typhoid', 'Standard clinical disease name', 'OQ-01, 02, 03 / BR-01'],
    ['disease_category', 'TEXT', 'None', 'No', 'Vector-borne, Airborne, Waterborne', 'Epidemiological transmission vector', 'OQ-03, 10 / BR-06'],
    ['description', 'TEXT', 'None', 'Yes', 'Free text description', 'Clinical summary and pathogen pathology', 'Informational'],
    ['is_contagious', 'INTEGER', 'None', 'No', '0 or 1 (CHECK)', 'Binary indicator for human-to-human transmission', 'BR-01, BR-05'],
    ['typical_incubation_days', 'INTEGER', 'None', 'No', '1 to 60', 'Standard incubation period in days', 'BR-05, BR-06'],
]
style_table(ws_dd1, 1, dd_headers, dd1_data, {'A': 24, 'B': 14, 'C': 16, 'D': 12, 'E': 36, 'F': 44, 'G': 20})

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SHEET 4: DD_region_master
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ws_dd2 = wb.create_sheet(title='DD_region_master')
ws_dd2.views.sheetView[0].showGridLines = True
dd2_data = [
    ['region_id', 'INTEGER', 'PRIMARY KEY', 'No', '1 to 10', 'Surrogate key for state boundary', 'All OQs / BR-10'],
    ['region_name', 'TEXT', 'UNIQUE', 'No', 'Uttar Pradesh, Maharashtra, Delhi, Rajasthan, Bihar, West Bengal, Tamil Nadu, Karnataka, Gujarat, Madhya Pradesh', 'Official Indian state/UT name', 'OQ-02, 05 / BR-02'],
    ['state_code', 'TEXT', 'UNIQUE', 'No', 'UP, MH, DL, RJ, BR, WB, TN, KA, GJ, MP', 'Two-letter ISO state code', 'OQ-02 / BR-02'],
    ['zone', 'TEXT', 'None', 'No', 'North, South, East, West, Central', 'Geographic administrative zone of India', 'OQ-02 / BR-02'],
    ['population', 'INTEGER', 'None', 'No', '> 0 (1M to 250M)', 'Census population count', 'OQ-06 / BR-08'],
    ['area_sqkm', 'REAL', 'None', 'No', '> 0 (1,000 to 350,000)', 'Geographic surface area in square kilometers', 'OQ-06 / BR-08'],
    ['population_density', 'REAL', 'None', 'No', 'population / area_sqkm', 'Derived population density (persons per sq. km)', 'OQ-06 / BR-08'],
]
style_table(ws_dd2, 1, dd_headers, dd2_data, {'A': 22, 'B': 14, 'C': 16, 'D': 12, 'E': 42, 'F': 44, 'G': 20})

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SHEET 5: DD_demographic_group
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ws_dd3 = wb.create_sheet(title='DD_demographic_group')
ws_dd3.views.sheetView[0].showGridLines = True
dd3_data = [
    ['demo_id', 'INTEGER', 'PRIMARY KEY', 'No', '1 to 15', 'Unique demographic cohort identifier', 'OQ-04 / BR-04'],
    ['age_group', 'TEXT', 'None', 'No', '0-14, 15-29, 30-44, 45-59, 60+', 'Standard 15-year age cohort bracket', 'OQ-04 / BR-04'],
    ['gender', 'TEXT', 'None', 'No', 'Male, Female, Other', 'Biological and social gender identity', 'OQ-04 / BR-04'],
    ['age_min', 'INTEGER', 'None', 'No', '0 to 60', 'Lower age bound (inclusive)', 'OQ-04 / BR-04'],
    ['age_max', 'INTEGER', 'None', 'No', '14 to 99', 'Upper age bound (inclusive)', 'OQ-04 / BR-04'],
]
style_table(ws_dd3, 1, dd_headers, dd3_data, {'A': 20, 'B': 14, 'C': 16, 'D': 12, 'E': 28, 'F': 44, 'G': 20})

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SHEET 6: DD_disease_cases (Main Fact Table)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ws_dd4 = wb.create_sheet(title='DD_disease_cases')
ws_dd4.views.sheetView[0].showGridLines = True
dd4_data = [
    ['case_id', 'INTEGER', 'PRIMARY KEY', 'No', '1 to 3003', 'Unique surrogate transactional transaction key', 'All OQs / BR-10'],
    ['disease_id', 'INTEGER', 'FOREIGN KEY', 'No', 'References disease_master(disease_id)', 'FK link to disease entity', 'All OQs / BR-01'],
    ['region_id', 'INTEGER', 'FOREIGN KEY', 'No', 'References region_master(region_id)', 'FK link to geographic state', 'All OQs / BR-02'],
    ['report_date', 'DATE', 'None', 'No', '2020-01-01 to 2024-12-01', 'First day of the reporting month (ISO 8601)', 'OQ-01, 03, 09 / BR-01'],
    ['report_year', 'INTEGER', 'None', 'No', '2020, 2021, 2022, 2023, 2024', 'Calendar observation year for fast filtering', 'OQ-01, 09 / BR-01, 09'],
    ['report_month', 'INTEGER', 'None', 'No', '1 to 12', 'Calendar month (1=Jan .. 12=Dec)', 'OQ-03, 10 / BR-06'],
    ['cases_reported', 'INTEGER', 'None', 'No (Cleaned)', '>= 0 (CHECK)', 'Total clinical confirmed incident cases in state-month', 'OQ-01, 02 / BR-01'],
    ['deaths', 'INTEGER', 'None', 'No (Cleaned)', '0 <= deaths <= cases_reported (CHECK)', 'Reported disease-specific mortalities', 'OQ-05 / BR-03'],
    ['recovered', 'INTEGER', 'None', 'No', '0 <= recovered <= cases_reported (CHECK)', 'Documented clinical discharges / recoveries', 'OQ-07 / BR-07'],
    ['active_cases', 'INTEGER', 'None', 'No', 'cases - deaths - recovered (>= 0)', 'Net ongoing active caseload at month end', 'BR-01, BR-02'],
    ['hospitalized', 'INTEGER', 'None', 'No', '0 <= hospitalized <= cases_reported', 'Caseload requiring in-patient bed admission', 'BR-02'],
    ['is_outbreak', 'INTEGER', 'None', 'No', '0 or 1', 'Outbreak anomaly flag (cases > 1.5x historical mean)', 'OQ-08 / BR-05'],
    ['data_source', 'TEXT', 'None', 'No', 'ICMR Synthetic, State Health Dept, WHO India', 'Originating reporting institutional body', 'Audit / BR-10'],
    ['created_at', 'TIMESTAMP', 'None', 'No', 'ISO timestamp', 'Database load and audit creation timestamp', 'Audit / BR-10'],
]
style_table(ws_dd4, 1, dd_headers, dd4_data, {'A': 22, 'B': 14, 'C': 16, 'D': 14, 'E': 38, 'F': 48, 'G': 20})

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SHEET 7: DD_demographic_breakdown
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ws_dd5 = wb.create_sheet(title='DD_demographic_breakdown')
ws_dd5.views.sheetView[0].showGridLines = True
dd5_data = [
    ['breakdown_id', 'INTEGER', 'PRIMARY KEY', 'No', '1 to 300+', 'Surrogate identifier for demographic slice', 'OQ-04 / BR-04'],
    ['case_id', 'INTEGER', 'FOREIGN KEY', 'No', 'References disease_cases(case_id)', 'Foreign key link to specific state-month case batch', 'OQ-04 / BR-04'],
    ['demo_id', 'INTEGER', 'FOREIGN KEY', 'No', 'References demographic_group(demo_id)', 'Foreign key link to demographic cohort', 'OQ-04 / BR-04'],
    ['cases_in_group', 'INTEGER', 'None', 'No', '>= 0', 'Number of incident cases belonging to this demographic cohort', 'OQ-04 / BR-04'],
    ['deaths_in_group', 'INTEGER', 'None', 'No', '0 <= deaths <= cases_in_group', 'Number of fatalities within this cohort', 'OQ-04 / BR-04'],
    ['recovered_in_group', 'INTEGER', 'None', 'No', '0 <= recov <= cases_in_group', 'Number of patient recoveries within this cohort', 'OQ-04 / BR-04'],
]
style_table(ws_dd5, 1, dd_headers, dd5_data, {'A': 22, 'B': 14, 'C': 16, 'D': 12, 'E': 36, 'F': 48, 'G': 20})

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SHEET 8: Relationships
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ws_rel = wb.create_sheet(title='Relationships')
ws_rel.views.sheetView[0].showGridLines = True
rel_headers = ['Relationship ID', 'Parent Table', 'Child Table', 'Foreign Key / Join Column', 'Cardinality', 'Referential Rule', 'Operational Purpose']
rel_data = [
    ['REL-01', 'disease_master', 'disease_cases', 'disease_id', 'One-to-Many (1:N)', 'ON DELETE RESTRICT', 'Every disease case record must reference a valid disease entity.'],
    ['REL-02', 'region_master', 'disease_cases', 'region_id', 'One-to-Many (1:N)', 'ON DELETE RESTRICT', 'Every disease case record must belong to a known state jurisdiction.'],
    ['REL-03', 'disease_cases', 'demographic_breakdown', 'case_id', 'One-to-Many (1:N)', 'ON DELETE CASCADE', 'Case records are partitioned into detailed demographic sub-slices.'],
    ['REL-04', 'demographic_group', 'demographic_breakdown', 'demo_id', 'One-to-Many (1:N)', 'ON DELETE RESTRICT', 'Every demographic breakdown row references a valid age-gender cohort.'],
]
style_table(ws_rel, 1, rel_headers, rel_data, {'A': 18, 'B': 22, 'C': 26, 'D': 24, 'E': 20, 'F': 22, 'G': 46})

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SHEET 9: KPIs_Measures
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ws_kpi = wb.create_sheet(title='KPIs_Measures')
ws_kpi.views.sheetView[0].showGridLines = True
kpi_headers = ['Measure / KPI Name', 'Mathematical Formula', 'Units', 'Aggregation Grain', 'Governing OQ', 'Governing BR']
kpi_data = [
    ['Total Incident Cases', 'SUM(cases_reported)', 'Count (Cases)', 'Dynamic per Filter Slice', 'OQ-01, 02', 'BR-01, BR-02'],
    ['Total Fatalities', 'SUM(deaths)', 'Count (Deaths)', 'Dynamic per Filter Slice', 'OQ-05', 'BR-03'],
    ['Total Recoveries', 'SUM(recovered)', 'Count (Patients)', 'Dynamic per Filter Slice', 'OQ-07', 'BR-07'],
    ['Case Fatality Rate (CFR %)', '(SUM(deaths) / SUM(cases_reported)) * 100', 'Percentage (0.00%)', 'Per Disease / State / Period', 'OQ-05', 'BR-03'],
    ['Clinical Recovery Rate (%)', '(SUM(recovered) / SUM(cases_reported)) * 100', 'Percentage (0.00%)', 'Per Disease / State / Period', 'OQ-07', 'BR-07'],
    ['Incidence per Lakh', '(SUM(cases) / population) * 100,000', 'Rate per 100,000', 'State Annual / Monthly', 'OQ-06', 'BR-08'],
    ['Year-over-Year Delta (YoY %)', '((Cases_t - Cases_t-1) / Cases_t-1) * 100', 'Percentage (+/- 0.0%)', 'Annual per Disease', 'OQ-09', 'BR-09'],
    ['Seasonal Transmission Index', 'AVG(cases_month) / AVG(cases_annual)', 'Normalized Ratio', 'Calendar Month (1-12)', 'OQ-03, 10', 'BR-06'],
    ['Concurrent Outbreak Flag', 'COUNT(Diseases where Cases > 1.5 * Mean) >= 2', 'Binary (1 / 0)', 'State-Month Level', 'OQ-08', 'BR-05'],
]
style_table(ws_kpi, 1, kpi_headers, kpi_data, {'A': 28, 'B': 44, 'C': 20, 'D': 24, 'E': 16, 'F': 16})

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SHEET 10: SQLite_DDL
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ws_ddl = wb.create_sheet(title='SQLite_DDL')
ws_ddl.views.sheetView[0].showGridLines = True

ws_ddl.cell(row=1, column=1, value='EXECUTABLE SQLITE DDL STATEMENTS').fill = fill_header
ws_ddl.cell(row=1, column=1).font = font_title
ws_ddl.row_dimensions[1].height = 28

ddl_blocks = [
    ("PRAGMA Settings", "PRAGMA foreign_keys = ON;"),
    ("TABLE: disease_master",
     "CREATE TABLE IF NOT EXISTS disease_master (\n"
     "    disease_id INTEGER PRIMARY KEY,\n"
     "    disease_name TEXT NOT NULL UNIQUE,\n"
     "    disease_category TEXT NOT NULL,\n"
     "    description TEXT,\n"
     "    is_contagious INTEGER NOT NULL CHECK (is_contagious IN (0, 1)),\n"
     "    typical_incubation_days INTEGER NOT NULL CHECK (typical_incubation_days > 0)\n"
     ");"),
    ("TABLE: region_master",
     "CREATE TABLE IF NOT EXISTS region_master (\n"
     "    region_id INTEGER PRIMARY KEY,\n"
     "    region_name TEXT NOT NULL UNIQUE,\n"
     "    state_code TEXT NOT NULL UNIQUE,\n"
     "    zone TEXT NOT NULL,\n"
     "    population INTEGER NOT NULL CHECK (population > 0),\n"
     "    area_sqkm REAL NOT NULL CHECK (area_sqkm > 0),\n"
     "    population_density REAL NOT NULL CHECK (population_density >= 0)\n"
     ");"),
    ("TABLE: demographic_group",
     "CREATE TABLE IF NOT EXISTS demographic_group (\n"
     "    demo_id INTEGER PRIMARY KEY,\n"
     "    age_group TEXT NOT NULL,\n"
     "    gender TEXT NOT NULL,\n"
     "    age_min INTEGER NOT NULL CHECK (age_min >= 0),\n"
     "    age_max INTEGER NOT NULL CHECK (age_max >= age_min),\n"
     "    UNIQUE (age_group, gender)\n"
     ");"),
    ("TABLE: disease_cases",
     "CREATE TABLE IF NOT EXISTS disease_cases (\n"
     "    case_id INTEGER PRIMARY KEY,\n"
     "    disease_id INTEGER NOT NULL,\n"
     "    region_id INTEGER NOT NULL,\n"
     "    report_date DATE NOT NULL,\n"
     "    report_year INTEGER NOT NULL CHECK (report_year BETWEEN 2020 AND 2026),\n"
     "    report_month INTEGER NOT NULL CHECK (report_month BETWEEN 1 AND 12),\n"
     "    cases_reported INTEGER NOT NULL CHECK (cases_reported >= 0),\n"
     "    deaths INTEGER NOT NULL CHECK (deaths >= 0 AND deaths <= cases_reported),\n"
     "    recovered INTEGER NOT NULL CHECK (recovered >= 0 AND recovered <= cases_reported),\n"
     "    active_cases INTEGER NOT NULL CHECK (active_cases >= 0),\n"
     "    hospitalized INTEGER NOT NULL CHECK (hospitalized >= 0 AND hospitalized <= cases_reported),\n"
     "    is_outbreak INTEGER NOT NULL CHECK (is_outbreak IN (0, 1)),\n"
     "    data_source TEXT NOT NULL,\n"
     "    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\n"
     "    FOREIGN KEY (disease_id) REFERENCES disease_master (disease_id) ON DELETE RESTRICT,\n"
     "    FOREIGN KEY (region_id) REFERENCES region_master (region_id) ON DELETE RESTRICT\n"
     ");"),
    ("TABLE: demographic_breakdown",
     "CREATE TABLE IF NOT EXISTS demographic_breakdown (\n"
     "    breakdown_id INTEGER PRIMARY KEY,\n"
     "    case_id INTEGER NOT NULL,\n"
     "    demo_id INTEGER NOT NULL,\n"
     "    cases_in_group INTEGER NOT NULL CHECK (cases_in_group >= 0),\n"
     "    deaths_in_group INTEGER NOT NULL CHECK (deaths_in_group >= 0 AND deaths_in_group <= cases_in_group),\n"
     "    recovered_in_group INTEGER NOT NULL CHECK (recovered_in_group >= 0 AND recovered_in_group <= cases_in_group),\n"
     "    FOREIGN KEY (case_id) REFERENCES disease_cases (case_id) ON DELETE CASCADE,\n"
     "    FOREIGN KEY (demo_id) REFERENCES demographic_group (demo_id) ON DELETE RESTRICT\n"
     ");"),
    ("INDEXES FOR QUERY ACCELERATION",
     "CREATE INDEX IF NOT EXISTS idx_cases_disease ON disease_cases (disease_id);\n"
     "CREATE INDEX IF NOT EXISTS idx_cases_region ON disease_cases (region_id);\n"
     "CREATE INDEX IF NOT EXISTS idx_cases_date ON disease_cases (report_year, report_month);\n"
     "CREATE INDEX IF NOT EXISTS idx_breakdown_case ON demographic_breakdown (case_id);\n"
     "CREATE INDEX IF NOT EXISTS idx_breakdown_demo ON demographic_breakdown (demo_id);"),
    ("VIEW: v_disease_analysis",
     "CREATE VIEW IF NOT EXISTS v_disease_analysis AS\n"
     "SELECT\n"
     "    dc.case_id,\n"
     "    dc.report_date,\n"
     "    dc.report_year,\n"
     "    dc.report_month,\n"
     "    dm.disease_id,\n"
     "    dm.disease_name,\n"
     "    dm.disease_category,\n"
     "    dm.is_contagious,\n"
     "    rm.region_id,\n"
     "    rm.region_name,\n"
     "    rm.state_code,\n"
     "    rm.zone,\n"
     "    rm.population,\n"
     "    rm.area_sqkm,\n"
     "    rm.population_density,\n"
     "    dc.cases_reported,\n"
     "    dc.deaths,\n"
     "    dc.recovered,\n"
     "    dc.active_cases,\n"
     "    dc.hospitalized,\n"
     "    dc.is_outbreak,\n"
     "    ROUND(CAST(dc.deaths AS REAL) / NULLIF(dc.cases_reported, 0) * 100, 2) AS cfr_pct,\n"
     "    ROUND(CAST(dc.recovered AS REAL) / NULLIF(dc.cases_reported, 0) * 100, 2) AS recovery_rate_pct,\n"
     "    ROUND(CAST(dc.cases_reported AS REAL) / rm.population * 100000, 2) AS incidence_per_lakh,\n"
     "    dc.data_source,\n"
     "    dc.created_at\n"
     "FROM disease_cases dc\n"
     "JOIN disease_master dm ON dc.disease_id = dm.disease_id\n"
     "JOIN region_master rm ON dc.region_id = rm.region_id;"),
]

row_idx = 3
for block_title, sql_text in ddl_blocks:
    c_title = ws_ddl.cell(row=row_idx, column=1, value=f'-- {block_title}')
    c_title.fill = fill_sub
    c_title.font = font_header
    ws_ddl.row_dimensions[row_idx].height = 22
    row_idx += 1
    
    c_sql = ws_ddl.cell(row=row_idx, column=1, value=sql_text)
    c_sql.font = font_code
    c_sql.alignment = align_left
    c_sql.fill = fill_alt
    ws_ddl.row_dimensions[row_idx].height = max(35, len(sql_text.split('\n')) * 15)
    row_idx += 2

ws_ddl.column_dimensions['A'].width = 110

save_path = r'c:\Users\Hp\Downloads\hcl\docs\08_ArgJain_DiseaseTrendAnalysis_DBDesign.xlsx'
wb.save(save_path)
print(f'SAVED: {save_path}')

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ALSO UPDATE RTM with "DB Table.Column"
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
rtm_path = r'c:\Users\Hp\Downloads\hcl\docs\04_ArgJain_DiseaseTrendAnalysis_RTM.xlsx'
if os.path.exists(rtm_path):
    wb_rtm = load_workbook(rtm_path)
    ws_r = wb_rtm['RTM']
    
    db_mapping = {
        'BR-01': 'disease_cases.cases_reported, report_date',
        'BR-02': 'region_master.region_name, disease_cases.cases_reported',
        'BR-03': 'disease_cases.deaths, disease_cases.cases_reported',
        'BR-04': 'demographic_breakdown.cases_in_group, demo_id',
        'BR-05': 'disease_cases.is_outbreak, cases_reported',
        'BR-06': 'disease_cases.report_month, cases_reported',
        'BR-07': 'disease_cases.recovered, cases_reported',
        'BR-08': 'region_master.population_density, cases_reported',
        'BR-09': 'disease_cases.report_year, cases_reported',
        'BR-10': 'Entire Schema (app.db all 5 tables)',
        'BR-11': 'Sidebar Filter Dimensions across all tables',
        'BR-12': 'v_disease_analysis (all 35 columns)',
        'BR-13': 'Data Pipeline Audit Metadata',
        'BR-14': 'All Tables & Constraints',
        'BR-15': 'data/app.db deployment asset',
    }
    
    for row in range(2, ws_r.max_row + 1):
        br_id = ws_r.cell(row=row, column=3).value
        if br_id in db_mapping:
            cell = ws_r.cell(row=row, column=9)
            cell.value = db_mapping[br_id]
            cell.font = font_regular
            cell.fill = fill_white
            cell.alignment = align_left
            
    # Update Change Log
    ws_log = wb_rtm['Change_Log']
    for r in range(2, ws_log.max_row + 1):
        if ws_log.cell(row=r, column=1).value == 'v1.1':
            ws_log.cell(row=r, column=2, value='18-Nov-2026')
            ws_log.cell(row=r, column=5, value='Populated DB Table.Column mapping for all requirements.')
            
    wb_rtm.save(rtm_path)
    print(f'UPDATED RTM: {rtm_path} (DB Table.Column populated)')
