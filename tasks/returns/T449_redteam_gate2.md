# Red-Team / Adversarial-QA Gate 2 — TASK-449 (brined fermentation-marker inversion fix + router fix)

**Gate:** 2 of 2 (independent adversarial QA). **Agent:** adversarial-qa-agent (Opus, independent of builders).
**Package:** branch `fix/task449-brined-inversion`, worktree `C:\bari_wt_t449`.
**Key commits verified:** engine `1a25819b`, router `6616f78a`, candidate rebuild P461 `b35058d5`, content `1c0f0223`.
**Scope:** 36 products, `/hashvaot/brined-cheeses` (the GOLDEN page).
**Method:** read artifacts directly + re-ran the engine, gates, router, and leakage checks independently. Never accepted a builder summary.
**`C:\Bari` treated read-only. No fixes applied. No push/PR/deploy. OFF ban respected (no OFF read/write anywhere).**

---

## VERDICT

**GO_WITH_FIXES.**

The core engineering is correct and independently reproducible: the flagship dimension-Pareto inversion is resolved, the fix is downward-only within brined, score↔trace↔engine parity is exact 36/36, the one retained-bonus product is a legitimate Path-A (declared-culture) exception, the router collision fix works and is score-neutral, and all changed consumer copy is leakage-clean and (for edited lines) factually grounded. Track V is GREEN on every propagation and reproduction gate.

**But two CRITICAL stale-artifact side-effects the returns did NOT disclose must be fixed before this reaches the live golden route**, plus one HIGH copy-truth defect on an edited line. None require touching the engine or the co-signed scores — they are downstream artifacts that still assert the OLD grade counts.

**Blockers to clear before owner PR:**
- **RT-1 (CRITICAL)** — stale `_meta.grade_distribution` in the candidate JSON.
- **RT-2 (CRITICAL)** — stale brined FAQ JSON-LD schema (public, machine-readable) asserting the old A-count / old top score / 8 now-downgraded products as grade A.
- **RT-3 (HIGH)** — edited `7290019635826` rowVerdict re-asserts "shortest list possible" while a 2-ingredient product is displayed.

---

## PARETO-INVERSION COUNT (THE acceptance test)

**Residual dimension-Pareto inversions in the ON-ON candidate: 2** (flagship RESOLVED).

Guardrail re-run independently on freshly re-generated ON-ON traces (definition: for a displayed pair, if B ≥ A on all 10 dimension scores with ≥1 strict, then final(B) must be ≥ final(A); any violation = inversion). Confirmed stable across two independent engine re-generations.

| better-on-all-dims (B) | final | outranked-by worse (A) | final | gap | driver |
|---|---|---|---|---|---|
| 7290019790112 (פטה כבשים 20%) | 63.5 | 7296073641902 (פטה כבשים 20%) | 64.8 | 1.30 | `SODIUM_SHELF_SURCHARGE` |
| 7290019790808 (פטה עיזים 16%) | 64.7 | 7296073641902 | 64.8 | 0.10 | `SODIUM_SHELF_SURCHARGE` |

**Flagship (bc-028 sheep 71.6 vs bc-037 cow 66.3): RESOLVED.** Cow `48413` now 67.4/B; every former marker-feta that outranked it dropped −8 and now sits below or tied. `48413` `fermentation_bonus_applied=False`, weighted_dim 79.42.

**Ruling on the 2 residual inversions — pre-existing structural residue, NOT introduced by this fix, NOT a launch blocker for this deploy:**
1. **Mechanism.** All three products lose the +8 uniformly (they were all name-marker feta), so their *relative* order is unchanged. `7296073641902` (sodium 1100 mg) outranks `7290019790112` (1500 mg) and `7290019790808` (1400 mg) because the latter two carry a second sodium charge (`SODIUM_SHELF_SURCHARGE` −4, EV-056) that is NOT reflected in the 10 dimension scores. This is precisely the **sodium double-count** structural finding logged in TASK-449 RETURN-1 (`regulatory_quality` dimension + a separate post-dimension sodium penalty) — real, and here mildly inversion-producing, but *non-causal to the flagship* and untouched by Option A (which only addresses the fermentation marker).
2. **Pre-existing.** In live: `902`=72.8/B, `808`=72.7/B, `112`=71.5/B → `902` already outranked both. The inversion existed live, masked inside a +8 cluster. This fix did not create it.
3. **Consumer-invisible severity.** Both gaps (1.30, 0.10) are inside the ≤2-pt "noise / indistinguishable" band of Comparison Governance v1. All three land in the **same C grade** (ranks 22/23/28) — no grade inversion, no adjacent-grade misrepresentation.
- **Route:** `nutrition-agent` for the standing sodium-double-count finding (a separate methodology item, TASK-449 RETURN-1 already opened it). **Does not block this deploy** — it is a pre-existing, sub-noise, same-grade residue.

