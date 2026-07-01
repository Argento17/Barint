#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
apply_scan_keepers.py  —  the "implement" half of the Hebrew Health Scan loop (TASK-381).

The cloud routine (extractor) READS Israeli health articles and proposes Lane-A register
keepers into the Notion "Bari Routine Log". This script is the APPLY step that the routine
itself cannot do (cloud routines here are read-only / cannot commit to the repo). It takes
those keepers, runs a DETERMINISTIC no-harvest firewall, and folds the surviving register
lessons into the Content Agent's voice corpus (file 9) so the next Hebrew it writes is better.

It is transport-agnostic on purpose: it does NOT talk to Notion. The caller (the orchestrator
via the Notion MCP, or a future token-based fetcher) hands it the rows as JSON on --in, and it
emits per-row verdicts on --out so the caller can flip Notion Status (Actioned / Dropped).
That keeps the FIREWALL logic deterministic, testable, and free of credentials.

THE FIREWALL (Lane A = register technique only, never harvested phrasing — file 9 firewall):
  Each keeper gets one of three verdicts:
    APPLY  — clean technique note; appended to file 9.
    HOLD   — borderline; left as Status=New for a human / Adversarial QA (preserves the
             original calibration caution for edge cases instead of silently applying).
    REJECT — clear harvest/format violation; caller marks it Dropped (with reason).
  Rules (deterministic):
    F1  Bucket must be "Content-Hebrew skills"  -> else SKIP (Lane B/other; not file 9's job).
    F2  Finding must be framed as technique: starts with EMULATE or AVOID -> else HOLD.
    F3  No verbatim Hebrew run longer than MAX_HEB_RUN words -> else REJECT.
        (A harvested *sentence* for reuse is the risk; a short quoted title/label as the NAME
         of a technique is citation, backed by the Source URL. Sentences run 8+ words.)
    F4  Total Hebrew words across the keeper <= MAX_HEB_TOTAL -> else HOLD (too much Hebrew
        for a pure technique note; a human should look).
  Source URL is provenance only — it is NEVER a data source (OFF ban + file 9 firewall).

Usage:
  python apply_scan_keepers.py --in keepers.json --file9 ../../../content_voice/tom_bari_voice/9_israeli_food_blog_research.md --out results.json
  python apply_scan_keepers.py --selftest

keepers.json = list of objects with Notion property names:
  {"Finding": str, "Detail": str, "Source URL": str, "Tag": str, "Bucket": str,
   "date:Date:start": "YYYY-MM-DD", "url": "<notion page url>"}
"""

import argparse
import json
import re
import sys
from pathlib import Path

MAX_HEB_RUN = 7        # > this many consecutive Hebrew words verbatim => looks like a harvested sentence => REJECT
MAX_HEB_TOTAL = 14     # > this many Hebrew words total => too much copied Hebrew for a technique note => HOLD

SECTION_HEADER = "## 6. Daily Scan keepers (auto-applied by the Hebrew Health Scan loop)"
SECTION_PREAMBLE = (
    "> Appended automatically by `apply_scan_keepers.py` (TASK-381). Each row passed the\n"
    "> deterministic Lane-A no-harvest firewall: no Hebrew verbatim run > {run} words, <= {total}\n"
    "> Hebrew words total, EMULATE/AVOID technique framing. Source URL is provenance only —\n"
    "> never a data source (OFF ban + file 9 firewall)."
).format(run=MAX_HEB_RUN, total=MAX_HEB_TOTAL)

_HEB = re.compile(r"[֐-׿]")


def _is_hebrew_token(tok):
    return bool(_HEB.search(tok))


def hebrew_stats(text):
    """Return (longest_consecutive_hebrew_run, total_hebrew_words)."""
    toks = text.split()
    longest = run = total = 0
    for t in toks:
        if _is_hebrew_token(t):
            total += 1
            run += 1
            longest = max(longest, run)
        else:
            run = 0
    return longest, total


def firewall(keeper):
    """Return (verdict, reason, stats) for one keeper."""
    bucket = (keeper.get("Bucket") or "").strip()
    finding = (keeper.get("Finding") or "").strip()
    detail = (keeper.get("Detail") or "").strip()
    blob = finding + "\n" + detail
    run, total = hebrew_stats(blob)
    stats = {"heb_run": run, "heb_total": total, "max_run": MAX_HEB_RUN, "max_total": MAX_HEB_TOTAL}

    if bucket != "Content-Hebrew skills":
        return "SKIP", "not Lane A (bucket=%r) -> routed to its own owner, not file 9" % bucket, stats
    head = finding.upper().lstrip("\"' ")
    if not (head.startswith("EMULATE") or head.startswith("AVOID")):
        return "HOLD", "not technique-framed (Finding must start EMULATE/AVOID)", stats
    if run > MAX_HEB_RUN:
        return "REJECT", "verbatim Hebrew run %d > %d words (looks like harvested phrasing)" % (run, MAX_HEB_RUN), stats
    if total > MAX_HEB_TOTAL:
        return "HOLD", "Hebrew word total %d > %d (too much copied Hebrew for a technique note)" % (total, MAX_HEB_TOTAL), stats
    return "APPLY", "clean technique note", stats


def render_bullet(keeper, stats):
    finding = (keeper.get("Finding") or "").strip()
    detail = (keeper.get("Detail") or "").strip()
    src = (keeper.get("Source URL") or "").strip()
    tag = (keeper.get("Tag") or "").strip()
    src_md = "[source](%s)" % src if src else "(no source url)"
    tag_md = (" · `%s`" % tag) if tag else ""
    return "- **%s** %s %s · firewall: run=%d/<=%d, heb=%d/<=%d%s" % (
        finding, detail, src_md, stats["heb_run"], MAX_HEB_RUN, stats["heb_total"], MAX_HEB_TOTAL, tag_md,
    )


def apply_to_file9(file9_path, applied_by_date):
    """Append APPLY bullets to file 9 under a managed section, grouped by date. Idempotent
    via the applied-index sidecar (the caller dedups by url before passing rows; here we just
    write what we're given)."""
    p = Path(file9_path)
    text = p.read_text(encoding="utf-8")
    if SECTION_HEADER not in text:
        text = text.rstrip() + "\n\n---\n\n" + SECTION_HEADER + "\n" + SECTION_PREAMBLE + "\n"
    for date in sorted(applied_by_date):
        bullets = applied_by_date[date]
        date_head = "### " + date
        block = "\n".join(bullets)
        if date_head in text:
            # append after the existing date subheading's block: insert before next "### " or "## " or EOF
            idx = text.index(date_head) + len(date_head)
            rest = text[idx:]
            m = re.search(r"\n(### |## )", rest)
            cut = idx + (m.start() if m else len(rest))
            text = text[:cut].rstrip() + "\n" + block + "\n" + text[cut:]
        else:
            text = text.rstrip() + "\n\n" + date_head + "\n" + block + "\n"
    p.write_text(text, encoding="utf-8")


def run(in_path, file9_path, out_path, index_path):
    keepers = json.loads(Path(in_path).read_text(encoding="utf-8"))
    if isinstance(keepers, dict):
        keepers = [keepers]
    applied_index = []
    if index_path and Path(index_path).exists():
        applied_index = json.loads(Path(index_path).read_text(encoding="utf-8"))
    seen = {r.get("url") for r in applied_index if r.get("url")}

    results = []
    applied_by_date = {}
    for k in keepers:
        url = k.get("url")
        if url and url in seen:
            results.append({"url": url, "Finding": k.get("Finding"), "verdict": "DUPLICATE",
                            "reason": "already applied in a previous run", "action": "none"})
            continue
        verdict, reason, stats = firewall(k)
        action = {"APPLY": "mark Actioned", "REJECT": "mark Dropped",
                  "HOLD": "leave New (human/Adversarial QA)", "SKIP": "leave for its owner"}[verdict]
        rec = {"url": url, "Finding": k.get("Finding"), "verdict": verdict,
               "reason": reason, "action": action, "stats": stats}
        results.append(rec)
        if verdict == "APPLY":
            date = (k.get("date:Date:start") or "undated").strip()
            applied_by_date.setdefault(date, []).append(render_bullet(k, stats))
            applied_index.append({"url": url, "Finding": k.get("Finding"), "date": date})

    if applied_by_date:
        apply_to_file9(file9_path, applied_by_date)
    if index_path:
        Path(index_path).write_text(json.dumps(applied_index, ensure_ascii=False, indent=2), encoding="utf-8")
    if out_path:
        Path(out_path).write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")

    counts = {}
    for r in results:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
    print("apply_scan_keepers: " + ", ".join("%s=%d" % (v, c) for v, c in sorted(counts.items())))
    for r in results:
        print("  [%s] %s -> %s" % (r["verdict"], (r["Finding"] or "")[:70], r["reason"]))
    return results


def selftest():
    cases = [
        # clean EMULATE with short quoted Hebrew label -> APPLY
        ({"Bucket": "Content-Hebrew skills", "Finding": "EMULATE: question-opener arc",
          "Detail": "Headline uses 'האם אנחנו באמת צריכים' then pivots to evidence."}, "APPLY"),
        # AVOID with a 6-word quoted title -> APPLY (title citation, under the run cap)
        ({"Bucket": "Content-Hebrew skills", "Finding": "AVOID: listicle verdict framing",
          "Detail": "Article '6 מאכלים עם ערך תזונתי נמוך במיוחד' moralizes; name what a food provides instead."}, "APPLY"),
        # harvested sentence (long Hebrew run) -> REJECT
        ({"Bucket": "Content-Hebrew skills", "Finding": "EMULATE: nice line",
          "Detail": "Copy this: סירופ תירס נשמע כמעט כמו משהו בריאותי אבל הוא ודומיו הם למעשה תחליף זול וגרוע מאוד."}, "REJECT"),
        # not technique-framed -> HOLD
        ({"Bucket": "Content-Hebrew skills", "Finding": "Sugar is bad", "Detail": "x"}, "HOLD"),
        # wrong lane -> SKIP
        ({"Bucket": "Scoring/methodology", "Finding": "EMULATE: x", "Detail": "y"}, "SKIP"),
    ]
    ok = True
    for k, want in cases:
        got, reason, stats = firewall(k)
        flag = "OK " if got == want else "FAIL"
        if got != want:
            ok = False
        print("%s want=%-7s got=%-7s run=%d total=%d  %s" % (flag, want, got, stats["heb_run"], stats["heb_total"], reason))
    print("SELFTEST", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="in_path")
    ap.add_argument("--file9", dest="file9_path")
    ap.add_argument("--out", dest="out_path")
    ap.add_argument("--index", dest="index_path", default=None,
                    help="sidecar JSON of already-applied keeper urls (dedup across runs)")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    if a.selftest:
        return selftest()
    if not (a.in_path and a.file9_path):
        ap.error("--in and --file9 are required (or use --selftest)")
    run(a.in_path, a.file9_path, a.out_path, a.index_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
