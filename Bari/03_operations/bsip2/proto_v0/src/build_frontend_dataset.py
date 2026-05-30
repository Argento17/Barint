"""
Frontend Dataset Builder — Real Bread Retail 002 v2 (Shufersal)

Reads  : BSIP2 per-product JSONs  (bsip2/*.json)
         Raw BSIP0 JSON           (for ingredient text, barcode-matched)
Writes : real_bread_retail_002_v2_frontend_dataset.json
         frontend_dataset_schema.md
         frontend_dataset_examples.md
"""

from __future__ import annotations
import sys, json, re, pathlib, datetime
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BSIP2_DIR  = pathlib.Path(r"C:\Bari\02_products\bread_retail_002\bsip2")
RAW_JSON   = pathlib.Path(r"C:\Bari\02_products\bread_retail_002\real_bread_retail_002_v2_20260525T165557_bsip0_raw.json")
OUT_DIR    = pathlib.Path(r"C:\Bari\02_products\bread_retail_002")
RUN_ID     = "real_bread_retail_002_v2"
TODAY      = "2026-05-25"

# ─── signal keyword banks ──────────────────────────────────────────────────────

FERM_REAL_KW  = ["מחמצת","שאור","תרבויות","חיידקים","חומצה לקטית","lactobacillus","sourdough"]
FERM_IND_KW   = ["שמרים"]
MATRIX_KW     = ["אינולין","inulin","psyllium","פסיליום","ציקוריה","chicory",
                  "cellulose","צלולוז","גואר","קסנטן","xanthan"]
WG_KW         = ["קמח מלא","שיפון מלא","חיטה מלאה","כוסמין מלא",
                  "wholegrain","whole grain","whole wheat","100% כוסמין",
                  "100% שיפון","100%שיפון"]
SEED_KW       = ["שומשום","פשתן","דלעת","גרעיני","זרעי","צ'יה","chia",
                  "sunflower","sesame","pumpkin","flax","כוסמת","אמרנט"]
REFINED_KW    = ["קמח חיטה","קמח לבן","white flour","wheat flour"]

CATEGORY_LABELS_HE = {
    "bread":           "לחם",
    "cracker":         "קרקר",
    "crispbread":      "לחמית",
    "pita":            "פיתה",
    "default":         "מוצר אפייה",
    "snack_bar_granola": "גרנולה / חטיף",
}

CONF_LEVEL_MAP = {
    "FULL":        "verified",
    "CAUTIOUS":    "verified",
    "UNCERTAINTY": "partial",
    "INSUFFICIENT": "insufficient",
}

# ─── signal computation ────────────────────────────────────────────────────────

def _ing(r: dict) -> str:
    return (r.get("ingredients_text") or "").lower()

def _name(r: dict) -> str:
    return (r.get("name_he") or "").lower()

def signal_fermentation_real(r: dict) -> bool:
    """
    Genuine fermentation: מחמצת/שאור present in ingredients, without a name-claim mismatch.
    Matches batch_run logic exactly:
    - has_real AND NOT has_ind → genuine (pure starter)
    - has_real AND has_ind, no name claim → genuine (starter + yeast assist, no misleading claim)
    - name claim AND has_ind → mismatch (NOT genuine)
    """
    ing      = _ing(r)
    name     = _name(r)
    if not ing:
        return False
    has_real  = any(kw in ing for kw in FERM_REAL_KW)
    has_ind   = "שמרים" in ing
    has_claim = "מחמצת" in name
    if not (has_claim or has_real):
        return False
    if has_real and not has_ind:
        return True   # pure starter, no industrial yeast
    elif has_claim and has_ind:
        return False  # name claims sourdough but yeast is primary leavener → mismatch
    else:
        return True   # has_real + has_ind, no name claim → genuine with yeast assist

def signal_fermentation_mismatch(r: dict) -> bool:
    """Name claims מחמצת but שמרים (industrial yeast) appears in ingredient text."""
    name = _name(r)
    ing  = _ing(r)
    has_claim = "מחמצת" in name
    has_ind   = "שמרים" in ing
    return bool(ing) and has_claim and has_ind

def signal_fiber_laundering(r: dict) -> bool:
    ing   = _ing(r)
    fiber = (r.get("nutrition") or {}).get("dietary_fiber_g")
    return bool(ing) and fiber is not None and fiber >= 5 and any(kw in ing for kw in MATRIX_KW)

def signal_seed_halo(r: dict) -> bool:
    ing  = _ing(r)
    name = _name(r)
    has_seeds = any(kw in ing or kw in name for kw in SEED_KW)
    has_wg    = any(kw in ing for kw in WG_KW)
    return bool(ing) and has_seeds and not has_wg

def signal_whole_grain(r: dict) -> bool:
    ing  = _ing(r)
    name = _name(r)
    return any(kw in ing or kw in name for kw in WG_KW)

def signal_refined_base(r: dict) -> bool:
    ing = _ing(r)
    return bool(ing) and any(kw in ing for kw in REFINED_KW) and not signal_whole_grain(r)

def signal_high_sodium(r: dict) -> bool:
    na = (r.get("nutrition") or {}).get("sodium_mg")
    return na is not None and na > 600

def signal_rye(r: dict) -> bool:
    ing  = _ing(r)
    name = _name(r)
    return "שיפון" in ing or "שיפון" in name

def signal_spelt(r: dict) -> bool:
    ing  = _ing(r)
    name = _name(r)
    return "כוסמין" in ing or "כוסמין" in name

def compute_ingredient_visibility(r: dict) -> str:
    has_ing  = bool(r.get("ingredients_text"))
    has_nutr = (r.get("nutrition") or {}).get("energy_kcal") is not None
    if has_ing and has_nutr: return "full"
    if has_ing or has_nutr:  return "partial"
    return "none"

