"""Cut mascot poses out of the gradient-background renders → transparent PNGs.
Two-character images are split L/R (LUMO left, OLI right); the high-five stays a pair."""
import pathlib
from rembg import remove, new_session
from PIL import Image

SRC = pathlib.Path(r"C:\Bari\design\Social\new images")
OUT = pathlib.Path(r"C:\Bari\design\Mascots\poses")
OUT.mkdir(parents=True, exist_ok=True)
session = new_session("u2net")

# (filename, tag, split_fraction or None, mode)
jobs = [
    ("4859edd6-b244-40df-bf73-b5221be98f77.png", "wave_cart", 0.50, "split"),
    ("ChatGPT Image Jul 2, 2026, 11_09_07 AM.png", "inspect_cart", 0.55, "split"),
    ("ChatGPT Image Jul 2, 2026, 11_17_46 AM.png", "highfive", None, "whole"),
    ("ChatGPT Image Jul 2, 2026, 11_19_34 AM.png", "heroes", 0.50, "split"),
]

def autocrop(img, pad=20):
    bb = img.getbbox()
    if not bb:
        return img
    l, t, r, b = bb
    l = max(0, l - pad); t = max(0, t - pad)
    r = min(img.width, r + pad); b = min(img.height, b + pad)
    return img.crop((l, t, r, b))

for fn, tag, frac, mode in jobs:
    src = SRC / fn
    if not src.exists():
        print("MISSING", fn); continue
    img = Image.open(src).convert("RGBA")
    out = remove(img, session=session, post_process_mask=True)
    W, H = out.size
    pair = autocrop(out)
    pair.save(OUT / f"{tag}_pair.png")
    line = f"{tag}: pair {pair.size}"
    if mode == "split" and frac:
        xw = int(W * frac)
        L = autocrop(out.crop((0, 0, xw, H)))
        R = autocrop(out.crop((xw, 0, W, H)))
        L.save(OUT / f"{tag}_L.png")   # LUMO (leaf)
        R.save(OUT / f"{tag}_R.png")   # OLI (olive)
        line += f" | L {L.size} | R {R.size}"
    a = out.split()[-1].getextrema()
    print(line, "| alpha", a)
print("DONE ->", OUT)
