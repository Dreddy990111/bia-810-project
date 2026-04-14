from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import date

# ── Atelier Theme Colors ────────────────────────────────────────────────────────
INK        = colors.HexColor("#0e0e0e")   # deep black background
INK2       = colors.HexColor("#1c1c1c")   # card background
INK3       = colors.HexColor("#2a2a2a")   # subtle surface
PAPER      = colors.HexColor("#f5f2ed")   # warm white text
PAPER2     = colors.HexColor("#ede9e2")
GOLD       = colors.HexColor("#b8913a")   # primary gold
GOLD_LIGHT = colors.HexColor("#d4a84b")   # bright gold
GOLD_DIM   = colors.HexColor("#7a5f24")   # muted gold
MIST       = colors.HexColor("#6b6560")
MIST2      = colors.HexColor("#8c847c")
MIST3      = colors.HexColor("#aba39b")
LINE       = colors.HexColor("#2d2516")   # gold-tinted dark line
LINE2      = colors.HexColor("#3d3220")

OUTPUT = "/Users/dreddy/Desktop/BIA 810 project/Atelier_Project_Report.pdf"

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=letter,
    rightMargin=0.85 * inch,
    leftMargin=0.85 * inch,
    topMargin=1 * inch,
    bottomMargin=1 * inch,
)

styles = getSampleStyleSheet()

# ── Custom Styles ───────────────────────────────────────────────────────────────
title_style = ParagraphStyle(
    "CustomTitle",
    parent=styles["Title"],
    fontSize=30,
    textColor=GOLD_LIGHT,
    spaceAfter=4,
    alignment=TA_CENTER,
    fontName="Helvetica-Bold",
)
subtitle_style = ParagraphStyle(
    "Subtitle",
    parent=styles["Normal"],
    fontSize=11,
    textColor=MIST3,
    spaceAfter=3,
    alignment=TA_CENTER,
    fontName="Helvetica",
)
meta_style = ParagraphStyle(
    "Meta",
    parent=styles["Normal"],
    fontSize=10,
    textColor=MIST2,
    spaceAfter=3,
    alignment=TA_CENTER,
    fontName="Helvetica",
)
section_style = ParagraphStyle(
    "Section",
    parent=styles["Heading1"],
    fontSize=13,
    textColor=GOLD,
    spaceBefore=18,
    spaceAfter=4,
    fontName="Helvetica-Bold",
)
subsection_style = ParagraphStyle(
    "Subsection",
    parent=styles["Heading2"],
    fontSize=10.5,
    textColor=GOLD_LIGHT,
    spaceBefore=10,
    spaceAfter=3,
    fontName="Helvetica-Bold",
)
body_style = ParagraphStyle(
    "Body",
    parent=styles["Normal"],
    fontSize=9.5,
    textColor=PAPER2,
    spaceAfter=6,
    leading=15,
    alignment=TA_JUSTIFY,
    fontName="Helvetica",
)
bullet_style = ParagraphStyle(
    "Bullet",
    parent=body_style,
    leftIndent=16,
    spaceAfter=3,
    bulletIndent=4,
)
code_style = ParagraphStyle(
    "Code",
    parent=styles["Code"],
    fontSize=8,
    textColor=GOLD_LIGHT,
    backColor=INK3,
    borderColor=GOLD_DIM,
    borderWidth=0.5,
    borderPad=6,
    fontName="Courier",
    spaceAfter=8,
)
caption_style = ParagraphStyle(
    "Caption",
    parent=body_style,
    fontSize=8.5,
    textColor=MIST3,
    alignment=TA_CENTER,
    spaceAfter=6,
)

def divider(color=None, thickness=0.8):
    c = color or GOLD_DIM
    return HRFlowable(width="100%", thickness=thickness, color=c, spaceAfter=6, spaceBefore=2)

def make_table(data, col_widths, header=True):
    t = Table(data, colWidths=col_widths)
    style = [
        # Header row
        ("BACKGROUND", (0, 0), (-1, 0), INK2),
        ("TEXTCOLOR", (0, 0), (-1, 0), GOLD_LIGHT),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 9),
        # Body rows
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [INK3, INK2]),
        ("TEXTCOLOR", (0, 1), (-1, -1), PAPER2),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 1), (-1, -1), 8.5),
        # Grid
        ("GRID", (0, 0), (-1, -1), 0.4, GOLD_DIM),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
    ]
    t.setStyle(TableStyle(style))
    return t

