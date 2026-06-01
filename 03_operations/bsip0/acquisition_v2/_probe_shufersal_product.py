"""
Probe a Shufersal product page to check nutrition/ingredient availability.
Also fix URL extraction from the <li> elements.
"""
import requests, re, sys, json
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

h = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36",
    "Accept-Language": "he-IL,he;q=0.9",
    "Accept": "text/html,*/*",
}

BASE = "https://www.shufersal.co.il"

# Load the saved raw products and look at the li HTML more carefully
r = requests.get(f"{BASE}/online/he/search?q=%D7%9C%D7%97%D7%9D&pageSize=5", headers=h, timeout=20)
soup = BeautifulSoup(r.text, "html.parser")
items = soup.find_all("li", attrs={"data-product-name": True})

print(f"Found {len(items)} product items")
if items:
    li = items[0]
    print("\n=== First <li> attrs ===")
    for k, v in li.attrs.items():
        print(f"  {k}: {str(v)[:100]}")

    print("\n=== Links in first <li> ===")
    for a in li.find_all("a"):
        print(f"  href={a.get('href', '')}  class={a.get('class', '')}")

    # Find the product detail URL - try various attrs
    url_attrs = ["data-product-url", "data-href", "data-link", "data-product-link"]
    for attr in url_attrs:
        val = li.get(attr, "")
        if val:
            print(f"  {attr}: {val}")

# Build product URLs from code — Shufersal uses /online/he/P_CODE
# Try multiple URL patterns
sample_code = "P_6451934"
url_patterns = [
    f"{BASE}/online/he/{sample_code}",
    f"{BASE}/online/he/p/{sample_code.lower()}",
    f"{BASE}/online/he/product/{sample_code}",
]
print("\n=== Product URL patterns ===")
for url in url_patterns:
    r2 = requests.get(url, headers=h, timeout=15, allow_redirects=True)
    print(f"  {r2.status_code} {len(r2.content)}B {r2.url}")
    if r2.status_code == 200 and len(r2.content) > 10000:
        soup2 = BeautifulSoup(r2.text, "html.parser")
        # Check for nutrition data
        nutr_signals = ["ערך תזונתי", "קלוריות", "חלבון", "פחמימות", "nutritionFact", "סיבים"]
        ingr_signals = ["רכיבים", "מרכיבים", "Ingredients"]
        for sig in nutr_signals + ingr_signals:
            if sig in r2.text:
                idx = r2.text.find(sig)
                print(f"    FOUND '{sig}': ...{r2.text[max(0,idx-30):idx+150]}...")
                break
        break
