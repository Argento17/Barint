"""
Analyze Victory's AngularJS app.js to find the nutrition API endpoint.
The frontend SaaS JS will contain the API URLs it calls.
"""
from __future__ import annotations
import sys, re, requests
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

VICTORY_BASE = "https://www.victoryonline.co.il"

# ── 1. Read data.js (retailer-specific config) ───────────────────────────────
print("=== 1. data.js (retailer config) ===", flush=True)
data_js_url = "https://htmlcache.blob.core.windows.net/html-production-env/r-1470/desktop/multi-true/data.js?c=1782126421251"
try:
    r = requests.get(data_js_url, timeout=30)
    print(f"  HTTP {r.status_code}, len={len(r.text)}", flush=True)
    # Look for API base URLs
    api_urls = re.findall(r'https?://[^\s"\'\\]+', r.text)
    seen = set()
    for u in api_urls:
        domain = re.match(r'https?://[^/]+', u)
        if domain and domain.group() not in seen:
            seen.add(domain.group())
    print(f"  Distinct domains: {sorted(seen)}", flush=True)
    # Look for nutrition-related keys
    nutr_refs = re.findall(r'[^\s"\']+(?:nutrition|ingredient|product)[^\s"\']{0,50}', r.text, re.I)
    print(f"  Nutrition refs: {nutr_refs[:20]}", flush=True)
    # Show first 3000 chars
    print(f"  First 3000 chars: {r.text[:3000]}", flush=True)
except Exception as e:
    print(f"  ERROR: {e}", flush=True)

# ── 2. Read app.js (minified SaaS frontend) ───────────────────────────────────
print("\n=== 2. app.js (minified — search for API paths) ===", flush=True)
app_js_url = "https://d226b0iufwcjmj.cloudfront.net/frontend/Prutah/0.1.1125/app.js"
try:
    r = requests.get(app_js_url, timeout=60)
    print(f"  HTTP {r.status_code}, len={len(r.text)}", flush=True)
    # Search for nutrition API paths
    nutr_paths = re.findall(r'["\'/][a-zA-Z0-9/_-]*(?:nutrition|ingredient|component)[a-zA-Z0-9/_-]*["\'/]', r.text, re.I)
    print(f"  Nutrition/ingredient paths: {nutr_paths[:30]}", flush=True)
    # Search for /api/ paths
    api_paths = re.findall(r'["\'][/]api[/][a-zA-Z0-9/_-]+["\']', r.text)
    unique_paths = sorted(set(api_paths))
    print(f"  /api/ paths ({len(unique_paths)}): {unique_paths[:40]}", flush=True)
    # Look for product-modal related endpoints
    modal_paths = re.findall(r'["\'][^"\']*(?:modal|details?|popup)[^"\']*["\']', r.text, re.I)
    print(f"  Modal/detail paths: {modal_paths[:20]}", flush=True)
    # Look for "product" + "nutrition" proximity
    product_nutr = re.findall(r'.{0,50}product.{0,100}nutrition.{0,50}', r.text, re.I)
    print(f"  Product+nutrition proximity: {product_nutr[:5]}", flush=True)
except Exception as e:
    print(f"  ERROR: {e}", flush=True)

# ── 3. Try Playwright with network interception to capture XHR calls ──────────
# This is the reliable way to find the API. We'll use Playwright's route interceptor.
print("\n=== 3. Playwright network intercept on product modal ===", flush=True)
try:
    from playwright.sync_api import sync_playwright
    captured_requests = []

    def handle_request(request):
        url = request.url
        if any(k in url.lower() for k in ["nutrition", "ingredient", "product", "component"]):
            if "cloudfront" not in url or "product-info" in url:
                captured_requests.append({"url": url, "method": request.method})

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1500, "height": 900},
            locale="he-IL",
            extra_http_headers={"Accept-Language": "he-IL,he;q=0.9"},
            permissions=[],
        )
        page = context.new_page()
        page.on("request", handle_request)

        # Navigate to a known product
        TEST_BC = "4820005195848"
        search_url = f"{VICTORY_BASE}/category?search={TEST_BC}"
        print(f"  Loading: {search_url}", flush=True)
        page.goto(search_url, wait_until="networkidle", timeout=60000)
        page.wait_for_timeout(8000)

        # Dismiss popups
        for sel in ['button:has-text("אישור")', 'button:has-text("מסכים")', 'button:has-text("הבנתי")']:
            try:
                btn = page.locator(sel).first
                if btn.is_visible(timeout=500):
                    btn.click(force=True)
                    page.wait_for_timeout(500)
            except Exception:
                pass

        print(f"  Captured so far: {len(captured_requests)}", flush=True)

        # Try to click the first product card
        imgs = page.locator("img[src*='cloudfront.net']").all()
        print(f"  Product images found: {len(imgs)}", flush=True)

        if imgs:
            # Get barcodes from CDN urls on the page
            for img in imgs[:5]:
                try:
                    src = img.get_attribute("src") or ""
                    m = re.search(r"/gs1-products/\d+/\w+/(\d{8,13})-", src)
                    if m:
                        bc = m.group(1)
                        print(f"  Found barcode in img: {bc}", flush=True)
                except Exception:
                    pass

            # Try to click the first image to open modal
            try:
                imgs[0].click(force=True)
                page.wait_for_timeout(5000)
                print(f"  Clicked first product, waiting for modal...", flush=True)
                print(f"  Captured after click: {len(captured_requests)}", flush=True)
                for req in captured_requests:
                    print(f"    {req['method']} {req['url']}", flush=True)
            except Exception as e:
                print(f"  Click failed: {e}", flush=True)
        else:
            # No products on this search — try a different query
            print("  No product images. Trying שוקולד מריר search...", flush=True)
            page.goto(f"{VICTORY_BASE}/category?search=שוקולד מריר", wait_until="networkidle", timeout=60000)
            page.wait_for_timeout(8000)
            imgs2 = page.locator("img[src*='cloudfront.net']").all()
            print(f"  Found {len(imgs2)} images on שוקולד מריר search", flush=True)
            if imgs2:
                imgs2[0].click(force=True)
                page.wait_for_timeout(5000)
                print(f"  Captured after click: {len(captured_requests)}", flush=True)
                for req in captured_requests[:20]:
                    print(f"    {req['method']} {req['url']}", flush=True)

        # Capture ALL network requests after modal
        all_requests = []
        page.on("request", lambda req: all_requests.append(req.url))
        page.wait_for_timeout(3000)

        context.close()
        browser.close()

    print(f"\n  Total captured: {len(captured_requests)}", flush=True)
    for req in captured_requests:
        print(f"  {req['method']} {req['url']}", flush=True)

except Exception as e:
    print(f"  ERROR: {e}", flush=True)
    import traceback
    traceback.print_exc()
