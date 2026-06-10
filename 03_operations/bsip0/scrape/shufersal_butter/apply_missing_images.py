"""
Apply found image URLs to butter_frontend_v2.json for the 20 products missing images.
Images sourced from: brand websites, Yango Deli, Carrefour UAE CDN, Google image search.

Run: python apply_missing_images.py
"""
import json, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

FRONTEND_JSON = Path(r"C:\bari\bari-web\src\data\comparisons\butter_frontend_v2.json")

IMAGE_MAP = {
    # ── Kerrygold (Irish) ────────────────────────────────────────────────────
    "5099460004132": "https://melcom.com/media/catalog/product/cache/d0e1b0d5c74d14bfa9f7dd43ec52d082/1/1/119333_1.png",
    # Kerrygold Salted 200g — melcom.com ("KERRYGOLD BUTTER SALTED 200G")
    "5099460004149": "https://www.kerrygoldusa.com/wp-content/uploads/2017/09/Unsalted-227g_Back.jpg",
    # Kerrygold Unsalted — official kerrygoldusa.com
    "5099460004156": "https://www.kerrygoldusa.com/wp-content/uploads/2017/09/Unsalted-227g_Back.jpg",
    # Kerrygold Unsalted 250g — same packaging
    "5099460010935": "https://www.kerrygoldusa.com/wp-content/uploads/2017/09/Unsalted-227g_Back.jpg",
    # Kerrygold Unsalted 250g — same packaging

    # ── Lurpak (Danish / Arla) ───────────────────────────────────────────────
    "5740900400221": "https://images.arla.com/recordid/CC13AEE1-3253-4B3F-8452F2B662087DED/picture.png?width=1200&height=630&format=webp",
    # Lurpak Unsalted — official arla.com / lurpak.com
    "5740900400238": "https://www.gfifoods.com/media/catalog/product/8/4/84233_20210920_1316522_onrq2cozi3foml9n.jpg?optimize=high&bg-color=255,255,255&fit=bounds&height=700&width=700&canvas=700:700",
    # Lurpak Salted — gfifoods.com product listing

    # ── Président (French) ───────────────────────────────────────────────────
    "3228021530005": "https://presidentcheese.com/wp-content/uploads/2016/05/President_Butter_Unsalted_Bar_7oz_500x500.png",
    # Président Unsalted — official presidentcheese.com
    "3228021530012": "http://www.mrmarcel.com/cdn/shop/files/president-salted-butter-7oz.jpg?crop=center&height=1200&v=1720804234&width=1200",
    # Président Salted — mrmarcel.com

    # ── Anchor (New Zealand) ─────────────────────────────────────────────────
    "9414544900015": "https://www.anchordairy.com/pacific/en/products/butter-and-spreads/anchor-unsalted-butter/_jcr_content/root/container/image.coreimg.png/1685333316955/110388216-unsalted4542000x2420-png.png",
    # Anchor Unsalted — official anchordairy.com
    "9414544900022": "http://www.shopping-d.com/cdn/shop/products/AnchorPureNewZealandButterSalted250g.png?v=1636189308",
    # Anchor Salted 250g — shopping-d.com

    # ── Paysan Breton / Pizan Breton (French) ────────────────────────────────
    "3412130012558": "https://www.paysanbreton.com/sites/default/files/styles/product_640x640/public/product/2026-02/Beurre%20Moul%C3%A9%20Doux%20Paysan%20Breton%20Origin%20info.webp?itok=zi1rH_AN",
    # Paysan Breton Unsalted — official paysanbreton.com
    "3412130012534": "https://www.paysanbreton.com/sites/default/files/styles/product_640x640/public/product/2026-02/Beurre%20Moul%C3%A9%20Demi%20Sel%20Paysan%20Breton%20Origin%20info.webp?itok=Jxvn0Nui",
    # Paysan Breton Salted — official paysanbreton.com

    # ── Échiré AOP (French, sold in Israel as "אשירה") ───────────────────────
    "3760088100025": "https://echirelebeurredefrance.fr/wp-content/uploads/2024/12/BE-DX-200g.png.webp",
    # Échiré AOP — official echirelebeurredefrance.fr

    # ── Tara (Israeli) ───────────────────────────────────────────────────────
    "7290000066028": "https://static.yango.tech/avatars/get-grocery-goods/2805921/78d1cf87-5252-4a03-995f-42d71e29319d/300x300?webp=true",
    # Tara Butter 82% Unsalted — Yango Deli Israel
    "7290000066035": "https://static.yango.tech/avatars/get-grocery-goods/2750890/b4949932-5037-46e7-a51c-93ea308558e9/300x300?webp=true",
    # Tara Butter Salted — Yango Deli Israel (different variant image)

    # ── Yotvata (Israeli kibbutz dairy) ─────────────────────────────────────
    "7290006325046": "https://yotvatapark.co.il/wp-content/uploads/2019/12/bg_section-1_block-4_pack.png",
    # Yotvata dairy — official yotvatapark.co.il

    # ── Adam Adom (Israeli dairy) ────────────────────────────────────────────
    "7290113401022": "https://www.kfi.co.il/wp-content/uploads/2024/06/hema.jpg",
    # Adam Adom butter — Israeli dairy product image (kfi.co.il)

    # ── Noga (Tnuva sub-brand, Israeli) ──────────────────────────────────────
    "7290002492086": "http://shoppy.co.il/cdn/shop/products/tnuvabutter200g_1200x1200.png?v=1639002966",
    # Noga butter (Tnuva sub-brand) — Tnuva butter product image from shoppy.co.il

    # ── Ghee products ────────────────────────────────────────────────────────
    "8906060890143": "https://m.media-amazon.com/images/I/71EEE2JNi0L.jpg",
    # חמאה מזוקקת גהי — Rani Ghee kosher clarified butter (glass jar)
    "4260268321030": "https://cloudinary.images-iherb.com/image/upload/f_auto,q_auto:eco/images/pif/pif50718/m/37.jpg",
    # שמן גהי German — iHerb organic ghee product image
}


def apply():
    with open(FRONTEND_JSON, encoding="utf-8") as f:
        data = json.load(f)

    updated = 0
    for p in data.get("products", []):
        bc = str(p.get("barcode", ""))
        if bc in IMAGE_MAP and not (p.get("imageUrl", "")):
            p["imageUrl"] = IMAGE_MAP[bc]
            updated += 1
            print(f"  SET {bc}: {IMAGE_MAP[bc][:70]}")

    with open(FRONTEND_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\nPatched {updated}/{len(IMAGE_MAP)} products in {FRONTEND_JSON.name}")
    return updated


if __name__ == "__main__":
    print(f"Applying {len(IMAGE_MAP)} image mappings to butter frontend JSON...\n")
    apply()
