# Milk Re-baseline — Rescore on Pinned Engine Baseline + Owner Sign-off Memo

**Task:** TASK-180A (Step 1 of TASK-180; executes the TASK-178 audit re-baseline plan)
**Date:** 2026-06-04
**Author:** Data Agent (bari-category-factory / bari-qa-audit / bari-bsip2-scoring-governance)
**Type:** Rescore + model only. **No score shipped, no frontend JSON changed, no engine edited.**
**Status:** Awaiting owner sign-off gate. Stops here — does NOT proceed to snack (180B) or bread (180C).

---

## 0. Headline (most important first)

- **Frozen invariant HELD.** Milk top trio (whole 3.4% / natural 4% / goat) reproduces
  **exactly 85/A** on the pinned baseline. **No frozen-top move. No STOP-and-escalate condition.**
- **One grade flip needs owner approval:** Alpro Choco soy drink `bsip1_5411188300328`
  **38.1/D → 34.5/E (−3.6)**. It is a *downward, mid/lower-shelf* move (a sweetened soy
  drink dropping one grade) — defensible, but it is a grade change and requires owner sign-off.
- **Reproduction rate 13/20 (65%) confirmed** against the published `run_004_recalibrated`.
  The audit's classification (1 D→E flip + 2 ≥2pt same-grade + 4 cosmetic) is **confirmed, not corrected.**
- All 7 misses are **mid/lower shelf**; all 3 grade-affecting moves are **downward**
  (the re-baseline tightens these scores, it does not inflate them — unlike bread/snack).

---

## 1. Step 0 — Engine baseline pinned

| Item | Value |
|---|---|
| Tag | `engine-baseline-2026-06-04` (annotated) |
| Commit | `f075d9e077cba3db6e50f3b85eff23a9af352992` (= HEAD, branch `cc-agent-v2`) |
| Pre-tag dirty check | `score_engine.py`, `constants.py`, and all tracked `proto_v0/src` modules **clean** at HEAD (0 tracked modifications). The only working-tree entry under `proto_v0/src` was one **untracked** helper (`run_169E_snackbars_recal.py`), which is not in any commit and does not affect what the tag pins. |
| Result | Tag created and verified to point at HEAD. Closes the pre-git engine-pin gap (git init 2026-06-01 post-dated all May freezes). Every legacy rescore from here is bisectable to this tag. |

---

## 2. Step 1 — Milk rescore on the pinned baseline

- **Runner:** `03_operations/bsip2/proto_v0/src/batch_run_milk_005_headpin.py`
- **New run dir (does NOT overwrite run_004):**
  `02_products/milk_and_alternatives/intelligence_bsip2/run_005_headpin/`
  (20 per-product `bsip2_trace.json` + `run_record.json`)
- **BSIP1 source:** `03_operations/bsip1/run_milk_002/output` — the **same corpus** that
  produced published `run_004_recalibrated`, so every delta below is engine state, not corpus change.
- **Comparison:** HEAD `final_score_estimate`/`grade_estimate` vs published `run_004_recalibrated` trace.

### 2.1 Reproduction + classification (from the actual HEAD re-run)

| Metric | Value |
|---|---|
| Published scored | 20 |
| Reproduced exactly | **13 / 20 (65%)** |
| Grade-affecting (flip OR \|Δ\|≥2pt) | **3** |
| — grade flips | 1 |
| — ≥2pt same-grade | 2 |
| Cosmetic (<2pt, same grade) | 4 |

This **confirms** the TASK-178 figure (13/20) and its split (1 flip + 2 ≥2pt + 4 cosmetic).

### 2.2 Per-product delta table — the 7 non-exact products

| Product ID | Name (he) | Published | HEAD | Δ | Class |
|---|---|---|---|---|---|
| `bsip1_5411188300328` | אלפרו שוקו משקה סויה | 38.1/D | **34.5/E** | **−3.6** | **GRADE FLIP D→E** |
| `bsip1_7290107932134` | חלב בבקבוק 1% מועשר — מהדרין | 60.2/C | 56.6/C | −3.6 | ≥2pt same-grade |
| `bsip1_7290114313285` | מולר פרוטאין משקה בננה 25g | 49.6/D | 46.5/D | −3.1 | ≥2pt same-grade |
| `bsip1_5411188112709` | אלפרו שקדים ללא סוכר | 45.3/D | 47.1/D | +1.8 | cosmetic |
| `bsip1_7290014760141` | משקה שקדים | 52.7/C | 54.5/C | +1.8 | cosmetic |
| `bsip1_7290110324773` | משקה חלב גו 27g חלבון 2% וניל | 41.4/D | 40.4/D | −1.0 | cosmetic |
| `bsip1_7290119385560` | משקה סויה בריסטה אלפרו 500ml | 48.7/D | 48.4/D | −0.3 | cosmetic |

The other **13** products reproduce exactly (|Δ| < 0.05, same grade) and need no sign-off.

