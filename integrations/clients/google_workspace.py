"""Google Workspace read-only connector — Gmail + Calendar for CC (Tom's Chief of Staff).

For: CC Agent. This is the *personal* layer of the Command Center. It lets CC see Tom's
inbox and calendar so it can surface only what needs him — awaiting-reply mail, time-
sensitive threads, calendar conflicts, missing prep — and draft replies he approves.

POSTURE (owner-decided 2026-06-05):
  - READ-ONLY. Scopes are gmail.readonly + calendar.readonly. This module has no send /
    modify / delete verb. CC can compose draft text to show Tom, but never touches his
    account state. Widening to write requires new scopes AND a new owner decision.
  - LOCAL KEY. The OAuth credential (client secret + refresh token) lives in a single
    JSON file OUTSIDE the repo: ~/.bari/google_token.json (override: $BARI_GOOGLE_TOKEN).
    It is never committed, never pushed, never leaves the laptop. No third party holds it.
  - FULL VISIBILITY, SURFACES LITTLE. CC may read the whole inbox/calendar so it misses
    nothing, but by design shows almost nothing — only what needs Tom.

ZERO install footprint — stdlib only (urllib + http.server for the one-time consent).

One-time setup (Tom runs once; see integrations/clients/google_workspace_SETUP.md):
    python -m integrations.clients.google_workspace --auth --client-secret <downloaded.json>

After that, any agent can:
    from integrations.clients import google_workspace as gw
    if gw.is_connected():
        triage = gw.inbox_triage()      # mail that needs Tom
        day    = gw.calendar_day()      # today's events + conflicts
        status = gw.status()            # one-glance summary for the board

Read-only smoke test once connected:
    python -m integrations.clients.google_workspace
"""
from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any

# ── Config ───────────────────────────────────────────────────────────────────
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/calendar.readonly",
]
TOKEN_URI = "https://oauth2.googleapis.com/token"
AUTH_URI = "https://accounts.google.com/o/oauth2/v2/auth"
GMAIL_API = "https://gmail.googleapis.com/gmail/v1"
CALENDAR_API = "https://www.googleapis.com/calendar/v3"
USER_AGENT = "Bari-CC/1.0 (+chief-of-staff; contact tbarhaim@gmail.com)"
DEFAULT_TIMEOUT = 25


def token_path() -> str:
    """Where the local credential lives — outside the repo, never committed."""
    override = os.environ.get("BARI_GOOGLE_TOKEN")
    if override:
        return override
    return os.path.join(os.path.expanduser("~"), ".bari", "google_token.json")


class GoogleError(Exception):
    """Raised on an unrecoverable Google API / auth failure."""


# ── Credential store ─────────────────────────────────────────────────────────
def _load_store() -> dict | None:
    p = token_path()
    if not os.path.exists(p):
        return None
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return None


def _save_store(store: dict) -> None:
    p = token_path()
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(store, f, indent=2)
    # Best-effort tighten perms (no-op semantics on Windows, real on POSIX).
    try:
        os.chmod(p, 0o600)
    except OSError:
        pass


def is_connected() -> bool:
    """True if a usable credential (client + refresh token) is on disk."""
    s = _load_store()
    return bool(s and s.get("client_id") and s.get("client_secret") and s.get("refresh_token"))


