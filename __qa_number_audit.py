# -*- coding: utf-8 -*-
"""Comprehensive superlative + number audit for juices v3."""
import json, re, sys

with open(r"C:\Bari\bari-web\src\data\comparisons\juices_frontend_v3.json", encoding="utf-8") as f:
    data = json.load(f)

products = data["products"]
meta = data["_meta"]

# ---- Build lookup structures ------------------------------------------------
by_id = {p["id"]: p for p in products}
grade_dist = meta["grade_distribution"]

scores = {p["id"]: p["score"] for p in products}
grades = {p["id"]: p["grade"] for p in products}
sugars = {p["id"]: p.get("sugarPer100ml") for p in products}
kcals = {p["id"]: p.get("kcalPer100ml") for p in products}

a_products = [p for p in products if p["grade"] == "A"]
d_products = [p for p in products if p["grade"] == "D"]
e_products = [p for p in products if p["grade"] == "E"]

results = []

def chk(pid, field, claim, truth, status, detail=""):
    results.append({"pid": pid, "field": field, "claim": claim,
                    "truth": truth, "status": status, "detail": detail})

print("=" * 70)
print("GRADE DISTRIBUTION")
print(f"  meta says A={grade_dist.get('A')}, D={grade_dist.get('D')}, E={grade_dist.get('E')}")
actual_a = sum(1 for p in products if p["grade"] == "A")
actual_d = sum(1 for p in products if p["grade"] == "D")
actual_e = sum(1 for p in products if p["grade"] == "E")
print(f"  actual A={actual_a}, D={actual_d}, E={actual_e}")

print()
print("=" * 70)
print("SCORE DISTRIBUTION")
for p in sorted(products, key=lambda x: x["score"], reverse=True):
    print(f"  {p['id']} {p['grade']} score={p['score']} sugar={p.get('sugarPer100ml')} kcal={p.get('kcalPer100ml')}")

print()
print("=" * 70)
print("KEY CLAIM AUDITS")

# --- jc-017: "הפרש של 60 נקודות בין מוצר זה לסחוטי ה-A" ---
pid = "jc-017"
score_jc017 = by_id[pid]["score"]
a_score = 85.0  # all A products are 85
gap_actual = a_score - score_jc017
row = by_id[pid]["rowVerdict"]
gap_claimed_row = None
m = re.search(r'הפרש של (\d+) נקודות', row)
if m:
    gap_claimed_row = int(m.group(1))
m2 = re.search(r'הפרש של (\d+) נקודות', by_id[pid]["expansion"].get("comparisonContext", ""))
gap_claimed_ctx = None
if m2:
    gap_claimed_ctx = int(m2.group(1))

print(f"\njc-017 GAP CLAIM:")
print(f"  jc-017 score={score_jc017}, A score={a_score}, actual gap={a_score - score_jc017:.1f}")
print(f"  rowVerdict claims: {gap_claimed_row} points")
print(f"  comparisonContext claims: {gap_claimed_ctx} points")
status_rv = "TRUE" if gap_claimed_row is None or abs(gap_claimed_row - gap_actual) < 2 else f"FALSE (actual={gap_actual:.1f})"
status_ctx = "TRUE" if gap_claimed_ctx is None or abs(gap_claimed_ctx - gap_actual) < 2 else f"FALSE (actual={gap_actual:.1f})"
print(f"  rowVerdict status: {status_rv}")
print(f"  comparisonContext status: {status_ctx}")

# --- jc-011: "44 קלוריות" ---
pid = "jc-011"
p = by_id[pid]
kcal_actual = p.get("kcalPer100ml")
rv = p.get("rowVerdict", "")
insight = p.get("insightLine", "")
kcal_match_rv = re.search(r'(\d+)\s*קלוריות', rv)
kcal_match_ins = re.search(r'(\d+)\s*קלוריות', insight)
print(f"\njc-011 KCAL CLAIM (residual panel recitation):")
print(f"  actual kcalPer100ml={kcal_actual}")
print(f"  rowVerdict has kcal claim: {kcal_match_rv.group(0) if kcal_match_rv else 'NONE'}")
print(f"  insightLine has kcal claim: {kcal_match_ins.group(0) if kcal_match_ins else 'NONE'}")
print(f"  rowVerdict text: '{rv}'")

