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


def extract_nutrition_rows(soup) -> list[dict[str, str]]:
    """Extract the raw ``(value, unit, label)`` rows from ``div.nutritionList``.

    The Shufersal nutritionItem structure has three child divs:
      - ``div.number`` → the numeric value (e.g. "7", "פחות מ 0.5", "414")
      - ``div.name``   → the unit label (e.g. "גרם" = g, "מג" = mg, "קל" = kcal)
      - ``div.text``   → the nutrient name (e.g. "נתרן", "שומנים")

    We now capture all three. The ``unit`` field is used by ``parse_sodium_mg`` to
    distinguish a value already in mg (unit="מג") from a gram value that must be
    converted (unit="גרם" or absent). Earlier versions captured only value+label,
    losing the unit; for sodium values ≤ 10 the heuristic multiply-by-1000 rule
    then over-converted them (e.g. sodium=7mg on the page → parsed as 7000 mg).

    This is the source signal BEFORE any Hebrew-label classification — exactly the
    pairs ``parse_nutrition_rows`` consumes. Persisting this list in the BSIP0 record
    (see ``extract_nutrition_raw``) lets any future parser fix be replayed OFFLINE,
    so an EV-029-class bug never again forces a fresh network re-scrape to recover
    data the old parser discarded at scrape time.
    """
    rows: list[dict[str, str]] = []
    nutr_div = soup.find("div", class_="nutritionList")
    if not nutr_div:
        return rows
    for item in nutr_div.find_all("div", class_="nutritionItem"):
        # Use named div classes where available to avoid position-dependence
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

    Returns ``{"rows": [{value,label}…], "html": "<outer HTML of div.nutritionList>"}``.
    Scrapers persist this under ``nutrition_raw_source`` in the BSIP0 record. ``rows``
    is the compact, replay-ready signal (feed it back to ``parse_nutrition_rows``);
    ``html`` is the defensive full copy for any future need the row pairs don't cover.
    Empty/absent panel → ``{"rows": [], "html": ""}``.
    """
    nutr_div = soup.find("div", class_="nutritionList")
    return {
        "rows": extract_nutrition_rows(soup),
        "html": str(nutr_div) if nutr_div else "",
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
    # sodium: accept raw string (mg or g heuristic) OR already-converted numeric sodium_mg
    sodium_raw_val = g("sodium", "sodium_raw")
    # Apply the same mg heuristic as parse_sodium_mg: >10 = already mg, else *1000
    sodium_mg = None
    if sodium_raw_val is not None:
        sodium_raw_str = str(nutr.get("sodium") or nutr.get("sodium_raw") or "")
        if "mg" in sodium_raw_str.lower() or sodium_raw_val > 10:
            sodium_mg = sodium_raw_val
        else:
            sodium_mg = sodium_raw_val * 1000
    # Also accept the already-numeric key from parse_nutrition_numeric output
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
