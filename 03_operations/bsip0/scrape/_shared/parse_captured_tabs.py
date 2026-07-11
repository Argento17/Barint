"""
TASK-515 — parse the captured per-product tab HTML (nutrition.html / ingredients.html)
written by the Victory/Yohananof Playwright scrapers (capture_tab() in
03_operations/bsip0/scrape/victory/01_acquire_victory.py, reused for Yohananof).

Those scrapers' run_report only carries a STATUS STRING per tab ("success" /
"tab_missing" / "timeout" / ...) — the actual nutrition VALUES and ingredients TEXT
live in the saved HTML files under outputs/<barcode>/{nutrition,ingredients}.html.
This module is the missing parse step: reads those files, dispatches to the
retailer-specific nutrition parser already built in bsip0_nutrition.py
(_parse_victory_nutrition / _parse_yohananof_nutrition via extract_nutrition_raw_auto),
and extracts ingredients text directly (the captured tab HTML IS the ingredients
panel — no label-hunting needed, unlike Shufersal's single full-page scrape).
"""
from __future__ import annotations

import sys
from pathlib import Path

from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).resolve().parent))
from bsip0_nutrition import extract_nutrition_raw_auto, parse_nutrition_rows  # noqa: E402

NUTR_KEYS = ["energy", "fat", "saturated_fat", "carbs", "sugar", "fiber", "protein", "sodium"]


def parse_nutrition_html(html_text: str) -> dict:
    """html_text = the captured nutrition-tab dialog innerHTML. Returns the same
    *_raw-keyed dict shape used everywhere else (energy_kcal_raw, fat_raw, ...),
    or an empty dict (all keys "") if the panel could not be classified."""
    empty = {f"{k if k != 'energy' else 'energy_kcal'}_raw": "" for k in NUTR_KEYS}
    if not html_text or not html_text.strip():
        return empty
    soup = BeautifulSoup(html_text, "html.parser")
    result = extract_nutrition_raw_auto(soup)
    selection = result.get("selection", {})
    if selection.get("insufficient"):
        return empty  # never guess a basis — NULL is correct here
    rows = result.get("rows", [])
    parsed = parse_nutrition_rows(rows)  # {field: raw_value_string}
    out = {}
    for k in NUTR_KEYS:
        out_key = f"{k if k != 'energy' else 'energy_kcal'}_raw"
        out[out_key] = parsed.get(k, "")
    return out


def parse_ingredients_html(html_text: str) -> str:
    """The captured *.html file is the WHOLE MUI dialog (capture_current_dialog
    grabs [role="dialog"], not the active tab alone), so a blunt get_text() picks
    up name/price/kashrut/breadcrumb noise ahead of the real ingredient text.
    Yohananof/Victory (same SaaS) render ingredients in '#simple-tabpanel-0'
    specifically (confirmed against a captured sample, TASK-515) — isolate that
    sub-panel first, same discipline as the nutrition parser's own tabpanel-1
    scoping. Falls back to the whole dialog only if that id is absent."""
    if not html_text or not html_text.strip():
        return ""
    soup = BeautifulSoup(html_text, "html.parser")
    panel = soup.select_one("#simple-tabpanel-0")
    scope = panel if panel is not None else soup
    text = scope.get_text(separator=" ", strip=True)
    import re
    text = re.sub(r"^\s*רכיבים?\s*[:\-]?\s*", "", text)
    return text[:1200]


def enrich_run_report(run_report: list[dict], outputs_dir: Path) -> tuple[int, int]:
    """Mutates each record in run_report IN PLACE, adding 'nutrition' and
    'ingredients_raw' keys parsed from outputs/<barcode>/*.html. Returns
    (n_nutrition_parsed, n_ingredients_parsed) for the run summary."""
    n_nutr = 0
    n_ingr = 0
    for rec in run_report:
        bc = str(rec.get("barcode") or "")
        product_dir = outputs_dir / bc
        nutr_html = ""
        ingr_html = ""
        nutr_path = product_dir / "nutrition.html"
        ingr_path = product_dir / "ingredients.html"
        if nutr_path.exists():
            nutr_html = nutr_path.read_text(encoding="utf-8", errors="replace")
        if ingr_path.exists():
            ingr_html = ingr_path.read_text(encoding="utf-8", errors="replace")

        nutrition = parse_nutrition_html(nutr_html)
        ingredients_raw = parse_ingredients_html(ingr_html)

        rec["nutrition"] = nutrition
        rec["ingredients_raw"] = ingredients_raw
        rec["ingredients_language"] = (
            "he" if ingredients_raw and any("א" <= c <= "ת" for c in ingredients_raw) else ""
        )
        if any(nutrition.values()):
            n_nutr += 1
        if ingredients_raw:
            n_ingr += 1
    return n_nutr, n_ingr
