"""
Victory branch API — correctly fetch products with nutritionValues.

Key findings:
1. /v2/retailers/1470/branches/2930/products?appId=4&filters={...} returns full data
   INCLUDING nutritionValues and ingredients in data.1.ingredients
2. The filters use LISTING IDs (not barcode, not productId from /api/products/)
3. We need to find listing IDs for our target products

Strategy:
- Intercept the branch API calls from Playwright to find the actual listing IDs
  in use, then call the branch API directly with our target IDs
- Alternative: use a search endpoint to get listing IDs for specific barcodes
"""
import sys, re, json, requests
from urllib.parse import urlencode, quote
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright

VICTORY_BASE = "https://www.victoryonline.co.il"
RETAILER_ID = 1470
BRANCH_ID = 2930

# Target products from /api/products/{barcode}
TARGETS = {
    "4820005195848": {"pid": 415280,  "label": "Millennium 80%"},
    "3046920023443": {"pid": 7872576, "label": "Lindt Excellence dark"},
    "3046920023429": {"pid": 7872575, "label": "Lindt caramel milk"},
    "3046920023368": {"pid": 7872574, "label": "Lindt Excellence milk"},
    "3046920028004": {"pid": 6181,    "label": "Lindt 70%"},
    "4820005198597": {"pid": 324953,  "label": "Millennium 74%"},
    "5941021001261": {"pid": 817732,  "label": "75% dark"},
    "7290119500482": {"pid": 7630501, "label": "62% dark"},
}

# Branch API helper — make the request WITHOUT encoding Hebrew in filters
# (the API returns products when filters contains IS-ACTIVE+visible terms)
def fetch_branch_products_by_ids(listing_ids: list[int]) -> list[dict]:
    """
    Fetch products from the branch API using listing IDs (the 8-digit IDs
    used in the Playwright-intercepted filter URLs).
    """
    filters = {
        "must": {
            "exists": ["family.id", "family.categoriesPaths.id", "branch.regularPrice"],
            "term": {
                "branch.isActive": True,
                "branch.isVisible": True,
                "id": listing_ids,
            }
        },
        "mustNot": {"term": {"branch.regularPrice": 0}},
        "bool": {"should": [
            {"bool": {"must_not": {"exists": {"field": "branch.outOfStockShowUntilDate"}}}},
            {"bool": {"must": [
                {"range": {"branch.outOfStockShowUntilDate": {"gt": "now"}}},
                {"term": {"branch.isOutOfStock": True}},
            ]}},
            {"bool": {"must": [{"term": {"branch.isOutOfStock": False}}]}},
        ]}
    }
    # Use requests with proper encoding
    filters_str = json.dumps(filters, ensure_ascii=True, separators=(",", ":"))
    url = f"{VICTORY_BASE}/v2/retailers/{RETAILER_ID}/branches/{BRANCH_ID}/products"
    try:
        r = requests.get(url, params={"appId": 4, "filters": filters_str, "from": 0, "size": len(listing_ids) + 5},
                         timeout=30, headers={"Accept": "application/json"})
        print(f"  Branch API: {r.status_code} len={len(r.text)}", flush=True)
        if r.text.strip()[:1] == "{":
            return r.json().get("products", [])
    except Exception as e:
        print(f"  Branch API error: {e}", flush=True)
    return []


# ── Step 1: Use Playwright to find listing IDs for our targets ─────────────────
print("=== Using Playwright to find listing IDs for target products ===", flush=True)

listing_id_map = {}  # productId -> listing_id
all_listing_data = {}  # listing_id -> product data

captured_api_data = []

