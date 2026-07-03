# Adversarial QA Report — TASK-461 Phase-2 #5: SNACKS copy overhaul (21 products)

Date: 2026-07-02  ·  Scope: 21 products, snacks_frontend_v5.json (insightLine + rowVerdict only)
Challenger: adversarial-qa-agent (Opus, independent lane)  ·  Route: /hashvaot/snacks

## VERDICT: GO_WITH_FIXES
0 CRITICAL · 0 HIGH · 3 MEDIUM (advisory)

All 21 products' claims are trace-grounded and bulletproof. Field isolation is clean, all
hygiene gates pass, and the hebrew_readability gate is clean on all 42 strings. The 3 MEDIUMs
are advisory (one is a pre-existing baseline schema debt outside this task's scope; two are
soft editorial-superlative flags that are defensible as written). No blocker to handover.

Independence note: I fetched origin/master `snacks_frontend_v5.json` myself (sha256
afd691b4fe011cedc03448d9136d0b2f3c52f9618247504f485ee79ff45067dd), built my own rank tables
over all 21 products across 9 fields, and re-derived every hotspot claim. I did not rely on the
author's report or scripts.

---

## TRACK V — VERIFICATION

### V.1 Field isolation (21/21) — PASS
- `_meta` byte-identical to baseline. Product id set identical (21 = 21).
- For every product, ONLY `insightLine` and `rowVerdict` changed. All of score/grade/rank/
  categoryTotal/nutrition_per_100g/confidence/d4_additives/expansion(comparisonContext,
  positiveSignals, limitingFactors)/_hash_no_rank are byte-identical (JSON-canonical compare).
- Both fields changed in all 21 (insightLine 21/21, rowVerdict 21/21). No illegal field touched.
- Candidate sha256 confirmed = 406d8363…5e968a8 (matches spec).

### V.2 Claim-by-claim truth audit (ALL 21) — PASS
Every orchestrator hotspot verified TRUE against my independent rank tables + parsed ingredient
strings:

| Hotspot | Claim | Verified |
|---|---|---|
| snk-001 | fiber-max 23g (22.9 rounds), sugar-min (9.9), "מוביל את המדף" (rank 1) | TRUE — fiber #1/21, sugar #1-lowest, rank 1 |
| snk-001 | no stale 70/B ceiling echo (current top 66.9) | TRUE — no "70"/"תקרה" token present |
| snk-002 | dates 76% ≈ "שלושה רבעים", "אין שום ממתיק מוסף" | TRUE — 76% in list; list = dates/PB/peanuts/salt only, "ללא תוספת סוכר" |
| snk-004 | shortest list (2 ings: 84%+16%), sweetest (sugar-max 50.5), coating "אין בו גרם ממתיק" | TRUE — 2 ings (unique-min); sugar #1/21; coating = 100% מוצקי קקאו |
| snk-004 | sugar "כמחצית ממשקל" | TRUE — 50.5g/100g ≈ half |
| snk-010/008/009 | shared formula 65/19/16; satFat almond<cashew≪coconut; coconut "פי שניים ויותר" | TRUE — 6.1<7.1<16.2; 16.2 ≥ 2× (2.28× cashew, 2.66× almond) |
| snk-010 | "מדורגת ראשונה מבין השלוש" (best of trio), satFat lowest in family | TRUE — rank 5<7<10; satFat 6.1 = min of 3 |
| snk-012 | dual record: protein-max 14g + kcal-max 540; "קרוב לארבעים אחוז בוטנים" | TRUE — protein #1/21 (14.0), kcal #1/21 (540), peanuts 39% |
| snk-017 | "שיא המלח של המדף כולו: 416 מ\"ג", "קרוב לשליש בוטנים" (29.3%) | TRUE — sodium #1/21 (416); peanuts 29.3% |
| snk-015 | "המלח מטפס כמעט לשיא" | TRUE — sodium #2/21 (372 = 89% of max), cross-consistent with snk-017 claim |
| snk-021 | "שיא השומן הרווי: 18 גרם" (18.1), last place, "כשמינית דגן מלא" (13%) | TRUE — satFat #1/21; rank 21; whole grain 13% ≈ 1/8 |
| snk-006 | honey 3%, oats "שישים אחוז" (60%) | TRUE — "דבש (3%)", oats "(60%)" |
| snk-007 | maple 2%, oats 60%, twin Δ0.1 | TRUE — "סירופ מייפל (2%)", 60%, score 36.2 vs 36.1 = 0.1 |
| snk-013 | honey 1% + maple 1% | TRUE — "דבש (1%)" + "סירופ מייפל (1%)" |
| snk-018 | dried fruit "אחוז אחד כל אחד" (raisin 1% + prune 1%) | TRUE — "צימוקים 1%", "שזיפים 1%" |
| snk-014 | chocolate "שלושה רבעים" (74%), grain "בקושי לחמישית" (19%) | TRUE — "(74%)", "(19%)"; claims sit on intact list head (pre-"????" tail) |
| snk-016 | same 74% choc + <1/5 grain (19%), kids-marketed | TRUE — "(74%)", "(19%)"; kids label real |
| snk-019 | chocolate FIRST ingredient | TRUE — list starts "שוקולד מריר מעולה (24%)" ahead of grain |
| snk-020 | milk-choc FIRST, fiber-min "הדלים ביותר", grain "עשירית" (10%) | TRUE — starts "שוקולד חלב"; fiber 3.1 = lowest non-null; whole grain 10% |
| snk-005 | "מובילי החלבון של משפחת חטיפי התמרים" (scoped to date family) | TRUE — 9.6g = highest of 8 date bars (shelf-max is snk-012 14g; copy correctly scopes) |
| snk-003 | "חמישה מזונות שלמים" | TRUE — dates/raisins/cashew/sunflower/sesame = 5 |

