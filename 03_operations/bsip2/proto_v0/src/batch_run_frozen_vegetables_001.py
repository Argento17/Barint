"""
BSIP1 — Frozen vegetables batch runner (run_frozen_vegetables_001).
BSIP0 source: scope-clean v2_1 (53 products, Shufersal).
Engine: standard (BARI_RECAL_P0=on).

Transforms BSIP0 scraped data → BSIP1 product dicts in memory,
runs the full scoring pipeline, produces traces + report.

Two pasta-veg mixes (P_107622, P_103730) carry bsip1_note annotations.
"""
import sys, os, json, pathlib, logging, datetime, re

sys.path.insert(0, str(pathlib.Path(__file__).parent))

os.environ["BARI_RECAL_P0"] = "on"

from input_loader import get_nutrition, get_ingredients, get_ingredients_text
from signal_extractor import extract_signals
from router_v2 import classify_category
from nova_proxy import infer_nova
from evaluation_scope import assign_evaluation_scope
from score_engine import score_product, evaluate_guardrails
from trace_writer import assemble_trace, write_trace
from structural_classifier import classify_structural_class
from constants import score_to_grade

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

# ── Paths ───────────────────────────────────────────────────────────────
BASE = pathlib.Path(r"C:\Bari")
BSIP0_PATH = BASE / "02_products" / "frozen_vegetables" / "bsip0_outputs" / "bsip0_shufersal_frozen_vegetables_scope_clean_v2_1.json"
BSIP1_DIR = BASE / "02_products" / "frozen_vegetables" / "bsip1_outputs"
BSIP2_DIR = BASE / "02_products" / "frozen_vegetables" / "bsip2_outputs" / "run_frozen_vegetables_001"
REPORT_DIR = BASE / "02_products" / "frozen_vegetables" / "reports"
RUN_ID = "run_frozen_vegetables_001"
CATEGORY_TAG = "frozen_vegetables"

# ── Hebrew→English nutrition field mapping ─────────────────────────────
NUTRITION_MAP = {
    "אנרגיה": "energy_kcal",
    "חלבונים": "protein_g",
    "פחמימות": "carbohydrates_g",
    "סוכרים מתוך פחמימות": "sugars_g",
    "שומנים": "fat_g",
    "שומן רווי": "fat_saturated_g",
    "שומן טראנס": "fat_trans_g",
    "סיבים תזונתיים": "dietary_fiber_g",
    "נתרן": "sodium_mg",
}

def _parse_he_value(raw: str) -> float | None:
    """Parse Hebrew nutrition value like '121 קל' or '8.3 גרם' or '0 מג'."""
    if not raw:
        return None
    raw = raw.strip().replace(",", ".")
    m = re.search(r"([-+]?\d+\.?\d*)", raw)
    if m:
        return float(m.group(1))
    return None

