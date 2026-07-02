"""
ingredient_reading_diagnosis.py
================================
TASK-395 — Diagnose ingredient-reading failures on the real corpus (gold set).

Standalone — no imports from engine src/. stdlib only.

Analyzes matrix_gold_set_v1.json to quantify the confirmed expand_composites bug:
  When ingredient text has (X%) (מכיל גלוטן) — the sub_match regex fires on the
  FIRST parenthetical (the allergen declaration), treats it as a composite parent,
  and the ingredient is lost from marker extraction.

Tasks:
  1. Bug-type frequency analysis
  2. Percentage phrasings inventory
  3. stated_pct extraction accuracy simulation
  4. Whole/refined qualifier coverage + BSIP1 vs BSIP2 probe comparison

Outputs:
  ingredient_reading_diagnosis_numbers.txt  (human-readable, full Hebrew)
  ingredient_reading_diagnosis_numbers.json (machine-readable, ASCII-safe reprs)
"""

import json
import re
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional

# ─────────────────────────────────────────────────────────────────────────────
# Paths
# ─────────────────────────────────────────────────────────────────────────────
REPO_ROOT   = Path("C:/Bari")
GOLD_SET    = REPO_ROOT / "03_operations/bsip2/proto_v0/analysis/matrix_gold_set_v1.json"
OUT_DIR     = REPO_ROOT / "03_operations/bsip2/proto_v0/analysis"
OUT_TXT     = OUT_DIR / "ingredient_reading_diagnosis_numbers.txt"
OUT_JSON    = OUT_DIR / "ingredient_reading_diagnosis_numbers.json"

# ─────────────────────────────────────────────────────────────────────────────
# Hebrew allergen / containment phrases that mark a declaration, NOT a sub-recipe
# ─────────────────────────────────────────────────────────────────────────────
ALLERGEN_RE = re.compile(r"מכיל|עלול להכיל|יתכן.*מכיל")

# ─────────────────────────────────────────────────────────────────────────────
# Percentage patterns
# ─────────────────────────────────────────────────────────────────────────────
# Captures the numeric portion of any percent expression
PCT_BARE_RE        = re.compile(r"[\(≈~]?\s*(\d+(?:\.\d+)?)\s*%\s*[\)]?")
# (54%) form — percentage alone inside parens
PCT_PAREN_BARE_RE  = re.compile(r"\(\s*(\d+(?:\.\d+)?)\s*%\s*\)")
# X% מהמוצר / X% ממשקל המוצר
PCT_PRODUCT_WT_RE  = re.compile(r"(\d+(?:\.\d+)?)\s*%\s*(?:מהמוצר|ממשקל\s+המוצר|מהמשקל\s+הכולל)")
# X% מהקמחים / X% מסך הקמחים / X% מהקמח
PCT_FLOUR_WT_RE    = re.compile(r"(\d+(?:\.\d+)?)\s*%\s*(?:מהקמח|מהקמחים|מסך\s+הקמח|מסך\s+הקמחים)")
# Sub-pct: percentage inside a parenthetical that itself is inside another paren → hard to detect
# We approximate: a percentage that is NOT the first paren-group percentage at the item level

# ─────────────────────────────────────────────────────────────────────────────
# Whole / refined qualifier patterns
# ─────────────────────────────────────────────────────────────────────────────
WHOLE_QUAL_RE   = re.compile(r"מלאה?|מלאים")
REFINED_QUAL_RE = re.compile(r"לבנה?|בהיר")

# ─────────────────────────────────────────────────────────────────────────────
# Ingredient item splitter — replicates BSIP1 logic (depth-0 comma split only)
# ─────────────────────────────────────────────────────────────────────────────
def split_depth0(text: str) -> list:
    """Split on commas/semicolons at parenthesis depth == 0 (BSIP1 behaviour)."""
    parts = []
    depth = 0
    current = []
    for ch in text:
        if ch in "({[":
            depth += 1
            current.append(ch)
        elif ch in ")}]":
            depth = max(0, depth - 1)
            current.append(ch)
        elif ch in ",;" and depth == 0:
            s = "".join(current).strip()
            if s:
                parts.append(s)
            current = []
        else:
            current.append(ch)
    s = "".join(current).strip()
    if s:
        parts.append(s)
    return parts