Name-vs-content exposures (brand-adversarial): all bulletproof and proportionate — factual
share exposure, no mockery. Kids-product (snk-016) framing is factual/structural, not alarmist.

### V.2.k Partial-panel / data-flag discipline — PASS
- snk-018: sodium 0.2mg (suspect) and dietary_fiber_g = NULL. Copy cites NEITHER sodium nor a
  fiber number — leans only on ingredient-order + dried-fruit 1%/1% shares (all intact/reliable).
  Correct: no claim rides the suspect/missing field.
- snk-014 / snk-016: corrupted "????" ingredient tails. Both copies' claims (74% choc / 19%
  grain) sit on the list HEAD, before the corruption. No claim depends on the garbled segment.
- snk-010/013: stray "n" parse artifacts in ingredient string. No copy claim references them.
- All 21 are confidence="verified"; disclosure is consistent (R2): copy narrates data-vs-name
  gaps only where material (018/013/006/007), never over-narrating a clean panel.

### V.3 Hygiene census — PASS
| Check | Result |
|---|---|
| Em dash (—) | 0 |
| En dash / spaced hyphen | 0 |
| Engine vocab (חציון/חיסרון/פרמטר/מדד עיבוד/NOVA/cap/floor…) | 0 |
| Antithesis "X, not Y" (ולא/אלא define-by-negation) | 0 |
| R4 buy-verb (כדאי/שווה + לקנות/לבחור; imperative קנו/קחו) | 0 |
| Opening uniqueness (first-3-words, 42 strings) | 42/42 unique |
| OFF references | 0 |
| 5-gram census (R3, editorial phrase >2×) | 0 over 2× (max repeat = 1) |
| Panel numbers in copy | 4 products, all shelf extremes (snk-001 fiber 23; snk-012 protein 14 + kcal 540; snk-017 sodium 416; snk-021 satFat 18) — each IS the fired driver |

### V.4 hebrew_readability gate — PASS
42/42 strings `is_clean=True`. 0 blocking leaks (framework/score_mechanic/recommendation).
0 English leaks (no brand-mask false positives — "FREE" brand appears only in names, not copy).

### V.5 run_gates.py (G1–G8, primary instrument) — advisory
Ran with `--baseline` = origin/master snacks_v5. Exit 1, driven SOLELY by **G1 SCHEMA**, which
fails **byte-identically on both candidate and baseline** (`diff` = empty) — pre-existing schema
debt (schema rejects name_he/image_url/nutrition_per_100g/_scoring_trace and expects
limitingFactors as strings). This overhaul introduces nothing new. Same pattern the pilot
handover documented.
- G4 OFF: PASS · G6 COPY-SAFETY: PASS · G7 PARITY: PASS (21=21, 0 grade changes, image 100%=100%,
  avg chars/product 598 vs 587 = +11) · G8 DATA-SANITY: PASS.
- G2/G3/G5 = WARN only because no --run/--corpus dir supplied (copy-only task); not failures.

---

## TRACK C — ADVERSARIAL CHALLENGE

Every line delivers the engine's opinion with a stance + a real driver. Brand-adversarial
name-vs-content lines are evidence-bulletproof AND proportionate (factual exposure of the
label gap, never mockery). No health-halo on the date/nut products — each pairs the honest
positive ("מזון שלם", "חלבון וסיבים של ממש") with the density caveat ("דחוס", "מנות קטנות",
"פינוק"). Ties are handled as ties (snk-006/007 explicitly). Kids-product (snk-016) is factual,
not alarmist. Hebrew reads natural throughout.