def compute_key_flags(r: dict) -> list[str]:
    flags = []
    if signal_whole_grain(r):        flags.append("גרעינים מלאים")
    if signal_fermentation_real(r):  flags.append("מחמצת אמיתית")
    if signal_fermentation_mismatch(r): flags.append("שם מחמצת / שמרים בפועל")
    if signal_fiber_laundering(r):   flags.append("סיבים מוספים")
    if signal_seed_halo(r):          flags.append("זרעים על בסיס מזוקק")
    if signal_high_sodium(r):        flags.append("נתרן גבוה")
    fiber = (r.get("nutrition") or {}).get("dietary_fiber_g")
    if fiber is not None and fiber >= 8: flags.append("סיבים גבוהים במיוחד")
    elif fiber is not None and fiber >= 5: flags.append("סיבים גבוהים")
    if signal_rye(r):   flags.append("שיפון")
    if signal_spelt(r): flags.append("כוסמין")
    return flags

def compute_comparison_tags(r: dict) -> list[str]:
    tags = []
    cat = r.get("category","")
    tags.append(cat)
    if signal_fermentation_real(r):   tags.append("fermentation_real")
    if signal_fermentation_mismatch(r): tags.append("fermentation_mismatch")
    if signal_whole_grain(r):         tags.append("whole_grain")
    if signal_refined_base(r):        tags.append("refined_base")
    if signal_fiber_laundering(r):    tags.append("fiber_laundering")
    if signal_seed_halo(r):           tags.append("seed_halo")
    if signal_rye(r):                 tags.append("rye")
    if signal_spelt(r):               tags.append("spelt")
    fiber = (r.get("nutrition") or {}).get("dietary_fiber_g")
    if fiber is not None:
        if fiber >= 8:  tags.append("high_fiber")
        elif fiber < 3: tags.append("low_fiber")
    if r.get("degradation_level") in ("FULL","CAUTIOUS") and r.get("ingredients_text"):
        tags.append("verified")
    return tags

def compute_ingredient_architecture(r: dict) -> str:
    ing  = _ing(r)
    name = _name(r)
    if not ing:
        return "רשימת רכיבים לא זמינה"
    parts = []
    # Base
    if signal_whole_grain(r):
        if "שיפון מלא" in ing: parts.append("קמח שיפון מלא")
        elif "כוסמין מלא" in ing or "כוסמין" in name: parts.append("קמח כוסמין מלא")
        elif "קמח מלא" in ing: parts.append("קמח חיטה מלא")
        else: parts.append("בסיס דגן מלא")
    else:
        if "שיפון" in ing: parts.append("קמח שיפון")
        elif "קמח חיטה" in ing or "white flour" in ing: parts.append("קמח חיטה לבן")
        else: parts.append("קמח")
    # Leavening
    if signal_fermentation_real(r): parts.append("מחמצת")
    elif any(kw in ing for kw in FERM_IND_KW): parts.append("שמרים")
    # Seeds
    found_seeds = [kw for kw in ["שומשום","פשתן","דלעת","זרעי"] if kw in ing]
    if found_seeds: parts.append(" ".join(found_seeds[:2]))
    # Fiber additives
    if signal_fiber_laundering(r):
        found_add = [kw for kw in MATRIX_KW if kw in ing]
        if found_add: parts.append(f"+ {found_add[0]} (סיב מוסף)")
    return " · ".join(parts)

def compute_short_summary_he(r: dict) -> str:
    cat   = CATEGORY_LABELS_HE.get(r.get("category",""), "מוצר אפייה")
    fiber = (r.get("nutrition") or {}).get("dietary_fiber_g")
    score = r.get("final_score")
    deg   = r.get("degradation_level","")
    name  = r.get("name_he","")

    if deg == "INSUFFICIENT":
        return f"{cat} — אין מספיק נתונים לניתוח ודאי."

    lines = []
    # Fermentation note
    if signal_fermentation_real(r) and not signal_fermentation_mismatch(r):
        lines.append("מחמצת מאומתת ברשימת הרכיבים.")
    elif signal_fermentation_mismatch(r):
        lines.append("שם המוצר כולל 'מחמצת' — שמרים תעשייתיים הם המתפיח הראשי.")

    # Whole grain / base
    if signal_whole_grain(r):
        if "שיפון" in (r.get("name_he","") + _ing(r)):
            lines.append("עשוי מקמח שיפון מלא.")
        elif "כוסמין" in (r.get("name_he","") + _ing(r)):
            lines.append("עשוי מקמח כוסמין מלא.")
        else:
            lines.append("עשוי מקמח מלא.")
    elif signal_refined_base(r):
        lines.append("בסיס קמח לבן מזוקק.")

    # Fiber note
    if fiber is not None:
        if fiber >= 10:
            lines.append(f"תכולת סיבים גבוהה במיוחד — {fiber:.1f}g ל-100g.")
        elif fiber >= 6:
            lines.append(f"סיבים: {fiber:.1f}g ל-100g.")

    # Laundering / seed halo
    if signal_fiber_laundering(r):
        lines.append("חלק מהסיבים מקורם בתוספות (אינולין / ציקוריה).")
    elif signal_seed_halo(r):
        lines.append("זרעים על גבי בסיס מזוקק — אפקט אופטי בלבד.")

    if not lines:
        return f"{cat} — ציון {int(score) if score else '—'}."

    return " ".join(lines)

# ─── displayability ────────────────────────────────────────────────────────────

def is_displayable(r: dict) -> bool:
    return (
        r.get("degradation_level") in ("FULL","CAUTIOUS")
        and bool(r.get("ingredients_text"))
    )

def _first_img(r: dict) -> str:
    imgs = r.get("image_urls") or []
    return imgs[0] if imgs else ""

# ─── load data ─────────────────────────────────────────────────────────────────

