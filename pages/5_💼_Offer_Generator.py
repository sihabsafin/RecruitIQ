import json
from datetime import date, timedelta
import streamlit as st
from utils.styles import inject_styles, page_header, section_title
from utils.execution_log import run_crew_with_log
from crews.crews import run_offer_crew
from utils.database import save_offer

st.set_page_config(page_title="Offer Generator · RecruitIQ", layout="wide")
inject_styles()
page_header("💼", "Offer Generator", "Salary benchmarks · Personalized offer letter · Negotiation playbook")

candidate  = st.session_state.get("selected_candidate",{})
jd_parsed  = st.session_state.get("current_jd_parsed",{})
screening  = candidate.get("screening",{})

with st.form("offer_form"):
    col1,col2 = st.columns(2)
    cand_name    = col1.text_input("Candidate Name", value=candidate.get("name",""))
    company_name = col2.text_input("Company Name",   value=jd_parsed.get("company_name","") if isinstance(jd_parsed,dict) else "")
    col3,col4 = st.columns(2)
    job_title  = col3.text_input("Job Title",  value=jd_parsed.get("job_title","") if isinstance(jd_parsed,dict) else "")
    location   = col4.text_input("Location",   value=jd_parsed.get("location","Remote") if isinstance(jd_parsed,dict) else "Remote")
    col5,col6 = st.columns(2)
    exp_years  = col5.number_input("Years of Experience", 0, 30, 3)
    start_date = col6.date_input("Proposed Start Date", value=date.today()+timedelta(weeks=3))
    submitted  = st.form_submit_button("🚀 Generate Offer Package", use_container_width=True)

if submitted:
    if not cand_name or not job_title:
        st.error("Please fill in candidate name and job title.")
        st.stop()
    try:
        result = run_crew_with_log(
            run_offer_crew,
            cand_name, job_title, company_name, location, exp_years, str(start_date), screening,
            phase_name="Offer Generation Crew",
            agents=["Salary Benchmarker","Offer Drafter","Negotiation Advisor"],
        )
        save_offer(None, result.get("salary_data",{}), json.dumps(result.get("offer_letter",{})), result.get("negotiation_guide",{}))
        st.session_state["offer_result"] = result
        st.session_state["offers_sent"]  = st.session_state.get("offers_sent",0) + 1
    except Exception as e:
        st.stop()

offer_result = st.session_state.get("offer_result")
if offer_result:
    salary = offer_result.get("salary_data",{})
    offer  = offer_result.get("offer_letter",{})
    nego   = offer_result.get("negotiation_guide",{})

    tab1,tab2,tab3 = st.tabs(["💰  Salary Benchmark","📄  Offer Letter","🤝  Negotiation Playbook"])
    with tab1:
        if isinstance(salary,dict):
            band = salary.get("salary_band",{})
            if band:
                col1,col2,col3,col4 = st.columns(4)
                curr = salary.get("currency","$")
                col1.metric("P25 — Entry",  f"{curr} {band.get('p25','N/A')}")
                col2.metric("P50 — Market", f"{curr} {band.get('p50','N/A')}")
                col3.metric("P75 — Senior", f"{curr} {band.get('p75','N/A')}")
                col4.metric("P90 — Top",    f"{curr} {band.get('p90','N/A')}")
            rec = salary.get("recommended_offer_range",{})
            if rec:
                st.markdown(f"<div style='background:rgba(34,197,94,0.06);border:1px solid rgba(34,197,94,0.2);border-radius:8px;padding:14px 18px;font-family:DM Sans;font-size:14px;color:#22c55e;margin:12px 0;'>💡 Recommended: <strong>{salary.get('currency','$')} {rec.get('min','?')} – {rec.get('max','?')}</strong> · Target: <strong>{rec.get('target','?')}</strong></div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-family:DM Sans;font-size:13px;color:rgba(232,230,240,0.5);line-height:1.6;'>{salary.get('market_context','')}</div>", unsafe_allow_html=True)
    with tab2:
        if isinstance(offer,dict):
            if offer.get("subject_line"):
                st.markdown(f"<div style='font-family:DM Sans;font-size:12px;color:rgba(232,230,240,0.4);text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;'>Email Subject</div><div style='font-family:DM Sans;font-size:14px;color:#a78bfa;background:#13131f;border:1px solid rgba(139,92,246,0.2);border-radius:6px;padding:10px 14px;margin-bottom:16px;'>{offer['subject_line']}</div>", unsafe_allow_html=True)
            if offer.get("offer_letter_text"):
                st.text_area("", offer["offer_letter_text"], height=480, label_visibility="collapsed")
                st.download_button("📥 Download Offer Letter (.txt)", data=offer["offer_letter_text"],
                    file_name=f"offer_{cand_name.replace(' ','_')}.txt", mime="text/plain", use_container_width=True)
    with tab3:
        if isinstance(nego,dict):
            col1,col2 = st.columns(2)
            col1.markdown(f"<div style='font-family:DM Sans;font-size:12px;color:rgba(232,230,240,0.4);text-transform:uppercase;letter-spacing:1px;margin-bottom:4px;'>Candidate Leverage</div><div style='font-family:DM Sans;font-size:13px;color:#e8e6f0;'>{nego.get('candidate_leverage_assessment','N/A')}</div>", unsafe_allow_html=True)
            col2.markdown(f"<div style='font-family:DM Sans;font-size:12px;color:rgba(232,230,240,0.4);text-transform:uppercase;letter-spacing:1px;margin-bottom:4px;'>Walk-Away Point</div><div style='font-family:DM Sans;font-size:13px;color:#ef4444;'>{nego.get('walk_away_point','N/A')}</div>", unsafe_allow_html=True)
            section_title("Non-Salary Levers")
            for l in nego.get("non_salary_levers",[]):
                st.markdown(f"<div style='font-family:DM Sans;font-size:13px;color:rgba(232,230,240,0.6);padding:5px 0 5px 12px;border-left:2px solid rgba(139,92,246,0.3);margin-bottom:5px;'>→ {l}</div>", unsafe_allow_html=True)
            section_title("Closing Scripts")
            for i,s in enumerate(nego.get("closing_scripts",[]),1):
                with st.expander(f"Option {i}"):
                    st.markdown(f"<div style='font-family:DM Sans;font-size:13px;color:rgba(232,230,240,0.65);line-height:1.7;'>{s}</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.download_button("📥 Download Full Offer Package (JSON)", data=json.dumps(offer_result,indent=2),
        file_name=f"offer_package_{cand_name.replace(' ','_')}.json", mime="application/json", use_container_width=True)
    st.balloons()
