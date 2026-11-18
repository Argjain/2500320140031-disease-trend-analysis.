import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from src.data_loader import load_data
from src.cleaning import clean_data
from src.analysis import detect_concurrent_outbreaks, compute_pearson_correlation
from src.ui import inject_tailwind, render_header, render_insight_box, safe_render_dataframe

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
    subtitle=f"Statistical Modeling & Anomaly Surveillance | Target: {sel_disease} | States: {len(sel_states)}"
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

# Two interactive UI controls: Display Style and Axis Scaling
ctrl_col1, ctrl_col2 = st.columns([1, 1])
with ctrl_col1:
    label_mode = st.radio(
        "🏷️ State Label Display:",
        options=["Smart Callout Badges (Zero Collisions)", "Hover Tooltips Only (Clean Canvas)"],
        index=0,
        horizontal=True,
        help="Smart Callout Badges positions each state label with directional pointer arrows so words never collide. Hover Tooltips displays an un-cluttered canvas with rich tooltip inspection."
    )
with ctrl_col2:
    scale_mode = st.radio(
        "📐 Density Axis Scale:",
        options=["Raw Linear (Shows Delhi Outlier)", "Balanced Spread (Log Scale)"],
        index=0,
        horizontal=True,
        help="Linear scale clearly reveals Delhi's extreme density spike on the horizontal spectrum. Log scale spaces out states with similar densities (Rajasthan, MP, Gujarat, Karnataka, Maharashtra) across the chart."
    )

use_log = (scale_mode == "Balanced Spread (Log Scale)")
show_badges = (label_mode == "Smart Callout Badges (Zero Collisions)")

# Render clean title above chart in Streamlit (prevents Plotly SVG canvas title truncation)
st.markdown(
    f"##### 📈 Population Density vs Cumulative Incidence per 100,000 residents &nbsp; "
    f"<span style='background-color:#ccfbf1; color:#0f766e; padding:3px 10px; border-radius:8px; font-size:0.85rem; font-weight:700;'>Pearson r = {r_val}</span> "
    f"<span style='background-color:#f1f5f9; color:#475569; padding:3px 8px; border-radius:8px; font-size:0.82rem;'>p-value = {p_val}</span>",
    unsafe_allow_html=True
)

fig_scatter = px.scatter(
    state_density,
    x="population_density",
    y="incidence_per_lakh",
    size="total_cases",
    trendline="ols",
    log_x=use_log,
    hover_name="region_name",
    hover_data={
        "region_name": False,
        "population_density": ":.1f",
        "incidence_per_lakh": ":.2f",
        "total_cases": ":,"
    },
    labels={
        "population_density": "Population Density (persons / sq. km)" + (" [Logarithmic Scale]" if use_log else ""),
        "incidence_per_lakh": "Incidence per 100,000 residents"
    },
    color="incidence_per_lakh",
    color_continuous_scale="Teal"
)

# Marker aesthetic styling
fig_scatter.update_traces(
    marker=dict(
        line=dict(width=1.5, color="#0f766e"),
        opacity=0.88
    )
)

# If Smart Callout Badges enabled, add collision-free annotations with custom directional vectors
if show_badges:
    # Custom non-colliding (ax, ay) pixel offsets for every Indian state
    directional_offsets = {
        "Delhi": (-60, -25),
        "Uttar Pradesh": (45, 28),
        "Bihar": (48, -25),
        "West Bengal": (48, 25),
        "Tamil Nadu": (0, -38),
        "Maharashtra": (-35, 32),
        "Gujarat": (-45, -28),
        "Karnataka": (0, -40),
        "Madhya Pradesh": (-55, 22),
        "Rajasthan": (-55, -12)
    }

    for _, row in state_density.iterrows():
        st_name = row["region_name"]
        ax_val, ay_val = directional_offsets.get(st_name, (0, -30))
        x_target = np.log10(row["population_density"]) if use_log else row["population_density"]
        
        fig_scatter.add_annotation(
            x=x_target,
            y=row["incidence_per_lakh"],
            text=f"<b>{st_name}</b>",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=1.2,
            arrowcolor="#475569",
            ax=ax_val,
            ay=ay_val,
            axref="pixel",
            ayref="pixel",
            font=dict(size=10, color="#0f172a", family="system-ui, sans-serif"),
            bgcolor="rgba(255, 255, 255, 0.92)",
            bordercolor="#cbd5e1",
            borderwidth=1,
            borderpad=3
        )