# ── HTTP (read GET + the two OAuth POSTs this module needs) ───────────────────
def _post_form(url: str, data: dict[str, str], timeout: int = DEFAULT_TIMEOUT) -> dict:
    body = urllib.parse.urlencode(data).encode("utf-8")
    req = urllib.request.Request(
        url, data=body, method="POST",
        headers={"User-Agent": USER_AGENT, "Content-Type": "application/x-www-form-urlencoded"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8", errors="replace"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")
        raise GoogleError(f"OAuth POST {e.code}: {detail[:300]}") from e
    except urllib.error.URLError as e:
        raise GoogleError(f"network error reaching {url}: {e.reason}") from e


# in-memory access-token cache: (token, expires_at_epoch)
_ACCESS: tuple[str, float] | None = None


def _access_token() -> str:
    """Exchange the stored refresh token for a short-lived access token (cached)."""
    global _ACCESS
    if _ACCESS and _ACCESS[1] - 60 > time.time():
        return _ACCESS[0]
    store = _load_store()
    if not store:
        raise GoogleError(
            "Not connected. Run: python -m integrations.clients.google_workspace "
            "--auth --client-secret <downloaded.json>  (see google_workspace_SETUP.md)"
        )
    resp = _post_form(TOKEN_URI, {
        "client_id": store["client_id"],
        "client_secret": store["client_secret"],
        "refresh_token": store["refresh_token"],
        "grant_type": "refresh_token",
    })
    tok = resp.get("access_token")
    if not tok:
        raise GoogleError(f"no access_token in refresh response: {resp}")
    _ACCESS = (tok, time.time() + int(resp.get("expires_in", 3600)))
    return tok


def _api_get(url: str, params: dict[str, Any] | None = None, timeout: int = DEFAULT_TIMEOUT,
             retries: int = 2, backoff: float = 1.5) -> dict:
    """Authorized read-only GET against a Google API. Polite retry on 429/5xx."""
    if params:
        # doseq=True so list-valued params (e.g. metadataHeaders=[From,Subject,Date])
        # are emitted as repeated query keys, which is what the Google APIs require —
        # without it the list is stringified and silently ignored (empty headers).
        url = f"{url}?{urllib.parse.urlencode(params, doseq=True)}"
    last: Exception | None = None
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": USER_AGENT,
                "Authorization": f"Bearer {_access_token()}",
                "Accept": "application/json",
            })
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read().decode("utf-8", errors="replace"))
        except urllib.error.HTTPError as e:
            last = GoogleError(f"HTTP {e.code} for {url}: {e.read().decode('utf-8', 'replace')[:200]}")
            if e.code in (429, 500, 502, 503, 504) and attempt < retries:
                time.sleep(backoff * (attempt + 1))
                continue
            raise last
        except urllib.error.URLError as e:
            last = GoogleError(f"network error for {url}: {e.reason}")
            if attempt < retries:
                time.sleep(backoff * (attempt + 1))
                continue
            raise last
    raise last or GoogleError(f"unknown error for {url}")


# ── Gmail (read-only) ────────────────────────────────────────────────────────
@dataclass
class Mail:
    id: str
    thread_id: str
    sender: str
    subject: str
    date: str
    snippet: str
    unread: bool
    labels: list[str] = field(default_factory=list)

    def as_dict(self) -> dict:
        return self.__dict__


def _header(payload: dict, name: str) -> str:
    for h in payload.get("headers", []):
        if h.get("name", "").lower() == name.lower():
            return h.get("value", "")
    return ""


def list_message_ids(query: str = "", max_results: int = 25) -> list[str]:
    """Gmail search → message ids. `query` is standard Gmail search syntax."""
    params = {"maxResults": str(max_results)}
    if query:
        params["q"] = query
    data = _api_get(f"{GMAIL_API}/users/me/messages", params)
    return [m["id"] for m in data.get("messages", [])]


def get_message(msg_id: str) -> Mail:
    """Fetch one message as metadata (headers + snippet) — body is NOT pulled."""
    data = _api_get(
        f"{GMAIL_API}/users/me/messages/{msg_id}",
        {"format": "metadata", "metadataHeaders": ["From", "Subject", "Date"]},
    )
    payload = data.get("payload", {})
    labels = data.get("labelIds", [])
    return Mail(
        id=data.get("id", msg_id),
        thread_id=data.get("threadId", ""),
        sender=_header(payload, "From"),
        subject=_header(payload, "Subject"),
        date=_header(payload, "Date"),
        snippet=data.get("snippet", ""),
        unread="UNREAD" in labels,
        labels=labels,
    )


def messages(query: str = "", max_results: int = 25) -> list[Mail]:
    """Search + hydrate to Mail objects (metadata only)."""
    return [get_message(mid) for mid in list_message_ids(query, max_results)]


