"""
_blast_radius_check.py
======================
Scan all products in matrix_gold_set_v2.json (67 products) AND the broader
bread corpus for products where:
  - 'refined_wheat_flour' or any marker label appears both at a top-level record
    AND as a sub-record inside a composite parent
  - The sub-record wins the dedup race (i.e., replaces the top-level stated_pct
    with a position-weight fallback)

The bug mechanism:
  1. Reader emits a sub-record for 'קמח חיטה לבן' inside a parent composite
     (e.g. מחמצת חיטה לבן 18% (קמח חיטה לבן, מים))
  2. Sub-record has: position = parent_outer_pos + sub_pos - 1 (e.g. 3)
                     stated_pct = None (no pct inside the sub-composite)
  3. Top-level record has: stated_pct = 40.0 at position 1
  4. Dedup compares ew_new vs ew_old:
     - ew_old (top-level, stated_pct=40) = 0.40
     - ew_new (sub-record, stated_pct=None, pos=3) = pos_weight(3) = 0.68
  5. 0.68 > 0.40 -> REPLACE: sub-record wins, stated_pct becomes None, pos=3
  6. refined_wheat_flour gets base_w = pos_weight(3) = 0.68 (too high)
     instead of the correct stated_pct=40% = 0.40

Read-only. No edits to engine.
"""
import sys
import json
import re
from pathlib import Path

sys.path.insert(0, r"C:\Bari\03_operations\bsip2\proto_v0\analysis")
from structured_ingredient_reader import parse_ingredients, is_unparseable, _extract_groups

# Position-weight curve
def _pos_weight(pos):
    if pos is None: return 0.12
    if pos == 1:    return 1.00
    if pos == 2:    return 0.82
    if pos == 3:    return 0.68
    if pos == 4:    return 0.55
    if pos == 5:    return 0.44
    if pos == 6:    return 0.35
    if pos == 7:    return 0.28
    if pos == 8:    return 0.22
    if pos == 9:    return 0.17
    if pos == 10:   return 0.13
    if pos <= 15:   return max(0.08, 0.13 * (0.85 ** (pos - 10)))
    return 0.08

