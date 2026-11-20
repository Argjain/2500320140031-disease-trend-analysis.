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

# Color Palette Definitions (Executive Healthcare Theme)
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

def add_content_slide(slide, title, subtitle, image_path, bullets, explain_text, notes_text):
    """Creates a structured two-column presentation slide with image, bullets, and spoken explanation."""
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
    
    # Right Column: Highlights & Explanation
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
        
    # 2. Easy Spoken Explanation Card (Normal Language Paragraph)
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
    cp1.text = "🗣️ How to Explain this to Teachers & Students:"
    cp1.font.name = "Segoe UI"
    cp1.font.size = Pt(12)
    cp1.font.bold = True
    cp1.font.color.rgb = TEAL
    
    cp2 = ctf.add_paragraph()
    cp2.text = explain_text
    cp2.font.name = "Segoe UI"
    cp2.font.size = Pt(10.2)
    cp2.font.color.rgb = SLATE_DARK
    cp2.space_before = Pt(5)
    
    # Add Speaker Notes
    notes_slide = slide.notes_slide
    notes_slide.notes_text_frame.text = notes_text

# ==========================================
# SLIDE 1: Title Slide (Grand Cover)
# ==========================================
slide1 = prs.slides.add_slide(blank_layout)

bg = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(4.5))
bg.fill.solid()
bg.fill.fore_color.rgb = NAVY
bg.line.fill.background()

tb = slide1.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(11.7), Inches(3.0))
tf = tb.text_frame
tf.word_wrap = True

p1 = tf.paragraphs[0]
p1.text = "🏥 Disease Trend Analysis Intelligence Cockpit"
p1.font.name = "Segoe UI"
p1.font.size = Pt(32)
p1.font.bold = True
p1.font.color.rgb = WHITE

p2 = tf.add_paragraph()
p2.text = "An Interactive Healthcare Surveillance & Epidemiological Data Analytics Platform for India"
p2.font.name = "Segoe UI"
p2.font.size = Pt(16)
p2.font.color.rgb = RGBColor(186, 230, 253)
p2.space_before = Pt(10)

p3 = tf.add_paragraph()
p3.text = "Project ID: P-01 | Healthcare Data Analytics | Technology Stack: Python, Streamlit, SQLite, Plotly, Tailwind CSS"
p3.font.name = "Segoe UI"
p3.font.size = Pt(12)
p3.font.color.rgb = RGBColor(224, 242, 254)
p3.space_before = Pt(14)

# Candidate & Mentor Details Card
card1 = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.9), Inches(11.7), Inches(2.0))
card1.fill.solid()
card1.fill.fore_color.rgb = WHITE
card1.line.color.rgb = BORDER_COLOR
card1.line.width = Pt(1.5)

ctf1 = card1.text_frame
ctf1.word_wrap = True
ctf1.margin_left = Inches(0.3)
ctf1.margin_top = Inches(0.25)

p_cand = ctf1.paragraphs[0]
p_cand.text = "Student / Developer: Arg Jain (University Roll No. 2500320140031)"
p_cand.font.name = "Segoe UI"
p_cand.font.size = Pt(14)
p_cand.font.bold = True
p_cand.font.color.rgb = NAVY

p_dept = ctf1.add_paragraph()
p_dept.text = "MCA 2nd Year — Data Analytics Specialization | ABES Engineering College, Ghaziabad (AKTU Code 032)"
p_dept.font.name = "Segoe UI"
p_dept.font.size = Pt(12)
p_dept.font.color.rgb = SLATE_DARK
p_dept.space_before = Pt(4)

p_ment = ctf1.add_paragraph()
p_ment.text = "Faculty Project Mentor: Ms. Kalpana Dwivedi | Target Academic Release: November 2026"
p_ment.font.name = "Segoe UI"
p_ment.font.size = Pt(12)
p_ment.font.bold = True
p_ment.font.color.rgb = TEAL
p_ment.space_before = Pt(4)

