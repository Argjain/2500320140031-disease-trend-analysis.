import streamlit as st
import streamlit.components.v1 as components

TAILWIND_CDN = '<script src="https://cdn.tailwindcss.com"></script>'

def inject_tailwind():
    """Injects Tailwind CSS into an isolated iframe to pre-load utility classes."""
    components.html(f"{TAILWIND_CDN}<div style='display:none;'></div>", height=0)

def render_header(title: str, subtitle: str = ""):
    """Renders a styled responsive executive header banner."""
    html = f"""
    {TAILWIND_CDN}
    <div class="bg-gradient-to-r from-blue-900 to-sky-700 text-white px-6 py-4 rounded-xl shadow-lg mb-4 flex flex-col justify-center">
        <div class="flex items-center space-x-3">
            <span class="text-3xl">🏥</span>
            <div>
                <h1 class="text-2xl md:text-3xl font-extrabold tracking-tight">{title}</h1>
                <p class="text-blue-100 text-xs md:text-sm mt-0.5">{subtitle}</p>
            </div>
        </div>
    </div>
    """
    components.html(html, height=105)

def render_kpi_card(label: str, value: str, delta: str = None, icon: str = "📊", color: str = "#1A5376"):
    """Generates an HTML string for a Tailwind styled KPI stat card."""
    delta_html = ""
    if delta:
        is_pos = delta.startswith("+") or "growth" in delta.lower() or "surge" in delta.lower()
        delta_color = "text-emerald-600 bg-emerald-50" if not is_pos else "text-rose-600 bg-rose-50"
        delta_html = f'<div class="mt-2 text-xs font-semibold px-2 py-0.5 rounded-full inline-block {delta_color}">{delta}</div>'
    
    html = f"""
    {TAILWIND_CDN}
    <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-4 text-center hover:shadow-md transition-shadow">
        <div class="text-2xl mb-1">{icon}</div>
        <div class="text-xs uppercase tracking-wider font-semibold text-slate-500">{label}</div>
        <div class="text-2xl md:text-3xl font-black text-slate-800 mt-1" style="color:{color};">{value}</div>
        {delta_html}
    </div>
    """
    return html

def render_kpi_card_iframe(label: str, value: str, delta: str = None, icon: str = "📊", color: str = "#1A5376", height: int = 145):
    """Renders the KPI card directly inside an iframe component."""
    card_html = render_kpi_card(label, value, delta, icon, color)
    components.html(card_html, height=height)

def render_insight_box(title: str, text: str, alert_type: str = "info"):
    """Renders a styled analytical observation callout box."""
    colors = {
        "info": ("border-blue-500", "bg-blue-50", "text-blue-900", "ℹ️"),
        "warning": ("border-amber-500", "bg-amber-50", "text-amber-900", "⚠️"),
        "danger": ("border-rose-500", "bg-rose-50", "text-rose-900", "🚨"),
        "success": ("border-emerald-500", "bg-emerald-50", "text-emerald-900", "✅"),
    }
    b_col, bg_col, t_col, icon = colors.get(alert_type, colors["info"])
    html = f"""
    {TAILWIND_CDN}
    <div class="border-l-4 {b_col} {bg_col} p-4 rounded-r-lg shadow-xs my-3">
        <div class="flex items-center space-x-2">
            <span class="text-lg">{icon}</span>
            <span class="font-bold text-sm {t_col}">{title}</span>
        </div>
        <p class="text-xs md:text-sm text-slate-700 mt-1 leading-relaxed">{text}</p>
    </div>
    """
    components.html(html, height=95)