# --- jc-024: "(35.4)" ---
pid = "jc-024"
p = by_id[pid]
rv = p.get("rowVerdict", "")
ins = p.get("insightLine", "")
score_actual = p["score"]
print(f"\njc-024 SCORE RECITATION CHECK:")
print(f"  actual score={score_actual}")
print(f"  rowVerdict: '{rv}'")
print(f"  insightLine: '{ins}'")
score_in_rv = str(score_actual) in rv or "35.4" in rv
score_in_ins = str(score_actual) in ins or "35.4" in ins
print(f"  score appears in rowVerdict: {score_in_rv}")
print(f"  score appears in insightLine: {score_in_ins}")

# --- jc-027: "28.5" ---
pid = "jc-027"
p = by_id[pid]
rv = p.get("rowVerdict", "")
ins = p.get("insightLine", "")
score_actual = p["score"]
print(f"\njc-027 SCORE RECITATION CHECK:")
print(f"  actual score={score_actual}")
print(f"  rowVerdict: '{rv}'")
print(f"  insightLine: '{ins}'")
score_in_rv = "28.5" in rv
score_in_ins = "28.5" in ins
print(f"  score appears in rowVerdict: {score_in_rv}")
print(f"  score appears in insightLine: {score_in_ins}")

# --- jc-006: "הגבוה ביותר בין שישת מוצרי ה-A" for sugar ---
pid = "jc-006"
p = by_id[pid]
sugar_jc006 = p.get("sugarPer100ml")
rv = p.get("rowVerdict", "")
a_sugars = [(pp["id"], pp.get("sugarPer100ml")) for pp in a_products]
max_a_sugar = max((s for _, s in a_sugars if s is not None), default=None)
print(f"\njc-006 'highest sugar among A' CLAIM:")
print(f"  jc-006 sugar={sugar_jc006}")
print(f"  A-product sugars: {a_sugars}")
print(f"  max A-sugar={max_a_sugar}")
print(f"  claim TRUE: {sugar_jc006 == max_a_sugar}")
print(f"  rowVerdict: '{rv[:120]}'")

# --- jc-021: "40% פרי — הגבוה ביותר בין כל מוצרי ה-D" ---
pid = "jc-021"
p = by_id[pid]
rv = p.get("rowVerdict", "")
ins = p.get("insightLine", "")
comp = p["expansion"].get("comparisonContext", "")
print(f"\njc-021 '40% fruit - highest among D' CLAIM:")
# D products and their fruit %
# Must check ingredients for % statements
d_fruit = {}
for dp in d_products:
    dp_id = dp["id"]
    ing = dp["expansion"].get("ingredients", "") or ""
    # Extract highest % mentioned
    pcts = re.findall(r'(\d+(?:\.\d+)?)\s*%', ing)
    pcts_float = [float(x) for x in pcts]
    dp_sub = dp.get("subPool", "")
    d_fruit[dp_id] = {"sub": dp_sub, "pcts_in_ingredients": pcts_float, "score": dp["score"]}
print(f"  jc-021 rowVerdict: '{rv[:120]}'")
print(f"  D products fruit pcts from ingredients:")
for dp_id, info in d_fruit.items():
    print(f"    {dp_id} sub={info['sub']} pcts={info['pcts_in_ingredients']}")

# jc-021 claims 40% fruit. Check actual from ingredients
jc021_ing = by_id["jc-021"]["expansion"]["ingredients"]
print(f"  jc-021 ingredients: '{jc021_ing}'")

# --- jc-027: "הנמוך ביותר בסקירה" ---
pid = "jc-027"
p = by_id[pid]
min_score = min(scores.values())
print(f"\njc-027 'lowest score in survey' CLAIM:")
print(f"  jc-027 score={p['score']}, min in corpus={min_score}")
print(f"  STATUS: {'TRUE' if p['score'] == min_score else 'FALSE'}")

# --- jc-024: "הנמוך ביותר בציון בין שלושת נקטרי ספרינג" ---
pid = "jc-024"
spring_nectars = ["jc-021", "jc-022", "jc-024"]
spring_scores = {pid: scores[pid] for pid in spring_nectars}
print(f"\njc-024 'lowest among 3 Spring nectars' CLAIM:")
print(f"  Spring nectar scores: {spring_scores}")
print(f"  jc-024 score={scores['jc-024']}, min={min(spring_scores.values())}")
print(f"  STATUS: {'TRUE' if scores['jc-024'] == min(spring_scores.values()) else 'FALSE'}")

