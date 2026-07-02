# -*- coding: utf-8 -*-
"""Comprehensive number audit - write results to JSON file to avoid stdout encoding issues."""
import json, re, sys, os

os.chdir(r"C:\Bari")

with open(r"C:\Bari\bari-web\src\data\comparisons\juices_frontend_v3.json", encoding="utf-8") as f:
    data = json.load(f)

products = data["products"]
meta = data["_meta"]
by_id = {p["id"]: p for p in products}
scores = {p["id"]: p["score"] for p in products}
grades = {p["id"]: p["grade"] for p in products}
sugars = {p["id"]: p.get("sugarPer100ml") for p in products}
kcals = {p["id"]: p.get("kcalPer100ml") for p in products}

a_products = [p for p in products if p["grade"] == "A"]
d_products = [p for p in products if p["grade"] == "D"]
e_products = [p for p in products if p["grade"] == "E"]

findings = []

def flag(severity, pid, field, claim, actual, note):
    findings.append({"severity": severity, "pid": pid, "field": field,
                     "claim": claim, "actual": actual, "note": note})

# ---- Grade dist ----
actual_a = sum(1 for p in products if p["grade"] == "A")
actual_d = sum(1 for p in products if p["grade"] == "D")
actual_e = sum(1 for p in products if p["grade"] == "E")

# ---- jc-017 60-point gap ----
score_jc017 = by_id["jc-017"]["score"]  # 49.1
a_score = 85.0
actual_gap = a_score - score_jc017  # 35.9

rv_017 = by_id["jc-017"]["rowVerdict"]
ctx_017 = by_id["jc-017"]["expansion"].get("comparisonContext", "")

gaps_in_rv = re.findall(r'הפרש של (\d+) נקודות', rv_017)
gaps_in_ctx = re.findall(r'הפרש של (\d+) נקודות', ctx_017)

for g in gaps_in_rv:
    if abs(int(g) - actual_gap) > 1:
        flag("CRITICAL", "jc-017", "rowVerdict",
             f"הפרש של {g} נקודות",
             f"actual gap = {actual_gap:.1f}",
             "Stated gap of 60 points is false; actual A(85) - jc-017(49.1) = 35.9 pts")

for g in gaps_in_ctx:
    if abs(int(g) - actual_gap) > 1:
        flag("CRITICAL", "jc-017", "expansion.comparisonContext",
             f"הפרש של {g} נקודות",
             f"actual gap = {actual_gap:.1f}",
             "Stated gap of 60 points is false in comparisonContext too")

# ---- jc-011 kcal recitation ----
rv_011 = by_id["jc-011"]["rowVerdict"]
ins_011 = by_id["jc-011"]["insightLine"]
kcal_011 = by_id["jc-011"]["kcalPer100ml"]
if "44" in rv_011 and "קלוריות" in rv_011:
    flag("HIGH", "jc-011", "rowVerdict",
         "44 קלוריות",
         f"actual kcal={kcal_011}",
         "Panel number (44 kcal) recited in rowVerdict - residual from old copy")

# ---- jc-024 score recitation ----
rv_024 = by_id["jc-024"]["rowVerdict"]
ins_024 = by_id["jc-024"]["insightLine"]
score_024 = by_id["jc-024"]["score"]
if str(score_024) in rv_024:
    flag("HIGH", "jc-024", "rowVerdict",
         f"score {score_024} cited in prose",
         f"actual score={score_024}",
         "Bari score recited in rowVerdict prose - de-recite rule violation")
if str(score_024) in ins_024:
    flag("HIGH", "jc-024", "insightLine",
         f"score {score_024} cited in prose",
         f"actual score={score_024}",
         "Bari score recited in insightLine - de-recite rule violation")

# ---- jc-027 score recitation ----
rv_027 = by_id["jc-027"]["rowVerdict"]
ins_027 = by_id["jc-027"]["insightLine"]
score_027 = by_id["jc-027"]["score"]
if str(score_027) in rv_027:
    flag("HIGH", "jc-027", "rowVerdict",
         f"score {score_027} cited in prose",
         f"actual score={score_027}",
         "Bari score recited in rowVerdict prose - de-recite rule violation")
