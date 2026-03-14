"""
utils/database.py
Supabase client wrapper + all DB operations for RecruitIQ.

Run the SQL in SCHEMA_SQL once in your Supabase SQL editor to set up tables.
"""

import os
from datetime import datetime
from typing import Optional
from supabase import create_client, Client
try:
    import streamlit as st
    SUPABASE_URL = st.secrets.get("SUPABASE_URL", "")
    SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", "")
except Exception:
    from config import SUPABASE_URL, SUPABASE_KEY

# ── Schema (run once in Supabase SQL editor) ─────────────────────────────────
SCHEMA_SQL = """
-- Job Descriptions
create table if not exists job_descriptions (
    id          uuid primary key default gen_random_uuid(),
    title       text not null,
    company     text,
    raw_text    text not null,
    parsed_json jsonb,
    created_at  timestamptz default now()
);

-- Candidates
create table if not exists candidates (
    id           uuid primary key default gen_random_uuid(),
    jd_id        uuid references job_descriptions(id),
    name         text,
    email        text,
    resume_text  text,
    resume_url   text,
    match_score  float,
    screening_report jsonb,
    status       text default 'pending',  -- pending | shortlisted | rejected
    created_at   timestamptz default now()
);

-- Interview Kits
create table if not exists interview_kits (
    id           uuid primary key default gen_random_uuid(),
    candidate_id uuid references candidates(id),
    jd_id        uuid references job_descriptions(id),
    questions    jsonb,
    rubric       jsonb,
    created_at   timestamptz default now()
);

-- Evaluations
create table if not exists evaluations (
    id              uuid primary key default gen_random_uuid(),
    candidate_id    uuid references candidates(id),
    interview_notes text,
    scores          jsonb,
    risk_flags      jsonb,
    recommendation  text,
    created_at      timestamptz default now()
);

-- Offer Letters
create table if not exists offers (
    id              uuid primary key default gen_random_uuid(),
    candidate_id    uuid references candidates(id),
    salary_data     jsonb,
    offer_letter    text,
    negotiation_tips jsonb,
    status          text default 'draft',
    created_at      timestamptz default now()
);
"""
# ─────────────────────────────────────────────────────────────────────────────

def get_client() -> Optional[Client]:
    if not SUPABASE_URL or not SUPABASE_KEY:
        return None
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def save_jd(title: str, company: str, raw_text: str, parsed_json: dict) -> Optional[str]:
    db = get_client()
    if not db:
        return None
    res = db.table("job_descriptions").insert({
        "title": title,
        "company": company,
        "raw_text": raw_text,
        "parsed_json": parsed_json,
    }).execute()
    return res.data[0]["id"] if res.data else None


def save_candidate(jd_id: str, name: str, email: str,
                   resume_text: str, match_score: float,
                   screening_report: dict) -> Optional[str]:
    db = get_client()
    if not db:
        return None
    res = db.table("candidates").insert({
        "jd_id": jd_id,
        "name": name,
        "email": email,
        "resume_text": resume_text,
        "match_score": match_score,
        "screening_report": screening_report,
        "status": "shortlisted" if match_score >= 70 else "pending",
    }).execute()
    return res.data[0]["id"] if res.data else None


def get_candidates_for_jd(jd_id: str) -> list:
    db = get_client()
    if not db:
        return []
    res = (db.table("candidates")
             .select("*")
             .eq("jd_id", jd_id)
             .order("match_score", desc=True)
             .execute())
    return res.data or []


def save_interview_kit(candidate_id: str, jd_id: str,
                       questions: list, rubric: dict) -> Optional[str]:
    db = get_client()
    if not db:
        return None
    res = db.table("interview_kits").insert({
        "candidate_id": candidate_id,
        "jd_id": jd_id,
        "questions": questions,
        "rubric": rubric,
    }).execute()
    return res.data[0]["id"] if res.data else None


def save_offer(candidate_id: str, salary_data: dict,
               offer_letter: str, negotiation_tips: dict) -> Optional[str]:
    db = get_client()
    if not db:
        return None
    res = db.table("offers").insert({
        "candidate_id": candidate_id,
        "salary_data": salary_data,
        "offer_letter": offer_letter,
        "negotiation_tips": negotiation_tips,
    }).execute()
    return res.data[0]["id"] if res.data else None
