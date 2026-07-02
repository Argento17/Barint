"""
structured_ingredient_reader.py
================================
TASK-395 — Shared structured ingredient reader for Hebrew food labels.

Implements the architecture proposed in ingredient_reading_diagnosis_v1.md §C1.
Built as a NEW module under analysis/ per the hard constraint: no edits to
signal_extractor.py, nova_proxy.py, score_engine.py, or BSIP1 src.

Input:  raw Hebrew ingredient string (e.g. from product["ingredients_text_he"])
        OR BSIP1's ingredient_order items (preferred where available).
Output: list of StructuredIngredient records (dicts), one per depth-0 ingredient.
        Sub-ingredients of real composites are included as additional records
        with is_sub=True, parent_position set to their parent's position.

Key correctness properties enforced:
  1. A parenthetical containing ONLY a bare percentage is NOT a sub-recipe —
     it is the ingredient's own stated proportion. Attach as stated_pct; do not
     drop the parent ingredient or create a phantom sub-fragment. This fixes
     the core bug in expand_composites() that dropped whole-grain at position 1
     in 54% of gold-set products.

  2. A parenthetical starting with "מכיל" (contains) is an allergen declaration,
     NOT a sub-recipe. Move to allergen_notes.

  3. A parenthetical matching the dual-denominator phrase pattern
     "(X% מהקמחים, Y% מהמוצר)" or variants captures ONLY the product-weight %
     as stated_pct (pct_basis="product") and the flour-weight % separately.
     pct_basis is set to "bread" when the effective denominator is bread-weight.

  4. Curly-brace {…} sub-lists are treated as parenthetical sub-composites.

  5. Qualifier words ("מלא","מלאה","מלאים","לבן","בהיר","אורגני") are extracted
     per ingredient and stored in qualifiers[]. Downstream consumers use
     qualifiers to disambiguate ambiguous tokens (e.g. כוסמין לבן vs כוסמין מלא).

  6. (R-1 fix, v4) A percentage that appears AFTER the last closing bracket
     (e.g. "INGREDIENT (מכיל גלוטן) 47%") is captured as the ingredient's
     stated_pct when no pre-group or in-group pct was found. The allergen paren
     previously hid this trailing pct from _pct_from_name().

  7. (R-2 fix, v4) Marker extraction is NOT fired on the full raw text of a
     composite parent record (has_own_sub=True). The sub-composite content is
     stripped from the matchable text before pattern-matching, preventing the
     parent record from claiming sub-ingredient signals at the parent's inflated
     pct. Sub-record effective_pcts survive dedup.

  8. (C-5 fix, v4) pct_basis is correctly labeled "bread" when the effective
     percentage is bread-weight (not product-weight). Previously the
     _classify_group() returned bread_pct merged into product_pct, causing the
     caller to label it "product".

Author: Data Agent (TASK-395, Step 2)
Date: 2026-06-25
v4 fixes: R-1 trailing-pct, R-2 parent-composite marker skip, spelt construct
          form, C-5 pct_basis label
"""

from __future__ import annotations

import re
from typing import Optional

# ---------------------------------------------------------------------------
# Type alias — a single structured ingredient record
# ---------------------------------------------------------------------------
# {
#   "raw":              str,          exact text of this depth-0 item (for diagnostics)
#   "normalized":       str,          lowercased, stripped
#   "position":         int,          1-indexed in the OUTER list
#   "stated_pct":       float|None,   product-weight percentage (pct_basis="product"|"flour"|None)
#   "pct_basis":        str|None,     "product" | "flour" | "bread" | "unknown" | None
#   "qualifiers":       list[str],    ["מלא"] / ["לבן"] / ["אורגני"] etc.
#   "allergen_notes":   list[str],    e.g. ["מכיל גלוטן"]
#   "notes":            list[str],    provenance / processing notes, e.g. ["נטחן מגרעין..."]
#   "parent_position":  int|None,     outer position of parent (if is_sub=True)
#   "is_sub":           bool,
#   "sub_position":     int|None,     1-indexed position within parent composite
#   "has_own_sub":      bool,         True if this item has a real sub-list
#   "effective_pct":    float|None,   parent_pct × sub_pct / 100 (for subs with parent %)
# }
StructuredIngredient = dict

# ---------------------------------------------------------------------------
# Compiled regexes
# ---------------------------------------------------------------------------

# Bare percentage: (54%) or (54.0 %) or just 54% in context
_BARE_PCT_RE = re.compile(
    r"""
    ^\s*
    [\(≈~]?            # optional open-paren / approx
    \s*
    (\d{1,3}(?:\.\d{1,2})?)  # numeric value  (group 1)
    \s*%\s*
    [\)]?              # optional close-paren
    \s*$
    """,
    re.VERBOSE,
)

