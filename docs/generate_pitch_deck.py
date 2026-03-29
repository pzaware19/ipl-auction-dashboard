"""
RR Decision Intelligence Platform — Investor / Client Pitch Deck
Landscape A4, 10 slides, strong visual design
"""

from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
import os
from datetime import date

OUT = os.path.join(os.path.dirname(__file__), "RR_Pitch_Deck.pdf")

# ── Page dimensions ───────────────────────────────────────────────────────────
PW, PH = landscape(A4)   # 841.9 x 595.3 pt
M  = 14 * mm
CW = PW - 2 * M          # content width
CH = PH - 2 * M          # content height

# ── Colours ───────────────────────────────────────────────────────────────────
NAVY      = colors.HexColor("#06081A")
NAVY2     = colors.HexColor("#0C1230")
BLUE      = colors.HexColor("#14336B")
BLUE_MID  = colors.HexColor("#1E4D9B")
BLUE_LT   = colors.HexColor("#2F6FE0")
PINK      = colors.HexColor("#E8175D")
PINK_LT   = colors.HexColor("#FF4B82")
PINK_DIM  = colors.HexColor("#3D0518")
GOLD      = colors.HexColor("#F7C948")
WHITE     = colors.white
OFF_WHITE = colors.HexColor("#EEF2FF")
MUTED     = colors.HexColor("#7B8DB8")
GREY_LINE = colors.HexColor("#2A3560")
GREY_LITE = colors.HexColor("#D1D5DB")
DARK_TEXT = colors.HexColor("#1E293B")
GREEN     = colors.HexColor("#10B981")
GREEN_LT  = colors.HexColor("#34D399")
RED       = colors.HexColor("#EF4444")
BG_ALT    = colors.HexColor("#111830")
BG_CARD   = colors.HexColor("#111830")

# ── Styles ────────────────────────────────────────────────────────────────────
def _s(name, **kw):
    return ParagraphStyle(name, **kw)

S = {
    # Slide labels
    "eyebrow":   _s("eyebrow",   fontSize=7,  textColor=PINK,      fontName="Helvetica-Bold",
                    alignment=TA_LEFT, leading=10, letterSpacing=2.5, spaceAfter=3),
    "eyebrow_c": _s("eyebrow_c", fontSize=7,  textColor=PINK,      fontName="Helvetica-Bold",
                    alignment=TA_CENTER, leading=10, letterSpacing=2.5, spaceAfter=3),
    "slide_no":  _s("slide_no",  fontSize=7,  textColor=MUTED,     fontName="Helvetica",
                    alignment=TA_RIGHT,  leading=10),

    # Headlines
    "h_xl":   _s("h_xl",   fontSize=38, textColor=WHITE,    fontName="Helvetica-Bold",
                 alignment=TA_LEFT,   leading=42, spaceAfter=6),
    "h_xl_c": _s("h_xl_c", fontSize=38, textColor=WHITE,    fontName="Helvetica-Bold",
                 alignment=TA_CENTER, leading=42, spaceAfter=6),
    "h_xl_p": _s("h_xl_p", fontSize=38, textColor=PINK,     fontName="Helvetica-Bold",
                 alignment=TA_CENTER, leading=42, spaceAfter=6),
    "h_lg":   _s("h_lg",   fontSize=28, textColor=WHITE,    fontName="Helvetica-Bold",
                 alignment=TA_LEFT,   leading=32, spaceAfter=5),
    "h_lg_c": _s("h_lg_c", fontSize=28, textColor=WHITE,    fontName="Helvetica-Bold",
                 alignment=TA_CENTER, leading=32, spaceAfter=5),
    "h_md":   _s("h_md",   fontSize=18, textColor=WHITE,    fontName="Helvetica-Bold",
                 alignment=TA_LEFT,   leading=22, spaceAfter=4),
    "h_md_c": _s("h_md_c", fontSize=18, textColor=WHITE,    fontName="Helvetica-Bold",
                 alignment=TA_CENTER, leading=22, spaceAfter=4),
    "h_sm":   _s("h_sm",   fontSize=13, textColor=WHITE,    fontName="Helvetica-Bold",
                 alignment=TA_LEFT,   leading=16, spaceAfter=3),
    "h_sm_p": _s("h_sm_p", fontSize=13, textColor=PINK,     fontName="Helvetica-Bold",
                 alignment=TA_LEFT,   leading=16, spaceAfter=3),
    "h_sm_g": _s("h_sm_g", fontSize=13, textColor=GOLD,     fontName="Helvetica-Bold",
                 alignment=TA_LEFT,   leading=16, spaceAfter=3),
    "h_sm_c": _s("h_sm_c", fontSize=13, textColor=WHITE,    fontName="Helvetica-Bold",
                 alignment=TA_CENTER, leading=16, spaceAfter=3),

    # Body
    "body":    _s("body",    fontSize=9,  textColor=OFF_WHITE, fontName="Helvetica",
                  alignment=TA_LEFT,   leading=14, spaceAfter=4),
    "body_c":  _s("body_c",  fontSize=9,  textColor=OFF_WHITE, fontName="Helvetica",
                  alignment=TA_CENTER, leading=14, spaceAfter=4),
    "body_m":  _s("body_m",  fontSize=9,  textColor=MUTED,     fontName="Helvetica",
                  alignment=TA_LEFT,   leading=14, spaceAfter=4),
    "body_m_c":_s("body_m_c",fontSize=9,  textColor=MUTED,     fontName="Helvetica",
                  alignment=TA_CENTER, leading=14, spaceAfter=4),
    "bullet":  _s("bullet",  fontSize=9,  textColor=OFF_WHITE, fontName="Helvetica",
                  leftIndent=10, leading=14, spaceAfter=4),

    # Numbers / hero stats
    "stat_xl": _s("stat_xl", fontSize=52, textColor=PINK,     fontName="Helvetica-Bold",
                  alignment=TA_CENTER, leading=56, spaceAfter=2),
    "stat_lg": _s("stat_lg", fontSize=36, textColor=PINK,     fontName="Helvetica-Bold",
                  alignment=TA_CENTER, leading=40, spaceAfter=2),
    "stat_g":  _s("stat_g",  fontSize=36, textColor=GOLD,     fontName="Helvetica-Bold",
                  alignment=TA_CENTER, leading=40, spaceAfter=2),
    "stat_w":  _s("stat_w",  fontSize=36, textColor=WHITE,    fontName="Helvetica-Bold",
                  alignment=TA_CENTER, leading=40, spaceAfter=2),
    "stat_lbl":_s("stat_lbl",fontSize=7.5,textColor=MUTED,    fontName="Helvetica-Bold",
                  alignment=TA_CENTER, leading=11, letterSpacing=1.5),

    # Footer
    "footer":  _s("footer",  fontSize=7,  textColor=MUTED,    fontName="Helvetica",
                  alignment=TA_CENTER, leading=10),
    "footer_r":_s("footer_r",fontSize=7,  textColor=MUTED,    fontName="Helvetica",
                  alignment=TA_RIGHT,  leading=10),
}