slide1.notes_slide.notes_text_frame.text = (
    "Good morning respected external examiner and faculty mentor Ms. Kalpana Dwivedi. My name is Arg Jain, "
    "Roll Number 2500320140031, from MCA 2nd Year Data Analytics at ABES Engineering College. "
    "Today, I am proud to present Project P-01: 'Disease Trend Analysis Intelligence Cockpit', an end-to-end "
    "healthcare analytics platform developed across 18 rigorous engineering steps."
)

# ==========================================
# SLIDE 2: Business Problem & HMW Statements
# ==========================================
slide2 = prs.slides.add_slide(blank_layout)
add_header(slide2, "1. Healthcare Surveillance Problem & Design Thinking (HMW)", "Transforming Fragmented Indian Public Health Data into Actionable Epidemiological Intelligence")

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
pp1.text = "⚠️ The Real-World Healthcare Problem"
pp1.font.name = "Segoe UI"
pp1.font.size = Pt(14)
pp1.font.bold = True
pp1.font.color.rgb = RED

prob_points = [
    "Fragmented Surveillance: Public health data in India is dispersed across static monthly PDF bulletins, hospital registers, and isolated databases.",
    "Delayed Outbreak Warnings: Health officers take weeks to recognize emerging contagion waves, losing the critical 14-day containment window.",
    "Resource Misallocation: Hospitals face sudden shortages of ICU beds, oxygen, and emergency therapeutic supplies during seasonal surges.",
    "Unclear Fatality Metrics: Decision-makers struggle to benchmark Case Fatality Rates (CFR) across states to justify emergency financial grants."
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
hp1.text = "💡 Design Thinking: How Might We (HMW) Statements"
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
    "In our research, we found that hospital staff and health officers in India lose critical weeks trying to combine "
    "disjointed data sources. We formulated 10 HMW questions to design our platform around real human needs: "
    "instant surge spotting, single-glance fatality comparison, and predictive ICU planning."
)

# ==========================================
# SLIDE 3: Executive Surveillance Cockpit (UI-01)
# ==========================================
slide3 = prs.slides.add_slide(blank_layout)
add_content_slide(
    slide3,
    title="2. Executive Surveillance Cockpit & Key Health Metrics",
    subtitle="Overview Dashboard | Live Morbidity, Fatalities, Recoveries & Active Caseload Across India",
    image_path="docs/screenshots/01_cockpit_home.png",
    bullets=[
        "Monitors 5 major diseases: Dengue, Malaria, Tuberculosis, COVID-19, and Typhoid.",
        "Tracks 10 representative Indian states over a 5-year timeline (2020 to 2024, 60 monthly periods).",
        "4 live KPI stat cards calculate Morbidity (1.67M), Deaths (43.5k), Recoveries (1.51M), and Active Cases (116k).",
        "Interactive sidebar provides clean dropdowns for Category, Disease, Zone, State, and a 5-year timeline slider."
    ],
    explain_text=(
        "Teachers and students, what you are looking at is the command center of our application. "
        "Imagine you are a Public Health Officer managing disease spread across India. Instead of opening 10 different "
        "spreadsheets, this cockpit immediately tells you the total picture: 1.67 million recorded cases, 43,500 deaths, "
        "and our national 90.4% clinical recovery rate. Using the clean sidebar on the left, you can select any disease like Dengue "
        "or any state like Maharashtra, and all 4 KPI cards recalculate instantly."
    ),
    notes_text=(
        "When explaining this slide: Point to the 4 KPI cards at the top. Mention that these cards recalculate in sub-second "
        "speeds using cached SQLite queries. Point out the sidebar filters and explain that the Quick Presets were removed "
        "for a cleaner user experience."
    )
)

