"""Fallback approach: scroll-to-find the product image by barcode substring in
its decoded _next/image src, then click it to open the modal. Verify this works
for a barcode NOT in the initial viewport (7290014758544, which failed direct nav)."""
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright
from urllib.parse import quote as _q, unquote, urlparse, parse_qs
import re

BASE_URL = "https://yochananof.co.il"
QUERY = "חמאה"
TARGET_BARCODE = "7290014758544"


def _decode(raw_src):
    first = (raw_src or "").split(" ")[0]
    if "/_next/image" in first and "url=" in first:
        qs = parse_qs(urlparse(first).query)
        if "url" in qs:
            return unquote(qs["url"][0])
    return first


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
    for text in ["אישור", "מסכים", "קבל", "הבנתי", "Accept"]:
        try:
            btn = page.get_by_text(text, exact=False).first
            if btn.is_visible(timeout=400):
                btn.click(force=True)
                page.wait_for_timeout(500)
        except Exception:
            pass

    found = False
    for scroll_i in range(1, 40):
        imgs = page.locator(f'img[src*="{TARGET_BARCODE}"]').all()
        if imgs:
            print(f"found at scroll {scroll_i}, {len(imgs)} matching imgs")
            try:
                imgs[0].scroll_into_view_if_needed(timeout=5000)
                page.wait_for_timeout(500)
                imgs[0].click(force=True, timeout=5000)
                page.wait_for_timeout(2000)
                dc = page.locator('[role="dialog"]').count()
                print("dialog_count after click:", dc)
                found = True
            except Exception as e:
                print("click failed:", e)
            break
        page.mouse.wheel(0, 1400)
        page.wait_for_timeout(1200)
    if not found:
        print("NEVER FOUND after 40 scrolls")
    context.close()
    browser.close()
