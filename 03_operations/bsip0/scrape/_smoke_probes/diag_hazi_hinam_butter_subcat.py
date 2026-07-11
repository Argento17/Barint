import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent / "outputs" / "hazi_hinam_subcat_10868_butter.json"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        viewport={"width": 1500, "height": 1000}, locale="he-IL",
        timezone_id="Asia/Jerusalem", extra_http_headers={"Accept-Language": "he-IL,he;q=0.9"},
        permissions=[],
    )
    page = context.new_page()
    page.goto("https://shop.hazi-hinam.co.il/", wait_until="domcontentloaded", timeout=30000)
    page.wait_for_timeout(3000)
    result = page.evaluate("""
        async () => {
            const res = await fetch('https://shop.hazi-hinam.co.il/proxy/api/item/getItemsBySubCategory?Id=10868&IsDescending=false&SortBy=-1', {headers: {'Accept':'application/json'}});
            return {status: res.status, text: await res.text()};
        }
    """)
    print("status:", result["status"])
    OUT.write_text(result["text"], encoding="utf-8")
    data = json.loads(result["text"])
    sc = data["Results"]["Category"]["SubCategory"]
    items = sc["Items"]
    print("subcat name:", sc["Name"], "num items:", len(items))
    for it in items:
        print(" ", it.get("Id"), it.get("BarKod"), it.get("Name"))
    context.close()
    browser.close()
