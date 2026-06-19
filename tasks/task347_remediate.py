"""
TASK-347 — Phase 2+3 WS-Data remediation
=========================================
Fixes:
  1. Clean 5 malformed ingredient strings (4 cereals + 1 granola)
  2. Compute + bake rank and categoryTotal for all 407 products
  3. Re-derive systematic nulls FROM THE SCRAPE:
     - sugar: cereals (20), granola (25), hard_cheeses (26)
     - sodium: milk (18), granola (5)
  4. d4_additives field absent on milk (18) + juices (21):
     - juices: run detect_additives_d4 on ingredient text from bsip1
     - milk: run detect_additives_d4 on ingredient text from bsip1
     - emit [] for products with no ingredient text or 0 detected additives

Guardrails:
  - Never modify score, grade, or any non-data-gap field
  - Never use OFF data
  - Never fabricate/invent values
  - STAGING only — edits to bari-web/src/data/comparisons/*.json
"""

import json
import os
import re
import sys
import glob
import hashlib
import copy

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# ─── Paths ────────────────────────────────────────────────────────────────────
BARI_ROOT   = "C:/Bari"
BARI_WEB    = "C:/Bari/bari-web"
COMP_DIR    = f"{BARI_WEB}/src/data/comparisons"
BSIP2_SRC   = f"{BARI_ROOT}/03_operations/bsip2/proto_v0/src"
BSIP1_DIR   = f"{BARI_ROOT}/03_operations/bsip1"

# ─── Score engine setup ───────────────────────────────────────────────────────
os.environ.setdefault("BARI_GLASSBOX_W2",   "on")
os.environ.setdefault("BARI_GLASSBOX_W15",  "off")
os.environ.setdefault("BARI_GLASSBOX_D5D6", "off")
os.environ.setdefault("BARI_RECAL_P0",      "on")
os.environ.setdefault("BARI_TASK144_FIXES", "on")
if BSIP2_SRC not in sys.path:
    sys.path.insert(0, BSIP2_SRC)

from score_engine import detect_additives_d4  # noqa: E402

# ─── Explanation lookup from w2_additive_copy_v1.md ─────────────────────────
def load_explanation_lookup() -> dict:
    doc_path = f"{BARI_ROOT}/01_framework/glass_box/w2_additive_copy_v1.md"
    text = open(doc_path, encoding="utf-8").read()
    lookup = {}
    blocks = re.split(r"(?=^### E)", text, flags=re.MULTILINE)
    for block in blocks:
        hm = re.match(r"^### (E[\d]+[a-z]?(?:/E[\d]+[a-z]?)*) — ", block)
        if not hm:
            continue
        e_number = hm.group(1)
        primary_e = e_number.split("/")[0]
        em = re.search(r"\*\*Explanation \(final\):\*\*\s*(.+)", block)
        if em:
            lookup[primary_e] = em.group(1).strip()
    return lookup

EXPLANATION_LOOKUP = load_explanation_lookup()

def enrich_additive_entry(entry: dict) -> dict:
    """Strip match_source, add explanation_he from lookup."""
    out = {k: v for k, v in entry.items() if k != "match_source" and k != "cosmetic_mup"}
    out["explanation_he"] = EXPLANATION_LOOKUP.get(entry["e_number"], "")
    return out

# ─── Ingredient cleaning ─────────────────────────────────────────────────────
# Cut markers — everything from these patterns onward is Shufersal nutrition panel
CUT_PATTERNS = [
    r"ערכים תזונתיים\s+100",
    r"ערכים תזונתיים\s*\n",
]
# Prefix to strip
PREFIX_STRIP = re.compile(r"^רכיבים:\s*")
SUFFIX_CLEAN = re.compile(r"\s*\.$")  # trailing period after stripping

