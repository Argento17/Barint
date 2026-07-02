"""
Now that we have product IDs, probe Victory for nutrition via product-ID-based routes.
Also check the SaaS backend endpoints that Yochananof/Victory share.
"""
from __future__ import annotations
import sys, re, requests, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

VICTORY_BASE = "https://www.victoryonline.co.il"

# Known product IDs from the previous probe
PRODUCTS = {
    "3046920023443": {"id": 7872576, "name": "שוקולד קרמי מריר"},      # Lindt Excellence dark
    "3046920023429": {"id": 7872575, "name": "אקסטרה קרימי שוקולד חלב מעולה עם חתיכות קרמל ומלח"},
    "3046920023368": {"id": 7872574, "name": "אקסטרה קרימי שוקולד חלב"},
    "4820005195848": {"id": 415280,  "name": "שוקולד מריר 80%"},          # Millennium 80%
    "3046920028004": {"id": 6181,    "name": "אקסלנס שוקולד מריר 70% קקאו"},
    "4820005198597": {"id": 324953,  "name": "שוקולד מריר 74%"},
    "5941021001261": {"id": 817732,  "name": "שוקולד מריר 75% קקאו"},
    "7290119500482": {"id": 7630501, "name": "שוקולד מריר מעולה 62%"},
}

# Test with Millennium 80% first (key target)
TEST_BC = "4820005195848"
TEST_ID = 415280

def get(url: str) -> requests.Response:
    try:
        return requests.get(url, timeout=15, headers={
            "Accept": "application/json",
            "Accept-Language": "he-IL,he;q=0.9",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0.0.0",
        })
    except Exception as e:
        print(f"  ERR {e}", flush=True)
        class Fake:
            status_code = 0
            text = ""
        return Fake()

print(f"=== Probing nutrition endpoints for Millennium 80% (id={TEST_ID}) ===", flush=True)

NUTRITION_ENDPOINTS = [
    # By product id
    f"{VICTORY_BASE}/api/products/{TEST_ID}",
    f"{VICTORY_BASE}/api/products/{TEST_ID}/info",
    f"{VICTORY_BASE}/api/products/{TEST_ID}/page",
    f"{VICTORY_BASE}/api/products/{TEST_ID}/product",
    # Category-based
    f"{VICTORY_BASE}/api/catalog/{TEST_ID}",
    f"{VICTORY_BASE}/api/catalog/item/{TEST_ID}",
    # Nutrition specific
    f"{VICTORY_BASE}/api/nutrition/{TEST_ID}",
    f"{VICTORY_BASE}/api/nutritions/{TEST_ID}",
    f"{VICTORY_BASE}/api/product-nutrition/{TEST_ID}",
    f"{VICTORY_BASE}/api/product/{TEST_ID}",
    # The /api/products/{barcode} variant showed 558 bytes of JSON
    # Let's explore that more fully
    f"{VICTORY_BASE}/api/products/{TEST_BC}",
    # Component endpoints
    f"{VICTORY_BASE}/api/components/{TEST_ID}",
    f"{VICTORY_BASE}/api/components/product/{TEST_ID}",
    # Yochananof/Victory SaaS backend typically at /retailer/...
    f"{VICTORY_BASE}/retailer/products/{TEST_ID}",
    f"{VICTORY_BASE}/retailer/api/products/{TEST_ID}",
    # Check if there's a mobile or app API
    f"{VICTORY_BASE}/app/api/products/{TEST_ID}",
    f"{VICTORY_BASE}/mobile/api/products/{TEST_ID}",
]

for url in NUTRITION_ENDPOINTS:
    r = get(url)
    is_json = r.text.strip()[:1] in ("{", "[") if r.text else False
    has_nutr = any(k in r.text for k in ["נתרן", "sodium", "kcal", "קלוריות", "nutritionValues", "חלבון", "שומן"])
    print(f"  {r.status_code} len={len(r.text)} json={is_json} nutr={has_nutr} | {url}", flush=True)
    if has_nutr and len(r.text) < 3000:
        print(f"  DATA: {r.text[:500]}", flush=True)

# Check the full response of the known-working endpoint
print("\n=== Full /api/products/{barcode} response for Millennium 80% ===", flush=True)
r = get(f"{VICTORY_BASE}/api/products/{TEST_BC}")
print(r.text, flush=True)

# ── Check if there's a separate nutrition/ingredients SaaS API (e.g. under cdn or api subdomain) ──
print("\n=== Try alternate subdomains ===", flush=True)
SUBDOMAIN_URLS = [
    f"https://api.victoryonline.co.il/products/{TEST_BC}",
    f"https://api.victoryonline.co.il/products/{TEST_ID}",
    f"https://cdn.victoryonline.co.il/products/{TEST_ID}/nutrition",
    # The CDN is d226b0iufwcjmj.cloudfront.net — check if it has a products API
    f"https://d226b0iufwcjmj.cloudfront.net/product-info/{TEST_ID}",
    f"https://d226b0iufwcjmj.cloudfront.net/products/{TEST_ID}/nutrition",
    # Check if ZuZ (the AngularJS app name from page) is a SaaS vendor
    f"https://www.zuz.co.il/api/products/{TEST_ID}",
    # The SaaS vendor is likely "Green Invoice" / "Shlomo" / "Nibit" or similar
    # Let's check if the API is at a different path based on the AngularJS controller
    f"{VICTORY_BASE}/api/items/{TEST_ID}",
    f"{VICTORY_BASE}/api/item/{TEST_ID}",
]
for url in SUBDOMAIN_URLS:
    try:
        r = get(url)
        has_nutr = any(k in r.text for k in ["נתרן", "sodium", "kcal", "קלוריות", "nutrition", "protein"])
        if r.status_code != 0:
            print(f"  {r.status_code} len={len(r.text)} nutr={has_nutr} | {url}", flush=True)
            if has_nutr:
                print(f"  DATA: {r.text[:400]}", flush=True)
    except Exception:
        pass

# ── Inspect what JavaScript files reference nutritionValues ──────────────────
print("\n=== Check main page JS for API path ===", flush=True)
r = get(VICTORY_BASE)
# Find all .js script src attributes
scripts = re.findall(r'src="([^"]*\.js[^"]*)"', r.text)
print(f"  Scripts: {scripts[:10]}", flush=True)
# Look for nutritionValues or nutrition in the page
nutr_refs = re.findall(r'([^\s"\'<>{}\[\]]+nutrition[^\s"\'<>{}\[\]]+)', r.text, re.I)
print(f"  Nutrition refs in HTML: {nutr_refs[:10]}", flush=True)
