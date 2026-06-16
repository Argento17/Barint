"""
TASK-238 — Open Food Facts removal remediation (DATA side).

Owner hard rule (2026-06-10): nutrition + ingredients come ONLY from the direct product
scrape. If a field came from OFF, it is NULLed. NULL/"data could not be retrieved" is the
only fallback. No source substitution. Engine UNCHANGED — a product whose entire nutrition
panel was OFF has no defensible scoring basis and becomes `insufficient` (score=null).

This script edits the SHIPPED frontend JSONs in bari-web/src/data/comparisons/ in
place, using the precise per-product OFF contamination map verified against the source
corpora (BSIP1/BSIP0 nutrition-provenance fields + shipped imageUrl host).

Per product it does, for OFF-contaminated fields ONLY:
  * OFF image  (imageUrl host = images.openfoodfacts.org)  -> imageUrl: null
  * OFF nutrition / ingredients (panel_source/external_nutrition_provenance/off_candidate
    /open_food_facts_fallback) -> nutrition values null, ingredients null, score=null,
    grade=null, confidence=insufficient, honest "data could not be retrieved" unknowns line.
Direct-scrape fields are untouched.

Deterministic re-score: every OFF-nutrition product in scope had its ENTIRE panel from a
single OFF source (verified — no partial direct panel to fall back on), so removing OFF
leaves no panel and the product is insufficient. No engine re-run is required or possible
on a null panel; the engine methodology is unchanged.
"""
import json, pathlib, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from frontend_core import grade_from_score  # noqa: E402  (None-safe)
import confidence_annotation as CA  # noqa: E402

COMP = pathlib.Path(r"C:\Bari\bari-web\src\data\comparisons")

# Honest "data could not be retrieved" line (owner rule), Hebrew, consumer-facing.
DATA_UNRETRIEVABLE_HE = (
    "נתוני התזונה והרכיבים של מוצר זה לא ניתנים לאחזור ממקור הסריקה הישיר — "
    "ולכן המוצר טרם נוקד."
)

# ── Precise OFF contamination map (verified against source corpora) ──────────────
# nutrition: products whose nutrition panel + ingredients came from OFF -> insufficient.
# image: products whose shipped imageUrl host is openfoodfacts -> imageUrl null.
# (image set is recomputed live from the JSON to stay exact; this lists the nutrition set.)
NUTRITION_OFF = {
    "cereals_frontend_v2.json": {
        "bsip1_cereal_7613037686906", "bsip1_cereal_7613033548192", "bsip1_cereal_5900020041142",
        "bsip1_cereal_3560071016074", "bsip1_cereal_7290116537351", "bsip1_cereal_4005528115218",
        "bsip1_cereal_42400108153", "bsip1_cereal_5900020046833",
    },
    "granola_frontend_v1.json": {
        "bsip1_cereal_7290120871069", "bsip1_cereal_7297488099821", "bsip1_cereal_5010026515919",
        "bsip1_cereal_7290114603034", "bsip1_cereal_7290019603634", "bsip1_cereal_5010026521149",
        "bsip1_cereal_7290011668570", "bsip1_cereal_3560070826186", "bsip1_cereal_7613035758834",
    },
    # hard_cheeses: 3 products with panel_source open_food_facts_fallback (by barcode).
    "hard_cheeses_frontend_v2.json": {
        "__by_barcode__": {"7290014455252", "3073781199918", "7290102302864"},
    },
    "butter_frontend_v2.json": {
        "__by_barcode__": {"4820217240114", "3161911229199"},
    },
    "juices_frontend_v3.json": {
        "__by_barcode__": {"7290000525969", "7290003009640", "7290110114893"},
    },
    # salty_snacks v4: ENTIRE scored shelf nutrition came from OFF panels -> all insufficient.
    "salty_snacks_frontend_v4.json": "__ALL__",
}

# yogurts: special — the 7 Yohananof products (provenance off_candidate_panel) are identity
# (il_prices) + OFF panel/image only. With OFF removed they have ZERO direct-scrape nutrition
# and cannot be shown -> DE-LIST (remove from products). The 11 Shufersal products are direct.
YOGURTS_FILE = "yogurts_frontend_v3.json"


def null_nutrition_block(nut):
    if not isinstance(nut, dict):
        return {}
    return {k: None for k in nut}