# ── Page background canvas callback ────────────────────────────────────────────
def dark_background(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(INK)
    canvas.rect(0, 0, letter[0], letter[1], fill=1, stroke=0)
    # Subtle gold bottom rule
    canvas.setStrokeColor(GOLD_DIM)
    canvas.setLineWidth(0.5)
    canvas.line(0.85*inch, 0.65*inch, letter[0]-0.85*inch, 0.65*inch)
    # Page number
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MIST3)
    canvas.drawCentredString(letter[0]/2, 0.45*inch, f"{doc.page}")
    canvas.restoreState()

story = []

# ── COVER ──────────────────────────────────────────────────────────────────────
story.append(Spacer(1, 0.7 * inch))
story.append(Paragraph("Atelier", title_style))
story.append(Paragraph("Vendor Intelligence Platform", subtitle_style))
story.append(Spacer(1, 0.12 * inch))
story.append(divider(GOLD, 1.5))
story.append(Spacer(1, 0.18 * inch))
story.append(Paragraph("BIA 810 — Course Project Report", meta_style))
story.append(Paragraph(f"Date: {date.today().strftime('%B %d, %Y')}", meta_style))
story.append(Spacer(1, 0.12 * inch))
story.append(Paragraph("Project by:", meta_style))
for name in ["Rohini Mallikarjunaiah", "Jaanvi Vemana", "Lynn Chirimumimba", "Dhanvanth Reddy"]:
    story.append(Paragraph(name, ParagraphStyle(
        "TeamName", parent=meta_style,
        fontSize=11, textColor=PAPER, spaceAfter=2, fontName="Helvetica-Bold"
    )))
story.append(Spacer(1, 0.3 * inch))
story.append(divider(GOLD_DIM))

# ── 1. EXECUTIVE SUMMARY ───────────────────────────────────────────────────────
story.append(Paragraph("1. Executive Summary", section_style))
story.append(divider())
story.append(Paragraph(
    "Atelier is a full-stack vendor intelligence web application developed for BIA 810. "
    "It provides a curated, searchable directory of 100 event vendors across New York and New Jersey, "
    "complete with 2025 market-rate pricing, advanced filtering, and an integrated AI chat assistant "
    "powered by Anthropic's Claude. The platform is deployed on Cloudflare's global edge network, "
    "delivering fast, secure access with HMAC-based session authentication — all without a traditional "
    "server or database.",
    body_style,
))
story.append(Paragraph(
    "The project demonstrates the application of modern serverless architecture, AI integration, "
    "and practical event-industry domain knowledge in a single cohesive product.",
    body_style,
))

# ── 2. PROJECT OBJECTIVES ──────────────────────────────────────────────────────
story.append(Paragraph("2. Project Objectives", section_style))
story.append(divider())
for item in [
    "Build a production-grade, publicly accessible web application — not just a prototype.",
    "Integrate a live AI assistant capable of answering natural-language queries about vendors and event planning.",
    "Reflect real 2025 NYC/NJ market pricing across five vendor categories.",
    "Implement secure, stateless authentication without a database.",
    "Deploy to a global CDN (Cloudflare Workers) with zero infrastructure overhead.",
]:
    story.append(Paragraph(f"• {item}", bullet_style))

# ── 3. TECHNOLOGY STACK ────────────────────────────────────────────────────────
story.append(Paragraph("3. Technology Stack", section_style))
story.append(divider())
story.append(Spacer(1, 4))
stack_data = [
    ["Layer", "Technology", "Purpose"],
    ["Runtime", "Cloudflare Workers (Python/Pyodide)", "Serverless edge compute — runs worker.py globally"],
    ["Frontend", "Vanilla HTML / CSS / JavaScript", "Single-page dashboard, zero framework dependencies"],
    ["AI Engine", "Anthropic Claude claude-sonnet-4-20250514", "Natural language chat with live web search tool"],
    ["Authentication", "HMAC-signed session cookies", "Stateless, secure sessions — no database required"],
    ["Local Dev", "Flask (app.py) + Wrangler CLI", "Local testing that mirrors production behavior"],
    ["Version Control", "Git / GitHub", "Source history at Dreddy990111/bia-810-project"],
    ["Secrets Mgmt", "Cloudflare Secrets Vault", "API keys never exposed to the browser"],
]
story.append(make_table(stack_data, [1.1*inch, 2.3*inch, 3.0*inch]))