def _make_bsip1_product(p: dict) -> dict | None:
    """Transform a BSIP0 product dict into BSIP1 format."""
    code = p.get("product_code", "")
    barcode = p.get("barcode_ld") or p.get("product_code", "").replace("P_", "")
    name_he = p.get("name_he") or ""
    brand = p.get("brand") or ""
    price = p.get("price_jsonld") or p.get("price") or None
    nut_raw = p.get("nutrition_raw") or {}
    ing_text = p.get("ingredient_text") or ""
    allergen_contains = p.get("allergen_contains") or ""
    allergen_may_contain = p.get("allergen_may_contain") or ""
    image_url = p.get("image_url_jsonld") or p.get("image_url") or ""
    product_url = p.get("product_url") or ""
    bsip1_note = p.get("bsip1_note") or ""
    scope_class = p.get("scope_class") or ""

    # Normalize nutrition
    nn = {}
    for he_key, en_key in NUTRITION_MAP.items():
        val = _parse_he_value(nut_raw.get(he_key))
        if val is not None:
            nn[en_key] = val
    # Remove nulls
    nn = {k: v for k, v in nn.items() if v is not None}

    if not nn.get("energy_kcal"):
        log.warning("  No energy_kcal for %s (%s)", code, name_he)
        return None

    # Parse ingredients list
    ing_list = [i.strip() for i in ing_text.replace(".", ",").replace("\n", ",").split(",") if i.strip()]

    product_id = f"bsip1_{barcode}"

    bsip1 = {
        "schema_version": "bsip1_v0_1",
        "file_type": "product",
        "canonical_product_id": product_id,
        "barcode": barcode,
        "canonical_name_he": name_he,
        "brand": brand,
        "source_retailers": ["shufersal"],
        "category": "frozen_vegetable",
        "bsip_frozen_vegetable_subtype": scope_class,
        "image_url": image_url,
        "product_url": product_url,
        "price_ils": price,
        "normalized_nutrition_per_100g": nn,
        "ingredients_text_he": ing_text,
        "ingredients_list": ing_list,
        "ingredients_raw": ing_text,
        "ingredient_count": len(ing_list),
        "allergens_contains": [allergen_contains] if allergen_contains else [],
        "allergens_may_contain": [allergen_may_contain] if allergen_may_contain else [],
        "data_sufficiency": "sufficient",
        "nutrition_basis_claimed": "ל-100 גרם",
        "nutrition_basis_detected": "per_100g",
        "canonical_trust_score": 0.85,
        "canonical_trust_level": "high",
        "confidence": {
            "identity_confidence": "high",
            "barcode_confidence": "confirmed",
            "nutrition_confidence": "confirmed_per_100g",
            "matched_by": "retailer_catalog_direct",
            "observation_count": 1,
        },
        "conflicts_summary": [],
        "missing_fields": [],
        "inferred_fields": [],
        "audit_ref": None,
        "bsip0_code": code,
        "bsip0_scope_class": scope_class,
        "bsip1_note": bsip1_note,
    }
    return bsip1


def run_pipeline(product: dict) -> dict:
    """Run the full BSIP2 scoring pipeline on a BSIP1 product.
    
    Router now knows frozen_vegetable as a category (router_v2 CATEGORIES entry,
    hard anchors for מוקפא/קפוא, and BSIP1 subtype prior for the 14 products
    without frozen indicators in their names). No manual override needed.
    """
    signals = extract_signals(product)
    cat = classify_category(product)
    l3 = signals["L3_inferred_classifications"]
    nova = infer_nova(product, l3)
    scope = assign_evaluation_scope(product, cat["category"])
    score = score_product(product, signals, cat, nova, scope)
    trace = assemble_trace(product, signals, cat, nova, scope, score)
    trace["structural_class"] = classify_structural_class(trace)
    trace["bsip0_code"] = product.get("bsip0_code", "")
    trace["bsip0_scope_class"] = product.get("bsip0_scope_class", "")
    trace["bsip1_note"] = product.get("bsip1_note", "")
    trace["bsip1_product_id"] = product.get("canonical_product_id", "")
    return trace


