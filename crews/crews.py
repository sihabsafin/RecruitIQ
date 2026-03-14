"""
crews/crews.py
The 5 RecruitIQ crews. Agents are lazy-loaded at call time so st.secrets works.
"""

import json
from crewai import Crew, Process
from agents.agents import (
    get_jd_parser_agent, get_skills_extractor_agent, get_bias_checker_agent,
    get_resume_screener_agent, get_skills_matcher_agent,
    get_question_generator_agent, get_rubric_builder_agent,
    get_interview_analyst_agent, get_reference_checker_agent,
    get_salary_benchmarker_agent, get_offer_drafter_agent, get_negotiation_advisor_agent,
)
from agents.tasks import (
    task_parse_jd, task_extract_skills, task_check_bias,
    task_screen_resume, task_match_skills,
    task_generate_questions, task_build_rubric,
    task_analyze_interview, task_reference_check,
    task_benchmark_salary, task_draft_offer, task_negotiation_advice,
)


def _safe_json(raw: str) -> dict:
    """Try to parse JSON from agent output, fallback to raw string."""
    try:
        cleaned = raw.strip().strip("```json").strip("```").strip()
        return json.loads(cleaned)
    except Exception:
        return {"raw_output": raw}


def _task_output(task) -> str:
    """Safely extract string output from a task."""
    try:
        out = task.output
        if hasattr(out, "raw"):
            return str(out.raw)
        return str(out)
    except Exception:
        return "{}"


# ── CREW 1: JD Intake ────────────────────────────────────────────────────────

def run_jd_intake_crew(jd_text: str) -> dict:
    a1 = get_jd_parser_agent()
    a2 = get_skills_extractor_agent()
    a3 = get_bias_checker_agent()

    t1 = task_parse_jd(a1, jd_text)
    t2 = task_extract_skills(a2, jd_text)
    t3 = task_check_bias(a3, jd_text)

    Crew(
        agents=[a1, a2, a3],
        tasks=[t1, t2, t3],
        process=Process.sequential,
        verbose=True,
    ).kickoff()

    return {
        "jd_parsed":       _safe_json(_task_output(t1)),
        "skills_taxonomy": _safe_json(_task_output(t2)),
        "bias_report":     _safe_json(_task_output(t3)),
    }


# ── CREW 2: Resume Screening ─────────────────────────────────────────────────

def run_screening_crew(resume_text: str, jd_parsed: dict, skills_taxonomy: dict) -> dict:
    jd_str = json.dumps(jd_parsed, indent=2)
    sk_str = json.dumps(skills_taxonomy, indent=2)

    a1 = get_resume_screener_agent()
    a2 = get_skills_matcher_agent()

    t1 = task_screen_resume(a1, resume_text, jd_str)
    t2 = task_match_skills(a2, resume_text, sk_str)

    Crew(
        agents=[a1, a2],
        tasks=[t1, t2],
        process=Process.sequential,
        verbose=True,
    ).kickoff()

    return {
        "screening_report": _safe_json(_task_output(t1)),
        "skills_match":     _safe_json(_task_output(t2)),
    }


# ── CREW 3: Interview Prep ───────────────────────────────────────────────────

def run_interview_prep_crew(candidate_summary: dict, jd_parsed: dict) -> dict:
    cand_str = json.dumps(candidate_summary, indent=2)
    jd_str   = json.dumps(jd_parsed, indent=2)

    a1 = get_question_generator_agent()
    t1 = task_generate_questions(a1, cand_str, jd_str)

    Crew(agents=[a1], tasks=[t1], process=Process.sequential, verbose=True).kickoff()
    questions = _safe_json(_task_output(t1))

    a2 = get_rubric_builder_agent()
    t2 = task_build_rubric(a2, json.dumps(questions, indent=2))

    Crew(agents=[a2], tasks=[t2], process=Process.sequential, verbose=True).kickoff()

    return {
        "questions": questions,
        "rubric":    _safe_json(_task_output(t2)),
    }


# ── CREW 4: Candidate Evaluation ─────────────────────────────────────────────

def run_evaluation_crew(interview_notes: str, rubric: dict,
                        candidate_name: str, resume_text: str) -> dict:
    rubric_str = json.dumps(rubric, indent=2)

    a1 = get_interview_analyst_agent()
    t1 = task_analyze_interview(a1, interview_notes, rubric_str, candidate_name)

    Crew(agents=[a1], tasks=[t1], process=Process.sequential, verbose=True).kickoff()
    evaluation = _safe_json(_task_output(t1))

    a2 = get_reference_checker_agent()
    t2 = task_reference_check(a2, resume_text, json.dumps(evaluation, indent=2))

    Crew(agents=[a2], tasks=[t2], process=Process.sequential, verbose=True).kickoff()

    return {
        "evaluation":      evaluation,
        "reference_guide": _safe_json(_task_output(t2)),
    }


# ── CREW 5: Offer Generation ─────────────────────────────────────────────────

def run_offer_crew(candidate_name: str, job_title: str, company_name: str,
                   location: str, experience_years: int,
                   start_date: str, screening_report: dict) -> dict:

    a1 = get_salary_benchmarker_agent()
    t1 = task_benchmark_salary(a1, job_title, location, experience_years)

    Crew(agents=[a1], tasks=[t1], process=Process.sequential, verbose=True).kickoff()
    salary_data = _safe_json(_task_output(t1))

    a2 = get_offer_drafter_agent()
    a3 = get_negotiation_advisor_agent()
    t2 = task_draft_offer(a2, candidate_name, job_title, company_name,
                          json.dumps(salary_data, indent=2), start_date)
    t3 = task_negotiation_advice(a3, candidate_name,
                                  json.dumps(salary_data, indent=2),
                                  json.dumps(screening_report, indent=2))

    Crew(
        agents=[a2, a3],
        tasks=[t2, t3],
        process=Process.sequential,
        verbose=True,
    ).kickoff()

    return {
        "salary_data":       salary_data,
        "offer_letter":      _safe_json(_task_output(t2)),
        "negotiation_guide": _safe_json(_task_output(t3)),
    }
