import json
import streamlit as st
from utils.styles import inject_styles, page_header, section_title
from crews.crews import run_jd_intake_crew
from utils.database import save_jd

st.set_page_config(page_title="JD Intake · RecruitIQ", layout="wide")
inject_styles()
page_header("📋", "JD Intake", "Parse job descriptions · Extract skills · Audit for bias")

with st.form("jd_form"):
    col1, col2 = st.columns(2)
    job_title = col1.text_input("Job Title", placeholder="e.g. Senior Backend Engineer")
    company   = col2.text_input("Company Name", placeholder="e.g. TechCorp Ltd")
    jd_text   = st.text_area("Job Description", placeholder="Paste the full job description here...", height=280)
    submitted = st.form_submit_button("🚀 Run JD Intake Crew", use_container_width=True, type="primary")

if submitted:
    if not jd_text.strip():
        st.error("Please paste a job description.")
        st.stop()

    with st.status("Running JD Intake Crew...", expanded=True) as status:
        st.write("🤖 JD Parser Agent — extracting structure...")
        st.write("🧠 Skills Extractor Agent — building taxonomy...")
        st.write("⚖️ Bias Checker Agent — auditing language...")
        try:
            result = run_jd_intake_crew(jd_text)
            status.update(label="✅ JD Intake complete!", state="complete")
        except Exception as e:
            status.update(label="Error", state="error")
            st.error(f"Crew error: {e}")
            st.stop()

    jd_id = save_jd(job_title, company, jd_text, result.get("jd_parsed", {}))
    st.session_state.update({
        "current_jd_id": jd_id,
        "current_jd_text": jd_text,
        "current_jd_parsed": result.get("jd_parsed", {}),
        "current_skills": result.get("skills_taxonomy", {}),
        "active_jds": st.session_state.get("active_jds", 0) + 1,
    })

    st.markdown("""
    <div style="
        background:rgba(52,211,153,0.06); border:1px solid rgba(52,211,153,0.2);
        border-radius:8px; padding:12px 16px; margin:12px 0;
        font-family:'DM Sans',sans-serif; font-size:13px; color:#34d399;
    ">✓ JD processed and saved successfully</div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📄  Parsed JD", "🎯  Skills Taxonomy", "⚖️  Bias Report"])

    with tab1:
        jd_parsed = result.get("jd_parsed", {})
        if isinstance(jd_parsed, dict) and "raw_output" not in jd_parsed:
            col1, col2, col3 = st.columns(3)
            col1.markdown(f"<div style='font-family:DM Sans;font-size:12px;color:rgba(232,230,240,0.4);text-transform:uppercase;letter-spacing:1px;margin-bottom:4px;'>Job Title</div><div style='font-family:Syne;font-size:15px;font-weight:600;color:#e8e6f0;'>{jd_parsed.get('job_title','N/A')}</div>", unsafe_allow_html=True)
            col2.markdown(f"<div style='font-family:DM Sans;font-size:12px;color:rgba(232,230,240,0.4);text-transform:uppercase;letter-spacing:1px;margin-bottom:4px;'>Level</div><div style='font-family:Syne;font-size:15px;font-weight:600;color:#e8e6f0;'>{jd_parsed.get('experience_level','N/A')}</div>", unsafe_allow_html=True)
            col3.markdown(f"<div style='font-family:DM Sans;font-size:12px;color:rgba(232,230,240,0.4);text-transform:uppercase;letter-spacing:1px;margin-bottom:4px;'>Location</div><div style='font-family:Syne;font-size:15px;font-weight:600;color:#e8e6f0;'>{jd_parsed.get('location','N/A')}</div>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            section_title("Responsibilities")
            for r in jd_parsed.get("responsibilities", []):
                st.markdown(f"<div style='font-family:DM Sans;font-size:13px;color:rgba(232,230,240,0.65);padding:4px 0 4px 12px;border-left:2px solid rgba(139,92,246,0.3);margin-bottom:6px;'>→ {r}</div>", unsafe_allow_html=True)
            section_title("Required Qualifications")
            for q in jd_parsed.get("qualifications_required", []):
                st.markdown(f"<div style='font-family:DM Sans;font-size:13px;color:rgba(232,230,240,0.65);padding:4px 0 4px 12px;border-left:2px solid rgba(139,92,246,0.3);margin-bottom:6px;'>• {q}</div>", unsafe_allow_html=True)
        else:
            st.json(jd_parsed)

    with tab2:
        skills = result.get("skills_taxonomy", {})
        if isinstance(skills, dict) and "raw_output" not in skills:
            col1, col2 = st.columns(2)
            with col1:
                section_title("Must-Have Skills")
                for s in skills.get("must_have_skills", []):
                    name = s.get("skill", s) if isinstance(s, dict) else s
                    weight = s.get("importance_weight", "") if isinstance(s, dict) else ""
                    badge = f"<span style='background:rgba(124,58,237,0.15);color:#a78bfa;font-size:10px;padding:1px 7px;border-radius:99px;margin-left:6px;'>{weight}/10</span>" if weight else ""
                    st.markdown(f"<div style='font-family:DM Sans;font-size:13px;color:#e8e6f0;padding:7px 12px;background:#13131f;border:1px solid rgba(139,92,246,0.12);border-radius:6px;margin-bottom:6px;'><code style='background:transparent;color:#a78bfa;font-size:12px;'>{name}</code>{badge}</div>", unsafe_allow_html=True)
            with col2:
                section_title("Nice-to-Have Skills")
                for s in skills.get("nice_to_have_skills", []):
                    name = s.get("skill", s) if isinstance(s, dict) else s
                    st.markdown(f"<div style='font-family:DM Sans;font-size:13px;color:rgba(232,230,240,0.6);padding:7px 12px;background:#13131f;border:1px solid rgba(255,255,255,0.06);border-radius:6px;margin-bottom:6px;'><code style='background:transparent;color:rgba(167,139,250,0.6);font-size:12px;'>{name}</code></div>", unsafe_allow_html=True)
            section_title("Deal-breakers If Missing")
            for s in skills.get("red_flag_if_missing", []):
                st.markdown(f"<div style='font-family:DM Sans;font-size:13px;color:#f87171;padding:7px 12px;background:rgba(248,113,113,0.06);border:1px solid rgba(248,113,113,0.2);border-radius:6px;margin-bottom:6px;'>⛔ {s}</div>", unsafe_allow_html=True)
        else:
            st.json(skills)

    with tab3:
        bias = result.get("bias_report", {})
        if isinstance(bias, dict) and "raw_output" not in bias:
            score = bias.get("bias_score", 0)
            color = "#34d399" if score >= 7 else ("#fbbf24" if score >= 4 else "#f87171")
            st.markdown(f"""
            <div style='background:#13131f;border:1px solid rgba(139,92,246,0.15);border-radius:10px;padding:20px;margin-bottom:16px;'>
                <div style='font-family:DM Sans;font-size:11px;color:rgba(232,230,240,0.4);text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;'>Inclusivity Score</div>
                <div style='font-family:Syne;font-size:36px;font-weight:800;color:{color};'>{score}<span style='font-size:18px;color:rgba(232,230,240,0.3);'>/10</span></div>
                <div style='font-family:DM Sans;font-size:13px;color:rgba(232,230,240,0.55);margin-top:8px;'>{bias.get("overall_assessment","")}</div>
            </div>
            """, unsafe_allow_html=True)
            if bias.get("suggested_rewrites"):
                section_title("Suggested Rewrites")
                for orig, new in bias.get("suggested_rewrites", {}).items():
                    st.markdown(f"<div style='font-family:DM Sans;font-size:13px;padding:8px 12px;background:#13131f;border:1px solid rgba(139,92,246,0.12);border-radius:6px;margin-bottom:6px;'><span style='color:#f87171;text-decoration:line-through;'>{orig}</span> → <span style='color:#34d399;'>{new}</span></div>", unsafe_allow_html=True)
        else:
            st.json(bias)

    st.markdown("""
    <div style='background:rgba(139,92,246,0.06);border:1px solid rgba(139,92,246,0.15);border-radius:8px;padding:12px 16px;font-family:DM Sans;font-size:13px;color:rgba(232,230,240,0.5);margin-top:8px;'>
        ✅ JD saved · Navigate to <strong style='color:#a78bfa;'>Resume Screening</strong> to upload candidates
    </div>
    """, unsafe_allow_html=True)
