"""
Shared BSIP0 nutrition-panel parser for Shufersal product pages.

Created for TASK-142A to fix the NUTR_LABEL_MAP overwrite defect (EV-026 family).

ROOT CAUSE (the bug this module replaces)
-----------------------------------------
The legacy per-scraper ``NUTR_LABEL_MAP`` mapped BOTH ``"שומנים"`` (total fat) and
``"שומן"`` (a substring of every fat sub-row label — ``"שומן טראנס"``,
``"חומצות שומן רוויות"``) to the single field ``fat``, and matched with
break-on-first-substring while iterating the dict.

A Shufersal nutrition panel lists the TOTAL fat row first, then indented
"of which" sub-rows (``מתוכו חומצות שומן רוויות`` / ``שומן טראנס``). Every sub-row
label contains the substring ``"שומן"``, which re-matched the generic ``"שומן"→fat``
rule and **overwrote** the already-stored total fat. The last fat-bearing row (trans,
typically ``"פחות מ 0.5"``) therefore won → ``fat`` collapsed to ``0.5`` on every
product that declared a trans/saturated sub-row. Saturated fat was *never* captured,
because the generic ``"שומן"→fat`` entry preceded the specific ``"שומן רווי"→
saturated_fat`` entry in iteration order and the loop broke on first match.

THE FIX
-------
``classify_nutr_label`` classifies each row explicitly, **most-specific-first**
(trans → saturated → … → generic fat LAST), and never lets an "of which" sub-row
overwrite a total macro. ``parse_nutrition_list`` keeps the first value per field
(totals appear before their sub-rows), so total fat is read from the genuine total
row and saturated/trans land in their own fields.

This module is the single source of truth for the Shufersal ``div.nutritionList``
parse. All Shufersal BSIP0 scrapers import it so the fix cannot drift back into one
scraper while another stays broken (which is exactly how TASK-039 missed this:
the defect was audited in hummus but never fixed at the shared path).
"""
from __future__ import annotations

import re

# Hebrew final-form letters → regular forms. Critical: ``"שומן"`` (final ן) is NOT a
# substring of ``"שומנים"`` (regular נ), and likewise ``"חלבון"`` vs ``"חלבונים"``.
# We normalise both the label and our match tokens so stem matching is form-agnostic.
_FINALS = str.maketrans({"ך": "כ", "ם": "מ", "ן": "נ", "ף": "פ", "ץ": "צ"})


def _norm(s: str) -> str:
    return (s or "").translate(_FINALS)


# "of which" markers (normalised) — a row carrying these is a sub-component, never a total.
# TASK-192 / EV-046: the original list covered מתוכו (final-vav) and מתוכנ (final-nun → מתוכנ)
# but MISSED מתוכמ (final-mem → מתוכמ), the plural-masculine "of which" form Shufersal uses
# for FAT sub-rows ("מתוכם חומצות שומן רוויות / שומן טראנס") and SUGAR sub-rows
# ("מתוכם סוכרים"). A generic "of-which fat" sub-row ("מתוכם שומן ...") that lacks a
# רווי/טראנס token therefore fell through to the generic "שומן→fat" rule and OVERWROTE total
# fat with the sub-row value ("פחות מ 0.5") — the 3rd recurrence of the EV-029 mis-capture
# (run_cereals_005). Now covers every final-form of the stem so no "of which" sub-row can
# ever populate a parent total field. Stems are final-form-normalised (see _norm).
_SUBROW_MARKERS = (
    "מתוכמ", "מתוכנ", "מתוכו",   # מתוכם / מתוכן / מתוכו — all "of which" forms
    "מתוכ",                       # bare stem (defensive: any other "of which …" inflection)
    "מהמ", "מהנ", "שמהמ", "שמהנ",  # "מהם" / "שמהם" colloquial variants
)


def classify_nutr_label(label: str) -> str | None:
    """Map a Hebrew nutrition-row label to a canonical field, most-specific-first.

    Returns ``None`` for rows we deliberately ignore (mono/poly-unsaturated fat,
    or an "of which … fat" sub-row that must not overwrite total fat). Match tokens
    below are written in final-form-normalised Hebrew (see ``_norm``).
    """
    l = _norm((label or "").strip())
    low = l.lower()
    is_subrow = any(m in l for m in _SUBROW_MARKERS)

    # --- fat family: specific sub-types BEFORE generic total fat ---
    if "טראנס" in l or "trans" in low:
        return "trans_fat"
    if "בלתי רווי" in l or "unsaturat" in low:        # mono/poly-unsaturated: ignore
        return None
    if "רווי" in l or "saturat" in low:               # רווי / רוויה / רוויות
        return "saturated_fat"
    # --- sugars before carbs (sugar is itself an "of which" of carbs) ---
    if "סוכר" in l or "sugar" in low:
        return "sugar"
    if "פחמימ" in l or "carb" in low:
        return "carbs"
    if "סיב" in l or "fib" in low:                    # סיבים תזונתיים
        return "fiber"
    if "חלבונ" in l or "protein" in low:              # חלבון / חלבונים
        return "protein"
    if "נתרנ" in l or "sodium" in low:                # נתרן — sodium only, never "מלח"/salt (2.5x)
        return "sodium"
    if ("אנרגיה" in l or "קלורי" in l or "קל\"" in l or "קל'" in l
            or "kcal" in low or "energy" in low):
        return "energy"
    # --- generic fat LAST, and never from an "of which" sub-row ---
    if "שומנ" in l or "fat" in low:                   # שומן / שומנים
        return None if is_subrow else "fat"
    return None


