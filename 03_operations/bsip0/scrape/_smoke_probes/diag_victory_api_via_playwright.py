"""
TASK-518 diag -- Cloudflare blocks plain `requests` (403 "Just a moment...") even
for the homepage. Try calling the same v2/retailers REST API via `fetch()`
EXECUTED INSIDE a real Playwright browser page (same TLS fingerprint + cookies
Cloudflare already cleared for the page load) -- this is untried hypothesis (b)
from the TASK-518 brief (real-browser XHR replay), applied to the multiretailer
JSON API discovered in multiretailer_olive_oil/01_scrape_carrefour_victory.py
rather than a HAR capture of the Angular UI's own calls.
"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright

OUT_DIR = Path(__file__).resolve().parent / "outputs"

BASE_FILTERS = json.dumps({
    "must": {
        "exists": ["family.id", "family.categoriesPaths.id", "branch.regularPrice"],
        "term": {"branch.isActive": True, "branch.isVisible": True},
    },
    "mustNot": {"term": {"branch.regularPrice": 0}},
})

RETAILERS = [
    {"name": "victory", "host": "www.victoryonline.co.il", "retailer_id": 1470, "branch_id": 2930},
    {"name": "carrefour", "host": "www.carrefour.co.il", "retailer_id": 1540, "branch_id": 3003},
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for r in RETAILERS:
        print(f"\n===== {r['name']} =====")
        context = browser.new_context(
            viewport={"width": 1500, "height": 1000}, locale="he-IL",
            timezone_id="Asia/Jerusalem", extra_http_headers={"Accept-Language": "he-IL,he;q=0.9"},
            permissions=[],
        )
        page = context.new_page()
        home = f"https://{r['host']}/"
        try:
            resp = page.goto(home, wait_until="domcontentloaded", timeout=45000)
            print("home status:", resp.status if resp else None)
            page.wait_for_timeout(4000)
        except Exception as e:
            print("home goto failed:", str(e)[:200])
            context.close()
            continue

        import urllib.parse
        params = urllib.parse.urlencode({
            "appId": "4", "filters": BASE_FILTERS, "from": "0",
            "isSearch": "true", "languageId": "1", "query": "חמאה", "size": "5",
        })
        api_url = f"https://{r['host']}/v2/retailers/{r['retailer_id']}/branches/{r['branch_id']}/products?{params}"
        result = page.evaluate("""
            async (url) => {
                try {
                    const res = await fetch(url, {headers: {'Accept': 'application/json'}});
                    const status = res.status;
                    const text = await res.text();
                    return {status, text: text.slice(0, 200000)};
                } catch (e) {
                    return {error: String(e)};
                }
            }
        """, api_url)
        print("fetch status:", result.get("status"), "error:", result.get("error"))
        if result.get("text"):
            try:
                parsed = json.loads(result["text"])
                print("total:", parsed.get("total"), "fetched:", len(parsed.get("products", [])))
                if parsed.get("products"):
                    p0 = parsed["products"][0]
                    print("TOP KEYS:", list(p0.keys()))
                    dat = p0.get("data", {})
                    print("data KEYS:", list(dat.keys()) if isinstance(dat, dict) else dat)
                    inner = (dat or {}).get("1", {})
                    print("data.1 KEYS:", list(inner.keys()) if isinstance(inner, dict) else inner)
                (OUT_DIR / f"api_sample_playwright_{r['name']}.json").write_text(
                    json.dumps(parsed, ensure_ascii=False, indent=2), encoding="utf-8"
                )
            except Exception as e:
                print("json parse failed:", str(e)[:200], "raw sample:", result["text"][:300])
        context.close()
    browser.close()