---

## TRACK V — VERIFICATION (deterministic)

| # | Check | Result | Evidence (observed value) |
|---|---|---|---|
| 1 | Pareto flagship resolved | **PASS** | 48413 → 67.4/B, ferment off; former markers dropped below |
| 1 | Residual Pareto inversions | **2 (ruled pre-existing, sub-noise, same-grade)** | see table above |
| 2 | Score↔trace parity 36/36 | **PASS** | 0 mismatches (candidate score/grade == trace final_score_estimate/grade_estimate) |
| 2 | Rank == competition order + stable live tiebreak | **PASS** | 0 rank mismatches, recomputed independently |
| 2 | Barcode set == live 36/36 | **PASS** | 0 added, 0 dropped, set-equal |
| 3 | Sweep preservation 3/3 | **PASS** | 7290108509106 A/80.3, 7290108509755 B/65.7, 369617 C/50.9 — all unchanged vs worktree-live |
| 3 | Sweep exception real (not a bug) | **PASS** | see RT-note-A below |
| 4a | All 36 traces emit `fermentation_bonus_applied`+`_note` | **PASS** | 0 missing; exactly 1 True (7290108509106) |
| 4b | Step A reproduction (OFF flags → live 36/36) | **PASS (re-run by me)** | OFF-OFF engine rescore == **worktree-live** 36/36, 0 diffs |
| 4b | ON-ON reproduces candidate | **PASS (re-run by me)** | engine ON-ON == candidate scores/grades 36/36, 0 diffs; dist min 47.10/max 82.70/median 66.15/stdev 8.11 matches P461 |
| 4c | grade-distribution artifact exists + matches | **FAIL → RT-1** | `_meta.grade_distribution` says A:8 B:21 C:6 D:1; ACTUAL grades A:3 B:18 C:13 D:2 |
| 5 | Copy scope (only score/grade/rank/_meta + 12 copy fields differ) | **PASS** | 0 undeclared diffs; exactly score(24)/grade(14)/rank(34)/insightLine(3)/rowVerdict(9)=12 copy fields; `_meta.p461_construction` added (allowed) |
| 6 | Copy accuracy (edited lines) | **PASS** | all numeric/superlative claims re-checked vs traces + all-36 facts (below) |
| 7 | Router: whole milk routes dairy | **PASS (re-run by me)** | `חלב מלא`/`חלב 3%`/`חלב טרי` → dairy_protein; `לחם מלא` still bread |
| 7 | Router zero-movement | **PASS (re-run by me)** | brined OFF rescore reproduces worktree-live 36/36 with router in HEAD; bread 0 grade-moves; C10 milk drift NOT router-attributable (those products route beverage) |
| 8 | Banned phrases (incl. חלבון נמוך) | **PASS** | 0 hits in consumer copy |
| 8 | hebrew_readability on 12 changed lines | **PASS** | 12/12 `is_clean=True` |
| 8 | G1–G8 re-run (baseline = worktree-live) | **PASS w/ pre-existing debt** | Overall FAIL exit 1 driven ONLY by G1 SCHEMA + G3 SCOPE, which **also fail on the live baseline itself** (confirmed by running gates on live). G4/G5/G6/G7/G8 PASS. Candidate PASSES G5 where live FAILs (live scores are +8 inflated vs fixed traces — independent confirmation of the fix). |

**RT-note-A (sweep exception is REAL, not a bug):** 7290108509106 keeps its +8 via **Path A (declared culture)**, not the suppressed name-marker path. Its parsed ingredient list contains `תרבית לקטית` (lactic culture) → `has_fermentation=True` → `eligible_ferm = has_fermentation` (score_engine.py:3921) fires independent of the name marker. Its note is `R-02 fermentation_bonus: +8 (direct, pre-cap)` **without** the `[R7 v1.1 Path B]` suffix, confirming it did NOT route through `cultured_cheese_name`. By contrast, all 14 downgraded products have `has_fermentation=False` (milk + salt + preservative only) and previously earned +8 only from the name word. The asymmetry is honest and exactly the intended behavior: reward *declared* fermentation, stop rewarding the *word*.

