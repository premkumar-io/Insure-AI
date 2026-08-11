import streamlit as st
import requests
import os
import math
import textwrap
import pandas as pd
import altair as alt
import base64
from typing import Tuple, Dict, Any, Optional

# ------------------------------------------------------------------------------
# API & System Configuration
# ------------------------------------------------------------------------------
API_URL = os.getenv("API_URL", "http://localhost:8000/predict")
HEALTH_URL = API_URL.replace("/predict", "/health")

# Page Configuration
st.set_page_config(
    page_title="Insure AI | Enterprise AI Insurance Risk Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------------------------------------------------------
# Image Helper
# ------------------------------------------------------------------------------
def get_base64_image(image_path: str) -> str:
    """Helper to convert local image to base64 for inline HTML rendering."""
    if os.path.exists(image_path):
        try:
            with open(image_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode("utf-8")
        except Exception:
            pass
    return ""

logo_b64 = get_base64_image("logo.png")

# ------------------------------------------------------------------------------
# Session State Initialization
# ------------------------------------------------------------------------------
if "preset" not in st.session_state:
    st.session_state["preset"] = "Young Executive"
    st.session_state["age"] = 28
    st.session_state["weight"] = 68.0
    st.session_state["height_m"] = 1.75
    st.session_state["height_ft"] = 5
    st.session_state["height_in"] = 9
    st.session_state["unit_mode"] = "Meters (m)"
    st.session_state["income_lpa"] = 14.0
    st.session_state["smoker"] = False
    st.session_state["city"] = "Bangalore"
    st.session_state["occupation"] = "private_job"
    st.session_state["last_result"] = None
    st.session_state["api_error"] = None

if "theme_mode" not in st.session_state:
    st.session_state["theme_mode"] = "💻 System Default"

# ------------------------------------------------------------------------------
# Dynamic Theme System & Custom Navbar CSS
# ------------------------------------------------------------------------------
mode = st.session_state["theme_mode"]

dark_css_snippet = """
    .stApp { background-color: #090d16; color: #f1f5f9; }
    .nav-banner {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.85) 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 12px 35px -10px rgba(0, 0, 0, 0.6);
    }
    .brand-heading {
        background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .brand-sub { color: #94a3b8; }
    .nav-chip {
        background: rgba(255, 255, 255, 0.05);
        color: #cbd5e1;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .nav-chip:hover {
        background: rgba(255, 255, 255, 0.1);
        color: #ffffff;
    }
    .status-badge-on {
        background: rgba(16, 185, 129, 0.15);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.4);
    }
    .status-badge-off {
        background: rgba(239, 68, 68, 0.15);
        color: #f87171;
        border: 1px solid rgba(239, 68, 68, 0.4);
    }
    .card-title { color: #f8fafc; }
    .result-card-low { background: linear-gradient(135deg, rgba(6, 78, 59, 0.4) 0%, rgba(15, 23, 42, 0.9) 100%); border: 1.5px solid #10b981; box-shadow: 0 12px 30px -10px rgba(16, 185, 129, 0.25); }
    .result-card-medium { background: linear-gradient(135deg, rgba(120, 53, 15, 0.4) 0%, rgba(15, 23, 42, 0.9) 100%); border: 1.5px solid #f59e0b; box-shadow: 0 12px 30px -10px rgba(245, 158, 11, 0.25); }
    .result-card-high { background: linear-gradient(135deg, rgba(127, 29, 29, 0.4) 0%, rgba(15, 23, 42, 0.9) 100%); border: 1.5px solid #ef4444; box-shadow: 0 12px 30px -10px rgba(239, 68, 68, 0.25); }
    .res-label { color: #94a3b8; }
    .metric-box { background: rgba(30, 41, 59, 0.5); border: 1px solid rgba(255, 255, 255, 0.06); }
    .metric-val { color: #38bdf8; }
    .metric-sub { color: #94a3b8; }
    .preview-panel {
        background: rgba(15, 23, 42, 0.6);
        border: 1px dashed rgba(255, 255, 255, 0.12);
        border-radius: 16px;
        padding: 24px;
    }
    div.stButton > button { background: linear-gradient(135deg, #2563eb 0%, #4f46e5 100%) !important; color: #ffffff !important; box-shadow: 0 10px 25px -5px rgba(79, 70, 229, 0.4) !important; }
    .disclaimer-box { background: rgba(30, 41, 59, 0.4); border-left: 3px solid #64748b; color: #94a3b8; }
"""

light_css_snippet = """
    .stApp { background-color: #f8fafc; color: #0f172a; }
    .nav-banner {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        box-shadow: 0 6px 25px rgba(0, 0, 0, 0.06);
    }
    .brand-heading {
        background: linear-gradient(135deg, #0284c7 0%, #4338ca 50%, #7e22ce 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .brand-sub { color: #64748b; }
    .nav-chip {
        background: #f1f5f9;
        color: #475569;
        border: 1px solid #e2e8f0;
    }
    .nav-chip:hover {
        background: #e2e8f0;
        color: #0f172a;
    }
    .status-badge-on {
        background: #ecfdf5;
        color: #059669;
        border: 1px solid #a7f3d0;
    }
    .status-badge-off {
        background: #fef2f2;
        color: #dc2626;
        border: 1px solid #fecaca;
    }
    .card-title { color: #0f172a; }
    .result-card-low { background: linear-gradient(135deg, #ecfdf5 0%, #ffffff 100%); border: 1.5px solid #10b981; box-shadow: 0 10px 25px -5px rgba(16, 185, 129, 0.15); }
    .result-card-medium { background: linear-gradient(135deg, #fffbeb 0%, #ffffff 100%); border: 1.5px solid #f59e0b; box-shadow: 0 10px 25px -5px rgba(245, 158, 11, 0.15); }
    .result-card-high { background: linear-gradient(135deg, #fef2f2 0%, #ffffff 100%); border: 1.5px solid #ef4444; box-shadow: 0 10px 25px -5px rgba(239, 68, 68, 0.15); }
    .res-label { color: #64748b; }
    .metric-box { background: #ffffff; border: 1px solid #e2e8f0; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05); }
    .metric-val { color: #0284c7; }
    .metric-sub { color: #64748b; }
    .preview-panel {
        background: #ffffff;
        border: 1px dashed #cbd5e1;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
    }
    div.stButton > button { background: linear-gradient(135deg, #0284c7 0%, #4338ca 100%) !important; color: #ffffff !important; box-shadow: 0 8px 20px -5px rgba(67, 56, 202, 0.3) !important; }
    .disclaimer-box { background: #f1f5f9; border-left: 3px solid #64748b; color: #475569; }
"""

common_css_header = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    /* Keyframes for Pulsing Status Dot */
    @keyframes pulse-ring {
        0% { transform: scale(0.95); opacity: 0.8; }
        50% { transform: scale(1.25); opacity: 1; }
        100% { transform: scale(0.95); opacity: 0.8; }
    }

    .pulse-dot-green {
        width: 8px;
        height: 8px;
        background-color: #10b981;
        border-radius: 50%;
        display: inline-block;
        animation: pulse-ring 2s infinite ease-in-out;
        box-shadow: 0 0 10px #10b981;
    }

    .pulse-dot-red {
        width: 8px;
        height: 8px;
        background-color: #ef4444;
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 10px #ef4444;
    }

    /* Top Professional Navbar */
    .nav-banner {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-radius: 18px;
        padding: 16px 28px;
        margin-bottom: 22px;
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        flex-wrap: wrap;
        gap: 16px;
    }

    .brand-section {
        display: flex;
        align-items: center;
        gap: 16px;
    }

    .brand-heading {
        font-size: 1.85rem;
        font-weight: 800;
        letter-spacing: -0.035em;
        line-height: 1.2;
    }

    .brand-sub {
        font-size: 0.88rem;
        font-weight: 400;
        margin-top: 2px;
    }

    .nav-links {
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .nav-chip {
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 600;
        text-decoration: none !important;
        transition: all 0.2s ease-in-out;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }

    .status-badge-on, .status-badge-off {
        padding: 7px 16px;
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 8px;
    }

    /* Custom Sleek Dropdown Select Box Styling */
    div[data-baseweb="select"] > div {
        border-radius: 12px !important;
        border: 1.5px solid rgba(56, 189, 248, 0.25) !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.08) !important;
    }
    div[data-baseweb="select"] > div:hover, div[data-baseweb="select"] > div:focus-within {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 0 3.5px rgba(56, 189, 248, 0.25), 0 6px 20px rgba(0, 0, 0, 0.15) !important;
        transform: translateY(-1px) !important;
    }
    div[data-baseweb="select"] span {
        font-weight: 700 !important;
        font-size: 0.92rem !important;
        letter-spacing: -0.01em !important;
    }

    .card-title { font-size: 1.15rem; font-weight: 700; margin-bottom: 16px; display: flex; align-items: center; gap: 8px; }
    .res-val { font-size: 2.5rem; font-weight: 800; margin: 8px 0; letter-spacing: -0.02em; }
    .res-label { font-size: 0.85rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; }
    .metric-box { border-radius: 12px; padding: 14px 18px; text-align: center; }
    .metric-val { font-size: 1.3rem; font-weight: 700; }
    .metric-sub { font-size: 0.8rem; margin-top: 2px; }
    div.stButton > button { font-weight: 700 !important; font-size: 1.05rem !important; border-radius: 12px !important; border: none !important; padding: 14px 28px !important; transition: all 0.2s ease-in-out !important; }
    div.stButton > button:hover { transform: translateY(-2px) !important; filter: brightness(1.1) !important; }
    .disclaimer-box { padding: 12px 16px; border-radius: 0 8px 8px 0; font-size: 0.82rem; line-height: 1.5; margin-top: 16px; }
"""

if mode == "🌙 Dark":
    full_css = common_css_header + dark_css_snippet + "</style>"
    is_dark = True
elif mode == "☀️ Light":
    full_css = common_css_header + light_css_snippet + "</style>"
    is_dark = False
else:
    # System Default
    full_css = common_css_header + f"""
    @media (prefers-color-scheme: dark) {{ {dark_css_snippet} }}
    @media (prefers-color-scheme: light) {{ {light_css_snippet} }}
    </style>
    """
    is_dark = True

st.markdown(full_css, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# Helper Functions & Backend Connectivity
# ------------------------------------------------------------------------------
def check_backend_health() -> Tuple[bool, Optional[str]]:
    """Query FastAPI /health endpoint to check server availability."""
    try:
        r = requests.get(HEALTH_URL, timeout=2.5)
        if r.status_code == 200 and r.json().get("status") == "OK":
            return True, r.json().get("version", "2.0.0")
    except Exception:
        pass
    return False, None

def apply_preset(preset_name: str, age: int, weight: float, height_m: float, income: float, smoker: bool, city: str, occ: str):
    st.session_state["preset"] = preset_name
    st.session_state["age"] = age
    st.session_state["weight"] = weight
    st.session_state["height_m"] = height_m
    total_inches = round(height_m * 39.3701)
    st.session_state["height_ft"] = total_inches // 12
    st.session_state["height_in"] = total_inches % 12
    st.session_state["income_lpa"] = income
    st.session_state["smoker"] = smoker
    st.session_state["city"] = city
    st.session_state["occupation"] = occ
    st.session_state["last_result"] = None
    st.session_state["api_error"] = None

def reset_form():
    apply_preset("Young Executive", 28, 68.0, 1.75, 14.0, False, "Bangalore", "private_job")

# Check backend status
is_online, api_version = check_backend_health()

# ------------------------------------------------------------------------------
# Sleek & Professional Top Navbar Banner (Insure AI Separated)
# ------------------------------------------------------------------------------
if logo_b64:
    logo_element = f'<img src="data:image/png;base64,{logo_b64}" style="height: 44px; width: 44px; border-radius: 12px; object-fit: cover; box-shadow: 0 4px 15px rgba(56, 189, 248, 0.35); border: 1.5px solid rgba(255,255,255,0.2);" />'
else:
    logo_element = '<div style="height: 44px; width: 44px; border-radius: 12px; background: linear-gradient(135deg, #0284c7, #4338ca); display: flex; align-items: center; justify-content: center; font-size: 1.5rem; box-shadow: 0 4px 15px rgba(2, 132, 199, 0.35);">🛡️</div>'

if is_online:
    status_badge_html = f'<span class="status-badge-on"><span class="pulse-dot-green"></span>API Connected (v{api_version})</span>'
else:
    status_badge_html = '<span class="status-badge-off"><span class="pulse-dot-red"></span>API Offline</span>'

badge_color = "#38bdf8" if is_dark else "#0284c7"
badge_bg = "rgba(56, 189, 248, 0.15)" if is_dark else "#e0f2fe"
badge_border = "rgba(56, 189, 248, 0.3)" if is_dark else "#bae6fd"

nav_html = textwrap.dedent(f"""
<div class="nav-banner">
<div class="brand-section">
{logo_element}
<div>
<div class="brand-heading">
Insure AI
<span style="font-size: 0.72rem; font-weight: 700; color: {badge_color}; background: {badge_bg}; padding: 3px 10px; border-radius: 9999px; border: 1px solid {badge_border}; vertical-align: middle; margin-left: 6px;">
ENTERPRISE v2.0
</span>
</div>
<div class="brand-sub">AI-Powered Insurance Premium Risk Analytics & Underwriting Platform</div>
</div>
</div>
<div class="nav-links">
<span class="nav-chip">🛡️ Risk Analytics</span>
<span class="nav-chip">⚡ Random Forest ML</span>
<a href="http://localhost:8000/docs" target="_blank" class="nav-chip" style="color: inherit;">📡 OpenAPI Docs ↗</a>
</div>
<div>
{status_badge_html}
</div>
</div>
""")

st.markdown(nav_html, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# Sidebar Controls, Theme Switcher & Preset Profiles
# ------------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🎨 Theme Mode")
    theme_options = ["💻 System Default", "🌙 Dark", "☀️ Light"]
    default_idx = theme_options.index(st.session_state["theme_mode"]) if st.session_state["theme_mode"] in theme_options else 0
    selected_theme = st.selectbox(
        "Select Theme Mode",
        options=theme_options,
        index=default_idx,
        label_visibility="collapsed"
    )
    if selected_theme != st.session_state["theme_mode"]:
        st.session_state["theme_mode"] = selected_theme
        st.rerun()

    st.markdown("---")
    st.markdown("### ⚡ Quick Applicant Profiles")
    st.caption("Select a pre-configured scenario to auto-populate form:")

    p1, p2 = st.columns(2)
    with p1:
        if st.button("👨‍💼 Young Exec", use_container_width=True):
            apply_preset("Young Executive", 28, 68.0, 1.75, 14.0, False, "Bangalore", "private_job")
    with p2:
        if st.button("🚬 High Risk", use_container_width=True):
            apply_preset("High-Risk Smoker", 46, 94.0, 1.68, 12.0, True, "Delhi", "business_owner")

    p3, p4 = st.columns(2)
    with p3:
        if st.button("🏃 Fitness Pro", use_container_width=True):
            apply_preset("Fitness Enthusiast", 31, 62.0, 1.78, 18.0, False, "Pune", "freelancer")
    with p4:
        if st.button("👴 Senior", use_container_width=True):
            apply_preset("Senior Citizen", 64, 72.0, 1.65, 7.5, False, "Jaipur", "retired")

    st.markdown("---")
    st.markdown("### ⚙️ System Settings")
    st.write(f"**Backend Endpoint:** `{API_URL}`")
    st.write("**Model Engine:** Random Forest Classifier")
    st.write("**Environment:** Production-Ready")

    st.markdown("---")
    if st.button("🔄 Reset Assessment", use_container_width=True):
        reset_form()
        st.rerun()

# ------------------------------------------------------------------------------
# Main Application Content Grid (Balanced Alignment)
# ------------------------------------------------------------------------------
col_form, col_output = st.columns([1.1, 1], gap="medium")

with col_form:
    st.markdown('<div class="card-title">📋 Applicant Demographics & Health Parameters</div>', unsafe_allow_html=True)
    
    # Form Row 1: Age & Weight
    r1_c1, r1_c2 = st.columns(2)
    with r1_c1:
        age = st.number_input(
            "Age (Years)",
            min_value=1,
            max_value=119,
            value=int(st.session_state["age"]),
            step=1,
            help="Applicant age must be between 1 and 119 years."
        )
    with r1_c2:
        weight = st.number_input(
            "Weight (kg)",
            min_value=1.0,
            max_value=300.0,
            value=float(st.session_state["weight"]),
            step=0.5,
            help="Body weight in kilograms."
        )

    # Form Row 2: Height Unit Toggle & Input
    r2_c1, r2_c2 = st.columns(2)
    with r2_c1:
        unit_mode = st.radio(
            "Height Unit System",
            options=["Meters (m)", "Feet & Inches (ft/in)"],
            horizontal=True
        )

    with r2_c2:
        if unit_mode == "Meters (m)":
            height_m = st.number_input(
                "Height (meters)",
                min_value=0.50,
                max_value=2.50,
                value=float(st.session_state["height_m"]),
                step=0.01,
                help="Height in meters (0.50 m - 2.50 m)."
            )
        else:
            ft_col, in_col = st.columns(2)
            with ft_col:
                feet = st.number_input("Feet (ft)", min_value=1, max_value=8, value=int(st.session_state["height_ft"]), step=1)
            with in_col:
                inches = st.number_input("Inches (in)", min_value=0, max_value=11, value=int(st.session_state["height_in"]), step=1)
            height_m = round(((feet * 12) + inches) * 0.0254, 2)
            st.caption(f"Converted Height: **{height_m:.2f} m**")

    # Form Row 3: Income & Smoker Status
    r3_c1, r3_c2 = st.columns(2)
    with r3_c1:
        income_lpa = st.number_input(
            "Annual Income (₹ LPA)",
            min_value=0.1,
            max_value=1000.0,
            value=float(st.session_state["income_lpa"]),
            step=0.5,
            help="Gross annual income in Lakhs Per Annum (LPA)."
        )
    with r3_c2:
        smoker = st.selectbox(
            "Tobacco / Smoking Habit",
            options=[False, True],
            index=1 if st.session_state["smoker"] else 0,
            format_func=lambda x: "🚬 Active Smoker" if x else "🚭 Non-Smoker",
            help="Select active smoker status."
        )

    # Form Row 4: City & Occupation
    r4_c1, r4_c2 = st.columns(2)
    with r4_c1:
        city = st.text_input(
            "City of Residence",
            value=st.session_state["city"],
            help="Residential city name."
        )
    with r4_c2:
        occupation_options = [
            'private_job', 'government_job', 'business_owner',
            'freelancer', 'student', 'retired', 'unemployed'
        ]
        curr_occ = st.session_state["occupation"]
        default_idx = occupation_options.index(curr_occ) if curr_occ in occupation_options else 0
        occupation = st.selectbox(
            "Occupation Type",
            options=occupation_options,
            index=default_idx,
            format_func=lambda x: x.replace('_', ' ').title(),
            help="Select employment category."
        )

    # --------------------------------------------------------------------------
    # Live Health & Lifestyle Indicators
    # --------------------------------------------------------------------------
    st.markdown("<div style='margin-top: 16px; border-top: 1px solid rgba(255,255,255,0.08);'></div>", unsafe_allow_html=True)
    st.markdown("#### 🩺 Live Health Indicators")
    
    # Calculate live BMI
    bmi = weight / (height_m ** 2) if height_m > 0 else 0.0
    if bmi < 18.5:
        bmi_cat, bmi_color = "Underweight", "#38bdf8" if is_dark else "#0284c7"
    elif 18.5 <= bmi <= 24.9:
        bmi_cat, bmi_color = "Normal", "#34d399" if is_dark else "#059669"
    elif 25.0 <= bmi <= 29.9:
        bmi_cat, bmi_color = "Overweight", "#fbbf24" if is_dark else "#d97706"
    else:
        bmi_cat, bmi_color = "Obese", "#f87171" if is_dark else "#dc2626"

    # Lifestyle Risk
    if smoker and bmi > 30:
        lifestyle_risk, risk_color = "High", "#f87171" if is_dark else "#dc2626"
    elif smoker or bmi > 27:
        lifestyle_risk, risk_color = "Medium", "#fbbf24" if is_dark else "#d97706"
    else:
        lifestyle_risk, risk_color = "Low", "#34d399" if is_dark else "#059669"

    # City Tier
    tier_1 = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
    tier_2 = [
        "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
        "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
        "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
        "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
        "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
        "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
    ]
    city_clean = city.strip().title()
    city_tier_str = "Tier 1 Metro" if city_clean in tier_1 else ("Tier 2 City" if city_clean in tier_2 else "Tier 3 City")

    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(textwrap.dedent(f"""
        <div class="metric-box">
        <div class="metric-val" style="color: {bmi_color};">{bmi:.1f} kg/m²</div>
        <div class="metric-sub">BMI ({bmi_cat})</div>
        </div>
        """), unsafe_allow_html=True)
    with m2:
        st.markdown(textwrap.dedent(f"""
        <div class="metric-box">
        <div class="metric-val" style="color: {risk_color};">{lifestyle_risk}</div>
        <div class="metric-sub">Lifestyle Risk Factor</div>
        </div>
        """), unsafe_allow_html=True)
    with m3:
        st.markdown(textwrap.dedent(f"""
        <div class="metric-box">
        <div class="metric-val" style="color: {'#c084fc' if is_dark else '#7e22ce'};">{city_tier_str}</div>
        <div class="metric-sub">Classification</div>
        </div>
        """), unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 16px;'></div>", unsafe_allow_html=True)
    
    # Submission Button
    submit_btn = st.button("🚀 Predict Insurance Risk", use_container_width=True)

# ------------------------------------------------------------------------------
# Results & Visualization Column (Balanced Right Side Panel)
# ------------------------------------------------------------------------------
with col_output:
    st.markdown('<div class="card-title">📊 Prediction Analytics & Risk Distribution</div>', unsafe_allow_html=True)
    
    if submit_btn:
        if not is_online:
            st.error("❌ Cannot connect to FastAPI prediction service. Please ensure `python3 run.py` is running.")
        elif not city.strip():
            st.warning("⚠️ Please enter a valid city of residence.")
        else:
            payload = {
                "age": int(age),
                "weight": float(weight),
                "height": float(height_m),
                "income_lpa": float(income_lpa),
                "smoker": bool(smoker),
                "city": str(city),
                "occupation": str(occupation)
            }

            with st.spinner("Analyzing applicant profile with Random Forest model..."):
                try:
                    resp = requests.post(API_URL, json=payload, timeout=5)
                    if resp.status_code == 200:
                        st.session_state["last_result"] = resp.json()
                        st.session_state["api_error"] = None
                    else:
                        st.session_state["last_result"] = None
                        st.session_state["api_error"] = resp.json()
                except Exception as ex:
                    st.session_state["last_result"] = None
                    st.session_state["api_error"] = {"error": str(ex)}

    # Display API Errors if present
    if st.session_state.get("api_error"):
        err = st.session_state["api_error"]
        st.error("⚠️ Prediction Request Failed")
        st.json(err)

    # Render Prediction Result
    result_data = st.session_state.get("last_result")
    if result_data:
        category = result_data.get("predicted_category", "Low")
        confidence = result_data.get("confidence", 0.0)
        probs = result_data.get("class_probabilities", {})

        card_class = f"result-card-{category.lower()}"
        val_color = "#34d399" if category == "Low" else ("#fbbf24" if category == "Medium" else "#f87171")
        if not is_dark:
            val_color = "#059669" if category == "Low" else ("#d97706" if category == "Medium" else "#dc2626")

        result_card_html = textwrap.dedent(f"""
        <div class="{card_class}">
        <div class="res-label">Predicted Premium Category</div>
        <div class="res-val" style="color: {val_color};">{category} Premium Risk</div>
        <div style="font-size: 0.95rem; color: {'#cbd5e1' if is_dark else '#475569'};">
        Model Confidence Score: <strong>{confidence * 100:.1f}%</strong>
        </div>
        </div>
        """)
        st.markdown(result_card_html, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### 🎯 Class Probability Distribution")

        if probs:
            # Donut Chart with Altair
            df_probs = pd.DataFrame([
                {"Category": k, "Probability": v, "Percentage": f"{v*100:.1f}%"}
                for k, v in probs.items()
            ])

            donut_chart = alt.Chart(df_probs).mark_arc(
                innerRadius=55,
                stroke="#090d16" if is_dark else "#ffffff",
                strokeWidth=2
            ).encode(
                theta=alt.Theta(field="Probability", type="quantitative"),
                color=alt.Color(
                    field="Category",
                    type="nominal",
                    scale=alt.Scale(
                        domain=["Low", "Medium", "High"],
                        range=["#34d399", "#fbbf24", "#f87171"] if is_dark else ["#10b981", "#f59e0b", "#ef4444"]
                    ),
                    legend=alt.Legend(orient="bottom")
                ),
                tooltip=["Category", "Percentage"]
            ).properties(height=240)

            st.altair_chart(donut_chart, use_container_width=True)

            # Segmented Breakdown Bars
            for cat_name in ["Low", "Medium", "High"]:
                val = probs.get(cat_name, 0.0)
                pct_val = val * 100
                b_col1, b_col2 = st.columns([1, 4])
                with b_col1:
                    st.write(f"**{cat_name}**")
                with b_col2:
                    st.progress(float(val), text=f"{pct_val:.1f}%")

        # Contextual Policy Guidance
        st.markdown("---")
        st.markdown("#### 💡 Underwriting & Policy Guidance")
        
        if category == "Low":
            st.success("✅ **Standard Preferred Tier**: Low underwriting risk. Applicant qualifies for standard baseline rates with maximum coverage eligibility.")
        elif category == "Medium":
            st.warning("⚠️ **Moderate Tier Underwriting**: Moderate risk indicators detected. Standard policy with minor premium loading or lifestyle rider recommended.")
        else:
            st.error("🚨 **High Tier Risk Loading**: High risk classification due to health/lifestyle metrics. Comprehensive underwriting review & medical checkup required.")

        disclaimer_html = textwrap.dedent("""
        <div class="disclaimer-box">
        <strong>Legal Disclaimer:</strong> Insure AI provides AI-generated risk classification for analytical and informational purposes only. It does not constitute a binding insurance quote, financial contract, or official underwriting decision.
        </div>
        """)
        st.markdown(disclaimer_html, unsafe_allow_html=True)

    elif not st.session_state.get("api_error"):
        # Initial State Panel (Strict dedent to prevent markdown raw HTML escaping)
        preview_html = textwrap.dedent(f"""
        <div class="preview-panel">
        <div style="font-size: 1.05rem; font-weight: 700; color: {'#38bdf8' if is_dark else '#0284c7'}; margin-bottom: 12px; display: flex; align-items: center; gap: 8px;">
        ⚡ Ready for Risk Assessment
        </div>
        <div style="font-size: 0.88rem; color: {'#94a3b8' if is_dark else '#64748b'}; line-height: 1.6; margin-bottom: 18px;">
        Click the <strong>Predict Insurance Risk</strong> button on the left to evaluate applicant demographics against the Random Forest ML classifier.
        </div>

        <div style="font-size: 0.85rem; font-weight: 700; text-transform: uppercase; tracking: 1px; color: {'#cbd5e1' if is_dark else '#475569'}; margin-bottom: 10px;">
        📋 Current Applicant Parameters Summary
        </div>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; font-size: 0.85rem; margin-bottom: 20px;">
        <div style="background: {'rgba(30, 41, 59, 0.4)' if is_dark else '#f1f5f9'}; padding: 10px 14px; border-radius: 8px;">
        <div style="color: {'#94a3b8' if is_dark else '#64748b'}; font-size: 0.78rem;">Age & Weight</div>
        <div style="font-weight: 600; font-size: 0.95rem;">{age} Yrs • {weight} kg</div>
        </div>
        <div style="background: {'rgba(30, 41, 59, 0.4)' if is_dark else '#f1f5f9'}; padding: 10px 14px; border-radius: 8px;">
        <div style="color: {'#94a3b8' if is_dark else '#64748b'}; font-size: 0.78rem;">Height & Income</div>
        <div style="font-weight: 600; font-size: 0.95rem;">{height_m:.2f} m • ₹ {income_lpa} LPA</div>
        </div>
        <div style="background: {'rgba(30, 41, 59, 0.4)' if is_dark else '#f1f5f9'}; padding: 10px 14px; border-radius: 8px;">
        <div style="color: {'#94a3b8' if is_dark else '#64748b'}; font-size: 0.78rem;">Smoking Habit</div>
        <div style="font-weight: 600; font-size: 0.95rem;">{'🚬 Active Smoker' if smoker else '🚭 Non-Smoker'}</div>
        </div>
        <div style="background: {'rgba(30, 41, 59, 0.4)' if is_dark else '#f1f5f9'}; padding: 10px 14px; border-radius: 8px;">
        <div style="color: {'#94a3b8' if is_dark else '#64748b'}; font-size: 0.78rem;">Location & Job</div>
        <div style="font-weight: 600; font-size: 0.95rem;">{city_clean} ({city_tier_str.split()[0]} {city_tier_str.split()[1]})</div>
        </div>
        </div>

        <div style="background: {'rgba(56, 189, 248, 0.1)' if is_dark else '#e0f2fe'}; border: 1px solid {'rgba(56, 189, 248, 0.25)' if is_dark else '#bae6fd'}; border-radius: 10px; padding: 12px 16px; font-size: 0.82rem; color: {'#38bdf8' if is_dark else '#0369a1'}; display: flex; align-items: center; gap: 10px;">
        💡 <span>Live metrics: Calculated <strong>BMI is {bmi:.1f} kg/m² ({bmi_cat})</strong> with <strong>{lifestyle_risk} Lifestyle Risk</strong>.</span>
        </div>
        </div>
        """)
        st.markdown(preview_html, unsafe_allow_html=True)