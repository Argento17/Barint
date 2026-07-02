"""
Verify Victory storefront search works and diagnose why products aren't found.
Tests:
1. Can Victory be reached at all?
2. Does a known simple search return results?
3. Does searching by barcode find CDN image URLs?
4. Does laibcatalog serve Victory files via POST/form?
"""
from __future__ import annotations
import sys, re, requests, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from urllib.parse import quote

VICTORY_BASE = "https://www.victoryonline.co.il"
VICTORY_SEARCH = VICTORY_BASE + "/category?search={query}"
LAIB_BASE = "https://laibcatalog.co.il/"

# ── 1. Victory reachability ──────────────────────────────────────────────────
print("=== 1. Victory reachability ===", flush=True)
try:
    r = requests.get(VICTORY_BASE, timeout=15)
    print(f"  victoryonline.co.il: HTTP {r.status_code}, len={len(r.text)}", flush=True)
except Exception as e:
    print(f"  ERROR: {e}", flush=True)

# ── 2. Search result check ───────────────────────────────────────────────────
print("\n=== 2. Victory search (שוקולד מריר) ===", flush=True)
try:
    url = VICTORY_SEARCH.format(query=quote("שוקולד מריר"))
    r = requests.get(url, timeout=15, headers={"Accept-Language": "he-IL,he;q=0.9"})
    print(f"  HTTP {r.status_code}, len={len(r.text)}", flush=True)
    # Check if it's a JS app (AngularJS)
    has_angular = "ng-app" in r.text or "angular" in r.text.lower()
    has_category = "category" in r.text.lower()
    has_products = "cloudfront" in r.text.lower()
    print(f"  angular={has_angular}, category={has_category}, cloudfront={has_products}", flush=True)
    # If JS renders, the page may just be the shell
    print(f"  First 500 chars: {r.text[:500]}", flush=True)
except Exception as e:
    print(f"  ERROR: {e}", flush=True)

# ── 3. Victory product page (direct URL if any) ───────────────────────────────
# Some sites have direct product URLs by barcode
print("\n=== 3. Try direct product URL patterns ===", flush=True)
TEST_BARCODE = "3046920023443"  # Lindt Excellence dark
candidate_urls = [
    f"{VICTORY_BASE}/product/{TEST_BARCODE}",
    f"{VICTORY_BASE}/item/{TEST_BARCODE}",
    f"{VICTORY_BASE}/p/{TEST_BARCODE}",
    f"{VICTORY_BASE}/category?barcode={TEST_BARCODE}",
    f"{VICTORY_BASE}/api/products/{TEST_BARCODE}",
    f"{VICTORY_BASE}/api/v1/product?barcode={TEST_BARCODE}",
    # The Victory/Yochananof SaaS often has a product search API
    f"{VICTORY_BASE}/api/v1/products?q={TEST_BARCODE}",
    f"{VICTORY_BASE}/api/products/search?barcode={TEST_BARCODE}",
]
for url in candidate_urls:
    try:
        r = requests.get(url, timeout=10)
        has_lindt = "lindt" in r.text.lower() or "לינדט" in r.text
        has_choc = "שוקולד" in r.text or "chocolate" in r.text.lower()
        print(f"  {r.status_code} len={len(r.text)} lindt={has_lindt} choc={has_choc} | {url}", flush=True)
        if has_lindt or (r.status_code == 200 and len(r.text) > 100 and "<!DOCTYPE" not in r.text[:50]):
            print(f"  Content: {r.text[:300]}", flush=True)
    except Exception as e:
        print(f"  ERROR: {e} | {url}", flush=True)

# ── 4. Laibcatalog POST/form for Victory ───────────────────────────────────────
print("\n=== 4. Laibcatalog POST/form for Victory files ===", flush=True)
VICTORY_CHAIN = "7290696200003"
try:
    # The page has a <select> with chain IDs - try posting the form
    session = requests.Session()
    main_r = session.get(LAIB_BASE, timeout=15)

    # Extract hidden form fields
    viewstate = re.search(r'__VIEWSTATE[^>]*value="([^"]*)"', main_r.text)
    eventvalidation = re.search(r'__EVENTVALIDATION[^>]*value="([^"]*)"', main_r.text)
    viewstategenerator = re.search(r'__VIEWSTATEGENERATOR[^>]*value="([^"]*)"', main_r.text)

    # Extract select name for chain
    chain_select = re.search(r'name="([^"]*chainId[^"]*|[^"]*chain[^"]*|[^"]*Chain[^"]*)"', main_r.text)
    chain_select_name = chain_select.group(1) if chain_select else "ctl00$MainContent$chainId"

    # Find the submit button name
    submit_btn = re.search(r'name="([^"]*button[^"]*|[^"]*Button[^"]*|[^"]*submit[^"]*|[^"]*Submit[^"]*)"', main_r.text)
    submit_name = submit_btn.group(1) if submit_btn else "ctl00$MainContent$btnSearch"

    print(f"  ViewState found: {bool(viewstate)}", flush=True)
    print(f"  Chain select name: {chain_select_name}", flush=True)

    form_data = {
        "__VIEWSTATE": viewstate.group(1) if viewstate else "",
        "__EVENTVALIDATION": eventvalidation.group(1) if eventvalidation else "",
        "__VIEWSTATEGENERATOR": viewstategenerator.group(1) if viewstategenerator else "",
        chain_select_name: VICTORY_CHAIN,
        submit_name: "חפש",
    }

    post_r = session.post(LAIB_BASE, data=form_data, timeout=15)
    has_gz = '.gz' in post_r.text.lower()
    print(f"  POST result: HTTP {post_r.status_code}, len={len(post_r.text)}, gz={has_gz}", flush=True)

    if has_gz:
        gz_links = re.findall(r'href=["\']([^"\']*\.gz[^"\']*)["\']', post_r.text)
        print(f"  GZ links: {len(gz_links)}", flush=True)
        for lnk in gz_links[:10]:
            print(f"    {lnk}", flush=True)

    # Look for all form inputs to understand the structure
    form_inputs = re.findall(r'<input[^>]*name="([^"]*)"[^>]*value="([^"]*)"', main_r.text)
    print(f"\n  Form inputs: {len(form_inputs)}", flush=True)
    for name, val in form_inputs[:20]:
        if not name.startswith("__VIEWSTATE") and not name.startswith("__EVENT"):
            print(f"    {name!r} = {val[:50]!r}", flush=True)

    # Find the actual select element for chains
    select_m = re.search(r'<select[^>]*name="([^"]*)"[^>]*>(.*?)</select>', main_r.text, re.DOTALL | re.I)
    if select_m:
        print(f"\n  Select name: {select_m.group(1)}", flush=True)
        options = re.findall(r'<option[^>]*value="([^"]*)"[^>]*>([^<]*)</option>', select_m.group(2))
        print(f"  Options: {len(options)}", flush=True)
        for val, label in options[:10]:
            print(f"    {val} = {label}", flush=True)

except Exception as e:
    print(f"  ERROR: {e}", flush=True)
    import traceback
    traceback.print_exc()
