import os
import sys
import time
from pathlib import Path
import docx2pdf

def main():
    docs_dir = Path(r"c:\Users\Hp\Downloads\hcl\docs")
    docx_files = sorted(docs_dir.glob("*.docx"))
    print(f"Found {len(docx_files)} DOCX files to convert to PDF in {docs_dir}:")
    
    success = 0
    failed = []
    
    for idx, docx_path in enumerate(docx_files, 1):
        pdf_path = docx_path.with_suffix(".pdf")
        print(f"\n[{idx}/{len(docx_files)}] Converting: {docx_path.name} -> {pdf_path.name}")
        t0 = time.time()
        try:
            docx2pdf.convert(str(docx_path), str(pdf_path))
            elapsed = time.time() - t0
            print(f"    -> SUCCESS in {elapsed:.1f}s | Size: {pdf_path.stat().st_size // 1024} KB")
            success += 1
        except Exception as e:
            print(f"    -> ERROR: {e}")
            failed.append((docx_path.name, str(e)))
            
    print(f"\n==========================================")
    print(f"CONVERSION COMPLETE: {success}/{len(docx_files)} converted successfully.")
    if failed:
        print(f"Failed files: {failed}")
    print(f"==========================================")

if __name__ == "__main__":
    main()
