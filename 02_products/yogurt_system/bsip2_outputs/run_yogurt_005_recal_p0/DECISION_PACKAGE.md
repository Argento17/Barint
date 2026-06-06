# TASK-169D — Yogurt recal decision package (run_yogurt_005_recal_p0)

**Status:** DECISION MODEL ONLY. No live score, no frontend JSON shipped. Published dirs
(run_yogurt_003 / run_yogurt_004) + live `yogurts_frontend_v2.json` untouched. Owner decides
the ceiling (option a vs b) before any reship is scoped.

- **Run id:** `run_yogurt_005_recal_p0`
- **Engine config hash (with 169D trim flag present, default OFF):** `38654862b46baaac`
- **Corpus:** `03_operations/bsip1/run_yogurt_003/output` (n=86, the frozen yogurt corpus)
- **Flags:** `BARI_RECAL_P0` (recal) + `BARI_RECAL_P0_YOGURT_TRIM` (169D option-b trim, default OFF)

---

## 1. Before → after distribution (live/OFF → recal/ON, same HEAD)

| grade | OFF (flag-OFF baseline) | ON (recal, option a) |
|---|---|---|
| S | 0 | **3** |
| A | 0 | **11** |
| B | 29 | 30 |
| C | 32 | 24 |
| D | 24 | 18 |
| E | 1 | 0 |

Recal moves: 86 products, broad lift; new top tier = **11 A / 3 S** (option a). This MATCHES
the P0 v1.1 acceptance check A6 (11 A / 3 S) — NOT the v1.1 §3 headline table's "14 A / 3 S"
(that figure was an internal inconsistency in the model doc; the verified rescore confirms
the A6 number, 11 A / 3 S).

### S-list (option a) — all 3 reach S via the +8 culture bonus on a high base
| score | protein g | protein_dim | nutrient_density | +8 | OFF | name |
|---|---|---|---|---|---|---|
| 98.8/S | **190.0 (CORRUPT)** | 85.0 | 100 | +8 | 78.2/B | יוגורט גו נטול לקטוז |
| 97.0/S | 12.5 | 78.6 | 92.5 | +8 | 71.8/B | יוגורט GO חלבון 25 גרם |
| 93.2/S | 10.0 | 63.8 | 75.0 | +8 | 70.3/B | יופלה GO מועשר בחלבון |

> **DATA-INTEGRITY FLAG:** `יוגורט גו נטול לקטוז` (bsip1_7290116932620) carries
> **protein_g = 190.0 / 100 g** at only 86 kcal — physically impossible (190 g protein ≈
> 760 kcal). The corrupt value pre-exists in published run_yogurt_004 (78.2/B there); recal's
> +8 exposes it as a false 98.8/S. This S is an artifact of bad corpus data, not a scoring
> outcome. It must be corrected/withheld regardless of which option is chosen — so the
> *legitimate* option-a top is effectively **2 real S (GO 25g, יופלה GO) + 1 corrupt S**.

### A-list (option a) — 11 products
| score | protein g | +8 | OFF | name |
|---|---|---|---|---|
| 87.0/A | 10.0 | +8 | 78.2/B | דנונה פרו 20 גרם חלבון |
| 87.0/A | 10.5 | +8 | 78.7/B | דנונה פרו 21 חלבון 0% |
| 86.2/A | 11.2 | +8 | 77.0/B | יוגורט פרו עם שוקולד |
| 84.8/A | 12.5 | **none** | 75.0/B | מולר אקטיב לבן 0% 25 חלבון |
| 81.4/A | 5.2 | +8 | 74.9/B | יוגורט ביו 1.5% |
| 81.4/A | 5.2 | +8 | 74.9/B | יוגורט ביו תנובה 1.5% |
| 80.9/A | 5.3 | +8 | 73.9/B | יוגורט ביו 3% |
| 80.9/A | 5.3 | +8 | 73.9/B | יוגורט ביו תנובה 3% |
| 80.8/A | 3.8 | +8 | 66.7/B | יוגורט עזים טבעי 3% |
| 80.7/A | 5.3 | +8 | 74.0/B | יוגורט ביו 1.7% דנונה |
| 80.1/A | 5.0 | +8 | 73.3/B | יוגורט נטול לקטוז 3% שומן |

Note: 10 of 11 A's depend on the +8; `מולר אקטיב 25 חלבון` reaches A on protein mass alone
(no +8 — it routes without a qualifying cultured-yogurt subtype/marker). The low-protein bio
yogurts (5 g) reach A almost entirely on the +8 stacked on a B-level base.

---

## 2. Culture-gate audit — the +8 fires only on genuine cultured yogurt

- **Received +8: 35 yogurts.** Subtype split: yogurt 24 / protein_yogurt 7 / bio_yogurt 3 /
  greek_yogurt 1. NOVA split: NOVA-3 ×29, NOVA-2 ×6.
- **Leaks: 0.** No non-yogurt-subtype, no plain fluid milk, no plant drink received the +8.
  The gate keys on the real router yogurt SUBTYPES (per 169A router note — there is no
  top-level `yogurt` category; all dairy routes to `dairy_protein`).
- **Spot-check of correct EXCLUSIONS (no +8):**
  - `יוגורט תות 3%`, `יוגורט אפרסק 3%`, `מולר מיקס …`, `יופלה GO תות/אפרסק` — all NOVA-4
    (fruited / mix-in / sweetened) → blocked by the `nova_level ≤ 3` gate and the
    flavored-variant clause. Correct: these are not plain cultured yogurts.
  - `יוגורט ביו נטורל 2.8%` (NOVA-2, plain bio) — got **no +8** (FALSE exclusion). Cause:
    its "ingredient list" field is **marketing copy** ("…עם פירות… גרנולה, דבש מתוק…") and the
    word `דבש` (honey) trips the flavored-variant clause. This is OCR / marketing-text bleed
    in the corpus (same class flagged in run_yogurt_004 provenance), **not** a gate-logic
    fault. The gate is correct; the input field is contaminated.

