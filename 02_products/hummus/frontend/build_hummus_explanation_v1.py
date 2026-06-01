#!/usr/bin/env python3
"""
TASK-086 — Implement the TASK-085 BSIP2 -> Web Translation Contract for Hummus.

Builds hummus_frontend_v3.json = hummus_frontend_v2.json (authoritative scores,
grades, insightLines, nutrition — UNCHANGED) PLUS four deterministically-derived
explanation arrays per product, written into expansion:

    positiveSignals[]  -> "מה שבלט"           (what helped)
    limitingFactors[]  -> "מה שהגביל"          (what limited)
    unknowns[]         -> "מה שלא ניתן לאמת"   (what Bari could not verify)
    caveats[]          -> "הערות"              (product-level caveats)

DETERMINISTIC ONLY. No LLM-generated copy. Each array is a pure function of
structured BSIP2-trace + BSIP1 signals through a fixed phrase table; the same
evidence always yields byte-identical output. Re-running this script on the same
inputs reproduces the same file.

Does NOT touch: score, grade, insightLine, confidence, nutrition, ranking.
Does NOT modify BSIP2 scoring. Does NOT introduce categories.

Sources:
  - base products : C:\\Users\\HP\\bari\\src\\data\\comparisons\\hummus_frontend_v2.json (run_hummus_002)
  - additives/nut : C:\\Bari\\02_products\\hummus\\canonical_bsip1\\bsip1_*.json
  - scored signals: C:\\Bari\\02_products\\hummus\\intelligence_bsip2\\run_hummus_002\\products\\*/bsip2_trace.json
  - caveat strings: C:\\Bari\\02_products\\hummus\\hummus_content_v3.json (caveated_product_messages, short)

Contract: bsip2_to_web_translation_contract_v1.md (§3), hummus_web_readiness_rules.md (§2,§3).
"""
import json, glob, os, io, sys, datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

HERE     = os.path.dirname(os.path.abspath(__file__))
V2       = r"C:\bari\bari-web\src\data\comparisons\hummus_frontend_v2.json"
BSIP1    = r"C:\Bari\02_products\hummus\canonical_bsip1\bsip1_*.json"
TRACES   = r"C:\Bari\02_products\hummus\intelligence_bsip2\run_hummus_002\products"
CONTENT  = r"C:\Bari\02_products\hummus\hummus_content_v3.json"
OUT_WS   = os.path.join(HERE, "hummus_frontend_v3.json")
OUT_WEB  = r"C:\bari\bari-web\src\data\comparisons\hummus_frontend_v3.json"

# ── Fixed phrase table (the ONLY copy this layer emits) ───────────────────────
# Category-wide mandatory fat disclosure (mirrors methodology footer Line 3 / KL-1).
FAT_UNKNOWN  = "ערכי השומן לא היו זמינים במקור הנתונים — מדד זה לא נכלל בניתוח."
LIST_ABSENT  = "פירוט הרכיבים המלא לא היה זמין במקור הנתונים."
LIST_UNVERIF = "פירוט הרכיבים המלא לא אומת — לא ניתן לאשר נוכחות או היעדר חומר משמר."

VEG_TYPES = {"matbucha", "eggplant_spread", "pepper_spread"}

# Branded canned whole chickpeas whose ingredient text was marketing copy, not a
# verified list (TASK-064 R-2). Never assert "ללא חומר משמר" for these.
CANNED_MARKETING_IDS = {"bsip1_7290018359686", "bsip1_208428"}

def fmt(n):
    """Render a number without a trailing .0 (deterministic)."""
    if n is None:
        return None
    return str(int(n)) if float(n).is_integer() else str(round(float(n), 1))

# ── Load caveat short-strings (Nutrition-approved, content_v3) ────────────────
cmsg = json.load(open(CONTENT, encoding="utf-8"))["caveated_product_messages"]
CAV_STRUCTURAL  = cmsg["structural_emptiness"]["short"]      # ציון מבוסס על נתונים חלקיים
CAV_LOW_NOVA    = cmsg["low_nova_confidence"]["short"]       # הערכת עיבוד חלקית
CAV_ROUTING     = cmsg["category_routing_imprecise"]["short"]# סיווג חלקי — מוצג כממרח
CAV_UNAVAILABLE = cmsg["unavailable"]["short"]               # ציון לא זמין

