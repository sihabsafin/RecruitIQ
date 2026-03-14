"""
utils/pdf_report.py
Generates a professional candidate report PDF using reportlab.
"""

import io
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

# ── Color palette ─────────────────────────────────────────────────────────────
C_BG        = HexColor("#0a0a0f")
C_CARD      = HexColor("#13131f")
C_PURPLE    = HexColor("#7c3aed")
C_PURPLE_LT = HexColor("#a78bfa")
C_TEXT      = HexColor("#e8e6f0")
C_MUTED     = HexColor("#6b7280")
C_GREEN     = HexColor("#22c55e")
C_YELLOW    = HexColor("#fbbf24")
C_RED       = HexColor("#ef4444")
C_BORDER    = HexColor("#1f1f2e")
C_WHITE     = white


def _score_color(score):
    try:
        s = float(str(score).replace("%",""))
        if s >= 75: return C_GREEN
        if s >= 55: return C_YELLOW
        return C_RED
    except:
        return C_MUTED


def _safe_str(val, default="N/A"):
    if val is None: return default
    s = str(val).strip()
    return s if s else default


def _safe_list(val):
    if isinstance(val, list): return val
    return []


def generate_candidate_pdf(candidate: dict, jd_parsed: dict = None) -> bytes:
    """Generate a full candidate report PDF and return as bytes."""

    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        leftMargin=18*mm, rightMargin=18*mm,
        topMargin=16*mm, bottomMargin=16*mm,
    )

    W = A4[0] - 36*mm  # usable width

    # ── Styles ────────────────────────────────────────────────────────────────
    def style(name, **kw):
        defaults = dict(fontName="Helvetica", fontSize=10, textColor=C_TEXT,
                       leading=14, spaceAfter=0, spaceBefore=0)
        defaults.update(kw)
        return ParagraphStyle(name, **defaults)

    S_HERO_NAME  = style("hero_name",  fontName="Helvetica-Bold", fontSize=22, textColor=C_WHITE, leading=26)
    S_HERO_SUB   = style("hero_sub",   fontSize=11, textColor=C_PURPLE_LT, leading=14)
    S_SECTION    = style("section",    fontName="Helvetica-Bold", fontSize=9,
                         textColor=C_MUTED, leading=12, spaceBefore=14, spaceAfter=6)
    S_BODY       = style("body",       fontSize=9.5, textColor=C_TEXT, leading=14, spaceAfter=3)
    S_BODY_MUTED = style("body_muted", fontSize=9,   textColor=C_MUTED, leading=13, spaceAfter=2)
    S_BULLET     = style("bullet",     fontSize=9.5, textColor=C_TEXT, leading=14,
                         leftIndent=10, spaceAfter=3)
    S_LABEL      = style("label",      fontName="Helvetica-Bold", fontSize=8.5,
                         textColor=C_PURPLE_LT, leading=12)
    S_CENTER     = style("center",     fontSize=9,   textColor=C_MUTED, leading=12,
                         alignment=TA_CENTER)
    S_FOOTER     = style("footer",     fontSize=8,   textColor=C_MUTED, leading=10,
                         alignment=TA_CENTER)

    story = []

    screening = candidate.get("screening", {}) or {}
    skills_m  = candidate.get("skills_match", {}) or {}
    name      = _safe_str(candidate.get("name") or screening.get("candidate_name"))
    email     = _safe_str(candidate.get("email") or screening.get("candidate_email"))
    ai_score  = candidate.get("ai_score", 0)
    sem_score = candidate.get("semantic_score", 0)
    rec       = _safe_str(candidate.get("recommendation") or screening.get("recommendation"), "hold")
    summary   = _safe_str(screening.get("summary"))
    exp_years = _safe_str(screening.get("experience_years"))
    edu_match = _safe_str(screening.get("education_match"))
    job_title = _safe_str(jd_parsed.get("job_title") if jd_parsed else None, "Role")
    company   = _safe_str(jd_parsed.get("company_name") if jd_parsed else None, "")
    generated = datetime.now().strftime("%B %d, %Y at %H:%M")

    sc = _score_color(ai_score)
    rec_lower = rec.lower()
    rec_label = "Shortlist" if "shortlist" in rec_lower else ("Reject" if "reject" in rec_lower else "Hold")
    rec_color = C_GREEN if "shortlist" in rec_lower else (C_RED if "reject" in rec_lower else C_YELLOW)

    # ── HEADER BLOCK ──────────────────────────────────────────────────────────
    header_data = [[
        Paragraph(name, S_HERO_NAME),
        Table([[
            Paragraph(f"{float(str(ai_score).replace('%','')):.0f}%", style("big_score",
                fontName="Helvetica-Bold", fontSize=28, textColor=sc,
                leading=32, alignment=TA_CENTER)),
        ]], colWidths=[28*mm],
        style=TableStyle([
            ("BACKGROUND", (0,0), (-1,-1), C_CARD),
            ("ROUNDEDCORNERS", (0,0), (-1,-1), 6),
            ("ALIGN", (0,0), (-1,-1), "CENTER"),
            ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
            ("TOPPADDING",    (0,0),(-1,-1), 8),
            ("BOTTOMPADDING", (0,0),(-1,-1), 8),
        ])),
    ]]
    header_tbl = Table(header_data, colWidths=[W - 32*mm, 32*mm])
    header_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), C_PURPLE),
        ("TOPPADDING",    (0,0),(-1,-1), 10),
        ("BOTTOMPADDING", (0,0),(-1,-1), 10),
        ("LEFTPADDING",   (0,0),(-1,-1), 14),
        ("RIGHTPADDING",  (0,0),(-1,-1), 8),
        ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
        ("ROUNDEDCORNERS",(0,0),(-1,-1), 8),
    ]))
    story.append(header_tbl)
    story.append(Spacer(1, 4*mm))

    # Sub-header row
    sub_data = [[
        Paragraph(email, S_BODY_MUTED),
        Paragraph(f"Role: {job_title}" + (f" · {company}" if company else ""), S_BODY_MUTED),
        Paragraph(f"Generated: {generated}", style("gen", fontSize=8, textColor=C_MUTED,
                  leading=12, alignment=TA_RIGHT)),
    ]]
    sub_tbl = Table(sub_data, colWidths=[W*0.35, W*0.4, W*0.25])
    sub_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0),(-1,-1), C_CARD),
        ("TOPPADDING",    (0,0),(-1,-1), 6),
        ("BOTTOMPADDING", (0,0),(-1,-1), 6),
        ("LEFTPADDING",   (0,0),(-1,-1), 10),
        ("RIGHTPADDING",  (0,0),(-1,-1), 10),
        ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
        ("ROUNDEDCORNERS",(0,0),(-1,-1), 6),
    ]))
    story.append(sub_tbl)
    story.append(Spacer(1, 5*mm))

    # ── SCORE CARDS ROW ───────────────────────────────────────────────────────
    def score_card(label, value, color):
        try:
            v = f"{float(str(value).replace('%','')):.0f}%"
        except:
            v = str(value)
        return Table([[
            Paragraph(label, style(f"sc_lbl_{label}", fontSize=8, textColor=C_MUTED,
                      leading=10, alignment=TA_CENTER)),
            Paragraph(v, style(f"sc_val_{label}", fontName="Helvetica-Bold", fontSize=18,
                      textColor=color, leading=22, alignment=TA_CENTER)),
        ]], colWidths=[None],
        style=TableStyle([
            ("BACKGROUND", (0,0),(-1,-1), C_CARD),
            ("TOPPADDING",    (0,0),(-1,-1), 8),
            ("BOTTOMPADDING", (0,0),(-1,-1), 8),
            ("LEFTPADDING",   (0,0),(-1,-1), 6),
            ("RIGHTPADDING",  (0,0),(-1,-1), 6),
            ("ROUNDEDCORNERS",(0,0),(-1,-1), 6),
        ]))

    sec_scores = screening.get("section_scores", {}) or {}
    def gs(k):
        try: return float(str(sec_scores.get(k, ai_score)).replace("%",""))
        except: return float(str(ai_score).replace("%","")) * 0.9

    cards_data = [[
        score_card("AI Match",   ai_score,        _score_color(ai_score)),
        score_card("Semantic",   sem_score,       _score_color(sem_score)),
        score_card("Experience", gs("experience"), _score_color(gs("experience"))),
        score_card("Skills",     gs("skills"),     _score_color(gs("skills"))),
        score_card("Education",  gs("education"),  _score_color(gs("education"))),
    ]]
    cards_tbl = Table(cards_data, colWidths=[W/5]*5, hAlign="LEFT")
    cards_tbl.setStyle(TableStyle([
        ("LEFTPADDING",  (0,0),(-1,-1), 3),
        ("RIGHTPADDING", (0,0),(-1,-1), 3),
        ("VALIGN",       (0,0),(-1,-1), "MIDDLE"),
    ]))
    story.append(cards_tbl)
    story.append(Spacer(1, 5*mm))

    # ── RECOMMENDATION BANNER ─────────────────────────────────────────────────
    rec_tbl = Table([[
        Paragraph("RECOMMENDATION", style("rec_lbl", fontSize=8, fontName="Helvetica-Bold",
                  textColor=rec_color, leading=10)),
        Paragraph(rec_label.upper(), style("rec_val", fontSize=14, fontName="Helvetica-Bold",
                  textColor=rec_color, leading=18)),
    ]], colWidths=[40*mm, W - 40*mm])
    rec_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), HexColor("#13131f")),
        ("LINEBELOW",     (0,0),(-1,-1), 0.5, rec_color),
        ("LINETOP",       (0,0),(-1,-1), 0.5, rec_color),
        ("TOPPADDING",    (0,0),(-1,-1), 8),
        ("BOTTOMPADDING", (0,0),(-1,-1), 8),
        ("LEFTPADDING",   (0,0),(-1,-1), 12),
        ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
        ("ROUNDEDCORNERS",(0,0),(-1,-1), 6),
    ]))
    story.append(rec_tbl)
    story.append(Spacer(1, 5*mm))

    # ── SUMMARY ───────────────────────────────────────────────────────────────
    if summary and summary != "N/A":
        story.append(Paragraph("CANDIDATE SUMMARY", S_SECTION))
        story.append(HRFlowable(width=W, thickness=0.5, color=C_BORDER))
        story.append(Spacer(1, 2*mm))
        story.append(Paragraph(summary, S_BODY))
        story.append(Spacer(1, 4*mm))

    # ── QUICK FACTS ───────────────────────────────────────────────────────────
    facts = []
    if exp_years != "N/A": facts.append(("Experience", exp_years + " years"))
    if edu_match != "N/A": facts.append(("Education Match", edu_match.title()))
    must_cov = _safe_str(skills_m.get("must_have_coverage"))
    if must_cov != "N/A": facts.append(("Must-Have Coverage", must_cov))
    skills_sc = _safe_str(skills_m.get("overall_skills_score"))
    if skills_sc != "N/A": facts.append(("Skills Score", f"{skills_sc}%"))

    if facts:
        story.append(Paragraph("PROFILE AT A GLANCE", S_SECTION))
        story.append(HRFlowable(width=W, thickness=0.5, color=C_BORDER))
        story.append(Spacer(1, 2*mm))
        rows = []
        for i in range(0, len(facts), 2):
            row = []
            for label, val in facts[i:i+2]:
                cell = Table([[
                    Paragraph(label, S_LABEL),
                    Paragraph(val, style(f"fact_val_{label}", fontName="Helvetica-Bold",
                              fontSize=11, textColor=C_TEXT, leading=14)),
                ]], style=TableStyle([
                    ("BACKGROUND",    (0,0),(-1,-1), C_CARD),
                    ("TOPPADDING",    (0,0),(-1,-1), 8),
                    ("BOTTOMPADDING", (0,0),(-1,-1), 8),
                    ("LEFTPADDING",   (0,0),(-1,-1), 10),
                    ("ROUNDEDCORNERS",(0,0),(-1,-1), 6),
                ]))
                row.append(cell)
            while len(row) < 2:
                row.append(Paragraph("", S_BODY))
            rows.append(row)
        facts_tbl = Table(rows, colWidths=[W/2 - 2*mm, W/2 - 2*mm], hAlign="LEFT")
        facts_tbl.setStyle(TableStyle([
            ("LEFTPADDING",  (0,0),(-1,-1), 2),
            ("RIGHTPADDING", (0,0),(-1,-1), 2),
            ("TOPPADDING",   (0,0),(-1,-1), 2),
            ("BOTTOMPADDING",(0,0),(-1,-1), 2),
        ]))
        story.append(facts_tbl)
        story.append(Spacer(1, 4*mm))

    # ── GREEN / RED FLAGS ─────────────────────────────────────────────────────
    green_flags = _safe_list(screening.get("green_flags"))
    red_flags   = _safe_list(screening.get("red_flags"))

    if green_flags or red_flags:
        story.append(Paragraph("SCREENING FLAGS", S_SECTION))
        story.append(HRFlowable(width=W, thickness=0.5, color=C_BORDER))
        story.append(Spacer(1, 2*mm))

        left_items, right_items = [], []
        for f in green_flags[:5]:
            left_items.append(Paragraph(f"✓  {_safe_str(f)}", style("gf", fontSize=9,
                textColor=C_GREEN, leading=13, leftIndent=4, spaceAfter=3)))
        for f in red_flags[:4]:
            right_items.append(Paragraph(f"⚠  {_safe_str(f)}", style("rf", fontSize=9,
                textColor=C_RED, leading=13, leftIndent=4, spaceAfter=3)))

        if left_items or right_items:
            flags_data = [[
                left_items  or [Paragraph("No green flags", S_BODY_MUTED)],
                right_items or [Paragraph("No red flags",   S_BODY_MUTED)],
            ]]
            flags_tbl = Table(flags_data, colWidths=[W*0.5 - 3*mm, W*0.5 - 3*mm])
            flags_tbl.setStyle(TableStyle([
                ("VALIGN",       (0,0),(-1,-1), "TOP"),
                ("LEFTPADDING",  (0,0),(-1,-1), 6),
                ("RIGHTPADDING", (0,0),(-1,-1), 6),
                ("TOPPADDING",   (0,0),(-1,-1), 0),
                ("BOTTOMPADDING",(0,0),(-1,-1), 0),
                ("LINEAFTER",    (0,0),(0,-1), 0.5, C_BORDER),
            ]))
            story.append(flags_tbl)
        story.append(Spacer(1, 4*mm))

    # ── SKILLS BREAKDOWN ──────────────────────────────────────────────────────
    breakdown = _safe_list(skills_m.get("skills_match_breakdown"))
    if breakdown:
        story.append(Paragraph("SKILLS ASSESSMENT", S_SECTION))
        story.append(HRFlowable(width=W, thickness=0.5, color=C_BORDER))
        story.append(Spacer(1, 2*mm))

        rows = [[
            Paragraph("Skill", style("th", fontSize=8, fontName="Helvetica-Bold",
                      textColor=C_MUTED, leading=10)),
            Paragraph("Found", style("th2", fontSize=8, fontName="Helvetica-Bold",
                      textColor=C_MUTED, leading=10, alignment=TA_CENTER)),
            Paragraph("Score", style("th3", fontSize=8, fontName="Helvetica-Bold",
                      textColor=C_MUTED, leading=10, alignment=TA_CENTER)),
            Paragraph("Evidence", style("th4", fontSize=8, fontName="Helvetica-Bold",
                      textColor=C_MUTED, leading=10)),
        ]]
        for sk in breakdown[:12]:
            if not isinstance(sk, dict): continue
            found = sk.get("found_in_resume", False)
            score_val = sk.get("score_0_to_10", "?")
            try:
                sc_f = float(str(score_val))
                sc_color = C_GREEN if sc_f >= 7 else (C_YELLOW if sc_f >= 5 else C_RED)
            except:
                sc_color = C_MUTED
            rows.append([
                Paragraph(_safe_str(sk.get("skill")), style("sk_name", fontSize=9, textColor=C_TEXT, leading=12)),
                Paragraph("Yes" if found else "No", style("sk_found", fontSize=9,
                    textColor=C_GREEN if found else C_RED, leading=12, alignment=TA_CENTER)),
                Paragraph(f"{score_val}/10", style("sk_sc", fontSize=9, textColor=sc_color,
                    fontName="Helvetica-Bold", leading=12, alignment=TA_CENTER)),
                Paragraph(_safe_str(sk.get("evidence",""))[:80], style("sk_ev", fontSize=8,
                    textColor=C_MUTED, leading=11)),
            ])

        sk_tbl = Table(rows, colWidths=[W*0.25, W*0.1, W*0.1, W*0.55])
        sk_tbl.setStyle(TableStyle([
            ("BACKGROUND",    (0,0),(-1,0), C_CARD),
            ("ROWBACKGROUNDS",(0,1),(-1,-1), [HexColor("#0d0d14"), HexColor("#13131f")]),
            ("TOPPADDING",    (0,0),(-1,-1), 5),
            ("BOTTOMPADDING", (0,0),(-1,-1), 5),
            ("LEFTPADDING",   (0,0),(-1,-1), 8),
            ("RIGHTPADDING",  (0,0),(-1,-1), 8),
            ("LINEBELOW",     (0,0),(-1,0), 0.5, C_PURPLE),
            ("VALIGN",        (0,0),(-1,-1), "TOP"),
        ]))
        story.append(sk_tbl)
        story.append(Spacer(1, 4*mm))

    # ── KEYWORD HITS / GAPS ───────────────────────────────────────────────────
    kw_hits = _safe_list(screening.get("keyword_hits"))
    kw_gaps = _safe_list(screening.get("keyword_gaps"))

    if kw_hits or kw_gaps:
        story.append(Paragraph("KEYWORD ANALYSIS", S_SECTION))
        story.append(HRFlowable(width=W, thickness=0.5, color=C_BORDER))
        story.append(Spacer(1, 2*mm))

        def kw_pills(items, color):
            text = "  ·  ".join([_safe_str(k) for k in items[:15]])
            return Paragraph(text or "None", style(f"kw_{color}", fontSize=8.5,
                textColor=HexColor(color), leading=14))

        kw_data = [[
            [Paragraph("Matched Keywords", S_LABEL), Spacer(1,2), kw_pills(kw_hits, "#22c55e")],
            [Paragraph("Missing Keywords", S_LABEL), Spacer(1,2), kw_pills(kw_gaps, "#ef4444")],
        ]]
        kw_tbl = Table(kw_data, colWidths=[W*0.5 - 3*mm, W*0.5 - 3*mm])
        kw_tbl.setStyle(TableStyle([
            ("VALIGN",       (0,0),(-1,-1), "TOP"),
            ("LEFTPADDING",  (0,0),(-1,-1), 8),
            ("RIGHTPADDING", (0,0),(-1,-1), 8),
            ("TOPPADDING",   (0,0),(-1,-1), 6),
            ("BOTTOMPADDING",(0,0),(-1,-1), 6),
            ("BACKGROUND",   (0,0),(-1,-1), C_CARD),
            ("LINEAFTER",    (0,0),(0,-1), 0.5, C_BORDER),
            ("ROUNDEDCORNERS",(0,0),(-1,-1), 6),
        ]))
        story.append(kw_tbl)
        story.append(Spacer(1, 4*mm))

    # ── FOOTER ────────────────────────────────────────────────────────────────
    story.append(Spacer(1, 4*mm))
    story.append(HRFlowable(width=W, thickness=0.5, color=C_BORDER))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph(
        f"Generated by RecruitIQ · AI-Powered Hiring Platform · {generated}",
        S_FOOTER
    ))

    doc.build(story)
    return buf.getvalue()