def run_batch():
    log.info("=" * 60)
    log.info("BSIP1 Frozen Vegetables — %s", RUN_ID)
    log.info("Source: %s", BSIP0_PATH)
    log.info("Output: %s", BSIP2_DIR)
    log.info("=" * 60)

    # Create output dirs
    BSIP1_DIR.mkdir(parents=True, exist_ok=True)
    BSIP2_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    # Clean previous run if any
    if BSIP2_DIR.exists():
        import shutil; shutil.rmtree(BSIP2_DIR)
    BSIP2_DIR.mkdir(parents=True, exist_ok=True)
    pdir = BSIP2_DIR / "products"
    pdir.mkdir(parents=True, exist_ok=True)

    # Load BSIP0 data
    bsip0 = json.loads(BSIP0_PATH.read_text(encoding="utf-8"))
    raw_products = bsip0["products"]
    log.info("BSIP0 products loaded: %d", len(raw_products))

    # Transform to BSIP1
    bsip1_products = []
    skipped = []
    for p in raw_products:
        bsip1 = _make_bsip1_product(p)
        if bsip1 is None:
            skipped.append(p.get("product_code", "unknown"))
            continue
        bsip1_products.append(bsip1)
        # Write BSIP1 file
        fname = f"bsip1_{bsip1['barcode']}.json"
        (BSIP1_DIR / fname).write_text(
            json.dumps(bsip1, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    log.info("BSIP1 products created: %d", len(bsip1_products))
    if skipped:
        log.warning("Skipped (no energy_kcal): %s", skipped)

    # Run pipeline
    traces = []
    errors = []

    for product in bsip1_products:
        pid = product.get("canonical_product_id", "unknown")
        code = product.get("bsip0_code", "")
        name = (product.get("canonical_name_he") or "")[:40]
        try:
            trace = run_pipeline(product)
            write_trace(trace, BSIP2_DIR)
            traces.append(trace)

            score = trace.get("final_score_estimate")
            grade = trace.get("grade_estimate")
            cat = trace.get("category", "?")
            nova = trace.get("nova_proxy", "?")
            sc = (trace.get("structural_class") or {}).get("structural_class", "?")
            cap = trace.get("binding_cap") or "-"
            log.info("  [%s] %-42s score=%-5s grade=%s  cat=%-18s nova=%s  sc=%s  cap=%s",
                     code or "", pid, score, grade, cat, nova, sc, cap)
        except Exception as e:
            log.error("  PIPELINE ERROR %s (%s): %s", code, pid, e)
            import traceback; traceback.print_exc()
            errors.append({"code": code, "product_id": pid, "error": str(e)})

    log.info("Batch complete. Processed: %d, Errors: %d", len(traces), len(errors))

    # ── Generate report ──
    _write_report(traces, errors, bsip1_products)
    return traces, errors


def _write_report(traces, errors, products):
    run_dt = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    sufficient = [t for t in traces if t.get("data_sufficiency") != "insufficient"
                  and t.get("final_score_estimate") is not None]

    # Grade distribution
    dist = {}
    for t in sufficient:
        g = t.get("grade_estimate"); dist[g] = dist.get(g, 0) + 1

    scores = sorted(t.get("final_score_estimate") for t in sufficient)
    median = scores[len(scores) // 2] if scores else None

    # NOVA distribution
    nova_dist = {}
    for t in traces:
        n = t.get("nova_proxy"); nova_dist[str(n)] = nova_dist.get(str(n), 0) + 1

    # Top/Bottom 5
    def _name(t):
        ref = t.get("input_reference") or {}
        return ref.get("product_name_he") or ref.get("canonical_name_he") or ""
    top5 = sorted(sufficient, key=lambda t: -(t.get("final_score_estimate") or 0))[:5]
    bottom5 = sorted(sufficient, key=lambda t: (t.get("final_score_estimate") or 0))[:5]

    # Products with bsip1_note
    noted = [t for t in sufficient if t.get("bsip1_note")]
    # Products with unresolved flags (confidence/missing data)
    flagged_confidence = [t for t in sufficient if t.get("unresolved_flags")]

    # Scope class breakdown
    scope_dist = {}
    for t in sufficient:
        sc = t.get("bsip0_scope_class", "?"); scope_dist[sc] = scope_dist.get(sc, 0) + 1

    lines = [
        f"# BSIP1 Frozen Vegetables — {RUN_ID} Scoring Report",
        f"",
        f"**Run date:** {run_dt}",
        f"**Source:** Shufersal BSIP0 scrape (scope-clean v2_1)",
        f"**Products processed:** {len(traces)}",
        f"**Scored (sufficient data):** {len(sufficient)}",
        f"**Errors:** {len(errors)}",
        f"",
        f"## Grade Distribution",
        f"",
    ]
    for g in sorted(dist.keys()):
        lines.append(f"- **{g}**: {dist[g]}")
    if median is not None:
        lines.append(f"\n**Median score:** {median}")
    if scores:
        lines.append(f"**Score range:** {scores[0]} – {scores[-1]}")

    lines += [
        f"",
        f"## Scope Class Breakdown",
        f"",
    ]
    for sc, cnt in sorted(scope_dist.items()):
        lines.append(f"- {sc}: {cnt}")

    lines += [
        f"",
        f"## NOVA Distribution",
        f"",
    ]
    for n, cnt in sorted(nova_dist.items()):
        lines.append(f"- NOVA {n}: {cnt}")

    lines += [
        f"",
        f"## Top 5 (highest scores)",
        f"",
    ]
    for t in top5:
        n = _name(t)
        code = t.get("bsip0_code", "")
        note_mark = " ⚠️" if t.get("bsip1_note") else ""
        lines.append(
            f"- {code}: **{t.get('final_score_estimate')}** → {t.get('grade_estimate')} "
            f"(NOVA {t.get('nova_proxy')}, {n[:50]}){note_mark}"
        )

    lines += [
        f"",
        f"## Bottom 5 (lowest scores)",
        f"",
    ]
    for t in bottom5:
        n = _name(t)
        code = t.get("bsip0_code", "")
        note_mark = " ⚠️" if t.get("bsip1_note") else ""
        lines.append(
            f"- {code}: **{t.get('final_score_estimate')}** → {t.get('grade_estimate')} "
            f"(NOVA {t.get('nova_proxy')}, {n[:50]}){note_mark}"
        )

    if noted:
        lines += [
            f"",
            f"## Manual-Review Products (bsip1_note)",
            f"",
        ]
        for t in noted:
            n = _name(t)
            code = t.get("bsip0_code", "")
            note = t.get("bsip1_note", "")
            lines.append(
                f"- {code}: **{t.get('final_score_estimate')}** → {t.get('grade_estimate')} "
                f"(NOVA {t.get('nova_proxy')}, {n[:50]})"
            )
            lines.append(f"  - Note: {note}")

    if flagged_confidence:
        lines += [
            f"",
            f"## Confidence Flags / Unresolved Issues",
            f"",
        ]
        for t in flagged_confidence:
            n = _name(t)
            code = t.get("bsip0_code", "")
            flags = t.get("unresolved_flags", [])
            lines.append(f"- {code} ({n[:40]}): {flags}")

    if errors:
        lines += [
            f"",
            f"## Errors",
            f"",
        ]
        for e in errors:
            lines.append(f"- {e.get('code', '?')} ({e.get('product_id', '?')}): {e.get('error', '?')}")

    # Detail table
    lines += [
        f"",
        f"## All Products — Detail",
        f"",
        f"| Code | Name | Score | Grade | NOVA | Scope Class | Note |",
        f"|------|------|-------|-------|------|-------------|------|",
    ]
    for t in sorted(sufficient, key=lambda x: -(x.get("final_score_estimate") or 0)):
        code = t.get("bsip0_code", "")
        n = (_name(t) or "?")[:40]
        s = t.get("final_score_estimate", "?")
        g = t.get("grade_estimate", "?")
        nov = t.get("nova_proxy", "?")
        sc = t.get("bsip0_scope_class", "?")
        note = "⚠️ " if t.get("bsip1_note") else ""
        lines.append(f"| {code} | {n} | {s} | {g} | {nov} | {sc} | {note} |")

    report = "\n".join(lines)
    report_path = REPORT_DIR / "bsip1_scoring_report_frozen_vegetables_001.md"
    report_path.write_text(report, encoding="utf-8")
    log.info("Report written: %s", report_path)

    # Also write JSON summary
    summary = {
        "run_id": RUN_ID,
        "generated": run_dt,
        "engine": "proto_v0 / BARI_RECAL_P0=on",
        "source": "Shufersal BSIP0 scope-clean v2_1",
        "processed": len(traces),
        "scored_sufficient": len(sufficient),
        "errors": len(errors),
        "grade_distribution": dist,
        "score_median": median,
        "score_range": [scores[0], scores[-1]] if scores else None,
        "nova_distribution": nova_dist,
        "scope_breakdown": scope_dist,
    }
    (REPORT_DIR / "bsip1_scoring_summary_frozen_vegetables_001.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    log.info("Summary written: %s", REPORT_DIR / "bsip1_scoring_summary_frozen_vegetables_001.json")


if __name__ == "__main__":
    run_batch()