def inbox_triage(max_results: int = 12) -> dict:
    """What needs Tom — driven by HIS curation, not a heuristic.

    Owner decision (2026-06-05): the inbox surfaces ONLY mail Tom has starred in
    Gmail. Starring is his inclusion signal; un-starring removes it at the source.
    This is clean and controllable — no guessing what "needs a reply," no garbage.
    Cheap too: starred is a small set, so hydration is fast.

    starred / needs_reply : the same starred list (needs_reply kept for the board's
                            existing field name; both point at Tom's flagged mail).
    """
    ids = list_message_ids("is:starred", max_results=max_results)
    starred = [get_message(mid) for mid in ids]
    rows = [m.as_dict() for m in starred]
    return {
        "connected": True,
        "starred": rows,
        "needs_reply": rows,                 # board reads needs_reply; same data
        "starred_count": len(ids),
        "needs_reply_count": len(ids),
    }


# ── Calendar (read-only) ─────────────────────────────────────────────────────
@dataclass
class Event:
    id: str
    summary: str
    start: str
    end: str
    location: str
    attendees: int
    description: str
    all_day: bool

    def as_dict(self) -> dict:
        return self.__dict__


def _evt_time(node: dict) -> str:
    return node.get("dateTime") or node.get("date") or ""


def list_events(time_min: str, time_max: str, calendar_id: str = "primary",
                max_results: int = 50) -> list[Event]:
    """Events in [time_min, time_max] (RFC3339). Read-only."""
    data = _api_get(f"{CALENDAR_API}/calendars/{urllib.parse.quote(calendar_id)}/events", {
        "timeMin": time_min, "timeMax": time_max,
        "singleEvents": "true", "orderBy": "startTime",
        "maxResults": str(max_results),
    })
    out: list[Event] = []
    for e in data.get("items", []):
        start_node = e.get("start", {})
        out.append(Event(
            id=e.get("id", ""),
            summary=e.get("summary", "(no title)"),
            start=_evt_time(start_node),
            end=_evt_time(e.get("end", {})),
            location=e.get("location", ""),
            attendees=len(e.get("attendees", []) or []),
            description=e.get("description", ""),
            all_day="date" in start_node,
        ))
    return out


def _conflicts(events: list[Event]) -> list[tuple[str, str]]:
    """Pairs of timed events whose intervals overlap."""
    timed = [e for e in events if not e.all_day and e.start and e.end]
    out: list[tuple[str, str]] = []
    for i in range(len(timed)):
        for j in range(i + 1, len(timed)):
            if timed[i].end > timed[j].start and timed[i].start < timed[j].end:
                out.append((timed[i].summary, timed[j].summary))
    return out


def calendar_day(days: int = 1) -> dict:
    """Today (or next `days`) — events, conflicts, and meetings missing prep."""
    now = datetime.now(timezone.utc)
    start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    evts = list_events(start.isoformat(), (start + timedelta(days=days)).isoformat())
    no_prep = [e.summary for e in evts
               if e.attendees >= 2 and not e.all_day and not e.description.strip()]
    return {
        "connected": True,
        "events": [e.as_dict() for e in evts],
        "count": len(evts),
        "conflicts": _conflicts(evts),
        "no_prep": no_prep,
    }


# ── One-glance status for the board ──────────────────────────────────────────
def status() -> dict:
    """Compact summary CC can render at the top of the Command Center.

    Degrades gracefully: if not connected, returns {connected: False} with a hint
    instead of raising, so the board never crashes on a missing credential."""
    if not is_connected():
        return {
            "connected": False,
            "hint": "Gmail/Calendar not linked yet. See integrations/clients/"
                    "google_workspace_SETUP.md (one-time, ~15 min, key stays local).",
        }
    try:
        tri = inbox_triage()
        day = calendar_day()
        next_evt = next((e for e in day["events"] if not e["all_day"]), None)
        return {
            "connected": True,
            "needs_reply_count": tri["needs_reply_count"],
            "starred_count": len(tri["starred"]),
            "events_today": day["count"],
            "conflicts": day["conflicts"],
            "no_prep": day["no_prep"],
            "next_event": next_evt,
        }
    except GoogleError as e:
        return {"connected": True, "error": str(e)}


