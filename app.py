import streamlit as st

st.set_page_config(
    page_title="RecruitIQ · AI Hiring Platform",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;1,9..40,300&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0a0a0f !important;
    color: #e8e6f0 !important;
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stAppViewContainer"] > .main { background: #0a0a0f !important; }
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stToolbar"] { display: none; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #0f0f18 !important;
    border-right: 1px solid rgba(139,92,246,0.15) !important;
}
[data-testid="stSidebar"] > div { padding-top: 0 !important; }

.sidebar-brand {
    padding: 28px 24px 20px;
    border-bottom: 1px solid rgba(139,92,246,0.12);
    margin-bottom: 8px;
}
.sidebar-logo {
    font-family: 'Syne', sans-serif;
    font-size: 22px;
    font-weight: 800;
    background: linear-gradient(135deg, #a78bfa 0%, #7c3aed 50%, #ec4899 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -0.5px;
}
.sidebar-tagline {
    font-size: 11px;
    color: rgba(232,230,240,0.4);
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-top: 4px;
    font-weight: 300;
}

/* Sidebar nav links */
[data-testid="stSidebarNav"] a {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13.5px !important;
    font-weight: 400 !important;
    color: rgba(232,230,240,0.6) !important;
    border-radius: 8px !important;
    padding: 8px 12px !important;
    transition: all 0.2s ease !important;
}
[data-testid="stSidebarNav"] a:hover {
    color: #a78bfa !important;
    background: rgba(139,92,246,0.08) !important;
}
[data-testid="stSidebarNav"] a[aria-current="page"] {
    color: #a78bfa !important;
    background: rgba(139,92,246,0.12) !important;
    font-weight: 500 !important;
}

/* ── Main content ── */
.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}
.main .block-container { padding: 0 2rem 2rem !important; }

/* ── Typography ── */
h1, h2, h3 { font-family: 'Syne', sans-serif !important; }

/* ── Metrics ── */
[data-testid="metric-container"] {
    background: #13131f !important;
    border: 1px solid rgba(139,92,246,0.15) !important;
    border-radius: 12px !important;
    padding: 20px !important;
}
[data-testid="metric-container"] label {
    color: rgba(232,230,240,0.45) !important;
    font-size: 11px !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    font-family: 'DM Sans', sans-serif !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-family: 'Syne', sans-serif !important;
    font-size: 32px !important;
    font-weight: 700 !important;
    color: #a78bfa !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #6d28d9) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    padding: 10px 24px !important;
    transition: all 0.2s ease !important;
    letter-spacing: 0.2px !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #8b5cf6, #7c3aed) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 24px rgba(124,58,237,0.35) !important;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #7c3aed, #ec4899) !important;
    box-shadow: 0 4px 20px rgba(124,58,237,0.3) !important;
}

/* ── Inputs ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stNumberInput > div > div > input,
.stSelectbox > div > div {
    background: #13131f !important;
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
.stTextInput label, .stTextArea label, .stNumberInput label,
.stSelectbox label, .stDateInput label, .stFileUploader label {
    color: rgba(232,230,240,0.6) !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    letter-spacing: 0.5px !important;
    text-transform: uppercase !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid rgba(139,92,246,0.15) !important;
    gap: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: rgba(232,230,240,0.45) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    padding: 10px 20px !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
}
.stTabs [aria-selected="true"] {
    color: #a78bfa !important;
    border-bottom: 2px solid #a78bfa !important;
    background: transparent !important;
}

/* ── Expander ── */
.streamlit-expanderHeader {
    background: #13131f !important;
    border: 1px solid rgba(139,92,246,0.15) !important;
    border-radius: 8px !important;
    color: rgba(232,230,240,0.7) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
}
.streamlit-expanderContent {
    background: #13131f !important;
    border: 1px solid rgba(139,92,246,0.15) !important;
    border-top: none !important;
}

/* ── Alerts / Info boxes ── */
.stAlert {
    background: #13131f !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
}
[data-testid="stNotification"] { border-radius: 8px !important; }

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border: 1px solid rgba(139,92,246,0.15) !important;
    border-radius: 10px !important;
    overflow: hidden !important;
}

/* ── Divider ── */
hr { border-color: rgba(139,92,246,0.12) !important; }

