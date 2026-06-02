# -*- coding: utf-8 -*-
"""
TASK-161B — Add deterministic positiveSignals[] / limitingFactors[] to the live
yogurts comparison JSON (yogurts_frontend_v2.json). The 3c packaging pass
(build_yogurts_frontend_v2.py) explicitly DEFERRED interpretive expansion; this
pass installs it from the SAME run_yogurt_004 BSIP2 traces, deterministically.

SAME source pattern hummus used: arrays are a pure function of structured BSIP2
trace signals (caps_applied / penalties_applied / L1 observed macros) through a
fixed Hebrew phrase table. No LLM copy, no per-product hand-written strings.

The trace ingredient_list is OCR/disclaimer-polluted (3c builder note), so this
layer derives NOTHING from ingredient text — only from the engine's caps/penalties
(which already encode additive/sugar/list findings) and the clean L1 macro grid.

Does NOT touch: score, grade, confidence, insightLine, nutrition, _cluster, order.
Scores verified byte-identical by id after regen.

Honors explanation-engine v2 governance (9 banned phrases asserted absent; every
signal carries a real value; no positive invented when none exists — omitted).

id->barcode map is the run_yogurt_004 packaging ROWS (build_yogurts_frontend_v2.py),
cross-checked against the barcode embedded in each product's imageUrl.
"""
import io, json, os, re

LIVE  = r"C:\bari\bari-web\src\data\comparisons\yogurts_frontend_v2.json"
TRACE = r"C:\Bari\02_products\yogurt_system\bsip2_outputs\run_yogurt_004\products"

BANNED = ["עיבוד מרבי", "בסיס מהונדס", "ריבוי ממתיקים", "מיצוב פיטנס",
          "מוצר מעובד מאוד", "בעיית סוכר", "חלבון נמוך", "מרכיבים רבים", "ציון בסיסי"]

# yog-id -> barcode (verbatim from build_yogurts_frontend_v2.py ROWS, the authoritative
# 3c packaging map; each is re-verified below against the imageUrl-embedded barcode).
ID_BARCODE = {
    "yog-001": "7290112336712", "yog-002": "7290110328221", "yog-003": "7290014758100",
    "yog-004": "7290114311069", "yog-005": "7290014758117", "yog-006": "7290012645297",
    "yog-007": "7290107936309", "yog-008": "7290110321031", "yog-009": "7290014890589",
    "yog-010": "7290110321680", "yog-011": "7290010471669",
}


def fmt(n):
    if n is None:
        return None
    return str(int(n)) if float(n).is_integer() else str(round(float(n), 1))


def load_trace(barcode):
    p = os.path.join(TRACE, f"bsip1_yogurt_{barcode}", "bsip2_trace.json")
    return json.load(io.open(p, encoding="utf-8"))


def positive_signals(L, caps, pens, cluster):
    out = []
    prot = L.get("protein_g")
    sug = L.get("sugars_g")
    fib = L.get("dietary_fiber_g")
    fat = L.get("fat_g")

    # P1 — protein (the category's headline differentiator; cluster-aware threshold).
    if prot is not None:
        if prot >= 10:
            out.append(f"חלבון גבוה לקטגוריה — {fmt(prot)} גרם ל-100 גרם")
        elif prot >= 8:
            out.append(f"חלבון בולט — {fmt(prot)} גרם ל-100 גרם")

    # P2 — dietary fiber, when actually measured.
    if len(out) < 2 and fib is not None and fib >= 2:
        out.append(f"סיבים תזונתיים — {fmt(fib)} גרם ל-100 גרם")

    # P3 — low sugar with NO added-sugar penalty firing (real low-sugar base, not
    # an absence-of-data claim: requires a measured sugar value AND clean penalties).
    no_added = ("MULTIPLE_ADDED_SUGAR_MARKERS" not in pens)
    if (len(out) < 2 and no_added and sug is not None and sug <= 5
            and "ADDITIVE_MARKERS_3_PLUS" not in caps
            and "ADDITIVE_MARKERS_5_PLUS" not in caps):
        out.append(f"סוכר נמוך — {fmt(sug)} גרם ל-100 גרם, ללא סוכר מוסף שזוהה")

    # P4 — low fat (real measured value).
    if len(out) < 2 and fat is not None and fat <= 1.5:
        out.append(f"שומן נמוך — {fmt(fat)} גרם ל-100 גרם")

    # P5 — simple base (last resort). Fires only for a genuinely clean plain yogurt
    # the engine scored without ANY additive cap or penalty — the absence of those
    # is the engine's own traced finding (NOVA3 base, no flagged additions). This
    # guarantees every clean scored product surfaces at least one truthful strength,
    # mirroring the hummus veg-base anchor. Never fires for flavored/penalized rows.
    clean = (not pens
             and "ADDITIVE_MARKERS_3_PLUS" not in caps
             and "ADDITIVE_MARKERS_5_PLUS" not in caps
             and "NOVA_PROXY_4_ULTRA_PROCESSED" not in caps)
    if not out and clean and cluster == "plain":
        out.append("בסיס יוגורט פשוט — ללא תוספי מזון או סוכר מוסף שזוהו")

    return out[:2]


