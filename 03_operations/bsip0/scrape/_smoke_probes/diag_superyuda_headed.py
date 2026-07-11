"""Retry Super Yuda with a real headed (non-headless) Chromium instance --
headless Chromium carries fingerprint tells (navigator.webdriver=true, missing
plugins/mimeTypes, headless UA string) that some WAFs (Akamai/Imperva-style,
not Cloudflare's auto-solving JS challenge) block outright regardless of
JS execution. The immediate '403 Forbidden / Transaction ID:' page (no
'just a moment' interstitial) suggests exactly this kind of gate."""
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright

BASE = "https://www.yuda.co.il"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, args=["--disable-blink-features=AutomationControlled"])
    context = browser.new_context(
        viewport={"width": 1500, "height": 1000}, locale="he-IL",
        timezone_id="Asia/Jerusalem", extra_http_headers={"Accept-Language": "he-IL,he;q=0.9"},
        permissions=[],
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    )
    page = context.new_page()
    try:
        resp = page.goto(BASE + "/", wait_until="domcontentloaded", timeout=45000)
        print("status:", resp.status if resp else None)
    except Exception as e:
        print("goto failed:", str(e)[:300])
    page.wait_for_timeout(5000)
    print("title:", page.title())
    print("body sample:", page.evaluate("document.body.innerText.slice(0,300)"))
    context.close()
    browser.close()