# ── Multi-table basis selection (TASK-239) ─────────────────────────────────────
#
# THE DUAL-TABLE BUG (frozen vegetables, fixed here structurally)
# ---------------------------------------------------------------
# A Shufersal product page can carry MORE THAN ONE ``div.nutritionList``. Frozen
# Dorot-style products (e.g. ``ג'ינג'ר קצוץ מוקפא`` / chopped frozen ginger,
# product P_7290018989456) declare TWO panels:
#     Table 0 — basis "100 גרם"  (per 100 g):  energy 77 kcal, sodium 12 mg
#     Table 1 — basis "קוביה"    (per cube):   energy  6 kcal, sodium  1 mg
# The legacy inline scrapers either (a) read only ``soup.find("div","nutritionList")``
# = the FIRST table with no per-100g check, or (b) iterated ``soup.find_all`` across
# the whole page into a label-keyed dict, so the LAST (per-cube) table OVERWROTE the
# per-100g values. Both produced 6 kcal / 1 mg — a 13× understatement — which then
# had to be MANUALLY JSON-PATCHED back to 77/12 (scope_clean_v2_1.json). Manual
# patching is not a fix: the parser path recreates the bug on the next run.
#
# THE FIX: every panel basis is read from the table's own ``div.subInfo`` header
# ("100 גרם" / "קוביה" / "מנה"). ``select_nutrition_table`` EXPLICITLY prefers the
# per-100g table. When >1 table exists and NO per-100g table can be identified, the
# selection is marked ``insufficient`` (basis="unknown") so the BSIP0 gate fails the
# product loudly — the parser NEVER silently selects the first table.

# subInfo tokens (final-form-normalised) that mark a panel as PER 100 G.
_PER_100G_MARKERS = ("ל-100 גרמ", "ל 100 גרמ", "100 גרמ", "per 100g",
                     "per 100 g", "100g", "100 g", "ל100 גרמ")
# subInfo tokens that mark a panel as PER SERVING / per discrete unit (not 100 g).
_PER_SERVING_MARKERS = ("קוביה", "קוביות", "מנה", "מנת", "יחידה", "יחידת",
                        "פרוסה", "כוס", "כף", "כפית", "serving", "portion",
                        "piece", "cube", "slice", "unit")


def classify_basis(subinfo: str) -> str:
    """Classify a panel basis label → ``"per_100g"`` | ``"per_serving"`` | ``"unknown"``.

    ``subinfo`` is the text of the table's ``div.subInfo`` header ("100 גרם",
    "קוביה", "מנה" …). per-100g is checked first because "100 גרם" is the
    unambiguous canonical basis the whole pipeline scores on.
    """
    s = _norm((subinfo or "").strip())
    low = s.lower()
    if any(m in s or m in low for m in _PER_100G_MARKERS):
        return "per_100g"
    if any(m in s or m in low for m in _PER_SERVING_MARKERS):
        return "per_serving"
    return "unknown"


def _table_subinfo(nutr_div) -> str:
    """Read the basis header (``div.subInfo``) for a single ``div.nutritionList``.

    The Shufersal structure nests the panel inside an ``<li>`` that also carries a
    ``div.nutritionListTitle`` with a ``div.subInfo`` ("100 גרם" / "קוביה"). We look
    up to the enclosing ``<li>`` (then any ancestor) for the nearest ``div.subInfo``.
    Returns "" when no basis header is present (single legacy panels sometimes omit it).
    """
    container = nutr_div.find_parent("li") or nutr_div.parent
    for _ in range(4):
        if container is None:
            break
        sub = container.find("div", class_="subInfo")
        if sub:
            return sub.get_text(strip=True)
        container = container.parent
    return ""


def _rows_from_div(nutr_div) -> list[dict[str, str]]:
    """Extract ``(value, unit, label)`` rows from ONE ``div.nutritionList``."""
    rows: list[dict[str, str]] = []
    for item in nutr_div.find_all("div", class_="nutritionItem"):
        # Use named div classes where available to avoid position-dependence.
        # CRITICAL (TASK-239): the LABEL is ``div.text`` (nutrient name, e.g. "נתרן"),
        # NOT ``div.name`` (which is the UNIT, e.g. "מג"). The legacy inline scrapers
        # used ``item.find(class_="name")`` first as the label and keyed the dict on
        # the unit ("גרם"/"מג") — collapsing every gram-unit row onto one key.
        num_div   = item.find("div", class_="number")
        name_div  = item.find("div", class_="name")
        text_div  = item.find("div", class_="text")
        if num_div and text_div:
            value = num_div.get_text(strip=True)
            unit  = name_div.get_text(strip=True) if name_div else ""
            label = text_div.get_text(strip=True)
            if value and label:
                rows.append({"value": value, "unit": unit, "label": label})
            continue
        # Fallback: positional extraction for pages without class names (defensive)
        divs = item.find_all("div")
        parts = [d.get_text(strip=True) for d in divs if d.get_text(strip=True)]
        if len(parts) < 2:
            continue
        rows.append({"value": parts[0], "unit": parts[1] if len(parts) >= 3 else "", "label": parts[-1]})
    return rows


