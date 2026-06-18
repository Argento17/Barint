"""
BSIP1 run_brined_cheeses_002 — corpus hygiene pass.

Applies the following RT-verified fixes to produce a cleaned BSIP1 corpus:

Fix 1 (RT-2/RT-6/RT-13):
  bc-035 (barcode 7290114310550) and bc-045 (barcode 2107071) — marketing copy in
  ingredients field. NULL ingredients, set ingredient_text_quality="marketing_bleed",
  confidence downgraded to partial, ingredient_count→0, ingredients_list→[].

Fix 2 (RT-9/RT-10/RT-11 — source-text hygiene):
  - Trailing ".n" and " n" scrape artifacts stripped from ingredients_text_he and
    the last element of ingredients_list.
  - "ערכים תזונתיים" nutrition-label bleed stripped from ingredient strings.
  - "ח.משמר).(E-202" reversed-parenthesis artifact corrected to "ח.משמר (E-202)".
  - Split word "פ וטסיום" repaired to "פוטסיום".
  - Typo "פנטסיום" corrected to "פוטסיום" (bc-006 barcode 7290011499129,
    bc-031 barcode 7290019635222).

Fix 3 (RT-11):
  bc-001 (barcode 7290019635826) canonical name "קוביות פטה עיזים מעודנ5%"
  corrected to "קוביות פטה עיזים מעודנת 5%".

Source: run_brined_001 (48 files).
Output: run_brined_002/output/ (all 48 files; unchanged files are copied verbatim).
"""

import json
import re
import os
import shutil
from pathlib import Path

SRC = Path("C:/Bari/03_operations/bsip1/run_brined_cheeses_001/output")
DST = Path("C:/Bari/03_operations/bsip1/run_brined_cheeses_002/output")
DST.mkdir(parents=True, exist_ok=True)

MARKETING_BARCODES = {"7290114310550", "2107071"}
TYPO_BARCODES = {"7290011499129", "7290019635222"}  # פנטסיום → פוטסיום
NAME_FIX_BARCODE = "7290019635826"  # bc-001 name truncation

MARKETING_MARKER = "משק צוריאל הוא מותג"

changes = []

def strip_trailing_artifacts(text: str) -> str:
    """Strip trailing .n / n scrape artifacts."""
    text = re.sub(r'\s*\.n\s*$', '', text.rstrip())
    text = re.sub(r'\s+n\s*$', '', text.rstrip())
    return text.strip()

def strip_nutrition_bleed(text: str) -> str:
    """Strip 'ערכים תזונתיים' and everything after it."""
    idx = text.find("ערכים תזונתיים")
    if idx != -1:
        text = text[:idx].rstrip(" ,")
    return text

def fix_reversed_parenthesis(text: str) -> str:
    """Fix ח.משמר).(E-202 → ח.משמר (E-202)"""
    # Pattern: word).(E-NNN → word (E-NNN)
    text = re.sub(r'([\w\.]+)\)\.\(E-(\d+)', r'\1 (E-\2)', text)
    return text

def fix_split_potassium(text: str) -> str:
    """Fix 'פ וטסיום' → 'פוטסיום'"""
    return text.replace("פ וטסיום", "פוטסיום")

def fix_typo_potassium(text: str) -> str:
    """Fix 'פנטסיום' → 'פוטסיום' (transposition error in source label/scrape)."""
    return text.replace("פנטסיום", "פוטסיום")

def clean_ingredient_text(text: str, fixes_log: list) -> str:
    """Apply all text-hygiene fixes and log what changed."""
    original = text
    text = strip_trailing_artifacts(text)
    text = strip_nutrition_bleed(text)
    text = fix_reversed_parenthesis(text)
    text = fix_split_potassium(text)
    if text != original:
        fixes_log.append(f"  ingredients_text: {repr(original)} → {repr(text)}")
    return text

def clean_ingredient_list(lst: list, fixes_log: list) -> list:
    """Apply hygiene fixes to each item in the ingredient list."""
    cleaned = []
    for item in lst:
        orig = item
        item = strip_trailing_artifacts(item)
        item = strip_nutrition_bleed(item)
        item = fix_reversed_parenthesis(item)
        item = fix_split_potassium(item)
        if item != orig:
            fixes_log.append(f"  ing_list item: {repr(orig)} → {repr(item)}")
        if item:  # drop empty strings after cleanup
            cleaned.append(item)
    return cleaned

def is_marketing_text(text: str) -> bool:
    return MARKETING_MARKER in (text or "")

