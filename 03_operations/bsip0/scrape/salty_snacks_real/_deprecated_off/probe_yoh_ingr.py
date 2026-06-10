"""Confirm ingredients tab capture for Yochananof modal."""
import sys, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

EAN = sys.argv[1] if len(sys.argv) > 1 else "7290000066318"

def close_popup(page):
    for t in ["אישור","מסכים","מאשר","קבל","הבנתי","Accept","OK","סגור"]:
        try:
            b = page.get_by_text(t, exact=False).first
            if b.is_visible(timeout=500):
                b.click(force=True); page.wait_for_timeout(300); return
        except Exception:
            pass

with sync_playwright() as pw:
    br = pw.chromium.launch(headless=True)
    pg = br.new_page(viewport={"width":1400,"height":1100},
                     user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36")
    # direct modal URL
    pg.goto(f"https://yochananof.co.il/category?search={EAN}&openPopups=product-{EAN}", wait_until="domcontentloaded", timeout=60000)
    try:
        pg.wait_for_selector('[role=dialog]', timeout=25000)
    except Exception as e:
        print("no dialog via direct url:", str(e)[:80])
    pg.wait_for_timeout(2500)
    close_popup(pg)
    for label in ["רכיבים","ערכים תזונתיים","מידע אלרגני"]:
        try:
            tab = pg.get_by_role("tab", name=label).first
            if tab.count() > 0:
                tab.click(force=True); pg.wait_for_timeout(1800)
                dlg = pg.locator('[role=dialog]').first
                html = dlg.inner_html()
                s = BeautifulSoup(html,"lxml")
                txt = " ".join(p.get_text(' ',strip=True) for p in s.select('#simple-tabpanel-0,#simple-tabpanel-1,#simple-tabpanel-2') if p.get_text(strip=True))
                print(f"=== TAB {label} ===")
                print(repr(txt)[:500])
        except Exception as e:
            print("tab fail", label, str(e)[:80])
    br.close()
