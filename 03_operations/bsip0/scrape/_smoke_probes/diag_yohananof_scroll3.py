"""
TASK-518 diagnostic #3 — replicate the EXACT browse_yohananof_candidates() logic
from yohananof_yogurt/acquire_yogurt_task515.py (same regex, same filters, same
stale-scroll stopping rule) but instrument every rejection reason, to find why
production plateaus at 8 while the raw img-src count (diag #2) grows past 100.
"""
from __future__ import annotations
import json
import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import unquote, urlparse, parse_qs, quote as _q

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent / "outputs" / "diag_yohananof_scroll3.json"
BASE_URL = "https://yochananof.co.il"
QUERY = "יוגורט"

_BARCODE_IN_FILENAME = re.compile(r"_(\d{13})_")

SPOONABLE_INCLUDE = [
    "יוגורט", "yogurt", "yoghurt", "יווני", "greek", "סקיר", "skyr",
    "אקטיביה", "activia", "ביו", "bio", "מולר", "muller", "müller",
    "יופלה", "yoplait", "דנונה", "danone", "פרופ", "froop",
    "קפיר", "kefir", "לאבנה", "labneh", "labne",
]
HARD_DROP = [
    "גלידה", "ice cream", "חמאה", "מרגרינה", "שמנת", "גבינה צהובה",
    "קוטג", "קצפת", "מעדן", "מילקי", "מוס", "פודינג",
    "תוסף", "קפסול", "טבליות", "כמוסות", "זית", "זיתים", "olive",
    "שמפו", "סבון", "ניקוי",
]


def _decode_next_image_url(raw_src: str) -> str:
    first = (raw_src or "").split(" ")[0]
    if "/_next/image" in first and "url=" in first:
        qs = parse_qs(urlparse(first).query)
        if "url" in qs:
            return unquote(qs["url"][0])
    return first


def close_cookie_popup(page):
    for text in ["אישור", "מסכים", "קבל", "הבנתי", "Accept"]:
        try:
            btn = page.get_by_text(text, exact=False).first
            if btn.is_visible(timeout=400):
                btn.click(force=True)
                page.wait_for_timeout(500)
        except Exception:
            pass


_LOAD_MORE_TEXTS = ["טען עוד", "הצג עוד", "עוד תוצאות", "טעינת עוד", "load more"]


def _try_click_load_more(page) -> tuple[bool, str]:
    for text in _LOAD_MORE_TEXTS:
        try:
            btn = page.get_by_text(text, exact=False).first
            if btn.is_visible(timeout=300):
                btn.click(force=True)
                page.wait_for_timeout(1500)
                return True, text
        except Exception:
            pass
    return False, ""


rejects = Counter()
candidates = []
seen_barcodes = set()
stale_scrolls = 0
STALE_LIMIT = 15
MAX_SCROLLS = 30  # shortened for diagnostic speed
per_scroll_log = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        viewport={"width": 1500, "height": 1000},
        locale="he-IL",
        timezone_id="Asia/Jerusalem",
        extra_http_headers={"Accept-Language": "he-IL,he;q=0.9"},
        permissions=[],
    )
    page = context.new_page()
    url = f"{BASE_URL}/category?search={_q(QUERY)}"
    page.goto(url, wait_until="domcontentloaded", timeout=45000)
    page.wait_for_timeout(6000)
    close_cookie_popup(page)

    for scroll_i in range(1, MAX_SCROLLS + 1):
        before = len(candidates)
        imgs = page.locator('img[src*="_next/image"]').all()
        no_regex_match = 0
        no_name = 0
        hard_dropped = 0
        no_include_signal = 0
        dup = 0
        for img in imgs:
            try:
                src = img.get_attribute("src") or ""
                decoded = _decode_next_image_url(src)
                m = _BARCODE_IN_FILENAME.search(decoded)
                if not m:
                    no_regex_match += 1
                    continue
                bc = m.group(1)
                if bc in seen_barcodes:
                    dup += 1
                    continue
                name = (img.get_attribute("alt") or "").strip()
                if not name:
                    no_name += 1
                    continue
                if any(h.lower() in name.lower() for h in HARD_DROP):
                    hard_dropped += 1
                    continue
                if SPOONABLE_INCLUDE and not any(s.lower() in name.lower() for s in SPOONABLE_INCLUDE):
                    no_include_signal += 1
                    continue
                seen_barcodes.add(bc)
                candidates.append({"barcode": bc, "name": name})
            except Exception as e:
                rejects["exception"] += 1

        rejects["no_regex_match"] += no_regex_match
        rejects["no_name"] += no_name
        rejects["hard_dropped"] += hard_dropped
        rejects["no_include_signal"] += no_include_signal
        rejects["dup"] += dup

        clicked, clicked_text = _try_click_load_more(page)
        page.mouse.wheel(0, 1400)
        page.wait_for_timeout(1400 if not clicked else 2000)

        per_scroll_log.append({
            "scroll": scroll_i, "imgs_in_dom": len(imgs), "new_candidates": len(candidates) - before,
            "cum_candidates": len(candidates), "clicked_load_more": clicked, "clicked_text": clicked_text,
            "no_regex_match": no_regex_match, "no_name": no_name, "hard_dropped": hard_dropped,
            "no_include_signal": no_include_signal, "dup": dup,
        })

        if len(candidates) == before:
            stale_scrolls += 1
        else:
            stale_scrolls = 0
        if stale_scrolls >= STALE_LIMIT:
            print(f"STOPPED at scroll {scroll_i}: stale_scrolls={stale_scrolls}")
            break

    context.close()
    browser.close()

result = {
    "total_candidates": len(candidates),
    "candidates": candidates,
    "reject_totals": dict(rejects),
    "per_scroll_log": per_scroll_log,
}
OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"TOTAL CANDIDATES: {len(candidates)}")
print("REJECT TOTALS:", dict(rejects))
for row in per_scroll_log:
    print(row)
