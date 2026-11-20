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
from src.ui import inject_tailwind, render_header, render_kpi_card_iframe, render_insight_box, safe_render_dataframe, render_sidebar_filters

st.set_page_config(page_title="Overview | Disease Trend Analysis", page_icon="📊", layout="wide")
inject_tailwind()

# Load & Clean Data
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
    title="Executive Overview & KPI Cockpit (UI-01)",
    subtitle=f"Target: {sel_disease} ({sel_category}) | Zone: {sel_zone} | Timeline: {sel_years[0]}–{sel_years[1]} | States: {len(sel_states)} | Slice: {len(filtered):,} records"
)

if filtered.empty:
    st.warning("⚠️ No records match the active filter criteria. Please broaden your selection in the sidebar.")
    st.stop()

# Row 1: KPI Stat Cards
tot_cases = int(filtered["cases_reported"].sum())
tot_deaths = int(filtered["deaths"].sum())
tot_rec = int(filtered["recovered"].sum())
tot_act = int(filtered["active_cases"].sum())
cfr = round((tot_deaths / tot_cases * 100.0), 2) if tot_cases > 0 else 0.0
rec_rate = round((tot_rec / tot_cases * 100.0), 2) if tot_cases > 0 else 0.0

c1, c2, c3, c4 = st.columns(4)
with c1:
    render_kpi_card_iframe("Total Morbidity", f"{tot_cases:,}", delta=f"{len(filtered):,} reports", icon="🦠", color="#1A5376", height=150)
with c2:
    render_kpi_card_iframe("Total Fatalities", f"{tot_deaths:,}", delta=f"CFR: {cfr}%", icon="⚠️", color="#C0392B", height=150)
with c3:
    render_kpi_card_iframe("Recovered Cases", f"{tot_rec:,}", delta=f"{rec_rate}% Recovery", icon="🩺", color="#1E8B4C", height=150)
with c4:
    render_kpi_card_iframe("Active Caseload", f"{tot_act:,}", delta="Ongoing In-Care", icon="🏥", color="#E67E22", height=150)

st.markdown("---")

# Organized Tabs for Deep-Dive Views
tab1, tab2, tab3 = st.tabs(["📊 State Burden & Metric Ranking", "📋 Cross-State Benchmark Table", "🌐 Zonal Morbidity Split"])

with tab1:
    col_ctrl1, col_ctrl2 = st.columns([2, 1])
    with col_ctrl1:
        st.subheader("📍 State-Level Performance Ranking (OQ-02, BR-02)")
    with col_ctrl2:
        rank_metric = st.selectbox(
            "Sort States By Metric:",
            options=["Total Cases", "Deaths", "Recovered", "Active Cases", "Hospitalized"],
            index=0,
            key="ov_rank_metric"
        )
    
    metric_col_map = {
        "Total Cases": "cases_reported",
        "Deaths": "deaths",
        "Recovered": "recovered",
        "Active Cases": "active_cases",
        "Hospitalized": "hospitalized"
    }
    target_metric = metric_col_map[rank_metric]
    
    reg_group = filtered.groupby("region_name")[target_metric].sum().reset_index()
    reg_group = reg_group.sort_values(by=target_metric, ascending=True)
    max_c = reg_group[target_metric].max() if not reg_group.empty else 1000

    color_scale_map = {
        "Total Cases": "Blues",
        "Deaths": "Reds",
        "Recovered": "Greens",
        "Active Cases": "Oranges",
        "Hospitalized": "Purples"
    }

    fig_bar = px.bar(
        reg_group,
        x=target_metric,
        y="region_name",
        orientation="h",
        title=f"States Ranked by {rank_metric} — Scope: {sel_disease}",
        labels={target_metric: rank_metric, "region_name": "Indian State"},
        color=target_metric,
        color_continuous_scale=color_scale_map[rank_metric],
        text_auto=",.0f"
    )
    fig_bar.update_traces(textposition="outside", cliponaxis=False, textfont=dict(size=11, color="#1e293b"))
    fig_bar.update_layout(height=450, margin=dict(l=120, r=60, t=40, b=30))
    fig_bar.update_xaxes(range=[0, max_c * 1.18], automargin=True)
    fig_bar.update_yaxes(automargin=True)
    st.plotly_chart(fig_bar, use_container_width=True)