# ── Helpers ───────────────────────────────────────────────────────────────────
def sp(h=3):
    return Spacer(1, h * mm)

def rule(c=PINK, t=1.2, w="100%"):
    return HRFlowable(width=w, thickness=t, color=c, spaceAfter=4, spaceBefore=2)

def dim_rule():
    return HRFlowable(width="100%", thickness=0.5, color=GREY_LINE, spaceAfter=3, spaceBefore=3)

def b(text, color=OFF_WHITE):
    style = _s("_b", fontSize=9, textColor=color, fontName="Helvetica",
               leftIndent=12, leading=14, spaceAfter=4)
    return Paragraph(f"→ &nbsp; {text}", style)

def dark_cell(content_para, bg=NAVY2, pad=6):
    """Wrap a paragraph in a dark rounded card."""
    t = Table([[content_para]], colWidths=[CW])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), bg),
        ("TOPPADDING",    (0,0), (-1,-1), pad),
        ("BOTTOMPADDING", (0,0), (-1,-1), pad),
        ("LEFTPADDING",   (0,0), (-1,-1), pad + 2),
        ("RIGHTPADDING",  (0,0), (-1,-1), pad + 2),
    ]))
    return t

def slide_footer(n, total=10):
    footer_tbl = Table(
        [[Paragraph("CreaseIQ · Rajasthan Royals · Decision Intelligence Platform · Confidential", S["footer"]),
          Paragraph(f"{n} / {total}", S["footer_r"])]],
        colWidths=[CW * 0.85, CW * 0.15],
    )
    footer_tbl.setStyle(TableStyle([
        ("TOPPADDING",    (0,0), (-1,-1), 0),
        ("BOTTOMPADDING", (0,0), (-1,-1), 0),
        ("LEFTPADDING",   (0,0), (-1,-1), 0),
        ("RIGHTPADDING",  (0,0), (-1,-1), 0),
    ]))
    return footer_tbl

def two_col(left_items, right_items, left_w=None, right_w=None):
    lw = left_w  or (CW / 2 - 3 * mm)
    rw = right_w or (CW / 2 - 3 * mm)
    left_content  = [i for i in left_items]
    right_content = [i for i in right_items]
    # Build as a table
    rows = max(len(left_content), len(right_content))
    while len(left_content)  < rows: left_content.append(Spacer(1, 0))
    while len(right_content) < rows: right_content.append(Spacer(1, 0))
    data = [[l, r] for l, r in zip(left_content, right_content)]
    t = Table(data, colWidths=[lw, rw])
    t.setStyle(TableStyle([
        ("TOPPADDING",    (0,0), (-1,-1), 0),
        ("BOTTOMPADDING", (0,0), (-1,-1), 0),
        ("LEFTPADDING",   (0,0), (-1,-1), 0),
        ("RIGHTPADDING",  (0,1), (-1,-1), 0),
        ("RIGHTPADDING",  (0,0), (0,-1),  4 * mm),
        ("VALIGN",        (0,0), (-1,-1), "TOP"),
    ]))
    return t

def stat_card(value, label, val_style="stat_lg", bg=NAVY2, border=PINK):
    t = Table(
        [[Paragraph(value, S[val_style])],
         [Paragraph(label, S["stat_lbl"])]],
        colWidths=[(CW / 3) - 3 * mm],
    )
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), bg),
        ("BOX",           (0,0), (-1,-1), 1, border),
        ("TOPPADDING",    (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING",   (0,0), (-1,-1), 4),
        ("RIGHTPADDING",  (0,0), (-1,-1), 4),
    ]))
    return t

def three_stat_row(stats):
    """stats = [(value, label, val_style, border_color), ...]"""
    cells = []
    for v, l, vs, bc in stats:
        cells.append(stat_card(v, l, vs, NAVY2, bc))
    w = (CW - 6 * mm) / 3
    t = Table([cells], colWidths=[w, w, w])
    t.setStyle(TableStyle([
        ("TOPPADDING",    (0,0), (-1,-1), 0),
        ("BOTTOMPADDING", (0,0), (-1,-1), 0),
        ("LEFTPADDING",   (0,0), (-1,-1), 0),
        ("RIGHTPADDING",  (0,0), (0,-1),  3 * mm),
        ("RIGHTPADDING",  (1,0), (1,-1),  3 * mm),
        ("RIGHTPADDING",  (2,0), (2,-1),  0),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ]))
    return t

def pink_bar():
    """Thin pink top-border accent strip."""
    t = Table([[""]], colWidths=[CW], rowHeights=[2])
    t.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,-1), PINK)]))
    return t

def section_tag(text):
    t = Table(
        [[Paragraph(text, _s("_tag", fontSize=7, textColor=PINK, fontName="Helvetica-Bold",
                              letterSpacing=2, alignment=TA_LEFT, leading=10))]],
        colWidths=[None],
        hAlign="LEFT",
    )
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), PINK_DIM),
        ("BOX",           (0,0), (-1,-1), 0.5, PINK),
        ("TOPPADDING",    (0,0), (-1,-1), 3),
        ("BOTTOMPADDING", (0,0), (-1,-1), 3),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("RIGHTPADDING",  (0,0), (-1,-1), 8),
    ]))
    return t

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDES
# ═══════════════════════════════════════════════════════════════════════════════

