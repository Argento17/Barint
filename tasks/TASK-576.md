---
id: TASK-576
title: PROGRAM: site-wide copy sweep + Content Agent training (judge-calibrated triage across all shelves)
owner: content-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-07-10
depends_on: []
blocks: []
category_id: null
summary: >
  Owner-initiated program (tripwire #3). Sweep consumer copy across all live shelves: KEEP / TOUCH (1-3 word fix) / REWRITE triage, not a blanket rewrite. Prerequisites BEFORE any sweep: (1) provenance census — classify every row as owner-written vs baseline_placeholder template vs content_agent_v1, so the active product-descriptions freeze is never violated; (2) owner finishes reading cereals (17 of 20 rows unread) to establish the real defect rate; (3) build an LLM judge calibrated against owner verdicts on real rows — it is not trusted until it reproduces owner rulings on held-out rows. Training runs two channels: mechanical (every owner ruling that can be a deterministic check becomes one, with selftest fixtures) and editorial (owner corrections become before/after few-shot pairs in the voice brief). Rationale: owner read 3 rows and found 3 defects that ALL existing gates passed. Sequence: cereals (done) -> yogurt (67 products, hardest) -> fan out. Cost: ~400 products, ~8min/product, 4x parallel = ~13h machine time per pass; engine reliability (9-attempt Vitabix failure) must be fixed first.
---

# TASK-576 — PROGRAM: site-wide copy sweep + Content Agent training

## CENSUS RESULTS (orchestrator, 2026-07-10) — read-only, nothing written

**Scale: 19 live shelves, 710 products** (the prior ~400 estimate was low by ~75%).

**Live violations of standing owner rules:**
- **1,801 em-dashes** across 710 products (~2.5/product). Owner rule: minimize.
- **140/710 rows (20%)** violate the project's own `copy_rules.ANTITHESIS_RE` — the
  "X, לא Y" define-by-negation ban. Measured with the real project regex, not a
  hand-rolled one.
- 0/710 rows carry `author_copy.py` baseline-template fingerprints, so live copy is NOT
  current-template output. This does NOT establish owner authorship — see the blocker.

**Worst shelves by antithesis density:** chocolate_tablets 24/35 (69%), protein_combined
22/32 (69%), cakes_hard_cookies 14/62, hummus 11/57, milk 10/18.
**Already clean:** yogurt_spoonable 0/50, yogurt_drinkable 0/17, crackers 0/53 (0 em-dashes too).

**BLOCKER — provenance metadata is effectively absent.** Only 4/19 shelves carry any
`copy_status`; only 1 (`hummus_v5`) carries `content_source`. 15/19 shelves have NO
authorship metadata at all. **The files cannot tell us which rows the owner wrote.** With
the product-descriptions freeze active, a blind sweep risks clobbering the owner's own
rewrites. Must be resolved before any write. Open question for the owner: are his rewritten
descriptions in these JSONs at all, or held elsewhere?

## Plan shape (data-driven)
The defect classes split cleanly, which makes the sweep affordable:
- **TOUCH-class** (deterministic, 1–3 word fixes): em-dash budget, antithesis constructions.
  Machine-detectable, machine-fixable, human-spot-checked. This is the bulk of the volume.
- **REWRITE-class** (structural / voice: flow, rank contradiction, over-praise): needs the
  calibrated judge — no gate detects these. Proven: the owner read 3 cereals rows and found
  3 defects that every existing gate had passed.

## Prerequisites before any write
1. Resolve provenance (owner question + git-history reconstruction where possible).
2. Owner finishes reading cereals (17/20 rows unread) → establishes the real defect rate,
   which sizes the whole program.
3. Build the LLM judge; it is NOT trusted until it reproduces owner verdicts on held-out rows.
4. Fix engine reliability (Vitabix needed 9 attempts, ended hand-written) before any mass run.

## Training — two channels
- **Mechanical:** every owner ruling that can become a deterministic check does, with selftest
  fixtures (done: banned phrase, rank contradiction, ingredient-opener; next: em-dash budget).
- **Editorial:** owner corrections become before/after few-shot pairs in the voice brief.
  Highest-value asset in the program — the owner IS the voice; the daily scan only learns
  register from strangers. See `content_voice/tom_bari_voice/8_edit_feedback_log.md` §H3.

## Sequence
cereals (pilot, done) → yogurt (67 products, where the worst failures on record happened;
if it survives yogurt it survives anything) → fan out by defect density.

## Notes
- Related: TASK-550 (the engine), TASK-553 (margin gate + S_VERBATIM cleanup),
  TASK-374 (Project Tom's Voice), [[owner_product_descriptions_freeze]],
  [[gates_designed_not_enforced]], [[baseline_copy_shipped_trap]].

---

## H4 PATTERN SET + DETECTORS BUILT (orchestrator, 2026-07-10)

Owner read 21 of 30 sampled live rows and gave verbatim Hebrew verdicts. Patterns
extracted to `content_voice/tom_bari_voice/8_edit_feedback_log.md` §H4 (H4-P1..P7).

**Detectors built and TESTED** (`03_operations/evals/copy_evals/copy_rules.py`):
`rule_grade_in_prose` (+ vitamin-letter guard), `rule_ingredient_count`,
`rule_stock_phrase`, `find_cross_field_value_repetition`.
Proof: `test_copy_rules_h4.py` — 27 cases, 27 pass.

**Measured across all 710 live rows** (prose fields only: insightLine, rowVerdict,
consumerTakeaway, ce.whyRated, ce.takeaway, ce.context):

| pattern | rows | occurrences |
|---|---|---|
| em_dash (H4-P4) | 558/710 (78.6%) | 1131 |
| grade_in_prose (H4-P7) | 237/710 (33.4%) | 270 |
| cross_field_value_repeat (H4-P3) | 122/710 (17.2%) | 164 |
| antithesis (owner ban) | 95/710 (13.4%) | 104 |
| ingredient_count (H4-P2) | 59/710 (8.3%) | 85 |
| stock_phrase (H4-P6) | 4/710 (0.6%) | 4 |

Wide scope (incl. good[]/watchOut[] bullets): em_dash 584 rows, value_repeat 222 rows.

**Correction to the orchestrator's first reading**: an earlier scratchpad measurement
reported grade_in_prose at 20% and value_repeat at 34%. Both were wrong. `\b` does not
form a word boundary against Hebrew letters, so `ל-D` / `בין C ל-E` never matched
(undercount ~3x); and `%` was being counted as a nutrition unit (overcount ~2x). The
table above is from the tested rules. This is the second time an untested regex produced
a confidently wrong number in this program.

## CRITICAL — live violation of the highest-priority owner ruling

`hard_cheeses_frontend_v4` shipped, and the gate passed it with `banned=0`:
- "רשימת הרכיבים לא הגיעה מהסריקה, כך שהציון מבוסס על הנתונים התזונתיים בלבד."
- "אי-אפשר לאמת את פרופיל התוספים."
- "השומן הגבוה (32%) ועדר נתוני רכיבים שמגביל את האמינות."  ← "עדר" (herd) typo for "היעדר"

This is `consumer_copy_never_narrates_datastate` — the owner's worst-blowup ruling.
Scope: 19 fields, 2 shelves (hard_cheeses_v4 = 12, cookies_coffee_v2 = 7).

**Root cause (the failure class, not the instance):** `BANNED_CONSUMER_PHRASES` is a list
of LITERAL strings. It bans "לא מאומת"; the copy wrote "לא אומת". It bans "מגביל את הציון";
the copy wrote "מגביל את האמינות". A literal list only ever bans phrasings the engine has
already emitted; the next paraphrase walks through.

**Fix shipped:** `copy_constants.BANNED_CONSUMER_PATTERNS` — 5 regex FAMILIES banning the
ACT (narrating provenance / verification / confidence / data-absence), wired as CHECK 6
(hard, affects exit code) in `validate_copy_authored.py`.
Proof: `test_banned_patterns.py` — 10 live violations fire, 8 legitimate strings stay
silent (incl. the "בהיעדר סוכר מוסף" trap). 18/18 pass.

## Two further gate blindnesses found (dispatched, not yet fixed)

1. **CRASH**: `iter_consumer_copy_fields()` assumes `expansion.consumerExplanation` is a
   dict. In `granola_frontend_v2.json` it is `str` (7 products) / `None` (15). The gate
   has never run on granola — it aborts with AttributeError.
2. **FIELD COVERAGE**: `CONSUMER_PROSE_FIELDS` omits `expansion.limitingFactors[]`, which
   is rendered and which ships "הציון מבוסס על" live in `juices_frontend_v3`.
   (`confidence_tooltip_he` also matches, but that is the SANCTIONED place for data-state.)

## Dispatched 2026-07-10 (parallel)
- `gate-coverage` (Adversarial QA) — fix the crash + field coverage, with regression tests.
- `gate-census` (Adversarial QA) — read-only audit: for every written copy rule, what
  actually enforces it on the live line? Output: scratchpad/gate_enforcement_audit.md
- `datastate-rewrite` (Content Agent) — DRAFTS ONLY for the 19 offending fields, into
  scratchpad/datastate_rewrite_drafts.json. Freeze respected: zero edits under bari-web/.

## Tier split for the sweep
- **TOUCH (deterministic, detector exists):** em_dash, grade_in_prose, ingredient_count,
  stock_phrase, antithesis. NOTE: grade_in_prose is NOT a pure deletion — live copy embeds
  it structurally ("היא נוחתת ב-B מוצק", "ממקמים אותה ב-C"). Removing the letter leaves
  broken Hebrew. It is a REWRITE in a TOUCH costume, and must route through Content.
- **REWRITE (no detector possible):** H4-P1, the copy scores instead of describes.
  `cookies_coffee_v2` is not scattered damage: 126 grade hits / 117 rows, nearly all the
  template "...מגיעות ל-D". One shelf = 47% of the site's worst pattern. Fix the generator.
- **Clean is reachable:** yogurt_drinkable, yogurt_spoonable and crackers score ZERO on
  em_dash, antithesis, grade_in_prose and stock_phrase.

## Still open
- Owner has not issued a WRITTEN lift of the PRODUCT DESCRIPTIONS FREEZE. No live copy edited.
- The H4-P1 judge is unbuilt. No regex will ever catch "doesn't describe the product".

---

## THREE LANES RETURNED + ORCHESTRATOR-VERIFIED (2026-07-10)

### gate-coverage (Adversarial QA) — RETURNED, verified
Fixed 2 gate blindnesses in `validate_copy_authored.py` + `copy_constants.py`:
- CRASH: `iter_consumer_copy_fields` now returns `(fields, malformed)`, tolerates
  str/None/dict at every level; a wrong shape emits a `malformed_shape` FINDING (FAIL),
  never a crash. Granola now runs.
- COVERAGE: added the 3 rendered-but-unwatched authored fields — `comparisonContext`,
  `positiveSignals[]`, `limitingFactors[]` — each cited to a component file:line. Excluded
  block (confidenceLabel/servingNote/sourceLine/ingredients/unknowns[]/caveats[]) documents
  why UI-state fields stay out.
- Test: `test_field_coverage_and_shape.py` — fails pre-fix (incl. the AttributeError),
  passes post-fix.
- ORCHESTRATOR RE-RAN all 19 shelves: 8 PASS / 11 FAIL / 0 CRASH. Matches its table exactly.
- NEW exposed: 28 copy violations on the 3 added fields across 8 shelves (limitingFactors 19,
  comparisonContext 9) + 7 malformed granola records. Status flips: juices PASS→FAIL,
  snacks PASS→FAIL, granola CRASH→FAIL.
- The granola crash was HIDING a real banned phrase ("מוריד את הציון") inside the string-typed
  consumerExplanation the gate aborted on.
- **cereals_v2 (the content_agent_v1 pilot) went 3→9 violations** — score-mechanism narration
  ("הגורם המגביל", "מגביל את הציון") in limitingFactors/comparisonContext, fields the gate
  wasn't reading when the pilot was reported "4 gates green." Already-banned phrases, unseen.
- Corrected an error in the orchestrator's dispatch brief: conformance_scan / hebrew_readability
  import copy_rules, NOT these modules. Verified both unaffected anyway.
- ROUTING: 7 granola shape defects → Data Agent (str where dict).

### gate-census (Adversarial QA) — RETURNED, read-only audit
`scratchpad/gate_enforcement_audit.md`. Verdict: detectors exist, almost nothing is wired to
the live line.
- ZERO CI workflows import any copy detector. Only enforcement points: generation (only on
  rebuild) and the commit hook (staged files only, fails OPEN on infra error). The 710-row
  corpus sits behind no gate; a rule added after sign-off is never applied retroactively.
- 3 HARD owner bans have NO gate anywhere (not gen, not validate, not run_gates, not CI):
  grade_in_prose (256 live rows), cross_field_value_repetition (256), ingredient_count (63).
  antithesis is gated at generation only.
- 9/19 live shelves fail-or-crash the sole commit-path copy gate, yet are live.
- H4-P1 ("scores instead of describes") has NO possible mechanical detector — judge or owner only.

### datastate-rewrite (Content Agent) — RETURNED, DRAFTS ONLY, verified
`scratchpad/datastate_rewrite_drafts.json` — 19 replacement fields (hard_cheeses 12,
cookies_coffee 7). Zero edits under bari-web/. Freeze respected.
- ORCHESTRATOR VERIFIED independently: 0/19 hit any rule (grade/em-dash/antithesis/ingcount/
  stock/all 5 banned-patterns/all banned-phrases); 0 cross-field repeats.
- Fact-check vs source nutrition: 31 exact, 9 honest roundings (27.3→27, 19.9→~20), 5 numbers
  that are cross-product/category REFERENCES — all 5 verified TRUE against the corpus
  (grana wedge = 29g fat real; 32g protein = #3/31; 396 kcal = #3; 490 sodium low vs 28% set).
- Content DISCLOSED: all 19 hand-authored (not rule-generated); it ROUNDED 6 decimals to pass
  a readability heuristic (disclosed, not hidden); DictaBERT grammar gate could not run
  (pre-existing venv breakage: ModuleNotFoundError http.client); Nakdan blocked (no network).
- NOT signed off: drafts await owner + Adversarial QA review under the freeze. No live edit.

## THE DECISION THIS FORCES
Fixing these 28 by hand fixes nothing structural — the next paraphrase ships next week,
exactly as these did. The real fix is a corpus-wide CI gate that runs every copy detector
against all 710 rows on every push. Proposed, owner-gated (it will block merges).

## OPEN / BLOCKED ON OWNER
- No WRITTEN lift of the PRODUCT DESCRIPTIONS FREEZE. 19 drafts + 28 findings are all scratch.
- DictaBERT grammar gate is DOWN (venv). Any grammar claim on drafts is currently unverifiable.
- H4-P1 judge unbuilt.

---

## CORPUS-WIDE CI GATE BUILT (orchestrator, 2026-07-10) — the missing enforcement line

`03_operations/spine/corpus_copy_gate.py` — runs every HARD copy detector across
ALL 19 live shelves. It is a RATCHET against `copy_violation_baseline.json`:
- --check FAILS only when a (shelf, rule) count EXCEEDS baseline, or a new
  (shelf, rule) appears. At/below baseline PASSES. So the dirty corpus does not
  block every PR, but no new violation can land, and every fix lowers the baseline.
- Gated (hard): banned_phrase, banned_pattern, malformed_shape, grade_in_prose,
  ingredient_count, stock_phrase, antithesis, cross_field_value_repetition, sodium_term.
- Advisory (reported, NEVER gated, per owner minimize-not-ban): em_dash, number_density.

**Baseline census (current live state, 19 shelves):**
- 1,002 gated violations. 1,954 advisory em-dashes.
- Worst gated: grade_in_prose 310, cross_field_value_repetition 292, antithesis 186,
  ingredient_count 106, banned_pattern 38, sodium_term 34 (all cheese_v4), banned_phrase 23,
  malformed_shape 7 (granola), stock_phrase 6.
- Clean shelves: yogurt_drinkable, yogurt_spoonable (0 gated). crackers = 0 em-dash.

CI: `.github/workflows/copy_corpus_gate.yml` — runs the 4 detector test suites, then
--check, on every PR touching comparison data or copy tooling, and on push to master.

Tests: `test_corpus_gate_ratchet.py` — 12 cases, proves a new violation FAILS and an
em-dash spike does NOT. All 4 copy test suites green. Scan verified deterministic
(identical across runs) so the baseline is stable.

**This does not fix a single row of copy.** It stops the corpus getting worse while the
sweep makes it better. Landing it is owner-gated because --check will block merges.
