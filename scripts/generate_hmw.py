"""
STEP 2 – How Might We (HMW) Statements Document Generator
Project: Disease Trend Analysis | P100
Student: Arg Jain | Roll: 2500320140031
"""

import os
from docx import Document
from docx.shared import Pt, Cm, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import copy

# ── colour constants ──────────────────────────────────────────────────────────
C_HEADING   = RGBColor(26, 83, 118)   # #1A5376
C_TH_BG     = "1A5376"               # table header bg
C_ALT1      = "EBF5FB"               # row alt 1
C_ALT2      = "FFFFFF"               # row alt 2
C_PRIORITY  = "FEF9E7"               # priority row
C_FOOTER    = RGBColor(127, 127, 127) # grey

# ── helpers ───────────────────────────────────────────────────────────────────
def set_cell_bg(cell, hex_color):
    """Set table cell background shading."""
    tc   = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd  = OxmlElement("w:shd")
    shd.set(qn("w:val"),   "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"),  hex_color)
    tcPr.append(shd)

def set_cell_margins(cell, top=60, start=80, bottom=60, end=80):
    tc   = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcMar = OxmlElement("w:tcMar")
    for side, val in [("top", top), ("start", start), ("bottom", bottom), ("end", end)]:
        node = OxmlElement(f"w:{side}")
        node.set(qn("w:w"),    str(val))
        node.set(qn("w:type"), "dxa")
        tcMar.append(node)
    tcPr.append(tcMar)

def cell_text(cell, text, bold=False, font_size=9, color=None,
              align=WD_ALIGN_PARAGRAPH.LEFT, italic=False):
    """Clear a cell and add styled text."""
    cell.text = ""
    para = cell.paragraphs[0]
    para.alignment = align
    run  = para.add_run(str(text))
    run.bold   = bold
    run.italic = italic
    run.font.name = "Calibri"
    run.font.size = Pt(font_size)
    if color:
        run.font.color.rgb = color

def set_col_widths(table, widths_cm):
    for row in table.rows:
        for i, cell in enumerate(row.cells):
            if i < len(widths_cm):
                cell.width = Cm(widths_cm[i])

def add_header_row(table, headers, widths_cm=None):
    """Style first row as dark-blue header."""
    row = table.rows[0]
    for i, hdr in enumerate(headers):
        cell = row.cells[i]
        set_cell_bg(cell, C_TH_BG)
        set_cell_margins(cell)
        cell_text(cell, hdr, bold=True, font_size=9,
                  color=RGBColor(255, 255, 255), align=WD_ALIGN_PARAGRAPH.CENTER)
    if widths_cm:
        set_col_widths(table, widths_cm)

def style_data_row(row, is_priority=False, alt=False):
    """Apply alternating or priority row colour."""
    bg = C_PRIORITY if is_priority else (C_ALT1 if alt else C_ALT2)
    for cell in row.cells:
        set_cell_bg(cell, bg)
        set_cell_margins(cell)

def add_section_heading(doc, text, level=1):
    para = doc.add_paragraph()
    para.paragraph_format.space_before = Pt(14)
    para.paragraph_format.space_after  = Pt(4)
    run  = para.add_run(text)
    run.bold = True
    run.font.name  = "Calibri"
    run.font.size  = Pt(13 if level == 1 else 11)
    run.font.color.rgb = C_HEADING
    return para

def add_body_para(doc, text, size=10):
    para = doc.add_paragraph()
    run  = para.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(size)
    para.paragraph_format.space_after = Pt(4)
    return para

def set_page_margins(doc):
    for section in doc.sections:
        section.top_margin    = Cm(2.5)
        section.bottom_margin = Cm(2.5)
        section.left_margin   = Cm(3.0)
        section.right_margin  = Cm(2.0)