# ── SLIDE 1: COVER ────────────────────────────────────────────────────────────
def slide_cover():
    e = []
    e.append(pink_bar())
    e.append(sp(12))

    e.append(Paragraph("CREASEIQ  ·  DECISION INTELLIGENCE PLATFORM", _s("eye", fontSize=8, textColor=PINK,
        fontName="Helvetica-Bold", alignment=TA_CENTER, leading=11, letterSpacing=3, spaceAfter=4)))

    # Main title block
    title_tbl = Table(
        [[Paragraph("CreaseIQ", _s("rr_title", fontSize=52, textColor=PINK,
            fontName="Helvetica-Bold", alignment=TA_CENTER, leading=56))],
         [Paragraph("Decision Intelligence for Rajasthan Royals", _s("rr_sub", fontSize=26, textColor=WHITE,
            fontName="Helvetica-Bold", alignment=TA_CENTER, leading=30))]],
        colWidths=[CW],
    )
    title_tbl.setStyle(TableStyle([
        ("TOPPADDING",    (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ("LEFTPADDING",   (0,0), (-1,-1), 0),
        ("RIGHTPADDING",  (0,0), (-1,-1), 0),
    ]))
    e.append(title_tbl)

    e.append(sp(5))
    e.append(HRFlowable(width="40%", thickness=1, color=PINK, hAlign="CENTER",
                        spaceAfter=5, spaceBefore=3))

    e.append(Paragraph(
        "Ball-by-ball decision intelligence · Auction strategy · Match planning · Salary valuation · Live AI briefs",
        _s("tagline", fontSize=10, textColor=MUTED, fontName="Helvetica",
           alignment=TA_CENTER, leading=15)))

    e.append(sp(8))

    # Meta row
    meta = Table(
        [[Paragraph("IPL 2026  ·  Front-Office Analytics", S["body_m_c"]),
          Paragraph("|", S["body_m_c"]),
          Paragraph(f"March {date.today().year}", S["body_m_c"]),
          Paragraph("|", S["body_m_c"]),
          Paragraph("Prepared by CreaseIQ · Piyush Zaware", S["body_m_c"])]],
        colWidths=[CW*0.3, CW*0.04, CW*0.15, CW*0.04, CW*0.47],
    )
    meta.setStyle(TableStyle([
        ("TOPPADDING",    (0,0), (-1,-1), 0),
        ("BOTTOMPADDING", (0,0), (-1,-1), 0),
        ("LEFTPADDING",   (0,0), (-1,-1), 0),
        ("RIGHTPADDING",  (0,0), (-1,-1), 0),
        ("ALIGN",         (0,0), (-1,-1), "CENTER"),
    ]))
    e.append(meta)
    e.append(sp(6))
    e.append(slide_footer(1))
    return e

# ── SLIDE 2: THE OPPORTUNITY ──────────────────────────────────────────────────
def slide_opportunity():
    e = []
    e.append(pink_bar())
    e.append(sp(5))
    e.append(section_tag("THE OPPORTUNITY"))
    e.append(sp(3))
    e.append(Paragraph("RR spends ₹15.79 Crores on analytics.", S["h_lg"]))
    e.append(Paragraph("Over half goes offshore. The decision layer doesn't exist yet.", S["h_sm_p"]))
    e.append(sp(4))
    e.append(dim_rule())
    e.append(sp(3))

    # Four stat cards
    stat_w = (CW - 9 * mm) / 4
    cards = [
        ("₹15.79 Cr",  "Analytics & Trial Budget FY25",    36, PINK),
        ("+18.7%",     "YoY budget growth (FY24 → FY25)",  36, GOLD),
        ("52.8%",      "Share going to offshore vendors",  36, PINK),
        ("₹1.91 Cr",   "New related-party tech vendor FY25",36, MUTED),
    ]
    card_cells = []
    for val, lbl, fs, border in cards:
        tc = Table(
            [[Paragraph(val, _s("_cv", fontSize=fs, textColor=WHITE if border==MUTED else border,
                fontName="Helvetica-Bold", alignment=TA_CENTER, leading=fs+4))],
             [Paragraph(lbl, S["stat_lbl"])]],
            colWidths=[stat_w],
        )
        tc.setStyle(TableStyle([
            ("BACKGROUND",    (0,0), (-1,-1), NAVY2),
            ("BOX",           (0,0), (-1,-1), 1, border),
            ("TOPPADDING",    (0,0), (-1,-1), 10),
            ("BOTTOMPADDING", (0,0), (-1,-1), 10),
            ("LEFTPADDING",   (0,0), (-1,-1), 4),
            ("RIGHTPADDING",  (0,0), (-1,-1), 4),
        ]))
        card_cells.append(tc)

    stats_row = Table([card_cells], colWidths=[stat_w]*4)
    stats_row.setStyle(TableStyle([
        ("TOPPADDING",    (0,0), (-1,-1), 0),
        ("BOTTOMPADDING", (0,0), (-1,-1), 0),
        ("LEFTPADDING",   (0,0), (-1,-1), 0),
        ("RIGHTPADDING",  (0,0), (2,-1),  3 * mm),
        ("RIGHTPADDING",  (3,0), (3,-1),  0),
    ]))
    e.append(stats_row)
    e.append(sp(4))
    e.append(dim_rule())
    e.append(sp(3))

    callout = Table(
        [[Paragraph(
            "Source: Royal Multisport Pvt Ltd — Audited P&amp;L FY2025 · "
            "Note 33 (foreign currency spend) · Note 29 (related-party vendor)",
            _s("_src", fontSize=8, textColor=MUTED, fontName="Helvetica",
               alignment=TA_LEFT, leading=12))]],
        colWidths=[CW],
    )
    callout.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), NAVY2),
        ("LEFTPADDING",   (0,0), (-1,-1), 10),
        ("TOPPADDING",    (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("BOX",           (0,0), (-1,-1), 0.5, GREY_LINE),
    ]))
    e.append(callout)
    e.append(sp(4))
    e.append(slide_footer(2))
    return e