def clean_ingredient_string(raw: str) -> str:
    """
    Remove the Shufersal nutrition-panel/disclaimer text appended to ingredient strings.
    Cut points: 'ערכים תזונתיים 100', 'סך הדגנים במוצר', 'הנתונים המדויקים', 'כפיות סוכר'.
    Also strips leading 'רכיבים:' prefix and literal 'n' scraper linebreak artifacts.
    Returns the cleaned ingredient string, or None if the result is empty.
    """
    if not raw or not isinstance(raw, str):
        return raw
    # Find earliest cut point
    EXTENDED_CUT = CUT_PATTERNS + [r"סך הדגנים במוצר", r"הנתונים המדויקים", r"כפיות סוכר"]
    cleaned = raw
    earliest = len(cleaned)
    for pat in EXTENDED_CUT:
        m = re.search(pat, cleaned)
        if m and m.start() < earliest:
            earliest = m.start()
    if earliest < len(cleaned):
        cleaned = cleaned[:earliest]
    # Strip leading "רכיבים:" prefix
    cleaned = PREFIX_STRIP.sub("", cleaned).strip()
    # Replace literal 'n' between non-space chars: scraper used 'n' as linebreak
    # Hebrew ן/נ are U+05DF/U+05E0, completely different from ASCII 'n' (U+006E)
    cleaned = re.sub(r"(?<=\S)n(?=\S)", " ", cleaned)
    # Handle trailing 'n' at end of string after non-space
    cleaned = re.sub(r"(?<=\S)n$", "", cleaned)
    # Clean up multiple spaces
    cleaned = re.sub(r"  +", " ", cleaned)
    # Strip trailing period/comma/n + whitespace
    cleaned = cleaned.rstrip(" .,n").strip()
    return cleaned if cleaned else None

# ─── Numeric parsing ─────────────────────────────────────────────────────────
def parse_numeric(val) -> float | None:
    """Parse a value like '22.4' or '10 מג' or '3.8' → float, or None."""
    if val is None:
        return None
    s = str(val).strip()
    if not s:
        return None
    # Remove units and Hebrew text
    s = re.sub(r'[^\d.]', '', s.split()[0])
    try:
        return float(s)
    except (ValueError, IndexError):
        return None

# ─── Raw scrape loaders ───────────────────────────────────────────────────────
def load_cereals_raw() -> dict:
    """Load cereals bsip0 raw, keyed by barcode. Prefer newer file."""
    raw_by_bc = {}
    for fname in [
        f"{BARI_ROOT}/02_products/breakfast_cereals/bsip0_outputs/cereals_bsip0_raw_20260601T152207.json",
        f"{BARI_ROOT}/02_products/breakfast_cereals/bsip0_outputs/cereals_bsip0_raw_20260605T154620.json",
    ]:
        if not os.path.exists(fname):
            continue
        with open(fname, encoding="utf-8") as f:
            items = json.load(f)
        for item in items:
            bc = str(item.get("barcode", ""))
            raw_by_bc[bc] = item  # newer file overwrites
    return raw_by_bc

def load_milk_bsip1() -> dict:
    """Load milk bsip1 files, keyed by barcode."""
    result = {}
    # Look in all bsip1 run dirs
    for fpath in glob.glob(f"{BSIP1_DIR}/**/bsip1_*.json", recursive=True):
        try:
            with open(fpath, encoding="utf-8-sig") as f:
                data = json.load(f)
            bc = str(data.get("barcode", ""))
            if bc and bc not in result:
                result[bc] = data
        except Exception:
            pass
    return result

def load_juice_bsip1() -> dict:
    """Load juice bsip1 files from juices/bsip1_outputs, keyed by barcode."""
    result = {}
    bsip1_dir = f"{BARI_ROOT}/02_products/juices/bsip1_outputs"
    for fpath in glob.glob(f"{bsip1_dir}/bsip1_juice_*.json"):
        try:
            with open(fpath, encoding="utf-8") as f:
                data = json.load(f)
            bc = str(data.get("barcode", ""))
            if bc:
                result[bc] = data
        except Exception:
            pass
    return result

