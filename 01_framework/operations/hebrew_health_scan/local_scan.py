#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
local_scan.py  —  the FULLY-LOCAL, fully-autonomous Hebrew Health Scan (TASK-381).

Why this exists (owner ruling 2026-07-01): the CLOUD routine could never work — its
environment's HTTPS egress proxy blocks every .co.il domain (ynet/mako/walla/israelhayom/
n12/clalit/maccabi4u/efsharibari + all food blogs return 403). It therefore read nothing,
learned nothing, and (separately) couldn't hand keepers to the local applier (git push 403s,
and the Notion write didn't land headless). This machine reaches .co.il fine, so the WHOLE
loop now runs here — no cloud, no Notion, no human trigger:

  1. Invoke headless `claude` (already logged-in; no API key needed) with WebSearch + WebFetch
     to READ 1-2 real Israeli health articles and emit register keepers as a JSON array file.
     Claude holds the no-harvest firewall (technique described, never phrasing copied).
  2. Run those keepers through the deterministic no-harvest firewall (apply_scan_keepers).
  3. Append survivors to content_voice/tom_bari_voice/9_israeli_food_blog_research.md (§6) — the
     canonical register-calibration file the Content Agent loads when it writes (charter: file 9
     stays register-calibration-only). Loop closed to the writer.
  4. git commit the change locally.

Schedule this daily via a Windows Scheduled Task (see register_local_scan_task.ps1). It replaces
the old cloud routine + Notion + drain_and_apply chain for the reading/applying job.

Usage:
  python local_scan.py                 # real run (reads web, writes 2b, commits)
  python local_scan.py --dry-run       # read + firewall + write 2b, but NO git commit
  python local_scan.py --no-web        # skip the claude/web read; just firewall an existing keepers file
  python local_scan.py --selftest      # offline wiring check (mock keepers -> firewall -> temp file)
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[2]
VOICE_FILE = REPO_ROOT / "content_voice" / "tom_bari_voice" / "9_israeli_food_blog_research.md"
SCANS = HERE / "daily_scans"
LOG = SCANS / "local_scan_log.txt"
MODEL = "claude-sonnet-4-6"
CLAUDE_TIMEOUT = 600  # seconds

sys.path.insert(0, str(HERE))
import apply_scan_keepers as ASK  # noqa: E402


def log(msg, stamp):
    line = "[%s] %s" % (stamp, msg)
    print(line)
    try:
        SCANS.mkdir(parents=True, exist_ok=True)
        with open(LOG, "a", encoding="utf-8") as fh:
            fh.write(line + "\n")
    except Exception:
        pass


def scan_prompt(date, out_path):
    """The reading brief. Claude reads real Israeli health writing and writes a JSON array of
    Lane-A register keepers to out_path. No Notion, no consumer copy, no scores, no phrasing copied."""
    return f"""You are Bari's Hebrew Health Scan — a daily reader of Israeli health/nutrition writing whose ONLY job is to learn natural Hebrew REGISTER so Bari's Content Agent writes better Hebrew. Today is {date}.

Read the BODY of 1-2 real Israeli health articles (LEAD WITH A VOICE source — this is where the good Hebrew is), extract EMULATE/AVOID register TECHNIQUE, and WRITE THE KEEPERS as a JSON array to this exact file path using the Write tool: {out_path}

SOURCES (voice — read one, rotate desks day to day): ynet.co.il/wellness (a specific /wellness/article/<id>) · mako.co.il health (a specific Article-*.htm) · israelhayom.co.il/news/health · n12.co.il · walla.co.il · an Israeli food/nutrition blog. These load fine from here. Use WebSearch with a site: query to get a DIRECT article URL, then WebFetch it and confirm several Hebrew paragraphs of real body (not a cards/index page). If one won't load, try another. Do NOT read a static gov/HMO guidance page for the voice lesson.

NON-NEGOTIABLE FIREWALLS:
1. Register-calibration ONLY. NEVER copy a phrase/sentence into the keeper. Describe the TECHNIQUE ("opens from a familiar buying moment, then pivots to a side-by-side test"), never the words. You may quote at most a SHORT label (a few words) to name a technique. A keeper must contain NO verbatim Hebrew run longer than 7 words and no more than 14 Hebrew words total.
2. Inherit NO data — never copy a number/ingredient/nutrition value. A blog is a pointer, never a value of record. Open Food Facts and external panels are BANNED.
3. No health claims, no consumer copy, no score moves. You only learn register.
4. HARD READ-GATE: a keeper may ONLY come from an article whose BODY you actually read. No body read (403/paywall/cards-only) = no keeper. Never invent coverage.
5. If a genuine read yields no new register lesson, write an empty array []. An honest empty day beats a padded one.

Each keeper object MUST have exactly these keys:
  "Finding": a short title that MUST start with "EMULATE:" or "AVOID:" (technique framing),
  "Detail": the technique described + why it matters (no copied phrasing, no inherited number),
  "Source URL": the exact article URL you read,
  "Tag": one of "ACT" | "WATCH" | "DROP",
  "Bucket": "Content-Hebrew skills",
  "date:Date:start": "{date}"

After writing the file, reply with a one-line summary: how many articles you body-read and how many keepers you wrote. Write NOTHING else to disk. Do not commit."""


