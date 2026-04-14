import json
import hmac
import hashlib
import base64
import time
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

    return await serve_asset(env, request, path)
