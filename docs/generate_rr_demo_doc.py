"""
Generate RR Decision Intelligence Platform — Demo Documentation PDF
Updated: March 2026 — includes AI match brief, Render deployment, full feature set
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether, PageBreak
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
import os
from datetime import date

OUT = os.path.join(os.path.dirname(__file__), "RR_Demo_Platform_Documentation.pdf")

# ── Brand colours ────────────────────────────────────────────────────────────
RR_PINK   = colors.HexColor("#E8175D")
RR_BLUE   = colors.HexColor("#14336B")
RR_NAVY   = colors.HexColor("#06081A")
RR_DARK2  = colors.HexColor("#0C1230")
RR_LIGHT  = colors.HexColor("#EEF2FF")
RR_MUTED  = colors.HexColor("#7B8DB8")
WHITE     = colors.white
GREY_LINE = colors.HexColor("#D1D5DB")
DARK_TEXT = colors.HexColor("#1E293B")
GREEN_OK  = colors.HexColor("#059669")
RED_WARN  = colors.HexColor("#DC2626")
AMBER     = colors.HexColor("#D97706")
BG_PINK   = colors.HexColor("#FFF1F5")
BG_GREEN  = colors.HexColor("#F0FDF4")
BG_BLUE   = colors.HexColor("#F0F4FF")
BG_ALT    = colors.HexColor("#F8F9FF")

W, H = A4
M = 18 * mm   # margin

# ── Style definitions ────────────────────────────────────────────────────────
def _s(name, **kw):
    return ParagraphStyle(name, **kw)

S = {
    # Cover
    "label_upper": _s("label_upper", fontSize=7.5, textColor=RR_MUTED,
        fontName="Helvetica", alignment=TA_CENTER, spaceAfter=3, leading=11, letterSpacing=2),
    "cover_team":  _s("cover_team", fontSize=13, textColor=RR_LIGHT,
        fontName="Helvetica", alignment=TA_CENTER, spaceAfter=2, leading=17, letterSpacing=0.5),
    "cover_title": _s("cover_title", fontSize=34, textColor=WHITE,
        fontName="Helvetica-Bold", alignment=TA_CENTER, spaceAfter=4, leading=38),
    "cover_title_accent": _s("cover_title_accent", fontSize=34, textColor=RR_PINK,
        fontName="Helvetica-Bold", alignment=TA_CENTER, spaceAfter=4, leading=38),
    "cover_sub":   _s("cover_sub", fontSize=11, textColor=RR_MUTED,
        fontName="Helvetica", alignment=TA_CENTER, spaceAfter=3, leading=16),
    "cover_badge": _s("cover_badge", fontSize=8, textColor=RR_MUTED,
        fontName="Helvetica", alignment=TA_CENTER, spaceAfter=2, leading=12, letterSpacing=1.5),
    # Body
    "h1":     _s("h1", fontSize=13, textColor=RR_PINK, fontName="Helvetica-Bold",
        spaceBefore=12, spaceAfter=5, leading=17),
    "h2":     _s("h2", fontSize=10, textColor=RR_BLUE, fontName="Helvetica-Bold",
        spaceBefore=7, spaceAfter=4, leading=14),
    "body":   _s("body", fontSize=9, textColor=DARK_TEXT, fontName="Helvetica",
        spaceAfter=4, leading=14),
    "muted":  _s("muted", fontSize=8, textColor=RR_MUTED, fontName="Helvetica",
        spaceAfter=3, leading=12),
    "bullet": _s("bullet", fontSize=9, textColor=DARK_TEXT, fontName="Helvetica",
        leftIndent=10, spaceAfter=3, leading=13),
    # Table
    "th":   _s("th",   fontSize=8, textColor=WHITE,     fontName="Helvetica-Bold",
        alignment=TA_CENTER, leading=11),
    "tc":   _s("tc",   fontSize=8, textColor=DARK_TEXT, fontName="Helvetica",
        alignment=TA_LEFT, leading=11),
    "tc_c": _s("tc_c", fontSize=8, textColor=DARK_TEXT, fontName="Helvetica",
        alignment=TA_CENTER, leading=11),
    # Footer
    "footer": _s("footer", fontSize=7, textColor=RR_MUTED, fontName="Helvetica",
        alignment=TA_CENTER, leading=10),
    # Callout
    "callout": _s("callout", fontSize=9, textColor=RR_BLUE, fontName="Helvetica-Bold",
        spaceAfter=3, leading=13),
}

# ── Helpers ──────────────────────────────────────────────────────────────────
def rule(color=RR_PINK, thickness=1.5):
    return HRFlowable(width="100%", thickness=thickness, color=color,
                      spaceAfter=5, spaceBefore=2)

def grey_rule():
    return HRFlowable(width="100%", thickness=0.4, color=GREY_LINE,
                      spaceAfter=4, spaceBefore=4)

def sp(h=3):
    return Spacer(1, h * mm)

def bullet(text):
    return Paragraph(f"• &nbsp; {text}", S["bullet"])

def tbl_style(hbg=RR_BLUE, alt=True):
    cmds = [
        ("BACKGROUND",    (0,0), (-1,0),  hbg),
        ("TEXTCOLOR",     (0,0), (-1,0),  WHITE),
        ("FONTNAME",      (0,0), (-1,0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0,0), (-1,0),  8),
        ("ALIGN",         (0,0), (-1,0),  "CENTER"),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 7),
        ("RIGHTPADDING",  (0,0), (-1,-1), 7),
        ("GRID",          (0,0), (-1,-1), 0.35, GREY_LINE),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("FONTNAME",      (0,1), (-1,-1), "Helvetica"),
        ("FONTSIZE",      (0,1), (-1,-1), 8),
    ]
    if alt:
        cmds.append(("ROWBACKGROUNDS", (0,1), (-1,-1), [WHITE, BG_ALT]))
    return TableStyle(cmds)

# ── Cover page ───────────────────────────────────────────────────────────────
def cover():
    e = []
    e.append(sp(6))
    e.append(Paragraph("CONFIDENTIAL — DEMO DOCUMENTATION", S["label_upper"]))
    e.append(sp(3))

    # ── Hero banner: dark navy card with both names large ──────────
    hero_tbl = Table(
        [[
            Paragraph("RAJASTHAN ROYALS", _s("rr_hero",
                fontSize=36, textColor=RR_PINK, fontName="Helvetica-Bold",
                alignment=TA_CENTER, leading=40, spaceAfter=0)),
        ]],
        colWidths=[W - 2*M],
    )
    hero_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), RR_NAVY),
        ("TOPPADDING",    (0,0), (-1,-1), 18),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ("LEFTPADDING",   (0,0), (-1,-1), 14),
        ("RIGHTPADDING",  (0,0), (-1,-1), 14),
    ]))
    e.append(hero_tbl)

    dip_tbl = Table(
        [[Paragraph("CreaseIQ · Decision Intelligence Platform", _s("dip_hero",
            fontSize=22, textColor=WHITE, fontName="Helvetica-Bold",
            alignment=TA_CENTER, leading=26))]],
        colWidths=[W - 2*M],
    )
    dip_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), RR_BLUE),
        ("TOPPADDING",    (0,0), (-1,-1), 10),
        ("BOTTOMPADDING", (0,0), (-1,-1), 14),
        ("LEFTPADDING",   (0,0), (-1,-1), 14),
        ("RIGHTPADDING",  (0,0), (-1,-1), 14),
    ]))
    e.append(dip_tbl)

    e.append(sp(3))
    e.append(Paragraph("IPL 2026  ·  Front-Office Analytics  ·  v1.1", S["cover_badge"]))
    e.append(sp(6))
    e.append(rule())
    e.append(sp(3))

    meta = [
        ["Prepared for",   "Rajasthan Royals — Analytics & Performance Team"],
        ["Platform",       "CreaseIQ · RR Decision Intelligence Platform v1.1"],
        ["Date",           date.today().strftime("%B %d, %Y")],
        ["Live URL",       "https://ipl-auction-dashboard-1.onrender.com/rr_login.html"],
        ["Access code",    "royals2026"],
        ["Data coverage",  "IPL 2017–2025 · 1,169 matches · 350,000+ deliveries"],
        ["AI engine",      "Groq · Llama 3.3 70B — match brief generation"],
    ]
    mt = Table(meta, colWidths=[48*mm, W - 2*M - 48*mm])
    mt.setStyle(TableStyle([
        ("FONTNAME",      (0,0), (0,-1), "Helvetica-Bold"),
        ("FONTNAME",      (1,0), (1,-1), "Helvetica"),
        ("FONTSIZE",      (0,0), (-1,-1), 9),
        ("TEXTCOLOR",     (0,0), (0,-1), RR_BLUE),
        ("TEXTCOLOR",     (1,0), (1,-1), DARK_TEXT),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LINEBELOW",     (0,0), (-1,-2), 0.3, GREY_LINE),
    ]))
    e.append(mt)
    e.append(sp(8))

    # Two-column summary cards
    sum_left = (
        "<b>What this is:</b> The <b>Rajasthan Royals Decision Intelligence Platform</b> is a "
        "franchise-specific front-office analytics tool converting ball-by-ball IPL data into "
        "prescriptive intelligence — auction strategy, match planning, salary valuation, "
        "scouting, and AI-generated match briefs."
    )
    sum_right = (
        "<b>Why RR:</b> RR discloses ₹15.79 Cr analytics spend (FY25, +18.7% YoY) with "
        "52.8% going offshore. The <b>Decision Intelligence Platform</b> delivers domestic, "
        "franchise-tailored intelligence at a fraction of that cost."
    )
    sum_tbl = Table(
        [[Paragraph(sum_left, S["body"]), Paragraph(sum_right, S["body"])]],
        colWidths=[(W - 2*M - 4*mm)/2, (W - 2*M - 4*mm)/2],
        hAlign="LEFT"
    )
    sum_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (0,0), BG_BLUE),
        ("BACKGROUND",    (1,0), (1,0), BG_PINK),
        ("VALIGN",        (0,0), (-1,-1), "TOP"),
        ("TOPPADDING",    (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("RIGHTPADDING",  (0,0), (-1,-1), 8),
        ("BOX",           (0,0), (0,0), 0.5, RR_BLUE),
        ("BOX",           (1,0), (1,0), 0.5, RR_PINK),
        ("ROUNDEDCORNERS", [4]),
    ]))
    e.append(sum_tbl)
    e.append(sp(4))
    return e

# ── Section 1: Platform overview ─────────────────────────────────────────────
def section_overview():
    e = []
    e.append(Paragraph("1. Decision Intelligence Platform — Overview", S["h1"]))
    e.append(rule())
    e.append(Paragraph(
        "Nine integrated modules built on a single Python data pipeline. The payload is "
        "pre-computed from Cricsheet ball-by-ball data and served as a JavaScript object — "
        "keeping the front end fast and the quantitative backbone rigorous.",
        S["body"]))
    e.append(sp(2))

    rows = [
        ["Module", "Purpose", "RR Mode", "Status"],
        ["RR Hub",             "Branded landing page — next-match card, fixture strip, squad overview", "✓ Default", "✓ Live"],
        ["Password Gate",      "Session auth — branded login card, shake animation, sessionStorage", "✓ Included", "✓ Live"],
        ["AI Match Brief",     "Claude Sonnet 4.6 generates structured tactical brief from match data", "✓ Integrated", "✓ Live"],
        ["Match Planning",     "Opponent-aware SWOT + phase tactics for all 14 RR 2026 fixtures", "✓ Auto-selects RR", "✓ Live"],
        ["Salary Value Lab",   "Fair salary vs 2026 contract; SVI + value gap for full IPL player pool", "✓ Defaults RR squad", "✓ Live"],
        ["Matchup Intelligence","Ball-by-ball H2H batter vs bowler with direct dismissal weighting", "✓ Accessible", "✓ Live"],
        ["Auction War Room",   "Shared-league simulation with 500 Monte Carlo auction paths", "✓ Accessible", "✓ Live"],
        ["Batter Diagnostics", "Phase/pressure/venue/bowling-family breakdown per batter", "✓ Accessible", "✓ Live"],
        ["Phase Studio",       "Bayesian-shrunk phase impact leaderboard — PP / middle / death", "✓ Accessible", "✓ Live"],
    ]
    cw = [34*mm, 82*mm, 26*mm, 18*mm]
    t = Table(rows, colWidths=cw)
    st = tbl_style()
    for i in range(1, len(rows)):
        st.add("TEXTCOLOR", (3,i), (3,i), GREEN_OK)
        st.add("FONTNAME",  (3,i), (3,i), "Helvetica-Bold")
        st.add("ALIGN",     (2,i), (3,i), "CENTER")
        if i == 3:  # AI Match Brief — highlight
            st.add("BACKGROUND", (0,i), (-1,i), BG_BLUE)
    t.setStyle(st)
    e.append(t)
    e.append(sp(3))

    # Tech stack callout
    tech_tbl = Table(
        [[
            Paragraph("<b>Data pipeline</b><br/>Python · Cricsheet CSVs · Bayesian shrinkage", S["muted"]),
            Paragraph("<b>Front end</b><br/>Vanilla HTML/CSS/JS · No framework build overhead", S["muted"]),
            Paragraph("<b>AI engine</b><br/>Claude Sonnet 4.6 (Anthropic API) · Structured JSON output", S["muted"]),
            Paragraph("<b>Deployment</b><br/>Render.com · Auto-deploy on git push · Always-on free tier", S["muted"]),
        ]],
        colWidths=[(W - 2*M - 9*mm)/4]*4,
    )
    tech_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), BG_ALT),
        ("BOX",           (0,0), (-1,-1), 0.4, GREY_LINE),
        ("INNERGRID",     (0,0), (-1,-1), 0.4, GREY_LINE),
        ("TOPPADDING",    (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING",   (0,0), (-1,-1), 7),
        ("RIGHTPADDING",  (0,0), (-1,-1), 7),
        ("VALIGN",        (0,0), (-1,-1), "TOP"),
    ]))
    e.append(tech_tbl)
    e.append(sp(4))
    return e

# ── Section 2: AI Match Brief ─────────────────────────────────────────────────
def section_ai_brief():
    e = []
    e.append(Paragraph("2. AI Match Brief — Claude Sonnet 4.6", S["h1"]))
    e.append(rule())
    e.append(Paragraph(
        "The platform integrates Anthropic's Claude Sonnet 4.6 to generate a fixture-specific "
        "match brief on demand. When the analyst clicks 'Generate AI Match Brief' on the RR Hub, "
        "the server assembles the full structured match context — venue profile, phase impact scores, "
        "matchup evidence, active core players — and sends it to the Claude API. "
        "The model returns a structured JSON object rendered directly in the hub.",
        S["body"]))
    e.append(sp(2))

    e.append(Paragraph("Output Structure (8 fields, always populated)", S["h2"]))
    fields = [
        ["Field", "Content", "Example (RR vs CSK, Mar 30)"],
        ["headline",               "One-sentence fixture framing", "\"RR's death-over control vs CSK's experience edge at Guwahati\""],
        ["opening_call",           "Tactical recommendation sentence", "\"Bowl first — venue favours chase, Sandeep Sharma leads PP\""],
        ["why_this_matchup_is_live","Key reason this fixture matters", "\"CSK's Dhoni unknown for 2026; RR's spin depth is untested\""],
        ["tactical_edges",         "Array of 2–4 RR advantages", "[\"Sandeep vs Gaikwad — 3 dismissals in H2H\", ...]"],
        ["matchup_watch",          "Array of critical player duels", "[\"Jaiswal vs Rahul Chahar\", ...]"],
        ["venue_read",             "Venue-specific strategy note", "\"168.1 avg; set 165–170 or chase — avoid loose PP bowling\""],
        ["risk_flags",             "Array of RR vulnerabilities", "[\"Parag's form gap mid-overs\", ...]"],
        ["recommended_plan",       "Array of concrete action items", "[\"Open Archer over 1–3\", \"Use Bishnoi against Dhoni\", ...]"],
    ]
    cw = [36*mm, 44*mm, W - 2*M - 80*mm]
    t = Table(fields, colWidths=cw)
    st = tbl_style()
    st.add("ALIGN", (0,1), (0,-1), "CENTER")
    t.setStyle(st)
    e.append(t)
    e.append(sp(2))

    e.append(Paragraph("Technical implementation", S["h2"]))
    impl = [
        "<b>Backend:</b> server.py assembles match context from the dashboard payload and POSTs to <i>api.anthropic.com/v1/messages</i>.",
        "<b>Model:</b> claude-sonnet-4-6 with max_tokens=2048 — sized to complete the full JSON without truncation.",
        "<b>Robustness:</b> Markdown code-fence stripping applied before JSON parsing; graceful fallback if parse fails.",
        "<b>Prompt design:</b> System prompt enforces cricket-literate language (opener, enforcer, death hitter, new-ball bowler) and prohibits inventing statistics not present in the context.",
        "<b>Latency:</b> Typically 4–8 seconds for a complete structured brief.",
    ]
    for i in impl:
        e.append(bullet(i))
    e.append(sp(4))
    return e

# ── Section 3: Demo access and walkthrough ───────────────────────────────────
def section_access():
    e = []
    e.append(Paragraph("3. Demo Access & Recommended Walkthrough", S["h1"]))
    e.append(rule())

    e.append(Paragraph("Access Details", S["h2"]))
    access = [
        ["Item", "Value"],
        ["Live URL",           "https://ipl-auction-dashboard-1.onrender.com/rr_login.html"],
        ["Access code",        "royals2026"],
        ["Session behaviour",  "Persists for browser tab — cleared on close"],
        ["Wrong password",     "Card shake animation + error banner"],
        ["Unauthenticated access", "Auto-redirect to login from any /rr_ page"],
    ]
    t = Table(access, colWidths=[44*mm, W - 2*M - 44*mm])
    t.setStyle(tbl_style())
    e.append(t)
    e.append(sp(3))

    e.append(Paragraph("10-Minute Demo Script", S["h2"]))
    steps = [
        ("<b>0:00 — Login (30 sec)</b>",
         "Open the live URL. Enter 'royals2026'. Land on the RR-branded hub with the RR monogram and IPL 2026 badge."),
        ("<b>0:30 — Hub overview (2 min)</b>",
         "Point to the Next Match card (RR vs CSK, Mar 30, Guwahati — auto-populated from the schedule). "
         "Scroll through the fixture strip (all 14 RR 2026 fixtures with dates, opponents, venues). "
         "Show the squad section summarising RR's active core."),
        ("<b>2:30 — AI Match Brief (2 min)</b>",
         "Click 'Generate AI Match Brief'. Wait 4–8 seconds. Walk through the rendered structured brief: "
         "headline, opening call, tactical edges, matchup watch, risk flags, recommended plan. "
         "Emphasise this is grounded in the structured match data — not hallucinated."),
        ("<b>4:30 — Match Planning (2 min)</b>",
         "Click 'Open Match Intelligence Brief'. Page auto-selects RR vs CSK, RR lens. "
         "Walk through SWOT (Sandeep Sharma vs CSK top-order; Guwahati avg 168.1). "
         "Switch lens to CSK to show opponent-awareness."),
        ("<b>6:30 — Salary Value Lab (2 min)</b>",
         "Click 'Open Value Lab'. Defaults to RR squad. Select Sandeep Sharma — SVI 350, "
         "current salary ₹4 Cr, model fair value ₹14 Cr, gap +₹10 Cr. "
         "Frame: 'The model tells you where the front office got value and where it didn't — before the next auction.'"),
        ("<b>8:30 — Wrap (1.5 min)</b>",
         "Switch to Matchup Intelligence, pull up Jaiswal vs Rahul Chahar head-to-head. "
         "Close by explaining the data spine: 350,000+ Cricsheet deliveries, "
         "Bayesian-shrunk phase metrics, shared auction simulation."),
    ]
    step_rows = []
    for label, desc in steps:
        step_rows.append([Paragraph(label, S["tc"]), Paragraph(desc, S["tc"])])
    st_tbl = Table(step_rows, colWidths=[36*mm, W - 2*M - 36*mm])
    st_tbl.setStyle(TableStyle([
        ("ROWBACKGROUNDS", (0,0), (-1,-1), [WHITE, BG_ALT]),
        ("TOPPADDING",    (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING",   (0,0), (-1,-1), 7),
        ("RIGHTPADDING",  (0,0), (-1,-1), 7),
        ("GRID",          (0,0), (-1,-1), 0.35, GREY_LINE),
        ("VALIGN",        (0,0), (-1,-1), "TOP"),
    ]))
    e.append(st_tbl)
    e.append(sp(4))
    return e

# ── Section 4: RR Squad Salary ───────────────────────────────────────────────
def section_salary():
    e = []
    e.append(Paragraph("4. RR Squad — Salary Valuation Snapshot", S["h1"]))
    e.append(rule())
    e.append(Paragraph(
        "Model-implied fair salary versus 2026 IPL contract. "
        "<b>Salary Value Index (SVI)</b> = 100 × Fair Salary / Current Salary. "
        "SVI &gt; 100: undervalued relative to model output. SVI &lt; 100: overvalued.",
        S["body"]))
    e.append(sp(2))

    rows = [
        ["Player", "Role", "Salary\n(₹Cr)", "Fair\n(₹Cr)", "Gap\n(₹Cr)", "SVI", "Verdict"],
        ["Yashaswi Jaiswal",    "Opening Bat",   "18.0", "9.7",  "−8.3", "54",  "Overvalued"],
        ["Ravindra Jadeja",     "All-Rounder",   "14.0", "14.1", "+0.1", "101", "Fair Value"],
        ["Riyan Parag",         "Bat / Captain", "14.0", "6.6",  "−7.4", "47",  "Overvalued"],
        ["Dhruv Jurel",         "WK / Bat",      "14.0", "4.8",  "−9.2", "34",  "Overvalued"],
        ["Jofra Archer",        "Pace",          "12.5", "9.6",  "−2.9", "77",  "Overvalued"],
        ["Shimron Hetmyer",     "Bat",           "11.0", "13.4", "+2.4", "122", "Undervalued"],
        ["Tushar Deshpande",    "Pace",          "6.5",  "4.1",  "−2.4", "63",  "Overvalued"],
        ["Sandeep Sharma",      "Pace",          "4.0",  "14.0", "+10.0","350", "Undervalued ★"],
        ["Sam Curran",          "All-Rounder",   "2.4",  "4.4",  "+2.0", "182", "Undervalued"],
        ["Kwena Maphaka",       "Pace",          "1.5",  "1.4",  "−0.1", "94",  "Fair Value"],
        ["Vaibhav Suryavanshi", "Bat",           "1.1",  "1.4",  "+0.3", "127", "Undervalued"],
        ["Donovan Ferreira",    "Bat",           "1.0",  "0.9",  "−0.1", "92",  "Fair Value"],
    ]
    cw = [40*mm, 24*mm, 16*mm, 16*mm, 16*mm, 12*mm, 24*mm]
    t = Table(rows, colWidths=cw)
    st = tbl_style()
    for i, row in enumerate(rows[1:], 1):
        v = row[6]
        if "Undervalued" in v:
            st.add("TEXTCOLOR", (6,i), (6,i), GREEN_OK)
            st.add("FONTNAME",  (6,i), (6,i), "Helvetica-Bold")
        elif "Overvalued" in v:
            st.add("TEXTCOLOR", (6,i), (6,i), RED_WARN)
        if "Sandeep" in row[0]:
            st.add("BACKGROUND", (0,i), (-1,i), BG_GREEN)
            st.add("FONTNAME",   (0,i), (-1,i), "Helvetica-Bold")
        st.add("ALIGN", (2,i), (5,i), "CENTER")
    t.setStyle(st)
    e.append(t)
    e.append(sp(2))

    callout = Table(
        [[Paragraph(
            "★  Sandeep Sharma (SVI 350) is the demo's strongest hook: RR contracted him at ₹4 Cr "
            "against a model-implied fair value of ₹14 Cr — a +₹10 Cr surplus for RR. "
            "Opens any salary-efficiency or retention-value conversation naturally.",
            S["body"])]],
        colWidths=[W - 2*M]
    )
    callout.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), BG_GREEN),
        ("BOX",           (0,0), (-1,-1), 1, GREEN_OK),
        ("TOPPADDING",    (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING",   (0,0), (-1,-1), 10),
        ("RIGHTPADDING",  (0,0), (-1,-1), 10),
    ]))
    e.append(callout)
    e.append(sp(4))
    return e

# ── Section 5: RR 2026 Fixture Schedule ──────────────────────────────────────
def section_fixtures():
    e = []
    e.append(Paragraph("5. RR IPL 2026 — Full Fixture Schedule", S["h1"]))
    e.append(rule())
    e.append(Paragraph(
        "All 14 RR fixtures are embedded in the platform payload. The hub auto-populates "
        "the Next Match card and the match planning module auto-selects the next upcoming RR fixture.",
        S["body"]))
    e.append(sp(2))

    rows = [
        ["#", "Date",   "Opponent", "Venue",                         "City",      "H/A",      "Time"],
        ["1",  "Mar 30","CSK",      "Barsapara Stadium",              "Guwahati",  "Home Alt",  "7:30 PM"],
        ["2",  "Apr 4", "GT",       "Narendra Modi Stadium",          "Ahmedabad", "Away",      "7:30 PM"],
        ["3",  "Apr 7", "MI",       "Barsapara Stadium",              "Guwahati",  "Home Alt",  "7:30 PM"],
        ["4",  "Apr 10","RCB",      "Barsapara Stadium",              "Guwahati",  "Home Alt",  "7:30 PM"],
        ["5",  "Apr 13","SRH",      "Rajiv Gandhi Intl Stadium",      "Hyderabad", "Away",      "7:30 PM"],
        ["6",  "Apr 19","KKR",      "Eden Gardens",                   "Kolkata",   "Away",      "3:30 PM"],
        ["7",  "Apr 22","LSG",      "BRSABVE Stadium",                "Lucknow",   "Away",      "7:30 PM"],
        ["8",  "Apr 25","SRH",      "Sawai Mansingh Stadium",         "Jaipur",    "Home",      "7:30 PM"],
        ["9",  "Apr 28","PBKS",     "PCA Stadium",                    "Mullanpur", "Away",      "7:30 PM"],
        ["10", "May 1", "DC",       "Sawai Mansingh Stadium",         "Jaipur",    "Home",      "3:30 PM"],
        ["11", "May 9", "GT",       "Sawai Mansingh Stadium",         "Jaipur",    "Home",      "7:30 PM"],
        ["12", "May 17","DC",       "Arun Jaitley Stadium",           "Delhi",     "Away",      "7:30 PM"],
        ["13", "May 19","LSG",      "Sawai Mansingh Stadium",         "Jaipur",    "Home",      "7:30 PM"],
        ["14", "May 24","MI",       "Wankhede Stadium",               "Mumbai",    "Away",      "3:30 PM"],
    ]
    cw = [8*mm, 15*mm, 14*mm, 52*mm, 22*mm, 18*mm, 18*mm]
    t = Table(rows, colWidths=cw)
    st = tbl_style()
    # Highlight next match
    st.add("BACKGROUND", (0,1), (-1,1), BG_PINK)
    st.add("FONTNAME",   (0,1), (-1,1), "Helvetica-Bold")
    st.add("TEXTCOLOR",  (0,1), (-1,1), RR_PINK)
    # Home matches in green
    for i, row in enumerate(rows[1:], 1):
        if row[5] == "Home":
            st.add("TEXTCOLOR", (5,i), (5,i), GREEN_OK)
            st.add("FONTNAME",  (5,i), (5,i), "Helvetica-Bold")
        st.add("ALIGN", (0,i), (0,i), "CENTER")
    t.setStyle(st)
    e.append(t)
    e.append(sp(2))
    e.append(Paragraph(
        "Highlighted row (pink) = next upcoming fixture auto-selected by the platform. "
        "Home Alt = home game played at Guwahati while Sawai Mansingh is under renovation.",
        S["muted"]))
    e.append(sp(4))
    return e

# ── Section 6: Match Intelligence — RR vs CSK ────────────────────────────────
def section_match_intel():
    e = []
    e.append(Paragraph("6. Sample Match Intelligence — RR vs CSK (Mar 30)", S["h1"]))
    e.append(rule())
    e.append(Paragraph(
        "Illustrative output from the Match Planning module for RR's first fixture. "
        "This is the brief an analyst sees on opening match_planning.html?team=RR.",
        S["body"]))
    e.append(sp(2))

    e.append(Paragraph("Venue Profile — Barsapara Stadium, Guwahati", S["h2"]))
    venue = [
        ["Metric", "Value", "Strategic Implication"],
        ["Avg innings total",    "168.1",  "Control ground — target 165–172; not a 190+ venue"],
        ["Matches in sample",    "10",     "Directional only; treat as moderate-confidence"],
        ["Tactical read",        "—",      "Field placement discipline > blind acceleration; death bowling crucial"],
    ]
    t = Table(venue, colWidths=[42*mm, 20*mm, W - 2*M - 62*mm])
    t.setStyle(tbl_style())
    e.append(t)
    e.append(sp(2))

    e.append(Paragraph("RR Active Core", S["h2"]))
    core = [
        ["Role",         "Player",             "Relevance"],
        ["Lead bat",     "Yashaswi Jaiswal",   "Primary anchor; highest impact score in RR squad; sets first-half platform"],
        ["Captain/No.3", "Riyan Parag",        "Tempo setter; needs PP platform from Jaiswal"],
        ["Finisher",     "Shimron Hetmyer",    "Death-overs specialist (overs 16–20); SVI 122 — undervalued retention pick"],
        ["Lead bowler",  "Sandeep Sharma",     "Swing in PP; best matchup vs Gaikwad / Conway — open bowling"],
        ["Pace threat",  "Jofra Archer",       "Powerplay wicket-taking; target: Ruturaj Gaikwad over 1–3"],
        ["Spin anchor",  "Ravi Bishnoi",       "Middle-overs controller (overs 7–15); restricts CSK's Dhoni in death"],
    ]
    t = Table(core, colWidths=[26*mm, 40*mm, W - 2*M - 66*mm])
    t.setStyle(tbl_style())
    e.append(t)
    e.append(sp(2))

    e.append(Paragraph("CSK Threat Map", S["h2"]))
    threats = [
        ["CSK Player",      "Threat Type",                          "Recommended RR Counter"],
        ["Ruturaj Gaikwad", "Consistent PP scorer; sets big totals", "Archer over 1–3; Sandeep Sharma swing in over 2"],
        ["Rahul Chahar",    "Spin in middle overs vs RR right-handers","Deploy Jaiswal as left-side anchor in PP for later mismatch"],
        ["Noor Ahmad",      "Left-arm wrist spin — traps right-handers","Promote Hetmyer (left-hand) to No.4 to break spin grip"],
        ["MS Dhoni",        "Death-over finisher; disrupts plans",   "Bishnoi + Sandeep Sharma to cramp off-side options"],
    ]
    t = Table(threats, colWidths=[34*mm, 54*mm, W - 2*M - 88*mm])
    t.setStyle(tbl_style())
    e.append(t)
    e.append(sp(4))
    return e

# ── Section 7: Commercial context ────────────────────────────────────────────
def section_commercial():
    e = []
    e.append(Paragraph("7. Commercial Context", S["h1"]))
    e.append(rule())

    e.append(Paragraph("RR Analytics Budget — Verified from Audited Accounts", S["h2"]))
    e.append(Paragraph(
        "Rajasthan Royals (Royal Multisport Pvt Ltd) explicitly reports 'Analytics and Trial Expenses' "
        "as a named line item. The data below is drawn from the FY2025 audited P&L.",
        S["body"]))
    e.append(sp(1))

    budget = [
        ["Metric",                    "Value",               "Source / Note"],
        ["RR analytics budget FY25",  "₹15.79 Crores",       "Audited P&L — Royal Multisport Pvt Ltd"],
        ["YoY growth",                "+18.7%",              "FY24: ₹13.29 Cr → FY25: ₹15.79 Cr"],
        ["Offshore vendor share",     "52.8%",               "Note 33 — foreign currency analytics spend"],
        ["Related-party tech vendor", "₹1.91 Cr",            "Note 29 — Blenheim Chalcot IT (new in FY25)"],
        ["Suggested entry contract",  "₹50–150 Lakhs/season","3–10% of current analytics budget"],
    ]
    t = Table(budget, colWidths=[52*mm, 38*mm, W - 2*M - 90*mm])
    st = tbl_style(RR_BLUE)
    st.add("TEXTCOLOR", (1,5), (1,5), GREEN_OK)
    st.add("FONTNAME",  (1,5), (1,5), "Helvetica-Bold")
    t.setStyle(st)
    e.append(t)
    e.append(sp(3))

    e.append(Paragraph("Pitch Positioning", S["h2"]))
    points = [
        "Selling the <b>modelling layer and product surface</b>, not the underlying Cricsheet data — which RR already accesses.",
        "Strongest entry modules: <b>Auction War Room + Salary Value Lab</b> (auction edge, RTM strategy) and <b>Match Planning + AI Brief</b> (weekly in-season tactical prep).",
        "Competitive moat: <b>decision-usefulness framing</b> — prescriptive intelligence, not descriptive statistics.",
        "Franchise-specific mode: all RR modules default to the RR squad, RR fixtures, and RR lens — not a generic cricket stats site.",
        "Scalable: payloads rebuild from source data; custom RR proprietary feeds (GPS, wearables, internal scouting) can be ingested without re-architecting.",
    ]
    for p in points:
        e.append(bullet(p))
    e.append(sp(3))

    e.append(Paragraph("Objection Handling", S["h2"]))
    obj = [
        ["Likely Objection",                        "Response"],
        ["\"We already have Cricsheet data\"",       "This sells the modelling and product layer: phase-shrunk metrics, auction simulation, matchup engine, AI brief synthesis."],
        ["\"Our analysts build these internally\"",  "This takes 6 months to build to this quality. We can be live next match."],
        ["\"The model is too simple\"",              "Every metric is explainable. Complexity can be added with your proprietary data on top."],
        ["\"Cost is too high\"",                     "Entry at ₹50 Lakhs is 3% of your current analytics spend. Pilot on auction module only."],
    ]
    t = Table(obj, colWidths=[62*mm, W - 2*M - 62*mm])
    t.setStyle(tbl_style(RR_PINK))
    e.append(t)
    e.append(sp(4))
    return e

# ── Section 8: Next steps ─────────────────────────────────────────────────────
def section_next():
    e = []
    e.append(Paragraph("8. Roadmap & Next Steps", S["h1"]))
    e.append(rule())

    rows = [
        ["Priority", "Action",                                          "Effort",  "Status"],
        ["1 — Done",  "Deploy to Render (live URL live)",                "Low",    "✓ Complete"],
        ["2 — Done",  "AI match brief (Claude Sonnet 4.6 integrated)",   "Medium", "✓ Complete"],
        ["3 — Week 1","Live score widget on RR Hub (CricAPI)",           "Low",    "Queued"],
        ["4 — Week 1","Bowler diagnostics (symmetric to batter module)", "Medium", "Queued"],
        ["5 — Week 1","Match brief PDF/PNG export",                     "Low",    "Queued"],
        ["6 — Week 2","Polish UI to full commercial grade",             "Medium", "Queued"],
        ["7 — Outreach","Cold outreach — RR Head of Analytics / CTO",  "—",      "Ready"],
    ]
    cw = [34*mm, 88*mm, 18*mm, 20*mm]
    t = Table(rows, colWidths=cw)
    st = tbl_style()
    for i in (1, 2):
        st.add("TEXTCOLOR", (3,i), (3,i), GREEN_OK)
        st.add("FONTNAME",  (3,i), (3,i), "Helvetica-Bold")
        st.add("BACKGROUND",(0,i), (-1,i), BG_GREEN)
    st.add("ALIGN", (2,1), (3,-1), "CENTER")
    t.setStyle(st)
    e.append(t)
    e.append(sp(4))
    return e

# ── Footer ────────────────────────────────────────────────────────────────────
def footer():
    return [
        grey_rule(),
        Paragraph(
            f"<b>Rajasthan Royals — Decision Intelligence Platform</b>  ·  Demo Documentation  ·  "
            f"Prepared {date.today().strftime('%B %d, %Y')}  ·  Confidential",
            S["footer"]),
    ]

# ── Build ─────────────────────────────────────────────────────────────────────
def build():
    doc = SimpleDocTemplate(
        OUT,
        pagesize=A4,
        leftMargin=M, rightMargin=M,
        topMargin=M,  bottomMargin=M,
        title="RR Decision Intelligence Platform — Demo Documentation",
        author="Piyush Zaware",
        subject="Rajasthan Royals Analytics Demo",
    )
    story = []
    story += cover()
    story += section_overview()
    story += section_ai_brief()
    story += section_access()
    story += section_salary()
    story += section_fixtures()
    story += section_match_intel()
    story += section_commercial()
    story += section_next()
    story += footer()
    doc.build(story)
    print(f"PDF written → {OUT}")

if __name__ == "__main__":
    build()