def load_all() -> list[dict]:
    # Load BSIP2 per-product JSONs
    bsip2_files = sorted(BSIP2_DIR.glob("bsip2_shufersal_*.json"))
    bsip2 = {}
    for f in bsip2_files:
        d = json.loads(f.read_text(encoding="utf-8"))
        bc = str(d.get("barcode",""))
        bsip2[bc] = d

    # Load raw BSIP0 for ingredients text
    raw_products = json.loads(RAW_JSON.read_text(encoding="utf-8"))
    raw_by_bc = {}
    for rp in raw_products:
        bc = str(rp.get("barcode",""))
        if bc:
            raw_by_bc[bc] = rp

    # Merge
    products = []
    for bc, b in bsip2.items():
        raw = raw_by_bc.get(bc, {})
        merged = dict(b)
        merged["ingredients_text"] = (raw.get("ingredients_raw") or "").strip()
        products.append(merged)

    return products

# ─── build sections ────────────────────────────────────────────────────────────

def build_product_record(r: dict) -> dict:
    nutr  = r.get("nutrition") or {}
    fiber = nutr.get("dietary_fiber_g")
    prot  = nutr.get("protein_g")
    na    = nutr.get("sodium_mg")
    score = r.get("final_score")
    grade = r.get("final_grade")
    deg   = r.get("degradation_level","INSUFFICIENT")
    disp  = is_displayable(r)

    return {
        "id":                             r.get("product_id",""),
        "name_he":                        r.get("name_he",""),
        "category":                       r.get("category",""),
        "category_label_he":              CATEGORY_LABELS_HE.get(r.get("category",""),"מוצר אפייה"),
        "score":                          round(score) if (score is not None and disp) else None,
        "grade":                          grade if disp else None,
        "displayable":                    disp,
        "confidence_label_he":            r.get("confidence_label_he","לא מספיק לניתוח ודאי"),
        "confidence_level":               CONF_LEVEL_MAP.get(deg,"insufficient"),
        "fiber_g":                        round(fiber, 1) if fiber is not None else None,
        "protein_g":                      round(prot, 1) if prot is not None else None,
        "sodium_mg":                      round(na, 0) if na is not None else None,
        "energy_kcal":                    round(nutr.get("energy_kcal", 0) or 0) if nutr.get("energy_kcal") is not None else None,
        "fermentation_real":              signal_fermentation_real(r),
        "fermentation_mismatch":          signal_fermentation_mismatch(r),
        "fiber_laundering":               signal_fiber_laundering(r),
        "seed_halo":                      signal_seed_halo(r),
        "whole_grain":                    signal_whole_grain(r),
        "ingredient_visibility":          compute_ingredient_visibility(r),
        "image_url":                      _first_img(r),
        "source_url":                     r.get("source_url",""),
        "key_flags":                      compute_key_flags(r),
        "short_summary_he":               compute_short_summary_he(r),
        "ingredient_architecture_summary": compute_ingredient_architecture(r),
        "comparison_tags":                compute_comparison_tags(r),
    }

def build_featured_product(r: dict, p: dict) -> dict:
    return {
        "id":                   p["id"],
        "name_he":              p["name_he"],
        "category":             p["category"],
        "category_label_he":    p["category_label_he"],
        "score":                p["score"],
        "grade":                p["grade"],
        "confidence_label_he":  p["confidence_label_he"],
        "image_url":            p["image_url"],
        "source_url":           p["source_url"],
        "fiber_g":              p["fiber_g"],
        "fermentation_real":    p["fermentation_real"],
        "key_flags":            p["key_flags"],
        "short_summary_he":     p["short_summary_he"],
        "ingredient_architecture_summary": p["ingredient_architecture_summary"],
    }

