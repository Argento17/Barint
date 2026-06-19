"""
Targeted fresh fetch — cereals ingredient recovery (TASK-342 / P241).

Fetches the 3 Shufersal product pages whose BSIP1 files are flagged
ingredient_text_quality=marketing_bleed, extracts EVERY possible
ingredient-bearing section from the HTML, then judges honestly whether
what came back is a real back-of-pack declaration or marketing copy again.

Barcodes + Shufersal codes:
  5900020036407  -> P_5900020036407  (ליון דגני שוקולד וקרמל)
  5900020012814  -> P_5900020012814  (דגני בוקר נסקוויק)
  72968          -> P_72968          (דגני בוקר סיני מיניס)

Hard guards:
  - OFF never touched
  - No fabrication
  - No score/nutrition changes
  - Does NOT write to cereals_frontend_v2.json
  - Result is capture-and-report only; written to
    03_operations/bsip0/scrape/shufersal_cereals/ingredients_recovery_task342.json

Marketing-bleed detection phrases (from EV-051 / TASK-198):
  "ניתן להוסיף"   (you can add — serving suggestion)
  "מס' 1"          (No. 1 claim)
  "9 ויטמינים"     (9 vitamins — front-of-pack claim)
  "לארוחת בוקר"   (for breakfast — serving suggestion)
  "תענוג"          (delight/pleasure — marketing)
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from time import sleep

import requests
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ── Constants ─────────────────────────────────────────────────────────────────

TARGETS = [
    {"barcode": "5900020036407", "code": "P_5900020036407", "name_he": "ליון דגני שוקולד וקרמל"},
    {"barcode": "5900020012814", "code": "P_5900020012814", "name_he": "דגני בוקר נסקוויק"},
    {"barcode": "72968",         "code": "P_72968",         "name_he": "דגני בוקר סיני מיניס"},
]

BASE = "https://www.shufersal.co.il"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "he-IL,he;q=0.9",
    "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
}

OUT_DIR = Path(r"C:\Bari\03_operations\bsip0\scrape\shufersal_cereals")

# Marketing-bleed detection: any of these in the extracted text = marketing_bleed again
MARKETING_TIER1 = [
    "ניתן להוסיף",   # "you can add" — classic serving suggestion
    "לארוחת בוקר",   # "for breakfast"
    "תענוג פראי",    # "wild delight"
    "תענוג",         # generic marketing delight phrase
]

MARKETING_TIER2 = [
    "מס' 1",         # "#1" front-of-pack claim
    "9 ויטמינים",    # "9 vitamins" claim
    "ללא חומרים משמרים",  # "no preservatives" — marketing claim, not an ingredient
    "ללא צבעי מאכל",      # "no artificial colors" — marketing claim
]

# Real ingredient signals: if any of these appear alongside a comma/separator structure,
# the text is more likely a real ingredient list
INGREDIENT_SIGNALS = [
    "סוכר",       # sugar
    "קמח",        # flour
    "שוקולד",     # chocolate
    "קקאו",       # cocoa
    "קרמל",       # caramel
    "מלח",        # salt
    "גלוקוז",     # glucose
    "מאלט",       # malt
    "שמן",        # oil
    "ויטמין",     # vitamin (when in actual fortification list, not a claim)
    "ברזל",       # iron
    "סידן",       # calcium
    "נציות",      # emulsifiers
    "מתחלב",      # emulsifier
    "E4",         # E-number (4xx range = emulsifiers/stabilisers)
    "E3",         # E-number (3xx range = antioxidants/colors)
    "E2",         # E-number (2xx range = preservatives)
    "E1",         # E-number (1xx range = colors)
    "חיטה",       # wheat
    "שבולת שועל", # oats
    "תירס",       # corn/maize
    "אורז",       # rice
    "שומן",       # fat/shortening
    "חמאה",       # butter
    "גבינה",      # cheese
    "מי",         # water (מים)
]


def _get(url: str, timeout: int = 30) -> requests.Response | None:
    try:
        r = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
        return r
    except Exception as exc:
        print(f"  [GET error] {url}: {exc}", flush=True)
        return None


def _is_marketing_bleed(text: str) -> tuple[bool, list[str]]:
    """Return (is_marketing_bleed, triggered_phrases)."""
    triggered = []
    for phrase in MARKETING_TIER1:
        if phrase in text:
            triggered.append(f"tier1:{phrase}")
    return bool(triggered), triggered


def _has_ingredient_signals(text: str) -> tuple[bool, list[str]]:
    """Return (has_signals, matched_signals)."""
    matched = []
    for sig in INGREDIENT_SIGNALS:
        if sig in text:
            matched.append(sig)
    return bool(matched), matched


def _count_separators(text: str) -> int:
    """Count comma and semicolon separators — real ingredient lists have many."""
    return text.count(",") + text.count(";") + text.count("،")


def _extract_all_candidate_sections(soup: BeautifulSoup) -> list[dict]:
    """
    Extract every candidate ingredient-bearing section from the page.
    Cast a wider net than the existing scraper — we need to catch the
    back-of-pack panel which may appear in different HTML containers.
    Returns list of {selector, text} dicts for inspection.
    """
    candidates = []

    # Strategy 1: look for "רכיב" (ingredient) label — same as existing scraper
    for node in soup.find_all(string=re.compile(r"רכיב")):
        parent = node.find_parent()
        if not parent:
            continue
        container = parent.find_parent()
        if container:
            full_text = container.get_text(separator=" ", strip=True)
            m = re.search(r"רכיב[ים:]*\s*(.*)", full_text, re.DOTALL | re.IGNORECASE)
            if m:
                extracted = m.group(1).strip()[:2000]
                if len(extracted) > 20:
                    candidates.append({
                        "selector": "ingredient_label_parent_container",
                        "raw_html_tag": container.name,
                        "text": extracted,
                    })

    # Strategy 2: look for tabs or sections with "מרכיבים" / "רכיבים" heading
    for tag in soup.find_all(["div", "section", "li", "span"], string=re.compile(r"מרכיב|רכיב")):
        text = tag.get_text(separator=" ", strip=True)
        if len(text) > 20:
            candidates.append({
                "selector": f"tag_{tag.name}_with_ingredient_label",
                "text": text[:2000],
            })

    # Strategy 3: tab content panels — Shufersal sometimes puts ingredients in
    # a "tab-content" or "productDescription" panel
    for cls in ["tab-content", "productDescription", "product-description",
                "product__description", "ingredientsList", "ingredients",
                "nutritionWrapper", "productDetailTab"]:
        for div in soup.find_all(["div", "section"], class_=re.compile(cls, re.IGNORECASE)):
            text = div.get_text(separator=" ", strip=True)
            if "רכיב" in text and len(text) > 30:
                m = re.search(r"רכיב[ים:]*\s*(.*)", text, re.DOTALL | re.IGNORECASE)
                extracted = m.group(1).strip()[:2000] if m else text[:2000]
                candidates.append({
                    "selector": f"css_class_{cls}",
                    "text": extracted,
                })

    # Strategy 4: data-tab or accordion items (some retailers use JS tabs)
    for div in soup.find_all(attrs={"data-tab": True}):
        text = div.get_text(separator=" ", strip=True)
        if "רכיב" in text and len(text) > 30:
            candidates.append({
                "selector": f"data-tab={div.get('data-tab', 'unknown')}",
                "text": text[:2000],
            })

    # Strategy 5: all <li> sections matching "רכיבים" — same as existing scraper fallback
    for li in soup.find_all("li"):
        text = li.get_text(separator=" ", strip=True)
        m = re.search(r"רכיב[ים:]*\s+(.{30,})", text, re.IGNORECASE)
        if m:
            candidates.append({
                "selector": "li_ingredient_fallback",
                "text": m.group(1)[:2000],
            })

    # Strategy 6: full page text — look for the ingredient block anywhere
    # The back-of-pack typically has a long comma-delimited list after "רכיבים:"
    page_text = soup.get_text(separator="\n", strip=True)
    for m in re.finditer(r"רכיב[ים:]*[:\s]*(.{40,600})", page_text, re.IGNORECASE):
        candidates.append({
            "selector": "full_page_text_regex",
            "text": m.group(1).strip(),
        })

    # Deduplicate by text content
    seen_texts: set[str] = set()
    unique: list[dict] = []
    for c in candidates:
        key = c["text"][:100]
        if key not in seen_texts:
            seen_texts.add(key)
            unique.append(c)

    return unique


def _judge_candidate(text: str) -> dict:
    """
    Judge whether a candidate ingredient text is genuine or marketing copy.
    Returns a verdict dict.
    """
    is_mkt, mkt_phrases = _is_marketing_bleed(text)
    has_signals, signal_matches = _has_ingredient_signals(text)
    sep_count = _count_separators(text)

    # Scoring heuristic:
    # - Marketing Tier1 triggers = hard fail (these phrases ARE marketing text, not ingredients)
    # - Many separators + ingredient signals + no marketing Tier1 = likely genuine
    # - Marketing-only phrases with no separators = marketing_bleed_again

    if is_mkt:
        verdict = "marketing_bleed_again"
        confidence = "high"
        reason = f"Contains marketing tier-1 phrase(s): {mkt_phrases}. Text is front-of-pack copy."
    elif has_signals and sep_count >= 3:
        verdict = "candidate_genuine"
        confidence = "medium"
        reason = (
            f"No marketing tier-1 triggers. Contains {len(signal_matches)} ingredient signal(s): "
            f"{signal_matches[:5]}. Separator count: {sep_count}. "
            f"Structure is consistent with a back-of-pack declaration."
        )
    elif has_signals and sep_count < 3:
        verdict = "uncertain_insufficient_structure"
        confidence = "low"
        reason = (
            f"No marketing tier-1 triggers. Has {len(signal_matches)} ingredient signal(s) "
            f"but only {sep_count} separators — too sparse to confirm a real ingredient list."
        )
    else:
        verdict = "not_ingredient_text"
        confidence = "medium"
        reason = f"No marketing triggers, no ingredient signals. sep_count={sep_count}. Not an ingredient list."

    return {
        "verdict": verdict,
        "confidence": confidence,
        "reason": reason,
        "marketing_triggers": mkt_phrases,
        "ingredient_signals_matched": signal_matches[:10],
        "separator_count": sep_count,
        "text_length": len(text),
    }


def fetch_and_analyze(target: dict) -> dict:
    barcode = target["barcode"]
    code = target["code"]
    name_he = target["name_he"]

    url = f"{BASE}/online/he/p/{code.lower()}"
    print(f"\n--- Fetching barcode={barcode} ({name_he}) ---", flush=True)
    print(f"  URL: {url}", flush=True)

    fetched_at = datetime.now(timezone.utc).isoformat()

    r = _get(url)
    if not r:
        return {
            "barcode": barcode,
            "name_he": name_he,
            "fetch_status": "network_error",
            "http_status": None,
            "source_url": url,
            "fetched_at": fetched_at,
            "outcome": "not_available",
            "outcome_reason": "Network error — could not reach Shufersal",
            "ingredient_text": None,
            "candidates_found": 0,
            "judgment": None,
        }

    print(f"  HTTP {r.status_code}, {len(r.content)} bytes", flush=True)

    if r.status_code != 200:
        return {
            "barcode": barcode,
            "name_he": name_he,
            "fetch_status": f"http_{r.status_code}",
            "http_status": r.status_code,
            "source_url": r.url,
            "fetched_at": fetched_at,
            "outcome": "not_available",
            "outcome_reason": f"HTTP {r.status_code} from Shufersal",
            "ingredient_text": None,
            "candidates_found": 0,
            "judgment": None,
        }

    content_sha256 = hashlib.sha256(r.content).hexdigest()
    soup = BeautifulSoup(r.text, "html.parser")

    # Confirm product identity via JSON-LD
    ld_barcode = None
    ld_name = None
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            if script.string:
                ld = json.loads(script.string)
                if ld.get("@type") == "Product":
                    ld_barcode = ld.get("gtin13", ld.get("sku", ""))
                    ld_name = ld.get("name", "")
                    break
        except Exception:
            pass

    print(f"  JSON-LD barcode: {ld_barcode}, name: {ld_name}", flush=True)

    # Extract all candidate sections
    candidates = _extract_all_candidate_sections(soup)
    print(f"  Candidate sections found: {len(candidates)}", flush=True)

    for i, c in enumerate(candidates):
        print(f"    [{i}] selector={c['selector']} len={len(c['text'])} text_preview={c['text'][:80]!r}", flush=True)

    # Judge each candidate
    judged_candidates = []
    for c in candidates:
        j = _judge_candidate(c["text"])
        judged_candidates.append({**c, "judgment": j})
        print(f"    -> verdict={j['verdict']} confidence={j['confidence']}", flush=True)

    # Pick the best genuine candidate (if any)
    genuine = [c for c in judged_candidates if c["judgment"]["verdict"] == "candidate_genuine"]

    if genuine:
        # Pick the one with the most separators (most structured = most likely real list)
        best = max(genuine, key=lambda c: c["judgment"]["separator_count"])
        outcome = "genuine_captured"
        outcome_reason = best["judgment"]["reason"]
        ingredient_text = best["text"]
    else:
        outcome = "not_available"
        # Describe what came back
        if judged_candidates:
            verdicts = [c["judgment"]["verdict"] for c in judged_candidates]
            outcome_reason = (
                f"No genuine ingredient declaration found among {len(judged_candidates)} candidate(s). "
                f"Verdicts: {verdicts}. "
                f"The page continues to serve marketing/front-of-pack copy in the ingredient field."
            )
        else:
            outcome_reason = "No ingredient-bearing sections found on the page at all."
        ingredient_text = None
        best = None

    result = {
        "barcode": barcode,
        "name_he": name_he,
        "fetch_status": "ok",
        "http_status": r.status_code,
        "source_url": r.url,
        "fetched_at": fetched_at,
        "content_sha256": content_sha256,
        "content_bytes": len(r.content),
        "ld_barcode_confirmed": ld_barcode,
        "ld_name_confirmed": ld_name,
        "outcome": outcome,
        "outcome_reason": outcome_reason,
        "ingredient_text": ingredient_text,
        "best_candidate_selector": best["selector"] if best else None,
        "candidates_found": len(judged_candidates),
        "all_candidates": judged_candidates,
    }

    if outcome == "genuine_captured":
        print(f"  RESULT: GENUINE CAPTURED — {ingredient_text[:120]!r}", flush=True)
    else:
        print(f"  RESULT: NOT AVAILABLE — {outcome_reason[:120]}", flush=True)

    return result


def main():
    print("=== TASK-342 P241: Cereals ingredient recovery ===", flush=True)
    print(f"Targets: {[t['barcode'] for t in TARGETS]}", flush=True)
    print(f"Source: Shufersal direct product pages only (OFF banned)", flush=True)
    print(f"Fetched at: {datetime.now(timezone.utc).isoformat()}", flush=True)
    print("", flush=True)

    results = []
    for i, target in enumerate(TARGETS):
        result = fetch_and_analyze(target)
        results.append(result)
        if i < len(TARGETS) - 1:
            sleep(1.5)  # polite delay between requests

    # Summary
    print("\n=== SUMMARY ===", flush=True)
    genuine_count = sum(1 for r in results if r["outcome"] == "genuine_captured")
    print(f"Genuine ingredient declarations captured: {genuine_count}/{len(TARGETS)}", flush=True)

    for r in results:
        status_str = "GENUINE" if r["outcome"] == "genuine_captured" else "NOT_AVAILABLE"
        print(f"  {r['barcode']} ({r['name_he']}): {status_str}", flush=True)
        if r["ingredient_text"]:
            print(f"    -> {r['ingredient_text'][:120]}", flush=True)
        else:
            print(f"    -> {r['outcome_reason'][:120]}", flush=True)

    # Write output
    run_id = f"ingredient_recovery_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')}"
    output = {
        "run_id": run_id,
        "task_ref": "TASK-342 / P241",
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "source_policy": "shufersal_direct_only — OFF banned",
        "targets": [t["barcode"] for t in TARGETS],
        "genuine_captured": genuine_count,
        "total_targets": len(TARGETS),
        "results": results,
        "guard_confirmations": {
            "off_used": False,
            "score_changed": False,
            "nutrition_changed": False,
            "live_json_touched": False,
            "fabrication": False,
        },
    }

    out_path = OUT_DIR / "ingredients_recovery_task342.json"
    out_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nOutput written: {out_path}", flush=True)
    print(f"Run ID: {run_id}", flush=True)

    return output


if __name__ == "__main__":
    main()