# ── SLIDE 3: THE PROBLEM ──────────────────────────────────────────────────────
def slide_problem():
    e = []
    e.append(pink_bar())
    e.append(sp(5))
    e.append(section_tag("THE PROBLEM"))
    e.append(sp(3))
    e.append(Paragraph("Generic cricket stats describe.\nThey don't help you decide.", S["h_lg"]))
    e.append(sp(5))

    col_w = (CW - 6 * mm) / 3

    def col_block(title, title_color, items, bg, border):
        rows = [[Paragraph(title, _s("_ct", fontSize=11, textColor=title_color,
                    fontName="Helvetica-Bold", alignment=TA_CENTER, leading=14))]]
        rows.append([HRFlowable(width="80%", thickness=1, color=border, hAlign="CENTER",
                                spaceAfter=4, spaceBefore=4)])
        for item in items:
            rows.append([Paragraph(item, _s("_ci", fontSize=8.5, textColor=OFF_WHITE,
                             fontName="Helvetica", alignment=TA_LEFT, leading=13,
                             leftIndent=6, spaceAfter=4))])
        t = Table(rows, colWidths=[col_w])
        t.setStyle(TableStyle([
            ("BACKGROUND",    (0,0), (-1,-1), bg),
            ("BOX",           (0,0), (-1,-1), 1,   border),
            ("TOPPADDING",    (0,0), (0,0),   10),
            ("BOTTOMPADDING", (0,0), (0,0),   6),
            ("TOPPADDING",    (0,1), (-1,-1), 4),
            ("BOTTOMPADDING", (0,1), (-1,-1), 4),
            ("LEFTPADDING",   (0,0), (-1,-1), 10),
            ("RIGHTPADDING",  (0,0), (-1,-1), 10),
            ("ALIGN",         (0,0), (0,0),   "CENTER"),
            ("VALIGN",        (0,0), (-1,-1), "TOP"),
        ]))
        return t

    left  = col_block("What teams have today", MUTED,
        ["Season batting averages", "Generic player rankings", "Static scouting reports",
         "One-size-fits-all matchup tables", "Post-match analysis only"],
        NAVY2, GREY_LINE)

    mid   = col_block("What teams actually need", GOLD,
        ["Phase-specific impact (PP/mid/death)", "Opponent-aware SWOT per fixture",
         "Salary vs fair-value comparison", "Live auction counterfactuals",
         "Decision-grade AI match briefs"],
        colors.HexColor("#1A1500"), GOLD)

    right = col_block("What we built", GREEN_LT,
        ["Bayesian-shrunk phase impact scores", "14-fixture match planning suite",
         "Salary Value Index for full IPL pool", "500-path Monte Carlo auction sim",
         "Groq-powered AI brief in < 2 seconds"],
        colors.HexColor("#061510"), GREEN)

    cols = Table([[left, mid, right]], colWidths=[col_w, col_w, col_w])
    cols.setStyle(TableStyle([
        ("TOPPADDING",    (0,0), (-1,-1), 0),
        ("BOTTOMPADDING", (0,0), (-1,-1), 0),
        ("LEFTPADDING",   (0,0), (-1,-1), 0),
        ("RIGHTPADDING",  (0,0), (0,-1),  3 * mm),
        ("RIGHTPADDING",  (1,0), (1,-1),  3 * mm),
        ("RIGHTPADDING",  (2,0), (2,-1),  0),
        ("VALIGN",        (0,0), (-1,-1), "TOP"),
    ]))
    e.append(cols)
    e.append(sp(4))
    e.append(slide_footer(3))
    return e

# ── SLIDE 4: THE PLATFORM ─────────────────────────────────────────────────────
def slide_platform():
    e = []
    e.append(pink_bar())
    e.append(sp(5))
    e.append(section_tag("THE PLATFORM"))
    e.append(sp(3))
    e.append(Paragraph("9 integrated decision tools. One data backbone. Zero setup.", S["h_lg"]))
    e.append(sp(4))

    modules = [
        ("AI Match Brief",      "Groq/Llama 3.3 70B generates structured tactical brief from match data",    PINK),
        ("Match Planning",      "Opponent-aware SWOT + phase tactics for all 14 RR 2026 fixtures",           PINK),
        ("Salary Value Lab",    "Fair salary vs 2026 contract · SVI + value gap in ₹Cr for full IPL pool",   PINK),
        ("Auction War Room",    "500 Monte Carlo shared-auction paths · role budgets · competitor modelling", GOLD),
        ("Matchup Intelligence","Ball-by-ball H2H batter vs bowler with direct dismissal weighting",          GOLD),
        ("Batter Diagnostics",  "Phase / pressure / venue / bowling-family / dismissal breakdown per batter", GOLD),
        ("Scenario Builder",    "Counterfactual auction: adjust RR priorities, replay the shared market",     BLUE_LT),
        ("Phase Studio",        "Bayesian-shrunk powerplay / middle / death impact leaderboards",             BLUE_LT),
        ("Live Score Widget",   "CricAPI integration · auto-activates during RR match windows",               GREEN_LT),
    ]

    rows = []
    row = []
    for i, (name, desc, accent) in enumerate(modules):
        cell = Table(
            [[Paragraph(name, _s("_mn", fontSize=9, textColor=accent,
                fontName="Helvetica-Bold", leading=12, spaceAfter=2))],
             [Paragraph(desc, _s("_md", fontSize=7.5, textColor=MUTED,
                fontName="Helvetica", leading=11))]],
            colWidths=[(CW - 6 * mm) / 3],
        )
        cell.setStyle(TableStyle([
            ("BACKGROUND",    (0,0), (-1,-1), NAVY2),
            ("BOX",           (0,0), (-1,-1), 0.5, accent),
            ("TOPPADDING",    (0,0), (-1,-1), 8),
            ("BOTTOMPADDING", (0,0), (-1,-1), 8),
            ("LEFTPADDING",   (0,0), (-1,-1), 9),
            ("RIGHTPADDING",  (0,0), (-1,-1), 9),
            ("LINEABOVE",     (0,0), (-1,0),  2, accent),
            ("VALIGN",        (0,0), (-1,-1), "TOP"),
        ]))
        row.append(cell)
        if len(row) == 3:
            rows.append(row)
            row = []
    if row:
        while len(row) < 3:
            row.append(Spacer(1, 0))
        rows.append(row)

    w = (CW - 6 * mm) / 3
    grid = Table(rows, colWidths=[w, w, w],
                 rowHeights=[None, None, None])
    grid.setStyle(TableStyle([
        ("TOPPADDING",    (0,0), (-1,-1), 0),
        ("BOTTOMPADDING", (0,0), (2,-2),  3 * mm),
        ("BOTTOMPADDING", (0,-1),(-1,-1), 0),
        ("LEFTPADDING",   (0,0), (-1,-1), 0),
        ("RIGHTPADDING",  (0,0), (1,-1),  3 * mm),
        ("RIGHTPADDING",  (2,0), (2,-1),  0),
        ("VALIGN",        (0,0), (-1,-1), "TOP"),
    ]))
    e.append(grid)
    e.append(sp(4))
    e.append(slide_footer(4))
    return e