# ==========================================
# SLIDE 4: State Burden & Benchmarking (UI-01)
# ==========================================
slide4 = prs.slides.add_slide(blank_layout)
add_content_slide(
    slide4,
    title="3. State-Level Morbidity Burden & Metric Ranking",
    subtitle="Interactive Regional Case Ranking & Cross-State Epidemiological Performance Benchmarking",
    image_path="docs/screenshots/02_overview_state_burden.png",
    bullets=[
        "Dynamic re-ranking bar chart with dropdown: sort states by Total Cases, Deaths, Recoveries, Active, or Hospitalized.",
        "Maharashtra (244k) and Delhi (230k) carry the highest caseload due to urban density and travel connectivity.",
        "Cross-state benchmark table features background heat gradients for Case Fatality Rate (CFR %) and Recovery (%).",
        "1-Click CSV export allows health officials to download the active state benchmark table for offline reporting."
    ],
    explain_text=(
        "On this second screen, we answer a vital operational question: Which states are carrying the heaviest disease load? "
        "Our horizontal bar chart ranks all 10 states. Notice that Maharashtra and Delhi lead the caseload. "
        "Right below it, our styled benchmark table compares Case Fatality Rate (CFR %) side-by-side with recovery rates. "
        "This tells health ministers not just where cases are high, but which states are having trouble keeping patients alive, "
        "so emergency oxygen, ventilators, and medical doctors can be dispatched immediately."
    ),
    notes_text=(
        "When explaining this slide: Emphasize that total cases alone don't show clinical severity. "
        "Case Fatality Rate (CFR %) is what tells doctors which health systems are overwhelmed. Mention the CSV export button."
    )
)

# ==========================================
# SLIDE 5: Longitudinal Waves & Seasonality (UI-02)
# ==========================================
slide5 = prs.slides.add_slide(blank_layout)
add_content_slide(
    slide5,
    title="4. 60-Month Trajectory & 12-Month Seasonal Heatmap",
    subtitle="Tracking Longitudinal Waves (2020–2024), Moving Average Smoothing & Annual Monsoon Surges",
    image_path="docs/screenshots/03_trends_seasonality.png",
    bullets=[
        "Continuous 60-month time-series line chart tracks transmission dynamics for each pathogen.",
        "Interactive curve smoothing toggle: switch between Raw Monthly, 3-Month Rolling Average, and 6-Month Trendline.",
        "Year-over-Year (YoY %) delta matrix tracks percentage growth or decline across calendar years.",
        "12-Month Seasonal Intensity Heatmap proves that Dengue and Malaria peak every year in July–October post-monsoon."
    ],
    explain_text=(
        "This is one of our most important discoveries. Diseases in India do not strike randomly—they follow cyclical seasons. "
        "Our line chart tracks 5 years of monthly numbers. But look at the seasonal heatmap on the right: "
        "it clearly proves that mosquito-borne diseases like Dengue and Malaria peak every single year between July and October "
        "right after the monsoon rains. Respiratory illnesses like COVID-19 and Tuberculosis spike in winter (December–February). "
        "By knowing this 60 days in advance, hospitals can stock test kits and intravenous fluids before the rush starts."
    ),
    notes_text=(
        "When explaining this slide: Emphasize the concept of 'Predictive Prepositioning'. "
        "Explain that monsoons create stagnant water pools where mosquitoes breed, while cold winter air accelerates airborne transmission."
    )
)

# ==========================================
# SLIDE 6: Regional Resilience Quadrant (UI-03)
# ==========================================
slide6 = prs.slides.add_slide(blank_layout)
add_content_slide(
    slide6,
    title="5. Regional Burden & Health System Resilience Quadrant",
    subtitle="Cross-State Health System Capacity, Infection Rate vs Mortality & Hospital Bed Pressure",
    image_path="docs/screenshots/04_regional_cfr_recovery.png",
    bullets=[
        "Clinical Resilience Quadrant scatter plot maps Incidence Rate per 100k (x-axis) vs Case Fatality Rate % (y-axis).",
        "High-Resilience Quadrant (High Cases, Low CFR): Efficient healthcare containment prevents patient deaths (Tamil Nadu, Karnataka).",
        "High-Vulnerability Quadrant (High Cases, High CFR): Critical infrastructure deficit demanding emergency federal intervention.",
        "Hospital Bed Triage Pressure index tracks inpatient bed utilization vs outpatient care capacity."
    ],
    explain_text=(
        "In this screen, we evaluate how well each state's healthcare system handles disease outbreaks. "
        "We plot Incidence per 100,000 residents against Case Fatality Rate (CFR %). "
        "States in the bottom-right quadrant have high infection rates but very low mortality—meaning their doctors, hospitals, "
        "and treatment protocols are working exceptionally well. On the other hand, states in the top-right quadrant have high cases "
        "and high deaths, indicating an urgent need for hospital infrastructure investment."
    ),
    notes_text=(
        "When explaining this slide: Use the term 'Resilience Quadrant'. "
        "Explain that high cases do not have to mean high deaths if clinical management is effective."
    )
)

