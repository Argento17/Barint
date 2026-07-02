import json, subprocess, glob, os
from pathlib import Path

files = [
    "bari-web/src/data/comparisons/cheese_frontend_v4.json",
    "bari-web/src/data/comparisons/cakes_hard_cookies_frontend_v1.json",
    "bari-web/src/data/comparisons/cookies_coffee_frontend_v2.json",
    "bari-web/src/data/comparisons/bread_frontend_v3.json",
    "bari-web/src/data/comparisons/hummus_frontend_v5.json",
    "bari-web/src/data/comparisons/juices_frontend_v3.json",
    "bari-web/src/data/comparisons/hard_cheeses_frontend_v2.json",
]
for f in files:
    try:
        raw = subprocess.check_output(["git","show",f"origin/master:{f}"])
        d = json.loads(raw)
        products = d.get("products", d if isinstance(d,list) else [])
        if isinstance(d, dict) and "products" not in d and "totalProducts" in d:
            products = d["products"]
        n = len(products)
        has = sum(1 for p in products if p.get("brand"))
        hidden = sum(1 for p in products if p.get("brand") and p["brand"].lower() in (p.get("name") or "").lower())
        print(f"{Path(f).name}: {n} products | brand set: {has} | brand hidden in title: {hidden} | no brand: {n-has}")
    except Exception as e:
        print(f, e)
