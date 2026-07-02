"""
TASK-397 Track A, Step 2 — Finalize rescrape_results.json with documented findings.

Documented reachability findings:
- Victory: WordPress site (not WooCommerce). Home page reachable (68KB). Product search
  returns generic 38KB search-results shell with NO product or nutrition data in HTML.
  WooCommerce REST API (/wp-json/wc/v3/) returns 404 — not enabled publicly.
  No nutrition accessible without JS rendering.

- Rami Levy: Nuxt.js SPA. Root domain reachable (635KB SSR HTML). Product pages
  /he/online/product/{barcode} return 200 with the barcode in route path, but:
  (a) No product-specific content in SSR HTML — all product data loaded client-side.
  (b) Nutrition data served by www-api.rami-levy.co.il which requires OAuth authentication.
  (c) The "שומן" found in SSR pages is a UI i18n label ("אחוז שומן") at the same
      offset in every page — NOT a nutrition value for the specific product.
  Both authenticated API and client-side rendering required — not accessible one-shot.

- Yochananof: Blocked/unreachable (connection failed on probe).

Result: 0/22 barcodes recovered. All 22 are discard_candidate=true.
The 9 priority-implausible barcodes remain unresolvable via secondary-retailer scrape
in this environment without browser automation + auth.
"""
from __future__ import annotations
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

OUT_DIR = Path(__file__).parent

IMPLAUSIBLE = {
    "2079033", "2079217", "6451484", "7290014321168",
    "7290016245325", "7290016967074", "74252", "8434165658523", "96086000966"
}

SENTINEL_DATA = {
    "2079033":          {"name": "לחם דגנים לייט",               "kcal": 222.0, "kcal_gap": 56.2,  "priority": True},
    "2079217":          {"name": "לחם מחמצת שיפון+אגוזים",       "kcal": 259.0, "kcal_gap": 64.8,  "priority": True},
    "6451484":          {"name": "לחם מחמצת אגוזים צימוקים",      "kcal": 266.0, "kcal_gap": 54.6,  "priority": True},
    "7290014321168":    {"name": "לחם לס פרוס קיטו",              "kcal": 231.0, "kcal_gap": 104.8, "priority": True},
    "7290016245325":    {"name": "לחם טחינה פרוס",                "kcal": 192.0, "kcal_gap": 59.3,  "priority": True},
    "7290016967074":    {"name": "לחם אנג'ל חיטה מלאה",          "kcal": 242.0, "kcal_gap": 63.8,  "priority": True},
    "74252":            {"name": "קרקר שומשום אסם",               "kcal": 465.0, "kcal_gap": 146.8, "priority": True},
    "8434165658523":    {"name": "קרקר קרם קרקר",                 "kcal": 448.0, "kcal_gap": 129.8, "priority": True},
    "96086000966":      {"name": "קרקר כוסמין מלא ושומשום",       "kcal": 418.0, "kcal_gap": 111.8, "priority": True},
    "2079927":          {"name": "לחם דגנים מלא",                 "kcal": 242.0, "kcal_gap": 35.8,  "priority": False},
    "3054183":          {"name": "לחם שיפון מלא מסטמכר",         "kcal": 191.0, "kcal_gap": 30.8,  "priority": False},
    "3268252":          {"name": "לחם חיטה מלא לילדים",           "kcal": 221.0, "kcal_gap": 21.2,  "priority": False},
    "3268429":          {"name": "לחם ירוק מקמח מלא",             "kcal": 223.0, "kcal_gap": 26.8,  "priority": False},
    "481197":           {"name": "לחם מחמצת גרעינים",             "kcal": 220.0, "kcal_gap": 30.2,  "priority": False},
    "481203":           {"name": "לחם מחמצת קמח מלא",             "kcal": 227.0, "kcal_gap": 37.9,  "priority": False},
    "497044":           {"name": "לחם ברמן אקטיב",                "kcal": 233.0, "kcal_gap": 46.8,  "priority": False},
    "574370":           {"name": "לחם שיפון קל",                  "kcal": 198.0, "kcal_gap": 37.3,  "priority": False},
    "6451507":          {"name": "לחם מחמצת מכוסמין",             "kcal": 213.0, "kcal_gap": 21.6,  "priority": False},
    "7290018500460":    {"name": "לחם אנג'ל חצי מלא",            "kcal": 220.0, "kcal_gap": 20.5,  "priority": False},
    "7296073134442":    {"name": "קרקר פריך עם קמח שיפון",        "kcal": 376.0, "kcal_gap": 31.8,  "priority": False},
    "7296073134459":    {"name": "קרקר פריך בסגנון שוודי",        "kcal": 371.0, "kcal_gap": 31.9,  "priority": False},
    "96086000577":      {"name": "קרקר כוסמין אורגני",            "kcal": 380.0, "kcal_gap": 33.8,  "priority": False},
}

