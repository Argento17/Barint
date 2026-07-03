# Adversarial QA Report — TASK-461 Phase-2 #4: HUMMUS copy overhaul (57 products)

Challenger: adversarial-qa-agent (Opus, independent lane) · Date: 2026-07-02
Category: hummus · Route: /hashvaot/hummus · Artifact: `hummus_copy_overhaul.json`
Candidate sha256: `50f4be85e91848c3c3224e65842adf6068ecffc04e393541b8220194325a24b6` (VERIFIED — matches spec)
Baseline: origin/master blob `2fbd70fd…` (`bari-web/src/data/comparisons/hummus_frontend_v5.json`, fetched independently — blob confirmed)

---

## VERDICT: GO_WITH_FIXES

Track V (verification) is fully GREEN. Track C (challenge) has **0 CRITICAL, 0 HIGH, 3 MEDIUM**.
The 3 MEDIUMs are advisory/observational and do NOT block handover; none is a truth defect. Every one
of the 92 re-authored strings is trace-grounded, every superlative rank-checks TRUE, the HUM-001
fat-suppression trap is fully avoided, and all duplicate-recipe families are ruled honestly as ties.

I do not fix or close. Proposing RETURNED with the MEDIUM notes routed below.

---

## Track V — Verification (all PASS)

| Gate | Result | Observed |
|---|---|---|
| Candidate hash == spec | PASS | 50f4be85… exact |
| Baseline blob == spec (2fbd70fd) | PASS | independent `git show` = 2fbd70fdc8368b… |
| Field isolation (only IL/rowVerdict) | PASS | 57/57; non-product top-level byte-identical; scores/grades/ranks/nutrition/_meta/d4 all unchanged |
| **rowVerdict key-set == baseline exactly** | PASS | base 35 == cand 35, **added 0 keys, removed 0 keys**; 22 products correctly lack the key |
| Re-authored surface | PASS | 57 IL + 35 RV = **92** strings (matches spec) |
| Overhaul actually happened | PASS | 0/57 insightLines identical to baseline |
| Grade distribution self-consistent | PASS | per-product B2/C42/D13 == _meta.grade_distribution |
| No BOM / clean UTF-8 | PASS | file starts without BOM |
| **HUM-001 fat trap** (no fat-gram claims) | PASS | `שומן` appears **0×** across all 92 strings; fat is suppressed (`nutrition_policy.suppressed=[fat,sat_fat]`, `fat_values_dropped:57`) yet raw fat values still sit in JSON — none is cited |
| HUM-002 (no sugar-gram claims) | PASS | sugar-with-number 0× |
| Protein leak (18.2g partial-parse #2) | PASS | 0 protein-gram claims; #2's 18.2g not cited |
| Em dash / en dash | PASS | 0 / 0 |
| Engine-mechanic vocab | PASS | 0 (חציון/חיסרון/פרמטר/תקרה/NOVA/cap/…) |
| Antithesis "X, not Y" (`ולא/אלא`) | PASS | 0 |
| R4 buy-verb (כדאי/שווה+לקנות/לבחור/לרכוש) | PASS | 0 |
| OFF references | PASS | 0 |
| IL openings unique (first 3 words) | PASS | 57/57 |
| RV openings unique | PASS | 35/35 |
| R3 5-gram census (no phrase >2×) | PASS | 0 phrases repeat >2× |
| Panel-number citations enumerated + justified | PASS | exactly 6, each a verified shelf extreme (see below) |
| Hebrew leakage gate (`hebrew_readability.is_clean`) | PASS* | 90/92 clean; the 2 flags are heuristic FALSE POSITIVES on "15.5" (a real tahini %, not a score) |

\* readability numeric flag is heuristic; only `is_clean`/structural leakage is a hard gate, and no
structural leakage exists. Both "15.5" hits (174551, 579319) are label-grounded tahini percentages.

### Panel-number census (6/6 exact, all extremes — none "stamped")
| id | field | claim | actual (trace) | role |
|---|---|---|---|---|
| 725404 | RV | 231 מ"ג | sodium 231.0 | shelf **min** sodium |
| 721533 | IL | 32 קלוריות | kcal 32.0 | shelf **min** kcal |
| 154265 | IL | 599 קלוריות | kcal 599.0 | shelf **max** kcal |
| 725510 | IL | 852 מ"ג | sodium 852.0 | 852-trio (real) |
| 725633 | IL | 852 מ"ג | sodium 852.0 | 852-trio, twin identity |
| 451969 | IL | 852 מ"ג | sodium 852.0 | 852-trio (own real value) |

The 852 is one shared value cited thrice; it does NOT read stamped — 725510/725633 are genuine full-panel
twins (identical kcal 94 / prot 1.6 / fat 6.2 / fiber 1.9 / sugar 6.0 / sod 852 / score 46.0 / grade D)
and the copy explicitly says so; 451969 is a pepper spread that independently carries 852 and does NOT
claim twinship. Each citation is the driver of that product's low rank.

---

## Rank tables (independently derived from the trace, all 57)

**Sodium (mg), ascending — lowest:** 725404 **231** · 858175 257 · 725381 328 · 725398 328 · 989096 334 · 467320 360 …
**Sodium, descending — highest:** 154265 **864** · 725510 852 · 725633 852 · 451969 852 · 666444 623 · 666307 480 · 520905 452 · 931330 398
**kcal, ascending — lowest:** 721533 **32** · 800642 74 · 563492 79 · 577572 79 · 725510 94 · 725633 94
**kcal, descending — highest:** 154265 **599** · 724786 332 · 564360 311 · 467153 296 · 373710 294 · 725367 288
**Protein (g), descending:** 666307 **18.2** (partial-parse, NOT cited) · 564360 11.0 · 373710 10.6 · 725404 10.1 · 579319/557478 8.6
**Tahini %, top:** 564360 **40%** · 373710 37% · 467320/780314 26% · 579319 20% · 968685 20%
**Score dist:** min 36.6 · max 70.6 · mean 53.0 · median 54.0 · **pstdev 6.11** · most-common 54.0 (×3) · B2/C42/D13
**Only adjacent gap > 3.0:** rank 2→3 (67.7→60.7, 7.0) — cross-type (lean-list hummus vs 623mg matbucha), mechanism stated in both verdicts.
**Rank-order sanity 3/3:** 231mg leader > 852 matbucha ✓ · clean #2 > canola-first צ'ומה ✓ · 257mg pepper > 852 pepper ✓. No inversions.

---

## Track C — Challenge (product-by-product, hotspots)

Every ORCHESTRATOR HOTSPOT was independently re-derived from the trace + ingredient list. All TRUE:

**(a) Leader 725404 (70.6/B):** "יד רחבה בטחינה ויד קמוצה במלח" — tahini 31% (INGR ✓), sodium 231 = category min ✓.
Helper claim "חומר משמר ושני מווסתי חומציות" == d4 exactly {E202 preservative; E500+E330 acidity regulators} ✓.

**(b) #2 666307 (67.7/B):** BOTH superlatives scoped to hummus-spread subgroup and TRUE within it —
sodium 480 = max of the 33 hummus_spreads ✓; helper count 1 = **unique** min of the subgroup ✓.
Subgroup = `_product_type==hummus_spread`, a defensible label-grounded partition. Partial-panel disclosure
present ("הפירוט שהגיע בסריקה חלקי"). protein 18.2g NOT cited ✓.

**(c) 852 trio:** each product's sodium == 852 verified; twins (725510/725633) share full panel + score
46.0/D — identity claim "עד הציון האחיד" TRUE ✓. "יותר מכפול מהמקובל במדף": shelf median/mode sodium = 395,
852/395 = 2.16 > 2× ✓.

**(d) Duplicate families — all honest:**
- 564360 "אלוף הטחינה 40%" first ingredient ✓; 373710 "על השם 40%, ברשימה 37%" — both numbers real (INGR "37%" + note "…40%") ✓.
- 467320 "26% טחינה… חמישייה הנדיבה" ✓ + twin 780314 (both 26%, both 54.0) "בשינוי אריזה" ✓.
- Quadruplet 174551/964564/987963/645935: all 61%+15.5%, sodium 393, kcal 186, scores 56.6–56.8 (spread 0.2) — framed "הבדל תזונתי… אינו קיים" ✓.
- אסלי 725565/725589 (full panel identical, 58.4) ✓; מסעדה 727667/576513 (identical, 57.0) ✓; גלילי 579319/557478 (57.7 vs 57.6, gap 0.1) "הפרש שאין לו משמעות" ✓; מטבוחה 931330/644112 (identical, 55.2) ✓.

**(e) Composition claims:** every % sampled (40/37/26/1.8/0.6/0.17/31/48/70/92/73/72/69/23/67) present in that
product's own ingredient list. 725640 "שמן סויה שלוש פעמים" = exactly 3 occurrences ✓. 154265 "הרכיב הראשון
שמן קנולה" first in INGR ✓ + "599 קלוריות הצפוף והמלוח ביותר" — 599 = kcal max AND 864 sodium = shelf max
(> the 852 trio), so **NO contradiction: צ'ומה genuinely IS saltiest** ✓. 724786 "היחיד במדף שמוותר על
חומר משמר" — verified sole preservative-free list across 57 ✓.

**(f) HUM-001 trap:** cleared — 0 fat-gram claims; no claim leans on 18.2g protein or corrupted fat.

**(g) Boundary rule ("סלט"):** all 5 uses are label/name references — 4 quoted ('סלט חומוס'/'סלט פלפלים'/
'סלט טחינה'/'סלט פלפלים חריף'), the 5th (725633 "התאומה של סלט מטבוחה פיקנטי") references its twin **by that
twin's exact product name** (725510.name == "סלט מטבוחה פיקנטי"). "סלט" is NEVER the author's own classifier;
prepared-vs-raw distinctions ride tahini/sodium/energy, never protein ✓.

**(h) R2 partial clause:** appears on exactly 666307 + 666444 = exactly the 2 `partial` products; none on any
verified product ✓. (Note: stale `_meta.confidence_distribution:{partial:57}` conflicts with per-product
55 verified / 2 partial — the per-product field is authoritative and untouched by this task; flagging for
awareness, not a copy defect.)

### Brand-adversarial claims (all bulletproof + proportionate)
צנובר 1.8% ("קישוט נעים… ההצדקה היא מה שהרשימה חוסכת") · זעתר 0.17% ("קורט שנועד בעיקר לשם") · 'אמיתית'
("מתארת נכון את הירקות" then pivots to additives) · 40%-vs-37% (dilution explained) · סמיר 48%-inside-'סלט חומוס'
("השם גדול מהתכולה"). Each names the label's promise, then grounds the gap in real composition. Staple-shelf
tone throughout: who-it-suits, no moralizing, ties ruled as ties.

---

## Findings by severity

### CRITICAL — none.
### HIGH — none.

### MEDIUM (advisory — do NOT block handover)
- **RT-M1 (observational, content/style):** 725633 uses the twin's product name "סלט מטבוחה פיקנטי" **unquoted**
  while the other 4 "סלט" references are quoted. Factually correct (it is a proper-noun reference, boundary
  rule intact) but stylistically inconsistent. Optional: quote it for consistency. Routes to: content-agent.
- **RT-M2 (data flag, not copy):** 154265 (צ'ומה) has `d4_additives: null` although its ingredient list
  contains additives (סודיום בנזואט preservative, מלח לימון acidity regulator). The COPY correctly avoids any
  additive-count claim here, so no consumer-facing defect — but the empty d4 is a latent data gap. Routes to:
  data-agent (parity with the cheese-lane "E2 02"/empty-d4 flag).
- **RT-M3 (stale meta, pre-existing, out of 2-field scope):** `_meta.confidence_distribution` says
  `{partial:57}` but per-product fields are 55 verified / 2 partial. Baseline-inherited, untouched by this
  task. Copy uses the correct per-product values. Routes to: data-agent / later meta-regen pass.

---

## Independence self-check
Read the artifact directly (all 92 strings), fetched baseline independently via `git show origin/master`,
re-derived every rank table and superlative from the trace (not the author's `h_*.py` scripts or report).
Would an outside reviewer agree? Yes — every claim maps to a verifiable trace field or ingredient-list token,
and Track V is green on real data (not on a wrong-but-consistent assumption): the one place the data itself
is questionable (suppressed/corrupted fat, empty d4 on צ'ומה, stale meta) the copy correctly does NOT lean on
it, which is exactly the HUM-001 discipline the spec demanded.

## Weakest 3 strings (Track-C, still acceptable)
1. 725633 IL — the unquoted "סלט מטבוחה פיקנטי" (RT-M1); reads fine but breaks the quoting convention.
2. 666444 IL — "כף המלח כאן מהכבדות במדף" leans on 623mg (rank 5/57); defensible ("מהכבדות" = among heaviest,
   top-5) but the softest superlative on the shelf.
3. 154265 IL — packs three findings (canola-first, 599 kcal, saltiest) into one line; all true but dense.

---

```json
{
  "task": "TASK-461 (Phase-2 #4 hummus)",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": "scratchpad/hummus_copy_overhaul.json", "action": "verified-not-modified",
     "sha256": "50f4be85e91848c3c3224e65842adf6068ecffc04e393541b8220194325a24b6"},
    {"path": "scratchpad/TASK-461_hummus_QA_report.md", "action": "created",
     "sha256": "SELF"}
  ],
  "counts": {
    "field_isolation_clean": "57/57 (products; only insightLine+rowVerdict differ vs origin/master blob 2fbd70fd)",
    "rowVerdict_keys_cand_vs_base": "35/35 (equal set, 0 added, 0 removed; 22/57 lack key as in baseline)",
    "reauthored_strings": "92/92 (57 IL + 35 RV)",
    "fat_gram_claims": "0/92 (HUM-001 trap avoided; 'שומן' census)",
    "sugar_number_claims": "0/92",
    "protein_gram_claims": "0/92",
    "em_dash": "0/92", "en_dash": "0/92",
    "engine_vocab_hits": "0/92", "antithesis_hits": "0/92", "buy_verb_hits": "0/92", "off_refs": "0/92",
    "il_openings_unique": "57/57", "rv_openings_unique": "35/35",
    "five_gram_over_2x": "0 (R3)",
    "leakage_gate_is_clean": "90/92 (2 heuristic false-positives on real tahini % '15.5'; 0 structural leakage)",
    "panel_number_citations": "6/6 exact-match extremes (min sodium, min/max kcal, 852-trio)",
    "852_trio_sodium_verified": "3/3 == 852; twins full-panel+score identical (46.0/D)",
    "852_over_2x_typical": "true (852/median 395 = 2.16)",
    "subgroup_superlatives_666307": "2/2 true (sodium 480 = hummus_spread max; helper count 1 = unique subgroup min)",
    "R2_partial_clause_placement": "2/2 on partial products (666307,666444); 0 on verified",
    "boundary_salt_word": "5/5 label-or-name references, 0 author-classifier uses",
    "composition_pct_grounded": "all sampled % present in own ingredient list",
    "duplicate_families_honest": "quadruplet + 4 twin-pairs verified, all ties framed as ties",
    "adjacent_gaps_over_3pt": "1/56 (rank2->3, 7.0, cross-type, explained)",
    "rank_order_inversions": "0/3 known-better pairs",
    "score_distribution": "min 36.6 / max 70.6 / mean 53.0 / median 54.0 / pstdev 6.11 / mode 54.0(x3) / B2 C42 D13 (== baseline, unchanged)"
  },
  "commands_run": [
    {"cmd": "git rev-parse origin/master:bari-web/src/data/comparisons/hummus_frontend_v5.json", "exit_code": 0},
    {"cmd": "git show origin/master:.../hummus_frontend_v5.json > BASELINE_hummus_RAW.json", "exit_code": 0},
    {"cmd": "python -X utf8 qh_isolation.py", "exit_code": 0},
    {"cmd": "python -X utf8 qh_facts.py", "exit_code": 0},
    {"cmd": "python -X utf8 qh_hygiene.py", "exit_code": 0},
    {"cmd": "python -X utf8 qh_claims.py", "exit_code": 0},
    {"cmd": "python -X utf8 qh_panelcensus.py", "exit_code": 0},
    {"cmd": "python -X utf8 qh_final.py", "exit_code": 0},
    {"cmd": "python -X utf8 qh_run/qh_readability.py (clean dir, avoids inspect.py shadow)", "exit_code": 0}
  ],
  "not_done": [
    "run_gates.py G1-G8 not run (out of this lane's 2-field copy scope; the git-owning sibling lane runs G1-G8 with --baseline origin/master at handover per the pilot protocol)",
    "rendered-page DOM/mobile-geometry check not run (copy-only task; no TS/route/component change; page structure byte-identical)"
  ],
  "self_check": "Structural fact (rowVerdict key-set cand==base exactly, 0 keys added; 92-string surface) CONFIRMED; all 92 strings trace-grounded with 0 CRITICAL/0 HIGH -> VERDICT GO_WITH_FIXES (3 MEDIUM advisory, routed, non-blocking)."
}
```