# ==========================================
# SLIDE 7: Demographic Vulnerability & Tornado Chart (UI-04)
# ==========================================
slide7 = prs.slides.add_slide(blank_layout)
add_content_slide(
    slide7,
    title="6. Demographic Segmentation & Geriatric Risk Multiplier",
    subtitle="Morbidity Across 5 Age Brackets, Gender Proportions & Senior Citizen Mortality Vulnerability",
    image_path="docs/screenshots/05_demographics_cohorts.png",
    bullets=[
        "Morbidity disaggregation across 5 distinct age cohorts: 0-14, 15-29, 30-44, 45-59, and 60+ seniors.",
        "Bidirectional Male vs Female Tornado Pyramid chart highlights gender symmetry and workforce vulnerability.",
        "Geriatric Risk Multiplier Card: Senior citizens (60+) face a 3.6x to 4.3x higher Case Fatality Rate (4.8% vs 1.1%).",
        "Fully synchronized with sidebar filters: selecting Malaria or Dengue immediately updates the demographic breakdown."
    ],
    explain_text=(
        "Here we analyzed WHO gets sick and WHO is most at risk of dying. "
        "While young working adults aged 15 to 44 catch the highest number of infections because they travel and work, "
        "look at the Geriatric Mortality Risk Card on the right: senior citizens aged 60 and older face a Case Fatality Rate "
        "over 4 times higher than young people. This proves that while public health campaigns should target youth for infection prevention, "
        "hospital ICU beds and antiviral therapies must be reserved immediately for senior citizens."
    ),
    notes_text=(
        "When explaining this slide: Point to the Tornado chart showing male and female side-by-side. "
        "Highlight that 60+ seniors have the lowest infection count but the highest death rate, which is a key clinical insight."
    )
)

# ==========================================
# SLIDE 8: Urban Density Correlation (UI-05)
# ==========================================
slide8 = prs.slides.add_slide(blank_layout)
add_content_slide(
    slide8,
    title="7. Urban Crowding Scatter Regression & Statistical Proof",
    subtitle="Statistically Verified Pearson Correlation (r = 0.9606) Between Density & Contagion Velocity",
    image_path="docs/screenshots/06_eda_urban_density.png",
    bullets=[
        "Scatter plot correlates Population Density (persons/km²) with Cumulative Incidence per 100,000 residents.",
        "Statistical Proof: Pearson r = 0.9606, p-value = 0.0001 proves that urban crowding directly drives contagion speed.",
        "Non-colliding directional pointer callouts: smart badges label every state clearly with zero overlapping text.",
        "Interactive dual-scale toggle: switch between Raw Linear scale (showing Delhi outlier) and Logarithmic scale."
    ],
    explain_text=(
        "This slide presents our deepest statistical evidence. We wanted to mathematically prove: Does urban crowding accelerate disease spread? "
        "We calculated the Pearson correlation coefficient between population density and disease incidence. "
        "The result was r = 0.96, which is an exceptionally strong, statistically significant relationship (p = 0.0001). "
        "Notice Delhi at the top-right: with over 11,000 people per square kilometer, it experiences the highest incidence. "
        "We also built smart callout badges with directional arrows so that state labels never collide or overlap."
    ),
    notes_text=(
        "When explaining this slide: Explain what Pearson r = 0.96 means: near-perfect positive linear relationship. "
        "Mention that p = 0.0001 means the probability of this happening by chance is less than 1 in 10,000."
    )
)

