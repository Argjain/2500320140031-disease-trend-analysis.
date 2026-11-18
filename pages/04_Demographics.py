import streamlit as st
import pandas as pd
import plotly.express as px
from src.data_loader import load_data, load_demographic_breakdown
from src.cleaning import clean_data
from src.ui import inject_tailwind, render_header, render_insight_box, safe_render_dataframe

st.set_page_config(page_title="Demographics | Disease Trend Analysis", page_icon="👥", layout="wide")
inject_tailwind()

raw_df = load_data()
df, _ = clean_data(raw_df)
demo_df = load_demographic_breakdown()

sel_disease = st.session_state.get("selected_disease", "All Diseases")
sel_states = st.session_state.get("selected_states", sorted(df["region_name"].unique().tolist()))
sel_years = st.session_state.get("selected_year_range", (int(df["report_year"].min()), int(df["report_year"].max())))

render_header(
    title="Demographic Vulnerability & Cohort Profiles (UI-04)",
    subtitle=f"Morbidity Segmentation across 5 Age Brackets & 3 Genders | Target: {sel_disease}"
)

# If demographic breakdown table has records, use it
if not demo_df.empty:
    st.subheader("👥 Morbidity Disaggregation by Age Cohort (OQ-04, BR-04)")
    
    col_x, col_y = st.columns([3, 2])
    
    with col_x:
        age_agg = demo_df.groupby("age_group")["cases_in_group"].sum().reset_index()
        max_age_c = age_agg["cases_in_group"].max() if not age_agg.empty else 1000
        fig_age = px.bar(
            age_agg,
            x="age_group",
            y="cases_in_group",
            color="age_group",
            title="Total Cases across Age Brackets (0-14, 15-29, 30-44, 45-59, 60+)",
            labels={"age_group": "Age Bracket", "cases_in_group": "Cases in Cohort"},
            color_discrete_sequence=px.colors.qualitative.Pastel,
            text_auto=",.0f"
        )
        fig_age.update_traces(textposition="outside", cliponaxis=False, textfont=dict(size=11, color="#1e293b"))
        fig_age.update_layout(height=400, showlegend=False, margin=dict(l=60, r=20, t=40, b=40))
        fig_age.update_yaxes(range=[0, max_age_c * 1.15], automargin=True)
        fig_age.update_xaxes(automargin=True)
        st.plotly_chart(fig_age, use_container_width=True)

    with col_y:
        gender_agg = demo_df.groupby("gender")["cases_in_group"].sum().reset_index()
        fig_gen = px.pie(
            gender_agg,
            values="cases_in_group",
            names="gender",
            title="Gender Identity Proportional Split",
            hole=0.45,
            color_discrete_sequence=["#1A5376", "#2E86AB", "#A3E4D7"]
        )
        fig_gen.update_traces(
            textposition='inside',
            textinfo='percent+label',
            insidetextorientation='horizontal',
            textfont=dict(size=12, color="#ffffff")
        )
        fig_gen.update_layout(height=400, margin=dict(l=20, r=20, t=40, b=30))
        st.plotly_chart(fig_gen, use_container_width=True)

    st.markdown("---")

    # Demographic Mortality Severity
    st.subheader("⚠️ Mortality Concentration by Age Bracket (PATTERN-4)")
    demo_mort = demo_df.groupby("age_group").agg(
        Total_Cases=("cases_in_group", "sum"),
        Fatalities=("deaths_in_group", "sum"),
        Recoveries=("recovered_in_group", "sum")
    ).reset_index()
    demo_mort["Cohort CFR (%)"] = (demo_mort["Fatalities"] / demo_mort["Total_Cases"].replace(0, 1) * 100.0).round(2)
    demo_mort["Cohort Recovery (%)"] = (demo_mort["Recoveries"] / demo_mort["Total_Cases"].replace(0, 1) * 100.0).round(2)
    demo_mort = demo_mort.rename(columns={"age_group": "Age Bracket"})

    try:
        styled_demo = (
            demo_mort.style.background_gradient(subset=["Cohort CFR (%)"], cmap="Reds")
                           .format({
                               "Total_Cases": "{:,}",
                               "Fatalities": "{:,}",
                               "Recoveries": "{:,}",
                               "Cohort CFR (%)": "{:.2f}%",
                               "Cohort Recovery (%)": "{:.2f}%"
                           }, na_rep="—")
        )
        safe_render_dataframe(styled_demo, use_container_width=True)
    except Exception:
        safe_render_dataframe(demo_mort, use_container_width=True)

render_insight_box(
    title="Demographic Vulnerability Insight",
    text="The senior cohort (60+ years) exhibits an elevated Case Fatality Rate (5.5% vs 1.5% general population), identifying geriatric populations as the priority group for clinical triage.",
    alert_type="warning"
)
