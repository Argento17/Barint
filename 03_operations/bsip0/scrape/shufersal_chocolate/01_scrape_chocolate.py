"""
BSIP0 Shufersal — Chocolate shelf scraper (TASK-362, pages 3+4).

Reuses the PROVEN bar engine (shufersal_snack_bars/01_scrape_snack_bars.py) by
overriding its query/filter globals — no logic duplicated. Pulls the chocolate
shelf broadly (countline chocolate bars + chocolate tablets). The countline-vs-
tablet split is a downstream classify step (like classify_bar for protein bars).

OFF banned. Output: 02_products/chocolate/bsip0_outputs/choc_bsip0_raw_<ts>.json
"""
from __future__ import annotations
import importlib.util, json, pathlib, sys, datetime, os

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = pathlib.Path(r"C:\Bari")
BAR = ROOT / "03_operations" / "bsip0" / "scrape" / "shufersal_snack_bars" / "01_scrape_snack_bars.py"

spec = importlib.util.spec_from_file_location("bar_engine", BAR)
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)

# cooldown to let any Shufersal rate-limit reset (the first run got 0 results
# right after the heavy bar scrape), and slow the engine's per-request pacing.
import time as _t
_cooldown = int(os.environ.get("CHOC_COOLDOWN", "0"))
if _cooldown:
    print(f"cooldown {_cooldown}s before chocolate scrape...", flush=True)
    _t.sleep(_cooldown)
b.PRODUCT_PAGE_DELAY = 1.1

# ── override category-specific globals (the engine reads these at call time) ──
b.MAX_PRODUCTS = int(os.environ.get("CHOC_MAX", "150"))
b.QUERY_PLAN = [
    ("שוקולד פרה", "mainstream"),
    ("טבלת שוקולד", "mainstream"),
    ("שוקולד מריר", "mainstream"),
    ("שוקולד חלב", "mainstream"),
    ("פסק זמן", "mainstream"),
    ("קיט קט", "mainstream"),
    ("חטיף שוקולד", "mainstream"),
    ("מקופלת", "specialty"),
    ("קליק שוקולד", "specialty"),
    ("טוויקס", "specialty"),
    ("סניקרס", "specialty"),
    ("מארס שוקולד", "specialty"),
    ("לינדט", "specialty"),
    ("מילקה", "specialty"),
    ("טובלרון", "specialty"),
    ("כיף כף", "specialty"),
    ("שוקולד ממולא", "specialty"),
]
b.INCLUDE_SIGNALS = [
    "שוקולד", "פסק זמן", "קיט קט", "טוויקס", "סניקרס", "מארס", "באונטי",
    "מקופלת", "קליק", "לינדט", "כיף כף", "מילקה", "milka", "טובלרון",
    "toblerone", "טבלת", "chocolate",
]
b.EXCLUDE_SIGNALS = [
    # drinks / spreads / baking / desserts that share the word שוקולד
    "משקה", "שוקו ל", "שתיה", "שתייה", "ממרח", "נוטלה", "nutella",
    "עוגי", "עוגת", "עוגה", "גלידה", "קרטיב", "שלגון", "אבקת", "קקאו לאפיה",
    "קורנפלקס", "דגני בוקר", "חלב מרוכז", "ציפוי", "פתיתי שוקולד",
    "סירופ", "רוטב", "מוס", "פודינג", "קרם ממרח", "מייפל",
    # savory / non-chocolate
    "במבה", "ביסלי", "פופקורן",
]

ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%S")
out_dir = ROOT / "02_products" / "chocolate" / "bsip0_outputs"
out_dir.mkdir(parents=True, exist_ok=True)
raw_path = out_dir / f"choc_bsip0_raw_{ts}.json"
log_path = out_dir / f"choc_bsip0_log_{ts}.txt"

products, notes = b.run_acquisition(verbose=True)
raw_path.write_text(json.dumps(products, ensure_ascii=False, indent=2), encoding="utf-8")
log_path.write_text("\n".join(notes), encoding="utf-8")

n_nutr = sum(1 for p in products if p["nutrition"]["energy_kcal_raw"] or p["nutrition"]["carbs_raw"])
n_ingr = sum(1 for p in products if p["ingredients_raw"])
print(f"\n=== CHOCOLATE DONE === {len(products)} products | nutrition {n_nutr} | ingredients {n_ingr}")
print("raw:", raw_path)