# ─────────────────────────────────────────────────────────────────────────────
# Reproduce the BSIP2 probe's sub_match regex (the buggy line)
# ─────────────────────────────────────────────────────────────────────────────
# From matrix_signal_probe_v2.py line 230:
SUB_MATCH_RE = re.compile(r'^(.*?)\s*\(([^)]*%[^)]*)\)')

def _extract_item_pct(item: str) -> Optional[float]:
    """Reproduce probe v2 _extract_item_pct."""
    m = re.search(r'[\(≈~]?\s*(\d+(?:\.\d+)?)\s*%', item)
    if m:
        v = float(m.group(1))
        if 0.1 <= v <= 100.0:
            return v
    return None

def probe_expand_fires_bug(item: str) -> bool:
    """
    Return True if the BSIP2 probe's expand_composites would fire on this item
    in the bug-triggering way: sub_match fires AND item_pct is not None,
    causing is_composite_parent=True and a useless sub_text fragment.
    """
    item_pct = _extract_item_pct(item)
    if item_pct is None:
        return False
    sub_match = SUB_MATCH_RE.search(item)
    if sub_match:
        sub_text = sub_match.group(2)
        # Bug is specifically harmful when sub_text matches an allergen declaration
        # OR when sub_text is just a bare percentage (e.g. "54%") with no real sub-ingredients
        return True
    return False

def probe_bug_is_harmful(item: str) -> bool:
    """
    True if the bug fires AND the sub_text is an allergen or bare percentage
    (meaning no real sub-ingredients exist — the item is misclassified as composite).
    """
    item_pct = _extract_item_pct(item)
    if item_pct is None:
        return False
    sub_match = SUB_MATCH_RE.search(item)
    if not sub_match:
        return False
    sub_text = sub_match.group(2).strip()
    # sub_text is harmful-false-positive if:
    # (a) it is ONLY a percentage: "54%" / "40.8%" / "98%"
    # (b) it is an allergen declaration: "מכיל גלוטן", "מכיל סויה", etc.
    is_bare_pct   = bool(re.fullmatch(r'\s*[\d.]+\s*%\s*', sub_text))
    is_allergen    = bool(ALLERGEN_RE.search(sub_text))
    return is_bare_pct or is_allergen


# ─────────────────────────────────────────────────────────────────────────────
# Bug-type classifiers (Task 1)
# ─────────────────────────────────────────────────────────────────────────────
def classify_bug_types(item: str) -> set:
    """Return set of bug-type codes that apply to this item."""
    types = set()
    has_pct = bool(PCT_BARE_RE.search(item))

    # Count parenthetical groups in the item
    paren_groups = re.findall(r'\([^()]*\)', item)

    # Check for allergen declaration
    allergen_parens = [pg for pg in paren_groups if ALLERGEN_RE.search(pg)]
    has_allergen_paren = len(allergen_parens) > 0

    # ALLERGEN_PLUS_PCT: item has (מכיל ...) AND a percentage
    if has_allergen_paren and has_pct:
        types.add("ALLERGEN_PLUS_PCT")

    # DOUBLE_PAREN_PCT: has at least 2 parenthetical groups AND a pct in one of them
    pct_parens = [pg for pg in paren_groups if re.search(r'\d+(?:\.\d+)?\s*%', pg)]
    if len(paren_groups) >= 2 and len(pct_parens) >= 1:
        types.add("DOUBLE_PAREN_PCT")

    # PCT_ONLY_PAREN: has a paren group that is ONLY a percentage (and nothing else)
    for pg in paren_groups:
        inner = pg[1:-1].strip()
        if re.fullmatch(r'[\d.]+\s*%', inner):
            types.add("PCT_ONLY_PAREN")
            break

    # CURLY_OR_BRACKET: item uses { } or [ ]
    if re.search(r'[{\[\]}]', item):
        types.add("CURLY_OR_BRACKET")

    # MULTILEVEL_NESTING: item has nested parentheses
    if re.search(r'\([^()]*\([^()]*\)[^()]*\)', item):
        types.add("MULTILEVEL_NESTING")

    return types


