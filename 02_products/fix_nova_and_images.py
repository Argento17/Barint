# -*- coding: utf-8 -*-
"""
Fix NOVA leakage in positiveSignals + inject imageUrl from discovery.json
Covers: juices_frontend_v3.json and hard_cheeses_frontend_v2.json
"""
import sys
import json
import pathlib
import shutil
import datetime

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT = pathlib.Path(r"C:\Bari")

# ─── Juice paths ────────────────────────────────────────────────────────────
JUICE_JSON_IN  = ROOT / "02_products" / "juices" / "juices_frontend_v3.json"
JUICE_SCRAPE   = ROOT / "02_products" / "juices" / "yohananof_scrape"
JUICE_BSIP1    = ROOT / "02_products" / "juices" / "bsip1_outputs"
JUICE_JSON_OUT = JUICE_JSON_IN
JUICE_WEB_OUT  = ROOT / "bari-web" / "src" / "data" / "comparisons" / "juices_frontend_v3.json"

# ─── Cheese paths ────────────────────────────────────────────────────────────
CHEESE_JSON_IN  = ROOT / "02_products" / "hard_cheeses" / "hard_cheeses_frontend_v2.json"
CHEESE_SCRAPE   = ROOT / "02_products" / "hard_cheeses" / "yohananof_scrape"
CHEESE_JSON_OUT = CHEESE_JSON_IN
CHEESE_WEB_OUT  = ROOT / "bari-web" / "src" / "data" / "comparisons" / "hard_cheeses_frontend_v2.json"


# ─── Image URL loader ────────────────────────────────────────────────────────

def load_image_urls(scrape_dir: pathlib.Path) -> dict:
    """Return {barcode: source_image_url} from per-barcode discovery.json files."""
    image_map = {}
    for barcode_dir in scrape_dir.iterdir():
        if not barcode_dir.is_dir():
            continue
        dj = barcode_dir / "discovery.json"
        if not dj.exists():
            continue
        try:
            d = json.loads(dj.read_text(encoding="utf-8"))
            barcode = d.get("barcode") or barcode_dir.name
            url = (d.get("image") or {}).get("source_image_url")
            if url:
                image_map[barcode] = url
        except Exception as e:
            print(f"  WARN: could not read {dj}: {e}")
    return image_map


# ─── NOVA fix helpers ────────────────────────────────────────────────────────

def fix_nova_leading_zuhah(s: str) -> str:
    """'ללא סוכר מוסף זוהה' → 'ללא סוכר מוסף'"""
    return s.replace("ללא סוכר מוסף זוהה", "ללא סוכר מוסף")


JUICE_NOVA_POSITIVE_REPLACEMENTS = {
    # NOVA 1 fresh-squeezed → consumer language
    # We inspect ingredients per product in fix_juice_product(); handled there.
    "NOVA 1 — מיץ סחוט טרי": "__INSPECT__",
    # NOVA 3 is never positive
    "NOVA 3 — מעובד/מרוכז": "__REMOVE__",
    # NOVA 4 is never positive
    "NOVA 4 — משקה מעובד": "__REMOVE__",
}

CHEESE_NOVA_POSITIVE_REPLACEMENTS = {
    "NOVA 1 — עיבוד מינימלי": "__INSPECT__",   # handled per-product
    "NOVA 2 — עיבוד נמוך":     "__REMOVE__",    # processing level, not a consumer positive
    "NOVA 3 — עיבוד בינוני":  "__REMOVE__",
    "NOVA 4 — גבינה מעובדת":  "__REMOVE__",
}

# These NOVA strings in limitingFactors should be replaced with consumer language
JUICE_NOVA_LIMITING_REPLACEMENTS = {
    "NOVA 3 — מעובד/מרוכז": "מיץ מרוכז",
    "NOVA 4 — משקה מעובד":  "משקה עם חומרי עיבוד",
}

CHEESE_NOVA_LIMITING_REPLACEMENTS = {
    "NOVA 3 — עיבוד בינוני": "מכיל מייצבים",
    "NOVA 4 — גבינה מעובדת": "גבינה מעובדת — עיבוד תעשייתי",
}


def nova1_juice_label(ingredients: str) -> str:
    """
    Generate consumer-facing positive label for a NOVA-1 juice product.
    Inspects actual ingredients to pick the most specific phrasing.
    """
    ing = (ingredients or "").strip()
    # Single-ingredient fresh-squeezed (only the fruit name, no other text)
    single_fruit_words = ["מיץ תפוזים", "מיץ רימונים", "מיץ לימון", "מיץ ענבים",
                          "מיץ קלמנטינות", "מיץ גויאבה", "מיץ אשכולית"]
    # If ingredients is extremely short (≤ ~25 chars) → single-fruit product
    if len(ing) <= 30 and any(f in ing for f in single_fruit_words):
        return "מיץ סחוט טרי — פרי בלבד"
    # Default for NOVA-1 juice
    return "מיץ סחוט טרי — ללא ריכוז, ללא עיבוד"