# --- jc-020: "כמעט פי עשרה מקריסטל מיץ ענבים" (17% vs 2%) ---
pid = "jc-020"
p = by_id[pid]
rv = p.get("rowVerdict", "")
print(f"\njc-020 'almost 10x Kristal' CLAIM:")
print(f"  jc-020 (Jump) fruit %=17 vs jc-018 (Kristal) fruit %=2")
print(f"  actual ratio=17/2={17/2:.1f}x")
print(f"  claim 'כמעט פי עשרה': {17/2:.1f}x — 8.5x, is 'almost 10x' defensible?")
print(f"  rowVerdict: '{rv[:160]}'")

# --- jc-018 comparisonContext: score is cited as 41.8 but actual is 39.8 ---
pid = "jc-018"
p = by_id[pid]
score_actual = p["score"]
comp = p["expansion"].get("comparisonContext", "")
score_cited = re.search(r'ציון\s+([\d.]+)', comp)
print(f"\njc-018 SCORE IN comparisonContext:")
print(f"  actual score={score_actual}")
print(f"  cited in comparisonContext: {score_cited.group(1) if score_cited else 'none found'}")
print(f"  full comparisonContext: '{comp}'")

# --- jc-020 comparisonContext: score is cited as 40.1 but actual is 38.1 ---
pid = "jc-020"
p = by_id[pid]
score_actual = p["score"]
comp = p["expansion"].get("comparisonContext", "")
score_cited = re.search(r'ציון\s+([\d.]+)', comp)
print(f"\njc-020 SCORE IN comparisonContext:")
print(f"  actual score={score_actual}")
print(f"  cited in comparisonContext: {score_cited.group(1) if score_cited else 'none found'}")
print(f"  full comparisonContext: '{comp}'")

# --- Metadata: description says "65 מיצים" but product_count=17 ---
desc_in_ts = "השוואת 65 מיצים ומשקאות פירות"
print(f"\nMETADATA DESCRIPTION claim '65 מיצים':")
print(f"  product_count in JSON={meta.get('product_count')}, totalProducts={data.get('totalProducts')}")
print(f"  description in TS: '{desc_in_ts}'")
print(f"  STATUS: FALSE — description says 65, JSON has {meta.get('product_count')}")

# --- Check all score recitations in rowVerdict/insightLine/comparisonContext ---
print(f"\nSCORE RECITATION SCAN (all products):")
for p in products:
    pid = p["id"]
    score = p["score"]
    score_str = str(score)
    for field_name in ["insightLine", "rowVerdict"]:
        text = p.get(field_name, "") or ""
        if score_str in text:
            print(f"  RECITATION: {pid}.{field_name} contains score {score_str}")
    comp = p["expansion"].get("comparisonContext", "") or ""
    if score_str in comp:
        print(f"  SCORE-IN-CTX: {pid}.comparisonContext contains score {score_str}")

# --- Check all number claims in rowVerdict against nutrition data ---
print(f"\nNUMBER CLAIMS vs NUTRITION DATA:")
for p in products:
    pid = p["id"]
    sugar_actual = p.get("sugarPer100ml")
    kcal_actual = p.get("kcalPer100ml")
    for field_name in ["insightLine", "rowVerdict"]:
        text = p.get(field_name, "") or ""
        # look for sugar claims
        for m in re.finditer(r'(\d+(?:\.\d+)?)\s*גרם\s*סוכר', text):
            val = float(m.group(1))
            if sugar_actual is not None and abs(val - sugar_actual) > 0.5:
                print(f"  MISMATCH: {pid}.{field_name} claims sugar={val}, actual={sugar_actual}")
            elif sugar_actual is None:
                print(f"  NO-DATA: {pid}.{field_name} claims sugar={val}, actual=NULL")
        # look for kcal claims
        for m in re.finditer(r'(\d+(?:\.\d+)?)\s*קלוריות', text):
            val = float(m.group(1))
            if kcal_actual is not None and abs(val - kcal_actual) > 1:
                print(f"  MISMATCH: {pid}.{field_name} claims kcal={val}, actual={kcal_actual}")
            elif kcal_actual is None:
                print(f"  NO-DATA: {pid}.{field_name} claims kcal={val}, actual=NULL")

print("\nDONE")
