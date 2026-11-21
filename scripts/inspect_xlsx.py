import openpyxl
from pathlib import Path

files = [
    "LMS_Submission_Folder/06_Database_Schema.xlsx",
    "LMS_Submission_Folder/06_Project_Database.xlsx",
    "LMS_Submission_Folder/08_Other_Project_Documents/04_Traceability_Matrix.xlsx",
    "LMS_Submission_Folder/08_Other_Project_Documents/08_Database_Design.xlsx",
    "disease_trend_analysis_data.xlsx"
]

for f in files:
    p = Path(f)
    if not p.exists():
        print("Missing:", f)
        continue
    wb = openpyxl.load_workbook(str(p), data_only=True)
    print("\n" + "=" * 50)
    print("FILE:", f)
    print("Sheets:", wb.sheetnames)
    for s in wb.sheetnames:
        ws = wb[s]
        rows = list(ws.iter_rows(values_only=True))
        non_empty = [r for r in rows if any(c is not None for c in r)]
        print(f"  [Sheet: '{s}'] max_row={ws.max_row}, non_empty_rows={len(non_empty)}")
        for i, r in enumerate(non_empty[:10]):
            print(f"    row {i+1}: {r[:5]}")
