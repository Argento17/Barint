"""Bari social carousel — code-composed. Real logo + posed mascots + real site card + Hebrew RTL.
v2: Segoe UI, deep-green headlines, CTA pill, per-panel poses, real crackers card in panel 4."""
import pathlib
from PIL import Image, ImageDraw, ImageFont
from bidi.algorithm import get_display

ROOT = pathlib.Path(r"C:\Bari")
PUB = ROOT / "bari-web" / "public"
MASC = ROOT / "design" / "Mascots"
POSE = MASC / "poses"
SHOT = ROOT / "design" / "Social" / "shots"
OUT = ROOT / "design" / "Social" / "panels"
OUT.mkdir(parents=True, exist_ok=True)

S = 1080
MARG = 96
CREAM = (247, 247, 242, 255)
WHITE = (252, 252, 249, 255)
HEAD  = (20, 58, 44, 255)     # deep forest green headlines (was near-black)
GREEN = (31, 143, 106, 255)   # #1F8F6A
DARK  = (20, 40, 32, 255)
SLATE = (78, 86, 99, 255)
PALE  = (223, 239, 232, 255)
TRACK = (224, 227, 221, 255)
BORDER = (228, 230, 224, 255)
FB = r"C:\Windows\Fonts\segoeuib.ttf"
FR = r"C:\Windows\Fonts\segoeui.ttf"

def f(size, bold=True):
    return ImageFont.truetype(FB if bold else FR, size)

def he(s):
    return get_display(s)

def scale_h(img, h):
    return img.resize((int(img.width * h / img.height), h), Image.LANCZOS)

def load(p):
    return Image.open(p).convert("RGBA")

LOGO = load(PUB / "Bari_logo_concept3_transparent_highres.png")
# pose library
P_LUMO_WAVE   = load(POSE / "wave_cart_L.png")
P_OLI_CART    = load(POSE / "wave_cart_R.png")
P_LUMO_INSPECT= load(POSE / "inspect_cart_L.png")
P_HIGHFIVE    = load(POSE / "highfive_pair.png")
P_HEROES      = load(POSE / "heroes_pair.png")
OLI_PLAIN     = load(MASC / "oli_cutout_trim.png")
LUMO_PLAIN    = load(MASC / "lumo_cutout_trim.png")

def new():
    c = Image.new("RGBA", (S, S), CREAM)
    return c, ImageDraw.Draw(c)

