"""Debug laibcatalog page structure to find Victory PriceFull files."""
import sys, re, requests, html
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

LAIBCATALOG_PORTAL = "https://laibcatalog.co.il/"
r = requests.get(LAIBCATALOG_PORTAL, timeout=15)
page = r.text

# The original client looks for href=".*.gz" patterns
# Let's check different link formats
print("=== Searching for file links ===", flush=True)

# Check for all href patterns
all_hrefs = re.findall(r'href=["\']([^"\']*)["\']', page)
gz_hrefs = [h for h in all_hrefs if '.gz' in h.lower()]
print(f"GZ hrefs: {len(gz_hrefs)}", flush=True)
for h in gz_hrefs[:10]:
    print(f"  {h}", flush=True)

# Check for data- attributes or JS patterns
js_matches = re.findall(r'["\']([^"\']*PriceFull[^"\']*)["\']', page, re.I)
print(f"\nPriceFull references: {len(js_matches)}", flush=True)
for m in js_matches[:10]:
    print(f"  {m}", flush=True)

# Check for Victory chain ID context
victory_id = "7290696200003"
idx = page.find(victory_id)
while idx != -1:
    snippet = page[max(0, idx-100):idx+200]
    if ".gz" in snippet or "Price" in snippet:
        print(f"\nVictory context with file ref:\n  {snippet[:300]}", flush=True)
        break
    idx = page.find(victory_id, idx + 1)

# Check for any URL-like patterns with the chain ID
url_patterns = re.findall(r'https?://[^\s"\'<>]*' + re.escape(victory_id) + r'[^\s"\'<>]*', page)
print(f"\nURLs with Victory chain ID: {len(url_patterns)}", flush=True)
for u in url_patterns[:5]:
    print(f"  {u}", flush=True)

# Show a sample of the first 3000 chars to understand structure
print("\n=== First 3000 chars of page ===", flush=True)
print(page[:3000], flush=True)