# ==========================================
# SLIDE 9: Automated Concurrent Outbreak Detector (UI-05)
# ==========================================
slide9 = prs.slides.add_slide(blank_layout)
add_content_slide(
    slide9,
    title="8. Multi-Disease Concurrent Outbreak Surveillance Engine",
    subtitle="Automated Anomaly Detection with Sensitivity Multiplier Slider (1.1x to 2.5x Baseline)",
    image_path="docs/screenshots/06_eda_urban_density.png",
    bullets=[
        "Automated algorithm scans 3,000 state-month records to detect concurrent multi-pathogen outbreak events.",
        "Trigger Condition: Flags state-months where 2 or more distinct diseases simultaneously exceed baseline threshold.",
        "Interactive Sensitivity Slider: Allows health directors to adjust anomaly trigger threshold from 1.1x to 2.5x baseline.",
        "Early Warning Defense: Prevents dual-surge hospital gridlock when post-monsoon Dengue coincides with typhoid spikes."
    ],
    explain_text=(
        "What happens when two different diseases hit the same state at the same time? Hospitals face sudden collapse. "
        "To solve this, we engineered an automated concurrent outbreak surveillance algorithm. "
        "It establishes a 5-year monthly baseline for every state and disease. If two or more diseases simultaneously exceed "
        "1.5 times their normal baseline, our system immediately triggers a high-priority red alert. "
        "Directors can even adjust the sensitivity slider between 1.1x and 2.5x to fine-tune alert thresholds for their specific district."
    ),
    notes_text=(
        "When explaining this slide: Tell the teachers this addresses Operational Question OQ-08. "
        "Explain that simultaneous outbreaks (like Dengue + Typhoid in August) overwhelm diagnostic labs and hospital blood banks."
    )
)

# ==========================================
# SLIDE 10: Data Governance & 3NF Schema (UI-06)
# ==========================================
slide10 = prs.slides.add_slide(blank_layout)
add_content_slide(
    slide10,
    title="9. Data Cleaning Pipeline, Audit Ledger & 3NF Database",
    subtitle="Automated Sanitization (Duplicates, Imputation, Capping) & Relational SQLite Architecture",
    image_path="docs/screenshots/07_data_quality_ledger.png",
    bullets=[
        "Deterministic Python Cleaning Pipeline: Purged 149 duplicate entries, imputed 42 missing values, and capped 7 extreme outliers.",
        "Data Quality Ledger: Transparent scorecard accounts for every raw ingestion row (3,000 in ➔ 2,854 clean certified rows).",
        "Third Normal Form (3NF) Relational SQLite Schema: 5 base tables (region_master, disease_master, demographic_group, etc.).",
        "Analytical View v_disease_analysis: Materializes joined dimensions with precomputed metrics for sub-second query latency."
    ],
    explain_text=(
        "In healthcare analytics, raw data is often messy—hospital clerks make typing mistakes, servers drop duplicate rows, "
        "and fields are left empty. We built a deterministic data cleaning pipeline in Python that automatically detected and purged "
        "149 duplicate rows, filled missing values using disease medians, and capped extreme typing errors using the IQR method. "
        "The certified clean data is stored in a normalized Third Normal Form SQLite database, ensuring zero orphan records "
        "and total referential integrity."
    ),
    notes_text=(
        "When explaining this slide: Emphasize that 'Garbage in, Garbage out' is the #1 danger in medical AI and analytics. "
        "Showcase that our Data Quality Ledger provides 100% audit transparency for every record modified."
    )
)

# ==========================================
# SLIDE 11: 100% Automated Testing Suite (QA)
# ==========================================
slide11 = prs.slides.add_slide(blank_layout)
add_header(slide11, "10. Quality Assurance & 100% Automated Test Suite", "17 Comprehensive Verification Unit Tests Across Database Schema, Clinical Math & App Routes")

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
tp3.text = "🚀 App Smoke & Rigor\n(3 Tests — test_app.py)"
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
    "To ensure that our project meets professional software engineering standards, we built an automated test runner. "
    "By running 'python run_tests.py', all 17 unit tests execute in just 60 milliseconds with a 100% success rate, "
    "validating database referential integrity, clinical math formulas, and web page entry points."
)