**G1/G3 pre-existing debt (Hard Rule 7):** G1 (comparisonContext/satFat/limitingFactors schema) and G3 (12 scored-but-not-displayed barcodes, no `_meta` exclusions) FAIL identically on the untouched live baseline. Known live debt, not introduced here; noted, not re-flagged as a new blocker for this task. Routes to `frontend-agent`/`data-agent` as standing debt.

---

## TRACK C — CHALLENGE (adversarial)

### Public defensibility of the 14 downward flips (item 9): DEFENSIBLE
All 14 grade-flippers verified `fermentation_bonus_applied=False` AND `has_fermentation=False` — every one is a name-marker-only product with no declared live culture. Each flip is journalist-explainable in one sentence: *"The engine stopped adding 8 points for the word 'feta'/'bulgarian' in the name when the product carries no declared culture in its ingredients — that word names the cheese type, not fermentation quality above the brined baseline."* No product's new grade is indefensible against its composition (they are milk + salt + preservative simples; a B/C for a high-sodium preserved cheese with no declared culture is defensible).

### The one retained-bonus product (item 10): DEFENSIBLE
See RT-note-A. Asymmetry is grounded in a parsed ingredient (`תרבית לקטית`), observable in the trace field `has_fermentation`, and consistent with the D6/D7 co-signed rationale (declared culture = real fermentation evidence; name word ≠ evidence).

### Silent side-effects the returns did NOT surface (item 11): TWO CRITICAL FOUND
See RT-1 and RT-2. The returns' scope discipline was tight on the comparison JSON (0 undeclared diffs there), but neither builder checked the **derived/adjacent artifacts** that also encode brined grade counts: the candidate's own `_meta.grade_distribution` and the separately-shipped FAQ JSON-LD schema. Both still assert the pre-fix world.

---

## FINDINGS BY SEVERITY

### CRITICAL — must resolve before the golden page goes live

**RT-1: Candidate `_meta.grade_distribution` is stale (asserts the OLD distribution).**
- Evidence: `_rescore_staging/brined_cheeses/brined_cheeses_candidate_brinedfix.json` → `_meta.grade_distribution = {A:8, B:21, C:6, D:1}`. Actual product grades in the same file = **{A:3, B:18, C:13, D:2}** (independently counted). The field was carried over from live and not regenerated after 14 grades dropped.
- Implication: any consumer/SEO surface that reads `_meta.grade_distribution` renders a false count ("8 products earned an A" when 3 did). The live featured card recomputes counts dynamically (safe), but the JSON's own self-description is wrong and would seed any future consumer of that field.
- Routes to: `data-agent` (regenerate `_meta.grade_distribution` from actual candidate grades before deploy).

**RT-2: Brined FAQ JSON-LD schema asserts old, now-false grade claims — served on the live golden route.**
- Evidence: `bari-web/src/data/seo/brined_cheeses_faq_schema.json`, wired into the live page via `bari-web/src/app/hashvaot/brined-cheeses/page.tsx:30` (`faqKey="brined_cheeses"` → `ComparisonPageSeo` injects JSON-LD). Contains, in Hebrew consumer/schema.org text:
  - *"9 מוצרים קיבלו ציון A"* (9 products received grade A) — candidate has **3** A.
  - *"הציון הגבוה ביותר הוא 85/100"* (highest score 85/100) — candidate top is **82.7**.
  - Names ≥8 products as grade A that are now **B**, e.g. `7290019635826` (76.1/B), `7290102397334` (74.2/B), `2133162` (73.0/B), `7296073641940` (74.8/B).
- Implication: machine-readable rich-results / AI-answer markup published to Google that directly contradicts the new on-page scores. Consumer-facing false claim on the golden page. Out of the declared copy scope; neither return mentioned it.
- Routes to: `content-agent` (rewrite FAQ answers to new counts) + `data-agent` (if the schema is generator-produced, regenerate it from the candidate). This is content — requires the two-gate (Content + this gate) before it re-ships, per the content sign-off hard rule.

### HIGH — should resolve before launch

**RT-3: Edited `7290019635826` rowVerdict asserts "shortest list possible" but a 2-ingredient product is displayed.**
- Evidence: edited rowVerdict = `...עם הרשימה הקצרה ביותר האפשרית: חלב עיזים מפוסטר, מלח, חומר משמר אחד` (3 ingredients). Displayed product `3075805` (rank 25) has **2** ingredients (`חלב בקר מפוסטר, מלח`). Both are brined cheeses, so the content agent's own defense ("shortest for a preserved brined cheese") does not hold.
- This line is one of the 12 fields *edited in this change* → the false superlative is IN-SCOPE for this deploy (not merely pre-existing). Content flagged it for gate-2 ruling; ruling = the superlative is false against the displayed corpus.
- Implication: a defensibility failure a competitor/journalist can trivially disprove by pointing at 3075805 on the same page.
- Routes to: `content-agent` (drop "האפשרית", or scope to "…among 3-ingredient options", or move superlative to 3075805).

