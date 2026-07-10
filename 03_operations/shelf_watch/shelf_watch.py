#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
shelf_watch.py — Shelf Watch pilot (TASK-570). Weekly, ALERT-ONLY label-change monitor for
the LIVE cereals + bread corpora.

Design doc (read first): 01_framework/operations/shelf_watch/shelf_watch_pilot_v1.md

Hard rules enforced here (standing owner rulings — do not relax without a new task):
  - ALERT-ONLY. This script never writes to bari-web/src/data/comparisons/, never changes a
    score, never auto-publishes. Its only output is a report JSON under runs/.
  - Missing-data discard rule: a failed fetch/parse is DISCARDED from the diff, logged as
    `scrape_failed`, and NEVER counted as drift, NEVER re-sourced from another provider (never
    Open Food Facts — OFF is banned project-wide, forever, every field).
  - Canary-first: before any diffing, 2-3 known-stable barcodes must come back healthy. If not,
    the run aborts with `adapter_unhealthy` rather than emit comparisons off a broken fetch.
  - Retailer scope for this pilot = Shufersal only (both live corpora are 100% Shufersal
    identity — see design doc section 2 for why this is a deliberate scope-fit, not a gap).

KNOWN HISTORY (TASK-590, 2026-07-10) — nutrition_drift was silently disabled from launch
until this fix: ``fetch_shufersal_product`` chained ``bn.parse_nutrition_list(soup)``
(bare keys: "energy", "fat", "sodium", ...) straight into ``bn.parse_nutrition_numeric(...)``
(requires "_raw"-suffixed keys: "energy_kcal_raw", "fat_raw", ...). Every nutrition field
therefore parsed to ``None`` on every run since this pilot went live (TASK-570) — masked
because ``run_canary()``'s health check is ``bool(nutrition)``, and a dict with keys but
all-``None`` values is still truthy, so the canary always reported "healthy". Escalated via
TASK-582 (found while fixing the unrelated 01_acquire_shufersal.py 404), fixed here by
routing through the shared, correct chain ``bn.parse_nutrition_list_numeric(soup)``.
CONSEQUENCE FOR PAST RUNS: every ``no_change`` / ``cosmetic`` classification issued before
this fix is UNTRUSTWORTHY for nutrition specifically — the new-fetch side of every
nutrition comparison was always ``None``, so ``diff_nutrition`` always skipped it
(never asserted a change, never a false positive — just a silent false negative on every
field, every week). Ingredient-change detection was NOT affected (text-based, independent
code path) — the 2 genuine bread ingredient findings from the first real run stand.
Past runs are not rewritten/re-baselined by this fix; only future runs get real nutrition
comparisons. See also: baseline_backfill handling in ``classify_product`` below, added so
the FIRST real-nutrition run for any given product/field is reported distinctly from a
genuine drift, not conflated with it.

Usage (from C:\\Bari):
  python 03_operations\\shelf_watch\\shelf_watch.py                # real run
  python 03_operations\\shelf_watch\\shelf_watch.py --canary-only  # just run the health check
  python 03_operations\\shelf_watch\\shelf_watch.py --selftest     # offline wiring check (no network)
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[1]
RUNS_DIR = HERE / "runs"
BARI_WEB_COMPARISONS = REPO_ROOT.parent / "bari" / "bari-web" / "src" / "data" / "comparisons"

sys.path.insert(0, str(REPO_ROOT / "03_operations" / "bsip0" / "scrape" / "_shared"))
import bsip0_nutrition as bn  # noqa: E402

# ---------------------------------------------------------------------------
# Config — the pilot's watch list. Extend only after extending the canary set
# (design doc section 9) to cover any new retailer that enters scope.
# ---------------------------------------------------------------------------

WATCH_LIST = {
    "breakfast_cereals": {
        "baseline_path": BARI_WEB_COMPARISONS / "cereals_frontend_v2.json",
        "baseline_rel": "bari-web/src/data/comparisons/cereals_frontend_v2.json",
    },
    "bread": {
        "baseline_path": BARI_WEB_COMPARISONS / "bread_frontend_v4.json",
        "baseline_rel": "bari-web/src/data/comparisons/bread_frontend_v4.json",
    },
}

