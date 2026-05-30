#!/usr/bin/env python3
"""
לחם — Bread Calibration Patch v1
Applies surgical post-scoring corrections to lechem_frontend_v1.json
Writes: lechem_frontend_v2.json  (BariProductVM[], patched scores)
        lechem_calibration_patch_v1.md  (full audit trail)

Correction types:
  fiber_laundering    — added isolated fiber scored as whole-grain fiber
  inulin_augmentation — explicit prebiotic inulin boosting fiber credit
  fiber_implausible   — reported fiber inconsistent with declared grain fractions
  fermentation_authenticity — white-flour sourdough credited as whole-grain sourdough
  white_flour_base    — enriched white bread clearing B threshold via nutritional floor
  white_spelt_base    — sifted spelt (not whole) scored on par with whole-spelt products
  additive_accumulation — dual preservative + low fiber; score contradicts insight line

Unchanged products: documented at end of report.
"""
import json
import sys
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

IN_JSON    = Path(r"C:\Bari\02_products\bread_retail_003\lechem_frontend_v1.json")
OUT_JSON   = Path(r"C:\Bari\02_products\bread_retail_003\lechem_frontend_v2.json")
OUT_REPORT = Path(r"C:\Bari\02_products\bread_retail_003\lechem_calibration_patch_v1.md")

# ── Calibration patch table ───────────────────────────────────────────────────
# Each entry: barcode → delta (negative), correction_type, rationale
# Deltas are restrained: correct to where an honest ingredient-aware scorer
# would land, not to the minimum defensible score.

