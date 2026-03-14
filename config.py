"""
config.py
Reads secrets from st.secrets (Streamlit Cloud) with os.getenv fallback for local.
Uses CrewAI 1.x LLM class (not langchain directly).
"""

import os


def _secret(key: str, default: str = "") -> str:
    """Read from st.secrets first, fallback to os.getenv."""
    try:
        import streamlit as st
        val = st.secrets.get(key, "")
        return val if val else os.getenv(key, default)
    except Exception:
        return os.getenv(key, default)


def get_llm(temperature: float = 0.3):
    """
    Returns CrewAI 1.x LLM object.
    Primary: Groq LLaMA 3.3 70B (free, fast)
    Fallback: Gemini 2.0 Flash
    """
    from crewai import LLM

    groq_key = _secret("GROQ_API_KEY")
    if groq_key:
        return LLM(
            model="groq/llama-3.3-70b-versatile",
            api_key=groq_key,
            temperature=temperature,
        )

    gemini_key = _secret("GEMINI_API_KEY")
    return LLM(
        model="gemini/gemini-2.0-flash",
        api_key=gemini_key,
        temperature=temperature,
    )


SUPABASE_URL = _secret("SUPABASE_URL")
SUPABASE_KEY = _secret("SUPABASE_KEY")
SERPER_KEY   = _secret("SERPER_API_KEY")
RESEND_KEY   = _secret("RESEND_API_KEY")