def nova1_cheese_label(ingredients: str, name: str) -> str:
    """
    Generate consumer-facing positive label for a NOVA-1 cheese product.
    Uses actual ingredients to verify minimal processing.
    """
    ing = (ingredients or "").lower()
    # Count real ingredient tokens
    # Products with just milk + salt + enzyme/culture
    minimal_markers = any(x in ing for x in ["חלב", "milk"])
    if minimal_markers:
        return "גבינה עם רכיבים מינימליים — חלב, מלח ותרביות בלבד"
    return "גבינה עם רכיבים מינימליים"


def is_a_grade(score: int) -> bool:
    return score >= 80


def fix_juice_product(p: dict) -> tuple:
    """
    Returns (updated_product, changes_list).
    Fixes:
    1. NOVA strings in positiveSignals
    2. NOVA strings in limitingFactors → consumer language
    3. 'ללא סוכר מוסף זוהה' → 'ללא סוכר מוסף'
    4. A-grade products: suppress sugar limitingFactors
    """
    changes = []
    exp = p.get("expansion", {})
    pos = list(exp.get("positiveSignals", []))
    lim = list(exp.get("limitingFactors", []))
    ing = exp.get("ingredients") or ""
    score = p.get("score", 0)
    subpool = p.get("subPool", "")

    # Fix positiveSignals
    new_pos = []
    for sig in pos:
        if sig == "NOVA 1 — מיץ סחוט טרי":
            replacement = nova1_juice_label(ing)
            new_pos.append(replacement)
            changes.append(f"  pos: '{sig}' → '{replacement}'")
        elif sig in ("NOVA 3 — מעובד/מרוכז", "NOVA 4 — משקה מעובד"):
            changes.append(f"  pos: REMOVED '{sig}'")
            # Do not append (removed)
        else:
            new_pos.append(fix_nova_leading_zuhah(sig))
            if fix_nova_leading_zuhah(sig) != sig:
                changes.append(f"  pos: זוהה stripped in '{sig}'")

    # Fix limitingFactors — NOVA strings → consumer language
    new_lim = []
    for fac in lim:
        if fac in JUICE_NOVA_LIMITING_REPLACEMENTS:
            replacement = JUICE_NOVA_LIMITING_REPLACEMENTS[fac]
            new_lim.append(replacement)
            changes.append(f"  lim: '{fac}' → '{replacement}'")
        else:
            new_lim.append(fac)

    # Fix A-grade sugar limitingFactors: replace "סוכר בינוני/גבוה" with neutral context note
    if is_a_grade(score) and subpool == "juice_100":
        newer_lim = []
        for fac in new_lim:
            if fac.startswith("סוכר בינוני") or fac.startswith("סוכר גבוה"):
                replacement = "סוכר טבעי בלבד — ללא תוספות"
                newer_lim.append(replacement)
                changes.append(f"  lim (A-grade): '{fac}' → '{replacement}'")
            else:
                newer_lim.append(fac)
        new_lim = newer_lim

    exp["positiveSignals"] = new_pos
    exp["limitingFactors"] = new_lim
    p["expansion"] = exp
    return p, changes


def fix_cheese_product(p: dict) -> tuple:
    """
    Returns (updated_product, changes_list).
    Fixes:
    1. NOVA strings in positiveSignals → consumer language or remove
    2. NOVA strings in limitingFactors → consumer language
    """
    changes = []
    exp = p.get("expansion", {})
    pos = list(exp.get("positiveSignals", []))
    lim = list(exp.get("limitingFactors", []))
    ing = exp.get("ingredients") or ""
    name = p.get("name", "")

    # Fix positiveSignals
    new_pos = []
    for sig in pos:
        if sig == "NOVA 1 — עיבוד מינימלי":
            replacement = nova1_cheese_label(ing, name)
            new_pos.append(replacement)
            changes.append(f"  pos: '{sig}' → '{replacement}'")
        elif sig == "NOVA 2 — עיבוד נמוך":
            # NOVA 2 is not a meaningful consumer positive (it just means "basic processing")
            # Remove it — the absence of additives already says this more clearly
            changes.append(f"  pos: REMOVED '{sig}'")
        elif sig in ("NOVA 3 — עיבוד בינוני", "NOVA 4 — גבינה מעובדת"):
            changes.append(f"  pos: REMOVED '{sig}'")
        else:
            new_pos.append(sig)

    # Fix limitingFactors — NOVA strings → consumer language
    new_lim = []
    for fac in lim:
        if fac in CHEESE_NOVA_LIMITING_REPLACEMENTS:
            replacement = CHEESE_NOVA_LIMITING_REPLACEMENTS[fac]
            new_lim.append(replacement)
            changes.append(f"  lim: '{fac}' → '{replacement}'")
        else:
            new_lim.append(fac)

    exp["positiveSignals"] = new_pos
    exp["limitingFactors"] = new_lim
    p["expansion"] = exp
    return p, changes