# ── Index BSIP1 + BSIP2 ───────────────────────────────────────────────────────
b1 = {}
for f in glob.glob(BSIP1):
    d = json.load(open(f, encoding="utf-8"))
    b1[d["canonical_product_id"]] = d

def load_trace(pid):
    p = os.path.join(TRACES, pid, "bsip2_trace.json")
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None

# ── Deterministic marker extraction (structured signal, not free text) ────────
def markers(pid, rec_b1, trace):
    """Return the set of additive-kind markers and flag fields from structured data
    plus a deterministic substring scan of the declared ingredient text.

    For CANNED_MARKETING_IDS the ingredient text is marketing copy, not a verified
    list (TASK-064 R-2): we must not derive ANY additive/sugar claim from it. We
    treat the list as absent so no composition limiter or clean-list positive fires;
    the unverified-list note is surfaced in unknowns instead."""
    if pid in CANNED_MARKETING_IDS:
        return {"kinds": set(), "load": 0, "preservative": False,
                "modified_starch": False, "added_sugar": False, "has_text": False}
    text = (rec_b1.get("ingredients_text_he") or "") if rec_b1 else ""
    cats = {a.get("category") for a in (rec_b1.get("extracted_additives") or [])}
    sweet = bool(rec_b1.get("extracted_sweeteners")) if rec_b1 else False
    penalties = {p["rule"] for p in (trace.get("penalties_applied") or [])} if trace else set()

    preservative = ("חומר משמר" in text) or ("סורבט" in text) or ("בנזואט" in text) or ("preservative" in cats)
    acidity      = ("מווסת חומציות" in text) or ("acidity_regulator" in cats)
    stabilizer   = ("מייצב" in text) or ("גואר" in text) or ("קסנטן" in text) \
                   or ("stabilizer" in cats) or ("stabilizer_thickener" in cats)
    mod_starch   = ("עמילן מעובד" in text) or ("עמילן מותמר" in text)
    added_sugar  = sweet or ("MULTIPLE_ADDED_SUGAR_MARKERS" in penalties) \
                   or ("סוכר" in text) or ("סילאן" in text) or ("סירופ" in text)

    kinds = {k for k, present in (
        ("preservative", preservative), ("acidity_regulator", acidity),
        ("stabilizer", stabilizer), ("modified_starch", mod_starch),
    ) if present}
    return {
        "kinds": kinds, "load": len(kinds),
        "preservative": preservative, "modified_starch": mod_starch,
        "added_sugar": added_sugar,
        "has_text": bool(text.strip()),
    }

# ── The three translation functions (contract §3.A/B/C) ───────────────────────
VEG_BASE = {
    "matbucha":        "בסיס ירקות מבושל — עגבניות ופלפל",   # מבושל, never קלוי (TASK-064 B-6)
    "eggplant_spread": "בסיס חציל קלוי כרכיב מרכזי",
    "pepper_spread":   "בסיס פלפלים קלויים",
}

def positive_signals(rec_b1, trace, m, ptype):
    """מה שבלט — genuine, product-grounded strengths. Priority: protein, then a
    clean short list, then fiber, then low sodium; a vegetable-base anchor is used
    only as a last resort so every scored product surfaces at least one strength."""
    out = []
    nn = (rec_b1.get("normalized_nutrition_per_100g") or {}) if rec_b1 else {}
    prot, sod, fib = nn.get("protein_g"), nn.get("sodium_mg"), nn.get("dietary_fiber_g")

    # P1 — protein (legume base; median in category ≈ 7.7g)
    if prot is not None and prot >= 11:
        out.append(f"חלבון גבוה לקטגוריה — {fmt(prot)} גרם ל-100 גרם")
    elif prot is not None and prot >= 7:
        out.append(f"תכולת חלבון משמעותית לקטגוריה — {fmt(prot)} גרם ל-100 גרם")
    # P2 — clean / short additive list (only when a list actually exists; absence
    # of detected additives in a missing list is not evidence of cleanliness)
    if m["has_text"] and m["load"] == 0 and not m["added_sugar"]:
        out.append("רשימת רכיבים נקייה — ללא תוספי מזון מזוהים")
    elif m["has_text"] and m["load"] == 1 and not m["added_sugar"]:
        out.append("רשימת תוספים קצרה — תוסף מזון יחיד מעבר לבסיס")
    # P3 — dietary fiber
    if len(out) < 2 and fib is not None and fib >= 4:
        out.append(f"סיבים תזונתיים — {fmt(fib)} גרם ל-100 גרם")
    # P4 — low sodium (median ≈ 393mg)
    if len(out) < 2 and sod is not None and sod <= 250:
        out.append(f"נתרן נמוך יחסית לקטגוריה — {fmt(sod)} מ\"ג ל-100 גרם")
    # P5 — vegetable-base anchor (last resort; veg spreads are low-protein by nature)
    if not out and ptype in VEG_BASE:
        out.append(VEG_BASE[ptype])
    return out[:2]

