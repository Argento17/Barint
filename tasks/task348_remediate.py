"""
TASK-348 — Comprehensive malformed-ingredient sweep across all 10 live pages
=============================================================================
Scope:
  - cookies_coffee_frontend_v2.json   : 4 products with 'סך הדגנים במוצר' appended
  - snacks_frontend_v3.json           : 3 products with '*סך הדגנים במוצר:' appended
  - juices_frontend_v3.json           : 13 products with 'ערכים תזונתיים ערכים תזונתיים' prepended
  - All others: clean (grep hits are in rowVerdict/consumerTakeaway/category text, NOT ingredients)

Cleaning logic:
  APPEND patterns (cookies_coffee, snacks):
    - Cut from first occurrence of 'סך הדגנים' onward (may be preceded by '. ' or '*')
    - Also handles: הנתונים המדויקים, כפיות סוכר, ערכים תזונתיים 100, 100% מסך
  PREPEND pattern (juices):
    - Strip leading 'ערכים תזונתיים ' (one or more repetitions) from the start
    - The real ingredient text follows immediately after

Guardrails:
  - Clean ONLY ingredients field
  - NEVER touch score, grade, nutrition, additives, rank, or any other field
  - NEVER fabricate data
  - OFF banned
  - Staging only (bari-web/src/data/comparisons/*.json)
"""

import json
import os
import re
import sys
import hashlib
import copy

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

COMP_DIR = "C:/Bari/bari-web/src/data/comparisons"

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

# ─── All detection markers (exhaustive) ───────────────────────────────────────
APPEND_MARKERS = [
    r"[\.*]\s*סך הדגנים",   # '*סך הדגנים' (snacks) or '. סך הדגנים' (cookies_coffee)
    r"\.\s*סך הדגנים",      # '. סך הדגנים' pattern
    r"\bסך הדגנים",         # 'סך הדגנים' anywhere in middle
    r"ערכים תזונתיים\s+100",
    r"ערכים תזונתיים\s*\n",
    r"הנתונים המדויקים",
    r"כפיות סוכר",
    r"100% מסך הדגנים",
    # scraper linebreak artifact BEFORE a marker (e.g., "...לימון).nסך הדגנים")
    r"n\s*סך הדגנים",
]

# PREPEND pattern: "ערכים תזונתיים" (possibly doubled) at very start
PREPEND_PATTERN = re.compile(r"^(?:ערכים תזונתיים\s+)+", re.UNICODE)

# Strip trailing period/comma/space artifacts after cutting
SUFFIX_STRIP = re.compile(r"[\s.,n]+$")


def sha256_file(path: str) -> str:
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def snapshot_invariants(products: list) -> dict:
    """Capture score+grade for every product before cleaning."""
    return {p["id"]: {"score": p.get("score"), "grade": p.get("grade")} for p in products}


def check_invariants(pre: dict, post_products: list) -> list:
    violations = []
    for p in post_products:
        pid = p["id"]
        if pid not in pre:
            continue
        if p.get("score") != pre[pid]["score"]:
            violations.append(f"{pid}: score {pre[pid]['score']} -> {p.get('score')}")
        if p.get("grade") != pre[pid]["grade"]:
            violations.append(f"{pid}: grade {pre[pid]['grade']} -> {p.get('grade')}")
    return violations


def detect_malformed(ing: str) -> bool:
    """Return True if the ingredient string contains appended or prepended panel text."""
    if not ing or not isinstance(ing, str):
        return False
    # Prepend pattern (juices)
    if PREPEND_PATTERN.match(ing):
        return True
    # Append patterns
    for pat in APPEND_MARKERS:
        if re.search(pat, ing):
            return True
    return False


def clean_ingredients(ing: str, bc: str = "") -> str:
    """
    Remove appended nutrition-panel text or prepended 'ערכים תזונתיים' header.
    Returns cleaned string; does NOT return None (caller handles empty→None if needed).
    """
    if not ing or not isinstance(ing, str):
        return ing

    cleaned = ing

    # ── Step 1: strip prepended 'ערכים תזונתיים' header (juices pattern) ──────
    cleaned = PREPEND_PATTERN.sub("", cleaned)

    # ── Step 2: find earliest append cut point ────────────────────────────────
    # We look for 'סך הדגנים' including when preceded by '. ' or '*' or 'n'
    earliest = len(cleaned)

    # Primary: bare 'סך הדגנים'
    m = re.search(r"סך הדגנים", cleaned)
    if m:
        # Walk back to include the separator character (., *, space, n) if immediately before
        start = m.start()
        # Check for separator chars just before: '. ', '*', 'n' (scraper newline artifact)
        look_back = cleaned[max(0, start - 2):start]
        if look_back and look_back[-1] in (".", "*", "n", " "):
            # find the real start of the real sentence end
            # Only strip if the separator immediately precedes (no gap)
            sep_pos = start - 1
            while sep_pos >= 0 and cleaned[sep_pos] in (". ", "*", "n", " ", "."):
                sep_pos -= 1
            # Don't go further back than where the sentence ends naturally
            # Use the . or n character position as the cut, not earlier
            cut = start - (len(look_back) - len(look_back.rstrip(". *n")))
            if cut < earliest:
                earliest = cut
        else:
            if start < earliest:
                earliest = start

    # Additional markers
    other_markers = [
        r"ערכים תזונתיים\s+100",
        r"הנתונים המדויקים",
        r"כפיות סוכר",
        r"100% מסך הדגנים",
    ]
    for pat in other_markers:
        mm = re.search(pat, cleaned)
        if mm and mm.start() < earliest:
            earliest = mm.start()

    if earliest < len(cleaned):
        cleaned = cleaned[:earliest]

    # ── Step 3: strip trailing separators/artifacts ───────────────────────────
    cleaned = SUFFIX_STRIP.sub("", cleaned).strip()

    return cleaned