def extract_nutrition_tables(soup) -> list[dict]:
    """Extract EVERY ``div.nutritionList`` on the page as a separate basis-tagged table.

    Returns a list of ``{"table_index", "basis", "subInfo", "rows"}`` in document
    order. This is the multi-table-aware layer that ``select_nutrition_table`` reads.
    """
    tables: list[dict] = []
    for idx, nutr_div in enumerate(soup.find_all("div", class_="nutritionList")):
        subinfo = _table_subinfo(nutr_div)
        tables.append({
            "table_index": idx,
            "basis": classify_basis(subinfo),
            "subInfo": subinfo,
            "rows": _rows_from_div(nutr_div),
        })
    return tables


def select_nutrition_table(tables: list[dict]) -> dict:
    """Choose the per-100g panel from a list of basis-tagged tables.

    Selection policy (TASK-239) — NEVER silently pick the first table:
      * 0 tables                         → ``selected_basis="none"``, rows=[]
      * exactly 1 table                  → select it; basis = its own classified basis
                                           (a lone panel is the product's panel even if
                                           its header is missing/unknown)
      * >1 table, >=1 is per_100g        → select the (first) per_100g table
      * >1 table, NONE is per_100g       → ``selected_basis="unknown"``,
                                           ``insufficient=True`` (gate must FAIL — we
                                           refuse to guess which non-100g table to use)

    Returns a dict::

        {
          "rows": [...],                 # rows of the selected table ([] if insufficient)
          "selected_basis": "per_100g"|"per_serving"|"unknown"|"none",
          "selected_table_index": int|None,
          "selected_table_header": str,  # the subInfo text of the selected table
          "competing_table_count": int,  # total nutritionList tables on the page
          "insufficient": bool,          # True -> BSIP0 gate fail (no per-100g identifiable)
        }
    """
    n = len(tables)
    if n == 0:
        return {"rows": [], "selected_basis": "none", "selected_table_index": None,
                "selected_table_header": "", "competing_table_count": 0,
                "insufficient": False}

    if n == 1:
        t = tables[0]
        return {"rows": t["rows"], "selected_basis": t["basis"],
                "selected_table_index": t["table_index"],
                "selected_table_header": t["subInfo"],
                "competing_table_count": 1, "insufficient": False}

    # Multiple tables: explicitly prefer per_100g.
    per_100g = [t for t in tables if t["basis"] == "per_100g"]
    if per_100g:
        t = per_100g[0]
        return {"rows": t["rows"], "selected_basis": "per_100g",
                "selected_table_index": t["table_index"],
                "selected_table_header": t["subInfo"],
                "competing_table_count": n, "insufficient": False}

    # >1 table and no identifiable per-100g panel -> refuse to guess.
    return {"rows": [], "selected_basis": "unknown", "selected_table_index": None,
            "selected_table_header": "; ".join(t["subInfo"] for t in tables),
            "competing_table_count": n, "insufficient": True}


def extract_nutrition_rows(soup) -> list[dict[str, str]]:
    """Extract the raw ``(value, unit, label)`` rows from the PER-100G ``div.nutritionList``.

    TASK-239: now multi-table-aware. Selects the per-100g table via
    ``select_nutrition_table`` so a per-cube/per-serving panel can never overwrite or
    masquerade as the per-100g panel. For a single-table page this is identical to the
    legacy behaviour. When a multi-table page has no identifiable per-100g panel, returns
    ``[]`` (the gate, reading ``extract_nutrition_selection``, fails the product).

    The Shufersal nutritionItem structure has three child divs:
      - ``div.number`` → the numeric value (e.g. "7", "פחות מ 0.5", "414")
      - ``div.name``   → the unit label (e.g. "גרם" = g, "מג" = mg, "קל" = kcal)
      - ``div.text``   → the nutrient name (e.g. "נתרן", "שומנים")

    The ``unit`` field is used by ``parse_sodium_mg`` to distinguish a value already
    in mg (unit="מג") from a gram value that must be converted (unit="גרם" or absent).
    """
    return select_nutrition_table(extract_nutrition_tables(soup))["rows"]


def extract_nutrition_selection(soup) -> dict:
    """Full multi-table selection result for a page (rows + basis metadata).

    Thin wrapper exposing ``select_nutrition_table(extract_nutrition_tables(soup))``.
    Scrapers persist the metadata (``selected_basis``, ``selected_table_index``,
    ``selected_table_header``, ``competing_table_count``, ``insufficient``) in the BSIP0
    record so the gate and any offline replay see the same basis decision the live
    scrape made.
    """
    return select_nutrition_table(extract_nutrition_tables(soup))


