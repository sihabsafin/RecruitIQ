"""
utils/execution_log.py
Terminal-style live execution log using st.components.v1.html
"""
import streamlit as st
import streamlit.components.v1 as components
import time


def _build_html(logs: list, status: str = "running") -> str:
    status_color = "#fbbf24" if status == "running" else ("#22c55e" if status == "complete" else "#ef4444")
    status_label = "RUNNING" if status == "running" else ("COMPLETE" if status == "complete" else "ERROR")

    rows_html = ""
    for i, (tag, color, msg) in enumerate(logs):
        ts = f"{i * 0.2:.1f}s"
        rows_html += f"""
        <div class="row" style="animation-delay:{i*0.04}s">
            <span class="ts">{ts}</span>
            <span class="tag" style="background:{color}22;color:{color};border-color:{color}44;">{tag}</span>
            <span class="msg">{msg}</span>
        </div>"""

    cursor = '<div class="cursor-row"><span class="ts"></span><span class="cursor"></span></div>' if status == "running" else ""

    return f"""<!DOCTYPE html>
<html>
<head>
<style>
  @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ background: transparent; font-family: 'JetBrains Mono', monospace; }}

  .terminal {{
    background: #0d0d14;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 24px 48px rgba(0,0,0,0.5);
  }}

  .titlebar {{
    background: #161622;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    padding: 10px 16px;
    display: flex;
    align-items: center;
    gap: 10px;
  }}
  .dots {{ display: flex; gap: 6px; }}
  .dot {{ width: 12px; height: 12px; border-radius: 50%; }}
  .dot-r {{ background: #ff5f57; }}
  .dot-y {{ background: #ffbd2e; }}
  .dot-g {{ background: #28ca41; }}
  .title {{
    color: rgba(255,255,255,0.3);
    font-size: 11px;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-left: 8px;
  }}
  .status {{
    margin-left: auto;
    font-size: 11px;
    color: {status_color};
    letter-spacing: 1px;
  }}
  .status-dot {{
    display: inline-block;
    width: 7px; height: 7px;
    border-radius: 50%;
    background: {status_color};
    margin-right: 6px;
    {"animation: pulse 1.2s ease-in-out infinite;" if status == "running" else ""}
  }}

  .body {{
    padding: 16px 20px;
    min-height: 140px;
    max-height: 320px;
    overflow-y: auto;
  }}

  .row {{
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 4px 0;
    opacity: 0;
    animation: fadein 0.25s ease forwards;
  }}
  .ts {{
    color: rgba(255,255,255,0.2);
    font-size: 11px;
    min-width: 30px;
    padding-top: 1px;
    flex-shrink: 0;
  }}
  .tag {{
    font-size: 10px;
    font-weight: 700;
    padding: 1px 7px;
    border-radius: 4px;
    letter-spacing: 1px;
    min-width: 54px;
    text-align: center;
    border: 1px solid;
    flex-shrink: 0;
    margin-top: 1px;
  }}
  .msg {{
    color: rgba(255,255,255,0.72);
    font-size: 12.5px;
    line-height: 1.5;
  }}

  .cursor-row {{
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 4px 0;
  }}
  .cursor {{
    display: inline-block;
    width: 8px; height: 16px;
    background: #a78bfa;
    border-radius: 1px;
    animation: blink 1s step-end infinite;
    margin-left: 46px;
  }}

  @keyframes fadein {{ to {{ opacity: 1; }} }}
  @keyframes blink {{ 0%,100%{{opacity:1}} 50%{{opacity:0}} }}
  @keyframes pulse {{ 0%,100%{{opacity:1}} 50%{{opacity:0.3}} }}

  .body::-webkit-scrollbar {{ width: 3px; }}
  .body::-webkit-scrollbar-thumb {{ background: rgba(139,92,246,0.3); border-radius: 99px; }}
</style>
</head>
<body>
<div class="terminal">
  <div class="titlebar">
    <div class="dots">
      <div class="dot dot-r"></div>
      <div class="dot dot-y"></div>
      <div class="dot dot-g"></div>
    </div>
    <span class="title">RECRUITIQ · EXECUTION LOG</span>
    <div class="status">
      <span class="status-dot"></span>{status_label}
    </div>
  </div>
  <div class="body" id="logbody">
    {rows_html}
    {cursor}
  </div>
</div>
<script>
  var el = document.getElementById('logbody');
  if(el) el.scrollTop = el.scrollHeight;
</script>
</body>
</html>"""


def run_crew_with_log(crew_fn, *args, phase_name="Crew", agents=None, **kwargs):
    """Run a crew function with a live terminal-style execution log."""
    if agents is None:
        agents = []

    placeholder = st.empty()
    logs = []

    def render(status="running"):
        with placeholder:
            components.html(_build_html(logs, status), height=320, scrolling=False)

    def add(tag, color, msg):
        logs.append((tag, color, msg))
        render("running")
        time.sleep(0.12)

    add("SYS",   "#64748b", f"Initializing {phase_name}")
    add("SYS",   "#64748b", "Model: LLaMA 3.3 70B  ·  Provider: GROQ  ·  Mode: Sequential")
    add("AGENT", "#a78bfa", f"Instantiating {len(agents)} specialist agents...")
    if agents:
        add("AGENT", "#a78bfa", "  ·  ".join(agents))
    add("TASK",  "#f59e0b", f"{len(agents)} tasks queued  →  Sequential pipeline starting")
    for i, agent in enumerate(agents):
        add("RUN", "#06b6d4", f"[{i+1}/{len(agents)}] {agent} → working...")
    add("LLM",   "#8b5cf6", "Sending prompts to Groq API  ·  Awaiting response...")

    try:
        result = crew_fn(*args, **kwargs)
        logs.append(("DONE", "#22c55e", f"✓ {phase_name} completed successfully"))
        render("complete")
        return result
    except Exception as e:
        logs.append(("ERROR", "#ef4444", str(e)[:100]))
        render("error")
        raise e
