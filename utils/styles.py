"""
utils/styles.py
Shared premium dark UI styles injected on every page.
"""
import streamlit as st

def inject_styles():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;1,9..40,300&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, [data-testid="stAppViewContainer"] {
    background: #0a0a0f !important;
    color: #e8e6f0 !important;
    font-family: 'DM Sans', sans-serif !important;
}
[data-testid="stAppViewContainer"] > .main { background: #0a0a0f !important; }
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stToolbar"] { display: none; }
[data-testid="stSidebar"] {
    background: #0f0f18 !important;
    border-right: 1px solid rgba(139,92,246,0.15) !important;
}
.block-container { padding: 2rem !important; max-width: 100% !important; }
h1,h2,h3 { font-family: 'Syne', sans-serif !important; }

/* Form */
[data-testid="stForm"] {
    background: #13131f !important;
    border: 1px solid rgba(139,92,246,0.15) !important;
    border-radius: 12px !important;
    padding: 24px !important;
}
/* Inputs */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stNumberInput > div > div > input {
    background: #0f0f18 !important;
    border: 1px solid rgba(139,92,246,0.2) !important;
    border-radius: 8px !important;
    color: #e8e6f0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: rgba(139,92,246,0.5) !important;
    box-shadow: 0 0 0 3px rgba(139,92,246,0.1) !important;
}
.stTextInput label,.stTextArea label,.stNumberInput label,
.stSelectbox label,.stDateInput label,.stFileUploader label {
    color: rgba(232,230,240,0.55) !important;
    font-size: 11px !important;
    font-weight: 500 !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
}
/* Buttons */
.stButton > button {
    background: linear-gradient(135deg,#7c3aed,#6d28d9) !important;
    color: white !important; border: none !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important; font-weight: 500 !important;
    padding: 10px 24px !important; transition: all 0.2s !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg,#8b5cf6,#7c3aed) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 24px rgba(124,58,237,0.35) !important;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg,#7c3aed,#ec4899) !important;
}
/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid rgba(139,92,246,0.15) !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: rgba(232,230,240,0.4) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important; font-weight: 500 !important;
    padding: 10px 20px !important; border: none !important;
    border-bottom: 2px solid transparent !important;
}
.stTabs [aria-selected="true"] {
    color: #a78bfa !important;
    border-bottom: 2px solid #a78bfa !important;
}
/* Metrics */
[data-testid="metric-container"] {
    background: #13131f !important;
    border: 1px solid rgba(139,92,246,0.15) !important;
    border-radius: 12px !important; padding: 20px !important;
}
[data-testid="metric-container"] label {
    color: rgba(232,230,240,0.45) !important;
    font-size: 11px !important; letter-spacing: 1px !important;
    text-transform: uppercase !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-family: 'Syne', sans-serif !important;
    font-size: 28px !important; font-weight: 700 !important;
    color: #a78bfa !important;
}
/* Expander */
.streamlit-expanderHeader {
    background: #13131f !important;
    border: 1px solid rgba(139,92,246,0.15) !important;
    border-radius: 8px !important; color: rgba(232,230,240,0.7) !important;
    font-size: 13px !important;
}
.streamlit-expanderContent {
    background: #13131f !important;
    border: 1px solid rgba(139,92,246,0.15) !important;
    border-top: none !important;
}
/* Alerts */
.stAlert { background: #13131f !important; border-radius: 8px !important; font-size:13px !important; }
/* Dataframe */
[data-testid="stDataFrame"] {
    border: 1px solid rgba(139,92,246,0.15) !important;
    border-radius: 10px !important; overflow: hidden !important;
}
/* Progress */
.stProgress > div > div {
    background: linear-gradient(90deg,#7c3aed,#ec4899) !important;
    border-radius: 99px !important;
}
/* File uploader */
[data-testid="stFileUploader"] {
    background: #13131f !important;
    border: 1.5px dashed rgba(139,92,246,0.3) !important;
    border-radius: 10px !important;
}
/* Status */
[data-testid="stStatus"] {
    background: #13131f !important;
    border: 1px solid rgba(139,92,246,0.2) !important;
    border-radius: 10px !important;
}
hr { border-color: rgba(139,92,246,0.12) !important; }
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-thumb { background: rgba(139,92,246,0.3); border-radius: 99px; }
</style>
""", unsafe_allow_html=True)


def page_header(icon: str, title: str, subtitle: str):
    st.markdown(f"""
    <div style="
        padding: 32px 0 24px;
        border-bottom: 1px solid rgba(139,92,246,0.12);
        margin-bottom: 28px;
    ">
        <div style="display:flex; align-items:center; gap:12px; margin-bottom:8px;">
            <div style="
                width:40px; height:40px; border-radius:10px;
                background:rgba(139,92,246,0.12);
                border:1px solid rgba(139,92,246,0.2);
                display:flex; align-items:center; justify-content:center;
                font-size:18px;
            ">{icon}</div>
            <h1 style="
                font-family:'Syne',sans-serif;
                font-size:26px; font-weight:800;
                color:#f0eeff; letter-spacing:-0.8px; margin:0;
            ">{title}</h1>
        </div>
        <p style="
            font-family:'DM Sans',sans-serif;
            font-size:14px; color:rgba(232,230,240,0.45);
            font-weight:300; margin:0 0 0 52px;
        ">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)


def stat_card(label: str, value: str, color: str = "#a78bfa"):
    st.markdown(f"""
    <div style="
        background:#13131f;
        border:1px solid rgba(139,92,246,0.15);
        border-radius:10px; padding:16px 20px;
        margin-bottom:10px;
    ">
        <div style="
            font-family:'DM Sans',sans-serif;
            font-size:11px; color:rgba(232,230,240,0.4);
            letter-spacing:1px; text-transform:uppercase;
            margin-bottom:6px;
        ">{label}</div>
        <div style="
            font-family:'Syne',sans-serif;
            font-size:22px; font-weight:700; color:{color};
        ">{value}</div>
    </div>
    """, unsafe_allow_html=True)


def score_badge(score: float) -> str:
    if score >= 75:
        color, bg, label = "#34d399", "rgba(52,211,153,0.1)", "Strong Match"
    elif score >= 55:
        color, bg, label = "#fbbf24", "rgba(251,191,36,0.1)", "Partial Match"
    else:
        color, bg, label = "#f87171", "rgba(248,113,113,0.1)", "Weak Match"
    return f"""<span style="
        background:{bg}; color:{color};
        border:1px solid {color}40;
        font-size:11px; font-weight:500;
        padding:3px 10px; border-radius:99px;
        font-family:'DM Sans',sans-serif;
        letter-spacing:0.3px;
    ">{score:.0f}% · {label}</span>"""


def section_title(text: str):
    st.markdown(f"""
    <div style="
        font-family:'Syne',sans-serif;
        font-size:14px; font-weight:700;
        color:#f0eeff; letter-spacing:-0.2px;
        margin: 20px 0 12px;
        padding-bottom: 8px;
        border-bottom: 1px solid rgba(139,92,246,0.1);
    ">{text}</div>
    """, unsafe_allow_html=True)
