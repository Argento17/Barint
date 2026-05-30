import requests, json, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

h = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36",
    "Accept-Language": "he-IL,he;q=0.9",
    "Accept": "application/json, */*",
}

print("=== /api/products/search ===")
r = requests.get("https://www.shufersal.co.il/api/products/search?q=%D7%9C%D7%97%D7%9D&pageSize=5", headers=h, timeout=20)
print(f"Status: {r.status_code}  CT: {r.headers.get('content-type', '')}")
try:
    data = r.json()
    print(f"Type: {type(data).__name__}")
    if isinstance(data, dict):
        print(f"Keys: {list(data.keys())[:12]}")
        for k in ["products", "items", "results", "data", "hits"]:
            if k in data:
                items = data[k]
                print(f"  '{k}': {len(items)} items")
                if items:
                    p = items[0]
                    print(f"  first item keys: {list(p.keys())[:15]}")
                    print(f"  name: {p.get('name', p.get('title', ''))}")
                    print(f"  has nutrition: {'nutritionFacts' in p or 'nutrition' in p}")
                    print(f"  has ingredients: {'ingredients' in p}")
    elif isinstance(data, list):
        print(f"List len: {len(data)}")
        if data:
            p = data[0]
            print(f"First keys: {list(p.keys())[:15]}")
            print(f"name: {p.get('name', p.get('title', ''))}")
except Exception as e:
    print(f"Not JSON: {e}")
    print(r.text[:500])

print("\n=== /online/he/search?format=json ===")
r2 = requests.get("https://www.shufersal.co.il/online/he/search?q=%D7%9C%D7%97%D7%9D&format=json&pageSize=3", headers=h, timeout=20)
print(f"Status: {r2.status_code}  CT: {r2.headers.get('content-type', '')}")
try:
    data2 = r2.json()
    print(f"Type: {type(data2).__name__}")
    if isinstance(data2, dict):
        print(f"Keys: {list(data2.keys())[:12]}")
        for k in ["products", "results", "pagination", "data"]:
            if k in data2:
                v = data2[k]
                if isinstance(v, list):
                    print(f"  '{k}': {len(v)} items")
                    if v:
                        p = v[0]
                        print(f"  first keys: {list(p.keys())[:15]}")
                        print(f"  name: {p.get('name', p.get('label', ''))}")
                elif isinstance(v, dict):
                    print(f"  '{k}': dict with keys {list(v.keys())[:8]}")
    elif isinstance(data2, list):
        print(f"List len: {len(data2)}")
except Exception as e:
    print(f"Not JSON: {e}")
    print(r2.text[:500])
