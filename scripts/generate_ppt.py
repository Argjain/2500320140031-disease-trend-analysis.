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

# Color Palette Definitions
NAVY = RGBColor(15, 43, 72)         # Primary Dark Navy #0F2B48
TEAL = RGBColor(26, 83, 118)        # Brand Teal #1A5376
SKY = RGBColor(2, 132, 199)         # Bright Sky Blue #0284C7
SLATE_DARK = RGBColor(30, 41, 59)   # Slate Charcoal #1E293B
SLATE_MUTED = RGBColor(100, 116, 139) # Muted Text #64748B
BG_LIGHT = RGBColor(248, 250, 252)  # Card Background #F8FAFC
BORDER_COLOR = RGBColor(226, 232, 240) # Card Border #E2E8F0
EMERALD = RGBColor(5, 150, 105)     # Success Green #059669
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
    header_box = slide.shapes.add_textbox(Inches(0.6), Inches(0.4), Inches(12.133), Inches(0.9))
    tf = header_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    p_title = tf.paragraphs[0]
    p_title.text = title_text
    p_title.font.name = "Segoe UI"
    p_title.font.size = Pt(22)
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
    """Creates a structured two-column presentation slide with image, bullets, and explanation."""
    add_header(slide, title, subtitle)
    
    # Left Column: Screenshot Image
    img_left = Inches(0.6)
    img_top = Inches(1.5)
    img_width = Inches(6.4)
    img_height = Inches(5.3)
    
    resolved_img = resolve_path(image_path) if image_path else None
    if resolved_img and resolved_img.exists():
        # Add background frame for the image
        frame = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, img_left - Inches(0.05), img_top - Inches(0.05), img_width + Inches(0.1), img_height + Inches(0.1))
        frame.fill.solid()
        frame.fill.fore_color.rgb = WHITE
        frame.line.color.rgb = BORDER_COLOR
        frame.line.width = Pt(1.5)
        
        slide.shapes.add_picture(str(resolved_img), img_left, img_top, width=img_width, height=img_height)
    
    # Right Column: Explanation & Key Points
    right_left = Inches(7.3)
    right_top = Inches(1.5)
    right_width = Inches(5.4)
    
    # 1. Key Highlights Card
    h_box = slide.shapes.add_textbox(right_left, right_top, right_width, Inches(2.3))
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
        bp.font.size = Pt(11)
        bp.font.color.rgb = SLATE_DARK
        bp.space_before = Pt(4)
        
    # 2. Easy Spoken Explanation Card (Normal Language Paragraph)
    card_top = Inches(4.0)
    card_height = Inches(2.8)
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
    cp2.font.size = Pt(10.5)
    cp2.font.color.rgb = SLATE_DARK
    cp2.space_before = Pt(5)
    
    # Add Speaker Notes
    notes_slide = slide.notes_slide
    notes_slide.notes_text_frame.text = notes_text

# ==========================================
# SLIDE 1: Title Slide (Grand Cover)
# ==========================================
slide1 = prs.slides.add_slide(blank_layout)

# Background Accent Box
bg = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(4.5))
bg.fill.solid()
bg.fill.fore_color.rgb = NAVY
bg.line.fill.background()

# Title text
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
p3.text = "Project ID: P-01 | Domain: Healthcare Data Analytics | Technology Stack: Python, Streamlit, SQLite, Plotly"
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
p_cand.text = "Student / Developer: Arg Jain (Roll No. 2500320140031)"
p_cand.font.name = "Segoe UI"
p_cand.font.size = Pt(14)
p_cand.font.bold = True
p_cand.font.color.rgb = NAVY

p_dept = ctf1.add_paragraph()
p_dept.text = "MCA 2nd Year — Data Analytics Specialization | ABES Engineering College, Ghaziabad"
p_dept.font.name = "Segoe UI"
p_dept.font.size = Pt(12)
p_dept.font.color.rgb = SLATE_DARK
p_dept.space_before = Pt(4)

