---
id: TASK-175
title: "Maadanim engine reads protein-enriched יופלה GO as a 'sweet dessert' — investigate category-assumption leak + fix self-contradictory verdict copy"
owner: nutrition-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-06-03
closed_at: 2026-06-03
closed_by: cc-agent
depends_on: []
blocks: []
category_id: maadanim
work_type: investigation
roadmap_impact: false
resolution: "Close-readiness gate PASSED (independently verified). Root cause confirmed text-only: trace bsip2_trace.json shows sweetener_detected:false, added_sugar_sources_count:0, sugars_g:null — the 'sweet base' claim was hand-authored copy unsupported by the product's own data, NOT a score input (score 78/B correctly earned, untouched). Corrected verdict shipped + verified live in maadanim_frontend_v2.json ('הבסיס בנוי על חלב ואבקת חלב מועשרים, לא על מבנה חלב שלם'); 'מעדן מתוק' fully removed (insightLine + limitingFactors); fix also applied upstream (build_frontend_json.py) and the editorial reference (row_description_standard_v1.md) so it can't regenerate. Sweep clean — leak isolated to GO. tsc exit 0."
summary: >
  On the live maadanim comparison page, יופלה GO מועשר בחלבון (bsip1_maadanim_7290110321031,
  78/B) carries a verdict that calls it a "sweet dessert" while simultaneously praising it for
  having no sweeteners. The product's own data does not support "sweet": sugar is unavailable
  (null) and the ingredient list is milk + milk protein (7.4%) + milk powder — three clean
  items, no sweetener. The "sweet base" reading appears to come from a maadanim category-level
  assumption (maadanim = sweet dessert) overriding the product's actual composition. Investigate
  whether/where the category framing is applied, and correct the published verdict so it is
  internally consistent and grounded in real signals (not an unsupported sugar claim).
---

# TASK-175 — יופלה GO read as "sweet" despite clean, no-sweetener composition

## What a shopper sees (live)
Row + expansion verdict for **יופלה GO מועשר בחלבון** (78/B):

> "…10 גרם חלבון מהחלב ושלושה רכיבים בלבד, **נדיר במדף של ממתיקים ומייצבים**. עוצר ב-B כי **הבסיס עדיין מעדן מתוק, לא מוצר חלבון**."

The line praises the absence of sweeteners/stabilizers, then asserts a sweet base in the same breath. That is the "not understandable" part the owner flagged.

## What the data actually says
From `maadanim_frontend_v2.json` (id `bsip1_maadanim_7290110321031`):
- **nutrition (per 100g):** energy 72 kcal · protein 10.0g · fat 2.0g · sodium 69mg · **sugar: null (unavailable)** · fiber: null
- **ingredients:** `חלב, חלבוני חלב (7.4%), אבקת חלב` — no sugar, no sweetener, no stabilizer
- `expansion.unknowns`: "ערכי הסוכר לא היו זמינים במקור הנתונים — מדד זה לא נכלל בניתוח."

So the engine has **no sugar evidence** and **no sweetener in the ingredient list**, yet the verdict brands the base "sweet." The "sweet" reading is not derived from this product's signals.

## Hypothesis to test
The "sweet dessert" framing is a **maadanim category-level assumption** (the whole shelf is treated as sweet desserts) leaking into a product that doesn't match it. This is the framework-leak / category-assumption-over-product failure mode the editorial governance forbids.

## Scope of investigation (Nutrition, with Content for the copy)
1. Trace where the "sweet base" reasoning originates — scorer dimension, category interpretation, or authored copy only? Is it a real score input or just verdict text?
2. Decide the correct treatment: either the maadanim framing must not assert "sweet" for products with no sugar evidence + clean ingredient list, or the B verdict must be re-justified on real grounds (e.g. category-relative position, processing) without an unsupported sugar claim.
3. Rewrite the published verdict so it is internally consistent (no "rare among sweeteners" + "still a sweet dessert" contradiction).
4. Check whether the same assumption mis-describes other clean/protein-enriched maadanim rows.

## Not in scope here
Score change to 78/B is not pre-authorized — if the investigation finds the score itself is mis-driven, that escalates separately. This task is the diagnosis + (at minimum) the copy correction.

---

## FINDINGS (Nutrition, 2026-06-03)