def logo_at(c, top, h=128):
    lg = scale_h(LOGO, h)
    c.alpha_composite(lg, ((S - lg.width) // 2, top))

def headline(d, lines, y, size=56, fill=HEAD, gap=76, x=None):
    x = S / 2 if x is None else x
    for ln in lines:
        d.text((x, y), he(ln), font=f(size), fill=fill, anchor="ma")
        y += gap
    return y

def divider(d, y, cx=S/2, w=66):
    d.rounded_rectangle([cx - w, y, cx + w, y + 6], radius=3, fill=GREEN)

def cta_pill(c, d, y=956):
    pf = f(29); txt = "בדקו ב־bari.digital"
    t = he(txt); tw = d.textlength(t, font=pf); pw, ph = tw + 84, 62
    px = (S - pw) / 2
    d.rounded_rectangle([px, y, px + pw, y + ph], radius=ph / 2, fill=GREEN)
    d.text((S / 2, y + ph / 2), t, font=pf, fill=WHITE, anchor="mm")

def eyebrow(d, text, y=70):
    d.text((S / 2, y), he(text), font=f(26, bold=False), fill=GREEN, anchor="ma")

# ---- line icons ----
def _w(s): return max(3, int(s * 0.085))
def ic_magnifier(d, cx, cy, s, col):
    r = s * 0.28; ox, oy = cx - s*0.12, cy - s*0.12
    d.ellipse([ox-r, oy-r, ox+r, oy+r], outline=col, width=_w(s))
    d.line([ox+r*0.7, oy+r*0.7, cx+s*0.34, cy+s*0.34], fill=col, width=_w(s)+1)
def ic_flask(d, cx, cy, s, col):
    t = s*0.34
    d.line([cx-s*0.12, cy-t, cx-s*0.12, cy-s*0.02], fill=col, width=_w(s))
    d.line([cx+s*0.12, cy-t, cx+s*0.12, cy-s*0.02], fill=col, width=_w(s))
    d.line([cx-s*0.2, cy-t, cx+s*0.2, cy-t], fill=col, width=_w(s))
    d.polygon([cx-s*0.12, cy-s*0.02, cx+s*0.12, cy-s*0.02, cx+s*0.3, cy+s*0.34, cx-s*0.3, cy+s*0.34],
              outline=col, width=_w(s))
def ic_shield(d, cx, cy, s, col):
    r = s*0.34
    d.polygon([cx, cy-r, cx+r, cy-r*0.55, cx+r, cy+r*0.2, cx, cy+r, cx-r, cy+r*0.2, cx-r, cy-r*0.55],
              outline=col, width=_w(s))
    d.line([cx-r*0.4, cy, cx-r*0.05, cy+r*0.35, cx+r*0.5, cy-r*0.35], fill=col, width=_w(s))
def ic_target(d, cx, cy, s, col):
    for rr in (s*0.34, s*0.2):
        d.ellipse([cx-rr, cy-rr, cx+rr, cy+rr], outline=col, width=_w(s))
    d.ellipse([cx-s*0.06, cy-s*0.06, cx+s*0.06, cy+s*0.06], fill=col)
def ic_leaf(d, cx, cy, s, col):
    r = s*0.34
    d.pieslice([cx-r, cy-r, cx+r, cy+r], 200, 20, outline=col, width=_w(s))
    d.line([cx-r*0.5, cy+r*0.5, cx+r*0.5, cy-r*0.5], fill=col, width=_w(s))
def ic_scales(d, cx, cy, s, col):
    r = s*0.32
    d.line([cx, cy-r, cx, cy+r], fill=col, width=_w(s))
    d.line([cx-r, cy-r*0.7, cx+r, cy-r*0.7], fill=col, width=_w(s))
    d.line([cx-r*0.6, cy+r, cx+r*0.6, cy+r], fill=col, width=_w(s))
    for sx in (-r, r):
        d.arc([cx+sx-r*0.5, cy-r*0.7, cx+sx+r*0.5, cy+r*0.3], 0, 180, fill=col, width=_w(s))
def ic_person(d, cx, cy, s, col):
    r = s*0.16
    d.ellipse([cx-r, cy-s*0.3, cx+r, cy-s*0.3+2*r], outline=col, width=_w(s))
    d.arc([cx-s*0.3, cy+s*0.02, cx+s*0.3, cy+s*0.6], 180, 360, fill=col, width=_w(s))
def ic_heart(d, cx, cy, s, col):
    r = s*0.18
    d.ellipse([cx-2*r, cy-r-2, cx, cy+r-2], outline=col, width=_w(s))
    d.ellipse([cx, cy-r-2, cx+2*r, cy+r-2], outline=col, width=_w(s))
    d.line([cx-1.9*r, cy+r*0.3, cx, cy+s*0.34], fill=col, width=_w(s))
    d.line([cx+1.9*r, cy+r*0.3, cx, cy+s*0.34], fill=col, width=_w(s))
ICONS = {"magnifier": ic_magnifier, "flask": ic_flask, "shield": ic_shield, "target": ic_target,
         "leaf": ic_leaf, "scales": ic_scales, "person": ic_person, "heart": ic_heart}

def icon_disc(c, d, cx, cy, name, r=42):
    d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=PALE)
    ICONS[name](d, cx, cy, r*1.32, GREEN)

def rtl_row(c, d, top, name, bold, sub):
    cx = S - MARG - 42; cy = top + 42
    icon_disc(c, d, cx, cy, name)
    tx = cx - 42 - 30
    d.text((tx, top + 6), he(bold), font=f(33), fill=HEAD, anchor="ra")
    d.text((tx, top + 52), he(sub), font=f(26, bold=False), fill=SLATE, anchor="ra")

def gauge(c, d, cx, cy, r, value=72):
    d.arc([cx-r, cy-r, cx+r, cy+r], 135, 45, fill=TRACK, width=int(r*0.16))
    d.arc([cx-r, cy-r, cx+r, cy+r], 135, 135 + 270*value/100, fill=GREEN, width=int(r*0.16))
    d.text((cx, cy - r*0.06), str(value), font=f(int(r*0.85)), fill=HEAD, anchor="mm")
    d.text((cx, cy + r*0.5), "100", font=f(int(r*0.26), bold=False), fill=SLATE, anchor="mm")
    d.text((cx, cy + r + 26), he("ציון בארי"), font=f(int(r*0.24)), fill=SLATE, anchor="ma")

def round_img(img, radius):
    m = Image.new("L", img.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, img.width, img.height], radius=radius, fill=255)
    out = img.copy(); out.putalpha(m); return out

def place(c, img, h, cx=None, bottom=None, left=None):
    im = scale_h(img, h)
    x = int((S - im.width)/2) if cx is None else int(cx - im.width/2)
    if left is not None: x = left
    y = bottom - im.height
    c.alpha_composite(im, (x, y))

# ---------------- panels ----------------
def panel1():
    c, d = new()
    logo_at(c, 96, 130)
    y = headline(d, ["אנחנו הופכים מידע על אוכל", "למידע שאפשר לסמוך עליו"], 330)
    divider(d, y + 16)
    place(c, P_LUMO_WAVE, 300, cx=270, bottom=904)
    place(c, OLI_PLAIN,   288, cx=812, bottom=904)
    cta_pill(c, d)
    return c

