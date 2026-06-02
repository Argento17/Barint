# Maadanim Dairy-Boundary Review — 8 newly-routed dairy_protein products

**Owner:** Nutrition Agent · **Date:** 2026-06-01 · **Mode:** review only, **no score changes**
**Inputs read:** TASK-139A (RULING-DAIRY-A-01), TASK-139B (EV-022 culture credit), TASK-139C,
`router_misroute_fix_139C.md`
**Governing ruling:** `RULING-DAIRY-A-01` — A reachable only by clean, additive-free, **live-culture**
dairy (C1–C6); B is the truthful ceiling for the sweetened/stabilized mainstream.

---

## 1. Product list (with label evidence)

All values per 100 g. "culture" = explicit live-culture marker found in the ingredient text.

| # | Product | Protein | Fat | kcal | Added sugar | Eng. starch | Sweeteners | Live culture |
|---|---------|--------:|----:|-----:|:-----------:|:-----------:|:----------:|:------------:|
| 1 | יופלה GO מועשר בחלבון | 10.0 | 2.0 | 72 | no | — | — | **none found** |
| 2 | יופלה GO תות | 10.0 | 2.0 | 98 | yes | E1422 | — | none found |
| 3 | יופלה GO אפרסק | 10.0 | 2.0 | 99 | yes | E1422 | — | none found |
| 4 | יופלה GO פירות יער | 10.0 | 2.0 | 98 | yes | E1422 | — | none found |
| 5 | יופלה GO דובדבן 0.7% | 10.0 | 0.5 | 60 | yes | E1422 | aspartame, ace-K | none found |
| 6 | יופלה GO אפרסק 0.7% | 10.0 | 0.4 | 62 | yes | E1442 | aspartame, ace-K | none found |
| 7 | דנונ.פרו ללא סוכר פיסטוק | 10.0 | 0.0 | 55 | no | E1442 | sucralose, ace-K | **חיידקי יוגורט ✓** |
| 8 | מולר פרוטאין טופ בוטנים | 13.1 | 0.5 | 133 | yes | — | — | none found |

**Decisive nutritional signature:** every product carries **10–13 g protein/100 g** at **0–2 g fat** —
3–4× the protein of a true dairy dessert (Milky/mousse/pudding ≈ 3–4 g) and a fraction of its fat. The
base is **milk + milk proteins** (קזאינים / חלבוני מי גבינה), not a cream/dessert base. This is the
**protein-yogurt / fromage-frais archetype**, not the indulgence (dessert) archetype.

---

## 2. Recommended category assignment

**All 8 → dairy family (`dairy_protein`, subtype `protein_yogurt`). Unanimous. The router correction is
nutritionally correct.**

The boundary the router now draws is the right one, and it is **format identity, not protein number**:

- **Protein YOGURT format** (`יופלה GO`, `מולר פרוטאין`, `דנונה פרו`) → **dairy**. ✅ these 8.
- **Protein PUDDING / `מעדן`-format** (`מעדן חלבון`, `מעדן פרו`, 8.7–10 g protein) → **stay dessert**.
  The `מעדן` anchor correctly holds these in Maadanim — they are dessert-textured indulgences that
  happen to be protein-fortified. The router does **not** touch them. Correct.

Within the 8, two nutritional sub-grades (both still dairy_protein):

- **Cultured protein yogurt** — #7 דנונ.פרו (live culture confirmed). Unambiguous yogurt.
- **Protein-set fresh dairy / fromage-frais** — #1–6 יופלה GO, #8 מולר (no culture marker on label).
  Still dairy (cottage/קוטג' is already a culture-agnostic dairy_protein anchor), but the
  yogurt-defining positive is **absent**, so under RULING-DAIRY-A-01 **C3 is not met**.

**Grade consequence (informational, not applied):** **none of the 8 can reach A.** #1 is the only clean
matrix, but it still lacks a confirmed culture (fails C3); #2–8 additionally fail **C2** (modified starch
E1422/E1442) and/or carry added sugar/sweeteners. They land **B/C** — the truthful protein-yogurt band.
→ **These 8 do not pressure the unresolved A-threshold (80 vs 85);** that precondition is not triggered
by this cohort.

