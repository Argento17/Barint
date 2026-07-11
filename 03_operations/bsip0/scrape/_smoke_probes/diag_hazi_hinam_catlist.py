"""Capture ALL xhr/fetch requests fired on initial category-78 (dairy) page load
to find the subcategory-list endpoint (so we can find the butter subcategory id)."""
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        viewport={"width": 1500, "height": 1000}, locale="he-IL",
        timezone_id="Asia/Jerusalem", extra_http_headers={"Accept-Language": "he-IL,he;q=0.9"},
        permissions=[],
    )
    page = context.new_page()
    urls = []
    page.on("request", lambda req: urls.append(req.url) if req.resource_type in ("xhr", "fetch") else None)
    page.goto("https://shop.hazi-hinam.co.il/catalog/78/%D7%9E%D7%95%D7%A6%D7%A8%D7%99-%D7%97%D7%9C%D7%91-%D7%95%D7%91%D7%99%D7%A6%D7%99%D7%9D",
               wait_until="domcontentloaded", timeout=30000)
    page.wait_for_timeout(6000)
    print(f"{len(urls)} xhr/fetch requests:")
    for u in urls:
        print(" ", u)
    context.close()
    browser.close()