def parse_nutrition_rows(rows: list[dict[str, str]]) -> dict[str, str]:
    """Classify pre-extracted ``(value, unit, label)`` rows → ``{field: raw_value_string}``.

    The classification half of the parse, split out so it can run on rows read live
    from a page OR on rows replayed from a persisted ``nutrition_raw_source.rows``
    block. Total fat is read from the genuine total row; saturated/trans land in
    their own fields and never overwrite total fat. First value per field wins —
    totals appear before their sub-rows, so this is correct by construction and also
    defends against any duplicate rows.

    Unit propagation for sodium: Shufersal uses ``div.name`` to carry the physical
    unit of each row (``גרם`` / ``מג`` / ``קל``). For sodium, the unit is ``מג``
    (milligrams) when the declared value is small (e.g. 7 mg). The
    ``parse_sodium_mg`` downstream heuristic would otherwise over-multiply any
    value ≤ 10 by ×1000 (treating it as grams). To pass the unit information
    through the raw string dict without breaking the existing interface, we append
    the unit token to the stored sodium value when the unit is ``מג`` so the
    heuristic's ``"mg" in str(raw).lower()`` branch fires correctly.
    """
    # Unit tokens that, when present in div.name, unambiguously signal milligrams.
    _MG_UNITS = {"מג", 'מ"ג', "מֳג", "mg", "milligram"}

    nutr: dict[str, str] = {}
    for row in rows or []:
        field = classify_nutr_label(row.get("label", ""))
        if field and field not in nutr:
            value = row.get("value", "")
            unit = (row.get("unit") or "").strip()
            # For sodium: append the unit when it is explicitly "מג" / "mg" so the
            # downstream heuristic (value > 10 = already in mg) is bypassed correctly.
            # All other fields use gram units and are unaffected.
            if field == "sodium" and unit in _MG_UNITS:
                value = f"{value} מג" if value else value
            nutr[field] = value
    return nutr


def parse_nutrition_list(soup) -> dict[str, str]:
    """Parse ``div.nutritionList`` → ``{field: raw_value_string}``.

    Isolated from ingredients (reads only inside the nutrition div). Thin wrapper
    over ``extract_nutrition_rows`` + ``parse_nutrition_rows`` — identical behaviour,
    one extraction path shared with the raw-source capture.
    """
    return parse_nutrition_rows(extract_nutrition_rows(soup))


def extract_nutrition_raw(soup) -> dict:
    """Capture the raw nutrition source for offline replay of future parser fixes.

    TASK-239: now records EVERY table (with its basis) plus the basis-selection
    decision, so an offline re-parse can replay the EXACT same selection the live
    scrape made — and so a future fix to the basis logic can be replayed without a
    network re-scrape. ``rows`` is the SELECTED (per-100g) table's rows for backward
    compatibility; ``tables`` carries all panels; ``selection`` carries the metadata.

    Returns::

        {
          "rows": [...],            # rows of the selected per-100g table (replay-ready)
          "tables": [{table_index, basis, subInfo, rows}, ...],  # every panel
          "selection": {selected_basis, selected_table_index, selected_table_header,
                        competing_table_count, insufficient},
          "html": "<outer HTML of every nutritionList div, concatenated>",
        }

    Empty/absent panel → all-empty structure.
    """
    tables = extract_nutrition_tables(soup)
    selection = select_nutrition_table(tables)
    nutr_divs = soup.find_all("div", class_="nutritionList")
    return {
        "rows": selection["rows"],
        "tables": tables,
        "selection": {k: v for k, v in selection.items() if k != "rows"},
        "html": "".join(str(d) for d in nutr_divs),
    }


# ── Canonical raw-string → numeric layer (BSIP0 → BSIP1 build) ──────────────────
#
# TASK-192 / EV-046. Before this, every per-category BSIP1 builder
# (02_build_bsip1_*.py) re-implemented its OWN `_parse_num` / `_parse_sodium` /
# `_parse_nutrition` to turn the scraper's raw strings into floats. Three problems:
#   (a) the "פחות מ N" / "<N" less-than token was silently flattened to N, losing the
#       "this is an upper bound" semantics the QA guard and scoring need;
#   (b) no builder enforced total_fat >= saturated_fat, so an upstream mis-capture
#       sailed straight through to the scored panel;
#   (c) duplication = drift: a fix in one builder never reaches the others (exactly how
#       the EV-029 mis-capture kept recurring). These functions are now the SINGLE
#       numeric path every builder must call.

# Tokens that mark a value as a "less-than" upper bound ("פחות מ 0.5", "< 0.5", "עד 0.5").
_LESS_THAN_MARKERS = ("פחות מ", "פחות", "פחותמ", "<", "עד ", "מתחת ל")


