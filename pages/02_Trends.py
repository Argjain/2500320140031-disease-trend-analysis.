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
from src.analysis import compute_yoy_change, compute_seasonal_trend
from src.ui import inject_tailwind, render_header, render_insight_box, safe_render_dataframe, render_sidebar_filters

st.set_page_config(page_title="Trends | Disease Trend Analysis", page_icon="📈", layout="wide")
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
    title="Longitudinal & Seasonal Transmission Trends (UI-02)",
    subtitle=f"Temporal Dynamics | Scope: {sel_disease} ({sel_category}) | Zone: {sel_zone} | Window: {sel_years[0]}–{sel_years[1]} | States: {len(sel_states)}"
)

if filtered.empty:
    st.warning("⚠️ No records match active filters.")
    st.stop()

# Tabs for Organized Temporal Perspectives
tab_trend1, tab_trend2, tab_trend3 = st.tabs([
    "📅 60-Month Trajectory & Smoothing",
    "🔄 Annual Overlapping Cycles & YoY %",
    "🌡️ 12-Month Seasonal Heatmap"
])

with tab_trend1:
    c_t1, c_t2 = st.columns([2, 1])
    with c_t1:
        st.subheader("📅 Continuous Transmission Trajectory (OQ-01, OQ-03)")
    with c_t2:
        smooth_choice = st.radio(
            "Curve Smoothing Window:",
            options=["Raw Monthly (Unsmoothed)", "3-Month Rolling Average", "6-Month Trendline"],
            index=1,
            horizontal=True,
            key="smooth_window_sel"
        )
        
    time_agg = filtered.groupby(["report_date", "disease_name"])["cases_reported"].sum().reset_index()
    time_agg["report_date"] = pd.to_datetime(time_agg["report_date"])
    time_agg = time_agg.sort_values(by="report_date")
    
    if smooth_choice == "3-Month Rolling Average":
        time_agg["display_cases"] = time_agg.groupby("disease_name")["cases_reported"].transform(
            lambda s: s.rolling(window=3, min_periods=1, center=True).mean()
        )
        chart_title = "Monthly Incident Cases (3-Month Centered Rolling Average)"
    elif smooth_choice == "6-Month Trendline":
        time_agg["display_cases"] = time_agg.groupby("disease_name")["cases_reported"].transform(
            lambda s: s.rolling(window=6, min_periods=1, center=True).mean()
        )
        chart_title = "Monthly Incident Cases (6-Month Smoothed Trendline)"
    else:
        time_agg["display_cases"] = time_agg["cases_reported"]
        chart_title = "Monthly Incident Cases Over Time (Raw Monthly Data)"

    fig_line = px.line(
        time_agg,
        x="report_date",
        y="display_cases",
        color="disease_name",
        markers=(smooth_choice == "Raw Monthly (Unsmoothed)"),
        title=chart_title,
        labels={"report_date": "Timeline (Monthly)", "display_cases": "Incident Cases", "disease_name": "Disease Entity"},
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    fig_line.update_layout(height=430, hovermode="x unified", margin=dict(l=60, r=20, t=40, b=40))
    fig_line.update_yaxes(automargin=True)
    st.plotly_chart(fig_line, use_container_width=True)

    # Optional Small Multiples View
    with st.expander("🔍 View Disease-Wise Isolated Trajectories (Small Multiples)"):
        fig_facet = px.line(
            time_agg,
            x="report_date",
            y="display_cases",
            facet_col="disease_name",
            facet_col_wrap=3,
            color="disease_name",
            title="Individual Transmission Trajectories per Disease Entity",
            labels={"report_date": "Date", "display_cases": "Cases", "disease_name": "Disease"}
        )
        fig_facet.update_layout(height=450, showlegend=False)
        fig_facet.update_yaxes(matches=None)
        st.plotly_chart(fig_facet, use_container_width=True)

with tab_trend2:
    st.subheader("🔄 Multi-Year Overlapping Annual Wave Cycles (OQ-09)")
    c_l, c_r = st.columns([1, 1])

    with c_l:
        yoy_agg = filtered.groupby(["report_month", "report_year"])["cases_reported"].sum().reset_index()
        yoy_agg["report_year"] = yoy_agg["report_year"].astype(str)
        month_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        
        fig_yoy = px.line(
            yoy_agg,
            x="report_month",
            y="cases_reported",
            color="report_year",
            markers=True,
            title="Comparative Annual Waves (Months 1 to 12)",
            labels={"report_month": "Calendar Month", "cases_reported": "Cases Reported", "report_year": "Year"},
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        fig_yoy.update_xaxes(tickmode='array', tickvals=list(range(1, 13)), ticktext=month_labels)
        fig_yoy.update_layout(height=380, margin=dict(l=50, r=20, t=40, b=40))
        st.plotly_chart(fig_yoy, use_container_width=True)

    with c_r:
        st.write("**Year-over-Year (YoY %) Annual Delta Matrix**")
        yoy_df = compute_yoy_change(filtered)
        if not yoy_df.empty:
            try:
                styled_yoy = yoy_df.style.background_gradient(cmap="coolwarm", axis=None).format("{:+.1f}%", na_rep="—")
                safe_render_dataframe(styled_yoy, use_container_width=True)
            except Exception:
                safe_render_dataframe(yoy_df.fillna("—"), use_container_width=True)
        else:
            st.info("Insufficient longitudinal range to compute YoY delta.")

with tab_trend3:
    st.subheader("🌡️ 12-Month Seasonal Intensity Heatmap Matrix (OQ-10)")
    seasonal_matrix = compute_seasonal_trend(filtered)

    if not seasonal_matrix.empty:
        month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        seasonal_matrix.columns = [month_names[m - 1] for m in seasonal_matrix.columns if 1 <= m <= 12]
        
        fig_heat = px.imshow(
            seasonal_matrix,
            color_continuous_scale="YlOrRd",
            title="Average Monthly Incident Cases per Disease Entity",
            labels=dict(x="Calendar Month", y="Disease Entity", color="Avg Cases"),
            text_auto=".0f"
        )
        fig_heat.update_layout(height=380, margin=dict(l=110, r=30, t=40, b=40))
        st.plotly_chart(fig_heat, use_container_width=True)
        
        st.caption("Notice the highlighted monsoon surge window in July–October for vector-borne diseases (Dengue, Malaria).")

render_insight_box(
    title="Seasonal Transmission Insight",
    text="Vector-borne illnesses (Dengue & Malaria) exhibit pronounced surges during the post-monsoon window (July to September), demanding therapeutic prepositioning 60 days in advance.",
    alert_type="warning"
)
