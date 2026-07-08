#!/usr/bin/env python3
"""
validate_comparison_page.py — terminal pre-ship gate battery for a Bari comparison page.

Codifies the error classes the run_005 (cookies) adversarial cycle exposed so future pages
catch them in ONE command instead of via a red-team block:
  - score==trace        (RT score-integrity)
  - OFF ban             (off_used must be 0)
  - PENDING render       (any placeholder in a field a component renders)  [C3-after CRIT-1]
  - count consistency    (_meta / hero / filters / caveat all agree)         [RT-3]
  - ingredient sanity    (no truncation '(' '{' / trailing comma / marketing-bleed) [RT-4/5, C3-after/final CRIT-2]
  - stale-rank copy       (verdicts claiming #1/'בראש' flagged for manual confirm) [RT-1]
  - image presence        (every product has an imageUrl; optional HTTP check)

Usage:
  python validate_comparison_page.py --json <frontend_json> --traces <run_dir/products> [--http]
Exit 0 = all hard gates pass. Exit 1 = at least one hard gate failed.
"""
import argparse, glob, json, os, re, sys

PENDING = "PENDING_COPY"
# fields a render component actually surfaces (resolve against the component, not the mapper)
RENDERED_FIELDS = ["rowVerdict", "insightLine"]
RENDERED_EXPANSION = ["bottomLine", "positiveSignals", "limitingFactors", "unknowns",
                      "caveats", "comparisonContext", "ingredients"]
BLEED_MARKERS = ["ערכים תזונתיים", "יש לקרוא", "התמונות והתאריכים", "אין להסתמך"]
RANK_PHRASES = ["הגבוה ביותר במדף", "עומד בראש", "עומדות בראש", "עלה לראש", "הציון שני", "הציון הראשון"]


