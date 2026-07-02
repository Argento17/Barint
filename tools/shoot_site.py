"""Screenshot the live Bari site for use inside panel 4 (real UI, not a mockup)."""
import pathlib
from playwright.sync_api import sync_playwright

OUT = pathlib.Path(r"C:\Bari\design\Social\shots")
OUT.mkdir(parents=True, exist_ok=True)

urls = {
    "crackers": "https://bari.digital/hashvaot/crackers",
    "hub": "https://bari.digital/hashvaot/supermarket",
    "milk": "https://bari.digital/hashvaot/milk-comparison",
}
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1180, "height": 1500}, device_scale_factor=2)
    for name, url in urls.items():
        try:
            resp = pg.goto(url, wait_until="domcontentloaded", timeout=45000)
            pg.wait_for_timeout(2500)
            pg.screenshot(path=str(OUT / f"{name}.png"), full_page=False)
            print(f"{name}: {resp.status if resp else '?'} -> {OUT / (name+'.png')}")
        except Exception as e:
            print(f"{name}: FAIL {str(e)[:160]}")
    b.close()