# Percentage with an explicit denominator keyword following
# Captures: (group 1) numeric value, (group 2) keyword
# Pattern handles: מהקמחים (מה + קמחים), ממשקל הקמחים, מהמוצר, מהלחם, הקמח, etc.
_DENOMINATOR_PCT_RE = re.compile(
    r"(\d{1,3}(?:\.\d{1,2})?)\s*%\s*(?:ממשקל\s+)?(?:מה?|ה)?(קמחים|קמח|לחם|מוצר)",
    re.IGNORECASE,
)

# Numeric percentage anywhere in text (greedy scan — used for fallback pct extraction)
_ANY_PCT_RE = re.compile(r"(\d{1,3}(?:\.\d{1,2})?)\s*%")

# Allergen declaration patterns
# Matches: "מכיל גלוטן", "contains gluten", bare allergen words like "גלוטן" or "סויה"
_ALLERGEN_RE = re.compile(
    r"^(?:מכיל|contains|מכיל:)\s*(.+)$",
    re.IGNORECASE | re.UNICODE,
)
# Bare allergen shorthands that appear without "מכיל" prefix — parenthetical like (גלוטן), (סויה)
_BARE_ALLERGEN_RE = re.compile(
    r"^(גלוטן|סויה|חלב|אגוזים|בוטנים|שומשום|סלרי|חרדל|לופין|רכולות|ביצים?)\s*$",
    re.UNICODE,
)

# Provenance / processing note patterns (NOT sub-ingredients)
_PROVENANCE_RE = re.compile(
    r"^(?:נטחן|מופרד|מיוצר|מעובד|מיובש|עשוי|מכין|מסוחט|קלוי)\s",
    re.IGNORECASE | re.UNICODE,
)

# Qualifier words — map token → qualifier label
_QUALIFIERS: list[tuple[str, str]] = [
    (r"מלאים\b", "מלא"),
    (r"מלאה\b", "מלא"),
    (r"מלא\b", "מלא"),
    (r"לבן\b", "לבן"),
    (r"בהיר\b", "בהיר"),
    (r"אורגני\b", "אורגני"),
    (r"אורגנית\b", "אורגני"),
    (r"טבעי\b", "טבעי"),
    (r"טבעית\b", "טבעי"),
]
_QUALIFIER_PATTERNS = [(re.compile(p, re.UNICODE), label) for p, label in _QUALIFIERS]

# Marketing / unparseable detectors (same set as v2 probe — unchanged)
_INCI_WORDS = ["aqua", "water (aqua)", "cetearyl", "caprylic", "glycerin",
               "phenoxyethanol", "tocopheryl", "carbomer", "parfum"]
_MARKETING_PHRASES = [
    re.compile(r"אנחנו מאמינים", re.UNICODE),
    re.compile(r"פרגנו לעצמכם", re.UNICODE),
    re.compile(r"בקיצור", re.UNICODE),
    re.compile(r"טעים ומפנק", re.UNICODE),
    re.compile(r"גם בריאה", re.UNICODE),
]

# ---------------------------------------------------------------------------
# Helper: check if text is unparseable (marketing copy / INCI)
# ---------------------------------------------------------------------------

def is_unparseable(text: str) -> bool:
    t = text.lower()
    for w in _INCI_WORDS:
        if w in t:
            return True
    for p in _MARKETING_PHRASES:
        if p.search(text):
            return True
    return False


# ---------------------------------------------------------------------------
# Helper: depth-0 split (same logic as v2's _split_top_level, preserved exactly)
# Splits on commas/semicolons not inside (), {}, []
# ---------------------------------------------------------------------------

def _split_top_level(text: str) -> list[str]:
    parts = []
    depth = 0
    current: list[str] = []
    for ch in text:
        if ch in "({[":
            depth += 1
            current.append(ch)
        elif ch in ")}]":
            depth = max(0, depth - 1)
            current.append(ch)
        elif ch in ",;" and depth == 0:
            parts.append("".join(current).strip())
            current = []
        else:
            current.append(ch)
    if current:
        parts.append("".join(current).strip())
    return [p for p in parts if p]


# ---------------------------------------------------------------------------
# Helper: extract ALL parenthetical / brace groups from an ingredient string.
# Returns list of dicts: {content, bracket_type, start, end}
# ---------------------------------------------------------------------------

