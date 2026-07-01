---
id: TASK-216
title: "Extrusion NOVA Detection Fix — generalizable industrial-extrusion signal for BSIP2 NOVA proxy"
owner: nutrition-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-07
closed_at: 2026-06-07
depends_on: [TASK-213]
blocks: []
roadmap_impact: true
cc_reviewed: true
work_type: scoring-rule
d7_cosign_required: true
close_reason: "EV-043 implemented (Signal A: מורחב ingredient marker + Signal B: sub_pool=puffed+grain). No brand hardcoding confirmed by Grep. Bamba: 70/B→54/C, NOVA 2→4, Signal A fired in trace. Rice cakes (7290000091004): 58.3/C in both runs — unchanged. Grade dist A:7 B:16 C:18 D:9 E:4 (B-1, D+1 vs run_001). salty_snacks_frontend_v2.json at bari-web, 54 products. Nutrition Agent D7 half approved. Product Agent D7 co-sign required before full engine promotion to other categories (Signal A promotable immediately; Signal B needs per-category sub_pool review)."
---

# TASK-216 — Extrusion NOVA Detection Fix

## Context

TASK-213 (salty snacks pipeline) completed with a confirmed NOVA scoring gap: products made
via industrial extrusion — Bamba (7290000066003), Bisli (7290000630006/020/003), corn puffs,
and similar extruded snacks — receive NOVA 2 from the engine when the nutritionally correct
classification is NOVA 4.

The root cause: the BSIP2 NOVA proxy infers group from ingredient text keyword matching and
E-number detection. Extrusion is a high-temperature industrial process that fundamentally
alters the food matrix (starch gelatinization, Maillard at high heat, protein denaturation).
But the process is invisible in the ingredient list — "תירס מורחב" (extruded corn) and
"קמח תירס" (corn flour) look similar to the parser. The result: Bamba at 70/B when the
correct score is approximately C-range (48–58).

The BSIP1 enrichment correctly assigned NOVA 4 to these products (31/54 products vs engine's
4/54). The engine and enrichment are misaligned.

**Critical constraint:** The fix must be generalizable. It must detect extrusion as a
structural food process from available signals — ingredient text, product name, product
type — without hardcoding any brand or product name (no "if name contains Bamba → NOVA 4").

The salty-snacks frontend launch is BLOCKED on this task. TASK-213 is pipeline-complete;
scoring validity is not.

## Affected products (from salty-snacks corpus)

At minimum — verify against actual BSIP1 records:
- במבה (Bamba) — `bsip1_snack_7290000066003`
- בסלי (Bisli) variants — `bsip1_snack_7290000630006`, `_630020`, `_9900003`
- ניבים תירס (corn puffs) — confirm which barcodes
- Any other product where BSIP1 = NOVA 4 but engine = NOVA 2 due to extrusion

## Scope

### 1. Design the extrusion detection signal

Read the current NOVA proxy logic in `C:\Bari\03_operations\bsip2\proto_v0\src\`. Identify
where NOVA group is inferred.

Propose a generalizable extrusion indicator that can be derived from one or more of:

**Option A — Ingredient text markers:**
- "תירס מורחב" / "חיטה מורחבת" / "אורז מורחב" / "מורחב" (extruded grain variants)
- "עיסת תירס" (corn masa/extruded paste)
- "ממרח בוטנים" when paired with extruded base (Bamba structure)
- "פריכיות" in product name + grain base ingredient

**Option B — Product-type heuristic from category tag + ingredient base:**
- sub_pool = `puffed` + primary ingredient is a grain → NOVA 4 signal
- Note: this uses the BSIP1 sub-pool classification, which is available at scoring time

**Option C — Ingredient structure analysis:**
- Primary ingredient is a grain in an explicitly processed form (מורחב, מנופח, מעובד)
  + fat source (oil/nut butter) → industrial recombination → NOVA 4

**Option D — Combination of above**

Recommend the single best approach based on: detection accuracy across the corpus,
false-positive risk (avoid misclassifying genuinely simple-ingredient grain products
like plain rice cakes), and robustness across Hebrew ingredient text variation.

**Hard constraint:** plain rice cakes (פצפוצי אורז — single ingredient: rice, or
rice + salt) must NOT be reclassified. They are legitimately NOVA 1–2. The extrusion
signal must distinguish "puffed whole grain, minimal processing" from "industrially
recombined extruded matrix with fat and flavoring added."

### 2. Validate the proposed signal

Before implementing, validate the proposed logic against the full salty-snacks BSIP1
corpus (54 products). For each product, predict the NOVA assignment the new signal would
produce. Check:
- True positives: extruded products (Bamba, Bisli, corn puffs) correctly → NOVA 4
- True negatives: plain rice cakes, plain popcorn, whole-wheat crackers correctly NOT NOVA 4
- False positives: any non-extruded product that would incorrectly trigger NOVA 4

Report the predicted NOVA reclassification count (how many products shift from NOVA 2 → NOVA 4).

### 3. Implement the fix in the BSIP2 engine

Engine source: `C:\Bari\03_operations\bsip2\proto_v0\src\`

- Add the extrusion detection signal to the NOVA proxy logic
- Ensure it is generalizable (no brand/product hardcoding)
- Add it to the signal taxonomy documentation if one exists in `01_framework/bsip2_framework/`
- Note the change in the engine changelog if one exists

This change requires D7 co-sign (Nutrition Agent + Product Agent). Nutrition Agent proposes
and self-approves the scientific validity half. Product Agent must co-sign before the change
is deployed to the live engine (per scoring governance). For this task, the Nutrition Agent
may implement the fix to the salty-snacks rescore only — do not update any live category
scores until Product Agent signs off on the rule as a general engine change.

### 4. Rescore the salty-snacks corpus

After implementing the fix, rerun BSIP2 on all 54 salty-snacks products.

Output: new `bsip2_outputs/run_salty_snacks_002/` with updated traces.
Regenerate `salty_snacks_frontend_v2.json` and copy to bari-web.

### 5. Verify the outcome

Confirm:
- Bamba scores C (approximately 48–58 range) — not forced, emergent from the extrusion signal
- Bisli scores C or D depending on other signals (high sodium, E150c)
- Corn puffs with E-numbers remain D/E (the E-number signals still fire on top)
- Plain rice cakes retain their A/B score (not reclassified)
- Score distribution across the corpus is plausible (no category-wide collapse to D/E)

## Acceptance criteria

- [ ] Extrusion detection signal designed and documented — no brand hardcoding
- [ ] Signal validation against full 54-product corpus with false-positive analysis
- [ ] BSIP2 engine updated with the new signal
- [ ] Salty-snacks corpus rescored: `run_salty_snacks_002/` complete (54 traces)
- [ ] Bamba final score in C range (approx 48–58) — confirm it's score-emergent, not forced
- [ ] Plain rice cakes retain A/B score — confirm not reclassified by extrusion signal
- [ ] `salty_snacks_frontend_v2.json` generated and copied to bari-web
- [ ] D7 co-sign block noted: signal is approved for salty-snacks rescore; full engine
      promotion requires Product Agent co-sign (separate step)

## Return block

Report:
1. Which extrusion detection approach was selected and why
2. False-positive analysis: any non-extruded products that triggered the signal?
3. Products reclassified (NOVA 2 → 4) and their score shifts
4. Bamba: old score → new score, with trace confirming the extrusion signal fired
5. Plain rice cakes: score unchanged — confirm
6. Full grade distribution shift (old vs new)
7. Recommendation on whether the signal is ready for full engine promotion (all categories)
   or needs scoping constraints first
