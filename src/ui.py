import streamlit as st
import streamlit.components.v1 as components
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
