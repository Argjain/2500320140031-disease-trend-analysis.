import os
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# 1. Initialize Widescreen Presentation (16:9)
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

# Color Palette Definitions (Executive Healthcare Academic Theme)
NAVY = RGBColor(15, 43, 72)           # Primary Dark Navy #0F2B48
TEAL = RGBColor(26, 83, 118)          # Brand Teal #1A5376
SKY = RGBColor(2, 132, 199)           # Bright Sky Blue #0284C7
SLATE_DARK = RGBColor(30, 41, 59)     # Slate Charcoal #1E293B
SLATE_MUTED = RGBColor(100, 116, 139) # Muted Text #64748B
BG_LIGHT = RGBColor(248, 250, 252)    # Card Background #F8FAFC
BORDER_COLOR = RGBColor(226, 232, 240)# Card Border #E2E8F0
EMERALD = RGBColor(5, 150, 105)       # Success Green #059669
AMBER = RGBColor(217, 119, 6)         # Warning Amber #D97706
RED = RGBColor(185, 28, 28)           # Alert Red #B91C1C
WHITE = RGBColor(255, 255, 255)

BASE_DIR = Path(__file__).resolve().parent.parent
SCREENSHOTS_DIR = BASE_DIR / "docs" / "screenshots"

def resolve_path(p):
    path = Path(p)
    if path.is_absolute() and path.exists():
        return path
    if (BASE_DIR / p).exists():
        return BASE_DIR / p
    return path

def add_header(slide, title_text, subtitle_text):
    """Draws a clean executive header bar at the top of the slide."""
    header_box = slide.shapes.add_textbox(Inches(0.6), Inches(0.4), Inches(12.133), Inches(0.95))
    tf = header_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    p_title = tf.paragraphs[0]
    p_title.text = title_text
    p_title.font.name = "Segoe UI"
    p_title.font.size = Pt(21)
    p_title.font.bold = True
    p_title.font.color.rgb = NAVY
    
    if subtitle_text:
        p_sub = tf.add_paragraph()
        p_sub.text = subtitle_text
        p_sub.font.name = "Segoe UI"
        p_sub.font.size = Pt(11)
        p_sub.font.color.rgb = SKY
        p_sub.space_before = Pt(3)

def add_content_slide(slide, title, subtitle, image_path, bullets, insight_text, notes_text):
    """Creates a structured two-column presentation slide for official academic submission."""
    add_header(slide, title, subtitle)
    
    # Left Column: Screenshot Image Card
    img_left = Inches(0.6)
    img_top = Inches(1.45)
    img_width = Inches(6.4)
    img_height = Inches(5.45)
    
    resolved_img = resolve_path(image_path) if image_path else None
    if resolved_img and resolved_img.exists():
        frame = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, img_left - Inches(0.04), img_top - Inches(0.04), img_width + Inches(0.08), img_height + Inches(0.08))
        frame.fill.solid()
        frame.fill.fore_color.rgb = WHITE
        frame.line.color.rgb = BORDER_COLOR
        frame.line.width = Pt(1.5)
        
        slide.shapes.add_picture(str(resolved_img), img_left, img_top, width=img_width, height=img_height)
    
    # Right Column: Highlights & Decision Value
    right_left = Inches(7.3)
    right_top = Inches(1.45)
    right_width = Inches(5.4)
    
    # 1. Key Highlights Card
    h_box = slide.shapes.add_textbox(right_left, right_top, right_width, Inches(2.35))
    htf = h_box.text_frame
    htf.word_wrap = True
    htf.margin_left = htf.margin_top = htf.margin_right = htf.margin_bottom = 0
    
    hp = htf.paragraphs[0]
    hp.text = "📌 Key Technical & Analytical Highlights"
    hp.font.name = "Segoe UI"
    hp.font.size = Pt(13)
    hp.font.bold = True
    hp.font.color.rgb = NAVY
    
    for b in bullets:
        bp = htf.add_paragraph()
        bp.text = f"• {b}"
        bp.font.name = "Segoe UI"
        bp.font.size = Pt(10.5)
        bp.font.color.rgb = SLATE_DARK
        bp.space_before = Pt(4)
        
    # 2. Formal Epidemiological Decision Value Card
    card_top = Inches(4.0)
    card_height = Inches(2.9)
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, right_left, card_top, right_width, card_height)
    card.fill.solid()
    card.fill.fore_color.rgb = BG_LIGHT
    card.line.color.rgb = SKY
    card.line.width = Pt(1.5)
    
    ctf = card.text_frame
    ctf.word_wrap = True
    ctf.margin_left = ctf.margin_right = ctf.margin_top = ctf.margin_bottom = Inches(0.2)
    
    cp1 = ctf.paragraphs[0]
    cp1.text = "🎯 Surveillance Intelligence & Decision Impact:"
    cp1.font.name = "Segoe UI"
    cp1.font.size = Pt(12)
    cp1.font.bold = True
    cp1.font.color.rgb = TEAL
    
    cp2 = ctf.add_paragraph()
    cp2.text = insight_text
    cp2.font.name = "Segoe UI"
    cp2.font.size = Pt(10.2)
    cp2.font.color.rgb = SLATE_DARK
    cp2.space_before = Pt(5)
    
    # Add Speaker Notes
    notes_slide = slide.notes_slide
    notes_slide.notes_text_frame.text = notes_text

# ==========================================
# SLIDE 1: Title Slide (Grand Official Submission Cover)
# ==========================================
slide1 = prs.slides.add_slide(blank_layout)

