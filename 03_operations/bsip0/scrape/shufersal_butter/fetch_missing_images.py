"""
Fetch image URLs for butter products missing images.
Tries Shufersal product pages (JSON-LD) first, then Carrefour search API.
Updates butter_frontend_v2.json in-place.

Run from C:\Bari:
  python 03_operations/bsip0/scrape/shufersal_butter/fetch_missing_images.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from time import sleep

import requests
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

FRONTEND_JSON = Path(r"C:\bari\bari-web\src\data\comparisons\butter_frontend_v2.json")

SHUFERSAL_BASE = "https://www.shufersal.co.il"
CARREFOUR_BASE = "https://www.carrefour.co.il"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "he-IL,he;q=0.9",
    "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
}

MISSING_BARCODES = [
    "7290113401022", "9414544900015", "3760088100025", "7290000066028",
    "7290006325046", "5740900400221", "8906060890143", "7290002492086",
    "3412130012558", "3228021530005", "5099460004149", "5099460004156",
    "5099460010935", "4260268321030", "9414544900022", "7290000066035",
    "5740900400238", "3412130012534", "3228021530012", "5099460004132",
]


def _get(url: str, timeout: int = 20) -> requests.Response | None:
    try:
        return requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
    except Exception as exc:
        print(f"  [GET error] {url[-60:]}: {exc}")
        return None


def _shufersal_image(barcode: str) -> str | None:
    """Try Shufersal product page for this barcode; return first image URL or None."""
    url = f"{SHUFERSAL_BASE}/online/he/p/p_{barcode}"
    r = _get(url)
    if not r or r.status_code != 200:
        return None
    soup = BeautifulSoup(r.text, "html.parser")
    # JSON-LD structured data (most reliable)
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            ld = json.loads(script.string)
            if ld.get("@type") == "Product":
                images = ld.get("image", [])
                if isinstance(images, str):
                    images = [images]
                for img in images:
                    if img:
                        return img
        except Exception:
            pass
    # Fallback: og:image meta tag
    og = soup.find("meta", property="og:image")
    if og and og.get("content"):
        return og["content"]
    # Fallback: first Cloudinary image in page
    m = re.search(r'https://res\.cloudinary\.com/shufersal/[^\s"\'<>]+\.(?:png|jpg|webp)', r.text)
    if m:
        return m.group(0)
    return None


def _carrefour_image(barcode: str) -> str | None:
    """Try Carrefour search API for this barcode; return first image URL or None."""
    # Carrefour product search by barcode
    url = f"{CARREFOUR_BASE}/search?text={barcode}&format=json"
    r = _get(url)
    if not r or r.status_code != 200:
        return None
    try:
        data = r.json()
        products = data.get("results", data.get("products", []))
        for p in products:
            # Check barcode/EAN match
            p_barcode = str(p.get("ean", p.get("barcode", p.get("id", "")))).strip()
            if p_barcode == barcode:
                images = p.get("images", p.get("media", []))
                for img in images:
                    url_val = img.get("url", img) if isinstance(img, dict) else img
                    if url_val and isinstance(url_val, str):
                        return url_val
    except Exception:
        pass
    # Fallback: scrape Carrefour search HTML for the barcode
    url2 = f"{CARREFOUR_BASE}/search?text={barcode}"
    r2 = _get(url2)
    if r2 and r2.status_code == 200:
        soup = BeautifulSoup(r2.text, "html.parser")
        # Look for product image with barcode in data attributes
        for el in soup.find_all(attrs={"data-ean": barcode}):
            img = el.find("img")
            if img and img.get("src"):
                return img["src"]
    return None


def _yochananof_image(barcode: str) -> str | None:
    """Try Yochananof search for this barcode; return first image URL or None."""
    url = f"https://yochananof.co.il/search?q={barcode}"
    r = _get(url)
    if not r or r.status_code != 200:
        return None
    soup = BeautifulSoup(r.text, "html.parser")
    for el in soup.find_all(attrs={"data-barcode": barcode}):
        img = el.find("img")
        if img and img.get("src"):
            return img["src"]
    # Look for product cards mentioning this barcode
    for el in soup.find_all("article"):
        text = el.get_text()
        if barcode in text:
            img = el.find("img")
            if img:
                return img.get("src") or img.get("data-src") or ""
    return None


def fetch_images_for_missing() -> dict[str, str]:
    """Returns {barcode: image_url} for successfully found images."""
    results: dict[str, str] = {}
    for bc in MISSING_BARCODES:
        print(f"\n{bc}:", end="  ", flush=True)
        # 1. Try Shufersal
        img = _shufersal_image(bc)
        if img:
            print(f"SHUFERSAL OK: {img[:70]}")
            results[bc] = img
            sleep(0.8)
            continue
        sleep(0.5)
        # 2. Try Carrefour
        img = _carrefour_image(bc)
        if img:
            print(f"CARREFOUR OK: {img[:70]}")
            results[bc] = img
            sleep(0.8)
            continue
        sleep(0.5)
        # 3. Try Yochananof
        img = _yochananof_image(bc)
        if img:
            print(f"YOCHANANOF OK: {img[:70]}")
            results[bc] = img
            sleep(0.8)
            continue
        sleep(0.5)
        print("NOT FOUND")
    return results


def patch_frontend_json(image_map: dict[str, str]) -> int:
    """Patch imageUrl for matched barcodes. Returns number of products updated."""
    if not image_map:
        print("\nNo images found — nothing to patch.")
        return 0
    with open(FRONTEND_JSON, encoding="utf-8") as f:
        data = json.load(f)
    updated = 0
    for p in data.get("products", []):
        bc = str(p.get("barcode", ""))
        if bc in image_map:
            p["imageUrl"] = image_map[bc]
            updated += 1
    with open(FRONTEND_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return updated


if __name__ == "__main__":
    print(f"Fetching images for {len(MISSING_BARCODES)} missing butter products...")
    image_map = fetch_images_for_missing()
    print(f"\n\nFound images for {len(image_map)}/{len(MISSING_BARCODES)} products")
    if image_map:
        for bc, url in image_map.items():
            print(f"  {bc}: {url[:80]}")
    n = patch_frontend_json(image_map)
    print(f"\nPatched {n} products in {FRONTEND_JSON}")
