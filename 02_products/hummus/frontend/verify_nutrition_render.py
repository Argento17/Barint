#!/usr/bin/env python3
"""Capture an expanded Hummus product row (nutrition panel, fat suppressed)."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from playwright.sync_api import sync_playwright

url, out = sys.argv[1], sys.argv[2]
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 460, "height": 950}, device_scale_factor=2)
    pg.goto(url, wait_until="networkidle")
    pg.wait_for_timeout(800)
    # a product-row toggle is an aria-expanded button that contains a product image
    row_btn = pg.query_selector("button[aria-expanded='false']:has(img)")
    if not row_btn:
        # fallback: nth aria-expanded button that is inside the list (skip nav)
        btns = pg.query_selector_all("button[aria-expanded='false']")
        row_btn = btns[1] if len(btns) > 1 else (btns[0] if btns else None)
    if row_btn:
        row_btn.scroll_into_view_if_needed()
        row_btn.click()
        pg.wait_for_timeout(700)
        row_btn.scroll_into_view_if_needed()
        pg.wait_for_timeout(300)
    pg.screenshot(path=out)
    # check the nutrition grid labels exist near an expanded row
    grid = pg.query_selector("text=נתרן")
    print("sodium cell rendered:", grid is not None)
    print("saved", out)
    b.close()
