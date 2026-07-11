"""Check GetItemGS1Details/<id> -- likely carries GS1 nutrition/ingredients data."""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent / "outputs" / "hazi_hinam_gs1_6049.json"

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
            const res = await fetch('https://shop.hazi-hinam.co.il/proxy/api/item/GetItemGS1Details/6049', {headers: {'Accept':'application/json'}});
            return {status: res.status, text: await res.text()};
        }
    """)
    print("status:", result["status"])
    OUT.write_text(result["text"], encoding="utf-8")
    try:
        data = json.loads(result["text"])
        print(json.dumps(data, ensure_ascii=False, indent=2)[:3000])
    except Exception as e:
        print("parse fail:", e, result["text"][:500])
    context.close()
    browser.close()
