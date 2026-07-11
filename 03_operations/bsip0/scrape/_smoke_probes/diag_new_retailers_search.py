"""Check if Osher Ad / Tiv Taam have an actual online storefront with product
search (not just a corporate/marketing site), and if so what platform."""
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright
import urllib.parse

TRIES = [
    ("osher_ad", "https://www.osherad.co.il/?s=" + urllib.parse.quote("חמאה")),
    ("osher_ad_online", "https://www.osherad-online.co.il/"),
    ("tiv_taam", "https://www.tivtaam.co.il/search?q=" + urllib.parse.quote("חמאה")),
    ("tiv_taam_online", "https://www.tivtaam.co.il/online"),
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for name, url in TRIES:
        print(f"\n===== {name}: {url} =====")
        context = browser.new_context(
            viewport={"width": 1500, "height": 1000}, locale="he-IL",
            timezone_id="Asia/Jerusalem", extra_http_headers={"Accept-Language": "he-IL,he;q=0.9"},
            permissions=[],
        )
        page = context.new_page()
        try:
            resp = page.goto(url, wait_until="domcontentloaded", timeout=25000)
            print("status:", resp.status if resp else None)
            page.wait_for_timeout(4000)
            print("final url:", page.url)
            print("title:", page.title())
            body = page.evaluate("document.body.innerText.slice(0,200)")
            print("body sample:", body[:200])
        except Exception as e:
            print("goto failed:", str(e)[:200])
        context.close()
    browser.close()
