"""
Victory product page direct navigation via productId.
From /api/products/{barcode} we get the internal id.
Victory product pages load as: /category?item={productId}
or similar patterns. Try these to get to the product modal directly
without searching.
"""
import sys, re, json, requests
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright

VICTORY_BASE = "https://www.victoryonline.co.il"

# Known ids from /api/products/{barcode}
MILLENNIUM_BC = "4820005195848"
MILLENNIUM_API_ID = 415280  # This is the "id" in /api/products response (= productId in v2)

# Let's try to navigate to a product directly by id
# Common patterns: /item/{id}, /product/{id}, /category?itemId={id}, etc.

DIRECT_URLS = [
    f"{VICTORY_BASE}/product/{MILLENNIUM_API_ID}",
    f"{VICTORY_BASE}/category?item={MILLENNIUM_API_ID}",
    f"{VICTORY_BASE}/category?itemId={MILLENNIUM_API_ID}",
    f"{VICTORY_BASE}/category?productId={MILLENNIUM_API_ID}",
    # Try the barcode directly in a category search
    f"{VICTORY_BASE}/category?search={MILLENNIUM_BC}",
    f"{VICTORY_BASE}/category?barcode={MILLENNIUM_BC}",
    # The /api/products endpoint also maps via /api/products/{bc}
    # Maybe there's a redirect or deep link for the product page
    f"{VICTORY_BASE}/p/{MILLENNIUM_BC}",
    f"{VICTORY_BASE}/item/{MILLENNIUM_BC}",
]

print("=== Testing direct product page URLs ===", flush=True)
for url in DIRECT_URLS[:6]:
    r = requests.get(url, timeout=10)
    has_products = "cloudfront" in r.text.lower()
    has_modal = "nutritionValues" in r.text or "nutrition" in r.text.lower()
    print(f"  {r.status_code} len={len(r.text)} cdn={has_products} nutr={has_modal} | {url}", flush=True)

# Use Playwright to navigate to the product search page and intercept the product XHR
print("\n=== Playwright: navigate to search page, intercept XHR for product modal ===", flush=True)

captured_responses = []
captured_nutrition = None

def handle_response(response):
    global captured_nutrition
    url = response.url
    # We care about API responses that might include nutritionValues
    if "victoryonline" in url and ("product" in url.lower() or "catalog" in url.lower() or "nutrition" in url.lower()):
        try:
            ct = response.headers.get("content-type", "")
            if "json" in ct:
                body = response.body()
                if b"nutrition" in body.lower() or b"ingredients" in body.lower():
                    text = body.decode("utf-8", errors="replace")
                    captured_responses.append({
                        "url": url,
                        "size": len(body),
                        "preview": text[:300],
                    })
                    if b"nutritionValues" in body and b"values" in body:
                        captured_nutrition = text
        except Exception:
            pass

with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=True)
    context = browser.new_context(
        viewport={"width": 1500, "height": 900},
        locale="he-IL",
        extra_http_headers={"Accept-Language": "he-IL,he;q=0.9"},
        permissions=[],
    )
    page = context.new_page()
    page.on("response", handle_response)

    # Strategy 1: Search by barcode (expecting Victory to show the product)
    url = f"{VICTORY_BASE}/category?search={MILLENNIUM_BC}"
    print(f"\nNavigating to: {url}", flush=True)
    page.goto(url, wait_until="networkidle", timeout=60000)
    page.wait_for_timeout(8000)

    # Dismiss popups
    for sel in ['button:has-text("אישור")', 'button:has-text("מסכים")']:
        try:
            btn = page.locator(sel).first
            if btn.is_visible(timeout=500):
                btn.click(force=True)
                page.wait_for_timeout(500)
        except Exception:
            pass

    # Check what's on the page
    imgs = page.locator("img[src*='cloudfront.net']").all()
    print(f"  Images found: {len(imgs)}", flush=True)

    # Show the first few image URLs to understand what's on the page
    for img in imgs[:10]:
        try:
            src = img.get_attribute("src") or img.get_attribute("ng-src") or ""
            m = re.search(r"/gs1-products/\d+/\w+/(\d{8,13})-", src)
            if m:
                print(f"  BC in img: {m.group(1)} | {src[:100]}", flush=True)
        except Exception:
            pass

    # Check all XHR requests captured so far
    all_requests = []
    page.on("request", lambda r: all_requests.append(r.url) if "victoryonline" in r.url else None)
    page.wait_for_timeout(3000)

    print(f"\n  Captured API responses: {len(captured_responses)}", flush=True)
    for r_info in captured_responses:
        print(f"  {r_info['url']} ({r_info['size']} bytes)", flush=True)

    # Strategy 2: Use the AngularJS "item" route if it exists
    # Victory's AngularJS router may have a route like /category/item/{id}
    for test_url in [
        f"{VICTORY_BASE}/category/item/{MILLENNIUM_API_ID}",
        f"{VICTORY_BASE}/category#!/item/{MILLENNIUM_API_ID}",
        f"{VICTORY_BASE}#!/category/item/{MILLENNIUM_API_ID}",
    ]:
        print(f"\nTrying: {test_url}", flush=True)
        try:
            page.goto(test_url, wait_until="networkidle", timeout=30000)
            page.wait_for_timeout(5000)
            dialog = page.locator('[role="dialog"]').first
            if dialog.count() > 0:
                print(f"  Modal found!", flush=True)
                print(f"  Dialog HTML: {dialog.inner_html(timeout=3000)[:500]}", flush=True)
            else:
                print(f"  No modal. Page title: {page.title()}", flush=True)
        except Exception as e:
            print(f"  Error: {e}", flush=True)

    print(f"\n  Total API responses with nutrition: {len([r for r in captured_responses if 'nutrition' in r['url'].lower()])}", flush=True)
    if captured_nutrition:
        print(f"\n  NUTRITION DATA FOUND:\n  {captured_nutrition[:1000]}", flush=True)

    context.close()
    browser.close()