# Full marker set (identical to probe)
MARKERS = [
    (r"קמח חיטה מלאה?", "whole_wheat_flour", "whole"),
    (r"חיטה מלאה", "whole_wheat_grain", "whole"),
    (r"קמח (?:חיטת )?כוסמין מלא", "whole_spelt_flour", "whole"),
    (r"כוסמין מלא", "whole_spelt_grain", "whole"),
    (r"קמח שיבולת שועל מלא", "whole_oat_flour", "whole"),
    (r"שיבולת שועל מלאה?", "whole_oat", "whole"),
    (r"פתיתי שיבולת שועל מלאה?|פתיתי שיבולת שועל מלאים", "whole_oat_flakes", "whole"),
    (r"קמח שיפון מלא", "whole_rye_flour", "whole"),
    (r"שיפון מלא", "whole_rye_grain", "whole"),
    (r"קמח תירס מלא", "whole_corn_flour", "whole"),
    (r"קמח שעורה מלא", "whole_barley_flour", "whole"),
    (r"אורז מלא|קמח(?:\s+מ)?אורז מלא", "whole_rice", "whole"),
    (r"קינואה(?:\s+מלאה)?", "quinoa", "whole"),
    (r"כוסמת", "buckwheat", "whole"),
    (r"גריסי שיבולת שועל", "oat_groats", "whole"),
    (r"שיבולת שועל קלופה", "hulled_oats", "whole"),
    (r"שיבולת שועל(?!\s+מלאה?)(?!\s+מלאים)", "oat_flakes_plain", "whole"),
    (r"לתת שעורה|מיצוי לתת שעורה", "barley_malt", "whole"),
    (r"אגוז(?:י)?\s+(?:פקאן|לוז|מלך|מקדמיה|ברזיל)|אגוזים", "nuts", "whole"),
    (r"שקד(?:ים)?", "almonds", "whole"),
    (r"בוטנ(?:ים|ות)?", "peanuts", "whole"),
    (r"פיסטוק(?:ים)?", "pistachios", "whole"),
    (r"קשיו", "cashews", "whole"),
    (r"גרעיני?\s+(?:חמנ(?:ייה|יה)|דלעת|פשתן)", "seeds_specific", "whole"),
    (r"גרעינים", "seeds_generic", "whole"),
    (r"שומשום(?!\s+לבן)", "sesame_seeds", "whole"),
    (r"זרעי?\s+צ'יה|צ'יה", "chia_seeds", "whole"),
    (r"גרעיני פשתן|פשתן", "flax_seeds", "whole"),
    (r"עדשים", "lentils", "whole"),
    (r"חומוס(?!\s+שחור)", "chickpeas", "whole"),
    (r"תמר(?:ים)?", "dates", "whole"),
    (r"צימוקים", "raisins", "whole"),
    (r"מחמצת", "sourdough_starter", "whole"),
    (r"חמאה(?!\s+קקאו)(?!\s+שמן)", "butter_dairy", "whole"),
    (r"שמן זית", "olive_oil", "whole"),
    (r"טחינה|ממרח שומשום", "tahini", "whole"),
    (r"קמח כוסמין לבן", "white_spelt_flour", "refined"),
    (r"קמח חיטה(?!\s+מלאה?)(?!\s+מלא)", "refined_wheat_flour", "refined"),
    (r"גריסי תירס", "corn_grits", "refined"),
    (r"קמח תירס(?!\s+מלא)", "corn_flour_refined", "refined"),
    (r"סמולינה(?:\s+מתירס)?", "semolina", "refined"),
    (r"קמח אורז(?!\s+מלא)", "rice_flour_refined", "refined"),
    (r"אורז לבן", "white_rice", "refined"),
    (r"עמילן תירס", "corn_starch", "refined"),
    (r"עמילן חיטה", "wheat_starch", "refined"),
    (r"עמילן אורז", "rice_starch", "refined"),
    (r"עמילן(?!\s+תירס)(?!\s+חיטה)(?!\s+אורז)", "generic_starch", "refined"),
    (r"(?<!\S)סוכר(?!\s+קנים\s+אורגני)", "sugar", "refined"),
    (r"סירופ\s+גלוקוז(?:-פרוקטוז)?|סירופ\s+גלוקוזה(?:-פרוקטוזה)?", "glucose_syrup", "refined"),
    (r"סירופ\s+סוכר\s+אינברטי|סוכר\s+אינברטי", "inverted_sugar", "refined"),
    (r"גלוקוז(?!\s+מיובש)(?![א-ת])", "glucose", "refined"),
    (r"דקסטרוז|דקסטרוזה", "dextrose", "refined"),
    (r"דקסטרין", "dextrin", "refined"),
    (r"פרוקטוז", "fructose", "refined"),
    (r"מלטודקסטרין", "maltodextrin", "refined"),
    (r"שמן דקל(?!ים)(?!\s+אדום)", "palm_oil", "refined"),
    (r"שמן דקלים", "palm_oil_pl", "refined"),
    (r"שמנים\s+צמחיים", "veg_oils_pl", "refined"),
    (r"שמן\s+צמחי(?!ים)", "veg_oil_sg", "refined"),
    (r"שומן\s+צמחי", "hydrogenated_veg_fat", "refined"),
    (r"מרגרינה", "margarine", "refined"),
    (r"שמן\s+קוקוס", "coconut_oil", "refined"),
]

def _name_only_text(record):
    raw = record["raw"]
    if not record.get("has_own_sub"):
        return raw
    groups = _extract_groups(raw)
    if not groups:
        return raw
    return raw[:groups[0]["start"]].strip()