p_ment = ctf1.add_paragraph()
p_ment.text = "Faculty Mentor: Ms. Kalpana Dwivedi | Target Release: December 2026"
p_ment.font.name = "Segoe UI"
p_ment.font.size = Pt(12)
p_ment.font.bold = True
p_ment.font.color.rgb = TEAL
p_ment.space_before = Pt(4)

slide1.notes_slide.notes_text_frame.text = (
    "Good morning respected teachers and fellow students. My name is Arg Jain, Roll Number 2500320140031, "
    "from MCA 2nd Year Data Analytics at ABES Engineering College. Under the mentorship of Ms. Kalpana Dwivedi, "
    "I have developed an end-to-end data analytics project called Disease Trend Analysis Intelligence Cockpit. "
    "Today, I will walk you through the real-world problem we solved, our live web application, and the major healthcare findings we discovered."
)

# ==========================================
# SLIDE 2: Executive Surveillance Cockpit (UI-01)
# ==========================================
slide2 = prs.slides.add_slide(blank_layout)
add_content_slide(
    slide2,
    title="1. Executive Surveillance Cockpit & Key Health Metrics",
    subtitle="Overview Dashboard | Live Morbidity, Fatalities, Recoveries & Active Caseload Across India",
    image_path="docs/screenshots/01_cockpit_kpis.png",
    bullets=[
        "Monitors 5 major diseases: Dengue, Malaria, Tuberculosis, COVID-19, and Typhoid.",
        "Tracks 10 representative Indian states over a 5-year timeline (2020 to 2024, 60 months).",
        "4 live KPI stat cards calculate Morbidity (1.67M), Deaths (43.5k), Recoveries (1.51M), and Active Cases (128k).",
        "Interactive sidebar lets the user filter by any disease, state, or year range with instant recalculation."
    ],
    explain_text=(
        "Teachers and students, what you are looking at is the main dashboard of our web application. "
        "Imagine you are a Public Health Officer managing disease spread across India. Instead of digging through "
        "spreadsheets, this cockpit immediately shows you the big picture: how many people got infected, how many passed away, "
        "and our current 90.4% clinical recovery rate. Using the sidebar on the left, you can filter for any specific state like Uttar Pradesh "
        "or disease like Dengue, and all the cards recalculate instantly."
    ),
    notes_text=(
        "When explaining this slide: Point to the 4 KPI cards at the top. Mention that these cards update in real-time "
        "based on the filters selected in the left sidebar. State that this answers Operational Question 1 (overall trend) "
        "and gives decision-makers immediate situational awareness."
    )
)

# ==========================================
# SLIDE 3: State-Level Disease Burden Ranking (UI-01)
# ==========================================
slide3 = prs.slides.add_slide(blank_layout)
add_content_slide(
    slide3,
    title="2. State-Level Morbidity Burden & Performance Benchmarking",
    subtitle="Regional Case Volume Ranking & Cross-State Case Fatality Rate (CFR %) Comparison",
    image_path="docs/screenshots/02_overview_state_burden.png",
    bullets=[
        "Horizontal bar chart ranks all 10 states by total incident caseload (Maharashtra and Delhi lead).",
        "Data table benchmarks Case Fatality Rate (CFR %) and recovery percentages side by side.",
        "Color-coded gradients highlight high-risk mortality zones in red and high-recovery zones in green.",
        "Answers Operational Questions OQ-02 (State Burden) and OQ-05 (CFR benchmarking)."
    ],
    explain_text=(
        "In this second screen, we answer a critical question: Which states are carrying the heaviest disease load? "
        "As you can see in the bar chart, states with dense urban centers like Maharashtra and Delhi have the highest total cases. "
        "Right below it, our performance table compares the Case Fatality Rate (CFR) across states. This tells health ministers "
        "not just where the most cases are, but which states are having difficulty managing severe cases so that medical supplies, "
        "oxygen, and emergency staff can be sent there immediately."
    ),
    notes_text=(
        "When explaining this slide: Emphasize that total cases alone don't tell the full story; Case Fatality Rate (CFR) "
        "shows the severity. Point out that color gradients make it easy for doctors and officials to spot high-risk states in seconds."
    )
)

