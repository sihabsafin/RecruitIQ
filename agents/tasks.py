"""
agents/tasks.py
All RecruitIQ tasks — agents are passed in at call time (lazy loaded).
"""

from crewai import Task


# ── PHASE 1 TASKS ────────────────────────────────────────────────────────────

def task_parse_jd(agent, jd_text: str) -> Task:
    return Task(
        description=f"""
Parse the following job description and extract structured information.

JOB DESCRIPTION:
{jd_text}

Extract and return a JSON with:
- job_title
- company_name (if present)
- department
- experience_level (entry/mid/senior/lead)
- employment_type (full-time/part-time/contract)
- location (remote/hybrid/onsite + city)
- responsibilities (list)
- qualifications_required (list)
- qualifications_preferred (list)
- compensation_mentioned (yes/no + details)
- company_culture_signals (list of phrases)
""",
        expected_output="A detailed JSON object with all parsed JD fields.",
        agent=agent,
    )


def task_extract_skills(agent, jd_text: str) -> Task:
    return Task(
        description=f"""
Analyze the following job description and extract a complete skills taxonomy.

JOB DESCRIPTION:
{jd_text}

Return a JSON with:
- must_have_skills: list of {{skill, category, importance_weight (1-10)}}
- nice_to_have_skills: list of {{skill, category}}
- inferred_skills: skills implied but not explicitly stated
- skill_categories: breakdown by (technical / soft / domain / tool)
- red_flag_if_missing: top 3 skills that would disqualify a candidate
""",
        expected_output="A structured skills taxonomy JSON.",
        agent=agent,
    )


def task_check_bias(agent, jd_text: str) -> Task:
    return Task(
        description=f"""
Audit the following job description for biased, exclusive, or legally risky language.

JOB DESCRIPTION:
{jd_text}

Return a JSON with:
- bias_score: 0 (very biased) to 10 (fully inclusive)
- gender_coded_words: list of found words + gender lean
- age_bias_indicators: any found
- credential_inflation: unnecessary degree/year requirements
- exclusive_phrases: list of problematic phrases
- suggested_rewrites: dict of original -> inclusive alternative
- overall_assessment: short paragraph
""",
        expected_output="A bias audit report JSON.",
        agent=agent,
    )


# ── PHASE 2 TASKS ────────────────────────────────────────────────────────────

def task_screen_resume(agent, resume_text: str, jd_parsed: str) -> Task:
    return Task(
        description=f"""
Screen the following resume against the job requirements.

RESUME:
{resume_text}

JOB REQUIREMENTS (parsed):
{jd_parsed}

Return a JSON with:
- candidate_name
- candidate_email
- overall_match_score: 0-100
- experience_years: estimated
- education_match: strong/partial/weak
- section_scores: {{experience, skills, education, achievements}} each 0-100
- green_flags: list of strong positive signals
- red_flags: list of concerns
- keyword_hits: matched keywords from JD
- keyword_gaps: important missing keywords
- summary: 2-3 sentence recruiter summary
- recommendation: shortlist/hold/reject with reason
""",
        expected_output="A complete resume screening report JSON.",
        agent=agent,
    )


def task_match_skills(agent, resume_text: str, skills_taxonomy: str) -> Task:
    return Task(
        description=f"""
Perform a detailed skills gap analysis.

RESUME:
{resume_text}

REQUIRED SKILLS TAXONOMY:
{skills_taxonomy}

Return a JSON with:
- skills_match_breakdown: list of {{skill, found_in_resume, evidence, score_0_to_10}}
- must_have_coverage: percentage of must-have skills covered
- nice_to_have_coverage: percentage covered
- transferable_skills: skills not in JD but relevant
- skills_gap_summary: what the candidate would need to learn
- overall_skills_score: 0-100
""",
        expected_output="A detailed skills match analysis JSON.",
        agent=agent,
    )


# ── PHASE 3 TASKS ────────────────────────────────────────────────────────────

def task_generate_questions(agent, candidate_summary: str, jd_parsed: str) -> Task:
    return Task(
        description=f"""
Generate a complete interview question bank for this candidate and role.

CANDIDATE SUMMARY:
{candidate_summary}

JOB REQUIREMENTS:
{jd_parsed}

Return a JSON with:
- technical_questions: list of 5 role-specific technical questions
- behavioral_questions: list of 5 STAR-format behavioral questions
- situational_questions: list of 3 scenario-based questions
- culture_fit_questions: list of 3 questions
- red_flag_probing_questions: list of 2-3 questions targeting resume gaps
- opening_question: one warm-up question
- closing_question: one candidate-question prompt

Each question: question_text, purpose, follow_up_probes (list)
""",
        expected_output="A complete interview question bank JSON.",
        agent=agent,
    )