CANARY_BARCODES = [
    ("breakfast_cereals", "5010029000061"),
    ("breakfast_cereals", "7297488098688"),
    ("bread", "7290016245325"),
]

SHUFERSAL_BASE = "https://www.shufersal.co.il"
SHUFERSAL_PRODUCT_URL = SHUFERSAL_BASE + "/online/he/p/p_{barcode}"
HTTP_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "he-IL,he;q=0.9",
    "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
}
REQUEST_TIMEOUT = 25
REQUEST_DELAY_S = 0.6
NUTRITION_EPSILON = 0.05  # float/rounding noise only, NOT a business tolerance band

# Boilerplate that Shufersal appends AFTER the real ingredient list inside the same
# div.componentsText text node (whole-grain-percentage footnote, legal disclaimer, serving
# suggestion). The baseline corpus (built by shufersal_cereals/01_scrape_cereals.py and
# siblings) never included this trailing boilerplate, so a fresh fetch must be truncated at
# the same boundary or every product with a footnote would false-positive as ingredient_change.
# Found live 2026-07-10 while diagnosing 13/43 false-positive ingredient_change results on
# this pilot's first real run (see design doc section 9 / the return for this task).
INGREDIENT_BOUNDARY_MARKERS = [
    "סך הדגנים",            # whole-grain-percentage footnote (cereals)
    "אין להסתמך",           # "do not rely on the site listing" disclaimer
    "יש לקרוא את המופיע",   # "read what's on the physical package" disclaimer
    "התמונות והתאריכים",     # "images/dates are illustrative" disclaimer
    "ערכים תזונתיים 100 גרם",  # stray nutrition-table text (wrong-container bleed guard)
    "לארוחת בוקר ניתן להוסיף",  # serving-suggestion marketing copy
    "מאפיינים נוספים",       # "additional characteristics" claims section heading
]
# Trailing sentence starters trimmed from the END only (never mid-string — a parenthetical
# "(מכיל גלוטן)" qualifier on a specific flour item is untouched; only a full trailing
# sentence like ". מכיל גלוטן חיטה" tacked on after the ingredient list closes is trimmed).
# Applied to BOTH the baseline (frontend JSON) text and the fresh fetch so the two sides are
# compared on the same scope — core ingredient list only, no allergen/claims tail. The
# baseline corpus's own original scraper (01_scrape_cereals.py-family) inconsistently
# included this tail; comparing on the narrower, consistent "ingredients only" scope on both
# sides is more correct than trying to reproduce that inconsistency (see design doc §9 / the
# return for this task).
TRAILING_CLAIM_SENTENCE_STARTERS = ["מכיל ", "עלול להכיל", "ייתכן ויכיל", "עשוי להכיל"]
# A bare (non-parenthesized) "מכיל .../עלול להכיל ..." allergen clause tacked directly onto
# the end of the ingredient text with NO period separator at all (observed live, e.g. "...
# מכיל סויה עלול להכיל אגוזי לוז" with no "." before it). Negative lookbehind excludes a
# legitimate mid-list parenthetical qualifier like "(מכיל גלוטן)", which is always preceded
# by "(" — this only matches a free-standing occurrence.
_BARE_ALLERGEN_CLAUSE_RE = re.compile(r"(?<!\()\s(?:מכיל|עלול להכיל)\b")
_LEADING_INGREDIENTS_LABEL_RE = re.compile(r"^\s*רכיבים\s*:\s*")

# Shufersal's own live HTML sometimes renders an internal line break as a bare literal "n"
# or "r" character (confirmed in raw response bytes, not a BeautifulSoup artifact — see
# design doc / return). Collapse a standalone n/r that touches Hebrew text or punctuation
# (and is NOT part of a vitamin/additive code like "B3"/"E920"/"E341iii", which always has a
# digit or another Latin letter directly adjacent) back to a space.
_STRAY_NEWLINE_LETTER_RE = re.compile(r"(?<![A-Za-z0-9])[nr](?![A-Za-z0-9])")

