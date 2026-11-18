import streamlit as st
import pandas as pd
import plotly.express as px
from src.data_loader import load_data
from src.cleaning import clean_data
from src.ui import inject_tailwind, render_header, render_kpi_card_iframe, render_insight_box

st.set_page_config(page_title="Overview | Disease Trend Analysis", page_icon="📊", layout="wide")
inject_tailwind()

# Load & Clean Data
raw_df = load_data()
df, _ = clean_data(raw_df)

# Retrieve Filter State from Session
sel_disease = st.session_state.get("selected_disease", "All Diseases")
sel_states = st.session_state.get("selected_states", sorted(df["region_name"].unique().tolist()))
sel_years = st.session_state.get("selected_year_range", (int(df["report_year"].min()), int(df["report_year"].max())))

# Apply Filters
filtered = df.copy()
if sel_disease != "All Diseases":
    filtered = filtered[filtered["disease_name"] == sel_disease]
filtered = filtered[
    (filtered["region_name"].isin(sel_states)) &
    (filtered["report_year"] >= sel_years[0]) &
    (filtered["report_year"] <= sel_years[1])
]

render_header(
    title="Executive Overview & KPI Cockpit (UI-01)",
    subtitle=f"Target: {sel_disease} | Timeline: {sel_years[0]}–{sel_years[1]} | Filtered Records: {len(filtered):,}"
)

if filtered.empty:
    st.warning("⚠️ No records match the active filter criteria. Please broaden your selection in the sidebar.")
    st.stop()

# Row 1: KPI Stat Cards
tot_cases = int(filtered["cases_reported"].sum())
tot_deaths = int(filtered["deaths"].sum())
tot_rec = int(filtered["recovered"].sum())
cfr = round((tot_deaths / tot_cases * 100.0), 2) if tot_cases > 0 else 0.0

c1, c2, c3, c4 = st.columns(4)
with c1:
    render_kpi_card_iframe("Total Cases", f"{tot_cases:,}", delta="Active Filter Slice", icon="🦠", color="#1A5376")
with c2:
    render_kpi_card_iframe("Total Fatalities", f"{tot_deaths:,}", delta=f"CFR: {cfr}%", icon="⚠️", color="#C0392B")
with c3:
    render_kpi_card_iframe("Recovered Cases", f"{tot_rec:,}", delta=f"{round(tot_rec/tot_cases*100, 1) if tot_cases else 0}% Recov", icon="🩺", color="#1E8B4C")
with c4:
    render_kpi_card_iframe("Active Cases", f"{int(filtered['active_cases'].sum()):,}", delta="Ongoing In-Care", icon="🏥", color="#E67E22")

st.markdown("---")

# Row 2: Regional Case Volume Ranking (Horizontal Bar Chart)
st.subheader("📍 State-Level Morbidity Burden (OQ-02, BR-02)")
reg_group = filtered.groupby("region_name")["cases_reported"].sum().reset_index()
reg_group = reg_group.sort_values(by="cases_reported", ascending=True)

fig_bar = px.bar(
    reg_group,
    x="cases_reported",
    y="region_name",
    orientation="h",
    title=f"Total Morbidity by State — {sel_disease}",
    labels={"cases_reported": "Total Incident Cases", "region_name": "Indian State"},
    color="cases_reported",
    color_continuous_scale="Blues",
    text_auto=",.0f"
)
fig_bar.update_layout(height=420, margin=dict(l=20, r=20, t=40, b=20))
st.plotly_chart(fig_bar, use_container_width=True)

# Row 3: Cross-State CFR Benchmark Table (OQ-05, BR-03)
st.subheader("📋 State-Level Epidemiological Performance Summary")
summary_tbl = filtered.groupby("region_name").agg(
    Total_Cases=("cases_reported", "sum"),
    Deaths=("deaths", "sum"),
    Recoveries=("recovered", "sum"),
    Population=("population", "first")
).reset_index()

summary_tbl["CFR (%)"] = (summary_tbl["Deaths"] / summary_tbl["Total_Cases"].replace(0, 1) * 100.0).round(2)
summary_tbl["Recovery (%)"] = (summary_tbl["Recoveries"] / summary_tbl["Total_Cases"].replace(0, 1) * 100.0).round(2)
summary_tbl["Incidence/Lakh"] = (summary_tbl["Total_Cases"] / summary_tbl["Population"] * 100000.0).round(2)
summary_tbl = summary_tbl.sort_values(by="Total_Cases", ascending=False)

st.dataframe(
    summary_tbl.style.background_gradient(subset=["CFR (%)"], cmap="Reds")
                     .background_gradient(subset=["Recovery (%)"], cmap="Greens")
                     .format({"Total_Cases": "{:,}", "Deaths": "{:,}", "Recoveries": "{:,}", "Population": "{:,}", "CFR (%)": "{:.2f}%", "Recovery (%)": "{:.2f}%", "Incidence/Lakh": "{:.2f}"}),
    use_container_width=True
)

render_insight_box(
    title="Key Surveillance Finding",
    text=f"Higher case volumes are concentrated in dense urban zones (Maharashtra and Delhi), while Case Fatality Rates reflect hospital management capacity.",
    alert_type="info"
)
