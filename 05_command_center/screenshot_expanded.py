#!/usr/bin/env python3
"""Screenshot with the completed-tasks section expanded (verifies PART B)."""
import sys
from playwright.sync_api import sync_playwright

url, out = sys.argv[1], sys.argv[2]
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1280, "height": 1400}, device_scale_factor=2)
    page.goto(url, wait_until="networkidle")
    page.wait_for_timeout(500)
    btn = page.query_selector("#togComplete")
    if btn:
        btn.click()
        page.wait_for_timeout(400)
    page.screenshot(path=out, full_page=True)
    browser.close()
print("saved", out)