# Baseline (frontend JSON) expansion.nutrition key -> canonical field name used for the diff.
BASELINE_FIELD_MAP = {
    "energyKcal": "energy_kcal",
    "protein": "protein_g",
    "sugar": "sugars_g",
    "fat": "fat_g",
    "fiber": "dietary_fiber_g",
    "sodium": "sodium_mg",
}


# ---------------------------------------------------------------------------
# Baseline loading
# ---------------------------------------------------------------------------

def load_baseline(category: str) -> dict[str, dict]:
    """barcode -> {name, nutrition: {canonical_field: value}, ingredients: str}"""
    cfg = WATCH_LIST[category]
    path = cfg["baseline_path"]
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    out: dict[str, dict] = {}
    for p in data.get("products", []):
        bc = (p.get("barcode") or "").strip()
        if not bc:
            continue
        exp = p.get("expansion") or {}
        nutr_raw = exp.get("nutrition") or {}
        nutrition = {}
        for src_key, canon_key in BASELINE_FIELD_MAP.items():
            v = nutr_raw.get(src_key)
            if v is not None:
                nutrition[canon_key] = float(v)
        out[bc] = {
            "name": p.get("name") or "",
            "retailer": p.get("retailer") or "",
            "nutrition": nutrition,
            "ingredients": exp.get("ingredients") or "",
        }
    return out


# ---------------------------------------------------------------------------
# Fetch + parse (Shufersal direct-by-barcode; see design doc section 2 for why
# this reuses the requests+BeautifulSoup engine, not the broken crawlee one).
# ---------------------------------------------------------------------------

def normalize_ingredients_text(text: str) -> str:
    """Shared normalization applied to BOTH the baseline (frontend JSON) ingredients string
    and the freshly-fetched one, so the diff compares the same scope on both sides:
      1. Unicode NFKC + collapse the site's stray literal n/r line-break artifacts.
      2. Truncate at the first non-ingredient boundary marker (footnote/disclaimer/claims
         heading — see INGREDIENT_BOUNDARY_MARKERS).
      3. Trim a trailing "מכיל .../עלול להכיל..." allergen-claim sentence (only if it is the
         LAST period-delimited sentence — never touches a parenthetical mid-list qualifier).
    """
    if not text:
        return ""
    t = unicodedata.normalize("NFKC", text)
    t = _STRAY_NEWLINE_LETTER_RE.sub(" ", t)
    t = re.sub(r"\s+", " ", t).strip()
    t = _LEADING_INGREDIENTS_LABEL_RE.sub("", t)  # some templates embed "רכיבים:" in the text itself

    cut_idx = len(t)
    for marker in INGREDIENT_BOUNDARY_MARKERS:
        idx = t.find(marker)
        if idx != -1:
            cut_idx = min(cut_idx, idx)
    t = t[:cut_idx].rstrip(" .rn*")

    while True:
        parts = t.rsplit(".", 1)
        if len(parts) != 2:
            break
        head, tail = parts
        if any(tail.strip().startswith(s) for s in TRAILING_CLAIM_SENTENCE_STARTERS):
            t = head.rstrip(" .rn*")
            continue
        break

    m = _BARE_ALLERGEN_CLAUSE_RE.search(t)
    if m:
        t = t[:m.start()].rstrip(" .rn*")

    return t[:1200]