# ─────────────────────────────────────────────────────────────────────────────
# Main analysis
# ─────────────────────────────────────────────────────────────────────────────
def run_analysis():
    # ── Load gold set ──────────────────────────────────────────────────────────
    with open(GOLD_SET, encoding="utf-8") as f:
        gold = json.load(f)

    products = gold["products"]
    total_products = len(products)

    # Products with ingredient text (exclude UNREADABLE / None)
    products_with_text = [
        p for p in products
        if p.get("ingredients_text_he") and p.get("tier") != "UNREADABLE"
    ]
    n_with_text = len(products_with_text)

    # ══════════════════════════════════════════════════════════════════════════
    # TASK 1: Bug-type frequency analysis
    # ══════════════════════════════════════════════════════════════════════════
    bug_type_product_sets  = {k: set() for k in [
        "ALLERGEN_PLUS_PCT", "DOUBLE_PAREN_PCT", "PCT_ONLY_PAREN",
        "CURLY_OR_BRACKET", "MULTILEVEL_NESTING"
    ]}
    bug_type_item_counts   = {k: 0 for k in bug_type_product_sets}
    bug_examples           = {k: [] for k in bug_type_product_sets}

    # Also track: items where the probe bug fires harmfully
    harmful_bug_products   = set()
    harmful_bug_items      = []   # (barcode, item_text)
    harmful_bug_item_count = 0

    for p in products_with_text:
        barcode  = p["barcode"]
        ing_text = p["ingredients_text_he"]
        items    = split_depth0(ing_text)

        for item in items:
            bug_types = classify_bug_types(item)
            for bt in bug_types:
                bug_type_product_sets[bt].add(barcode)
                bug_type_item_counts[bt] += 1
                if len(bug_examples[bt]) < 5:
                    bug_examples[bt].append({
                        "barcode": barcode,
                        "name_he": p.get("name_he", ""),
                        "item": item,
                    })

            if probe_bug_is_harmful(item):
                harmful_bug_item_count += 1
                harmful_bug_products.add(barcode)
                if len(harmful_bug_items) < 10:
                    harmful_bug_items.append({
                        "barcode": barcode,
                        "name_he": p.get("name_he", ""),
                        "item": item,
                        "item_pct": _extract_item_pct(item),
                    })

    task1 = {
        "total_products_analyzed": n_with_text,
        "bug_types": {},
        "harmful_bug": {
            "products_affected": len(harmful_bug_products),
            "items_affected": harmful_bug_item_count,
            "examples": harmful_bug_items,
        }
    }
    for bt in bug_type_product_sets:
        task1["bug_types"][bt] = {
            "products_affected": len(bug_type_product_sets[bt]),
            "items_affected": bug_type_item_counts[bt],
            "examples": bug_examples[bt],
        }

    # ══════════════════════════════════════════════════════════════════════════
    # TASK 2: Percentage phrasings inventory
    # ══════════════════════════════════════════════════════════════════════════
    phrasing_categories = {
        "BARE_PCT":          [],   # (54%) or 54% without qualifier
        "PCT_PRODUCT_WEIGHT":  [],   # X% מהמוצר / ממשקל המוצר
        "PCT_FLOUR_WEIGHT":    [],   # X% מהקמחים / מסך הקמחים
        "PCT_WITHIN_PARENT":   [],   # pct inside a sub-list paren (not bare)
    }

    for p in products_with_text:
        barcode  = p["barcode"]
        ing_text = p["ingredients_text_he"]
        items    = split_depth0(ing_text)

        for item in items:
            # PCT_PRODUCT_WEIGHT
            for m in PCT_PRODUCT_WT_RE.finditer(item):
                phrasing_categories["PCT_PRODUCT_WEIGHT"].append({
                    "barcode": barcode, "item": item, "value": m.group(0)
                })

            # PCT_FLOUR_WEIGHT
            for m in PCT_FLOUR_WT_RE.finditer(item):
                phrasing_categories["PCT_FLOUR_WEIGHT"].append({
                    "barcode": barcode, "item": item, "value": m.group(0)
                })

            # BARE_PCT: pct in parens that is not product-weight or flour-weight
            for m in PCT_PAREN_BARE_RE.finditer(item):
                # Check it's not already captured by the above
                surrounding = item[max(0, m.start()-5):m.end()+20]
                if not PCT_PRODUCT_WT_RE.search(surrounding) and not PCT_FLOUR_WT_RE.search(surrounding):
                    phrasing_categories["BARE_PCT"].append({
                        "barcode": barcode, "item": item, "value": m.group(0)
                    })

            # PCT_WITHIN_PARENT: percentage inside a paren group that has other content too
            paren_groups = re.findall(r'\(([^()]+)\)', item)
            for pg in paren_groups:
                if re.search(r'\d+(?:\.\d+)?\s*%', pg):
                    # Is it more than just a bare pct?
                    stripped = re.sub(r'\d+(?:\.\d+)?\s*%', '', pg).strip()
                    if stripped and not ALLERGEN_RE.search(pg):
                        # Real sub-list with percentages
                        phrasing_categories["PCT_WITHIN_PARENT"].append({
                            "barcode": barcode, "item": item, "sub_text": pg
                        })

    # Deduplicate by item text (keep first occurrence)
    for cat in phrasing_categories:
        seen = set()
        deduped = []
        for entry in phrasing_categories[cat]:
            key = entry.get("item", entry.get("sub_text", ""))
            if key not in seen:
                seen.add(key)
                deduped.append(entry)
        phrasing_categories[cat] = deduped

    # Count totals (before dedup is applied above — re-count per product)
    def count_matches_in_corpus(pattern, field="ingredients_text_he"):
        total = 0
        for p in products_with_text:
            total += len(pattern.findall(p[field]))
        return total

    task2 = {
        "BARE_PCT": {
            "count_unique_items": len(phrasing_categories["BARE_PCT"]),
            "examples": [e["item"] for e in phrasing_categories["BARE_PCT"][:8]],
        },
        "PCT_PRODUCT_WEIGHT": {
            "count_unique_items": len(phrasing_categories["PCT_PRODUCT_WEIGHT"]),
            "examples": [e["item"] for e in phrasing_categories["PCT_PRODUCT_WEIGHT"][:8]],
        },
        "PCT_FLOUR_WEIGHT": {
            "count_unique_items": len(phrasing_categories["PCT_FLOUR_WEIGHT"]),
            "examples": [e["item"] for e in phrasing_categories["PCT_FLOUR_WEIGHT"][:8]],
        },
        "PCT_WITHIN_PARENT": {
            "count_unique_items": len(phrasing_categories["PCT_WITHIN_PARENT"]),
            "examples": [e["item"] for e in phrasing_categories["PCT_WITHIN_PARENT"][:8]],
        },
    }

    # ══════════════════════════════════════════════════════════════════════════
    # TASK 3: stated_pct extraction accuracy simulation
    # ══════════════════════════════════════════════════════════════════════════
    # For each ingredient item:
    # A) Does it have a visible percentage in the text?
    # B) Would the probe's _extract_item_pct RETURN NONE because the item was
    #    classified as is_composite_parent=True (the bug) — meaning the parent
    #    item is SKIPPED in marker extraction, even though it has a real pct?
    # C) Does the item have a flour-weight denominator (should not be used as product-weight)?

    pct_correctly_captured   = 0   # has pct, bug does NOT fire harmfully
    pct_lost_to_bug          = 0   # has pct, bug fires → item skipped in marker extraction
    pct_flour_denominator    = 0   # pct is מהקמחים — wrong denominator

    lost_examples  = []
    flour_examples = []

    for p in products_with_text:
        barcode  = p["barcode"]
        ing_text = p["ingredients_text_he"]
        items    = split_depth0(ing_text)

        for item in items:
            item_has_pct = bool(PCT_BARE_RE.search(item))
            if not item_has_pct:
                continue

            # Flour-weight denominator check
            if PCT_FLOUR_WT_RE.search(item):
                pct_flour_denominator += 1
                if len(flour_examples) < 6:
                    flour_examples.append({"barcode": barcode, "item": item})
                continue   # Don't count as captured or lost — it's a different denominator

            # Bug check
            if probe_bug_is_harmful(item):
                pct_lost_to_bug += 1
                if len(lost_examples) < 8:
                    lost_examples.append({
                        "barcode": barcode,
                        "name_he": p.get("name_he", ""),
                        "item": item,
                        "item_pct": _extract_item_pct(item),
                    })
            else:
                pct_correctly_captured += 1

    task3 = {
        "pct_correctly_captured": pct_correctly_captured,
        "pct_lost_to_bug": pct_lost_to_bug,
        "pct_flour_denominator_excluded": pct_flour_denominator,
        "pct_loss_rate": round(pct_lost_to_bug / max(1, pct_lost_to_bug + pct_correctly_captured), 4),
        "lost_examples": lost_examples,
        "flour_denominator_examples": flour_examples,
    }

    # ══════════════════════════════════════════════════════════════════════════
    # TASK 4: Whole/refined qualifier coverage + BSIP1 vs BSIP2 comparison
    # ══════════════════════════════════════════════════════════════════════════
    whole_items_bsip1   = []   # items seen as single unit by BSIP1
    refined_items_bsip1 = []
    whole_items_probe   = []   # items the probe would CORRECTLY see (no bug)
    whole_items_lost    = []   # items with whole qualifier that are LOST by the probe bug

    whole_count_bsip1   = 0
    refined_count_bsip1 = 0
    whole_lost_count    = 0

    for p in products_with_text:
        barcode  = p["barcode"]
        ing_text = p["ingredients_text_he"]

        # BSIP1: splits at depth 0 only — sees each top-level item as atomic
        bsip1_items = split_depth0(ing_text)

        for item in bsip1_items:
            has_whole   = bool(WHOLE_QUAL_RE.search(item))
            has_refined = bool(REFINED_QUAL_RE.search(item))

            if has_whole:
                whole_count_bsip1 += 1
                if len(whole_items_bsip1) < 8:
                    whole_items_bsip1.append({"barcode": barcode, "item": item})

            if has_refined:
                refined_count_bsip1 += 1
                if len(refined_items_bsip1) < 8:
                    refined_items_bsip1.append({"barcode": barcode, "item": item})

            # Would the probe lose this item?
            if has_whole and probe_bug_is_harmful(item):
                whole_lost_count += 1
                if len(whole_items_lost) < 8:
                    whole_items_lost.append({
                        "barcode": barcode,
                        "name_he": p.get("name_he", ""),
                        "item": item,
                    })

    # Products where the probe would get the whole/refined label WRONG due to
    # losing the primary whole-grain ingredient
    # Specifically: T1 products where the first BSIP1 item has a whole qualifier
    # but the probe fires the bug on it → first ingredient lost
    t1_prods_with_first_item_lost = []
    for p in products_with_text:
        if p.get("tier") != "T1":
            continue
        barcode  = p["barcode"]
        ing_text = p["ingredients_text_he"]
        bsip1_items = split_depth0(ing_text)
        if bsip1_items:
            first_item = bsip1_items[0]
            if WHOLE_QUAL_RE.search(first_item) and probe_bug_is_harmful(first_item):
                t1_prods_with_first_item_lost.append({
                    "barcode": barcode,
                    "name_he": p.get("name_he", ""),
                    "first_item": first_item,
                })

    task4 = {
        "whole_items_bsip1_count": whole_count_bsip1,
        "refined_items_bsip1_count": refined_count_bsip1,
        "whole_items_lost_by_probe_bug": whole_lost_count,
        "t1_products_with_first_ingredient_lost": len(t1_prods_with_first_item_lost),
        "bsip1_behavior": (
            "BSIP1 _parse_ingredients_ordered splits at depth=0 only (no sub-composite expansion). "
            "It sees פתיתי שיבולת שועל מלאה (54%) (מכיל גלוטן) as a SINGLE item. "
            "CORRECT behavior: whole qualifier is visible, position=1 intact."
        ),
        "bsip2_probe_behavior": (
            "BSIP2 probe expand_composites fires sub_match on the FIRST paren group containing %. "
            "For items like X (54%) (מכיל גלוטן): sub_match captures (54%), sub_text='54%'. "
            "is_composite_parent=True → item SKIPPED in marker extraction. "
            "The whole oat/spelt/wheat DISAPPEARS from the marker list entirely."
        ),
        "t1_first_ingredient_lost_examples": t1_prods_with_first_item_lost[:8],
        "whole_item_examples_bsip1": whole_items_bsip1[:6],
        "whole_items_lost_examples": whole_items_lost[:6],
        "refined_item_examples_bsip1": refined_items_bsip1[:6],
    }

    # ══════════════════════════════════════════════════════════════════════════
    # Assemble full summary
    # ══════════════════════════════════════════════════════════════════════════
    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "gold_set_path": str(GOLD_SET),
        "total_products": total_products,
        "products_with_ingredient_text": n_with_text,
        "task1_bug_frequency": task1,
        "task2_pct_phrasings": task2,
        "task3_pct_extraction_accuracy": task3,
        "task4_whole_refined_coverage": task4,
        "verdict": {
            "bsip1_reading_failure": False,
            "bsip2_probe_reading_failure": True,
            "summary": (
                "BSIP1 (_parse_ingredients_ordered) does NOT have this bug. It treats "
                "each depth-0 comma-separated item atomically, so allergen declarations "
                "and percentages remain part of the ingredient token — the whole qualifier "
                "is preserved and correctly visible to downstream logic. "
                "BSIP2 probe (expand_composites in matrix_signal_probe_v2.py) has the confirmed bug: "
                "sub_match fires on the FIRST paren group that contains %, which includes "
                "(54%) standalone and (מכיל גלוטן) — neither is a composite sub-recipe. "
                "This marks the item is_composite_parent=True and skips it in marker extraction, "
                "causing whole-grain ingredients at position 1 to be silently dropped. "
                "The fix: before treating an item as composite, verify that (a) the parenthetical "
                "sub_text is NOT an allergen declaration and (b) NOT a bare percentage alone. "
                "Only expand when the paren content contains comma-separated sub-ingredients."
            ),
        },
    }

    return summary


