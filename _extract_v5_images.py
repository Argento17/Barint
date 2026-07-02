import re, base64
from pathlib import Path

html = Path(r"c:\Users\HP\Downloads\bari_homepage_v5_layout_fix.html").read_text(encoding="utf-8")
out = Path(r"c:\Bari\bari-web\public\home")
out.mkdir(parents=True, exist_ok=True)

hero_m = re.search(r'class="hero-stage-img"\s+src="(data:image/[^"]+)"', html)
comp_m = re.search(r'class="comparison-img"\s+src="(data:image/[^"]+)"', html)

for name, m in [("hero-product-stage.png", hero_m), ("featured-cereal-duel-stage.png", comp_m)]:
    if not m:
        print("missing", name)
        continue
    data_url = m.group(1)
    header, b64 = data_url.split(",", 1)
    path = out / name
    path.write_bytes(base64.b64decode(b64))
    print(name, path.stat().st_size)
