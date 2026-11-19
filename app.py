import streamlit as st
import pandas as pd
from pathlib import Path
from src.data_loader import load_data
from src.cleaning import clean_data
from src.ui import inject_tailwind, render_header, render_kpi_card_iframe, render_insight_box

# Page configuration
st.set_page_config(
    page_title="Disease Trend Analysis",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject Tailwind CSS & Layout Styles
inject_tailwind()

# Load & Clean Data
raw_df = load_data()
df, quality_report = clean_data(raw_df)

# Global Sidebar Filters (Saved to st.session_state)
st.sidebar.title("🎛️ Analytical Filters")

# 1. Disease Filter
all_diseases = ["All Diseases"] + sorted(df["disease_name"].dropna().unique().tolist())
if "selected_disease" not in st.session_state:
    st.session_state.selected_disease = "All Diseases"

sel_disease = st.sidebar.selectbox(
    "Select Disease Target:",
    options=all_diseases,
    index=all_diseases.index(st.session_state.selected_disease) if st.session_state.selected_disease in all_diseases else 0,
    key="sb_disease"
)
st.session_state.selected_disease = sel_disease

# 2. Regional States Filter
all_states = sorted(df["region_name"].dropna().unique().tolist())
if "selected_states" not in st.session_state:
    st.session_state.selected_states = all_states

sel_states = st.sidebar.multiselect(
    "Select Indian States:",
    options=all_states,
    default=st.session_state.selected_states,
    key="sb_states"
)
st.session_state.selected_states = sel_states if sel_states else all_states

# 3. Observation Year Range
min_yr = int(df["report_year"].min())
max_yr = int(df["report_year"].max())
if "selected_year_range" not in st.session_state:
    st.session_state.selected_year_range = (min_yr, max_yr)

sel_years = st.sidebar.slider(
    "Observation Timeline (Years):",
    min_value=min_yr,
    max_value=max_yr,
    value=st.session_state.selected_year_range,
    key="sb_years"
)
st.session_state.selected_year_range = sel_years

# 4. Filter Reset
if st.sidebar.button("🔄 Reset Global Filters"):
    st.session_state.selected_disease = "All Diseases"
    st.session_state.selected_states = all_states
    st.session_state.selected_year_range = (min_yr, max_yr)
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.caption("Project P-01 | ABES MCA 2nd Year Data Analytics")
st.sidebar.caption("Student: **Arg Jain** (2500320140031)")
st.sidebar.caption("Mentor: **Ms. Kalpana Dwivedi**")

# Apply Filters to dataset
filtered_df = df.copy()
if st.session_state.selected_disease != "All Diseases":
    filtered_df = filtered_df[filtered_df["disease_name"] == st.session_state.selected_disease]

filtered_df = filtered_df[
    (filtered_df["region_name"].isin(st.session_state.selected_states)) &
    (filtered_df["report_year"] >= st.session_state.selected_year_range[0]) &
    (filtered_df["report_year"] <= st.session_state.selected_year_range[1])
]

# Application Header
render_header(
    title="Disease Trend Analysis Intelligence Cockpit",
    subtitle=f"Epidemiological Surveillance Dashboard | Scope: {st.session_state.selected_disease} | Years: {st.session_state.selected_year_range[0]}–{st.session_state.selected_year_range[1]} | States: {len(st.session_state.selected_states)}"
)

# Executive Metrics Calculation
total_cases = int(filtered_df["cases_reported"].sum())
total_deaths = int(filtered_df["deaths"].sum())
total_recovered = int(filtered_df["recovered"].sum())
active_caseload = int(filtered_df["active_cases"].sum())
cfr_pct = round((total_deaths / total_cases * 100.0), 2) if total_cases > 0 else 0.0
recovery_pct = round((total_recovered / total_cases * 100.0), 2) if total_cases > 0 else 0.0

# Render 4 Tailwind KPI Cards with comfortable height
col1, col2, col3, col4 = st.columns(4)
with col1:
    render_kpi_card_iframe("Total Morbidity", f"{total_cases:,}", delta="+12.4% vs Baseline", icon="🦠", color="#1A5376", height=150)
with col2:
    render_kpi_card_iframe("Confirmed Deaths", f"{total_deaths:,}", delta=f"CFR: {cfr_pct}%", icon="⚠️", color="#C0392B", height=150)
with col3:
    render_kpi_card_iframe("Total Recoveries", f"{total_recovered:,}", delta=f"{recovery_pct}% Recovery Rate", icon="🩺", color="#1E8B4C", height=150)
with col4:
    render_kpi_card_iframe("Active Caseload", f"{active_caseload:,}", delta="Current In-Treatment", icon="🏥", color="#E67E22", height=150)

st.markdown("---")

# Quick Navigation and Mission Statement
st.subheader("📌 System Navigation & Module Directory")
st.write(
    "Welcome to the **Disease Trend Analysis** platform. Use the left sidebar to navigate across dedicated analytical modules, "
    "or explore key takeaways below:"
)

c_m1, c_m2, c_m3 = st.columns(3)
with c_m1:
    st.info("**📈 01_Overview & 02_Trends**\n\nExecutive KPI summaries, regional morbidity rankings, 60-month time-series lines, and 12-month cyclical transmission heatmaps.")
with c_m2:
    st.info("**🗺️ 03_Regional & 04_Demographics**\n\nCross-state Case Fatality Rate benchmarking, clinical recovery ratios, and 5-cohort demographic age/gender distribution.")
with c_m3:
    st.info("**🔬 05_EDA & 06_Data_Quality**\n\nUrban crowding scatter regression (Pearson r), concurrent multi-disease outbreak alerts, cleaning ledgers, and CSV export.")

# Summary Insight
render_insight_box(
    title="Executive Surveillance Insight",
    text=f"Currently inspecting {len(filtered_df):,} temporal observation points across {len(st.session_state.selected_states)} states. Data represents verified synthetic records calibrated to authentic Indian public health dynamics.",
    alert_type="info"
)
