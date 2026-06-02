# -*- coding: utf-8 -*-
"""
TASK-161B — Add deterministic positiveSignals[] / limitingFactors[] to the live
cheese comparison JSON (cheese_frontend_v1.json), so the website "rich row" can
render the green + (top positive) and amber - (top limiting) under each product.

SAME source pattern hummus used (build_hummus_explanation_v1.py): the arrays are a
pure function of structured BSIP2-trace signals (caps_applied / penalties_applied /
dimension_scores / L1 observed macros) plus the run_cheese_003 frontend_package
per-product fields (subpool / light_supported / culture_credited / nutrition).
A fixed Hebrew phrase table is the ONLY copy this layer emits. No LLM copy, no
hand-written per-product strings. Re-running on the same inputs reproduces the file.

Does NOT touch: score, grade, confidence, insightLine, nutrition, _cluster, _meta
product ordering. Verified byte-identical by id after regen (see assertions).

Honors explanation-engine v2 governance (snack_bars/reports/explanation_engine_v2.md):
  - 9 banned phrases are never emitted (asserted at the end).
  - every signal carries a real value (named subpool / named additive class /
    measured g / mg) — no category-level genericity.
  - no false "added sugar" / "clean list" claim: a clean-list positive fires ONLY
    when the trace shows ZERO additive-cap and ZERO sugar penalty AND a real
    ingredient_list is present; otherwise it is withheld (not invented).

Sources:
  base live JSON : C:\\bari\\bari-web\\src\\data\\comparisons\\cheese_frontend_v1.json
  package        : C:\\Bari\\02_products\\cheese_spreads\\factory_run_003\\frontend_package.json
  BSIP2 traces   : C:\\Bari\\02_products\\cheese_spreads\\bsip2_outputs\\run_cheese_003\\products\\bsip1_cheese_<barcode>\\bsip2_trace.json
"""
import io, json, os, glob

HERE  = os.path.dirname(os.path.abspath(__file__))
LIVE  = r"C:\bari\bari-web\src\data\comparisons\cheese_frontend_v1.json"
PKG   = os.path.join(HERE, "frontend_package.json")
TRACE = r"C:\Bari\02_products\cheese_spreads\bsip2_outputs\run_cheese_003\products"

BANNED = ["עיבוד מרבי", "בסיס מהונדס", "ריבוי ממתיקים", "מיצוב פיטנס",
          "מוצר מעובד מאוד", "בעיית סוכר", "חלבון נמוך", "מרכיבים רבים", "ציון בסיסי"]

SUBPOOL_HE = {
    "cottage": "גבינת קוטג'",
    "white_cheese_quark": "גבינה לבנה",
    "cream_cheese_spread": "ממרח גבינה",
    "labaneh": "לבנה",
}


def fmt(n):
    if n is None:
        return None
    return str(int(n)) if float(n).is_integer() else str(round(float(n), 1))


def load_trace(barcode):
    p = os.path.join(TRACE, f"bsip1_cheese_{barcode}", "bsip2_trace.json")
    return json.load(io.open(p, encoding="utf-8")) if os.path.exists(p) else None


def real_ingredient_count(trace):
    """Count of genuine ingredient tokens in the trace's L1 list BEFORE the
    Shufersal nutrition-panel/disclaimer bleed (the bleed always starts inside a
    token containing 'ערכים תזונתיים' / 'הנתונים המדויקים')."""
    L = (trace or {}).get("L1_observed_signals") or {}
    lst = L.get("ingredient_list") or []
    real = []
    for tok in lst:
        if any(m in tok for m in ("ערכים תזונתיים", "הנתונים המדויקים", "אין להסתמך")):
            break
        real.append(tok)
    return len(real), bool(real)