def find_dedup_inversions(text, barcode="?", name="?"):
    """
    Returns list of (label, top_level_ew, sub_ew, top_pos, top_stated, sub_pos, sub_stated)
    for any label where a sub-record wins the dedup race over a top-level record with stated_pct.
    """
    if not text or is_unparseable(text):
        return []

    records = parse_ingredients(text)

    # Collect all candidate marker hits per record
    all_hits = []
    for record in records:
        text_nm = _name_only_text(record)
        pos = record.get("position")
        stated = record.get("effective_pct") if record.get("effective_pct") is not None else record.get("stated_pct")
        is_sub = record.get("is_sub", False)

        for pattern, label, grain_class in MARKERS:
            if re.search(pattern, text_nm, re.IGNORECASE):
                ew = stated / 100.0 if stated is not None else _pos_weight(pos)
                all_hits.append({
                    "label": label,
                    "class": grain_class,
                    "position": pos,
                    "stated_pct": stated,
                    "ew": ew,
                    "is_sub": is_sub,
                    "record_raw": record.get("raw", "")[:80],
                })

    # Find cases where a label appears multiple times AND the sub wins
    from collections import defaultdict
    by_label = defaultdict(list)
    for h in all_hits:
        by_label[h["label"]].append(h)

    inversions = []
    for label, hits in by_label.items():
        if len(hits) < 2:
            continue
        # Simulate the dedup race
        winner = hits[0]
        losers = []
        for h in hits[1:]:
            if h["ew"] > winner["ew"]:
                losers.append(winner)
                winner = h
            else:
                losers.append(h)

        # Check if a sub-record beat a top-level record that had stated_pct
        top_level_with_stated = [h for h in losers if not h["is_sub"] and h["stated_pct"] is not None]
        if top_level_with_stated and winner["stated_pct"] is None:
            inversions.append({
                "label": label,
                "winner": winner,
                "beaten_top_level": top_level_with_stated,
                "all_hits": hits,
            })

    return inversions


# Load gold set
gold_path = r"C:\Bari\03_operations\bsip2\proto_v0\analysis\matrix_gold_set_v2.json"
with open(gold_path, encoding="utf-8") as f:
    gold = json.load(f)

out = []
out.append("=== DEDUP INVERSION SCAN ===")
out.append("Pattern: sub-record wins dedup race over top-level stated_pct record")
out.append(f"Gold set: {len(gold['products'])} products")
out.append("")

affected_gold = []
for p in gold["products"]:
    bc = p["barcode"]
    name = p.get("name_he", "")
    text = p.get("ingredients_text_he", "")
    inversions = find_dedup_inversions(text, bc, name)
    if inversions:
        affected_gold.append({"barcode": bc, "name": name, "inversions": inversions, "tier": p["tier"]})
        out.append(f"AFFECTED: {bc} ({name}) tier={p['tier']}")
        for inv in inversions:
            top = inv["beaten_top_level"][0]
            winner = inv["winner"]
            out.append(f"  Label: {inv['label']}")
            out.append(f"    WINNER: pos={winner['position']} stated={winner['stated_pct']} ew={winner['ew']:.4f} is_sub={winner['is_sub']}")
            out.append(f"    LOSER (top-level with stated_pct): pos={top['position']} stated={top['stated_pct']} ew={top['ew']:.4f}")
            out.append(f"    Effect: position-weight {winner['ew']:.4f} used instead of stated {top['ew']:.4f}")
            out.append(f"    Winner record: {winner['record_raw'][:80]}")

out.append(f"\nTotal affected in gold set (67): {len(affected_gold)}")