CALIBRATION_PATCH: dict[str, dict] = {

    # ── Fiber laundering ──────────────────────────────────────────────────────
    # Added isolated fiber appears in top-3 ingredients; reported fiber
    # significantly exceeds what the declared grain fractions can produce.

    "2079996": {
        "delta": -7,
        "correction_type": "fiber_laundering",
        "name_he": "לחם אחיד פרוס קל",
        "score_before": 73,
        "rationale": (
            "סיבים תזונתיים (isolated fiber) is the 3rd ingredient — immediately after dark wheat flour and water. "
            "Reported fiber=10.4g; dark wheat flour at ~50% of product produces ≤3g naturally. "
            "The remaining 7g is supplement. Whole flour fractions (whole wheat, whole rye) appear 7th–8th. "
            "Score 73 assumed all 10.4g fiber is structural. Corrected to 66, consistent with a dark-flour "
            "bread with partial whole-grain addition."
        ),
    },
    "497044": {
        "delta": -4,
        "correction_type": "inulin_augmentation",
        "name_he": "לחם ברמן אקטיב",
        "score_before": 72,
        "rationale": (
            "Explicit label: 'סיבים פרה ביוטיים (אינולין) 3%'. At 3g/100g added inulin, roughly 26% of "
            "reported fiber=11.4g is supplemented. Base is genuinely 100% whole wheat (53% of product) — "
            "a real grain foundation. Correction is moderate: preserves whole-grain credit, removes "
            "inulin inflation. Corrected to 68."
        ),
    },
    "2079033": {
        "delta": -5,
        "correction_type": "fiber_implausible",
        "name_he": "לחם דגנים לייט",
        "score_before": 74,
        "rationale": (
            "Reported fiber=14.2g. Declared grain fractions: whole wheat 32%, whole rye 11%, dark wheat ~7%, "
            "grain mix 8% = ~58% total grain. At 10g fiber/100g whole grain flour, ~58% grain → ~5.8g fiber. "
            "The gap to 14.2g (≈8g) requires undisclosed supplemented fiber. Water is ingredient #1, "
            "suggesting high hydration that concentrates reported values. Base is genuinely whole grain. "
            "Moderate correction to 69 — preserves whole-grain credit while removing implausible fiber premium."
        ),
    },
    "497570": {
        "delta": -6,
        "correction_type": "fiber_laundering",
        "name_he": "לחם דגנים פלוס",
        "score_before": 68,
        "rationale": (
            "Reported fiber=12.7g from 35% whole wheat + 10% grain mix. Maximum plausible from grain alone: "
            "~4.5g. Remaining 8g comes from supplemented fiber (grain mix includes oat flakes, rye flakes, "
            "barley flakes — concentrated bran sources likely added as fiber booster). Insight line already "
            "states 'ה-פלוס הוא תוספת סיבים, לא גרעין שלם' — score 68/B directly contradicts this. "
            "Corrected to 62/C."
        ),
    },

    # ── Fermentation authenticity ─────────────────────────────────────────────
    # Fermentation was detected from ingredient text but the base flour is
    # predominantly white, so the glycemic/structural benefit doesn't apply.

    "481180": {
        "delta": -7,
        "correction_type": "fermentation_authenticity",
        "name_he": "לחם מחמצת שאור",
        "score_before": 71,
        "rationale": (
            "White wheat flour comprises 75% of all flour fractions (40% of total product weight). "
            "The sourdough starter itself (מחמצת חיטה לבן 18%) is white-flour based. Fiber=2.5g — "
            "the lowest among all B-grade non-cracker products in this corpus. "
            "Score 71 places this product level with genuinely whole-grain sourdoughs at 70–74. "
            "Insight line states 'הבסיס לבן, המחמצת שלישית ברשימה' — the score was contradicting this. "
            "Corrected to 64/C, consistent with white-flour sourdoughs in the C cluster (62–64)."
        ),
    },

    # ── White flour base (enriched breads at B/C threshold) ──────────────────
    # White flour is primary or exclusive flour; sugar appears in top-3 ingredients;
    # emulsifiers and preservative present. These products cleared 65 via
    # nutritional floor (low fat, adequate protein) without compositional merit.

    "4033736": {
        "delta": -4,
        "correction_type": "white_flour_base",
        "name_he": "לחם עננים בסגנון בריוש",
        "score_before": 66,
        "rationale": (
            "100% white flour (60% of product weight). Sugar is ingredient #3. "
            "Three emulsifiers (E471, E481, E472e) + preservative (E282). "
            "Added isolated fiber later in list. Insight line: 'קמח לבן 100%, סוכר שני ברשימה, מתחלבים — "
            "הסגנון מסביר את הרכב'. A score of 66/B implies parity with products containing 70–80% "
            "whole grain. Corrected to 62/C."
        ),
    },
    "7290018500231": {
        "delta": -3,
        "correction_type": "white_flour_base",
        "name_he": "לחם אנג'ל WEEKEND",
        "score_before": 65,
        "rationale": (
            "White flour is primary flour. Sugar is ingredient #3. Emulsifier (E481) + preservative (E282). "
            "Added isolated fiber (ingredient #7). Insight line: 'קמח לבן, סוכר, מתחלבים. אנג'ל לשבת, לא לשבוע'. "
            "Score 65/B = same letter as לחם ירוק מקמח מלא (80/B), a 100% whole-wheat clean-label product. "
            "Corrected to 62/C."
        ),
    },
    "7290017947105": {
        "delta": -3,
        "correction_type": "white_flour_base",
        "name_he": "לחם בסגנון אמריקה",
        "score_before": 65,
        "rationale": (
            "White flour is primary flour. Sugar is ingredient #3. Five E-numbers including three emulsifiers "
            "(E471, E472e, E481) + preservative (E282). Composition identical to WEEKEND profile. "
            "Insight line: 'קמח לבן ראשון, סוכר שני, מתחלבים שלישי. הסגנון מסביר את הרכב'. "
            "Corrected to 62/C. Consistent with WEEKEND correction."
        ),
    },

    # ── White spelt (sifted grain, not whole) ────────────────────────────────
    # Spelt marketed as premium but the 'לבן' (white/sifted) designation means
    # the bran has been removed — structurally closer to white flour than whole grain.

    "7290018500316": {
        "delta": -4,
        "correction_type": "white_spelt_base",
        "name_he": "לחם כוסמין לבן",
        "score_before": 68,
        "rationale": (
            "כוסמין לבן = sifted spelt: germ and most bran removed. 88% of flour fraction (61% of product) "
            "is sifted spelt. Fiber=3.3g — consistent with white flour, not whole grain. "
            "Scored 68 alongside genuinely whole-grain products at 68–72. "
            "Insight line: 'גרעין כוסמין מנופה. 3.3 גרם סיבים בלבד, פחות מגרסת הכוסמין המלא'. "
            "Corrected to 64/C."
        ),
    },

    # ── Additive accumulation + low fiber ────────────────────────────────────
    # Not white flour, but dual-preservative load is unique in the corpus and
    # the insight line explicitly frames this product as the additive maximum.

    "2079477": {
        "delta": -3,
        "correction_type": "additive_accumulation",
        "name_he": "לחם אחיד פרוס",
        "score_before": 67,
        "rationale": (
            "Two distinct preservatives: קלציום פרופיונט (E282) + פוטסיום סורבט (E202) — unique in corpus. "
            "Two emulsifiers (E471, E481). Fiber=3.0g from dark wheat base. "
            "Insight line: 'שני חומרים משמרים... לחם אחיד, שיא התוספות'. "
            "Score 67/B contradicts 'שיא התוספות'. Corrected to 64/C."
        ),
    },
}


