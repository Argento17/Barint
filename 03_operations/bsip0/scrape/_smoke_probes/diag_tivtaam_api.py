"""Tiv Taam runs the SAME v2/retailers/<rid>/branches/<bid>/products JSON API as
Victory/Carrefour (retailer_id=1062, branch_id=924, confirmed via live XHR capture
in diag_tivtaam_interact.py) but on its OWN domain (www.tivtaam.co.il) -- and that
domain is NOT behind the self-point.com WAF that hard-blocked Victory/Carrefour
this session (proven: real page load + real XHRs succeeded above, no 403/challenge).
Query this API directly for "חמאה" (butter) and inspect the full product JSON shape
-- specifically whether `data.<n>` carries a nutrition table, not just ingredients."""
import json
import sys
import urllib.parse
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent / "outputs" / "tivtaam_api_sample.json"

BASE_FILTERS = json.dumps({
    "must": {
        "exists": ["family.id", "family.categoriesPaths.id", "branch.regularPrice"],
        "term": {"branch.isActive": True, "branch.isVisible": True},
    },
    "mustNot": {"term": {"branch.regularPrice": 0}},
})

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        viewport={"width": 1500, "height": 1000}, locale="he-IL",
        timezone_id="Asia/Jerusalem", extra_http_headers={"Accept-Language": "he-IL,he;q=0.9"},
        permissions=[],
    )
    page = context.new_page()
    page.goto("https://www.tivtaam.co.il/", wait_until="domcontentloaded", timeout=30000)
    page.wait_for_timeout(4000)

    params = urllib.parse.urlencode({
        "appId": "4", "filters": BASE_FILTERS, "from": "0",
        "isSearch": "true", "languageId": "1", "query": "חמאה", "size": "10",
    })
    api_url = f"https://www.tivtaam.co.il/v2/retailers/1062/branches/924/products?{params}"
    result = page.evaluate("""
        async (url) => {
            try {
                const res = await fetch(url, {headers: {'Accept': 'application/json'}});
                return {status: res.status, text: await res.text()};
            } catch (e) { return {error: String(e)}; }
        }
    """, api_url)
    print("status:", result.get("status"), "error:", result.get("error"))
    if result.get("text"):
        data = json.loads(result["text"])
        print("total:", data.get("total"), "fetched:", len(data.get("products", [])))
        if data.get("products"):
            p0 = data["products"][0]
            print("TOP KEYS:", list(p0.keys()))
            dat = p0.get("data", {})
            print("data KEYS:", list(dat.keys()) if isinstance(dat, dict) else dat)
            for k, v in (dat or {}).items():
                print(f"  data.{k} KEYS:", list(v.keys()) if isinstance(v, dict) else v)
        OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    context.close()
    browser.close()
