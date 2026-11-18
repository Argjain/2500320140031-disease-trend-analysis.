import os
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter

os.makedirs(r'c:\Users\Hp\Downloads\hcl\docs', exist_ok=True)
wb = Workbook()

# Colors
HEX_HEADER_FILL = '1A5376' # Deep Blue
HEX_WHITE = 'FFFFFF'
HEX_MUST_FILL = 'EAFAF1' # Light Green
HEX_SHOULD_FILL = 'FEF9E7' # Light Yellow
HEX_COULD_FILL = 'FDEBD0' # Light Orange
HEX_STATUS_FILL = 'EBF5FB' # Light Blue
HEX_TBD_FILL = 'F2F3F4' # Light Grey
HEX_BORDER = 'BDC3C7'

font_header = Font(name='Calibri', size=11, bold=True, color=HEX_WHITE)
font_regular = Font(name='Calibri', size=10)
font_bold = Font(name='Calibri', size=10, bold=True)
font_tbd = Font(name='Calibri', size=9, italic=True, color='7F8C8D')

align_center = Alignment(horizontal='center', vertical='center', wrap_text=True)
align_left = Alignment(horizontal='left', vertical='center', wrap_text=True)

thin_border = Border(
    left=Side(style='thin', color=HEX_BORDER),
    right=Side(style='thin', color=HEX_BORDER),
    top=Side(style='thin', color=HEX_BORDER),
    bottom=Side(style='thin', color=HEX_BORDER)
)

fill_header = PatternFill(start_color=HEX_HEADER_FILL, end_color=HEX_HEADER_FILL, fill_type='solid')
fill_must = PatternFill(start_color=HEX_MUST_FILL, end_color=HEX_MUST_FILL, fill_type='solid')
fill_should = PatternFill(start_color=HEX_SHOULD_FILL, end_color=HEX_SHOULD_FILL, fill_type='solid')
fill_could = PatternFill(start_color=HEX_COULD_FILL, end_color=HEX_COULD_FILL, fill_type='solid')
fill_status = PatternFill(start_color=HEX_STATUS_FILL, end_color=HEX_STATUS_FILL, fill_type='solid')
fill_tbd = PatternFill(start_color=HEX_TBD_FILL, end_color=HEX_TBD_FILL, fill_type='solid')

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SHEET 1: RTM (Requirements Traceability Matrix)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ws_rtm = wb.active
ws_rtm.title = 'RTM'
ws_rtm.views.sheetView[0].showGridLines = True

headers = [
    'OQ ID',
    'HMW ID',
    'Req ID (BR)',
    'Requirement Description',
    'Stakeholder (SH)',
    'Priority',
    'Status',
    'Feature ID',
    'DB Table.Column',
    'User Story ID',
    'UI Screen ID',
    'Test Case (TC-F)',
    'Test Case (TC-T)'
]

ws_rtm.append(headers)
for col_idx in range(1, len(headers) + 1):
    cell = ws_rtm.cell(row=1, column=col_idx)
    cell.fill = fill_header
    cell.font = font_header
    cell.alignment = align_center
    cell.border = thin_border
ws_rtm.row_dimensions[1].height = 28

