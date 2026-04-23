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

        if change_request and current_draft:
            prompt = f"""Revise this vendor inquiry email based on the requested changes.

Current draft:
Subject: {current_draft.get('subject', '')}

{current_draft.get('body', '')}

Changes requested: {change_request}

Apply the requested changes while keeping the email professional and appropriate for a {vtype} inquiry addressed to {contact} at {vname}. Keep it ~150–200 words.

Respond ONLY with a JSON object (no markdown, no code fences):
{{"subject": "...", "body": "..."}}"""
        else:
            extra = {k.rstrip(' *'): v for k, v in ud.items() if k not in ("name", "email", "date", "budget") and v}
            detail_lines = "\n".join(f"  • {k}: {v}" for k, v in extra.items())
            if not detail_lines:
                detail_lines = "  (no additional details provided)"

            prompt = f"""Draft a professional inquiry email from an event planner to a {vtype} vendor.

=== SENDER ===
Name: {ud.get('name', '[Name]')}
Email: {ud.get('email', '')}

=== VENDOR ===
Name: {vname}
Contact: {contact}
Type: {vtype}
City: {city}

=== EVENT DETAILS (MUST all appear in the email body) ===
  • Event date: {ud.get('date', 'TBD')}
  • Budget: {ud.get('budget', 'Flexible')}
{detail_lines}

=== INSTRUCTIONS ===
Write the email body addressed to {contact}. The body MUST naturally include every detail listed under EVENT DETAILS above — do not skip any. Structure it as:
1. Brief intro: who {ud.get('name','I')} am and the event
2. The specifics: weave in ALL the event details (date, guest count, equipment, style, dietary needs, etc. — whatever is listed above)
3. What you're requesting: availability confirmation + pricing/packages for {vtype} services
4. Clear next step / call to action

Tone: professional yet warm. Length: 180–220 words. Do NOT include email headers (From/To/Subject) in the body.

Return ONLY a JSON object — no markdown, no code fences:
{{"subject": "...", "body": "..."}}"""""

        init = to_js({
            "method": "POST",
            "headers": {
                "Content-Type": "application/json",
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
            },
            "body": json.dumps({
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 800,
                "messages": [{"role": "user", "content": prompt}],
            }),
        }, dict_converter=Object.fromEntries)

        resp = await fetch("https://api.anthropic.com/v1/messages", init)
        data = json.loads(await resp.text())
        raw = (data.get("content") or [{}])[0].get("text", "")

        # Strip markdown code fences Claude sometimes adds
        clean = re.sub(r'^```(?:json)?\s*', '', raw.strip())
        clean = re.sub(r'\s*```$', '', clean).strip()

        result = None
        # Try direct parse first
        try:
            result = json.loads(clean)
        except Exception:
            pass

        # Fallback: find the outermost {...} block
        if not result:
            m = re.search(r'\{[\s\S]*\}', clean)
            if m:
                try:
                    result = json.loads(m.group())
                except Exception:
                    pass

        # Ensure result has non-empty subject and body
        if not isinstance(result, dict) or not (result.get("body") or "").strip():
            result = {
                "subject": result.get("subject", f"Booking Inquiry — {vname}") if isinstance(result, dict) else f"Booking Inquiry — {vname}",
                "body": raw,
            }

        return json_resp({"subject": result.get("subject", f"Booking Inquiry — {vname}"), "body": result.get("body", raw)})
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