# ==========================================
# SLIDE 4: Longitudinal Trends & Seasonality (UI-02)
# ==========================================
slide4 = prs.slides.add_slide(blank_layout)
add_content_slide(
    slide4,
    title="3. 60-Month Disease Transmission Trends & Seasonal Heatmap",
    subtitle="Tracking Longitudinal Waves (2020–2024) & Cyclical Monsoon vs Winter Outbreak Spikes",
    image_path="docs/screenshots/03_trends_seasonal_heatmap.png",
    bullets=[
        "Continuous 60-month time-series line chart tracks transmission waves for each of the 5 diseases.",
        "Year-over-Year (YoY %) Annual Delta table tracks percentage growth or decline across calendar years.",
        "12-Month Seasonal Intensity Heatmap reveals recurring cyclic peaks across months (January to December).",
        "Clinical Discovery: Vector-borne diseases (Dengue & Malaria) reliably surge in post-monsoon July–October."
    ],
    explain_text=(
        "This is one of the most powerful analytical screens in our project. Diseases do not happen randomly; they follow seasons. "
        "The line chart tracks monthly cases from 2020 to 2024. But look at the seasonal heatmap at the bottom: "
        "it clearly proves that mosquito-borne diseases like Dengue and Malaria peak every year between July and October after the monsoon rains. "
        "Conversely, respiratory illnesses like COVID-19 and Tuberculosis spike in winter (December to February). "
        "By knowing this 60 days in advance, hospitals can stock test kits and medicines before the surge hits."
    ),
    notes_text=(
        "When explaining this slide: Highlight the word 'Predictive Preparation'. Explain to teachers that vector diseases "
        "depend on standing water from monsoons, while winter promotes respiratory transmission. This proves data analytics directly saves lives."
    )
)

# ==========================================
# SLIDE 5: Urban Density Correlation & Outbreak Anomaly (UI-05)
# ==========================================
slide5 = prs.slides.add_slide(blank_layout)
add_content_slide(
    slide5,
    title="4. Urban Density Correlation & Outbreak Anomaly Detection",
    subtitle="Statistical Pearson Correlation (r = 0.96) & Automated Concurrent Multi-Disease Surveillance",
    image_path="docs/screenshots/04_eda_density_scatter.png",
    bullets=[
        "Scatter plot correlates Population Density (persons/km²) against Incidence per 100,000 residents.",
        "Statistical Proof: Pearson r = 0.9606 (p = 0.0001) proves urban crowding dramatically accelerates contagion.",
        "Non-colliding directional pointer badges clearly label every Indian state without text overlap.",
        "Automated Anomaly Detector: Flags any state-month where 2+ diseases exceed 1.5x of their historical baseline."
    ],
    explain_text=(
        "Here we conducted deep statistical modeling. We wanted to answer: Does urban crowding cause faster disease spread? "
        "We calculated the Pearson correlation coefficient between population density and disease incidence. The result was r = 0.96, "
        "which is a very strong, statistically verified positive relationship. You can see Delhi at the top-right outlier position. "
        "We also built an automated anomaly detector that scans the entire database and automatically sounds an alarm if two different "
        "diseases surge at the same time in the same state, preventing hospital system collapse."
    ),
    notes_text=(
        "When explaining this slide: Point out the callout arrows and badges showing each state cleanly. "
        "Explain that r = 0.96 means crowding strongly drives infection rates. Mention the 1.5x outbreak threshold algorithm."
    )
)

