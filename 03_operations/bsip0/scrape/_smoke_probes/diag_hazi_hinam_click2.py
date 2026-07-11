"""Hazi Hinam: the existing exploration script's click on the card didn't open
a nutrition modal. Try clicking directly on the product NAME text/link inside
the card (not the outer card wrapper), and log network requests fired on click
to see if a product-detail XHR exists even if the DOM doesn't visibly change."""
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright

DAIRY_URL = "https://shop.hazi-hinam.co.il/catalog/78/%D7%9E%D7%95%D7%A6%D7%A8%D7%99-%D7%97%D7%9C%D7%91-%D7%95%D7%91%D7%99%D7%A6%D7%99%D7%9D"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        viewport={"width": 1500, "height": 1000}, locale="he-IL",
        timezone_id="Asia/Jerusalem", extra_http_headers={"Accept-Language": "he-IL,he;q=0.9"},
        permissions=[],
    )
    page = context.new_page()

    xhr_log = []
    def on_request(req):
        if req.resource_type in ("xhr", "fetch"):
            xhr_log.append(req.url)
    page.on("request", on_request)

    page.goto(DAIRY_URL, wait_until="domcontentloaded", timeout=30000)
    page.wait_for_timeout(5000)
    for sel in ['button:has-text("סגור")', 'button:has-text("אישור")']:
        try:
            btn = page.locator(sel).first
            if btn.is_visible(timeout=800):
                btn.click(force=True)
                page.wait_for_timeout(500)
        except Exception:
            pass

    xhr_log.clear()
    card = page.locator("[class*='product-item']").first
    # Dump the card's inner HTML structure to find the real clickable target
    html = card.inner_html()
    print("CARD HTML (first 1500 chars):")
    print(html[:1500])

    # Try clicking a product-name-like element inside the card
    name_el = card.locator("a, [class*='name'], [class*='title']").first
    print("\nname_el count:", card.locator("a, [class*='name'], [class*='title']").count())
    try:
        name_el.click(force=True, timeout=5000)
        page.wait_for_timeout(3000)
    except Exception as e:
        print("click failed:", str(e)[:200])

    print("\nXHR/fetch requests fired after click:")
    for u in xhr_log[:30]:
        print(" ", u)

    dialog_count = page.locator('[role="dialog"], .modal, [class*="modal"]').count()
    print("\nmodal-like element count:", dialog_count)
    content = page.content()
    for sig in ["ערכים תזונתיים", "רכיבים", "מידע אלרגני", "רכיבי", "אנרגיה"]:
        if sig in content:
            print("found signal in DOM:", sig)

    context.close()
    browser.close()