def run_claude(date, out_path, stamp):
    prompt = scan_prompt(date, str(out_path).replace("\\", "/"))
    # Prompt goes via STDIN (claude -p reads stdin when no positional prompt) so the long Hebrew
    # text never hits the command line. On Windows the `claude` entry point is a .cmd shim that
    # CreateProcess can't launch directly, so route through cmd.exe.
    flags = ["-p", "--allowedTools", "WebSearch", "WebFetch", "Write", "Read",
             "--permission-mode", "bypassPermissions", "--model", MODEL]
    cmd = (["cmd", "/c", "claude"] + flags) if os.name == "nt" else (["claude"] + flags)
    log("invoking headless claude (model=%s, timeout=%ss) ..." % (MODEL, CLAUDE_TIMEOUT), stamp)
    try:
        r = subprocess.run(cmd, input=prompt, cwd=str(REPO_ROOT), capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=CLAUDE_TIMEOUT)
    except subprocess.TimeoutExpired:
        log("claude timed out after %ss" % CLAUDE_TIMEOUT, stamp)
        return False
    tail = (r.stdout or "").strip().splitlines()[-1:] or [""]
    log("claude exit=%s · %s" % (r.returncode, tail[0][:160]), stamp)
    if r.returncode != 0:
        log("claude stderr: %s" % (r.stderr or "").strip()[:200], stamp)
    return out_path.exists()


def load_keepers(path, stamp):
    try:
        raw = Path(path).read_text(encoding="utf-8")
    except FileNotFoundError:
        log("no keepers file written — treating as empty day", stamp)
        return []
    # tolerate a fenced ```json block or surrounding prose
    m = re.search(r"\[.*\]", raw, re.S)
    text = m.group(0) if m else raw
    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        log("keepers file is not valid JSON (%s) — treating as empty" % e, stamp)
        return []
    if isinstance(data, dict):
        data = [data]
    # per-keeper dedup key so re-reading an article can still surface NEW findings
    for k in data:
        src = (k.get("Source URL") or "").strip()
        find = (k.get("Finding") or "").strip()
        k["url"] = (src + "#" + find[:48]) if (src or find) else ""
    return data


def git_commit(stamp):
    rel_voice = str(VOICE_FILE.relative_to(REPO_ROOT)).replace("\\", "/")
    rel_scans = str(SCANS.relative_to(REPO_ROOT)).replace("\\", "/")
    porc = subprocess.run(["git", "status", "--porcelain", "--", rel_voice, rel_scans],
                          cwd=str(REPO_ROOT), capture_output=True, text=True)
    if not porc.stdout.strip():
        log("git: nothing to commit", stamp)
        return
    subprocess.run(["git", "add", "--", rel_voice, rel_scans], cwd=str(REPO_ROOT), check=True)
    msg = ("TASK-381: Hebrew Health Scan local auto-apply (%s)\n\n"
           "Learned register moves from real Israeli writing, folded into file 2b.\n\n"
           "Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>") % stamp[:10]
    r = subprocess.run(["git", "commit", "-m", msg], cwd=str(REPO_ROOT), capture_output=True, text=True)
    log("git commit: %s" % (r.stdout.strip() or r.stderr.strip())[:160], stamp)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-web", action="store_true", help="skip the claude/web read; firewall an existing keepers file")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--now", default=None)
    a = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    if a.selftest:
        return selftest()

    stamp = a.now or datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")
    date = stamp[:10]
    SCANS.mkdir(parents=True, exist_ok=True)
    kpath = SCANS / ("keepers_%s.json" % date)
    rpath = SCANS / ("results_%s.json" % date)
    ipath = SCANS / "applied_index.json"

    if not a.no_web:
        ok = run_claude(date, kpath, stamp)
        if not ok:
            log("no web read produced — done (nothing learned today)", stamp)
            return 0

    keepers = load_keepers(kpath, stamp)
    log("loaded %d keeper(s) from the read" % len(keepers), stamp)
    if not keepers:
        log("nothing to apply — honest empty day", stamp)
        return 0

    results = ASK.run(str(kpath), str(VOICE_FILE), str(rpath), str(ipath))
    counts = {}
    for r in results:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
    log("verdicts: %s" % (", ".join("%s=%d" % kv for kv in sorted(counts.items())) or "none"), stamp)

    if a.dry_run:
        log("dry-run: skipped git commit", stamp)
    else:
        git_commit(stamp)
    return 0


def selftest():
    stamp = "2026-07-01 00:00:00Z"
    import tempfile
    d = Path(tempfile.mkdtemp())
    kp = d / "keepers.json"
    kp.write_text(json.dumps([
        {"Finding": "EMULATE: investigation-arc opener", "Detail": "Opens from a familiar buying moment then pivots to a side-by-side test; verdict-first.",
         "Source URL": "https://www.ynet.co.il/wellness/article/xxx", "Tag": "WATCH", "Bucket": "Content-Hebrew skills", "date:Date:start": "2026-07-01"},
        {"Finding": "not framed", "Detail": "should be rejected", "Source URL": "https://x", "Tag": "DROP", "Bucket": "Content-Hebrew skills", "date:Date:start": "2026-07-01"},
    ], ensure_ascii=False), encoding="utf-8")
    keepers = load_keepers(kp, stamp)
    assert keepers[0]["url"].startswith("https://www.ynet.co.il"), "dedup url build failed"
    v = [ASK.firewall(k)[0] for k in keepers]
    print("selftest verdicts:", v)
    ok = v == ["APPLY", "REJECT"]
    print("SELFTEST", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
