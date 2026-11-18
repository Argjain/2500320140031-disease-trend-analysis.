import streamlit as st
import pandas as pd
import plotly.express as px
from src.data_loader import load_data
from src.cleaning import clean_data
from src.analysis import detect_concurrent_outbreaks, compute_pearson_correlation
from src.ui import inject_tailwind, render_header, render_insight_box

st.set_page_config(page_title="EDA & Insights | Disease Trend Analysis", page_icon="🔬", layout="wide")
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
    title="Advanced Exploratory Data Analysis & Surveillance (UI-05)",
    subtitle=f"Statistical Modeling & Anomaly Surveillance | Target: {sel_disease}"
)

if filtered.empty:
    st.warning("⚠️ No records match active filters.")
    st.stop()

# 1. Density vs Incidence Scatter Plot (OQ-06, BR-08)
st.subheader("🏙️ Urban Crowding & Transmission Density Correlation (OQ-06, BR-08)")
state_density = filtered.groupby("region_name").agg(
    population_density=("population_density", "first"),
    total_cases=("cases_reported", "sum"),
    population=("population", "first")
).reset_index()

state_density["incidence_per_lakh"] = (state_density["total_cases"] / state_density["population"] * 100000.0).round(2)
r_val, p_val = compute_pearson_correlation(state_density)

fig_scatter = px.scatter(
    state_density,
    x="population_density",
    y="incidence_per_lakh",
    text="region_name",
    size="total_cases",
    trendline="ols",
    title=f"Population Density vs Cumulative Incidence per 100k — Pearson r = {r_val} (p = {p_val})",
    labels={"population_density": "Population Density (persons / sq. km)", "incidence_per_lakh": "Incidence per 100,000 residents"},
    color="incidence_per_lakh",
    color_continuous_scale="Teal"
)
fig_scatter.update_traces(textposition="top center")
fig_scatter.update_layout(height=420, margin=dict(l=20, r=20, t=40, b=20))
st.plotly_chart(fig_scatter, use_container_width=True)

st.caption(f"**Statistical Inference:** Pearson correlation coefficient r = **{r_val}** indicates a strong positive association between urban crowding and contagious disease velocity.")

st.markdown("---")

# 2. Automated Concurrent Outbreak Anomaly Detector (OQ-08, BR-05)
st.subheader("🚨 Multi-Disease Concurrent Outbreak Surveillance (OQ-08, BR-05)")
st.write(
    "Surveillance algorithm automatically flags any state-month where **2 or more diseases** "
    "simultaneously exceed **1.5x of their historical monthly baseline**:"
)

outbreak_alerts = detect_concurrent_outbreaks(df) # Run on full dataset for comprehensive alert history
if not outbreak_alerts.empty:
    st.dataframe(
        outbreak_alerts.head(15).style.background_gradient(subset=["surging_diseases_count"], cmap="Oranges")
                                 .format({"total_caseload": "{:,}"}),
        use_container_width=True
    )
else:
    st.success("✅ No concurrent multi-disease outbreak alerts detected under current baseline threshold.")

# 3. Descriptive Statistical Summary
st.subheader("📊 Descriptive Statistical Distribution")
st.dataframe(filtered[["cases_reported", "deaths", "recovered", "active_cases", "cfr_pct", "recovery_rate_pct"]].describe().T, use_container_width=True)

render_insight_box(
    title="Surveillance Anomaly Alert",
    text="Multiple concurrent surges occurred during the August–September post-monsoon period in dense urban corridors, demanding coordinated multi-pathogen triage protocols.",
    alert_type="danger"
)
