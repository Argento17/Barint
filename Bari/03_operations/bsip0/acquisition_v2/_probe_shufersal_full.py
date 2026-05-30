"""Full extraction of nutrition + ingredients from a Shufersal product page."""
import requests, sys, json, re
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

h = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36",
    "Accept-Language": "he-IL,he;q=0.9",
    "Accept": "text/html,*/*",
}
BASE = "https://www.shufersal.co.il"

r = requests.get(f"{BASE}/online/he/p/p_6451934", headers=h, timeout=20, allow_redirects=True)
soup = BeautifulSoup(r.text, "html.parser")

# JSON-LD
ld = None
for script in soup.find_all("script", type="application/ld+json"):
    try:
        ld = json.loads(script.string)
        if ld.get("@type") == "Product":
            break
    except Exception:
        pass
if ld:
    print("=== JSON-LD Product ===")
    print(f"name: {ld.get('name')}")
    print(f"sku: {ld.get('sku')}")
    print(f"gtin13: {ld.get('gtin13')}")
    print(f"images: {ld.get('image', [])[:2]}")

# Nutrition list
nutr_div = soup.find("div", class_="nutritionList")
if nutr_div:
    print("\n=== Nutrition Items ===")
    items = nutr_div.find_all("div", class_="nutritionItem")
    for item in items:
        number = item.find("div", class_="number")
        label_div = item.find("div", class_=re.compile("label|name|title"))
        # Try any div after the number
        divs = item.find_all("div")
        texts = [d.get_text(strip=True) for d in divs if d.get_text(strip=True)]
        print(f"  {texts}")
    # Also show raw text
    print("\nRaw nutrition text:", nutr_div.get_text(separator=" | ", strip=True)[:400])

# Ingredients
# Look for common patterns
for label_text in ["מרכיבים", "רכיבים", "רכיבים:"]:
    label_el = soup.find(string=re.compile(label_text))
    if label_el:
        # Get parent and its surrounding content
        parent = label_el.find_parent()
        container = parent.find_parent()
        if container:
            text = container.get_text(separator=" ", strip=True)
            print(f"\n=== Ingredients (via '{label_text}') ===")
            print(text[:600])
            break

# Broader search in all li elements of productDetails type sections
for section in soup.find_all("li"):
    text = section.get_text(separator=" ", strip=True)
    if "מרכיב" in text and len(text) > 50:
        print(f"\n=== Ingredients candidate li ===")
        print(text[:600])
        break

# Look in data attributes
for el in soup.find_all(attrs={"data-ingredients": True}):
    print(f"\n=== data-ingredients ===")
    print(el["data-ingredients"][:300])

# Check for structured product tabs
tabs = soup.find_all(class_=re.compile(r"tab|Tab"))
for tab in tabs:
    text = tab.get_text(separator=" ", strip=True)
    if any(kw in text for kw in ["מרכיב", "רכיב", "ingredients"]):
        print(f"\n=== Tab with ingredients ===")
        print(text[:400])
        break