bg = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(4.5))
bg.fill.solid()
bg.fill.fore_color.rgb = NAVY
bg.line.fill.background()

tb = slide1.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.7), Inches(3.2))
tf = tb.text_frame
tf.word_wrap = True

p1 = tf.paragraphs[0]
p1.text = "🏥 Disease Trend Analysis Intelligence Cockpit"
p1.font.name = "Segoe UI"
p1.font.size = Pt(31)
p1.font.bold = True
p1.font.color.rgb = WHITE

p2 = tf.add_paragraph()
p2.text = "An Interactive Healthcare Surveillance & Epidemiological Analytics Platform for India"
p2.font.name = "Segoe UI"
p2.font.size = Pt(16)
p2.font.color.rgb = RGBColor(186, 230, 253)
p2.space_before = Pt(10)

p3 = tf.add_paragraph()
p3.text = "Project ID: P100 | Healthcare Data Analytics Specialization | Academic Session: 2025–2026\nSubmitted in partial fulfillment of the requirements for Master of Computer Applications (MCA)"
p3.font.name = "Segoe UI"
p3.font.size = Pt(11.5)
p3.font.color.rgb = RGBColor(224, 242, 254)
p3.space_before = Pt(12)

# Candidate & Mentor Details Card
card1 = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.85), Inches(11.7), Inches(2.1))
card1.fill.solid()
card1.fill.fore_color.rgb = WHITE
card1.line.color.rgb = BORDER_COLOR
card1.line.width = Pt(1.5)

ctf1 = card1.text_frame
ctf1.word_wrap = True
ctf1.margin_left = Inches(0.3)
ctf1.margin_top = Inches(0.25)

p_cand = ctf1.paragraphs[0]
p_cand.text = "Candidate: Arg Jain (University Roll No. 2500320140031)"
p_cand.font.name = "Segoe UI"
p_cand.font.size = Pt(14)
p_cand.font.bold = True
p_cand.font.color.rgb = NAVY

p_dept = ctf1.add_paragraph()
p_dept.text = "Department of Master of Computer Applications (MCA) — Data Analytics Specialization\nABES Engineering College, Ghaziabad (Affiliated to Dr. A.P.J. Abdul Kalam Technical University, AKTU Code 032)"
p_dept.font.name = "Segoe UI"
p_dept.font.size = Pt(11.5)
p_dept.font.color.rgb = SLATE_DARK
p_dept.space_before = Pt(4)

p_ment = ctf1.add_paragraph()
p_ment.text = "Faculty Project Mentor: Mr. Dinesh | Batch ID: ABES_OND26_MCA2ndYear_Data Analytics_Batch01"
p_ment.font.name = "Segoe UI"
p_ment.font.size = Pt(11.5)
p_ment.font.bold = True
p_ment.font.color.rgb = TEAL
p_ment.space_before = Pt(4)

slide1.notes_slide.notes_text_frame.text = (
    "Good morning respected external examiners and faculty mentor Mr. Dinesh. My name is Arg Jain, "
    "Roll Number 2500320140031, from MCA 2nd Year Data Analytics at ABES Engineering College. "
    "Today, I present Project P100: 'Disease Trend Analysis Intelligence Cockpit', an end-to-end "
    "healthcare analytics platform developed across 18 formal engineering steps."
)

# ==========================================
# SLIDE 2: Business Problem & HMW Statements
# ==========================================
slide2 = prs.slides.add_slide(blank_layout)
add_header(slide2, "1. Epidemiological Surveillance Challenge & Design Thinking Framework", "Addressing Public Health Information Fragmentation & Emergency Intervention Delays Across India")

col_w = Inches(5.8)
col_h = Inches(5.3)

# Left Column: Problem Card
card_prob = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(1.5), col_w, col_h)
card_prob.fill.solid()
card_prob.fill.fore_color.rgb = WHITE
card_prob.line.color.rgb = RED
card_prob.line.width = Pt(1.5)

ptf = card_prob.text_frame
ptf.word_wrap = True
ptf.margin_left = ptf.margin_right = ptf.margin_top = Inches(0.25)

pp1 = ptf.paragraphs[0]
pp1.text = "⚠️ Critical Public Health Challenges"
pp1.font.name = "Segoe UI"
pp1.font.size = Pt(14)
pp1.font.bold = True
pp1.font.color.rgb = RED

prob_points = [
    "Fragmented Surveillance: Public health data in India is dispersed across static monthly PDF bulletins, hospital registers, and isolated state repositories.",
    "Delayed Outbreak Warnings: Health officers take weeks to recognize emerging contagion waves, losing the critical early 14-day containment window.",
    "Resource Misallocation: Hospitals face sudden shortages of ICU beds, oxygen, and emergency therapeutic supplies during seasonal surges.",
    "Unclear Fatality Metrics: Decision-makers lack normalized Case Fatality Rate (CFR) benchmarks across states to justify emergency financial grants."
]
for p in prob_points:
    pp = ptf.add_paragraph()
    pp.text = f"• {p}"
    pp.font.name = "Segoe UI"
    pp.font.size = Pt(10.5)
    pp.font.color.rgb = SLATE_DARK
    pp.space_before = Pt(8)

# Right Column: HMW Statements Card
card_hmw = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), col_w, col_h)
card_hmw.fill.solid()
card_hmw.fill.fore_color.rgb = WHITE
card_hmw.line.color.rgb = TEAL
card_hmw.line.width = Pt(1.5)

