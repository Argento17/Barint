"""
Harvest (name, image_url) pairs from Yochananof snack shelves so corpus products can be
matched to REAL images by NAME (corpus barcodes are fabricated — see resolve_yohananof_images).

Writes yoh_named_catalog.json: [{name, url}]  — deduped by url.
A separate matcher scores corpus names against this catalog; only strong matches ship.
"""
import sys, json, re, pathlib, urllib.parse as up
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).parent
OUT = HERE / "yoh_named_catalog.json"

QUERIES = [
    "במבה", "ביסלי", "פרינגלס", "דוריטוס", "תפוצ'יפס", "אפרופו", "צ'יפס",
    "פופקורן", "בייגלה", "בייגל", "קרקרים", "נאצ'וס", "חטיף עדשים",
    "חטיף אורז", "פצפוצי אורז", "פיתות", "חטיף תירס", "טייסטי", "ביסקוטי",
    "מצנצ'ים", "דובונים", "פריכיות", "חטיף בריאות", "חטיפים",
]


def decode(u):
    m = re.search(r"[?&]url=([^&]+)", u)
    return up.unquote(m.group(1)) if m else u


def close_popup(page):
    for t in ["אישור", "מסכים", "מאשר", "קבל", "הבנתי", "Accept", "OK"]:
        try:
            b = page.get_by_text(t, exact=False).first
            if b.is_visible(timeout=600):
                b.click(force=True); page.wait_for_timeout(500); return
        except Exception:
            pass


def grab(page):
    return page.evaluate(
        """() => Array.from(document.querySelectorAll('img'))
            .map(i => ({src: i.currentSrc || i.src || '', alt: i.getAttribute('alt') || ''}))
            .filter(o => o.src.includes('catalog') || o.src.includes('url='))"""
    )


def main():
    cat = {}
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1500, "height": 1000})
        for q in QUERIES:
            try:
                page.goto(f"https://yochananof.co.il/category?search={q}",
                          wait_until="networkidle", timeout=60000)
            except Exception as e:
                print(f"  goto fail {q}: {e}"); continue
            page.wait_for_timeout(2500)
            close_popup(page)
            stable = last = 0
            for _ in range(50):
                for o in grab(page):
                    url = decode(o["src"])
                    alt = (o["alt"] or "").strip()
                    if "catalog" in url and alt and url not in cat:
                        cat[url] = alt
                if len(cat) == last:
                    stable += 1
                else:
                    stable = 0; last = len(cat)
                if stable >= 8:
                    break
                page.mouse.wheel(0, 1100); page.wait_for_timeout(650)
            print(f"  [{q}] catalog size: {len(cat)}")
        browser.close()

    rows = [{"name": v, "url": k} for k, v in cat.items()]
    OUT.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nHarvested {len(rows)} named images -> {OUT}")


if __name__ == "__main__":
    main()
