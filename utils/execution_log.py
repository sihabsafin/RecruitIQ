"""
utils/execution_log.py
Terminal-style live execution log component for RecruitIQ.
Renders a macOS-style terminal window with real-time agent progress.
"""
import streamlit as st
import time


def terminal_log(placeholder, logs: list, status: str = "running"):
    """
    Renders a terminal-style execution log.
    logs: list of (tag, color, message) tuples
    status: running | complete | error
    """
    status_dot = "🟡" if status == "running" else ("🟢" if status == "complete" else "🔴")
    
    rows_html = ""
    for i, (tag, color, msg) in enumerate(logs):
        ts = f"{i * 0.2:.1f}s"
        rows_html += f"""
        <div style="display:flex;align-items:flex-start;gap:12px;padding:5px 0;animation:fadein 0.3s ease forwards;opacity:0;animation-delay:{i*0.05}s;">
            <span style="color:rgba(255,255,255,0.2);font-size:11px;min-width:28px;padding-top:1px;font-family:'JetBrains Mono',monospace;">{ts}</span>
            <span style="
                background:{color}22;color:{color};
                font-size:10px;font-weight:700;
                padding:1px 7px;border-radius:4px;
                letter-spacing:1px;min-width:52px;text-align:center;
                font-family:'JetBrains Mono',monospace;
                border:1px solid {color}44;
                flex-shrink:0;margin-top:1px;
            ">{tag}</span>
            <span style="color:rgba(255,255,255,0.75);font-size:12.5px;font-family:'JetBrains Mono',monospace;line-height:1.5;">{msg}</span>
        </div>"""

    # Blinking cursor if running
    cursor = ""
    if status == "running":
        cursor = """<div style="display:flex;align-items:center;gap:12px;padding:5px 0;">
            <span style="color:rgba(255,255,255,0.2);font-size:11px;min-width:28px;font-family:'JetBrains Mono',monospace;"></span>
            <span style="display:inline-block;width:8px;height:16px;background:#a78bfa;border-radius:1px;animation:blink 1s step-end infinite;"></span>
        </div>"""

    placeholder.markdown(f"""
<style>
@keyframes fadein {{ to {{ opacity:1; }} }}
@keyframes blink {{ 0%,100%{{opacity:1}} 50%{{opacity:0}} }}
@keyframes spin {{ to{{transform:rotate(360deg)}} }}
</style>
<div style="
    background:#0d0d14;
    border:1px solid rgba(255,255,255,0.08);
    border-radius:12px;
    overflow:hidden;
    font-family:'JetBrains Mono',monospace;
    margin:16px 0;
    box-shadow:0 24px 48px rgba(0,0,0,0.4);
">
    <!-- Title bar -->
    <div style="
        background:#161622;
        border-bottom:1px solid rgba(255,255,255,0.06);
        padding:10px 16px;
        display:flex;
        align-items:center;
        gap:10px;
    ">
        <div style="display:flex;gap:6px;">
            <div style="width:12px;height:12px;border-radius:50%;background:#ff5f57;"></div>
            <div style="width:12px;height:12px;border-radius:50%;background:#ffbd2e;"></div>
            <div style="width:12px;height:12px;border-radius:50%;background:#28ca41;"></div>
        </div>
        <span style="
            color:rgba(255,255,255,0.35);
            font-size:11px;
            letter-spacing:2px;
            text-transform:uppercase;
            margin-left:8px;
        ">RECRUITIQ · EXECUTION LOG</span>
        <div style="margin-left:auto;font-size:11px;color:rgba(255,255,255,0.25);">
            {status_dot} {"RUNNING" if status=="running" else ("COMPLETE" if status=="complete" else "ERROR")}
        </div>
    </div>
    <!-- Log body -->
    <div style="padding:16px 20px;min-height:160px;max-height:340px;overflow-y:auto;">
        {rows_html}
        {cursor}
    </div>
</div>
""", unsafe_allow_html=True)


def run_crew_with_log(crew_fn, *args, phase_name="Crew", agents=None, **kwargs):
    """
    Runs a crew function while showing a live terminal log.
    Returns the crew result.
    """
    if agents is None:
        agents = []

    placeholder = st.empty()
    logs = []

    def add_log(tag, color, msg):
        logs.append((tag, color, msg))
        terminal_log(placeholder, logs, status="running")

    # Boot sequence
    add_log("SYS", "#64748b", f"Initializing {phase_name} · Python 3.11")
    time.sleep(0.15)
    add_log("SYS", "#64748b", "Model: LLaMA 3.3 70B  ·  Provider: GROQ  ·  Mode: Sequential")
    time.sleep(0.15)
    add_log("AGENT", "#a78bfa", f"Instantiating {len(agents)} specialist agents...")
    time.sleep(0.1)
    if agents:
        add_log("AGENT", "#a78bfa", "  ·  ".join(agents))
    time.sleep(0.1)
    add_log("TASK", "#f59e0b", f"{len(agents)} tasks queued  →  Sequential pipeline starting")
    time.sleep(0.2)

    # Agent progress
    for i, agent in enumerate(agents):
        add_log("RUN", "#06b6d4", f"[{i+1}/{len(agents)}] {agent} → working...")
        time.sleep(0.1)

    add_log("LLM", "#8b5cf6", "Sending prompts to Groq API...")
    time.sleep(0.2)

    # Run the actual crew
    try:
        result = crew_fn(*args, **kwargs)
        logs.append(("DONE", "#22c55e", f"✓ {phase_name} completed successfully"))
        terminal_log(placeholder, logs, status="complete")
        return result
    except Exception as e:
        logs.append(("ERROR", "#ef4444", str(e)[:120]))
        terminal_log(placeholder, logs, status="error")
        raise e