htf2 = card_hmw.text_frame
htf2.word_wrap = True
htf2.margin_left = htf2.margin_right = htf2.margin_top = Inches(0.25)

hp1 = htf2.paragraphs[0]
hp1.text = "💡 Operational Design Thinking: How Might We (HMW)"
hp1.font.name = "Segoe UI"
hp1.font.size = Pt(14)
hp1.font.bold = True
hp1.font.color.rgb = TEAL

hmw_points = [
    "HMW-01 (Surge Alert): How might we help health officers instantly spot which disease is spiking in a region vs. last year?",
    "HMW-03 (CFR Benchmark): How might we help policy makers compare Case Fatality Rates across states in a single glance to justify targeted emergency budgets?",
    "HMW-05 (Outbreak Detector): How might we alert hospital directors when multiple diseases surge simultaneously so ICUs don't collapse?",
    "HMW-08 (Urban Density): How might we correlate urban population density with transmission velocity to mandate timely municipal containment?"
]
for h in hmw_points:
    hp = htf2.add_paragraph()
    hp.text = f"• {h}"
    hp.font.name = "Segoe UI"
    hp.font.size = Pt(10.5)
    hp.font.color.rgb = SLATE_DARK
    hp.space_before = Pt(8)

slide2.notes_slide.notes_text_frame.text = (
    "Our research identified that public health authorities lose critical weeks attempting to correlate fragmented "
    "surveillance reports. Applying design-thinking principles, we formulated 10 actionable HMW statements targeting "
    "rapid outbreak detection, mortality severity benchmarking, and healthcare bed capacity preservation."
)

# ==========================================
# SLIDE 3: Executive Surveillance Cockpit (UI-01)
# ==========================================
slide3 = prs.slides.add_slide(blank_layout)
add_content_slide(
    slide3,
    title="2. Executive Surveillance Cockpit & High-Level Health Metrics",
    subtitle="Centralized Macro Monitoring Across 10 States, 5 Pathogens & 60 Monthly Longitudinal Intervals",
    image_path="docs/screenshots/01_cockpit_home.png",
    bullets=[
        "Monitors 5 major diseases: Dengue, Malaria, Tuberculosis, COVID-19, and Typhoid.",
        "Tracks 10 representative Indian states over a 5-year timeline (2020 to 2024, 60 monthly periods).",
        "4 Executive Tailwind KPI Cards: Total Morbidity (1.67M), Fatalities (43.5k), Clinical Recoveries (1.51M), and Active Caseload (116k).",
        "Interactive multi-dimensional sidebar: clean cascading filters for Category, Disease, Zone, State, Years, and Source."
    ],
    insight_text=(
        "Decision Impact: Consolidates multi-source surveillance streams into a centralized real-time command dashboard. "
        "Public health directors can assess national morbidity trends, track national Case Fatality Rate (2.6%), and benchmark "
        "active hospitalization pressure across 10 Indian states in sub-second queries, eliminating fragmented paper reporting."
    ),
    notes_text=(
        "The Executive Cockpit provides high-level situational awareness. The KPI cards dynamically re-aggregate based on the "
        "active sidebar filters, allowing health administrators to inspect macro-level epidemiological metrics instantly."
    )
)

# ==========================================
# SLIDE 4: State Burden & Benchmarking (UI-01)
# ==========================================
slide4 = prs.slides.add_slide(blank_layout)
add_content_slide(
    slide4,
    title="3. State-Level Morbidity Burden & Cross-State Benchmarking",
    subtitle="Regional Caseload Rankings & Cross-State Epidemiological Clinical Performance Analysis",
    image_path="docs/screenshots/02_overview_state_burden.png",
    bullets=[
        "Dynamic re-ranking bar chart with dropdown: sort states by Total Cases, Deaths, Recoveries, Active, or Hospitalized load.",
        "Metropolitan states lead absolute caseload: Maharashtra (244k) and Delhi (230k) carry the highest national burdens.",
        "Benchmark table incorporates conditional heat gradients for Case Fatality Rate (CFR %) and Clinical Recovery (%).",
        "1-Click CSV export enables state health officers to extract active benchmark datasets for offline reporting."
    ],
    insight_text=(
        "Decision Impact: Cross-evaluates absolute case volume against clinical severity. "
        "While metropolitan centers carry the largest gross infection volume, conditional gradients identify states with "
        "disproportionately elevated mortality rates, ensuring critical medical supplies, oxygen reserves, and clinical specialists "
        "are dispatched to high-fatality zones."
    ),
    notes_text=(
        "This view resolves Operational Questions OQ-02 and OQ-05. Gross case volume alone is insufficient; "
        "Case Fatality Rate benchmarking reveals healthcare management capacity and directs emergency aid where it saves lives."
    )
)

