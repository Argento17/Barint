"""Remove backgrounds from mascot standalone renders -> clean transparent PNGs.
Keeps originals; writes *_cutout.png (full frame) and *_cutout_trim.png (cropped to figure)."""
import pathlib
from rembg import remove, new_session
from PIL import Image

SRC = pathlib.Path(r"C:\Bari\design\Mascots")
files = ["lumo_standalone.png", "oli_standalone.png"]

session = new_session("u2net")  # good general foreground model

for name in files:
    src = SRC / name
    img = Image.open(src).convert("RGBA")
    out = remove(img, session=session, post_process_mask=True)  # RGBA w/ alpha

    stem = src.stem.replace("_standalone", "")
    full = SRC / f"{stem}_cutout.png"
    out.save(full)

    # tight crop to the visible figure + small transparent margin
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

    # report transparency + size
    alpha = out.split()[-1]
    amin, amax = alpha.getextrema()
    print(f"{name}: -> {full.name} ({out.size}) + {trim.name} ({trimmed.size}) | alpha range {amin}-{amax}")

print("DONE")
