# -*- coding: utf-8 -*-
"""
Frontend JSON builder — Juices & Fruit Drinks v3 (run_juices_yohananof_002)
TASK-214 / pipeline step: Stage 7 Frontend Packaging

Reads:   BSIP1 outputs + BSIP2 trace outputs (run_juices_yohananof_002)
         Content Agent insight lines (content_draft_v1.md)
Writes:  juices_frontend_v3.json → 02_products/juices/
         + bari-web/src/data/comparisons/juices_frontend_v3.json

Excluded barcodes (out-of-scope products):
  jc-015  miz agvaniot    → 5411188115434  (tomato juice)
  jc-018  alpro soya      → 7290013608680  (soy drink)
  jc-020  alpro oat       → 7290110325893  (oat drink)
  jc-024  tnuva go ice    → 7290110558420  (coffee-milk)

These barcodes match the excluded_pids in run_summary.json.
"""
import sys
import re
import json
import pathlib
import datetime
import shutil

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT       = pathlib.Path(r"C:\Bari")
BSIP1_DIR  = ROOT / "02_products" / "juices" / "bsip1_outputs"
BSIP2_DIR  = ROOT / "02_products" / "juices" / "bsip2_outputs" / "run_juices_yohananof_002" / "products"
CONTENT_MD = ROOT / "02_products" / "juices" / "content_draft_v1.md"
OUT_LOCAL  = ROOT / "02_products" / "juices" / "juices_frontend_v3.json"
OUT_WEB    = ROOT / "bari-web" / "src" / "data" / "comparisons" / "juices_frontend_v3.json"

# Excluded barcodes — products out of juice/fruit-drink scope
EXCLUDED_BARCODES = {
    "5411188115434",   # jc-015 miz agvaniot (tomato)
    "7290013608680",   # jc-018 alpro barista soya
    "7290110325893",   # jc-020 alpro oat
    "7290110558420",   # jc-024 tnuva go ice coffee-milk
}

# Manual name overrides: BSIP1 truncated/spaced names → content draft canonical name
# Used when automatic matching fails due to OCR artifacts in BSIP1 name
NAME_OVERRIDES = {
    # barcode → content_draft_name (as it appears in content_draft_v1.md jc-NNN field)
    "7290013608260": "מיץ רימונים 100% מיץ סחוט טרי מצונן 1 ליטר",   # jc-006
    # jc-013: BSIP1 has "1 ל'" (abbreviated), content draft has "1 ל" without apostrophe.
    # Normalizer collapses both to same as jc-008/009 base. Force direct content name.
    "7290117765630": "מיץ תירוש יוחננוף 100% טבעי 1 ל",               # jc-013 (partial)
}


# ---------------------------------------------------------------------------
# Content Agent insight line parser
# ---------------------------------------------------------------------------

def load_content_insight_lines(md_path: pathlib.Path) -> dict:
    """Parse 'jc-NNN | [name] | [insight line]' entries from markdown.

    Returns dict: normalized_name → insight_line
    """
    lines_map = {}
    if not md_path.exists():
        print(f"WARNING: content_draft_v1.md not found at {md_path}")
        return lines_map

    text = md_path.read_text(encoding="utf-8")
    pattern = re.compile(r"^(jc-\d+)\s*\|\s*(.+?)\s*\|\s*(.+)$", re.MULTILINE)
    for m in pattern.finditer(text):
        jc_id   = m.group(1).strip()
        name    = m.group(2).strip()
        insight = m.group(3).strip()
        # Store by jc_id and by normalized name for dual-lookup
        lines_map[jc_id] = (name, insight)

    print(f"Content lines loaded: {len(lines_map)} entries")
    return lines_map


def normalize_name(name: str) -> str:
    """Normalize Hebrew product name for fuzzy matching."""
    # collapse whitespace, strip trailing/leading, remove trailing volume refs
    s = re.sub(r"\s+", " ", name).strip()
    # remove trailing pack-size patterns like "1 ליטר", "2 ליטר", "500 מ"ל", "1 ל'"
    s = re.sub(r'\s+\d+[\.\d]*\s*(ל[יי]טר|ל\'|מ"ל|מ׳׳ל|ליטר|ml|L)\s*$', "", s, flags=re.IGNORECASE)
    return s.strip()


