import json
from datetime import date, timedelta
import streamlit as st
from utils.styles import inject_styles, page_header, section_title
from crews.crews import run_offer_crew
from utils.database import save_offer

st.set_page_config(page_title="Offer Generator · RecruitIQ", layout="wide")
inject_styles()
page_header("💼", "Offer Generator", "Market salary benchmarks · Personalized offer letter · Negotiation playbook")

candidate  = st.session_state.get("selected_candidate", {})
jd_parsed  = st.session_state.get("current_jd_parsed", {})
screening  = candidate.get("screening", {})

with st.form("offer_form"):
    col1, col2 = st.columns(2)
    cand_name    = col1.text_input("Candidate Name",  value=candidate.get("name",""))
    company_name = col2.text_input("Company Name",    value=jd_parsed.get("company_name","") if isinstance(jd_parsed,dict) else "")
    col3, col4   = st.columns(2)
    job_title    = col3.text_input("Job Title",  value=jd_parsed.get("job_title","") if isinstance(jd_parsed,dict) else "")
    location     = col4.text_input("Location",   value=jd_parsed.get("location","Remote") if isinstance(jd_parsed,dict) else "Remote")
    col5, col6   = st.columns(2)
    exp_years    = col5.number_input("Years of Experience", 0, 30, 3)
    start_date   = col6.date_input("Proposed Start Date", value=date.today()+timedelta(weeks=3))
    submitted    = st.form_submit_button("🚀 Generate Offer Package", use_container_width=True)

if submitted:
    if not cand_name or not job_title:
        st.error("Please fill in candidate name and job title.")
        st.stop()
    with st.status("Running Offer Generation Crew...", expanded=True) as status:
        st.write("💰 Salary Benchmarker Agent — researching market data...")
        st.write("✍️ Offer Drafter Agent — writing personalized letter...")
        st.write("🤝 Negotiation Advisor Agent — building playbook...")
        try:
            result = run_offer_crew(
                candidate_name=cand_name, job_title=job_title,
                company_name=company_name, location=location,
                experience_years=exp_years, start_date=str(start_date),
                screening_report=screening,
            )
            status.update(label="✅ Offer package ready!", state="complete")
        except Exception as e:
            status.update(label="Error", state="error")
            st.error(f"Crew error: {e}")
            st.stop()
    save_offer(None, result.get("salary_data",{}), json.dumps(result.get("offer_letter",{})), result.get("negotiation_guide",{}))
    st.session_state["offer_result"] = result
    st.session_state["offers_sent"]  = st.session_state.get("offers_sent",0) + 1

offer_result = st.session_state.get("offer_result")
if offer_result:
    salary     = offer_result.get("salary_data", {})
    offer      = offer_result.get("offer_letter", {})
    nego_guide = offer_result.get("negotiation_guide", {})

    tab1, tab2, tab3 = st.tabs(["💰  Salary Benchmark", "📄  Offer Letter", "🤝  Negotiation Playbook"])

    with tab1:
        if isinstance(salary, dict):
            band = salary.get("salary_band", {})
            if band:
                col1,col2,col3,col4 = st.columns(4)
                curr = salary.get("currency","$")
                col1.metric("P25 — Entry",  f"{curr} {band.get('p25','N/A')}")
                col2.metric("P50 — Market", f"{curr} {band.get('p50','N/A')}")
                col3.metric("P75 — Senior", f"{curr} {band.get('p75','N/A')}")
                col4.metric("P90 — Top",    f"{curr} {band.get('p90','N/A')}")
            rec = salary.get("recommended_offer_range",{})
            if rec:
                st.markdown(f"""
                <div style='background:rgba(52,211,153,0.06);border:1px solid rgba(52,211,153,0.2);border-radius:8px;padding:14px 18px;font-family:DM Sans;font-size:14px;color:#34d399;margin:12px 0;'>
                    💡 Recommended offer: <strong>{salary.get('currency','$')} {rec.get('min','?')} – {rec.get('max','?')}</strong>
                    &nbsp;·&nbsp; Target: <strong>{rec.get('target','?')}</strong>
                </div>
                """, unsafe_allow_html=True)
            st.markdown(f"<div style='font-family:DM Sans;font-size:13px;color:rgba(232,230,240,0.5);line-height:1.6;'>{salary.get('market_context','')}</div>", unsafe_allow_html=True)
            section_title("Competitiveness Tips")
            for t in salary.get("offer_competitiveness_tips",[]):
                st.markdown(f"<div style='font-family:DM Sans;font-size:13px;color:rgba(232,230,240,0.6);padding:5px 0 5px 12px;border-left:2px solid rgba(139,92,246,0.3);margin-bottom:5px;'>→ {t}</div>", unsafe_allow_html=True)

    with tab2:
        if isinstance(offer, dict):
            subject = offer.get("subject_line","")
            letter  = offer.get("offer_letter_text","")
            if subject:
                st.markdown(f"<div style='font-family:DM Sans;font-size:12px;color:rgba(232,230,240,0.4);text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;'>Email Subject</div><div style='font-family:DM Sans;font-size:14px;color:#a78bfa;background:#13131f;border:1px solid rgba(139,92,246,0.2);border-radius:6px;padding:10px 14px;margin-bottom:16px;'>{subject}</div>", unsafe_allow_html=True)
            if letter:
                st.text_area("Offer Letter", value=letter, height=480, label_visibility="collapsed")
                st.download_button("📥 Download Offer Letter (.txt)", data=letter,
                    file_name=f"offer_{cand_name.replace(' ','_')}.txt", mime="text/plain", use_container_width=True)

    with tab3:
        if isinstance(nego_guide, dict):
            col1, col2 = st.columns(2)
            col1.markdown(f"<div style='font-family:DM Sans;font-size:12px;color:rgba(232,230,240,0.4);text-transform:uppercase;letter-spacing:1px;margin-bottom:4px;'>Candidate Leverage</div><div style='font-family:DM Sans;font-size:13px;color:#e8e6f0;'>{nego_guide.get('candidate_leverage_assessment','N/A')}</div>", unsafe_allow_html=True)
            col2.markdown(f"<div style='font-family:DM Sans;font-size:12px;color:rgba(232,230,240,0.4);text-transform:uppercase;letter-spacing:1px;margin-bottom:4px;'>Walk-Away Point</div><div style='font-family:DM Sans;font-size:13px;color:#f87171;'>{nego_guide.get('walk_away_point','N/A')}</div>", unsafe_allow_html=True)
            section_title("Non-Salary Levers")
            for l in nego_guide.get("non_salary_levers",[]):
                st.markdown(f"<div style='font-family:DM Sans;font-size:13px;color:rgba(232,230,240,0.6);padding:5px 0 5px 12px;border-left:2px solid rgba(139,92,246,0.3);margin-bottom:5px;'>→ {l}</div>", unsafe_allow_html=True)
            section_title("Closing Scripts")
            for i, s in enumerate(nego_guide.get("closing_scripts",[]), 1):
                with st.expander(f"Option {i}"):
                    st.markdown(f"<div style='font-family:DM Sans;font-size:13px;color:rgba(232,230,240,0.65);line-height:1.7;'>{s}</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.download_button("📥 Download Full Offer Package (JSON)",
        data=json.dumps(offer_result, indent=2),
        file_name=f"offer_package_{cand_name.replace(' ','_')}.json",
        mime="application/json", use_container_width=True)
    st.balloons()
