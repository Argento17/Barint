"""
TASK-518 diagnostic #4 — dump the actual decoded src values that FAIL the barcode
regex, to see what's actually populating the "no_regex_match" bucket, and separately
count how many DISTINCT decoded urls appear across the whole scroll session (to see
if the list is really short, or if genuine product images are being missed by the
regex/selector).
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

OUT = Path(__file__).resolve().parent / "outputs" / "diag_yohananof_scroll4.json"
BASE_URL = "https://yochananof.co.il"
QUERY = "יוגורט"
_BARCODE_IN_FILENAME = re.compile(r"_(\d{13})_")


def _decode(raw_src):
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


all_decoded = Counter()
non_matching_samples = set()
matching_barcodes = set()

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        viewport={"width": 1500, "height": 1000}, locale="he-IL",
        timezone_id="Asia/Jerusalem", extra_http_headers={"Accept-Language": "he-IL,he;q=0.9"},
        permissions=[],
    )
    page = context.new_page()
    url = f"{BASE_URL}/category?search={_q(QUERY)}"
    page.goto(url, wait_until="domcontentloaded", timeout=45000)
    page.wait_for_timeout(6000)
    close_cookie_popup(page)

    for scroll_i in range(1, 25):
        imgs = page.locator('img[src*="_next/image"]').all()
        for img in imgs:
            src = img.get_attribute("src") or ""
            alt = img.get_attribute("alt") or ""
            decoded = _decode(src)
            all_decoded[decoded] += 1
            m = _BARCODE_IN_FILENAME.search(decoded)
            if m:
                matching_barcodes.add(m.group(1))
            else:
                if len(non_matching_samples) < 40:
                    non_matching_samples.add(f"{decoded} | alt={alt[:60]}")
        page.mouse.wheel(0, 1400)
        page.wait_for_timeout(1200)

    # also check: total DISTINCT decoded urls seen, and how many of those look like
    # product photos (contain 'media/catalog/product') vs other assets
    product_like = [d for d in all_decoded if "media/catalog/product" in d or "catalog" in d.lower()]
    context.close()
    browser.close()

result = {
    "distinct_decoded_total": len(all_decoded),
    "matching_barcodes_total": len(matching_barcodes),
    "matching_barcodes": sorted(matching_barcodes),
    "product_like_distinct": len(product_like),
    "non_matching_samples": sorted(non_matching_samples),
    "top_decoded_by_frequency": all_decoded.most_common(15),
}
OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))
