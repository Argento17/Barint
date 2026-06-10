"""Probe Yochananof product modal for nutrition + ingredients (TASK-237)."""
import sys, json, pathlib, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright

EAN = sys.argv[1] if len(sys.argv) > 1 else "7290000066318"

def close_popup(page):
    for t in ["אישור", "מסכים", "מאשר", "קבל", "הבנתי", "Accept", "OK", "סגור"]:
        try:
            b = page.get_by_text(t, exact=False).first
            if b.is_visible(timeout=500):
                b.click(force=True); page.wait_for_timeout(400); return
        except Exception:
            pass

with sync_playwright() as pw:
    br = pw.chromium.launch(headless=True)
    pg = br.new_page(viewport={"width": 1400, "height": 1100},
                     user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36")
    pg.goto(f"https://yochananof.co.il/category?search={EAN}", wait_until="domcontentloaded", timeout=60000)
    try:
        pg.wait_for_selector('img[src*="catalog/product"]', timeout=20000)
    except Exception as e:
        print("no product img selector:", str(e)[:80])
    pg.wait_for_timeout(2500)
    close_popup(pg)
    # click the first product card (image with EAN in src, or first product tile)
    clicked = False
    for sel in [f'img[src*="{EAN}"]', 'img[src*="catalog/product"]', '[class*="product"] a', 'main a']:
        try:
            loc = pg.locator(sel).first
            if loc.count() > 0:
                loc.scroll_into_view_if_needed(timeout=4000)
                pg.wait_for_timeout(400)
                loc.click(force=True)
                pg.wait_for_timeout(4000)
                clicked = True
                print("clicked via", sel)
                break
        except Exception as e:
            print("sel fail", sel, str(e)[:60])
    print("URL after click:", pg.url)
    # look for tabs
    tabs = pg.evaluate("""() => Array.from(document.querySelectorAll('[role=tab],button,a'))
        .map(e=>e.innerText).filter(x=>x && (x.includes('רכיב')||x.includes('תזונת')||x.includes('אלרג')))""")
    print("TAB-LIKE:", json.dumps(tabs[:10], ensure_ascii=False))
    # try clicking each ingredient/nutrition tab and dump
    for label in ["רכיבים", "ערכים תזונתיים"]:
        try:
            tab = pg.get_by_role("tab", name=label).first
            if tab.count() > 0:
                tab.click(force=True); pg.wait_for_timeout(1500)
                print(f"clicked tab {label}")
        except Exception as e:
            print("tab fail", label, str(e)[:60])
    body = pg.inner_text("body")
    for kw in ["רכיב", "אנרגיה", "נתרן", "חלבון", "שומן", "פחמימ"]:
        i = body.find(kw)
        print(f"--- '{kw}' @ {i}:", body[max(0,i-20):i+200].replace("\n"," | ") if i>=0 else "NONE")
    # dump dialog html if any
    try:
        dlg = pg.locator('[role=dialog]').first
        if dlg.count() > 0:
            pathlib.Path(__file__).parent.joinpath("probe_dialog.html").write_text(dlg.inner_html(), encoding="utf-8")
            print("dialog html saved")
    except Exception as e:
        print("dialog err", str(e)[:60])
    pathlib.Path(__file__).parent.joinpath("probe_body_v2.txt").write_text(body, encoding="utf-8")
    br.close()
