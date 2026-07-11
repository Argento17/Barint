"""Super Yuda's WAF identifies as Radware (server: rdwr header) -- an edge-level
ACL/reputation block, not a Cloudflare-style JS challenge (no interstitial, just
an instant '403 Forbidden / Transaction ID' page). Try a few more angles before
concluding BLOCKED:
  1. static assets (robots.txt, sitemap.xml) -- sometimes served from edge cache
     without invoking the full bot-check.
  2. a second request in the SAME context/session (some Radware configs set an
     unblocking cookie after a first "sacrificial" 403).
  3. a different path prefix (some sites only gate the app routes, not all paths).
"""
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright

BASE = "https://www.yuda.co.il"
PATHS = ["/robots.txt", "/sitemap.xml", "/he", "/shop", "/online", "/", "/"]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        viewport={"width": 1500, "height": 1000}, locale="he-IL",
        timezone_id="Asia/Jerusalem", extra_http_headers={"Accept-Language": "he-IL,he;q=0.9"},
        permissions=[],
    )
    page = context.new_page()
    for path in PATHS:
        try:
            resp = page.goto(BASE + path, wait_until="domcontentloaded", timeout=20000)
            status = resp.status if resp else None
            body = page.evaluate("document.body.innerText.slice(0,120)")
            print(f"{path}: status={status} body={body!r}")
        except Exception as e:
            print(f"{path}: FAILED {str(e)[:150]}")
        page.wait_for_timeout(1500)
    print("\ncookies after all requests:", context.cookies())
    context.close()
    browser.close()