# ── 4. SYSTEM ARCHITECTURE ────────────────────────────────────────────────────
story.append(Paragraph("4. System Architecture", section_style))
story.append(divider())
story.append(Paragraph(
    "Atelier follows a serverless, edge-first architecture. There is no traditional web server, "
    "application server, or database. All logic runs inside a single Cloudflare Worker (worker.py), "
    "which handles routing, authentication, static asset delivery, and AI proxying.",
    body_style,
))
story.append(Paragraph("Request Flow:", subsection_style))
story.append(Paragraph("Browser  →  Cloudflare Edge Network  →  worker.py", code_style))
flow_data = [
    ["Route", "Method", "What Happens"],
    ["/", "GET", "Redirects to /login or /dashboard based on session state"],
    ["/login", "GET", "Serves the static login page (login.html)"],
    ["/login", "POST", "Validates credentials, sets HMAC-signed session cookie"],
    ["/dashboard", "GET", "Validates session cookie, serves dashboard.html"],
    ["/logout", "GET", "Clears session cookie, redirects to /login"],
    ["/api/chat", "POST", "Validates session, proxies request to Anthropic API, streams response"],
]
story.append(make_table(flow_data, [1.1*inch, 0.75*inch, 4.5*inch]))
story.append(Spacer(1, 6))
story.append(Paragraph(
    "The AI chat endpoint acts as a secure proxy — the Anthropic API key lives in Cloudflare's "
    "secret vault and is never sent to the browser. All AI calls are made server-side.",
    body_style,
))

# ── 5. CODEBASE BREAKDOWN ─────────────────────────────────────────────────────
story.append(Paragraph("5. Codebase Breakdown", section_style))
story.append(divider())

story.append(Paragraph("5.1  worker.py — Cloudflare Worker (Backend)", subsection_style))
story.append(Paragraph(
    "The core of the application. This single Python file handles everything the server needs to do:",
    body_style,
))
for item in [
    "Route dispatch — maps incoming HTTP paths to handler functions.",
    "HMAC cookie auth — signs cookies on login using SECRET_KEY; validates on every protected route.",
    "Static file serving — returns login.html and dashboard.html as HTTP responses.",
    "Anthropic API proxy — receives chat messages from the browser, forwards them to Claude, and streams the response back.",
    "Secret injection — reads ANTHROPIC_API_KEY and SECRET_KEY from Cloudflare's runtime environment.",
]:
    story.append(Paragraph(f"• {item}", bullet_style))

story.append(Paragraph("5.2  public/dashboard.html — Frontend Application", subsection_style))
story.append(Paragraph("The entire user-facing application in a single HTML file. It contains:", body_style))
for item in [
    "Vendor data array — 100 vendors with names, categories, ratings, and pricing embedded as JavaScript.",
    "Pricing normalization — runs at page load; computes per-type display prices from base rates using rating and event-type multipliers.",
    "Filtering engine — category selector and price range slider filter the vendor array in memory (no server calls).",
    "Vendor cards & modal — dynamically rendered DOM elements; modal shows full vendor detail with Book Now and Visit Website buttons.",
    "AI chat panel — sends fetch() POST to /api/chat, renders streamed response; reads user-supplied Anthropic key from localStorage.",
]:
    story.append(Paragraph(f"• {item}", bullet_style))

story.append(Paragraph("5.3  public/login.html — Login Page", subsection_style))
story.append(Paragraph(
    "Static HTML form. Submits credentials to POST /login. JavaScript handles and displays error messages "
    "returned by the Worker without a full page reload.",
    body_style,
))

story.append(Paragraph("5.4  wrangler.toml — Deployment Configuration", subsection_style))
story.append(Paragraph(
    "Configures the Cloudflare Workers deployment: account ID, worker name, Python runtime, "
    "and asset bindings. A single command (npx wrangler deploy) pushes the full application to production.",
    body_style,
))

story.append(Paragraph("5.5  app.py — Local Development Server (Flask)", subsection_style))
story.append(Paragraph(
    "A Flask application that mirrors the Worker's routes for local development and testing "
    "without requiring Cloudflare. Kept as a legacy development tool.",
    body_style,
))

# ── 6. KEY FEATURES ───────────────────────────────────────────────────────────
story.append(Paragraph("6. Key Features", section_style))
story.append(divider())