def find_content_insight(product_name: str, content_map: dict) -> tuple:
    """Return (insight_line, matched_jc_id, ambiguous:bool).

    Matching priority:
    1. Exact literal match on full name (including volume suffix)
    2. Exact normalized match (volume stripped from both sides)
    3. Partial normalized containment (fallback)
    """
    # Pass 1: exact literal
    for jc_id, (cname, insight) in content_map.items():
        if product_name == cname:
            return insight, jc_id, False

    # Pass 2: exact after normalization — but only accept if unique
    norm_product = normalize_name(product_name)
    norm_matches = []
    for jc_id, (cname, insight) in content_map.items():
        norm_content = normalize_name(cname)
        if norm_product == norm_content:
            norm_matches.append((jc_id, cname, insight))

    if len(norm_matches) == 1:
        return norm_matches[0][2], norm_matches[0][0], False
    if len(norm_matches) > 1:
        # Multiple norm matches → flag as ambiguous but take first
        return norm_matches[0][2], norm_matches[0][0], True

    # Pass 3: partial containment (product name starts with content base name)
    partial_matches = []
    for jc_id, (cname, insight) in content_map.items():
        norm_content = normalize_name(cname)
        if norm_product.startswith(norm_content) or norm_content.startswith(norm_product):
            partial_matches.append((jc_id, cname, insight))

    if len(partial_matches) == 1:
        return partial_matches[0][2], partial_matches[0][0], False
    if len(partial_matches) > 1:
        return partial_matches[0][2], partial_matches[0][0], True

    return None, None, False


# ---------------------------------------------------------------------------
# Confidence label helpers
# ---------------------------------------------------------------------------

def confidence_label(nn: dict) -> tuple:
    kcal  = nn.get("energy_kcal")
    carbs = nn.get("carbohydrates_g")
    sugar = nn.get("sugars_g")
    present = sum(1 for v in [kcal, carbs, sugar] if v is not None)
    if kcal is None:
        return "insufficient", "נתונים לא מספיקים"
    if present >= 3:
        return "verified", "נתונים מאומתים"
    return "partial", "נתונים חלקיים"


# ---------------------------------------------------------------------------
# Positive signals / limiting factors (carried from v2 build logic)
# ---------------------------------------------------------------------------

def _nova1_juice_label(ing: str) -> str:
    """Consumer-facing replacement for NOVA-1 fresh-juice signal.
    Inspects actual ingredients text to choose the most specific phrasing.
    Never exposes the word 'NOVA' to the consumer layer.
    """
    single_fruit_tokens = [
        "מיץ תפוזים", "מיץ רימונים", "מיץ לימון", "מיץ ענבים",
        "מיץ קלמנטינות", "מיץ גויאבה", "מיץ אשכולית",
    ]
    # Single-ingredient fresh product: ingredient text is very short and
    # consists only of a fruit name.
    if len(ing.strip()) <= 30 and any(f in ing for f in single_fruit_tokens):
        return "מיץ סחוט טרי — פרי בלבד"
    return "מיץ סחוט טרי — ללא ריכוז, ללא עיבוד"


def build_positive_signals(bsip1: dict) -> list:
    signals = []
    sugar  = bsip1.get("sugars_g")
    nova   = bsip1.get("nova_proxy")
    subp   = bsip1.get("juice_subpool", "fruit_drink")
    addt   = bsip1.get("detected_additives") or []
    ing    = bsip1.get("ingredients_text_he") or ""

    if subp == "juice_100":
        signals.append("100% פרי ללא תוספות" if len(addt) == 0 else "100% פרי")
    has_added_sugar = "סוכר לבן" in ing or ("סוכר" in ing and subp != "juice_100")
    if not has_added_sugar:
        # Drop the machine-Hebrew "זוהה" — consumers don't need the detection qualifier
        signals.append("ללא סוכר מוסף")
    if sugar is not None and sugar < 8:
        signals.append(f"סוכר נמוך ({sugar:.1f}g ל-100מ\"ל)")
    if nova == 1:
        # Never expose "NOVA" in consumer-facing copy; translate to product-specific language
        signals.append(_nova1_juice_label(ing))
    # NOVA 3 and NOVA 4 are never positive signals — omit entirely
    return signals


