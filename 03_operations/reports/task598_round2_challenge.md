# TASK-598 Round 2 — Opus adversarial challenge of Sol's BSIP0 audit

Challenger: claude-opus-4-8 (CHALLENGE pin; cross-vendor vs Sol/GPT producer). Every claim below
was checked against the code/repo, not against Sol's prose.

## A. REFUTED — Sol's finding is factually wrong

**A1. "The 4-retailer fleet is not real" — REFUTED.** Sol wrote: "no canonical Tiv Taam peer was
found… Hazi Hinam is represented by an exploratory test." Both are false. Verified on disk:
`03_operations/bsip0/scrape/hazi_hinam/acquire_hazi_hinam.py` (223 lines, 17 def/http/url hits — a
real acquirer, NOT the `test_hazi_hinam_explore.py` sitting beside it) and
`03_operations/bsip0/scrape/tiv_taam/acquire_tivtaam.py` (exists, plus live captures under
`_smoke_probes/outputs/tivtaam_butter/`). Shufersal (`01_acquire_shufersal.py`, TASK-582-fixed) and
Yohananof (`raw_store/fetch_yohananof.py` 480 lines + per-category scrapers) complete the four.
→ The standing memory `bsip0_retailer_fleet_state` ("4 READY") holds. Sol's search missed the files
(likely the `acquire_tivtaam.py`/`acquire_hazi_hinam.py` naming). **DOWNGRADE the finding** from
"fleet not real" to Sol's *valid* sub-point: the four acquirers exist but share no uniform
interface/conformance contract — which is a real gap, just not the alarming one Sol stated. Sol must
concede the factual error and re-scope.

## B. CONFIRMED — verified real, keep

- **B1 comma-thousands** (`_to_float:555` blind `replace(",", ".")`) — confirmed, `'1,628'`→1.628.
- **B2 first-value-wins collisions** (`:324` `if field and field not in nutr`) — confirmed silent.
- **B3 sodium ceiling overbroad** (`:523-533` ">2000 mg/100g physically impossible") — confirmed
  scientifically wrong: salt ~39,000, soy sauce ~5,000-6,000, many cured/bouillon products exceed
  2,000 mg/100g legitimately. Sol is right it over-flags.

## C. CRUX — genuine disagreement, must resolve

**C1. The 0.2-mg sodium case — BOTH prior positions are overconfident.** Sol's Part A asserts snacks
`7290019297208` `'0.2'`+מג "must be 0.2 mg." My TASK-595 adjudication asserted it's 200 mg (0.2 g,
matching published). **Neither is defensible from the capture alone.** 0.2 mg sodium/100g is
physically absurd for a snack; 200 mg is plausible — but we are BOTH inferring the label from a
capture that recorded `{value:'0.2', unit:'מג'}` without the source image. Sol's own rule ("trust
the token, never infer unit from magnitude") mechanically yields 0.2 mg — i.e. **Sol's recommended
rule fails on Sol's own acceptance case by launder­ing an implausible value into a confident
output.** My "200 mg" equally assumes a scraper mis-tag we can't prove. **Correct resolution:
fail-CLOSED to FLAGGED/UNRECOVERABLE on a token-vs-plausibility conflict** — when the token says mg
but the value as-mg is implausibly low for the field, emit NULL+flag, never a number. This specific
value needs the label image; it is not recoverable from the row. Sol must move off "0.2 mg = truth."

**C2. Sol's framework is internally inconsistent.** Sol argues (units) "never infer from magnitude —
a present unit is authoritative," yet its comma rule IS magnitude/context reasoning: `'1,234'`→1234
vs 1.234 cannot be resolved lexically without field awareness (energy 1,234 kcal/100g is impossible
→ must be 1.234; sodium 1,234 mg is fine → thousands; fat 1,234 g is impossible). **A purely lexical
comma rule is field-blind and will mis-disambiguate.** Either magnitude/field plausibility is a
legitimate input (then it applies to BOTH units and commas, and C1 resolves toward flagging) or it
isn't (then the comma rule is unsafe). Sol can't have it both ways. My position: plausibility is a
FLAGGING signal, never a silent CORRECTION — it decides "trust vs flag," never rewrites a value.

## D. OVERBUILD CHALLENGE — 9 accepts is not a plan

Anti-overbuild doctrine ([owner_systematic_not_artisanal], MVP-first): Sol accepted all 9 proposals.
That's a wish-list, not a sequence. Force a ranking tied to DEFECT EVIDENCE:
- **Prerequisite (must, enables everything):** #2 capture provenance manifest + #1 replay-everything
  harness. Without a canonical capture set + replay, NONE of the integrity checks can even be
  quantified (Sol's own probe returned `parsed_nutrition_candidates=0`). These two first.
- **Second wave (should, high evidence):** the comma+unit fix (owned by another session), typed
  `{value,unit,relation}` quantity (fixes B2 + bound-loss), and the sodium-ceiling correction (B3).
- **Later / needs justification:** capture format v2 (large migration — the raw HTML + a manifest may
  suffice, Sol's own counter-argument), per-category sodium bounds (circularity risk Sol flagged),
  energy-macros validator (Atwater tolerance makes it review-only, low yield).
Challenge to Sol: defend any "must-now" beyond #1/#2 with a defect count, or concede it to "later."

## E. Cruxes for Round 3 (Sol to defend or concede, point by point)
1. A1: concede the retailer factual error; re-scope to "no uniform interface."
2. C1: does Sol hold "0.2 mg = truth," or accept fail-closed-to-flagged?
3. C2: resolve the units-vs-comma magnitude-inference inconsistency.
4. D: rank the 9 proposals into must/should/later with defect evidence, or defend all-9.
