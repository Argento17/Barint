"""Fetch a Shufersal product page and extract nutrition + ingredients."""
import requests, sys, json, re
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

h = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36",
    "Accept-Language": "he-IL,he;q=0.9",
    "Accept": "text/html,*/*",
}
BASE = "https://www.shufersal.co.il"

# Use lowercase p/ redirect pattern
r = requests.get(f"{BASE}/online/he/p/p_6451934", headers=h, timeout=20, allow_redirects=True)
print(f"Status: {r.status_code}  Size: {len(r.content)}B")
print(f"Final URL: {r.url}")

soup = BeautifulSoup(r.text, "html.parser")

# 1. Look for nutrition section
nutr_section = soup.find(class_=re.compile(r"nutrition|nut[rR]ition|nutritionTab", re.I))
if nutr_section:
    print("\n=== Nutrition section ===")
    print(nutr_section.get_text(separator="|", strip=True)[:500])

# Look for any table with nutrition-like content
for table in soup.find_all("table"):
    text = table.get_text(separator=" ", strip=True)
    if any(kw in text for kw in ["קלוריות", "חלבון", "פחמימות", "kcal", "energy"]):
        print("\n=== Nutrition table ===")
        print(text[:600])
        break

# 2. Look for ingredients by Hebrew label
for tag in soup.find_all(string=re.compile(r"רכיב|מרכיב")):
    parent = tag.parent
    # Get next sibling text
    sib = parent.find_next_sibling()
    text = (sib.get_text(strip=True) if sib else "") or parent.get_text(strip=True)
    if len(text) > 20:
        print(f"\n=== Ingredients candidate ===")
        print(text[:400])
        break

# 3. Look for JSON-LD or data-component JSON
for script in soup.find_all("script", type="application/ld+json"):
    try:
        data = json.loads(script.string)
        print(f"\n=== JSON-LD: @type={data.get('@type','')} ===")
        print(json.dumps(data, ensure_ascii=False, indent=2)[:800])
    except Exception:
        pass

# 4. Grab all text containing nutritional keywords in context
html = r.text
for kw in ["100 גרם", "ל-100", "kcal", "קלוריה"]:
    idx = html.find(kw)
    if idx >= 0:
        print(f"\n=== Context around '{kw}' ===")
        print(html[max(0, idx-200):idx+400])
        break

# 5. Check for productData JSON object in page
pd_match = re.search(r'productData\s*[=:]\s*(\{[^;]{100,}?\})\s*[;,]', html, re.DOTALL)
if pd_match:
    print("\n=== productData object ===")
    print(pd_match.group(1)[:600])