rtm_rows = [
    ('OQ-01', 'HMW-01', 'BR-01', 'Aggregate disease case counts by disease, region and time period', 'SH-01, SH-03', 'Must', 'Identified'),
    ('OQ-09', 'HMW-09', 'BR-01', 'Aggregate disease case counts by disease, region and time period', 'SH-01, SH-03', 'Must', 'Identified'),
    ('OQ-02', 'HMW-02', 'BR-02', 'Provide region-level disease comparison across all states', 'SH-02', 'Must', 'Identified'),
    ('OQ-05', 'HMW-03', 'BR-03', 'Display Case Fatality Rates (CFR) across diseases and regions', 'SH-03', 'Must', 'Identified'),
    ('OQ-04', 'HMW-04', 'BR-04', 'Demographic filtering and breakdown by age group and gender', 'SH-04', 'Must', 'Identified'),
    ('OQ-08', 'HMW-05', 'BR-05', 'Detect concurrent multi-disease outbreaks in same region-month', 'SH-01, SH-04', 'Must', 'Identified'),
    ('OQ-03', 'HMW-06', 'BR-06', 'Seasonal and monthly disease outbreak cycle profiling', 'SH-01, SH-04', 'Must', 'Identified'),
    ('OQ-10', 'HMW-06', 'BR-06', 'Identify peak transmission months across all diseases', 'SH-01, SH-04', 'Must', 'Identified'),
    ('OQ-07', 'HMW-07', 'BR-07', 'Compute and display recovery rates per disease and region', 'SH-02', 'Must', 'Identified'),
    ('OQ-06', 'HMW-08', 'BR-08', 'Evaluate disease incidence vs population density correlation', 'SH-04', 'Should', 'Identified'),
    ('OQ-09', 'HMW-09', 'BR-09', 'Calculate year-over-year percentage change per disease', 'SH-03', 'Should', 'Identified'),
    ('OQ-01..10', 'HMW-10', 'BR-10', 'Store disease intelligence in structured SQLite relational database', 'SH-05', 'Must', 'Identified'),
    ('OQ-01', 'HMW-01', 'BR-11', 'Multidimensional sidebar filters updating all visuals concurrently', 'SH-01..04', 'Must', 'Identified'),
    ('OQ-02', 'HMW-02', 'BR-11', 'Multidimensional sidebar filters updating all visuals concurrently', 'SH-01..04', 'Must', 'Identified'),
    ('OQ-05', 'HMW-03', 'BR-11', 'Multidimensional sidebar filters updating all visuals concurrently', 'SH-01..04', 'Must', 'Identified'),
    ('OQ-04', 'HMW-04', 'BR-11', 'Multidimensional sidebar filters updating all visuals concurrently', 'SH-01..04', 'Must', 'Identified'),
    ('OQ-08', 'HMW-05', 'BR-11', 'Multidimensional sidebar filters updating all visuals concurrently', 'SH-01..04', 'Must', 'Identified'),
    ('OQ-01..10', 'HMW-10', 'BR-12', 'Export filtered analytical datasets to CSV for offline analysis', 'SH-04, SH-05', 'Should', 'Identified'),
    ('OQ-01..10', 'HMW-10', 'BR-13', 'Transparent data quality audit summary showing cleaning steps', 'SH-05', 'Could', 'Identified'),
    ('OQ-01..10', 'All HMWs', 'BR-14', 'Automated pytest test suite with >=80% coverage and zero failures', 'SH-06', 'Must', 'Identified'),
    ('OQ-01..10', 'OBJ-04', 'BR-15', 'Cloud deployment on Streamlit Community Cloud with public URL', 'SH-05, SH-06', 'Should', 'Identified'),
]

for row_idx, r_data in enumerate(rtm_rows, start=2):
    full_row = list(r_data) + ['TBD', 'TBD', 'TBD', 'TBD', 'TBD', 'TBD']
    ws_rtm.append(full_row)
    ws_rtm.row_dimensions[row_idx].height = 22
    
    priority_val = full_row[5]
    fill_p = fill_must if priority_val == 'Must' else (fill_should if priority_val == 'Should' else fill_could)
    
    for c_idx in range(1, len(full_row) + 1):
        cell = ws_rtm.cell(row=row_idx, column=c_idx)
        cell.border = thin_border
        cell.font = font_regular
        
        if c_idx in [1, 2, 3, 5]:
            cell.alignment = align_center
        elif c_idx == 4:
            cell.alignment = align_left
        elif c_idx == 6: # Priority
            cell.fill = fill_p
            cell.alignment = align_center
            cell.font = font_bold
        elif c_idx == 7: # Status
            cell.fill = fill_status
            cell.alignment = align_center
            cell.font = font_bold
        else: # TBD columns
            cell.fill = fill_tbd
            cell.alignment = align_center
            cell.font = font_tbd

# Freeze header and enable filter
ws_rtm.freeze_panes = 'A2'
ws_rtm.auto_filter.ref = f'A1:M{len(rtm_rows)+1}'

col_widths = {
    'A': 12, 'B': 12, 'C': 12, 'D': 46, 'E': 16,
    'F': 12, 'G': 14, 'H': 14, 'I': 20, 'J': 14,
    'K': 14, 'L': 16, 'M': 16
}
for col, width in col_widths.items():
    ws_rtm.column_dimensions[col].width = width

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SHEET 2: Coverage_Check
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ws_cov = wb.create_sheet(title='Coverage_Check')
ws_cov.views.sheetView[0].showGridLines = True

