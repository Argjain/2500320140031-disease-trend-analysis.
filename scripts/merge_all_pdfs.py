import os
import pypdfium2 as pdfium
from pathlib import Path

docs_dir = Path(r"c:\Users\Hp\Downloads\hcl\docs")

# Exact sequential list of all 15 project deliverable PDFs
pdf_sequence = [
    "01_ArgJain_DiseaseTrendAnalysis_ProjectUnderstanding.pdf",
    "02_ArgJain_DiseaseTrendAnalysis_HMWStatements.pdf",
    "03_ArgJain_DiseaseTrendAnalysis_NeedsAnalysis.pdf",
    "04_ArgJain_DiseaseTrendAnalysis_RTM.pdf",
    "05_ArgJain_DiseaseTrendAnalysis_BRD.pdf",
    "07_ArgJain_DiseaseTrendAnalysis_TRD.pdf",
    "08_ArgJain_DiseaseTrendAnalysis_DBDesign.pdf",
    "09_ArgJain_DiseaseTrendAnalysis_ERDiagram.pdf",
    "11_ArgJain_DiseaseTrendAnalysis_UserStories.pdf",
    "12_ArgJain_DiseaseTrendAnalysis_UIFramework.pdf",
    "13_ArgJain_DiseaseTrendAnalysis_TestCases.pdf",
    "14_ArgJain_DiseaseTrendAnalysis_BuildPlan.pdf",
    "16_ArgJain_DiseaseTrendAnalysis_DeploymentGuide.pdf",
    "17_ArgJain_DiseaseTrendAnalysis_ProjectDocument.pdf",
    "18_ArgJain_DiseaseTrendAnalysis_Presentation.pdf"
]

print("Initializing Master Merged PDF...")
merged_doc = pdfium.PdfDocument.new()

total_pages = 0
found_files = []

for idx, fname in enumerate(pdf_sequence, 1):
    fpath = docs_dir / fname
    if fpath.exists():
        src_doc = pdfium.PdfDocument(str(fpath))
        page_count = len(src_doc)
        merged_doc.import_pages(src_doc)
        total_pages += page_count
        found_files.append(fpath)
        print(f"[{idx}/{len(pdf_sequence)}] Merged: {fname} ({page_count} pages)")
    else:
        print(f"[{idx}/{len(pdf_sequence)}] WARNING: File not found: {fname}")

master_pdf_path = docs_dir / "ArgJain_DiseaseTrendAnalysis_Complete_Project_Dossier.pdf"
merged_doc.save(str(master_pdf_path))
print(f"\n==========================================")
print(f"MASTER PDF CREATED SUCCESSFULLY: {master_pdf_path.name}")
print(f"Total Pages: {total_pages} | File Size: {master_pdf_path.stat().st_size // 1024} KB")
print(f"==========================================")

# Now remove individual separate PDFs as requested by user
print("\nRemoving separate individual PDF files...")
deleted_count = 0
for fpath in found_files:
    try:
        fpath.unlink()
        print(f"  -> Deleted: {fpath.name}")
        deleted_count += 1
    except Exception as e:
        print(f"  -> Error deleting {fpath.name}: {e}")

# Also delete presentation slides PDF if exists
slides_pdf = docs_dir / "18_ArgJain_DiseaseTrendAnalysis_Presentation_Slides.pdf"
if slides_pdf.exists():
    slides_pdf.unlink()
    print("  -> Deleted: 18_ArgJain_DiseaseTrendAnalysis_Presentation_Slides.pdf")

print(f"\nClean-up Complete: {deleted_count} separate PDF files removed.")
print(f"Single unified project PDF retained: {master_pdf_path.name}")