---

## 3. Impact on the Maadanim corpus

- Maadanim run_maadanim_001 = **200 products**. Removing these 8 → **192**.
- **The 8 are the router-surfaced tip of a larger cohort.** A high-protein (≥8 g) scan of Maadanim
  returns **37 products**, of which **23 already route to `dairy_protein`** (e.g. `מולר פרוטאין יוגורט`,
  `יוגורט GO קרמי ×3`, `דנונה פרו 20ג`, בולגרית/צפתית cheeses). Maadanim is today a **mixed corpus** —
  true dairy desserts **plus** protein yogurts/cheeses sitting in it by shelf-placement, not food identity.
- Net effect of the fix: it **increases internal consistency** (it stops splitting the same `מולר פרוטאין`
  / `דנונה פרו` family across dessert and dairy). It does **not** dilute Maadanim's editorial anchor — the
  **מילקי paradox** (indulgent dessert with an innocent icon) is *sharpened* once functional yogurts leave.
- **No live-page change now.** `maadanim_frontend_v2` is frozen; a router edit affects only future re-runs.
- Out-of-scope contaminants surfaced in passing (NOT part of this task, flag for a corpus cleanup):
  `נודלס חלבון` (protein noodles), `חטיף/נייטשר פרוטאין` (protein bars), `ממרח טחינה` — these are not dairy
  desserts at all and predate 139C.

## 4. Impact on the future dairy corpus

- The 8 (+ their already-dairy siblings) become a **protein-yogurt cluster** on the yogurt/dairy shelf —
  their correct home. They are valuable as the **"best ≠ excellent" contrast**: high protein, yet capped
  at **B/C** by modified starch + sweeteners + (mostly) absent cultures. They make the A-condition legible.
- **Culture credit (EV-022) applies unevenly and correctly:** only #7 דנונ.פרו gets the fermentation bonus;
  #1–6, #8 do not (no marker) → they score *lower*, truthfully. This is the engine reading labels honestly,
  exactly as intended.
- **Data-quality caveats to resolve before any A-eligibility claim on this family:**
  1. **Verify culture status for יופלה GO / מולר פרוטאין** — labels were OCR-truncated; "none found" may be
     extraction loss rather than true absence. Does not change the B/C outcome (additives already cap them),
     but matters if a clean GO variant ever appears.
  2. **Outlier:** `יוגורט גו נטול לקטוז` shows **protein = 190 g/100 g** (OCR/parse error) — fix before it
     enters any dairy scoring run.

## 5. Recommendation for the TASK-139B re-score

1. **Approve all 8 → `dairy_protein` / `protein_yogurt`.** Nutritionally settled; no objection.
2. **Do it as one coordinated migration, not piecemeal.** Fold these 8 into the **same maadanim re-score
   already flagged in 139B** (the ~30-SKU culture-credit event). Migrate the **whole protein-yogurt cohort**
   (the 8 + the 23 already-dairy protein yogurts/`GO`/`מולר פרוטאין`), so the yogurt shelf and the slimmed
   Maadanim shelf are produced in one consistent pass.
3. **Keep `מעדן`-format protein desserts in Maadanim** (`מעדן חלבון`, `מעדן פרו`). They are correctly dessert
   — do not let the protein number pull them out.
4. **No A-threshold blocker from this cohort.** All 8 are A-ineligible on C2/C3 → the 80-vs-85 reconciliation
   inherited by 139B is **not gated by these products**; they can re-score to B/C immediately once the shelf
   split is approved.
5. **Hold the live `maadanim_frontend_v2` publish** until Product co-signs (a) the corpus split and (b) the
   destination yogurt shelf existing — these products should *move*, not vanish. Consistent with this review's
   no-score-change constraint.
6. **Resolve the two data-quality flags** (culture verification for GO/מולר; the 190 g protein outlier)
   before the dairy re-score is treated as authoritative.

**Bottom line:** the router was right — all 8 are protein yogurts, not desserts. Move them, score them under
the yogurt standard (most land B/C, none reach A), and execute it inside the already-planned 139B maadanim
re-score with Product co-sign. No scores change until then.