def build_comparisons(products: list[dict], recs: list[dict]) -> list[dict]:

    def find_best(match_fn, exclude_fn=None) -> dict | None:
        candidates = [
            p for p in products
            if p["displayable"] and match_fn(p)
            and (exclude_fn is None or not exclude_fn(p))
            and p["score"] is not None
        ]
        if not candidates: return None
        return max(candidates, key=lambda x: x["score"])

    def find_worst(match_fn, exclude_fn=None) -> dict | None:
        candidates = [
            p for p in products
            if p["displayable"] and match_fn(p)
            and (exclude_fn is None or not exclude_fn(p))
            and p["score"] is not None
            and p.get("fiber_g") is not None
        ]
        if not candidates: return None
        return min(candidates, key=lambda x: x["fiber_g"] or 999)

    comps = []

    # 1. Genuine fermentation vs industrial yeast (rye breads)
    real_ferm_rye = find_best(
        lambda p: p["fermentation_real"] and "rye" in p["comparison_tags"],
    )
    ind_yeast_rye = find_best(
        lambda p: "rye" in p["comparison_tags"] and not p["fermentation_real"] and not p["fermentation_mismatch"],
        exclude_fn=lambda p: p["fermentation_real"],
    )
    if real_ferm_rye and ind_yeast_rye and real_ferm_rye["id"] != ind_yeast_rye["id"]:
        comps.append({
            "id": "comp_fermentation_rye",
            "title": "מחמצת ברכיבים לעומת שמרים בלבד — לחם שיפון",
            "narrative": "שני לחמי שיפון ממדף שופרסל. האחד כולל מחמצת ברשימת הרכיבים (לא רק בשם). השני מתפיח עם שמרים תעשייתיים בלבד. ההבדל לא בשם — אלא ברכיבים.",
            "left_product_id":  real_ferm_rye["id"],
            "right_product_id": ind_yeast_rye["id"],
            "key_difference": "מחמצת ברכיבים לעומת שמרים בלבד",
            "visual_direction": "left_wins",
        })

    # 2. Fermentation name claim vs genuine (no claim)
    mismatch_p = find_best(lambda p: p["fermentation_mismatch"])
    genuine_p  = find_best(
        lambda p: p["fermentation_real"] and not p["fermentation_mismatch"],
    )
    if mismatch_p and genuine_p and mismatch_p["id"] != genuine_p["id"]:
        comps.append({
            "id": "comp_fermentation_claim",
            "title": "'מחמצת' בשם לעומת מחמצת ברכיבים",
            "narrative": "מוצר אחד נושא את השם 'מחמצת' אך השמרים התעשייתיים הם המתפיח הראשי. המוצר השני אינו מציין 'מחמצת' בשמו — אך הרכיבים כוללים אותה בפועל.",
            "left_product_id":  genuine_p["id"],
            "right_product_id": mismatch_p["id"],
            "key_difference": "מחמצת בפועל לעומת שמרים תעשייתיים עם שם מטעה",
            "visual_direction": "left_wins",
        })

    # 3. High fiber natural vs low fiber (verified only)
    hi_fiber = find_best(
        lambda p: p["whole_grain"] and p["fiber_g"] is not None and p["fiber_g"] >= 8,
        exclude_fn=lambda p: p["fiber_laundering"],
    )
    lo_fiber = find_worst(
        lambda p: p["displayable"],
    )
    if hi_fiber and lo_fiber and hi_fiber["id"] != lo_fiber["id"]:
        comps.append({
            "id": "comp_fiber_extremes",
            "title": "פער הסיבים — עד 10× הבדל על אותו מדף",
            "narrative": "שני מוצרים ממדף שופרסל עם תכולת סיבים שונה לחלוטין. הסיבים הגבוהים מגיעים ישירות מבסיס דגנים מלאים — לא מתוספות.",
            "left_product_id":  hi_fiber["id"],
            "right_product_id": lo_fiber["id"],
            "key_difference": f"{hi_fiber['fiber_g']}g לעומת {lo_fiber['fiber_g']}g סיבים ל-100g",
            "visual_direction": "left_wins",
        })

    # 4. Spelt crackers — top two by score
    spelt_crackers = sorted(
        [p for p in products if p["displayable"] and "cracker" in p["comparison_tags"]
         and "spelt" in p["comparison_tags"] and p["score"] is not None],
        key=lambda x: x["score"], reverse=True
    )
    if len(spelt_crackers) >= 2:
        comps.append({
            "id": "comp_spelt_crackers",
            "title": "קרקרי כוסמין: לא כולם שווים",
            "narrative": "שני קרקרי כוסמין ממדף שופרסל — שניהם עם שם דומה, ציון שונה. ההבדל בתכולת הסיבים ובמבנה הרכיבים.",
            "left_product_id":  spelt_crackers[0]["id"],
            "right_product_id": spelt_crackers[1]["id"],
            "key_difference": f"ציון {spelt_crackers[0]['score']} לעומת {spelt_crackers[1]['score']}",
            "visual_direction": "left_wins",
        })

    # 5. Fiber laundering vs natural whole grain fiber
    fib_laund = find_best(lambda p: p["fiber_laundering"])
    nat_fiber  = find_best(
        lambda p: p["whole_grain"] and p["fiber_g"] is not None and p["fiber_g"] >= 6,
        exclude_fn=lambda p: p["fiber_laundering"],
    )
    if fib_laund and nat_fiber and fib_laund["id"] != nat_fiber["id"]:
        comps.append({
            "id": "comp_fiber_laundering",
            "title": "סיבים טבעיים מדגן מלא לעומת תוספות סיבים",
            "narrative": "שני מוצרים בעלי תכולת סיבים גבוהה — אך ממקורות שונים. האחד מכיל סיבים מדגנים מלאים; השני מוסיף סיבים בודדים (אינולין / ציקוריה) לבסיס מזוקק.",
            "left_product_id":  nat_fiber["id"],
            "right_product_id": fib_laund["id"],
            "key_difference": "סיבים מדגן מלא לעומת תוספות סיבים בודדות",
            "visual_direction": "left_wins",
        })

    return comps

