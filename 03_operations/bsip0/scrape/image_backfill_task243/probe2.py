"""Probe 2: decode _next/image proxy URLs to get real api.yochananof.co.il paths."""
import sys, re, urllib.parse
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

TEST = [
    ("7290110324872", "hard cheese 1"),
    ("7290000057088", "hard cheese 2"),
    ("7290116537351", "cereal IL"),
    ("7290004122348", "hard cheese 3"),
    ("7290000057118", "hard cheese 4"),
]

JS = """() => Array.from(document.querySelectorAll('img'))
    .map(i => ({src: i.currentSrc || i.src || '', alt: i.alt || ''}))
    .filter(o => o.src.includes('_next') || o.src.includes('catalog') || o.src.includes('api.yochananof'))
"""

def decode(src):
    if "_next/image" in src:
        qs = urllib.parse.parse_qs(urllib.parse.urlparse(src).query)
        inner = qs.get("url", [None])[0]
        if inner:
            return urllib.parse.unquote(inner)
    return src


def close_popup(page):
    for text in ["אישור", "מסכים", "מאשר", "קבל", "הבנתי", "Accept", "OK", "סגור"]:
        try:
            btn = page.get_by_text(text, exact=False).first
            if btn.is_visible(timeout=500):
                btn.click(force=True)
                page.wait_for_timeout(400)
                return
        except Exception:
            pass


def main():
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1400, "height": 1000}, user_agent=UA)
        for ean, label in TEST:
            page.goto(f"https://yochananof.co.il/category?search={ean}",
                      wait_until="domcontentloaded", timeout=45000)
            page.wait_for_timeout(3000)
            close_popup(page)
            page.mouse.wheel(0, 800)
            page.wait_for_timeout(800)
            imgs = page.evaluate(JS)
            print(f"\n{ean} ({label}): {len(imgs)} imgs")
            for img in imgs[:5]:
                real = decode(img["src"])
                fname = real.split("/")[-1].split("?")[0]
                ean_in_fname = ean in fname
                print(f"  decoded: {real}")
                print(f"  fname: {fname} | EAN_in_fname={ean_in_fname} | alt={img['alt'][:40]}")
        browser.close()


if __name__ == "__main__":
    main()