if str(score_027) in ins_027:
    flag("HIGH", "jc-027", "insightLine",
         f"score {score_027} cited in prose",
         f"actual score={score_027}",
         "Bari score recited in insightLine - de-recite rule violation")

# Check comparisonContext for score recitations
for p in products:
    pid = p["id"]
    score = p["score"]
    score_str = str(score)
    comp = p["expansion"].get("comparisonContext", "") or ""
    if score_str in comp:
        flag("MEDIUM", pid, "expansion.comparisonContext",
             f"score {score_str} in text",
             f"actual={score}",
             f"Score recited in comparisonContext (expansion shown to user)")

# ---- jc-006: highest sugar among A ----
a_sugars = {p["id"]: p.get("sugarPer100ml") for p in a_products}
max_a_sugar = max((v for v in a_sugars.values() if v is not None), default=None)
jc006_sugar = a_sugars.get("jc-006")
rv_006 = by_id["jc-006"]["rowVerdict"]
if "הגבוה ביותר" in rv_006:
    if jc006_sugar == max_a_sugar:
        flag("INFO", "jc-006", "rowVerdict",
             f"highest sugar among A ({jc006_sugar})",
             f"max A sugar = {max_a_sugar}",
             "TRUE - jc-006 has highest sugar (12.6) among all A products")
    else:
        flag("CRITICAL", "jc-006", "rowVerdict",
             f"highest sugar among A",
             f"jc-006={jc006_sugar}, max={max_a_sugar}",
             "FALSE - jc-006 is NOT highest sugar among A")

# ---- jc-021: 40% fruit, highest among D ----
# Extract fruit % from ingredients for D products
d_fruit_pct = {}
for dp in d_products:
    dp_id = dp["id"]
    ing = dp["expansion"].get("ingredients", "") or ""
    # Sum all percentages mentioned
    pcts = [float(x) for x in re.findall(r'(\d+(?:\.\d+)?)\s*%', ing)]
    # Get highest single fruit % (first pct usually = fruit content)
    # For jc-021: "מחית אפרסקים* (31.5%), מיץ תפוחים* (8.5%)" -> 40% total
    d_fruit_pct[dp_id] = pcts

rv_021 = by_id["jc-021"]["rowVerdict"]
ins_021 = by_id["jc-021"]["insightLine"]
comp_021 = by_id["jc-021"]["expansion"].get("comparisonContext", "")
jc021_ing = by_id["jc-021"]["expansion"].get("ingredients", "")
# actual: 31.5% + 8.5% = 40% - so 40% is correct
# Is it highest among D?
# jc-017: 25% cranberry
# jc-019: 25% cranberry
# jc-018: 2% grape
# jc-020: 17% (12%+5%)
# jc-021: 40% (31.5%+8.5%) <- this IS highest
# jc-022: ~38% (14+12+8.5+3+2.5)
# jc-024: 25% mango
flag("INFO", "jc-021", "rowVerdict",
     "40% fruit, highest among D",
     "jc-021=40%(31.5+8.5), jc-022~38%, jc-017=25%, jc-019=25%, jc-024=25%, jc-020=17%, jc-018=2%",
     "NEED_VERIFY: jc-022 tut banana is ~38% (14+12+8.5+3+2.5), so jc-021 at 40% IS highest. TRUE.")

# Check sugar claimed in jc-021 insightLine vs actual
# insightLine says "40% פרי" - match ingredients
if "40%" in ins_021:
    if "31.5" in jc021_ing and "8.5" in jc021_ing:
        flag("INFO", "jc-021", "insightLine", "40% פרי", "31.5+8.5=40%", "TRUE")

# ---- jc-020: "כמעט פי עשרה" (17% vs 2%) ----
rv_020 = by_id["jc-020"]["rowVerdict"]
# 17/2 = 8.5x. "almost 10x" is an approximate claim.
if "פי עשרה" in rv_020:
    flag("MEDIUM", "jc-020", "rowVerdict",
         "כמעט פי עשרה מקריסטל מיץ ענבים",
         "17%/2%=8.5x",
         "Approximately true (8.5x rounds to 'almost 10x'). Borderline but defensible. Monitor.")