def limiting_factors(rec_b1, trace, m, ptype):
    caps = {c["rule"] for c in (trace.get("caps_applied") or [])} if trace else set()
    pens = {p["rule"] for p in (trace.get("penalties_applied") or [])} if trace else set()
    nn = (rec_b1.get("normalized_nutrition_per_100g") or {}) if rec_b1 else {}
    sod = nn.get("sodium_mg")
    ranked = []  # (salience, phrase)

    # L1 — additive load (salience 1)
    if "ADDITIVE_MARKERS_5_PLUS" in caps or m["load"] >= 3:
        ranked.append((1, "רשימת תוספים ארוכה — מספר תוספי מזון מעבר לבסיס"))
    elif "ADDITIVE_MARKERS_3_PLUS" in caps or m["load"] == 2:
        if m["preservative"]:
            ranked.append((1, "מספר תוספי מזון ברשימה — חומר משמר ותוסף נוסף מעבר לבסיס"))
        else:
            ranked.append((1, "מספר תוספי מזון ברשימה — מעבר לרכיבי הבסיס"))
    elif m["load"] == 1 and m["preservative"]:
        # TASK-064 R-3: "חומר משמר אחד" only when total additive load is genuinely one
        ranked.append((1, "חומר משמר אחד מופיע ברשימה — תוספת בודדת על בסיס פשוט"))

    # L2 — added sugar (salience 2; strong differentiator for veg-base spreads)
    if m["added_sugar"]:
        if ptype in VEG_TYPES:
            ranked.append((2, "סוכר מצוין ברשימת הרכיבים — תוספת סוכר על בסיס ירקות"))
        else:
            ranked.append((2, "סוכר מצוין ברשימת הרכיבים"))

    # L3 — high sodium (salience 3)
    if "HIGH_SODIUM_700MG_PLUS" in caps or (sod is not None and sod >= 700):
        ranked.append((3, f"נתרן גבוה — {fmt(sod)} מ\"ג ל-100 גרם" if sod else "נתרן גבוה יחסית לקטגוריה"))

    # L4 — long ingredient list (salience 4)
    if "LONG_INGREDIENT_LIST" in pens:
        ranked.append((4, "רשימת רכיבים ארוכה ומרובת מרכיבים"))

    # L5 — modified starch (salience 5)
    if m["modified_starch"]:
        ranked.append((5, "עמילן מעובד מצוין ברשימה — לצד תוספות נוספות"))

    # L6 — processed structure (salience 6; fallback only, when nothing more specific fired)
    if not ranked and "NOVA_PROXY_3_PROCESSED" in caps:
        ranked.append((6, "מבנה רכיבים מעובד — מעבר לממרח בסיסי"))

    # dedup by phrase, keep best salience, sort, take 2
    best = {}
    for s, phrase in ranked:
        if phrase not in best or s < best[phrase]:
            best[phrase] = s
    ordered = sorted(best.items(), key=lambda kv: kv[1])
    return [phrase for phrase, _ in ordered][:2]

def unknowns(pid, rec_b1, trace, m):
    out = [FAT_UNKNOWN]  # category-wide suppression — always present on scored products
    if pid in CANNED_MARKETING_IDS:
        out.append(LIST_UNVERIF)
    elif not m["has_text"]:
        out.append(LIST_ABSENT)
    return out