# ==========================================
# SLIDE 5: Longitudinal Waves & Seasonality (UI-02)
# ==========================================
slide5 = prs.slides.add_slide(blank_layout)
add_content_slide(
    slide5,
    title="4. 60-Month Trajectories & 12-Month Seasonal Surge Heatmap",
    subtitle="Longitudinal Transmission Waves (2020–2024), Moving Average Smoothing & Cyclical Patterns",
    image_path="docs/screenshots/03_trends_seasonality.png",
    bullets=[
        "Continuous 60-month time-series line chart tracks transmission waves for each pathogen over a 5-year observation horizon.",
        "Interactive smoothing window selector: toggle between Raw Monthly Data, 3-Month Rolling Average, and 6-Month Trendline.",
        "Year-over-Year (YoY %) delta matrix quantifies annual growth or reduction across epidemiological cycles.",
        "12-Month Seasonal Heatmap proves that Dengue and Malaria peak every year in July–October post-monsoon."
    ],
    insight_text=(
        "Decision Impact: Proves that disease transmission in India follows predictable cyclical seasonality. "
        "Mosquito-borne vector diseases (Dengue and Malaria) strictly surge between July and October post-monsoon, whereas "
        "respiratory pathogens peak during winter (December–February). This enables health ministries to execute prophylactic "
        "resource prepositioning 60 days before caseload spikes."
    ),
    notes_text=(
        "This answers OQ-01 and OQ-03. Proving repeatable annual cycles allows state departments to shift from reactive "
        "firefighting to proactive advance procurement of test kits, mosquito larvicides, and IV fluids."
    )
)

# ==========================================
# SLIDE 6: Regional Resilience Quadrant (UI-03)
# ==========================================
slide6 = prs.slides.add_slide(blank_layout)
add_content_slide(
    slide6,
    title="5. Regional Burden & Health System Resilience Quadrant",
    subtitle="Evaluating Healthcare Resilience, Infection Rates vs Mortality & Inpatient Bed Pressure",
    image_path="docs/screenshots/04_regional_cfr_recovery.png",
    bullets=[
        "Clinical Resilience Quadrant maps Incidence per 100k (x-axis) against Case Fatality Rate (CFR %, y-axis).",
        "High-Resilience Quadrant (High Cases, Low CFR): Highlights healthcare systems with superior clinical containment (Tamil Nadu, Karnataka).",
        "High-Vulnerability Quadrant (High Cases, High CFR): Pinpoints regional health deficits requiring urgent federal intervention.",
        "Hospital Bed Triage Pressure index tracks inpatient bed utilization vs outpatient care capacity across states."
    ],
    insight_text=(
        "Decision Impact: Distinguishes between high transmission and clinical management efficacy. "
        "A high infection rate does not result in high mortality if clinical protocols, ICU beds, and medications are administered "
        "effectively. The Resilience Quadrant enables policy makers to direct infrastructure grants to vulnerable healthcare networks."
    ),
    notes_text=(
        "This screen supports hospital directors and budget committees. By charting resilience, states can identify best clinical "
        "practices from high-resilience territories and deploy them in high-vulnerability regions."
    )
)

# ==========================================
# SLIDE 7: Demographic Vulnerability & Tornado Chart (UI-04)
# ==========================================
slide7 = prs.slides.add_slide(blank_layout)
add_content_slide(
    slide7,
    title="6. Demographic Segmentation & Geriatric Vulnerability Index",
    subtitle="Morbidity Distribution Across 5 Age Brackets, Gender Proportions & Senior Mortality Risk",
    image_path="docs/screenshots/05_demographics_cohorts.png",
    bullets=[
        "Morbidity segmentation across 5 standard cohorts: 0–14, 15–29, 30–44, 45–59, and 60+ senior citizens.",
        "Bidirectional Male vs Female Tornado Pyramid chart highlights gender symmetry and workforce cohort exposure.",
        "Geriatric Risk Multiplier Card: Senior citizens (60+) experience a 4.3x higher Case Fatality Rate (4.8% vs 1.1%).",
        "Dynamic filter synchronization: selecting specific pathogens or regions instantly recalculates demographic vulnerability."
    ],
    insight_text=(
        "Decision Impact: Identifies the critical divergence between infection risk and mortality risk. "
        "Young working-age populations (15–44) experience high infection volumes due to daily mobility, but senior citizens (60+) "
        "face four-fold higher fatality rates, justifying mandatory clinical triage protocols and targeted booster vaccination "
        "drives for geriatric cohorts."
    ),
    notes_text=(
        "Resolves OQ-04. The population pyramid demonstrates that while young adults drive disease spread, the elderly bear "
        "the clinical brunt of mortality. Triage protocols must prioritize elderly patients upon hospital admission."
    )
)

# ==========================================
# SLIDE 8: Urban Density Correlation (UI-05)
# ==========================================
slide8 = prs.slides.add_slide(blank_layout)
add_content_slide(
    slide8,
    title="7. Urban Density Scatter Regression & Contagion Velocity",
    subtitle="Statistically Verified Pearson Correlation (r = 0.9606) Between Density & Disease Incidence",
    image_path="docs/screenshots/06_eda_urban_density.png",
    bullets=[
        "Scatter regression correlates Population Density (persons/km²) with Cumulative Incidence per 100,000 residents.",
        "Statistical Proof: Pearson r = 0.9606, p-value = 0.0001 confirms a near-perfect positive linear relationship.",
        "Non-colliding smart directional badges label every state without text overlapping or visual occlusion.",
        "Dual-scale toggle: switch between Raw Linear scale (highlighting Delhi's extreme density) and Logarithmic scale."
    ],
    insight_text=(
        "Decision Impact: Provides empirical mathematical evidence that urban crowding accelerates transmission velocity. "
        "High-density metropolitan districts suffer rapid viral contagion compared to dispersed rural areas, delivering "
        "statistical justification for localized micro-containment and targeted sanitation investments during early outbreak phases."
    ),
    notes_text=(
        "Answers OQ-06. The Pearson correlation coefficient r = 0.9606 (p < 0.001) proves statistically that population density "
        "is a primary determinant of infection velocity across Indian administrative states."
    )
)

