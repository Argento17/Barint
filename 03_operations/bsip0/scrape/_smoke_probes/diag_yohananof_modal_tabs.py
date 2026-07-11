"""
TASK-518 diag #6 -- inspect the Yohananof product modal's tab structure (role=tab
labels) so we can build a reusable Playwright panel-scrape (ingredients + nutrition)
analogous to victory's capture_tab(). Dumps the modal's tab labels + raw HTML.
"""
from __future__ import annotations
import json
import sys
from pathlib import Path
from urllib.parse import quote as _q

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright

OUT_DIR = Path(__file__).resolve().parent / "outputs"
BASE_URL = "https://yochananof.co.il"
QUERY = "יוגורט"

findings = {}

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        viewport={"width": 1500, "height": 1000}, locale="he-IL",
        timezone_id="Asia/Jerusalem", extra_http_headers={"Accept-Language": "he-IL,he;q=0.9"},
        permissions=[],
    )
    page = context.new_page()
    url = f"{BASE_URL}/category?search={_q(QUERY)}"
    page.goto(url, wait_until="domcontentloaded", timeout=45000)
    page.wait_for_timeout(6000)
    for text in ["אישור", "מסכים", "קבל", "הבנתי", "Accept"]:
        try:
            btn = page.get_by_text(text, exact=False).first
            if btn.is_visible(timeout=400):
                btn.click(force=True)
                page.wait_for_timeout(500)
        except Exception:
            pass

    img = page.locator('img[src*="_next/image"]').first
    img.scroll_into_view_if_needed(timeout=5000)
    img.click(force=True, timeout=5000)
    page.wait_for_timeout(2500)

    tabs = page.locator('[role="tab"]').all()
    findings["tab_count"] = len(tabs)
    findings["tab_labels"] = []
    for t in tabs:
        try:
            findings["tab_labels"].append(t.inner_text(timeout=1000))
        except Exception as e:
            findings["tab_labels"].append(f"ERR:{e}")

    dialog = page.locator('[role="dialog"]').first
    try:
        full_html = dialog.inner_html(timeout=5000)
    except Exception as e:
        full_html = f"ERROR: {e}"
    (OUT_DIR / "yohananof_modal_full.html").write_text(full_html, encoding="utf-8")
    findings["modal_html_len"] = len(full_html)

    # try clicking each tab and capture text length change
    tab_texts = {}
    for label in findings["tab_labels"]:
        try:
            tab = page.get_by_role("tab", name=label).first
            tab.click(force=True, timeout=3000)
            page.wait_for_timeout(1500)
            txt = page.locator('[role="dialog"]').first.inner_text(timeout=3000)
            tab_texts[label] = txt[:400]
        except Exception as e:
            tab_texts[label] = f"ERROR: {e}"
    findings["tab_texts_sample"] = tab_texts

    context.close()
    browser.close()

(OUT_DIR / "diag_yohananof_modal_tabs.json").write_text(
    json.dumps(findings, ensure_ascii=False, indent=2), encoding="utf-8"
)
print(json.dumps(findings, ensure_ascii=False, indent=2)[:3000])
