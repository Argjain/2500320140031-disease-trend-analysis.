import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from pathlib import Path

BASE_DIR = Path(r"c:\Users\Hp\Downloads\hcl")
DOCS_DIR = BASE_DIR / "docs"

doc = docx.Document()
section = doc.sections[0]
section.top_margin = Inches(0.7)
section.bottom_margin = Inches(0.7)
section.left_margin = Inches(1.0)
section.right_margin = Inches(1.0)

# Add Logo
logo_path = DOCS_DIR / "abes_logo.jpg"
if logo_path.exists():
    p_logo = doc.add_paragraph()
    p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_logo = p_logo.add_run()
    run_logo.add_picture(str(logo_path), width=Inches(3.2))
    p_logo.paragraph_format.space_after = Pt(2)

# College Code
p_code = doc.add_paragraph("College Code: 032")
p_code.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_code.runs[0].font.name = "Times New Roman"
p_code.runs[0].font.size = Pt(10)
p_code.runs[0].font.bold = True
p_code.paragraph_format.space_after = Pt(10)

# College Name
p_col = doc.add_paragraph("ABES ENGINEERING COLLEGE")
p_col.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_col.runs[0].font.name = "Times New Roman"
p_col.runs[0].font.size = Pt(20)
p_col.runs[0].font.bold = True
p_col.runs[0].font.color.rgb = RGBColor(20, 20, 20)
p_col.paragraph_format.space_after = Pt(2)

# Location
p_loc = doc.add_paragraph("Ghaziabad, Uttar Pradesh")
p_loc.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_loc.runs[0].font.name = "Times New Roman"
p_loc.runs[0].font.size = Pt(13)
p_loc.runs[0].font.bold = True
p_loc.paragraph_format.space_after = Pt(2)

# Affiliation
p_aff = doc.add_paragraph("Affiliated to Dr. A.P.J. Abdul Kalam Technical University (AKTU), Uttar Pradesh")
p_aff.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_aff.runs[0].font.name = "Times New Roman"
p_aff.runs[0].font.size = Pt(11)
p_aff.paragraph_format.space_after = Pt(20)

# PROJECT SYNOPSIS
p_syn = doc.add_paragraph("PROJECT SYNOPSIS")
p_syn.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_syn.runs[0].font.name = "Times New Roman"
p_syn.runs[0].font.size = Pt(16)
p_syn.runs[0].font.bold = True
p_syn.paragraph_format.space_after = Pt(4)

# on
p_on = doc.add_paragraph("on")
p_on.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_on.runs[0].font.name = "Times New Roman"
p_on.runs[0].font.size = Pt(13)
p_on.runs[0].font.italic = True
p_on.paragraph_format.space_after = Pt(6)

# Title
p_title = doc.add_paragraph("Disease Trend Analysis Intelligence Cockpit")
p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_title.runs[0].font.name = "Times New Roman"
p_title.runs[0].font.size = Pt(18)
p_title.runs[0].font.bold = True
p_title.paragraph_format.space_after = Pt(4)

# Subtitle
p_sub = doc.add_paragraph("A Multi-Disease Surveillance & Epidemiological Analytics System\n(Project ID: P100)")
p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_sub.runs[0].font.name = "Times New Roman"
p_sub.runs[0].font.size = Pt(12)
p_sub.runs[0].font.bold = True
p_sub.runs[0].font.italic = True
p_sub.paragraph_format.space_after = Pt(20)

# Submission text
p_subm = doc.add_paragraph("Submitted in partial fulfilment of the requirements for the degree of")
p_subm.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_subm.runs[0].font.name = "Times New Roman"
p_subm.runs[0].font.size = Pt(11)
p_subm.paragraph_format.space_after = Pt(4)

p_deg = doc.add_paragraph("Master of Computer Applications")
p_deg.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_deg.runs[0].font.name = "Times New Roman"
p_deg.runs[0].font.size = Pt(15)
p_deg.runs[0].font.bold = True
p_deg.paragraph_format.space_after = Pt(2)

p_in = doc.add_paragraph("in")
p_in.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_in.runs[0].font.name = "Times New Roman"
p_in.runs[0].font.size = Pt(11)
p_in.runs[0].font.italic = True
p_in.paragraph_format.space_after = Pt(2)

p_spec = doc.add_paragraph("Data Analytics")
p_spec.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_spec.runs[0].font.name = "Times New Roman"
p_spec.runs[0].font.size = Pt(13)
p_spec.runs[0].font.bold = True
p_spec.paragraph_format.space_after = Pt(16)

p_prog = doc.add_paragraph("Training Programme: HCLTech Career Shaper Programme")
p_prog.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_prog.runs[0].font.name = "Times New Roman"
p_prog.runs[0].font.size = Pt(12)
p_prog.runs[0].font.bold = True
p_prog.paragraph_format.space_after = Pt(22)

# Details block
tbl = doc.add_table(rows=7, cols=2)
tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
tbl.autofit = False

details = [
    ("Submitted by:", "Arg Jain"),
    ("University Roll Number:", "2500320140031"),
    ("Project ID:", "P100"),
    ("Batch ID:", "ABES_OND26_MCA2ndYear_Data Analytics_Batch01"),
    ("Project Guide / Mentor:", "Mr. Dinesh"),
    ("Academic Session:", "2026–2027"),
    ("Submission Date:", "21 November 2026")
]

for row_idx, (k, v) in enumerate(details):
    r = tbl.rows[row_idx]
    c1, c2 = r.cells[0], r.cells[1]
    c1.width = Inches(2.3)
    c2.width = Inches(4.3)
    
    p1 = c1.paragraphs[0]
    p1.paragraph_format.space_before = Pt(2)
    p1.paragraph_format.space_after = Pt(2)
    run1 = p1.add_run(k)
    run1.font.name = "Times New Roman"
    run1.font.size = Pt(10.5)
    run1.bold = True
    
    p2 = c2.paragraphs[0]
    p2.paragraph_format.space_before = Pt(2)
    p2.paragraph_format.space_after = Pt(2)
    run2 = p2.add_run(v)
    run2.font.name = "Times New Roman"
    run2.font.size = Pt(10.5)
    run2.bold = True

out_p = DOCS_DIR / "00_ArgJain_DiseaseTrendAnalysis_ProjectSynopsis_CoverPage.docx"
doc.save(str(out_p))
print(f"Generated updated cover page with Batch ID: {out_p}")