### Root cause — "sweet" is hand-authored copy, NOT a score input. Score is clean.
Authoritative trace: `02_products/maadanim/bsip2_outputs/run_maadanim_001/products/bsip1_maadanim_7290110321031/bsip2_trace.json` (engine 0.4.1, final 77.7 → 78/B).
- `sweetener_detected: false`, `sweetener_matches: []`, `added_sugar_sources_count: 0`, `sugars_g: null`.
- `glycemic_quality: "90 - sugar_penalty(0.0) ..."` → sugar contributes **zero** to the score.
- Every sugar/sweet cap considered fired `false` (HIGH_SUGAR_*, ISRAELI_RED_LABEL_1_SUGAR, HP_FAT_SUGAR_COMBO).
- `explanation_drivers: ["PRIMARY SIGNAL: nutrient_density=50.0 (lowest dimension)"]`. The B is held by `nutrient_density` / `protein_quality` / neutral `fat_quality` (all 50) + NOVA-2 reconstituted base — **nothing sweet/dessert touches the number.**
- Category config (`02_products/maadanim/category_config.json`) carries no "sweet" scoring assumption — only `name_en: "Dairy Desserts"`. No category-level "sweet" leak into the engine.

**Verdict: the "sweet base" reading is text-only and factually unsupported by the product's own data.** It originated as hand-authored verdict copy during the TASK-168 verdict-model rollout — and worse, it was enshrined as the **"approved target voice" reference example** in `01_framework/editorial/row_description_standard_v1.md`, so it was the model the other 84 verdicts were measured against.

### Score: NOT mis-driven, NOT changed. No escalation needed.
The 78/B is correctly earned (and consistent with `go_score_diagnosis_144.md` + RULING-DAIRY-A-01: GO fails A on C3 no-live-culture + C4 reconstituted-matrix). Score untouched.

### Fix applied (copy correction at source layers)
**Live verdict — before → after** (`bari-web/src/data/comparisons/maadanim_frontend_v2.json`, `insightLine`, routed to rowVerdict):
- BEFORE: "…נדיר במדף של ממתיקים ומייצבים. עוצר ב-B כי **הבסיס עדיין מעדן מתוק, לא מוצר חלבון**."
- AFTER:  "…נדיר במדף של ממתיקים ומייצבים. עוצר ב-B כי **הבסיס בנוי על חלב ואבקת חלב מועשרים, לא על מבנה חלב שלם**."  (158 chars, 2 lines, trace-grounded: NOVA-2 reconstituted/enriched base.)

Files edited:
1. `bari-web/src/data/comparisons/maadanim_frontend_v2.json` — `insightLine` + `expansion.limitingFactors` (the LF also asserted "עדיין מעדן מתוק" → replaced with the enriched-base reason). `bottomLine` left as-is (already grounded + non-contradictory).
2. `02_products/maadanim/build_frontend_json.py` — upstream `CE_INTERPRETIVE_OVERRIDES` `limitingFactors` for GO, so a re-run regenerates consistent copy (with a TASK-175 comment).
3. `01_framework/editorial/row_description_standard_v1.md` — corrected the GO "approved target voice" in all 4 places (intro example, §2a grade-rationale, char-count reference, worked example) + added a TASK-175 correction note making GO the canonical illustration of the trace-anchored-catch rule. Old text retained only inside the explanatory note.

tsc: `npx tsc --noEmit` → exit 0 (JSON is TS-imported).

### Sweep — leak is ISOLATED to GO. No other row needs this fix.
Swept all 84 maadanim products for "sweet/dessert asserted with no sugar evidence" (sugar value ≤0/null AND no `סוכר`/`ממתיק`/`גלוקוז`/`פרוקטוז` in ingredients). **GO was the sole hit.** Every other "מתוק"/"קינוח" verdict is grounded — either a measured sugar value >0 or `סוכר` explicit in the ingredient list (usually 2nd–3rd ingredient). The three other sugar=null protein-10g siblings (7290110329143, 7290110325312, 7290110325510) all have `סוכר`/`סירופ גלוקוזה` in their lists AND already justify their grade on processing/stabilizers, not sweetness — correct as written. **Recommendation: no further row edits.**

## Proposed status: RETURNED → CLOSE
Copy correction shipped at canonical + upstream + editorial layers; score untouched (correctly earned); sweep clean (single isolated leak fixed); tsc green. No escalation: score is not mis-driven. Recommend close after CC verifies the before→after against the cited trace.