# ==========================================
# SLIDE 9: Automated Concurrent Outbreak Detector (UI-05)
# ==========================================
slide9 = prs.slides.add_slide(blank_layout)
add_content_slide(
    slide9,
    title="8. Multi-Disease Concurrent Outbreak Surveillance Engine",
    subtitle="Automated Surge Detection Algorithm with Dynamic Anomaly Sensitivity Multiplier (1.1x–2.5x)",
    image_path="docs/screenshots/06_eda_urban_density.png",
    bullets=[
        "Surveillance algorithm monitors 3,000 temporal records to detect simultaneous multi-pathogen surge events.",
        "Trigger Condition: Automatically flags state-months where 2 or more distinct diseases exceed baseline thresholds.",
        "Dynamic Sensitivity Slider: Allows health directors to calibrate anomaly sensitivity between 1.1x and 2.5x baseline.",
        "Dual-Surge Early Warning: Prevents hospital system collapse when post-monsoon Dengue coincides with Typhoid surges."
    ],
    insight_text=(
        "Decision Impact: Protects healthcare infrastructure against concurrent syndromic gridlock. "
        "By benchmarking historical monthly baselines across every state and pathogen, the surveillance engine automatically warns "
        "administrators when multiple co-infections surge simultaneously, preventing diagnostic lab backlogs and blood bank depletion."
    ),
    notes_text=(
        "Answers OQ-08. Simultaneous epidemics overwhelm hospital capacity much faster than isolated diseases. "
        "Automated multi-disease anomaly alerts enable proactive multi-department coordination."
    )
)

# ==========================================
# SLIDE 10: Data Governance & 3NF Schema (UI-06)
# ==========================================
slide10 = prs.slides.add_slide(blank_layout)
add_content_slide(
    slide10,
    title="9. Data Quality Governance, In-Pipeline Cleaning & 3NF Schema",
    subtitle="Automated Pipeline Sanitization (Duplicates, Imputation, Capping) & Relational SQLite Architecture",
    image_path="docs/screenshots/07_data_quality_ledger.png",
    bullets=[
        "Automated cleaning pipeline: purged 149 duplicate entries, median-imputed 42 nulls, and capped 7 extreme outliers.",
        "Data Quality Ledger: Complete audit transparency accounting for every ingested record (3,000 in ➔ 2,854 clean rows).",
        "Third Normal Form (3NF) Relational SQLite Schema: 5 base tables with primary keys, foreign keys, and CHECK constraints.",
        "Precomputed Analytical View (v_disease_analysis): Materializes joined facts and dimensions for sub-second query latency."
    ],
    insight_text=(
        "Decision Impact: Enforces enterprise data governance before analytical consumption. "
        "Eliminating duplicate transactions, imputing missing values, and Winsorizing extreme typographical errors guarantees "
        "clinical reporting reliability, while a Third Normal Form relational architecture eliminates redundant data storage and maintains relational integrity."
    ),
    notes_text=(
        "Demonstrates data engineering rigor. The pipeline automatically enforces business rules and sanitizes raw hospital data "
        "into verified analytical records certified for clinical policy modeling."
    )
)

# ==========================================
# SLIDE 11: 100% Automated Testing Suite (QA)
# ==========================================
slide11 = prs.slides.add_slide(blank_layout)
add_header(slide11, "10. Software Quality Assurance & 100% Automated Testing Suite", "Unit Verification Across Schema Constraints, Clinical Formulations & Application Entry Points")

tcol_w = Inches(3.8)
tcol_h = Inches(5.3)

# Test Column 1: Database & Schema
tcard1 = slide11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(1.5), tcol_w, tcol_h)
tcard1.fill.solid()
tcard1.fill.fore_color.rgb = WHITE
tcard1.line.color.rgb = NAVY
tcard1.line.width = Pt(1.5)

tf1 = tcard1.text_frame
tf1.word_wrap = True
tf1.margin_left = tf1.margin_right = tf1.margin_top = Inches(0.2)

tp1 = tf1.paragraphs[0]
tp1.text = "🗄️ Database & Schema Tests\n(8 Tests — test_data.py)"
tp1.font.name = "Segoe UI"
tp1.font.size = Pt(12)
tp1.font.bold = True
tp1.font.color.rgb = NAVY

t1_points = [
    "TC-T-01: All 5 base tables exist in SQLite.",
    "TC-T-02: Volume verification (~3,000 rows).",
    "TC-T-03: Masters exact row counts.",
    "TC-T-04: Zero orphaned foreign keys.",
    "TC-T-05: Clinical bounds (deaths <= cases).",
    "TC-T-06: Unique disease name constraint.",
    "TC-T-07: Materialized view column match.",
    "TC-T-15: Query latency < 1.5 seconds."
]
for p in t1_points:
    tp = tf1.add_paragraph()
    tp.text = f"✅ {p}"
    tp.font.name = "Segoe UI"
    tp.font.size = Pt(9.5)
    tp.font.color.rgb = SLATE_DARK
    tp.space_before = Pt(4)

# Test Column 2: Mathematical Formulations
tcard2 = slide11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.75), Inches(1.5), tcol_w, tcol_h)
tcard2.fill.solid()
tcard2.fill.fore_color.rgb = WHITE
tcard2.line.color.rgb = TEAL
tcard2.line.width = Pt(1.5)

