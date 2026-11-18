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
os.makedirs(r'c:\Users\Hp\Downloads\hcl\src', exist_ok=True)
os.makedirs(r'c:\Users\Hp\Downloads\hcl\.streamlit', exist_ok=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 1. WRITE .streamlit/config.toml
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
toml_content = """[theme]
primaryColor = "#1A5376"
backgroundColor = "#F0F8FF"
secondaryBackgroundColor = "#E8F4FD"
textColor = "#2C3E50"
font = "sans serif"

[server]
headless = true
enableCORS = false
enableXsrfProtection = false
"""
with open(r'c:\Users\Hp\Downloads\hcl\.streamlit\config.toml', 'w', encoding='utf-8') as f:
    f.write(toml_content)
print("Saved .streamlit/config.toml")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 2. WRITE src/ui.py
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ui_py_content = '''import streamlit as st
import streamlit.components.v1 as components

TAILWIND_CDN = '<script src="https://cdn.tailwindcss.com"></script>'

def inject_tailwind():
    """Injects Tailwind CSS into an isolated iframe to pre-load utility classes."""
    components.html(f"{TAILWIND_CDN}<div style='display:none;'></div>", height=0)

def render_header(title: str, subtitle: str = ""):
    """Renders a styled responsive executive header banner."""
    html = f"""
    {TAILWIND_CDN}
    <div class="bg-gradient-to-r from-blue-900 to-sky-700 text-white px-6 py-4 rounded-xl shadow-lg mb-4 flex flex-col justify-center">
        <div class="flex items-center space-x-3">
            <span class="text-3xl">🏥</span>
            <div>
                <h1 class="text-2xl md:text-3xl font-extrabold tracking-tight">{title}</h1>
                <p class="text-blue-100 text-xs md:text-sm mt-0.5">{subtitle}</p>
            </div>
        </div>
    </div>
    """
    components.html(html, height=105)

def render_kpi_card(label: str, value: str, delta: str = None, icon: str = "📊", color: str = "#1A5376"):
    """Generates an HTML string for a Tailwind styled KPI stat card."""
    delta_html = ""
    if delta:
        is_pos = delta.startswith("+") or "growth" in delta.lower() or "surge" in delta.lower()
        delta_color = "text-emerald-600 bg-emerald-50" if not is_pos else "text-rose-600 bg-rose-50"
        delta_html = f'<div class="mt-2 text-xs font-semibold px-2 py-0.5 rounded-full inline-block {delta_color}">{delta}</div>'
    
    html = f"""
    {TAILWIND_CDN}
    <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-4 text-center hover:shadow-md transition-shadow">
        <div class="text-2xl mb-1">{icon}</div>
        <div class="text-xs uppercase tracking-wider font-semibold text-slate-500">{label}</div>
        <div class="text-2xl md:text-3xl font-black text-slate-800 mt-1" style="color:{color};">{value}</div>
        {delta_html}
    </div>
    """
    return html

def render_kpi_card_iframe(label: str, value: str, delta: str = None, icon: str = "📊", color: str = "#1A5376", height: int = 145):
    """Renders the KPI card directly inside an iframe component."""
    card_html = render_kpi_card(label, value, delta, icon, color)
    components.html(card_html, height=height)

def render_insight_box(title: str, text: str, alert_type: str = "info"):
    """Renders a styled analytical observation callout box."""
    colors = {
        "info": ("border-blue-500", "bg-blue-50", "text-blue-900", "ℹ️"),
        "warning": ("border-amber-500", "bg-amber-50", "text-amber-900", "⚠️"),
        "danger": ("border-rose-500", "bg-rose-50", "text-rose-900", "🚨"),
        "success": ("border-emerald-500", "bg-emerald-50", "text-emerald-900", "✅"),
    }
    b_col, bg_col, t_col, icon = colors.get(alert_type, colors["info"])
    html = f"""
    {TAILWIND_CDN}
    <div class="border-l-4 {b_col} {bg_col} p-4 rounded-r-lg shadow-xs my-3">
        <div class="flex items-center space-x-2">
            <span class="text-lg">{icon}</span>
            <span class="font-bold text-sm {t_col}">{title}</span>
        </div>
        <p class="text-xs md:text-sm text-slate-700 mt-1 leading-relaxed">{text}</p>
    </div>
    """
    components.html(html, height=95)
'''
with open(r'c:\Users\Hp\Downloads\hcl\src\ui.py', 'w', encoding='utf-8') as f:
    f.write(ui_py_content)
print("Saved src/ui.py")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 3. BUILD WORD DOCUMENT (docs/12_ArgJain_DiseaseTrendAnalysis_UIFramework.docx)
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
run_sub = p_sub.add_run('STEP 12 — User Interface (UI) Architecture & Wireframes')
run_sub.font.size = Pt(14)
run_sub.font.bold = True
run_sub.font.color.rgb = RGBColor(0x2E, 0x86, 0xAB)

doc.add_paragraph()

meta_data = [
    ('Project ID & Title', 'P-01 | Disease Trend Analysis'),
    ('Domain', 'Healthcare Data Analytics'),
    ('UI/UX Architect', 'Arg Jain (Roll No. 2500320140031)'),
    ('Academic Program', 'MCA 2nd Year (Data Analytics Specialization)'),
    ('Institution', 'ABES Engineering College, Ghaziabad'),
    ('Faculty Mentor', 'Ms. Kalpana Dwivedi'),
    ('Document Version', 'v1.0'),
    ('UI Tech Stack', 'Streamlit 1.35 Multi-Page + Tailwind CSS (CDN in iframe) + Plotly 5.22'),
    ('Total Application Screens', '6 Dedicated Analytical Screens (UI-01 to UI-06)'),
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
# 1. SCREEN INVENTORY
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
add_heading_1('1. Application Screen Inventory (UI-01 to UI-06)')
p_si_intro = doc.add_paragraph(
    'The application interface is structured into six dedicated analytical screens conforming to standard '
    'Streamlit multi-page routing conventions under the pages/ directory:'
)
p_si_intro.runs[0].font.size = Pt(10)

screen_headers = ['UI ID', 'Screen Title', 'File Route', 'Analytical Scope', 'Core Visual Components', 'Supported User Stories']
screen_data = [
    ['UI-01', 'Executive Overview & KPIs', 'pages/01_Overview.py', 'High-level epidemiological snapshot and state rankings', '4 Tailwind KPI cards, horizontal bar chart, state CFR table', 'US-04, US-05, US-06, US-07'],
    ['UI-02', 'Longitudinal & Seasonal Trends', 'pages/02_Trends.py', 'Multi-year trajectory and monthly cyclic transmission', '60-month time series line, overlapping YoY lines, cyclic heatmap', 'US-08, US-09, US-10, US-11'],
    ['UI-03', 'Regional Burden & Clinical Efficacy', 'pages/03_Regional_Analysis.py', 'Cross-state mortality and recovery rate benchmarking', 'Ranked state cases bar, CFR percentage bar, recovery vs CFR', 'US-12'],
    ['UI-04', 'Demographic Cohort Drilldown', 'pages/04_Demographics.py', 'Age group and gender vulnerability profiles', 'Stacked age group bar chart, gender distribution donut/pie', 'US-13'],
    ['UI-05', 'Advanced EDA & Surveillance', 'pages/05_EDA_Statistics.py', 'Crowding correlation and co-occurring outbreak alerts', 'Density vs incidence scatter (OLS line), outbreak alert table', 'US-14, US-15'],
    ['UI-06', 'Data Quality Audit & Export', 'pages/06_Data_Quality.py', 'Pipeline transparency ledger and filtered dataset download', 'Cleaning scorecard ledger, null/dupe audits, CSV download trigger', 'US-16, US-17'],
]
t_si = doc.add_table(rows=len(screen_data) + 1, cols=6)
format_table(t_si, [Cm(1.5), Cm(3.2), Cm(3.6), Cm(3.5), Cm(2.5), Cm(1.7)], screen_headers, screen_data)
doc.add_paragraph()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 2. ASCII WIREFRAMES PER SCREEN
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
add_heading_1('2. Comprehensive ASCII Wireframes')

wireframe_ui01 = """+---------------------------------------------------------------------------------------------------+
|  [H1] DISEASE TREND ANALYSIS — EXECUTIVE COCKPIT (pages/01_Overview.py)                           |
+----------------------+----------------------------------------------------------------------------+
| SIDEBAR FILTERS      | [ROW 1: 4 TAILWIND KPI STAT CARDS]                                         |
|                      | +------------------+ +------------------+ +---------------+ +-------------+ |
| Disease:             | | Total Cases      | | Total Deaths     | | Recoveries    | | CFR %       | |
| [ All Diseases    v] | | 1,428,520        | | 31,427           | | 1,328,940     | | 2.20%       | |
|                      | | [+14.2% YoY]     | | [-2.1% YoY]      | | [93.0% Rate]  | | [Stable]    | |
| States:              | +------------------+ +------------------+ +---------------+ +-------------+ |
| [ All 10 States   v] |                                                                            |
|                      | [ROW 2: REGIONAL BURDEN RANKING — Plotly Horizontal Bar Chart]             |
| Observation Years:   |  Maharashtra   |████████████████████████████████████████  320,410          |
| [2020 ====== 2024]   |  Delhi         |██████████████████████████████            241,120          |
|                      |  Uttar Pradesh |████████████████████████                  198,340          |
| Age Cohort:          |  West Bengal   |████████████████                          142,500          |
| [ All Ages        v] |  Bihar         |████████████                              110,230          |
|                      |                                                                            |
| Gender Identity:     | [ROW 3: INSIGHT CALLOUT BOX — Tailwind Blue]                               |
| (o) All  ( ) M  ( )F | "Maharashtra and Delhi account for 39.3% of cumulative national morbidity."|
|                      |                                                                            |
| [ Reset Filters ]    | [ROW 4: STATE-LEVEL CFR BENCHMARK TABLE — Interactive St.DataFrame]        |
|                      | State Name    | Cases    | Deaths | Recoveries | CFR (%) | Trend Badge |
| Active Filters: 0    | Maharashtra   | 320,410  | 7,690  | 298,120    | 2.40%   | High Risk   |
+----------------------+----------------------------------------------------------------------------+"""

wireframe_ui02 = """+---------------------------------------------------------------------------------------------------+
|  [H1] LONGITUDINAL & SEASONAL TRENDS (pages/02_Trends.py)                                          |
+----------------------+----------------------------------------------------------------------------+
| SIDEBAR FILTERS      | [SECTION 1: 60-MONTH LONGITUDINAL TIME SERIES — Plotly Line with Hover]    |
| (Same Persistent     | Cases                                                                      |
|  Session State)      |  50k|                   ▲ (2021 COVID Delta Wave Peak)                     |
|                      |  30k|                  / \\                                                 |
|                      |  10k|   _/\_/\_      _/   \\_      _/\_/\_ (Annual Monsoon Dengue Surges)   |
|                      |   0 +-------------------------------------------------------------> Time   |
|                      |     2020         2021         2022         2023         2024               |
|                      |                                                                            |
|                      | [SECTION 2: MULTI-YEAR OVERLAPPING YoY WAVES (Months 1 to 12)]             |
|                      |   Lines: ── 2020  ── 2021  ── 2022  ── 2023  ── 2024                       |
|                      |                                                                            |
|                      | [SECTION 3: 12-MONTH CYCLICAL TRANSMISSION HEATMAP — Plotly Imshow]        |
|                      | Disease       | Jan | Feb | Mar | Apr | May | Jun | Jul | Aug | Sep | Oct...|
|                      | Dengue        | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [█] | [█] | [█] | [▓]  |
|                      | Malaria       | [ ] | [ ] | [ ] | [ ] | [ ] | [░] | [█] | [█] | [█] | [░]  |
|                      | Tuberculosis  | [▓] | [▓] | [▓] | [▓] | [▓] | [▓] | [▓] | [▓] | [▓] | [▓]  |
+----------------------+----------------------------------------------------------------------------+"""

wireframe_ui05 = """+---------------------------------------------------------------------------------------------------+
|  [H1] ADVANCED EDA & SURVEILLANCE SURGE DETECTOR (pages/05_EDA_Statistics.py)                     |
+----------------------+----------------------------------------------------------------------------+
| SIDEBAR FILTERS      | [SECTION 1: URBAN CROWDING & DENSITY REGRESSION — Plotly Scatter + OLS]    |
| (Same Persistent     | Incidence/Lakh                                                             |
|  Session State)      |       ▲                                                                    |
|                      |   120 |                                       * Delhi (Density: 22,198)    |
|                      |    80 |                             * MH                                   |
|                      |    40 |                * WB     * TN                                       |
|                      |     0 +----------------------------------------------------> Density       |
|                      |         Pearson r = 0.84 | p-value < 0.001 | Strong Positive Correlation   |
|                      |                                                                            |
|                      | [SECTION 2: CONCURRENT OUTBREAK ANOMALY DETECTOR (>=2 Diseases in Surge)]  |
|                      | State       | Month-Year  | Surging Diseases           | Combined Caseload |
|                      | Delhi       | August 2021 | COVID-19, Dengue           | 14,890 (Alert)    |
|                      | Maharashtra | Sept 2022   | Dengue, Malaria, Typhoid   | 18,220 (Critical) |
+----------------------+----------------------------------------------------------------------------+"""

add_heading_2('2.1 Wireframe: UI-01 Executive Overview Dashboard')
add_code_block(wireframe_ui01)
doc.add_paragraph()

add_heading_2('2.2 Wireframe: UI-02 Longitudinal Trends & Seasonality')
add_code_block(wireframe_ui02)
doc.add_paragraph()

add_heading_2('2.3 Wireframe: UI-05 Advanced EDA & Outbreak Surveillance')
add_code_block(wireframe_ui05)
doc.add_paragraph()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 3. GLOBAL LAYOUT, THEME & PALETTE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
add_heading_1('3. Global Layout Architecture & Color Palette')
p_theme_intro = doc.add_paragraph(
    'The visual system implements a healthcare-optimized corporate palette balancing high contrast, '
    'clinical trustworthiness, and accessible data visualization:'
)
p_theme_intro.runs[0].font.size = Pt(10)

palette_headers = ['Color Role', 'Hex Code', 'Visual Description', 'Application Point']
palette_data = [
    ['Primary Dominant', '#1A5376', 'Deep Navy Blue', 'Application headers, table header rows, primary button fills, major axis labels'],
    ['Secondary Accent', '#2E86AB', 'Vibrant Sea Blue', 'Plotly line chart series, secondary button borders, sub-headings, filter borders'],
    ['Clinical Success', '#1E8B4C', 'Forest Emerald Green', 'High recovery percentages (>90%), negative/curbed outbreak deltas, valid status tags'],
    ['Warning Attention', '#E67E22', 'Amber Ochre', 'Moderate CFR rates (2.0% - 4.0%), cautionary data quality indicators'],
    ['Critical Danger', '#C0392B', 'Crimson Red', 'High CFR (>4.0%), active outbreak anomaly alerts, mortality metrics'],
    ['Background Canvas', '#F0F8FF', 'Alice Blue Soft Grey', 'Global page background canvas behind visual containers'],
    ['Card Surface', '#FFFFFF', 'Pure Crisp White', 'KPI card backgrounds, Plotly chart container canvas, data tables'],
    ['High-Contrast Text', '#2C3E50', 'Charcoal Slate', 'Primary typography body text, numerical figures, chart legends'],
]
t_pal = doc.add_table(rows=len(palette_data) + 1, cols=4)
format_table(t_pal, [Cm(2.5), Cm(2.0), Cm(3.2), Cm(8.3)], palette_headers, palette_data)
doc.add_paragraph()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 4. BEST CHART FOR EACH OQ (AND WHY)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
add_heading_1('4. Visualization Selection Matrix per Operational Question')
p_oq_intro = doc.add_paragraph('Theoretical justification for chart selection aligned with data visualization best practices:')
p_oq_intro.runs[0].font.size = Pt(10)

oq_chart_headers = ['OQ ID', 'Operational Question', 'Primary Chart Type', 'Plotly Implementation', 'Visualization Rationale']
oq_chart_data = [
    ['OQ-01', '5-Year Case Increase', 'Multi-Series Line Chart', 'px.line(markers=True)', 'Continuous time series lines represent direction and magnitude of multi-year trajectories clearly.'],
    ['OQ-02', 'Regional State Rankings', 'Horizontal Bar Chart', 'px.bar(orientation=\'h\')', 'Horizontal orientation allows clear reading of 10 long state labels without diagonal slant text.'],
    ['OQ-03', 'Monthly Cyclical Trend', 'Transmission Curve Line', 'px.line(x=\'month\')', 'Connecting 12 monthly data points establishes immediate visual wave recognition.'],
    ['OQ-04', 'Demographic Cohorts', 'Stacked Demographic Bar', 'px.bar(barmode=\'stack\')', 'Stacked bars illustrate total morbidity while simultaneously displaying age bracket proportions.'],
    ['OQ-05', 'Case Fatality Rate (CFR)', 'Bi-Dimensional Heatmap', 'px.imshow(color_continuous_scale)', 'Matrix heatmaps allow rapid cognitive scanning of 50 state-disease cells to identify dark hot spots.'],
    ['OQ-06', 'Density Correlation', 'Scatter Plot + Trendline', 'px.scatter(trendline=\'ols\')', 'Scatter plotting reveals clustering and bivariate linearity; OLS regression line shows trajectory.'],
    ['OQ-07', 'Clinical Recovery Rates', 'Grouped Comparison Bar', 'px.bar(barmode=\'group\')', 'Side-by-side grouped bars facilitate direct visual benchmarking between recovery and mortality.'],
    ['OQ-08', 'Concurrent Outbreaks', 'Bubble Scatter Alert Chart', 'px.scatter(size=\'cases\')', 'Surfaces multi-disease overlap spikes as prominent visual clusters along the time axis.'],
    ['OQ-09', 'Year-over-Year Delta', 'Diverging Colored Table', 'st.dataframe(style.background_gradient)', 'Tabular representation with green/red gradient highlights negative vs positive trajectories.'],
    ['OQ-10', 'Peak Transmission Months', 'Monthly Intensity Heatmap', 'px.imshow(labels=dict(x=\'Month\'))', '12 columns across 5 disease rows highlight the exact calendar month of maximum transmission.'],
]
t_oq = doc.add_table(rows=len(oq_chart_data) + 1, cols=5)
format_table(t_oq, [Cm(1.5), Cm(3.2), Cm(3.3), Cm(3.2), Cm(4.8)], oq_chart_headers, oq_chart_data)
doc.add_paragraph()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 5. REUSABLE TAILWIND COMPONENTS & src/ui.py SPECIFICATION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
add_heading_1('5. Reusable UI Components Library (src/ui.py)')
p_comp = doc.add_paragraph(
    'To guarantee design consistency across all six pages, common UI widgets are encapsulated inside src/ui.py. '
    'These methods programmatically construct Tailwind CSS HTML markup and render it via Streamlit\'s component engine:\n'
    '1. inject_tailwind(): Silent pre-initialization of Tailwind CDN scripts.\n'
    '2. render_header(title, subtitle): Generates responsive executive gradient banners.\n'
    '3. render_kpi_card(label, value, delta, icon, color): Builds responsive metric tiles with percentage indicators.\n'
    '4. render_insight_box(title, text, alert_type): Standardizes qualitative clinical takeaway callouts.'
)
p_comp.runs[0].font.size = Pt(9.5)

doc.add_paragraph()
p_foot = doc.add_paragraph()
p_foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
rn_f = p_foot.add_run('12_ArgJain_DiseaseTrendAnalysis_UIFramework.docx | v1.0 | ABES Engineering College | November 2026')
rn_f.font.size = Pt(8)
rn_f.font.color.rgb = RGBColor(0x88, 0x88, 0x88)

save_path = r'c:\Users\Hp\Downloads\hcl\docs\12_ArgJain_DiseaseTrendAnalysis_UIFramework.docx'
doc.save(save_path)
print(f'SAVED DOCX: {save_path}')

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ALSO UPDATE RTM with "UI Screen ID"
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
rtm_path = r'c:\Users\Hp\Downloads\hcl\docs\04_ArgJain_DiseaseTrendAnalysis_RTM.xlsx'
if os.path.exists(rtm_path):
    wb_rtm = load_workbook(rtm_path)
    ws_r = wb_rtm['RTM']
    
    ui_mapping = {
        'BR-01': 'UI-01, UI-02',
        'BR-02': 'UI-01, UI-03',
        'BR-03': 'UI-01, UI-03',
        'BR-04': 'UI-04',
        'BR-05': 'UI-05',
        'BR-06': 'UI-02',
        'BR-07': 'UI-03',
        'BR-08': 'UI-05',
        'BR-09': 'UI-01, UI-02',
        'BR-10': 'All Screens',
        'BR-11': 'Sidebar (All)',
        'BR-12': 'UI-06',
        'BR-13': 'UI-06',
        'BR-14': 'All Screens',
        'BR-15': 'All Screens',
    }
    
    for row in range(2, ws_r.max_row + 1):
        br_id = ws_r.cell(row=row, column=3).value
        if br_id in ui_mapping:
            cell = ws_r.cell(row=row, column=11)
            cell.value = ui_mapping[br_id]
            cell.font = Font(name='Calibri', size=10)
            cell.fill = PatternFill(start_color='FFFFFF', end_color='FFFFFF', fill_type='solid')
            cell.alignment = Alignment(horizontal='center', vertical='center')
            
    # Update Change Log
    ws_log = wb_rtm['Change_Log']
    for r in range(2, ws_log.max_row + 1):
        if ws_log.cell(row=r, column=1).value == 'v1.3':
            ws_log.cell(row=r, column=2, value='18-Nov-2026')
            ws_log.cell(row=r, column=5, value='Populated UI Screen IDs (UI-01..UI-06) across all requirements.')
            
    wb_rtm.save(rtm_path)
    print(f'UPDATED RTM: {rtm_path} (UI Screen ID populated)')