### Product-by-product Track-C stance summary
- Top (snk-001..004): opinion-first, honest superlatives, correctly scoped. Justified.
- Date family (003/005/008/009/010): "dense-but-honest" whole-food framing; twin/trio families
  ruled once, differentiated by the real satFat/fat mechanism. Justified.
- Nature Valley oat bars (006/007/011/015/017): consistent "good grain wrapped in candy /
  surprising salt" thesis, each grounded in ingredient order + sodium rank. Justified.
- Chocolate-dominant bottom (014/016/019/020/021): "candy in a grain-bar format" thesis,
  grounded in chocolate-first ordering + share %. Justified.
- Marketing-gap bars (013/018): name-vs-list exposure, shares verified. Justified.

### Weakest 3 lines (flagged per spec — all still defensible, none block)
1. **snk-002 rowVerdict** "…מהכנים שיש במדף הזה" (among the most honest on this shelf). A
   subjective editorial superlative, not a measurable rank. Grounded (3 whole-food ingredients,
   no added sweetener) so defensible, but it is the softest claim in the set — an "honesty"
   ranking is inherently interpretive. MEDIUM-M2.
2. **snk-015 insightLine** "אחת הרשימות הארוכות במדף" (one of the longest lists). True as
   written (snk-015 is #5/21 by list-complexity; the Korni bars 019/020/021 and snk-017 are
   longer). The hedge "אחת ה…" is correct — it does NOT claim "the longest," so it holds; flagged
   only because a hasty reader could hear "longest." MEDIUM-M3.
3. **snk-006 rowVerdict** "יותר דגן אמיתי מכמעט כל מתחרה כאן" (more real grain than almost any
   competitor). 60% oats is top-2 whole-grain share (tied with snk-007). "כמעט כל" is the right
   hedge. Defensible; softest of the grain-share claims. (Rolled into M-set, no separate ID.)

### Proportionality (Hard Rule 11) — PASS
Scores are frozen and out of scope. Several adjacent near-ties exist (Δ0.1 006/007, Δ0.2 011/013,
Δ0.2 017/015, Δ0.4 020/019). The authored copy does NOT manufacture differentiation across any
near-tie; snk-006/007 are explicitly framed as a tie ("הפער… קטן מכדי להכריע"). The two large
gaps (Δ8.0 at snk-003, Δ7.7 at snk-014) are grade-cluster transitions the copy grounds in the
satFat/chocolate-share mechanism. No unexplained gap.

---

## FINDINGS BY SEVERITY

### CRITICAL — none
### HIGH — none
### MEDIUM (advisory — none block handover)
- **M1 (Track V, routes to: none / informational):** G1 SCHEMA gate fails on the candidate, but
  byte-identically to origin/master baseline (pre-existing debt: name_he/image_url/
  nutrition_per_100g/_scoring_trace not in schema; limitingFactors typed as string not dict).
  Nothing introduced by this task. Document at handover (same as pilot); does not gate copy.
  Broader schema fix is a separate concern (owner: frontend/data schema owner), not this lane.
- **M2 (Track C, routes to: content-agent — monitor):** snk-002 "מהכנים שיש במדף" is a
  subjective honesty-superlative. Defensible (grounded), but the softest claim; note for
  consistency if the phrase recurs across categories.
- **M3 (Track C, routes to: content-agent — monitor):** snk-015 "אחת הרשימות הארוכות" — true and
  correctly hedged; flagged only as the second-softest superlative. No change required.

---

## Machine-readable verdict
```json
{
  "task": "TASK-461-phase2-snacks",
  "verdict": "GO_WITH_FIXES",
  "critical": 0, "high": 0, "medium": 3,
  "track_v": {
    "field_isolation": "PASS (21/21, only insightLine+rowVerdict)",
    "truth_audit": "PASS (21/21 products, all hotspots TRUE)",
    "hygiene": "PASS (em0, vocab0, antithesis0, buyverb0, openings42/42, OFF0, 5gram<=1x, panelnums=4 extremes)",
    "readability_gate": "PASS (42/42 is_clean)",
    "run_gates": "G1 pre-existing (byte-identical to baseline), G4/G6/G7/G8 PASS, G2/G3/G5 WARN(no run dir)"
  },
  "track_c": "all 21 justified; 0 health-halo; ties-as-ties; kids factual; weakest3=snk-002,snk-015,snk-006",
  "blocks_handover": false
}
```

Recommendation: TASK-461 Phase-2 #5 (snacks) is TWO-GATE-eligible on the Adversarial QA side.
Propose RETURNED to orchestrator (this agent does not close). No fix required to ship; M1 is a
handover note, M2/M3 are monitor-only.