tf2 = tcard2.text_frame
tf2.word_wrap = True
tf2.margin_left = tf2.margin_right = tf2.margin_top = Inches(0.2)

tp2 = tf2.paragraphs[0]
tp2.text = "📐 Analytical Math Tests\n(6 Tests — test_analysis.py)"
tp2.font.name = "Segoe UI"
tp2.font.size = Pt(12)
tp2.font.bold = True
tp2.font.color.rgb = TEAL

t2_points = [
    "TC-T-09: CFR formula (100 cases, 5 deaths = 5.0%).",
    "TC-T-10: Recovery rate (100 cases, 92 rec = 92.0%).",
    "TC-T-11: YoY % growth (+100.0% for 200 vs 100).",
    "TC-T-12: Incidence / 100k (1000 in 1M = 100.0).",
    "TC-T-13: Concurrent outbreak trigger threshold.",
    "TC-T-14: Pearson r = 1.0 for linear series."
]
for p in t2_points:
    tp = tf2.add_paragraph()
    tp.text = f"✅ {p}"
    tp.font.name = "Segoe UI"
    tp.font.size = Pt(9.5)
    tp.font.color.rgb = SLATE_DARK
    tp.space_before = Pt(5)

# Test Column 3: App Smoke & Structure
tcard3 = slide11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.9), Inches(1.5), tcol_w, tcol_h)
tcard3.fill.solid()
tcard3.fill.fore_color.rgb = WHITE
tcard3.line.color.rgb = EMERALD
tcard3.line.width = Pt(1.5)

tf3 = tcard3.text_frame
tf3.word_wrap = True
tf3.margin_left = tf3.margin_right = tf3.margin_top = Inches(0.2)

tp3 = tf3.paragraphs[0]
tp3.text = "🚀 App Smoke & Routing\n(3 Tests — test_app.py)"
tp3.font.name = "Segoe UI"
tp3.font.size = Pt(12)
tp3.font.bold = True
tp3.font.color.rgb = EMERALD

t3_points = [
    "TC-T-16: app.py and all 6 multi-page files exist.",
    "TC-T-17: All modular src/ files exist.",
    "TC-T-18: Configuration & manifests verified.",
    "17 PASSED, 0 FAILED in 0.06 seconds.",
    "Zero-dependency runner: python run_tests.py.",
    "100% Success Rate across entire test suite."
]
for p in t3_points:
    tp = tf3.add_paragraph()
    tp.text = f"✅ {p}"
    tp.font.name = "Segoe UI"
    tp.font.size = Pt(9.5)
    tp.font.color.rgb = SLATE_DARK
    tp.space_before = Pt(5)

slide11.notes_slide.notes_text_frame.text = (
    "Our quality assurance suite guarantees software reliability. Executing 'python run_tests.py' verifies all 17 unit tests "
    "in 60 milliseconds with zero dependencies, proving relational schema integrity, formula accuracy, and UI module readiness."
)

# ==========================================
# SLIDE 12: BI Integration (Tableau & Power BI)
# ==========================================
slide12 = prs.slides.add_slide(blank_layout)
add_header(slide12, "11. Enterprise Business Intelligence: Tableau & Power BI Integration", "Enterprise Star-Schema Data Marts, Production DAX Measures & Tableau Calculated Fields")

bi_w = Inches(5.8)
bi_h = Inches(5.3)

# Power BI Card
card_pbi = slide12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(1.5), bi_w, bi_h)
card_pbi.fill.solid()
card_pbi.fill.fore_color.rgb = WHITE
card_pbi.line.color.rgb = AMBER
card_pbi.line.width = Pt(1.5)

ptfb = card_pbi.text_frame
ptfb.word_wrap = True
ptfb.margin_left = ptfb.margin_right = ptfb.margin_top = Inches(0.25)

pbi_title = ptfb.paragraphs[0]
pbi_title.text = "📊 Power BI Enterprise Architecture"
pbi_title.font.name = "Segoe UI"
pbi_title.font.size = Pt(14)
pbi_title.font.bold = True
pbi_title.font.color.rgb = AMBER

pbi_bullets = [
    "Data Source Mart: data/disease_analysis_merged.csv (3,003 rows, 25 columns) + demographics_merged.csv (300 rows).",
    "Star Schema Model: 1 centralized Fact table linked to 4 Dimension tables (Date, Disease, Region, Demographics).",
    "Production DAX Measures: Documented in docs/powerbi_dax_measures.txt:",
    "  • Total Morbidity = SUM(FactCases[cases_reported])",
    "  • Case Fatality Rate (CFR %) = DIVIDE([Total Fatalities], [Total Morbidity], 0) * 100",
    "  • 3-Month Moving Average = CALCULATE(AVERAGEX(FactCases, [Total Morbidity]), DATESINPERIOD(DimDate[Date], MAX(DimDate[Date]), -3, MONTH))",
    "  • Geriatric Vulnerability Index = DIVIDE([Senior CFR], [Pediatric CFR], 1.0)"
]
for b in pbi_bullets:
    bp = ptfb.add_paragraph()
    bp.text = b
    bp.font.name = "Segoe UI"
    bp.font.size = Pt(10)
    bp.font.color.rgb = SLATE_DARK
    bp.space_before = Pt(6)

# Tableau Card
card_tab = slide12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), bi_w, bi_h)
card_tab.fill.solid()
card_tab.fill.fore_color.rgb = WHITE
card_tab.line.color.rgb = SKY
card_tab.line.width = Pt(1.5)

