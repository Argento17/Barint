"""Mobile-viewport screenshot of the live crackers page for panel 4's phone frame."""
import pathlib
from playwright.sync_api import sync_playwright

OUT = pathlib.Path(r"C:\Bari\design\Social\shots")
OUT.mkdir(parents=True, exist_ok=True)
url = "https://bari.digital/hashvaot/crackers"

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 430, "height": 932}, device_scale_factor=3, is_mobile=True)
    pg.goto(url, wait_until="domcontentloaded", timeout=45000)
    pg.wait_for_timeout(3000)
    # try to dismiss cookie banner if present
    for label in ["קבל הכל", "אישור", "Accept"]:
        try:
            pg.get_by_text(label, exact=False).first.click(timeout=1200)
            pg.wait_for_timeout(600); break
        except Exception:
            pass
    pg.screenshot(path=str(OUT / "crackers_mobile_full.png"), full_page=True)
    print("full ->", OUT / "crackers_mobile_full.png")
    b.close()
