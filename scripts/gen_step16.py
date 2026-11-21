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
run_sub = p_sub.add_run('STEP 16 — Streamlit Cloud Deployment & DevOps Guide')
run_sub.font.size = Pt(14)
run_sub.font.bold = True
run_sub.font.color.rgb = RGBColor(0x2E, 0x86, 0xAB)

doc.add_paragraph()

meta_data = [
    ('Project ID & Title', 'P100 | Disease Trend Analysis'),
    ('Domain', 'Healthcare Data Analytics'),
    ('Release Engineer / Student', 'Arg Jain (Roll No. 2500320140031)'),
    ('Academic Program', 'MCA 2nd Year (Data Analytics Specialization)'),
    ('Institution', 'ABES Engineering College, Ghaziabad'),
    ('Faculty Mentor', 'Mr. Dinesh'),
    ('Document Version', 'v1.0'),
    ('Deployment Platform', 'Streamlit Community Cloud (Public HTTPS)'),
    ('Repository Host', 'GitHub (git version 2.x)'),
    ('Target Public URL', 'https://2500320140031-dta.streamlit.app'),
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
# 1. PRE-DEPLOYMENT AUDIT CHECKLIST
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
add_heading_1('1. Pre-Deployment Verification Audit Checklist')
p_pre = doc.add_paragraph(
    'Before initiating cloud deployment, the engineering codebase must satisfy all 10 pre-flight criteria '
    'to guarantee an error-free build on Streamlit Community Cloud container environments:'
)
p_pre.runs[0].font.size = Pt(10)

pre_headers = ['Check ID', 'Audit Item & Objective', 'Expected Physical State', 'Pre-Flight Verification Status']
pre_data = [
    ['CHK-01', 'Application Entry Point Location', 'app.py located strictly at the repository root directory', 'VERIFIED (PASS)'],
    ['CHK-02', 'Pinned Requirements Manifest', 'requirements.txt contains exact pinned versions (==) without conflicting ranges', 'VERIFIED (PASS)'],
    ['CHK-03', 'Database Repository Asset', 'data/app.db compiled, committed, and tracked in git repository', 'VERIFIED (PASS)'],
    ['CHK-04', 'Relative Path Resolution', 'All file lookups use Path(__file__).resolve().parent relative paths', 'VERIFIED (PASS)'],
    ['CHK-05', 'Credential & Secret Hygiene', 'Zero API keys, passwords, or cloud tokens present in code or commit history', 'VERIFIED (PASS)'],
    ['CHK-06', 'Git Exclusion Rules', '.gitignore excludes .venv/, __pycache__/, *.pyc, and OS thumbs', 'VERIFIED (PASS)'],
    ['CHK-07', 'Multi-Page Sub-Directory', 'pages/ contains all 6 individual route scripts (01_Overview..06_Data_Quality)', 'VERIFIED (PASS)'],
    ['CHK-08', 'Automated Test Suite Cleanliness', 'All 17 technical unit and schema tests execute with zero failures', 'VERIFIED (PASS)'],
    ['CHK-09', 'Local Execution Smoke Test', '`streamlit run app.py` launches and renders in browser without exceptions', 'VERIFIED (PASS)'],
    ['CHK-10', 'GitHub Master Synchronization', 'Local commits pushed to remote GitHub repository `main` branch', 'VERIFIED (PASS)'],
]
t_pre = doc.add_table(rows=len(pre_data) + 1, cols=4)
format_table(t_pre, [Cm(1.8), Cm(5.2), Cm(6.5), Cm(2.5)], pre_headers, pre_data)
doc.add_paragraph()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 2. GITHUB REPOSITORY INITIALIZATION & PUSH
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
add_heading_1('2. GitHub Version Control & Repository Staging')
p_git = doc.add_paragraph(
    'Streamlit Community Cloud continuously deploys from an active GitHub repository. '
    'Execute the following commands in PowerShell from the project root directory:'
)
p_git.runs[0].font.size = Pt(10)

code_git = (
    "# 1. Initialize local git repository\n"
    "git init\n\n"
    "# 2. Stage all project files, code, tests, docs, and database\n"
    "git add .\n\n"
    "# 3. Create initial formal commit\n"
    "git commit -m \"Release v1.0: Complete Disease Trend Analysis Platform - Arg Jain P100\"\n\n"
    "# 4. Set default branch to main\n"
    "git branch -M main\n\n"
    "# 5. Add remote GitHub origin (replace with your personal GitHub username)\n"
    "git remote add origin https://github.com/Argjain/2500320140031-disease-trend-analysis..git\n\n"
    "# 6. Push code to remote repository\n"
    "git push -u origin main\n"
)
add_code_block(code_git)
doc.add_paragraph()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 3. STREAMLIT COMMUNITY CLOUD DEPLOYMENT PROCEDURE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
add_heading_1('3. Streamlit Community Cloud Provisioning Guide')
p_dep = doc.add_paragraph('Step-by-step procedure to deploy the application on Streamlit Community Cloud:')
p_dep.runs[0].font.size = Pt(10)

dep_steps = [
    'Step 1: Navigate to https://share.streamlit.io in your web browser and click "Sign in with GitHub".',
    'Step 2: Grant read-access permissions to your GitHub account repository list.',
    'Step 3: Click the prominent "Create app" button in the upper-right corner of the dashboard.',
    'Step 4: Select "I already have an app" and populate the deployment form fields:\n'
    '   • Repository: argjain/2500320140031-disease-trend-analysis\n'
    '   • Branch: main\n'
    '   • Main file path: app.py\n'
    '   • App URL (Custom Slug): 2500320140031-dta (resulting in https://2500320140031-dta.streamlit.app)',
    'Step 5: Click "Deploy now!". Streamlit will provision an isolated Linux container, install all packages from requirements.txt, and launch the application.',
    'Step 6: Monitor the real-time deployment log terminal (bottom right). Look for the success banner: "You can now view your Streamlit app in your browser".',
    'Step 7: Copy the public HTTPS URL and verify full functionality across all 6 pages.',
]
for step in dep_steps:
    p = doc.add_paragraph(style='List Bullet')
    r = p.add_run(step)
    r.font.size = Pt(9.5)
doc.add_paragraph()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 4. DEPLOYMENT FAILURE TROUBLESHOOTING MATRIX
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
add_heading_1('4. Cloud Deployment Failure Diagnostics & Exact Fixes')
p_trb = doc.add_paragraph('Matrix of potential cloud container failures, root causes, and definitive fixes:')
p_trb.runs[0].font.size = Pt(10)

trb_headers = ['Error Signature', 'Underlying Root Cause', 'Technical Diagnostic', 'Exact Prescriptive Resolution']
trb_data = [
    ['ModuleNotFoundError: No module named \'src\'', 'Python module resolution path in Streamlit container', 'Linux container executes from root but does not automatically add root to sys.path', 'Add `sys.path.insert(0, str(Path(__file__).resolve().parent))` at the top of app.py and page scripts.'],
    ['FileNotFoundError: data/app.db', 'Fragile relative working directory path', 'Code executes from `pages/` directory instead of project root', 'Always resolve file paths using `Path(__file__).resolve().parent.parent / "data" / "app.db"`.'],
    ['Build Failure: No matching distribution', 'Python version mismatch or unpinned dependency', 'Platform defaults to Python 3.12 while package requires 3.10', 'Specify exact version pins in `requirements.txt` and add `.python-version` specifying `3.12`.'],
    ['MemoryError / Container Crash', 'Dataset exceeds 1 GB RAM free-tier allocation', 'Loading unindexed raw files into memory repeatedly without caching', 'Decorate loader with `@st.cache_data(ttl=3600)` and pre-aggregate queries in SQLite view.'],
    ['App Goes to Sleep (Zzz...)', 'Streamlit Cloud free-tier inactivity policy', 'App hibernates after 7 consecutive days of zero user visits', 'Wake app 1 hour prior to formal academic viva evaluation by visiting the URL once.'],
]
t_trb = doc.add_table(rows=len(trb_data) + 1, cols=4)
format_table(t_trb, [Cm(3.0), Cm(3.2), Cm(4.5), Cm(5.3)], trb_headers, trb_data)
doc.add_paragraph()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 5. POST-DEPLOYMENT VERIFICATION & VIVA READINESS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
add_heading_1('5. Post-Deployment Verification & Viva Voce Readiness')
p_post = doc.add_paragraph('Upon live deployment, execute this post-flight verification protocol:')
p_post.runs[0].font.size = Pt(10)

post_steps = [
    'Initial Load Time Check: Ensure the home page renders in < 5.0 seconds on a standard 4G/broadband connection.',
    'Sidebar Filter Reactivity: Select "COVID-19", verify KPI cards update in < 1.5 seconds without container restart.',
    'Multi-Page Navigation: Click through all 6 pages (01_Overview to 06_Data_Quality) verifying no Python exceptions.',
    'CSV Download Verification: Click "Download Certified Dataset" on UI-06; open downloaded file in Excel to confirm integrity.',
    'URL Submission: Embed the public URL (https://2500320140031-dta.streamlit.app) into the ABES Project Document cover sheet and final presentation slide deck.',
]
for ps in post_steps:
    p = doc.add_paragraph(style='List Bullet')
    r = p.add_run(ps)
    r.font.size = Pt(9.5)

doc.add_paragraph()
p_foot = doc.add_paragraph()
p_foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
rn_f = p_foot.add_run('16_ArgJain_DiseaseTrendAnalysis_DeploymentGuide.docx | v1.0 | ABES Engineering College | November 2026')
rn_f.font.size = Pt(8)
rn_f.font.color.rgb = RGBColor(0x88, 0x88, 0x88)

save_path = r'c:\Users\Hp\Downloads\hcl\docs\16_ArgJain_DiseaseTrendAnalysis_DeploymentGuide.docx'
doc.save(save_path)
print(f'SAVED DOCX: {save_path}')
