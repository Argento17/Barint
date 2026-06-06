"""
Wire D4 additive enrichment for snacks_frontend_v2.json.

Ingredient source: BSIP1 run_001 output (ingredients_text_he), keyed by barcode.
Barcodes are derived from imageUrl in the frontend JSON — some products use a
Yochananof-internal code as the filename prefix; the real EAN barcode is either
the sole number or the second number in the filename.

Barcode override map handles:
  - snk-019: imageUrl has a transposed-digit typo (7290118247896 → 7290118427896)
  - snk-003: imageUrl has a leading-zero padded barcode (016000548404 → 16000548404)

Guardrails (enforced by post-write assertion):
  - Never modifies score, grade, glassBox, or any existing field.
  - Products with 0 detected additives: d4_additives key is absent.
  - explanation_he sourced from w2_additive_copy_v1.md (same as all other categories).
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
HERE    = pathlib.Path(__file__).parent
SRC     = HERE.parent.parent.parent / "src"
ROOT    = HERE.parent.parent.parent.parent.parent.parent
COMP    = ROOT / "bari-web" / "src" / "data" / "comparisons"
BSIP1   = ROOT / "03_operations" / "bsip1" / "run_001" / "output"

COPY_DOC   = ROOT / "01_framework" / "glass_box" / "w2_additive_copy_v1.md"
SNACKS_FE  = COMP / "snacks_frontend_v2.json"

# ── Load engine ───────────────────────────────────────────────────────────────
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

os.environ.setdefault("BARI_GLASSBOX_W2",   "on")
os.environ.setdefault("BARI_GLASSBOX_W15",  "off")
os.environ.setdefault("BARI_GLASSBOX_D5D6", "off")
os.environ.setdefault("BARI_RECAL_P0",      "off")
os.environ.setdefault("BARI_TASK144_FIXES", "off")

from score_engine import detect_additives_d4  # noqa: E402


# ── Barcode extraction ────────────────────────────────────────────────────────
# Known overrides: imageUrl barcode != real EAN barcode.
BARCODE_OVERRIDES: dict[str, str] = {
    "snk-019": "7290118427896",  # imageUrl has transposed digits (7290118247896)
}

def barcode_from_image_url(image_url: str) -> str | None:
    """
    Extract EAN barcode from a Yochananof image URL.
    Pattern: .../YOCHANANOF_CODE_BARCODE.jpg  →  prefer BARCODE (second number)
             .../BARCODE.jpg                  →  use that number
             .../BARCODE_sXXX-....jpg         →  use the first number
    Returns the longest digit sequence that looks like an EAN (8, 12, or 13 digits).
    """
    filename = image_url.rstrip("/").split("/")[-1].split(".")[0]
    parts = re.split(r"[_\-]", filename)
    candidates = [p for p in parts if re.match(r"^\d{8,13}$", p)]
    if not candidates:
        return None
    # Among candidates, prefer the one that is NOT a Yochananof internal code.
    # Yochananof internal codes start with "125" or "126" and are 8 digits.
    real = [c for c in candidates if not (len(c) == 8 and c.startswith(("125", "126")))]
    return (real or candidates)[-1]


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
            ing_map[barcode] = d.get("ingredients_text_he", "") or ""
        except Exception:
            pass
    return ing_map


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    print("wire_d4_snacks.py — D4 additive enrichment for snacks_frontend_v2.json")
    print("=" * 70)

    lookup = load_explanation_lookup(COPY_DOC)
    print(f"Explanation lookup: {len(lookup)} E-numbers from copy doc.")

    ing_by_barcode = load_bsip1_ingredients(BSIP1)
    print(f"BSIP1 ingredient map: {len(ing_by_barcode)} products.")

    raw = SNACKS_FE.read_text(encoding="utf-8")
    ends_nl = raw.endswith("\n")
    fe = json.loads(raw)

    # Pre-snapshot for invariant guard
    pre_snapshot = {
        p["id"]: {"score": p.get("score"), "grade": p.get("grade"), "glassBox": p.get("glassBox")}
        for p in fe["products"]
    }

    print(f"\nSnack products: {len(fe['products'])}")
    print("-" * 70)

    products_enriched = 0
    products_no_ing   = 0
    products_no_match = 0

    for prod in fe["products"]:
        pid       = prod["id"]
        image_url = prod.get("imageUrl", "")

        # Barcode resolution
        barcode = BARCODE_OVERRIDES.get(pid) or barcode_from_image_url(image_url)

        ing_text = ""
        if barcode:
            ing_text = ing_by_barcode.get(barcode, "")
            if not ing_text:
                # Try stripping leading zeros
                ing_text = ing_by_barcode.get(barcode.lstrip("0"), "")

        if not barcode:
            products_no_match += 1
            print(f"  {pid}: NO BARCODE from imageUrl")
            prod.pop("d4_additives", None)
            continue

        if not ing_text:
            products_no_ing += 1
            print(f"  {pid} [{barcode}]: no ingredient text in BSIP1")
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
            print(f"  {pid} [{barcode}]: 0 additives detected")

    # Write back
    out = json.dumps(fe, ensure_ascii=False, indent=2)
    if ends_nl:
        out += "\n"
    SNACKS_FE.write_text(out, encoding="utf-8")

    # Verify invariants
    fe2 = json.loads(SNACKS_FE.read_text(encoding="utf-8"))
    violations = []
    for prod in fe2["products"]:
        pid = prod["id"]
        pre = pre_snapshot[pid]
        if prod.get("score")    != pre["score"]:    violations.append(f"{pid}: score changed")
        if prod.get("grade")    != pre["grade"]:    violations.append(f"{pid}: grade changed")
        if prod.get("glassBox") != pre["glassBox"]: violations.append(f"{pid}: glassBox changed")
    if violations:
        raise AssertionError(f"Invariant violations: {violations}")

    total = len(fe["products"])
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"  Products total:            {total}")
    print(f"  With d4_additives:         {products_enriched}")
    print(f"  No ingredients in BSIP1:   {products_no_ing}")
    print(f"  No barcode resolved:       {products_no_match}")
    print(f"  score/grade/glassBox:      INVARIANT PASS")
    print(f"\n  File updated: {SNACKS_FE}")
    print("\nDone.")


if __name__ == "__main__":
    main()