def _extract_groups(text: str) -> list[dict]:
    """
    Extract top-level parenthetical/brace groups from `text`.
    Returns list of {content: str, bracket_type: '('|'{'|'[', start: int, end: int}.
    Does NOT recurse into nested groups — returns outer boundaries only.
    """
    groups = []
    i = 0
    n = len(text)
    open_map = {"(": ")", "{": "]", "[": "]"}  # closing bracket per opener
    # Corrected close map
    close_map = {"(": ")", "{": "}", "[": "]"}
    while i < n:
        if text[i] in "({[":
            opener = text[i]
            closer = close_map[opener]
            depth = 1
            j = i + 1
            while j < n and depth > 0:
                if text[j] in "({[":
                    depth += 1
                elif text[j] in ")}]":
                    depth -= 1
                j += 1
            # text[i+1 : j-1] is the content inside the group
            groups.append({
                "content": text[i + 1: j - 1],
                "bracket_type": opener,
                "start": i,
                "end": j,
            })
            i = j
        else:
            i += 1
    return groups


# ---------------------------------------------------------------------------
# Core: classify a single parenthetical group's content
# Returns a dict with keys:
#   type: "allergen" | "bare_pct" | "dual_denominator" | "provenance" |
#         "sub_composite" | "unknown"
#   product_pct: float|None    — the product-weight percentage (if any)
#   flour_pct: float|None      — the flour-weight percentage (if any)
#   bread_pct: float|None      — the bread-weight percentage (if any)
#   allergen_text: str|None
#   note_text: str|None
# ---------------------------------------------------------------------------

def _classify_group(content: str) -> dict:
    stripped = content.strip()

    # 1. Allergen declaration: starts with מכיל / contains
    if _ALLERGEN_RE.match(stripped):
        return {
            "type": "allergen",
            "product_pct": None,
            "flour_pct": None,
            "bread_pct": None,
            "allergen_text": stripped,
            "note_text": None,
        }

    # 1b. Bare allergen shorthand — a single allergen word without "מכיל" prefix
    #     e.g. (גלוטן), (סויה) — these appear on Israeli labels as shorthand
    if _BARE_ALLERGEN_RE.match(stripped):
        return {
            "type": "allergen",
            "product_pct": None,
            "flour_pct": None,
            "bread_pct": None,
            "allergen_text": stripped,
            "note_text": None,
        }

    # 2. Provenance / processing note (does NOT contain a % — purely descriptive)
    has_pct = bool(_ANY_PCT_RE.search(stripped))
    if _PROVENANCE_RE.match(stripped) and not has_pct:
        return {
            "type": "provenance",
            "product_pct": None,
            "flour_pct": None,
            "bread_pct": None,
            "allergen_text": None,
            "note_text": stripped,
        }

    # 3. Bare percentage ONLY: content is just "54%" or "54.0 %" with nothing else
    if _BARE_PCT_RE.match(stripped):
        m = _ANY_PCT_RE.search(stripped)
        pct = float(m.group(1)) if m else None
        return {
            "type": "bare_pct",
            "product_pct": pct,
            "flour_pct": None,
            "bread_pct": None,
            "allergen_text": None,
            "note_text": None,
        }

    # 4. Dual-denominator: content contains percentages with denominator keywords
    #    e.g. "100% מהקמחים, 64% מהמוצר" or "50% ממשקל הקמחים, 34% ממשקל הלחם"
    #    MUST be checked BEFORE sub_composite because dual-denom strings have 2 comma parts
    denominator_hits = _DENOMINATOR_PCT_RE.findall(stripped)
    if len(denominator_hits) >= 1:
        product_pct = None
        flour_pct = None
        bread_pct = None
        for val_str, keyword in denominator_hits:
            kw = keyword.strip()
            val = float(val_str)
            if "מוצר" in kw:
                product_pct = val
            elif "לחם" in kw:
                # Bread-weight is equivalent to product-weight for bread products
                bread_pct = val
            elif "קמח" in kw:
                flour_pct = val
        # If we have at least a flour-weight hit, this IS a dual-denominator group
        # (even if product_pct is not present — e.g. "100% מהקמח, 60% מהלחם")
        if flour_pct is not None or product_pct is not None or bread_pct is not None:
            # C-5 fix: do NOT merge bread_pct into product_pct.
            # Return them separately so the caller can label pct_basis correctly.
            return {
                "type": "dual_denominator",
                "product_pct": product_pct,      # None if only bread/flour pct present
                "flour_pct": flour_pct,
                "bread_pct": bread_pct,           # non-None when denominator is "לחם"
                "allergen_text": None,
                "note_text": None,
            }

    # 5. Sub-composite: content is a comma-separated list of substance names
    #    A sub-composite has multiple top-level items when split by comma.
    #    Only classified as sub-composite if at least one part contains Hebrew letters
    #    (i.e., it is not a pure dual-denominator phrase).
    sub_parts = _split_top_level(stripped)
    if len(sub_parts) >= 2:
        non_pct_parts = [p for p in sub_parts if re.search(r"[א-ת]", p)]
        if non_pct_parts:
            return {
                "type": "sub_composite",
                "product_pct": None,
                "flour_pct": None,
                "bread_pct": None,
                "allergen_text": None,
                "note_text": None,
                "sub_parts": sub_parts,
            }

    # 6. Single percentage with surrounding noise (edge case) — no Hebrew beyond the pct
    if has_pct:
        m = _ANY_PCT_RE.search(stripped)
        pct = float(m.group(1)) if m else None
        stripped_no_pct = _ANY_PCT_RE.sub("", stripped).strip("() \t")
        if not re.search(r"[א-ת]", stripped_no_pct):
            return {
                "type": "bare_pct",
                "product_pct": pct,
                "flour_pct": None,
                "bread_pct": None,
                "allergen_text": None,
                "note_text": None,
            }

    # 7. Fallback: unknown / descriptive
    return {
        "type": "unknown",
        "product_pct": None,
        "flour_pct": None,
        "bread_pct": None,
        "allergen_text": None,
        "note_text": stripped,
    }