# ── One-time OAuth consent (loopback flow, stdlib only) ───────────────────────
def _run_oauth_flow(client_id: str, client_secret: str, port: int = 8765) -> dict:
    """Installed-app loopback flow: open browser → consent → capture code locally →
    exchange for a refresh token. The credential never leaves this machine."""
    import http.server
    import webbrowser

    redirect_uri = f"http://localhost:{port}/"
    auth_url = f"{AUTH_URI}?" + urllib.parse.urlencode({
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": " ".join(SCOPES),
        "access_type": "offline",      # ask for a refresh token
        "prompt": "consent",           # force refresh-token issuance every time
    })

    holder: dict[str, str] = {}

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):  # noqa: N802
            q = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(q)
            holder["code"] = (params.get("code") or [""])[0]
            holder["error"] = (params.get("error") or [""])[0]
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            msg = ("CC is linked. You can close this tab and return to the terminal."
                   if holder.get("code") else
                   f"Authorization failed: {holder.get('error')}")
            self.wfile.write(f"<html><body style='font-family:sans-serif'>{msg}</body></html>"
                             .encode("utf-8"))

        def log_message(self, *args):  # silence the default stderr logging
            return

    server = http.server.HTTPServer(("localhost", port), Handler)
    print(f"\nOpening your browser to authorize (read-only Gmail + Calendar)...")
    print(f"If it doesn't open, paste this URL:\n  {auth_url}\n")
    webbrowser.open(auth_url)
    server.handle_request()   # blocks until Google redirects back once
    server.server_close()

    if holder.get("error") or not holder.get("code"):
        raise GoogleError(f"consent not granted: {holder.get('error') or 'no code returned'}")

    resp = _post_form(TOKEN_URI, {
        "client_id": client_id,
        "client_secret": client_secret,
        "code": holder["code"],
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
    })
    refresh = resp.get("refresh_token")
    if not refresh:
        raise GoogleError(
            "Google did not return a refresh_token. Revoke prior access at "
            "myaccount.google.com/permissions and re-run (prompt=consent forces it)."
        )
    return {
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh,
        "scopes": SCOPES,
        "linked_at": datetime.now(timezone.utc).isoformat(),
    }


def _auth_cli(client_secret_file: str, port: int = 8765) -> None:
    """Read a Google 'Desktop app' client-secret JSON, run consent, save the token."""
    with open(client_secret_file, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    node = cfg.get("installed") or cfg.get("web") or cfg
    cid, csecret = node.get("client_id"), node.get("client_secret")
    if not (cid and csecret):
        raise GoogleError(f"{client_secret_file} is not a valid OAuth client-secret JSON "
                          "(expected an 'installed' Desktop-app client).")
    store = _run_oauth_flow(cid, csecret, port=port)
    _save_store(store)
    print(f"\n✓ Linked. Credential saved (local only) at: {token_path()}")
    print("  Smoke test:  python -m integrations.clients.google_workspace")


# ── CLI ──────────────────────────────────────────────────────────────────────
def _smoke() -> None:
    if not is_connected():
        print(json.dumps(status(), indent=2, ensure_ascii=False))
        return
    print("Gmail + Calendar linked — read-only. One-glance status:\n")
    print(json.dumps(status(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(description="Google Workspace read-only connector for CC")
    ap.add_argument("--auth", action="store_true", help="run the one-time consent flow")
    ap.add_argument("--client-secret", help="path to the downloaded Desktop-app client secret JSON")
    ap.add_argument("--port", type=int, default=8765, help="loopback port for the consent redirect")
    args = ap.parse_args()

    if args.auth:
        if not args.client_secret:
            raise SystemExit("--auth requires --client-secret <downloaded.json>")
        _auth_cli(args.client_secret, port=args.port)
    else:
        _smoke()
