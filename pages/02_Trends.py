import streamlit as st
import pandas as pd
import plotly.express as px
from src.data_loader import load_data
from src.cleaning import clean_data
from src.analysis import compute_yoy_change, compute_seasonal_trend
from src.ui import inject_tailwind, render_header, render_insight_box

st.set_page_config(page_title="Trends | Disease Trend Analysis", page_icon="📈", layout="wide")
inject_tailwind()

raw_df = load_data()
df, _ = clean_data(raw_df)

sel_disease = st.session_state.get("selected_disease", "All Diseases")
sel_states = st.session_state.get("selected_states", sorted(df["region_name"].unique().tolist()))
sel_years = st.session_state.get("selected_year_range", (int(df["report_year"].min()), int(df["report_year"].max())))

filtered = df.copy()
if sel_disease != "All Diseases":
    filtered = filtered[filtered["disease_name"] == sel_disease]
filtered = filtered[
    (filtered["region_name"].isin(sel_states)) &
    (filtered["report_year"] >= sel_years[0]) &
    (filtered["report_year"] <= sel_years[1])
]

render_header(
    title="Longitudinal & Seasonal Transmission Trends (UI-02)",
    subtitle=f"Temporal Dynamics | Target: {sel_disease} | Observation Window: {sel_years[0]}–{sel_years[1]}"
)

if filtered.empty:
    st.warning("⚠️ No records match active filters.")
    st.stop()

# 1. 60-Month Longitudinal Time Series (OQ-01, OQ-03, BR-01)
st.subheader("📅 60-Month Continuous Transmission Trajectory (OQ-01, OQ-03)")
time_agg = filtered.groupby(["report_date", "disease_name"])["cases_reported"].sum().reset_index()

fig_line = px.line(
    time_agg,
    x="report_date",
    y="cases_reported",
    color="disease_name",
    markers=True,
    title="Monthly Incident Cases Over Time",
    labels={"report_date": "Timeline (Monthly)", "cases_reported": "Incident Cases", "disease_name": "Disease Entity"},
    color_discrete_sequence=px.colors.qualitative.Bold
)
fig_line.update_layout(height=420, hovermode="x unified", margin=dict(l=20, r=20, t=40, b=20))
st.plotly_chart(fig_line, use_container_width=True)

# 2. Multi-Year Overlapping YoY Comparison (OQ-09, BR-09)
st.subheader("🔄 Multi-Year Overlapping Annual Wave Cycles (OQ-09)")
c_l, c_r = st.columns([3, 2])

with c_l:
    yoy_agg = filtered.groupby(["report_month", "report_year"])["cases_reported"].sum().reset_index()
    yoy_agg["report_year"] = yoy_agg["report_year"].astype(str)
    
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
    fig_yoy.update_layout(height=380, margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig_yoy, use_container_width=True)

with c_r:
    st.write("**Year-over-Year (YoY %) Delta Table**")
    yoy_df = compute_yoy_change(filtered)
    if not yoy_df.empty:
        st.dataframe(yoy_df.style.background_gradient(cmap="coolwarm", axis=None).format("{:+.1f}%"), use_container_width=True)
    else:
        st.info("Insufficient longitudinal range to compute YoY delta.")

# 3. 12-Month Seasonal Transmission Heatmap (OQ-10, BR-06)
st.subheader("🌡️ 12-Month Seasonal Intensity Heatmap Matrix (OQ-10)")
seasonal_matrix = compute_seasonal_trend(filtered)

if not seasonal_matrix.empty:
    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    seasonal_matrix.columns = [month_names[m - 1] for m in seasonal_matrix.columns if 1 <= m <= 12]
    
    fig_heat = px.imshow(
        seasonal_matrix,
        color_continuous_scale="YlOrRd",
        title="Average Monthly Cases per Disease Entity",
        labels=dict(x="Calendar Month", y="Disease Entity", color="Avg Cases"),
        text_auto=".0f"
    )
    fig_heat.update_layout(height=350, margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig_heat, use_container_width=True)

render_insight_box(
    title="Seasonal Transmission Insight",
    text="Vector-borne illnesses (Dengue & Malaria) exhibit pronounced surges during the post-monsoon window (July to September), demanding therapeutic prepositioning 60 days in advance.",
    alert_type="warning"
)