def parse_value_bound(raw) -> tuple[float | None, bool]:
    """Parse a raw Hebrew nutrition value → ``(value, is_upper_bound)``.

    ``"פחות מ 0.5"`` / ``"< 0.5"`` → ``(0.5, True)`` — the true value is *below* 0.5.
    ``"34.2"`` / ``"34.2 גרם"`` → ``(34.2, False)``. ``None``/empty/no-number → ``(None, False)``.
    The float is byte-identical to the legacy per-builder ``_parse_num`` (same number is
    extracted); the second element preserves the less-than semantics those builders dropped.
    """
    if raw is None:
        return None, False
    s = str(raw)
    is_bound = any(mark in s for mark in _LESS_THAN_MARKERS)
    val = _to_float(s)
    return val, (is_bound and val is not None)


def parse_num(raw) -> float | None:
    """Raw value → float (or None). Canonical replacement for per-builder ``_parse_num``.

    Byte-identical to the legacy builder copies on every value they already handled
    (extracts the same number; ``"פחות מ 0.5"`` → 0.5). The less-than flag is available
    separately via ``parse_value_bound`` for callers that need it.
    """
    return parse_value_bound(raw)[0]


def parse_sodium_mg(raw) -> float | None:
    """Raw sodium value → milligrams. Canonical replacement for per-builder ``_parse_sodium``.

    Mirrors the legacy heuristic exactly (byte-identical): if the string says ``mg``
    (Latin) or ``מג`` (Hebrew milligram abbreviation, appended by ``parse_nutrition_rows``
    when div.name="מג") or the number is > 10, the value is already in mg; otherwise it
    is grams → ×1000.

    The Hebrew ``מג`` check is necessary because Shufersal's nutrition panel uses the
    Hebrew milligram abbreviation for sodium (נתרן) on many granola/muesli SKUs, where
    the sodium is a small number (e.g. 7 mg). Without this check the legacy heuristic
    would over-convert 7 mg × 1000 = 7000 mg (TASK-190 root cause for 7 products).
    """
    val = parse_num(raw)
    if val is None:
        return None
    raw_str = str(raw)
    # "mg" (Latin) or "מג" (Hebrew abbreviation for מיליגרם)
    if "mg" in raw_str.lower() or "מג" in raw_str or 'מ"ג' in raw_str or val > 10:
        return val
    return val * 1000


def parse_nutrition_numeric(n: dict) -> dict:
    """Raw ``*_raw`` nutrition dict → canonical numeric panel (the ONE builder path).

    Replaces the per-category ``_parse_nutrition``. Output keys match what the BSIP1
    builders already write, so migrating a builder to call this is byte-identical for
    every panel that was already correct:

        energy_kcal, fat_g, fat_saturated_g, fat_trans_g, cholesterol_mg, sodium_mg,
        carbohydrates_g, sugars_g, dietary_fiber_g, protein_g

    INVARIANT (TASK-192 / EV-046): ``fat_g >= fat_saturated_g``. If a panel arrives with
    saturated > total fat (the unambiguous sub-row-overwrote-total signature), the panel
    is left numerically untouched (no silent repair — that would mask a real upstream
    defect) but ``_integrity`` records the violation so the QA guard / composition gate
    fails the run loudly. Callers that want the flags can read the ``_integrity`` key;
    callers that ignore it get a byte-identical numeric dict for clean panels.
    """
    fat, fat_is_bound = parse_value_bound(n.get("fat_raw"))
    sat, sat_is_bound = parse_value_bound(n.get("saturated_fat_raw"))
    out = {
        "energy_kcal":     parse_num(n.get("energy_kcal_raw")),
        "fat_g":           fat,
        "fat_saturated_g": sat,
        "fat_trans_g":     None,
        "cholesterol_mg":  None,
        "sodium_mg":       parse_sodium_mg(n.get("sodium_raw") or ""),
        "carbohydrates_g": parse_num(n.get("carbs_raw")),
        "sugars_g":        parse_num(n.get("sugar_raw")),
        "dietary_fiber_g": parse_num(n.get("fiber_raw")),
        "protein_g":       parse_num(n.get("protein_raw")),
    }
    integrity: list[str] = []
    if fat is not None and sat is not None and sat > fat + 0.05:
        integrity.append(f"sat_gt_total_fat: saturated={sat}g > total_fat={fat}g")
    if fat_is_bound:
        integrity.append("fat_is_less_than_bound")
    if sat_is_bound:
        integrity.append("saturated_is_less_than_bound")
    # TASK-190 / EV-046 sodium-sanity gate: values above 2000 mg/100g are physically
    # impossible (human cells fail above ~1100 mg/100g; 2000 mg is the safety ceiling).
    # Root cause in the Shufersal cereals corpus: a unit-corruption bug converted g→mg
    # twice (e.g. 4.0 g sodium → recorded as 4000 mg). Products carrying a corrupt
    # sodium value must NOT be scored as if the value were real — route to confidence
    # = insufficient so the BSIP1 builder suppresses scoring. The raw value is preserved
    # (no silent rewrite) so the corruption is auditable downstream.
    sodium_mg = out.get("sodium_mg")
    if sodium_mg is not None and sodium_mg > 2000:
        integrity.append(
            f"sodium_implausible: {sodium_mg:.0f} mg/100g exceeds the 2000 mg safety ceiling "
            f"(unit corruption — value is suppressed from scoring)"
        )
    if integrity:
        out["_integrity"] = integrity
    return out


