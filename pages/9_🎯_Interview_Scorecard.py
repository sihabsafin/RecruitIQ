import streamlit as st
import streamlit.components.v1 as components
import json
from utils.styles import inject_styles, page_header, section_title
from config import get_llm

st.set_page_config(page_title="Interview Scorecard · RecruitIQ", layout="wide")
inject_styles()
page_header("🎯", "AI Interview Scorecard", "Fill live during interview · AI scores in real-time · Instant hire decision")

candidates  = st.session_state.get("screened_candidates", [])
jd_parsed   = st.session_state.get("current_jd_parsed", {}) or {}
kit         = st.session_state.get("interview_kit", {}) or {}

# ── Candidate selector ────────────────────────────────────────────────────────
names = [c["name"] for c in candidates] if candidates else []
col1, col2 = st.columns([2,2])
selected_name = col1.selectbox("Select Candidate", ["— select —"] + names)
interviewer   = col2.text_input("Interviewer Name", placeholder="e.g. Safin Ahmed")

cand = next((c for c in candidates if c["name"] == selected_name), None)

if not cand and selected_name == "— select —":
    st.markdown("""<div style='background:rgba(139,92,246,0.06);border:1px solid rgba(139,92,246,0.15);
    border-radius:8px;padding:12px 16px;font-family:DM Sans;font-size:13px;color:rgba(232,230,240,0.4);margin-top:12px;'>
    Select a candidate above to begin the live scorecard.</div>""", unsafe_allow_html=True)
    st.stop()

# ── Competency framework ──────────────────────────────────────────────────────
COMPETENCIES = [
    ("Technical Skills",       "Depth of technical knowledge relevant to the role"),
    ("Problem Solving",        "Structured thinking, approach to unknown problems"),
    ("Communication",          "Clarity, articulation, active listening"),
    ("Culture Fit",            "Alignment with company values and team dynamics"),
    ("Leadership / Ownership", "Initiative, accountability, past ownership examples"),
    ("Growth Mindset",         "Learning agility, handling feedback, adaptability"),
]

st.markdown("<br>", unsafe_allow_html=True)

# ── Live scoring form ─────────────────────────────────────────────────────────
st.markdown(f"""
<div style='background:#13131f;border:1px solid rgba(139,92,246,0.2);border-radius:12px;
padding:20px 24px;margin-bottom:20px;'>
    <div style='font-family:Syne,sans-serif;font-size:16px;font-weight:700;color:#f0eeff;margin-bottom:4px;'>
        Live Scorecard — {selected_name}
    </div>
    <div style='font-family:DM Sans;font-size:12px;color:rgba(232,230,240,0.4);'>
        Score each competency 1–5 as the interview progresses. Add notes per section.
    </div>
</div>
""", unsafe_allow_html=True)

scores   = {}
notes    = {}
total_w  = 0
total_sc = 0

WEIGHTS = [0.25, 0.20, 0.15, 0.15, 0.15, 0.10]

for (comp, desc), weight in zip(COMPETENCIES, WEIGHTS):
    key_s = f"score_{comp}"
    key_n = f"note_{comp}"

    col1, col2, col3 = st.columns([2.5, 1.5, 3])
    with col1:
        st.markdown(f"""
        <div style='padding:8px 0;'>
            <div style='font-family:DM Sans;font-size:13px;font-weight:500;color:#e8e6f0;margin-bottom:2px;'>{comp}</div>
            <div style='font-family:DM Sans;font-size:11px;color:rgba(232,230,240,0.35);'>{desc}</div>
        </div>""", unsafe_allow_html=True)

    with col2:
        score = st.select_slider(
            f"Score",
            options=[1, 2, 3, 4, 5],
            value=st.session_state.get(key_s, 3),
            key=key_s,
            label_visibility="collapsed",
        )
        score_color = "#22c55e" if score >= 4 else ("#fbbf24" if score == 3 else "#ef4444")
        label = ["", "Poor", "Below Avg", "Average", "Good", "Excellent"][score]
        st.markdown(f"""<div style='text-align:center;font-family:Syne,sans-serif;
        font-size:20px;font-weight:800;color:{score_color};margin-top:-8px;'>{score}
        <span style='font-size:11px;color:{score_color};opacity:0.7;display:block;
        font-family:DM Sans;font-weight:400;margin-top:-4px;'>{label}</span></div>""",
        unsafe_allow_html=True)

    with col3:
        note = st.text_input(
            "Notes",
            value=st.session_state.get(key_n, ""),
            placeholder=f"Notes on {comp.lower()}...",
            key=key_n,
            label_visibility="collapsed",
        )

    scores[comp] = score
    notes[comp]  = note
    total_sc += score * weight
    total_w  += weight

    st.markdown("<hr style='border-color:rgba(139,92,246,0.07);margin:4px 0;'>", unsafe_allow_html=True)