def extract_ingredients(soup) -> str:
    """Shufersal product-page ingredients.

    PRIMARY: `div.componentsText` — the precise DOM container confirmed live 2026-07-10
    (sibling of the `div.title > div.mainInfo` "רכיבים" heading, inside an `<li>`). Found
    while diagnosing false-positive drift on this pilot's first real run: a naive
    "first element whose text contains the substring 'רכיב'" match sometimes hits a
    marketing badge ("• רכיב מס' 1 חיטה מלאה • ...") that precedes the real ingredients
    section in DOM order on some product templates, or bleeds into the adjacent
    nutrition-table/disclaimer text. `div.componentsText` is unambiguous.

    FALLBACK: the old broad "רכיב" text-search, only if the precise container is absent
    (defensive — has not been observed missing on any product checked, but the pilot's
    corpus is only 43 products and this must not hard-fail on a template variant).
    """
    container = soup.select_one("div.componentsText")
    if container is not None:
        text = container.get_text(" ", strip=True)
    else:
        text = ""
        ingr_label = soup.find(string=re.compile(r"רכיב"))
        if ingr_label:
            parent = ingr_label.find_parent()
            broad = parent.find_parent() if parent else None
            if broad:
                full_text = broad.get_text(separator=" ", strip=True)
                m = re.search(r"רכיב[ים:]*\s*(.*)", full_text, re.DOTALL)
                if m:
                    text = m.group(1).strip()
        if not text:
            for section in soup.find_all("li"):
                t = section.get_text(separator=" ", strip=True)
                m = re.search(r"רכיב[ים:]*\s+(.{30,})", t)
                if m:
                    text = m.group(1)
                    break

    return normalize_ingredients_text(text)


def fetch_shufersal_product(barcode: str) -> dict:
    """Fetch one product page by barcode. Returns a status envelope, never raises."""
    import requests
    from bs4 import BeautifulSoup

    url = SHUFERSAL_PRODUCT_URL.format(barcode=barcode)
    try:
        r = requests.get(url, headers=HTTP_HEADERS, timeout=REQUEST_TIMEOUT, allow_redirects=True)
    except Exception as e:
        return {"status": "scrape_failed", "reason": f"request_exception: {str(e)[:200]}", "barcode": barcode}

    if r.status_code == 404:
        return {"status": "page_gone", "reason": "http_404_on_direct_barcode_url", "barcode": barcode,
                "final_url": r.url}
    if r.status_code != 200:
        return {"status": "scrape_failed", "reason": f"http_{r.status_code}", "barcode": barcode}

    text = r.text
    if len(text) < 5000 and any(s in text.lower() for s in ("maintenance", "אתר בתחזוקה", "בתחזוקה")):
        return {"status": "scrape_failed", "reason": "maintenance_page", "barcode": barcode}

    soup = BeautifulSoup(text, "html.parser")

    ld_gtin = ""
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            ld = json.loads(script.string)
        except Exception:
            continue
        if ld.get("@type") == "Product":
            ld_gtin = ld.get("gtin13", ld.get("gtin", "")) or ""
            break

    if not ld_gtin:
        return {"status": "scrape_failed", "reason": "no_ld_json_product_block", "barcode": barcode,
                "final_url": r.url}

    if str(ld_gtin).strip() != barcode:
        return {"status": "page_gone", "reason": f"gtin_mismatch: resolved to {ld_gtin}", "barcode": barcode,
                "final_url": r.url}

    # Nutrition — the shared canonical parser (same module every Shufersal BSIP0 scraper
    # uses). MUST go through parse_nutrition_list_numeric(), NOT parse_nutrition_list() +
    # parse_nutrition_numeric() composed directly — that direct chain silently returns
    # None for every field (TASK-590: parse_nutrition_list returns bare keys like "energy";
    # parse_nutrition_numeric requires "_raw"-suffixed keys like "energy_kcal_raw"). This
    # exact bug disabled nutrition_drift detection on every shelf_watch run to date — see
    # the module docstring "KNOWN HISTORY" note.
    nutr_numeric = bn.parse_nutrition_list_numeric(soup)

    ingredients_raw = extract_ingredients(soup)

    has_any_nutrition = any(v is not None for k, v in nutr_numeric.items() if not k.startswith("_"))
    if not has_any_nutrition and not ingredients_raw:
        return {"status": "scrape_failed", "reason": "empty_panel_no_nutrition_no_ingredients",
                "barcode": barcode, "final_url": r.url}

    return {
        "status": "scraped",
        "barcode": barcode,
        "final_url": r.url,
        "nutrition": {k: v for k, v in nutr_numeric.items() if not k.startswith("_")},
        "ingredients": ingredients_raw,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
    }


# ---------------------------------------------------------------------------
# Diff + classification
# ---------------------------------------------------------------------------