# ── SLIDE 5: FEATURE — AI MATCH BRIEF ────────────────────────────────────────
def slide_ai_brief():
    e = []
    e.append(pink_bar())
    e.append(sp(5))
    e.append(section_tag("FEATURE SPOTLIGHT"))
    e.append(sp(3))

    left = [
        Paragraph("AI Match Brief", S["h_md"]),
        Paragraph("Tactical intelligence in under 2 seconds.", S["h_sm_p"]),
        sp(3),
        Paragraph(
            "One click on the RR Hub generates a full structured match brief "
            "powered by Groq's Llama 3.3 70B — grounded entirely in the platform's "
            "ball-by-ball data. No hallucinated statistics. No generic templates.",
            S["body"]),
        sp(3),
        b("Headline + opening tactical call"),
        b("Why this specific matchup is decisive"),
        b("2–4 concrete tactical edges for RR"),
        b("Key player duels to watch (matchup watch)"),
        b("Venue-specific strategy read"),
        b("Risk flags + recommended action plan"),
        sp(3),
        Paragraph("Powered by Groq · Llama 3.3 70B · Free tier · &lt; 2 sec response", S["body_m"]),
    ]

    right_rows = [
        ("headline",                 "\"RR's death-over control vs CSK at Guwahati\""),
        ("opening_call",             "\"Bowl first — 168 avg favours chase, Sandeep leads PP\""),
        ("why_this_matchup_is_live", "\"Dhoni unknown for 2026; RR spin depth untested\""),
        ("tactical_edges",           "[\"Sandeep vs Gaikwad — 3 H2H dismissals\", ...]"),
        ("matchup_watch",            "[\"Jaiswal vs Rahul Chahar\", ...]"),
        ("venue_read",               "\"168.1 avg; set 165–170 or chase\""),
        ("risk_flags",               "[\"Parag mid-overs form gap\", ...]"),
        ("recommended_plan",         "[\"Open Archer overs 1–3\", ...]"),
    ]
    right_table_rows = [
        [Paragraph("Field", _s("_rh", fontSize=7.5, textColor=MUTED, fontName="Helvetica-Bold",
                               alignment=TA_LEFT, leading=10)),
         Paragraph("Example output", _s("_rh", fontSize=7.5, textColor=MUTED,
                               fontName="Helvetica-Bold", alignment=TA_LEFT, leading=10))]
    ]
    for field, example in right_rows:
        right_table_rows.append([
            Paragraph(field, _s("_rf", fontSize=7.5, textColor=PINK_LT,
                                fontName="Courier", alignment=TA_LEFT, leading=11)),
            Paragraph(example, _s("_re", fontSize=7.5, textColor=OFF_WHITE,
                                  fontName="Helvetica", alignment=TA_LEFT, leading=11)),
        ])

    rw = (CW / 2 - 5 * mm)
    right_t = Table(right_table_rows, colWidths=[rw * 0.42, rw * 0.58])
    right_t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,0),  BLUE),
        ("BACKGROUND",    (0,1), (-1,-1), NAVY2),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [NAVY2, colors.HexColor("#0E1628")]),
        ("FONTSIZE",      (0,0), (-1,-1), 7.5),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 7),
        ("RIGHTPADDING",  (0,0), (-1,-1), 7),
        ("GRID",          (0,0), (-1,-1), 0.3, GREY_LINE),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("LINEABOVE",     (0,0), (-1,0),  2, PINK),
    ]))

    right = [right_t]

    lw = CW * 0.44
    rw2 = CW - lw - 6 * mm
    e.append(two_col(left, right, lw, rw2))
    e.append(sp(4))
    e.append(slide_footer(5))
    return e

