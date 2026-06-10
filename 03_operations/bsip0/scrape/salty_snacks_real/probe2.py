"""Probe Yochananof: find product page URL from a name search and inspect its DOM for
nutrition + ingredients."""
import sys, re, json, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright

def close_popup(page):
    for t in ["אישור", "מסכים", "מאשר", "קבל", "הבנתי", "Accept", "OK"]:
        try:
            b = page.get_by_text(t, exact=False).first
            if b.is_visible(timeout=600):
                b.click(force=True); page.wait_for_timeout(400); return
        except Exception:
            pass

with sync_playwright() as pw:
    br = pw.chromium.launch(headless=True)
    pg = br.new_page(viewport={"width": 1400, "height": 1100})
    pg.goto("https://yochananof.co.il/category?search=במבה", wait_until="networkidle", timeout=60000)
    pg.wait_for_timeout(3000)
    close_popup(pg)
    # all anchor hrefs
    hrefs = pg.evaluate("() => Array.from(document.querySelectorAll('a')).map(a=>a.href).filter(Boolean)")
    uniq = sorted(set(h for h in hrefs if "yochananof" in h))
    print("SAMPLE HREFS:")
    for h in uniq[:25]:
        print("  ", h)
    # try clicking first product card image
    try:
        card = pg.query_selector("a:has(img)")
        if card:
            href = card.get_attribute("href")
            print("FIRST CARD HREF:", href)
    except Exception as e:
        print("card err", e)
    br.close()