with tab2:
    st.subheader("📋 Cross-State Epidemiological Performance Summary (OQ-05, BR-03)")
    summary_tbl = filtered.groupby("region_name").agg(
        Total_Cases=("cases_reported", "sum"),
        Deaths=("deaths", "sum"),
        Recoveries=("recovered", "sum"),
        Active=("active_cases", "sum"),
        Hospitalized=("hospitalized", "sum"),
        Population=("population", "first")
    ).reset_index()

    summary_tbl["CFR (%)"] = (summary_tbl["Deaths"] / summary_tbl["Total_Cases"].replace(0, 1) * 100.0).round(2)
    summary_tbl["Recovery (%)"] = (summary_tbl["Recoveries"] / summary_tbl["Total_Cases"].replace(0, 1) * 100.0).round(2)
    summary_tbl["Incidence/Lakh"] = (summary_tbl["Total_Cases"] / summary_tbl["Population"] * 100000.0).round(2)
    summary_tbl = summary_tbl.sort_values(by="Total_Cases", ascending=False)
    summary_tbl = summary_tbl.rename(columns={"region_name": "State"})

    try:
        styled_summary = (
            summary_tbl.style.background_gradient(subset=["CFR (%)"], cmap="Reds")
                             .background_gradient(subset=["Recovery (%)"], cmap="Greens")
                             .format({
                                 "Total_Cases": "{:,}",
                                 "Deaths": "{:,}",
                                 "Recoveries": "{:,}",
                                 "Active": "{:,}",
                                 "Hospitalized": "{:,}",
                                 "Population": "{:,}",
                                 "CFR (%)": "{:.2f}%",
                                 "Recovery (%)": "{:.2f}%",
                                 "Incidence/Lakh": "{:.2f}"
                             }, na_rep="—")
        )
        safe_render_dataframe(styled_summary, use_container_width=True)
    except Exception:
        safe_render_dataframe(summary_tbl, use_container_width=True)

    csv_summary = summary_tbl.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Export Benchmark Table (CSV)",
        data=csv_summary,
        file_name="state_epidemiological_benchmarks.csv",
        mime="text/csv"
    )

with tab3:
    st.subheader("🌐 Zonal Case Distribution & Comparison")
    zone_agg = filtered.groupby("zone").agg(
        Total_Cases=("cases_reported", "sum"),
        Total_Deaths=("deaths", "sum")
    ).reset_index()
    zone_agg["CFR (%)"] = (zone_agg["Total_Deaths"] / zone_agg["Total_Cases"].replace(0, 1) * 100.0).round(2)

    cz1, cz2 = st.columns(2)
    with cz1:
        fig_zone_pie = px.pie(
            zone_agg,
            values="Total_Cases",
            names="zone",
            title="Caseload Proportion Across Zones",
            hole=0.45,
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        fig_zone_pie.update_traces(textposition='inside', textinfo='percent+label', insidetextorientation='horizontal')
        fig_zone_pie.update_layout(height=380, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_zone_pie, use_container_width=True)
        
    with cz2:
        fig_zone_bar = px.bar(
            zone_agg,
            x="zone",
            y="Total_Cases",
            color="CFR (%)",
            color_continuous_scale="Reds",
            title="Total Cases & Average CFR by Zone",
            labels={"Total_Cases": "Total Cases", "zone": "Zone"},
            text_auto=",.0f"
        )
        fig_zone_bar.update_traces(textposition="outside", cliponaxis=False)
        fig_zone_bar.update_layout(height=380, margin=dict(l=40, r=20, t=40, b=30))
        st.plotly_chart(fig_zone_bar, use_container_width=True)

render_insight_box(
    title="Key Surveillance Finding",
    text="Higher absolute morbidity concentrates in dense metropolitan centers (Maharashtra and Delhi), while Case Fatality Rates reflect hospital management capacity.",
    alert_type="info"
)