def build_insights(products: list[dict], recs: list[dict]) -> dict:
    all_p    = products
    verified = [p for p in all_p if p["displayable"]]
    n        = len(all_p)
    nv       = len(verified)

    fibers_v = [p["fiber_g"] for p in verified if p["fiber_g"] is not None]
    avg_fiber_v = round(sum(fibers_v)/len(fibers_v), 1) if fibers_v else None

    ferm_real     = sum(1 for p in verified if p["fermentation_real"])
    ferm_mismatch = sum(1 for p in all_p   if p["fermentation_mismatch"])
    industrial    = sum(1 for p in verified if not p["fermentation_real"] and not p["fermentation_mismatch"])
    seed_halo_n   = sum(1 for p in all_p   if p["seed_halo"])
    fiber_laund_n = sum(1 for p in all_p   if p["fiber_laundering"])
    whole_grain_n = sum(1 for p in verified if p["whole_grain"])
    high_sod_n    = sum(1 for p in verified if p["sodium_mg"] is not None and p["sodium_mg"] > 600)

    deg_dist = {}
    for p in all_p:
        lvl = "verified" if p["confidence_level"] == "verified" else p["confidence_level"]
        deg_dist[lvl] = deg_dist.get(lvl, 0) + 1

    grade_dist = {}
    for p in verified:
        g = p.get("grade","?") or "?"
        grade_dist[g] = grade_dist.get(g, 0) + 1

    # Fiber extremes (verified only)
    with_fiber = [p for p in verified if p["fiber_g"] is not None]
    top_fiber = sorted(with_fiber, key=lambda x: x["fiber_g"], reverse=True)[:3]
    bot_fiber = sorted(with_fiber, key=lambda x: x["fiber_g"])[:3]

    return {
        "fermentation": {
            "headline_he": f"מתוך {nv} מוצרים מאומתים, {ferm_real} כוללים מחמצת אמיתית ברשימת הרכיבים.",
            "genuine_count": ferm_real,
            "mismatch_count": ferm_mismatch,
            "industrial_only_count": industrial,
            "verified_base": nv,
            "note_he": f"{ferm_mismatch} מוצרים נושאים את השם 'מחמצת' אך כוללים שמרים תעשייתיים ברשימת הרכיבים.",
        },
        "fiber": {
            "headline_he": f"ממוצע סיבים במוצרים מאומתים: {avg_fiber_v}g ל-100g.",
            "avg_fiber_verified": avg_fiber_v,
            "high_fiber_count": sum(1 for p in verified if p["fiber_g"] is not None and p["fiber_g"] >= 6),
            "very_high_fiber_count": sum(1 for p in verified if p["fiber_g"] is not None and p["fiber_g"] >= 10),
            "top_fiber_products": [{"id": p["id"], "name_he": p["name_he"], "fiber_g": p["fiber_g"]} for p in top_fiber],
            "lowest_fiber_products": [{"id": p["id"], "name_he": p["name_he"], "fiber_g": p["fiber_g"]} for p in bot_fiber],
            "note_he": "הסיבים בחלק מהמוצרים מגיעים מתוספות בודדות (אינולין, ציקוריה) — לא מבסיס דגן מלא.",
        },
        "seed_halo": {
            "headline_he": f"{seed_halo_n} מוצרים מכילים זרעים על גבי בסיס קמח מזוקק.",
            "affected_count": seed_halo_n,
            "total_base": n,
            "note_he": "זרעים על גבי קמח לבן יוצרים רושם בריאותי מבלי לשנות את מבנה הקמח הבסיסי.",
        },
        "fiber_laundering": {
            "headline_he": f"{fiber_laund_n} מוצרים בעלי סיבים גבוהים כוללים תוספות סיבים בודדות.",
            "affected_count": fiber_laund_n,
            "note_he": "סיב תזונתי מוסף (אינולין, ציקוריה, פסיליום) אינו שקול לסיב הטבעי שבדגן מלא.",
        },
        "transparency": {
            "headline_he": f"רק {nv} מתוך {n} מוצרים כוללים גם לוח תזונה וגם רשימת רכיבים.",
            "verified_count": nv,
            "total_count": n,
            "no_data_count": sum(1 for p in all_p if p["ingredient_visibility"] == "none"),
            "note_he": "מוצרים ללא רשימת רכיבים אינם נכנסים לניתוח מלא — הציון שלהם אינו ודאי.",
        },
        "confidence_distribution": {
            "verified": deg_dist.get("verified", 0),
            "partial": deg_dist.get("partial", 0),
            "insufficient": deg_dist.get("insufficient", 0),
        },
        "grade_distribution_verified": grade_dist,
        "whole_grain": {
            "headline_he": f"{whole_grain_n} מתוך {nv} מוצרים מאומתים עשויים מדגנים מלאים.",
            "count": whole_grain_n,
            "verified_base": nv,
        },
        "sodium": {
            "headline_he": f"{high_sod_n} מוצרים מאומתים מכילים נתרן גבוה (מעל 600mg/100g).",
            "high_sodium_count": high_sod_n,
        },
    }

def build_homepage_sections(products: list[dict]) -> dict:
    verified = [p for p in products if p["displayable"]]
    sorted_v = sorted(verified, key=lambda x: x["score"] or 0, reverse=True)

    strongest_verified = [
        {"id": p["id"], "name_he": p["name_he"], "score": p["score"],
         "grade": p["grade"], "category_label_he": p["category_label_he"],
         "image_url": p["image_url"], "confidence_label_he": p["confidence_label_he"],
         "short_summary_he": p["short_summary_he"], "key_flags": p["key_flags"]}
        for p in sorted_v[:8]
    ]

    interesting_patterns = []
    for p in products:
        if p["fiber_laundering"] or p["seed_halo"] or p["fermentation_mismatch"]:
            interesting_patterns.append({
                "id": p["id"], "name_he": p["name_he"],
                "pattern": (
                    "fiber_laundering" if p["fiber_laundering"] else
                    "seed_halo"        if p["seed_halo"] else
                    "fermentation_mismatch"
                ),
                "short_summary_he": p["short_summary_he"],
                "image_url": p["image_url"],
                "source_url": p["source_url"],
            })

    fermentation_examples = {
        "genuine": [
            {"id": p["id"], "name_he": p["name_he"], "score": p["score"],
             "image_url": p["image_url"], "short_summary_he": p["short_summary_he"]}
            for p in sorted_v if p["fermentation_real"] and not p["fermentation_mismatch"]
        ][:6],
        "mismatch": [
            {"id": p["id"], "name_he": p["name_he"], "score": p["score"],
             "image_url": p["image_url"], "short_summary_he": p["short_summary_he"]}
            for p in products if p["fermentation_mismatch"] and p["displayable"]
        ][:6],
    }

    fiber_spectrum = {
        "high_end": [
            {"id": p["id"], "name_he": p["name_he"], "fiber_g": p["fiber_g"],
             "score": p["score"], "image_url": p["image_url"]}
            for p in sorted(verified, key=lambda x: x["fiber_g"] or 0, reverse=True)
            if p["fiber_g"] is not None
        ][:5],
        "low_end": [
            {"id": p["id"], "name_he": p["name_he"], "fiber_g": p["fiber_g"],
             "score": p["score"], "image_url": p["image_url"]}
            for p in sorted(verified, key=lambda x: x["fiber_g"] or 999)
            if p["fiber_g"] is not None
        ][:5],
    }

    structural_examples = {
        "whole_grain_strong": [
            {"id": p["id"], "name_he": p["name_he"], "score": p["score"],
             "ingredient_architecture_summary": p["ingredient_architecture_summary"],
             "image_url": p["image_url"]}
            for p in sorted_v if p["whole_grain"] and not p["fiber_laundering"]
        ][:5],
        "refined_base": [
            {"id": p["id"], "name_he": p["name_he"], "score": p["score"],
             "ingredient_architecture_summary": p["ingredient_architecture_summary"],
             "image_url": p["image_url"]}
            for p in sorted(verified, key=lambda x: x["score"] or 0)
            if not p["whole_grain"] and p["ingredient_visibility"] == "full"
        ][:5],
    }

    return {
        "strongest_verified":   strongest_verified,
        "interesting_patterns": interesting_patterns[:10],
        "fermentation_examples": fermentation_examples,
        "fiber_spectrum":       fiber_spectrum,
        "structural_examples":  structural_examples,
        "blog_titles_he": [
            "מה יש בלחם מהמדף? ניתחנו 108 מוצרים משופרסל",
            "לחם, פיתה וקרקרים: מה הציון שלנו ומה הוא לא יכול לומר",
            "שקיפות בלחם: ניתוח נתוני מדף אמיתי מרשת שופרסל",
            "מחמצת אמיתית לעומת שמרים: מה שמסתתר מאחורי השם",
        ],
        "mandatory_framing_he": (
            "ניתחנו 108 מוצרי לחם, פיתה וקרקרים ממדף שופרסל. "
            "32 מוצרים עמדו בסף הנתונים הנדרש לניתוח מלא. "
            "זהו ניתוח של מדף שופרסל בלבד — לא סקר שוק ישראלי מלא."
        ),
        "mandatory_framing_en": (
            "We analyzed 108 bread, pita and cracker products from a real Shufersal shelf. "
            "32 products had sufficient data for reliable scoring. "
            "This is a Shufersal shelf snapshot — not a full Israeli market survey."
        ),
    }

