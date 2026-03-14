# RecruitIQ 🎯
### End-to-end AI hiring pipeline — JD → Screen → Interview → Offer

Built with **CrewAI + Groq + Supabase + Streamlit** | Cost: **$0/month**

---

## What it does

RecruitIQ is a 5-phase autonomous hiring pipeline where each phase is powered by a dedicated CrewAI crew:

| Phase | Crew | What it does |
|-------|------|-------------|
| 1 | JD Intake | Parses JD, extracts skills taxonomy, audits for bias |
| 2 | Resume Screening | Scores resumes 0–100, ranks candidates, flags gaps |
| 3 | Interview Prep | Generates question bank + scoring rubric per candidate |
| 4 | Evaluation | Analyzes interview notes, gives hire/no-hire + reference guide |
| 5 | Offer Generator | Benchmarks salary, drafts offer letter, negotiation playbook |

---

## Tech Stack (all free)

| Layer | Tool | Free Limit |
|-------|------|------------|
| LLM | Groq LLaMA 3.3 70B | 14,400 req/day |
| LLM fallback | Google Gemini 2.0 Flash | 1,500 req/day |
| Agent framework | CrewAI (open source) | Unlimited |
| Embeddings | sentence-transformers (local) | Unlimited |
| Vector DB | ChromaDB (in-memory) | Unlimited |
| Database | Supabase PostgreSQL | 500MB free |
| File storage | Supabase Storage | 1GB free |
| Hosting | Streamlit Community Cloud | Unlimited public apps |
| Resume parsing | PyMuPDF (local) | Unlimited |

---

## Project Structure

```
recruitiq/
├── app.py                          # Main Streamlit entry point (dashboard)
├── config.py                       # LLM setup, env vars
├── requirements.txt
├── .env.example                    # Copy to .env and fill in keys
├── .streamlit/
│   ├── config.toml                 # UI theme config
│   └── secrets.toml.example        # For Streamlit Cloud deployment
│
├── agents/
│   ├── agents.py                   # All 12 CrewAI agents
│   └── tasks.py                    # All task definitions (one per agent action)
│
├── crews/
│   └── crews.py                    # 5 crew orchestrators
│
├── utils/
│   ├── database.py                 # Supabase helpers + schema SQL
│   ├── resume_parser.py            # PDF/DOCX text extraction
│   └── vector_store.py             # ChromaDB + sentence-transformers
│
└── pages/
    ├── 1_📋_JD_Intake.py
    ├── 2_🔍_Resume_Screening.py
    ├── 3_🎤_Interview_Prep.py
    ├── 4_📊_Evaluation.py
    └── 5_💼_Offer_Generator.py
```

---

## Deploy to Streamlit Community Cloud (GitHub → Live URL)

This project is designed to run **directly from GitHub** — no local setup needed.

### Step 1 — Fork / push to GitHub

Push this entire folder to a **public GitHub repo**.
Make sure these files are present at the root:
- `app.py`
- `requirements.txt`
- `packages.txt`
- `.streamlit/secrets.toml` (with empty values — safe to commit)

### Step 2 — Get your free API keys

| Service | URL | Free limit |
|---------|-----|------------|
| Groq | https://console.groq.com | 14,400 req/day |
| Supabase | https://supabase.com | 500MB DB + 1GB storage |
| Serper | https://serper.dev | 2,500 searches/month |
| Gemini (optional) | https://aistudio.google.com | 1,500 req/day |

### Step 3 — Set up Supabase tables

1. Create a free Supabase project
2. Go to **SQL Editor** in your project
3. Copy the SQL from `utils/database.py` → the `SCHEMA_SQL` string
4. Paste and run it — this creates all 5 tables

### Step 4 — Deploy on Streamlit Cloud

1. Go to **https://share.streamlit.io**
2. Click **Create app**
3. Select your GitHub repo
4. Set **Main file path** → `app.py`
5. Click **Advanced settings** → **Secrets**
6. Paste your real keys:

```toml
GROQ_API_KEY   = "gsk_xxxxxxxxxxxx"
SUPABASE_URL   = "https://xxxx.supabase.co"
SUPABASE_KEY   = "eyJxxxxxx"
SERPER_API_KEY = "xxxxxxxx"
```

7. Click **Deploy** — your app goes live at:
   `https://your-app-name.streamlit.app`

### That's it — no server, no Docker, no cost.

---

## Agents Overview

### Phase 1 — JD Intake Crew
- `JDParserAgent` — extracts structure from raw JD text
- `SkillsExtractorAgent` — builds must-have / nice-to-have taxonomy
- `BiasCheckerAgent` — flags exclusive language, suggests inclusive rewrites

### Phase 2 — Resume Screening Crew
- `ResumeScreenerAgent` — scores resume 0–100 with section breakdown
- `SkillsMatcherAgent` — skill-by-skill gap analysis with evidence

### Phase 3 — Interview Prep Crew
- `QuestionGeneratorAgent` — behavioral, technical, situational, culture-fit questions
- `RubricBuilderAgent` — 1/3/5 star scoring rubric per question

### Phase 4 — Evaluation Crew
- `InterviewAnalystAgent` — scores interview notes, gives hire recommendation
- `ReferenceCheckerAgent` — targeted reference questions + call script

### Phase 5 — Offer Generation Crew
- `SalaryBenchmarkerAgent` — P25/P50/P75/P90 salary bands for role + location
- `OfferDrafterAgent` — personalized offer letter with subject line
- `NegotiationAdvisorAgent` — counter-offer scenarios + closing scripts

---

## Capacity Estimate (free tier)

| Metric | Per Day |
|--------|---------|
| Resumes screened | ~200–500 |
| Full pipeline runs | ~30–50 |
| Concurrent users | ~20–30 |
| LLM requests (Groq) | 14,400 |

---

## Recruiter-Facing Features

- Multi-resume batch upload (PDF + DOCX)
- Candidate ranking table with sortable scores
- One-click interview kit generation
- Downloadable offer letters (.txt)
- Full pipeline output exportable as JSON
- Supabase audit trail for every hire decision

---

## License

MIT License — free to use, modify, and deploy.

---

*Built by Safin | Showcasing CrewAI multi-agent orchestration*