def grade_from_score(score: int) -> str:
    if score >= 80: return "A"
    if score >= 65: return "B"
    if score >= 50: return "C"
    if score >= 35: return "D"
    return "E"


# ── Load and patch ────────────────────────────────────────────────────────────
with open(IN_JSON, encoding="utf-8") as f:
    data = json.load(f)

products_v1 = data["products"]
products_v2 = []
changes = []

for p in products_v1:
    bc = p["id"]
    patch = CALIBRATION_PATCH.get(bc)

    if patch is None:
        products_v2.append(p)
        continue

    old_score = p["score"]
    new_score = max(0, old_score + patch["delta"])
    old_grade = p["grade"]
    new_grade = grade_from_score(new_score)

    p2 = dict(p)
    p2["score"] = new_score
    p2["grade"] = new_grade
    p2["_calibration"] = {
        "score_v1": old_score,
        "grade_v1": old_grade,
        "delta": patch["delta"],
        "correction_type": patch["correction_type"],
    }
    products_v2.append(p2)

    changes.append({
        "barcode": bc,
        "name": p["name"],
        "score_before": old_score,
        "grade_before": old_grade,
        "score_after": new_score,
        "grade_after": new_grade,
        "delta": patch["delta"],
        "correction_type": patch["correction_type"],
        "grade_change": old_grade != new_grade,
    })

# Re-sort
products_v2.sort(key=lambda p: p["score"], reverse=True)

# ── Grade distributions ───────────────────────────────────────────────────────
def grade_dist(products):
    d = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0}
    for p in products:
        g = p.get("grade", "?")
        d[g] = d.get(g, 0) + 1
    return d

dist_before = grade_dist(products_v1)
dist_after  = grade_dist(products_v2)

# ── Write patched JSON ────────────────────────────────────────────────────────
payload = {
    "_meta": {
        "generated":     datetime.utcnow().isoformat() + "Z",
        "category":      "lechem",
        "product_count": len(products_v2),
        "schema":        "BariProductVM[]",
        "version":       "v2",
        "source":        "bread_retail_003 (Shufersal) — calibrated scores",
        "calibration":   "Bread Calibration Patch v1 applied (10 products corrected)",
        "base_version":  "lechem_frontend_v1.json",
    },
    "products": products_v2,
}

with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False, indent=2)

print(f"v2 JSON: {OUT_JSON}")

# ── Build report ──────────────────────────────────────────────────────────────
grade_rows_compare = "\n".join(
    f"| {g} | {dist_before.get(g, 0)} ({dist_before.get(g,0)/81*100:.0f}%) "
    f"| {dist_after.get(g, 0)} ({dist_after.get(g,0)/81*100:.0f}%) "
    f"| {dist_after.get(g,0) - dist_before.get(g,0):+d} |"
    for g in ("A", "B", "C", "D")
)

grade_changes = [c for c in changes if c["grade_change"]]
score_only    = [c for c in changes if not c["grade_change"]]

change_rows = "\n".join(
    f"| {c['barcode']} | {c['name']} | {c['score_before']}/{c['grade_before']} "
    f"| {c['score_after']}/{c['grade_after']} | {c['delta']:+d} | {c['correction_type']} |"
    for c in changes
)

