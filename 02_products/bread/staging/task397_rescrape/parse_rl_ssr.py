"""
Parse nutrition from Rami Levy SSR pages (window.__NUXT__ state).
The product page /he/online/product/{barcode} returns Nuxt SSR HTML
with the full product data embedded in window.__NUXT__.
"""
from __future__ import annotations
import re, sys, json, urllib.request, urllib.error

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

def get(url, headers=None, timeout=25):
    hdrs = {
        "User-Agent": UA,
        "Accept": "text/html,*/*",
        "Accept-Language": "he-IL,he;q=0.9,en;q=0.7",
        "Referer": "https://www.rami-levy.co.il/",
    }
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


# Test barcodes — focusing on the 9 priority implausible ones
TEST_BARCODES = [
    "74252",          # Osem sesame crackers (kcal_gap=147 — very implausible)
    "7290016245325",  # Tahini bread (kcal_gap=59)
    "7290016967074",  # Angel whole wheat bread (kcal_gap=64)
    "8434165658523",  # Cream crackers (kcal_gap=130)
    "96086000966",    # Whole spelt sesame crackers (kcal_gap=112)
    "7290014321168",  # Les Prusa Keto (kcal_gap=105)
    "2079033",        # Light grain bread (kcal_gap=56)
    "2079217",        # Sourdough rye+nuts (kcal_gap=65)
    "6451484",        # Sourdough nuts+raisins (kcal_gap=55)
]


def extract_nuxt_data(html: str) -> dict | None:
    """Extract window.__NUXT__ data from Rami Levy SSR page."""
    # The NUXT state is a compressed IIFE — too complex to eval safely.
    # Instead, look for JSON-LD structured data or product-specific JSON blobs.

    # Method 1: JSON-LD
    for m in re.finditer(r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', html, re.DOTALL):
        try:
            obj = json.loads(m.group(1))
            if isinstance(obj, dict) and obj.get("@type") in ("Product", "FoodProduct"):
                return {"source": "json_ld", "data": obj}
            if isinstance(obj, list):
                for item in obj:
                    if isinstance(item, dict) and item.get("@type") in ("Product", "FoodProduct"):
                        return {"source": "json_ld", "data": item}
        except Exception:
            pass

    # Method 2: Look for nutrition-related JSON patterns in the page
    # Rami Levy embeds product data in Nuxt state — search for nutrition patterns
    fat_patterns = [
        r'"fat"\s*:\s*(\d+[\.,]\d*|\d+)',
        r'"שומן"\s*:\s*"?(\d+[\.,]\d*)"?',
        r'"total_fat"\s*:\s*(\d+[\.,]\d*|\d+)',
        r'"totalFat"\s*:\s*"?(\d+[\.,]\d*)"?',
        r'שומן[^<\n]{0,30}?(\d+[\.,]\d*)\s*(?:ג|g)',
    ]
    for pat in fat_patterns:
        m = re.search(pat, html, re.UNICODE | re.I)
        if m:
            try:
                val = float(m.group(1).replace(",", "."))
                if 0 < val < 100:
                    return {"source": "html_pattern", "fat_g": val, "raw": m.group(0)[:120]}
            except ValueError:
                pass

    # Method 3: Extract the __NUXT__ IIFE argument list (compressed values)
    # The pattern is: window.__NUXT__=(function(a,b,c,...){ return {...} })(val1,val2,...)
    # The return object references variable names. Very hard without eval.
    # Instead search for any numeric values in close proximity to "שומן"
    fat_idx = html.find("שומן")
    while fat_idx >= 0:
        chunk = html[fat_idx:fat_idx+300]
        for m in re.finditer(r'(\d+[\.,]\d+|\d{1,3})', chunk):
            val_str = m.group(1).replace(",", ".")
            try:
                v = float(val_str)
                if 0.5 <= v <= 50.0:  # plausible fat range for bread/crackers
                    return {"source": "proximity", "fat_g": v,
                            "raw": chunk[:150], "note": "proximity heuristic — needs verification"}
            except ValueError:
                pass
        fat_idx = html.find("שומן", fat_idx + 1)

    return None


# Test each barcode
print("=== Testing Rami Levy product pages ===\n")

for bc in TEST_BARCODES:
    url = f"https://www.rami-levy.co.il/he/online/product/{bc}"
    print(f"[{bc}] {url}")
    data, status = get(url)
    if not data or status != 200:
        print(f"  FAILED: status={status}")
        continue

    html = data.decode("utf-8", errors="replace")
    print(f"  status={status} bytes={len(html)}")

    # Check if the barcode appears in the page (product found vs generic 404-within-200)
    title_m = re.search(r'<title>([^<]+)</title>', html)
    title = title_m.group(1) if title_m else ""
    print(f"  title: {title[:80]}")

    # Check for product name (Hebrew content)
    if bc in html:
        print(f"  barcode found in HTML")

    # Look for שומן (fat) near the barcode
    fat_idx = html.find("שומן")
    if fat_idx >= 0:
        chunk = html[max(0,fat_idx-200):fat_idx+500]
        print(f"  'שומן' found at idx={fat_idx}")
        print(f"  context: {chunk[:400]}")
    else:
        print(f"  'שומן' NOT found in page")

    # Try extraction
    result = extract_nuxt_data(html)
    if result:
        print(f"  EXTRACTED: {result}")
    else:
        print(f"  No nutrition extracted")

    # Also check for __NUXT__ size and snip relevant part
    nuxt_idx = html.find("window.__NUXT__")
    if nuxt_idx >= 0:
        # Search for barcode in the NUXT chunk
        nuxt_chunk = html[nuxt_idx:nuxt_idx+50000]
        bc_in_nuxt = bc in nuxt_chunk
        print(f"  barcode in __NUXT__ data: {bc_in_nuxt}")
        if bc_in_nuxt:
            idx = nuxt_chunk.find(bc)
            print(f"  context around bc in NUXT: {nuxt_chunk[max(0,idx-100):idx+500]}")

    print()

print("=== Done ===")