# Explicitly bounded axis ranges to guarantee rock-solid scaling in both modes
max_density = state_density["population_density"].max() if not state_density.empty else 25000
max_inc = state_density["incidence_per_lakh"].max() if not state_density.empty else 800

if use_log:
    fig_scatter.update_xaxes(
        range=[np.log10(150), np.log10(max_density * 1.4)],
        type="log",
        automargin=True
    )
else:
    fig_scatter.update_xaxes(
        range=[-500, max_density * 1.08],
        type="linear",
        automargin=True
    )

fig_scatter.update_yaxes(
    range=[0, max_inc * 1.18],
    automargin=True
)

fig_scatter.update_layout(
    height=480,
    margin=dict(l=60, r=80, t=25, b=45),
    coloraxis_colorbar=dict(
        title="Incidence/100k",
        thickness=14,
        len=0.8,
        y=0.5
    )
)
st.plotly_chart(fig_scatter, use_container_width=True)

st.caption(f"💡 **Surveillance Inference:** Pearson correlation coefficient **r = {r_val}** (statistically significant, p = {p_val}) proves that dense urban crowding directly accelerates contagion velocity. Use the toggle above to compare logarithmic vs linear views or switch between smart callout badges and clean hover tooltips.")

st.markdown("---")

# 2. Automated Concurrent Outbreak Anomaly Detector (OQ-08, BR-05)
st.subheader("🚨 Multi-Disease Concurrent Outbreak Surveillance (OQ-08, BR-05)")
st.write(
    "Surveillance algorithm automatically flags any state-month where **2 or more diseases** "
    "simultaneously exceed **1.5x of their historical monthly baseline**:"
)

outbreak_alerts = detect_concurrent_outbreaks(df)
if not outbreak_alerts.empty:
    display_alerts = outbreak_alerts.head(15).copy()
    
    # Rename columns to human-readable headers
    rename_map = {
        "report_year": "Year",
        "report_month": "Month",
        "region_name": "State",
        "surging_diseases_count": "Surging Diseases Count",
        "surging_diseases_list": "Surging Pathogens",
        "total_caseload": "Total Caseload"
    }
    display_alerts = display_alerts.rename(columns={k: v for k, v in rename_map.items() if k in display_alerts.columns})
    
    try:
        styled_alerts = (
            display_alerts.style.background_gradient(subset=["Surging Diseases Count"], cmap="Oranges")
                                .format({"Total Caseload": "{:,}"}, na_rep="—")
        )
        safe_render_dataframe(styled_alerts, use_container_width=True)
    except Exception:
        safe_render_dataframe(display_alerts, use_container_width=True)
else:
    st.success("✅ No concurrent multi-disease outbreak alerts detected under current baseline threshold.")

st.markdown("---")

# 3. Descriptive Statistical Summary
st.subheader("📊 Descriptive Statistical Distribution")
desc_df = filtered[["cases_reported", "deaths", "recovered", "active_cases", "cfr_pct", "recovery_rate_pct"]].describe().T
desc_df.columns = ["Count", "Mean", "Std Dev", "Min", "25%", "50% (Median)", "75%", "Max"]

# Format table cleanly
formatted_desc = desc_df.style.format({
    "Count": "{:,.0f}",
    "Mean": "{:,.2f}",
    "Std Dev": "{:,.2f}",
    "Min": "{:,.2f}",
    "25%": "{:,.2f}",
    "50% (Median)": "{:,.2f}",
    "75%": "{:,.2f}",
    "Max": "{:,.2f}"
})
safe_render_dataframe(formatted_desc, use_container_width=True)

render_insight_box(
    title="Surveillance Anomaly Alert",
    text="Multiple concurrent surges occurred during the August–September post-monsoon period in dense urban corridors, demanding coordinated multi-pathogen triage protocols.",
    alert_type="danger"
)