def add_footer(doc):
    section  = doc.sections[0]
    footer   = section.footer
    para     = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    para.clear()
    run = para.add_run(
        "02_ArgJain_DiseaseTrendAnalysis_HMWStatements.docx  |  Version 1.0  "
        "|  November 2026  |  ABES Engineering College"
    )
    run.font.name  = "Calibri"
    run.font.size  = Pt(8)
    run.font.color.rgb = C_FOOTER

def add_thin_border_table(doc, rows, cols):
    table = doc.add_table(rows=rows, cols=cols)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = "Table Grid"
    return table

# ── document build ─────────────────────────────────────────────────────────────
def build_document():
    doc = Document()
    set_page_margins(doc)

    # ── default style ──────────────────────────────────────────────────────────
    style = doc.styles["Normal"]
    style.font.name = "Calibri"
    style.font.size = Pt(10)

    # ══════════════════════════════════════════════════════════════════════════
    # COVER BLOCK
    # ══════════════════════════════════════════════════════════════════════════
    # top decorative line
    top_line = doc.add_paragraph()
    top_line.paragraph_format.space_before = Pt(0)
    top_line.paragraph_format.space_after  = Pt(6)
    run = top_line.add_run("━" * 72)
    run.font.color.rgb = C_HEADING
    run.font.size      = Pt(10)
    top_line.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # main title
    t = doc.add_paragraph()
    t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    t.paragraph_format.space_before = Pt(2)
    t.paragraph_format.space_after  = Pt(2)
    r = t.add_run("DISEASE TREND ANALYSIS")
    r.bold = True
    r.font.name  = "Calibri"
    r.font.size  = Pt(22)
    r.font.color.rgb = C_HEADING

    # subtitle
    sub = doc.add_paragraph()
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sub.paragraph_format.space_before = Pt(0)
    sub.paragraph_format.space_after  = Pt(2)
    rs = sub.add_run("STEP 2 – How Might We (HMW) Statements")
    rs.bold = True
    rs.font.name  = "Calibri"
    rs.font.size  = Pt(14)
    rs.font.color.rgb = C_HEADING

    # bottom decorative line
    bot_line = doc.add_paragraph()
    bot_line.alignment = WD_ALIGN_PARAGRAPH.CENTER
    bot_line.paragraph_format.space_before = Pt(2)
    bot_line.paragraph_format.space_after  = Pt(10)
    run2 = bot_line.add_run("━" * 72)
    run2.font.color.rgb = C_HEADING
    run2.font.size      = Pt(10)

    # meta table (2 col)
    meta = [
        ("Project ID",    "P100"),
        ("Student",       "Arg Jain"),
        ("Roll Number",   "2500320140031"),
        ("Course",        "MCA 2nd Year – Data Analytics"),
        ("Institute",     "ABES Engineering College"),
        ("Mentor",        "Mr. Dinesh"),
        ("Date",          "November 2026"),
    ]
    mt = doc.add_table(rows=len(meta), cols=2)
    mt.alignment = WD_TABLE_ALIGNMENT.CENTER
    mt.style = "Table Grid"
    for i, (k, v) in enumerate(meta):
        bg = C_ALT1 if i % 2 == 0 else C_ALT2
        set_cell_bg(mt.rows[i].cells[0], bg)
        set_cell_bg(mt.rows[i].cells[1], bg)
        set_cell_margins(mt.rows[i].cells[0])
        set_cell_margins(mt.rows[i].cells[1])
        cell_text(mt.rows[i].cells[0], k, bold=True, font_size=9.5)
        cell_text(mt.rows[i].cells[1], v, font_size=9.5)
    for row in mt.rows:
        row.cells[0].width = Cm(5)
        row.cells[1].width = Cm(9)

    doc.add_paragraph().paragraph_format.space_after = Pt(2)

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 1 – STAKEHOLDER PAIN POINTS
    # ══════════════════════════════════════════════════════════════════════════
    add_section_heading(doc, "Section 1 – Stakeholder Pain Points")
    add_body_para(doc,
        "The following pain points were elicited through stakeholder interviews and "
        "domain analysis. Each stakeholder's operational frustrations directly drive "
        "the HMW framing in Section 2.", size=9.5)

    sp_headers = ["SH ID", "Stakeholder", "Pain Point 1", "Pain Point 2", "Pain Point 3"]
    sp_data = [
        ("SH-01", "Public Health Officer",
         "No single dashboard shows real-time district/state disease spikes",
         "Outbreak alerts arrive days late; pattern recognition is manual",
         "Co-occurring outbreaks are invisible until strain on clinics is severe"),
        ("SH-02", "Hospital Administrator",
         "Bed and staff planning is reactive – surge data arrives post-crisis",
         "Recovery vs fatality benchmarks are not visible across peer hospitals",
         "Seasonal admission spikes cause resource shortages every year"),
        ("SH-03", "Policy Maker / Ministry",
         "CFR data is scattered across state PDFs; cross-regional comparison impossible",
         "No year-over-year summary to redirect budgets to rising-disease states",
         "Funding decisions rely on anecdotal reports rather than trend evidence"),
        ("SH-04", "Epidemiologist / Researcher",
         "No drill-down by age group or gender to pinpoint vulnerable demographics",
         "Population-density vs incidence correlation requires manual GIS work",
         "Seasonal pattern analysis across 5 diseases needs custom scripting each cycle"),
    ]

    sp_widths = [1.6, 3.2, 4.0, 4.0, 4.0]
    sp_table = add_thin_border_table(doc, len(sp_data) + 1, 5)
    add_header_row(sp_table, sp_headers, sp_widths)

    for i, row_data in enumerate(sp_data):
        row = sp_table.rows[i + 1]
        style_data_row(row, alt=(i % 2 == 0))
        for j, val in enumerate(row_data):
            cell_text(row.cells[j], val, font_size=8.5)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 2 – HMW STATEMENTS TABLE
    # ══════════════════════════════════════════════════════════════════════════
    add_section_heading(doc, "Section 2 – How Might We (HMW) Statements")
    add_body_para(doc,
        "Ten HMW statements were synthesised from stakeholder pain points and "
        "linked to the ten Organisational Questions (OQ-01 … OQ-10). The top five "
        "are marked PRIORITY and form the core scope of the system.", size=9.5)

    hmw_headers = ["HMW ID", "How Might We…?", "Stakeholder(s)", "Pain Point Addressed",
                   "Linked OQ(s)", "Priority"]
    hmw_data = [
        # (id, statement, sh, pain, oqs, priority)
        ("HMW-01",
         "How might we help public health officers instantly spot which disease is "
         "spiking in a specific region this month vs last year?",
         "SH-01", "No unified real-time trend view", "OQ-01, OQ-09", True),
        ("HMW-02",
         "How might we show hospital administrators which states will face a patient "
         "surge next season so they can pre-allocate beds?",
         "SH-02", "Reactive not proactive planning", "OQ-02, OQ-03", True),
        ("HMW-03",
         "How might we help policy makers compare case fatality rates across regions "
         "in a single glance to justify targeted budget allocations?",
         "SH-03", "Data scattered across reports", "OQ-05, OQ-02", True),
        ("HMW-04",
         "How might we enable epidemiologists to filter disease data by age group and "
         "gender to identify the most vulnerable demographic segments?",
         "SH-04", "No demographic drill-down", "OQ-04", True),
        ("HMW-05",
         "How might we surface co-occurring disease outbreaks in the same region-time "
         "window to alert response teams before crises escalate?",
         "SH-01, SH-04", "Outbreaks treated in isolation", "OQ-08", True),
        ("HMW-06",
         "How might we visualise seasonal disease peaks across all diseases on one "
         "chart so analysts can prepare resources months in advance?",
         "SH-01, SH-04", "Seasonal patterns buried", "OQ-10, OQ-03", False),
        ("HMW-07",
         "How might we display recovery rates alongside fatality rates per region so "
         "administrators can benchmark their hospitals against peer states?",
         "SH-02", "Recovery data not compared", "OQ-07, OQ-05", False),
        ("HMW-08",
         "How might we show the correlation between population density and disease "
         "incidence on a scatter chart so researchers can prioritise dense urban zones?",
         "SH-04", "No spatial-incidence link", "OQ-06", False),
        ("HMW-09",
         "How might we provide a year-over-year trend table that highlights which "
         "diseases are growing vs declining so ministers can redirect funds quickly?",
         "SH-03", "No YoY summary", "OQ-09, OQ-01", False),
        ("HMW-10",
         "How might we give analysts a clean downloadable dataset with a data quality "
         "summary so they can demonstrate rigorous EDA methodology?",
         "SH-05", "No exportable clean data view", "OQ-01..OQ-10", False),
    ]

    hmw_widths = [1.5, 5.8, 1.8, 3.0, 2.0, 1.5]
    hmw_table  = add_thin_border_table(doc, len(hmw_data) + 1, 6)
    add_header_row(hmw_table, hmw_headers, hmw_widths)

    for i, (hid, stmt, sh, pain, oqs, priority) in enumerate(hmw_data):
        row = hmw_table.rows[i + 1]
        style_data_row(row, is_priority=priority, alt=(i % 2 == 0))
        cell_text(row.cells[0], hid,  bold=True,  font_size=8.5)
        cell_text(row.cells[1], stmt,              font_size=8.5)
        cell_text(row.cells[2], sh,                font_size=8.5)
        cell_text(row.cells[3], pain,              font_size=8.5)
        cell_text(row.cells[4], oqs,               font_size=8.5, align=WD_ALIGN_PARAGRAPH.CENTER)
        p_label = "✔ PRIORITY" if priority else "—"
        cell_text(row.cells[5], p_label, bold=priority, font_size=8.5,
                  color=RGBColor(26, 83, 118) if priority else None,
                  align=WD_ALIGN_PARAGRAPH.CENTER)

    # legend note
    leg = doc.add_paragraph()
    leg.paragraph_format.space_before = Pt(4)
    leg.paragraph_format.space_after  = Pt(4)
    lr = leg.add_run(
        "Legend:  Rows shaded in yellow (#FEF9E7) = PRIORITY HMW (core system scope).  "
        "Rows in blue-tint (#EBF5FB) or white = secondary HMW (stretch goals)."
    )
    lr.font.name   = "Calibri"
    lr.font.size   = Pt(8.5)
    lr.font.italic = True
    lr.font.color.rgb = RGBColor(80, 80, 80)

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 3 – PRIORITY HMW JUSTIFICATIONS
    # ══════════════════════════════════════════════════════════════════════════
    add_section_heading(doc, "Section 3 – Priority HMW Justifications")
    add_body_para(doc,
        "The five PRIORITY HMWs were selected because they address the highest-severity "
        "pain points of the highest-priority stakeholders (SH-01 H, SH-02 H, SH-03 H) "
        "and together cover the broadest slice of the OQs.", size=9.5)

    pj_headers = ["HMW ID", "Priority Justification"]
    pj_data = [
        ("HMW-01",
         "Real-time regional spike detection is the #1 public-health-officer need; "
         "without it, outbreak response is delayed and lives are at risk (OQ-01, OQ-09)."),
        ("HMW-02",
         "Proactive seasonal surge prediction directly prevents hospital resource crises; "
         "highest operational impact for SH-02 administrators (OQ-02, OQ-03)."),
        ("HMW-03",
         "CFR comparison across regions in one view empowers evidence-based policy funding "
         "decisions—currently impossible without this dashboard (OQ-05, OQ-02)."),
        ("HMW-04",
         "Demographic filtering (age/gender) is fundamental to epidemiological investigation; "
         "missing this makes the system non-viable for SH-04 researchers (OQ-04)."),
        ("HMW-05",
         "Concurrent outbreak detection prevents compounding crises; no existing tool "
         "provides this multi-disease, single-region-window view (OQ-08)."),
    ]

    pj_widths = [1.8, 14.5]
    pj_table  = add_thin_border_table(doc, len(pj_data) + 1, 2)
    add_header_row(pj_table, pj_headers, pj_widths)

    for i, (hid, reason) in enumerate(pj_data):
        row = pj_table.rows[i + 1]
        style_data_row(row, is_priority=True)
        cell_text(row.cells[0], hid,    bold=True, font_size=9)
        cell_text(row.cells[1], reason, font_size=9)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 4 – OQ COVERAGE CHECK
    # ══════════════════════════════════════════════════════════════════════════
    add_section_heading(doc, "Section 4 – OQ Coverage Check")
    add_body_para(doc,
        "Every Organisational Question (OQ-01 … OQ-10) must be traceable to at least "
        "one HMW statement. The table below verifies full coverage.", size=9.5)

    oq_headers = ["OQ ID", "Organisational Question (summary)", "Covered by HMW(s)"]
    oq_data = [
        ("OQ-01", "Which diseases have shown highest case increase over 5 years?",
         "HMW-01, HMW-09, HMW-10"),
        ("OQ-02", "Which regions are most affected by each disease?",
         "HMW-02, HMW-03"),
        ("OQ-03", "What is the monthly/seasonal trend of disease outbreaks?",
         "HMW-02, HMW-06"),
        ("OQ-04", "Which age group/gender are most vulnerable?",
         "HMW-04"),
        ("OQ-05", "What is the case fatality rate per disease per region?",
         "HMW-03, HMW-07"),
        ("OQ-06", "How does incidence correlate with population density?",
         "HMW-08"),
        ("OQ-07", "Which diseases have highest recovery rates, and where?",
         "HMW-07"),
        ("OQ-08", "Are there concurrent outbreaks in any region?",
         "HMW-05"),
        ("OQ-09", "What is year-over-year change in cases per disease?",
         "HMW-01, HMW-09"),
        ("OQ-10", "Which months see peak disease reporting by disease type?",
         "HMW-06"),
    ]

    oq_widths = [1.6, 8.5, 6.2]
    oq_table  = add_thin_border_table(doc, len(oq_data) + 1, 3)
    add_header_row(oq_table, oq_headers, oq_widths)

    for i, (oqid, question, hmws) in enumerate(oq_data):
        row = oq_table.rows[i + 1]
        style_data_row(row, alt=(i % 2 == 0))
        cell_text(row.cells[0], oqid,     bold=True, font_size=9)
        cell_text(row.cells[1], question, font_size=9)
        cell_text(row.cells[2], hmws,     font_size=9, color=C_HEADING, bold=True)

    # footer note
    fn = doc.add_paragraph()
    fn.paragraph_format.space_before = Pt(6)
    fn.paragraph_format.space_after  = Pt(4)
    fn_run = fn.add_run(
        "✔ Coverage Confirmed: All 10 Organisational Questions (OQ-01 … OQ-10) are "
        "addressed by at least one HMW statement. No gap identified."
    )
    fn_run.bold = True
    fn_run.font.name  = "Calibri"
    fn_run.font.size  = Pt(9)
    fn_run.font.color.rgb = RGBColor(26, 83, 118)

    # ── document footer ────────────────────────────────────────────────────────
    add_footer(doc)

    # ── save ───────────────────────────────────────────────────────────────────
    out_path = r"c:\Users\Hp\Downloads\hcl\docs\02_ArgJain_DiseaseTrendAnalysis_HMWStatements.docx"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    doc.save(out_path)
    return out_path


if __name__ == "__main__":
    path = build_document()
    print(f"SAVED: {path}")
