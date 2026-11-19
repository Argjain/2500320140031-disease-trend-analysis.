import streamlit as st
import pandas as pd
import openpyxl
import docx
from pathlib import Path
from src.ui import inject_tailwind, render_header, render_insight_box, safe_render_dataframe

st.set_page_config(
    page_title="Project Documents & Deliverables | Disease Trend Analysis",
    page_icon="📄",
    layout="wide"
)
inject_tailwind()

render_header(
    title="Project Deliverables & Document Previewer (UI-07)",
    subtitle="Interactive In-App Document Inspection & Official Deliverables Download Center (Steps 01–18)"
)

DOCS_DIR = Path(__file__).resolve().parent.parent / "docs"

# Registry of all 18-step official deliverables
DELIVERABLES = {
    "Step 01 — Project Understanding (Word .docx)": "01_ArgJain_DiseaseTrendAnalysis_ProjectUnderstanding.docx",
    "Step 02 — How Might We Statements (Word .docx)": "02_ArgJain_DiseaseTrendAnalysis_HMWStatements.docx",
    "Step 03 — Needs Analysis (Word .docx)": "03_ArgJain_DiseaseTrendAnalysis_NeedsAnalysis.docx",
    "Step 04 — Requirements Traceability Matrix (Excel .xlsx)": "04_ArgJain_DiseaseTrendAnalysis_RTM.xlsx",
    "Step 05 — Business Requirements Document (Word .docx)": "05_ArgJain_DiseaseTrendAnalysis_BRD.docx",
    "Step 07 — Technical Requirements Document (Word .docx)": "07_ArgJain_DiseaseTrendAnalysis_TRD.docx",
    "Step 08 — Database Design & Schema (Excel .xlsx)": "08_ArgJain_DiseaseTrendAnalysis_DBDesign.xlsx",
    "Step 09 — ER Diagram Report (Word .docx)": "09_ArgJain_DiseaseTrendAnalysis_ERDiagram.docx",
    "Step 09 — High-Resolution ER Diagram (Image .png)": "09_ER_Diagram.png",
    "Step 11 — User Stories & Acceptance Criteria (Word .docx)": "11_ArgJain_DiseaseTrendAnalysis_UserStories.docx",
    "Step 12 — UI Framework & Wireframes (Word .docx)": "12_ArgJain_DiseaseTrendAnalysis_UIFramework.docx",
    "Step 13 — Test Cases & QA Traceability (Word .docx)": "13_ArgJain_DiseaseTrendAnalysis_TestCases.docx",
    "Step 14 — Implementation Build Plan (Word .docx)": "14_ArgJain_DiseaseTrendAnalysis_BuildPlan.docx",
    "Step 16 — Streamlit Cloud Deployment Guide (Word .docx)": "16_ArgJain_DiseaseTrendAnalysis_DeploymentGuide.docx",
    "Step 17 — Final ABES Project Document (Word .docx)": "17_ArgJain_DiseaseTrendAnalysis_ProjectDocument.docx",
    "Step 18 — Viva Presentation Slide Deck (Word .docx)": "18_ArgJain_DiseaseTrendAnalysis_Presentation.docx",
}

# Deliverable Selector Controls
c_sel, c_info = st.columns([3, 2])

with c_sel:
    selected_label = st.selectbox(
        "📂 Select Project Deliverable to Preview & Download:",
        options=list(DELIVERABLES.keys()),
        index=0,
        help="Select any official document from Steps 01 to 18 to view its content directly in the browser."
    )

selected_file = DELIVERABLES[selected_label]
file_path = DOCS_DIR / selected_file