def limiting_factors(L, caps, pens, cluster):
    sug = L.get("sugars_g")
    sat = L.get("fat_saturated_g")
    fat = L.get("fat_g")
    ranked = []  # (salience, phrase)

    # L1 — additive load (binding cap; names the band).
    if "ADDITIVE_MARKERS_5_PLUS" in caps:
        ranked.append((1, "חמישה תוספי מזון ומעלה ברשימה — מעבר לבסיס היוגורט"))
    elif "ADDITIVE_MARKERS_3_PLUS" in caps:
        ranked.append((1, "שלושה תוספי מזון ומעלה ברשימה — מעבר לבסיס היוגורט"))

    # L2 — added sugar (penalty fired) — pair with the measured value when present.
    if "MULTIPLE_ADDED_SUGAR_MARKERS" in pens:
        if sug is not None:
            ranked.append((2, f"סוכר מוסף זוהה — {fmt(sug)} גרם סוכר ל-100 גרם"))
        else:
            ranked.append((2, "מספר מקורות סוכר מוסף ברשימת הרכיבים"))
    elif sug is not None and sug >= 9:
        # high measured sugar even without the multi-marker penalty
        ranked.append((2, f"סוכר גבוה — {fmt(sug)} גרם ל-100 גרם"))

    # L3 — high saturated fat (measured; the C-grade greek driver). Israeli red-label
    # threshold ~ >=4g/100g for a semi-solid dairy; state the real value.
    if "ISRAELI_RED_LABEL_1_SAT_FAT" in caps or (sat is not None and sat >= 4):
        if sat is not None:
            ranked.append((3, f"שומן רווי גבוה — {fmt(sat)} גרם ל-100 גרם"))
        else:
            ranked.append((3, "שומן רווי גבוה על האריזה"))
    elif fat is not None and fat >= 6.5:
        # full-fat greek without a separate sat value present
        ranked.append((3, f"עתיר שומן לקטגוריה — {fmt(fat)} גרם שומן ל-100 גרם"))

    # L4 — long ingredient list penalty (named as list-length, not generic).
    if "LONG_INGREDIENT_LIST" in pens:
        ranked.append((4, "רשימת רכיבים ארוכה — מעבר לבסיס היוגורט"))

    best = {}
    for s, phrase in ranked:
        if phrase not in best or s < best[phrase]:
            best[phrase] = s
    return [ph for ph, _ in sorted(best.items(), key=lambda kv: kv[1])][:2]


def main():
    live = json.load(io.open(LIVE, encoding="utf-8"))
    before = {p["id"]: (p["score"], p["grade"], p["confidence"]) for p in live["products"]}

    stats = {"pos": 0, "lim": 0, "neither": 0, "n": 0}
    no_signal = []
    for p in live["products"]:
        bc = ID_BARCODE[p["id"]]
        # re-verify against imageUrl-embedded barcode (no cross-wiring)
        m = re.search(r"_(\d{6,})_\d+\.png", p["imageUrl"] or "")
        assert m and m.group(1) == bc, f"barcode mismatch for {p['id']}"
        t = load_trace(bc)
        L = t["L1_observed_signals"]
        caps = {c["rule"] for c in (t.get("caps_applied") or [])}
        pens = {x["rule"] for x in (t.get("penalties_applied") or [])}
        cluster = p.get("_cluster")
        pos = positive_signals(L, caps, pens, cluster)
        lim = limiting_factors(L, caps, pens, cluster)
        exp = p.setdefault("expansion", {})
        exp["positiveSignals"] = pos
        exp["limitingFactors"] = lim
        stats["n"] += 1
        stats["pos"] += bool(pos)
        stats["lim"] += bool(lim)
        if not pos and not lim:
            stats["neither"] += 1
            no_signal.append(p["id"])
        for arr in (pos, lim):
            for s in arr:
                for b in BANNED:
                    assert b not in s, f"banned phrase '{b}' in {p['id']}: {s}"

    after = {p["id"]: (p["score"], p["grade"], p["confidence"]) for p in live["products"]}
    assert before == after, "SCORE/GRADE/CONFIDENCE CHANGED — aborting"

    live["_meta"]["expansion"] = "interpretive_expansion_v1"
    live["_meta"].setdefault("provenance", {})["signals_task"] = "TASK-161B"
    live["_meta"]["provenance"]["signals_from"] = (
        "deterministic from run_yogurt_004 bsip2_trace.json (caps_applied/penalties_applied/L1); "
        "ingredient text NOT used (OCR bleed); engine-v2 governance"
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