---

## 3. Step 2 — Frozen-invariant check (CLAUDE.md)

**Invariant:** "Milk scores = run_004_recalibrated. Top = 85/A (whole/4%/goat dairy). No reversion."

| Product ID | Item | Expected | HEAD | Status |
|---|---|---|---|---|
| `bsip1_7290000051352` | חלב מלא בטעם של פעם 3.4% (whole) | 85/A | **85/A** | **HELD** |
| `bsip1_7290019790259` | חלב טבעי 4% (natural 4%) | 85/A | **85/A** | **HELD** |
| `bsip1_7290102392094` | חלב עיזים (goat) | 85/A | **85/A** | **HELD** |

**All three HELD exactly. No frozen-top move appeared. No STOP-and-escalate condition triggered.**
The 7 drifts are all mid/lower shelf; none touch the frozen top.

---

## 4. Owner sign-off memo — grade-affecting milk moves requiring approval

Sign-off is requested on the **3 grade-affecting moves**. (The 4 cosmetic <2pt moves and the
13 exact reproductions are listed for completeness but do not change a published grade and need
no decision.) All 3 are **downward** — the re-baseline makes these mid/lower-shelf scores slightly
stricter; none inflate.

| # | Product | Old → New | Reason (one line) |
|---|---|---|---|
| **1** | `bsip1_5411188300328` — Alpro Choco soy drink (אלפרו שוקו משקה סויה) | **D → E (38.1 → 34.5, −3.6)** | **The only grade flip.** A sweetened, flavored NOVA-processed soy drink falls below the recalibrated D/E threshold (E < 35); on the pinned baseline it scores 34.5, 0.5pt under the line. Downward and defensible (it is a low-shelf processed drink), but it crosses a grade boundary, so it needs explicit approval. |
| **2** | `bsip1_7290107932134` — 1% fortified milk, Mehadrin (חלב בבקבוק 1% מועשר) | **C → C (60.2 → 56.6, −3.6)** | No grade change, but a ≥2pt visible downward move on the live shelf. Stays C; surfaced because a ≥2pt shift is a defensibility-relevant change even without a flip. |
| **3** | `bsip1_7290114313285` — Muller protein banana drink (מולר פרוטאין משקה בננה) | **D → D (49.6 → 46.5, −3.1)** | No grade change; ≥2pt downward move on a processed flavored protein drink. Stays D; surfaced for the same reason. |

**Recommendation (Data Agent):** all 3 are downward, mid/lower-shelf, and consistent with the
recalibrated thresholds the rest of the shelf already uses. The single flip (#1, D→E) is the
only consumer-visible grade change and is the defensible direction (a flavored processed drink
sliding to E, not a whole food being penalised). I recommend the owner approve all three so QA
can freeze `run_005_headpin` as the pinned milk baseline. **Nothing ships until that sign-off.**

---

## 5. Next steps (gated — not executed here)

1. **Owner sign-off gate** on the 3 moves in §4 (esp. the D→E flip). — *blocking*
2. On accept → QA Agent re-runs reproduction against `run_005_headpin` (100% by construction)
   and **freezes** it as the pinned milk baseline (QA owns the freeze; Data provides run ID +
   artifacts per D9).
3. On accept → Frontend Agent regenerates `milk-comparison.json` from `run_005_headpin`.
4. Snack (180B) and bread (180C) remain **out of scope** for this task and are not touched.

---

## 6. Hard-rule / constraint compliance

- **No reship, no frontend JSON change, no engine edit.** Only new artifacts: a tag, a new
  run dir (`run_005_headpin`), a runner script, and this report. `run_004_recalibrated` untouched.
- **Every delta is from an actual HEAD re-run** of the same BSIP1 corpus vs the published trace
  — no invented values. Independently confirms TASK-178 §2a/§2b.
- **Frozen invariant named and verified:** milk top 85/A trio HELD (§3).
- **Stopped at the owner sign-off gate.** Did not proceed to 180B/180C.

---

## Artifacts

- This report: `C:\Bari\03_operations\qa\reports\milk_rebaseline_TASK-180A_2026-06-04.md`
- Pinned baseline tag: `engine-baseline-2026-06-04` → `f075d9e077cba3db6e50f3b85eff23a9af352992`
- Rescore runner: `C:\Bari\03_operations\bsip2\proto_v0\src\batch_run_milk_005_headpin.py`
- New milk run (rescore, ships nothing):
  `C:\Bari\02_products\milk_and_alternatives\intelligence_bsip2\run_005_headpin\`
  (20 traces + `run_record.json` with full delta table + invariant block)
- Source corpus: `C:\Bari\03_operations\bsip1\run_milk_002\output`
- Published baseline compared against: `…\intelligence_bsip2\run_004_recalibrated\products`
- Audit basis: `C:\Bari\03_operations\qa\reports\legacy_score_drift_audit_TASK-178_2026-06-04.md`
