"""
TASK-179S Phase 5 — Glass Box W2 D4 frontend enrichment.

For each pilot category (hummus, maadanim):
  1. Re-runs the engine with BARI_GLASSBOX_W2=on to get d4_additives per product.
  2. Loads the live frontend JSON.
  3. For each product that has d4_additives in the engine output:
     - Adds explanation_he from w2_additive_copy_v1.md (lookup by e_number).
     - Removes match_source (engine-internal field, not in AdditiveEntry view-model).
  4. Writes d4_additives back to the frontend JSON (purely additive — never touches
     score, grade, glassBox, or any other field).
  5. Preserves trailing-newline state and json.dumps(ensure_ascii=False, indent=2)
     formatting, same contract as wire_glassbox_frontend.py.

CONTRACT (non-negotiable):
  - NEVER modify score, grade, glassBox, or any existing field.
  - Products with no engine findings get no d4_additives key (consistent with the
    component's `product.d4_additives ?? []` fallback).
  - If a product already has d4_additives in the FE JSON (defensive), overwrite it
    with the enriched version.
  - e_numbers not in the lookup dict → explanation_he = "" (safe: component has
    a ?? "" fallback).
"""

import json
import os
import pathlib
import re
import sys

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
HERE   = pathlib.Path(__file__).parent                    # .../glass_box/w2/
SRC    = HERE.parent.parent.parent / "src"                # .../proto_v0/src
ROOT   = HERE.parent.parent.parent.parent.parent.parent   # C:\Bari
COMP   = ROOT / "bari-web" / "src" / "data" / "comparisons"

COPY_DOC = ROOT / "01_framework" / "glass_box" / "w2_additive_copy_v1.md"

PILOTS = {
    "hummus": {
        "corpus": ROOT / "02_products" / "hummus" / "canonical_bsip1",
        "fe":     COMP / "hummus_frontend_v4.json",
    },
    "maadanim": {
        "corpus": ROOT / "03_operations" / "bsip1" / "run_maadanim_001" / "output",
        "fe":     COMP / "maadanim_frontend_v2.json",
    },
}

# Engine modules that must be reloaded when toggling flags
_MODULES = [
    "signal_extractor", "score_engine", "nova_proxy", "trace_writer",
    "router_v2", "evaluation_scope", "input_loader", "constants",
    "structural_classifier",
]


# ---------------------------------------------------------------------------
# Step 1 — Parse w2_additive_copy_v1.md → e_number -> explanation_he
# ---------------------------------------------------------------------------
def load_explanation_lookup(doc_path: pathlib.Path) -> dict:
    """Parse **Explanation (final):** lines from the copy doc.

    Each entry block looks like:
      ### E330 — חומצת לימון (Citric acid)
      ...
      **Explanation (final):** <text>

    Returns {e_number: explanation_he} for all 20 entries.
    """
    text = doc_path.read_text(encoding="utf-8")
    lookup = {}
    # Split on H3 entry headers to isolate each block
    blocks = re.split(r"(?=^### E)", text, flags=re.MULTILINE)
    for block in blocks:
        # Extract e_number from header: ### E330 — ...  or  ### E472e — ...
        # Pattern: E followed by digits, optional slash-separated variants, optional
        # lowercase letter suffix (e.g. E472e).
        header_m = re.match(r"^### (E[\d]+[a-z]?(?:/E[\d]+[a-z]?)*)", block)
        if not header_m:
            continue
        e_number = header_m.group(1)
        # Normalize slash-delimited composite numbers (E450/E451 -> canonical key E450)
        # The copy doc uses E450/E451 but the engine emits E450. Keep the first token.
        # E472e stays E472e (the lowercase suffix is part of the sub-type identity).
        primary_e = e_number.split("/")[0]
        # Extract explanation line
        exp_m = re.search(r"\*\*Explanation \(final\):\*\*\s*(.+)", block)
        if exp_m:
            lookup[primary_e] = exp_m.group(1).strip()
    return lookup