/* ── Progress ── */
.stProgress > div > div {
    background: linear-gradient(90deg, #7c3aed, #ec4899) !important;
    border-radius: 99px !important;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: #13131f !important;
    border: 1.5px dashed rgba(139,92,246,0.3) !important;
    border-radius: 10px !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: rgba(139,92,246,0.6) !important;
}

/* ── Status box ── */
[data-testid="stStatus"] {
    background: #13131f !important;
    border: 1px solid rgba(139,92,246,0.2) !important;
    border-radius: 10px !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(139,92,246,0.3); border-radius: 99px; }
::-webkit-scrollbar-thumb:hover { background: rgba(139,92,246,0.5); }

/* ── Form ── */
[data-testid="stForm"] {
    background: #13131f !important;
    border: 1px solid rgba(139,92,246,0.15) !important;
    border-radius: 12px !important;
    padding: 24px !important;
}
</style>
""", unsafe_allow_html=True)

# ── Sidebar brand ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="sidebar-logo">RecruitIQ</div>
        <div class="sidebar-tagline">AI · Hiring · Pipeline</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("##### Pipeline")

# ── Hero header ───────────────────────────────────────────────────────────────
st.markdown("""
<div style="
    background: linear-gradient(135deg, #13131f 0%, #1a0a2e 50%, #13131f 100%);
    border-bottom: 1px solid rgba(139,92,246,0.15);
    padding: 52px 48px 44px;
    margin: -2rem -2rem 2rem;
    position: relative;
    overflow: hidden;
">
    <div style="
        position: absolute; top: -60px; right: -60px;
        width: 300px; height: 300px;
        background: radial-gradient(circle, rgba(124,58,237,0.12) 0%, transparent 70%);
        pointer-events: none;
    "></div>
    <div style="
        display: inline-block;
        background: rgba(139,92,246,0.1);
        border: 1px solid rgba(139,92,246,0.25);
        color: #a78bfa;
        font-size: 11px;
        font-weight: 500;
        letter-spacing: 2px;
        text-transform: uppercase;
        padding: 5px 14px;
        border-radius: 99px;
        margin-bottom: 18px;
        font-family: 'DM Sans', sans-serif;
    ">End-to-End AI Hiring</div>
    <h1 style="
        font-family: 'Syne', sans-serif;
        font-size: 42px;
        font-weight: 800;
        color: #f0eeff;
        letter-spacing: -1.5px;
        line-height: 1.1;
        margin-bottom: 12px;
    ">Hire smarter.<br><span style="
        background: linear-gradient(135deg, #a78bfa, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    ">Ship faster.</span></h1>
    <p style="
        font-family: 'DM Sans', sans-serif;
        font-size: 15px;
        color: rgba(232,230,240,0.5);
        font-weight: 300;
        max-width: 460px;
        line-height: 1.7;
    ">From job description to signed offer — fully automated, bias-free, and powered by 12 specialized AI agents.</p>
</div>
""", unsafe_allow_html=True)

# ── Metrics ───────────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
col1.metric("Active JDs",       st.session_state.get("active_jds", 0))
col2.metric("Resumes Screened", st.session_state.get("resumes_screened", 0))
col3.metric("Shortlisted",      st.session_state.get("shortlisted", 0))
col4.metric("Offers Sent",      st.session_state.get("offers_sent", 0))

st.markdown("<br>", unsafe_allow_html=True)

# ── Pipeline steps ─────────────────────────────────────────────────────────────
st.markdown("""
<div style="margin-bottom: 8px;">
    <span style="font-family:'Syne',sans-serif; font-size:16px; font-weight:700; color:#f0eeff; letter-spacing:-0.3px;">
        The Pipeline
    </span>
</div>
""", unsafe_allow_html=True)

steps = [
    ("01", "JD Intake",        "Parse job description → extract skills taxonomy → bias audit",           "#7c3aed"),
    ("02", "Resume Screening", "Upload resumes → AI scores & ranks → shortlist candidates",              "#6d28d9"),
    ("03", "Interview Prep",   "Generate tailored question bank → scoring rubric per candidate",         "#5b21b6"),
    ("04", "Evaluation",       "Analyze interview notes → competency scores → hire recommendation",      "#4c1d95"),
    ("05", "Offer Generator",  "Market salary benchmarks → personalized offer letter → negotiation kit", "#3b0764"),
]

cols = st.columns(5)
for col, (num, title, desc, color) in zip(cols, steps):
    col.markdown(f"""
    <div style="
        background: #13131f;
        border: 1px solid rgba(139,92,246,0.15);
        border-top: 2px solid {color};
        border-radius: 10px;
        padding: 20px 16px;
        height: 140px;
        position: relative;
    ">
        <div style="
            font-family: 'Syne', sans-serif;
            font-size: 11px;
            font-weight: 700;
            color: rgba(139,92,246,0.5);
            letter-spacing: 2px;
            margin-bottom: 8px;
        ">{num}</div>
        <div style="
            font-family: 'Syne', sans-serif;
            font-size: 13px;
            font-weight: 600;
            color: #e8e6f0;
            margin-bottom: 8px;
            letter-spacing: -0.2px;
        ">{title}</div>
        <div style="
            font-family: 'DM Sans', sans-serif;
            font-size: 11.5px;
            color: rgba(232,230,240,0.4);
            line-height: 1.5;
            font-weight: 300;
        ">{desc}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Agent grid ────────────────────────────────────────────────────────────────
st.markdown("""
<div style="margin-bottom: 16px;">
    <span style="font-family:'Syne',sans-serif; font-size:16px; font-weight:700; color:#f0eeff; letter-spacing:-0.3px;">
        12 Specialized Agents
    </span>
</div>
""", unsafe_allow_html=True)

agents = [
    ("JD Parser",           "Phase 1", "Extracts structure from raw JD"),
    ("Skills Extractor",    "Phase 1", "Builds must-have taxonomy"),
    ("Bias Checker",        "Phase 1", "Audits for inclusive language"),
    ("Resume Screener",     "Phase 2", "Scores resumes 0–100"),
    ("Skills Matcher",      "Phase 2", "Skill-by-skill gap analysis"),
    ("Question Generator",  "Phase 3", "Creates tailored interview kit"),
    ("Rubric Builder",      "Phase 3", "Designs scoring criteria"),
    ("Interview Analyst",   "Phase 4", "Scores interview performance"),
    ("Reference Checker",   "Phase 4", "Prepares verification guide"),
    ("Salary Benchmarker",  "Phase 5", "P25/P50/P75 market data"),
    ("Offer Drafter",       "Phase 5", "Writes personalized letter"),
    ("Negotiation Advisor", "Phase 5", "Builds closing playbook"),
]

phase_colors = {"Phase 1": "#7c3aed", "Phase 2": "#0891b2", "Phase 3": "#059669", "Phase 4": "#d97706", "Phase 5": "#dc2626"}

cols = st.columns(4)
for i, (name, phase, desc) in enumerate(agents):
    color = phase_colors[phase]
    with cols[i % 4]:
        st.markdown(f"""
        <div style="
            background: #13131f;
            border: 1px solid rgba(255,255,255,0.06);
            border-radius: 8px;
            padding: 14px 16px;
            margin-bottom: 10px;
        ">
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:6px;">
                <div style="
                    width: 6px; height: 6px; border-radius: 50%;
                    background: {color}; flex-shrink: 0;
                "></div>
                <span style="
                    font-family:'DM Sans',sans-serif;
                    font-size:13px; font-weight:500; color:#e8e6f0;
                ">{name}</span>
            </div>
            <div style="
                display: inline-block;
                background: rgba(255,255,255,0.05);
                color: rgba(232,230,240,0.4);
                font-size: 10px; font-weight:500;
                letter-spacing: 0.8px;
                padding: 2px 8px; border-radius: 99px;
                text-transform: uppercase;
                font-family:'DM Sans',sans-serif;
                margin-bottom: 6px;
            ">{phase}</div>
            <div style="
                font-family:'DM Sans',sans-serif;
                font-size:11.5px; color:rgba(232,230,240,0.35);
                font-weight:300;
            ">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style="
    background: rgba(139,92,246,0.06);
    border: 1px solid rgba(139,92,246,0.15);
    border-radius: 10px;
    padding: 16px 20px;
    font-family: 'DM Sans', sans-serif;
    font-size: 13px;
    color: rgba(232,230,240,0.5);
">
    👈 <strong style="color:#a78bfa;">Use the sidebar</strong> to navigate between pipeline stages.
    Start with <strong style="color:#e8e6f0;">JD Intake</strong> → proceed through each phase in order.
</div>
""", unsafe_allow_html=True)
