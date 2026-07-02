"""
Search Victory data.js for target products.
The 6.9MB file contains all product data baked for Victory store #1470.
"""
import sys, re, json, requests
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

print("Downloading data.js (6.9MB)...", flush=True)
r = requests.get(
    "https://htmlcache.blob.core.windows.net/html-production-env/r-1470/desktop/multi-true/data.js?c=1782126421251",
    timeout=120
)
text = r.text
print(f"Downloaded: {len(text)} chars", flush=True)

# Our target productIds
TARGET_PIDS = [415280, 7872576, 7872575, 7872574, 6181, 324953, 817732, 7630501]

# Search for each
print("\n=== Searching data.js for target productIds ===", flush=True)
for pid in TARGET_PIDS:
    pid_str = str(pid)
    count = text.count(pid_str)
    if count > 0:
        idx = text.find(pid_str)
        # Get context
        ctx = text[max(0,idx-300):idx+500]
        # Check if this is a productId in context
        if re.search(r'"productId".*?' + re.escape(pid_str), ctx) or re.search(re.escape(pid_str) + r'.*?"productId"', ctx):
            print(f"\nPID {pid} found {count}x — looks like productId context", flush=True)
            print(f"  {ctx[:400]}", flush=True)
        else:
            print(f"PID {pid} found {count}x — context: {ctx[:200]}", flush=True)
    else:
        print(f"PID {pid}: NOT in data.js", flush=True)

# Also check barcodes
BARCODES = ["4820005195848", "3046920023443", "3046920023429", "3046920023368"]
print("\n=== Checking barcodes in data.js ===", flush=True)
for bc in BARCODES:
    count = text.count(bc)
    if count > 0:
        idx = text.find(bc)
        ctx = text[max(0,idx-200):idx+400]
        print(f"\nBarcode {bc} found {count}x:", flush=True)
        print(f"  {ctx[:300]}", flush=True)
    else:
        print(f"Barcode {bc}: NOT in data.js", flush=True)

# Check for "nutritionValues" in data.js
nutr_count = text.count("nutritionValues")
print(f"\n'nutritionValues' appears {nutr_count}x in data.js", flush=True)
if nutr_count > 0:
    idx = text.find("nutritionValues")
    print(f"First context: {text[max(0,idx-100):idx+400]}", flush=True)