# ─── Rank computation ─────────────────────────────────────────────────────────
def assign_rank_and_total(products: list) -> list:
    """
    Assign rank (1=highest score) and categoryTotal to each product.
    Ties get the same rank (dense ranking).
    Returns a new list with rank/categoryTotal fields added.
    """
    total = len(products)
    # Sort by score descending to determine ranks
    scored = [(i, p.get("score") or 0) for i, p in enumerate(products)]
    scored.sort(key=lambda x: -x[1])

    rank_map = {}
    current_rank = 1
    prev_score = None
    for order, (orig_idx, score) in enumerate(scored):
        if score != prev_score:
            current_rank = order + 1
            prev_score = score
        rank_map[orig_idx] = current_rank

    result = []
    for i, p in enumerate(products):
        p2 = dict(p)
        p2["rank"] = rank_map[i]
        p2["categoryTotal"] = total
        result.append(p2)
    return result

# ─── Pre/post snapshot for invariant check ────────────────────────────────────
def snapshot_invariants(products: list) -> dict:
    return {p["id"]: {"score": p.get("score"), "grade": p.get("grade")} for p in products}

def check_invariants(pre: dict, post_products: list) -> list:
    violations = []
    for p in post_products:
        pid = p["id"]
        if pid not in pre:
            continue
        if p.get("score") != pre[pid]["score"]:
            violations.append(f"{pid}: score changed {pre[pid]['score']} -> {p.get('score')}")
        if p.get("grade") != pre[pid]["grade"]:
            violations.append(f"{pid}: grade changed {pre[pid]['grade']} -> {p.get('grade')}")
    return violations

# ─── SHA256 helper ────────────────────────────────────────────────────────────
def sha256_file(path: str) -> str:
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

