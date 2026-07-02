"""
Probe Rami Levy JS bundles to find actual product search API URLs.
Rami Levy uses Nuxt.js — bundles served at /rl/*.js
"""
from __future__ import annotations
import re, sys, json, urllib.request, urllib.error

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

def get(url, headers=None, timeout=30):
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


BASE = "https://www.rami-levy.co.il"
BUNDLES = ["/rl/4f9ee55.js", "/rl/3322587.js", "/rl/d04b556.js", "/rl/ea76006.js"]

all_api_urls = set()

for bundle_path in BUNDLES:
    url = BASE + bundle_path
    print(f"Fetching {url}...")
    data, status = get(url, {"Referer": BASE + "/"})
    if not data:
        print(f"  FAILED: {status}")
        continue
    js = data.decode("utf-8", errors="replace")
    print(f"  size={len(js)} chars")

    # Find API URL patterns
    # Pattern 1: "/api/..." strings
    for m in re.finditer(r'["\'](/[a-zA-Z][a-zA-Z0-9/_-]{2,80})["\']', js):
        p = m.group(1)
        kws = ["search", "product", "catalog", "barcode", "item", "nutrition"]
        if any(k in p.lower() for k in kws) and p.count("/") >= 2:
            all_api_urls.add(p)

    # Pattern 2: full http URLs
    for m in re.finditer(r'["\']https?://[^"\']{5,120}["\']', js):
        u = m.group(0).strip("'\"")
        if any(k in u.lower() for k in ["api", "search", "product", "catalog"]):
            all_api_urls.add(u)

    # Pattern 3: baseURL
    for m in re.finditer(r'baseURL\s*[:=]\s*["\']([^"\']+)["\']', js):
        all_api_urls.add("BASE: " + m.group(1))

    # Pattern 4: Look for fetch/axios with URL templates
    for m in re.finditer(r'(?:fetch|axios\.(?:get|post))\s*\(`([^`]+)`', js):
        u = m.group(1)
        if len(u) < 200:
            all_api_urls.add("TMPL: " + u[:100])

print(f"\nAll API-like URLs found across bundles: {len(all_api_urls)}")
for u in sorted(all_api_urls):
    print(f"  {u}")

# Also try the Rami Levy search page via Nuxt route
print("\n\nTrying Rami Levy product pages via Nuxt routes...")
nuxt_test_urls = [
    f"{BASE}/he/online-store/search?q=74252",
    f"{BASE}/he/search?q=74252",
    f"{BASE}/he/products/74252",
    f"{BASE}/he/product/74252",
    f"{BASE}/he/catalog?q=74252",
    f"{BASE}/he/catalog/search?q=74252",
    f"{BASE}/he/store/search?q=74252",
    f"{BASE}/api/render-script.js",
]
for url in nuxt_test_urls:
    data, status = get(url, {"Accept": "application/json, text/html, */*", "Referer": BASE + "/"})
    if data and status == 200:
        snippet = data[:300].decode("utf-8", errors="replace")
        print(f"[{status}] {url}")
        print(f"  bytes={len(data)}")
        print(f"  {snippet[:200]}")
    else:
        print(f"[{status}] {url}")
    print()

print("=== Done ===")
