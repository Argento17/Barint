"""
wire_d4_bars.py — D4 additive enrichment for snacks_frontend_v5.json and
protein_bars_frontend_v1.json.

Ingredient source: product["expansion"]["ingredients"] (inline in the frontend JSON).
No BSIP1 run / barcode-from-imageUrl path needed — these corpora carry real ingredient
text directly.

Guardrails (enforced by post-write assertion):
  - Never modifies score, grade, glassBox, or any existing field.
  - Products with 0 detected additives: d4_additives key is set to [] (present, empty).
  - Products with additives detected: d4_additives is a list of AdditiveEntry objects.
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
HERE = pathlib.Path(__file__).parent
SRC  = HERE.parent.parent.parent / "src"
ROOT = HERE.parent.parent.parent.parent.parent.parent

COMP     = ROOT / "bari-web" / "src" / "data" / "comparisons"
COPY_DOC = ROOT / "01_framework" / "glass_box" / "w2_additive_copy_v1.md"

SNACKS_FE    = COMP / "snacks_frontend_v5.json"
PROT_BARS_FE = COMP / "protein_bars_frontend_v1.json"

# ── Load engine ───────────────────────────────────────────────────────────────
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

os.environ.setdefault("BARI_GLASSBOX_W2",   "on")
os.environ.setdefault("BARI_GLASSBOX_W15",  "off")
os.environ.setdefault("BARI_GLASSBOX_D5D6", "off")
os.environ.setdefault("BARI_RECAL_P0",      "off")
os.environ.setdefault("BARI_TASK144_FIXES", "off")

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


# ── Process a single shelf file ───────────────────────────────────────────────
def process_shelf(fe_path: pathlib.Path, lookup: dict, label: str) -> dict:
    """
    Returns a result dict with per-product stats for reporting.
    Writes the updated JSON back to fe_path.
    """
    print(f"\n{'='*70}")
    print(f"{label}: {fe_path.name}")
    print(f"{'='*70}")

    raw = fe_path.read_text(encoding="utf-8")
    ends_nl = raw.endswith("\n")
    fe = json.loads(raw)

    # Pre-snapshot for invariant guard
    pre_snapshot = {
        p["id"]: {
            "score":    p.get("score"),
            "grade":    p.get("grade"),
            "glassBox": p.get("glassBox"),
        }
        for p in fe["products"]
    }

    print(f"Products: {len(fe['products'])}")
    print("-" * 70)

    products_with_additives = 0
    products_no_ingredients = 0
    products_zero_detected  = 0
    missing_copy            = {}   # e_number -> list of pids
    detection_gaps          = []   # (pid, ingredients_snippet) — had keyword but no detect

    KNOWN_ADDITIVE_TOKENS = [
        "E", "לציטין", "מתחלב", "חומר תפיחה", "מייצב", "גליצרול",
        "טוקופרול", "חומצה ציטרי", "חומצה ציטרית", "פוטסיום סורבט",
        "סורבט", "סוכרלוז", "אצסולפאם", "סטיביה", "קסנטן", "קרגינן",
        "פקטין", "עמילן מעובד", "CMC", "DATEM", "SSL",
    ]

    def has_additive_tokens(text: str) -> bool:
        if not text:
            return False
        for tok in KNOWN_ADDITIVE_TOKENS:
            if tok in text:
                return True
        # Also check for E-number pattern like (E471) or E471
        if re.search(r"\bE\d{3}", text):
            return True
        return False

    for prod in fe["products"]:
        pid  = prod["id"]
        ing  = prod.get("expansion", {}).get("ingredients", "") or ""

        if not ing.strip():
            products_no_ingredients += 1
            prod["d4_additives"] = []
            print(f"  {pid}: NO ingredients text")
            continue

        d4 = detect_additives_d4(ing)

        if d4:
            enriched = [enrich_entry(e, lookup) for e in d4]
            prod["d4_additives"] = enriched
            products_with_additives += 1
            e_nums = [e["e_number"] for e in enriched]
            print(f"  {pid}: {e_nums}")
            # Collect missing copy
            for e in enriched:
                if e["explanation_he"] == "":
                    missing_copy.setdefault(e["e_number"], []).append(pid)
        else:
            prod["d4_additives"] = []
            products_zero_detected += 1
            print(f"  {pid}: 0 additives detected")
            # Flag detection gap if ingredients clearly contain additive tokens
            if has_additive_tokens(ing):
                snippet = ing[:120].replace("\n", " ")
                detection_gaps.append((pid, snippet))

    # Write back
    out = json.dumps(fe, ensure_ascii=False, indent=2)
    if ends_nl:
        out += "\n"
    fe_path.write_text(out, encoding="utf-8")

    # Verify invariants
    fe2 = json.loads(fe_path.read_text(encoding="utf-8"))
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
    print(f"\nSUMMARY — {label}")
    print(f"  Total products:          {total}")
    print(f"  With >=1 additive:       {products_with_additives}")
    print(f"  Zero additives detected: {products_zero_detected}")
    print(f"  No ingredient text:      {products_no_ingredients}")

    if missing_copy:
        print(f"\n  MISSING COPY (explanation_he='') — {len(missing_copy)} e_number(s):")
        for en, pids in sorted(missing_copy.items()):
            print(f"    {en}: {pids}")
    else:
        print("  Missing copy: none")

    if detection_gaps:
        print(f"\n  DETECTION GAPS — ingredients had additive tokens but engine returned 0:")
        for pid, snip in detection_gaps:
            print(f"    {pid}: \"{snip}\"")
    else:
        print("  Detection gaps: none")

    print(f"  score/grade/glassBox:    INVARIANT PASS")
    print(f"  File updated: {fe_path}")

    return {
        "total":                  total,
        "with_additives":         products_with_additives,
        "zero_detected":          products_zero_detected,
        "no_ingredients":         products_no_ingredients,
        "missing_copy":           missing_copy,
        "detection_gaps":         detection_gaps,
    }


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    print("wire_d4_bars.py — D4 additive enrichment for snacks_v5 + protein_bars_v1")
    print("=" * 70)

    lookup = load_explanation_lookup(COPY_DOC)
    print(f"Explanation lookup: {len(lookup)} E-numbers from copy doc.")

    snacks_result = process_shelf(SNACKS_FE,    lookup, "SNACKS (v5)")
    prot_result   = process_shelf(PROT_BARS_FE, lookup, "PROTEIN BARS (v1)")

    print("\n" + "=" * 70)
    print("COMBINED SUMMARY")
    print("=" * 70)
    for label, r in [("SNACKS", snacks_result), ("PROTEIN BARS", prot_result)]:
        print(f"\n  {label}:")
        print(f"    Total:             {r['total']}")
        print(f"    With >=1 additive: {r['with_additives']}")
        print(f"    Zero detected:     {r['zero_detected']}")
        print(f"    No ingredients:    {r['no_ingredients']}")
        mc = r["missing_copy"]
        print(f"    Missing copy:      {len(mc)} e_number(s) — {list(mc.keys()) if mc else 'none'}")
        dg = r["detection_gaps"]
        print(f"    Detection gaps:    {len(dg)} product(s) — {[x[0] for x in dg] if dg else 'none'}")

    print("\nDone.")


if __name__ == "__main__":
    main()
