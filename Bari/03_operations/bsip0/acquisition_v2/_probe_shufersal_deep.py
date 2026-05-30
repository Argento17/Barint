"""Deep inspection of Shufersal search HTML - find product data."""
import requests, json, re, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

h = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36",
    "Accept-Language": "he-IL,he;q=0.9",
    "Accept": "text/html,*/*",
}

with open("_shufersal_search.html", encoding="utf-8") as f:
    html = f.read()

# Show areas around 'data-product' and 'מחיר'
dp_idx = html.find('data-product')
if dp_idx >= 0:
    print("=== Around first 'data-product' ===")
    print(html[max(0, dp_idx-200):dp_idx+400])

price_idx = html.find('מחיר')
if price_idx >= 0:
    print("\n=== Around first 'מחיר' ===")
    print(html[max(0, price_idx-300):price_idx+300])

# Look for JSON blobs
json_scripts = re.findall(r'<script[^>]*type=["\']application/json["\'][^>]*>(.*?)</script>', html, re.DOTALL)
print(f"\nJSON script blocks: {len(json_scripts)}")
for i, blob in enumerate(json_scripts[:3]):
    print(f"  [{i}] {len(blob)}B: {blob[:100]}")

# Look for large inline JSON
inline_json = re.findall(r'=\s*(\{[^;]{200,}\})\s*;', html, re.DOTALL)
print(f"\nLarge inline JSON assignments: {len(inline_json)}")
for blob in inline_json[:3]:
    print(f"  {len(blob)}B: {blob[:120]}")

# Look for product-related HTML tags
for tag in ['<div class="product', '<article', 'class="item', 'class="product']:
    count = html.count(tag)
    if count:
        idx = html.find(tag)
        print(f"\n'{tag}' ({count}x): {html[idx:idx+200]}")