ttfb = card_tab.text_frame
ttfb.word_wrap = True
ttfb.margin_left = ttfb.margin_right = ttfb.margin_top = Inches(0.25)

tab_title = ttfb.paragraphs[0]
tab_title.text = "📈 Tableau Dashboard Architecture"
tab_title.font.name = "Segoe UI"
tab_title.font.size = Pt(14)
tab_title.font.bold = True
tab_title.font.color.rgb = SKY

tab_bullets = [
    "Data Connection: Direct live extract from SQLite / CSV analytical projection.",
    "Visual Hierarchy: 4 Interactive Dashboards (Executive Cockpit, Geospatial Heatmap, Temporal Trajectory, Demographic Pyramid).",
    "Tableau Calculated Fields: Documented in docs/tableau_calculated_fields.txt:",
    "  • [CFR %] = SUM([Deaths]) / SUM([Cases Reported]) * 100",
    "  • [Incidence per 100k] = (SUM([Cases Reported]) / ATTR([Population])) * 100000",
    "  • [Monsoon Peak Flag] = IF MONTH([Report Date]) >= 7 AND MONTH([Report Date]) <= 10 THEN 'Monsoon Surge' ELSE 'Baseline' END",
    "Enterprise Guide: Documented in docs/19_Tableau_PowerBI_Dashboard_Specification.md."
]
for b in tab_bullets:
    bp = ttfb.add_paragraph()
    bp.text = b
    bp.font.name = "Segoe UI"
    bp.font.size = Pt(10)
    bp.font.color.rgb = SLATE_DARK
    bp.space_before = Pt(6)

slide12.notes_slide.notes_text_frame.text = (
    "Beyond Streamlit, we created complete enterprise BI specifications for Tableau and Power BI. "
    "We wrote production-ready DAX formulas, Tableau calculated fields, and exported clean CSV data marts so that "
    "any enterprise analytics team can deploy these exact dashboards in Power BI Service or Tableau Server."
)

# ==========================================
# SLIDE 13: Future Scope & Strategic Recommendations (REPLACES CHEAT SHEET)
# ==========================================
slide13 = prs.slides.add_slide(blank_layout)
add_header(slide13, "12. Future Scope, System Scalability & Strategic Recommendations", "Next-Phase Architectural Enhancements, Predictive AI Modeling & Public Health Policy Roadmap")

scope_w = Inches(5.8)
scope_h = Inches(5.3)

# Left Column: Technical Roadmap
card_tech = slide13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(1.5), scope_w, scope_h)
card_tech.fill.solid()
card_tech.fill.fore_color.rgb = WHITE
card_tech.line.color.rgb = TEAL
card_tech.line.width = Pt(1.5)

ttfc = card_tech.text_frame
ttfc.word_wrap = True
ttfc.margin_left = ttfc.margin_right = ttfc.margin_top = Inches(0.25)

tc_title = ttfc.paragraphs[0]
tc_title.text = "🚀 Technical Architecture & AI Roadmap"
tc_title.font.name = "Segoe UI"
tc_title.font.size = Pt(14)
tc_title.font.bold = True
tc_title.font.color.rgb = TEAL

tech_points = [
    "Automated Hospital EHR Ingestion: Direct API connectors integrating with district hospital electronic records via HL7 / FHIR standards.",
    "Predictive Machine Learning Forecasting: Integration of deep learning LSTM and Prophet time-series models for 30-day advance outbreak wave projection.",
    "Mobile Progressive Web App: Lightweight offline-first mobile client for frontline ASHA and ANM community health workers in rural blocks.",
    "Geospatial Micro-Clustering: Sub-district and PIN code level GIS spatial autocorrelation (Moran's I) for precision epidemic containment."
]
for tp in tech_points:
    tpp = ttfc.add_paragraph()
    tpp.text = f"• {tp}"
    tpp.font.name = "Segoe UI"
    tpp.font.size = Pt(10.5)
    tpp.font.color.rgb = SLATE_DARK
    tpp.space_before = Pt(8)

# Right Column: Policy Recommendations
card_pol = slide13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), scope_w, scope_h)
card_pol.fill.solid()
card_pol.fill.fore_color.rgb = WHITE
card_pol.line.color.rgb = EMERALD
card_pol.line.width = Pt(1.5)

ptfp = card_pol.text_frame
ptfp.word_wrap = True
ptfp.margin_left = ptfp.margin_right = ptfp.margin_top = Inches(0.25)

pol_title = ptfp.paragraphs[0]
pol_title.text = "📋 Public Health & Policy Recommendations"
pol_title.font.name = "Segoe UI"
pol_title.font.size = Pt(14)
pol_title.font.bold = True
pol_title.font.color.rgb = EMERALD

pol_points = [
    "Proactive Medical Logistics Prepositioning: Mandate 60-day advance procurement and dispatch of mosquito larvicides and IV fluids ahead of July monsoon surges.",
    "Prioritized Geriatric Clinical Pathways: Formalize immediate admission and clinical triage protocols for senior citizens (60+) to reduce avoidable mortality.",
    "Automated Density-Triggered Containment: Enforce phased municipal containment and sanitation protocols automatically when density-adjusted incidence exceeds 1.5x baseline.",
    "Integrated Multi-Disease Vector Control: Coordinate joint vector abatement programs in urban corridors where Dengue and Malaria transmission windows overlap."
]
for pp in pol_points:
    ppp = ptfp.add_paragraph()
    ppp.text = f"• {pp}"
    ppp.font.name = "Segoe UI"
    ppp.font.size = Pt(10.5)
    ppp.font.color.rgb = SLATE_DARK
    ppp.space_before = Pt(8)