# ==========================================
# SLIDE 12: BI Integration (Tableau & Power BI)
# ==========================================
slide12 = prs.slides.add_slide(blank_layout)
add_header(slide12, "11. Business Intelligence Integration: Tableau & Power BI", "Enterprise BI Architecture, DAX Measures, Calculated Fields & Merged Analytical Data Marts")

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
    "Beyond Python and Streamlit, we created complete enterprise BI specifications for Tableau and Power BI. "
    "We wrote production-ready DAX formulas, Tableau calculated fields, and exported clean CSV data marts so that "
    "any enterprise analytics team can deploy these exact dashboards in Power BI Service or Tableau Server."
)

# ==========================================
# SLIDE 13: 2-Minute Viva Pitch Cheat-Sheet
# ==========================================
slide13 = prs.slides.add_slide(blank_layout)
add_header(slide13, "12. How to Explain this Project in 2 Minutes (Viva Cheat-Sheet)", "A Simple 4-Step Conversational Talking Framework for Teachers, Examiners, and Fellow Students")

card_w = Inches(5.8)
card_h = Inches(2.55)

coords = [
    (Inches(0.6), Inches(1.45), "Step 1: The Healthcare Problem", "Healthcare departments in India often track diseases in disconnected paper registers or separate portals. This delays spotting outbreaks, wastes hospital resources, and costs lives. Our goal was to create one unified, interactive visual cockpit.", NAVY),
    (Inches(6.8), Inches(1.45), "Step 2: The Solution We Built", "We engineered a full-stack Python application using Streamlit, Plotly, and SQLite. It models 5 major diseases across 10 states over 5 years (3,000 monthly reports) with interactive filters, allowing sub-second visual exploration.", TEAL),
    (Inches(0.6), Inches(4.3), "Step 3: What the Data Revealed", "1. Dengue & Malaria peak strictly in July–October post-monsoon.\n2. Dense cities (Delhi, Maharashtra) suffer 4x higher infection speed (r = 0.96).\n3. Senior citizens (60+) face a 4x higher Case Fatality Rate (4.8% vs 1.1%).", EMERALD),
    (Inches(6.8), Inches(4.3), "Step 4: The Technical Rigor", "Built across 18 professional software engineering steps: formal BRD, TRD, 3NF database schema, user stories, automated unit test suite (17/17 passing), and deployed on Streamlit Community Cloud with full traceability.", SKY)
]

for left, top, ctitle, ctext, ccol in coords:
    scard = slide13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, card_w, card_h)
    scard.fill.solid()
    scard.fill.fore_color.rgb = WHITE
    scard.line.color.rgb = ccol
    scard.line.width = Pt(1.5)
    
    sctf = scard.text_frame
    sctf.word_wrap = True
    sctf.margin_left = sctf.margin_right = sctf.margin_top = sctf.margin_bottom = Inches(0.2)
    
    tp1 = sctf.paragraphs[0]
    tp1.text = ctitle
    tp1.font.name = "Segoe UI"
    tp1.font.size = Pt(13)
    tp1.font.bold = True
    tp1.font.color.rgb = ccol
    
    tp2 = sctf.add_paragraph()
    tp2.text = ctext
    tp2.font.name = "Segoe UI"
    tp2.font.size = Pt(10.2)
    tp2.font.color.rgb = SLATE_DARK
    tp2.space_before = Pt(6)

slide13.notes_slide.notes_text_frame.text = (
    "This slide is your 2-minute elevator pitch! Memorize the 4 steps: "
    "1. The Problem (delayed outbreak detection), "
    "2. The Tool (Python Streamlit cockpit), "
    "3. The Findings (monsoon vector peaks, urban crowding, senior vulnerability), "
    "4. The Technical Rigor (3NF database, 17/17 unit tests)."
)