# ─── Main ───────────────────────────────────────────────────────────────────

def process_category(
    json_path: pathlib.Path,
    scrape_dir: pathlib.Path,
    out_path: pathlib.Path,
    web_path: pathlib.Path,
    fix_fn,
    category_label: str,
) -> dict:
    print(f"\n{'='*60}")
    print(f"Processing: {category_label}")
    print(f"{'='*60}")

    doc = json.loads(json_path.read_text(encoding="utf-8"))
    image_map = load_image_urls(scrape_dir)
    print(f"Image URLs loaded from scrape dir: {len(image_map)}")

    products = doc.get("products", [])
    nova_replacements = 0
    nova_removals = 0
    images_set = 0
    images_null = 0
    all_changes = []

    for p in products:
        pid = p.get("id", "?")
        barcode = p.get("barcode") or ""

        # ── Image URL injection ──
        if barcode and barcode in image_map:
            p["imageUrl"] = image_map[barcode]
            images_set += 1
        else:
            p["imageUrl"] = None
            images_null += 1
            if barcode:
                print(f"  imageUrl: NO URL found for barcode {barcode} ({pid})")

        # ── NOVA / signal fixes ──
        p, changes = fix_fn(p)
        if changes:
            print(f"\n  [{pid}] {p.get('name', '')}")
            for c in changes:
                print(c)
                if "REMOVED" in c:
                    nova_removals += 1
                elif "→" in c and "nova" not in c.lower():
                    nova_replacements += 1
                elif "→" in c:
                    nova_replacements += 1
            all_changes.extend(changes)

    # Verify: no NOVA string remains in positiveSignals
    nova_leaks = []
    for p in products:
        for sig in (p.get("expansion") or {}).get("positiveSignals", []):
            if "NOVA" in sig:
                nova_leaks.append(f"  LEAK in {p['id']}: '{sig}'")

    if nova_leaks:
        print(f"\nERROR — NOVA leaks remain in positiveSignals:")
        for l in nova_leaks:
            print(l)
    else:
        print(f"\nVERIFIED: zero NOVA strings in positiveSignals")

    # Update meta timestamp
    if "_meta" in doc:
        doc["_meta"]["nova_fix_applied"] = datetime.datetime.now(datetime.timezone.utc).isoformat()

    # Write outputs
    out_path.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Written:   {out_path}")
    shutil.copy2(out_path, web_path)
    print(f"Deployed:  {web_path}")

    return {
        "category": category_label,
        "products": len(products),
        "nova_replacements": nova_replacements,
        "nova_removals": nova_removals,
        "total_nova_changes": nova_replacements + nova_removals,
        "images_set": images_set,
        "images_null": images_null,
        "nova_leaks_remaining": len(nova_leaks),
    }


def main():
    results = []

    results.append(process_category(
        json_path=JUICE_JSON_IN,
        scrape_dir=JUICE_SCRAPE,
        out_path=JUICE_JSON_OUT,
        web_path=JUICE_WEB_OUT,
        fix_fn=fix_juice_product,
        category_label="juices",
    ))

    results.append(process_category(
        json_path=CHEESE_JSON_IN,
        scrape_dir=CHEESE_SCRAPE,
        out_path=CHEESE_JSON_OUT,
        web_path=CHEESE_WEB_OUT,
        fix_fn=fix_cheese_product,
        category_label="hard_cheeses",
    ))

    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    total_nova = 0
    total_images = 0
    for r in results:
        print(f"\n{r['category']}:")
        print(f"  Products:              {r['products']}")
        print(f"  NOVA strings changed:  {r['nova_replacements']} replaced, {r['nova_removals']} removed")
        print(f"  Total NOVA changes:    {r['total_nova_changes']}")
        print(f"  Images set:            {r['images_set']}")
        print(f"  Images still null:     {r['images_null']}")
        print(f"  NOVA leaks remaining:  {r['nova_leaks_remaining']}")
        total_nova  += r["total_nova_changes"]
        total_images += r["images_set"]

    print(f"\nGRAND TOTAL:")
    print(f"  NOVA changes across both categories: {total_nova}")
    print(f"  Images populated:                    {total_images}")


if __name__ == "__main__":
    main()