def panel2():
    c, d = new()
    eyebrow(d, "Bari · השוואות סופרמרקט")
    headline(d, ["אנחנו עושים", "את העבודה הקשה בשבילך"], 132, size=54)
    d.text((S/2, 268), he("מבוסס מדע תזונה: מנוע שמנתח נתונים בשיטתיות"),
           font=f(27), fill=GREEN, anchor="ma")
    rt = 360
    rtl_row(c, d, rt,       "magnifier", "סורקים ומנתחים", "מאות מוצרים מהמדפים")
    rtl_row(c, d, rt + 128, "flask",     "בודקים רכיבים ותוספים", "ערכים תזונתיים ואיכות")
    rtl_row(c, d, rt + 256, "shield",    "מנוע ניקוד אלגוריתמי", "שיטה אחת, אובייקטיבית ועקבית")
    place(c, P_LUMO_INSPECT, 268, cx=232, bottom=904)
    cta_pill(c, d)
    return c

def panel3():
    c, d = new()
    headline(d, ["אנחנו הופכים מידע מסובך", "לפשוט וברור"], 128, size=52)
    gauge(c, d, S/2, 402, 112, 72)
    box = [MARG + 60, 566, S - MARG - 60, 642]
    d.rounded_rectangle(box, radius=24, fill=PALE)
    d.text((S/2, 604), he("כדי שתדע בדיוק מה יש במוצר, בקלות ובבירור"),
           font=f(26, bold=False), fill=HEAD, anchor="mm")
    place(c, LUMO_PLAIN, 236, cx=250, bottom=946)
    place(c, P_OLI_CART, 250, cx=812, bottom=946)
    cta_pill(c, d, y=980)
    return c

def panel4():
    c, d = new()
    headline(d, ["איך זה נראה בפועל?"], 96, size=54)
    # real product card from the live site (crackers mobile screenshot)
    full = load(SHOT / "crackers_mobile_full.png")
    card = full.crop((28, 1912, 1262, 2232)).convert("RGBA")   # 82/A + name + product image
    cw = 900; card = card.resize((cw, int(card.height * cw / card.width)), Image.LANCZOS)
    card = round_img(card, 26)
    cardx, cardy = (S - cw)//2, 250
    d.rounded_rectangle([cardx-2, cardy-2, cardx+cw+2, cardy+card.height+2], radius=28,
                        outline=BORDER, width=3)
    c.alpha_composite(card, (cardx, cardy))
    cap_y = cardy + card.height + 46
    d.text((S/2, cap_y), he("מסך אמיתי מהאתר · דוגמה מתוך השוואת הקרקרים"),
           font=f(30), fill=HEAD, anchor="ma")
    d.text((S/2, cap_y + 46), he("מדורג 1 מתוך 19 · ציון A"),
           font=f(25, bold=False), fill=SLATE, anchor="ma")
    place(c, OLI_PLAIN, 210, cx=210, bottom=904)
    cta_pill(c, d)
    return c

def panel5():
    c, d = new()
    headline(d, ["בארי נותן לך ציון ברור ועצמאי", "ואתה מחליט מה עושים איתו"],
             150, size=46, gap=66)
    for k, s in enumerate(["שקיפות מלאה, מבוססת נתונים", "ההחלטה נשארת בידיים שלך, בעצמאות מלאה"]):
        d.text((S/2, 336 + k*58), he(s), font=f(31), fill=HEAD, anchor="ma")
    place(c, P_HIGHFIVE, 340, cx=S/2, bottom=944)
    cta_pill(c, d, y=980)
    return c

def panel6():
    c, d = new()
    d.text((S/2, 150), he("בארי."), font=f(150), fill=HEAD, anchor="ma")
    d.text((S/2, 336), "Food Intelligence", font=f(40), fill=GREEN, anchor="ma")
    headline(d, ["כי מגיע לך לדעת מה באמת", "בתוך מה שאתה אוכל"], 430, size=42, fill=SLATE, gap=58)
    place(c, P_HEROES, 300, cx=S/2, bottom=912)
    cta_pill(c, d)
    return c

# Active deck (owner removed cover + panel 3): hard-work · how-it-looks · you-choose · closing
active = [(2, panel2()), (4, panel4()), (5, panel5()), (6, panel6())]
for i, p in active:
    p.convert("RGB").save(OUT / f"panel{i}.png")

pad = 24; th_s = 480; tw = 2; th = 2
sheet = Image.new("RGB", (tw*th_s + (tw+1)*pad, th*th_s + (th+1)*pad), (60, 66, 62))
for k, (_, p) in enumerate(active):
    r, col = divmod(k, tw)
    sheet.paste(p.convert("RGB").resize((th_s, th_s), Image.LANCZOS),
                (pad + col*(th_s+pad), pad + r*(th_s+pad)))
sheet.save(OUT / "_contact_sheet.png")
print("wrote 4 panels + contact sheet")