def build_limiting_factors(bsip1: dict, score: int = 0) -> list:
    factors = []
    sugar  = bsip1.get("sugars_g")
    nova   = bsip1.get("nova_proxy")
    subp   = bsip1.get("juice_subpool", "fruit_drink")
    addt   = bsip1.get("detected_additives") or []
    ing    = bsip1.get("ingredients_text_he") or ""
    is_a_grade = score >= 80 and subp == "juice_100"

    if sugar is not None and sugar > 10:
        if is_a_grade:
            # Natural sugar in a top-scoring 100% juice is not a defect; provide context
            factors.append("סוכר טבעי בלבד — ללא תוספות")
        else:
            factors.append(f"סוכר גבוה ({sugar:.1f}g ל-100מ\"ל)")
    elif sugar is not None and sugar > 6:
        if is_a_grade:
            factors.append("סוכר טבעי בלבד — ללא תוספות")
        else:
            factors.append(f"סוכר בינוני ({sugar:.1f}g ל-100מ\"ל)")

    if subp == "fruit_drink":
        factors.append("תוכן פרי נמוך (<25%)")

    has_added_sugar = "סוכר לבן" in ing
    if has_added_sugar:
        factors.append("סוכר מוסף")

    # Never expose raw "NOVA N — ..." strings in consumer copy
    if nova == 4:
        factors.append("משקה עם חומרי עיבוד")
    elif nova == 3 and subp != "juice_100":
        factors.append("מיץ מרוכז")

    if addt:
        has_color_flavor = any(
            re.search(r"E1[0-9]{2}|E6[0-9]{2}|E4[0-9]{2}", a, re.I) for a in addt
        )
        if has_color_flavor or len(addt) >= 3:
            factors.append(f"תוספות צבע/טעם ({', '.join(addt[:3])})")

    return factors


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()

    # --- Load content insight lines ---
    content_map = load_content_insight_lines(CONTENT_MD)

    # --- Load BSIP1 files ---
    bsip1_map = {}
    for f in BSIP1_DIR.glob("bsip1_juice_*.json"):
        if "run_report" in f.name or "skipped" in f.name:
            continue
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
            barcode = d.get("barcode", "")
            pid     = d.get("canonical_product_id")
            # Skip excluded barcodes
            if barcode in EXCLUDED_BARCODES:
                print(f"  [EXCLUDED] {pid} (barcode {barcode})")
                continue
            if pid:
                bsip1_map[pid] = d
        except Exception as e:
            print(f"  BSIP1 load error {f.name}: {e}")

    print(f"BSIP1 loaded (after exclusions): {len(bsip1_map)}")

    # --- Load BSIP2 traces from run_juices_yohananof_002 ---
    trace_map = {}
    for trace_path in BSIP2_DIR.glob("*/bsip2_trace.json"):
        pid = trace_path.parent.name
        try:
            t = json.loads(trace_path.read_text(encoding="utf-8"))
            if pid in bsip1_map:
                trace_map[pid] = t
        except Exception as e:
            print(f"  BSIP2 load error {pid}: {e}")

    print(f"BSIP2 traces matched: {len(trace_map)}")

    # --- Build product list ---
    products_staging = []
    for pid, trace in trace_map.items():
        bsip1 = bsip1_map[pid]
        score = trace.get("final_score_estimate")
        grade = trace.get("grade_estimate")

        if score is None or grade in ("insufficient_data", None):
            print(f"  [SKIP] {pid} — no score/grade")
            continue

        nn     = bsip1.get("normalized_nutrition_per_100g") or {}
        name   = bsip1.get("canonical_name_he") or ""
        subp   = bsip1.get("juice_subpool") or "fruit_drink"
        conf_key, conf_label = confidence_label(nn)

        products_staging.append({
            "_pid":        pid,
            "_score":      score,
            "_grade":      grade,
            "_name":       name,
            "_subp":       subp,
            "_bsip1":      bsip1,
            "_nn":         nn,
            "_conf_key":   conf_key,
            "_conf_label": conf_label,
        })

    products_staging.sort(key=lambda x: x["_score"], reverse=True)

    # --- Integrate content insight lines + build output ---
    grade_dist    = {}
    out_products  = []
    matched_count = 0
    unmatched     = []
    ambiguous     = []

    for i, p in enumerate(products_staging):
        seq   = f"jc-{i+1:03d}"
        bsip1 = p["_bsip1"]
        nn    = p["_nn"]
        score = round(p["_score"])
        grade = p["_grade"]
        grade_dist[grade] = grade_dist.get(grade, 0) + 1

        # Content Agent insight line
        # Apply name override if barcode is in NAME_OVERRIDES
        barcode_for_lookup = bsip1.get("barcode", "")
        lookup_name = NAME_OVERRIDES.get(barcode_for_lookup, p["_name"])
        insight_line, matched_jc_id, is_ambiguous = find_content_insight(
            lookup_name, content_map
        )
        if insight_line:
            matched_count += 1
            if is_ambiguous:
                ambiguous.append({
                    "pid": p["_pid"],
                    "name": p["_name"],
                    "matched_jc_id": matched_jc_id,
                    "note": "ambiguous_match",
                })
        else:
            unmatched.append({"pid": p["_pid"], "name": p["_name"]})
            # Fallback: empty string — do not auto-generate
            insight_line = ""

        pos_sig = build_positive_signals(bsip1)
        lim_fac = build_limiting_factors(bsip1, score=score)

        out_products.append({
            "id":           seq,
            "name":         p["_name"],
            "brand":        bsip1.get("brand"),
            "barcode":      bsip1.get("barcode"),
            "imageUrl":     bsip1.get("image_url"),
            "score":        score,
            "grade":        grade,
            "confidence":   p["_conf_key"],
            "insightLine":  insight_line,
            "retailers":    bsip1.get("source_retailers") or ["yohananof"],
            "subPool":      p["_subp"],
            "novaGroup":    bsip1.get("nova_proxy"),
            "sugarPer100ml": nn.get("sugars_g"),
            "kcalPer100ml":  round(nn["energy_kcal"]) if nn.get("energy_kcal") is not None else None,
            "volumeMl":     bsip1.get("weight_g"),
            "expansion": {
                "nutrition": {
                    "energyKcal": nn.get("energy_kcal"),
                    "protein":    nn.get("protein_g"),
                    "sugar":      nn.get("sugars_g"),
                    "fat":        nn.get("fat_g"),
                    "satFat":     nn.get("fat_saturated_g"),
                    "fiber":      nn.get("dietary_fiber_g"),
                    "sodium":     nn.get("sodium_mg"),
                },
                "ingredients":     bsip1.get("ingredients_text_he"),
                "confidenceLabel": p["_conf_label"],
                "servingNote":     "ל-100 מ\"ל",
                "positiveSignals": pos_sig,
                "limitingFactors": lim_fac,
            },
        })

    # --- Assemble document ---
    doc = {
        "_meta": {
            "generated":         ts,
            "category":          "juices",
            "run_id":            "run_juices_yohananof_002",
            "schema":            "BariProductVM[] v3",
            "version":           "v3",
            "product_count":     len(out_products),
            "scored_count":      len(out_products),
            "excluded_count":    len(EXCLUDED_BARCODES),
            "excluded_barcodes": sorted(EXCLUDED_BARCODES),
            "provenance": (
                "bsip0_yohananof_juices_storefront_20260607 "
                "→ BSIP1 run_juices_yohananof_001 "
                "→ BSIP2 run_juices_yohananof_002 "
                "→ content_draft_v1 insight lines"
            ),
            "grade_distribution":    grade_dist,
            "insight_lines_matched": matched_count,
            "insight_lines_total":   len(out_products),
            "build_notes": {
                "ambiguous_matches": ambiguous,
                "unmatched_products": unmatched,
            },
        },
        # Legacy flat fields for TS compatibility
        "generatedAt":   ts,
        "totalProducts": len(out_products),
        "products":      out_products,
    }

    # --- Write outputs ---
    OUT_LOCAL.parent.mkdir(parents=True, exist_ok=True)
    OUT_LOCAL.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nWritten: {OUT_LOCAL}")

    OUT_WEB.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(OUT_LOCAL, OUT_WEB)
    print(f"Copied:  {OUT_WEB}")

    # --- Summary ---
    scores = [p["_score"] for p in products_staging]
    print(f"\n=== Frontend v3 Summary ===")
    print(f"  Products in JSON:       {len(out_products)}")
    print(f"  Excluded (out-of-scope):{len(EXCLUDED_BARCODES)}")
    print(f"  Grade distribution:     {grade_dist}")
    print(f"  Score range:            {min(scores):.1f}–{max(scores):.1f}")
    print(f"  Insight lines matched:  {matched_count}/{len(out_products)}")
    if unmatched:
        print(f"\n  Unmatched products ({len(unmatched)}):")
        for u in unmatched:
            print(f"    {u['pid']}  '{u['name']}'")
    if ambiguous:
        print(f"\n  Ambiguous matches ({len(ambiguous)}):")
        for a in ambiguous:
            print(f"    {a['pid']}  '{a['name']}' → {a['matched_jc_id']}")


if __name__ == "__main__":
    main()
