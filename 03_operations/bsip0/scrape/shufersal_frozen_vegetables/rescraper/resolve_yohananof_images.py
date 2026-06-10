"""
Barcode-VERIFIED image resolution for the salty-snacks corpus via Yochananof.

Yochananof product image URLs embed the real EAN barcode (e.g.
`.../cache/<hash>/7/2/7290011498870_s1_...jpg`). So unlike Shufersal (internal codes,
name-only matching → wrong images), Yochananof lets us match the corpus barcode EXACTLY:
we harvest snack-shelf cards, then keep only images whose URL CONTAINS one of our 54
corpus barcodes. No fuzzy name matching, no wrong-variant risk.

Output: resolved_yohananof.json  ->  { barcode: image_url }
"""
import sys, json, re, pathlib, urllib.parse as up
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).parent
CORPUS = pathlib.Path(r"C:\Bari\bari-web\src\data\comparisons\salty_snacks_frontend_v3.json")
OUT = HERE / "resolved_yohananof.json"

QUERIES = [
    "חטיפים מלוחים", "במבה", "ביסלי", "פרינגלס", "דוריטוס", "תפוצ'יפס",
    "צ'יפס", "חטיף", "פופקורן", "בייגלה", "קרקרים", "נאצ'וס", "אפרופו",
    "חטיף עדשים", "חטיף אורז", "פצפוצי אורז", "פיתות", "ביסקוטי",
    "חטיף תירס", "מתאבנים", "גלעינון", "טייסטי",
]


def _decode(u: str) -> str:
    # Yochananof wraps images in Next.js `/_next/image?url=<encoded api url>`.
    m = re.search(r"[?&]url=([^&]+)", u)
    return up.unquote(m.group(1)) if m else u


def harvest(page):
    raw = page.evaluate(
        """() => {
            const out = [];
            for (const img of Array.from(document.querySelectorAll('img'))) {
                const u = (img.currentSrc || img.src || '');
                if (u) out.push(u);
            }
            return out;
        }"""
    )
    return [_decode(u) for u in raw]


def close_popup(page):
    for t in ["אישור", "מסכים", "מאשר", "קבל", "הבנתי", "Accept", "OK"]:
        try:
            b = page.get_by_text(t, exact=False).first
            if b.is_visible(timeout=600):
                b.click(force=True); page.wait_for_timeout(500); return
        except Exception:
            pass


def biggest(url_blob: str, barcode: str) -> str:
    """Pick the single URL token that contains the barcode (prefer the largest cache size)."""
    toks = [t for t in re.split(r"\s+", url_blob) if barcode in t and t.startswith("http")]
    toks = [t.split("?")[0].rstrip(",") for t in toks]
    if not toks:
        return ""
    # Prefer non-thumbnail (no '/cache/.../50x' style tiny) — just take the longest URL.
    return max(toks, key=len)


def main():
    barcodes = [str(p.get("barcode") or "").strip()
                for p in json.loads(CORPUS.read_text(encoding="utf-8"))["products"]]
    barcodes = [b for b in barcodes if b]
    bcset = set(barcodes)
    resolved = {}

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1500, "height": 1000})
        for q in QUERIES:
            if len(resolved) == len(bcset):
                break
            url = f"https://yochananof.co.il/category?search={q}"
            try:
                page.goto(url, wait_until="networkidle", timeout=60000)
            except Exception as e:
                print(f"  goto fail {q}: {e}"); continue
            page.wait_for_timeout(2500)
            close_popup(page)
            stable = last = 0
            for _ in range(60):
                blob = " ".join(harvest(page))
                newhit = 0
                for b in bcset - resolved.keys():
                    if b in blob:
                        u = biggest(blob, b)
                        if u:
                            resolved[b] = u; newhit += 1
                if len(resolved) == last:
                    stable += 1
                else:
                    stable = 0; last = len(resolved)
                if stable >= 10:
                    break
                page.mouse.wheel(0, 1100)
                page.wait_for_timeout(700)
            print(f"  [{q}] resolved so far: {len(resolved)}/{len(bcset)}")
        browser.close()

    OUT.write_text(json.dumps(resolved, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nBarcode-verified images: {len(resolved)}/{len(bcset)} -> {OUT}")
    for b, u in resolved.items():
        print(f"  {b}  {u[:90]}")


if __name__ == "__main__":
    main()