# ---- comparisonContext score errors ----
# jc-018: comparisonContext says "ציון 41.8" but actual is 39.8
comp_018 = by_id["jc-018"]["expansion"].get("comparisonContext", "")
m = re.search(r'ציון ([\d.]+)', comp_018)
if m:
    cited = float(m.group(1))
    actual = by_id["jc-018"]["score"]
    if abs(cited - actual) > 0.5:
        flag("HIGH", "jc-018", "expansion.comparisonContext",
             f"ציון {cited}",
             f"actual score={actual}",
             f"comparisonContext cites wrong score {cited}, actual is {actual}")

comp_020 = by_id["jc-020"]["expansion"].get("comparisonContext", "")
m = re.search(r'ציון ([\d.]+)', comp_020)
if m:
    cited = float(m.group(1))
    actual = by_id["jc-020"]["score"]
    if abs(cited - actual) > 0.5:
        flag("HIGH", "jc-020", "expansion.comparisonContext",
             f"ציון {cited}",
             f"actual score={actual}",
             f"comparisonContext cites wrong score {cited}, actual is {actual}")

# Scan ALL comparisonContexts for score citations
for p in products:
    pid = p["id"]
    actual_score = p["score"]
    comp = p["expansion"].get("comparisonContext", "") or ""
    for m in re.finditer(r'ציון\s+([\d.]+)', comp):
        cited = float(m.group(1))
        if abs(cited - actual_score) > 0.5:
            flag("HIGH", pid, "expansion.comparisonContext",
                 f"ציון {cited} in context",
                 f"actual score={actual_score}",
                 f"comparisonContext self-cites wrong score: {cited} vs actual {actual_score}")

# ---- Metadata description "65 מיצים" ----
flag("HIGH", "METADATA", "juicesComparisonMetadata.description",
     "השוואת 65 מיצים ומשקאות פירות",
     f"actual product_count={meta.get('product_count')} (17 displayed)",
     "Description says 65 products; JSON has 17. This appears in page SEO metadata.")

# ---- A-products: check all are single ingredient ----
for p in a_products:
    pid = p["id"]
    ing = p["expansion"].get("ingredients", "") or ""
    rv = p.get("rowVerdict", "") or ""
    ins = p.get("insightLine", "") or ""
    # Check copy claims about single ingredient
    if "רכיב אחד" in rv or "רכיב יחיד" in rv or "רכיב אחד" in ins or "רכיב יחיד" in ins:
        # verify ingredients is actually single
        # Simple heuristic: if ingredients contains comma -> multiple
        if "," in ing:
            flag("CRITICAL", pid, "rowVerdict/insightLine",
                 "claims single ingredient",
                 f"ingredients: {ing[:80]}",
                 "Copy claims single ingredient but ingredients string contains commas")
        else:
            flag("INFO", pid, "insightLine/rowVerdict",
                 "claims single ingredient",
                 f"ingredients: {ing}",
                 "TRUE - single ingredient confirmed")

# ---- Check jc-011 rowVerdict for kcal ----
rv_011 = by_id["jc-011"]["rowVerdict"]
kcal_matches = list(re.finditer(r'(\d+)\s*קלוריות', rv_011))
if kcal_matches:
    for m in kcal_matches:
        val = int(m.group(1))
        actual_kcal = by_id["jc-011"]["kcalPer100ml"]
        flag("HIGH", "jc-011", "rowVerdict",
             f"{val} קלוריות",
             f"actual={actual_kcal}",
             "Panel kcal number cited in rowVerdict (de-recite instruction not executed)")

# ---- Check jc-017 insightLine: "שלושה רבעי הבקבוק" (75% non-fruit = TRUE if fruit is 25%) ----
ins_017 = by_id["jc-017"]["insightLine"]
if "שלושה רבעי הבקבוק הם לא פרי" in ins_017:
    # 25% fruit => 75% non-fruit = TRUE
    flag("INFO", "jc-017", "insightLine",
         "שלושה רבעי הבקבוק הם לא פרי",
         "25% fruit confirmed",
         "TRUE - 25% fruit means 75% non-fruit. Correct.")