### MEDIUM — document / monitor (pre-existing live copy, truth unchanged by this rescore)

**RT-4: `369617` rowVerdict — "8 גרם חלבון בלבד, הנמוך בין גבינות השמן".** 369617 protein 8.0 g is NOT the lowest in corpus (7290114312486=7.0, 7290114312707=7.3). Defensible only if "גבינות השמן" is a real subgroup excluding those; content notes it may be a one-member group (making "lowest" vacuous/misleading). Pre-existing, NOT edited here. Routes to `content-agent`.

**RT-5: `7290102393718` rowVerdict — "28 גרם שומן ו-356 קק"ל … הגבוהים בקטגוריה".** 356 kcal IS the corpus max, but 28 g fat is 2nd (369617=31 g); the plural "highest" over-attaches to fat. Pre-existing, NOT edited here. Routes to `content-agent`.

### Copy accuracy of edited lines (verified TRUE)
- 7290108509106: 720 mg = min among fat≥13 ✓; 12 g protein / 13 g fat ✓; 3-ingredient list incl. `תרבית לקטית` ✓.
- 7290102397334: 1550 mg = max among fat≤5.5 ✓; ≈550 mg above median (1000) ✓; protein 20.5 among category-high ✓.
- 2133162: protein 21 g = max among fat≤5.5 ✓; sodium 1300 = median+300 ✓.
- 7296073641902: sodium 1100 = median+100 ✓; grade C cited ✓.
- 7290019790112: sodium 1500 = median+500 ✓; grade C ✓.
- 7290102393718: 356 kcal = corpus max ✓; grade C ✓.
- 7296073641964: butter-in-list differentiator, grade B retained, boundary claim removed ✓.
- 7290017065236: sodium 1010 on median, grade C ✓.
- Deliberately-kept superlatives (554457/554532 lowest-sodium-in-A tied at 600 mg; 3075805 highest sodium 1628; 7290114312486 lowest score) re-verified against all 36 ✓.

### Content-log self-count note (informational, not a finding)
The content gate-1 log states "4 insightLine + 8 rowVerdict"; the actual artifact diverges on **3 insightLine + 9 rowVerdict** (total 12 — correct). Field-split mislabel in the log's own self-count; the 12 changed fields exactly match the enumerated products. No scope impact.

---

## ROUTING TABLE

| Finding | Severity | Owner | Recommended action (I do not implement) |
|---|---|---|---|
| RT-1 stale `_meta.grade_distribution` | CRITICAL | data-agent | regenerate from actual candidate grades (A:3 B:18 C:13 D:2) |
| RT-2 stale FAQ JSON-LD schema | CRITICAL | content-agent + data-agent | rewrite FAQ to new counts/top-score; re-run two-gate |
| RT-3 "shortest possible" false superlative (edited line) | HIGH | content-agent | drop/scope the superlative on 7290019635826 |
| RT-4 369617 oil-cheese "lowest protein" | MEDIUM | content-agent | scope or drop (pre-existing) |
| RT-5 393718 fat/calorie pair-claim | MEDIUM | content-agent | attach "highest" to calories only (pre-existing) |
| 2 residual sodium-double-count Pareto inversions | (standing) | nutrition-agent | TASK-449 RETURN-1 sodium-double-count item; sub-noise, same-grade, non-blocking |
| G1/G3 schema/scope debt | (standing) | frontend-agent / data-agent | pre-existing live debt (fails on live too) |

---

## What an outside reviewer would still ask (independence self-check)
Track V is green partly because I reproduced the numbers from the engine — that is genuine, not "internally consistent with a wrong assumption." The one place internal consistency masked a wrong value is RT-1/RT-2: the scores are right, but two *descriptions* of the score distribution (the meta field and the FAQ) still describe the pre-fix world. Caught and raised as CRITICAL rather than passed. The router "zero movement" claim was the softest builder assertion; I re-ran it and confirmed the milk drift is baseline-staleness (those products route beverage), not a router side-effect — but I did NOT independently re-run all 12 shelves, so cross-category router neutrality beyond brined+bread rests on the builder's cross-corpus proof (noted as a scoped limitation).

