import json
import streamlit as st
from utils.styles import inject_styles, page_header, section_title
from crews.crews import run_interview_prep_crew
from utils.database import save_interview_kit

st.set_page_config(page_title="Interview Prep · RecruitIQ", layout="wide")
inject_styles()
page_header("🎤", "Interview Prep", "Generate tailored question bank · Scoring rubric per candidate")

if "current_jd_parsed" not in st.session_state:
    st.markdown("""<div style='background:rgba(251,191,36,0.06);border:1px solid rgba(251,191,36,0.2);border-radius:8px;padding:14px 18px;font-family:DM Sans;font-size:13px;color:#fbbf24;'>⚠️ Complete <strong>JD Intake</strong> first.</div>""", unsafe_allow_html=True)
    st.stop()

candidate = st.session_state.get("selected_candidate")
jd_parsed = st.session_state["current_jd_parsed"]

if candidate:
    st.markdown(f"""
    <div style='background:rgba(52,211,153,0.06);border:1px solid rgba(52,211,153,0.15);border-radius:8px;padding:12px 16px;font-family:DM Sans;font-size:13px;color:#34d399;margin-bottom:16px;'>
        ✓ Candidate loaded: <strong>{candidate['name']}</strong> · AI Score: {candidate['ai_score']:.0f}%
    </div>
    """, unsafe_allow_html=True)
    screening_summary = candidate.get("screening", {})
else:
    st.markdown("""<div style='background:rgba(139,92,246,0.06);border:1px solid rgba(139,92,246,0.15);border-radius:8px;padding:12px 16px;font-family:DM Sans;font-size:13px;color:rgba(232,230,240,0.5);margin-bottom:16px;'>No candidate selected — you can still generate a generic kit below.</div>""", unsafe_allow_html=True)
    cand_name = st.text_input("Candidate Name")
    screening_summary = {"candidate_name": cand_name}
    candidate = {"name": cand_name, "screening": screening_summary, "resume_text": "", "ai_score": 0}

if st.button("🚀 Generate Interview Kit", use_container_width=True, type="primary"):
    with st.status("Running Interview Prep Crew...", expanded=True) as status:
        st.write("🤖 Question Generator Agent — crafting tailored questions...")
        st.write("📋 Rubric Builder Agent — designing scoring criteria...")
        try:
            result = run_interview_prep_crew(
                candidate_summary=candidate.get("screening", screening_summary),
                jd_parsed=jd_parsed,
            )
            status.update(label="✅ Interview kit ready!", state="complete")
        except Exception as e:
            status.update(label="Error", state="error")
            st.error(f"Crew error: {e}")
            st.stop()
    save_interview_kit(None, st.session_state.get("current_jd_id"), result.get("questions",{}), result.get("rubric",{}))
    st.session_state["interview_kit"]    = result.get("questions", {})
    st.session_state["interview_rubric"] = result.get("rubric", {})

kit    = st.session_state.get("interview_kit", {})
rubric = st.session_state.get("interview_rubric", {})

if kit:
    st.markdown("<br>", unsafe_allow_html=True)
    tabs = st.tabs(["💻  Technical", "🧠  Behavioral", "🎭  Situational", "💜  Culture Fit", "🔎  Probing", "📊  Rubric"])
    categories = [
        ("technical_questions", tabs[0]),
        ("behavioral_questions", tabs[1]),
        ("situational_questions", tabs[2]),
        ("culture_fit_questions", tabs[3]),
        ("red_flag_probing_questions", tabs[4]),
    ]
    for key, tab in categories:
        with tab:
            questions = kit.get(key, [])
            if not questions:
                st.markdown("<div style='font-family:DM Sans;font-size:13px;color:rgba(232,230,240,0.35);padding:20px 0;'>No questions in this category.</div>", unsafe_allow_html=True)
                continue
            for i, q in enumerate(questions, 1):
                q_text = q.get("question_text", str(q)) if isinstance(q, dict) else str(q)
                with st.expander(f"Q{i}: {q_text[:90]}{'...' if len(q_text)>90 else ''}"):
                    st.markdown(f"<div style='font-family:DM Sans;font-size:14px;color:#e8e6f0;line-height:1.6;margin-bottom:12px;'>{q_text}</div>", unsafe_allow_html=True)
                    if isinstance(q, dict):
                        if q.get("purpose"):
                            st.markdown(f"<div style='font-family:DM Sans;font-size:12px;color:rgba(232,230,240,0.4);margin-bottom:8px;'><strong style='color:rgba(167,139,250,0.7);'>Purpose:</strong> {q['purpose']}</div>", unsafe_allow_html=True)
                        for p in q.get("follow_up_probes", []):
                            st.markdown(f"<div style='font-family:DM Sans;font-size:12px;color:rgba(232,230,240,0.5);padding:3px 0 3px 12px;border-left:2px solid rgba(139,92,246,0.3);margin-bottom:4px;'>↳ {p}</div>", unsafe_allow_html=True)
    with tabs[5]:
        if isinstance(rubric, dict) and rubric:
            st.json(rubric)
        else:
            st.markdown("<div style='font-family:DM Sans;font-size:13px;color:rgba(232,230,240,0.35);'>Rubric not yet generated.</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.download_button(
        "📥 Download Interview Kit (JSON)",
        data=json.dumps({"questions": kit, "rubric": rubric}, indent=2),
        file_name=f"interview_kit_{candidate['name'].replace(' ','_')}.json",
        mime="application/json", use_container_width=True,
    )
