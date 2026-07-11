"""
Consolidate directly-scraped creatine supplement shelf facts (Shufersal + MyProtein-IL +
iHerb-IL) into one raw JSON dataset for TASK-492C data step 1.

All facts below were captured by direct HTTP GET + BeautifulSoup/JSON-LD parse against the
live retailer pages (Shufersal search+product pages, MyProtein-IL product pages, iHerb-IL
product pages) on 2026-07-03. No Open Food Facts. No invented doses/prices. A field left
None here means the field was not found on the scraped page (missing-data discard rule) --
never assumed.
"""
from __future__ import annotations

import json
from pathlib import Path

OUT_DIR = Path(r"C:\Bari\03_operations\bsip0\scrape\creatine_supplement_shelf")

products: list[dict] = []

# ── 1. SHUFERSAL -- pure creatine supplement powders (Israeli grocery retailer) ──────────
products.append({
    "retailer_id": "shufersal", "retailer_name": "שופרסל",
    "channel": "israeli_grocery_retailer",
    "source_url": "https://www.shufersal.co.il/online/he/p/p_7290014386006",
    "name_he": "קריאטין מונוהידראט ענבים",
    "brand": "Super Effect", "barcode": "7290014386006", "price_ils": 119.00, "weight_g": 300,
    "form": "monohydrate", "creatine_g_per_serving": None, "servings_per_container": None,
    "named_vs_blend": "named_no_dose", "standalone_or_blend": "standalone", "third_party_cert": None,
    "notes": "Grape-flavor creatine monohydrate, 300g. No per-serving gram/mg figure or usage "
             "instructions found in scraped page text -- dose undisclosed on this data source.",
})
products.append({
    "retailer_id": "shufersal", "retailer_name": "שופרסל",
    "channel": "israeli_grocery_retailer",
    "source_url": "https://www.shufersal.co.il/online/he/p/p_7290016392005",
    "name_he": "קריאטין מונוהידראט פירות",
    "brand": "Super Effect", "barcode": "7290016392005", "price_ils": 119.00, "weight_g": 300,
    "form": "monohydrate", "creatine_g_per_serving": None, "servings_per_container": None,
    "named_vs_blend": "named_no_dose", "standalone_or_blend": "standalone", "third_party_cert": None,
    "notes": "Same product line, mixed-berry flavor, 300g. Dose undisclosed on scraped page, "
             "same gap as the grape variant.",
})
products.append({
    "retailer_id": "shufersal", "retailer_name": "שופרסל",
    "channel": "israeli_grocery_retailer",
    "source_url": "https://www.shufersal.co.il/online/he/p/p_7290019766223",
    "name_he": "אולאין אבקת קריאטין",
    "brand": "All In", "barcode": "7290019766223", "price_ils": 99.90, "weight_g": 240,
    "form": "monohydrate", "creatine_g_per_serving": 3.0, "servings_per_container": 83.0,
    "named_vs_blend": "named_quantified", "standalone_or_blend": "standalone", "third_party_cert": None,
    "notes": "Page text: serving contains 3g monohydrate (מנת הגשה "
             "מכילה 3 גרם מונוהידראט); "
             "83 servings/container disclosed. Marketed for muscle recovery/building.",
})
products.append({
    "retailer_id": "shufersal", "retailer_name": "שופרסל",
    "channel": "israeli_grocery_retailer",
    "source_url": "https://www.shufersal.co.il/online/he/p/p_7290010081288",
    "name_he": "אבקת קריאטין מונוהידארט",
    "brand": "Sport GS", "barcode": "7290010081288", "price_ils": 167.00, "weight_g": 500,
    "form": "monohydrate", "creatine_g_per_serving": None, "servings_per_container": None,
    "named_vs_blend": "named_no_dose", "standalone_or_blend": "standalone", "third_party_cert": None,
    "notes": "500g monohydrate powder tub. No per-serving dose figure or usage instructions "
             "found in scraped page text.",
})

