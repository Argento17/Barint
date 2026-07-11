"""
TASK-518 continuation -- Super Yuda (סופר יודה) platform identification.
Plain requests gets 403 (bot-gate). Load via Playwright, capture:
  - final page title / meta tags
  - all xhr/fetch requests fired (to spot a v2/retailers/.../products style API,
    or a different white-label signature: Quik, Bianu, etc.)
  - script src tags (framework fingerprint)
"""
import json
import sys
from pathlib import Path
from urllib.parse import quote as _q

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright

OUT_DIR = Path(__file__).resolve().parent / "outputs"
BASE = "https://www.yuda.co.il"

xhr_log = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        viewport={"width": 1500, "height": 1000}, locale="he-IL",
        timezone_id="Asia/Jerusalem", extra_http_headers={"Accept-Language": "he-IL,he;q=0.9"},
        permissions=[],
    )
    page = context.new_page()
    page.on("request", lambda req: xhr_log.append((req.resource_type, req.url)))

    try:
        resp = page.goto(BASE + "/", wait_until="domcontentloaded", timeout=45000)
        print("home status:", resp.status if resp else None)
    except Exception as e:
        print("home goto failed:", str(e)[:300])
    page.wait_for_timeout(6000)

    title = page.title()
    print("title:", title)
    print("final url:", page.url)

    # dismiss any cookie/consent popups just in case
    for text in ["אישור", "מסכים", "קבל", "הבנתי", "Accept", "OK", "סגור"]:
        try:
            btn = page.get_by_text(text, exact=False).first
            if btn.is_visible(timeout=400):
                btn.click(force=True)
                page.wait_for_timeout(500)
        except Exception:
            pass

    meta = page.evaluate("""
        () => Array.from(document.querySelectorAll('meta')).map(m => ({
            name: m.getAttribute('name') || m.getAttribute('property'),
            content: m.getAttribute('content')
        })).filter(m => m.name)
    """)
    print("\nmeta tags (first 20):")
    for m in meta[:20]:
        print(" ", m)

    scripts = page.evaluate("""
        () => Array.from(document.querySelectorAll('script[src]')).map(s => s.src)
    """)
    print("\nscript src (first 25):")
    for s in scripts[:25]:
        print(" ", s)

    body_sample = page.evaluate("document.body.innerText.slice(0, 300)")
    print("\nbody text sample:", body_sample)

    # Try a butter search now that we're past the gate
    try:
        page.wait_for_timeout(2000)
        search_url = f"{BASE}/?s={_q('חמאה')}"
        page.goto(search_url, wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(5000)
        print("\nsearch attempt status/title:", page.title())
    except Exception as e:
        print("search attempt failed:", str(e)[:200])

    context.close()
    browser.close()

xhr_fetch_only = [(t, u) for t, u in xhr_log if t in ("xhr", "fetch")]
print(f"\n\n{len(xhr_fetch_only)} xhr/fetch requests total:")
for t, u in xhr_fetch_only[:60]:
    print(f"  [{t}] {u}")

(OUT_DIR / "superyuda_xhr_log.json").write_text(
    json.dumps(xhr_fetch_only, ensure_ascii=False, indent=2), encoding="utf-8"
)
