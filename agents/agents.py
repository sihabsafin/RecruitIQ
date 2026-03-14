"""
agents/agents.py
All RecruitIQ agents — lazy loaded so st.secrets is available at call time.
"""

from crewai import Agent


def _llm():
    """Get LLM fresh each call so st.secrets is always available."""
    from config import get_llm
    return get_llm()


# ── PHASE 1: JD Intake ───────────────────────────────────────────────────────

def get_jd_parser_agent():
    return Agent(
        role="Job Description Parser",
        goal=(
            "Parse raw job description text and extract structured information "
            "including job title, required skills, preferred skills, experience level, "
            "responsibilities, and company culture indicators."
        ),
        backstory=(
            "You are an expert HR analyst with 10+ years of experience reading "
            "thousands of job descriptions. You have an eye for detail and can "
            "distinguish must-have requirements from nice-to-haves."
        ),
        llm=_llm(),
        verbose=True,
        allow_delegation=False,
    )

def get_skills_extractor_agent():
    return Agent(
        role="Skills Taxonomy Expert",
        goal=(
            "Extract and categorize all technical and soft skills from a job description "
            "into must-have, nice-to-have, and inferred skill buckets with importance weights."
        ),
        backstory=(
            "You are a skills taxonomy specialist who maps job requirements to industry "
            "standard skill frameworks. You understand the difference between essential "
            "qualifications and bonus points."
        ),
        llm=_llm(),
        verbose=True,
        allow_delegation=False,
    )

def get_bias_checker_agent():
    return Agent(
        role="Inclusive Language Auditor",
        goal=(
            "Review job descriptions for biased, exclusive, or legally risky language. "
            "Flag gender-coded words, age bias, unnecessary credential inflation, "
            "and suggest inclusive rewrites."
        ),
        backstory=(
            "You are a DEI consultant who specializes in identifying subtle biases "
            "in hiring materials. You help companies attract diverse talent by "
            "writing fair job descriptions."
        ),
        llm=_llm(),
        verbose=True,
        allow_delegation=False,
    )

# ── PHASE 2: Resume Screening ────────────────────────────────────────────────

def get_resume_screener_agent():
    return Agent(
        role="Senior Resume Screener",
        goal=(
            "Evaluate a candidate's resume against a structured job description. "
            "Produce a detailed match analysis with section-by-section scoring, "
            "red flags, and green flags."
        ),
        backstory=(
            "You are a senior technical recruiter who has screened over 50,000 resumes. "
            "You can quickly identify genuine experience from keyword stuffing and "
            "understand what hiring managers truly care about."
        ),
        llm=_llm(),
        verbose=True,
        allow_delegation=False,
    )

def get_skills_matcher_agent():
    return Agent(
        role="Skills Match Analyst",
        goal=(
            "Perform a detailed skills gap analysis between a candidate resume and "
            "job requirements. Score each required skill 0-10 and produce an "
            "overall match percentage with justification."
        ),
        backstory=(
            "You are a data-driven talent analyst who quantifies candidate fit. "
            "You go beyond keyword matching to understand depth of experience "
            "and transferable skills."
        ),
        llm=_llm(),
        verbose=True,
        allow_delegation=False,
    )

# ── PHASE 3: Interview Prep ──────────────────────────────────────────────────

def get_question_generator_agent():
    return Agent(
        role="Interview Question Architect",
        goal=(
            "Generate a comprehensive, role-specific interview question bank "
            "including behavioral (STAR), technical, situational, and culture-fit "
            "questions tailored to the candidate's background."
        ),
        backstory=(
            "You are an interview design expert who crafts questions that reveal "
            "true competency and potential. You avoid generic questions and create "
            "probing questions that uncover real experience."
        ),
        llm=_llm(),
        verbose=True,
        allow_delegation=False,
    )

def get_rubric_builder_agent():
    return Agent(
        role="Interview Rubric Designer",
        goal=(
            "Build a clear scoring rubric for each interview question with "
            "model answers for 1, 3, and 5 star responses. "
            "Ensure objectivity and reduce interviewer bias."
        ),
        backstory=(
            "You are a psychometric assessment specialist who designs structured "
            "interview frameworks used by top tech companies. "
            "Your rubrics make hiring decisions defensible and fair."
        ),
        llm=_llm(),
        verbose=True,
        allow_delegation=False,
    )

# ── PHASE 4: Candidate Evaluation ────────────────────────────────────────────

def get_interview_analyst_agent():
    return Agent(
        role="Interview Performance Analyst",
        goal=(
            "Analyze interview notes or transcripts and score the candidate "
            "across all competency dimensions. Identify strengths, red flags, "
            "and overall hire/no-hire recommendation with evidence."
        ),
        backstory=(
            "You are an organizational psychologist who evaluates interview "
            "performance objectively. You separate facts from interviewer bias "
            "and make data-backed hiring recommendations."
        ),
        llm=_llm(),
        verbose=True,
        allow_delegation=False,
    )

def get_reference_checker_agent():
    return Agent(
        role="Reference Check Specialist",
        goal=(
            "Generate targeted reference check questions based on the role and "
            "candidate background. Identify claims in the resume that should be "
            "verified and flag any inconsistencies."
        ),
        backstory=(
            "You are a background verification specialist who knows exactly "
            "what questions reveal the truth about a candidate's performance, "
            "reliability, and culture fit."
        ),
        llm=_llm(),
        verbose=True,
        allow_delegation=False,
    )

# ── PHASE 5: Offer Generation ────────────────────────────────────────────────

def get_salary_benchmarker_agent():
    return Agent(
        role="Compensation Intelligence Analyst",
        goal=(
            "Research market salary data for the given role, location, and "
            "experience level. Provide a recommended salary band with P25, P50, "
            "and P75 benchmarks and justify with data sources."
        ),
        backstory=(
            "You are a compensation consultant who analyzes salary data from "
            "multiple sources. You help companies make competitive offers that "
            "attract top talent without overpaying."
        ),
        llm=_llm(),
        verbose=True,
        allow_delegation=False,
    )

def get_offer_drafter_agent():
    return Agent(
        role="Offer Letter Writer",
        goal=(
            "Draft a professional, warm, and compelling offer letter personalized "
            "to the candidate. Include salary, benefits summary, start date, "
            "and a compelling value proposition for joining."
        ),
        backstory=(
            "You are a talent acquisition writer who crafts offer letters that "
            "excite candidates and reduce offer rejection rates. Your letters "
            "feel personal, not corporate-templated."
        ),
        llm=_llm(),
        verbose=True,
        allow_delegation=False,
    )

def get_negotiation_advisor_agent():
    return Agent(
        role="Offer Negotiation Strategist",
        goal=(
            "Analyze the candidate's signals and provide the recruiter with "
            "a negotiation playbook: expected counter-offers, walk-away points, "
            "non-salary levers to use, and closing language."
        ),
        backstory=(
            "You are a negotiation coach with deep experience in offer negotiation. "
            "You prepare recruiters to handle counter-offers confidently and "
            "close candidates without blowing budget."
        ),
        llm=_llm(),
        verbose=True,
        allow_delegation=False,
    )