# ── 2. MYPROTEIN-IL -- import brand, direct e-commerce, ships to Israel ─────────────────
mp = [
    dict(pid="10530050", slug="creatine-monohydrate-powder", name_en="Impact Creatine (Unflavoured, 250g/73 servings)",
         gtin="5055534302002", price_ils=75.31, weight_g=250, servings=73, form="monohydrate",
         dose_g=3.0, dose_basis="named_quantified", cert="Informed Choice",
         notes="ProductGroup base SKU 'Impact Creatine'; description: 'Each serving delivers "
               "3g of creatine monohydrate'. Many flavor/size variants exist at the same URL; "
               "250g/73-serving Unflavoured in-stock variant price used as representative offer."),
    dict(pid="10574930", slug="creapure-micronised-creatine-capsules", name_en="Creapure Micronised Creatine Capsules",
         gtin=None, price_ils=146.0, weight_g=None, servings=None, form="monohydrate (Creapure-branded)",
         dose_g=2.8, dose_basis="named_quantified", cert=None,
         notes="Description: 'Each four-capsule serving delivers 2.8g of creatine monohydrate' -- "
               "BELOW the 3g/day dose-honesty floor per co-sign S4, though disclosed and named, "
               "not fairy-dusted by concealment (sub-therapeutic per SIE band, not undisclosed)."),
    dict(pid="13528283", slug="creatine-gummies", name_en="Creatine Gummies",
         gtin=None, price_ils=204.0, weight_g=None, servings=None, form="monohydrate",
         dose_g=3.0, dose_basis="named_quantified", cert=None,
         notes="Description: '1g of pure creatine monohydrate in every gummy ... full 3g daily "
               "dose in just 3 gummies.'"),
    dict(pid="10872819", slug="creatine-monohydrate-elite", name_en="Creatine Monohydrate Elite",
         gtin=None, price_ils=284.0, weight_g=None, servings=None, form="monohydrate",
         dose_g=3.0, dose_basis="named_quantified", cert="Informed Choice (page text)",
         notes="Description confirms 3g creatine per serving; full page text contains an "
               "'informed choice' mention (cert claim as stated on page, not independently "
               "re-verified against the certifying body's own registry)."),
    dict(pid="10575029", slug="creatine-monohydrate-tablets", name_en="Creatine Monohydrate Tablets",
         gtin=None, price_ils=60.0, weight_g=None, servings=None, form="monohydrate (tablet)",
         dose_g=None, dose_basis="named_no_dose", cert=None,
         notes="Marketing description truncated in scrape; no explicit per-serving gram/tablet-"
               "count figure found in scraped LD-JSON description text."),
    dict(pid="10529740", slug="the-creatine-creapure", name_en="THE Creatine Creapure",
         gtin=None, price_ils=213.0, weight_g=None, servings=None,
         form="monohydrate (Creapure-branded, 99.99% pure)", dose_g=3.0, dose_basis="named_quantified",
         cert="Informed Choice",
         notes="Description: 'Each serving delivers 3g of high-quality creatine ... Informed "
               "Choice certified.'"),
]
for m in mp:
    products.append({
        "retailer_id": "myprotein_il", "retailer_name": "MyProtein Israel",
        "channel": "import_brand_direct_ecommerce_available_in_israel",
        "source_url": f"https://www.myprotein.co.il/p/sports-nutrition/{m['slug']}/{m['pid']}/",
        "name_he": None, "name_en": m["name_en"], "brand": "Myprotein",
        "barcode": m["gtin"], "price_ils": m["price_ils"], "weight_g": m["weight_g"],
        "form": m["form"], "creatine_g_per_serving": m["dose_g"],
        "servings_per_container": m["servings"], "named_vs_blend": m["dose_basis"],
        "standalone_or_blend": "standalone", "third_party_cert": m["cert"], "notes": m["notes"],
    })

