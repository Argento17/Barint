---
id: TASK-550
title: Build content_agent_v1 — the real LLM authoring seam (retire baseline placeholder)
owner: content-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-07-09
depends_on: []
blocks: []
category_id: null
summary: >
  Implement content_agent_v1: a real Content-Agent LLM pass that satisfies authoring_contract.json (author(facts)->dict), wires the tom_bari_voice files incl. file 9 register keepers, produces milk-quality Hebrew, passes all copy gates + naturalness gate. Connects the Hebrew Health Scan feed to an actual reader for the first time. Engine build only — no live-page regeneration (product-descriptions freeze respected).
---

# TASK-550 — Build content_agent_v1 — the real LLM authoring seam

## Why (the finding)
The consumer copy that ships (insightLine / rowVerdict / expansion / bariInterpretation)
is produced by `03_operations/page_generator/copy/author_copy.py` — a **deterministic
template** (`author_engine: "baseline_placeholder"`), a fixed Hebrew phrase-bank keyed by
the driver "story" tag. It has no reader: it cannot use the voice files, cannot use the
Hebrew Health Scan register keepers (file 9 §6), cannot be improved by reading. The daily
scan has therefore been feeding a reader that does not exist in the shipping pipeline. The
capability to write excellent native Hebrew is proven (recent blog posts, owner-accepted
with zero comments); it is simply not wired into the product-page authoring seam.

## Scope — build the missing implementation only
The interface already exists and is a documented drop-in swap:
`03_operations/page_generator/copy/authoring_contract.json` v2 declares
`content_agent_v1` and states "plugs into the same seam with no code change." Build that
one implementation.

## Definition of Done
1. A real LLM authoring engine implementing `author(facts: dict) -> dict` exactly per
   `authoring_contract.json` v2 (same input `fact_sheets.json`, same output `authored.json`
   schema, every barcode covered, S-verbatim honored, `null` stays `null`).
2. Its prompt WIRES the voice system as context: `2_voice_fingerprint.md`,
   `3_before_after_pairs.md`, `4_approved_phrases.md`, `5_banned_phrases_and_claims.md`,
   and a distilled register-move catalog from **`9_israeli_food_blog_research.md` §6**
   (the scan feed) — so a scan lesson can actually shape the copy. This is the link that
   closes the loop.
3. Output tagged `author_engine: "content_agent_v1"`.
4. Output passes, on a test category, every existing gate with zero regressions:
   `validate_copy_authored.py`, `hebrew_readability.is_clean`, `hebrew_grammar_gate`,
   run_gates BANNED_PHRASES, and the CHECK-5 recite scan clean. Plus the naturalness gate
   (`integrations/clients/naturalness_gate.py`, F1+F2) at or above the Project Tom's Voice
   (TASK-374) threshold.
5. Proven on **one** pilot category to SCRATCH output only (e.g. a `*_content_agent_v1.json`
   under a scratch/reports path). **No live comparison JSON is regenerated or overwritten**
   — the product-descriptions freeze (owner) stays intact; live rollout is a separate,
   owner-gated step after this engine is accepted.
6. Returned through the two-gate content sign-off (Content Agent authored + Adversarial QA)
   with the machine-readable Return Contract JSON.

## Hard constraints
- Respect the PRODUCT DESCRIPTIONS FREEZE: engine + scratch proof only; do NOT touch live
  rowVerdict/insightLine/expansion on shipped pages.
- All standing copy law applies (no data-state narration, no recite, no framework leakage,
  sodium/fat never causal, no recommendation language, grade=badge only).
- Fact firewall: author asserts only what is in the fact sheet. No OFF. No invented values.
- Orchestrator does NOT author the Hebrew inline — the Content Agent lane owns the voice.

## Milestones
- M1: engine harness + voice-wired prompt; runs on one category → scratch authored.json,
  tagged content_agent_v1, passes all deterministic gates. (this dispatch)
- M2: naturalness-gate + golden-eval scoring of M1 output vs the milk/blog quality bar;
  refiner pass on any line below threshold.
- M3: Adversarial QA red-team gate; owner review of the scratch pilot page before any talk
  of live rollout.

## M1 OUTCOME — DELIVERED + orchestrator-verified (2026-07-09)
`content_agent_v1` runs end-to-end. 20/20 cereals products authored by the real
LLM engine (scratch: `03_operations/reports/content/cereals_content_agent_v1.json`,
engine=content_agent_v1, missing=[]). Gates: validate_copy_authored PASS exit 0
(banned/sentence_repeat/fingerprint/mass/recite all 0) — re-run independently by
orchestrator; hebrew_readability 565/565 and naturalness F1 565/565 clean (after a
logged 18-string manual repair pass). Orchestrator READ a 6-product sample: genuine
Tom-voice, grounded rank/median/red-label findings, no framework leakage, no
recite-only lines — a real step up from the placeholder.

