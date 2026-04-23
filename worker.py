import json
import hmac
import hashlib
import base64
import time
import re
from urllib.parse import parse_qs, urlparse
from js import fetch, Response, Headers, Object, Request as JsRequest
from pyodide.ffi import to_js

USERS = {
    "Best Prof. Ever": "Mr Nikouei",
}


def make_session_token(username, secret):
    payload = json.dumps({"u": username, "exp": int(time.time()) + 86400 * 7})
    sig = hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()
    return base64.urlsafe_b64encode(f"{payload}|||{sig}".encode()).decode()


def verify_session(request, secret):
    cookie_header = request.headers.get("Cookie") or ""
    for part in cookie_header.split(";"):
        part = part.strip()
        if part.startswith("session="):
            token = part[8:]
            try:
                decoded = base64.urlsafe_b64decode(token.encode()).decode()
                payload, sig = decoded.split("|||", 1)
                expected = hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()
                if hmac.compare_digest(sig, expected):
                    data = json.loads(payload)
                    if data["exp"] > int(time.time()):
                        return data["u"]
            except Exception:
                pass
    return None


def redirect_to(location, extra_headers=None):
    h = Headers.new()
    h.set("Location", location)
    if extra_headers:
        for k, v in extra_headers.items():
            h.set(k, v)
    return Response.new("", status=302, headers=h)


def json_resp(data, status=200):
    h = Headers.new()
    h.set("Content-Type", "application/json")
    return Response.new(json.dumps(data), status=status, headers=h)


async def serve_asset(env, request, path):
    url = request.url
    origin = url[:url.index("/", 8)] if "//" in url else url
    asset_req = JsRequest.new(f"{origin}{path}")
    return await env.ASSETS.fetch(asset_req)


async def handle_login_post(request, env, secret):
    body_text = await request.text()
    params = parse_qs(body_text)
    username = params.get("username", [""])[0].strip()
    password = params.get("password", [""])[0]

    if username in USERS and USERS[username] == password:
        token = make_session_token(username, secret)
        cookie = f"session={token}; Path=/; Max-Age=604800; HttpOnly; Secure; SameSite=Lax"
        return redirect_to("/dashboard", {"Set-Cookie": cookie})

    return redirect_to("/login?error=1")


async def handle_chat(request, env):
    body_text = await request.text()
    api_key = request.headers.get("x-anthropic-key") or getattr(env, "ANTHROPIC_API_KEY", "")

    init = to_js(
        {
            "method": "POST",
            "headers": {
                "Content-Type": "application/json",
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
            },
            "body": body_text,
        },
        dict_converter=Object.fromEntries,
    )

    resp = await fetch("https://api.anthropic.com/v1/messages", init)
    resp_text = await resp.text()

    h = Headers.new()
    h.set("Content-Type", "application/json")
    return Response.new(resp_text, status=resp.status, headers=h)


