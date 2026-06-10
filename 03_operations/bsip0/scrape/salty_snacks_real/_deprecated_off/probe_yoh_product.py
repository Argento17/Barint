"""Probe a Yochananof product page to discover URL pattern + nutrition/ingredient DOM."""
import sys, re, json, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright

EAN = "7290000066318"  # Bamba classic 80g — known to exist

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
    # search then click first product to learn product URL
    pg.goto(f"https://yochananof.co.il/category?search={EAN}", wait_until="networkidle", timeout=60000)
    pg.wait_for_timeout(2500)
    close_popup(pg)
    # collect anchors that look like product links
    links = pg.evaluate("""() => Array.from(document.querySelectorAll('a'))
        .map(a => a.href).filter(h => h && (h.includes('/product') || h.includes('/p/') || /\\/\\d{6,}/.test(h)))""")
    print("PRODUCT-LIKE LINKS:", json.dumps(links[:10], ensure_ascii=False))
    if links:
        purl = links[0]
        pg.goto(purl, wait_until="networkidle", timeout=60000)
        pg.wait_for_timeout(2500)
        close_popup(pg)
        body = pg.inner_text("body")
        # find nutrition + ingredient regions
        for kw in ["רכיב", "ערכים תזונתי", "אנרגיה", "נתרן", "חלבון"]:
            idx = body.find(kw)
            print(f"\n=== context around '{kw}' (idx {idx}) ===")
            if idx >= 0:
                print(body[max(0,idx-40):idx+400].replace("\n"," | "))
        pathlib.Path(__file__).parent.joinpath("probe_body.txt").write_text(body, encoding="utf-8")
        print("\nFINAL URL:", pg.url)
    br.close()