# Also scan the broader bread corpus (bsip2 outputs and real_bread_retail_003_v1)
out.append("\n=== BROADER BREAD CORPUS SCAN ===")
bread_paths = [
    r"C:\Bari\02_products\bread_retail_003\real_bread_retail_003_v1_20260525T194532_bsip0_raw.json",
]
bread_affected = []
for bp in bread_paths:
    bpath = Path(bp)
    if not bpath.exists():
        out.append(f"Not found: {bp}")
        continue
    with open(bpath, encoding="utf-8") as f:
        bread_data = json.load(f)

    # Try common structures
    products = []
    if isinstance(bread_data, list):
        products = bread_data
    elif "products" in bread_data:
        products = bread_data["products"]
    elif "items" in bread_data:
        products = bread_data["items"]
    else:
        # Try to find ingredient text fields
        out.append(f"  {bp}: unknown structure, keys={list(bread_data.keys())[:5]}")
        continue

    out.append(f"  {bpath.name}: {len(products)} products")
    for p in products:
        bc = p.get("barcode", p.get("id", "?"))
        name = p.get("name_he", p.get("name", "?"))
        # Try various ingredient text field names
        text = (p.get("ingredients_text_he") or p.get("ingredients_he") or
                p.get("ingredients") or p.get("ingredient_text") or "")
        if not text:
            continue
        inversions = find_dedup_inversions(str(text), str(bc), str(name))
        if inversions:
            bread_affected.append({"barcode": bc, "name": name, "inversions": inversions})
            out.append(f"  AFFECTED: {bc} ({str(name)[:40]})")
            for inv in inversions:
                top = inv["beaten_top_level"][0]
                winner = inv["winner"]
                out.append(f"    Label: {inv['label']}")
                out.append(f"    WINNER: pos={winner['position']} ew={winner['ew']:.4f} is_sub={winner['is_sub']}")
                out.append(f"    LOSER (stated_pct): pos={top['position']} stated={top['stated_pct']} ew={top['ew']:.4f}")

out.append(f"\nTotal affected in broader bread corpus: {len(bread_affected)}")

# Check pairs gate: does any affected product sit in a T3 gate pair?
out.append("\n=== GATE-PAIR IMPACT CHECK ===")
if "ranking_pairs_T3" in gold:
    pair_barcodes = set()
    for pair in gold["ranking_pairs_T3"]:
        pair_barcodes.add(pair["higher"])
        pair_barcodes.add(pair["lower"])

    for prod in affected_gold:
        if prod["barcode"] in pair_barcodes:
            # Find the pair
            for pair in gold["ranking_pairs_T3"]:
                if prod["barcode"] in (pair["higher"], pair["lower"]):
                    out.append(f"  GATE PAIR AFFECTED: {prod['barcode']} ({prod['name']}) in pair {pair['id']}")
                    out.append(f"    pair: {pair['higher']} vs {pair['lower']}")
                    out.append(f"    reason: {pair.get('reason', '')[:80]}")

# Confirm the fix direction
out.append("\n=== PROPOSED FIX (description only — not implemented) ===")
out.append("The dedup comparator in extract_all_markers_v4() uses effective_weight:")
out.append("  ew = stated_pct/100 if stated_pct else pos_weight(position)")
out.append("This means pos_weight(3)=0.68 beats stated_pct=40%=0.40.")
out.append("The fix: stated_pct records should ALWAYS beat position-weight records,")
out.append("regardless of relative numeric magnitude.")
out.append("Corrected dedup rule:")
out.append("  1. If only one has stated_pct -> that wins unconditionally")
out.append("  2. If both have stated_pct -> higher stated_pct wins")
out.append("  3. If neither has stated_pct -> higher pos_weight wins")
out.append("This preserves the original intent (use stated_pct when available)")
out.append("and prevents sub-records from displacing parent top-level stated_pcts.")

output_path = r"C:\Bari\03_operations\bsip2\proto_v0\analysis\_blast_radius_output.txt"
with open(output_path, "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print(f"Written to {output_path}")
print(f"Gold set affected: {len(affected_gold)}")
print(f"Their barcodes: {[a['barcode'] for a in affected_gold]}")