# ==========================================
# SLIDE 6: Data Quality Ledger & 3NF Database Design
# ==========================================
slide6 = prs.slides.add_slide(blank_layout)
add_content_slide(
    slide6,
    title="5. Data Quality Ledger, Cleaning Pipeline & SQLite Database",
    subtitle="Sanitization Accounting (Duplicates, Imputation, Outliers) & Third Normal Form (3NF) Architecture",
    image_path="docs/screenshots/06_database_er_diagram.png",
    bullets=[
        "In-pipeline data cleaning: Purges duplicate reports, imputes nulls with medians, and caps typographic entry spikes.",
        "Data Quality Ledger: Transparent scorecard accounting for every record cleaned before analysis.",
        "Third Normal Form (3NF) SQLite schema: 5 base tables (region_master, disease_master, demographic_group, etc.).",
        "Analytical View v_disease_analysis: Materializes joined dimensions with precomputed metrics for sub-second speed."
    ],
    explain_text=(
        "In real life, hospital data is dirty—staff make typo mistakes, duplicate entries occur, and some records have missing numbers. "
        "We built a deterministic data cleaning pipeline in Python that purges duplicates, fills missing values using medians, "
        "and caps extreme typing errors. The clean records are stored in a normalized Third Normal Form SQLite database. "
        "The diagram on the left shows our schema: separate master tables for states, diseases, and demographics linked to our central fact tables. "
        "This guarantees 100% data integrity and zero orphan records."
    ),
    notes_text=(
        "When explaining this slide: Explain why we don't just use one giant Excel sheet. Normalization into 3NF prevents redundant data, "
        "saves disk space, and enforces relational integrity via SQLite foreign key constraints."
    )
)

# ==========================================
# SLIDE 7: Quality Assurance & 100% Automated Testing
# ==========================================
slide7 = prs.slides.add_slide(blank_layout)
add_content_slide(
    slide7,
    title="6. Quality Assurance & 100% Automated Testing Suite",
    subtitle="Full Unit Verification Across Schema Integrity, Clinical Math Formulas, and App Routes",
    image_path="docs/screenshots/05_data_quality_ledger.png",
    bullets=[
        "17 Automated Pytest / Unittest test cases executed via zero-dependency runner (python run_tests.py).",
        "Schema Integrity (TC-T-01..08): Verifies 5 base tables, 0 orphan foreign keys, clinical bounds (deaths <= cases).",
        "Mathematical Formulations (TC-T-09..14): Validates CFR (5.0%), Recovery Rate (92.0%), YoY delta, and Pearson r.",
        "App Smoke Tests (TC-T-16..18): Ensures all 6 multi-page scripts, modular src/ files, and configs exist.",
        "100% Test Success Rate: All 17 tests execute and pass in under 0.10 seconds."
    ],
    explain_text=(
        "To ensure that our teachers, mentors, and examiners can completely trust our project, we wrote 17 automated tests. "
        "When we run our test suite, Python automatically checks that our database tables exist, that no broken foreign keys exist, "
        "and that every mathematical calculation—like Case Fatality Rate and recovery percentage—gives the exact right answer. "
        "Every single test passes with a 100% success rate in less than one-tenth of a second."
    ),
    notes_text=(
        "When explaining this slide: Tell the teachers that software testing is what separates amateur student projects from "
        "professional IT systems. Mention that running 'python run_tests.py' verifies all 17 tests instantly."
    )
)

# ==========================================
# SLIDE 8: How to Explain this Project (Cheat-Sheet)
# ==========================================
slide8 = prs.slides.add_slide(blank_layout)
add_header(slide8, "7. How to Explain this Project in 2 Minutes (Cheat-Sheet)", "A Simple Step-by-Step Talking Guide for Teachers, Viva Examiners, and Students")

# 4 Talking Point Cards
card_w = Inches(5.8)
card_h = Inches(2.5)