def handle_response(response):
    url = response.url
    if "victoryonline" in url and "branches" in url and "products" in url:
        try:
            ct = response.headers.get("content-type", "")
            if "json" in ct:
                body = response.body()
                text = body.decode("utf-8", errors="replace")
                if '"products"' in text and len(body) > 1000:
                    try:
                        data = json.loads(text)
                        prods = data.get("products", [])
                        captured_api_data.extend(prods)
                    except Exception:
                        pass
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

    # Load the chocolate category page which will trigger branch API calls
    url = f"{VICTORY_BASE}/category/2282"  # typical chocolate/candy category
    print(f"  Loading category page...", flush=True)
    page.goto(url, wait_until="networkidle", timeout=60000)
    page.wait_for_timeout(8000)

    # Dismiss popups
    for sel in ['button:has-text("אישור")', 'button:has-text("מסכים")', 'button:has-text("הבנתי")', '[data-aria-desc="dialog_cookies_accept"]']:
        try:
            btn = page.locator(sel).first
            if btn.is_visible(timeout=500):
                btn.click(force=True)
                page.wait_for_timeout(500)
        except Exception:
            pass

    # Scroll to trigger more API calls
    for _ in range(5):
        page.mouse.wheel(0, 1500)
        page.wait_for_timeout(1500)

    print(f"  Captured {len(captured_api_data)} products from branch API", flush=True)

    # Try searching for chocolate
    page.goto(f"{VICTORY_BASE}/category?search=שוקולד מריר 80", wait_until="networkidle", timeout=60000)
    page.wait_for_timeout(8000)

    # Dismiss popups again
    for sel in ['button:has-text("אישור")', 'button:has-text("מסכים")', 'button:has-text("הבנתי")']:
        try:
            btn = page.locator(sel).first
            if btn.is_visible(timeout=500):
                btn.click(force=True)
                page.wait_for_timeout(500)
        except Exception:
            pass

    # Scroll more
    for _ in range(20):
        page.mouse.wheel(0, 1200)
        page.wait_for_timeout(800)

    print(f"  Total captured after search: {len(captured_api_data)} products", flush=True)

    # Try clicking a visible product to get the full product modal API call
    imgs = page.locator("img[src*='cloudfront.net']").all()
    print(f"  Images on search page: {len(imgs)}", flush=True)

    if imgs:
        # Click first few images to trigger product modal API calls
        for img in imgs[:5]:
            try:
                src = img.get_attribute("src") or img.get_attribute("ng-src") or ""
                m = re.search(r"/gs1-products/\d+/\w+/(\d+)-", src)
                if m:
                    bc = m.group(1)
                    print(f"  Clicking product {bc}...", flush=True)
                    img.scroll_into_view_if_needed(timeout=3000)
                    page.wait_for_timeout(500)
                    img.click(force=True)
                    page.wait_for_timeout(4000)
                    dialog = page.locator('[role="dialog"]').first
                    if dialog.count() > 0:
                        inner_html = dialog.inner_html(timeout=3000)
                        if "nutritionValues" not in inner_html and len(inner_html) > 100:
                            print(f"    Modal opened, clicking nutrition tab...", flush=True)
                            nutr_tab = page.get_by_role("tab", name="ערכים תזונתיים").first
                            if nutr_tab.count() > 0:
                                nutr_tab.click(force=True)
                                page.wait_for_timeout(2000)
                    page.keyboard.press("Escape")
                    page.wait_for_timeout(800)
            except Exception as e:
                print(f"  Click error: {e}", flush=True)
                page.keyboard.press("Escape")

    print(f"  Final total captured: {len(captured_api_data)} products", flush=True)

    context.close()
    browser.close()

# ── Step 2: Find our targets in captured data ─────────────────────────────────
print(f"\n=== Searching captured data for our targets ===", flush=True)

# Build index by productId
by_product_id = {}
for p in captured_api_data:
    pid = p.get("productId") or p.get("id")
    if pid:
        by_product_id[pid] = p

print(f"  Unique products by ID: {len(by_product_id)}", flush=True)

# Look for 80% dark chocolate in captured products
print("\n  Scanning for 75-85% chocolate...")
for p in captured_api_data:
    name = p.get("localName") or p.get("name", "")
    branch_info = p.get("branch", {})
    prod_data = p.get("data", {})
    lang1_data = prod_data.get("1", {}) or prod_data.get(1, {})
    nv = p.get("nutritionValues", {})
    nv_values = nv.get("values", []) if isinstance(nv, dict) else []

    pct_m = re.search(r'(\d{2,3})\s*%', name or "")
    if pct_m:
        pct = int(pct_m.group(1))
        if 60 <= pct <= 90:
            pid = p.get("productId", p.get("id"))
            bc = p.get("barcode", "")
            ingr = lang1_data.get("ingredients", "") if isinstance(lang1_data, dict) else ""
            print(f"  {pct}% | id={pid} | bc={bc} | name={name[:60]}", flush=True)
            print(f"    nutr_rows={len(nv_values)} | ingr_len={len(ingr)}", flush=True)

# Look for target products by productId
print("\n  Searching for targets by productId:")
target_product_ids = {v["pid"] for v in TARGETS.values()}
for p in captured_api_data:
    pid = p.get("productId", p.get("id"))
    if pid in target_product_ids:
        name = p.get("localName") or p.get("name", "")
        bc = p.get("barcode", "")
        nv = p.get("nutritionValues", {})
        nv_values = nv.get("values", []) if isinstance(nv, dict) else []
        prod_data = p.get("data", {})
        lang1 = prod_data.get("1", {}) or prod_data.get(1, {})
        ingr = lang1.get("ingredients", "") if isinstance(lang1, dict) else ""
        print(f"  FOUND: pid={pid} | bc={bc} | name={name[:60]}", flush=True)
        print(f"    nutr_rows={len(nv_values)} | ingr={ingr[:100]}", flush=True)
        listing_id_map[pid] = p.get("id")

# Save any useful product data
import pathlib, datetime
out_path = pathlib.Path(r"C:\Bari\02_products\chocolate\victory_branch_captured.json")
out_path.write_text(json.dumps(
    {"total": len(captured_api_data), "by_pid_keys": list(by_product_id.keys())[:100]},
    ensure_ascii=False, indent=2
), encoding="utf-8")
print(f"\nSaved summary: {out_path}", flush=True)
