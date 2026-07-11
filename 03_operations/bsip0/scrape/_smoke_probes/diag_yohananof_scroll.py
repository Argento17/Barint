"""
TASK-518 diagnostic — why does Yohananof candidate-discovery plateau at ~8 items
when a manual reload of the same URL surfaces ~22? Inspect DOM structure: is the
product grid virtualized inside an inner overflow container (independent of the
window/body scroll), which `page.mouse.wheel` over the body would never reach?

Read-only diagnostic. Writes findings to _smoke_probes/outputs/diag_yohananof_scroll.json
"""
from __future__ import annotations
import json
import sys
from pathlib import Path
from urllib.parse import quote as _q

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent / "outputs" / "diag_yohananof_scroll.json"
BASE_URL = "https://yochananof.co.il"
QUERY = "חמאה"  # butter - small well-understood shelf

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
    print(f"goto {url}")
    page.goto(url, wait_until="domcontentloaded", timeout=45000)
    page.wait_for_timeout(6000)

    # dismiss cookie popup
    for text in ["אישור", "מסכים", "קבל", "הבנתי", "Accept"]:
        try:
            btn = page.get_by_text(text, exact=False).first
            if btn.is_visible(timeout=400):
                btn.click(force=True)
                page.wait_for_timeout(500)
        except Exception:
            pass

    imgs0 = page.locator('img[src*="_next/image"]').all()
    findings["initial_img_count"] = len(imgs0)

    # Inspect scrollable elements: find all elements whose scrollHeight > clientHeight
    scrollables = page.evaluate("""
    () => {
        const out = [];
        const all = document.querySelectorAll('*');
        for (const el of all) {
            if (el.scrollHeight > el.clientHeight + 50 && el.clientHeight > 200) {
                const style = getComputedStyle(el);
                if (style.overflowY === 'auto' || style.overflowY === 'scroll') {
                    out.push({
                        tag: el.tagName, cls: (el.className || '').toString().slice(0,120),
                        scrollHeight: el.scrollHeight, clientHeight: el.clientHeight,
                        scrollTop: el.scrollTop
                    });
                }
            }
        }
        return out;
    }
    """)
    findings["scrollable_containers"] = scrollables
    findings["body_scrollHeight"] = page.evaluate("document.body.scrollHeight")
    findings["window_innerHeight"] = page.evaluate("window.innerHeight")
    findings["document_scrollingElement_scrollHeight"] = page.evaluate(
        "document.scrollingElement ? document.scrollingElement.scrollHeight : null"
    )

    # Try window scroll via evaluate (not mouse.wheel) and see if img count grows
    counts_after_window_scroll = []
    for i in range(6):
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(1200)
        n = len(page.locator('img[src*="_next/image"]').all())
        counts_after_window_scroll.append(n)
    findings["counts_after_window_scrollTo_bottom_x6"] = counts_after_window_scroll

    # Try mouse.wheel over body center too, for comparison
    page.mouse.move(750, 500)
    counts_after_mouse_wheel = []
    for i in range(6):
        page.mouse.wheel(0, 1400)
        page.wait_for_timeout(1200)
        n = len(page.locator('img[src*="_next/image"]').all())
        counts_after_mouse_wheel.append(n)
    findings["counts_after_mouse_wheel_x6"] = counts_after_mouse_wheel

    # look for pagination / load-more buttons or numbered pages
    buttons_text = page.evaluate("""
    () => Array.from(document.querySelectorAll('button')).map(b => (b.innerText||'').trim()).filter(t => t.length>0 && t.length<20)
    """)
    findings["button_texts"] = buttons_text[:40]

    # look for a "page=" or offset param link
    links = page.evaluate("""
    () => Array.from(document.querySelectorAll('a')).map(a => a.href).filter(h => h.includes('page') || h.includes('offset'))
    """)
    findings["pagination_links"] = links[:20]

    context.close()
    browser.close()

OUT.write_text(json.dumps(findings, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Wrote {OUT}")
print(json.dumps(findings, ensure_ascii=False, indent=2)[:3000])
