"""Quick final check: does Osher Ad have a real online storefront (product pages,
not just a marketing/recipes site)? Look for footer/nav links to a shop domain,
and check common candidate subdomains."""
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
    page.goto("https://www.osherad.co.il/", wait_until="domcontentloaded", timeout=30000)
    page.wait_for_timeout(4000)
    all_links = page.evaluate("""
        () => Array.from(document.querySelectorAll('a')).map(a => a.href)
            .filter(h => h && !h.includes('facebook') && !h.includes('instagram') && !h.includes('javascript'))
    """)
    external_ish = [h for h in all_links if "osherad.co.il" not in h]
    print("non-osherad.co.il links:", len(external_ish))
    for h in sorted(set(external_ish))[:20]:
        print(" ", h)
    print("\ntotal internal links sample:")
    internal = sorted(set(h for h in all_links if "osherad.co.il" in h))
    for h in internal[:30]:
        print(" ", h)
    context.close()
    browser.close()