with c_info:
    if file_path.exists():
        size_kb = round(file_path.stat().st_size / 1024, 1)
        st.markdown(
            f"""
            <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:10px; padding:10px 16px; margin-top:22px;">
                <span style="font-size:0.75rem; text-transform:uppercase; color:#64748b; font-weight:700;">Active File</span><br>
                <b style="color:#0f172a; font-size:0.95rem;">{selected_file}</b>
                <span style="background:#e2e8f0; color:#334155; font-size:0.75rem; padding:2px 8px; border-radius:6px; margin-left:8px;">{size_kb} KB</span>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.error(f"File not found at {file_path}")

st.markdown("---")

# Download Action Bar
if file_path.exists():
    with open(file_path, "rb") as f:
        file_bytes = f.read()

    mime_types = {
        ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        ".png": "image/png"
    }
    ext = file_path.suffix.lower()
    mime = mime_types.get(ext, "application/octet-stream")

    c_btn, c_note = st.columns([1, 3])
    with c_btn:
        st.download_button(
            label=f"📥 Download {ext.upper()[1:]} File",
            data=file_bytes,
            file_name=selected_file,
            mime=mime,
            help=f"Download {selected_file} to your computer."
        )
    with c_note:
        st.caption("✅ Certified academic project artifact conforming to ABES Engineering College MCA requirements.")

st.markdown("### 👁️ Live In-App Document Preview")

# DOCUMENT PREVIEW ENGINE
if file_path.exists():
    ext = file_path.suffix.lower()
    
    # 1. PREVIEW WORD DOCUMENTS (.docx)
    if ext == ".docx":
        try:
            doc = docx.Document(file_path)
            
            with st.container():
                # Display Word Document Content
                for p in doc.paragraphs:
                    txt = p.text.strip()
                    if not txt:
                        continue
                    style = p.style.name.lower()
                    if "heading 1" in style or "title" in style:
                        st.markdown(f"## {txt}")
                    elif "heading 2" in style:
                        st.markdown(f"### {txt}")
                    elif "heading 3" in style:
                        st.markdown(f"#### {txt}")
                    elif "list" in style or "bullet" in style:
                        st.markdown(f"* {txt}")
                    else:
                        st.markdown(txt)

                # Display Document Tables
                if doc.tables:
                    st.markdown("#### 📋 Embedded Document Data Tables")
                    for i, tbl in enumerate(doc.tables):
                        rows = [[cell.text.strip().replace("\n", " ") for cell in row.cells] for row in tbl.rows]
                        if rows and len(rows) > 1:
                            header = rows[0]
                            data = rows[1:]
                            # Ensure unique column names
                            cols = []
                            for idx, h in enumerate(header):
                                col_name = h if h and h not in cols else f"Col_{idx+1}"
                                cols.append(col_name)
                            tbl_df = pd.DataFrame(data, columns=cols)
                            with st.expander(f"Table {i+1} ({len(tbl_df)} rows × {len(tbl_df.columns)} cols)", expanded=(i==0)):
                                safe_render_dataframe(tbl_df, use_container_width=True)
        except Exception as e:
            st.error(f"Error parsing Word document: {e}")

    # 2. PREVIEW EXCEL SPREADSHEETS (.xlsx)
    elif ext == ".xlsx":
        try:
            excel_file = pd.ExcelFile(file_path)
            sheet_names = excel_file.sheet_names
            
            st.write(f"The spreadsheet **`{selected_file}`** contains **{len(sheet_names)} sheets**:")
            
            # Sheet Tabs
            sheet_tabs = st.tabs(sheet_names)
            for tab, s_name in zip(sheet_tabs, sheet_names):
                with tab:
                    s_df = pd.read_excel(file_path, sheet_name=s_name)
                    st.caption(f"Sheet: **{s_name}** ({len(s_df)} rows, {len(s_df.columns)} columns)")
                    safe_render_dataframe(s_df, use_container_width=True)
        except Exception as e:
            st.error(f"Error loading Excel spreadsheet: {e}")

    # 3. PREVIEW IMAGES (.png)
    elif ext == ".png":
        st.image(str(file_path), caption="Entity-Relationship Diagram (3NF Crow's Foot Schema)", use_container_width=True)

else:
    st.warning("Selected deliverable file does not exist on disk.")

render_insight_box(
    title="Deliverable Governance & Traceability",
    text="All 15 formal documentation deliverables are synchronized with the database schema (Step 08), user stories (Step 11), and automated test suite (Step 13).",
    alert_type="info"
)
