"""Test the discovered Rami Levy API endpoints."""
from __future__ import annotations
import re, sys, json, urllib.request, urllib.error

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

def get(url, headers=None, timeout=25):
    hdrs = {"User-Agent": UA, "Accept": "*/*", "Accept-Language": "he-IL,he;q=0.9",
            "Referer": "https://www.rami-levy.co.il/"}
    if headers:
        hdrs.update(headers)
    try:
        req = urllib.request.Request(url, headers=hdrs)
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read()
            return raw, r.status, r.headers.get("Content-Type", ""), r.geturl()
    except urllib.error.HTTPError as e:
        body = b""
        try: body = e.read()[:300]
        except: pass
        return body, e.code, "", url
    except Exception as e:
        return None, str(e), "", url

def probe(label, url, headers=None):
    data, status, ct, final = get(url, headers)
    if data:
        snippet = data[:600].decode("utf-8", errors="replace")
        print(f"[{status}] {label}")
        print(f"  url: {url}")
        print(f"  ct: {ct[:80]}  bytes: {len(data)}")
        print(f"  snippet: {snippet[:400]}")
    else:
        print(f"[{status}] {label}")
        print(f"  url: {url}")
    print()

BC = "74252"  # Osem sesame crackers

# The catalog search
probe("RL-catalog-direct", f"https://www.rami-levy.co.il/api/catalog?q={BC}",
      {"Accept": "application/json"})

# www-api endpoints
probe("RL-www-api-v2", f"https://www-api.rami-levy.co.il/api/v2/site",
      {"Accept": "application/json"})

probe("RL-www-api-search", f"https://www-api.rami-levy.co.il/api/v2/products/search?q={BC}",
      {"Accept": "application/json"})

probe("RL-www-api-product", f"https://www-api.rami-levy.co.il/api/v2/products/{BC}",
      {"Accept": "application/json"})

probe("RL-www-api-barcode", f"https://www-api.rami-levy.co.il/api/v2/products?barcode={BC}",
      {"Accept": "application/json"})

probe("RL-www-api-v3", f"https://www-api.rami-levy.co.il/api/v3/site",
      {"Accept": "application/json"})

# Online search page (Nuxt SSR)
probe("RL-online-search", f"https://www.rami-levy.co.il/he/online/search?q={BC}",
      {"Accept": "text/html"})

# Try online product page
probe("RL-product-online", f"https://www.rami-levy.co.il/he/online/product/{BC}",
      {"Accept": "text/html"})

# Shelfs API
probe("RL-shelfs", f"https://www.rami-levy.co.il/api/shelfs/",
      {"Accept": "application/json"})

print("=== Done ===")
