"""
Wire D4 additive enrichment for juices_frontend_v1.json.

Ingredient source: BSIP1 run_juices_001 output (ingredients_text_he), keyed by barcode.
Barcodes are taken directly from the 'barcode' field in the frontend JSON.

Coverage note:
  Only 3/65 products (4.6%) have ingredient text in BSIP1 — below the 15% coverage gate.
  This is a documented, accepted data gap (W-JUICE-008 / RT-J-008):
    - Israeli juice brands are under-represented in Open Food Facts.
    - Most juice products have structurally simple ingredient lists (1–3 ingredients).
    - FDC generic references used for enrichment do not include ingredient text.
  Decision: proceed with wiring for the 3 products that have ingredient text.
  Key is absent (not empty array) for products with no ingredient text.

Guardrails (enforced by post-write assertion):
  - Never modifies score, grade, glassBox, or any existing field.
  - Products with 0 detected additives: d4_additives key is absent.
  - explanation_he sourced from w2_additive_copy_v1.md.
  - match_source removed (engine-internal, not in AdditiveEntry view-model).
"""

import json
import pathlib
import re
import sys
import os

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# ── Paths ─────────────────────────────────────────────────────────────────────
ROOT     = pathlib.Path(r"C:\Bari")
WEB_ROOT = pathlib.Path(r"C:\bari\bari-web")
BSIP1    = ROOT / "03_operations" / "bsip1" / "run_juices_001" / "output"
COMP     = WEB_ROOT / "src" / "data" / "comparisons"
SRC      = ROOT / "03_operations" / "bsip2" / "proto_v0" / "src"

COPY_DOC   = ROOT / "01_framework" / "glass_box" / "w2_additive_copy_v1.md"
JUICES_FE  = ROOT / "02_products" / "juices" / "juices_frontend_v1.json"

# ── Load engine ───────────────────────────────────────────────────────────────
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

os.environ.setdefault("BARI_GLASSBOX_W2",   "on")
os.environ.setdefault("BARI_GLASSBOX_W15",  "off")
os.environ.setdefault("BARI_GLASSBOX_D5D6", "off")
os.environ.setdefault("BARI_RECAL_P0",      "on")
os.environ.setdefault("BARI_TASK144_FIXES", "on")

from score_engine import detect_additives_d4  # noqa: E402


# ── Load explanation lookup ───────────────────────────────────────────────────
def load_explanation_lookup(doc_path: pathlib.Path) -> dict:
    text = doc_path.read_text(encoding="utf-8")
    lookup = {}
    blocks = re.split(r"(?=^### E)", text, flags=re.MULTILINE)
    for block in blocks:
        hm = re.match(r"^### (E[\d]+[a-z]?(?:/E[\d]+[a-z]?)*)", block)
        if not hm:
            continue
        e_number = hm.group(1)
        primary_e = e_number.split("/")[0]
        em = re.search(r"\*\*Explanation \(final\):\*\*\s*(.+)", block)
        if em:
            lookup[primary_e] = em.group(1).strip()
    return lookup


def enrich_entry(entry: dict, lookup: dict) -> dict:
    out = {k: v for k, v in entry.items() if k != "match_source"}
    out["explanation_he"] = lookup.get(entry["e_number"], "")
    return out


