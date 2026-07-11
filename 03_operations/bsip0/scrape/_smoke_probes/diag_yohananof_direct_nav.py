"""Does a FRESH page.goto() straight to the openPopups=product-<barcode> URL open
the modal directly (skipping scroll-to-find)? Test with a known butter barcode."""
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright
from urllib.parse import quote as _q

BASE_URL = "https://yochananof.co.il"
QUERY = "יוגורט"
BARCODE = "7290110578053"  # known from earlier diag (Danone yogurt)

url = f"{BASE_URL}/category?search={_q(QUERY)}&openPopups=product-{BARCODE}%3B%3Ar0%3A"
print("Navigating directly to:", url)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        viewport={"width": 1500, "height": 1000}, locale="he-IL",
        timezone_id="Asia/Jerusalem", extra_http_headers={"Accept-Language": "he-IL,he;q=0.9"},
        permissions=[],
    )
    page = context.new_page()
    page.goto(url, wait_until="domcontentloaded", timeout=45000)
    page.wait_for_timeout(6000)
    for text in ["אישור", "מסכים", "קבל", "הבנתי", "Accept"]:
        try:
            btn = page.get_by_text(text, exact=False).first
            if btn.is_visible(timeout=400):
                btn.click(force=True)
                page.wait_for_timeout(500)
        except Exception:
            pass
    dialog_count = page.locator('[role="dialog"]').count()
    print("dialog_count:", dialog_count)
    if dialog_count > 0:
        txt = page.locator('[role="dialog"]').first.inner_text(timeout=3000)
        print("dialog text sample:", txt[:300])
    context.close()
    browser.close()