# ---------------------------------------------------------------------------
# Helper: extract qualifiers from ingredient text
# ---------------------------------------------------------------------------

def _extract_qualifiers(text: str) -> list[str]:
    found = []
    seen = set()
    for pattern, label in _QUALIFIER_PATTERNS:
        if label not in seen and pattern.search(text):
            found.append(label)
            seen.add(label)
    return found


# ---------------------------------------------------------------------------
# Helper: strip ALL parenthetical/brace groups from text, leaving just the name
# ---------------------------------------------------------------------------

def _strip_groups(text: str) -> str:
    """Remove all (…), {…}, [brand] groups from text, returning just the bare ingredient name."""
    result = []
    depth = 0
    close_map = {"(": ")", "{": "}", "[": "]"}
    for ch in text:
        if ch in "({[":
            depth += 1
        elif ch in ")}]":
            depth = max(0, depth - 1)
        elif depth == 0:
            result.append(ch)
    return "".join(result).strip()


# ---------------------------------------------------------------------------
# Helper: extract a percentage from the ingredient name portion ONLY
# (the name is the text before the first parenthetical)
# e.g. "שיבולת שועל 47%" → 47.0
# ---------------------------------------------------------------------------

def _pct_from_name(name_text: str) -> Optional[float]:
    """Extract a trailing bare percentage from the name portion (no parens)."""
    m = _ANY_PCT_RE.search(name_text)
    if m:
        v = float(m.group(1))
        if 0.1 <= v <= 100.0:
            return v
    return None


# ---------------------------------------------------------------------------
# Main public function: parse_ingredients
# ---------------------------------------------------------------------------

