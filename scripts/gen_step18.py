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
run_sub = p_sub.add_run('STEP 18 — ABES Presentation Slide Deck & Speaker Script')
run_sub.font.size = Pt(14)
run_sub.font.bold = True
run_sub.font.color.rgb = RGBColor(0x2E, 0x86, 0xAB)

doc.add_paragraph()

meta_data = [
    ('Project ID & Title', 'P-01 | Disease Trend Analysis'),
    ('Domain', 'Healthcare Data Analytics'),
    ('Presenter / Student', 'Arg Jain (Roll No. 2500320140031)'),
    ('Academic Program', 'MCA 2nd Year (Data Analytics Specialization)'),
    ('Institution', 'ABES Engineering College, Ghaziabad'),
    ('Faculty Project Mentor', 'Ms. Kalpana Dwivedi'),
    ('Deck Structure', '11 Formal Slides (Conforming to ABES PPT Template)'),
    ('Total Presentation Time', '5 Minutes (30 Seconds Allocation per Slide)'),
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
# 1. 5-MINUTE VIVA VOCE TIMELINE GUIDE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
add_heading_1('1. Five-Minute Presentation Pacing Roadmap')
p_pace = doc.add_paragraph(
    'The 11-slide presentation is engineered for strict adherence to a 5-minute academic evaluation window. '
    'Each slide is budgeted for approximately 25 to 30 seconds of spoken remarks:'
)
p_pace.runs[0].font.size = Pt(10)

pacing_headers = ['Slide #', 'Slide Title', 'Target Time Budget', 'Elapsed Time', 'Core Focus of Spoken Remarks']
pacing_data = [
    ['Slide 1', 'Title & Project Attribution', '0:20 min', '0:20', 'Greet evaluators, introduce project ID P-01, student credentials, and faculty mentor.'],
    ['Slide 2', 'Problem Statement & Top 2 HMWs', '0:30 min', '0:50', 'State public health surveillance latency problem and introduce HMW-01 and HMW-03.'],
    ['Slide 3', 'Key Stakeholders & Influence', '0:25 min', '1:15', 'Highlight Public Health Officer, Hospital Admin, and Policy Maker decision rights.'],
    ['Slide 4', 'Requirements Traceability (RTM)', '0:30 min', '1:45', 'Demonstrate seamless end-to-end trace from HMW to BR, User Story, Code, and Test.'],
    ['Slide 5', 'Data Architecture & Quality Pipeline', '0:30 min', '2:15', 'Present 3,000-row fact dataset, 5 clinical patterns, and 3 data cleaning interventions.'],
    ['Slide 6', 'Solution Architecture & Tech Flow', '0:30 min', '2:45', 'Walk through data flow: SQLite to cached loader, cleaning, analytics, and Tailwind UI.'],
    ['Slide 7', 'Interactive Dashboard Screens', '0:30 min', '3:15', 'Showcase UI-01 Overview KPI cards and UI-02 60-month longitudinal time-series lines.'],
    ['Slide 8', 'Key Analytical Findings & Proofs', '0:35 min', '3:50', 'Present COVID 2021 spike (+300%), Dengue monsoon peak (6x), and density correlation.'],
    ['Slide 9', 'Quality Assurance & Test Suite (17/17)', '0:25 min', '4:15', 'Announce 17/17 automated tests passing, 0 critical failures, sub-second latency.'],
    ['Slide 10', 'Recommendations & Future Scope', '0:25 min', '4:40', 'Recommend district ICMR ingestion, note free-tier limitations, propose ML forecasting.'],
    ['Slide 11', 'Live Cloud Demonstration & Links', '0:20 min', '5:00', 'Present live Streamlit Cloud URL, GitHub repository, and transition to jury Q&A.'],
]
t_pace = doc.add_table(rows=len(pacing_data) + 1, cols=5)
format_table(t_pace, [Cm(1.5), Cm(4.5), Cm(2.2), Cm(2.2), Cm(5.6)], pacing_headers, pacing_data)
doc.add_paragraph()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 2. SLIDE-BY-SLIDE CONTENT & VERBATIM SPEAKER NOTES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
add_heading_1('2. Slide-by-Slide Visual Layout & Verbatim Speaker Scripts')

slides = [
    (
        "SLIDE 1: Title & Project Attribution",
        [
            "PROJECT TITLE: Disease Trend Analysis (Project ID: P-01)",
            "DOMAIN: Healthcare Data Analytics / Public Health Surveillance",
            "CANDIDATE: Arg Jain | University Roll No. 2500320140031",
            "ACADEMIC PROGRAM: MCA 2nd Year (Data Analytics Specialization)",
            "INSTITUTION: ABES Engineering College, Ghaziabad (AKTU Code 032)",
            "FACULTY MENTOR: Ms. Kalpana Dwivedi | Date: November 2026",
        ],
        "Good morning, respected external examiner and faculty mentor Ms. Kalpana Dwivedi. "
        "My name is Arg Jain, Roll No. 2500320140031. Today, I am proud to present Project P-01: "
        "'Disease Trend Analysis', an interactive public health surveillance intelligence platform "
        "developed as part of my MCA 2nd Year Data Analytics curriculum at ABES Engineering College."
    ),
    (
        "SLIDE 2: Business Problem & Top 2 HMW Statements",
        [
            "THE PROBLEM: Public health authorities lack a unified, interactive visual platform to monitor disease trends across states, time, and demographics.",
            "THE IMPACT: Results in delayed outbreak detection, inefficient ICU bed allocation, and misdirected health budgets.",
            "HMW-01 [Priority]: How might we help health officers instantly spot which disease is spiking in a region vs. last year?",
            "HMW-03 [Priority]: How might we help policy makers compare Case Fatality Rates (CFR) across states in a single glance to justify targeted emergency budgets?",
        ],
        "In our problem analysis, we discovered that Indian epidemiological surveillance data is severely fragmented across static monthly bulletins, "
        "causing multi-week delays in emergency intervention. Applying design thinking, we framed top opportunities: HMW-01 addresses instant outbreak detection "
        "compared to previous baselines, while HMW-03 provides policy makers a single-glance Case Fatality Rate matrix to justify targeted healthcare budgets."
    ),
    (
        "SLIDE 3: Key Stakeholders & Governance",
        [
            "SH-01: Public Health Officer (High Influence) — Deploys rapid field containment teams and issues regional health advisories.",
            "SH-02: Hospital Administrator (High Influence) — Anticipates seasonal surges to pre-allocate hospital beds, ICU units, and oxygen supplies.",
            "SH-03: Policy Maker / Ministry (High Influence) — Evaluates mortality severity to authorize emergency containment budgets.",
            "SH-04: Epidemiologist / Researcher (Medium Influence) — Investigates demographic vulnerability profiles and urban crowding correlations.",
            "GOVERNANCE: System satisfies the decision needs of all 4 operational personas through role-specific filtering.",
        ],
        "The system serves three high-influence stakeholders: Public Health Officers who deploy containment teams, Hospital Administrators "
        "who manage critical-care bed surge capacity, and Policy Makers who approve emergency health financing. Each persona interacts with customized "
        "analytical views through our unified interactive dashboard."
    ),
    (
        "SLIDE 4: End-to-End Requirements Traceability (RTM)",
        [
            "RTM-01: OQ-01 -> HMW-01 -> BR-01 -> US-04 -> disease_cases.cases_reported -> UI-01 -> TC-F-01, TC-T-02",
            "RTM-02: OQ-02 -> HMW-02 -> BR-02 -> US-06 -> region_master.region_name -> UI-01 -> TC-F-03, TC-T-03",
            "RTM-03: OQ-05 -> HMW-03 -> BR-03 -> US-07 -> disease_cases.deaths -> UI-03 -> TC-F-09, TC-T-09",
            "RTM-04: OQ-08 -> HMW-05 -> BR-05 -> US-15 -> disease_cases.is_outbreak -> UI-05 -> TC-F-13, TC-T-13",
            "AUDIT STATUS: 100% of 10 OQs, 10 HMWs, and 15 BRs trace end-to-end to verified code and passing tests.",
        ],
        "To ensure professional engineering rigor, we maintained a 100% complete Requirements Traceability Matrix. "
        "As visible on this slide, every stakeholder need directly maps to a Business Requirement, an Agile User Story, "
        "a physical SQLite database column, a dedicated UI screen, and both functional and technical automated test cases."
    ),
    (
        "SLIDE 5: Data Architecture & Quality Interventions",
        [
            "DATASET VOLUME: 3,003 records in disease_cases fact table (5 diseases, 10 states, 60 months: 2020–2024).",
            "RELATIONAL SCHEMA: 5 base tables in SQLite (`data/app.db`) + 1 joined view (`v_disease_analysis`, 35 columns).",
            "EMBEDDED CLINICAL PATTERNS: Monsoon Dengue surge, COVID-19 2021 spike, urban density incidence correlation.",
            "PIPELINE CLEANING 1: 3 exact duplicate reporting rows purged via `df.drop_duplicates()`.",
            "PIPELINE CLEANING 2: 54 missing case values imputed using group median per disease entity.",
            "PIPELINE CLEANING 3: 5 typographic extreme spikes (> 3.0*IQR) bounded via Winsorization capping.",
        ],
        "Our data layer models 60 months of epidemiological history across 10 Indian states. We embedded authentic clinical patterns, "
        "including post-monsoon vector-borne surges and the 2021 pandemic wave. Our cleaning pipeline automatically purges 3 duplicate rows, "
        "imputes 54 null values using disease medians, and bounds 5 extreme outliers to certify data integrity."
    ),
    (
        "SLIDE 6: Solution Architecture & Technical Flow",
        [
            "DATA TIER: SQLite 3 relational repository (`data/app.db`) enforcing PK/FK and non-negative CHECK constraints.",
            "INGESTION & CACHE: `src/data_loader.py` with `@st.cache_data(ttl=3600)` enabling sub-second query execution.",
            "ANALYTICAL ENGINE: Pure Python modules in `src/analysis.py` computing CFR%, recovery%, YoY%, and Pearson r.",
            "UI & STYLING: Streamlit 1.35 multi-page architecture + Tailwind CSS components injected via iframe.",
            "DEPLOYMENT: Streamlit Community Cloud with public HTTPS URL (zero cloud hosting licensing cost).",
        ],
        "Our technical architecture follows a modular decoupled pipeline: SQLite stores normalized records; `@st.cache_data` memoizes "
        "database projections in memory; pure Python functions compute mathematical ratios; and Tailwind CSS is injected into Streamlit "
        "to deliver a modern corporate visual experience with zero cloud hosting expense."
    ),
    (
        "SLIDE 7: Interactive Dashboard Screens",
        [
            "UI-01 (Executive Overview): 4 Tailwind KPI cards (Cases, Deaths, Recoveries, CFR), regional burden bar ranking.",
            "UI-02 (Longitudinal Trends): 60-month time-series line, multi-year overlapping YoY curves, 12-month seasonal heatmap.",
            "UI-03 (Regional Analysis): Cross-state CFR benchmarking and clinical recovery efficacy comparison bars.",
            "UI-04 (Demographics): 5-bracket stacked age group bar chart and gender distribution donut chart.",
            "UI-05 (Advanced EDA): Urban density scatter plot with OLS trendline, automated concurrent outbreak surge alerts.",
            "UI-06 (Data Quality): Pipeline cleaning accounting scorecard ledger and one-click filtered CSV dataset export.",
        ],
        "The application provides six dedicated analytical screens: UI-01 displays executive KPI cards and state rankings; "
        "UI-02 maps 60-month trends and seasonal heatmaps; UI-03 and 04 explore regional CFR and demographic vulnerability; "
        "while UI-05 surfaces statistical crowding correlations and concurrent outbreak alerts."
    ),
    (
        "SLIDE 8: Key Analytical Findings & Proofs",
        [
            "FINDING 1 (Pandemic Wave): COVID-19 surged by +279% in 2021 vs. 2020, followed by steady decline (OQ-01, OQ-09).",
            "FINDING 2 (Seasonal Cyclicity): Dengue cases surge by 6.04x during August monsoon months (1,401 avg) vs. January (231 avg) (OQ-03, OQ-10).",
            "FINDING 3 (Urban Crowding Correlation): Strong positive correlation (Pearson r = 0.84, p < 0.001) between state population density and disease incidence (OQ-06).",
            "FINDING 4 (Geriatric Risk): Senior cohort (60+) displays 5.5% Case Fatality Rate vs. 1.5% general population average (OQ-04).",
        ],
        "Our analysis revealed four statistically verifiable findings: COVID-19 experienced a 279% surge in 2021; Dengue incidence surges "
        "by over 6x during August monsoon weeks; state population density strongly correlates with infection velocity with a Pearson r of 0.84; "
        "and senior demographics face a 3.6x higher fatality rate."
    ),
    (
        "SLIDE 9: Quality Assurance & Verification Suite",
        [
            "AUTOMATED TESTS: 17/17 automated tests executed and passing with 100% success rate (zero critical failures).",
            "DATABASE TESTS (8 Tests): Table existence, 3,003 row volume, zero orphan FKs, and non-negative bounds verified.",
            "ANALYSIS TESTS (6 Tests): Known-vector validation of CFR (5.0%), Recovery (92.0%), YoY (+100%), and Pearson r (1.0).",
            "UI & CONFIG TESTS (3 Tests): Application routes, modular source packages, and pinned manifests verified.",
            "LATENCY VERIFICATION: Cold database analytical query completes in 0.042 seconds (Threshold: < 1.50s).",
        ],
        "Our automated QA suite executed 17 rigorous technical tests, achieving a 100% pass rate. We verified relational integrity, "
        "zero orphaned records, mathematical accuracy on known calculation vectors, and verified that cold database queries execute "
        "in just 0.042 seconds—well below our 1.5-second SLA threshold."
    ),
    (
        "SLIDE 10: Recommendations & Future Roadmap",
        [
            "STRATEGIC RECOMMENDATION: Transition synthetic pipelines to live district-level ICMR API feeds for active containment.",
            "SYSTEM LIMITATION 1: Synthetic data, while statistically calibrated, cannot model real-time behavioral shifts.",
            "SYSTEM LIMITATION 2: Free-tier cloud instances hibernate after 7 days of inactivity (re-wakes automatically upon visit).",
            "PHASE 2 ROADMAP 1: Deploy predictive Machine Learning forecasting (ARIMA / Prophet) for 60-day outbreak projection.",
            "PHASE 2 ROADMAP 2: Integrate automated WhatsApp and SMS outbound emergency dispatch alerts for field triage teams.",
        ],
        "We recommend transitioning this platform to live ICMR district data feeds for operational surveillance. In Phase 2, "
        "we plan to integrate ARIMA and Prophet machine learning models for 60-day predictive outbreak forecasting, and enable "
        "automated SMS dispatch notifications to hospital administrators."
    ),
    (
        "SLIDE 11: Live Demonstration & Artifact Links",
        [
            "LIVE APPLICATION URL: https://2500320140031-dta.streamlit.app",
            "GITHUB CODE REPOSITORY: https://github.com/Argjain/2500320140031-disease-trend-analysis.",
            "FULL PROJECT DOCUMENTATION: Complete 18-step deliverables available in `docs/` folder.",
            "DEMONSTRATION SCOPE: Resolving all 10 Operational Questions live in under 5 minutes.",
            "THANK YOU: Respected faculty and jury members. I am now open for viva voce questions.",
        ],
        "In conclusion, the platform is live and fully accessible at the URL shown on screen, backed by our public GitHub repository. "
        "All 10 Operational Questions can be demonstrated live in the running application. Thank you, respected evaluators, "
        "and I look forward to your questions."
    )
]

for title, bullets, notes in slides:
    add_heading_2(title)
    
    # Slide on-screen bullets
    p_b_box = doc.add_paragraph()
    r_hdr = p_b_box.add_run("ON-SCREEN SLIDE CONTENT (Max 6 Lines):")
    r_hdr.font.bold = True
    r_hdr.font.size = Pt(9.5)
    r_hdr.font.color.rgb = PRIMARY_COLOR
    
    for b in bullets:
        p = doc.add_paragraph(style='List Bullet')
        r = p.add_run(b)
        r.font.size = Pt(9.0)
        
    # Verbatim speaker notes
    p_spk = doc.add_paragraph()
    r_spk_hdr = p_spk.add_run("VERBATIM SPEAKER SCRIPT (~30 Seconds):")
    r_spk_hdr.font.bold = True
    r_spk_hdr.font.size = Pt(9.5)
    r_spk_hdr.font.color.rgb = RGBColor(0x92, 0x2B, 0x21)
    
    p_n = doc.add_paragraph()
    p_n.paragraph_format.left_indent = Cm(0.5)
    r_n = p_n.add_run(f'"{notes}"')
    r_n.font.italic = True
    r_n.font.size = Pt(9.5)
    
    doc.add_paragraph()

doc.add_paragraph()
p_foot = doc.add_paragraph()
p_foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
rn_f = p_foot.add_run('18_ArgJain_DiseaseTrendAnalysis_Presentation.docx | ABES Presentation Deck | November 2026')
rn_f.font.size = Pt(8)
rn_f.font.color.rgb = RGBColor(0x88, 0x88, 0x88)

save_path = r'c:\Users\Hp\Downloads\hcl\docs\18_ArgJain_DiseaseTrendAnalysis_Presentation.docx'
doc.save(save_path)
print(f'SAVED DOCX: {save_path}')
