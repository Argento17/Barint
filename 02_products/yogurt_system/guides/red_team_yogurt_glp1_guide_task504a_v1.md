# Red-Team Challenge Report — GLP-1 high-protein yogurt guide (TASK-504A)
Date: 2026-07-08
Scope: `/madrichim/yogurt-glp1`, 4-product shortlist + 3-product drinkable callout, reusing shipped
yogurt_spoonable (78) + yogurt_drinkable (20) comparison data. Verdict: **OWNER-READY — 0 CRITICAL, 0 HIGH.**

---

## Build history summary

**Origin:** blocked once (2026-07-05) on a milk-shelf corpus — 3 CRITICALs (gameable protein bar,
medication-frame overclaim, no real high-protein dairy in that corpus). Owner redirected into
building a real yogurt category (TASK-515/515A) instead. Rebuilt on that corpus, same session it
shipped (2026-07-08).

**Product re-scope (GO, orchestrator-verified):** both original CRITICALs resolved — 23/78 spoonable
products clear ≥8g protein/100g in a genuine bimodal tier (dead zone 6.5–10.0g, not a low-cal-filter
artifact); real high-protein dairy now in-corpus. Scope: spoonable primary, drinkable folded in as a
secondary callout (only 3/20 clear the threshold).

**Nutrition bar spec (locked, independently re-derived, orchestrator-verified exact):** protein =
absolute grams, ≥8g/100g; sodium = real corpus bands (≤35/36-65/>65mg); sugar = REDESIGNED 3-way
word-boundary keyword + d4_additives classifier (the originally-planned field didn't exist in the
real data; raw sugar_g alone was proven unusable — no-added max 5.3g overlapped added-sugar min
3.1g). `satiety_support` re-confirmed DROPPED (still calorie/ratio-driven one layer down).

**Content GATE-1 + Adversarial QA GATE-2:** one real round. RT-1 (HIGH): categoryCaveat +
shortlist[3] misidentified barcode 7290119377411's two score-limiting additives as "modified tapioca
starch + stabilizer" when the real tagged additives are modified starch (E1422) + citric acid (E330,
contested) — fixed by genericizing to match the product's own existing comparison-page copy
convention. RT-2 (HIGH): hero's lean-mass/protein science claims had no on-disk evidence record on a
medication-adjacent topic — Research produced `GLP1_GUIDE_SCIENCE_COSIGN_v1.md` (11 real PMIDs,
CrossRef-verified, primary source PMID:41877354 reports "25%-39%" near-verbatim; both claims ruled
defensible as written, no reword needed). Both fixes independently re-verified; GATE-2 re-check PASS.

**Frontend build:** `/madrichim/yogurt-glp1`, noindex until owner robots-flip, reuses frozen
ScoreChip + CategoryNoteBox components (0 new visual primitives), copy rendered byte-frozen. Build
correctly disclosed a spec-conflict (2 S-grade products fold to "A" badge per the frozen chip's no-S
rule) which surfaced a real gap: the signed-off copy's prose for those same 2 products literally said
"דירוג S" — the identical defect class (RT-R2-1) already caught once this session on the spoonable
comparison page. Fixed by genericizing to relative-standing framing ("one of the two highest-scoring
products"), no letter grade named; the 3rd shortlist card's accurate self-limitation reference
("...fell short of S") correctly left untouched.

---

## Terminal red-team (this report) — final state

**Track V (verification):** full GREEN. Copy byte-fidelity (source↔built, sha256 exact match).
Route 200, `lang=he dir=rtl`, noindex meta present. All 4 shortlist grade badges verified live in DOM
(93·A / 91·A / 90·A / 65·B) matching the shipped comparison JSON's raw scores/grades folded through
the same `frontendGradeFromScore` pipeline as the live comparison page — 0 literal "S" badges. Both
`fullListNote` links resolve 200. Category-caveat box confirmed rendering via the shared
`CategoryNoteBox` component (not a new one). 0 horizontal overflow, 0 console errors attributable to
the page, both 375px and desktop. Score-propagation audit: all 4 shortlist barcodes' protein/sodium/
sugar copy claims exact-match `expansion.nutrition`; drinkable callout's 3 barcodes exact-match;
sodium medians (drinkable 53, spoonable 48) exact-match.

**Track C (challenge):** PASS. Each shortlist card's specific claim independently re-derived against
its trace/JSON and found justified (the "highest-scoring" framing on cards 1–2 is accurate — 92.6 and
90.6 are genuinely the top 2 both within the shortlist and the full 78-corpus; card 3's ingredient-
length limitation matches its trace; card 4's generic "two additives" matches its trace exactly, RT-1
confirmed intact). **Shortlist completeness independently re-derived**: hand-checked the intersection
of protein≥8g AND no-added-sugar AND no-alt-sweetener across all 23 qualifying products — the 4
shortlisted barcodes are the exact, complete, correct set; no 5th product was wrongly omitted.
Medication-framing challenge: 0 drug brand names anywhere (JSON/HTML/meta), 0 per-product medical
claims, 0 "GLP-1 friendly" badge, 0 nausea/fiber/hydration mentions in visible DOM — stays within
general-nutrition-guide framing throughout.

## Final state — all findings

| ID | Severity | Status |
|---|---|---|
| RT-1 (wrong additive identity, 7290119377411) | HIGH | RESOLVED, verified |
| RT-2 (no evidence record for hero science claims) | HIGH | RESOLVED, verified |
| S-vs-A copy/chip mismatch (RT-R2-1 recurrence) | HIGH | RESOLVED, verified |
| RT-M1 (VM over-serialization into hydration payload) | MEDIUM | OPEN, non-blocking (TASK-531) |
| RT-L1 (stale sha256 in code comment) | LOW | OPEN, non-blocking (TASK-532) |

**0 open CRITICAL. 0 open HIGH.** Page is owner-ready.

## Non-blocking follow-ups (routed, not fixed)
- TASK-531 (MEDIUM, frontend-agent): pass a 4-field VM projection instead of the full comparison VM
  to avoid serializing framework-mechanic vocabulary + fiber text into the (consumer-invisible,
  noindex) hydration payload.
- TASK-532 (LOW, frontend-agent): refresh a stale sha256 reference in a code comment.
- TASK-529 (MEDIUM, data-agent, pre-existing/unrelated): 7290119377411's `expansion.ingredients`
  display text names a different E-number/additive than its scored `d4_additives` card — a separate
  data inconsistency from the RT-2H1 fix set, surfaced incidentally while re-verifying RT-1.
- TASK-530 (LOW, product-agent): decide whether the hero's science claims need a visible on-page
  citation before PUBLIC launch (the on-disk evidence record satisfies the defensibility requirement
  for this build; the visible-footnote question is a separate editorial call).

## Verification instruments run
`hebrew_readability.analyze` (all touched strings, is_clean=True), sha256 file-sync checks (source↔
built copy), Playwright real-DOM render at 375px + desktop, `verify_citations.py` C0 citation-
integrity gate (0 fabricated, 2 heuristic false-positives on real PMIDs — logged TASK-528), manual
guardrail term scan (drug names/medical claims/omitted-topics), independent shortlist-intersection
re-derivation against the full 78-product corpus.