```json
{
  "task": "TASK-449 adversarial-qa gate 2",
  "proposed_status": "GO_WITH_FIXES",
  "verdict": "GO_WITH_FIXES",
  "artifacts": [
    {"path": "tasks/returns/T449_redteam_gate2.md", "action": "created"}
  ],
  "counts": {
    "pareto_inversions_residual": "2/36-displayed (ON-ON candidate traces, re-generated by engine twice; flagship 48413 resolved; both residual sub-2pt same-grade, driven by SODIUM_SHELF_SURCHARGE, pre-existing in live)",
    "score_trace_parity": "36/36 (candidate score/grade == trace final_score_estimate/grade_estimate; 0 mismatch)",
    "engine_reproduction_ON": "36/36 (independent ON-ON rescore == candidate scores/grades; 0 diff)",
    "engine_reproduction_OFF": "36/36 (independent OFF-OFF rescore == worktree-live; 0 diff)",
    "rank_parity": "36/36 (competition order + stable live tiebreak; 0 mismatch)",
    "barcode_parity": "36/36 (0 added, 0 dropped)",
    "sweep_preserved": "3/3 (7290108509106, 7290108509755, 369617 unchanged)",
    "ferment_field_present": "36/36 traces; fermentation_bonus_applied=True on 1/36 (7290108509106, Path A declared culture, verified)",
    "grade_flippers_defensible": "14/14 (all ferment_applied=False AND has_fermentation=False; name-marker-only)",
    "undeclared_json_diffs": "0 (only score/grade/rank/_meta + 12 copy fields differ vs worktree-live)",
    "changed_copy_leakage_clean": "12/12 (hebrew_readability is_clean=True)",
    "banned_phrase_hits": "0 (incl. חלבון נמוך, in consumer copy)",
    "gates_pass": "G2/G4/G5/G6/G7/G8 PASS on candidate; G1/G3 FAIL are pre-existing (also FAIL on untouched live baseline)",
    "critical_findings": "2 (RT-1 stale _meta.grade_distribution, RT-2 stale FAQ JSON-LD)",
    "high_findings": "1 (RT-3 shortest-possible superlative on edited line)",
    "medium_findings": "2 (RT-4, RT-5 pre-existing loose claims)"
  },
  "commands_run": [
    {"cmd": "python pareto.py (dimension-Pareto guardrail re-run on ON-ON traces)", "exit_code": 0},
    {"cmd": "python parity.py (score/trace/rank/barcode/sweep/ferment-field checks)", "exit_code": 0},
    {"cmd": "python scopediff.py (candidate vs worktree-live full recursive diff)", "exit_code": 0},
    {"cmd": "BARI_REDLABEL_CONTINUOUS_V1=on BARI_FERMENT_MARKER_BRINED_FIX_V1=off python 03_operations/page_generator/rescore_all.py --shelf brined_cheeses", "exit_code": 0},
    {"cmd": "BARI_REDLABEL_CONTINUOUS_V1=on BARI_FERMENT_MARKER_BRINED_FIX_V1=on python 03_operations/page_generator/rescore_all.py --shelf brined_cheeses", "exit_code": 0},
    {"cmd": "BARI_REDLABEL_CONTINUOUS_V1=on BARI_FERMENT_MARKER_BRINED_FIX_V1=off python 03_operations/page_generator/rescore_all.py --shelf bread", "exit_code": 0},
    {"cmd": "python 03_operations/page_generator/gates/run_gates.py <candidate> --baseline bari-web/src/data/comparisons/brined_cheeses_frontend_v2.json", "exit_code": 1},
    {"cmd": "python 03_operations/page_generator/gates/run_gates.py bari-web/src/data/comparisons/brined_cheeses_frontend_v2.json --baseline <self> (prove G1/G3 pre-existing)", "exit_code": 1},
    {"cmd": "python router_v2.classify_category on whole-milk + bread + halva names", "exit_code": 0},
    {"cmd": "python hebrew_readability.analyze on 12 changed copy lines", "exit_code": 0}
  ],
  "not_done": [
    "Independent cross-corpus router re-run on all 12 shelves (verified brined + bread only; broader router neutrality rests on builder cross-corpus proof)",
    "Rendered-DOM check of the live page (JSON/data-path verified; did not launch the Next.js app)",
    "Any fix — findings routed, not implemented (no-self-healing)"
  ],
  "self_check": "Pareto flagship resolved + 2 residual ruled pre-existing/sub-noise; engine independently reproduces candidate 36/36 (ON) and worktree-live 36/36 (OFF); 2 CRITICAL stale-artifact side-effects found (RT-1 meta grade_distribution, RT-2 FAQ JSON-LD) that the returns did not disclose; verdict GO_WITH_FIXES."
}
```
