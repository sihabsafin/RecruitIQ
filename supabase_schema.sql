-- ============================================================
-- RecruitIQ — Supabase Schema
-- Copy everything below and paste into Supabase SQL Editor
-- Then click RUN
-- ============================================================


-- 1. Job Descriptions
create table if not exists job_descriptions (
    id          uuid primary key default gen_random_uuid(),
    title       text not null,
    company     text,
    raw_text    text not null,
    parsed_json jsonb,
    created_at  timestamptz default now()
);


-- 2. Candidates
create table if not exists candidates (
    id               uuid primary key default gen_random_uuid(),
    jd_id            uuid references job_descriptions(id),
    name             text,
    email            text,
    resume_text      text,
    resume_url       text,
    match_score      float,
    screening_report jsonb,
    status           text default 'pending',
    created_at       timestamptz default now()
);


-- 3. Interview Kits
create table if not exists interview_kits (
    id           uuid primary key default gen_random_uuid(),
    candidate_id uuid references candidates(id),
    jd_id        uuid references job_descriptions(id),
    questions    jsonb,
    rubric       jsonb,
    created_at   timestamptz default now()
);


-- 4. Evaluations
create table if not exists evaluations (
    id              uuid primary key default gen_random_uuid(),
    candidate_id    uuid references candidates(id),
    interview_notes text,
    scores          jsonb,
    risk_flags      jsonb,
    recommendation  text,
    created_at      timestamptz default now()
);


-- 5. Offer Letters
create table if not exists offers (
    id               uuid primary key default gen_random_uuid(),
    candidate_id     uuid references candidates(id),
    salary_data      jsonb,
    offer_letter     text,
    negotiation_tips jsonb,
    status           text default 'draft',
    created_at       timestamptz default now()
);


-- ============================================================
-- Done! You should see 5 tables created successfully.
-- ============================================================