# Retailer reachability — documented findings
retailer_reachability = {
    "victory": {
        "reachable": True,
        "probe_bytes": 68285,
        "nutrition_accessible": False,
        "site_type": "WordPress",
        "block_reason": "WordPress site with no public WooCommerce REST API. Search page /?s={barcode} returns 38KB generic shell with no product data in HTML. Nutrition not server-rendered. WooCommerce API /wp-json/wc/v3/ returns 404 (not enabled). No nutrition accessible without JavaScript rendering.",
        "status": "reachable_but_nutrition_inaccessible",
        "urls_tried": [
            "https://www.victory.co.il/?s={barcode}",
            "https://www.victory.co.il/wp-json/wc/v3/products?sku={barcode}",
            "https://www.victory.co.il/wp-json/wc/v3/products?search={barcode}",
            "https://www.victory.co.il/wp-json/wp/v2/search?search={barcode}&type=post",
            "https://www.victory.co.il/api/v2/products/search?q={barcode}",
            "https://www.victory.co.il/umbraco/api/product/getbybarcode?barcode={barcode}",
        ],
    },
    "rami_levy": {
        "reachable": True,
        "probe_bytes": 635747,
        "nutrition_accessible": False,
        "site_type": "Nuxt.js SPA",
        "block_reason": "Nuxt.js SPA. Product pages /he/online/product/{barcode} return 200 (barcode in route path) but no product-specific content is server-rendered. All product data (nutrition, name, ingredients) is loaded client-side via authenticated API at www-api.rami-levy.co.il which returns 404 without OAuth credentials. The 'שומן' string found in all SSR pages is a UI i18n label ('אחוז שומן' = 'fat percentage') at a fixed offset in the translation bundle, NOT a product nutrition value. Requires browser automation + session authentication — not feasible one-shot.",
        "status": "reachable_but_nutrition_inaccessible",
        "authenticated_api_discovered": "https://www-api.rami-levy.co.il/api/v2/",
        "urls_tried": [
            "https://www.rami-levy.co.il/he/online/product/{barcode}",
            "https://www.rami-levy.co.il/he/online/search?q={barcode}",
            "https://www-api.rami-levy.co.il/api/v2/products/{barcode}",
            "https://www-api.rami-levy.co.il/api/v2/products/search?q={barcode}",
            "https://www-api.rami-levy.co.il/api/v3/site",
            "https://www.rami-levy.co.il/api/catalog?q={barcode}",
        ],
    },
    "yochananof": {
        "reachable": False,
        "probe_bytes": 0,
        "nutrition_accessible": False,
        "site_type": "unknown",
        "block_reason": "Connection failed on probe. Host unreachable from this environment.",
        "status": "blocked_or_unreachable",
    },
}

