"""Is Carrefour also hard-blocked by Cloudflare/self-point WAF right now, or just
the v2 REST API path? Check the plain category page (not the API)."""
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
    url = f"https://www.carrefour.co.il/search?text={urllib.parse.quote('חמאה')}"
    try:
        resp = page.goto(url, wait_until="domcontentloaded", timeout=45000)
        print("initial status:", resp.status if resp else None)
        page.wait_for_timeout(8000)
        title = page.title()
        print("title after wait:", title)
        body_snippet = page.evaluate("document.body.innerText.slice(0, 300)")
        print("body text sample:", body_snippet)
    except Exception as e:
        print("goto failed:", str(e)[:300])
    context.close()
    browser.close()
