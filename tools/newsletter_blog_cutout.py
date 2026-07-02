"""Cut dark-green background off the newsletter + blog mascot renders -> transparent PNGs.
Mirrors mascot_cutout.py method (rembg u2net + tight trim). Writes *_cutout_trim.png."""
import pathlib
from rembg import remove, new_session
from PIL import Image

SRC = pathlib.Path(r"C:\Bari\design\Mascots")
files = {
    "ChatGPT Image Jul 2, 2026, 12_25_16 PM.png": "newsletter_reading",
    "ChatGPT Image Jul 2, 2026, 12_31_18 PM.png": "blog_desk",
}

session = new_session("u2net")

for name, stem in files.items():
    src = SRC / name
    img = Image.open(src).convert("RGBA")
    out = remove(img, session=session, post_process_mask=True)

    full = SRC / f"{stem}_cutout.png"
    out.save(full)

    bbox = out.getbbox()
    if bbox:
        pad = 24
        l, t, r, b = bbox
        l = max(0, l - pad); t = max(0, t - pad)
        r = min(out.width, r + pad); b = min(out.height, b + pad)
        trimmed = out.crop((l, t, r, b))
    else:
        trimmed = out
    trim = SRC / f"{stem}_cutout_trim.png"
    trimmed.save(trim)

    alpha = out.split()[-1]
    amin, amax = alpha.getextrema()
    print(f"{name}: -> {trim.name} ({trimmed.size}) | alpha range {amin}-{amax}")

print("DONE")
