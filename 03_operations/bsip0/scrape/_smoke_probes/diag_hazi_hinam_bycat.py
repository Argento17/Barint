import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent / "outputs" / "hazi_hinam_bycat_78.json"

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
            const res = await fetch('https://shop.hazi-hinam.co.il/proxy/api/Item/GetItemsByCategory/?Id=78', {headers: {'Accept':'application/json'}});
            return {status: res.status, text: await res.text()};
        }
    """)
    print("status:", result["status"])
    OUT.write_text(result["text"], encoding="utf-8")
    try:
        data = json.loads(result["text"])
        print("TOP KEYS:", list(data.keys()))
        res = data.get("Results")
        print("Results type:", type(res))
        if isinstance(res, list):
            print("num items:", len(res))
            butter = [it for it in res if "חמאה" in (it.get("Name") or "")]
            print("butter-name matches:", len(butter))
            for b in butter[:25]:
                print(" ", b.get("Id"), b.get("BarKod"), b.get("Name"))
        elif isinstance(res, dict):
            print("Results keys:", list(res.keys()))
    except Exception as e:
        print("parse fail:", e, result["text"][:400])
    context.close()
    browser.close()