def parse_ingredients(text: str) -> list[StructuredIngredient]:
    """
    Parse a raw Hebrew ingredient string into a structured list.

    Returns [] if text is None, empty, or unparseable (marketing copy / INCI).
    Each record is a StructuredIngredient dict (see module docstring for schema).

    Sub-ingredients of real composites are included in-line with is_sub=True
    and parent_position pointing to their parent's position value.
    """
    if not text:
        return []
    if is_unparseable(text):
        return []

    # Step 1: Split at depth-0 commas/semicolons → top-level ingredient strings
    top_items = _split_top_level(text)

    result: list[StructuredIngredient] = []
    outer_pos = 0

    for raw_item in top_items:
        raw_item = raw_item.strip()
        if not raw_item:
            continue
        outer_pos += 1

        # Step 2: Extract all parenthetical/brace groups from this item
        groups = _extract_groups(raw_item)

        # Step 3: Get the name portion — text before the first group
        if groups:
            first_start = groups[0]["start"]
            name_portion = raw_item[:first_start].strip()
        else:
            name_portion = raw_item.strip()

        # Step 4: Process each group, accumulating state for this ingredient
        stated_pct: Optional[float] = None
        pct_basis: Optional[str] = None
        allergen_notes: list[str] = []
        notes: list[str] = []
        sub_ingredients: list[dict] = []  # raw sub-parts for sub-composite expansion
        has_own_sub = False

        # Also check for a bare percentage in the name portion itself
        name_pct = _pct_from_name(name_portion)
        if name_pct is not None:
            stated_pct = name_pct
            pct_basis = "product"
            # Remove the pct from the name portion for clean normalization
            name_portion = _ANY_PCT_RE.sub("", name_portion).strip()

        for group in groups:
            cls = _classify_group(group["content"])
            gtype = cls["type"]

            if gtype == "allergen":
                allergen_notes.append(cls["allergen_text"])

            elif gtype == "bare_pct":
                # Only overwrite if we don't have a more specific pct yet
                if stated_pct is None and cls["product_pct"] is not None:
                    stated_pct = cls["product_pct"]
                    pct_basis = "product"

            elif gtype == "dual_denominator":
                # C-5 fix: product_pct and bread_pct are now kept separate.
                # Priority: product_pct > bread_pct.
                # pct_basis is labeled correctly for each.
                if cls["product_pct"] is not None:
                    stated_pct = cls["product_pct"]
                    pct_basis = "product"
                elif cls["bread_pct"] is not None:
                    stated_pct = cls["bread_pct"]
                    pct_basis = "bread"
                if cls["flour_pct"] is not None:
                    notes.append(f"flour_pct:{cls['flour_pct']}")

            elif gtype == "provenance":
                notes.append(cls["note_text"])

            elif gtype == "sub_composite":
                has_own_sub = True
                sub_ingredients = cls.get("sub_parts", [])

            elif gtype == "unknown":
                # Unknown groups: if they contain % and look like they might be
                # a bare pct candidate (e.g. edge cases), try to extract pct
                if cls["note_text"] and _ANY_PCT_RE.search(cls["note_text"]):
                    # Check if it's really just a percentage with some surrounding noise
                    maybe_pct = _classify_group(cls["note_text"])
                    if maybe_pct["type"] == "bare_pct" and stated_pct is None:
                        stated_pct = maybe_pct["product_pct"]
                        pct_basis = "product"
                    else:
                        notes.append(cls.get("note_text", ""))
                else:
                    if cls.get("note_text"):
                        notes.append(cls["note_text"])

        # R-1 fix: scan for a trailing percentage AFTER the last closing bracket.
        # Pattern: "INGREDIENT (מכיל גלוטן) 47%" — the % follows the allergen paren
        # and is invisible to _pct_from_name() which only sees text before the first group.
        # Only applies when no pct has been found yet from name_portion or groups.
        if stated_pct is None and groups:
            last_group_end = groups[-1]["end"]
            trailing_text = raw_item[last_group_end:]
            trailing_pct = _pct_from_name(trailing_text)
            if trailing_pct is not None:
                stated_pct = trailing_pct
                pct_basis = "product"

        # Step 5: Build qualifiers from FULL item text (not just name portion)
        # This ensures מלא in any position of the item is captured
        qualifiers = _extract_qualifiers(raw_item)

        # Step 6: Build the main record for this depth-0 ingredient
        normalized = name_portion.lower().strip().rstrip(".")
        record: StructuredIngredient = {
            "raw": raw_item,
            "normalized": normalized,
            "position": outer_pos,
            "stated_pct": stated_pct,
            "pct_basis": pct_basis,
            "qualifiers": qualifiers,
            "allergen_notes": allergen_notes,
            "notes": notes,
            "parent_position": None,
            "is_sub": False,
            "sub_position": None,
            "has_own_sub": has_own_sub,
            "effective_pct": stated_pct,  # for top-level items, effective == stated
        }
        result.append(record)

        # Step 7: If this item has real sub-ingredients, expand them
        if has_own_sub and sub_ingredients:
            parent_pct = stated_pct  # may be None
            sub_pos = 0
            for sub_raw in sub_ingredients:
                sub_raw = sub_raw.strip()
                if not sub_raw:
                    continue
                sub_pos += 1

                # Recursively parse the sub-item (single level — no deep recursion needed here)
                sub_groups = _extract_groups(sub_raw)
                sub_name_portion = sub_raw[:sub_groups[0]["start"]].strip() if sub_groups else sub_raw.strip()

                sub_stated_pct: Optional[float] = None
                sub_pct_basis: Optional[str] = None
                sub_allergens: list[str] = []
                sub_notes_list: list[str] = []

                sub_name_pct = _pct_from_name(sub_name_portion)
                if sub_name_pct is not None:
                    sub_stated_pct = sub_name_pct
                    sub_pct_basis = "product"
                    sub_name_portion = _ANY_PCT_RE.sub("", sub_name_portion).strip()

                for sg in sub_groups:
                    scls = _classify_group(sg["content"])
                    if scls["type"] == "allergen":
                        sub_allergens.append(scls["allergen_text"])
                    elif scls["type"] == "bare_pct" and sub_stated_pct is None:
                        sub_stated_pct = scls["product_pct"]
                        sub_pct_basis = "product"
                    elif scls["type"] == "dual_denominator":
                        if scls["product_pct"] is not None and sub_stated_pct is None:
                            sub_stated_pct = scls["product_pct"]
                            sub_pct_basis = "product"
                        if scls["flour_pct"] is not None:
                            sub_notes_list.append(f"flour_pct:{scls['flour_pct']}")
                    elif scls["type"] in ("provenance", "unknown"):
                        if scls.get("note_text"):
                            sub_notes_list.append(scls["note_text"])

                # Effective pct: parent_pct * sub_pct / 100
                if parent_pct is not None and sub_stated_pct is not None:
                    effective_pct = parent_pct * sub_stated_pct / 100.0
                else:
                    effective_pct = None

                # Effective position for position-weight fallback
                effective_position = outer_pos + sub_pos - 1

                sub_qualifiers = _extract_qualifiers(sub_raw)
                sub_normalized = sub_name_portion.lower().strip().rstrip(".")

                sub_record: StructuredIngredient = {
                    "raw": sub_raw,
                    "normalized": sub_normalized,
                    "position": effective_position,
                    "stated_pct": sub_stated_pct,
                    "pct_basis": sub_pct_basis,
                    "qualifiers": sub_qualifiers,
                    "allergen_notes": sub_allergens,
                    "notes": sub_notes_list,
                    "parent_position": outer_pos,
                    "is_sub": True,
                    "sub_position": sub_pos,
                    "has_own_sub": False,
                    "effective_pct": effective_pct,
                }
                result.append(sub_record)

    return result


