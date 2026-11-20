import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import os
import tempfile

# Ensure matplotlib uses a writable temp cache directory to avoid Windows permission errors
os.environ["MPLCONFIGDIR"] = os.path.join(tempfile.gettempdir(), "matplotlib")

TAILWIND_CDN = '<script src="https://cdn.tailwindcss.com"></script>'

def inject_tailwind():
    """Injects global CSS rules into Streamlit DOM to ensure zero-clip responsive styling."""
    st.markdown(
        """
        <style>
        /* Global typography & layout smoothing */
        .block-container {
            padding-top: 1.8rem;
            padding-bottom: 2.5rem;
            padding-left: 2rem;
            padding-right: 2rem;
        }
        /* Prevent iframe bottom scrollbar flicker */
        iframe {
            border: none;
            overflow: hidden !important;
        }
        /* Ensure table text wraps cleanly without truncation */
        div[data-testid="stDataFrame"] div[role="grid"] {
            font-size: 0.88rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def render_header(title: str, subtitle: str = ""):
    """Renders a styled responsive executive header banner with dynamic height calculation."""
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        {TAILWIND_CDN}
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            html, body {{ margin: 0; padding: 0; background: transparent; overflow: hidden; font-family: system-ui, -apple-system, sans-serif; }}
            .header-banner {{
                background: linear-gradient(135deg, #0d233a 0%, #1a5376 55%, #0284c7 100%);
                border-radius: 12px;
                padding: 14px 20px;
                color: #ffffff;
                box-shadow: 0 4px 12px rgba(13, 35, 58, 0.12);
                display: flex;
                align-items: center;
                gap: 16px;
            }}
        </style>
    </head>
    <body>
        <div class="header-banner">
            <span style="font-size: 2.3rem; line-height: 1; flex-shrink: 0;">🏥</span>
            <div style="flex-grow: 1; min-width: 0;">
                <h1 style="font-size: 1.35rem; font-weight: 800; letter-spacing: -0.02em; line-height: 1.25; margin-bottom: 3px; color: #ffffff;">{title}</h1>
                <p style="color: #bae6fd; font-size: 0.82rem; line-height: 1.35; margin: 0;">{subtitle}</p>
            </div>
        </div>
    </body>
    </html>
    """
    # Ample height to prevent any text clipping on smaller viewports
    components.html(html, height=115)

def render_kpi_card(label: str, value: str, delta: str = None, icon: str = "📊", color: str = "#1A5376"):
    """Generates an HTML string for a Tailwind styled KPI stat card."""
    delta_html = ""
    if delta:
        is_pos = delta.startswith("+") or "growth" in delta.lower() or "surge" in delta.lower()
        delta_color = "color: #059669; background-color: #ecfdf5; border: 1px solid #a7f3d0;" if not is_pos else "color: #dc2626; background-color: #fef2f2; border: 1px solid #fecaca;"
        delta_html = f'<div style="margin-top: 6px; font-size: 0.72rem; font-weight: 700; padding: 2px 8px; border-radius: 9999px; display: inline-block; {delta_color}">{delta}</div>'
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            html, body {{ margin: 0; padding: 2px; background: transparent; overflow: hidden; font-family: system-ui, -apple-system, sans-serif; }}
            .card {{
                background: #ffffff;
                border-radius: 12px;
                border: 1px solid #e2e8f0;
                padding: 12px 10px;
                text-align: center;
                box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            }}
            .card-icon {{ font-size: 1.55rem; line-height: 1; margin-bottom: 3px; }}
            .card-label {{ font-size: 0.68rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: #64748b; }}
            .card-val {{ font-size: 1.5rem; font-weight: 900; line-height: 1.2; margin-top: 2px; }}
        </style>
    </head>
    <body>
        <div class="card">
            <div class="card-icon">{icon}</div>
            <div class="card-label">{label}</div>
            <div class="card-val" style="color:{color};">{value}</div>
            {delta_html}
        </div>
    </body>
    </html>
    """
    return html

def render_kpi_card_iframe(label: str, value: str, delta: str = None, icon: str = "📊", color: str = "#1A5376", height: int = 150):
    """Renders the KPI card directly inside an iframe component with adequate breathing room."""
    card_html = render_kpi_card(label, value, delta, icon, color)
    components.html(card_html, height=height)

def render_insight_box(title: str, text: str, alert_type: str = "info"):
    """Renders a styled analytical observation callout box with dynamic height to prevent text cutoff."""
    colors = {
        "info": ("#0284c7", "#f0f9ff", "#0369a1", "ℹ️"),
        "warning": ("#f59e0b", "#fffbeb", "#b45309", "⚠️"),
        "danger": ("#ef4444", "#fef2f2", "#b91c1c", "🚨"),
        "success": ("#10b981", "#ecfdf5", "#047857", "✅"),
    }
    b_col, bg_col, t_col, icon = colors.get(alert_type, colors["info"])
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            html, body {{ margin: 0; padding: 3px; background: transparent; font-family: system-ui, -apple-system, sans-serif; }}
            .box {{
                border-left: 4px solid {b_col};
                background-color: {bg_col};
                border-radius: 0 8px 8px 0;
                padding: 10px 14px;
                box-shadow: 0 1px 2px rgba(0,0,0,0.04);
            }}
            .box-title {{
                display: flex;
                align-items: center;
                gap: 6px;
                font-size: 0.84rem;
                font-weight: 700;
                color: {t_col};
                margin-bottom: 3px;
            }}
            .box-text {{
                font-size: 0.81rem;
                line-height: 1.42;
                color: #334155;
                margin: 0;
            }}
        </style>
    </head>
    <body>
        <div class="box">
            <div class="box-title">
                <span style="font-size: 1.05rem; line-height: 1;">{icon}</span>
                <span>{title}</span>
            </div>
            <p class="box-text">{text}</p>
        </div>
    </body>
    </html>
    """
    # Dynamic height calculation based on text character volume
    char_len = len(text)
    if char_len < 90:
        box_height = 95
    elif char_len < 160:
        box_height = 115
    elif char_len < 240:
        box_height = 135
    else:
        box_height = 160
        
    components.html(html, height=box_height)

def safe_render_dataframe(df_or_styler, use_container_width: bool = True):
    """Safely renders pandas dataframe or styler with automatic fallback if styling throws an error."""
    try:
        st.dataframe(df_or_styler, use_container_width=use_container_width)
    except Exception:
        if hasattr(df_or_styler, "data"):
            st.dataframe(df_or_styler.data, use_container_width=use_container_width)
        else:
            st.dataframe(df_or_styler, use_container_width=use_container_width)

def render_sidebar_filters(df: pd.DataFrame) -> pd.DataFrame:
    """
    Renders advanced analytical sidebar filters (Transmission Category, Specific Disease, 
    Geographic Zone, States, Years, Surveillance Authority) with quick scenario presets, 
    persistent session state, and returns the filtered DataFrame slice.
    """
    st.sidebar.markdown(
        """
        <div style="background: linear-gradient(135deg, #0F2B48, #1A5376); padding: 10px 14px; border-radius: 8px; margin-bottom: 12px; color: white;">
            <div style="font-size: 0.95rem; font-weight: 800; display: flex; align-items: center; gap: 6px;">
                <span>🎛️</span><span>Analytical Filters</span>
            </div>
            <div style="font-size: 0.72rem; color: #bae6fd; margin-top: 2px;">Multi-Dimensional Slicing & Drill-down</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # ── Quick Scenario Presets ──────────────────────────────────────────
    st.sidebar.markdown("**⚡ Quick Scenario Presets:**")
    cp1, cp2 = st.sidebar.columns(2)
    with cp1:
        if st.sidebar.button("🇮🇳 All India", use_container_width=True, key="preset_all"):
            st.session_state.selected_disease = "All Diseases"
            st.session_state.selected_category = "All Categories"
            st.session_state.selected_zone = "All Zones"
            st.session_state.selected_states = sorted(df["region_name"].dropna().unique().tolist())
            st.session_state.selected_year_range = (int(df["report_year"].min()), int(df["report_year"].max()))
            st.session_state.selected_source = "All Data Sources"
            st.rerun()
            
    with cp2:
        if st.sidebar.button("🌧️ Monsoon Surge", use_container_width=True, key="preset_monsoon"):
            st.session_state.selected_category = "Vector-borne"
            st.session_state.selected_disease = "All Diseases"
            st.session_state.selected_zone = "All Zones"
            st.session_state.selected_states = sorted(df["region_name"].dropna().unique().tolist())
            st.session_state.selected_year_range = (int(df["report_year"].min()), int(df["report_year"].max()))
            st.rerun()

    cp3, cp4 = st.sidebar.columns(2)
    with cp3:
        if st.sidebar.button("🏙️ Top Metros", use_container_width=True, key="preset_metros"):
            st.session_state.selected_disease = "All Diseases"
            st.session_state.selected_category = "All Categories"
            st.session_state.selected_zone = "All Zones"
            st.session_state.selected_states = ["Delhi", "Maharashtra", "West Bengal"]
            st.rerun()
            
    with cp4:
        if st.sidebar.button("❄️ Winter Airborne", use_container_width=True, key="preset_winter"):
            st.session_state.selected_category = "Airborne"
            st.session_state.selected_disease = "All Diseases"
            st.session_state.selected_zone = "All Zones"
            st.session_state.selected_states = sorted(df["region_name"].dropna().unique().tolist())
            st.rerun()

    st.sidebar.markdown("---")

    # ── 1. Transmission Category Filter ────────────────────────────────
    categories = ["All Categories"] + sorted(df["disease_category"].dropna().unique().tolist())
    if "selected_category" not in st.session_state:
        st.session_state.selected_category = "All Categories"
        
    sel_category = st.sidebar.selectbox(
        "1. Transmission Category:",
        options=categories,
        index=categories.index(st.session_state.selected_category) if st.session_state.selected_category in categories else 0,
        key="sb_category"
    )
    st.session_state.selected_category = sel_category

    # ── 2. Specific Disease Filter (Filtered by Category) ───────────────
    if sel_category != "All Categories":
        avail_diseases = sorted(df[df["disease_category"] == sel_category]["disease_name"].dropna().unique().tolist())
    else:
        avail_diseases = sorted(df["disease_name"].dropna().unique().tolist())
    all_diseases = ["All Diseases"] + avail_diseases
    
    if "selected_disease" not in st.session_state or st.session_state.selected_disease not in all_diseases:
        st.session_state.selected_disease = "All Diseases"

    sel_disease = st.sidebar.selectbox(
        "2. Specific Disease Target:",
        options=all_diseases,
        index=all_diseases.index(st.session_state.selected_disease) if st.session_state.selected_disease in all_diseases else 0,
        key="sb_disease"
    )
    st.session_state.selected_disease = sel_disease

    # ── 3. Geographic Zone Filter ───────────────────────────────────────
    all_zones = ["All Zones"] + sorted(df["zone"].dropna().unique().tolist())
    if "selected_zone" not in st.session_state:
        st.session_state.selected_zone = "All Zones"

    sel_zone = st.sidebar.selectbox(
        "3. Geographic Zone:",
        options=all_zones,
        index=all_zones.index(st.session_state.selected_zone) if st.session_state.selected_zone in all_zones else 0,
        key="sb_zone"
    )
    st.session_state.selected_zone = sel_zone

    # ── 4. Indian States Filter (Filtered by Zone) ─────────────────────
    if sel_zone != "All Zones":
        avail_states = sorted(df[df["zone"] == sel_zone]["region_name"].dropna().unique().tolist())
    else:
        avail_states = sorted(df["region_name"].dropna().unique().tolist())

    if "selected_states" not in st.session_state:
        st.session_state.selected_states = avail_states
    else:
        current_valid = [s for s in st.session_state.selected_states if s in avail_states]
        if not current_valid:
            current_valid = avail_states
        st.session_state.selected_states = current_valid

    sel_states = st.sidebar.multiselect(
        "4. Indian States / UTs:",
        options=avail_states,
        default=st.session_state.selected_states,
        key="sb_states"
    )
    st.session_state.selected_states = sel_states if sel_states else avail_states

    # ── 5. Observation Timeline Slider ──────────────────────────────────
    min_yr = int(df["report_year"].min())
    max_yr = int(df["report_year"].max())
    if "selected_year_range" not in st.session_state:
        st.session_state.selected_year_range = (min_yr, max_yr)

    sel_years = st.sidebar.slider(
        "5. Observation Timeline (Years):",
        min_value=min_yr,
        max_value=max_yr,
        value=st.session_state.selected_year_range,
        key="sb_years"
    )
    st.session_state.selected_year_range = sel_years

    # ── 6. Surveillance Authority / Source ──────────────────────────────
    sources = ["All Data Sources"] + sorted(df["data_source"].dropna().unique().tolist())
    if "selected_source" not in st.session_state:
        st.session_state.selected_source = "All Data Sources"

    sel_source = st.sidebar.selectbox(
        "6. Surveillance Authority:",
        options=sources,
        index=sources.index(st.session_state.selected_source) if st.session_state.selected_source in sources else 0,
        key="sb_source"
    )
    st.session_state.selected_source = sel_source

    # ── 7. Reset Action ────────────────────────────────────────────────
    if st.sidebar.button("🔄 Reset All Filters", use_container_width=True, key="reset_all_btn"):
        st.session_state.selected_disease = "All Diseases"
        st.session_state.selected_category = "All Categories"
        st.session_state.selected_zone = "All Zones"
        st.session_state.selected_states = sorted(df["region_name"].dropna().unique().tolist())
        st.session_state.selected_year_range = (min_yr, max_yr)
        st.session_state.selected_source = "All Data Sources"
        st.rerun()

    # ── Filter Application ─────────────────────────────────────────────
    filtered = df.copy()
    if st.session_state.selected_category != "All Categories":
        filtered = filtered[filtered["disease_category"] == st.session_state.selected_category]
    if st.session_state.selected_disease != "All Diseases":
        filtered = filtered[filtered["disease_name"] == st.session_state.selected_disease]
    if st.session_state.selected_zone != "All Zones":
        filtered = filtered[filtered["zone"] == st.session_state.selected_zone]
    if st.session_state.selected_source != "All Data Sources":
        filtered = filtered[filtered["data_source"] == st.session_state.selected_source]
        
    filtered = filtered[
        (filtered["region_name"].isin(st.session_state.selected_states)) &
        (filtered["report_year"] >= st.session_state.selected_year_range[0]) &
        (filtered["report_year"] <= st.session_state.selected_year_range[1])
    ]

    # ── Live Active Slice Metadata ─────────────────────────────────────
    st.sidebar.markdown(
        f"""
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 10px; margin-top: 10px; font-size: 0.76rem; color: #475569;">
            <div style="font-weight: 700; color: #0f2b48; margin-bottom: 4px;">📊 Active Filter Slice:</div>
            <div>• Records: <b>{len(filtered):,}</b> / {len(df):,} ({len(filtered)/len(df)*100:.1f}%)</div>
            <div>• States: <b>{len(st.session_state.selected_states)}</b> selected</div>
            <div>• Timeline: <b>{st.session_state.selected_year_range[0]}–{st.session_state.selected_year_range[1]}</b></div>
            <div>• Caseload: <b>{int(filtered['cases_reported'].sum()):,}</b> cases</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.sidebar.markdown("---")
    st.sidebar.caption("Project P-01 | ABES MCA 2nd Year Data Analytics")
    st.sidebar.caption("Student: **Arg Jain** (2500320140031)")
    st.sidebar.caption("Mentor: **Ms. Kalpana Dwivedi**")

    return filtered
