"""
TASK-518 -- quick reachability + platform probe for two new candidate retailers
(Osher Ad, Tiv Taam) per the playbook's suggested expansion list. Time-boxed:
just check if the homepage/search loads via Playwright (passes any WAF) and
what platform signature it shows (Angular/self-point vs something else), so we
know whether to invest further.
"""
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright
import urllib.parse

CANDIDATES = [
    {"name": "osher_ad", "url": "https://www.osherad.co.il/"},
    {"name": "tiv_taam", "url": "https://www.tivtaam.co.il/"},
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for c in CANDIDATES:
        print(f"\n===== {c['name']} =====")
        context = browser.new_context(
            viewport={"width": 1500, "height": 1000}, locale="he-IL",
            timezone_id="Asia/Jerusalem", extra_http_headers={"Accept-Language": "he-IL,he;q=0.9"},
            permissions=[],
        )
        page = context.new_page()
        try:
            resp = page.goto(c["url"], wait_until="domcontentloaded", timeout=30000)
            print("status:", resp.status if resp else None)
            page.wait_for_timeout(5000)
            title = page.title()
            print("title:", title)
            blocked = "cloudflare" in title.lower() or "blocked" in page.evaluate("document.body.innerText.slice(0,200)").lower()
            print("blocked-looking:", blocked)
        except Exception as e:
            print("goto failed:", str(e)[:200])
        context.close()
    browser.close()