def _normalize_ingredient_items(text: str) -> list[str]:
    """Comma/semicolon-split items, each whitespace-collapsed + punctuation-stripped.
    Used for the DISPLAYED added/removed lists (readable), not for the equality test."""
    if not text:
        return []
    items = re.split(r"[,;]", text)
    out = []
    for it in items:
        s = unicodedata.normalize("NFKC", it)
        s = re.sub(r"\s+", " ", s).strip()
        s = s.strip(" .\"'״׳")  # trailing punctuation incl. Hebrew gershayim/geresh
        if s:
            out.append(s)
    return out


def _item_content_key(item: str) -> str:
    """Equality key: ALL whitespace removed. Absorbs Shufersal's own live-site spacing
    noise (a stray inserted/dropped space mid-word — e.g. "תערובת" rendered "תע רובת" on
    one fetch and "תערובת" on another; confirmed present in Shufersal's raw HTML itself,
    not a parsing artifact — see design doc section 9). A real ingredient add/remove/edit
    still changes this key; only pure internal spacing does not."""
    return re.sub(r"\s+", "", item)


def diff_ingredients(baseline_text: str, new_text: str) -> dict:
    # Fresh-fetch text has already been through normalize_ingredients_text() inside
    # extract_ingredients(); re-applying is idempotent. The baseline text (straight from the
    # frontend JSON) has NOT — apply the same normalization so both sides share scope.
    base_norm = normalize_ingredients_text(baseline_text)
    new_norm = normalize_ingredients_text(new_text)
    if base_norm == new_norm:
        return {"changed": False, "cosmetic_only": False, "added": [], "removed": []}

    base_display = _normalize_ingredient_items(base_norm)
    new_display = _normalize_ingredient_items(new_norm)
    base_keys = Counter(_item_content_key(x) for x in base_display)
    new_keys = Counter(_item_content_key(x) for x in new_display)
    if base_keys == new_keys:
        return {"changed": True, "cosmetic_only": True, "added": [], "removed": []}

    # Report the human-readable items whose content KEY is not present on the other side
    # (so a pure-spacing item never shows up as a spurious added/removed pair).
    base_by_key: dict[str, list[str]] = {}
    for x in base_display:
        base_by_key.setdefault(_item_content_key(x), []).append(x)
    new_by_key: dict[str, list[str]] = {}
    for x in new_display:
        new_by_key.setdefault(_item_content_key(x), []).append(x)

    added = []
    for k, cnt in (new_keys - base_keys).items():
        added.extend(new_by_key[k][:cnt])
    removed = []
    for k, cnt in (base_keys - new_keys).items():
        removed.extend(base_by_key[k][:cnt])

    return {"changed": True, "cosmetic_only": False, "added": added, "removed": removed}


def diff_nutrition(baseline: dict, new: dict) -> dict:
    """Compare baseline (published-corpus) nutrition to a fresh fetch.

    Returns ``{"deltas": {...}, "backfilled": [...]}``:
      - ``deltas``: fields present on BOTH sides whose values differ beyond
        ``NUTRITION_EPSILON`` — genuine nutrition_drift candidates.
      - ``backfilled`` (TASK-590): fields the fresh fetch has a real (non-None) value
        for, but that ``baseline`` never recorded a key for at all (``load_baseline()``
        only inserts a key when the source value is not None — a missing key is a
        field that was never observed, not a None value). There is no prior value to
        have drifted from, so these are reported distinctly and are NEVER counted as
        drift — added so the FIRST real-nutrition reading for a field (e.g. right
        after the TASK-590 all-None parse bug is fixed) cannot be mistaken for a
        product change.
    """
    deltas = {}
    for field, base_val in baseline.items():
        new_val = new.get(field)
        if new_val is None:
            continue  # field absent in fresh fetch -> not asserted as a change, just missing
        if abs(float(new_val) - float(base_val)) > NUTRITION_EPSILON:
            deltas[field] = {"baseline": base_val, "new": new_val, "delta": round(new_val - base_val, 3)}
    backfilled = sorted(f for f, v in new.items() if v is not None and f not in baseline)
    return {"deltas": deltas, "backfilled": backfilled}


