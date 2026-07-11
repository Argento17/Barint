#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bari_daily_digest.py  —  the FULLY-LOCAL Bari Daily Digest (consolidates the three former cloud
routines: BSIP2 Corroboration Ledger + Project Comp + Weekly Cross-Routine Synthesis).

Why local + why the Notion REST API (owner-verified 2026-07-09): the cloud routine delivered
NOTHING — a headless cloud run sent no email AND wrote nothing to Notion, because non-interactive
runs cannot drive the claude.ai MCP connectors (Gmail/Notion). Owner then chose: skip email, write
to Notion. So this runs locally and writes to the 'Bari Routine Log' via the **Notion REST API with
an integration token** (a plain authenticated HTTPS call that works headless) — NOT the MCP
connector. Same philosophy that made the Hebrew Health Scan local: bypass the flaky connector.

Flow:
  1. Headless `claude` (already logged-in; no API key) reads the web + repo and writes a STRUCTURED
     JSON array of actionable digest rows to rows_<date>.json (Claude does NOT touch Notion/git).
     Categories: (1) BSIP2 potential improvements  (2) blog materials  (3) contemporary news to
     write (like of-poultry-report)  (4) guides that could be useful.
  2. Python posts each row to the Notion 'Bari Routine Log' via the REST API (schema discovered at
     runtime so a property-type mismatch can't break it), and archives a local Markdown copy.

ANTI-REPETITION (owner: "crucial it doesn't repeat resources every day") is baked into the prompt as
THREE memory-free layers: deterministic day-of-year rotation of the source universe + watch-terms +
evidence roster; a hard freshness gate (only NEW dated developments qualify; evergreen auto-dropped);
best-effort self-dedup. No cross-run memory required.

Schedule daily 06:00 local via register_daily_digest_task.ps1.

NOTION INTEGRATION TOKEN read from, in order:
  1. env var  BARI_NOTION_TOKEN
  2. local file  01_framework/operations/comp/.daily_digest_secret   (gitignored; token only)
Create at notion.so/my-integrations (internal integration), then SHARE the 'Bari Routine Log'
database with that integration (Notion: ... -> Connections -> add your integration). Token starts
'secret_' or 'ntn_'.

Usage:
  python bari_daily_digest.py              # real run: read web -> rows.json -> post to Notion -> archive
  python bari_daily_digest.py --dry-run    # build rows + archive, do NOT post to Notion
  python bari_daily_digest.py --no-web      # skip the claude read; post/archive an existing rows file
  python bari_daily_digest.py --selftest    # offline wiring check (prompt builds, token + schema map resolve)
"""

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[2]
OUT = HERE / "daily_digests"
LOG = OUT / "daily_digest_log.txt"
SECRET_FILE = HERE / ".daily_digest_secret"

MODEL = "claude-sonnet-5"
CLAUDE_TIMEOUT = 900  # seconds — 4 categories of web work

# Notion 'Bari Routine Log' (from scheduled_routines_state memory): database_id for the REST API.
NOTION_DB_ID = "fb50a533316440c4a571f9bb32206e48"
NOTION_VERSION = "2022-06-28"
NOTION_API = "https://api.notion.com/v1"


def log(msg, stamp):
    line = "[%s] %s" % (stamp, msg)
    print(line)
    try:
        OUT.mkdir(parents=True, exist_ok=True)
        with open(LOG, "a", encoding="utf-8") as fh:
            fh.write(line + "\n")
    except Exception:
        pass


# ----------------------------------------------------------------------------- prompt

def digest_prompt(date, doy, rows_path):
    """Claude reads web+repo and writes a JSON ARRAY of actionable digest rows to rows_path.
    It does NOT touch Notion/git/email — the Python wrapper posts the rows to Notion."""
    return f"""You are the **Bari Daily Digest** — Bari's single daily intelligence routine, running LOCALLY on the owner's machine on the real working checkout at {REPO_ROOT}. Bari is a Hebrew consumer food-scoring product. Today is {date} (day-of-year N={doy}, Asia/Jerusalem). You are an INTELLIGENCE LAYER: you PROPOSE, you never ship. You change NOTHING — no scores, no registry, no copy, no git. Your ONLY write is the rows file below.

DELIVER: write a JSON ARRAY of the ACTIONABLE items (Tag ACT or WATCH only) using the Write tool to exactly this path: {rows_path}
Do NOT email, do NOT touch Notion, do NOT run git — a local wrapper posts these rows to Notion. After writing, reply with a one-line summary (how many rows, by category).

Produce at most 2-4 of the STRONGEST items PER CATEGORY across the four categories below. An honest thin day beats a padded one: if a category has nothing that passes the gates, include NO rows for it; if the whole day is quiet, write []. Never manufacture filler.

Each array element = ONE object with EXACTLY these keys:
  "Finding": short title (<=90 chars). For a Category-3 news item, prefix with "News: ".
  "Bucket": one of "Scoring/methodology" (Cat 1) | "Editorial/content" (Cat 2 AND Cat 3) | "Category opportunity" (Cat 4).
  "Tag": "ACT" or "WATCH".
  "Owner": one of nutrition-agent | product-agent | content-agent | marketing-agent | data-agent | research-agent | orchestrator.
  "Source URL": the primary source URL.
  "Detail": 1-4 sentences = the finding + the source's PUBLICATION DATE + why it matters to Bari + (for any creator/competitor/media item) credibility-vs-discourse + evidence strength. Self-contained.
  "Date": "{date}".

== ANTI-REPETITION (CRITICAL — the owner's #1 requirement: never surface the same resources/topics day after day) ==
THREE layers, strongest first:
1) DETERMINISTIC ROTATION (primary). Index entries in 01_framework/operations/comp/source_registry_v1.yaml and topic groups in 01_framework/operations/comp/project_comp_watch_terms_v1.yaml. Go DEEP on the ~1/7 slice whose zero-based index i satisfies i mod 7 == {doy} mod 7 — a DIFFERENT slice each day, whole universe across a week. Glance at always-on fast-movers (direct competitors + top health media) but LEAD with and pull most items from today's slice. Same i mod 7 == {doy} mod 7 rotation on the evidence-registry roster for Category 1.
2) HARD FRESHNESS GATE (anti-evergreen). An item qualifies ONLY with a VERIFIABLE publication/update DATE inside the window (Cat 2/3: last ~24-36h; Cat 1: last ~30 days; Cat 4: a genuinely new gap). A standing topic is NOT an item: "seed oils are debated", "UPF is controversial", "Yuka oversimplifies", "GLP-1 is trending" are NOT findings — only a NEW DATED development is. No date -> DROP. If all you can say is what was already true last week, it is not today's signal.
3) SELF-DEDUP (bonus). Skim daily_digests/ for recent digests/rows if present; do not repeat an item already sent. If absent, layers 1-2 still stand alone.
Acceptance test before writing each row: could this exact item have been sent verbatim a week ago? If yes, CUT it.