# ── QA / composition-gate guard ────────────────────────────────────────────────

def _to_float(v) -> float | None:
    """Parse a raw Hebrew nutrition value string to a float bound.

    ``"פחות מ 0.5"`` / ``"< 0.5"`` → 0.5; strips units (גרם / מ"ג / mg / g) and
    normalises decimal comma. Returns ``None`` when no number is present.
    """
    if v is None:
        return None
    s = str(v)
    s = (s.replace("פחות מ", "").replace("פחות", "").replace("<", "")
           .replace("גרם", "").replace('מ"ג', "").replace("מ”ג", "")
           .replace("mg", "").replace("kcal", "").replace("ק\"ג", "")
           .replace(",", ".").strip())
    m = re.search(r"-?\d+(?:\.\d+)?", s)
    return float(m.group()) if m else None


def nutrition_implausible(nutr: dict) -> str | None:
    """Return a reason string if parsed macros are physically implausible, else None.

    Targets the EV-026 fat-overwrite signature so the class fails the BSIP0
    composition gate instead of passing on coverage alone. Accepts either the
    parser's canonical keys (``fat``/``energy``/``saturated_fat``) or the scraper's
    ``*_raw`` output keys.

    Three signatures:
      1. ``saturated_fat > total_fat`` — a sub-row overwrote the total (unambiguous).
      2. Near-zero total fat while the declared energy is >= 50 kcal higher than the
         energy implied by protein+carbs+fat — i.e. fat is understated, not genuinely
         low. (Legitimately low-fat, high-carb foods like cereal flakes pass, because
         their carbs account for the declared energy.)
      3. sodium > 2000 mg/100g — physically impossible; unit corruption (TASK-190).
         Pure sodium chloride (table salt) is 39,330 mg sodium per 100g, so a food
         product cannot exceed ~2000 mg/100g without being pure salt. Detected values
         of 4000–10000 mg are unit-corruption artefacts (g × 1000 applied twice).
    """
    def g(*keys):
        for k in keys:
            if k in nutr and nutr[k] not in (None, ""):
                return _to_float(nutr[k])
        return None

    energy = g("energy", "energy_kcal_raw", "energy_kcal")
    fat = g("fat", "fat_raw", "fat_g")
    sat = g("saturated_fat", "saturated_fat_raw", "saturated_fat_g")
    protein = g("protein", "protein_raw", "protein_g")
    carbs = g("carbs", "carbs_raw", "carbs_g")
    # sodium: route the raw string through the CANONICAL parse_sodium_mg so the Hebrew
    # "מג" milligram marker is honoured (TASK-239 fix — the old inline heuristic here
    # checked only Latin "mg", so "10 מג" was treated as 10 g → 10000 mg, a false
    # implausible flag). Accept a pre-converted sodium_mg numeric as a fallback.
    sodium_raw = None
    for k in ("sodium", "sodium_raw"):
        if k in nutr and nutr[k] not in (None, ""):
            sodium_raw = nutr[k]
            break
    sodium_mg = parse_sodium_mg(sodium_raw) if sodium_raw is not None else None
    if sodium_mg is None:
        sodium_mg = g("sodium_mg")

    if fat is not None and sat is not None and sat > fat + 0.05:
        return f"sat_gt_total_fat: saturated={sat}g > total_fat={fat}g (fat-overwrite signature)"

    if fat is not None and fat <= 0.5 and energy is not None:
        macro_kcal = 4 * (protein or 0) + 4 * (carbs or 0) + 9 * fat
        if energy - macro_kcal >= 50:
            return (f"fat_understated: total_fat={fat}g but declared {energy}kcal exceeds "
                    f"protein+carb+fat energy ({macro_kcal:.0f}kcal) by "
                    f"{energy - macro_kcal:.0f}kcal")

    if sodium_mg is not None and sodium_mg > 2000:
        return (f"sodium_implausible: {sodium_mg:.0f} mg/100g exceeds 2000 mg safety ceiling "
                f"(unit corruption — double g→mg conversion; suppress from scoring)")

    return None


# ── TASK-211: Multi-retailer corpus filter functions ──────────────────────────
#
# These filter functions guard the BSIP0 gate for all retailer scrapers
# (Shufersal, Rami Levy, Carrefour, Victory, Yochananof, etc.). They are the
# shared enforcement layer so no individual scraper can silently skip a check.
# All functions operate on the raw BSIP0 product record dict (as written by the
# scraper) and return (should_filter: bool, reason: str | None).

