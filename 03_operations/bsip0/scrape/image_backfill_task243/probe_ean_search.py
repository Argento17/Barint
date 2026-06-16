"""Probe: what does Yochananof return for EAN searches? Show raw image URLs."""
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

TEST_EANS = [
    ("7290116537351", "hard cereal IL"),
    ("7290110324872", "hard cheese IL"),
    ("7290000057088", "hard cheese IL 2"),
    ("7290004122348", "hard cheese IL 3"),
    ("7290120871069", "granola IL"),
]


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


def probe(page, ean, label):
    print(f"\n=== {ean} ({label}) ===")
    page.goto(f"https://yochananof.co.il/category?search={ean}",
              wait_until="domcontentloaded", timeout=45000)
    page.wait_for_timeout(3000)
    close_popup(page)
    page.mouse.wheel(0, 800)
    page.wait_for_timeout(1000)

    # all images
    all_imgs = page.evaluate("""() =>
        Array.from(document.querySelectorAll('img'))
             .map(i => ({src: i.currentSrc || i.src || '', alt: i.alt || ''}))
    """)

    catalog_imgs = [i for i in all_imgs if "catalog" in i["src"] or "api.yochananof" in i["src"]]
    print(f"  Total imgs: {len(all_imgs)}, catalog imgs: {len(catalog_imgs)}")
    for img in catalog_imgs[:8]:
        print(f"  CATALOG: {img['src'][:120]}")
        if img['alt']:
            print(f"           alt={img['alt'][:60]}")

    # also check page title and text to see if product found
    title_text = page.title()
    print(f"  Page title: {title_text[:80]}")

    # check product cards
    cards = page.evaluate("""() =>
        Array.from(document.querySelectorAll('[class*="product"], [class*="item"], [class*="card"]'))
             .slice(0, 5)
             .map(el => el.innerText.slice(0, 80).replace(/\\n/g, ' '))
    """)
    print(f"  Cards ({len(cards)}): {cards[:3]}")


def main():
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1400, "height": 1000}, user_agent=UA)
        for ean, label in TEST_EANS:
            probe(page, ean, label)
        browser.close()


if __name__ == "__main__":
    main()