def classify_product(barcode: str, category: str, baseline: dict, fetch_result: dict) -> dict:
    name = baseline["name"]
    if fetch_result["status"] in ("scrape_failed", "page_gone"):
        return {
            "barcode": barcode, "category": category, "name": name,
            "class": fetch_result["status"], "reason": fetch_result.get("reason"),
            "nutrition_diff": {"deltas": {}, "backfilled": []}, "ingredients_diff": {},
            "notes": fetch_result.get("final_url"),
        }

    nutr_diff = diff_nutrition(baseline["nutrition"], fetch_result["nutrition"])
    ingr_diff = diff_ingredients(baseline["ingredients"], fetch_result["ingredients"])

    if nutr_diff["deltas"]:
        cls = "nutrition_drift"
    elif ingr_diff["changed"] and not ingr_diff["cosmetic_only"]:
        cls = "ingredient_change"
    elif ingr_diff["changed"] and ingr_diff["cosmetic_only"]:
        cls = "cosmetic"
    elif nutr_diff["backfilled"]:
        # No drift, no ingredient change — but at least one nutrition field has its
        # first-ever real (non-None) reading against this baseline. Reported so it is
        # visible in the run (and distinguishable in a future diff), never treated as
        # a change to alert on (TASK-590).
        cls = "nutrition_baseline_backfill"
    else:
        cls = "no_change"

    return {
        "barcode": barcode, "category": category, "name": name,
        "class": cls, "reason": None,
        "nutrition_diff": nutr_diff, "ingredients_diff": ingr_diff,
        "notes": None,
    }


# ---------------------------------------------------------------------------
# Canary
# ---------------------------------------------------------------------------

def run_canary() -> dict:
    results = []
    for category, barcode in CANARY_BARCODES:
        r = fetch_shufersal_product(barcode)
        nutr = r.get("nutrition") or {}
        # TASK-590: `bool(nutr)` is truthy even when every value in the dict is None —
        # this exact weak check reported "healthy" on every run while nutrition parsing
        # was silently all-None (the bug this task fixes). Require at least one REAL
        # (non-None) nutrition value, not just a non-empty dict of Nones.
        nutrition_field_count = sum(1 for v in nutr.values() if v is not None)
        healthy = r["status"] == "scraped" and nutrition_field_count > 0
        results.append({"category": category, "barcode": barcode, "status": r["status"],
                         "healthy": healthy, "reason": r.get("reason"),
                         "nutrition_field_count": nutrition_field_count})
    all_healthy = all(r["healthy"] for r in results)
    return {"healthy": all_healthy, "results": results}


# ---------------------------------------------------------------------------
# Main run
# ---------------------------------------------------------------------------

def run(categories: list[str] | None = None) -> dict:
    categories = categories or list(WATCH_LIST.keys())
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_id = f"shelf_watch_{ts}"

    print(f"[{run_id}] canary check ...")
    canary = run_canary()
    print(f"[{run_id}] canary healthy={canary['healthy']}: " +
          ", ".join(f"{r['category']}/{r['barcode']}={r['status']}" for r in canary["results"]))

    if not canary["healthy"]:
        report = {
            "run_id": run_id,
            "status": "adapter_unhealthy",
            "categories": categories,
            "adapter_health": {"shufersal": "unhealthy", "canary_results": canary["results"]},
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }
        RUNS_DIR.mkdir(parents=True, exist_ok=True)
        out_path = RUNS_DIR / f"{run_id}.json"
        out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[{run_id}] ABORTED — adapter_unhealthy. Report: {out_path}")
        return report

    baselines = {}
    baseline_sources = {}
    for cat in categories:
        baselines[cat] = load_baseline(cat)
        baseline_sources[cat] = WATCH_LIST[cat]["baseline_rel"]
        print(f"[{run_id}] baseline loaded: {cat} -> {len(baselines[cat])} products "
              f"({WATCH_LIST[cat]['baseline_rel']})")

    products_out = []
    counts = Counter()
    import time as _time
    for cat in categories:
        for i, (barcode, base) in enumerate(baselines[cat].items(), 1):
            fetch_result = fetch_shufersal_product(barcode)
            rec = classify_product(barcode, cat, base, fetch_result)
            products_out.append(rec)
            counts[rec["class"]] += 1
            if i % 10 == 0:
                print(f"[{run_id}]   {cat} {i}/{len(baselines[cat])} ...")
            _time.sleep(REQUEST_DELAY_S)

    flagged = [p for p in products_out if p["class"] in ("nutrition_drift", "ingredient_change", "page_gone")]

    report = {
        "run_id": run_id,
        "status": "completed",
        "categories": categories,
        "adapter_health": {"shufersal": "healthy", "canary_results": canary["results"]},
        "baseline_sources": baseline_sources,
        "products_total": len(products_out),
        "counts": dict(counts),
        "flagged_for_digest": flagged,
        "digest_worthy": len(flagged) > 0,
        "products": products_out,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = RUNS_DIR / f"{run_id}.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[{run_id}] DONE. products_total={len(products_out)} counts={dict(counts)}")
    print(f"[{run_id}] Report: {out_path}")
    return report


