"""
Deep probe: extract actual product/API data from Victory and Rami Levy pages.
"""
from __future__ import annotations
import re, sys, json, urllib.request, urllib.error

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

def get(url, headers=None, timeout=25):
    hdrs = {"User-Agent": UA, "Accept": "*/*", "Accept-Language": "he-IL,he;q=0.9"}
    if headers:
        hdrs.update(headers)
    try:
        req = urllib.request.Request(url, headers=hdrs)
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read(), r.status
    except urllib.error.HTTPError as e:
        return None, e.code
    except Exception as e:
        return None, str(e)

# ----------------------------------------------------------------
# Victory — examine the search page for product data
# ----------------------------------------------------------------
print("=== VICTORY: examining search result page ===\n")

data, status = get("https://www.victory.co.il/?s=74252")
if data:
    html = data.decode("utf-8", errors="replace")
    print(f"Page size: {len(html)} chars, status={status}")

    # Look for product names / WooCommerce data
    if "74252" in html:
        idx = html.find("74252")
        print(f"Barcode 74252 found at {idx}:")
        print(html[max(0,idx-200):idx+500])
    else:
        print("Barcode NOT found in search results page")

    # Look for any nutrition-related Hebrew terms
    fat_idx = html.find("שומן")
    if fat_idx >= 0:
        print(f"\n'שומן' found at {fat_idx}:")
        print(html[max(0,fat_idx-100):fat_idx+300])
    else:
        print("\n'שומן' NOT found in page")

    # Check for product links
    product_links = re.findall(r'href=["\']([^"\']+product[^"\']+)["\']', html)
    print(f"\nProduct-looking links: {len(product_links)}")
    for l in product_links[:5]:
        print(f"  {l}")

    # Check for WP-JSON or any JSON data in the page
    json_matches = re.findall(r'<script[^>]*type=["\']application/json["\'][^>]*>(.*?)</script>', html, re.DOTALL)
    print(f"\nJSON script blocks: {len(json_matches)}")

    # Look for any wp-json or REST endpoint hints
    for m in re.finditer(r'wp-json[^"\'\\s]{0,100}', html):
        print(f"  wp-json: {m.group(0)}")

# ----------------------------------------------------------------
# Rami Levy — examine home page for API endpoints in JS
# ----------------------------------------------------------------
print("\n\n=== RAMI LEVY: examining home page for API URLs ===\n")

data, status = get("https://www.rami-levy.co.il/")
if data:
    html = data.decode("utf-8", errors="replace")
    print(f"Page size: {len(html)} chars, status={status}")

    # Look for API URLs in the Nuxt config
    for m in re.finditer(r'["\'](/api[^"\']{0,100})["\']', html):
        p = m.group(1)
        if "search" in p.lower() or "product" in p.lower() or "catalog" in p.lower() or "barcode" in p.lower():
            print(f"  API pattern: {p}")

    # Look for axios baseURL or any fetch patterns
    for m in re.finditer(r'baseURL\s*[:=]\s*["\']([^"\']+)["\']', html):
        print(f"  baseURL: {m.group(1)}")

    # Look for __NUXT__ state with product data
    nuxt_idx = html.find("window.__NUXT__")
    if nuxt_idx >= 0:
        print(f"\nwindow.__NUXT__ found at {nuxt_idx}")
        chunk = html[nuxt_idx:nuxt_idx+2000]
        print(chunk[:500])

    # Look for nuxt data inline
    nuxt2 = html.find("__NUXT__=")
    if nuxt2 >= 0:
        print(f"\n__NUXT__= at {nuxt2}")
        print(html[nuxt2:nuxt2+300])

    # Find JS bundle URLs
    js_links = re.findall(r'src=["\']([^"\']*\.js[^"\']*)["\']', html)
    print(f"\nJS bundles: {len(js_links)}")
    for l in js_links[:8]:
        print(f"  {l}")

    # Fetch the first real app bundle to find API calls
    app_bundles = [l for l in js_links if "app" in l.lower() or "main" in l.lower() or "vendor" in l.lower()]
    print(f"\nApp-like bundles: {len(app_bundles)}")

    for bundle_url in app_bundles[:2]:
        print(f"\nFetching bundle: {bundle_url}")
        js_data, _ = get(bundle_url, {"Referer": "https://www.rami-levy.co.il/"})
        if js_data:
            js = js_data.decode("utf-8", errors="replace")
            print(f"  Bundle size: {len(js)} chars")
            # Find API patterns
            api_urls = set()
            for m in re.finditer(r'["\']((?:https?://[^"\']*)?/[a-z][a-z0-9/-]*(?:search|product|catalog|barcode)[a-z0-9/-]*)["\']', js, re.I):
                u = m.group(1)
                if len(u) > 3 and len(u) < 150:
                    api_urls.add(u)
            print(f"  API URLs found: {len(api_urls)}")
            for u in sorted(api_urls)[:20]:
                print(f"    {u}")

            # Also look for baseURL
            for m in re.finditer(r'baseURL\s*[:=]\s*["\']([^"\']+)["\']', js):
                print(f"  baseURL: {m.group(1)}")
        else:
            print(f"  Failed to fetch bundle")

print("\n=== Done ===")
