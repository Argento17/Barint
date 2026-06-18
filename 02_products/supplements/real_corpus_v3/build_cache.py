"""Emit candidate panel cache files for the v3 re-measurement sprint.

Each entry records HOW the panel was acquired (acquisition_method) for honesty:
  - brand_panel   : full panel scraped from the brand site (WebFetch), barcode-confirmed
  - search_panel  : per-active dose/form from retailer/search snippets (WebSearch)
  - name_derived  : single-active dose taken from the SP item name itself (PDP path)
Barcode on each panel = the SP SKU barcode (the panel IS that SKU — confirmed via
brand-site barcode, retailer title, or by-construction for name-derived). Claims are
PROVISIONAL (claim->tier is a Nutrition curation step); the sprint measures ACQUISITION,
not final grades. Missing field = null, never fabricated. EDPG: all candidate.
"""
import json, pathlib
HERE = pathlib.Path(__file__).resolve().parent
CACHE = HERE / "cache"
CACHE.mkdir(exist_ok=True)

# (barcode, brand, product_name, claim_he, [actives], method, source_url)
# active = (ingredient, amount, unit, form)
ROWS = [
    # ---- Tier A: brand-site full panels (WebFetch, barcode-confirmed) ----
    ("7290017218526", "altman", "אלטמן ביוטין 1000 מקג",
     "תומך בבריאות השיער; מחסור עלול להתבטא בנשירת שיער",
     [("ביוטין (Biotin)", 1000, "mcg", None)], "brand_panel",
     "https://www.altman.co.il/shop/beauty/hair-care/biotin/"),
    ("7290019444206", "altman", "אלטמן מגנזיום Balance",
     "קומפלקס מגנזיום לפעילות מאוזנת ולתפקוד תקין של השרירים ומערכת העצבים",
     [("מגנזיום (from oxide)", 450, "mg", "oxide"),
      ("אשווגנדה KSM-66", 50, "mg", None), ("ולריאן", 50, "mg", None),
      ("ויטמין B6", 30, "mg", None)], "brand_panel",
     "https://www.altman.co.il/shop/magnesium/magnesium-balance/"),
    ("7290011899127", "altman", "אלטמן אומגה 3 - 9 חודשים",
     "אומגה 3 עם EPA ו-DHA לתמיכה בהריון בהתאם להמלצות האיגוד למיילדות וגינקולוגיה",
     [("DHA", 300, "mg", None), ("EPA", 100, "mg", None),
      ("שמן דגים", 704, "mg", None), ("חומצה פולית", 400, "mcg", None)], "brand_panel",
     "https://www.altman.co.il/shop/pregnancy/prenatal/omega-3-9-months/"),
    ("7290019444183", "altman", "אלטמן ויטמין C500 ליפוזומלי",
     "ויטמין C כנוגד חמצון; חשוב לתפקוד מערכת החיסון",
     [("ויטמין C (ascorbic acid)", 500, "mg", "ascorbic acid")], "brand_panel",
     "https://www.altman.co.il/shop/winter/vitamin-c/liposomal-vitamin-c500/"),

    # ---- Tier B: retailer/search snippet panels (WebSearch) ----
    ("7290015429245", "amorphicure", "אמורפיקיור pH מגנזיום קרבונט אמורפי 160",
     "מגנזיום לתפקוד תקין של השרירים ומערכת העצבים",
     [("מגנזיום (carbonate)", 160, "mg", "carbonate")], "search_panel",
     "https://www.tevagil.co.il/items/7144413"),
    ("0033984003101", "solgar", "סולגר ביוטין 1000 מק\"ג",
     "תומך בבריאות העור, השיער והציפורניים",
     [("ביוטין (Biotin)", 1000, "mcg", None)], "search_panel",
     "https://www.vitaminglobal.com/biotin-1000-mcg-50-vegetable-capsules-solgar-p-4733-c-7_21_26.html"),
    ("7290013465535", "supherb", "סופהרב קפאין 200 מ\"ג",
     "קפאין לערנות ולפני פעילות גופנית אירובית",
     [("קפאין (Caffeine)", 200, "mg", None)], "search_panel",
     "https://www.supherb.co.il/product/קפאין/"),
    ("7290012760204", "supherb", "סופהרב אומגה 3 בד\"ץ 1000 מ\"ג",
     "אומגה 3 לתמיכה בבריאות הלב וכלי הדם",
     [("EPA", 180, "mg", None), ("DHA", 120, "mg", None),
      ("שמן דגים", 1000, "mg", None)], "search_panel",
     "https://www.tevazol.co.il/items/1348673"),
    ("7290118814061", "supherb", "סופהרב ברזל 9 חודשים 30 מ\"ג",
     "ברזל לתמיכה בהריון ולמניעת עייפות ותשישות (חוסר ברזל)",
     [("ברזל (iron bisglycinate / Ferrochel)", 30, "mg", "bisglycinate")], "search_panel",
     "https://www.supherb.co.il/product/ברזל-9-חודשים-בדץ/"),
    ("7290017243450", "supherb", "סופהרב ויטמין B12 + חומצה פולית 1000 מק\"ג",
     "ויטמין B12 וחומצה פולית ליצירת תאי דם אדומים ולהפחתת עייפות",
     [("ויטמין B12 (methylcobalamin)", 1000, "mcg", "methylcobalamin"),
      ("חומצה פולית (methylfolate)", 400, "mcg", None)], "search_panel",
     "https://www.supherb.co.il/product/ויטמין-b12-חומצה-פולית-למציצה/"),
    ("7290012056741", "tink", "טינק ברזל נוח 36 מ\"ג",
     "ברזל ביסגליצינאט לספיגה גבוהה; להפחתת עייפות (חוסר ברזל)",
     [("ברזל (iron bisglycinate)", 36, "mg", "bisglycinate"),
      ("ויטמין C", 100, "mg", None)], "search_panel",
     "https://www.tinc.co.il/web/?pagetype=9&itemid=237171"),
    ("7290017399638", "floris", "פלוריש ויטמין C טריו 50 מ\"ג לעיסה",
     "ויטמין C לתפקוד מערכת החיסון",
     [("ויטמין C", 50, "mg", None), ("ויטמין D", None, "IU", None),
      ("אבץ (zinc)", 3.5, "mg", None)], "search_panel",
     "https://medi-pharm.co.il/catalog.asp?prodid=2003719"),

    # ---- Tier B: name-derived single-active (dose from SP item name) ----
    ("7290001943700", "other", "הדס פול-מאג 600 מגנזיום",
     "מגנזיום להפחתת עייפות ותשישות",
     [("מגנזיום", 600, "mg", None)], "name_derived", None),
    ("7290012497643", "other", "ויטמין C500 לבליעה",
     "ויטמין C לתפקוד מערכת החיסון",
     [("ויטמין C", 500, "mg", None)], "name_derived", None),
    ("7290113828728", "life", "לייף ויטמין סי 500 לבליעה",
     "ויטמין C לתפקוד מערכת החיסון",
     [("ויטמין C", 500, "mg", None)], "name_derived", None),
    ("7290103449421", "life", "לייף ויטמין D-400 כמוסות רכות",
     "ויטמין D לספיגת סידן ולשמירה על בריאות העצם",
     [("ויטמין D3", 400, "IU", None)], "name_derived", None),
]

for bc, brand, name, claim, actives, method, url in ROWS:
    obj = {
        "url": url or f"name_derived://super_pharm/{bc}",
        "source_id": f"{brand}:{bc}",
        "acquisition_method": method,
        "json": {
            "brand": brand, "product_name": name, "barcode": bc,
            "serving_size": "1 unit", "servings_per_container": None,
            "ingredient_list_raw": None, "primary_claim": claim,
            "proprietary_blend": False,
            "actives": [{"ingredient": i, "amount": a, "unit": u, "form": f}
                        for (i, a, u, f) in actives],
        },
    }
    (CACHE / f"{bc}.json").write_text(json.dumps(obj, ensure_ascii=False, indent=2),
                                      encoding="utf-8")
print(f"wrote {len(ROWS)} cache panels to {CACHE}")