# Intentionally unchanged products with ambiguity
INTENTIONALLY_UNCHANGED = [
    ("BC=481197", "76/B", "לחם מחמצת גרעינים",
     "White flour is first among flour types (24% of product) but overall flour blend is mixed; "
     "40% of product is whole grain. Ambiguous — insight line flags it without score contradiction."),
    ("BC=497044-note", "72→68/B", "לחם ברמן אקטיב (partial)",
     "Inulin corrected from 72→68 but not pushed to C: whole-wheat base (53% of product) is genuine. "
     "Moderate correction only — the product has real structural quality beneath the supplement."),
    ("BC=2079033-note", "74→69/B", "לחם דגנים לייט (partial)",
     "Fiber corrected from implausible 14.2g but not pushed to C: grain fractions are genuinely whole. "
     "Water-first high-hydration bread with real grain base."),
    ("BC=7290016967074", "72/B", "לחם אנג'ל חיטה מלאה",
     "9 E-numbers — highest additive count in B-grade. But 100% whole wheat, 8g fiber. "
     "Additive load is editorially covered by insight line. High E-count alone does not trigger correction."),
    ("BC=7290014940901", "70/B", "לחם פשוט מלא",
     "6 E-numbers on a product named 'פשוט'. Insight line 'הפשטות מגיעה עד הרכיב הרביעי' already carries "
     "the editorial load. Score 70 for 100% whole wheat is defensible; correction would be punitive."),
    ("BC=4685157", "70/B", "לחם שיפון 100% פרוס",
     "100% whole rye, emulsifiers present. Score 70 with genuine whole-rye base is correct."),
    ("BC=7296073659945", "66/B", "קרקר דק רוזמרין",
     "Only 25% whole wheat but cracker format concentrates fiber. Palm oil present. "
     "Applying flour-base correction to crackers requires category-specific thresholds not yet defined."),
    ("BC=574035", "66/B", "לחם אחיד פרוס (תנובה)",
     "Dark wheat + vegetable oils + emulsifiers. Insight line notes absence of extended improvers — "
     "not contradicted by B score. One preservative only (not dual). Left unchanged."),
    ("BC=497112", "66/B", "לחם פרוס אחיד",
     "Dark wheat, E282 + E481. Insight 'הנוסחה הבסיסית' describes without contradicting B. "
     "Fiber=4.8g from dark wheat is genuine. Left unchanged."),
    ("BC=8713917", "67/B", "לחם שיפון כהה",
     "7 E-numbers — concerning. But dark wheat 66% + whole rye 34%, fiber=6.1g is real mixed grain. "
     "Additive count alone is not sufficient without insight line contradiction."),
]

unchanged_rows = "\n".join(
    f"| {bc} | {score} | {name} | {reason} |"
    for bc, score, name, reason in INTENTIONALLY_UNCHANGED
)

