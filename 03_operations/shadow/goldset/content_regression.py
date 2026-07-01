#!/usr/bin/env python3
r"""
content_regression.py — voice/structure golden regression for Bari content (TASK-421 / W2 content arm)
======================================================================================================

The gold set (gold_check.py) guards SCORE accuracy. This guards CONTENT: the owner-approved
golden pages — milk (content gold), brined-cheeses (structure gold), cereals (voice gold) — must
not silently drift out of Tom's voice when copy is re-authored. This is the content half of the
"golden regression suite" and the CI arm Project Tom's Voice lacked.

Two layers, mirroring the score gate:
  1. DETERMINISTIC (always, zero cost) — freeze each golden page's consumer copy fields into a
     baseline; on `check`, diff current vs baseline and report exactly which fields CHANGED. An
     unchanged golden = PASS with no model call.
  2. JUDGE (only on changed fields) — a pluggable rubric judge (an independent lane, same shape as
     verify_variance.py: field JSON on stdin -> {"score":0..1,"reason":"..."}) scores whether the
     changed copy still matches the voice fingerprint. A score below --threshold is a regression.

So the LLM judge runs only when copy actually changed, and a change that stays in-voice passes.
No hard model dependency: with no --judge, changed fields are reported as FLAGGED for manual review.

Golden pages + fields are frozen below. Baselines live next to this script under content_baseline/.

Commands:
  content_regression.py capture                 # freeze current golden copy as the baseline
  content_regression.py check [--judge CMD] [--threshold 0.7] [--json]
  content_regression.py --selftest

Exit: 0 no regression · 1 drift/regression (or unreviewed change with no judge) · 2 usage/load error.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(r"C:\Bari")
COMPARISONS = REPO_ROOT / "bari-web" / "src" / "data" / "comparisons"
BASELINE_DIR = Path(__file__).resolve().parent / "content_baseline"

# owner-approved golden pages (memory: golden_comparison_page_brined / owner_milk_page_content_gold_standard
# / cereals_voice_golden_template)
GOLDEN_PAGES = {
    "milk": "milk_frontend_v1.json",
    "brined_cheeses": "brined_cheeses_frontend_v2.json",
    "cereals": "cereals_frontend_v2.json",
}
PRODUCT_TEXT_FIELDS = ["insightLine", "rowVerdict"]
EXPANSION_TEXT_FIELDS = ["comparisonContext", "positiveSignals", "limitingFactors", "bottomLine"]

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
    except (AttributeError, ValueError):
        pass


def _extract_content(page: dict) -> dict:
    """Pull the consumer-facing copy fields keyed by product id + field."""
    out = {}
    for p in page.get("products", []):
        pid = str(p.get("id") or p.get("barcode") or "?")
        for f in PRODUCT_TEXT_FIELDS:
            v = p.get(f)
            if v:
                out[f"{pid}.{f}"] = str(v)
        ex = p.get("expansion", {}) or {}
        for f in EXPANSION_TEXT_FIELDS:
            v = ex.get(f)
            if isinstance(v, list):
                v = " | ".join(str(x) for x in v)
            if v:
                out[f"{pid}.expansion.{f}"] = str(v)
    pc = page.get("page_copy", {}) or {}
    for k in ("hero", "prologue", "caveat"):
        if pc.get(k):
            out[f"page_copy.{k}"] = json.dumps(pc[k], ensure_ascii=False, sort_keys=True)
    return out


def _load_page(slug: str) -> dict | None:
    path = COMPARISONS / GOLDEN_PAGES[slug]
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def cmd_capture() -> int:
    BASELINE_DIR.mkdir(parents=True, exist_ok=True)
    n = 0
    for slug in GOLDEN_PAGES:
        page = _load_page(slug)
        if page is None:
            print(f"[capture] SKIP {slug} — page not found")
            continue
        content = _extract_content(page)
        (BASELINE_DIR / f"{slug}.json").write_text(
            json.dumps(content, ensure_ascii=False, indent=1, sort_keys=True), encoding="utf-8")
        print(f"[capture] {slug}: froze {len(content)} copy fields")
        n += 1
    print(f"[capture] baseline written for {n} golden page(s) -> {BASELINE_DIR}")
    return 0


def _run_judge(judge_cmd: str, slug: str, field: str, baseline: str, current: str) -> tuple[float, str]:
    payload = json.dumps({"page": slug, "field": field, "baseline": baseline, "current": current},
                         ensure_ascii=False)
    try:
        # UTF-8 explicitly — payload carries Hebrew; the default cp1252 stdin encode crashes on it.
        proc = subprocess.run(judge_cmd, shell=True, input=payload, encoding="utf-8",
                              errors="replace", capture_output=True, timeout=120)
        obj = json.loads(proc.stdout.strip() or "{}")
        return float(obj.get("score", 0.0)), str(obj.get("reason", ""))[:200]
    except Exception as e:  # noqa: BLE001 — a judge hiccup → treat as unscored (flag)
        return -1.0, f"(judge error: {e})"


def cmd_check(judge_cmd: str | None, threshold: float, emit_json: bool) -> int:
    if not BASELINE_DIR.exists():
        print("check: no baseline. run `content_regression.py capture` first.", file=sys.stderr)
        return 2
    findings, changed_total, regressions = [], 0, 0
    for slug in GOLDEN_PAGES:
        bpath = BASELINE_DIR / f"{slug}.json"
        page = _load_page(slug)
        if not bpath.exists() or page is None:
            findings.append({"page": slug, "status": "SKIP", "detail": "no baseline or page missing"})
            continue
        baseline = json.loads(bpath.read_text(encoding="utf-8"))
        current = _extract_content(page)
        changed = {k for k in baseline if current.get(k) != baseline[k]}
        added = set(current) - set(baseline)
        removed = set(baseline) - set(current)
        for k in sorted(changed):
            changed_total += 1
            if judge_cmd:
                score, reason = _run_judge(judge_cmd, slug, k, baseline[k], current[k])
                if score < 0:
                    regressions += 1
                    findings.append({"page": slug, "field": k, "status": "FLAG", "detail": reason})
                elif score < threshold:
                    regressions += 1
                    findings.append({"page": slug, "field": k, "status": "REGRESSION",
                                     "detail": f"voice score {score:.2f} < {threshold} — {reason}"})
                else:
                    findings.append({"page": slug, "field": k, "status": "OK",
                                     "detail": f"voice score {score:.2f}"})
            else:
                regressions += 1  # a change with no judge is unreviewed → flag
                findings.append({"page": slug, "field": k, "status": "FLAG",
                                 "detail": "changed vs golden; no --judge → manual review"})
        for k in sorted(added):
            findings.append({"page": slug, "field": k, "status": "ADDED", "detail": "new field vs golden"})
        for k in sorted(removed):
            regressions += 1
            findings.append({"page": slug, "field": k, "status": "REMOVED", "detail": "field dropped vs golden"})

    verdict = "REGRESSION" if regressions else "PASS"
    if emit_json:
        print(json.dumps({"verdict": verdict, "changed": changed_total,
                          "regressions": regressions, "findings": findings}, ensure_ascii=False, indent=2))
    else:
        print(f"content_regression :: {verdict}  ({changed_total} changed field(s), {regressions} regression(s))")
        for f in findings:
            if f["status"] != "OK":
                print(f"  [{f['status']:<10}] {f.get('page')}:{f.get('field','')}  {f['detail']}")
    return 1 if regressions else 0


def _selftest() -> int:
    global BASELINE_DIR, GOLDEN_PAGES, _load_page
    import tempfile
    tmp = Path(tempfile.mkdtemp(prefix="content_reg_selftest_"))
    BASELINE_DIR = tmp / "baseline"
    ok = True
    try:
        pages = {
            "v0": {"products": [{"id": "A", "insightLine": "מוצר נקי במיוחד",
                                 "expansion": {"comparisonContext": "בראש המדף"}}]},
        }
        state = {"cur": pages["v0"]}
        GOLDEN_PAGES = {"g": "g.json"}
        globals()["_load_page"] = lambda slug: state["cur"]

        cmd_capture()
        # unchanged → PASS
        r1 = cmd_check(judge_cmd=None, threshold=0.7, emit_json=False)
        # change a field, no judge → FLAG (regression=1)
        state["cur"] = {"products": [{"id": "A", "insightLine": "טקסט חדש לגמרי",
                                      "expansion": {"comparisonContext": "בראש המדף"}}]}
        r2 = cmd_check(judge_cmd=None, threshold=0.7, emit_json=False)
        # same change but a judge that scores it in-voice (0.9) → PASS
        r3 = cmd_check(judge_cmd="python -c \"import sys,json;sys.stdin.read();print(json.dumps({'score':0.9,'reason':'in voice'}))\"",
                       threshold=0.7, emit_json=False)
        # a judge that scores it low (0.3) → REGRESSION
        r4 = cmd_check(judge_cmd="python -c \"import sys,json;sys.stdin.read();print(json.dumps({'score':0.3,'reason':'translationese'}))\"",
                       threshold=0.7, emit_json=False)
        print(f"  unchanged->PASS({r1==0}), changed-no-judge->REG({r2==1}), "
              f"in-voice-judge->PASS({r3==0}), low-judge->REG({r4==1})")
        ok = (r1 == 0 and r2 == 1 and r3 == 0 and r4 == 1)
        print(f"SELFTEST: {'OK' if ok else 'BROKEN'}")
        return 0 if ok else 1
    finally:
        import shutil
        shutil.rmtree(tmp, ignore_errors=True)


def main() -> int:
    ap = argparse.ArgumentParser(description="Voice/structure golden regression for Bari content.")
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("capture", help="freeze current golden-page copy as the baseline")
    c = sub.add_parser("check", help="diff golden pages vs baseline; judge changed fields")
    c.add_argument("--judge", help="rubric-judge lane command (field JSON on stdin -> {score,reason})")
    c.add_argument("--threshold", type=float, default=0.7, help="min voice score to pass a changed field")
    c.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return _selftest()
    if args.cmd == "capture":
        return cmd_capture()
    if args.cmd == "check":
        return cmd_check(args.judge, args.threshold, args.json)
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
