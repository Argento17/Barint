"""
TASK-518 diag -- test the shared REST API discovered in
multiretailer_olive_oil/01_scrape_carrefour_victory.py
(`https://<host>/v2/retailers/<rid>/branches/<bid>/products?...`) for BOTH
Victory and Carrefour, querying "חמאה" (butter), to see the FULL product JSON
shape -- specifically whether it carries a nutrition panel (not just
ingredients text), which would let us bypass Playwright/Angular UI entirely
for both retailers.
"""
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

OUT_DIR = Path(__file__).resolve().parent / "outputs"

RETAILERS = [
    {"name": "victory", "host": "www.victoryonline.co.il", "retailer_id": 1470, "branch_id": 2930},
    {"name": "carrefour", "host": "www.carrefour.co.il", "retailer_id": 1540, "branch_id": 3003},
]

BASE_FILTERS = json.dumps({
    "must": {
        "exists": ["family.id", "family.categoriesPaths.id", "branch.regularPrice"],
        "term": {"branch.isActive": True, "branch.isVisible": True},
    },
    "mustNot": {"term": {"branch.regularPrice": 0}},
})


def fetch_page(host, rid, bid, query, offset=0, size=10):
    params = urllib.parse.urlencode({
        "appId": "4", "filters": BASE_FILTERS, "from": str(offset),
        "isSearch": "true", "languageId": "1", "query": query, "size": str(size),
    })
    url = f"https://{host}/v2/retailers/{rid}/branches/{bid}/products?{params}"
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124",
        "Accept": "application/json",
        "Referer": f"https://{host}/",
    })
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read())


for r in RETAILERS:
    print(f"\n===== {r['name']} =====")
    try:
        data = fetch_page(r["host"], r["retailer_id"], r["branch_id"], "חמאה", size=5)
        print("total:", data.get("total"))
        products = data.get("products", [])
        print("fetched:", len(products))
        if products:
            p0 = products[0]
            print("TOP-LEVEL KEYS:", list(p0.keys()))
            data_field = p0.get("data", {})
            print("data KEYS:", list(data_field.keys()) if isinstance(data_field, dict) else type(data_field))
            inner = (data_field or {}).get("1", {})
            print("data.1 KEYS:", list(inner.keys()) if isinstance(inner, dict) else type(inner))
            (OUT_DIR / f"api_sample_{r['name']}.json").write_text(
                json.dumps(p0, ensure_ascii=False, indent=2), encoding="utf-8"
            )
    except Exception as e:
        print("ERROR:", str(e)[:300])