# ── Open questions ────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
section_title("Open Notes")
col1, col2 = st.columns(2)
notable_quotes  = col1.text_area("Notable Quotes / Standout Moments", height=100,
    placeholder="Anything the candidate said that stood out...")
concerns        = col2.text_area("Concerns / Follow-up Needed", height=100,
    placeholder="Questions unanswered, things to verify...")
overall_feeling = st.text_area("Overall Impression", height=80,
    placeholder="Your gut feeling about this candidate...")

# ── Live score display ────────────────────────────────────────────────────────
normalized = (total_sc / total_w) * 20 if total_w > 0 else 0
overall_color = "#22c55e" if normalized >= 75 else ("#fbbf24" if normalized >= 55 else "#ef4444")

components.html(f"""<!DOCTYPE html><html><head>
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@800&family=DM+Sans:wght@400;500&display=swap');
body{{margin:0;background:transparent;font-family:'DM Sans',sans-serif;}}
.wrap{{background:#0d0d14;border:1px solid rgba(139,92,246,0.2);border-radius:12px;
padding:20px 28px;display:flex;align-items:center;gap:32px;}}
.big{{font-family:'Syne',sans-serif;font-size:48px;font-weight:800;color:{overall_color};line-height:1;}}
.label{{font-size:11px;color:rgba(232,230,240,0.4);text-transform:uppercase;letter-spacing:1px;margin-bottom:4px;}}
.bar-wrap{{flex:1;background:rgba(255,255,255,0.06);border-radius:99px;height:10px;overflow:hidden;}}
.bar{{background:{overall_color};height:100%;width:{normalized}%;border-radius:99px;
transition:width 0.8s cubic-bezier(.4,0,.2,1);}}
.grades{{display:flex;gap:16px;flex-wrap:wrap;}}
.grade{{background:#13131f;border:1px solid rgba(255,255,255,0.07);
border-radius:8px;padding:8px 14px;text-align:center;}}
.g-label{{font-size:10px;color:rgba(232,230,240,0.35);text-transform:uppercase;letter-spacing:0.5px;}}
.g-val{{font-family:'Syne',sans-serif;font-size:16px;font-weight:800;margin-top:2px;}}
</style></head><body>
<div class="wrap">
  <div>
    <div class="label">Live Score</div>
    <div class="big">{normalized:.0f}<span style="font-size:22px;color:rgba(232,230,240,0.3);">%</span></div>
  </div>
  <div style="flex:1">
    <div class="label" style="margin-bottom:8px;">Score Breakdown</div>
    <div class="bar-wrap"><div class="bar"></div></div>
    <div style="display:flex;justify-content:space-between;margin-top:6px;">
      <span style="font-size:10px;color:rgba(232,230,240,0.2);">0</span>
      <span style="font-size:10px;color:rgba(232,230,240,0.2);">50</span>
      <span style="font-size:10px;color:rgba(232,230,240,0.2);">100</span>
    </div>
  </div>
  <div class="grades">
    {"".join(f'<div class="grade"><div class="g-label">{c[:8]}</div><div class="g-val" style="color:{"#22c55e" if s>=4 else "#fbbf24" if s==3 else "#ef4444"}">{s}/5</div></div>' for c,s in scores.items())}
  </div>
</div>
</body></html>""", height=130)