# ---------------------------------------------------------------------------
# Selftest (offline — exercises classification/diff logic only, no network)
# ---------------------------------------------------------------------------

def selftest() -> int:
    ok = True

    # nutrition_drift: any numeric change beyond epsilon
    d = diff_nutrition({"sodium_mg": 110.0, "energy_kcal": 342.0}, {"sodium_mg": 95.0, "energy_kcal": 342.02})
    if "sodium_mg" not in d["deltas"] or "energy_kcal" in d["deltas"]:
        print("FAIL: diff_nutrition epsilon/detection", d); ok = False

    # baseline_backfill (TASK-590): a field the baseline never recorded at all (absent
    # key, not None — load_baseline() only inserts a key when the source value is not
    # None) must NOT be reported as drift when the fresh fetch has a real value for it.
    d_bf = diff_nutrition({"energy_kcal": 342.0}, {"energy_kcal": 342.0, "fiber_g": 10.0})
    if d_bf["deltas"] or d_bf["backfilled"] != ["fiber_g"]:
        print("FAIL: diff_nutrition backfill not isolated from drift", d_bf); ok = False

    rec_bf = classify_product(
        "1", "breakfast_cereals",
        {"name": "x", "nutrition": {"energy_kcal": 342.0}, "ingredients": "a"},
        {"status": "scraped", "nutrition": {"energy_kcal": 342.0, "fiber_g": 10.0},
         "ingredients": "a"},
    )
    if rec_bf["class"] != "nutrition_baseline_backfill":
        print("FAIL: classify_product did not report baseline_backfill", rec_bf); ok = False

    # TASK-590 regression: parse_nutrition_list_numeric on a REAL captured Shufersal
    # nutritionList fixture (barcode 5010029000061, values captured live under TASK-582)
    # must yield non-None numeric fields. This is the exact defect: composing
    # parse_nutrition_list() + parse_nutrition_numeric() directly (the old shelf_watch.py
    # code) returns all-None on this same fixture; parse_nutrition_list_numeric() must not.
    from bs4 import BeautifulSoup
    fixture_html = """
    <li>
      <div class="nutritionListTitle"><div class="subInfo">ל-100 גרם</div></div>
      <div class="nutritionList">
        <div class="nutritionItem"><div class="number">342</div><div class="name">קל</div><div class="text">אנרגיה</div></div>
        <div class="nutritionItem"><div class="number">2</div><div class="name">גרם</div><div class="text">שומנים</div></div>
        <div class="nutritionItem"><div class="number">0.6</div><div class="name">גרם</div><div class="text">שומן רווי</div></div>
        <div class="nutritionItem"><div class="number">69</div><div class="name">גרם</div><div class="text">פחמימות</div></div>
        <div class="nutritionItem"><div class="number">4.2</div><div class="name">גרם</div><div class="text">סוכרים</div></div>
        <div class="nutritionItem"><div class="number">10</div><div class="name">גרם</div><div class="text">סיבים תזונתיים</div></div>
        <div class="nutritionItem"><div class="number">12</div><div class="name">גרם</div><div class="text">חלבון</div></div>
        <div class="nutritionItem"><div class="number">110</div><div class="name">מג</div><div class="text">נתרן</div></div>
      </div>
    </li>
    """
    fixture_soup = BeautifulSoup(fixture_html, "html.parser")
    expected = {
        "energy_kcal": 342.0, "fat_g": 2.0, "fat_saturated_g": 0.6, "carbohydrates_g": 69.0,
        "sugars_g": 4.2, "dietary_fiber_g": 10.0, "protein_g": 12.0, "sodium_mg": 110.0,
    }
    fixture_out = bn.parse_nutrition_list_numeric(fixture_soup)
    for field, want in expected.items():
        got = fixture_out.get(field)
        if got is None or abs(got - want) > 0.01:
            print(f"FAIL: parse_nutrition_list_numeric fixture field {field}: "
                  f"want {want}, got {got} (full: {fixture_out})")
            ok = False

    # OLD (broken) chain must still reproduce the all-None defect on this fixture — proves
    # the fixture actually exercises the bug this task fixes, not a no-op.
    old_chain = bn.parse_nutrition_numeric(bn.parse_nutrition_list(fixture_soup))
    if any(v is not None for k, v in old_chain.items() if not k.startswith("_")):
        print("FAIL: old direct-chain fixture check — expected all-None, got", old_chain)
        ok = False

    # cosmetic: reordering + punctuation only
    base = "חיטה, מלח, סוכר"
    new = "סוכר,מלח,חיטה"
    di = diff_ingredients(base, new)
    if not (di["changed"] and di["cosmetic_only"]):
        print("FAIL: cosmetic reordering not detected as cosmetic", di); ok = False

    # ingredient_change: percentage edit inside a token
    base2 = "חיטה (95%), מלח"
    new2 = "חיטה (90%), מלח"
    di2 = diff_ingredients(base2, new2)
    if not (di2["changed"] and not di2["cosmetic_only"]):
        print("FAIL: percentage change not detected as ingredient_change", di2); ok = False

    # no_change
    di3 = diff_ingredients("חיטה, מלח", "חיטה, מלח")
    if di3["changed"]:
        print("FAIL: identical text flagged as changed", di3); ok = False

    # classify_product end to end (scrape_failed / page_gone pass-through)
    rec = classify_product("123", "breakfast_cereals", {"name": "x", "nutrition": {}, "ingredients": ""},
                            {"status": "scrape_failed", "reason": "timeout"})
    if rec["class"] != "scrape_failed":
        print("FAIL: scrape_failed pass-through", rec); ok = False

    # TASK-590 regression: run_canary()'s health check must NOT report "healthy" on a
    # scraped page whose nutrition dict is non-empty but all-None (the exact shape the
    # all-None parse bug produced on every run to date — this is what let the bug hide).
    global fetch_shufersal_product  # noqa: PLW0603 — test-local monkeypatch, restored after
    _real_fetch = fetch_shufersal_product
    try:
        fetch_shufersal_product = lambda barcode: {  # noqa: E731
            "status": "scraped", "barcode": barcode,
            "nutrition": {"energy_kcal": None, "fat_g": None, "sodium_mg": None},
            "ingredients": "x",
        }
        canary_all_none = run_canary()
    finally:
        fetch_shufersal_product = _real_fetch
    if canary_all_none["healthy"]:
        print("FAIL: run_canary() reported healthy on an all-None nutrition dict", canary_all_none)
        ok = False

    print("SELFTEST", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--canary-only", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--categories", nargs="*", default=None)
    a = ap.parse_args()

    if a.selftest:
        return selftest()
    if a.canary_only:
        c = run_canary()
        print(json.dumps(c, ensure_ascii=False, indent=2))
        return 0 if c["healthy"] else 1

    report = run(a.categories)
    return 0 if report.get("status") == "completed" else 1


if __name__ == "__main__":
    sys.exit(main())