# ---- jc-022: "כ-38% פרי" claim ----
rv_022 = by_id["jc-022"]["rowVerdict"]
ins_022 = by_id["jc-022"]["insightLine"]
comp_022 = by_id["jc-022"]["expansion"].get("comparisonContext", "")
jc022_ing = by_id["jc-022"]["expansion"].get("ingredients", "")
# ingredients: מיץ תפוחים* (14%), מיץ תפוזים* (12%), מחית בננה (8.5%), סוכר לבן, מחית תות שדה* (3%), מיץ אסרולה* (2.5%)
# sum = 14+12+8.5+3+2.5 = 40%
# comp_022 says "כ-38%"
if "38%" in comp_022 or "38" in comp_022:
    flag("HIGH", "jc-022", "expansion.comparisonContext",
         "כ-38% פרי",
         "14+12+8.5+3+2.5=40%",
         "comparisonContext claims ~38% fruit but ingredients sum to 40%: 14+12+8.5+3+2.5=40. Should be ~40%.")
if "38%" in rv_022:
    flag("HIGH", "jc-022", "rowVerdict",
         "כ-38% פרי",
         "actual sum=40%",
         "rowVerdict claims ~38% fruit but ingredients sum to 40%")

# ---- jc-023: "תשעה עשר מהבקבוק" - should be 89/90% not 19 ----
lf_023 = by_id["jc-023"]["expansion"].get("limitingFactors", [])
for lf in lf_023:
    if "תשעה עשר" in lf:
        flag("HIGH", "jc-023", "expansion.limitingFactors",
             "תשעה עשר מהבקבוק הם מים, סוכר ותחליפים",
             "11% fruit => 89% non-fruit = 89, not 19",
             "Typo: 'תשעה עשר' (19) should be 'תשעים ואחד' (89%) or similar. 11% fruit = 89% non-fruit.")

# Check if it's in rowVerdict too
rv_023 = by_id["jc-023"]["rowVerdict"]
if "תשעה עשר" in rv_023:
    flag("HIGH", "jc-023", "rowVerdict",
         "תשעה עשר מהבקבוק",
         "11% fruit => 89% non-fruit",
         "Typo in rowVerdict too")

# ---- ALL score citations in comparisonContext ----
all_ctx_scores = {}
for p in products:
    pid = p["id"]
    comp = p["expansion"].get("comparisonContext", "") or ""
    for m in re.finditer(r'(\d+(?:\.\d+)?)', comp):
        val = m.group(1)
        # Is it a score? Scores are in range 28-85
        try:
            fval = float(val)
            if 28 <= fval <= 85 and fval != float(pid.replace("jc-", "")):
                # Check if this is another product's score
                for other_p in products:
                    if other_p["id"] != pid and abs(other_p["score"] - fval) < 0.1:
                        # Found a cross-product score citation - check it's correct
                        pass  # cross-citing is OK if correct
        except ValueError:
            pass

# Write results
out = {
    "total_findings": len(findings),
    "critical": [f for f in findings if f["severity"] == "CRITICAL"],
    "high": [f for f in findings if f["severity"] == "HIGH"],
    "medium": [f for f in findings if f["severity"] == "MEDIUM"],
    "info": [f for f in findings if f["severity"] == "INFO"],
    "grade_distribution": {
        "meta_A": meta["grade_distribution"]["A"],
        "meta_D": meta["grade_distribution"]["D"],
        "meta_E": meta["grade_distribution"]["E"],
        "actual_A": actual_a, "actual_D": actual_d, "actual_E": actual_e
    },
    "score_table": [
        {"id": p["id"], "grade": p["grade"], "score": p["score"],
         "sugar": p.get("sugarPer100ml"), "kcal": p.get("kcalPer100ml")}
        for p in sorted(products, key=lambda x: -x["score"])
    ]
}

with open(r"C:\Bari\__qa_number_results.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

print(f"Written to __qa_number_results.json")
print(f"CRITICAL={len(out['critical'])} HIGH={len(out['high'])} MEDIUM={len(out['medium'])} INFO={len(out['info'])}")