# ─── schema doc ───────────────────────────────────────────────────────────────

SCHEMA_MD = """\
# Frontend Dataset Schema — real_bread_retail_002_v2

**File:** `real_bread_retail_002_v2_frontend_dataset.json`
**Source:** Shufersal real-shelf scrape → BSIP0 → BSIP1 → BSIP2 pipeline
**Date:** 2026-05-25

This file is the ONLY frontend truth source for Cursor. Do not read raw BSIP2 reports directly.

---

## Top-Level Structure

```json
{
  "dataset_meta":      {},   // corpus metadata and caveats
  "featured_products": [],   // 10–15 curated display-safe products
  "products":          [],   // all 108 in-scope products (full schema)
  "comparisons":       [],   // pre-built comparison pairs
  "insights":          {},   // verified statistics for UI widgets
  "homepage_sections": {}    // pre-grouped product sets for page rendering
}
```

---

## dataset_meta

| Field | Type | Description |
|:------|:-----|:------------|
| `run_id` | string | Pipeline run identifier |
| `snapshot_date` | string | ISO date of scrape |
| `source_retailer` | string | Retailer name (Hebrew) |
| `source_retailer_en` | string | Retailer name (English) |
| `total_scraped` | int | Raw products scraped from Shufersal |
| `in_scope` | int | Products entering scoring pipeline |
| `excluded` | int | Out-of-scope products removed |
| `verified_products` | int | Products with full nutrition + ingredients |
| `nutrition_coverage_pct` | int | % products with nutrition data |
| `ingredient_coverage_pct` | int | % products with ingredient text |
| `avg_fiber_verified` | float | Average fiber in verified products (g/100g) |
| `caveats` | string[] | Mandatory display caveats |
| `mandatory_framing_he` | string | Hebrew required framing text |
| `mandatory_framing_en` | string | English required framing text |

---

## products[] — per-product fields

| Field | Type | Description |
|:------|:-----|:------------|
| `id` | string | Canonical product ID (`shufersal_<barcode>`) |
| `name_he` | string | Hebrew product name from Shufersal |
| `category` | string | Router category: `bread`, `cracker`, `crispbread`, `default` |
| `category_label_he` | string | Display label in Hebrew |
| `score` | int\\|null | BSIP2 score (0–100). Null if not displayable |
| `grade` | string\\|null | Letter grade A–E. Null if INSUFFICIENT |
| `displayable` | bool | True if CAUTIOUS/FULL degradation + ingredient text |
| `confidence_label_he` | string | Always set: נתונים חלקיים / חסרים נתונים מהותיים / לא מספיק לניתוח ודאי |
| `confidence_level` | string | `verified`, `partial`, or `insufficient` |
| `fiber_g` | float\\|null | Dietary fiber per 100g |
| `protein_g` | float\\|null | Protein per 100g |
| `sodium_mg` | float\\|null | Sodium per 100g in mg |
| `energy_kcal` | int\\|null | Energy per 100g in kcal |
| `fermentation_real` | bool | Genuine fermentation detected in ingredients |
| `fermentation_mismatch` | bool | Name claims מחמצת but ingredients show industrial yeast |
| `fiber_laundering` | bool | Fiber ≥5g but sourced from isolated additives |
| `seed_halo` | bool | Seeds present but no whole grain base |
| `whole_grain` | bool | Whole grain keywords detected in ingredients |
| `ingredient_visibility` | string | `full`, `partial`, or `none` |
| `image_url` | string | Primary Shufersal Cloudinary image URL |
| `source_url` | string | Direct Shufersal product page URL |
| `key_flags` | string[] | Human-readable Hebrew flags for display |
| `short_summary_he` | string | 1–3 sentence consumer-facing Hebrew summary |
| `ingredient_architecture_summary` | string | Brief Hebrew description of ingredient structure |
| `comparison_tags` | string[] | Tags for comparison grouping logic |

---

## featured_products[]

Subset of top-scored displayable products. Fields: `id`, `name_he`, `category`,
`category_label_he`, `score`, `grade`, `confidence_label_he`, `image_url`, `source_url`,
`fiber_g`, `fermentation_real`, `key_flags`, `short_summary_he`,
`ingredient_architecture_summary`.

Only `displayable=true` products appear here.

---

## comparisons[]

| Field | Type | Description |
|:------|:-----|:------------|
| `id` | string | Comparison identifier |
| `title` | string | Hebrew title for comparison card |
| `narrative` | string | Hebrew explanatory text |
| `left_product_id` | string | Product ID (usually the "better" example) |
| `right_product_id` | string | Product ID (the contrast) |
| `key_difference` | string | Single-line summary of the difference |
| `visual_direction` | string | `left_wins`, `right_wins`, or `neutral` |

---

## insights{}

Sub-objects:
- `fermentation` — genuine count, mismatch count, industrial count
- `fiber` — average, extremes, top/bottom product IDs
- `seed_halo` — count, narrative
- `fiber_laundering` — count, narrative
- `transparency` — verified vs total, no-data count
- `confidence_distribution` — verified/partial/insufficient counts
- `grade_distribution_verified` — A/B/C/D counts for verified products
- `whole_grain` — count of verified whole-grain products
- `sodium` — high sodium product count

All numbers are derived from real data. Safe to display.

---

## homepage_sections{}

| Key | Description |
|:----|:------------|
| `strongest_verified` | Top 8 verified products — for homepage hero / ranking widget |
| `interesting_patterns` | Products with fiber_laundering / seed_halo / fermentation_mismatch |
| `fermentation_examples` | `genuine[]` and `mismatch[]` product lists |
| `fiber_spectrum` | `high_end[]` and `low_end[]` — for fiber range visualization |
| `structural_examples` | `whole_grain_strong[]` and `refined_base[]` |
| `blog_titles_he` | Suggested Hebrew blog title options |
| `mandatory_framing_he` | Required transparency text in Hebrew |
| `mandatory_framing_en` | Required transparency text in English |

---

## Confidence Display Rules

| `confidence_level` | Score shown? | Grade shown? | UI note |
|:------------------|:-------------|:-------------|:--------|
| `verified` | Yes | Yes | Show grade badge |
| `partial` | Provisional | Provisional | Add asterisk or disclaimer |
| `insufficient` | No | No | Show label only |

## Score Display Rule

Only show score and grade for products where `displayable = true`.
Products with `displayable = false` should show the `confidence_label_he` only.
"""