# ── SLIDE 6: FEATURE — SALARY VALUE LAB ──────────────────────────────────────
def slide_salary():
    e = []
    e.append(pink_bar())
    e.append(sp(5))
    e.append(section_tag("FEATURE SPOTLIGHT"))
    e.append(sp(3))
    e.append(Paragraph("Salary Value Lab", S["h_md"]))
    e.append(Paragraph("You signed Sandeep Sharma at ₹4 Cr. The model says he's worth ₹14 Cr.", S["h_sm_p"]))
    e.append(sp(4))

    # Hero callout
    hero = Table(
        [[Paragraph("SVI  350", _s("_hero", fontSize=48, textColor=GOLD,
                fontName="Helvetica-Bold", alignment=TA_CENTER, leading=52)),
          Paragraph(
            "<b>Salary Value Index</b> = 100 × Fair Salary / Current Salary\n\n"
            "SVI <b>350</b> means Sandeep Sharma is contracted at <b>₹4 Cr</b> "
            "against a model-implied fair value of <b>₹14 Cr</b>.\n\n"
            "That is <b>+₹10 Crores of value captured by RR</b> in one signing.\n\n"
            "The platform surfaces this for every player in the IPL pool — "
            "not just RR. Use it for RTM decisions, auction targets, "
            "and retention valuations before every mega-auction.",
            _s("_hb", fontSize=9.5, textColor=OFF_WHITE, fontName="Helvetica",
               leading=15, alignment=TA_LEFT))]],
        colWidths=[CW * 0.28, CW * 0.72 - 4 * mm],
    )
    hero.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (0,-1), colors.HexColor("#1A1200")),
        ("BACKGROUND",    (1,0), (1,-1), NAVY2),
        ("BOX",           (0,0), (0,-1), 2, GOLD),
        ("BOX",           (1,0), (1,-1), 1, GREY_LINE),
        ("TOPPADDING",    (0,0), (-1,-1), 14),
        ("BOTTOMPADDING", (0,0), (-1,-1), 14),
        ("LEFTPADDING",   (0,0), (-1,-1), 12),
        ("RIGHTPADDING",  (0,0), (-1,-1), 12),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("RIGHTPADDING",  (0,0), (0,-1),  0),
        ("LEFTPADDING",   (1,0), (1,-1),  12),
    ]))
    e.append(hero)
    e.append(sp(4))

    # Mini table of selected RR players
    rows = [
        ["Player", "2026 Contract", "Model Fair Value", "Value Gap", "SVI", "Verdict"],
        ["Sandeep Sharma",  "₹4.0 Cr",  "₹14.0 Cr", "+₹10.0 Cr", "350", "Undervalued ★"],
        ["Shimron Hetmyer", "₹11.0 Cr", "₹13.4 Cr", "+₹2.4 Cr",  "122", "Undervalued"],
        ["Sam Curran",      "₹2.4 Cr",  "₹4.4 Cr",  "+₹2.0 Cr",  "182", "Undervalued"],
        ["Yashaswi Jaiswal","₹18.0 Cr", "₹9.7 Cr",  "−₹8.3 Cr",  "54",  "Overvalued"],
        ["Dhruv Jurel",     "₹14.0 Cr", "₹4.8 Cr",  "−₹9.2 Cr",  "34",  "Overvalued"],
    ]
    cw = [40*mm, 28*mm, 30*mm, 24*mm, 16*mm, 30*mm]
    t = Table(rows, colWidths=cw)
    st = TableStyle([
        ("BACKGROUND",    (0,0), (-1,0),  BLUE),
        ("TEXTCOLOR",     (0,0), (-1,0),  WHITE),
        ("FONTNAME",      (0,0), (-1,0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0,0), (-1,-1), 8),
        ("TOPPADDING",    (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ("LEFTPADDING",   (0,0), (-1,-1), 7),
        ("RIGHTPADDING",  (0,0), (-1,-1), 7),
        ("GRID",          (0,0), (-1,-1), 0.3, GREY_LINE),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [NAVY2, colors.HexColor("#0E1628")]),
        ("FONTNAME",      (0,1), (-1,-1), "Helvetica"),
        ("TEXTCOLOR",     (0,1), (-1,-1), OFF_WHITE),
        ("LINEABOVE",     (0,0), (-1,0),  2, PINK),
        ("ALIGN",         (3,0), (4,-1),  "CENTER"),
    ])
    # colour verdicts
    st.add("TEXTCOLOR", (5,1), (5,3), colors.HexColor("#34D399"))
    st.add("FONTNAME",  (5,1), (5,3), "Helvetica-Bold")
    st.add("TEXTCOLOR", (5,4), (5,5), RED)
    st.add("BACKGROUND",(0,1), (-1,1), colors.HexColor("#0D1A00"))
    st.add("TEXTCOLOR", (4,1), (4,1), GOLD)
    st.add("FONTNAME",  (4,1), (4,1), "Helvetica-Bold")
    t.setStyle(st)
    e.append(t)
    e.append(sp(3))
    e.append(slide_footer(6))
    return e

# ── SLIDE 7: FEATURE — AUCTION INTELLIGENCE ──────────────────────────────────
def slide_auction():
    e = []
    e.append(pink_bar())
    e.append(sp(5))
    e.append(section_tag("FEATURE SPOTLIGHT"))
    e.append(sp(3))
    e.append(Paragraph("Auction War Room", S["h_md"]))
    e.append(Paragraph("Know who you'll face competition for before the paddle goes up.", S["h_sm_p"]))
    e.append(sp(4))

    col_w = (CW - 4 * mm) / 2

    left = [
        Paragraph("How it works", _s("_hw", fontSize=10, textColor=GOLD,
                fontName="Helvetica-Bold", leading=13, spaceAfter=4)),
        b("500 Monte Carlo shared-auction simulations — every team bidding simultaneously"),
        b("Role-weighted team strategies for all 10 franchises"),
        b("Player expected price distribution across paths"),
        b("Focus team (RR) wins, misses, and rival pressure summary"),
        b("Scenario Builder: adjust RR purse, retained players, role priorities — re-run instantly"),
        sp(3),
        Paragraph("Why shared-auction matters", _s("_hw", fontSize=10, textColor=GOLD,
                fontName="Helvetica-Bold", leading=13, spaceAfter=4)),
        Paragraph(
            "Independent team-by-team analysis is economically incoherent — the same player "
            "cannot be acquired by two teams. The War Room runs one shared market, so "
            "competition effects, budget depletion, and rival priorities are all priced in.",
            S["body"]),
    ]

    right = [
        Paragraph("What RR gets out", _s("_hw", fontSize=10, textColor=GOLD,
                fontName="Helvetica-Bold", leading=13, spaceAfter=4)),
    ]

    output_rows = [
        ["Output",                "Decision value"],
        ["Expected clearing price","Know your ceiling before the room heats up"],
        ["Win probability by set", "Where in the auction is RR most competitive?"],
        ["Rival pressure ranking", "Which teams will push hardest on your targets?"],
        ["Role spend distribution","Are you over-concentrated in one phase?"],
        ["Missed targets log",     "Which high-need players went to others?"],
    ]
    ot = Table(output_rows, colWidths=[col_w * 0.42, col_w * 0.58])
    ot.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,0),  BLUE),
        ("TEXTCOLOR",     (0,0), (-1,0),  WHITE),
        ("FONTNAME",      (0,0), (-1,0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0,0), (-1,-1), 8),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 7),
        ("RIGHTPADDING",  (0,0), (-1,-1), 7),
        ("GRID",          (0,0), (-1,-1), 0.3, GREY_LINE),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [NAVY2, colors.HexColor("#0E1628")]),
        ("FONTNAME",      (0,1), (-1,-1), "Helvetica"),
        ("TEXTCOLOR",     (0,1), (-1,-1), OFF_WHITE),
        ("LINEABOVE",     (0,0), (-1,0),  2, GOLD),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ]))
    right.append(ot)

    e.append(two_col(left, right, col_w, col_w))
    e.append(sp(4))
    e.append(slide_footer(7))
    return e

