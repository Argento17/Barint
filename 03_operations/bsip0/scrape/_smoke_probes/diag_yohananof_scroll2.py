"""
TASK-518 diagnostic follow-up — confirm root cause: does page.mouse.wheel() at the
DEFAULT pointer position (0,0), with NO prior page.mouse.move(), actually scroll the
MUI virtualized <main> container? This is exactly what the production
browse_yohananof_candidates() loop does (no mouse.move before mouse.wheel).
Compare against explicit mouse.move into the container first.
"""
from __future__ import annotations
import json
import sys
from pathlib import Path
from urllib.parse import quote as _q

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent / "outputs" / "diag_yohananof_scroll2.json"
BASE_URL = "https://yochananof.co.il"
QUERY = "יוגורט"  # yogurt - the actual shelf that plateaus at 8

findings = {}

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        viewport={"width": 1500, "height": 1000},
        locale="he-IL",
        timezone_id="Asia/Jerusalem",
        extra_http_headers={"Accept-Language": "he-IL,he;q=0.9"},
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

    findings["mouse_pos_default_no_move"] = {}
    seen = set()
    counts = []
    for i in range(10):
        imgs = page.locator('img[src*="_next/image"]').all()
        for img in imgs:
            src = img.get_attribute("src") or ""
            seen.add(src)
        counts.append(len(seen))
        page.mouse.wheel(0, 1400)  # NO mouse.move first -- mirrors production bug
        page.wait_for_timeout(1200)
    findings["mouse_pos_default_no_move"]["cumulative_unique_seen"] = counts
    scrollTop_noMove = page.evaluate("""
        () => { const m = document.querySelector('main'); return m ? m.scrollTop : null; }
    """)
    findings["mouse_pos_default_no_move"]["final_main_scrollTop"] = scrollTop_noMove

    # reload fresh and repeat WITH explicit mouse.move into the main container first
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
    page.mouse.move(750, 500)  # move into the <main> bounds ONCE
    seen2 = set()
    counts2 = []
    for i in range(10):
        imgs = page.locator('img[src*="_next/image"]').all()
        for img in imgs:
            src = img.get_attribute("src") or ""
            seen2.add(src)
        counts2.append(len(seen2))
        page.mouse.wheel(0, 1400)
        page.wait_for_timeout(1200)
    findings["mouse_moved_into_main_first"] = {"cumulative_unique_seen": counts2}
    scrollTop_move = page.evaluate("""
        () => { const m = document.querySelector('main'); return m ? m.scrollTop : null; }
    """)
    findings["mouse_moved_into_main_first"]["final_main_scrollTop"] = scrollTop_move

    context.close()
    browser.close()

OUT.write_text(json.dumps(findings, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(findings, ensure_ascii=False, indent=2))