# Title
ws_cov.merge_cells('A1:E1')
title_cell = ws_cov.cell(row=1, column=1, value='REQUIREMENTS TRACEABILITY COVERAGE AUDIT')
title_cell.font = Font(name='Calibri', size=14, bold=True, color=HEX_WHITE)
title_cell.fill = fill_header
title_cell.alignment = align_center
ws_cov.row_dimensions[1].height = 30

ws_cov.append([])

# Table 1: OQ Coverage
ws_cov.append(['OQ ID', 'Operational Question', 'Linked HMW(s)', 'Linked BR(s)', 'Coverage Status'])
r_idx = 3
for c in range(1, 6):
    cell = ws_cov.cell(row=r_idx, column=c)
    cell.fill = PatternFill(start_color='2E86AB', end_color='2E86AB', fill_type='solid')
    cell.font = font_header
    cell.alignment = align_center
    cell.border = thin_border
ws_cov.row_dimensions[r_idx].height = 22

oq_cov_data = [
    ('OQ-01', 'Diseases with highest 5-year case increase', 'HMW-01, HMW-09', 'BR-01, BR-09, BR-11', 'COVERED (100%)'),
    ('OQ-02', 'Geographic states most affected per disease', 'HMW-02, HMW-03', 'BR-02, BR-11', 'COVERED (100%)'),
    ('OQ-03', 'Monthly / seasonal trend of disease outbreaks', 'HMW-02, HMW-06', 'BR-06, BR-11', 'COVERED (100%)'),
    ('OQ-04', 'Vulnerable age group and gender demographics', 'HMW-04', 'BR-04, BR-11', 'COVERED (100%)'),
    ('OQ-05', 'Case fatality rate (CFR) across diseases/regions', 'HMW-03, HMW-07', 'BR-03, BR-11', 'COVERED (100%)'),
    ('OQ-06', 'Incidence correlation with population density', 'HMW-08', 'BR-08, BR-11', 'COVERED (100%)'),
    ('OQ-07', 'Highest recovery rates and geographic spread', 'HMW-07', 'BR-07, BR-11', 'COVERED (100%)'),
    ('OQ-08', 'Concurrent disease outbreaks in same region-month', 'HMW-05', 'BR-05, BR-11', 'COVERED (100%)'),
    ('OQ-09', 'Year-over-year (YoY) percentage change in cases', 'HMW-01, HMW-09', 'BR-09, BR-01', 'COVERED (100%)'),
    ('OQ-10', 'Peak reporting months by disease type', 'HMW-06', 'BR-06, BR-11', 'COVERED (100%)'),
]

for row_data in oq_cov_data:
    ws_cov.append(list(row_data))
    r_idx += 1
    ws_cov.row_dimensions[r_idx].height = 20
    for c in range(1, 6):
        cell = ws_cov.cell(row=r_idx, column=c)
        cell.border = thin_border
        cell.font = font_regular
        if c in [1, 3, 4]:
            cell.alignment = align_center
        elif c == 5:
            cell.alignment = align_center
            cell.font = font_bold
            cell.fill = fill_must
        else:
            cell.alignment = align_left

ws_cov.append([])
r_idx += 1

# Table 2: HMW Coverage Summary
ws_cov.append(['HMW ID', 'HMW Statement Summary', 'Primary Stakeholder', 'Mapped BR(s)', 'Traceability Status'])
r_idx += 1
for c in range(1, 6):
    cell = ws_cov.cell(row=r_idx, column=c)
    cell.fill = PatternFill(start_color='2E86AB', end_color='2E86AB', fill_type='solid')
    cell.font = font_header
    cell.alignment = align_center
    cell.border = thin_border
ws_cov.row_dimensions[r_idx].height = 22

hmw_cov_data = [
    ('HMW-01 (Priority)', 'Instantly spot spiking disease vs last year', 'SH-01', 'BR-01, BR-11', 'MAPPED (100%)'),
    ('HMW-02 (Priority)', 'Anticipate seasonal state surge for bed allocation', 'SH-02', 'BR-02, BR-11', 'MAPPED (100%)'),
    ('HMW-03 (Priority)', 'Single-glance CFR comparison across states', 'SH-03', 'BR-03, BR-11', 'MAPPED (100%)'),
    ('HMW-04 (Priority)', 'Age and gender demographic drill-down', 'SH-04', 'BR-04, BR-11', 'MAPPED (100%)'),
    ('HMW-05 (Priority)', 'Detect concurrent co-occurring disease outbreaks', 'SH-01, SH-04', 'BR-05, BR-11', 'MAPPED (100%)'),
    ('HMW-06', 'Visualise seasonal peaks across diseases', 'SH-01, SH-04', 'BR-06, BR-11', 'MAPPED (100%)'),
    ('HMW-07', 'Recovery rate benchmarking per region', 'SH-02', 'BR-07, BR-11', 'MAPPED (100%)'),
    ('HMW-08', 'Incidence vs population density correlation', 'SH-04', 'BR-08, BR-11', 'MAPPED (100%)'),
    ('HMW-09', 'Year-over-year trend table of growing threats', 'SH-03', 'BR-09, BR-01', 'MAPPED (100%)'),
    ('HMW-10', 'Downloadable clean dataset and quality ledger', 'SH-05', 'BR-10, BR-12, BR-13', 'MAPPED (100%)'),
]