story.append(Paragraph("6.1  Vendor Directory", subsection_style))
story.append(Paragraph(
    "100 vendors across five categories: Catering, Venue, AV, Entertainment, and Decor. "
    "Each vendor includes a name, category, star rating, and pricing calculated from 2025 NYC/NJ market benchmarks.",
    body_style,
))

story.append(Paragraph("6.2  2025 Market-Rate Pricing", subsection_style))
pricing_data = [
    ["Category", "Pricing Display", "Market Range"],
    ["Catering", "$X/pp (per person, 75 guests)", "$95 – $160 per person"],
    ["Venue", "Total price", "$18,000 – $38,000"],
    ["AV", "$X/hr (total cost / 8hr day)", "$3,500 – $7,500 per day"],
    ["Entertainment", "$X/hr (total cost / 4hr event)", "$2,200 – $5,000 per event"],
    ["Decor", "Average cost per event type", "$3,500 – $12,000 per event"],
    ["Floral", "N/A — Quote on request", "Varies"],
]
story.append(make_table(pricing_data, [1.3*inch, 2.2*inch, 2.9*inch]))
story.append(Spacer(1, 4))
story.append(Paragraph(
    "Prices are dynamically normalized at page load using each vendor's star rating as a multiplier, "
    "ensuring higher-rated vendors reflect premium pricing consistent with market expectations.",
    body_style,
))

story.append(Paragraph("6.3  Filtering & Search", subsection_style))
for item in [
    "Category filter buttons — instantly shows vendors by type.",
    "Price range slider — range $2,200 to $38,000, filters vendors in real time.",
    "Text search — searches vendor names as the user types.",
]:
    story.append(Paragraph(f"• {item}", bullet_style))

story.append(Paragraph("6.4  Vendor Modal", subsection_style))
story.append(Paragraph(
    "Clicking any vendor card opens a detail modal showing the full vendor profile. Two action buttons are available:",
    body_style,
))
for item in [
    "Book Now — redirects to a Google search for the vendor's booking page.",
    "Visit Website — redirects to a Google search for the vendor's official website.",
]:
    story.append(Paragraph(f"• {item}", bullet_style))

story.append(Paragraph("6.5  AI Chat Assistant", subsection_style))
story.append(Paragraph(
    "An integrated chat panel powered by Anthropic's Claude (claude-sonnet-4-20250514). Key capabilities:",
    body_style,
))
for item in [
    "Natural language Q&A — users can ask anything about vendors, event planning, pricing comparisons, or logistics.",
    "Live web search — Claude has access to the web_search_20250305 tool, enabling it to retrieve current information during a conversation.",
    "Bring-your-own API key — users can paste their own Anthropic API key in the dashboard UI; saved to localStorage and sent via a custom request header. Falls back to the Cloudflare secret if none is provided.",
    "Secure proxying — all API calls go through /api/chat on the Worker; the key is never exposed client-side.",
]:
    story.append(Paragraph(f"• {item}", bullet_style))

story.append(Paragraph("6.6  Authentication", subsection_style))
story.append(Paragraph(
    "Atelier uses HMAC-signed session cookies for authentication — a stateless approach that requires no "
    "database. On login, the Worker signs a session payload with SECRET_KEY using HMAC-SHA256 and sets "
    "it as a cookie. Every subsequent request to a protected route verifies the signature. Tampered or "
    "missing cookies are rejected immediately.",
    body_style,
))

# ── 7. INFRASTRUCTURE ─────────────────────────────────────────────────────────
story.append(Paragraph("7. Infrastructure & Deployment", section_style))
story.append(divider())

story.append(Paragraph("7.1  Cloudflare Workers (Production)", subsection_style))
story.append(Paragraph("Cloudflare Workers is the sole production infrastructure. It provides:", body_style))
for item in [
    "Compute — executes worker.py at the edge, close to the user, with no cold-start penalty.",
    "Hosting — serves static HTML assets (login, dashboard) directly from the Worker.",
    "Security — stores API keys in a secret vault; enforces HTTPS automatically.",
    "Global CDN — runs in Cloudflare's 300+ data centers worldwide.",
    "Domain — atelier.atelier-iq.workers.dev (Cloudflare-managed subdomain).",
]:
    story.append(Paragraph(f"• {item}", bullet_style))
