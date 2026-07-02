"""
Search Victory data.js for our target products and their nutrition data.
The 6.9MB file likely contains the full product catalog with nutrition values pre-baked.
"""
from __future__ import annotations
import sys, re, requests, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

DATA_JS_URL = "https://htmlcache.blob.core.windows.net/html-production-env/r-1470/desktop/multi-true/data.js?c=1782126421251"

TARGET_BARCODES = [
    "4820005195848",  # Millennium 80%
    "3046920023443",  # Lindt Excellence dark
    "3046920023429",  # Lindt caramel milk
    "3046920023368",  # Lindt Excellence milk
    "3046920028004",  # Lindt 70%
    "4820005198597",  # Millennium 74%
    "5941021001261",  # 75% dark
    "7290119500482",  # 62% dark
]

print("Downloading data.js...", flush=True)
r = requests.get(DATA_JS_URL, timeout=60)
print(f"HTTP {r.status_code}, len={len(r.text)}", flush=True)

js_text = r.text

# Check if this is JSON data embedded in window.sp
# data.js format: window.sp = { frontendData: {...} }
# The JSON is 6.9MB so it contains a lot
# Let's check if it has nutrition data at all
has_nutrition = "nutritionValues" in js_text
has_ingredients = "ingredients" in js_text.lower()
print(f"Has nutritionValues: {has_nutrition}", flush=True)
print(f"Has ingredients: {has_ingredients}", flush=True)

# Check for our specific barcodes
for bc in TARGET_BARCODES:
    count = js_text.count(bc)
    if count > 0:
        # Find context
        idx = js_text.find(bc)
        snippet = js_text[max(0,idx-200):idx+500]
        print(f"\nBarcode {bc} found {count}x:", flush=True)
        print(f"  Context: {snippet[:400]}", flush=True)
    else:
        print(f"Barcode {bc}: NOT in data.js", flush=True)

# Look for nutritionValues pattern
if has_nutrition:
    idx = js_text.find("nutritionValues")
    snippet = js_text[max(0,idx-100):idx+500]
    print(f"\nnutritionValues context: {snippet[:500]}", flush=True)
