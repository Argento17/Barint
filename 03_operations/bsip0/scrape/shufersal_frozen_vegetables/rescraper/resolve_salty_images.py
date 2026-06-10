"""
Resolve REAL product images for the salty-snacks corpus from the Shufersal storefront.

Root cause this fixes: the salty-snacks BSIP0 scrape stubbed image URLs as
`https://images.{retailer}.co.il/{barcode}.jpg` (hosts that do not resolve). Every
other comparison category uses real Shufersal Cloudinary URLs.

Matching key: NAME, not barcode. Shufersal's catalog uses internal codes (e.g. Bamba =
66295), so the corpus EANs cannot be reconciled against it. We instead search each product
by name, score candidates by Hebrew token overlap, take the best match above a threshold,
open its product page, and extract the real Cloudinary image. Every chosen URL is verified
to return HTTP 200, and the matched Shufersal name is recorded so the mapping is auditable.

Output: resolved_images.json  ->  { barcode: {url, matched_name, score, corpus_name} }
"""
import sys, json, re, time, pathlib, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

import requests
from bs4 import BeautifulSoup

HERE = pathlib.Path(__file__).parent
CORPUS = pathlib.Path(r"C:\Bari\bari-web\src\data\comparisons\salty_snacks_frontend_v3.json")
OUT = HERE / "resolved_images.json"

SEARCH = "https://www.shufersal.co.il/online/he/search"
PRODUCT = "https://www.shufersal.co.il/online/he/p/{}"

session = requests.Session()
session.headers.update({
    "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                   "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"),
    "Accept-Language": "he-IL,he;q=0.9,en-US;q=0.7",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
})

# Words that don't help identity matching: retailer names, generic/packaging tokens.
STOP = {
    "קרפור", "יוחננוף", "שופרסל", "מארז", "מבצע", "גרם", "יח", "אריזה",
    "ללא", "עם", "טעם", "ענק", "חדש",
}


def norm(s: str) -> str:
    s = re.sub(r"\(.*?\)", " ", s or "")
    s = re.sub(r'["״׳\',.]', " ", s)
    return s


def tokens(s: str) -> set:
    return {w for w in re.split(r"\s+", norm(s).strip()) if len(w) >= 2 and w not in STOP}


def search_terms(name: str):
    toks = [w for w in re.split(r"\s+", norm(name).strip()) if w and w not in STOP]
    out, seen = [], set()
    for t in (" ".join(toks[:2]), toks[0] if toks else "", " ".join(toks[:3])):
        t = t.strip()
        if t and t not in seen:
            seen.add(t); out.append(t)
    return out


def candidates(query: str):
    """[(name, code)] from a search query."""
    try:
        r = session.get(SEARCH, params={"q": query, "pageSize": 48}, timeout=20)
        if r.status_code != 200:
            return []
    except Exception:
        return []
    soup = BeautifulSoup(r.text, "lxml")
    out = []
    for li in soup.find_all("li", attrs={"data-product-name": True}):
        nm = li.attrs.get("data-product-name")
        code = li.attrs.get("data-product-code")
        if nm and code:
            out.append((nm, code))
    return out


def detail_image(code: str):
    """Largest real Cloudinary product image from a Shufersal product page."""
    try:
        r = session.get(PRODUCT.format(code), timeout=20)
        if r.status_code != 200:
            return None
    except Exception:
        return None
    urls = re.findall(
        r"https://res\.cloudinary\.com/shufersal/[^\"'\\)\s]+/product_images/[^\"'\\)\s]+\.png",
        r.text,
    )
    if not urls:
        return None
    for pref in ("products_zoom", "products_large", "products_medium"):
        for u in urls:
            if pref in u:
                return u
    return urls[0]


def url_ok(u: str) -> bool:
    try:
        return session.get(u, timeout=15, stream=True).status_code == 200
    except Exception:
        return False


def main():
    products = json.loads(CORPUS.read_text(encoding="utf-8"))["products"]
    resolved = {}
    THRESHOLD = 0.5  # min Jaccard-ish overlap of corpus tokens covered by the match

    for i, p in enumerate(products, 1):
        bc = str(p.get("barcode") or "").strip()
        name = p.get("name") or ""
        ctoks = tokens(name)
        if not bc or not ctoks:
            print(f"  [{i}/{len(products)}] SKIP {name[:40]}")
            continue

        seen_codes, best = set(), None
        for term in search_terms(name):
            for nm, code in candidates(term):
                if code in seen_codes:
                    continue
                seen_codes.add(code)
                mtoks = tokens(nm)
                if not mtoks:
                    continue
                covered = len(ctoks & mtoks) / len(ctoks)
                if best is None or covered > best[0]:
                    best = (covered, nm, code)
            time.sleep(0.3)
            if best and best[0] >= 0.99:
                break

        if best and best[0] >= THRESHOLD:
            img = detail_image(best[2])
            if img and url_ok(img):
                resolved[bc] = {
                    "url": img, "matched_name": best[1],
                    "score": round(best[0], 2), "corpus_name": name,
                }
                print(f"  [{i}/{len(products)}] OK  ({best[0]:.2f}) {name[:32]}  ->  {best[1][:32]}")
                time.sleep(0.3)
                continue
        sc = f"{best[0]:.2f}/{best[1][:24]}" if best else "none"
        print(f"  [{i}/{len(products)}] MISS {name[:32]}  (best {sc})")

    OUT.write_text(json.dumps(resolved, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nResolved {len(resolved)}/{len(products)} -> {OUT}")


if __name__ == "__main__":
    main()
