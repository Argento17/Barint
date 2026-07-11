"""Tiv Taam: search needs real typing (autocomplete, 3+ chars). Try it, and check
if there's a proper e-commerce catalog (product pages, cart) at all -- some
Israeli chains only have a loyalty/info site, no real online store."""
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
    xhrs = []
    page.on("request", lambda req: xhrs.append(req.url) if req.resource_type in ("xhr", "fetch") else None)
    page.goto("https://www.tivtaam.co.il/", wait_until="domcontentloaded", timeout=30000)
    page.wait_for_timeout(4000)

    # find nav links mentioning shopping/store/online
    links = page.evaluate("""
        () => Array.from(document.querySelectorAll('a')).map(a => ({href:a.href, text:a.innerText.trim()}))
            .filter(x => x.text && (x.text.includes('חנות') || x.text.includes('קנ') || x.text.includes('אונליין') || x.text.includes('מוצר')))
    """)
    print("relevant nav links:", len(links))
    for l in links[:20]:
        print(" ", l)

    search_box = page.locator('input[type="search"], input[placeholder*="חפש"], input[type="text"]').first
    try:
        search_box.click(timeout=3000)
        search_box.type("חמאה", delay=100)
        page.wait_for_timeout(2500)
        suggestions = page.evaluate("document.body.innerText.slice(0, 500)")
        print("\nafter typing, body sample:", suggestions[:500])
    except Exception as e:
        print("search interaction failed:", str(e)[:200])

    print("\nxhr/fetch fired so far:", len(xhrs))
    for u in xhrs[-15:]:
        print(" ", u)

    context.close()
    browser.close()