EXAMPLES_MD = """\
# Frontend Dataset Examples — real_bread_retail_002_v2

Usage examples for Cursor to implement UI components.

---

## Example 1 — Product Card (verified, high score)

```json
{
  "id": "shufersal_96086000966",
  "name_he": "קרקר כוסמין מלא ושומשום",
  "category": "cracker",
  "category_label_he": "קרקר",
  "score": 82,
  "grade": "A",
  "displayable": true,
  "confidence_label_he": "נתונים חלקיים",
  "confidence_level": "verified",
  "fiber_g": 10.0,
  "fermentation_real": false,
  "whole_grain": true,
  "seed_halo": false,
  "key_flags": ["גרעינים מלאים", "כוסמין", "שומשום", "סיבים גבוהים במיוחד"],
  "short_summary_he": "עשוי מקמח כוסמין מלא. תכולת סיבים גבוהה במיוחד — 10.0g ל-100g.",
  "ingredient_architecture_summary": "קמח כוסמין מלא · שמרים · שומשום"
}
```

**Cursor implementation note:**
- Show score badge (82 / A)
- Show `confidence_label_he` as a small pill below the name
- Show `key_flags` as color-coded tags
- Use `image_url` for the product photo
- Link `source_url` to Shufersal product page

---

## Example 2 — Product Card (insufficient data)

```json
{
  "id": "shufersal_2759522",
  "name_he": "מארז לחמניות חלה מתוקה",
  "displayable": false,
  "confidence_label_he": "לא מספיק לניתוח ודאי",
  "confidence_level": "insufficient",
  "score": null,
  "grade": null
}
```

**Cursor implementation note:**
- Do NOT show a score or grade
- Show only the `confidence_label_he` label
- Gray out the card or show a "??" placeholder
- Do not include in rankings or top lists

---

## Example 3 — Comparison Card

```json
{
  "id": "comp_fermentation_rye",
  "title": "מחמצת אמיתית לעומת שמרים תעשייתיים — לחם שיפון",
  "narrative": "שני לחמי שיפון עם ציוני תזונה דומים — אך אחד מכיל מחמצת אמיתית ברשימת הרכיבים והשני מסתמך על שמרים תעשייתיים.",
  "left_product_id": "shufersal_574370",
  "right_product_id": "shufersal_3719259",
  "key_difference": "מחמצת אמיתית לעומת שמרים תעשייתיים",
  "visual_direction": "left_wins"
}
```

**Cursor implementation note:**
- Render as side-by-side card
- Left = "better" product by `visual_direction`
- Show `key_difference` as the central callout
- Pull full product data from `products[]` by ID

---

## Example 4 — Insight Widget (fermentation)

```json
{
  "headline_he": "מתוך 32 מוצרים מאומתים, 18 כוללים מחמצת אמיתית ברשימת הרכיבים.",
  "genuine_count": 18,
  "mismatch_count": 13,
  "industrial_only_count": 8,
  "note_he": "13 מוצרים נושאים את השם 'מחמצת' אך כוללים שמרים תעשייתיים ברשימת הרכיבים."
}
```

**Cursor implementation note:**
- Render as a stat card with donut chart
- `headline_he` is the primary text
- `note_he` is a secondary callout / warning

---

## Example 5 — Homepage Section (strongest_verified)

```json
[
  {
    "id": "shufersal_96086000966",
    "name_he": "קרקר כוסמין מלא ושומשום",
    "score": 82,
    "grade": "A",
    "category_label_he": "קרקר",
    "image_url": "https://res.cloudinary.com/shufersal/...",
    "short_summary_he": "עשוי מקמח כוסמין מלא. תכולת סיבים גבוהה במיוחד — 10.0g ל-100g."
  }
]
```

**Cursor implementation note:**
- Render as horizontal scroll or grid of product cards
- Use `score` for the badge, `grade` for the letter
- Use `image_url` for the product photo
- Only products in this list are guaranteed displayable

---

## Example 6 — Mandatory Transparency Text

Always show before any score rankings:

```
ניתחנו 108 מוצרי לחם, פיתה וקרקרים ממדף שופרסל.
32 מוצרים עמדו בסף הנתונים הנדרש לניתוח מלא.
זהו ניתוח של מדף שופרסל בלבד — לא סקר שוק ישראלי מלא.
```

Source: `homepage_sections.mandatory_framing_he`

---

## Confidence Label Color Guide

| Label | Color | When |
|:------|:------|:-----|
| נתונים חלקיים | Green / teal | `confidence_level = "verified"` |
| חסרים נתונים מהותיים | Orange / amber | `confidence_level = "partial"` |
| לא מספיק לניתוח ודאי | Gray | `confidence_level = "insufficient"` |

---

## Do NOT

- Do not read raw BSIP2 report markdown files for UI data
- Do not show score for `displayable = false` products
- Do not use the word "Israeli market" — this is Shufersal only
- Do not rank products across `confidence_level` tiers
"""