def main():
    print("TASK-348 — Comprehensive malformed-ingredient sweep")
    print("=" * 70)

    results = {}

    for slug, fpath in FILE_MAP.items():
        print(f"\n{'─'*70}")
        print(f"Processing: {slug}")

        with open(fpath, encoding="utf-8") as f:
            raw_text = f.read()
        ends_nl = raw_text.endswith("\n")
        data = json.loads(raw_text)

        products = data["products"]
        pre_snap = snapshot_invariants(products)

        # ── Count malformed BEFORE ────────────────────────────────────────────
        before_malformed = 0
        malformed_ids = []
        for p in products:
            ing = p.get("expansion", {}).get("ingredients", "")
            if detect_malformed(ing):
                before_malformed += 1
                malformed_ids.append(p.get("id", "?"))

        print(f"  BEFORE: {before_malformed} malformed ingredients")
        if malformed_ids:
            print(f"  IDs: {malformed_ids}")

        cleaned_count = 0

        # ── Clean ingredients ─────────────────────────────────────────────────
        for p in products:
            exp = p.get("expansion", {})
            ing = exp.get("ingredients", "")
            if detect_malformed(ing):
                orig = ing
                cleaned = clean_ingredients(ing, bc=str(p.get("barcode", "")))
                if cleaned != orig:
                    exp["ingredients"] = cleaned
                    p["expansion"] = exp
                    cleaned_count += 1
                    print(f"  CLEANED {p.get('id')} BC:{p.get('barcode')}")
                    print(f"    BEFORE: {orig[:120]!r}")
                    print(f"    AFTER:  {cleaned[:120]!r}")

        # ── Invariant check (score/grade must not change) ─────────────────────
        violations = check_invariants(pre_snap, products)
        if violations:
            print(f"  !!! INVARIANT VIOLATIONS:")
            for v in violations:
                print(f"    {v}")
            sys.exit(1)

        # ── Count malformed AFTER ─────────────────────────────────────────────
        after_malformed = 0
        still_malformed = []
        for p in products:
            ing = p.get("expansion", {}).get("ingredients", "")
            if detect_malformed(ing):
                after_malformed += 1
                still_malformed.append((p.get("id"), ing[:100]))

        if still_malformed:
            print(f"  !!! STILL MALFORMED ({after_malformed}):")
            for pid, snippet in still_malformed:
                print(f"    {pid}: {snippet!r}")

        print(f"  AFTER:  {after_malformed} malformed | cleaned: {cleaned_count}")

        results[slug] = {
            "n": len(products),
            "before_malformed": before_malformed,
            "after_malformed": after_malformed,
            "cleaned": cleaned_count,
        }

        # ── Write back (only if changes were made) ────────────────────────────
        if cleaned_count > 0:
            data["products"] = products
            out = json.dumps(data, ensure_ascii=False, indent=2)
            if ends_nl:
                out += "\n"
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(out)
            print(f"  Written: {fpath}")
        else:
            print(f"  No changes — file not rewritten.")

    # ─── Summary ──────────────────────────────────────────────────────────────
    print(f"\n{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}")
    print(f"{'Category':<22} {'N':>4} {'Before':>8} {'After':>7} {'Cleaned':>8}")
    print(f"{'-'*22} {'-'*4} {'-'*8} {'-'*7} {'-'*8}")
    total_before = 0
    total_after = 0
    total_cleaned = 0
    for slug, r in results.items():
        total_before += r["before_malformed"]
        total_after += r["after_malformed"]
        total_cleaned += r["cleaned"]
        print(f"{slug:<22} {r['n']:>4} {r['before_malformed']:>8} {r['after_malformed']:>7} {r['cleaned']:>8}")
    print(f"{'TOTAL':<22} {'':>4} {total_before:>8} {total_after:>7} {total_cleaned:>8}")

    if total_after > 0:
        print(f"\n!!! {total_after} malformed ingredients REMAIN — check above for ambiguous cases")
        sys.exit(1)
    else:
        print(f"\nAll malformed ingredients cleaned. Remaining: 0")

    # ─── OFF sweep ────────────────────────────────────────────────────────────
    print(f"\n{'─'*70}")
    print("OFF SWEEP (product objects only):")
    off_hits = 0
    for slug, fpath in FILE_MAP.items():
        with open(fpath, encoding="utf-8") as f:
            data = json.load(f)
        products_text = json.dumps(data.get("products", []), ensure_ascii=False)
        count = products_text.count("open_food_facts")
        if count > 0:
            print(f"  !!! OFF HIT in products: {slug} ({count} occurrences)")
            off_hits += count
    if off_hits == 0:
        print("  CLEAR — 0 OFF references in any product object")
    else:
        print(f"  !!! TOTAL OFF HITS: {off_hits}")
        sys.exit(1)

    # ─── SHA256 artifacts ─────────────────────────────────────────────────────
    print(f"\n{'─'*70}")
    print("ARTIFACT SHA256:")
    for slug, fpath in FILE_MAP.items():
        h = sha256_file(fpath)
        print(f"  {os.path.basename(fpath)}: {h}")

    print(f"\n{'='*70}")
    print("Done.")


if __name__ == "__main__":
    main()
