import pandas as pd
from pathlib import Path

docs_dir = Path("docs")

def df_to_md(df):
    cols = [str(c) for c in df.columns]
    header = "| " + " | ".join(cols) + " |"
    divider = "| " + " | ".join(["---"] * len(cols)) + " |"
    rows = []
    for _, row in df.fillna("—").iterrows():
        r_str = "| " + " | ".join([str(val).replace("\n", " ").replace("|", "/") for val in row]) + " |"
        rows.append(r_str)
    return "\n".join([header, divider] + rows)

for xlsx_name in ["04_ArgJain_DiseaseTrendAnalysis_RTM.xlsx", "08_ArgJain_DiseaseTrendAnalysis_DBDesign.xlsx"]:
    p = docs_dir / xlsx_name
    if not p.exists():
        continue
    
    excel = pd.ExcelFile(p)
    clean_title = p.stem.replace("_", " ")
    md_lines = [f"# {clean_title}\n", f"> Official Project Spreadsheet Artifact: `{p.name}`\n"]
    
    for s_name in excel.sheet_names:
        df = pd.read_excel(p, sheet_name=s_name)
        md_lines.append(f"\n## 📊 Sheet: {s_name} ({len(df)} rows)\n")
        md_lines.append(df_to_md(df))
        md_lines.append("\n")
        
    md_path = p.with_suffix(".md")
    md_path.write_text("\n".join(md_lines), encoding="utf-8")
    print(f"Generated Excel Markdown Preview: {md_path.name}")
