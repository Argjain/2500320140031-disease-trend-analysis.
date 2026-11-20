import streamlit as st
import pandas as pd
import plotly.express as px
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.data_loader import load_data
from src.cleaning import clean_data
from src.analysis import compute_regional_summary
from src.ui import inject_tailwind, render_header, render_insight_box, render_sidebar_filters

st.set_page_config(page_title="Regional | Disease Trend Analysis", page_icon="🗺️", layout="wide")
inject_tailwind()

raw_df = load_data()
df, _ = clean_data(raw_df)

# Global Sidebar Filters
filtered = render_sidebar_filters(df)

sel_disease = st.session_state.get("selected_disease", "All Diseases")
sel_category = st.session_state.get("selected_category", "All Categories")
sel_zone = st.session_state.get("selected_zone", "All Zones")
sel_years = st.session_state.get("selected_year_range", (int(df["report_year"].min()), int(df["report_year"].max())))
sel_states = st.session_state.get("selected_states", sorted(df["region_name"].unique().tolist()))

render_header(
    title="Regional Burden & Clinical Recovery Efficacy (UI-03)",
    subtitle=f"Cross-State Comparative Analysis | Scope: {sel_disease} ({sel_category}) | Zone: {sel_zone} | States: {len(sel_states)} | Timeline: {sel_years[0]}–{sel_years[1]}"
)

if filtered.empty:
    st.warning("⚠️ No records match active filters.")
    st.stop()

# State Summary Data
reg_summary = compute_regional_summary(filtered)

tab_reg1, tab_reg2, tab_reg3 = st.tabs([
    "📍 Caseload & Mortality Rankings",
    "🛡️ Health System Resilience Quadrant",
    "🛏️ Hospital Bed & Active Patient Pressure"
])

with tab_reg1:
    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("📍 State Case Burden Ranking (OQ-02)")
        max_tot = reg_summary["total_cases"].max() if not reg_summary.empty else 1000
        fig_cases = px.bar(
            reg_summary,
            x="total_cases",
            y="region_name",
            orientation="h",
            color="total_cases",
            color_continuous_scale="Viridis",
            title="Total Incident Cases by State",
            labels={"total_cases": "Total Cases", "region_name": "State"},
            text_auto=",.0f"
        )
        fig_cases.update_traces(textposition="outside", cliponaxis=False, textfont=dict(size=10, color="#1e293b"))
        fig_cases.update_layout(height=430, yaxis=dict(autorange="reversed", automargin=True), margin=dict(l=110, r=50, t=40, b=30))
        fig_cases.update_xaxes(range=[0, max_tot * 1.18], automargin=True)
        st.plotly_chart(fig_cases, use_container_width=True)

    with col_b:
        st.subheader("⚠️ Case Fatality Rate (CFR %) Ranking (OQ-05)")
        sorted_cfr = reg_summary.sort_values(by="cfr_pct", ascending=False)
        max_cfr = sorted_cfr["cfr_pct"].max() if not sorted_cfr.empty else 5.0
        fig_cfr = px.bar(
            sorted_cfr,
            x="cfr_pct",
            y="region_name",
            orientation="h",
            color="cfr_pct",
            color_continuous_scale="Reds",
            title="Case Fatality Rate (%) by State",
            labels={"cfr_pct": "CFR (%)", "region_name": "State"},
            text_auto=".2f"
        )
        fig_cfr.update_traces(textposition="outside", cliponaxis=False, textfont=dict(size=10, color="#1e293b"))
        fig_cfr.update_layout(height=430, yaxis=dict(autorange="reversed", automargin=True), margin=dict(l=110, r=50, t=40, b=30))
        fig_cfr.update_xaxes(range=[0, max_cfr * 1.2], automargin=True)
        st.plotly_chart(fig_cfr, use_container_width=True)

with tab_reg2:
    st.subheader("🛡️ Clinical Resilience Quadrant (Recovery vs Fatality)")
    avg_rec = reg_summary["recovery_rate_pct"].mean()
    avg_cfr = reg_summary["cfr_pct"].mean()
    
    fig_quad = px.scatter(
        reg_summary,
        x="recovery_rate_pct",
        y="cfr_pct",
        size="total_cases",
        color="cfr_pct",
        color_continuous_scale="RdYlGn_r",
        text="region_name",
        hover_name="region_name",
        hover_data={"recovery_rate_pct": ":.2f%", "cfr_pct": ":.2f%", "total_cases": ":,"},
        title="State Health System Resilience (Bubble Size = Caseload)",
        labels={"recovery_rate_pct": "Clinical Recovery Rate (%)", "cfr_pct": "Case Fatality Rate (%)"}
    )
    fig_quad.update_traces(textposition="top center", textfont=dict(size=11, color="#0f2b48"))
    fig_quad.add_hline(y=avg_cfr, line_dash="dash", line_color="#ef4444", annotation_text=f"National Avg CFR ({avg_cfr:.2f}%)")
    fig_quad.add_vline(x=avg_rec, line_dash="dash", line_color="#10b981", annotation_text=f"National Avg Recovery ({avg_rec:.1f}%)")
    fig_quad.update_layout(height=450, margin=dict(l=60, r=40, t=50, b=40))
    st.plotly_chart(fig_quad, use_container_width=True)
    
    st.caption("Quadrant Guide: Bottom-Right = High Recovery & Low Fatality (Resilient). Top-Left = Lower Recovery & Higher Fatality (Intervention Target).")

with tab_reg3:
    st.subheader("🛏️ Hospitalization vs Active In-Treatment Caseload")
    hosp_summary = filtered.groupby("region_name").agg(
        Active_Outpatients=("active_cases", "sum"),
        Hospitalized=("hospitalized", "sum")
    ).reset_index()
    
    fig_hosp = px.bar(
        hosp_summary,
        x="region_name",
        y=["Hospitalized", "Active_Outpatients"],
        title="Active Patients by Inpatient Hospitalization vs Outpatient Care",
        labels={"value": "Number of Patients", "region_name": "State", "variable": "Patient Triage Status"},
        barmode="stack",
        color_discrete_map={"Hospitalized": "#dc2626", "Active_Outpatients": "#3b82f6"}
    )
    fig_hosp.update_layout(height=420, margin=dict(l=50, r=20, t=40, b=40), xaxis=dict(tickangle=-30))
    st.plotly_chart(fig_hosp, use_container_width=True)

render_insight_box(
    title="Regional Efficacy Insight",
    text="States maintaining clinical recovery rates above 92.0% demonstrate superior critical-care triage resilience despite elevated raw case surges.",
    alert_type="success"
)