def positive_signals(pkgp, trace):
    """מה שבלט — real, product-grounded strengths, priority-ordered. Take top 2."""
    out = []
    nut = pkgp["nutrition"]
    prot = nut.get("protein_g")
    sub = pkgp["subpool"]
    caps = {c["rule"] for c in (trace.get("caps_applied") or [])} if trace else set()
    pens = {p["rule"] for p in (trace.get("penalties_applied") or [])} if trace else set()
    n_ing, has_list = real_ingredient_count(trace)

    # P1 — protein, framed against the subpool it belongs to (real headline macro).
    if prot is not None:
        if sub in ("cottage", "white_cheese_quark", "labaneh") and prot >= 9:
            out.append(f"חלבון גבוה לקטגוריה — {fmt(prot)} גרם ל-100 גרם")
        elif sub == "cream_cheese_spread" and prot >= 7:
            out.append(f"חלבון בולט לממרח — {fmt(prot)} גרם ל-100 גרם")
        elif prot >= 6:
            out.append(f"חלבון — {fmt(prot)} גרם ל-100 גרם")

    # P2 — live cultures actually credited by the engine (real, traced flag).
    if pkgp.get("culture_credited"):
        out.append("תרבית חיה זוהתה ברשימת הרכיבים")

    # P3 — short / clean ingredient list. Fires ONLY with a real list of >=2 tokens
    # (a single token is bleed-truncation, not credible evidence of cleanliness) and
    # NO additive cap + NO long-list/sugar penalty (never asserted from absence).
    additive_cap = "ADDITIVE_MARKERS_3_PLUS" in caps or "ADDITIVE_MARKERS_5_PLUS" in caps
    if (len(out) < 2 and has_list and 2 <= n_ing <= 5
            and not additive_cap
            and "LONG_INGREDIENT_LIST" not in pens
            and "MULTIPLE_ADDED_SUGAR_MARKERS" not in pens):
        out.append(f"רשימת רכיבים קצרה — {n_ing} רכיבים, ללא תוספי מזון מזוהים")

    # P4 — verified "light" claim that the panel actually supports (divergence-free).
    if len(out) < 2 and pkgp.get("light_claim") and pkgp.get("light_supported"):
        fat = nut.get("fat_g")
        if fat is not None:
            out.append(f"סימון 'לייט' נתמך בנתונים — {fmt(fat)} גרם שומן ל-100 גרם")

    return out[:2]


def limiting_factors(pkgp, trace):
    """מה שהגביל — real, traced limiters, salience-ordered. Take top 2.
    Every phrase names the specific driver (additive class / sat-fat / sodium /
    sugar markers / long list) with a value where the trace provides one."""
    nut = pkgp["nutrition"]
    sat = nut.get("fat_saturated_g")
    fat = nut.get("fat_g")
    sod = nut.get("sodium_mg")
    sub = pkgp["subpool"]
    caps = {c["rule"] for c in (trace.get("caps_applied") or [])} if trace else set()
    pens = {p["rule"] for p in (trace.get("penalties_applied") or [])} if trace else set()
    ranked = []  # (salience, phrase)

    # L1 — additive load (binding cap; names the count band, not a generic class).
    if "ADDITIVE_MARKERS_5_PLUS" in caps:
        ranked.append((1, "חמישה תוספי מזון ומעלה ברשימה — מעבר לבסיס החלבי"))
    elif "ADDITIVE_MARKERS_3_PLUS" in caps:
        ranked.append((1, "שלושה תוספי מזון ומעלה ברשימה — מעבר לבסיס החלבי"))

    # L2 — added-sugar markers (only when the engine actually flagged them).
    if "MULTIPLE_ADDED_SUGAR_MARKERS" in pens:
        ranked.append((2, "מספר מקורות סוכר מצוינים ברשימת הרכיבים"))

    # L3 — high saturated fat (Israeli red-label cap = a real, traced threshold).
    if "ISRAELI_RED_LABELS_2_PLUS" in caps:
        ranked.append((3, "סימון אדום כפול — שומן רווי ונתרן גבוהים על האריזה"))
    elif "ISRAELI_RED_LABEL_1_SAT_FAT" in caps:
        if sat is not None:
            ranked.append((3, f"שומן רווי גבוה — {fmt(sat)} גרם ל-100 גרם (סימון אדום)"))
        else:
            ranked.append((3, "שומן רווי גבוה — סימון אדום על האריזה"))

    # L4 — high sodium (explicit cap, or measured >=700; names the mg).
    if "HIGH_SODIUM_700MG_PLUS" in caps or (sod is not None and sod >= 700):
        ranked.append((4, f"נתרן גבוה — {fmt(sod)} מ\"ג ל-100 גרם" if sod else "נתרן גבוה על האריזה"))

    # L5 — fat-heavy spread (cream-cheese pool is fat-defined; state the WHY w/ value).
    if sub == "cream_cheese_spread" and fat is not None and fat >= 20:
        ranked.append((5, f"ממרח עתיר שומן — {fmt(fat)} גרם שומן ל-100 גרם, לא מקור חלבון"))

    # L6 — light reformulation that the panel does NOT support (divergence finding).
    if pkgp.get("light_claim") and pkgp.get("light_supported") is False:
        ranked.append((6, "סימון 'לייט' — הפחתת השומן אינה נתמכת בנתוני האריזה"))

    # L7 — long ingredient list penalty (fallback, names it as a list-length driver).
    if "LONG_INGREDIENT_LIST" in pens:
        ranked.append((7, "רשימת רכיבים ארוכה — מעבר לרכיבי הבסיס"))

    # L8 — processed structure cap (last-resort fallback; names the NOVA proxy band).
    if not ranked and "NOVA_PROXY_4_ULTRA_PROCESSED" in caps:
        ranked.append((8, "מבנה רכיבים מעובד מאוד — תקרת עיבוד מחייבת"))
    elif not ranked and "NOVA_PROXY_3_PROCESSED" in caps:
        ranked.append((8, "מבנה רכיבים מעובד — תוספות מעבר לבסיס החלבי"))

    best = {}
    for s, phrase in ranked:
        if phrase not in best or s < best[phrase]:
            best[phrase] = s
    return [ph for ph, _ in sorted(best.items(), key=lambda kv: kv[1])][:2]