== STEP 1 — GROUND IN REPO STATE (read-only, BEFORE web; dedupe against shipped work) ==
- 03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md — established evidence tiers (EV-###/BEV-###): tier (A/B/C) + directional verdict. Roster for Category 1.
- 01_framework/operations/comp/source_registry_v1.yaml + project_comp_watch_terms_v1.yaml — source universe + Hebrew/English watch terms (index for rotation).
- bari-web/src/app/blog/* + bari-web/src/data/blog/* — existing blog slugs (bread-*, food-dyes, hummus, lechem, milk-analysis, shemen-zayit, sugar-alcohols, yogurt). Don't re-propose one (Cat 2).
- bari-web/src/data/news/news-index.json + bari-web/src/app/news/* — published news; 'of-poultry-report' is the Cat-3 EXEMPLAR (a claims-audit: claim-status cards, verified/misleading/unproven). Don't re-propose one.
- bari-web/src/app/madrichim/* — existing guides (e.g. yogurt-glp1). Don't re-propose one (Cat 4).
- tasks/TASK-*.md titles/status — don't propose something already in flight.
Missing path -> note and continue.

== STEP 2 — WEB SWEEP (public pages; verify each source's DATE) ==
WebSearch/WebFetch over the window, LED by today's rotation slice. This machine reaches Israeli (.co.il) sites directly — read ynet/mako/n12/walla/israelhayom + IL Ministry of Health where relevant, plus PubMed/journals/EFSA/FDA/WHO for Category 1. NEVER use Open Food Facts (OFF) — any field, ever (project-wide hard ban). Public pages only. Keep credibility vs discourse SEPARATE — reach is never reliability.

== THE FOUR CATEGORIES (source the rows above) ==
1) BSIP2 potential improvements — within today's rotation slice of the evidence roster, where does fresh (~30d) literature/regulation CORROBORATE / CONTRADICT / REFINE an established tier or suggest a scoring-dimension improvement? PROPOSAL ONLY — never move a score/edit registry; only LABEL-DERIVABLE signals qualify; a CONTRADICTS is a flag for an owner-gated D6/D7 Nutrition task. Owner nutrition-agent. ACT only for a High-evidence CONTRADICTS.
2) Blog materials — a NEW dated development worth an evergreen /blog deep-dive (analysis voice), a fresh angle not already a slug. Signal not evidence. Owner content-agent.
3) Contemporary news to write — a time-sensitive item (dated last day or two) for the /news claims-audit format like 'of-poultry-report', not already published. Never assert a claim as true. Owner content-agent.
4) Guides that could be useful — a durable /madrichim "how to pick X" guide (attribute-level, tiered, like GLP-1/yogurt) that doesn't exist yet and serves real IL intent. Owner product-agent. Anti-overbuild: prefer a guide over a new category.

== FIREWALLS (violating any invalidates the run) ==
- ANTI-REPETITION is a firewall: no evergreen restatement, no undated item; today's slice must differ from other days.
- PROPOSE ONLY: never move a score, edit registry/KB/tasks, author final consumer copy, or run git. The ONLY file you write is {rows_path}.
- OFF BAN: never cite/use Open Food Facts, ever.
- Signal not evidence: never assert a circulating claim as fact; a consumer claim is a two-gate proposal to Content+Nutrition.
- No data inheritance: never copy a competitor/OFF number or ingredient as fact.
- No hallucinated coverage: anything you didn't open is "not checked"/"inaccessible", never "no update". If WebSearch/WebFetch are unavailable, write [] and stop — never fabricate.
"""


# ----------------------------------------------------------------------------- claude

def run_claude(date, doy, rows_path, stamp):
    prompt = digest_prompt(date, doy, str(rows_path).replace("\\", "/"))
    flags = ["-p", "--allowedTools", "WebSearch", "WebFetch", "Write", "Read", "Grep", "Glob", "Bash",
             "--permission-mode", "bypassPermissions", "--model", MODEL]
    cmd = (["cmd", "/c", "claude"] + flags) if os.name == "nt" else (["claude"] + flags)
    so_path = OUT / "claude_stdout.txt"
    se_path = OUT / "claude_stderr.txt"
    log("invoking headless claude (model=%s, timeout=%ss, pid=%s) ..." % (MODEL, CLAUDE_TIMEOUT, os.getpid()), stamp)
    try:
        with so_path.open("w", encoding="utf-8", errors="replace") as so, \
             se_path.open("w", encoding="utf-8", errors="replace") as se:
            r = subprocess.run(cmd, input=prompt, cwd=str(REPO_ROOT), stdout=so, stderr=se,
                               text=True, encoding="utf-8", errors="replace", timeout=CLAUDE_TIMEOUT)
    except subprocess.TimeoutExpired:
        log("claude timed out after %ss" % CLAUDE_TIMEOUT, stamp)
        return False
    out_txt = so_path.read_text(encoding="utf-8", errors="replace") if so_path.exists() else ""
    tail = out_txt.strip().splitlines()[-1:] or [""]
    log("claude exit=%s · %s" % (r.returncode, tail[0][:160]), stamp)
    if r.returncode != 0:
        err_txt = se_path.read_text(encoding="utf-8", errors="replace") if se_path.exists() else ""
        log("claude stderr: %s" % err_txt.strip()[:300], stamp)
    return rows_path.exists()


def load_rows(path, stamp):
    try:
        raw = Path(path).read_text(encoding="utf-8")
    except FileNotFoundError:
        log("no rows file written — treating as empty day", stamp)
        return []
    m = re.search(r"\[.*\]", raw, re.S)
    text = m.group(0) if m else raw
    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        log("rows file is not valid JSON (%s) — treating as empty" % e, stamp)
        return []
    if isinstance(data, dict):
        data = [data]
    return [r for r in data if isinstance(r, dict) and (r.get("Finding") or "").strip()]


# ----------------------------------------------------------------------------- notion REST

def get_secret():
    v = os.environ.get("BARI_NOTION_TOKEN")
    if v and v.strip():
        return v.strip()
    if SECRET_FILE.exists():
        t = SECRET_FILE.read_text(encoding="utf-8").strip()
        if t:
            return t
    return None


def _notion_req(method, url, token, payload=None):
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", "Bearer " + token)
    req.add_header("Notion-Version", NOTION_VERSION)
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def _prop_value(prop_type, value):
    """Build a Notion property payload matching the DB's actual type for this property."""
    if value is None or value == "":
        return None
    if prop_type == "title":
        return {"title": [{"text": {"content": str(value)[:1900]}}]}
    if prop_type == "rich_text":
        return {"rich_text": [{"text": {"content": str(value)[:1900]}}]}
    if prop_type == "select":
        return {"select": {"name": str(value)[:100]}}
    if prop_type == "multi_select":
        return {"multi_select": [{"name": str(value)[:100]}]}
    if prop_type == "url":
        return {"url": str(value)}
    if prop_type == "date":
        return {"date": {"start": str(value)}}
    if prop_type == "status":
        return {"status": {"name": str(value)[:100]}}
    return None  # unsupported type -> skip


def post_rows_to_notion(rows, stamp):
    token = get_secret()
    if not token:
        log("NO Notion token (set env BARI_NOTION_TOKEN or write the integration token to %s) — "
            "rows NOT posted; archived locally only" % SECRET_FILE.name, stamp)
        return 0
    # 1) discover the DB schema so we match property NAMES + TYPES exactly (no brittle assumptions).
    try:
        db = _notion_req("GET", "%s/databases/%s" % (NOTION_API, NOTION_DB_ID), token)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")[:300]
        log("Notion DB fetch FAILED (%s): %s — is the integration shared with the 'Bari Routine "
            "Log' database?" % (e.code, body), stamp)
        return 0
    except Exception as e:
        log("Notion DB fetch error: %s: %s" % (type(e).__name__, str(e)[:200]), stamp)
        return 0
    schema = {name: p.get("type") for name, p in (db.get("properties") or {}).items()}
    # case-insensitive name lookup so 'Source URL' / 'source url' both resolve
    lower = {k.lower(): k for k in schema}

    def resolve(field):
        return lower.get(field.lower())

    posted = 0
    for row in rows:
        props = {}
        for field, value in row.items():
            pname = resolve(field)
            if not pname:
                continue  # field not in this DB -> skip silently
            pv = _prop_value(schema[pname], value)
            if pv is not None:
                props[pname] = pv
        # always stamp Routine + Status if those columns exist and the row didn't set them
        for extra_field, extra_val in (("Routine", "Bari Daily Digest"), ("Status", "New")):
            pname = resolve(extra_field)
            if pname and pname not in props:
                pv = _prop_value(schema[pname], extra_val)
                if pv is not None:
                    props[pname] = pv
        payload = {"parent": {"database_id": NOTION_DB_ID}, "properties": props}
        try:
            _notion_req("POST", "%s/pages" % NOTION_API, token, payload)
            posted += 1
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", "replace")[:300]
            log("Notion row FAILED (%s) for %r: %s" % (e.code, (row.get("Finding") or "")[:60], body), stamp)
        except Exception as e:
            log("Notion row error for %r: %s" % ((row.get("Finding") or "")[:60], str(e)[:200]), stamp)
    log("Notion: posted %d/%d row(s) to 'Bari Routine Log'" % (posted, len(rows)), stamp)
    return posted


# ----------------------------------------------------------------------------- archive

def archive_markdown(rows, date, stamp):
    lines = ["# Bari Daily Digest — %s" % date, ""]
    if not rows:
        lines.append("_Quiet day — no actionable items cleared the freshness + rotation gates._")
    else:
        by_bucket = {}
        for r in rows:
            by_bucket.setdefault(r.get("Bucket", "Other"), []).append(r)
        for bucket, items in by_bucket.items():
            lines.append("## %s" % bucket)
            for r in items:
                lines.append("- **%s** — %s [%s, %s] — %s" % (
                    r.get("Finding", ""), r.get("Detail", ""), r.get("Tag", ""),
                    r.get("Owner", ""), r.get("Source URL", "")))
            lines.append("")
    path = OUT / ("%s.md" % date)
    path.write_text("\n".join(lines), encoding="utf-8")
    log("archived local copy -> %s" % path.name, stamp)


# ----------------------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="build rows + archive, do NOT post to Notion")
    ap.add_argument("--no-web", action="store_true", help="skip the claude read; post/archive an existing rows file")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--now", default=None)
    a = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    # Task Scheduler (no console) makes the nested `claude` Node CLI raise CTRL_C/CTRL_BREAK that would
    # kill THIS process (0xC000013A) mid-read. Ignore those so `claude` runs to completion (from local_scan.py).
    import signal
    for _sig in ("SIGINT", "SIGBREAK"):
        try:
            signal.signal(getattr(signal, _sig), signal.SIG_IGN)
        except (AttributeError, ValueError, OSError):
            pass
    if a.selftest:
        return selftest()

    stamp = a.now or datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")
    date = stamp[:10]
    doy = datetime.strptime(date, "%Y-%m-%d").timetuple().tm_yday
    OUT.mkdir(parents=True, exist_ok=True)
    rows_path = OUT / ("rows_%s.json" % date)

    if not a.no_web:
        ok = run_claude(date, doy, rows_path, stamp)
        if not ok:
            log("no rows file produced — aborting", stamp)
            return 1

    rows = load_rows(rows_path, stamp)
    log("loaded %d actionable row(s), day-of-year %d" % (len(rows), doy), stamp)
    archive_markdown(rows, date, stamp)

    if a.dry_run:
        log("dry-run: rows archived, NOT posted to Notion", stamp)
    elif rows:
        post_rows_to_notion(rows, stamp)
    else:
        log("empty day: nothing to post to Notion", stamp)
    return 0


def selftest():
    stamp = "2026-07-09 00:00:00Z"
    p = digest_prompt("2026-07-09", 190, str(OUT / "rows_2026-07-09.json"))
    assert "i mod 7 == 190 mod 7" in p, "rotation not injected"
    assert "2026-07-09" in p and "Open Food Facts" in p and "PROPOSE ONLY" in p, "date/firewalls missing"
    # property builder covers the schema types we expect on the DB
    assert _prop_value("title", "x")["title"][0]["text"]["content"] == "x"
    assert _prop_value("select", "ACT")["select"]["name"] == "ACT"
    assert _prop_value("url", "")  is None and _prop_value("date", "2026-07-09")["date"]["start"] == "2026-07-09"
    has_token = get_secret() is not None
    print("selftest: prompt OK · rotation-injected OK · firewalls OK · prop-builder OK · notion-token-present=%s" % has_token)
    print("SELFTEST PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