def caveats(trace):
    if not trace:
        return []
    out = []
    flags = [str(x) for x in (trace.get("unresolved_flags") or [])]
    ds = trace.get("data_sufficiency")
    if any("STRUCTURAL_EMPTINESS" in f for f in flags) or ds == "partial":
        out.append(CAV_STRUCTURAL)
    if trace.get("nova_confidence_band") == "low":
        out.append(CAV_LOW_NOVA)
    if trace.get("category_instability_flag"):
        out.append(CAV_ROUTING)
    if ds == "insufficient":
        out.append(CAV_UNAVAILABLE)
    # dedup, stable order
    seen, uniq = set(), []
    for c in out:
        if c not in seen:
            seen.add(c); uniq.append(c)
    return uniq

# ── Build v3 ──────────────────────────────────────────────────────────────────
v2 = json.load(open(V2, encoding="utf-8"))
assert v2["_meta"]["source_run_id"] == "run_hummus_002", "base is not run_hummus_002"

stats = {"pos": 0, "lim": 0, "unk": 0, "cav": 0, "scored": 0, "generic_leak": 0}
GENERIC = "פרופיל הרכב טוב ביחס לקטגוריה"

for p in v2["products"]:
    pid = p["id"]
    rec = b1.get(pid, {})
    trace = load_trace(pid)
    ptype = p.get("_product_type")
    scored = p.get("score") is not None and p.get("confidence") != "insufficient"
    m = markers(pid, rec, trace)

    exp = p.setdefault("expansion", {})
    if scored:
        exp["positiveSignals"] = positive_signals(rec, trace, m, ptype)
        exp["limitingFactors"] = limiting_factors(rec, trace, m, ptype)
        exp["unknowns"]        = unknowns(pid, rec, trace, m)
        exp["caveats"]         = caveats(trace)
        stats["scored"] += 1
        stats["pos"] += bool(exp["positiveSignals"])
        stats["lim"] += bool(exp["limitingFactors"])
        stats["unk"] += bool(exp["unknowns"])
        stats["cav"] += bool(exp["caveats"])
        # Hard guarantee: at least one of positive/limiting is non-empty (contract §2.1)
        assert exp["positiveSignals"] or exp["limitingFactors"], f"no signal for scored {pid}"
    else:
        # unscored: caveat only (UI renders a dedicated insufficient branch)
        exp["positiveSignals"] = []
        exp["limitingFactors"] = []
        exp["unknowns"]        = []
        exp["caveats"]         = caveats(trace) or [CAV_UNAVAILABLE]

    # Guarantee no generic fallback text was ever baked into a string field
    for field in ("insightLine",):
        if GENERIC in (p.get(field) or ""):
            stats["generic_leak"] += 1
    for arr in (exp["positiveSignals"], exp["limitingFactors"], exp["unknowns"], exp["caveats"]):
        assert GENERIC not in " ".join(arr), f"generic fallback leaked into arrays for {pid}"

# ── Meta ────────────────────────────────────────────────────────────────────
v2["_meta"]["version"] = "v3-explanation-layer"
v2["_meta"]["explanation_task"] = "TASK-086"
v2["_meta"]["explanation_contract"] = "bsip2_to_web_translation_contract_v1.md"
v2["_meta"]["generated"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
v2["_meta"]["explanation_layer"] = {
    "deterministic": True,
    "source_signals": ["caps_applied", "penalties_applied", "extracted_additives",
                       "extracted_sweeteners", "protein_g", "sodium_mg",
                       "nova_confidence_band", "data_sufficiency", "unresolved_flags"],
    "arrays": ["positiveSignals", "limitingFactors", "unknowns", "caveats"],
    "fat_disclosure": FAT_UNKNOWN,
    "coverage": stats,
}

for path in (OUT_WS, OUT_WEB):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(v2, f, ensure_ascii=False, indent=2)

print("Written:")
print(" ", OUT_WS)
print(" ", OUT_WEB)
print(f"scored {stats['scored']} | with positive {stats['pos']} | with limiting {stats['lim']} "
      f"| with unknowns {stats['unk']} | with caveats {stats['cav']}")
print(f"generic fallback leaks: {stats['generic_leak']} (must be 0)")
