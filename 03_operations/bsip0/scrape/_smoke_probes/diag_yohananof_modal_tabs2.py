"""Capture dialog HTML AFTER clicking the nutrition tab (lazy-mounted rows) and
re-verify the shared parser extracts real values."""
from __future__ import annotations
import sys
from pathlib import Path
from urllib.parse import quote as _q

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright

OUT_DIR = Path(__file__).resolve().parent / "outputs"
BASE_URL = "https://yochananof.co.il"
QUERY = "יוגורט"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        viewport={"width": 1500, "height": 1000}, locale="he-IL",
        timezone_id="Asia/Jerusalem", extra_http_headers={"Accept-Language": "he-IL,he;q=0.9"},
        permissions=[],
    )
    page = context.new_page()
    url = f"{BASE_URL}/category?search={_q(QUERY)}"
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

    img = page.locator('img[src*="_next/image"]').first
    img.scroll_into_view_if_needed(timeout=5000)
    img.click(force=True, timeout=5000)
    page.wait_for_timeout(2500)

    tab = page.get_by_role("tab", name="ערכים תזונתיים").first
    tab.click(force=True, timeout=3000)
    page.wait_for_timeout(1800)

    dialog = page.locator('[role="dialog"]').first
    html = dialog.inner_html(timeout=5000)
    (OUT_DIR / "yohananof_modal_after_nutrition_click.html").write_text(html, encoding="utf-8")
    print("saved, len=", len(html))
    context.close()
    browser.close()
