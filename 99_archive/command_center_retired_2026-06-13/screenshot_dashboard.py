#!/usr/bin/env python3
"""Capture a full-page screenshot of the command center for before/after docs.
Usage: python screenshot_dashboard.py <url> <output_png>
"""
import sys
from playwright.sync_api import sync_playwright

url = sys.argv[1]
out = sys.argv[2]

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1280, "height": 1400},
                            device_scale_factor=2)
    page.goto(url, wait_until="networkidle")
    page.wait_for_timeout(700)
    page.screenshot(path=out, full_page=True)
    browser.close()
print("saved", out)