# ── 3. IHERB-IL -- import marketplace, ships to Israel, ILS pricing ─────────────────────
ih = [
    dict(pid="68616", slug="optimum-nutrition-micronized-creatine-powder-unflavored-1-32-lb-600-g",
         name_he="Optimum Nutrition, אבקת קריאטין ממוזער", brand="Optimum Nutrition",
         gtin="748927023855", price_ils=122.89, weight_g=600, form="monohydrate (micronized)",
         dose_g=5.0, servings=120, cert="Informed-Choice",
         notes="Facts panel: serving size 5g (1 heaping tsp), 120 servings/container, "
               "creatine monohydrate 5g/serving. Informed-Choice tested."),
    dict(pid="70006", slug="thorne-creatine-16-oz-450-g",
         name_he="Thorne, קריאטין", brand="Thorne",
         gtin="693749006350", price_ils=133.43, weight_g=450, form="monohydrate",
         dose_g=5.0, servings=90, cert="NSF Certified for Sport",
         notes="Facts panel: serving size 1 scoop (5g), 90 servings/container, creatine "
               "monohydrate 5g/serving. NSF Certified for Sport disclosed on page."),
    dict(pid="687", slug="now-foods-sports-micronized-creatine-monohydrate-1-1-lbs-500-g",
         name_he="NOW Foods Sports, קריאטין מונוהידרט ממוזער", brand="NOW Foods",
         gtin="733739020383", price_ils=86.21, weight_g=500, form="monohydrate (micronized)",
         dose_g=4.2, servings=119, cert=None,
         notes="Facts panel: serving size 1.5 level tsp (~4.2g), ~119 servings/container, "
               "creatine monohydrate 4.2g (4,200mg)/serving. No third-party cert claim found on page."),
    dict(pid="74271", slug="muscletech-platinum-100-creatine-monohydrate-unflavored-14-11-oz-400-g",
         name_he="MuscleTech, 100% קריאטין מונוהידרט של Platinum", brand="MuscleTech",
         gtin="631656705737", price_ils=102.46, weight_g=400, form="monohydrate (HPLC-tested)",
         dose_g=5.0, servings=80, cert=None,
         notes="Facts panel: serving size 1 scoop (5g), ~80 servings/container, creatine "
               "monohydrate 5g/serving. Page states HPLC-tested; no named third-party sport-"
               "cert program (NSF/Informed-Sport) found on page."),
    dict(pid="120573", slug="california-gold-nutrition-sport-pure-creatine-monohydrate-750-mg-240-veggie-capsules",
         name_he="California Gold Nutrition Sport, קריאטין מונוהידרט טהור", brand="California Gold Nutrition",
         gtin="898220022830", price_ils=57.95, weight_g=None, form="monohydrate (capsule)",
         dose_g=0.75, servings=240, cert="iTested (third-party program named on page)",
         notes="Facts panel: serving size 1 capsule, 240 capsules/container, creatine "
               "monohydrate 750mg/capsule. 750mg/serving as labeled is a single-capsule dose -- "
               "the label does not state a recommended capsules-per-day count in the scraped "
               "text, so a computable daily dose was not assumed (missing-data discard rule)."),
    dict(pid="134139", slug="abe-creatine-monohydrate-micronized-powder-blue-raspberry-10-58-oz-300-g",
         name_he="ABE, קריאטין מונוהידרט מיקרוניזציה", brand="ABE",
         gtin="5056555204153", price_ils=54.90, weight_g=300, form="monohydrate (micronized)",
         dose_g=4.25, servings=60, cert="Informed Sport",
         notes="Facts panel: serving size 1 heaping scoop (5g), 60 servings/container, "
               "creatine monohydrate (micronized) 4.25g/serving. Informed Sport tested, "
               "batch-tested per page copy."),
    dict(pid="126238", slug="kaged-creatine-hcl-unflavored-1-98-oz-56-25-g",
         name_he="Kaged, קריאטין HCl", brand="Kaged",
         gtin="850045966478", price_ils=89.15, weight_g=56.25, form="hcl",
         dose_g=0.75, servings=75, cert="Informed Sport",
         notes="Facts panel: serving size 1 scoop (~750mg), ~75 servings/container, creatine "
               "hydrochloride (patented C-HCl) 750mg/serving. Marketing claims HCl form is "
               "absorbed more efficiently at lower dose than monohydrate -- this is a formulation "
               "claim, not independently verified here (co-sign S3.1: alternative forms carry no "
               "evidenced superiority over monohydrate; framing captured, not endorsed)."),
    dict(pid="85586", slug="con-cret-creatine-hcl-raw-tart-1-69-oz-48-g",
         name_he="Con-Cret, קריאטין HCl", brand="Con-Cret",
         gtin="682676700646", price_ils=86.12, weight_g=48, form="hcl",
         dose_g=0.75, servings=64, cert="NSF Certified for Sport",
         notes="Facts panel: serving size 1 scoop (750mg), 64 servings/container, creatine "
               "HCl 750mg/serving. NSF Certified for Sport disclosed on page. Same low-nominal-"
               "gram HCl pattern as Kaged."),
]
for m in ih:
    products.append({
        "retailer_id": "iherb_il", "retailer_name": "iHerb Israel",
        "channel": "import_marketplace_direct_ecommerce_available_in_israel",
        "source_url": f"https://il.iherb.com/pr/{m['slug']}/{m['pid']}",
        "name_he": m["name_he"], "name_en": None, "brand": m["brand"],
        "barcode": m["gtin"], "price_ils": m["price_ils"], "weight_g": m["weight_g"],
        "form": m["form"], "creatine_g_per_serving": m["dose_g"],
        "servings_per_container": m["servings"], "named_vs_blend": "named_quantified",
        "standalone_or_blend": "standalone", "third_party_cert": m["cert"], "notes": m["notes"],
    })

OUT_DIR.mkdir(parents=True, exist_ok=True)
raw_path = OUT_DIR / "creatine_supplement_shelf_bsip0_raw_v1.json"
raw_path.write_text(json.dumps(products, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Wrote {len(products)} products to {raw_path}")