for row_data in hmw_cov_data:
    ws_cov.append(list(row_data))
    r_idx += 1
    ws_cov.row_dimensions[r_idx].height = 20
    for c in range(1, 6):
        cell = ws_cov.cell(row=r_idx, column=c)
        cell.border = thin_border
        cell.font = font_regular
        if c in [1, 3, 4]:
            cell.alignment = align_center
        elif c == 5:
            cell.alignment = align_center
            cell.font = font_bold
            cell.fill = fill_must
        else:
            cell.alignment = align_left

ws_cov.append([])
r_idx += 1

# Summary Metrics Row
summary_row = ['AUDIT SUMMARY', '10/10 OQs Covered (100%) | 10/10 HMWs Mapped (100%) | 15/15 BRs Traced (100%) | 0 Unmapped Items', '', '', 'ALL CHECKS PASSED']
ws_cov.append(summary_row)
r_idx += 1
ws_cov.merge_cells(f'B{r_idx}:D{r_idx}')
ws_cov.row_dimensions[r_idx].height = 24
for c in range(1, 6):
    cell = ws_cov.cell(row=r_idx, column=c)
    cell.fill = fill_header
    cell.font = font_header
    cell.alignment = align_center
    cell.border = thin_border

for col, width in {'A': 20, 'B': 45, 'C': 22, 'D': 24, 'E': 22}.items():
    ws_cov.column_dimensions[col].width = width

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SHEET 3: Change_Log
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ws_log = wb.create_sheet(title='Change_Log')
ws_log.views.sheetView[0].showGridLines = True

ws_log.append(['Version', 'Release Date', 'Author / Role', 'Step ID', 'Scope of Change / Fields Updated'])
for c in range(1, 6):
    cell = ws_log.cell(row=1, column=c)
    cell.fill = fill_header
    cell.font = font_header
    cell.alignment = align_center
    cell.border = thin_border
ws_log.row_dimensions[1].height = 25

log_data = [
    ('v1.0', '18-Nov-2026', 'Arg Jain (Lead DA)', 'Step 4', 'Initial RTM created with OQ, HMW, BR, SH, Priority, Status columns populated. Later columns marked TBD.'),
    ('v1.1', 'Scheduled', 'Arg Jain (Lead DA)', 'Step 8', 'Database Design: Population of DB Table.Column mapping for all requirements.'),
    ('v1.2', 'Scheduled', 'Arg Jain (Lead DA)', 'Step 11', 'User Stories: Population of User Story IDs (US-01..US-17) and Epics.'),
    ('v1.3', 'Scheduled', 'Arg Jain (Lead DA)', 'Step 12', 'UI Framework: Population of UI Screen IDs (UI-01..UI-06).'),
    ('v1.4', 'Scheduled', 'Arg Jain (Lead DA)', 'Step 13', 'Test Cases: Population of Functional (TC-F) and Technical (TC-T) test case IDs.'),
]

for r_idx, row in enumerate(log_data, start=2):
    ws_log.append(list(row))
    ws_log.row_dimensions[r_idx].height = 20
    for c in range(1, 6):
        cell = ws_log.cell(row=r_idx, column=c)
        cell.border = thin_border
        cell.font = font_regular
        if c in [1, 2, 4]:
            cell.alignment = align_center
        else:
            cell.alignment = align_left

for col, width in {'A': 12, 'B': 16, 'C': 22, 'D': 12, 'E': 60}.items():
    ws_log.column_dimensions[col].width = width

save_path = r'c:\Users\Hp\Downloads\hcl\docs\04_ArgJain_DiseaseTrendAnalysis_RTM.xlsx'
wb.save(save_path)
print(f'SAVED: {save_path}')