report = f"""# לחם — Bread Calibration Patch v1

**Applied:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}
**Input:** `lechem_frontend_v1.json` (81 products, BSIP2 bread_retail_003)
**Output:** `lechem_frontend_v2.json`
**Approach:** Synthesis-level corrections only — no BSIP2 rerun

---

## Calibration Rationale

The BSIP2 bread scoring operated on nutrition macros only — the scorer had no access to parsed
ingredient data (`has_ingredients: true` but no ingredient list in BSIP2 files). As a result:

1. Fiber from added inulin/isolated fiber was treated identically to whole-grain fiber
2. White flour as primary base received no structural penalty
3. Fermentation credit was awarded based on name/label detection, not base-flour composition
4. Additive load (E-numbers, preservatives) had no effect on score

These four failure modes produced a 74% B distribution (60/81 products) where industrial
enriched breads occupied the same grade as genuinely clean whole-grain products.

**Editorial philosophy:** corrections are restrained — adjusted to where an honest
ingredient-aware rater would place the product, not to the minimum defensible score.
Products with genuine whole-grain bases received partial credit even when supplemented.

---

## Grade Distribution — Before / After

| Grade | Before | After | Change |
|-------|--------|-------|--------|
{grade_rows_compare}

**B: 74% → {dist_after.get('B',0)/81*100:.0f}%**
**C: 22% → {dist_after.get('C',0)/81*100:.0f}%**

---

## All Corrected Products

| Barcode | Name | Before | After | Delta | Type |
|---------|------|--------|-------|-------|------|
{change_rows}

**Grade changes (B→C):** {len(grade_changes)} products
**Score-only corrections (remain B):** {len(score_only)} products

---

## Grade Change Details (B → C)

{chr(10).join(
    f"### {c['name']} (BC={c['barcode']})"
    f"\\n**{c['score_before']}/{c['grade_before']} → {c['score_after']}/{c['grade_after']}** (Δ{c['delta']:+d})"
    f"\\n\\n{CALIBRATION_PATCH[c['barcode']]['rationale']}"
    f"\\n"
    for c in grade_changes
)}

---

## Score-Only Corrections (Remain B)

{chr(10).join(
    f"### {c['name']} (BC={c['barcode']})"
    f"\\n**{c['score_before']}/{c['grade_before']} → {c['score_after']}/{c['grade_after']}** (Δ{c['delta']:+d})"
    f"\\n\\n{CALIBRATION_PATCH[c['barcode']]['rationale']}"
    f"\\n"
    for c in score_only
)}

---

## Intentionally Unchanged (Ambiguous Cases)

These products showed calibration concerns but were left unchanged because the insight line
already carries the editorial correction, or the correction would be punitive rather than honest.

| Product | Score | Name | Reason |
|---------|-------|------|--------|
{unchanged_rows}

---

## Score-Insight Line Contradiction Check

After patch, the following score/insight contradictions are resolved:

| Barcode | Insight | Old Score | New Score | Resolution |
|---------|---------|-----------|-----------|------------|
| 2079477 | שיא התוספות | 67/B | 64/C | B said "acceptable"; C says "maximum additives = lower half" |
| 481180 | הבסיס לבן, המחמצת שלישית | 71/B | 64/C | B parity with whole-grain sourdoughs; C matches white-flour cluster |
| 497570 | ה'פלוס' הוא תוספת סיבים, לא גרעין שלם | 68/B | 62/C | B said "adequate"; C matches the editorial judgment |
| 4033736 | קמח לבן 100%, סוכר שני, מתחלבים | 66/B | 62/C | B for enriched white brioche-style was unjustifiable |
| 7290018500231 | אנג'ל לשבת, לא לשבוע | 65/B | 62/C | Score now matches occasion-framing in insight |
| 7290017947105 | הסגנון מסביר את הרכב | 65/B | 62/C | "Style explains composition" lands correctly at C |
| 7290018500316 | גרעין כוסמין מנופה. 3.3 גרם סיבים בלבד | 68/B | 64/C | Sifted spelt described as C-grade; score now confirms |

---

## Verdict

**Safe to wire as v2.**

The corrected distribution (B: {dist_after.get('B',0)}, C: {dist_after.get('C',0)}, A: {dist_after.get('A',0)}, D: {dist_after.get('D',0)}) improves
grade discrimination without destabilizing the corpus. A-grade products are unchanged.
The top of the B band (77–80) remains intact — the genuinely strong products were not touched.
Seven grade changes move products to where their composition and insight lines already placed them.
"""

with open(OUT_REPORT, "w", encoding="utf-8") as f:
    f.write(report)

print(f"Report:  {OUT_REPORT}")

# ── Console summary ────────────────────────────────────────────────────────────
print("\n=== CALIBRATION SUMMARY ===")
print(f"Products corrected: {len(changes)}")
print(f"Grade changes (B→C): {len(grade_changes)}")
print(f"Score-only: {len(score_only)}")
print(f"\nBefore: A={dist_before['A']} B={dist_before['B']} C={dist_before['C']} D={dist_before['D']}")
print(f"After:  A={dist_after['A']}  B={dist_after['B']}  C={dist_after['C']}  D={dist_after['D']}")
print("\nChanged products:")
for c in changes:
    arrow = f"{c['score_before']}/{c['grade_before']} → {c['score_after']}/{c['grade_after']}"
    flag = " [GRADE CHANGE]" if c["grade_change"] else ""
    print(f"  {arrow:20s}  Δ{c['delta']:+d}  {c['name']}{flag}")
print("\nDone.")