story.append(Paragraph("Deploy command:", subsection_style))
story.append(Paragraph("npx wrangler deploy", code_style))

story.append(Paragraph("7.2  GitHub (Version Control)", subsection_style))
story.append(Paragraph(
    "GitHub serves as source history and backup only — it has no role in serving the application. "
    "There is no CI/CD pipeline; deployments are triggered manually via the Wrangler CLI. "
    "Repository: Dreddy990111/bia-810-project, branch: main.",
    body_style,
))

story.append(Paragraph("7.3  Render (Legacy — Inactive)", subsection_style))
story.append(Paragraph(
    "An earlier version of Atelier was hosted on Render using the Flask backend (app.py). "
    "This has since been replaced by Cloudflare Workers. The Render service may still be running "
    "but serves an outdated version of the application and is no longer maintained.",
    body_style,
))

story.append(Paragraph("7.4  Local Development", subsection_style))
story.append(Paragraph("Two options for running Atelier locally:", body_style))
story.append(Paragraph(
    "# Option 1 - Cloudflare Wrangler (mirrors production)\nnpx wrangler dev --port 8787\n\n"
    "# Option 2 - Flask (legacy)\npython3 app.py   # runs at http://127.0.0.1:5000",
    code_style,
))

# ── 8. SECURITY DESIGN ────────────────────────────────────────────────────────
story.append(Paragraph("8. Security Design", section_style))
story.append(divider())
security_data = [
    ["Concern", "How Atelier Addresses It"],
    ["API Key Exposure", "Key stored in Cloudflare secret vault; never sent to browser"],
    ["Session Tampering", "HMAC-SHA256 signed cookies; invalid signatures rejected"],
    ["Unauthorized Access", "Every protected route validates the session cookie before responding"],
    ["Secret Management", "Secrets set via wrangler secret put; never committed to git"],
    ["HTTPS", "Enforced automatically by Cloudflare on all routes"],
]
story.append(make_table(security_data, [2.2*inch, 4.2*inch]))

# ── 9. DESIGN DECISIONS ───────────────────────────────────────────────────────
story.append(Paragraph("9. Design Decisions & Trade-offs", section_style))
story.append(divider())
decisions = [
    ("No framework (vanilla JS)", "Eliminates build tooling, npm, and bundler complexity. The frontend is a single deployable HTML file with no dependencies — ideal for a Cloudflare Workers static asset."),
    ("No database", "HMAC session cookies provide stateless auth. Vendor data is embedded in the HTML. This keeps the architecture simple and the Worker free of external service dependencies."),
    ("Cloudflare over Render/Heroku", "Edge execution means lower latency globally. Cloudflare's secret vault handles API key security natively. No always-on server required."),
    ("Anthropic over OpenAI", "Claude's web_search tool enables agentic, real-time lookups without a separate search API integration."),
    ("Single Worker file", "worker.py handles all server logic in one place — straightforward to audit, deploy, and reason about."),
]
for title, body in decisions:
    story.append(Paragraph(title, subsection_style))
    story.append(Paragraph(body, body_style))

# ── 10. CONCLUSION ────────────────────────────────────────────────────────────
story.append(Paragraph("10. Conclusion", section_style))
story.append(divider())
story.append(Paragraph(
    "Atelier demonstrates that a production-quality, AI-powered web application can be built and "
    "deployed globally with minimal infrastructure overhead. By combining Cloudflare Workers' serverless "
    "edge runtime, Anthropic's Claude AI, and a carefully crafted vanilla frontend, the project achieves "
    "a level of polish and functionality well beyond a typical course prototype.",
    body_style,
))
story.append(Paragraph(
    "The platform is live, publicly accessible, and reflects real-world engineering practices: "
    "secure secret management, stateless authentication, market-accurate data, and an AI assistant "
    "that can search the web in real time — all in a codebase deployable with a single command.",
    body_style,
))
story.append(Spacer(1, 0.25 * inch))
story.append(divider(GOLD, 1.5))
story.append(Paragraph("Live URL: https://atelier.atelier-iq.workers.dev", caption_style))
story.append(Paragraph("Credentials: Best Prof. Ever / Mr Nikouei", caption_style))
story.append(Paragraph("GitHub: github.com/Dreddy990111/bia-810-project", caption_style))

doc.build(story, onFirstPage=dark_background, onLaterPages=dark_background)
print(f"PDF generated: {OUTPUT}")
