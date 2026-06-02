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
_SUBROW_MARKERS = ("מתוכו", "מתוכנ", "מהמ", "מהנ", "שמהמ", "שמהנ")


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
    """Extract the raw ``(value, label)`` rows from ``div.nutritionList``.

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
        divs = item.find_all("div")
        parts = [d.get_text(strip=True) for d in divs if d.get_text(strip=True)]
        if len(parts) < 2:
            continue
        rows.append({"value": parts[0], "label": parts[-1]})
    return rows


def parse_nutrition_rows(rows: list[dict[str, str]]) -> dict[str, str]:
    """Classify pre-extracted ``(value, label)`` rows → ``{field: raw_value_string}``.

    The classification half of the parse, split out so it can run on rows read live
    from a page OR on rows replayed from a persisted ``nutrition_raw_source.rows``
    block. Total fat is read from the genuine total row; saturated/trans land in
    their own fields and never overwrite total fat. First value per field wins —
    totals appear before their sub-rows, so this is correct by construction and also
    defends against any duplicate rows.
    """
    nutr: dict[str, str] = {}
    for row in rows or []:
        field = classify_nutr_label(row.get("label", ""))
        if field and field not in nutr:
            nutr[field] = row.get("value", "")
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

    Two signatures:
      1. ``saturated_fat > total_fat`` — a sub-row overwrote the total (unambiguous).
      2. Near-zero total fat while the declared energy is >= 50 kcal higher than the
         energy implied by protein+carbs+fat — i.e. fat is understated, not genuinely
         low. (Legitimately low-fat, high-carb foods like cereal flakes pass, because
         their carbs account for the declared energy.)
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

    if fat is not None and sat is not None and sat > fat + 0.05:
        return f"sat_gt_total_fat: saturated={sat}g > total_fat={fat}g (fat-overwrite signature)"

    if fat is not None and fat <= 0.5 and energy is not None:
        macro_kcal = 4 * (protein or 0) + 4 * (carbs or 0) + 9 * fat
        if energy - macro_kcal >= 50:
            return (f"fat_understated: total_fat={fat}g but declared {energy}kcal exceeds "
                    f"protein+carb+fat energy ({macro_kcal:.0f}kcal) by "
                    f"{energy - macro_kcal:.0f}kcal")
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