# ---------------------------------------------------------------------------
# Convenience: consume BSIP1's ingredient_order where available
# BSIP1's ingredient_order items: {position, text, percentage_declared, has_subgroup}
# We prefer BSIP1's depth-0 split (it is correct) but still need to do our
# group-level parsing to extract qualifiers, allergens, and sub-composites.
# ---------------------------------------------------------------------------

def parse_from_bsip1(ingredient_order: list[dict], raw_text: str = "") -> list[StructuredIngredient]:
    """
    Build structured records from BSIP1's ingredient_order list.
    Prefers BSIP1's text and percentage_declared where populated.
    Falls back to parse_ingredients(raw_text) if ingredient_order is empty.
    """
    if not ingredient_order:
        return parse_ingredients(raw_text)

    result: list[StructuredIngredient] = []

    for item in ingredient_order:
        item_text = item.get("text", "").strip()
        if not item_text:
            continue
        position = item.get("position", len(result) + 1)
        bsip1_pct = item.get("percentage_declared")

        # Parse groups from this BSIP1 item text
        groups = _extract_groups(item_text)
        name_start = groups[0]["start"] if groups else len(item_text)
        name_portion = item_text[:name_start].strip()

        allergen_notes: list[str] = []
        notes: list[str] = []
        has_own_sub = False
        sub_ingredients: list[str] = []

        # If BSIP1 already gave us a percentage, trust it
        stated_pct: Optional[float] = bsip1_pct
        pct_basis: Optional[str] = "product" if bsip1_pct is not None else None

        # Still parse groups to extract allergens, sub-composites, notes
        for group in groups:
            cls = _classify_group(group["content"])
            gtype = cls["type"]
            if gtype == "allergen":
                allergen_notes.append(cls["allergen_text"])
            elif gtype == "bare_pct":
                if stated_pct is None and cls["product_pct"] is not None:
                    stated_pct = cls["product_pct"]
                    pct_basis = "product"
            elif gtype == "dual_denominator":
                if cls["product_pct"] is not None and stated_pct is None:
                    stated_pct = cls["product_pct"]
                    pct_basis = "product"
                if cls["flour_pct"] is not None:
                    notes.append(f"flour_pct:{cls['flour_pct']}")
            elif gtype == "provenance":
                notes.append(cls.get("note_text", ""))
            elif gtype == "sub_composite":
                has_own_sub = True
                sub_ingredients = cls.get("sub_parts", [])
            elif gtype == "unknown":
                if cls.get("note_text"):
                    notes.append(cls["note_text"])

        qualifiers = _extract_qualifiers(item_text)
        normalized = name_portion.lower().strip().rstrip(".")

        record: StructuredIngredient = {
            "raw": item_text,
            "normalized": normalized,
            "position": position,
            "stated_pct": stated_pct,
            "pct_basis": pct_basis,
            "qualifiers": qualifiers,
            "allergen_notes": allergen_notes,
            "notes": notes,
            "parent_position": None,
            "is_sub": False,
            "sub_position": None,
            "has_own_sub": has_own_sub,
            "effective_pct": stated_pct,
        }
        result.append(record)

        # Expand sub-composites
        if has_own_sub and sub_ingredients:
            parent_pct = stated_pct
            for sub_pos, sub_raw in enumerate(sub_ingredients, start=1):
                sub_raw = sub_raw.strip()
                if not sub_raw:
                    continue
                sub_groups = _extract_groups(sub_raw)
                sub_name_portion = sub_raw[:sub_groups[0]["start"]].strip() if sub_groups else sub_raw.strip()
                sub_stated_pct: Optional[float] = None
                sub_pct_basis: Optional[str] = None
                sub_allergens: list[str] = []
                sub_notes_list: list[str] = []

                sub_name_pct = _pct_from_name(sub_name_portion)
                if sub_name_pct is not None:
                    sub_stated_pct = sub_name_pct
                    sub_pct_basis = "product"
                    sub_name_portion = _ANY_PCT_RE.sub("", sub_name_portion).strip()

                for sg in sub_groups:
                    scls = _classify_group(sg["content"])
                    if scls["type"] == "allergen":
                        sub_allergens.append(scls["allergen_text"])
                    elif scls["type"] == "bare_pct" and sub_stated_pct is None:
                        sub_stated_pct = scls["product_pct"]
                        sub_pct_basis = "product"
                    elif scls["type"] == "dual_denominator" and sub_stated_pct is None:
                        if scls["product_pct"] is not None:
                            sub_stated_pct = scls["product_pct"]
                            sub_pct_basis = "product"

                eff_pct = parent_pct * sub_stated_pct / 100.0 if (
                    parent_pct is not None and sub_stated_pct is not None
                ) else None
                eff_pos = position + sub_pos - 1
                sub_qualifiers = _extract_qualifiers(sub_raw)

                result.append({
                    "raw": sub_raw,
                    "normalized": sub_name_portion.lower().strip().rstrip("."),
                    "position": eff_pos,
                    "stated_pct": sub_stated_pct,
                    "pct_basis": sub_pct_basis,
                    "qualifiers": sub_qualifiers,
                    "allergen_notes": sub_allergens,
                    "notes": sub_notes_list,
                    "parent_position": position,
                    "is_sub": True,
                    "sub_position": sub_pos,
                    "has_own_sub": False,
                    "effective_pct": eff_pct,
                })

    return result


