"""Deep probe: find working product search URLs on Victory and Rami Levy."""
from __future__ import annotations
import re, sys, json, urllib.request, urllib.error

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

def get(url, headers=None, timeout=20):
    hdrs = {"User-Agent": UA, "Accept": "*/*", "Accept-Language": "he-IL,he;q=0.9"}
    if headers:
        hdrs.update(headers)
    try:
        req = urllib.request.Request(url, headers=hdrs)
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read()
            ct = r.headers.get("Content-Type", "")
            return raw, r.status, ct, r.geturl()
    except urllib.error.HTTPError as e:
        body = b""
        try: body = e.read()[:200]
        except: pass
        return None, e.code, "", url

def probe(label, url, headers=None):
    data, status, ct, final = get(url, headers)
    if data:
        snippet = data[:400].decode("utf-8", errors="replace")
        print(f"[{status}] {label}")
        print(f"  url={url}")
        print(f"  ct={ct[:60]}  bytes={len(data)}")
        print(f"  {snippet[:300]}")
    else:
        print(f"[{status}] {label}")
        print(f"  url={url}  FAILED")
    print()

# ----- VICTORY (WordPress) -----
print("=== VICTORY (WP-based) ===\n")

# Victory appears to be a WordPress site. Try WP search + WooCommerce product search
probe("V-wp-search", "https://www.victory.co.il/?s=74252")
probe("V-wp-search-json", "https://www.victory.co.il/?s=74252&post_type=product")
probe("V-woocommerce-product-search", "https://www.victory.co.il/wp-json/wc/v3/products?sku=74252", {
    "Accept": "application/json"})
probe("V-woocommerce-search", "https://www.victory.co.il/wp-json/wc/v3/products?search=74252", {
    "Accept": "application/json"})
probe("V-wp-rest-search", "https://www.victory.co.il/wp-json/wp/v2/search?search=74252&type=post", {
    "Accept": "application/json"})

# Try the victory.co.il (no www)
probe("V-nowww-search", "https://victory.co.il/?s=74252")

# ----- RAMI LEVY -----
print("=== RAMI LEVY ===\n")

# Try to find which paths work
probe("RL-root", "https://www.rami-levy.co.il/")
probe("RL-he", "https://www.rami-levy.co.il/he")
probe("RL-catalog", "https://www.rami-levy.co.il/he/catalog")

# Based on their known URL structure from past scrapes
probe("RL-api-barcode", "https://www.rami-levy.co.il/api/catalog/v1/products?barcode=74252",
      {"Accept": "application/json", "Referer": "https://www.rami-levy.co.il/"})
probe("RL-catalog2", "https://www.rami-levy.co.il/api/v2/catalog?q=74252",
      {"Accept": "application/json"})
probe("RL-product-direct", "https://www.rami-levy.co.il/he/catalog/store/-1/product/74252",
      {"Accept": "text/html"})
probe("RL-api-search2", "https://api.rami-levy.co.il/api/catalog/v1/products?q=74252",
      {"Accept": "application/json"})

print("=== Done ===")
