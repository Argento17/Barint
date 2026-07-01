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
    mism = []
    for p in prods:
        t = tr.get(str(p["barcode"]))
        if not t:
            mism.append((p["barcode"], "no trace")); continue
        if (round(p["score"], 1), p["grade"]) != (round(t["final_score_estimate"], 1), t["grade_estimate"]):
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
    bad_ing = []
    for p in prods:
        ing = ((p.get("expansion", {}) or {}).get("ingredients") or "").strip()
        if not ing: continue
        if ing[-1] in ",({-–—" or len(ing) < 40:
            bad_ing.append((p["barcode"], "truncated/short", repr(ing[-18:])))
        elif any(mk in ing for mk in BLEED_MARKERS):
            bad_ing.append((p["barcode"], "marketing/nutrition bleed", ""))
    print(f"[{'FAIL' if bad_ing else 'PASS'}] ingredient    ({len(bad_ing)} truncated/bleed)")
    if bad_ing: fails.append(("ingredients", bad_ing[:8]))

    # 6. stale-rank copy (WARN — needs human/trace confirm, not auto-fail)
    ranked = sorted(prods, key=lambda p: -(p["score"] or 0))
    top_bc = ranked[0]["barcode"] if ranked else None
    rankflag = []
    for p in prods:
        txt = (p.get("rowVerdict", "") or "") + (p.get("insightLine", "") or "")
        if any(ph in txt for ph in RANK_PHRASES) and p["barcode"] != top_bc:
            rankflag.append((p["barcode"], "claims rank but is not #1"))
    print(f"[{'WARN' if rankflag else 'PASS'}] stale-rank    ({len(rankflag)} non-top products with rank claims)")
    if rankflag: warns.append(("stale-rank", rankflag))

    # 7. image presence (HTTP optional)
    noimg = [p["barcode"] for p in prods if not p.get("imageUrl")]
    print(f"[{'FAIL' if noimg else 'PASS'}] image present ({len(prods)-len(noimg)}/{len(prods)} have imageUrl)")
    if noimg: fails.append(("images", noimg))
    if a.http:
        import urllib.request
        dead = []
        for p in prods:
            u = p.get("imageUrl")
            if not u: continue
            try:
                urllib.request.urlopen(urllib.request.Request(u, method="HEAD"), timeout=8)
            except Exception:
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
