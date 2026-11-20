import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from src.data_loader import load_data
from src.cleaning import clean_data
from src.ui import inject_tailwind, render_header, render_kpi_card_iframe, render_insight_box, render_sidebar_filters

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

# Global Advanced Sidebar Filters (Preserves state and supports quick presets)
filtered_df = render_sidebar_filters(df)

# Application Header
sel_dis = st.session_state.get("selected_disease", "All Diseases")
sel_cat = st.session_state.get("selected_category", "All Categories")
sel_zn = st.session_state.get("selected_zone", "All Zones")
sel_yrs = st.session_state.get("selected_year_range", (2020, 2024))
sel_sts = st.session_state.get("selected_states", [])

render_header(
    title="Disease Trend Analysis Intelligence Cockpit",
    subtitle=f"Epidemiological Surveillance Dashboard | Disease: {sel_dis} ({sel_cat}) | Zone: {sel_zn} | Timeline: {sel_yrs[0]}–{sel_yrs[1]} | States: {len(sel_sts)}"
)

if filtered_df.empty:
    st.warning("⚠️ No records match the active filter criteria. Please broaden your selection in the sidebar.")
    st.stop()

# Executive Metrics Calculation
total_cases = int(filtered_df["cases_reported"].sum())
total_deaths = int(filtered_df["deaths"].sum())
total_recovered = int(filtered_df["recovered"].sum())
active_caseload = int(filtered_df["active_cases"].sum())
total_hosp = int(filtered_df["hospitalized"].sum())
cfr_pct = round((total_deaths / total_cases * 100.0), 2) if total_cases > 0 else 0.0
recovery_pct = round((total_recovered / total_cases * 100.0), 2) if total_cases > 0 else 0.0
hosp_pct = round((total_hosp / total_cases * 100.0), 2) if total_cases > 0 else 0.0

# Render 4 Tailwind KPI Cards with comfortable height
col1, col2, col3, col4 = st.columns(4)
with col1:
    render_kpi_card_iframe("Total Morbidity", f"{total_cases:,}", delta=f"{len(filtered_df):,} Reports", icon="🦠", color="#1A5376", height=150)
with col2:
    render_kpi_card_iframe("Confirmed Deaths", f"{total_deaths:,}", delta=f"CFR: {cfr_pct}%", icon="⚠️", color="#C0392B", height=150)
with col3:
    render_kpi_card_iframe("Total Recoveries", f"{total_recovered:,}", delta=f"{recovery_pct}% Recovery Rate", icon="🩺", color="#1E8B4C", height=150)
with col4:
    render_kpi_card_iframe("Active Caseload", f"{active_caseload:,}", delta=f"{hosp_pct}% Hospitalized", icon="🏥", color="#E67E22", height=150)

st.markdown("---")

# Row 2: Deep-Dive Surveillance Visuals
c_v1, c_v2 = st.columns([1, 1])

with c_v1:
    st.subheader("🧬 Morbidity by Transmission Category")
    cat_agg = filtered_df.groupby("disease_category")["cases_reported"].sum().reset_index()
    fig_cat = px.pie(
        cat_agg,
        values="cases_reported",
        names="disease_category",
        title="Disease Category Proportional Share",
        hole=0.48,
        color_discrete_sequence=["#1A5376", "#0284C7", "#059669"]
    )
    fig_cat.update_traces(
        textposition='inside',
        textinfo='percent+label',
        insidetextorientation='horizontal',
        textfont=dict(size=12, color="#ffffff")
    )
    fig_cat.update_layout(height=340, margin=dict(l=10, r=10, t=40, b=20))
    st.plotly_chart(fig_cat, use_container_width=True)

with c_v2:
    st.subheader("🎯 National Epidemiological Benchmarks")
    # Identify high-water mark insights
    top_state = filtered_df.groupby("region_name")["cases_reported"].sum().idxmax()
    top_state_val = int(filtered_df.groupby("region_name")["cases_reported"].sum().max())
    outbreak_months = int(filtered_df["is_outbreak"].sum())
    
    st.markdown(
        f"""
        <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 18px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); height: 340px; display: flex; flex-direction: column; justify-content: space-around;">
            <div style="border-bottom: 1px solid #f1f5f9; padding-bottom: 8px;">
                <span style="font-size: 0.8rem; font-weight: 700; color: #64748b; text-transform: uppercase;">Highest Caseload State</span>
                <div style="font-size: 1.25rem; font-weight: 800; color: #0f2b48;">📍 {top_state} <span style="font-size: 0.9rem; color: #0284c7; font-weight: 600;">({top_state_val:,} cases)</span></div>
            </div>
            <div style="border-bottom: 1px solid #f1f5f9; padding-bottom: 8px;">
                <span style="font-size: 0.8rem; font-weight: 700; color: #64748b; text-transform: uppercase;">Surveillance Surge Events</span>
                <div style="font-size: 1.25rem; font-weight: 800; color: #b91c1c;">🚨 {outbreak_months} State-Months Flagged <span style="font-size: 0.85rem; color: #64748b; font-weight: normal;">(Outbreak Triggered)</span></div>
            </div>
            <div style="border-bottom: 1px solid #f1f5f9; padding-bottom: 8px;">
                <span style="font-size: 0.8rem; font-weight: 700; color: #64748b; text-transform: uppercase;">Clinical Case Fatality Index</span>
                <div style="font-size: 1.25rem; font-weight: 800; color: {'#059669' if cfr_pct < 2.5 else '#dc2626'};">⚖️ {cfr_pct}% National Average CFR <span style="font-size: 0.85rem; color: #64748b; font-weight: normal;">(Target: &lt;2.0%)</span></div>
            </div>
            <div>
                <span style="font-size: 0.8rem; font-weight: 700; color: #64748b; text-transform: uppercase;">Critical Bed Utilization Pressure</span>
                <div style="font-size: 1.25rem; font-weight: 800; color: #d97706;">🛏️ {total_hosp:,} Patients Hospitalized <span style="font-size: 0.85rem; color: #64748b; font-weight: normal;">({hosp_pct}% of total cases)</span></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

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