# ─────────────────────────────────────────────────────────────────────────────
# Report writer
# ─────────────────────────────────────────────────────────────────────────────
def write_txt_report(s: dict, path: Path):
    lines = []
    add = lines.append

    add("=" * 80)
    add("BARI INGREDIENT READING DIAGNOSIS")
    add(f"Generated: {s['generated_at']}")
    add(f"Gold set:  {s['gold_set_path']}")
    add("=" * 80)
    add("")

    add(f"Total products in gold set:           {s['total_products']}")
    add(f"Products with ingredient text:        {s['products_with_ingredient_text']}")
    add("")

    # ── Task 1 ────────────────────────────────────────────────────────────────
    add("─" * 80)
    add("TASK 1: BUG-TYPE FREQUENCY ANALYSIS")
    add("─" * 80)

    t1 = s["task1_bug_frequency"]
    add(f"  Harmful bug fires (product skipped, whole grain LOST):")
    hb = t1["harmful_bug"]
    add(f"    Products affected: {hb['products_affected']} / {s['products_with_ingredient_text']}")
    add(f"    Items affected:    {hb['items_affected']}")
    add("")

    add(f"  Bug-type breakdown:")
    BT_DESCRIPTIONS = {
        "ALLERGEN_PLUS_PCT":   "(מכיל ...) paren AND a percentage in the same item — THE PRIMARY BUG",
        "DOUBLE_PAREN_PCT":    "Two or more parenthetical groups with a pct in one — fires sub_match",
        "PCT_ONLY_PAREN":      "(54%) alone — sub_text='54%', no real sub-ingredients",
        "CURLY_OR_BRACKET":    "{ } or [ ] used for sub-lists (not standard Hebrew label format)",
        "MULTILEVEL_NESTING":  "Nested parentheses ((...))",
    }
    for bt, desc in BT_DESCRIPTIONS.items():
        data = t1["bug_types"][bt]
        add(f"    {bt}")
        add(f"      {desc}")
        add(f"      Products: {data['products_affected']}  |  Items: {data['items_affected']}")
        if data["examples"]:
            add(f"      Examples:")
            for ex in data["examples"][:3]:
                add(f"        [{ex['barcode']}] {ex['name_he']}")
                add(f"          ITEM: {ex['item']}")
        add("")

    add(f"  Harmful-bug item examples (whole grain LOST):")
    for ex in hb["examples"][:6]:
        add(f"    [{ex['barcode']}] {ex['name_he']}  (item_pct={ex['item_pct']}%)")
        add(f"      ITEM: {ex['item']}")
    add("")

    # ── Task 2 ────────────────────────────────────────────────────────────────
    add("─" * 80)
    add("TASK 2: PERCENTAGE PHRASINGS INVENTORY")
    add("─" * 80)

    t2 = s["task2_pct_phrasings"]
    for cat, label in [
        ("BARE_PCT",           "BARE_PCT — standalone (54%) or 54% with no denominator qualifier"),
        ("PCT_PRODUCT_WEIGHT", "PCT_PRODUCT_WEIGHT — X% מהמוצר / X% ממשקל המוצר"),
        ("PCT_FLOUR_WEIGHT",   "PCT_FLOUR_WEIGHT — X% מהקמחים / X% מסך הקמחים  ← WRONG denominator for product-weight calc"),
        ("PCT_WITHIN_PARENT",  "PCT_WITHIN_PARENT — percentage inside a real sub-list parenthetical"),
    ]:
        data = t2[cat]
        add(f"  {label}")
        add(f"    Unique items: {data['count_unique_items']}")
        if data["examples"]:
            add(f"    Examples:")
            for ex in data["examples"][:4]:
                add(f"      {ex}")
        add("")

    # ── Task 3 ────────────────────────────────────────────────────────────────
    add("─" * 80)
    add("TASK 3: STATED_PCT EXTRACTION ACCURACY")
    add("─" * 80)

    t3 = s["task3_pct_extraction_accuracy"]
    total_pct_items = t3["pct_correctly_captured"] + t3["pct_lost_to_bug"]
    add(f"  Items where a percentage is present in text:")
    add(f"    Correctly captured by probe:        {t3['pct_correctly_captured']}")
    add(f"    Lost to bug (item skipped):         {t3['pct_lost_to_bug']}")
    add(f"    Flour-denominator (excluded):        {t3['pct_flour_denominator_excluded']}")
    add(f"    Pct-loss rate:                       {t3['pct_loss_rate'] * 100:.1f}%")
    add("")
    add(f"  Items lost to bug (probe marks as composite_parent, skips in marker extraction):")
    for ex in t3["lost_examples"][:6]:
        add(f"    [{ex['barcode']}] {ex['name_he']}  (pct={ex['item_pct']}%)")
        add(f"      ITEM: {ex['item']}")
    add("")
    add(f"  Items with מהקמחים denominator (different basis, should NOT be used as product-weight):")
    for ex in t3["flour_denominator_examples"][:4]:
        add(f"    [{ex['barcode']}] {ex['item']}")
    add("")

    # ── Task 4 ────────────────────────────────────────────────────────────────
    add("─" * 80)
    add("TASK 4: WHOLE / REFINED QUALIFIER COVERAGE")
    add("─" * 80)

    t4 = s["task4_whole_refined_coverage"]
    add(f"  Items with whole qualifiers (מלא/מלאה/מלאים) as seen by BSIP1:  {t4['whole_items_bsip1_count']}")
    add(f"  Items with refined qualifiers (לבן/לבנה/בהיר) as seen by BSIP1: {t4['refined_items_bsip1_count']}")
    add(f"  Whole-qualifier items LOST by probe bug:                         {t4['whole_items_lost_by_probe_bug']}")
    add(f"  T1 products where FIRST ingredient is lost by probe bug:         {t4['t1_products_with_first_ingredient_lost']}")
    add("")
    add(f"  BSIP1 behavior: {t4['bsip1_behavior']}")
    add("")
    add(f"  BSIP2 probe behavior: {t4['bsip2_probe_behavior']}")
    add("")
    add(f"  T1 products with first ingredient lost (CRITICAL — whole grain at position 1):")
    for ex in t4["t1_first_ingredient_lost_examples"][:6]:
        add(f"    [{ex['barcode']}] {ex['name_he']}")
        add(f"      FIRST ITEM: {ex['first_item']}")
    add("")
    add(f"  Sample whole-qualifier items as BSIP1 sees them (intact):")
    for ex in t4["whole_item_examples_bsip1"][:4]:
        add(f"    [{ex['barcode']}] {ex['item']}")
    add("")
    add(f"  Sample whole-qualifier items LOST by probe:")
    for ex in t4["whole_items_lost_examples"][:4]:
        add(f"    [{ex['barcode']}] {ex['name_he']}")
        add(f"      {ex['item']}")
    add("")

    # ── Verdict ───────────────────────────────────────────────────────────────
    add("─" * 80)
    add("VERDICT")
    add("─" * 80)
    v = s["verdict"]
    add(f"  BSIP1 reading failure:       {'YES' if v['bsip1_reading_failure'] else 'NO'}")
    add(f"  BSIP2 probe reading failure: {'YES' if v['bsip2_probe_reading_failure'] else 'NO'}")
    add("")
    # Wrap verdict text at 78 chars
    verdict_text = v["summary"]
    words = verdict_text.split()
    line = "  "
    for word in words:
        if len(line) + len(word) + 1 > 79:
            add(line)
            line = "  " + word
        else:
            if line == "  ":
                line += word
            else:
                line += " " + word
    if line.strip():
        add(line)
    add("")
    add("=" * 80)
    add("END OF REPORT")
    add("=" * 80)

    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"[OK] TXT report: {path}")