# ── SLIDE 8: DATA BACKBONE ────────────────────────────────────────────────────
def slide_data():
    e = []
    e.append(pink_bar())
    e.append(sp(5))
    e.append(section_tag("THE DATA BACKBONE"))
    e.append(sp(3))
    e.append(Paragraph("Built on rigorous quantitative foundations.", S["h_lg"]))
    e.append(sp(4))

    # Five stat cards
    stat_w = (CW - 12 * mm) / 5
    stats = [
        ("1,169",  "IPL Matches\nAnalyzed",      PINK),
        ("350K+",  "Ball-by-Ball\nDeliveries",   PINK),
        ("2017–25","Seasons of\nCoverage",        GOLD),
        ("3",      "Phases\nModeled",             GOLD),
        ("500",    "Monte Carlo\nAuction Paths",  BLUE_LT),
    ]
    cells = []
    for val, lbl, c in stats:
        tc = Table(
            [[Paragraph(val, _s("_sv", fontSize=30, textColor=c,
                fontName="Helvetica-Bold", alignment=TA_CENTER, leading=34))],
             [Paragraph(lbl, S["stat_lbl"])]],
            colWidths=[stat_w],
        )
        tc.setStyle(TableStyle([
            ("BACKGROUND",    (0,0), (-1,-1), NAVY2),
            ("LINEABOVE",     (0,0), (-1,0),  3, c),
            ("TOPPADDING",    (0,0), (-1,-1), 8),
            ("BOTTOMPADDING", (0,0), (-1,-1), 8),
            ("LEFTPADDING",   (0,0), (-1,-1), 4),
            ("RIGHTPADDING",  (0,0), (-1,-1), 4),
        ]))
        cells.append(tc)

    stats_t = Table([cells], colWidths=[stat_w] * 5)
    stats_t.setStyle(TableStyle([
        ("TOPPADDING",    (0,0), (-1,-1), 0),
        ("BOTTOMPADDING", (0,0), (-1,-1), 0),
        ("LEFTPADDING",   (0,0), (-1,-1), 0),
        ("RIGHTPADDING",  (0,0), (3,-1),  3 * mm),
        ("RIGHTPADDING",  (4,0), (4,-1),  0),
    ]))
    e.append(stats_t)
    e.append(sp(4))

    # Three method cards
    method_w = (CW - 6 * mm) / 3
    methods = [
        ("Bayesian Phase Metrics",
         "Phase impact scores are shrunk toward the league mean to correct for "
         "sample-size noise. Small-sample players don't dominate leaderboards. "
         "Reliable signal from the first innings a player appears.", PINK),
        ("Shared Auction Simulation",
         "One common auction universe — a player cannot be acquired by two teams. "
         "Rival budget depletion, role-weighted demand, and set-order dynamics "
         "are all modelled in a single pass.", GOLD),
        ("Cricsheet Ball-by-Ball",
         "Every delivery from IPL 2017–2025: outcome, wicket type, venue, phase, "
         "pressure state, batter, bowler. No line/length/swing — we are explicit "
         "about what the data does and doesn't support.", BLUE_LT),
    ]
    mcells = []
    for title, body, c in methods:
        mc = Table(
            [[Paragraph(title, _s("_mt", fontSize=9.5, textColor=c,
                fontName="Helvetica-Bold", leading=13, spaceAfter=3))],
             [Paragraph(body, _s("_mb", fontSize=8, textColor=MUTED,
                fontName="Helvetica", leading=12))]],
            colWidths=[method_w],
        )
        mc.setStyle(TableStyle([
            ("BACKGROUND",    (0,0), (-1,-1), NAVY2),
            ("LINEABOVE",     (0,0), (-1,0),  2, c),
            ("TOPPADDING",    (0,0), (-1,-1), 8),
            ("BOTTOMPADDING", (0,0), (-1,-1), 8),
            ("LEFTPADDING",   (0,0), (-1,-1), 9),
            ("RIGHTPADDING",  (0,0), (-1,-1), 9),
            ("VALIGN",        (0,0), (-1,-1), "TOP"),
        ]))
        mcells.append(mc)

    method_t = Table([mcells], colWidths=[method_w] * 3)
    method_t.setStyle(TableStyle([
        ("TOPPADDING",    (0,0), (-1,-1), 0),
        ("BOTTOMPADDING", (0,0), (-1,-1), 0),
        ("LEFTPADDING",   (0,0), (-1,-1), 0),
        ("RIGHTPADDING",  (0,0), (1,-1),  3 * mm),
        ("RIGHTPADDING",  (2,0), (2,-1),  0),
        ("VALIGN",        (0,0), (-1,-1), "TOP"),
    ]))
    e.append(method_t)
    e.append(sp(3))
    e.append(slide_footer(8))
    return e

# ── SLIDE 9: COMMERCIAL ───────────────────────────────────────────────────────
def slide_commercial():
    e = []
    e.append(pink_bar())
    e.append(sp(5))
    e.append(section_tag("COMMERCIAL"))
    e.append(sp(3))
    e.append(Paragraph("Entry at ₹50–150 Lakhs. That's 3–10% of your current analytics budget.", S["h_lg"]))
    e.append(sp(4))

    col_w = (CW - 4 * mm) / 2

    left = [
        Paragraph("What you get", _s("_hw", fontSize=10, textColor=GOLD,
                fontName="Helvetica-Bold", leading=13, spaceAfter=5)),
    ]
    tiers = [
        ("Entry  ₹50 Lakhs/season",
         "Auction War Room + Salary Value Lab — the two highest-ROI modules. "
         "Full access ahead of the next mega-auction.", GOLD),
        ("Standard  ₹100 Lakhs/season",
         "Full platform: all 9 modules, AI match briefs, live score integration, "
         "match planning for all 14 RR fixtures.", PINK),
        ("Premium  ₹150 Lakhs/season",
         "Standard + custom data integration (RR proprietary GPS, wearables, "
         "internal scouting feeds) + dedicated model updates.", BLUE_LT),
    ]
    for label, body, c in tiers:
        tc = Table(
            [[Paragraph(label, _s("_tl", fontSize=9.5, textColor=c,
                fontName="Helvetica-Bold", leading=13, spaceAfter=2))],
             [Paragraph(body, _s("_tb", fontSize=8.5, textColor=MUTED,
                fontName="Helvetica", leading=12))]],
            colWidths=[col_w],
        )
        tc.setStyle(TableStyle([
            ("BACKGROUND",    (0,0), (-1,-1), NAVY2),
            ("BOX",           (0,0), (-1,-1), 0.5, c),
            ("LINEABOVE",     (0,0), (-1,0),  2, c),
            ("TOPPADDING",    (0,0), (-1,-1), 7),
            ("BOTTOMPADDING", (0,0), (-1,-1), 7),
            ("LEFTPADDING",   (0,0), (-1,-1), 9),
            ("RIGHTPADDING",  (0,0), (-1,-1), 9),
            ("VALIGN",        (0,0), (-1,-1), "TOP"),
        ]))
        left.append(tc)
        left.append(sp(2))

    right = [
        Paragraph("Why this makes sense", _s("_hw", fontSize=10, textColor=GOLD,
                fontName="Helvetica-Bold", leading=13, spaceAfter=5)),
        b("₹50 Lakhs = 3.2% of your current ₹15.79 Cr analytics budget"),
        b("Offshore vendors currently take 52.8% of that budget — this replaces a fraction of that spend with a domestic, franchise-specific tool"),
        b("We sell the modelling layer and product surface — not Cricsheet data, which you already have"),
        b("The platform is live today at ipl-auction-dashboard-1.onrender.com — no waiting for a build"),
        sp(3),
        Paragraph("Pilot option", _s("_hw", fontSize=10, textColor=GOLD,
                fontName="Helvetica-Bold", leading=13, spaceAfter=4)),
        Paragraph(
            "Start with the Auction War Room module only — one season pilot "
            "at ₹25 Lakhs. If the 2027 auction prep delivers, expand to the full platform.",
            S["body"]),
    ]

    e.append(two_col(left, right, col_w, col_w))
    e.append(sp(3))
    e.append(slide_footer(9))
    return e