def make_insufficient(p):
    """Apply the insufficient state to an OFF-nutrition product, NULLing OFF fields."""
    deltas = {
        "id": p.get("id"),
        "old_score": p.get("score"),
        "old_grade": p.get("grade"),
        "old_conf": p.get("confidence"),
    }
    p["score"] = None
    p["grade"] = None
    p["confidence"] = "insufficient"
    p["confidence_label_he"] = CA.LABEL_INSUFFICIENT
    p["confidence_tooltip_he"] = CA.TOOLTIP_INSUFFICIENT
    p["confidence_sub_reason"] = "insufficient"
    exp = p.get("expansion")
    if isinstance(exp, dict):
        exp["nutrition"] = null_nutrition_block(exp.get("nutrition"))
        exp["ingredients"] = None
        exp["confidenceLabel"] = CA.LABEL_INSUFFICIENT
        # Honest "data could not be retrieved" state surfaced to the user.
        unknowns = exp.get("unknowns")
        unknowns = list(unknowns) if isinstance(unknowns, list) else []
        if DATA_UNRETRIEVABLE_HE not in unknowns:
            unknowns.insert(0, DATA_UNRETRIEVABLE_HE)
        exp["unknowns"] = unknowns
        # A scored verdict is no longer defensible; positive/limiting drivers were
        # derived from the OFF panel -> clear them. Copy strings (insightLine/rowVerdict)
        # are Content's; we leave them but they now describe an unscored product, so we
        # also blank the engine-derived signal arrays.
        exp["positiveSignals"] = []
        exp["limitingFactors"] = []
    deltas["new_score"] = None
    deltas["new_grade"] = None
    deltas["new_conf"] = "insufficient"
    return deltas


def is_off_image(p):
    return "openfoodfacts" in str(p.get("imageUrl") or "")


def matches_nutrition_off(p, spec):
    if spec == "__ALL__":
        return True
    if isinstance(spec, set):
        return p.get("id") in spec
    if isinstance(spec, dict) and "__by_barcode__" in spec:
        return str(p.get("barcode") or "") in spec["__by_barcode__"]
    return False


def process_standard(fn, spec, report):
    path = COMP / fn
    d = json.loads(path.read_text(encoding="utf-8"))
    products = d.get("products", d if isinstance(d, list) else [])
    img_nulled = nut_nulled = 0
    deltas = []
    for p in products:
        if is_off_image(p):
            p["imageUrl"] = None
            img_nulled += 1
        if matches_nutrition_off(p, spec):
            deltas.append(make_insufficient(p))
            nut_nulled += 1
    # refresh grade_distribution + counts in _meta if present
    if isinstance(d, dict) and "_meta" in d:
        gd = {}
        scored = 0
        for p in products:
            g = p.get("grade")
            if g:
                gd[g] = gd.get(g, 0) + 1
                scored += 1
        d["_meta"]["grade_distribution"] = gd
        d["_meta"]["scored_count"] = scored
        d["_meta"]["product_count"] = len(products)
        note = d["_meta"].get("provenance", "")
        d["_meta"]["provenance"] = (note + " | TASK-238: OFF removed — OFF nutrition NULLed "
                                    f"({nut_nulled} products -> insufficient), OFF images NULLed "
                                    f"({img_nulled}).").strip(" |")
    path.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
    report[fn] = {"img_nulled": img_nulled, "nut_nulled": nut_nulled, "deltas": deltas}


def process_yogurts(report):
    path = COMP / YOGURTS_FILE
    d = json.loads(path.read_text(encoding="utf-8"))
    products = d["products"]
    kept, delisted = [], []
    for p in products:
        off = (p.get("provenance") == "off_candidate_panel") or is_off_image(p)
        if off:
            delisted.append({"id": p.get("id"), "barcode": p.get("barcode"),
                             "old_score": p.get("score"), "old_grade": p.get("grade")})
        else:
            kept.append(p)
    d["products"] = kept
    gd = {}
    for p in kept:
        g = p.get("grade")
        if g:
            gd[g] = gd.get(g, 0) + 1
    d["_meta"]["grade_distribution"] = gd
    d["_meta"]["product_count"] = len(kept)
    d["_meta"]["scored_count"] = len(kept)
    d["_meta"]["retailer_breakdown"] = {"shufersal": sum(1 for p in kept if p.get("retailer") == "shufersal")}
    d["_meta"]["provenance"] = (
        "TASK-238: OFF removed. The 7 Yohananof products were identity (il_prices) + OFF "
        "candidate panel/image only — with OFF removed they have ZERO direct-scrape nutrition "
        "and were DE-LISTED. The 11 surviving products are direct Shufersal storefront scrapes "
        f"(html_parse, cloudinary images). Surviving={len(kept)}, de-listed={len(delisted)}."
    )
    path.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
    report[YOGURTS_FILE] = {"surviving": len(kept), "delisted": delisted}


def main():
    report = {}
    for fn, spec in NUTRITION_OFF.items():
        process_standard(fn, spec, report)
    process_yogurts(report)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
