# TASK-135 — Yogurt Engine Calibration Impact Audit

**Owner:** nutrition-agent · **Date:** 2026-06-01 · **Parent:** TASK-135 (DEC-005 retirement)
**Type:** AUDIT ONLY — no score tuning, no implementation, engine 0.4.0 read unmodified.
**Inputs read:** `TASK-135.md`, `reconciliation_135_run_yogurt_003_findings.md`,
`run_yogurt_003_run_summary.json` (88 traces), 4 representative BSIP2 traces,
`router_v2.py`, `score_engine.py`, `constants.py`, `ingredient_enricher.py`,
all 88 BSIP1 inputs (`run_yogurt_003/output/`).

**Purpose:** Quantify the impact of the three calibration gaps the run_yogurt_003
reconciliation identified, so TASK-135 has a costed, ordered fix path before any
run_yogurt_004. This audit *measures*; it does not change scores or code.

---

## TL;DR — the three gaps are not equal

| Gap | What it breaks | Products hit | Score impact | Verdict |
|---|---|---:|---|---|
| **(2) Culture detection** | The yogurt-defining *positive* signal is invisible | **54/88 carry culture text; ~33 NOVA≤3 get the real lift** | **+8.2 pts** each (NOVA≤3); moves 2–5 into grade A | **Highest impact — fix first** |
| **(1) Router** | Category *identity* (yogurt shown as dessert/cereal); corpus purity | **18/88 anomalies** (16 misrouted yogurts + 2 non-yogurt false positives) | **~0–2 pts each** (small) — this is an *identity/editorial* defect, not a score defect | Fix second |
| **(3) A-ceiling** | Whether plain live-culture yogurt *can* reach A | Whole category | Derivative of (2) | **Decide AFTER (2) re-runs — likely no philosophy change needed** |

The counter-intuitive headline: **the router gap barely moves scores** (the binding
caps are NOVA-driven and category-independent), while **the culture gap is the real
score story** and is also what actually governs the ceiling. Prioritize accordingly.

---

## Gap 2 — Culture / fermentation detection (HIGHEST SCORE IMPACT)

### 2.1 Measured miss rate
- Current `FERMENTATION_TERMS` (`ingredient_enricher.py:335`) match **0 / 88** products.
  Direct grep of all 88 BSIP1 inputs for the *current* term list
  (`תרבויות`, `ביפידובקטריום`, `לקטובציל`, `חיידקים חיים`, `תסיסה לקטית`) = **0 files**.
- Grep for the *Israeli label vocabulary actually used*
  (`ביפידוס`, `פרוביוטי`, `חיידק…`, `תרבית`, `BIFIDUS`, `אצידופילוס`) = **54 / 88 files (61%)**.
- Confirmed in-trace: e.g. `7290014758117` (יוגורט ביו תנובה 1.5%) ingredient text reads
  `בתוספת חיידקי ביפידוס` → trace still shows `has_fermentation: false`. The defining
  quality marker of a live-culture yogurt is present on the label and never credited.

**This is a pure vocabulary-coverage gap, not a data gap.** The corpus has the signal;
the dictionary doesn't.

### 2.2 Exact score mechanism (read from `score_engine.py`)
`has_fermentation == True` triggers two additive effects, both pre-cap:
1. `score_whole_food_integrity()` (line 497): **+5** to the WFI dimension → ×0.04 weight = **+0.20** weighted.
2. **R-02 direct fermentation bonus** (line 1011–1016): **+`FERMENTATION_DIRECT_BONUS` = 8**
   added straight to the weighted score — **but only when `nova_level <= 3`** (`constants.py:111`).

So the per-product gain from fixing detection is:
- **NOVA ≤ 3 product: +8.2 pts** (8 direct + 0.2 WFI), subject to the binding cap.
- **NOVA 4 product: +0.2 pts** (WFI only — the direct +8 is gated off).

This gating is *correct and important*: it credits cultures in clean plain/bio yogurts
(NOVA 2–3) but does **not** rescue sugar-laden flavored yogurts (NOVA 4). The fix is
self-limiting to exactly the products that deserve it.

