"""Does opening a FRESH page (new_page()) per product fix the 'only the first
openPopups direct-nav works' problem seen in the butter smoke run?"""
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright
from urllib.parse import quote as _q

BASE_URL = "https://yochananof.co.il"
QUERY = "חמאה"
BARCODES = ["7290116932033", "7290014758544", "7290015039130"]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        viewport={"width": 1500, "height": 1000}, locale="he-IL",
        timezone_id="Asia/Jerusalem", extra_http_headers={"Accept-Language": "he-IL,he;q=0.9"},
        permissions=[],
    )
    for bc in BARCODES:
        page = context.new_page()
        url = f"{BASE_URL}/category?search={_q(QUERY)}&openPopups=product-{bc}%3B%3Ar0%3A"
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(4000)
        for text in ["אישור", "מסכים", "קבל", "הבנתי", "Accept"]:
            try:
                btn = page.get_by_text(text, exact=False).first
                if btn.is_visible(timeout=400):
                    btn.click(force=True)
                    page.wait_for_timeout(500)
            except Exception:
                pass
        dc = page.locator('[role="dialog"]').count()
        print(bc, "dialog_count (fresh page):", dc)
        page.close()
    context.close()
    browser.close()
