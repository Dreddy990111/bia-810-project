# Atelier — Vendor Intelligence Platform
## BIA 810 Course Project

A vendor intelligence dashboard with login/session auth and an AI chat engine backed by Anthropic's API. Deployed to Cloudflare Workers (Python) with static assets.

---

## Stack

| Layer | Technology |
|-------|-----------|
| Runtime | Cloudflare Workers (Python via pyodide) |
| Frontend | Vanilla HTML/CSS/JS (single-page dashboard) |
| AI | Anthropic Claude (`claude-sonnet-4-20250514`) via Worker proxy |
| Auth | HMAC-signed session cookies |
| Local dev | Flask (app.py) + `wrangler dev` |

---

## Project Structure

```
BIA 810 project/
├── worker.py               # Cloudflare Worker — routes, auth, Anthropic proxy
├── wrangler.toml           # Wrangler deployment config
├── public/
│   ├── login.html          # Login page (static, JS error handling)
│   └── dashboard.html      # Main vendor intelligence dashboard
├── app.py                  # Flask server (local dev / legacy)
├── .env                    # API key (never commit)
├── .gitignore
├── requirements.txt
├── templates/              # Flask templates (legacy, kept for local dev)
│   ├── login.html
│   └── dashboard.html
└── vendoriq_elegant-4.html # Original standalone HTML (source of truth for UI)
```

---

## Deployment (Cloudflare Workers)

**Live URL:** https://atelier.atelier-iq.workers.dev

**Deploy:**
```bash
cd "/Users/dreddy/Desktop/BIA 810 project"
npx wrangler deploy
```

**Local dev:**
```bash
npx wrangler dev --port 8787
```

**Secrets** (set via `wrangler secret put`):
- `ANTHROPIC_API_KEY` — Anthropic API key (primary AI provider)
- `SECRET_KEY` — HMAC signing key for session cookies

**Account:**
- Cloudflare email: Dhanvanth0111@gmail.com
- Workers subdomain: `atelier-iq.workers.dev`
- Cloudflare Account ID: `4e0bedd2b206fd2123e1b057002baa70`

---

## Auth

- Sessions via HMAC-signed cookies (worker.py)
- Users defined in `USERS` dict — no database
- Current credentials: `Best Prof. Ever` / `Mr Nikouei`

## API Key

- `ANTHROPIC_API_KEY` stored as Cloudflare secret in production
- Users can also paste their own Anthropic key in the dashboard UI (stored in localStorage, sent via `x-anthropic-key` header)
- Never sent to the browser directly — all AI calls proxied through `/api/chat`

---

## Routes

| Route | Description |
|-------|-------------|
| `/` | Redirects to `/login` or `/dashboard` |
| `/login` | Login form (GET + POST) |
| `/dashboard` | Protected dashboard (requires session) |
| `/logout` | Clears session, redirects to login |
| `/api/chat` | Anthropic proxy — requires session, POST only |

---

## Dashboard Features

- **100 vendors** across 3 types: **AV** (35), **Catering** (35), **Venue** (30)
- **Real dataset**: `event_vendors_dataset_1.xlsx` — prices are real midpoints from dataset (`min_price`/`max_price`)
- **Price filter slider**: $1,000–$11,000 (real data range)
- **AI chat** — Anthropic claude-sonnet-4 with built-in `web_search_20250305` tool (agentic loop)
- **Anthropic API Key input** in chat panel — saves to localStorage, falls back to Cloudflare secret
- **Chat panel** has dark event venue background image
- **Header stats**: "Top Vendors", "24/7 Availability", "Top Rated" (static labels)
- **Vendor modal** includes:
  - Contact info (name, email, phone) from dataset
  - Short description, highlighted pros, limitations
  - Guest range, lead time, neighborhood, indoor/outdoor
  - **Send Booking Inquiry** — mailto: button with pre-filled professional email
  - **Book Now** — Google search redirect
  - **Visit Website** — Google search redirect
- **Per-type pricing display:**
  - Catering → `$X–$Y/pp` (real per-person range from dataset)
  - AV → `$X/hr` (midpoint ÷ 8hr day)
  - Venue → total midpoint price
- **`templates/dashboard.html`** kept in sync with `public/dashboard.html`

---

## GitHub

- Repo: https://github.com/Dreddy990111/bia-810-project
- Branch: `main`
- Latest commit: `cf2323e` — Integrate real vendor dataset — clean data, real prices, rich modal details

---

## Running Locally (Flask)

```bash
cd "/Users/dreddy/Desktop/BIA 810 project"
python3 app.py
# Opens at http://127.0.0.1:5000
```

---

## Render (legacy, may still be running)

- Service: `atelier` at https://atelier-9wo0.onrender.com
- Dashboard: https://dashboard.render.com/web/srv-d7dssk58nd3s73b6qgu0

---

## MCP Server

Filesystem MCP configured at:
`~/Library/Application Support/Claude/claude_desktop_config.json`

Grants Claude Desktop access to: Desktop, Downloads, Documents.
Restart Claude Desktop to activate.