### 2.3 Quantified impact
- **NOVA distribution (run 003):** NOVA 2 = 4, NOVA 3 = 31, NOVA 4 = 53.
- **Culture-bearing AND NOVA ≤ 3 ≈ 33 products** (intersection of the 54 culture-text files
  with the 35 NOVA≤3 products — virtually all plain/bio/Greek/probiotic lines carry the text).
- Each of those ~33 gains **+8.2 pts**, none capped out (their weighted scores 57–78 sit
  far below their NOVA-3 cap of 87, so the bonus flows through in full).

Worked examples (current → projected with culture credit):
| Product | Current | NOVA | Cap | Projected |
|---|---:|---:|---:|---:|
| יוגורט גו נטול לקטוז (top) | 78.2/B | 3 | 87 | **~86.4/A** |
| יוגורט ביו נטורל 2.8% | 72.1/B | 2 | — | **~80.3/A** |
| יוגורט ביו תנובה 1.5% | 66.7/B | 3 | 87 | **~74.9/B** |
| יוגורט עיזים ביו 3% | 62.4/C | 3 | 87 | **~70.6/B** |

→ Culture credit alone lifts the plain/bio tier by a full grade band in several cases
and produces the **first grade-A products in the entire machine run (≈2–5 of them)**.

> **Compounding data-quality note (not one of the 3 gaps, but it suppresses the same tier):**
> The enricher also produces a **false-positive added-sugar hit** on plain yogurts —
> it matches `סוכר` inside `סוכרים` (the *"X גרם סוכרים"* nutrition declaration that Shufersal
> crams into the ingredient string). Seen in `7290014758117`: `added_sugar_matches: ["סוכר"]`
> on a plain bio yogurt with no added sugar. It didn't fire a cap here (single marker), but it
> contaminates `added_sugar_sources_count` and risks tipping borderline products into sugar caps.
> Recommend ingredient/nutrition-text separation in BSIP1 be checked during the culture fix.
> (Same root cause as the `protein_g: 190` parse artifact in the lactose-free trace — label
> nutrition text is leaking into ingredient parsing.)

---

## Gap 1 — Router yogurt-anchor gap (IDENTITY defect, small score impact)

### 1.1 Measured misroute set (counted from `run_yogurt_003_run_summary.json`)
**18 / 88 routing anomalies** = 16 misrouted yogurts + 2 non-yogurt false positives:

| Routed to | Count | Products |
|---|---:|---|
| `dessert` | 10 | יופלה GO ×6 (321031/321680/321697/321703/323585/323592); דנונה ביו מולטי (558284); דנונ.פרו פיסטוק (558314); דנונה פרו 20 וניל 0% (330352); דנונה יווני מארז (115678222) |
| `cereal` | 2 | מולר מיקס קורנפלקס מצופה (394081); יוגורט קראנצ קורנפלקס (346629) |
| `snack_bar_granola` | 2 | מולר מיקס כדורי דגנים (397617); מולר פרוטאין טופ בוטנים (314596) |
| `whole_food_fat` | 2+1 | מולר מיקס שקדים ובוטנים (397600) **[yogurt]**; **זית ירוק יווני ×2 (735045/735052) [NOT yogurt — false positives]** |
| `default` | 1 | מולר פרופ אפרסק פסיפלורה (390465) |

(This is 18 vs the reconciliation's "17/88"; the 1-product difference is a classification
edge — immaterial. Either way ≈20%.)

### 1.2 Root-cause classification (read from `router_v2.py`)
The `יוגורט` hard anchor (`HARD_ANCHORS`, 0.92) **works when present** — products named
`יוגורט קראנצ פצפוצים` / `יוגורט קראנצ תות קורנפלק` / `יוגורט קרנצ כדורי דגנים` all correctly
held `dairy_protein` despite crunch/cornflake tokens. The gap is structural, in 3 causes:

- **RC-1 — Brand-as-identity miss (no `יוגורט` token in the name): ~10 products.**
  `יופלה GO …`, `דנונה ביו מולטי`, `דנונה פרו …` carry a *brand* (יופלה/דנונה/מולר) + flavor but
  not the literal word `יוגורט`. With no dairy anchor and `_DAIRY` signals being `name_only`,
  nothing dairy fires; weak dessert signals win by default. **This is the dominant cause.**