# ---------------------------------------------------------------------------
# Step 2 — Run engine with BARI_GLASSBOX_W2=on for one corpus
# ---------------------------------------------------------------------------
def run_engine_w2_on(corpus: pathlib.Path) -> dict:
    """Score all products in corpus with BARI_GLASSBOX_W2=on.

    Returns {pid: d4_additives_list} — only products with non-empty d4_additives.
    """
    # Reload engine modules fresh with flag set
    os.environ["BARI_GLASSBOX_W2"]   = "on"
    os.environ["BARI_GLASSBOX_W15"]  = "off"
    os.environ["BARI_GLASSBOX_D5D6"] = "off"
    os.environ["BARI_RECAL_P0"]      = "off"
    os.environ["BARI_TASK144_FIXES"] = "off"
    for m in _MODULES:
        sys.modules.pop(m, None)

    import io
    import contextlib

    from input_loader import load_batch
    from signal_extractor import extract_signals
    from router_v2 import classify_category
    from nova_proxy import infer_nova
    from evaluation_scope import assign_evaluation_scope
    from score_engine import score_product

    d4_map = {}
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
        products = list(load_batch(corpus))

    for product in products:
        pid = product.get("canonical_product_id", "?")
        try:
            sig  = extract_signals(product)
            cat  = classify_category(product)
            nova = infer_nova(product, sig["L3_inferred_classifications"])
            ev   = assign_evaluation_scope(product, cat["category"])
            r    = score_product(product, sig, cat, nova, ev)
            d4   = r.get("d4_additives", [])
            if d4:
                d4_map[pid] = d4
        except Exception as e:
            print(f"  WARNING: engine error for {pid}: {e}")
    return d4_map


# ---------------------------------------------------------------------------
# Step 3 — Enrich d4_additives entries
# ---------------------------------------------------------------------------
def enrich_entry(entry: dict, lookup: dict) -> dict:
    """Add explanation_he, remove match_source. Never mutates other keys."""
    e = entry["e_number"]
    out = {k: v for k, v in entry.items() if k != "match_source"}
    out["explanation_he"] = lookup.get(e, "")
    return out


# ---------------------------------------------------------------------------
# Step 4 — Process one pilot category
# ---------------------------------------------------------------------------
def process(category: str, cfg: dict, lookup: dict) -> dict:
    corpus_path = cfg["corpus"]
    fe_path     = cfg["fe"]

    print(f"\n[{category}] running engine (BARI_GLASSBOX_W2=on) ...")
    # Ensure src/ is on path for engine imports
    if str(SRC) not in sys.path:
        sys.path.insert(0, str(SRC))

    d4_map = run_engine_w2_on(corpus_path)
    print(f"[{category}] engine: {len(d4_map)} products have d4_additives")

    # Load FE JSON preserving trailing-newline state
    raw = fe_path.read_text(encoding="utf-8")
    ends_nl = raw.endswith("\n")
    fe = json.loads(raw)

    products_enriched   = 0
    entries_with_expl   = 0
    entries_empty_expl  = 0

    # Snapshot existing score/grade/glassBox for post-write verification
    pre_snapshot = {}
    for prod in fe["products"]:
        pid = prod["id"]
        pre_snapshot[pid] = {
            "score":    prod.get("score"),
            "grade":    prod.get("grade"),
            "glassBox": prod.get("glassBox"),
        }

    for prod in fe["products"]:
        pid = prod["id"]
        raw_entries = d4_map.get(pid)
        if raw_entries is None:
            # No additives detected — ensure key is absent (consistent with ?? [] fallback)
            prod.pop("d4_additives", None)
            continue

        enriched = [enrich_entry(e, lookup) for e in raw_entries]
        prod["d4_additives"] = enriched
        products_enriched += 1

        for e in enriched:
            if e["explanation_he"]:
                entries_with_expl += 1
            else:
                entries_empty_expl += 1

    # Write back
    out = json.dumps(fe, ensure_ascii=False, indent=2)
    if ends_nl:
        out += "\n"
    fe_path.write_text(out, encoding="utf-8")

    # Verify invariants: score/grade/glassBox must not have changed
    raw2 = fe_path.read_text(encoding="utf-8")
    fe2 = json.loads(raw2)
    for prod in fe2["products"]:
        pid = prod["id"]
        pre = pre_snapshot[pid]
        assert prod.get("score")    == pre["score"],    f"{pid}: score changed!"
        assert prod.get("grade")    == pre["grade"],    f"{pid}: grade changed!"
        assert prod.get("glassBox") == pre["glassBox"], f"{pid}: glassBox changed!"

    return {
        "products_enriched":  products_enriched,
        "entries_with_expl":  entries_with_expl,
        "entries_empty_expl": entries_empty_expl,
        "fe_path":            str(fe_path),
    }


