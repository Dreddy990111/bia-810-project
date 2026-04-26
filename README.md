# Atelier — Vendor Intelligence Platform

A vendor intelligence web application built for BIA 810 (Developing Business Applications using GenAI). Atelier helps event planners discover, filter, compare, and book vendors across New York City using smart filtering, composite scoring, and an AI-powered chat assistant backed by Anthropic Claude.

**Live application:** https://atelier.atelier-iq.workers.dev
**Team:** Rohini Mallikarjunaiah, Jaanavi Vemana, Lyne Chirimumimba, Dhanvanth Reddy

---

## 1. What the Code Does

Atelier is a single-page vendor intelligence dashboard that solves a real business problem: finding and evaluating event vendors is time-consuming, fragmented, and opaque. The platform addresses this by:

- **Aggregating 125 vendors** across three categories — AV/Equipment, Catering, and Venues — with real pricing data sourced from an event vendor dataset
- **Smart filtering** by vendor type, event type (corporate, wedding, party), budget range, and star rating using a live price-range slider and toggle pills
- **Composite scoring** that ranks vendors by a weighted formula combining price competitiveness, rating, and fit to the selected event type
- **Vendor detail modals** showing contact information, descriptions, highlighted pros, limitations, guest capacity, lead time, and neighborhood
- **Vendor comparison** allowing side-by-side evaluation of up to three vendors
- **Event date picker** for planning context
- **AI chat assistant** powered by Anthropic Claude (`claude-sonnet-4-20250514`) that answers questions strictly within the vendor dataset — no hallucinated vendors or prices
- **Secure authentication** via HMAC-signed session cookies, so only authorized users access the dashboard
- **Booking actions** on every vendor modal: Send Booking Inquiry (pre-filled email), Book Now (Google search), and Visit Website

---

## 2. Structure of the Code

```
BIA 810 project/
├── worker.py               # Cloudflare Worker — all server-side logic
│                           #   - Route handling (/, /login, /dashboard, /logout, /api/chat)
│                           #   - HMAC session cookie auth
│                           #   - Anthropic API proxy (/api/chat)
│
├── wrangler.toml           # Cloudflare Workers deployment config (account ID, routes)
│
├── public/                 # Static assets served by Cloudflare Workers
│   ├── login.html          # Login page with credential form and JS error handling
│   └── dashboard.html      # Main application — all UI, filtering, AI chat, vendor data
│                           #   - 125 vendor records embedded as a JS array
│                           #   - Filter/sort logic in vanilla JS
│                           #   - Anthropic API key input (saves to localStorage)
│                           #   - AI chat panel with agentic web_search tool
│
├── app.py                  # Flask server for local development (mirrors Worker routes)
├── requirements.txt        # Python dependencies (Flask, python-dotenv)
├── .env                    # Local environment variables — NOT committed to git
│
└── templates/              # Flask template copies (kept in sync with public/)
    ├── login.html
    └── dashboard.html
```

**Key design decisions:**
- All vendor data lives in `dashboard.html` as a JS array — no external database needed
- The Cloudflare Worker (`worker.py`) acts as a secure proxy; the Anthropic API key never reaches the browser
- Users may optionally paste their own Anthropic API key in the dashboard; it is stored only in `localStorage` and sent via a custom header, never to any third party

---

## 3. How to Prepare to Run

### Prerequisites

- **Node.js** (v18+) — required for Wrangler CLI
- **Python 3.9+** — required for local Flask development
- **npm** — comes with Node.js
- An **Anthropic API key** — obtain at https://console.anthropic.com

### Install dependencies

```bash
# Install Wrangler (Cloudflare Workers CLI)
npm install -g wrangler

# Install Python dependencies (for local Flask dev)
pip install -r requirements.txt
```

### Set up environment variables

**For local Flask development**, create a `.env` file in the project root:

```
ANTHROPIC_API_KEY=sk-ant-...your-key-here...
SECRET_KEY=any-random-string-for-session-signing
```

**For Cloudflare Workers (production)**, secrets are set via Wrangler and never stored in files:

```bash
npx wrangler secret put ANTHROPIC_API_KEY
npx wrangler secret put SECRET_KEY
```

### Authenticate with Cloudflare (first time only)

```bash
npx wrangler login
```

---

## 4. How to Run

### Option A — Local development with Flask

Flask runs the application locally on port 5000. This is the fastest way to develop and test changes.

```bash
cd "/Users/dreddy/Desktop/BIA 810 project"
python3 app.py
```

Open your browser to: **http://127.0.0.1:5000**

Login credentials:
- **Username:** `Best Prof. Ever`
- **Password:** `Mr Nikouei`

### Option B — Local development with Wrangler (mirrors production)

Wrangler dev runs the actual Cloudflare Worker locally, giving the closest approximation to production behavior.

```bash
cd "/Users/dreddy/Desktop/BIA 810 project"
npx wrangler dev --port 8787
```

Open your browser to: **http://localhost:8787**

### Option C — Deploy to Cloudflare Workers (production)

```bash
cd "/Users/dreddy/Desktop/BIA 810 project"
npx wrangler deploy
```

The app will be live at: **https://atelier.atelier-iq.workers.dev**

### Using the AI Chat

Once logged in, open the chat panel on the right side of the dashboard. You can either:
- Use the Anthropic API key already configured in production (no action needed), or
- Paste your own Anthropic API key into the key input field at the top of the chat panel (it saves automatically to your browser's localStorage)

Ask the assistant anything about the vendors — pricing, availability by event type, comparisons, recommendations.