# ── AI scoring button ─────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🤖 Generate AI Final Score & Recommendation", use_container_width=True, type="primary"):
    with st.spinner("AI is analyzing scorecard..."):
        try:
            llm = get_llm(temperature=0.2)
            prompt = f"""You are an expert hiring assessor. Analyze this interview scorecard and give a final recommendation.

CANDIDATE: {selected_name}
ROLE: {jd_parsed.get('job_title','N/A')} at {jd_parsed.get('company_name','N/A')}
INTERVIEWER: {interviewer}

COMPETENCY SCORES (1-5):
{json.dumps(scores, indent=2)}

INTERVIEWER NOTES:
{json.dumps(notes, indent=2)}

NOTABLE QUOTES: {notable_quotes}
CONCERNS: {concerns}
OVERALL IMPRESSION: {overall_feeling}

CALCULATED SCORE: {normalized:.1f}/100

Return a JSON with:
- final_score: 0-100
- hire_recommendation: strong_yes / yes / maybe / no / strong_no
- confidence_level: high / medium / low
- top_strengths: list of 3
- top_concerns: list of 2-3
- decisive_factor: the single most important thing that influenced the decision
- suggested_next_step: exactly what to do next
- one_line_verdict: one punchy sentence summary for the hiring manager
"""
            response = llm.call([{"role":"user","content":prompt}]) if hasattr(llm,'call') else str(llm)

            # Parse response
            try:
                raw = str(response)
                clean = raw.strip().strip("```json").strip("```").strip()
                ai_result = json.loads(clean)
            except:
                ai_result = {
                    "final_score": int(normalized),
                    "hire_recommendation": "yes" if normalized >= 70 else ("maybe" if normalized >= 55 else "no"),
                    "confidence_level": "medium",
                    "top_strengths": list(scores.keys())[:3],
                    "top_concerns": [k for k,v in scores.items() if v <= 2][:2] or ["None identified"],
                    "decisive_factor": "Overall competency scores",
                    "suggested_next_step": "Proceed to offer stage" if normalized >= 70 else "Schedule follow-up",
                    "one_line_verdict": f"Candidate scored {normalized:.0f}/100 across all competencies.",
                }

            st.session_state[f"scorecard_{selected_name}"] = {
                "scores": scores, "notes": notes,
                "overall": normalized, "ai_result": ai_result,
                "notable_quotes": notable_quotes, "concerns": concerns,
            }

            # Display result
            rec   = ai_result.get("hire_recommendation","maybe")
            rc    = {"strong_yes":"#22c55e","yes":"#22c55e","maybe":"#fbbf24","no":"#ef4444","strong_no":"#ef4444"}.get(rec,"#a78bfa")
            conf  = ai_result.get("confidence_level","medium")
            conf_c= {"high":"#22c55e","medium":"#fbbf24","low":"#ef4444"}.get(conf,"#fbbf24")

            st.markdown(f"""
            <div style='background:linear-gradient(135deg,{rc}12,{rc}06);
            border:1px solid {rc}33;border-radius:12px;padding:24px;margin-top:12px;'>
                <div style='display:flex;align-items:flex-start;gap:24px;flex-wrap:wrap;'>
                    <div>
                        <div style='font-family:DM Sans;font-size:11px;color:rgba(232,230,240,0.4);
                        text-transform:uppercase;letter-spacing:1px;margin-bottom:4px;'>AI Verdict</div>
                        <div style='font-family:Syne,sans-serif;font-size:26px;font-weight:800;color:{rc};'>
                            {rec.upper().replace("_"," ")}
                        </div>
                        <div style='background:{conf_c}18;color:{conf_c};border:1px solid {conf_c}44;
                        font-size:11px;padding:2px 10px;border-radius:99px;display:inline-block;
                        font-family:DM Sans;margin-top:6px;'>Confidence: {conf.upper()}</div>
                    </div>
                    <div style='flex:1;min-width:200px;'>
                        <div style='font-family:DM Sans;font-size:13px;color:rgba(232,230,240,0.7);
                        line-height:1.6;font-style:italic;border-left:3px solid {rc};padding-left:12px;'>
                            "{ai_result.get('one_line_verdict','')}"
                        </div>
                        <div style='font-family:DM Sans;font-size:12px;color:rgba(232,230,240,0.5);
                        margin-top:10px;'>
                            <strong style='color:#a78bfa;'>Next step:</strong> {ai_result.get('suggested_next_step','')}
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                section_title("Top Strengths")
                for s in ai_result.get("top_strengths",[]):
                    st.markdown(f"<div style='font-family:DM Sans;font-size:13px;color:#22c55e;padding:5px 10px 5px 12px;border-left:2px solid #22c55e;margin-bottom:5px;background:rgba(34,197,94,0.04);border-radius:0 4px 4px 0;'>✓ {s}</div>", unsafe_allow_html=True)
            with col2:
                section_title("Key Concerns")
                for s in ai_result.get("top_concerns",[]):
                    st.markdown(f"<div style='font-family:DM Sans;font-size:13px;color:#f87171;padding:5px 10px 5px 12px;border-left:2px solid #f87171;margin-bottom:5px;background:rgba(248,113,113,0.04);border-radius:0 4px 4px 0;'>⚠ {s}</div>", unsafe_allow_html=True)

            section_title("Decisive Factor")
            st.markdown(f"<div style='font-family:DM Sans;font-size:13px;color:rgba(232,230,240,0.65);background:#13131f;border:1px solid rgba(139,92,246,0.15);border-radius:8px;padding:12px 16px;line-height:1.6;'>{ai_result.get('decisive_factor','')}</div>", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"AI scoring error: {e}")
