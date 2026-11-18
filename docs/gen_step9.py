import os
from PIL import Image, ImageDraw, ImageFont
import docx
from docx import Document
from docx.shared import Pt, RGBColor, Cm, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

os.makedirs(r'c:\Users\Hp\Downloads\hcl\docs', exist_ok=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 1. DRAW HIGH-RESOLUTION ER DIAGRAM IMAGE VIA PILLOW
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
img_w, img_h = 1600, 1100
img = Image.new('RGB', (img_w, img_h), color='#F8FAFC')
draw = ImageDraw.Draw(img)

# Colors
C_BORDER = '#1A5376'
C_HEADER_FILL = '#1A5376'
C_FACT_HEADER = '#922B21'
C_BOX_BG = '#FFFFFF'
C_LINE = '#2C3E50'
C_TEXT = '#1E293B'
C_PK = '#B91C1C'
C_FK = '#1D4ED8'

# Draw Title Banner
draw.rectangle([40, 20, img_w - 40, 80], fill='#1A5376')
draw.text((img_w // 2, 50), "DISEASE TREND ANALYSIS — ENTITY RELATIONSHIP DIAGRAM (3NF SCHEMA)", fill='#FFFFFF', anchor='mm')

def draw_table_box(x, y, w, h, title, fields, is_fact=False):
    hdr_color = C_FACT_HEADER if is_fact else C_HEADER_FILL
    # Box shadow
    draw.rectangle([x+4, y+4, x+w+4, y+h+4], fill='#E2E8F0')
    # Box body
    draw.rectangle([x, y, x+w, y+h], fill=C_BOX_BG, outline=hdr_color, width=2)
    # Header
    draw.rectangle([x, y, x+w, y+35], fill=hdr_color)
    draw.text((x + w//2, y + 18), title, fill='#FFFFFF', anchor='mm')
    
    # Fields
    curr_y = y + 45
    for field_type, field_name, key_tag in fields:
        prefix = f"[{key_tag}] " if key_tag else "      "
        text_line = f"{prefix}{field_name} : {field_type}"
        fill_color = C_PK if key_tag == 'PK' else (C_FK if key_tag == 'FK' else C_TEXT)
        draw.text((x + 12, curr_y), text_line, fill=fill_color)
        curr_y += 20

# 1. disease_master (Master)
dm_fields = [
    ("int", "disease_id", "PK"),
    ("string", "disease_name", ""),
    ("string", "disease_category", ""),
    ("string", "description", ""),
    ("int", "is_contagious", ""),
    ("int", "typical_incubation_days", ""),
]
draw_table_box(60, 130, 320, 200, "disease_master (Dimension)", dm_fields)

# 2. region_master (Master)
rm_fields = [
    ("int", "region_id", "PK"),
    ("string", "region_name", ""),
    ("string", "state_code", ""),
    ("string", "zone", ""),
    ("int", "population", ""),
    ("real", "area_sqkm", ""),
    ("real", "population_density", ""),
]
draw_table_box(60, 410, 320, 220, "region_master (Dimension)", rm_fields)

# 3. demographic_group (Master)
dg_fields = [
    ("int", "demo_id", "PK"),
    ("string", "age_group", ""),
    ("string", "gender", ""),
    ("int", "age_min", ""),
    ("int", "age_max", ""),
]
draw_table_box(60, 720, 320, 180, "demographic_group (Dimension)", dg_fields)

# 4. disease_cases (Main Fact Table)
dc_fields = [
    ("int", "case_id", "PK"),
    ("int", "disease_id", "FK"),
    ("int", "region_id", "FK"),
    ("date", "report_date", ""),
    ("int", "report_year", ""),
    ("int", "report_month", ""),
    ("int", "cases_reported", ""),
    ("int", "deaths", ""),
    ("int", "recovered", ""),
    ("int", "active_cases", ""),
    ("int", "hospitalized", ""),
    ("int", "is_outbreak", ""),
    ("string", "data_source", ""),
    ("timestamp", "created_at", ""),
]
draw_table_box(490, 200, 380, 360, "disease_cases (Primary Fact)", dc_fields, is_fact=True)

# 5. demographic_breakdown (Sub-fact / Bridge)
db_fields = [
    ("int", "breakdown_id", "PK"),
    ("int", "case_id", "FK"),
    ("int", "demo_id", "FK"),
    ("int", "cases_in_group", ""),
    ("int", "deaths_in_group", ""),
    ("int", "recovered_in_group", ""),
]
draw_table_box(990, 380, 340, 200, "demographic_breakdown (Sub-Fact)", db_fields, is_fact=True)

# 6. v_disease_analysis (Analytical View)
va_fields = [
    ("view", "35+ Joined Analysis Columns", "VIEW"),
    ("kpi", "cfr_pct = deaths / cases * 100", ""),
    ("kpi", "recovery_rate_pct = rec / cases * 100", ""),
    ("kpi", "incidence_per_lakh = cases/pop * 100k", ""),
    ("grain", "One row per Disease x Region x Month", ""),
]
draw_table_box(990, 700, 380, 180, "v_disease_analysis (Analytical View)", va_fields)

# Connector Lines & Crow's Foot
# Line: disease_master -> disease_cases
draw.line([(380, 230), (490, 280)], fill=C_LINE, width=3)
draw.text((435, 235), "1 : N (has)", fill=C_LINE)

# Line: region_master -> disease_cases
draw.line([(380, 520), (490, 380)], fill=C_LINE, width=3)
draw.text((430, 460), "1 : N (reports in)", fill=C_LINE)

# Line: disease_cases -> demographic_breakdown
draw.line([(870, 380), (990, 480)], fill=C_LINE, width=3)
draw.text((910, 410), "1 : N (breaks down)", fill=C_LINE)

# Line: demographic_group -> demographic_breakdown
draw.line([(380, 810), (950, 810), (950, 530), (990, 530)], fill=C_LINE, width=3)
draw.text((700, 790), "1 : N (classifies)", fill=C_LINE)

# Footer note on image
draw.text((img_w // 2, img_h - 30), "Generated for ABES MCA Data Analytics Project P-01 | Arg Jain (2500320140031)", fill='#64748B', anchor='mm')

png_path = r'c:\Users\Hp\Downloads\hcl\docs\09_ER_Diagram.png'
img.save(png_path, dpi=(150, 150))
print(f'SAVED PNG: {png_path}')

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 2. BUILD WORD DOCUMENT (docs/09_ArgJain_DiseaseTrendAnalysis_ERDiagram.docx)
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
    run.font.size = Pt(8.5)
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
run_sub = p_sub.add_run('STEP 9 — Entity-Relationship (ER) Diagram Specification')
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
    ('Document Version', 'v1.0'),
    ('Schema Model', 'Extended Star / Snowstorm Relational Model (3NF)'),
    ('Diagram Assets', 'Mermaid DDL + Embedded High-Resolution PNG Graphic'),
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
# 1. MERMAID ER DIAGRAM CODE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
add_heading_1('1. Mermaid Entity-Relationship (ER) Definition')
p_m_intro = doc.add_paragraph(
    'The formal entity-relationship schema is defined below using declarative Mermaid erDiagram syntax. '
    'This specification explicitly documents all five base relational entities, their attribute data types, '
    'primary keys (PK), foreign keys (FK), and cardinality constraints:'
)
p_m_intro.runs[0].font.size = Pt(10)

mermaid_code = (
    "erDiagram\n"
    "    disease_master {\n"
    "        int disease_id PK\n"
    "        string disease_name\n"
    "        string disease_category\n"
    "        string description\n"
    "        int is_contagious\n"
    "        int typical_incubation_days\n"
    "    }\n"
    "    region_master {\n"
    "        int region_id PK\n"
    "        string region_name\n"
    "        string state_code\n"
    "        string zone\n"
    "        int population\n"
    "        real area_sqkm\n"
    "        real population_density\n"
    "    }\n"
    "    demographic_group {\n"
    "        int demo_id PK\n"
    "        string age_group\n"
    "        string gender\n"
    "        int age_min\n"
    "        int age_max\n"
    "    }\n"
    "    disease_cases {\n"
    "        int case_id PK\n"
    "        int disease_id FK\n"
    "        int region_id FK\n"
    "        date report_date\n"
    "        int report_year\n"
    "        int report_month\n"
    "        int cases_reported\n"
    "        int deaths\n"
    "        int recovered\n"
    "        int active_cases\n"
    "        int hospitalized\n"
    "        int is_outbreak\n"
    "        string data_source\n"
    "        timestamp created_at\n"
    "    }\n"
    "    demographic_breakdown {\n"
    "        int breakdown_id PK\n"
    "        int case_id FK\n"
    "        int demo_id FK\n"
    "        int cases_in_group\n"
    "        int deaths_in_group\n"
    "        int recovered_in_group\n"
    "    }\n"
    "\n"
    "    disease_master ||--o{ disease_cases : \"has\"\n"
    "    region_master ||--o{ disease_cases : \"reports\"\n"
    "    disease_cases ||--o{ demographic_breakdown : \"broken down by\"\n"
    "    demographic_group ||--o{ demographic_breakdown : \"classifies\"\n"
)
add_code_block(mermaid_code)
doc.add_paragraph()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 2. EMBEDDED HIGH-RESOLUTION ER DIAGRAM GRAPHIC
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
add_heading_1('2. Visual Architecture: Entity-Relationship Diagram')
p_img_intro = doc.add_paragraph(
    'The schematic diagram below illustrates the structural topology of the database, detailing primary key '
    'associations, foreign key references, and one-to-many cardinality flows across master dimensions and transaction facts:'
)
p_img_intro.runs[0].font.size = Pt(10)

if os.path.exists(png_path):
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_img = p_img.add_run()
    run_img.add_picture(png_path, width=Inches(6.2))
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rn_c = p_cap.add_run('Figure 9.1: Entity-Relationship Diagram for Disease Trend Analysis (app.db)')
    rn_c.font.size = Pt(8.5)
    rn_c.font.italic = True
    rn_c.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)

doc.add_paragraph()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 3. PLAIN-ENGLISH RELATIONSHIP DESCRIPTIONS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
add_heading_1('3. Plain-English Relationship Semantics')
p_rel_intro = doc.add_paragraph('Each relational join pathway enforces specific domain cardinality rules:')
p_rel_intro.runs[0].font.size = Pt(10)

rel_narratives = [
    ('Relationship 1: disease_master to disease_cases (1 : N)',
     'One disease entity in disease_master has zero or many periodic case reports in disease_cases. Conversely, each individual case record reports epidemiological incidence for exactly one disease entity. Orphan case records with unmapped disease identifiers are forbidden by foreign key constraints.'),
    ('Relationship 2: region_master to disease_cases (1 : N)',
     'One geographic state in region_master reports zero or many disease case records over time. Conversely, each individual case record belongs to exactly one sovereign state boundary. Case records without valid state associations cannot be inserted.'),
    ('Relationship 3: disease_cases to demographic_breakdown (1 : N)',
     'One aggregate case record in disease_cases is partitioned into zero or many demographic sub-group rows in demographic_breakdown. Conversely, each demographic breakdown slice belongs to exactly one aggregate state-month case transaction. Deleting a parent case record cascades to purge its demographic sub-slices.'),
    ('Relationship 4: demographic_group to demographic_breakdown (1 : N)',
     'One demographic cohort in demographic_group classifies zero or many clinical breakdown rows in demographic_breakdown. Conversely, each demographic sub-slice is categorized under exactly one standardized age-gender cohort.'),
    ('Relationship 5: v_disease_analysis Query View (Denormalized Join)',
     'The materialized analytical view v_disease_analysis executes an inner join across disease_cases, disease_master, and region_master, synthesizing a 35-column denormalized projection enriched with real-time computed KPIs (CFR %, recovery rate %, and incidence per 100,000 residents).'),
]

for title, desc in rel_narratives:
    add_heading_2(title)
    p = doc.add_paragraph(desc)
    p.runs[0].font.size = Pt(9.5)

doc.add_paragraph()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 4. BUSINESS RULES ENFORCED BY RELATIONAL DESIGN
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
add_heading_1('4. Business Rules Enforced by Relational Constraints')
p_br_intro = doc.add_paragraph('The database engine actively guarantees data integrity through physical DDL constraints:')
p_br_intro.runs[0].font.size = Pt(10)

br_enforced_data = [
    ['1', 'Referential Entity Integrity', 'disease_cases.disease_id REFERENCES disease_master(disease_id)', 'Guarantees every case record links to a recognized disease entity. Restricts deletion of active diseases.'],
    ['2', 'Geographic Jurisdiction Integrity', 'disease_cases.region_id REFERENCES region_master(region_id)', 'Guarantees all case reporting maps to an established state. Restricts orphaned regional data.'],
    ['3', 'Mortality Upper-Bound Constraint', 'CHECK (deaths >= 0 AND deaths <= cases_reported)', 'Physically forbids impossible clinical data where reported fatalities exceed total confirmed infections.'],
    ['4', 'Recovery Upper-Bound Constraint', 'CHECK (recovered >= 0 AND recovered <= cases_reported)', 'Physically forbids illogical clinical data where documented recoveries exceed total confirmed infections.'],
    ['5', 'Non-Negative Morbidity Rule', 'CHECK (cases_reported >= 0 AND active_cases >= 0)', 'Guarantees case counts cannot be negative under any reporting circumstance.'],
    ['6', 'Unique Disease Naming Constraint', 'disease_master.disease_name UNIQUE', 'Eliminates redundant taxonomic duplication (e.g., prevents having two distinct rows for Dengue).'],
    ['7', 'Demographic Cohort Uniqueness', 'UNIQUE (age_group, gender)', 'Ensures the 15-cell demographic segmentation matrix (5 age groups x 3 genders) is mathematically distinct.'],
]
t_br = doc.add_table(rows=len(br_enforced_data) + 1, cols=4)
format_table(t_br, [Cm(1.0), Cm(4.2), Cm(5.5), Cm(5.3)], ['#', 'Enforced Rule', 'Database Constraint Syntax', 'Operational Benefit'], br_enforced_data)
doc.add_paragraph()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 5. DESIGN PROBLEMS EVALUATED & REMEDIATIONS APPLIED
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
add_heading_1('5. Schema Review: Design Challenges & Remediation')
p_prob_intro = doc.add_paragraph(
    'During architectural peer review, five potential design pitfalls were evaluated. '
    'The table below itemizes the trade-offs considered and the architectural fixes adopted:'
)
p_prob_intro.runs[0].font.size = Pt(10)

review_data = [
    ['DP-01', 'Derived Column Redundancy in Fact', 'active_cases is mathematically derived as (cases - deaths - recovered). Storing derived data risks synchronization drift.', 'Medium', 'Adopted CHECK constraint: active_cases = cases - deaths - recovered. Retained column in SQLite to avoid recurring arithmetic overhead during high-frequency dashboard queries.'],
    ['DP-02', 'Geospatial Density Calculation Overhead', 'population_density is derived from population / area_sqkm in region_master.', 'Low', 'Pre-calculated and stored at master initialization. State land area and decennial census figures are static, making dynamic recalculation unnecessary.'],
    ['DP-03', 'M:N Cardinality Resolution', 'Directly linking disease_cases to demographic_group would create an unwieldy composite relation.', 'High', 'Resolved by introducing demographic_breakdown as a dedicated sub-fact / bridge table with independent surrogate key breakdown_id.'],
    ['DP-04', 'Redundant Temporal Dimension Columns', 'Storing report_year and report_month alongside report_date introduces slight storage redundancy.', 'Low', 'Deliberate architectural denormalization. Integer year/month columns enable ultra-fast indexed GROUP BY operations without date parsing latency.'],
    ['DP-05', 'Absence of Mutability Audit Trail', 'Base tables lack updated_at timestamp columns to log data corrections.', 'Low', 'Created created_at DEFAULT CURRENT_TIMESTAMP. Application dataset is designed as an append-only historical epidemiological ledger.'],
]
t_rev = doc.add_table(rows=len(review_data) + 1, cols=5)
format_table(t_rev, [Cm(1.5), Cm(3.5), Cm(4.5), Cm(1.8), Cm(4.7)], ['Item', 'Design Challenge Identified', 'Nature of Structural Issue', 'Severity', 'Adopted Engineering Remediation'], review_data)
doc.add_paragraph()

p_foot = doc.add_paragraph()
p_foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
rn_f = p_foot.add_run('09_ArgJain_DiseaseTrendAnalysis_ERDiagram.docx | v1.0 | ABES Engineering College | November 2026')
rn_f.font.size = Pt(8)
rn_f.font.color.rgb = RGBColor(0x88, 0x88, 0x88)

save_path = r'c:\Users\Hp\Downloads\hcl\docs\09_ArgJain_DiseaseTrendAnalysis_ERDiagram.docx'
doc.save(save_path)
print(f'SAVED DOCX: {save_path}')
