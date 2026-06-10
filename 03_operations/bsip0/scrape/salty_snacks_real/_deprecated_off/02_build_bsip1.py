"""
BSIP1 — Salty snacks REAL rebuild (TASK-228).
Curate the BSIP0 OFF-panel corpus into a balanced ~50-product shelf and emit BSIP1 v0.1
product JSONs into 02_products/salty_snacks/bsip1_outputs/ (the dir the batch runner reads).

Curation rules:
  - dedup by normalized name family (one representative per family; prefer ingredient-rich,
    then panel-complete, then smallest reasonable pack)
  - require core macros (already guaranteed by BSIP0)
  - balance across subpools
  - prioritize products with clean ingredient text (D4 coverage)
Target ~45-55 products.
"""
import sys, json, re, pathlib, hashlib
from datetime import datetime, timezone
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BSIP0 = pathlib.Path(r"C:\Bari\02_products\salty_snacks\bsip0_outputs\bsip0_salty_snacks_real_raw.json")
OUT_DIR = pathlib.Path(r"C:\Bari\02_products\salty_snacks\bsip1_outputs")

# Additive E-number from OFF tag (en:e621 -> E-621) for ingredient-light products,
# so the score engine's additive detection still has signal.
def additives_to_he(tags):
    out = []
    for t in tags or []:
        m = re.search(r"e(\d{3,4}[a-z]?)", t.lower())
        if m:
            out.append("E-" + m.group(1).upper())
    return out

def norm_family(name: str) -> str:
    """Collapse pack-size / flavor-pack variants to a family key for dedup."""
    n = name
    n = re.sub(r"\d+\s*\*?\s*\d*\s*(גרם|גר|ג'|ג|מ\"ל|מל|יח)", "", n)  # sizes
    n = re.sub(r"מארז|אחיד|שישיה|מולטיפק|מיני|פרו|\d+", "", n)
    n = re.sub(r"\s+", " ", n).strip()
    # keep first 3 meaningful tokens to define a family
    toks = n.split()
    return " ".join(toks[:3])

def clean_ing_list(text: str) -> list:
    if not text: return []
    parts = re.split(r"[,;]| ו(?=[א-ת])", text)
    return [p.strip(" .") for p in parts if p.strip(" .") and len(p.strip()) > 1][:25]

def main():
    d = json.loads(BSIP0.read_text(encoding="utf-8"))
    ps = d["products"]

    # score each product for curation priority
    def prio(p):
        has_ing = 1 if p.get("ingredients_clean") else 0
        nn = p["normalized_nutrition_per_100g"]
        completeness = sum(1 for v in nn.values() if v is not None)
        return (has_ing, completeness)

    # dedup by family, keep best
    best = {}
    for p in ps:
        fam = norm_family(p["name_he"])
        if fam not in best or prio(p) > prio(best[fam]):
            best[fam] = p
    deduped = list(best.values())

    # balance subpools — cap per subpool to keep shelf diverse, prioritize ingredient-rich
    deduped.sort(key=lambda p: prio(p), reverse=True)
    CAPS = {"chips": 14, "puffed": 9, "rice_cakes": 8, "pretzels": 7, "baked": 8, "popcorn": 6}
    counts = {}
    selected = []
    for p in deduped:
        sp = p["sub_pool"]
        if counts.get(sp, 0) >= CAPS.get(sp, 8):
            continue
        counts[sp] = counts.get(sp, 0) + 1
        selected.append(p)

    print(f"Deduped families: {len(deduped)} -> selected: {len(selected)}")
    from collections import Counter
    print("subpool dist:", dict(Counter(p["sub_pool"] for p in selected)))
    print("with ingredients:", sum(1 for p in selected if p.get("ingredients_clean")))

    # wipe + rebuild bsip1 dir
    if OUT_DIR.exists():
        for f in OUT_DIR.glob("bsip1_snack_*.json"):
            f.unlink()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    now = datetime.now(timezone.utc).isoformat()
    written = 0
    for p in selected:
        ean = p["barcode"]
        pid = f"bsip1_snack_{ean}"
        ing_text = p.get("ingredients_clean") or ""
        ing_list = clean_ing_list(ing_text)
        add_he = additives_to_he(p.get("additives_tags"))
        # if no free-text ingredients but OFF additives exist, synthesize a minimal
        # ingredient text carrying the E-numbers so additive/NOVA detection sees them
        if not ing_text and add_he:
            ing_text = ", ".join(add_he)
            ing_list = add_he
        nn = p["normalized_nutrition_per_100g"]
        has_ing = bool(p.get("ingredients_clean"))
        suf = "sufficient" if has_ing else "partial"
        rec = {
            "schema_version": "bsip1_v0_1",
            "file_type": "product",
            "canonical_product_id": pid,
            "barcode": ean,
            "canonical_name_he": p["name_he"],
            "canonical_name_en": p.get("name_off") or "",
            "brand": p.get("brand") or "",
            "package_size_g": None,
            "source_retailers": ["yochananof"],
            "sub_pool": p["sub_pool"],
            "category": "salty_snack",
            "image_url": p["image_url"],
            "image_urls": [p["image_url"]],
            "price_ils": None,
            "normalized_nutrition_per_100g": nn,
            "ingredients_text_he": ing_text,
            "ingredients_list": ing_list,
            "ingredients_raw": ing_text,
            "ingredient_count": len(ing_list),
            "claims_raw": "",
            "claims": [],
            "nova_proxy": p.get("nova_group_off"),
            "nova_confidence": 0.6 if p.get("nova_group_off") else None,
            "additive_categories": [],
            "additive_count": len(add_he),
            "allergens_contains": [],
            "allergens_may_contain": [],
            "data_sufficiency": suf,
            "nutrition_basis_claimed": "ל-100 גרם",
            "nutrition_basis_detected": "per_100g",
            "nutrition_consistency_status": "consistent",
            "ingredient_text_quality": "clean" if has_ing else "absent",
            "canonical_trust_score": 0.75 if has_ing else 0.6,
            "canonical_trust_level": "high" if has_ing else "medium",
            "canonical_risk_flags": [] if has_ing else ["ingredients_unavailable"],
            "confidence": {
                "identity_confidence": "high",
                "barcode_confidence": "confirmed",
                "nutrition_confidence": "confirmed_per_100g",
                "matched_by": "yochananof_catalog_real_ean + off_panel",
                "observation_count": 1,
            },
            "conflicts_summary": [],
            "missing_fields": [] if has_ing else ["ingredients_text_he"],
            "inferred_fields": ["nova_proxy"] if p.get("nova_group_off") else [],
            "audit_ref": None,
            "enrichment_run_id": "run_salty_snacks_bsip1_real_001",
            "enriched_at": now,
            "panel_provenance": p.get("panel_provenance"),
            "identity_source": "yochananof_catalog_harvest_real_ean",
        }
        (OUT_DIR / f"{pid}.json").write_text(json.dumps(rec, ensure_ascii=False, indent=2), encoding="utf-8")
        written += 1

    print(f"BSIP1 written: {written} products -> {OUT_DIR}")

if __name__ == "__main__":
    main()