# Core nutrient fields (raw strings) that must be present for a product to be
# scoreable. Missing >= 3 of these 6 → nutritionally incomplete.
_CORE_NUTRIENT_FIELDS = [
    "energy_kcal_raw",
    "fat_raw",
    "carbs_raw",
    "protein_raw",
    "sodium_raw",
]
# "sugar_raw" and "sugars_raw" are the same field spelled two ways across scrapers.
_SUGAR_FIELD_VARIANTS = ("sugar_raw", "sugars_raw")

# Non-informative ingredient placeholder strings — treated the same as null/empty.
# Covers Hebrew ("ראה אריזה"), French ("voir emballage"), and English ("see packaging").
NON_INFORMATIVE_INGREDIENTS: frozenset[str] = frozenset({
    "ראה אריזה",
    "see packaging",
    "voir emballage",
    "ver embalaje",
})

# Subcategory values that unambiguously mark a product as non-food.
NON_FOOD_SUBCATEGORIES: frozenset[str] = frozenset({
    "baby_care", "cleaning", "personal_care", "cosmetics",
    "pet_care", "hygiene", "household", "pharmacy",
})

# Plausible kcal/100g ceiling for any food (EV-047). Energy values above this
# signal a kJ-as-kcal unit mismatch (3138 kJ butter → 3138 kcal is impossible;
# true value is 3138 × 0.239 ≈ 750 kcal).
KCAL_PLAUSIBLE_UPPER: float = 900.0


def _count_present_core_nutrients(nutrition: dict) -> int:
    """Count how many of the 6 core nutrient fields are non-empty.

    The 6 core fields are: energy_kcal_raw, fat_raw, carbs_raw, protein_raw,
    sodium_raw, and sugar (either 'sugar_raw' or 'sugars_raw'). Returns 0–6.
    """
    present = 0
    for field in _CORE_NUTRIENT_FIELDS:
        if str(nutrition.get(field) or "").strip():
            present += 1
    # Sugar field: accept either spelling.
    for sf in _SUGAR_FIELD_VARIANTS:
        if str(nutrition.get(sf) or "").strip():
            present += 1
            break
    return present


def filter_incomplete_nutrition(product: dict) -> tuple[bool, str | None]:
    """F1 gate — reject products missing >= 3 of the 6 core nutrient fields.

    Returns ``(True, reason)`` when the product should be filtered, else
    ``(False, None)``. Operates on the raw BSIP0 product record; reads
    ``product["nutrition"]``.
    """
    nutrition = product.get("nutrition") or {}
    present = _count_present_core_nutrients(nutrition)
    missing = 6 - present
    if missing >= 3:
        return True, f"incomplete_nutrition: {present}/6 core nutrients present ({missing} missing)"
    return False, None


def filter_ingredients_absent(product: dict) -> tuple[bool, str | None]:
    """F2 gate — reject products with null, empty, or non-informative ingredients.

    Catches ``ingredients_raw: null``, ``""``, and placeholder strings such as
    ``"ראה אריזה"`` (see packaging). NOVA and additive scoring are impossible
    without a real ingredient list.

    Returns ``(True, reason)`` when the product should be filtered.
    """
    raw = product.get("ingredients_raw")
    if raw is None:
        return True, "ingredients_absent: ingredients_raw is null"
    text = str(raw).strip()
    if not text:
        return True, "ingredients_absent: ingredients_raw is empty string"
    if text in NON_INFORMATIVE_INGREDIENTS:
        return True, f"ingredients_absent: non-informative placeholder '{text}'"
    return False, None


def filter_non_food(product: dict) -> tuple[bool, str | None]:
    """F3 gate — reject non-food / cosmetic products scraped from mixed shelves.

    A product is non-food when ALL THREE hold simultaneously:
      (a) All 8 nutrition fields are empty/null.
      (b) ``ingredients_raw`` is null, empty, or a known placeholder.
      (c) ``subcategory_raw`` is in the non-food category set.

    Requiring all three prevents false-positives on legitimately zero-nutrition
    foods (water, pure salt) — those carry real ingredient lists.

    Returns ``(True, reason)`` when the product should be filtered.
    """
    nutrition = product.get("nutrition") or {}
    all_empty = all(
        not str(nutrition.get(f) or "").strip()
        for f in ("energy_kcal_raw", "protein_raw", "carbs_raw", "fat_raw",
                  "fiber_raw", "sodium_raw", "sugar_raw", "saturated_fat_raw")
    )
    raw = product.get("ingredients_raw")
    ingredients_absent = (
        raw is None
        or str(raw).strip() in ("", *NON_INFORMATIVE_INGREDIENTS)
    )
    subcategory = str(product.get("subcategory_raw") or "").strip().lower()
    non_food_cat = subcategory in NON_FOOD_SUBCATEGORIES

    if all_empty and ingredients_absent and non_food_cat:
        return True, (
            f"non_food: zero nutrition + no ingredients + subcategory='{subcategory}'"
        )
    return False, None


