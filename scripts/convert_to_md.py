import docx
from pathlib import Path

docs_dir = Path("docs")
docx_files = sorted(list(docs_dir.glob("*.docx")))

print(f"Converting {len(docx_files)} DOCX deliverables to Markdown for IDE preview...")

for df in docx_files:
    doc = docx.Document(df)
    clean_title = df.stem.replace("_", " ")
    md_lines = [f"# {clean_title}\n"]
    
    for p in doc.paragraphs:
        txt = p.text.strip()
        if not txt:
            continue
        style = p.style.name.lower()
        if "heading 1" in style or "title" in style:
            md_lines.append(f"\n## {txt}\n")
        elif "heading 2" in style:
            md_lines.append(f"\n### {txt}\n")
        elif "heading 3" in style:
            md_lines.append(f"\n#### {txt}\n")
        elif "list" in style or "bullet" in style:
            md_lines.append(f"* {txt}")
        else:
            md_lines.append(f"{txt}\n")
            
    if doc.tables:
        md_lines.append("\n---\n### 📋 Embedded Data Tables\n")
        for i, tbl in enumerate(doc.tables):
            rows = [[c.text.strip().replace("\n", " ").replace("|", "/") for c in r.cells] for r in tbl.rows]
            if rows and len(rows) > 1:
                header = rows[0]
                data = rows[1:]
                md_lines.append(f"\n#### Table {i+1}\n")
                md_lines.append("| " + " | ".join(header) + " |")
                md_lines.append("| " + " | ".join(["---"] * len(header)) + " |")
                for d in data:
                    md_lines.append("| " + " | ".join(d) + " |")
                md_lines.append("\n")
                
    md_path = df.with_suffix(".md")
    md_path.write_text("\n".join(md_lines), encoding="utf-8")
    print(f"Generated: {md_path.name}")

print("All Markdown previews generated successfully!")
