"""
TASK-518 diag #5 -- can we reach an individual Yohananof product page directly
(SSR HTML, via plain requests, no Playwright) once we know its barcode/sku? If so,
per-product scraping could skip the fragile modal-click approach entirely.
Uses Playwright only to discover one product's real URL by clicking a card, then
tests whether that same URL is fetchable+parseable via plain `requests`.
"""
from __future__ import annotations
import json
import sys
from pathlib import Path
from urllib.parse import quote as _q

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright
import requests

OUT = Path(__file__).resolve().parent / "outputs" / "diag_yohananof_product_url.json"
BASE_URL = "https://yochananof.co.il"
QUERY = "יוגורט"

findings = {}

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

    # find first product image, click its ancestor card/link, see what happens (new URL? modal?)
    img = page.locator('img[src*="_next/image"]').first
    img.scroll_into_view_if_needed(timeout=5000)
    before_url = page.url
    try:
        # try clicking the image itself
        img.click(force=True, timeout=5000)
        page.wait_for_timeout(2500)
    except Exception as e:
        findings["click_error"] = str(e)[:200]
    after_url = page.url
    findings["before_url"] = before_url
    findings["after_url"] = after_url
    findings["url_changed"] = before_url != after_url

    # check if a dialog/modal appeared instead
    dialog_count = page.locator('[role="dialog"]').count()
    findings["dialog_count_after_click"] = dialog_count
    if dialog_count > 0:
        try:
            findings["dialog_html_snippet"] = page.locator('[role="dialog"]').first.inner_html(timeout=3000)[:800]
        except Exception as e:
            findings["dialog_html_error"] = str(e)[:200]

    context.close()
    browser.close()

# If URL changed to a real product page, test requests-fetchability
if findings.get("url_changed"):
    try:
        r = requests.get(findings["after_url"], timeout=15, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36",
            "Accept-Language": "he-IL,he;q=0.9",
        })
        findings["requests_status"] = r.status_code
        findings["requests_body_len"] = len(r.text)
        findings["requests_has_hebrew_ingredients_marker"] = ("רכיב" in r.text)
        findings["requests_has_nutrition_marker"] = ("ערכים תזונתיים" in r.text) or ("קלוריות" in r.text)
    except Exception as e:
        findings["requests_error"] = str(e)[:300]

OUT.write_text(json.dumps(findings, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(findings, ensure_ascii=False, indent=2)[:2500])