# ---------------------------------------------------------------------------
# Step 5 — Validation sample: 3 products per category
# ---------------------------------------------------------------------------
def print_validation_sample(category: str, fe_path: pathlib.Path,
                             pre_snapshot: dict, n: int = 3):
    fe = json.loads(fe_path.read_text(encoding="utf-8"))
    sampled = 0
    print(f"\n--- Validation sample: {category} ---")
    for prod in fe["products"]:
        if "d4_additives" not in prod:
            continue
        pid = prod["id"]
        print(f"\n  pid: {pid}")
        print(f"  score (unchanged): {prod.get('score')}  "
              f"grade (unchanged): {prod.get('grade')}")
        gb = prod.get("glassBox")
        print(f"  glassBox present: {'yes — ' + gb.get('gateState', '?') if gb else 'no'}")
        for entry in prod["d4_additives"]:
            # Confirm match_source absent
            assert "match_source" not in entry, f"match_source still present in {pid}!"
            print(f"    {entry['e_number']}  tier={entry['tier']}")
            print(f"      explanation_he: {entry['explanation_he']!r}")
        sampled += 1
        if sampled >= n:
            break
    if sampled == 0:
        print(f"  (no products with d4_additives in {category})")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("Phase 5: Wire D4 additive explanations into pilot frontend JSONs")
    print("=" * 64)

    # Load the explanation lookup
    print(f"\nLoading explanation lookup from:\n  {COPY_DOC}")
    lookup = load_explanation_lookup(COPY_DOC)
    print(f"Loaded {len(lookup)} e_number -> explanation_he entries:")
    for k, v in sorted(lookup.items()):
        print(f"  {k}: {v[:60]}...")

    results = {}
    pre_snapshots = {}

    for category, cfg in PILOTS.items():
        if not cfg["corpus"].exists():
            print(f"\n[{category}] SKIP — corpus not found: {cfg['corpus']}")
            continue

        # Capture pre-snapshot before processing (for validation sample below)
        raw = cfg["fe"].read_text(encoding="utf-8")
        fe_pre = json.loads(raw)
        snap = {}
        for p in fe_pre["products"]:
            snap[p["id"]] = {
                "score": p.get("score"), "grade": p.get("grade"),
                "glassBox": p.get("glassBox"),
            }
        pre_snapshots[category] = snap

        result = process(category, cfg, lookup)
        results[category] = result

    # Summary
    print("\n" + "=" * 64)
    print("SUMMARY")
    print("=" * 64)
    for cat, r in results.items():
        print(f"\n[{cat}]")
        print(f"  Products enriched (received d4_additives): {r['products_enriched']}")
        print(f"  Entries with populated explanation_he:     {r['entries_with_expl']}")
        print(f"  Entries with empty explanation_he          ")
        print(f"    (unclassified additive, ?? '' fallback): {r['entries_empty_expl']}")
        print(f"  Frontend JSON: {r['fe_path']}")

    # Validation samples (3 per category)
    print("\n" + "=" * 64)
    print("VALIDATION SAMPLES")
    print("=" * 64)
    for category, cfg in PILOTS.items():
        if category not in results:
            continue
        print_validation_sample(category, cfg["fe"], pre_snapshots[category], n=3)

    print("\n" + "=" * 64)
    print("match_source: verified absent from all sampled entries.")
    print("score / grade / glassBox: invariant checks passed (assertions in process()).")
    print("Phase 5 complete.")


if __name__ == "__main__":
    main()