async def handle_draft_email(request, env):
    try:
        body = json.loads(await request.text())
        vendor = body.get("vendor", {})
        ud = body.get("user_details", {})
        api_key = request.headers.get("x-anthropic-key") or getattr(env, "ANTHROPIC_API_KEY", "")

        vtype = vendor.get("vendor_type", "")
        vname = vendor.get("vendor_name", "Vendor")
        contact = vendor.get("contact_name", "Team")
        city = vendor.get("location_city", "")
        price = vendor.get("price_range", "")
        resp_h = vendor.get("response_time_hours", 24)

        change_request = body.get("change_request", "")
        current_draft = body.get("current_draft", {})

        extra = {k.rstrip(' *'): v for k, v in ud.items() if k not in ("name", "email", "date", "budget") and v}
        detail_lines = "\n".join(f"- {k}: {v}" for k, v in extra.items())

        if change_request and current_draft:
            prompt = f"""Revise this vendor inquiry email. Output ONLY in the exact format below — no extra text, no markdown.

SUBJECT: [revised subject line]

BODY:
[revised email body]

Current draft:
SUBJECT: {current_draft.get('subject', '')}

BODY:
{current_draft.get('body', '')}

Changes requested: {change_request}
Keep it professional, ~150–200 words, addressed to {contact} at {vname}."""
        else:
            prompt = f"""Write a professional vendor inquiry email. Output ONLY in the exact format below — no extra text, no markdown, no JSON.

SUBJECT: [email subject line]

BODY:
[full email body — 180 to 220 words]

Use these details:
Sender name: {ud.get('name', '[Name]')}
Event date: {ud.get('date', 'TBD')}
Budget: {ud.get('budget', 'Flexible')}
Vendor: {vname} ({vtype}, {city})
Contact person: {contact}
{detail_lines}

The body must:
- Open with "Dear {contact},"
- Introduce {ud.get('name','the sender')} and the event
- Mention every detail listed above naturally in the text
- Ask about availability on the event date
- Ask for pricing and package details for {vtype} services
- Close with a clear call to action and "{ud.get('name','[Name]')}" as the sign-off name
- NOT include From/To/Subject headers"""

        init = to_js({
            "method": "POST",
            "headers": {
                "Content-Type": "application/json",
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
            },
            "body": json.dumps({
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 900,
                "messages": [{"role": "user", "content": prompt}],
            }),
        }, dict_converter=Object.fromEntries)

        resp = await fetch("https://api.anthropic.com/v1/messages", init)
        data = json.loads(await resp.text())
        raw = (data.get("content") or [{}])[0].get("text", "").strip()

        # Parse SUBJECT: and BODY: delimiters
        subject = f"Booking Inquiry — {vname}"
        body = ""

        subject_m = re.search(r'SUBJECT:\s*(.+)', raw)
        if subject_m:
            subject = subject_m.group(1).strip()

        body_m = re.search(r'BODY:\s*\n([\s\S]+)', raw)
        if body_m:
            body = body_m.group(1).strip()

        # Fallback: if no BODY: marker, use everything after the subject line
        if not body:
            body = re.sub(r'^SUBJECT:.*\n?', '', raw, count=1).strip()

        # Last resort: use the full raw response
        if not body:
            body = raw

        return json_resp({"subject": subject, "body": body})
    except Exception as e:
        return json_resp({"error": str(e)}, 500)


async def handle_send_email(request, env):
    try:
        body = json.loads(await request.text())
        resend_key = getattr(env, "RESEND_API_KEY", "")
        if not resend_key:
            return json_resp({"error": "Email service not configured — add RESEND_API_KEY as a Worker secret."}, 503)

        email_body = (body.get("body") or "").strip()
        if not email_body:
            return json_resp({"error": "Email body is empty — please go back and regenerate the draft."}, 400)

        html_body = "<br>".join(
            f"<p>{line}</p>" if line.strip() else "<br>"
            for line in email_body.split("\n")
        )

        payload = {
            "from": "Atelier Inquiry <onboarding@resend.dev>",
            "to": [body.get("to", "")],
            "reply_to": body.get("from_email", ""),
            "subject": body.get("subject") or "Vendor Inquiry",
            "html": html_body,
            "text": email_body,
        }

        init = to_js({
            "method": "POST",
            "headers": {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {resend_key}",
            },
            "body": json.dumps(payload),
        }, dict_converter=Object.fromEntries)

        resp = await fetch("https://api.resend.com/emails", init)
        result = json.loads(await resp.text())
        if resp.status >= 400:
            return json_resp({"error": result.get("message", "Email delivery failed")}, resp.status)

        return json_resp({"success": True, "id": result.get("id", "")})
    except Exception as e:
        return json_resp({"error": str(e)}, 500)


async def on_fetch(request, env):
    parsed = urlparse(request.url)
    path = parsed.path or "/"
    method = request.method
    secret = getattr(env, "SECRET_KEY", "atelier-default-secret-change-me")

    if path in ("/", ""):
        user = verify_session(request, secret)
        return redirect_to("/dashboard" if user else "/login")

    if path == "/login":
        if method == "POST":
            return await handle_login_post(request, env, secret)
        return await serve_asset(env, request, "/login.html")

    if path == "/dashboard":
        if not verify_session(request, secret):
            return redirect_to("/login")
        return await serve_asset(env, request, "/dashboard.html")

    if path == "/logout":
        return redirect_to("/login", {"Set-Cookie": "session=; Path=/; Max-Age=0; HttpOnly; Secure; SameSite=Lax"})

    if path == "/api/chat" and method == "POST":
        if not verify_session(request, secret):
            return json_resp({"error": "Unauthorized"}, 401)
        return await handle_chat(request, env)

    if path == "/api/draft-email" and method == "POST":
        if not verify_session(request, secret):
            return json_resp({"error": "Unauthorized"}, 401)
        return await handle_draft_email(request, env)

    if path == "/api/send-email" and method == "POST":
        if not verify_session(request, secret):
            return json_resp({"error": "Unauthorized"}, 401)
        return await handle_send_email(request, env)

    return await serve_asset(env, request, path)