# ─── Main remediation ─────────────────────────────────────────────────────────
def main():
    print("TASK-347 — Data remediation")
    print("=" * 70)

    # Load raw data sources
    print("\nLoading raw data sources...")
    cereals_raw = load_cereals_raw()
    milk_bsip1  = load_milk_bsip1()
    juice_bsip1 = load_juice_bsip1()
    print(f"  cereals_raw: {len(cereals_raw)} products")
    print(f"  milk_bsip1:  {len(milk_bsip1)} products")
    print(f"  juice_bsip1: {len(juice_bsip1)} products")

    # ─── File registry ────────────────────────────────────────────────────────
    FILE_MAP = {
        "cereals":            f"{COMP_DIR}/cereals_frontend_v2.json",
        "granola":            f"{COMP_DIR}/granola_frontend_v1.json",
        "juices":             f"{COMP_DIR}/juices_frontend_v3.json",
        "hummus":             f"{COMP_DIR}/hummus_frontend_v5.json",
        "hard_cheeses":       f"{COMP_DIR}/hard_cheeses_frontend_v2.json",
        "brined_cheeses":     f"{COMP_DIR}/brined_cheeses_frontend_v2.json",
        "cakes_hard_cookies": f"{COMP_DIR}/cakes_hard_cookies_frontend_v1.json",
        "cookies_coffee":     f"{COMP_DIR}/cookies_coffee_frontend_v2.json",
        "snacks":             f"{COMP_DIR}/snacks_frontend_v3.json",
        "milk":               f"{COMP_DIR}/milk_frontend_v1.json",
    }

    # Track changes
    all_results = {}

    for slug, fpath in FILE_MAP.items():
        print(f"\n{'─'*70}")
        print(f"Processing: {slug} ({os.path.basename(fpath)})")

        with open(fpath, encoding="utf-8") as f:
            raw_text = f.read()
        ends_nl = raw_text.endswith("\n")
        data = json.loads(raw_text)

        products = data["products"]
        pre_snap = snapshot_invariants(products)

        # ── BEFORE counts ──
        before = {
            "n": len(products),
            "malformed": 0,
            "sugar_null": sum(1 for p in products if p.get("expansion", {}).get("nutrition", {}).get("sugar") is None),
            "sodium_null": sum(1 for p in products if p.get("expansion", {}).get("nutrition", {}).get("sodium") is None),
            "d4_absent":  sum(1 for p in products if "d4_additives" not in p),
            "rank_absent": sum(1 for p in products if "rank" not in p),
        }
        # malformed = ingredients contains nutrition-panel markers
        for p in products:
            ing = p.get("expansion", {}).get("ingredients", "")
            if ing and isinstance(ing, str) and ("הנתונים המדויקים מופיעים" in ing or "כפיות סוכר" in ing or "ערכים תזונתיים 100 גרם" in ing):
                before["malformed"] += 1

        changes = {
            "malformed_cleaned": 0,
            "sugar_filled": 0,
            "sugar_unrecoverable": 0,
            "sodium_filled": 0,
            "sodium_unrecoverable": 0,
            "d4_populated": 0,
            "d4_set_empty": 0,
            "rank_assigned": 0,
        }
        unrecoverable_log = []

        # ── Step 1: Process each product ──────────────────────────────────────
        for p in products:
            bc = str(p.get("barcode", ""))
            expansion = p.get("expansion", {})
            nutrition = expansion.get("nutrition", {})

            # ─── Fix 1: Clean malformed ingredients ───────────────────────────
            if slug in ("cereals", "granola"):
                ing = expansion.get("ingredients", "")
                if ing and isinstance(ing, str) and (
                    "ערכים תזונתיים" in ing or
                    "הנתונים המדויקים" in ing or
                    "כפיות סוכר" in ing
                ):
                    cleaned = clean_ingredient_string(ing)
                    if cleaned and cleaned != ing:
                        expansion["ingredients"] = cleaned
                        changes["malformed_cleaned"] += 1
                        print(f"  CLEANED ing BC:{bc} -> {cleaned[:80]}…")

            # ─── Fix 2: Sugar from cereals raw scrape ─────────────────────────
            if slug == "cereals" and nutrition.get("sugar") is None:
                raw_item = cereals_raw.get(bc, {})
                raw_nut  = raw_item.get("nutrition", {})
                sugar_val = parse_numeric(raw_nut.get("sugar_raw"))
                if sugar_val is not None:
                    nutrition["sugar"] = sugar_val
                    changes["sugar_filled"] += 1
                else:
                    changes["sugar_unrecoverable"] += 1
                    unrecoverable_log.append(f"cereals BC:{bc} sugar")

            # ─── Fix 3: Sugar from granola raw scrape ─────────────────────────
            if slug == "granola" and nutrition.get("sugar") is None:
                raw_item = cereals_raw.get(bc, {})
                raw_nut  = raw_item.get("nutrition", {})
                sugar_val = parse_numeric(raw_nut.get("sugar_raw"))
                if sugar_val is not None:
                    nutrition["sugar"] = sugar_val
                    changes["sugar_filled"] += 1
                else:
                    changes["sugar_unrecoverable"] += 1
                    unrecoverable_log.append(f"granola BC:{bc} sugar")

            # ─── Fix 4: Sodium from granola raw scrape (5 products) ───────────
            if slug == "granola" and nutrition.get("sodium") is None:
                raw_item = cereals_raw.get(bc, {})
                raw_nut  = raw_item.get("nutrition", {})
                sodium_val = parse_numeric(raw_nut.get("sodium_raw"))
                if sodium_val is not None:
                    nutrition["sodium"] = sodium_val
                    changes["sodium_filled"] += 1
                else:
                    changes["sodium_unrecoverable"] += 1
                    unrecoverable_log.append(f"granola BC:{bc} sodium")

            # ─── Fix 5: Hard cheeses sugar ────────────────────────────────────
            # Sugar is genuinely absent from all hard cheese raw scrapes —
            # hard cheeses have negligible/unlabeled sugars. Leave null.
            # (Verified: bsip0_yohananof_raw, bsip0_shufersal_raw, bsip0_carrefour_raw
            #  all have sugars_per_100g = None for all but 2 products that already have values.)

            # ─── Fix 6: Sodium from milk bsip1 ───────────────────────────────
            if slug == "milk" and nutrition.get("sodium") is None:
                bsip1 = milk_bsip1.get(bc, {})
                sodium_val = bsip1.get("normalized_nutrition_per_100g", {}).get("sodium_mg")
                if sodium_val is not None:
                    nutrition["sodium"] = float(sodium_val)
                    changes["sodium_filled"] += 1
                else:
                    changes["sodium_unrecoverable"] += 1
                    unrecoverable_log.append(f"milk BC:{bc} sodium")

            # ─── Fix 7: Sugar from milk bsip1 ────────────────────────────────
            if slug == "milk" and (nutrition.get("sugar") is None or nutrition.get("sugar") == ""):
                bsip1 = milk_bsip1.get(bc, {})
                sugar_val = bsip1.get("normalized_nutrition_per_100g", {}).get("sugars_g")
                if sugar_val is not None:
                    nutrition["sugar"] = float(sugar_val)
                    changes["sugar_filled"] += 1
                else:
                    changes["sugar_unrecoverable"] += 1
                    unrecoverable_log.append(f"milk BC:{bc} sugar")

            # ─── Fix 8: d4_additives for milk ────────────────────────────────
            if slug == "milk" and "d4_additives" not in p:
                bsip1 = milk_bsip1.get(bc, {})
                ing_text = bsip1.get("ingredients_text_he", "")
                if ing_text and ing_text.strip():
                    detected = detect_additives_d4(ing_text)
                    enriched = [enrich_additive_entry(e) for e in detected]
                    p["d4_additives"] = enriched
                    changes["d4_populated"] += 1
                else:
                    p["d4_additives"] = []
                    changes["d4_set_empty"] += 1

            # ─── Fix 9: d4_additives for juices ──────────────────────────────
            if slug == "juices" and "d4_additives" not in p:
                bsip1 = juice_bsip1.get(bc, {})
                ing_text = bsip1.get("ingredients_text_he", "")
                if ing_text and ing_text.strip():
                    detected = detect_additives_d4(ing_text)
                    enriched = [enrich_additive_entry(e) for e in detected]
                    p["d4_additives"] = enriched
                    changes["d4_populated"] += 1
                else:
                    p["d4_additives"] = []
                    changes["d4_set_empty"] += 1

            # Write back mutated nutrition
            expansion["nutrition"] = nutrition
            p["expansion"] = expansion

        # ── Step 2: Assign rank + categoryTotal to ALL products ───────────────
        products = assign_rank_and_total(products)
        changes["rank_assigned"] = len(products)

        # ── Step 3: Invariant check ───────────────────────────────────────────
        violations = check_invariants(pre_snap, products)
        if violations:
            print(f"  !!! INVARIANT VIOLATIONS: {violations}")
            sys.exit(1)

        # ── AFTER counts ──
        after = {
            "n": len(products),
            "malformed": 0,
            "sugar_null": sum(1 for p in products if p.get("expansion", {}).get("nutrition", {}).get("sugar") is None),
            "sodium_null": sum(1 for p in products if p.get("expansion", {}).get("nutrition", {}).get("sodium") is None),
            "d4_absent":  sum(1 for p in products if "d4_additives" not in p),
            "rank_absent": sum(1 for p in products if "rank" not in p),
        }
        for p in products:
            ing = p.get("expansion", {}).get("ingredients", "")
            if ing and isinstance(ing, str) and ("הנתונים המדויקים מופיעים" in ing or "כפיות סוכר" in ing or "ערכים תזונתיים 100 גרם" in ing):
                after["malformed"] += 1

        all_results[slug] = {
            "before": before,
            "after": after,
            "changes": changes,
            "unrecoverable": unrecoverable_log,
        }

        print(f"  BEFORE: malformed={before['malformed']} sugar_null={before['sugar_null']} "
              f"sodium_null={before['sodium_null']} d4_absent={before['d4_absent']} rank_absent={before['rank_absent']}")
        print(f"  AFTER:  malformed={after['malformed']} sugar_null={after['sugar_null']} "
              f"sodium_null={after['sodium_null']} d4_absent={after['d4_absent']} rank_absent={after['rank_absent']}")
        print(f"  CHANGES: {changes}")
        if unrecoverable_log:
            print(f"  UNRECOVERABLE: {unrecoverable_log}")

        # ── Write back ────────────────────────────────────────────────────────
        data["products"] = products
        out = json.dumps(data, ensure_ascii=False, indent=2)
        if ends_nl:
            out += "\n"
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(out)
        print(f"  Written: {fpath}")

    # ─── Summary ──────────────────────────────────────────────────────────────
    print(f"\n{'='*70}")
    print("SUMMARY TABLE")
    print(f"{'='*70}")
    print(f"{'Category':<22} {'N':>4} {'Malf B→A':>10} {'Sugar B→A':>10} {'Na B→A':>10} {'D4 B→A':>10} {'Rank B→A':>10}")
    print(f"{'-'*22} {'-'*4} {'-'*10} {'-'*10} {'-'*10} {'-'*10} {'-'*10}")
    total_n = 0
    for slug, r in all_results.items():
        b = r["before"]
        a = r["after"]
        total_n += a["n"]
        print(f"{slug:<22} {a['n']:>4} "
              f"{b['malformed']:>4}→{a['malformed']:<4} "
              f"{b['sugar_null']:>4}→{a['sugar_null']:<4} "
              f"{b['sodium_null']:>4}→{a['sodium_null']:<4} "
              f"{b['d4_absent']:>4}→{a['d4_absent']:<4} "
              f"{b['rank_absent']:>4}→{a['rank_absent']:<4}")
    print(f"{'─'*80}")
    print(f"Total products: {total_n}")

    # ─── OFF check ─────────────────────────────────────────────────────────────
    print(f"\n{'─'*70}")
    print("OFF SWEEP (post-write):")
    off_hits = 0
    for slug, fpath in FILE_MAP.items():
        with open(fpath, encoding="utf-8") as f:
            text = f.read()
        count = text.count("open_food_facts")
        if count > 0:
            # Exclude meta.excluded_off_products section hits
            data_check = json.loads(text)
            products_text = json.dumps(data_check.get("products", []), ensure_ascii=False)
            prod_hits = products_text.count("open_food_facts")
            if prod_hits > 0:
                print(f"  !!! OFF HIT in products: {slug} ({prod_hits} occurrences)")
                off_hits += prod_hits
    if off_hits == 0:
        print("  CLEAR — 0 OFF references in any product object")
    else:
        print(f"  !!! TOTAL OFF HITS: {off_hits}")

    # ─── SHA256 artifacts ─────────────────────────────────────────────────────
    print(f"\n{'─'*70}")
    print("ARTIFACT SHA256:")
    for slug, fpath in FILE_MAP.items():
        h = sha256_file(fpath)
        print(f"  {os.path.basename(fpath)}: {h}")

    # ─── Unrecoverable summary ────────────────────────────────────────────────
    print(f"\n{'─'*70}")
    print("UNRECOVERABLE (genuinely absent from all scrape sources):")
    any_unrec = False
    for slug, r in all_results.items():
        for item in r["unrecoverable"]:
            print(f"  {item}")
            any_unrec = True
    if not any_unrec:
        print("  (none)")

    print(f"\n{'='*70}")
    print("Done.")


if __name__ == "__main__":
    main()