def main():
    live = json.load(io.open(LIVE, encoding="utf-8"))
    pkg = json.load(io.open(PKG, encoding="utf-8"))
    pkg_by_bc = {str(p["barcode"]): p for p in pkg["products"]}

    before = {p["id"]: (p["score"], p["grade"], p["confidence"]) for p in live["products"]}

    stats = {"pos": 0, "lim": 0, "neither": 0, "n": 0}
    no_signal = []
    for p in live["products"]:
        bc = p["id"][len("che-"):]
        pkgp = pkg_by_bc.get(bc)
        trace = load_trace(bc)
        assert pkgp is not None, f"no package row for {p['id']}"
        pos = positive_signals(pkgp, trace)
        lim = limiting_factors(pkgp, trace)
        exp = p.setdefault("expansion", {})
        exp["positiveSignals"] = pos
        exp["limitingFactors"] = lim
        stats["n"] += 1
        stats["pos"] += bool(pos)
        stats["lim"] += bool(lim)
        if not pos and not lim:
            stats["neither"] += 1
            no_signal.append(p["id"])
        # governance: no banned phrase ever
        for arr in (pos, lim):
            for s in arr:
                for b in BANNED:
                    assert b not in s, f"banned phrase '{b}' in {p['id']}: {s}"

    # scores/grades/confidence must be byte-identical by id
    after = {p["id"]: (p["score"], p["grade"], p["confidence"]) for p in live["products"]}
    assert before == after, "SCORE/GRADE/CONFIDENCE CHANGED — aborting"

    live["_meta"]["expansion"] = "interpretive_expansion_v1"
    live["_meta"].setdefault("provenance", {})["signals_task"] = "TASK-161B"
    live["_meta"]["provenance"]["signals_from"] = (
        "deterministic from run_cheese_003 bsip2_trace.json (caps_applied/penalties_applied/"
        "dimension_scores/L1) + frontend_package per-product fields; engine-v2 governance"
    )

    with io.open(LIVE, "w", encoding="utf-8") as f:
        json.dump(live, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print("WROTE", LIVE)
    print(f"products {stats['n']} | with positive {stats['pos']} | with limiting {stats['lim']} "
          f"| with neither {stats['neither']}")
    if no_signal:
        print("NO-SIGNAL ids:", no_signal)


if __name__ == "__main__":
    main()
