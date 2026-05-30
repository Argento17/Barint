"""Inspect Shufersal search HTML for embedded product JSON."""
import requests, json, re, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

h = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36",
    "Accept-Language": "he-IL,he;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

r = requests.get("https://www.shufersal.co.il/online/he/search?q=%D7%9C%D7%97%D7%9D", headers=h, timeout=20)
print(f"Status: {r.status_code}  Size: {len(r.content)}B")
html = r.text

# Look for embedded JSON patterns
patterns = [
    (r'window\.__INITIAL_STATE__\s*=\s*(\{.*?\});', "INITIAL_STATE"),
    (r'window\.__PRELOADED_STATE__\s*=\s*(\{.*?\});', "PRELOADED_STATE"),
    (r'"products"\s*:\s*(\[.*?\])', "products array"),
    (r'data-product-info="([^"]+)"', "data-product-info attrs"),
    (r'"barCode"\s*:\s*"(\d+)"', "barCode fields"),
    (r'"productName"\s*:\s*"([^"]+)"', "productName fields"),
    (r'product-item.*?data-product-id="([^"]+)"', "product-item with id"),
]

for pattern, label in patterns:
    matches = re.findall(pattern, html, re.DOTALL)
    print(f"{label}: {len(matches)} matches")
    if matches:
        print(f"  first: {str(matches[0])[:100]}")

# Check for product cards in HTML
card_counts = {
    '<li class="productForCategory': html.count('<li class="productForCategory'),
    'data-product': html.count('data-product'),
    'ga-item-id': html.count('ga-item-id'),
    'productName': html.count('productName'),
    'barCode': html.count('barCode'),
    'מחיר': html.count('מחיר'),
}
print("\nHTML content signals:")
for k, v in card_counts.items():
    print(f"  {k!r}: {v}")

# Save HTML for inspection
with open("_shufersal_search.html", "w", encoding="utf-8") as f:
    f.write(html)
print(f"\nSaved HTML ({len(html)} chars) to _shufersal_search.html")
