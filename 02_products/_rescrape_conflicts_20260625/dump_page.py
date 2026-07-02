"""Dump page HTML to file for pattern inspection."""
import sys, os, urllib.request, urllib.error, re
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "he-IL,he;q=0.9,en-US;q=0.8",
}

URL = "https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%95%D7%A8%D7%99%D7%95%D7%AA/%D7%A1%D7%95%D7%A4%D7%A8%D7%9E%D7%A8%D7%A7%D7%98/%D7%9E%D7%95%D7%A6%D7%A8%D7%99-%D7%97%D7%9C%D7%91-%D7%95%D7%91%D7%99%D7%A6%D7%99%D7%9D/%D7%92%D7%91%D7%99%D7%A0%D7%95%D7%AA-%D7%9E%D7%A2%D7%93%D7%A0%D7%99%D7%99%D7%94/%D7%92%D7%91%D7%99%D7%A0%D7%95%D7%AA-%D7%91%D7%A7%D7%A8-%D7%95%D7%A6%D7%90%D7%9F-%D7%9E%D7%99%D7%95%D7%97%D7%93%D7%95%D7%AA/%D7%92%D7%91%D7%99%D7%A0%D7%AA-%D7%A2%D7%96%D7%99%D7%9D-32%25-%D7%A9%D7%95%D7%9E%D7%9F/p/P_7290108506624"

req = urllib.request.Request(URL, headers=HEADERS)
with urllib.request.urlopen(req, timeout=20) as resp:
    html = resp.read().decode("utf-8", errors="replace")

STAGING = os.path.dirname(os.path.abspath(__file__))
out_path = os.path.join(STAGING, "dump_cheese_page.html")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(html)
print(f"Dumped {len(html)} bytes to {out_path}")

# Search for ingredients-related patterns
patterns_to_check = [
    "מרכיבים",
    "רכיבים",
    "כבשים",
    "עזים",
    "ingredient",
    "Ingredient",
    "description",
    "Details",
    "productDetails",
    "itemDescription",
    "specification",
    "specificationList",
    "description_he",
]
print("\n--- Pattern scan ---")
for pat in patterns_to_check:
    idx = html.find(pat)
    if idx >= 0:
        snippet = html[max(0,idx-50):idx+200].replace('\n', ' ')
        print(f"FOUND '{pat}' at {idx}: ...{snippet[:250]}...")
    else:
        print(f"NOT FOUND: '{pat}'")

# Also look for JSON-LD
import json
jsonld_matches = re.findall(r'<script[^>]+type="application/ld\+json"[^>]*>(.*?)</script>', html, re.DOTALL)
print(f"\n--- JSON-LD blocks: {len(jsonld_matches)} ---")
for i, block in enumerate(jsonld_matches):
    try:
        data = json.loads(block)
        print(f"Block {i}: {json.dumps(data, ensure_ascii=False)[:500]}")
    except:
        print(f"Block {i} (raw): {block[:300]}")
