"""
Generate: CreaseIQ — Internal Team Reference v2.0
Audience: internal dev / analyst team
Date: March 2026
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER
import os
from datetime import date

OUT = os.path.join(os.path.dirname(__file__), "Internal_Team_Reference.pdf")

# ── Colours ───────────────────────────────────────────────────────────────────
NAVY      = colors.HexColor("#06081A")
BLUE      = colors.HexColor("#14336B")
PINK      = colors.HexColor("#E8175D")
GOLD      = colors.HexColor("#F7C948")
WHITE     = colors.white
DARK_TEXT = colors.HexColor("#1E293B")
MUTED     = colors.HexColor("#7B8DB8")
GREY_LINE = colors.HexColor("#D1D5DB")
GREEN     = colors.HexColor("#059669")
RED       = colors.HexColor("#DC2626")
AMBER     = colors.HexColor("#D97706")
BG_ALT    = colors.HexColor("#F8F9FF")
BG_BLUE   = colors.HexColor("#F0F4FF")
BG_GREEN  = colors.HexColor("#F0FDF4")
BG_AMBER  = colors.HexColor("#FFFBEB")
BG_PINK   = colors.HexColor("#FFF1F5")
BG_DARK   = colors.HexColor("#F1F5F9")

W, H = A4
M = 18 * mm

def _s(name, **kw):
    return ParagraphStyle(name, **kw)

S = {
    "label": _s("label", fontSize=7, textColor=MUTED, fontName="Helvetica",
        alignment=TA_CENTER, leading=10, letterSpacing=2, spaceAfter=2),
    "h1": _s("h1", fontSize=13, textColor=PINK, fontName="Helvetica-Bold",
        spaceBefore=12, spaceAfter=5, leading=17),
    "h2": _s("h2", fontSize=10, textColor=BLUE, fontName="Helvetica-Bold",
        spaceBefore=7, spaceAfter=3, leading=14),
    "h3": _s("h3", fontSize=9, textColor=DARK_TEXT, fontName="Helvetica-Bold",
        spaceBefore=5, spaceAfter=2, leading=13),
    "body": _s("body", fontSize=9, textColor=DARK_TEXT, fontName="Helvetica",
        spaceAfter=4, leading=14),
    "code": _s("code", fontSize=8, textColor=colors.HexColor("#1E3A5F"),
        fontName="Courier", spaceAfter=3, leading=12,
        backColor=BG_BLUE, leftIndent=8, rightIndent=8),
    "muted": _s("muted", fontSize=8, textColor=MUTED, fontName="Helvetica",
        spaceAfter=3, leading=12),
    "bullet": _s("bullet", fontSize=9, textColor=DARK_TEXT, fontName="Helvetica",
        leftIndent=10, spaceAfter=3, leading=13),
    "warn": _s("warn", fontSize=8.5, textColor=AMBER, fontName="Helvetica-Bold",
        spaceAfter=3, leading=13),
    "footer": _s("footer", fontSize=7, textColor=MUTED, fontName="Helvetica",
        alignment=TA_CENTER, leading=10),
}

def rule(c=PINK, t=1.5):
    return HRFlowable(width="100%", thickness=t, color=c, spaceAfter=5, spaceBefore=2)

def grey_rule():
    return HRFlowable(width="100%", thickness=0.4, color=GREY_LINE, spaceAfter=4, spaceBefore=4)

def sp(h=3):
    return Spacer(1, h * mm)

def b(text):
    return Paragraph(f"• &nbsp; {text}", S["bullet"])

def code(text):
    return Paragraph(text, S["code"])

def callout(text, bg=BG_BLUE, border=BLUE):
    t = Table([[Paragraph(text, S["body"])]], colWidths=[W - 2*M])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), bg),
        ("BOX",           (0,0), (-1,-1), 0.8, border),
        ("TOPPADDING",    (0,0), (-1,-1), 7),
        ("BOTTOMPADDING", (0,0), (-1,-1), 7),
        ("LEFTPADDING",   (0,0), (-1,-1), 10),
        ("RIGHTPADDING",  (0,0), (-1,-1), 10),
    ]))
    return t

def tbl(rows, cw, hbg=BLUE):
    t = Table(rows, colWidths=cw)
    st = TableStyle([
        ("BACKGROUND",    (0,0), (-1,0),  hbg),
        ("TEXTCOLOR",     (0,0), (-1,0),  WHITE),
        ("FONTNAME",      (0,0), (-1,0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0,0), (-1,-1), 8),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 7),
        ("RIGHTPADDING",  (0,0), (-1,-1), 7),
        ("GRID",          (0,0), (-1,-1), 0.35, GREY_LINE),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [WHITE, BG_ALT]),
        ("FONTNAME",      (0,1), (-1,-1), "Helvetica"),
    ])
    t.setStyle(st)
    return t

# ── COVER ──────────────────────────────────────────────────────────────────────
def cover():
    e = []
    e.append(sp(8))
    e.append(Paragraph("INTERNAL TEAM REFERENCE — NOT FOR EXTERNAL DISTRIBUTION", S["label"]))
    e.append(sp(3))

    hero = Table(
        [[Paragraph("CreaseIQ · RR Decision Intelligence Platform", _s("h", fontSize=24,
            textColor=PINK, fontName="Helvetica-Bold", alignment=TA_CENTER, leading=28))],
         [Paragraph("Internal Build Reference  ·  v2.0  ·  March 2026",
            _s("sh", fontSize=11, textColor=colors.HexColor("#EEF2FF"),
            fontName="Helvetica", alignment=TA_CENTER, leading=15))]],
        colWidths=[W - 2*M],
    )
    hero.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), NAVY),
        ("TOPPADDING",    (0,0), (0,0),   16),
        ("BOTTOMPADDING", (0,0), (0,0),   4),
        ("TOPPADDING",    (0,1), (0,1),   4),
        ("BOTTOMPADDING", (0,1), (0,1),   16),
        ("LEFTPADDING",   (0,0), (-1,-1), 14),
        ("RIGHTPADDING",  (0,0), (-1,-1), 14),
    ]))
    e.append(hero)
    e.append(sp(4))
    e.append(rule())
    e.append(sp(3))

    meta = [
        ["Company",       "CreaseIQ"],
        ["Founder",       "Piyush Zaware  ·  zpiyushrd19@gmail.com"],
        ["Repo",          "github.com/pzaware19/ipl-auction-dashboard"],
        ["Public URL",    "https://ipl-auction-dashboard-1.onrender.com (marketing landing page)"],
        ["RR Demo URL",   "https://ipl-auction-dashboard-1.onrender.com/rr_login.html"],
        ["Demo password", "royals2026  (env var: RR_ACCESS_CODE)"],
        ["Deployment",    "Render.com — free tier — auto-deploy on push to main"],
        ["Uptime",        "UptimeRobot free — pings every 5 min to prevent cold start"],
        ["Data",          "IPL 2017–2025 · Cricsheet ball-by-ball CSVs · 350,000+ deliveries"],
        ["AI engine",     "Groq  ·  Llama 3.3 70B  (free tier: 14,400 req/day)"],
        ["Last updated",  date.today().strftime("%B %d, %Y")],
    ]
    mt = Table(meta, colWidths=[38*mm, W - 2*M - 38*mm])
    mt.setStyle(TableStyle([
        ("FONTNAME",      (0,0), (0,-1), "Helvetica-Bold"),
        ("FONTNAME",      (1,0), (1,-1), "Helvetica"),
        ("FONTSIZE",      (0,0), (-1,-1), 9),
        ("TEXTCOLOR",     (0,0), (0,-1), BLUE),
        ("TEXTCOLOR",     (1,0), (1,-1), DARK_TEXT),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LINEBELOW",     (0,0), (-1,-2), 0.3, GREY_LINE),
    ]))
    e.append(mt)
    e.append(sp(6))

    toc_items = [
        ("1",  "Product Structure — Two Products"),
        ("2",  "Architecture & File Map"),
        ("3",  "Authentication Architecture"),
        ("4",  "Environment Variables & API Keys"),
        ("5",  "Running Locally"),
        ("6",  "Data Pipeline"),
        ("7",  "Feature Inventory — All Modules"),
        ("8",  "API Integrations — Groq & CricAPI"),
        ("9",  "CricAPI Budget Model"),
        ("10", "Demo Request Flow"),
        ("11", "Deployment — Render"),
        ("12", "Uptime Monitoring — UptimeRobot"),
        ("13", "Known Limitations & Open Issues"),
        ("14", "Roadmap"),
    ]
    toc_rows = [["§", "Section"]] + toc_items
    e.append(tbl(toc_rows, [12*mm, W - 2*M - 12*mm], hbg=BLUE))
    e.append(sp(4))
    return e

# ── SECTION 1: Product Structure ───────────────────────────────────────────────
def s1_products():
    e = []
    e.append(Paragraph("1. Product Structure — Two Products", S["h1"]))
    e.append(rule())
    e.append(Paragraph(
        "CreaseIQ currently ships two distinct products from the same codebase and the same Render deployment.",
        S["body"]))
    e.append(sp(2))

    rows = [
        ["Product", "Entry point", "Audience", "Auth", "Status"],
        ["CreaseIQ Platform",
         "ipl-auction-dashboard-1.onrender.com",
         "Public — marketing landing page. No analytics data exposed.",
         "None (public)",
         "✓ Live"],
        ["CreaseIQ for RR",
         ".../rr_login.html → rr_hub.html",
         "Rajasthan Royals analytics/performance team (demo). Other franchises via separate access codes.",
         "Server-side cookie (HttpOnly)",
         "✓ Live"],
    ]
    t = Table(rows, colWidths=[30*mm, 42*mm, 54*mm, 28*mm, 16*mm])
    st = TableStyle([
        ("BACKGROUND",    (0,0), (-1,0),  BLUE),
        ("TEXTCOLOR",     (0,0), (-1,0),  WHITE),
        ("FONTNAME",      (0,0), (-1,0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0,0), (-1,-1), 7.5),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 6),
        ("RIGHTPADDING",  (0,0), (-1,-1), 6),
        ("GRID",          (0,0), (-1,-1), 0.35, GREY_LINE),
        ("VALIGN",        (0,0), (-1,-1), "TOP"),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [WHITE, BG_ALT]),
        ("FONTNAME",      (0,1), (-1,-1), "Helvetica"),
        ("TEXTCOLOR",     (4,1), (4,-1),  GREEN),
        ("FONTNAME",      (4,1), (4,-1),  "Helvetica-Bold"),
    ])
    t.setStyle(st)
    e.append(t)
    e.append(sp(3))

    e.append(Paragraph("Access control model", S["h2"]))
    access = [
        ["URL path", "Public?", "What is served"],
        ["/  or  /index.html",   "Yes", "Marketing landing page — no dashboard_data.js, no analytics"],
        ["/rr_login.html",       "Yes", "Login form — POSTs to /api/auth to get cookie"],
        ["/favicon.ico",         "Yes", "Favicon"],
        ["/api/demo-request",    "Yes (POST only)", "Collects name/email/franchise; logs to Render; emails founder"],
        ["/api/auth",            "Yes (POST only)", "Validates access code; sets HttpOnly session cookie"],
        ["All other .html pages","No — cookie required", "Redirected to /rr_login.html if no valid cookie"],
        ["/data/dashboard_data.js","No — cookie required", "All metrics, all methodology — fully gated"],
        ["/api/run-scenario",    "No — cookie required", "Auction simulation backend"],
        ["/api/match-brief",     "No — cookie required", "Groq AI match brief"],
        ["/api/live-score",      "No — cookie required", "CricAPI live score proxy"],
    ]
    t2 = Table(access, colWidths=[44*mm, 28*mm, W - 2*M - 72*mm])
    st2 = TableStyle([
        ("BACKGROUND",    (0,0), (-1,0),  BLUE),
        ("TEXTCOLOR",     (0,0), (-1,0),  WHITE),
        ("FONTNAME",      (0,0), (-1,0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0,0), (-1,-1), 7.5),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 7),
        ("RIGHTPADDING",  (0,0), (-1,-1), 7),
        ("GRID",          (0,0), (-1,-1), 0.35, GREY_LINE),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [WHITE, BG_ALT]),
        ("FONTNAME",      (0,1), (-1,-1), "Helvetica"),
    ])
    for i, row in enumerate(access[1:], 1):
        if row[1] == "Yes":
            st2.add("TEXTCOLOR", (1,i), (1,i), GREEN)
            st2.add("FONTNAME",  (1,i), (1,i), "Helvetica-Bold")
        elif row[1].startswith("No"):
            st2.add("TEXTCOLOR", (1,i), (1,i), RED)
            st2.add("FONTNAME",  (1,i), (1,i), "Helvetica-Bold")
        else:
            st2.add("TEXTCOLOR", (1,i), (1,i), AMBER)
            st2.add("FONTNAME",  (1,i), (1,i), "Helvetica-Bold")
    t2.setStyle(st2)
    e.append(t2)
    e.append(sp(4))
    return e

# ── SECTION 2: Architecture ─────────────────────────────────────────────────────
def s2_architecture():
    e = []
    e.append(Paragraph("2. Architecture & File Map", S["h1"]))
    e.append(rule())
    e.append(Paragraph(
        "The platform is <b>payload-first, framework-light</b>. A Python data pipeline "
        "pre-computes all metrics and writes a single JS file. The front end reads that "
        "file — no React, no build step, no bundler.",
        S["body"]))
    e.append(sp(2))

    e.append(Paragraph("Data flow", S["h2"]))
    flow = [
        ["Step", "What happens", "File"],
        ["1 — Build",  "Python reads Cricsheet CSVs + salary CSV → computes all metrics → writes payload", "Dashboard/build_dashboard_data.py"],
        ["2 — Serve",  "server.py authenticates requests via cookie, serves static files + API endpoints", "Dashboard/server.py"],
        ["3 — Load",   "Browser loads dashboard_data.js as window.DASHBOARD_DATA (only after auth)", "Dashboard/data/dashboard_data.js"],
        ["4 — Render", "Each HTML module reads the payload and renders its UI in vanilla JS", "Dashboard/*.html + *.js"],
    ]
    e.append(tbl(flow, [18*mm, 80*mm, 58*mm]))
    e.append(sp(3))

    e.append(Paragraph("Key files", S["h2"]))
    files = [
        ["File / Folder", "Purpose"],
        ["Dashboard/index.html",              "PUBLIC marketing landing page — no data loaded, two CTAs"],
        ["Dashboard/rr_login.html",           "Login gate — POSTs access code to /api/auth, sets cookie"],
        ["Dashboard/rr_hub.html",             "RR franchise hub: next-match card, live score banner, AI brief"],
        ["Dashboard/build_dashboard_data.py", "Central build script — most important file for new data features"],
        ["Dashboard/server.py",               "Server: cookie auth, scenario API, Groq brief, CricAPI proxy, demo requests"],
        ["Dashboard/match_planning.html/js",  "Opponent + venue aware SWOT; ?team=RR auto-selects RR lens"],
        ["Dashboard/salary_value_lab.html/js","Fair salary vs 2026 contract; SVI metric"],
        ["Dashboard/batter_diagnostics.html/js","Phase/pressure/venue/bowling-family splits per batter"],
        ["Dashboard/auction_war_room.html",   "Monte Carlo auction results; calls /api/run-scenario"],
        ["Dashboard/scenario_builder.html",   "User-adjustable auction counterfactual"],
        ["Dashboard/data/dashboard_data.js",  "Generated payload — do NOT edit manually; rebuild from Python"],
        ["Data/ipl_salaries_2026.csv",        "2026 salary sheet (normalised from PDF) — source of truth"],
        ["Code/rr_auction_simulator.py",      "Auction simulation logic; canonical player name normalisation"],
        ["docs/generate_rr_demo_doc.py",      "Generates RR_Demo_Platform_Documentation.pdf (client-facing)"],
        ["docs/generate_internal_doc.py",     "Generates this document"],
        ["docs/generate_pitch_deck.py",       "Generates RR_Pitch_Deck.pdf (investor/franchise pitch)"],
        ["render.yaml",                       "Render deployment config — build + start + envVars"],
        ["requirements.txt",                  "pandas>=2.2, openpyxl>=3.1 — minimal Python deps"],
    ]
    e.append(tbl(files, [68*mm, W - 2*M - 68*mm]))
    e.append(sp(4))
    return e

# ── SECTION 3: Auth Architecture ───────────────────────────────────────────────
def s3_auth():
    e = []
    e.append(Paragraph("3. Authentication Architecture", S["h1"]))
    e.append(rule())
    e.append(Paragraph(
        "Auth is entirely server-side. No access code or secret is ever sent to the browser. "
        "The sessionStorage approach used previously was client-side only and could be bypassed "
        "by direct URL access — it has been replaced.",
        S["body"]))
    e.append(sp(2))

    e.append(Paragraph("Login flow", S["h2"]))
    flow = [
        ["Step", "Action", "Detail"],
        ["1", "User opens /rr_login.html",           "Served without auth (public path)"],
        ["2", "User types access code, submits form", "JS fetch POST to /api/auth with {code: '...'}"],
        ["3", "Server validates code",                "Compares against RR_ACCESS_CODE env var (default: royals2026)"],
        ["4", "Server sets cookie on success",        "Set-Cookie: rr_auth=creaseiq_ok; Path=/; SameSite=Strict; HttpOnly"],
        ["5", "Browser redirects to /rr_hub.html",    "All subsequent requests carry the cookie automatically"],
        ["6", "Server checks cookie on every request","Unauthenticated requests → 302 redirect to /rr_login.html"],
    ]
    e.append(tbl(flow, [8*mm, 52*mm, W - 2*M - 60*mm]))
    e.append(sp(2))

    e.append(Paragraph("Cookie properties", S["h2"]))
    props = [
        ["Property", "Value", "Why"],
        ["Name",       "rr_auth",      "Cookie identifier"],
        ["Value",      "creaseiq_ok",  "Hardcoded expected value — compared in _is_authenticated()"],
        ["Path",       "/",            "Sent with all requests to the domain"],
        ["HttpOnly",   "Yes",          "JavaScript cannot read this cookie — prevents XSS theft"],
        ["SameSite",   "Strict",       "Cookie only sent on same-origin requests — prevents CSRF"],
        ["Secure",     "Not set",      "Render runs behind HTTPS reverse proxy — add Secure for extra hardening"],
        ["Expiry",     "Session",      "Cookie deleted when browser closes — forces re-login per session"],
    ]
    e.append(tbl(props, [22*mm, 28*mm, W - 2*M - 50*mm]))
    e.append(sp(2))

    e.append(callout(
        "<b>To change the access code:</b> Set RR_ACCESS_CODE env var on Render to the new value. "
        "No code change or redeploy needed — the server reads it at runtime. "
        "Each new franchise gets its own RR_ACCESS_CODE — deploy a separate Render service per franchise.",
        bg=BG_BLUE, border=BLUE))
    e.append(sp(4))
    return e

# ── SECTION 4: Environment Variables ───────────────────────────────────────────
def s4_env():
    e = []
    e.append(Paragraph("4. Environment Variables & API Keys", S["h1"]))
    e.append(rule())
    e.append(callout(
        "⚠  Never commit API keys to git. All secrets are passed as environment variables. "
        "Set them in Render → Service → Environment for production.",
        bg=BG_AMBER, border=AMBER))
    e.append(sp(2))

    rows = [
        ["Variable", "Required", "Default", "Notes"],
        ["GROQ_API_KEY",      "Yes (AI brief)",     "—",          "gsk_... format · Groq free tier: 14,400 req/day"],
        ["GROQ_MODEL",        "No",                 "llama-3.3-70b-versatile", "Override Groq model if needed"],
        ["CRICAPI_KEY",       "Yes (live score)",   "—",          "UUID format · d83c9a71-... · lifetime key"],
        ["RR_ACCESS_CODE",    "No",                 "royals2026", "Demo password — change per franchise"],
        ["GMAIL_USER",        "No (email notifs)",  "—",          "zpiyushrd19@gmail.com — sender for demo request emails"],
        ["GMAIL_APP_PASSWORD","No (email notifs)",  "—",          "16-char Gmail App Password — not your Gmail password"],
        ["LEAGUE_MC_ITERATIONS","No",               "varies",     "Set to 50 in render.yaml envVars for faster builds"],
        ["PORT",              "No",                 "8000",       "Set automatically by Render — do not override"],
        ["HOST",              "No",                 "0.0.0.0",    "Default binds to all interfaces"],
        ["RENDER",            "Auto",               "true on Render","Set by Render — used to skip runtime data rebuild"],
    ]
    e.append(tbl(rows, [40*mm, 22*mm, 30*mm, W - 2*M - 92*mm]))
    e.append(sp(3))

    e.append(Paragraph("Local dev pattern (never commit these)", S["h2"]))
    e.append(code("export GROQ_API_KEY='gsk_...'"))
    e.append(code("export CRICAPI_KEY='d83c9a71-b339-47ab-a536-84bf991b2746'"))
    e.append(code("export RR_ACCESS_CODE='royals2026'"))
    e.append(code("python Dashboard/server.py"))
    e.append(sp(4))
    return e

# ── SECTION 5: Running Locally ──────────────────────────────────────────────────
def s5_local():
    e = []
    e.append(Paragraph("5. Running Locally", S["h1"]))
    e.append(rule())

    e.append(Paragraph("One-time setup", S["h2"]))
    e.append(code("pip install -r requirements.txt"))
    e.append(sp(2))

    e.append(Paragraph("Rebuild the data payload", S["h2"]))
    e.append(Paragraph(
        "Run this whenever you change build_dashboard_data.py or the source CSVs. "
        "dashboard_data.js is in .gitignore — Render builds it from source on every deploy.",
        S["body"]))
    e.append(code("python Dashboard/build_dashboard_data.py"))
    e.append(sp(2))

    e.append(Paragraph("Start the server", S["h2"]))
    e.append(code("GROQ_API_KEY='...' CRICAPI_KEY='...' python Dashboard/server.py"))
    e.append(Paragraph(
        "Then open: http://localhost:8000  (marketing page) or "
        "http://localhost:8000/rr_login.html  (enter: royals2026)",
        S["muted"]))
    e.append(sp(2))

    e.append(Paragraph("JS syntax checks", S["h2"]))
    e.append(code("node --check Dashboard/app.js"))
    e.append(code("node --check Dashboard/match_planning.js"))
    e.append(code("node --check Dashboard/batter_diagnostics.js"))
    e.append(code("node --check Dashboard/salary_value_lab.js"))
    e.append(sp(2))

    e.append(Paragraph("Regenerate PDFs", S["h2"]))
    e.append(code("python docs/generate_rr_demo_doc.py"))
    e.append(code("python docs/generate_internal_doc.py"))
    e.append(code("python docs/generate_pitch_deck.py"))
    e.append(sp(4))
    return e

# ── SECTION 6: Data Pipeline ────────────────────────────────────────────────────
def s6_pipeline():
    e = []
    e.append(Paragraph("6. Data Pipeline", S["h1"]))
    e.append(rule())
    e.append(Paragraph(
        "build_dashboard_data.py is the single source of truth for all dashboard metrics. "
        "All features are implemented by enriching this payload rather than adding ad hoc "
        "client logic — maintain this pattern for all new features.",
        S["body"]))
    e.append(sp(2))

    e.append(Paragraph("Payload sections (window.DASHBOARD_DATA keys)", S["h2"]))
    sections = [
        ["Key", "Contents", "Primary consumer"],
        ["phase_studio",        "Phase-impact leaderboards (PP/mid/death) — batters + bowlers", "index.html / app.js"],
        ["player_lab",          "Radar, wins-added proxy, comps, trajectory per player", "index.html / app.js"],
        ["matchup_intelligence","Ball-by-ball H2H batter vs bowler matchup evidence", "matchup_intelligence.html"],
        ["auction_war_room",    "Monte Carlo auction paths, role budgets, target lists", "auction_war_room.html"],
        ["market_inefficiency", "Underpriced archetypes, role surplus/scarcity analysis", "market_inefficiency.html"],
        ["similarity_search",   "Phase-fingerprint similarity matrix for player comps", "similarity_search.html"],
        ["match_planning",      "All RR 2026 fixtures + venue profiles + SWOT + AI brief context", "match_planning.html, rr_hub.html"],
        ["batter_diagnostics",  "Phase/pressure/venue/bowling-family/named-bowler splits", "batter_diagnostics.html"],
        ["salary_value",        "Fair salary, SVI, value gap for all active IPL players", "salary_value_lab.html"],
    ]
    e.append(tbl(sections, [38*mm, 82*mm, 36*mm]))
    e.append(sp(3))

    e.append(Paragraph("Critical conventions", S["h2"]))
    items = [
        "<b>ACTIVE_CUTOFF_YEAR = 2025</b> — player must have IPL evidence through 2025 to be 'active'.",
        "<b>Name normalisation</b> — canonical names live in Code/rr_auction_simulator.py. Any new feature joining multiple data layers must use the existing alias map.",
        "<b>Salary source</b> — Data/ipl_salaries_2026.csv (normalised from PDF). Do not make the pipeline depend on PDF parsing at runtime.",
        "<b>Bayesian shrinkage</b> — phase impact scores are shrunk toward the league mean to correct for sample-size noise. Do not remove this.",
        "<b>Minimum signal thresholds</b> — salary model requires minimum batting/bowling signal before those sides contribute to valuation. Prevents distortion by tailenders with tiny batting samples.",
    ]
    for i in items:
        e.append(b(i))
    e.append(sp(4))
    return e

# ── SECTION 7: Feature Inventory ────────────────────────────────────────────────
def s7_features():
    e = []
    e.append(Paragraph("7. Feature Inventory — All Modules", S["h1"]))
    e.append(rule())

    rows = [
        ["Module", "Entry point", "Auth needed", "Backend call", "Status"],
        ["Marketing Landing Page", "index.html",              "No (public)",  "None",                  "✓ Live"],
        ["Demo Request Form",      "index.html (modal)",      "No (public)",  "/api/demo-request POST","✓ Live"],
        ["Password Gate",          "rr_login.html",           "No (public)",  "/api/auth POST",        "✓ Live"],
        ["RR Franchise Hub",       "rr_hub.html",             "Yes",          "match-brief + live-score","✓ Live"],
        ["Live Score Banner",      "rr_hub.html (inline)",    "Yes",          "/api/live-score",       "✓ Live"],
        ["AI Match Brief",         "rr_hub.html (inline)",    "Yes",          "/api/match-brief",      "✓ Live"],
        ["Match Planning",         "match_planning.html",     "Yes",          "None (payload)",        "✓ Live"],
        ["Salary Value Lab",       "salary_value_lab.html",   "Yes",          "None (payload)",        "✓ Live"],
        ["Batter Diagnostics",     "batter_diagnostics.html", "Yes",          "None (payload)",        "✓ Live"],
        ["Matchup Intelligence",   "matchup_intelligence.html","Yes",         "None (payload)",        "✓ Live"],
        ["Auction War Room",       "auction_war_room.html",   "Yes",          "/api/run-scenario",     "✓ Live"],
        ["Scenario Builder",       "scenario_builder.html",   "Yes",          "/api/run-scenario",     "✓ Live"],
        ["Phase Studio",           "index.html (old platform)","Yes",         "None (payload)",        "✓ Live"],
        ["Market Inefficiency",    "market_inefficiency.html","Yes",          "None (payload)",        "✓ Live"],
        ["Similarity Search",      "similarity_search.html",  "Yes",          "None (payload)",        "✓ Live"],
        ["Draft Board",            "draft_board.html",        "Yes",          "None (payload)",        "✓ Live"],
    ]
    t = Table(rows, colWidths=[36*mm, 38*mm, 22*mm, 34*mm, 16*mm])
    st = TableStyle([
        ("BACKGROUND",    (0,0), (-1,0),  BLUE),
        ("TEXTCOLOR",     (0,0), (-1,0),  WHITE),
        ("FONTNAME",      (0,0), (-1,0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0,0), (-1,-1), 7),
        ("TOPPADDING",    (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ("LEFTPADDING",   (0,0), (-1,-1), 5),
        ("RIGHTPADDING",  (0,0), (-1,-1), 5),
        ("GRID",          (0,0), (-1,-1), 0.35, GREY_LINE),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [WHITE, BG_ALT]),
        ("FONTNAME",      (0,1), (-1,-1), "Helvetica"),
        ("TEXTCOLOR",     (4,1), (4,-1),  GREEN),
        ("FONTNAME",      (4,1), (4,-1),  "Helvetica-Bold"),
    ])
    t.setStyle(st)
    e.append(t)
    e.append(sp(4))
    return e

# ── SECTION 8: API Integrations ─────────────────────────────────────────────────
def s8_apis():
    e = []
    e.append(Paragraph("8. API Integrations — Groq & CricAPI", S["h1"]))
    e.append(rule())

    e.append(Paragraph("8a — Groq / Llama 3.3 70B (AI Match Brief)", S["h2"]))
    e.append(callout(
        "<b>Migration note:</b> The platform was originally built on Anthropic Claude Sonnet 4.6 "
        "(ANTHROPIC_API_KEY). It was migrated to Groq in March 2026 to eliminate API costs. "
        "Groq's free tier provides 14,400 requests/day — far exceeding match-brief usage.",
        bg=BG_AMBER, border=AMBER))
    e.append(sp(2))
    groq = [
        ["Property", "Value"],
        ["Endpoint",    "https://api.groq.com/openai/v1/chat/completions"],
        ["Format",      "OpenAI-compatible (system + user messages array)"],
        ["Auth header", "Authorization: Bearer $GROQ_API_KEY"],
        ["User-Agent",  "python-requests/2.31.0  (required to pass Cloudflare WAF)"],
        ["Model",       "llama-3.3-70b-versatile (overridable via GROQ_MODEL env var)"],
        ["max_tokens",  "2048 — prevents JSON truncation mid-response"],
        ["temperature", "0.3 — consistent structured output"],
        ["Timeout",     "60 seconds"],
        ["Response",    "choices[0].message.content — stripped of markdown fences before json.loads()"],
        ["Fallback",    "If JSON parse fails: returns dict with headline + raw content in opening_call"],
        ["Output schema","headline, opening_call, why_this_matchup_is_live, tactical_edges, matchup_watch, venue_read, risk_flags, recommended_plan"],
        ["Free tier",   "14,400 req/day · 6,000 tokens/min · More than sufficient for match-brief usage"],
    ]
    e.append(tbl(groq, [40*mm, W - 2*M - 40*mm]))
    e.append(sp(3))

    e.append(Paragraph("8b — CricAPI (Live Score Widget)", S["h2"]))
    cric = [
        ["Property", "Value"],
        ["Endpoint",     "https://api.cricapi.com/v1/currentMatches?apikey={key}&offset=0"],
        ["Auth",         "API key in query string — key is server-side only, never in browser"],
        ["Filter",       "Server filters response for any team name containing 'rajasthan' (case-insensitive)"],
        ["Server cache", "180 seconds (3 min) — all browser tabs share one upstream call"],
        ["Client poll",  "Every 3 minutes — but ONLY within the match window"],
        ["Match window", "30 min before scheduled kickoff → 5 hours after kickoff"],
        ["Outside window","Zero API calls made — full budget preserved on non-match days"],
        ["Key",          "d83c9a71-b339-47ab-a536-84bf991b2746 (lifetime key, UUID format)"],
        ["Free tier cap","100 calls/day"],
        ["Fields used",  "teams[], score[]{r,w,o,inning}, status, matchStarted, matchEnded, venue, name"],
    ]
    e.append(tbl(cric, [38*mm, W - 2*M - 38*mm]))
    e.append(sp(4))
    return e

# ── SECTION 9: CricAPI Budget Model ────────────────────────────────────────────
def s9_budget():
    e = []
    e.append(Paragraph("9. CricAPI Budget Model", S["h1"]))
    e.append(rule())
    e.append(Paragraph(
        "Free tier: 100 calls/day. T20 match: 240 balls, 3.5–4.5 hours. Full budget accounting:",
        S["body"]))
    e.append(sp(2))

    budget = [
        ["Scenario", "Logic", "Calls used"],
        ["Non-match day",        "Client never enters match window → polling never starts", "0"],
        ["Match day (evening)",  "Window: kickoff−30min → kickoff+5h = 5.5h ÷ 3min = 110 max; actual match ~4h = 80 calls", "~80"],
        ["Multiple browser tabs","Server cache: all tabs share one upstream fetch per 3 min", "No extra calls"],
        ["Server restart mid-match","Cache resets → one immediate call, then resumes 3-min cadence", "+1"],
        ["Total per match day",  "Worst case ~90, typical ~80", "≤ 90 / 100 ✓"],
    ]
    t = Table(budget, colWidths=[44*mm, 88*mm, 24*mm])
    st = TableStyle([
        ("BACKGROUND",    (0,0), (-1,0),  BLUE),
        ("TEXTCOLOR",     (0,0), (-1,0),  WHITE),
        ("FONTNAME",      (0,0), (-1,0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0,0), (-1,-1), 8),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 7),
        ("RIGHTPADDING",  (0,0), (-1,-1), 7),
        ("GRID",          (0,0), (-1,-1), 0.35, GREY_LINE),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [WHITE, BG_ALT]),
        ("FONTNAME",      (0,1), (-1,-1), "Helvetica"),
        ("TEXTCOLOR",     (2,1), (2,-1),  GREEN),
        ("BACKGROUND",    (0,-1),(-1,-1), BG_GREEN),
    ])
    t.setStyle(st)
    e.append(t)
    e.append(sp(4))
    return e

# ── SECTION 10: Demo Request Flow ───────────────────────────────────────────────
def s10_demo():
    e = []
    e.append(Paragraph("10. Demo Request Flow", S["h1"]))
    e.append(rule())
    e.append(Paragraph(
        "The landing page (index.html) has a 'Request Franchise Demo' button that opens a modal form. "
        "This replaces the old mailto: links — requests are captured server-side, not via email client.",
        S["body"]))
    e.append(sp(2))

    e.append(Paragraph("Flow", S["h2"]))
    flow = [
        ["Step", "What happens"],
        ["1", "Visitor clicks 'Request Franchise Demo' on the public landing page"],
        ["2", "Modal opens — collects name, email, franchise/org, optional note"],
        ["3", "Form submits via fetch POST to /api/demo-request (no auth required)"],
        ["4", "Server validates name + email are present"],
        ["5", "Server logs the request to stdout: visible in Render dashboard → Logs"],
        ["6", "If GMAIL_USER + GMAIL_APP_PASSWORD are set: email sent to zpiyushrd19@gmail.com"],
        ["7", "Modal shows success state: 'Request received — demo access within 24 hours'"],
        ["8", "Founder reviews request → manually sends access code to approved contacts"],
    ]
    e.append(tbl(flow, [10*mm, W - 2*M - 10*mm]))
    e.append(sp(2))

    e.append(callout(
        "<b>Checking demo requests without email:</b> Render → your service → Logs tab. "
        "Search for '[DEMO REQUEST]'. Every submission is printed there regardless of email config.",
        bg=BG_BLUE, border=BLUE))
    e.append(sp(2))

    e.append(Paragraph("Gmail App Password setup (for email notifications)", S["h2"]))
    steps = [
        "Go to myaccount.google.com → Security",
        "Enable 2-Step Verification if not already on",
        "Go to myaccount.google.com/apppasswords",
        "Create an app password named 'CreaseIQ' → copy the 16-char code",
        "Set GMAIL_USER = zpiyushrd19@gmail.com and GMAIL_APP_PASSWORD = 16-char code on Render",
    ]
    for s in steps:
        e.append(b(s))
    e.append(sp(4))
    return e

# ── SECTION 11: Deployment ──────────────────────────────────────────────────────
def s11_deploy():
    e = []
    e.append(Paragraph("11. Deployment — Render", S["h1"]))
    e.append(rule())

    e.append(Paragraph("render.yaml (current)", S["h2"]))
    e.append(code("services:"))
    e.append(code("  - type: web"))
    e.append(code("    name: ipl-auction-dashboard"))
    e.append(code("    env: python"))
    e.append(code("    plan: free"))
    e.append(code("    buildCommand: pip install -r requirements.txt && python Dashboard/build_dashboard_data.py"))
    e.append(code("    startCommand: python Dashboard/server.py"))
    e.append(code("    autoDeploy: true"))
    e.append(code("    envVars:"))
    e.append(code("      - key: LEAGUE_MC_ITERATIONS"))
    e.append(code("        value: '50'"))
    e.append(sp(2))

    e.append(Paragraph("Build notes", S["h2"]))
    items = [
        "Every push to <b>main</b> triggers an automatic redeploy.",
        "Build step runs build_dashboard_data.py with LEAGUE_MC_ITERATIONS=50 (reduced from 100 to prevent free-tier build timeout).",
        "LEAGUE_MC_ITERATIONS is in envVars (not inline in buildCommand) — inline KEY=val syntax was silently ignored by Render's shell.",
        "dashboard_data.js is in .gitignore — built fresh on each deploy. If the build step fails, startup skips runtime rebuild and logs a warning (prevents health-check timeout).",
        "Python deps: only pandas + openpyxl — build is fast (~25s locally with 50 iterations).",
    ]
    for i in items:
        e.append(b(i))
    e.append(sp(2))

    e.append(Paragraph("Render environment variables to set manually", S["h2"]))
    env_rows = [
        ["Variable", "Value"],
        ["GROQ_API_KEY",       "gsk_... (your Groq key)"],
        ["CRICAPI_KEY",        "d83c9a71-b339-47ab-a536-84bf991b2746"],
        ["RR_ACCESS_CODE",     "royals2026 (or new code)"],
        ["GMAIL_USER",         "zpiyushrd19@gmail.com (optional — for demo request emails)"],
        ["GMAIL_APP_PASSWORD", "16-char app password (optional)"],
    ]
    e.append(tbl(env_rows, [48*mm, W - 2*M - 48*mm]))
    e.append(sp(2))

    e.append(Paragraph("Deployment checklist", S["h2"]))
    checklist = [
        "Push to main → watch Render logs for build success.",
        "Open / → verify marketing landing page loads (no data).",
        "Open /rr_login.html → enter 'royals2026' → verify RR hub loads.",
        "Click 'Generate AI Match Brief' → confirm JSON brief renders correctly.",
        "On a match day, open hub at kickoff−30min → verify live score banner appears.",
    ]
    for c in checklist:
        e.append(b(c))
    e.append(sp(4))
    return e

# ── SECTION 12: Uptime Monitoring ───────────────────────────────────────────────
def s12_uptime():
    e = []
    e.append(Paragraph("12. Uptime Monitoring — UptimeRobot", S["h1"]))
    e.append(rule())
    e.append(callout(
        "<b>Render free tier cold start:</b> The service spins down after 15 minutes of inactivity. "
        "The next visitor sees a Render loading screen for 30–90 seconds while the server wakes up. "
        "This is unacceptable for demos. UptimeRobot prevents it by pinging the server every 5 minutes.",
        bg=BG_AMBER, border=AMBER))
    e.append(sp(2))

    e.append(Paragraph("UptimeRobot setup", S["h2"]))
    steps = [
        "Go to uptimerobot.com → sign up for free account",
        "Add monitor → type: HTTP(S)",
        "URL: https://ipl-auction-dashboard-1.onrender.com",
        "Monitoring interval: 5 minutes",
        "Save → UptimeRobot will ping every 5 minutes, keeping Render awake",
    ]
    for s in steps:
        e.append(b(s))
    e.append(sp(2))

    props = [
        ["Property", "Detail"],
        ["Cost",           "Free — UptimeRobot free tier supports 50 monitors at 5-min intervals"],
        ["Effect",         "Server never goes idle → no cold start → demo loads instantly"],
        ["Render free tier","Allows external pings — this is within free tier rules"],
        ["Alternative",    "Upgrade Render to Starter ($7/month) for always-on compute"],
        ["Alert emails",   "UptimeRobot also emails you if the service goes down — useful for production monitoring"],
    ]
    e.append(tbl(props, [32*mm, W - 2*M - 32*mm]))
    e.append(sp(4))
    return e

# ── SECTION 13: Known Limitations ───────────────────────────────────────────────
def s13_limits():
    e = []
    e.append(Paragraph("13. Known Limitations & Open Issues", S["h1"]))
    e.append(rule())

    rows = [
        ["Item", "Detail", "Severity"],
        ["Cricsheet data ceiling",
         "Supports outcomes, wickets, phase, venue, pressure, named matchups. "
         "Does NOT support ball line/length/swing/wagon-wheel. Batter diagnostics is explicit about this.",
         "By design"],
        ["Active player cutoff = 2025",
         "Any player with no IPL record in 2025 is treated as inactive. "
         "Affects active views, match planning core, salary lab coverage.",
         "Known"],
        ["Salary model is heuristic",
         "SVI and fair salary are model-implied estimates based on IPL performance. "
         "Not a formal labour-market econometric model.",
         "Documented"],
        ["CricAPI free tier = 100 calls/day",
         "Current design uses ~90 on match days. If multiple users access the hub on match days "
         "the server cache means no extra calls — but review if usage grows.",
         "Managed"],
        ["Live score team-name matching",
         "Banner only appears if 'rajasthan' appears in CricAPI team name string. "
         "CricAPI team name format can vary across competitions — test on first live match.",
         "Minor"],
        ["Groq context window",
         "Llama 3.3 70B has an 8,192 token context limit on Groq free tier. "
         "The match brief input (venue profile + phase scores + matchup data) is large — "
         "monitor for truncation errors if context grows.",
         "Monitor"],
        ["Session cookie expires on browser close",
         "HttpOnly session cookie has no Max-Age — deleted when browser closes. "
         "Users must re-enter access code each new browser session.",
         "By design"],
        ["Render free tier = cold starts",
         "Without UptimeRobot pinging the service, Render sleeps after 15 min idle. "
         "Cold start = 30–90 second delay for next visitor.",
         "Mitigated"],
        ["No persistent storage on Render free",
         "Render free tier has no persistent disk. Demo requests are logged to stdout only "
         "(Render logs). If email is not configured, requests could be missed if logs scroll off.",
         "Mitigated"],
    ]
    t = Table(rows, colWidths=[36*mm, 100*mm, 20*mm])
    st = TableStyle([
        ("BACKGROUND",    (0,0), (-1,0),  BLUE),
        ("TEXTCOLOR",     (0,0), (-1,0),  WHITE),
        ("FONTNAME",      (0,0), (-1,0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0,0), (-1,-1), 7.5),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 7),
        ("RIGHTPADDING",  (0,0), (-1,-1), 7),
        ("GRID",          (0,0), (-1,-1), 0.35, GREY_LINE),
        ("VALIGN",        (0,0), (-1,-1), "TOP"),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [WHITE, BG_ALT]),
        ("FONTNAME",      (0,1), (-1,-1), "Helvetica"),
        ("ALIGN",         (2,0), (2,-1),  "CENTER"),
    ])
    for i, row in enumerate(rows[1:], 1):
        sev = row[2]
        if sev in ("By design", "Documented"):
            st.add("TEXTCOLOR", (2,i), (2,i), MUTED)
        elif sev in ("Caution", "Monitor"):
            st.add("TEXTCOLOR", (2,i), (2,i), AMBER)
            st.add("FONTNAME",  (2,i), (2,i), "Helvetica-Bold")
        elif sev == "Mitigated":
            st.add("TEXTCOLOR", (2,i), (2,i), GREEN)
            st.add("FONTNAME",  (2,i), (2,i), "Helvetica-Bold")
    t.setStyle(st)
    e.append(t)
    e.append(sp(4))
    return e

# ── SECTION 14: Roadmap ──────────────────────────────────────────────────────────
def s14_roadmap():
    e = []
    e.append(Paragraph("14. Roadmap", S["h1"]))
    e.append(rule())

    rows = [
        ["Priority", "Feature", "Effort", "Status"],
        ["✓ Done",  "Render deployment + auto-deploy",                     "Low",    "Complete"],
        ["✓ Done",  "Server-side cookie auth (all pages + data gated)",    "Medium", "Complete"],
        ["✓ Done",  "Public marketing landing page (index.html)",          "Medium", "Complete"],
        ["✓ Done",  "Demo request form → server log + Gmail notification", "Low",    "Complete"],
        ["✓ Done",  "AI Match Brief — Groq / Llama 3.3 70B",              "Medium", "Complete"],
        ["✓ Done",  "Live Score Widget — CricAPI, budget-aware polling",   "Medium", "Complete"],
        ["✓ Done",  "CreaseIQ brand applied across all surfaces",          "Low",    "Complete"],
        ["⚡ Now",  "Set up UptimeRobot to prevent cold starts",           "Low",    "Tonight"],
        ["⚡ Now",  "Set Render env vars: GROQ_API_KEY, CRICAPI_KEY",      "Low",    "Tonight"],
        ["⚡ Now",  "Live test on Mar 30 — RR vs CSK — score + AI brief",  "Low",    "Mar 30"],
        ["Next",    "Bowler diagnostics (mirror of batter diagnostics)",    "Medium", "Queued"],
        ["Next",    "Match brief PDF/PNG export",                           "Low",    "Queued"],
        ["Next",    "LinkedIn post + cold outreach to RR",                  "—",      "Mar 30"],
        ["Soon",    "Second franchise deployment (new access code)",        "Low",    "Backlog"],
        ["Soon",    "Custom domain (creaseiq.com or creaseiq.cricket)",     "Low",    "Backlog"],
        ["Backlog", "CricAPI upgrade if high concurrent usage",             "Low",    "Backlog"],
        ["Backlog", "Formal seed raise / franchise contract",               "—",      "Backlog"],
    ]
    t = Table(rows, colWidths=[22*mm, 90*mm, 18*mm, 26*mm])
    st = TableStyle([
        ("BACKGROUND",    (0,0), (-1,0),  BLUE),
        ("TEXTCOLOR",     (0,0), (-1,0),  WHITE),
        ("FONTNAME",      (0,0), (-1,0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0,0), (-1,-1), 8),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 7),
        ("RIGHTPADDING",  (0,0), (-1,-1), 7),
        ("GRID",          (0,0), (-1,-1), 0.35, GREY_LINE),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [WHITE, BG_ALT]),
        ("FONTNAME",      (0,1), (-1,-1), "Helvetica"),
    ])
    for i, row in enumerate(rows[1:], 1):
        if "✓" in row[0]:
            st.add("TEXTCOLOR",  (0,i), (0,i), GREEN)
            st.add("FONTNAME",   (0,i), (0,i), "Helvetica-Bold")
            st.add("BACKGROUND", (0,i), (-1,i), BG_GREEN)
        elif "⚡" in row[0]:
            st.add("TEXTCOLOR",  (0,i), (0,i), PINK)
            st.add("FONTNAME",   (0,i), (0,i), "Helvetica-Bold")
            st.add("BACKGROUND", (0,i), (-1,i), BG_PINK)
        elif row[0] == "Next":
            st.add("TEXTCOLOR",  (0,i), (0,i), BLUE)
            st.add("FONTNAME",   (0,i), (0,i), "Helvetica-Bold")
        elif row[0] == "Soon":
            st.add("TEXTCOLOR",  (0,i), (0,i), AMBER)
            st.add("FONTNAME",   (0,i), (0,i), "Helvetica-Bold")
    t.setStyle(st)
    e.append(t)
    e.append(sp(4))
    return e

# ── Footer ─────────────────────────────────────────────────────────────────────
def footer():
    return [
        grey_rule(),
        Paragraph(
            f"CreaseIQ  ·  Internal Team Reference  ·  v2.0  ·  "
            f"{date.today().strftime('%B %d, %Y')}  ·  Not for external distribution",
            S["footer"]),
    ]

# ── Build ──────────────────────────────────────────────────────────────────────
def build():
    doc = SimpleDocTemplate(
        OUT, pagesize=A4,
        leftMargin=M, rightMargin=M, topMargin=M, bottomMargin=M,
        title="CreaseIQ — Internal Team Reference v2.0",
        author="Piyush Zaware",
    )
    story = []
    story += cover()
    story += s1_products()
    story += s2_architecture()
    story += s3_auth()
    story += s4_env()
    story += s5_local()
    story += s6_pipeline()
    story += s7_features()
    story += s8_apis()
    story += s9_budget()
    story += s10_demo()
    story += s11_deploy()
    story += s12_uptime()
    story += s13_limits()
    story += s14_roadmap()
    story += footer()
    doc.build(story)
    print(f"PDF written → {OUT}")

if __name__ == "__main__":
    build()