slide13.notes_slide.notes_text_frame.text = (
    "Looking forward, the platform is designed for enterprise scale. Future iterations can integrate live hospital APIs, "
    "machine-learning forecasting models, and mobile reporting apps for field health workers, translating data analytics "
    "into life-saving national public health policies."
)

# ==========================================
# SLIDE 14: Formal Project Conclusion & Attribution (REPLACES VIVA LAST PAGE)
# ==========================================
slide14 = prs.slides.add_slide(blank_layout)
add_header(slide14, "13. Project Conclusion & Formal Academic Sign-Off", "Final Academic Evaluation Summary for Master of Computer Applications (MCA 2nd Year)")

conc_w = Inches(5.8)
conc_h = Inches(5.3)

# Left Column: Project Conclusion Summary
card_conc = slide14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(1.5), conc_w, conc_h)
card_conc.fill.solid()
card_conc.fill.fore_color.rgb = WHITE
card_conc.line.color.rgb = NAVY
card_conc.line.width = Pt(1.5)

ctfc = card_conc.text_frame
ctfc.word_wrap = True
ctfc.margin_left = ctfc.margin_right = ctfc.margin_top = Inches(0.25)

cc_title = ctfc.paragraphs[0]
cc_title.text = "🏆 Key Project Achievements"
cc_title.font.name = "Segoe UI"
cc_title.font.size = Pt(14)
cc_title.font.bold = True
cc_title.font.color.rgb = NAVY

achieve_points = [
    "Comprehensive 5-Year Surveillance: Engineered an interactive analytics cockpit tracking 3,000 monthly reports across 10 states and 5 high-burden diseases.",
    "Full-Stack Relational Architecture: Delivered a Third Normal Form SQLite database, sub-second cached queries, and Tailwind CSS injected components.",
    "Empirical Epidemiological Proof: Validated strong density correlation (r = 0.9606, p = 0.0001), monsoon vector cycles, and 4.3x senior mortality risk.",
    "Rigorous Quality Assurance: 100% automated test pass rate across 17 unit tests, verified data quality governance, and comprehensive BI models."
]
for ap in achieve_points:
    app = ctfc.add_paragraph()
    app.text = f"• {ap}"
    app.font.name = "Segoe UI"
    app.font.size = Pt(10.5)
    app.font.color.rgb = SLATE_DARK
    app.space_before = Pt(8)

# Right Column: Academic Sign-Off & Acknowledgments
card_ack = slide14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), conc_w, conc_h)
card_ack.fill.solid()
card_ack.fill.fore_color.rgb = WHITE
card_ack.line.color.rgb = TEAL
card_ack.line.width = Pt(1.5)

atf = card_ack.text_frame
atf.word_wrap = True
atf.margin_left = atf.margin_right = atf.margin_top = Inches(0.25)

ack_title = atf.paragraphs[0]
ack_title.text = "🎓 Academic Project Sign-Off & Attribution"
ack_title.font.name = "Segoe UI"
ack_title.font.size = Pt(14)
ack_title.font.bold = True
ack_title.font.color.rgb = TEAL

p_c = atf.add_paragraph()
p_c.text = "Candidate Name: Arg Jain\nUniversity Roll No.: 2500320140031\nProgram: MCA 2nd Year (Data Analytics Specialization)\nInstitution: ABES Engineering College, Ghaziabad (AKTU Code 032)"
p_c.font.name = "Segoe UI"
p_c.font.size = Pt(10.5)
p_c.font.color.rgb = SLATE_DARK
p_c.space_before = Pt(6)

p_m = atf.add_paragraph()
p_m.text = "Faculty Project Mentor: Mr. Dinesh\nDepartment: Department of Master of Computer Applications\nProject Identifier: Project P100 | Healthcare Data Analytics"
p_m.font.name = "Segoe UI"
p_m.font.size = Pt(10.5)
p_m.font.color.rgb = NAVY
p_m.font.bold = True
p_m.space_before = Pt(10)

p_thanks = atf.add_paragraph()
p_thanks.text = "Acknowledgments: Sincere gratitude to faculty mentor Mr. Dinesh, the Department of MCA, and the Examination Committee of ABES Engineering College for academic guidance, technical mentorship, and evaluation."
p_thanks.font.name = "Segoe UI"
p_thanks.font.size = Pt(10)
p_thanks.font.color.rgb = SLATE_MUTED
p_thanks.font.italic = True
p_thanks.space_before = Pt(12)

slide14.notes_slide.notes_text_frame.text = (
    "In conclusion, Project P100 successfully addresses fragmented public health reporting through an end-to-end "
    "data analytics platform. I express my sincere gratitude to my mentor Mr. Dinesh and the examination "
    "board for their continuous guidance. Thank you, and I am now ready for your questions."
)

# Save the presentation
output_pptx = Path("c:/Users/Hp/Downloads/hcl/docs/18_ArgJain_DiseaseTrendAnalysis_Presentation.pptx")
prs.save(str(output_pptx))
print(f"POWERPOINT PRESENTATION COMPILED SUCCESSFULLY: {output_pptx} ({output_pptx.stat().st_size // 1024} KB)")
