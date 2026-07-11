"""Inspect the /proxy/api/item/<id> JSON response directly -- does it carry
structured nutrition + ingredients, letting us skip DOM scraping entirely?"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent / "outputs" / "hazi_hinam_item_6049.json"

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
            const res = await fetch('https://shop.hazi-hinam.co.il/proxy/api/item/6049', {headers: {'Accept':'application/json'}});
            const status = res.status;
            const text = await res.text();
            return {status, text};
        }
    """)
    print("status:", result["status"])
    try:
        data = json.loads(result["text"])
        print("TOP KEYS:", list(data.keys()) if isinstance(data, dict) else type(data))
        OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        print("saved to", OUT)
    except Exception as e:
        print("not JSON or parse failed:", str(e)[:200])
        print(result["text"][:500])

    context.close()
    browser.close()