def dedup_by_barcode(products: list[dict]) -> dict:
    """F4 gate — deduplicate a product list by barcode, keeping the most complete record.

    Completeness = count of non-empty nutrition fields across all 8 raw keys.
    Ties are broken by ``scraped_at`` (most recent wins).

    Returns ``{"survivors": [...], "dropped": [...]}``. The caller should log
    dropped records for the run record. Products with no barcode are kept as-is
    (cannot deduplicate without a key).
    """
    from collections import defaultdict

    by_barcode: dict[str, list] = defaultdict(list)
    no_barcode = []
    for p in products:
        bc = str(p.get("barcode") or "").strip()
        if bc:
            by_barcode[bc].append(p)
        else:
            no_barcode.append(p)

    survivors, dropped = list(no_barcode), []
    for _, group in by_barcode.items():
        if len(group) == 1:
            survivors.append(group[0])
            continue

        def _score(p: dict) -> tuple[int, str]:
            nutr = p.get("nutrition") or {}
            filled = sum(
                1 for f in ("energy_kcal_raw", "protein_raw", "carbs_raw", "fat_raw",
                             "fiber_raw", "sodium_raw", "sugar_raw", "saturated_fat_raw")
                if str(nutr.get(f) or "").strip()
            )
            return filled, str(p.get("scraped_at") or "")

        ranked = sorted(group, key=_score, reverse=True)
        survivors.append(ranked[0])
        dropped.extend(ranked[1:])

    return {"survivors": survivors, "dropped": dropped}


def detect_kj_energy_misparse(product: dict) -> tuple[bool, str | None, float | None]:
    """F6 gate — detect EU kJ-as-kcal misparsing in the energy_kcal_raw field.

    EU-labeled products (common on Carrefour Israel) sometimes declare energy in
    kJ only. If the scraper captures the kJ row and stores it under
    ``energy_kcal_raw``, ``parse_num`` extracts the kJ number (e.g. 3138) which
    is physically impossible as kcal/100g for any food (ceiling is 900 kcal/100g).

    Returns ``(is_mismatch, reason_or_None, parsed_value_or_None)``.
      - ``is_mismatch=True``:  the field should be suppressed / re-parsed with the
                               0.239 kJ→kcal conversion before any scoring.
      - ``is_mismatch=False``: the value is plausible as kcal or the field is empty.
    """
    nutrition = product.get("nutrition") or {}
    raw_energy = str(nutrition.get("energy_kcal_raw") or "").strip()
    parsed_val = parse_num(raw_energy)

    has_kj_token = "kj" in raw_energy.lower()
    exceeds_ceiling = parsed_val is not None and parsed_val > KCAL_PLAUSIBLE_UPPER

    if has_kj_token and exceeds_ceiling:
        approx_kcal = round(parsed_val * 0.239)
        reason = (
            f"energy_unit_kj_misread_as_kcal: raw='{raw_energy}' parsed to "
            f"{parsed_val:.0f} which exceeds plausible kcal ceiling {KCAL_PLAUSIBLE_UPPER:.0f}. "
            f"Likely kJ value ({parsed_val:.0f} kJ ≈ {approx_kcal} kcal)."
        )
        return True, reason, parsed_val
    if exceeds_ceiling:
        reason = (
            f"energy_implausibly_high: raw='{raw_energy}' → {parsed_val:.0f} "
            f"> ceiling {KCAL_PLAUSIBLE_UPPER:.0f} (possible kJ without unit token — inspect)"
        )
        return True, reason, parsed_val
    return False, None, parsed_val


def apply_bsip0_filters(product: dict) -> tuple[bool, list[str]]:
    """Run all BSIP0 corpus filters against a single product record.

    Convenience wrapper that calls F1–F3 and F6 in sequence. F4 (dedup) must be
    run at corpus level via ``dedup_by_barcode``, not per-product.

    Returns ``(should_filter, [list_of_reasons])``. If any filter fires, the
    product should be excluded from the BSIP1 enrichment corpus.
    """
    reasons: list[str] = []
    for fn in (filter_incomplete_nutrition, filter_ingredients_absent, filter_non_food):
        fired, reason = fn(product)
        if fired:
            reasons.append(reason)
    kj_mismatch, kj_reason, _ = detect_kj_energy_misparse(product)
    if kj_mismatch:
        reasons.append(kj_reason)
    return bool(reasons), reasons


def composition_nutrition_report(products: list[dict], fail_pct: float = 5.0) -> dict:
    """Corpus-level plausibility tally for a BSIP0 ``main()`` composition gate.

    Each product is expected to carry a ``nutrition`` sub-dict with ``*_raw`` keys.
    Returns ``{passed, total, implausible, implausible_pct, examples}``. ``passed``
    is False when the implausible share reaches ``fail_pct`` — i.e. the EV-026
    fat-overwrite class fails the gate instead of passing on coverage alone.
    """
    total = len(products)
    flagged = []
    for p in products:
        reason = nutrition_implausible(p.get("nutrition", p))
        if reason:
            flagged.append((p.get("name_he", p.get("name", "?"))[:40], reason))
    n = len(flagged)
    pct = round(n * 100 / total, 1) if total else 0.0
    return {
        "passed": pct < fail_pct,
        "total": total,
        "implausible": n,
        "implausible_pct": pct,
        "examples": flagged[:8],
    }