# ── SLIDE 10: NEXT STEPS ──────────────────────────────────────────────────────
def slide_next():
    e = []
    e.append(pink_bar())
    e.append(sp(8))
    e.append(section_tag("NEXT STEPS"))
    e.append(sp(4))
    e.append(Paragraph("Three steps to get started.", S["h_lg_c"]))
    e.append(sp(6))

    steps = [
        ("01", "Live Demo", "30 minutes",
         "Open the platform live during an RR match. "
         "Walk through AI match brief, Salary Value Lab, and Auction War Room "
         "with your analytics team.",
         PINK),
        ("02", "Pilot Agreement", "1 week",
         "Sign a one-season pilot on the Auction War Room module. "
         "We calibrate the model to RR's specific squad priorities "
         "and auction strategy ahead of the next auction.",
         GOLD),
        ("03", "Full Platform", "2027 season",
         "Expand to the full 9-module suite. Add proprietary RR data feeds "
         "(GPS, wearables, internal scouting) on top of the Cricsheet backbone.",
         BLUE_LT),
    ]

    step_w = (CW - 6 * mm) / 3
    cells = []
    for num, title, time, body, c in steps:
        cell = Table(
            [[Paragraph(num,   _s("_sn", fontSize=32, textColor=c, fontName="Helvetica-Bold",
                                  alignment=TA_CENTER, leading=36))],
             [Paragraph(title, _s("_st", fontSize=13, textColor=WHITE, fontName="Helvetica-Bold",
                                  alignment=TA_CENTER, leading=16, spaceAfter=2))],
             [Paragraph(time,  _s("_sm", fontSize=7.5, textColor=c, fontName="Helvetica-Bold",
                                  alignment=TA_CENTER, leading=11, letterSpacing=1, spaceAfter=4))],
             [Paragraph(body,  _s("_sb", fontSize=8.5, textColor=MUTED, fontName="Helvetica",
                                  alignment=TA_CENTER, leading=13))]],
            colWidths=[step_w],
        )
        cell.setStyle(TableStyle([
            ("BACKGROUND",    (0,0), (-1,-1), NAVY2),
            ("BOX",           (0,0), (-1,-1), 1, c),
            ("LINEABOVE",     (0,0), (-1,0),  3, c),
            ("TOPPADDING",    (0,0), (-1,-1), 12),
            ("BOTTOMPADDING", (0,0), (-1,-1), 12),
            ("LEFTPADDING",   (0,0), (-1,-1), 10),
            ("RIGHTPADDING",  (0,0), (-1,-1), 10),
            ("VALIGN",        (0,0), (-1,-1), "TOP"),
        ]))
        cells.append(cell)

    row_t = Table([cells], colWidths=[step_w] * 3)
    row_t.setStyle(TableStyle([
        ("TOPPADDING",    (0,0), (-1,-1), 0),
        ("BOTTOMPADDING", (0,0), (-1,-1), 0),
        ("LEFTPADDING",   (0,0), (-1,-1), 0),
        ("RIGHTPADDING",  (0,0), (1,-1),  3 * mm),
        ("RIGHTPADDING",  (2,0), (2,-1),  0),
    ]))
    e.append(row_t)
    e.append(sp(5))

    contact = Table(
        [[Paragraph(
            "Piyush Zaware  ·  piyushzaware@uchicago.edu  ·  "
            "ipl-auction-dashboard-1.onrender.com  ·  Access code: royals2026",
            _s("_ct", fontSize=9, textColor=MUTED, fontName="Helvetica",
               alignment=TA_CENTER, leading=13))]],
        colWidths=[CW],
    )
    contact.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), NAVY2),
        ("BOX",           (0,0), (-1,-1), 0.5, GREY_LINE),
        ("TOPPADDING",    (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING",   (0,0), (-1,-1), 0),
        ("RIGHTPADDING",  (0,0), (-1,-1), 0),
    ]))
    e.append(contact)
    e.append(sp(3))
    e.append(slide_footer(10))
    return e

# ── BUILD ─────────────────────────────────────────────────────────────────────
def build():
    doc = SimpleDocTemplate(
        OUT,
        pagesize=landscape(A4),
        leftMargin=M, rightMargin=M,
        topMargin=M,  bottomMargin=M,
        title="RR Decision Intelligence Platform — Pitch Deck",
        author="Piyush Zaware",
        subject="Rajasthan Royals Analytics — Client Pitch",
    )

    def dark_background(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(NAVY)
        canvas.rect(0, 0, PW, PH, fill=1, stroke=0)
        canvas.restoreState()

    story = []
    slides = [
        slide_cover(),
        slide_opportunity(),
        slide_problem(),
        slide_platform(),
        slide_ai_brief(),
        slide_salary(),
        slide_auction(),
        slide_data(),
        slide_commercial(),
        slide_next(),
    ]
    for i, slide in enumerate(slides):
        story.extend(slide)
        if i < len(slides) - 1:
            story.append(PageBreak())

    doc.build(story, onFirstPage=dark_background, onLaterPages=dark_background)
    print(f"PDF written → {OUT}")

if __name__ == "__main__":
    build()