processed = 0
skipped = 0

for src_file in sorted(SRC.glob("bsip1_brinedcheese_*.json")):
    with open(src_file, encoding="utf-8") as f:
        product = json.load(f)

    barcode = str(product.get("barcode", ""))
    product_fixes = []
    modified = False

    # --- Fix 1: Marketing copy nullification ---
    if barcode in MARKETING_BARCODES:
        ing_text = product.get("ingredients_text_he", "")
        if is_marketing_text(ing_text):
            product["ingredients_text_he"] = None
            product["ingredients_list"] = []
            product["ingredient_count"] = 0
            product["ingredient_text_quality"] = "marketing_bleed"
            # Downgrade confidence: was 0.75 (medium), stays medium but with lower score
            # The confidence field in BSIP1 is descriptive (0.0-1.0); we deduct
            # for marketing_bleed as if it were corrupted data.
            old_conf = product.get("confidence", 0.75)
            product["confidence"] = max(0.0, old_conf - 0.25)
            product["canonical_trust_level"] = "low"
            product["canonical_trust_score"] = max(0.0, product.get("canonical_trust_score", 0.75) - 0.25)
            risk_flags = product.get("canonical_risk_flags", [])
            if "marketing_bleed_ingredients" not in risk_flags:
                risk_flags.append("marketing_bleed_ingredients")
            product["canonical_risk_flags"] = risk_flags
            # BSIP1 trust fields
            product["bsip1_trust_level"] = "low"
            product["bsip1_trust_score"] = max(0.0, product.get("bsip1_trust_score", 0.75) - 0.25)
            risk_flags2 = product.get("bsip1_risk_flags", [])
            if "marketing_bleed_ingredients" not in risk_flags2:
                risk_flags2.append("marketing_bleed_ingredients")
            product["bsip1_risk_flags"] = risk_flags2
            product_fixes.append(f"  MARKETING COPY NULLIFIED: ingredients→null, ingredient_text_quality→marketing_bleed, confidence downgraded")
            modified = True

    # --- Fix 2: Source-text hygiene ---
    if not modified or barcode not in MARKETING_BARCODES:
        # Only apply text hygiene to non-marketing-nullified products
        ing_text = product.get("ingredients_text_he")
        if ing_text:
            new_text = clean_ingredient_text(ing_text, product_fixes)
            if new_text != ing_text:
                product["ingredients_text_he"] = new_text
                modified = True

        ing_list = product.get("ingredients_list", [])
        new_list = clean_ingredient_list(ing_list, product_fixes)
        if new_list != ing_list:
            product["ingredients_list"] = new_list
            product["ingredient_count"] = len(new_list)
            modified = True

    # --- Fix for פנטסיום typo (bc-006 and bc-031) ---
    if barcode in TYPO_BARCODES:
        ing_text = product.get("ingredients_text_he", "")
        if ing_text and "פנטסיום" in ing_text:
            new_text = fix_typo_potassium(ing_text)
            product["ingredients_text_he"] = new_text
            product_fixes.append(f"  TYPO FIX: פנטסיום→פוטסיום in ingredients_text")
            modified = True
        ing_list = product.get("ingredients_list", [])
        new_list = [fix_typo_potassium(i) for i in ing_list]
        if new_list != ing_list:
            product["ingredients_list"] = new_list
            product_fixes.append(f"  TYPO FIX: פנטסיום→פוטסיום in ingredients_list")
            modified = True

    # --- Fix 3: bc-001 name truncation ---
    if barcode == NAME_FIX_BARCODE:
        old_name = product.get("canonical_name_he", "")
        if "מעודנ5%" in old_name:
            new_name = old_name.replace("מעודנ5%", "מעודנת 5%")
            product["canonical_name_he"] = new_name
            product_fixes.append(f"  NAME FIX: {repr(old_name)} → {repr(new_name)}")
            modified = True

    # Update run_id
    product["run_id"] = "run_brined_002"

    dst_file = DST / src_file.name
    with open(dst_file, "w", encoding="utf-8") as f:
        json.dump(product, f, ensure_ascii=False, indent=2)

    if modified:
        changes.append(f"{src_file.name} (barcode {barcode}):")
        changes.extend(product_fixes)
        processed += 1
    else:
        skipped += 1

print("=== BSIP1 run_brined_cheeses_002 build complete ===")
print(f"Total files: {processed + skipped}")
print(f"Modified: {processed}")
print(f"Unchanged (copied): {skipped}")
print()
print("=== Changes Applied ===")
for line in changes:
    print(line)
