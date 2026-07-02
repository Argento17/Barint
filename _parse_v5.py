import re
from pathlib import Path
p = Path(r"c:\Users\HP\Downloads\bari_homepage_v5_layout_fix.html")
text = p.read_text(encoding="utf-8")
text = re.sub(r'src="data:image[^"]+"', 'src="[img]"', text)
out = []
for label, pat in [
    ("comment", r"<!--.*?-->"),
    ("hero-copy", r'<div class="hero-copy">.*?</div>'),
    ("guidance", r'<div class="prototype-guidance">.*?</div>'),
    ("section-head", r'<div class="section-head">.*?</div>'),
]:
    m = re.search(pat, text, re.S)
    if m:
        out.append(f"=== {label} ===\n{m.group(0)[:4000]}\n")
Path(r"c:\Bari\_v5_extract.txt").write_text("\n".join(out), encoding="utf-8")
