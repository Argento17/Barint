"""
Extract products from Shufersal search HTML.
Products are in <li class="SEARCH tileBlock..."> with data-product-* attributes.
"""
import requests, re, sys, json
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

h = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36",
    "Accept-Language": "he-IL,he;q=0.9",
    "Accept": "text/html,*/*",
}

QUERIES = ["לחם", "קרקר", "כוסמין", "שיפון", "פיתה"]
BASE = "https://www.shufersal.co.il"


def fetch_search(query: str) -> list[dict]:
    url = f"{BASE}/online/he/search?q={requests.utils.quote(query)}&pageSize=48"
    r = requests.get(url, headers=h, timeout=20)
    if r.status_code != 200:
        print(f"  HTTP {r.status_code} for {query}")
        return []
    soup = BeautifulSoup(r.text, "html.parser")
    items = soup.find_all("li", attrs={"data-product-name": True})
    print(f"  '{query}' → {len(items)} product li elements")
    products = []
    for li in items:
        d = li.attrs
        name = d.get("data-product-name", "").strip()
        if not name:
            continue
        code = d.get("data-product-code", "")
        price = d.get("data-product-price", "")
        is_food = d.get("data-food", "false").lower() == "true"
        cats = d.get("data-all-categories", "")
        url_path = li.find("a", href=True)
        product_url = BASE + url_path["href"] if url_path else f"{BASE}/online/he/p/{code}"
        img = li.find("img")
        img_url = img.get("src", "") if img else ""
        products.append({
            "name": name,
            "code": code,
            "price": price,
            "is_food": is_food,
            "categories": cats,
            "url": product_url,
            "img": img_url,
        })
    return products


all_products = {}
for q in QUERIES:
    results = fetch_search(q)
    for p in results:
        code = p["code"]
        if code and code not in all_products:
            all_products[code] = p

print(f"\nTotal unique products: {len(all_products)}")

# Show sample
for code, p in list(all_products.items())[:10]:
    print(f"  {p['name']} | {code} | {p['price']}₪ | food={p['is_food']}")

# Save
with open("_shufersal_products_raw.json", "w", encoding="utf-8") as f:
    json.dump(list(all_products.values()), f, ensure_ascii=False, indent=2)
print(f"\nSaved {len(all_products)} products to _shufersal_products_raw.json")

# Now fetch a product page to see if nutrition/ingredients are available
if all_products:
    sample = list(all_products.values())[0]
    print(f"\n=== Product page probe: {sample['name']} ===")
    print(f"URL: {sample['url']}")
    r = requests.get(sample["url"], headers=h, timeout=20)
    print(f"Status: {r.status_code}  Size: {len(r.content)}B")
    soup2 = BeautifulSoup(r.text, "html.parser")

    # Look for nutrition table
    nutr_signals = ["nutritionFact", "nutrition-fact", "ערך תזונתי", "קלוריות", "חלבון", "פחמימות"]
    for sig in nutr_signals:
        count = r.text.count(sig)
        if count:
            idx = r.text.find(sig)
            print(f"  '{sig}' ({count}x): ...{r.text[max(0,idx-50):idx+100]}...")

    # Look for ingredients
    ingr_signals = ["רכיבים", "מרכיבים", "ingredients"]
    for sig in ingr_signals:
        count = r.text.count(sig)
        if count:
            idx = r.text.find(sig)
            print(f"  '{sig}' ({count}x): ...{r.text[max(0,idx-50):idx+200]}...")