coords = [
    (Inches(0.6), Inches(1.5), "Step 1: The Healthcare Problem", "Healthcare departments in India often track diseases in disconnected paper registers or separate portals. This delays spotting outbreaks, wastes hospital resources, and costs lives. Our goal was to create one unified, interactive visual cockpit.", NAVY),
    (Inches(6.8), Inches(1.5), "Step 2: The Solution We Built", "We engineered a full-stack Python application using Streamlit, Plotly, and SQLite. It models 5 major diseases across 10 states over 5 years (3,000 monthly reports) with interactive filters, allowing sub-second visual exploration.", TEAL),
    (Inches(0.6), Inches(4.3), "Step 3: What the Data Revealed", "1. Dengue & Malaria peak strictly in July–October post-monsoon.\n2. Dense cities (Delhi, Maharashtra) suffer 4x higher infection speed (r = 0.96).\n3. Senior citizens (60+) face a 3x higher Case Fatality Rate (5.5% vs 1.5%).", EMERALD),
    (Inches(6.8), Inches(4.3), "Step 4: The Technical Rigor", "Built across 18 professional software engineering steps: formal BRD, TRD, 3NF database schema, user stories, automated unit test suite (17/17 passing), and deployed on Streamlit Community Cloud with full traceability.", SKY)
]

for left, top, ctitle, ctext, ccol in coords:
    scard = slide8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, card_w, card_h)
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
    tp2.font.size = Pt(10.5)
    tp2.font.color.rgb = SLATE_DARK
    tp2.space_before = Pt(6)

slide8.notes_slide.notes_text_frame.text = (
    "This slide is your 2-minute elevator pitch! Memorize the 4 steps: "
    "1. The Problem (delayed outbreak detection), "
    "2. The Tool (Python Streamlit cockpit), "
    "3. The Findings (monsoon vector peaks, urban crowding, senior vulnerability), "
    "4. The Technical Rigor (3NF database, 17/17 unit tests)."
)

# ==========================================
# SLIDE 9: Project Deliverables & Submission Summary
# ==========================================
slide9 = prs.slides.add_slide(blank_layout)
add_header(slide9, "8. Academic Deliverables & Official Submission Summary", "All 18 Steps Executed, Documented, and Verified for ABES MCA Final Submission")

deliv_card = slide9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(1.5), Inches(12.133), Inches(5.3))
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
    ("Business & Requirements Specs:", "01_Project_Understanding.docx, 02_HMW_Statements.docx, 03_Needs_Analysis.docx, 05_BRD.docx"),
    ("Bidirectional Traceability Matrix:", "04_Traceability_Matrix.xlsx (Maps 10 OQs to 15 BRs, DB columns, User Stories, UI Screens, and Test Cases)"),
    ("Technical Architecture & Schema:", "07_TRD.docx, 08_Database_Design.xlsx (11 sheets), 09_ER_Diagram.docx + High-Res PNG"),
    ("Agile Specifications & Wireframes:", "11_User_Stories.docx (17 stories, 46 pts), 12_UI_Framework.docx (ASCII wireframes, Tailwind styling)"),
    ("Quality Assurance & Deployment:", "13_Test_Cases.docx (20 TC-F, 18 TC-T), 14_Build_Plan.docx, 16_Deployment_Guide.docx (Streamlit Cloud)"),
    ("Final Academic Report & Viva Deck:", "17_Project_Document.docx (Full ABES Project Template Synthesis), 18_Presentation.pptx (This Slide Deck)")
]

for label, desc in items:
    dip = dtf.add_paragraph()
    dip.text = f"• {label} "
    dip.font.name = "Segoe UI"
    dip.font.size = Pt(11)
    dip.font.bold = True
    dip.font.color.rgb = TEAL
    dip.space_before = Pt(6)
    
    run = dip.add_run()
    run.text = desc
    run.font.bold = False
    run.font.color.rgb = SLATE_DARK

slide9.notes_slide.notes_text_frame.text = (
    "To conclude: We completed every single one of the 18 steps from the kickoff instructions. "
    "We have formal Word documents, Excel workbooks, SQLite database files, clean modular Python source code, "
    "and a complete test suite. Everything is archived and ready for academic submission. Thank you!"
)

# Save the presentation
output_pptx = Path("c:/Users/Hp/Downloads/hcl/docs/18_ArgJain_DiseaseTrendAnalysis_Presentation.pptx")
prs.save(str(output_pptx))
print(f"POWERPOINT PRESENTATION GENERATED SUCCESSFULLY: {output_pptx} ({output_pptx.stat().st_size // 1024} KB)")