- **RC-2 — Topping/crunch token dominates when `יוגורט` is absent: ~5 products.**
  `מולר מיקס קורנפלקס`, `מולר מיקס כדורי דגנים`, `מולר מיקס שקדים`, `מולר פרוטאין טופ בוטנים` →
  the `קורנפלקס` anchor (0.93) / `גרנולה`-`snack` / WFF nut signals out-rank a yogurt identity
  that the name never asserts.
- **RC-3 — `יווני`/olive false positive: 2 products (corpus-curation defect, not router).**
  `זית ירוק יווני` (green olives) leaked the BSIP1 include-filter on the `יווני`/"Greek" token.
  The router *correctly* called them `whole_food_fat`; they should never have been in the corpus.

### 1.3 Score impact — deliberately measured, and it is SMALL
The category lever in `score_engine.py` is almost entirely the **calorie-density table**
(`CALORIE_DENSITY_TABLES`, weight 0.15). Everything else that sets these scores — the
NOVA cap (NOVA 3→87, NOVA 4→68/60), additive penalties, protein, sugar, sodium — is
**category-independent**. Comparing tables at yogurt kcal (50–120):

| kcal | yogurt | dessert | cereal | snack | default | WFF |
|---:|---:|---:|---:|---:|---:|---:|
| 60 | 95 | 85 | 85 | 90 | 90 | 90 |
| 100 | 88 | 85 | 85 | 90 | 90 | 90 |

→ Re-routing a misrouted flavored yogurt back to the yogurt table changes calorie-density
by ≈0–10 points = **≈0–1.5 weighted pts**. Verified against the data: every misrouted
NOVA-4 yogurt already carries its NOVA-4 cap (68/60) regardless of category, so the cap
doesn't move. **Net router-correction score movement ≈ 0–2 pts per product.**

Two caveats worth flagging (not score-moving today, but latent):
- `cereal` routing exposes products to the `HP_CRUNCH_SWEET_COMBO` penalty (cereal-only,
  `score_engine.py:721`) — a yogurt wrongly in `cereal` can be *over*-penalized.
- `whole_food_fat` routing uses a very lenient calorie table (≤350 kcal → 90) — a
  nut-topped yogurt mis-parked in WFF can be *over*-credited.

**Conclusion:** the router gap is an **identity / editorial-integrity** problem (a yogurt
displayed as "dessert" or "cereal" breaks the shelf, and 2 olives pollute the corpus), and
only a marginal **score** problem. Fix it for shelf correctness, not for the numbers.

---

## Gap 3 — The A-ceiling question (a Nutrition/Product decision, largely dissolved by Gap 2)

### 3.1 The question as posed
Run 003 tops out at **78.2/B**; the DEC-005 manual shelf tops at **88/A** (plain תנובה 3%).
Reconciliation framed it: *does Bari accept that mainstream Israeli yogurt tops out at B, or
should plain live-culture yogurt reach A?*

### 3.2 Audit finding: the ceiling is mostly an artifact of Gap 2, not a philosophy gap
Grade A = ≥ 80 (`GRADE_THRESHOLDS`). The reason no product reaches it is **not** a punitive
ceiling — it is that **the single positive that distinguishes a live yogurt is being scored as
zero.** Restore it (Gap 2) and:
- `+8.2` lifts the cleanest plain/bio/lactose-free yogurts to **80–86 → grade A organically**,
  with no change to scoring philosophy.
- The flavored NOVA-4 majority stays at C/D — **correctly**, because they genuinely contain
  added sugar + modified starch + stabilizers. That part of the run-003-vs-manual gap is *true*.

So a large share of the "missing A-ceiling" is simply the culture-detection gap wearing a
philosophy costume.

### 3.3 The residual, genuine philosophy question
After culture credit, one real disagreement remains: plain Israeli yogurts read as **NOVA 3**
(milk + **milk powder** `אבקת חלב` + culture), which costs ~20 pts across `processing_quality`
(65 vs 95) and `whole_food_integrity` (60 vs 100) and sets the 87 cap. The honest question is
narrower than "can yogurt reach A?":