# Build products list
products = []
for barcode, info in SENTINEL_DATA.items():
    products.append({
        "barcode": barcode,
        "name_he": info["name"],
        "is_priority_implausible": info["priority"],
        "kcal_gap_from_prior_analysis": info["kcal_gap"],
        "secondary_retailer": None,
        "real_fat_g": None,
        "plausibility_pass": None,
        "plausibility_gap_kcal": None,
        "recovery_status": "not_found",
        "discard_candidate": True,
        "not_found_reason": "Both reachable retailers (Victory, Rami Levy) load nutrition data client-side via authenticated/JavaScript-rendered content; not accessible one-shot. Yochananof blocked. Per missing-data-discard rule: no fat recoverable = discard_candidate.",
        "retailer_attempts": [
            {
                "retailer": "victory",
                "outcome": "no_nutrition_in_html",
                "detail": "WordPress site. /?s={barcode} returns generic 38KB shell. No product nutrition in server-rendered HTML. WooCommerce API not public.".replace("{barcode}", barcode),
            },
            {
                "retailer": "rami_levy",
                "outcome": "no_nutrition_in_html",
                "detail": "Nuxt SPA. /he/online/product/{barcode} returns 200 but only route shell; nutrition served by authenticated API (www-api.rami-levy.co.il) — requires OAuth. SSR 'שומן' is UI label only.".replace("{barcode}", barcode),
            },
            {
                "retailer": "yochananof",
                "outcome": "blocked",
                "detail": "Host unreachable from this environment.",
            },
        ],
    })

# Counts
total = len(products)
recovered = sum(1 for p in products if p["recovery_status"] == "recovered")
discard = sum(1 for p in products if p["discard_candidate"])
priority_implausible = len(IMPLAUSIBLE)
priority_discard = sum(1 for p in products if p["is_priority_implausible"] and p["discard_candidate"])

feasibility_summary = (
    "Secondary-retailer fat re-scrape for bread corpus (9 priority implausible + 13 opportunistic, "
    "22 total sentinel products). "
    "Reachability: Victory (68KB home, reachable) and Rami Levy (636KB home, reachable) were probed; "
    "Yochananof was blocked/unreachable. "
    "However, both reachable retailers load nutrition data client-side via authenticated/JavaScript APIs "
    "that are not accessible without browser automation and session credentials: "
    "Victory is a WordPress site whose WooCommerce REST API is not publicly enabled (all search pages "
    "return generic 38KB shells with no product content); "
    "Rami Levy is a Nuxt.js SPA where product pages return route shells only — nutrition is fetched "
    "client-side from www-api.rami-levy.co.il which requires OAuth (returns 404 unauthenticated). "
    "The 'שומן' string found in Rami Levy SSR pages is a fixed i18n UI label, not a nutrition value. "
    "Result: 0/22 fat values recovered. All 22 products are discard_candidate=true per the "
    "missing-data-discard rule. No kcal-derived or estimated fat values were injected — "
    "all nulls are genuine one-shot misses. "
    "Recovery would require a headless-browser approach with session authentication — "
    "outside the scope of a one-shot EDPG-compliant scrape."
)

run_id = f"rescrape_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}"

results = {
    "task": "TASK-397",
    "track": "A",
    "step": 2,
    "run_id": run_id,
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "script_version": "1.1.0",
    "off_ban_note": "Open Food Facts is BANNED. All nutrition from direct retailer scrape only. No OFF data used.",
    "source_policy": "Direct product page scrape only. No kcal-derived fat injected. No estimated values.",
    "retailer_priority_order": ["victory", "rami_levy", "yochananof"],
    "retailer_reachability": retailer_reachability,
    "reachable_retailers": ["victory", "rami_levy"],
    "blocked_retailers": ["yochananof"],
    "nutrition_accessible_retailers": [],
    "feasibility_summary": feasibility_summary,
    "products": products,
    "counts": {
        "total_sentinel_barcodes": total,
        "priority_implausible": priority_implausible,
        "recovered_total": recovered,
        "recovered_plausibility_pass": 0,
        "recovered_plausibility_fail": 0,
        "not_found_total": total - recovered,
        "blocked_total": 0,
        "discard_candidate_total": discard,
        "priority_implausible_recovered": 0,
        "priority_implausible_discard_candidate": priority_discard,
    },
}

out = OUT_DIR / "rescrape_results.json"
out.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
sha256 = hashlib.sha256(out.read_bytes()).hexdigest()

print(f"Written: {out}")
print(f"SHA256: {sha256}")
print(f"\nCounts:")
for k, v in results["counts"].items():
    print(f"  {k}: {v}")
print(f"\nrun_id: {run_id}")
