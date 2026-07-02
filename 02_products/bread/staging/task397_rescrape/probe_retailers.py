"""Probe Victory and Rami Levy API endpoints to find working product search URLs."""
from __future__ import annotations
import json
import sys
import urllib.error
import urllib.request

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

# Test barcode: Osem sesame crackers (74252) — a well-known Israeli product
# Also try 7290016245325 (tahini bread)
TEST_BARCODES = ["74252", "7290016245325", "7290016967074"]


def http_get(url: str, headers: dict = None, timeout: int = 20) -> tuple[bytes | None, dict]:
    hdrs = {
        "User-Agent": UA,
        "Accept": "*/*",
        "Accept-Language": "he-IL,he;q=0.9,en;q=0.7",
    }
    if headers:
        hdrs.update(headers)
    req = urllib.request.Request(url, headers=hdrs)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read(), {
                "status": r.status,
                "content_type": r.headers.get("Content-Type", ""),
                "final_url": r.geturl(),
            }
    except urllib.error.HTTPError as e:
        return None, {"status": e.code, "error": str(e)}
    except Exception as e:
        return None, {"status": 0, "error": str(e)}


def probe(label: str, url: str, extra_headers: dict = None):
    data, info = http_get(url, headers=extra_headers)
    if data:
        snippet = data[:600].decode("utf-8", errors="replace")
        print(f"  [{label}] {url}")
        print(f"    status={info.get('status')} ct={info.get('content_type','')[:60]} bytes={len(data)}")
        print(f"    snippet: {snippet[:400]}")
    else:
        print(f"  [{label}] {url}")
        print(f"    FAILED: {info}")
    print()


print("=== RAMI LEVY API PROBES ===\n")

bc = "74252"
# Probe various Rami Levy endpoints
probe("RL-catalog-v1",
    f"https://www.rami-levy.co.il/api/catalog/v1/products?q={bc}",
    {"Referer": "https://www.rami-levy.co.il/", "X-Requested-With": "XMLHttpRequest",
     "Accept": "application/json"})

probe("RL-catalog-search",
    f"https://www.rami-levy.co.il/api/catalog/search?q={bc}&page=1",
    {"Referer": "https://www.rami-levy.co.il/", "Accept": "application/json"})

probe("RL-product-id",
    f"https://www.rami-levy.co.il/api/catalog/v1/products/{bc}",
    {"Referer": "https://www.rami-levy.co.il/", "Accept": "application/json"})

probe("RL-product-barcode",
    f"https://www.rami-levy.co.il/api/catalog/v1/products?barcode={bc}",
    {"Referer": "https://www.rami-levy.co.il/", "Accept": "application/json"})

probe("RL-search-html",
    f"https://www.rami-levy.co.il/he/search?q={bc}",
    {"Referer": "https://www.rami-levy.co.il/", "Accept": "text/html"})

print("\n=== VICTORY API PROBES ===\n")

probe("V-search",
    f"https://www.victory.co.il/api/v2/products/search?q={bc}",
    {"Referer": "https://www.victory.co.il/", "Accept": "application/json"})

probe("V-catalog-search",
    f"https://www.victory.co.il/umbraco/surface/catalog/search?q={bc}",
    {"Referer": "https://www.victory.co.il/", "Accept": "application/json",
     "X-Requested-With": "XMLHttpRequest"})

probe("V-catalog-barcode",
    f"https://www.victory.co.il/umbraco/surface/catalog/search?barcode={bc}",
    {"Referer": "https://www.victory.co.il/", "Accept": "application/json"})

probe("V-product-page-html",
    f"https://www.victory.co.il/search?q={bc}",
    {"Referer": "https://www.victory.co.il/", "Accept": "text/html"})

probe("V-umbraco-product",
    f"https://www.victory.co.il/umbraco/api/product/getbybarcode?barcode={bc}",
    {"Referer": "https://www.victory.co.il/", "Accept": "application/json",
     "X-Requested-With": "XMLHttpRequest"})

probe("V-api-product",
    f"https://www.victory.co.il/api/products/{bc}",
    {"Referer": "https://www.victory.co.il/", "Accept": "application/json"})

print("\n=== Done ===")