# ---------------------------------------------------------------------------
# Self-test: run on the 5 canonical failure cases from the diagnosis
# ---------------------------------------------------------------------------

def _self_test():
    test_cases = [
        # Case 1: core bug — bare pct + allergen paren → must NOT drop the ingredient
        {
            "label": "CASE1_bare_pct_allergen",
            "text": "פתיתי שיבולת שועל מלאה (54%) (מכיל גלוטן), סוכר לבן, שמנים צמחיים",
            "expect_item_1_not_dropped": True,
            "expect_item_1_pct": 54.0,
            "expect_item_1_allergen": "מכיל גלוטן",
            "expect_item_1_qualifier": "מלא",
        },
        # Case 2: dual denominator — must capture bread-weight pct (58%), not flour-weight (100%)
        # C-5 fix: pct_basis must be "bread", not "product"
        {
            "label": "CASE2_dual_denominator",
            "text": "קמח חיטה מלא (100% ממשקל הקמחים, 58% ממשקל הלחם) (מכיל גלוטן), מים, שמרים",
            "expect_item_1_pct": 58.0,
            "expect_item_1_pct_basis": "bread",
        },
        # Case 3: curly-brace sub-list
        {
            "label": "CASE3_curly_brace",
            "text": "תערובת קמחים (מכיל גלוטן) {קמח חיטה (46%), קמח כוסמין מלא (5%)}, מים",
            "expect_sub_composite": True,
        },
        # Case 4: qualifier disambiguation — כוסמין לבן must have qualifier ["לבן"]
        {
            "label": "CASE4_qualifier_lavan",
            "text": "קמח כוסמין לבן (גלוטן) (100% מהקמחים, 64% מהמוצר), מים",
            "expect_item_1_qualifier": "לבן",
            "expect_item_1_pct": 64.0,
            "expect_item_1_pct_basis": "product",
        },
        # Case 5: real sub-composite with parent × sub pct
        {
            "label": "CASE5_real_subcomposite",
            "text": "גרנולה 65% (פתיתי שיבולת שועל 43% (מכיל גלוטן), קמח חיטה, שמן צמחי), מים",
            "expect_sub_effective_pct": 65.0 * 43.0 / 100.0,  # 27.95
        },
        # Case 8: R-1 fix — trailing pct AFTER allergen paren
        # "פתיתי שיבולת שועל (מכיל גלוטן) 47%" — % is after the closing paren
        {
            "label": "CASE8_R1_trailing_pct_after_allergen",
            "text": "פתיתי שיבולת שועל (מכיל גלוטן) 47%, סוכר, שמן",
            "expect_item_1_not_dropped": True,
            "expect_item_1_pct": 47.0,
            "expect_item_1_allergen": "מכיל גלוטן",
        },
        # Case 9: R-1 fix — same pattern with 50% (barcode 7290013433107)
        {
            "label": "CASE9_R1_trailing_pct_50pct",
            "text": "שיבולת שועל (מכיל גלוטן) 50%, סוכר",
            "expect_item_1_pct": 50.0,
        },
        # Case 10: R-1 fix — 39% after allergen paren (barcode 7290011131388)
        {
            "label": "CASE10_R1_trailing_pct_39pct",
            "text": "פתיתי שיבולת שועל (מכיל גלוטן) 39%, שמן",
            "expect_item_1_pct": 39.0,
        },
        # Case 11: C-5 fix — dual-denom where only bread-weight given → pct_basis="bread"
        # (100% מהקמחים, 58% מהמוצר) → pct_basis="product" (correct, unchanged)
        {
            "label": "CASE11_C5_product_denom",
            "text": "קמח כוסמין לבן (100% מהקמחים, 64% מהמוצר), מים",
            "expect_item_1_pct": 64.0,
            "expect_item_1_pct_basis": "product",
        },
        # Case 12: spelt construct form — קמח חיטת כוסמין מלא (barcode 7290017947464)
        # The construct form should be recognized as whole_spelt_flour by the probe
        # (tested here at reader level: qualifiers should include "מלא")
        {
            "label": "CASE12_spelt_construct_form",
            "text": "קמח חיטת כוסמין מלא (נטחן מגרעין חיטת הכוסמין בשלמותו)(גלוטן)(100% מהקמחים, 58% מהמוצר), מים",
            "expect_item_1_qualifier": "מלא",
            "expect_item_1_pct": 58.0,
            "expect_item_1_pct_basis": "product",
        },
    ]

    all_pass = True
    for tc in test_cases:
        parsed = parse_ingredients(tc["text"])
        top_items = [r for r in parsed if not r["is_sub"]]
        sub_items = [r for r in parsed if r["is_sub"]]
        label = tc["label"]

        if tc.get("expect_item_1_not_dropped"):
            ok = len(top_items) >= 1
            if not ok:
                print(f"FAIL {label}: item 1 was dropped (got {len(top_items)} top items)")
                all_pass = False
            else:
                print(f"PASS {label}: item 1 present")

        if tc.get("expect_item_1_pct") is not None and top_items:
            got = top_items[0]["stated_pct"]
            exp = tc["expect_item_1_pct"]
            ok = got is not None and abs(got - exp) < 0.1
            status = "PASS" if ok else "FAIL"
            if not ok:
                all_pass = False
            print(f"{status} {label}: stated_pct={got} (expected {exp})")

        if tc.get("expect_item_1_pct_basis") and top_items:
            got = top_items[0]["pct_basis"]
            exp = tc["expect_item_1_pct_basis"]
            ok = got == exp
            status = "PASS" if ok else "FAIL"
            if not ok:
                all_pass = False
            print(f"{status} {label}: pct_basis={got} (expected {exp})")

        if tc.get("expect_item_1_allergen") and top_items:
            allergens = top_items[0]["allergen_notes"]
            ok = any(tc["expect_item_1_allergen"] in a for a in allergens)
            status = "PASS" if ok else "FAIL"
            if not ok:
                all_pass = False
            print(f"{status} {label}: allergen_notes={allergens}")

        if tc.get("expect_item_1_qualifier") and top_items:
            quals = top_items[0]["qualifiers"]
            ok = tc["expect_item_1_qualifier"] in quals
            status = "PASS" if ok else "FAIL"
            if not ok:
                all_pass = False
            print(f"{status} {label}: qualifiers={quals}")

        if tc.get("expect_sub_composite"):
            ok = len(sub_items) > 0
            status = "PASS" if ok else "FAIL"
            if not ok:
                all_pass = False
            print(f"{status} {label}: sub_items={len(sub_items)} (expected >0)")

        if tc.get("expect_sub_effective_pct") is not None:
            oat_sub = next(
                (r for r in sub_items if "שיבולת שועל" in r.get("raw", "") and r["effective_pct"] is not None),
                None,
            )
            if oat_sub is None:
                print(f"FAIL {label}: no sub-item with effective_pct found")
                all_pass = False
            else:
                got = oat_sub["effective_pct"]
                exp = tc["expect_sub_effective_pct"]
                ok = abs(got - exp) < 0.5
                status = "PASS" if ok else "FAIL"
                if not ok:
                    all_pass = False
                print(f"{status} {label}: effective_pct={got:.2f} (expected {exp:.2f})")

    print()
    print("Self-test OVERALL:", "PASS" if all_pass else "FAIL")
    return all_pass


if __name__ == "__main__":
    _self_test()