def load_traces(trace_dir):
    tr = {}
    for f in glob.glob(os.path.join(trace_dir, "*", "bsip2_trace.json")):
        t = json.load(open(f, encoding="utf-8"))
        tr[str(t["input_reference"]["barcode"])] = t
    return tr


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", required=True)
    ap.add_argument("--traces", required=True, nargs="+", help="one or more run_dir/products dirs containing */bsip2_trace.json; first match wins on barcode collision")
    ap.add_argument("--http", action="store_true", help="also HTTP-check every imageUrl (slow)")
    ap.add_argument("--local-origin", default="http://localhost:3000",
                     help="dev-server origin used as a fallback check for scheme-less imageUrls when --http is set")
    ap.add_argument("--public-dir", default=None,
                     help="filesystem root for scheme-less imageUrls (default: <repo>/bari-web/public next to this script)")
    a = ap.parse_args()

    d = json.load(open(a.json, encoding="utf-8"))
    prods = d["products"]
    pc = d.get("page_copy", {})
    # Load traces from all provided dirs; first dir wins on barcode collision
    tr = {}
    for tdir in a.traces:
        for bc, t in load_traces(tdir).items():
            if bc not in tr:
                tr[bc] = t
    fails, warns = [], []

    # 1. score == trace
    # NOTE: a product can be legitimately unscored (score=None, grade=None is
    # the schema-documented state for INSUFFICIENT products — see
    # page_output_schema_v1.json "score: null for INSUFFICIENT products").
    # The trace still carries a placeholder final_score_estimate (e.g. the
    # neutral 50 the engine returns for structurally-empty input) — that is
    # an internal engine value, not something meant to be displayed, so it
    # must NOT be compared numerically against a null JSON score. Guard both
    # sides so a real null-vs-real-number mismatch still fails loudly.
    def _scores_match(json_score, json_grade, trace_score, trace_grade):
        if json_score is None:
            # Null score is only valid when the trace agrees the product is
            # unscoreable (insufficient/None grade_estimate on the engine
            # side); a null JSON score paired with a real trace grade is a
            # genuine mismatch and must still fail.
            return json_grade is None and trace_grade in (None, "insufficient_data")
        if trace_score is None:
            return False
        return (round(json_score, 1), json_grade) == (round(trace_score, 1), trace_grade)

    mism = []
    for p in prods:
        t = tr.get(str(p["barcode"]))
        if not t:
            mism.append((p["barcode"], "no trace")); continue
        if not _scores_match(p["score"], p["grade"], t["final_score_estimate"], t["grade_estimate"]):
            mism.append((p["barcode"], f'{p["score"]}/{p["grade"]} vs {t["final_score_estimate"]}/{t["grade_estimate"]}'))
    (fails if mism else warns).append(("score==trace", f"{len(mism)} mismatch") if mism else None) if mism else None
    print(f"[{'FAIL' if mism else 'PASS'}] score==trace  ({len(prods)} products, {len(mism)} mismatch)")
    if mism: fails.append(("score==trace", mism[:5]))

    # 2. OFF ban
    off = [p["barcode"] for p in prods if (p.get("expansion", {}) or {}).get("off_used") or p.get("off_used")]
    print(f"[{'FAIL' if off else 'PASS'}] OFF ban       ({len(off)} off_used)")
    if off: fails.append(("OFF", off))

    # 3. PENDING in rendered fields
    pend = []
    for p in prods:
        for k in RENDERED_FIELDS:
            if p.get(k) == PENDING: pend.append((p["barcode"], k))
        ex = p.get("expansion", {}) or {}
        for k in RENDERED_EXPANSION:
            if PENDING in json.dumps(ex.get(k), ensure_ascii=False): pend.append((p["barcode"], f"expansion.{k}"))
    for k in ("prologue", "caveat", "hero", "methodology"):
        if PENDING in json.dumps(pc.get(k), ensure_ascii=False): pend.append(("page_copy", k))
    print(f"[{'FAIL' if pend else 'PASS'}] PENDING render ({len(pend)} placeholder in rendered fields)")
    if pend: fails.append(("PENDING", pend[:8]))

    # 4. count consistency
    n = len(prods)
    meta = d.get("_meta", {})
    issues = []
    if meta.get("product_count") != n: issues.append(f"_meta.product_count={meta.get('product_count')}≠{n}")
    hero = pc.get("hero", {})
    if hero.get("productCount") not in (None, n): issues.append(f"hero.productCount={hero.get('productCount')}")
    if hero.get("scoredCount") not in (None, n): issues.append(f"hero.scoredCount={hero.get('scoredCount')}")
    allf = [f for f in pc.get("filters", []) if f.get("id") == "all"]
    if allf and allf[0].get("count") != n: issues.append(f"filters.all={allf[0].get('count')}")
    # any stale count strings anywhere in page_copy that don't equal n (within a small set of likely-count tokens)
    body = json.dumps(pc, ensure_ascii=False)
    for m in re.findall(r"מתוך (\d+) המוצרים", body):
        if int(m) != n: issues.append(f"caveat 'מתוך {m}'≠{n}")
    print(f"[{'FAIL' if issues else 'PASS'}] count consist ({len(issues)} disagreements)")
    if issues: fails.append(("counts", issues))

    # 5. ingredient sanity (truncation / trailing comma / marketing bleed)
    # NOTE (TASK-515A): a raw len<40 floor false-positives on genuinely short-but-
    # complete lists (e.g. Ayran "חלב בקר מפוסטר, מלח" = pasteurized cow milk, salt
    # — 2 real ingredients; same shape as butter's "cream, salt").
    #
    # NOTE (TASK-515, second pass): the len<40-AND-<2-comma-parts "bare fragment"
    # guess above was ITSELF a false-positive generator, not a narrow yogurt-only
    # quirk. A census of every already-shipped comparison JSON found it wrongly
    # flagging single-ingredient staples with no comma at all: milk "חלב" (plain
    # milk, 1 word), milk "חלב עיזים מפוסטר מהומגן", juices "מיץ תפוזים" / "מיץ
    # רימונים" / "100% מיץ תפוזים סחוט טבעי" (×6), crackers "כוסמת אורגנית (100%)"
    # / "אורז חום מלא (100%)" (×3), and yogurt "חלב כבשים מפוסטר" (pasteurized
    # sheep milk — this ticket's case; BSIP1 raw scrape confirms the label reads
    # "...מפוסטר" then immediately "מכיל חלב כבשים" (allergen line) then the
    # nutrition table, i.e. the real printed ingredient list IS one item — see
    # ingredients_raw_he in bsip1_yogurt_4068011.json). Comma-count says nothing
    # about completeness: single-item foods are simply written without a comma.
    # Checked against every category above: zero of these 12 were ever a real
    # truncation; every ACTUAL truncation in the corpus (132 bread rows with
    # mid-label cuts) ends on a dangling connector char and is still caught below.
    #
    # Principled rule: flag truncated/short iff the text ENDS IN A CONNECTOR char
    # (a dangling "," "(" "{" "-" "–" "—" means the source was literally cut off
    # mid-label — the reliable signal) OR the text is DEGENERATE — either near-
    # empty (<3 chars: OCR noise, not a real ingredient name) or literally just a
    # dangling Hebrew function word that grammatically requires a continuation
    # ("מכיל"/contains, "עם"/with, "של"/of, "או"/or, ...) and could never be a
    # complete ingredient statement on its own. A short-but-grammatically-whole
    # noun/adjective phrase (any word count, comma or none) is a complete simple
    # product and must PASS.
    CONNECTOR_CHARS = ",({-–—"
    DANGLING_FRAGMENT_WORDS = {"מכיל", "עם", "של", "או", "וגם", "וכן", "בתוספת", "המכיל", "ללא"}
    bad_ing = []
    for p in prods:
        ing = ((p.get("expansion", {}) or {}).get("ingredients") or "").strip()
        if not ing: continue
        is_degenerate_fragment = len(ing) < 3 or ing in DANGLING_FRAGMENT_WORDS
        if ing[-1] in CONNECTOR_CHARS or is_degenerate_fragment:
            bad_ing.append((p["barcode"], "truncated/short", repr(ing[-18:])))
        elif any(mk in ing for mk in BLEED_MARKERS):
            bad_ing.append((p["barcode"], "marketing/nutrition bleed", ""))
    print(f"[{'FAIL' if bad_ing else 'PASS'}] ingredient    ({len(bad_ing)} truncated/bleed)")
    if bad_ing: fails.append(("ingredients", bad_ing[:8]))

    # 6. superlative rank check — AUTOMATED via rank_check.py (TASK-422/W3).
    # Supersedes the old manual-WARN phrase scan: rank_check re-derives every superlative
    # claim (nutrient extremum / score / additives) against the FULL corpus and HARD-fails a
    # false one, while deferring subpool-scoped/uniqueness claims to WARN. Runs as a subprocess
    # so the two validators stay decoupled; if it is unavailable, degrade to a WARN (never crash
    # the ship gate).
    rc_path = os.path.join(os.path.dirname(__file__), "..", "validators", "rank_check.py")
    if os.path.exists(rc_path):
        try:
            import subprocess
            proc = subprocess.run([sys.executable, rc_path, "--json", a.json, "--emit-json"],
                                  capture_output=True, encoding="utf-8", errors="replace", timeout=120)
            rc = json.loads(proc.stdout or "{}")
            false_sups = [f for f in rc.get("findings", []) if f.get("status") == "FAIL"]
            manual = [f for f in rc.get("findings", []) if f.get("level") == "WARN"]
            print(f"[{'FAIL' if false_sups else 'PASS'}] superlative   "
                  f"({len(false_sups)} false, {len(manual)} manual-review) [rank_check.py]")
            if false_sups:
                fails.append(("superlative", [f["detail"] for f in false_sups][:8]))
            if manual:
                warns.append(("superlative-manual", [f["detail"] for f in manual][:8]))
        except Exception as e:  # noqa: BLE001 — a validator hiccup must not break the ship gate
            print(f"[WARN] superlative   (rank_check.py error: {e}) — run it standalone")
            warns.append(("superlative", f"rank_check.py error: {e}"))
    else:
        # fallback: the original lightweight phrase scan
        ranked = sorted(prods, key=lambda p: -(p["score"] or 0))
        top_bc = ranked[0]["barcode"] if ranked else None
        rankflag = [(p["barcode"], "claims rank but is not #1") for p in prods
                    if any(ph in ((p.get("rowVerdict", "") or "") + (p.get("insightLine", "") or ""))
                           for ph in RANK_PHRASES) and p["barcode"] != top_bc]
        print(f"[{'WARN' if rankflag else 'PASS'}] stale-rank    ({len(rankflag)} rank claims; rank_check.py absent)")
        if rankflag: warns.append(("stale-rank", rankflag))

    # 7. image presence (HTTP optional)
    noimg = [p["barcode"] for p in prods if not p.get("imageUrl")]
    print(f"[{'FAIL' if noimg else 'PASS'}] image present ({len(prods)-len(noimg)}/{len(prods)} have imageUrl)")
    if noimg: fails.append(("images", noimg))
    if a.http:
        # RT-V1 fix (TASK-515A red-team): a scheme-less/relative imageUrl like
        # "/products/x.webp" has no netloc, so urlopen(Request(u, method="HEAD"))
        # raises ValueError("unknown url type") for EVERY same-origin self-hosted
        # image — a guaranteed false FAIL regardless of whether the file is real.
        # Fix: resolve scheme-less URLs (start with "/") against the filesystem
        # under bari-web/public first (authoritative, no server dependency); if
        # the file isn't found there, fall back to a HEAD check against a local
        # dev origin (in case the asset is served dynamically / not yet built).
        # Absolute http(s) URLs keep the original HEAD check unchanged.
        import urllib.request
        from urllib.parse import urlparse
        dead = []
        public_dir = a.public_dir or os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "bari-web", "public"))
        for p in prods:
            u = p.get("imageUrl")
            if not u: continue
            parsed = urlparse(u)
            if parsed.scheme in ("http", "https") and parsed.netloc:
                try:
                    urllib.request.urlopen(urllib.request.Request(u, method="HEAD"), timeout=8)
                except Exception:
                    dead.append(p["barcode"])
            elif u.startswith("/"):
                fs_path = os.path.join(public_dir, u.lstrip("/"))
                ok = os.path.isfile(fs_path)
                if not ok:
                    try:
                        urllib.request.urlopen(
                            urllib.request.Request(a.local_origin.rstrip("/") + u, method="HEAD"), timeout=3)
                        ok = True
                    except Exception:
                        ok = False
                if not ok:
                    dead.append(p["barcode"])
            else:
                # unrecognized scheme (not http(s), not root-relative) — genuinely unresolvable
                dead.append(p["barcode"])
        print(f"[{'FAIL' if dead else 'PASS'}] image HTTP    ({len(dead)} dead)")
        if dead: fails.append(("image-http", dead))

    print("-" * 60)
    if fails:
        print(f"RESULT: FAIL — {len(fails)} hard gate(s) failed: {[f[0] for f in fails]}")
        for name, ev in fails:
            print(f"  · {name}: {ev}")
        if warns: print(f"  warnings: {[w[0] for w in warns]}")
        sys.exit(1)
    print(f"RESULT: PASS — all hard gates green" + (f" ({len(warns)} warning(s) to eyeball: {[w[0] for w in warns]})" if warns else ""))
    sys.exit(0)


if __name__ == "__main__":
    main()