def task_build_rubric(agent, questions_json: str) -> Task:
    return Task(
        description=f"""
Build a scoring rubric for the following interview questions.

QUESTIONS:
{questions_json}

For each question provide:
- score_1_response: what a poor answer looks like
- score_3_response: what an average answer looks like
- score_5_response: what an excellent answer looks like
- key_indicators: 3 signals interviewers should listen for
- time_allocation: recommended minutes per question

Return as a JSON rubric document.
""",
        expected_output="A complete interview scoring rubric JSON.",
        agent=agent,
    )


# ── PHASE 4 TASKS ────────────────────────────────────────────────────────────

def task_analyze_interview(agent, interview_notes: str, rubric: str, candidate_name: str) -> Task:
    return Task(
        description=f"""
Analyze the interview performance of {candidate_name}.

INTERVIEW NOTES:
{interview_notes}

SCORING RUBRIC:
{rubric}

Return a JSON with:
- competency_scores: dict of competency -> score (0-100)
- overall_interview_score: 0-100
- strongest_areas: list
- areas_of_concern: list
- notable_quotes: standout things the candidate said
- red_flags_observed: any concerns that emerged
- hire_recommendation: strong_yes / yes / maybe / no / strong_no
- hire_justification: detailed paragraph
- suggested_next_steps: list
""",
        expected_output="A complete interview evaluation report JSON.",
        agent=agent,
    )


def task_reference_check(agent, resume_text: str, evaluation_summary: str) -> Task:
    return Task(
        description=f"""
Prepare a reference check guide for this candidate.

RESUME:
{resume_text}

INTERVIEW EVALUATION SUMMARY:
{evaluation_summary}

Return a JSON with:
- claims_to_verify: list of specific resume claims that need verification
- suggested_reference_questions: list of 8-10 targeted questions
- red_flags_to_probe: concerns from interview that references should address
- reference_call_script: opening and closing language for the call
- warning_signs_to_listen_for: list of response patterns that signal issues
""",
        expected_output="A complete reference check guide JSON.",
        agent=agent,
    )


# ── PHASE 5 TASKS ────────────────────────────────────────────────────────────

def task_benchmark_salary(agent, job_title: str, location: str, experience_years: int) -> Task:
    return Task(
        description=f"""
Research and benchmark compensation for this role.

ROLE: {job_title}
LOCATION: {location}
EXPERIENCE: {experience_years} years

Based on your knowledge of compensation data from Glassdoor, Levels.fyi,
LinkedIn Salary, and industry surveys, provide:

Return a JSON with:
- role_title: standardized title
- location: city/remote
- currency: local currency
- salary_band: {{p25, p50, p75, p90}} annual figures
- recommended_offer_range: {{min, max, target}}
- total_compensation_components: base / bonus / equity / benefits
- market_context: 1-2 sentences on current market for this role
- competing_companies: top 5 companies hiring for similar roles
- offer_competitiveness_tips: list of 3 tips
""",
        expected_output="A salary benchmarking report JSON.",
        agent=agent,
    )


def task_draft_offer(agent, candidate_name: str, job_title: str, company_name: str,
                     salary_data: str, start_date: str) -> Task:
    return Task(
        description=f"""
Draft a professional and compelling offer letter.

CANDIDATE: {candidate_name}
ROLE: {job_title}
COMPANY: {company_name}
SALARY DATA: {salary_data}
PROPOSED START DATE: {start_date}

Write a warm, professional offer letter that includes:
- Congratulations and excitement about the hire
- Role title, department, reporting structure
- Compensation details (salary, bonus, equity if applicable)
- Benefits highlights
- Start date and onboarding details
- Offer expiration date (suggest 5 business days)
- Warm closing that re-sells the company

Return as: {{"subject_line": "...", "offer_letter_text": "full letter..."}}
""",
        expected_output="A complete offer letter JSON with subject line and full text.",
        agent=agent,
    )


def task_negotiation_advice(agent, candidate_name: str, offer_details: str,
                             screening_report: str) -> Task:
    return Task(
        description=f"""
Prepare a negotiation playbook for the recruiter.

CANDIDATE: {candidate_name}
OFFER DETAILS: {offer_details}
CANDIDATE SCREENING REPORT: {screening_report}

Return a JSON with:
- candidate_leverage_assessment: how strong is their negotiating position
- likely_counter_offer_range: expected ask
- our_flexibility: where we can bend (salary / equity / PTO / start date)
- non_salary_levers: list of perks/benefits to offer instead of salary bump
- walk_away_point: the max we should go
- closing_scripts: 3 different ways to close the negotiation
- red_flags_that_signal_dropout_risk: warning signs to watch
- urgency_tactics: ethical ways to create decision urgency
""",
        expected_output="A complete negotiation strategy playbook JSON.",
        agent=agent,
    )
