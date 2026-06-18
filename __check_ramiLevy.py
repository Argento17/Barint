import sys
import re
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright
import time

# Try Rami Levy for the missing products
BASE_URL = "https://www.rami-levy.co.il"

test_barcodes = [
    ("2511229", "בולגרית מעודנת 16%"),
    ("4861056", "גבינה צפתית 5%"),
    ("5992872", "גבינה צפתית במים 5%"),
    ("4861070", "גבינה צפתית קשה 24%"),
    ("7296073644996", "גבינה צפתית קשה 24% מגורד"),
    ("7296073730330", "פטינה בסגנון פטה 22%"),
    ("8606370", "פטינה גבינה סגנון פטה 22%"),
]

with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=True)
    ctx = browser.new_context(
        viewport={"width": 1500, "height": 1000},
        locale="he-IL",
        timezone_id="Asia/Jerusalem",
        extra_http_headers={"Accept-Language": "he-IL,he;q=0.9"},
    )
    page = ctx.new_page()
    
    for barcode, name in test_barcodes:
        search_url = f"{BASE_URL}/he/search?q={barcode}"
        try:
            page.goto(search_url, wait_until="domcontentloaded", timeout=25000)
            page.wait_for_timeout(4000)
            html = page.content()
            
            # Check for product results
            text = page.inner_text("body")[:500]
            barcode_in = barcode in html
            
            # Look for product card indicators
            has_product = any(x in html for x in [f'"{barcode}"', f'sku={barcode}', f'barcode={barcode}'])
            
            # Check for actual product count
            count_match = re.search(r'(\d+)\s+(?:מוצרים|תוצאות|results)', html)
            count = count_match.group(1) if count_match else "unknown"
            
            print(f"{barcode} ({name[:20]}): barcode_in={barcode_in}, has_product={has_product}, count={count}")
            print(f"  text_preview: {text[:150]}")
        except Exception as e:
            print(f"{barcode}: ERROR {type(e).__name__}: {str(e)[:60]}")
        
        time.sleep(2)
    
    browser.close()