---

## 3. R1-anchor top-trim model — option (a) vs option (b)

**Finding on the literal "R1 yogurt anchor":** the dedicated yogurt protein scale
(`PROTEIN_SCALE_TABLES["yogurt"]`) is currently **UNWIRED** — yogurt protein scores through
the shared `dairy_protein` scale. Routing yogurt through the yogurt scale does **NOT trim the
top**; it is more generous at the typical-yogurt midrange (5 g → 58 vs 35) and would **raise**
counts to ~25 A. The yogurt anchor is a category-relative *lift*, not a *trim*. The actual
top-trim lever is the **+8 stacking** that pushes an already-high base over 90 — so option (b)
is modeled as an **A-ceiling on the yogurt +8** (precedented cheese A-ceiling construct):
a +8 fired via the yogurt-subtype path may lift to A but cannot, by itself, manufacture an S.

| | **(a) accept as-is** | **(b) yogurt +8 A-ceiling trim (89.9)** |
|---|---|---|
| S count | 3 (1 corrupt) | **0** |
| A count | 11 | **14** |
| Mechanism | +8 lifts top over 90 | +8 capped at 89.9 pre-floor for yogurt-subtype recipients |
| Products moved | — | exactly 3: S→A (GO lactose-free, GO 25g, יופלה GO) |
| Collateral | — | **none** (only the 3 S's move; verified surgical) |

Trim drops (a → b): `יוגורט גו נטול לקטוז` 98.8→89.9, `GO 25 גרם` 97.0→89.9,
`יופלה GO` 93.2→89.9. All other 83 products identical between (a) and (b).

### Data recommendation — option (b), the A-ceiling trim
1. **No category ceiling yet exists for yogurt**, and an S grade is the platform's strongest
   signal. The 3 S's are all engineered high-protein "GO/חלבון" SKUs lifted by a +8 culture
   bonus — they are good yogurts, but awarding the top-of-platform grade to protein-fortified
   variants over plain cultured yogurt is hard to defend editorially and invites a "best ≠
   excellent" contradiction (the frozen framing doctrine).
2. **One of the 3 S's is corrupt data** (190 g protein). Shipping option (a) would put a
   data-error product at the very top of the shelf. Option (b) caps it regardless; option (a)
   requires a separate hard data fix before it is safe.
3. **The +8 is doing the lifting, not nutrition.** Capping the +8's reach to A (not S)
   preserves the recal's category-relative lift (14 A is a richer A-tier than the old 0 A)
   while keeping S reserved for a future, genuinely-exceptional case — consistent with the
   precedented cheese A-ceiling and the snack/milk "ceiling held" discipline.
4. **It is surgical and reversible** — flag-gated, inert when OFF, moves exactly 3 products.

Option (a) is defensible only if the owner accepts S-for-high-protein-yogurt as policy AND
the corrupt SKU is fixed first.

---

## 4. Drift separation (TASK-178 lens)

**HEAD reproduces published run_yogurt_004: 24/86.** (cf. milk 13/20.)
- 62/86 differ; of those only **7 are grade-level drift**, the rest are sub-grade score
  drift (1–2 pts, same letter).
- 2 of the 7 are corpus mismatches (run_yogurt_004 contains 2 SKUs absent from
  run_yogurt_003/output → `head_off = None`).
- This is **HEAD-vs-published engine drift since the run_yogurt_004 freeze (algo 0.4.0/0.4.1)**,
  NOT a recal effect. The recal effect is measured strictly OFF→ON on the **same** HEAD and is
  cleanly isolated; the published baseline simply no longer reproduces on current HEAD.
- **The live yogurt page (run_yogurt_004) is STALE relative to HEAD** even with recal OFF
  (only 28% trace reproduction). Whichever option the owner picks, the reship must rescore
  from current HEAD, not patch the old run_yogurt_004 numbers. Flag to QA.

---

## 5. Rollback + regression

- **Flag-OFF rollback identity: 86/86 byte-identical** (OFF run twice; and OFF/trim-off ==
  OFF/trim-on — the 169D trim flag is fully inert when `BARI_RECAL_P0` is OFF).
- **Golden corpus:** clean OFF / ON / ON+TRIM (0 FAIL, 1 pre-existing flag-insensitive WARN).
- **Router regression:** all PASS OFF / ON / ON+TRIM.
- **Option-b surgicality:** ON+trim changes exactly the 3 S products vs ON; 0 collateral.

---

## 6. Deviations from the P0 v1.1 prediction
- v1.1 §3/§4 headline said **14 A / 3 S**; the verified rescore is **11 A / 3 S** (matches
  v1.1 acceptance check A6). The "14 A" in the model doc was an internal inconsistency; the
  run is authoritative.
- v1.1 did not flag the **190 g protein corrupt SKU** nor the **bio-naturel false-exclusion**
  (marketing-text bleed). Both surfaced here and are corpus data-quality issues, not engine
  faults.

## 7. Artifacts
- `off.json`, `on.json`, `run_record.json` (this dir).
- Engine (flag-gated, decision-model trim): `score_engine.py` `RECAL_P0_YOGURT_TRIM`
  (default OFF; `RECAL_P0_YOGURT_TRIM_CEILING = 89.9`).
- Harness: `03_operations/bsip2/proto_v0/src/run_169D_yogurt_recal.py`.
- Evidence registry: NO new EV entry written — option (b)'s A-ceiling is a *modeled
  alternative pending owner decision*, not an approved rule. An EV entry is authored only if
  the owner selects (b) and it goes to P1/ship.