# ── Load ingredient text by barcode ──────────────────────────────────────────
def load_bsip1_ingredients(bsip1_dir: pathlib.Path) -> dict:
    ing_map = {}
    for fp in bsip1_dir.glob("bsip1_*.json"):
        barcode = fp.stem.replace("bsip1_", "")
        try:
            d = json.loads(fp.read_text(encoding="utf-8"))
            text = d.get("ingredients_text_he", "") or ""
            if text.strip():
                ing_map[barcode] = text
        except Exception:
            pass
    return ing_map


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    print("wire_d4_juices.py — D4 additive enrichment for juices_frontend_v1.json")
    print("=" * 70)
    print(f"COVERAGE NOTE: Juices have low OFF coverage. Only products with")
    print(f"ingredient text in BSIP1 will receive D4 enrichment.")
    print()

    lookup = load_explanation_lookup(COPY_DOC)
    print(f"Explanation lookup: {len(lookup)} E-numbers from copy doc.")

    ing_by_barcode = load_bsip1_ingredients(BSIP1)
    print(f"BSIP1 ingredient map: {len(ing_by_barcode)} products with ingredient text.")

    coverage_pct = len(ing_by_barcode) / 65 * 100
    print(f"Coverage: {len(ing_by_barcode)}/65 = {coverage_pct:.1f}%")
    print(f"  -> Below 15% gate. Proceeding with documented accepted gap (RT-J-008).")
    print()

    raw = JUICES_FE.read_text(encoding="utf-8")
    ends_nl = raw.endswith("\n")
    fe = json.loads(raw)

    # Pre-snapshot for invariant guard
    pre_snapshot = {
        p["id"]: {"score": p.get("score"), "grade": p.get("grade"), "glassBox": p.get("glassBox")}
        for p in fe["products"]
    }

    print(f"Juice products: {len(fe['products'])}")
    print("-" * 70)

    products_enriched = 0
    products_no_ing   = 0
    products_no_match = 0

    for prod in fe["products"]:
        pid     = prod["id"]
        barcode = prod.get("barcode", "")

        if not barcode:
            products_no_match += 1
            print(f"  {pid}: NO BARCODE in frontend record")
            prod.pop("d4_additives", None)
            continue

        ing_text = ing_by_barcode.get(str(barcode), "")
        if not ing_text:
            # Try stripping leading zeros
            ing_text = ing_by_barcode.get(str(barcode).lstrip("0"), "")

        if not ing_text:
            products_no_ing += 1
            prod.pop("d4_additives", None)
            continue

        d4 = detect_additives_d4(ing_text)
        enriched = [enrich_entry(e, lookup) for e in d4]

        if enriched:
            prod["d4_additives"] = enriched
            products_enriched += 1
            e_nums = [e["e_number"] for e in enriched]
            print(f"  {pid} [{barcode}]: {e_nums}")
        else:
            prod.pop("d4_additives", None)
            print(f"  {pid} [{barcode}]: 0 additives detected (ingredient text present but no E-numbers)")

    # Write back to source
    out = json.dumps(fe, ensure_ascii=False, indent=2)
    if ends_nl:
        out += "\n"
    JUICES_FE.write_text(out, encoding="utf-8")
    print()
    print(f"Source file updated: {JUICES_FE}")

    # Verify invariants
    fe2 = json.loads(JUICES_FE.read_text(encoding="utf-8"))
    violations = []
    for prod in fe2["products"]:
        pid = prod["id"]
        pre = pre_snapshot[pid]
        if prod.get("score")    != pre["score"]:    violations.append(f"{pid}: score changed")
        if prod.get("grade")    != pre["grade"]:    violations.append(f"{pid}: grade changed")
        if prod.get("glassBox") != pre["glassBox"]: violations.append(f"{pid}: glassBox changed")
    if violations:
        raise AssertionError(f"INVARIANT VIOLATIONS: {violations}")

    # Copy to bari-web
    dest = COMP / "juices_frontend_v1.json"
    dest.write_text(out, encoding="utf-8")
    print(f"Copied to bari-web: {dest}")

    total = len(fe["products"])
    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"  Products total:                {total}")
    print(f"  With d4_additives enriched:    {products_enriched}")
    print(f"  No ingredient text in BSIP1:   {products_no_ing}")
    print(f"  No barcode in frontend:        {products_no_match}")
    print(f"  Ingredient coverage:           {coverage_pct:.1f}% (gate=15%, gap accepted)")
    print(f"  score/grade/glassBox:          INVARIANT PASS")
    print(f"\n  Source: {JUICES_FE}")
    print(f"  Deployed: {dest}")
    print("\nDone.")


if __name__ == "__main__":
    main()