def write_json_report(s: dict, path: Path):
    """Write JSON with ASCII-safe repr for Hebrew strings."""

    def ascii_safe(obj):
        """Recursively replace Hebrew strings with their repr() form for JSON safety."""
        if isinstance(obj, str):
            # Try to encode as ASCII; if it fails, return repr
            try:
                obj.encode("ascii")
                return obj
            except UnicodeEncodeError:
                return repr(obj)
        elif isinstance(obj, dict):
            return {k: ascii_safe(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [ascii_safe(v) for v in obj]
        return obj

    safe = ascii_safe(s)
    path.write_text(json.dumps(safe, indent=2, ensure_ascii=True), encoding="utf-8")
    print(f"[OK] JSON report: {path}")


# ─────────────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Running ingredient reading diagnosis...")
    summary = run_analysis()

    write_txt_report(summary, OUT_TXT)
    write_json_report(summary, OUT_JSON)

    # Print quick summary to stdout
    t1 = summary["task1_bug_frequency"]
    t3 = summary["task3_pct_extraction_accuracy"]
    t4 = summary["task4_whole_refined_coverage"]
    hb = t1["harmful_bug"]

    print()
    print("=" * 60)
    print("QUICK SUMMARY")
    print("=" * 60)
    print(f"Products analyzed:              {summary['products_with_ingredient_text']}")
    print(f"Products hit by harmful bug:    {hb['products_affected']}")
    print(f"Items lost to bug:              {hb['items_affected']}")
    print(f"Pct-loss rate (Task 3):         {t3['pct_loss_rate']*100:.1f}%")
    print(f"Whole items lost (Task 4):      {t4['whole_items_lost_by_probe_bug']}")
    print(f"T1 first-ingredient lost:       {t4['t1_products_with_first_ingredient_lost']}")
    print(f"BSIP1 faulty:                   {summary['verdict']['bsip1_reading_failure']}")
    print(f"BSIP2 probe faulty:             {summary['verdict']['bsip2_probe_reading_failure']}")
    print("=" * 60)
    print()
    print("Done.")