> **Is plain set yogurt made from milk + milk-powder + live cultures a NOVA 2 product
> (minimally processed, fortified) or a NOVA 3 product (processed)?**

- If the engine's **NOVA 3** read stands, mainstream Israeli yogurt's *defensible* ceiling is
  **low-A / high-B (~80–86)** for the very cleanest, B for the rest — and Bari should retire the
  manual shelf's blanket 88/A as **over-generous format-credit the engine correctly disciplines.**
- If milk-powder-set plain yogurt should be **NOVA 2**, the cleanest tier rises further and a
  broader A-band returns — closer to the manual shelf.

**Audit recommendation:** Do **not** decide this in the abstract. Fix Gap 2, re-run, and read
the actual post-culture distribution. My expectation: the NOVA-2-vs-3 question becomes the
*only* remaining lever, and it is a small, well-scoped scoring-philosophy call — not a
category-wide recalibration. The manual shelf's 5×A is not reproducible and **should not be**
the target; ~2–5 earned A's on the cleanest plain/bio/lactose-free lines is the truthful outcome.

---

## Recommended fix order, expected movement, and run_yogurt_004 call

### Fix order (with rationale)
1. **Gap 2 — Enricher culture vocabulary (FIRST).** Highest score impact (+8.2 to ~33 products),
   smallest blast radius (yogurt-specific terms; governed BSIP1 change), and it is the
   *precondition* for answering Gap 3. You cannot judge the ceiling while the defining positive
   reads zero. While in the enricher, also fix the `סוכרים→סוכר` added-sugar false positive and
   the nutrition-text-in-ingredients leak (same root cause).
2. **Gap 1 — Router (SECOND).** Add a yogurt identity that survives a missing `יוגורט` token —
   strongest option is a **category prior carried from the BSIP0 yogurt-shelf acquisition query**
   (everything here was scraped *as yogurt*), plus brand anchors (יופלה / דנונה ביו / מולר in a
   dairy-format context). Separately, **drop the 2 olive false positives at curation** (tighten the
   `יווני` include-filter so it requires a dairy co-token). Low score impact; high shelf-integrity impact.
3. **Gap 3 — Ceiling philosophy (THIRD, AND ONLY AS A READ-OUT).** After 1+2 re-run, decide the
   single narrow NOVA-2-vs-3 question for milk-powder-set plain yogurt. Likely no broad change needed.

### Expected score movement after fixes (run_yogurt_004 projection)
| Cohort | n (≈) | Movement | Result |
|---|---:|---|---|
| Plain / bio / Greek / lactose-free, NOVA 2–3 | ~33 | **+8.2** (culture) +0–1.5 (route) | tier rises to ~74–86; **2–5 cross into A** |
| Flavored / crunch / protein-dessert, NOVA 4 | ~50 | ~0 (ferm gated off) ±0–2 (route) | stays C/D — correct |
| Olive false positives | 2 | removed | out of corpus |
| **Category median** | 88 | 57 → **~61–63** | still < manual 72 (truthfully — flavored lines carry sugar) |
| **Grade A count** | — | 0 → **~2–5** | first earned A's; not the manual 5×A by format |

### Recommendation for run_yogurt_004
- **GO to build run_yogurt_004 — but sequence it: enricher (Gap 2) → router/curation (Gap 1) →
  re-run → then read Gap 3.** Each is scoped, governed, and reversible.
- run_yogurt_004 will **narrow but not close** the gap to the DEC-005 manual shelf, and that is
  the correct outcome: the engine credits cultures (fixing the real defect) without restoring the
  manual shelf's blanket format-credit A-tier. Expect a defensible ~2–5 A's, not 5×A-by-format.
- **DEC-005 stays until** run_yogurt_004 clears the same bar a normal category launch must:
  culture-credited scores, clean routing, 0 false positives, and editorial/QA validation of the
  insight lines. This audit does not itself unblock TASK-135; it costs and orders the work that can.

*nutrition-agent · TASK-135 calibration impact audit · 2026-06-01 · audit only — no scores changed, no code modified · engine 0.4.0 read at proto_v0*