# ─── main ─────────────────────────────────────────────────────────────────────

def main():
    print("Loading BSIP2 + raw data...")
    recs = load_all()
    print(f"  Loaded {len(recs)} products")

    print("Building product records...")
    products = [build_product_record(r) for r in recs]
    products.sort(key=lambda p: (not p["displayable"], -(p["score"] or 0)))

    verified = [p for p in products if p["displayable"]]
    print(f"  Verified (displayable): {len(verified)}")

    print("Building featured products...")
    featured_recs  = [r for r in recs if is_displayable(r)]
    featured_recs.sort(key=lambda r: r.get("final_score") or 0, reverse=True)
    featured_products = [build_featured_product(r, build_product_record(r))
                         for r in featured_recs[:15]]

    print("Building comparisons...")
    comparisons = build_comparisons(products, recs)
    print(f"  {len(comparisons)} comparison pairs")

    print("Building insights...")
    insights = build_insights(products, recs)

    print("Building homepage sections...")
    homepage_sections = build_homepage_sections(products)

    # dataset_meta
    fibers_all  = [p["fiber_g"] for p in verified if p["fiber_g"] is not None]
    avg_fiber_v = round(sum(fibers_all)/len(fibers_all), 1) if fibers_all else None
    nutr_n      = sum(1 for p in products if p["energy_kcal"] is not None)
    ing_n       = sum(1 for p in products if p["ingredient_visibility"] in ("full","partial") and p.get("ingredient_visibility") != "none")
    # re-count: ingredient_visibility full or partial means has some data
    ing_n2      = sum(1 for p in products if p["ingredient_visibility"] != "none")

    dataset_meta = {
        "run_id":                  RUN_ID,
        "snapshot_date":           TODAY,
        "source_retailer":         "שופרסל",
        "source_retailer_en":      "Shufersal",
        "total_scraped":           110,
        "in_scope":                len(products),
        "excluded":                2,
        "verified_products":       len(verified),
        "nutrition_coverage_pct":  round(100 * nutr_n / len(products)),
        "ingredient_coverage_pct": round(100 * ing_n2 / len(products)),
        "avg_fiber_verified":      avg_fiber_v,
        "caveats": [
            "זהו ניתוח של מדף שופרסל בלבד — לא סקר שוק ישראלי מלא.",
            f"רק {len(verified)} מוצרים כוללים גם לוח תזונה וגם רשימת רכיבים — אלה בלבד מקבלים ציון מלא.",
            "ציונים מבוססים על נתוני מדף שופרסל — לא על בדיקת מעבדה.",
            "לא להציג ציון למוצרים עם confidence_level = insufficient.",
        ],
        "confidence_explanation_he": (
            "ניתחנו כל מוצר לפי זמינות הנתונים. "
            "'נתונים חלקיים' — המוצר כלל לוח תזונה ורשימת רכיבים, ציון הוא ודאי יחסית. "
            "'חסרים נתונים מהותיים' — חסרים נתונים חיוניים, הציון אינו אמין. "
            "'לא מספיק לניתוח ודאי' — אין מספיק נתונים להציג ציון."
        ),
        "mandatory_framing_he": homepage_sections["mandatory_framing_he"],
        "mandatory_framing_en": homepage_sections["mandatory_framing_en"],
        "score_display_rule": "Show score only when displayable=true. Show confidence_label_he on all products.",
        "not_to_say": [
            "Do not say 'Israeli market' — this is Shufersal only.",
            "Do not show scores for displayable=false products.",
            "Do not rank products across confidence tiers.",
        ],
    }

    dataset = {
        "dataset_meta":      dataset_meta,
        "featured_products": featured_products,
        "products":          products,
        "comparisons":       comparisons,
        "insights":          insights,
        "homepage_sections": homepage_sections,
    }

    # Write outputs
    out_json = OUT_DIR / f"{RUN_ID}_frontend_dataset.json"
    out_json.write_text(json.dumps(dataset, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nWrote: {out_json.name} ({out_json.stat().st_size // 1024}KB)")

    schema_path = OUT_DIR / "frontend_dataset_schema.md"
    schema_path.write_text(SCHEMA_MD, encoding="utf-8")
    print(f"Wrote: {schema_path.name}")

    examples_path = OUT_DIR / "frontend_dataset_examples.md"
    examples_path.write_text(EXAMPLES_MD, encoding="utf-8")
    print(f"Wrote: {examples_path.name}")

    # Summary
    print(f"\n── Dataset Summary ──────────────────────────────")
    print(f"  Total products:   {len(products)}")
    print(f"  Displayable:      {len(verified)}")
    print(f"  Featured:         {len(featured_products)}")
    print(f"  Comparisons:      {len(comparisons)}")
    print(f"  Fermentation OK:  {insights['fermentation']['genuine_count']}")
    print(f"  Ferm mismatch:    {insights['fermentation']['mismatch_count']}")
    print(f"  Fiber laundering: {insights['fiber_laundering']['affected_count']}")
    print(f"  Seed halo:        {insights['seed_halo']['affected_count']}")
    print(f"  Avg fiber (ver.): {avg_fiber_v}g")

if __name__ == "__main__":
    main()
