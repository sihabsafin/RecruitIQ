import streamlit as st
import streamlit.components.v1 as components
from utils.styles import inject_styles, page_header, section_title

st.set_page_config(page_title="Compare Candidates · RecruitIQ", layout="wide")
inject_styles()
page_header("⚖️", "Candidate Comparison", "Side-by-side analysis · Score breakdown · Final recommendation")

candidates = st.session_state.get("screened_candidates", [])

if len(candidates) < 2:
    st.markdown("""
    <div style='background:rgba(251,191,36,0.06);border:1px solid rgba(251,191,36,0.2);
    border-radius:8px;padding:14px 18px;font-family:DM Sans;font-size:13px;color:#fbbf24;'>
    ⚠️ You need at least 2 screened candidates. Complete <strong>Resume Screening</strong> first.
    </div>""", unsafe_allow_html=True)
    st.stop()

# ── Candidate selector ────────────────────────────────────────────────────────
names = [c["name"] for c in candidates]

st.markdown("""
<div style='font-family:DM Sans;font-size:12px;color:rgba(232,230,240,0.4);
text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;'>
Select candidates to compare (2 or 3)
</div>""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
sel1 = col1.selectbox("Candidate A", ["— select —"] + names, key="sel1")
sel2 = col2.selectbox("Candidate B", ["— select —"] + names, key="sel2")
sel3 = col3.selectbox("Candidate C (optional)", ["— none —"] + names, key="sel3")

selected = []
for sel in [sel1, sel2, sel3]:
    if sel not in ("— select —", "— none —"):
        match = next((c for c in candidates if c["name"] == sel), None)
        if match and match not in selected:
            selected.append(match)

if len(selected) < 2:
    st.markdown("""
    <div style='background:rgba(139,92,246,0.06);border:1px solid rgba(139,92,246,0.15);
    border-radius:8px;padding:12px 16px;font-family:DM Sans;font-size:13px;
    color:rgba(232,230,240,0.4);margin-top:12px;'>
    Select at least 2 candidates above to start comparing.
    </div>""", unsafe_allow_html=True)
    st.stop()

# ── Helper ────────────────────────────────────────────────────────────────────
def get_score(c, key, default=0):
    s = c.get("screening", {})
    if not isinstance(s, dict):
        return default
    sec = s.get("section_scores", {})
    if isinstance(sec, dict):
        val = sec.get(key, default)
        try:
            return float(val)
        except:
            return default
    return default

def safe_float(val, default=0):
    try:
        return float(str(val).replace("%","").strip())
    except:
        return default

def rec_color(rec):
    r = str(rec).lower()
    if "shortlist" in r or "strong" in r: return "#22c55e"
    if "reject" in r: return "#ef4444"
    return "#fbbf24"

def rec_label(rec):
    r = str(rec).lower()
    if "shortlist" in r: return "Shortlist"
    if "reject" in r: return "Reject"
    return "Hold"

COLORS = ["#a78bfa", "#06b6d4", "#f59e0b"]

# ── Radar chart ───────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
section_title("Score Radar — Multi-Dimension Comparison")

import math

def radar_svg(candidates, colors):
    dims = ["Overall", "Experience", "Skills", "Education", "Achievements"]
    n = len(dims)
    cx, cy, r = 260, 220, 160
    angle_step = 2 * math.pi / n

    def pt(i, val):
        a = i * angle_step - math.pi / 2
        rv = r * val / 100
        return cx + rv * math.cos(a), cy + rv * math.sin(a)

    def axis_pt(i, scale=1.0):
        a = i * angle_step - math.pi / 2
        return cx + r * scale * math.cos(a), cy + r * scale * math.sin(a)

    svg = f'<svg viewBox="0 0 520 440" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:520px;">'

    # Grid rings
    for ring in [0.25, 0.5, 0.75, 1.0]:
        pts = [axis_pt(i, ring) for i in range(n)]
        poly = " ".join(f"{x:.1f},{y:.1f}" for x,y in pts)
        svg += f'<polygon points="{poly}" fill="none" stroke="rgba(255,255,255,0.07)" stroke-width="1"/>'
        svg += f'<text x="{cx+6}" y="{cy - r*ring + 4}" fill="rgba(255,255,255,0.2)" font-size="9" font-family="JetBrains Mono">{int(ring*100)}</text>'

    # Axis lines + labels
    for i, dim in enumerate(dims):
        ax, ay = axis_pt(i)
        svg += f'<line x1="{cx}" y1="{cy}" x2="{ax:.1f}" y2="{ay:.1f}" stroke="rgba(255,255,255,0.08)" stroke-width="1"/>'
        lx, ly = axis_pt(i, 1.18)
        anchor = "middle"
        if lx < cx - 10: anchor = "end"
        elif lx > cx + 10: anchor = "start"
        svg += f'<text x="{lx:.1f}" y="{ly:.1f}" fill="rgba(255,255,255,0.55)" font-size="12" font-family="DM Sans" text-anchor="{anchor}" dominant-baseline="central">{dim}</text>'

    # Candidate polygons
    for ci, cand in enumerate(candidates):
        color = colors[ci]
        scores = [
            safe_float(cand.get("ai_score", 0)),
            get_score(cand, "experience", safe_float(cand.get("ai_score",0)) * 0.9),
            get_score(cand, "skills",     safe_float(cand.get("ai_score",0)) * 0.95),
            get_score(cand, "education",  safe_float(cand.get("ai_score",0)) * 0.85),
            get_score(cand, "achievements", safe_float(cand.get("ai_score",0)) * 0.8),
        ]
        pts_list = [pt(i, s) for i, s in enumerate(scores)]
        poly = " ".join(f"{x:.1f},{y:.1f}" for x,y in pts_list)
        svg += f'<polygon points="{poly}" fill="{color}" fill-opacity="0.12" stroke="{color}" stroke-width="2" stroke-linejoin="round"/>'
        for px, py in pts_list:
            svg += f'<circle cx="{px:.1f}" cy="{py:.1f}" r="4" fill="{color}" stroke="#0d0d14" stroke-width="1.5"/>'

    # Legend
    for ci, cand in enumerate(candidates):
        lx = 30 + ci * 160
        svg += f'<rect x="{lx}" y="410" width="12" height="12" rx="3" fill="{colors[ci]}"/>'
        svg += f'<text x="{lx+18}" y="421" fill="rgba(255,255,255,0.6)" font-size="11" font-family="DM Sans">{cand["name"][:18]}</text>'

    svg += '</svg>'
    return svg

radar = radar_svg(selected, COLORS)
st.markdown(f"""
<div style='background:#0d0d14;border:1px solid rgba(255,255,255,0.07);
border-radius:12px;padding:24px;display:flex;justify-content:center;'>
{radar}
</div>""", unsafe_allow_html=True)

# ── Score bars ────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
section_title("Score Breakdown")

metrics = [
    ("AI Match Score",    [safe_float(c.get("ai_score", 0)) for c in selected]),
    ("Semantic Score",    [safe_float(c.get("semantic_score", 0)) for c in selected]),
    ("Experience",        [get_score(c, "experience", safe_float(c.get("ai_score",0))*0.9) for c in selected]),
    ("Skills",            [get_score(c, "skills",     safe_float(c.get("ai_score",0))*0.95) for c in selected]),
    ("Education",         [get_score(c, "education",  safe_float(c.get("ai_score",0))*0.85) for c in selected]),
]

for label, scores in metrics:
    best_idx = scores.index(max(scores))
    st.markdown(f"""
    <div style='margin-bottom:14px;'>
        <div style='font-family:DM Sans;font-size:11px;color:rgba(232,230,240,0.4);
        text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;'>{label}</div>
        <div style='display:flex;gap:12px;align-items:center;'>
    """, unsafe_allow_html=True)

    bar_cols = st.columns(len(selected))
    for i, (col, score) in enumerate(zip(bar_cols, scores)):
        color = COLORS[i]
        is_best = (i == best_idx)
        best_badge = f"<span style='background:rgba(34,197,94,0.15);color:#22c55e;font-size:9px;padding:1px 6px;border-radius:99px;margin-left:6px;letter-spacing:0.5px;'>BEST</span>" if is_best else ""
        col.markdown(f"""
        <div style='background:#13131f;border:1px solid rgba(255,255,255,0.06);border-radius:8px;padding:10px 14px;'>
            <div style='font-family:DM Sans;font-size:11px;color:rgba(232,230,240,0.4);margin-bottom:6px;'>
                {selected[i]['name'][:20]}{best_badge}
            </div>
            <div style='background:rgba(255,255,255,0.06);border-radius:99px;height:6px;margin-bottom:6px;overflow:hidden;'>
                <div style='background:{color};height:100%;width:{score}%;border-radius:99px;
                transition:width 1s ease;'></div>
            </div>
            <div style='font-family:Syne,sans-serif;font-size:18px;font-weight:700;color:{color};'>{score:.0f}<span style='font-size:12px;color:rgba(232,230,240,0.3);'>%</span></div>
        </div>
        """, unsafe_allow_html=True)

# ── Head-to-head cards ────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
section_title("Head-to-Head Profile")

cols = st.columns(len(selected))
for i, (col, cand) in enumerate(zip(cols, selected)):
    color = COLORS[i]
    s = cand.get("screening", {})
    rec = cand.get("recommendation", "hold")
    rc = rec_color(rec)
    rl = rec_label(rec)

    green_flags = s.get("green_flags", [])[:3] if isinstance(s, dict) else []
    red_flags   = s.get("red_flags",   [])[:2] if isinstance(s, dict) else []
    summary     = s.get("summary", "")         if isinstance(s, dict) else ""
    email       = cand.get("email", "N/A")

    flags_html = ""
    for f in green_flags:
        flags_html += f"<div style='font-size:11.5px;color:#22c55e;padding:3px 0 3px 10px;border-left:2px solid #22c55e;margin-bottom:4px;line-height:1.4;'>✓ {str(f)[:60]}</div>"
    for f in red_flags:
        flags_html += f"<div style='font-size:11.5px;color:#f87171;padding:3px 0 3px 10px;border-left:2px solid #f87171;margin-bottom:4px;line-height:1.4;'>⚠ {str(f)[:60]}</div>"

    col.markdown(f"""
    <div style='background:#0d0d14;border:1px solid {color}33;border-top:3px solid {color};
    border-radius:10px;padding:20px;height:100%;'>
        <div style='font-family:Syne,sans-serif;font-size:16px;font-weight:700;
        color:#f0eeff;margin-bottom:4px;'>{cand['name']}</div>
        <div style='font-family:DM Sans;font-size:11px;color:rgba(232,230,240,0.35);
        margin-bottom:14px;'>{email}</div>

        <div style='display:flex;align-items:center;gap:8px;margin-bottom:14px;'>
            <div style='font-family:Syne,sans-serif;font-size:28px;font-weight:800;color:{color};'>
                {safe_float(cand.get("ai_score",0)):.0f}<span style='font-size:14px;color:rgba(232,230,240,0.3);'>%</span>
            </div>
            <div style='background:{rc}18;color:{rc};border:1px solid {rc}44;
            font-size:11px;font-weight:500;padding:3px 10px;border-radius:99px;
            font-family:DM Sans;letter-spacing:0.3px;'>{rl}</div>
        </div>

        <div style='font-family:DM Sans;font-size:11px;color:rgba(232,230,240,0.4);
        text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;'>Highlights</div>
        {flags_html if flags_html else '<div style="font-size:11px;color:rgba(232,230,240,0.2);">No highlights available</div>'}

        <div style='font-family:DM Sans;font-size:11px;color:rgba(232,230,240,0.4);
        text-transform:uppercase;letter-spacing:1px;margin:12px 0 6px;'>Summary</div>
        <div style='font-family:DM Sans;font-size:12px;color:rgba(232,230,240,0.5);
        line-height:1.6;'>{str(summary)[:200]}{'...' if len(str(summary))>200 else ''}</div>
    </div>
    """, unsafe_allow_html=True)

# ── Winner recommendation ─────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
section_title("AI Recommendation")

best = max(selected, key=lambda c: safe_float(c.get("ai_score", 0)))
best_idx = selected.index(best)
best_color = COLORS[best_idx]
runner_up = sorted(selected, key=lambda c: safe_float(c.get("ai_score",0)), reverse=True)

score_diff = safe_float(runner_up[0].get("ai_score",0)) - safe_float(runner_up[1].get("ai_score",0)) if len(runner_up) > 1 else 0
confidence = "High" if score_diff > 15 else ("Medium" if score_diff > 7 else "Low")
conf_color = "#22c55e" if confidence == "High" else ("#fbbf24" if confidence == "Medium" else "#ef4444")

col1, col2 = st.columns([2, 1])
with col1:
    st.markdown(f"""
    <div style='background:linear-gradient(135deg,{best_color}18,{best_color}08);
    border:1px solid {best_color}33;border-radius:12px;padding:24px;'>
        <div style='font-family:DM Sans;font-size:11px;color:rgba(232,230,240,0.4);
        text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;'>Top Candidate</div>
        <div style='font-family:Syne,sans-serif;font-size:24px;font-weight:800;
        color:#f0eeff;margin-bottom:6px;'>{best['name']}</div>
        <div style='font-family:DM Sans;font-size:13px;color:rgba(232,230,240,0.55);line-height:1.7;'>
            Leads with <strong style='color:{best_color};'>{safe_float(best.get("ai_score",0)):.0f}%</strong> AI match score,
            outperforming by <strong style='color:{best_color};'>{score_diff:.0f} points</strong>.
            Recommendation confidence is
            <strong style='color:{conf_color};'>{confidence}</strong> based on score gap analysis.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style='background:#0d0d14;border:1px solid rgba(255,255,255,0.07);
    border-radius:12px;padding:20px;height:100%;'>
        <div style='font-family:DM Sans;font-size:11px;color:rgba(232,230,240,0.4);
        text-transform:uppercase;letter-spacing:1px;margin-bottom:14px;'>Rankings</div>
    """, unsafe_allow_html=True)

    for rank, cand in enumerate(runner_up, 1):
        medal = ["🥇", "🥈", "🥉"][rank-1] if rank <= 3 else f"{rank}."
        rc = COLORS[selected.index(cand)]
        st.markdown(f"""
        <div style='display:flex;align-items:center;gap:10px;padding:8px 0;
        border-bottom:1px solid rgba(255,255,255,0.04);'>
            <span style='font-size:16px;'>{medal}</span>
            <div>
                <div style='font-family:DM Sans;font-size:13px;color:#e8e6f0;font-weight:500;'>{cand['name']}</div>
                <div style='font-family:Syne,sans-serif;font-size:13px;color:{rc};font-weight:700;'>{safe_float(cand.get("ai_score",0)):.0f}%</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ── Action buttons ────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
if col1.button(f"✅ Select {best['name']} for Interview Prep", use_container_width=True, type="primary"):
    st.session_state["selected_candidate"] = best
    st.success(f"✓ {best['name']} selected! Go to Interview Prep.")

# Export comparison as text
if col2.button("📥 Export Comparison Report", use_container_width=True):
    lines = [f"RecruitIQ — Candidate Comparison Report\n{'='*50}\n"]
    for rank, cand in enumerate(runner_up, 1):
        lines.append(f"\n#{rank} — {cand['name']}")
        lines.append(f"AI Score: {safe_float(cand.get('ai_score',0)):.0f}%")
        lines.append(f"Semantic Score: {safe_float(cand.get('semantic_score',0)):.0f}%")
        lines.append(f"Recommendation: {rec_label(cand.get('recommendation','hold'))}")
        s = cand.get("screening", {})
        if isinstance(s, dict):
            lines.append(f"Summary: {s.get('summary','N/A')}")
        lines.append("-"*40)

    report = "\n".join(lines)
    st.download_button(
        "📄 Download Report (.txt)",
        data=report,
        file_name="candidate_comparison.txt",
        mime="text/plain",
        use_container_width=True,
    )