# ==========================================
# SLIDE 14: Academic Deliverables & Submission
# ==========================================
slide14 = prs.slides.add_slide(blank_layout)
add_header(slide14, "13. Academic Deliverables & Official Submission Package", "All 18 Steps Executed, Documented, and Verified for ABES MCA Final Submission")

deliv_card = slide14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(1.45), Inches(12.133), Inches(5.45))
deliv_card.fill.solid()
deliv_card.fill.fore_color.rgb = WHITE
deliv_card.line.color.rgb = BORDER_COLOR
deliv_card.line.width = Pt(1.5)

dtf = deliv_card.text_frame
dtf.word_wrap = True
dtf.margin_left = dtf.margin_right = dtf.margin_top = dtf.margin_bottom = Inches(0.3)

dp1 = dtf.paragraphs[0]
dp1.text = "📦 Full Deliverable Package (Conforming to ABES Project Guidelines):"
dp1.font.name = "Segoe UI"
dp1.font.size = Pt(14)
dp1.font.bold = True
dp1.font.color.rgb = NAVY

items = [
    ("Requirements & Elicitation Specs (Steps 1–3, 5):", "01_Project_Understanding.docx/.pdf, 02_HMW_Statements.docx/.pdf, 03_Needs_Analysis.docx/.pdf, 05_BRD.docx/.pdf"),
    ("Bidirectional Traceability Matrix (Step 4):", "04_Traceability_Matrix.xlsx & 04_RTM.md (Maps 10 OQs to 15 BRs, DB columns, User Stories, UI Screens, and Test Cases)"),
    ("Technical Architecture & Schema (Steps 7–9):", "07_TRD.docx/.pdf, 08_Database_Design.xlsx (11 sheets), 09_ER_Diagram.docx/.pdf + High-Res PNG"),
    ("Agile Specifications & Wireframes (Steps 11–12):", "11_User_Stories.docx/.pdf (17 stories, 46 pts), 12_UI_Framework.docx/.pdf (Component wireframes, Tailwind styling)"),
    ("Quality Assurance & Deployment (Steps 13–16):", "13_Test_Cases.docx/.pdf (20 TC-F, 18 TC-T), 14_Build_Plan.docx/.pdf, 16_Deployment_Guide.docx/.pdf (Streamlit Cloud)"),
    ("Final Academic Report & Viva Deck (Steps 17–18):", "17_Project_Document.docx/.pdf (Full ABES Synthesis), 18_Presentation.docx/.pdf, 18_Presentation.pptx (This Slide Deck)"),
    ("Data Science & BI Deliverables (Step 19):", "EDA_Lesson_Notebook.ipynb (69 cells, fully executed), Tableau & Power BI Specs + DAX & Calculated Fields")
]

for label, desc in items:
    dip = dtf.add_paragraph()
    dip.text = f"• {label} "
    dip.font.name = "Segoe UI"
    dip.font.size = Pt(10.5)
    dip.font.bold = True
    dip.font.color.rgb = TEAL
    dip.space_before = Pt(5)
    
    run = dip.add_run()
    run.text = desc
    run.font.bold = False
    run.font.color.rgb = SLATE_DARK

slide14.notes_slide.notes_text_frame.text = (
    "To conclude: We completed every single one of the 18 steps from the kickoff instructions. "
    "We have formal Word documents, PDF versions, Excel workbooks, SQLite database files, clean modular Python source code, "
    "an executable Jupyter EDA notebook, and a complete test suite. Everything is archived and ready for academic submission. Thank you!"
)

# Save the presentation
output_pptx = Path("c:/Users/Hp/Downloads/hcl/docs/18_ArgJain_DiseaseTrendAnalysis_Presentation.pptx")
prs.save(str(output_pptx))
print(f"POWERPOINT PRESENTATION GENERATED SUCCESSFULLY: {output_pptx} ({output_pptx.stat().st_size // 1024} KB)")
