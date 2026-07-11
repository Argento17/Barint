"""Explore getItemsBySubCategory -- confirm it lists full items with id+barcode+name
for a given subcategory, and find the butter subcategory id under dairy (cat 78)."""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright

OUT_DIR = Path(__file__).resolve().parent / "outputs"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        viewport={"width": 1500, "height": 1000}, locale="he-IL",
        timezone_id="Asia/Jerusalem", extra_http_headers={"Accept-Language": "he-IL,he;q=0.9"},
        permissions=[],
    )
    page = context.new_page()
    page.goto("https://shop.hazi-hinam.co.il/catalog/78/%D7%9E%D7%95%D7%A6%D7%A8%D7%99-%D7%97%D7%9C%D7%91-%D7%95%D7%91%D7%99%D7%A6%D7%99%D7%9D",
               wait_until="domcontentloaded", timeout=30000)
    page.wait_for_timeout(5000)

    # Find the subcategory nav (likely a side-menu of subcategories with ids)
    subcats = page.evaluate("""
        () => Array.from(document.querySelectorAll('a[href*="SubCategory"], a[href*="subcategory"], [class*="subcategory"] a, [class*="sub-cat"] a'))
            .map(a => ({href: a.href, text: a.innerText.trim()})).filter(x => x.text)
    """)
    print("subcat-like links found:", len(subcats))
    for s in subcats[:30]:
        print(" ", s)

    # Fetch items for the subcategory id seen in the earlier XHR (11211) as a sample
    result = page.evaluate("""
        async () => {
            const res = await fetch('https://shop.hazi-hinam.co.il/proxy/api/item/getItemsBySubCategory?Id=11211&IsDescending=false&SortBy=-1', {headers: {'Accept':'application/json'}});
            return {status: res.status, text: await res.text()};
        }
    """)
    print("\nsubcategory 11211 fetch status:", result["status"])
    try:
        data = json.loads(result["text"])
        print("TOP KEYS:", list(data.keys()))
        results = data.get("Results", {})
        print("Results type:", type(results), list(results.keys()) if isinstance(results, dict) else len(results))
        (OUT_DIR / "hazi_hinam_subcat_11211.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception as e:
        print("parse fail:", e, result["text"][:400])

    context.close()
    browser.close()