Infra debugged by orchestrator (mechanical, in-lane): Windows subprocess layer —
capture_output deadlock → stream-to-disk; 76KB prompt via stdin PIPE hit the 64KB
buffer and hung → fed via FILE HANDLE; timeout widened to 900s + `_kill_tree`.
Content Agent distilled the voice brief (76KB→~13.5KB), tuned BATCH_SIZE=1 (env
contention), added retry-once + per-batch checkpointing + a logged defingerprint
table (4/20 template-phrase collisions rewritten).

### Carried into M2 (open, not blockers)
- 148 hebrew_grammar_gate medium-confidence agreement flags → human/refiner pass.
- T11 shelf-wide monotony: nearly every rowVerdict is "positive → אבל/יחד עם זאת
  catch"; each line legal, the shelf rhythm is not. Prompt-refine for closer variety.
- Grade C vs D products don't yet read meaningfully firmer than each other.
- Voice-brief carve-out contradiction: the distilled brief's "לא X אלא Y (positive)
  = approved" vs `copy_rules.ANTITHESIS_RE` zero-exception ban — resolve in brief.
- naturalness F2 two-axis independent judge (Adversarial-QA lane) not yet run.

## M3 RED-TEAM (Adversarial QA, opus) — delivered 2026-07-09
Track V (verification) **PASS**: 0 invented numbers, 0 invented ingredients, all median
citations recompute, all red-label regulatory claims grounded, nulls respected,
bariInterpretation pass-through 0/200 diffs, defingerprint rewrites audited clean.
Track C (challenge) **FAIL** — 1 CRITICAL, 2 HIGH, 8 MEDIUM.
- **RT-1 CRITICAL** — engine minted absolute superlatives for 2 products whose
  `superlatives_allowed` is `[]` (9 assertions). Corpus-TRUE but UNAUTHORIZED. The
  breach is authorization, not accuracy: an engine that self-authorizes a true
  superlative will self-authorize a false one on the next corpus.
- **RT-2 HIGH** — fat framed as score-causal (2 products). On Delifkan the copy calls
  fat a headline negative while that product's `fat_quality` = 93.0 / "חזק".
- **RT-3 HIGH** — T11 monotony CONFIRMED + quantified: 18/20 rowVerdicts carry an
  explicit adversative pivot; effective rate 20/20.
- MEDIUM: define-by-negation survived the repair pass (Nesquik); double em-dash;
  "lowest sugar" absolute while sugar n=19; seed-oil qualifier not on label;
  advisory/motive framing (Trix); rounding; phantom `s_products`.
- **Key systemic result:** QA re-ran `hebrew_readability.is_clean` on 5 findings —
  **all 5 return True**. The deterministic gates are blind to every one. "565/565
  is_clean" certifies absence of banned strings, NOT defensibility. The adversarial
  layer is load-bearing, not decorative.

## NUTRITION RULINGS (governance, delivered 2026-07-09) — no owner escalation, no tripwire
1. **Sodium superlatives NOT sanctioned.** Sodium is in neither product's fired driver
   chain (no cap, no penalty, not lowest_dimension); no SKU in the run trips a sodium
   cap. A rank claim on a metric the engine never scored on is decorative, not a
   finding — it breaks "verdict names the real fired driver."
2. **New policy: `01_framework/editorial/superlatives_allowed_policy_v1.md`** — 5
   conditions: uniqueness · corpus n>=12 · margin >=10% of corpus range over 2nd place ·
   null-awareness · **driver-relevance tiering** (protein/kcal/sugar always headline-
   eligible; every other metric additionally requires being in that product's fired
   driver chain).
3. **RT-6 fixed in code:** `superlatives_context_for()` attaches `n_measured` /
   `phrase_as_among_measured`. Superlatives on incomplete metrics are claimable but the
   copy MUST say "among measured." Rice-apple's lowest_sugar margin is thin (0.4g on a
   26.1g range) — would fail the proposed margin gate; not to be headlined.
4. **RT-2 diagnosed:** copy misread the trace; the SCORE is correct, no change warranted
   (stopped at diagnosis per tripwire #1). Generalizable guard issued: copy's directional
   framing of a metric must never contradict that metric's own dimension score/strength.
5. **RT-7:** seed oil IS in the real scrape (BSIP1 `ingredients_list` 7/21 = "שמן צמחי"),
   not OFF, not fabricated — but the copy's "שמן צמחי מזרעים" adds a qualifier the label
   does not print, and only 1 of 4 seed_oil_present products names it. Rephrase + unify.
6. **RT-11 root-caused + fixed:** `S_VERBATIM` was a module global in the SHARED
   build_copy_inputs.py hardcoded with the YOGURT S-grade barcodes, leaked into EVERY
   category's `_meta.s_products`. Minimal filter fix applied + verified (cereals now `[]`).

Follow-ups spun out to **TASK-553** (code the margin gate; de-hardcode S_VERBATIM).

## Notes
- Related: [[baseline_copy_shipped_trap]], [[project_toms_voice]], TASK-374, TASK-262 (the
  seam / contract), the Hebrew Health Scan (TASK-381), [[gates_designed_not_enforced]],
  [[superlative_claims_need_corpus_rankcheck]].
