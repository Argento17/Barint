"""Does the Victory Cloudflare interstitial (403 on initial goto) actually resolve
to real page content after waiting, the way it apparently did for prior successful
Victory scraper runs earlier today? Check page.content() after a long wait."""
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright
import urllib.parse

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        viewport={"width": 1500, "height": 1000}, locale="he-IL",
        timezone_id="Asia/Jerusalem", extra_http_headers={"Accept-Language": "he-IL,he;q=0.9"},
        permissions=[],
    )
    page = context.new_page()
    url = f"https://www.victoryonline.co.il/category?search={urllib.parse.quote('חמאה')}"
    resp = page.goto(url, wait_until="domcontentloaded", timeout=45000)
    print("initial status:", resp.status if resp else None)
    page.wait_for_timeout(9000)
    title = page.title()
    print("title after wait:", title)
    body_snippet = page.evaluate("document.body.innerText.slice(0, 300)")
    print("body text sample:", body_snippet)
    is_cf = "Just a moment" in title or "challenge" in page.url.lower() or "cloudflare" in (page.content().lower()[:2000])
    print("still on CF challenge:", is_cf)
    img_count = page.locator('img[src*="cloudfront.net"], img[ng-src*="cloudfront.net"]').count()
    print("cloudfront img count:", img_count)
    context.close()
    browser.close()
