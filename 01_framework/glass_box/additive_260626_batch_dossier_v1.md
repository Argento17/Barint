---
document: additive_260626_batch_dossier_v1
task: owner gap-fill batch (conversation work, 2026-06-26) — follow-on to E120
program: TASK-181 (Glass Box D4 additive library) — addendum to 181A/181B
phase: Detector wired (score-neutral). D4 TIERS = Nutrition CO-SIGNED 2026-06-26 (2 down-ranked from researcher proposal). Citation IDs corrected to operative anchors; C0 verify still pending before consumer use.
status: TIERS CO-SIGNED (Nutrition) — Product scope co-sign + C0 citation pass + promotion pending
owner: orchestrator (transcription) → Nutrition (tiers + citation reconciliation) → Product (emulsifier scoring-entry + scope co-sign)
provenance:
  - "research/Evidence Registry/Additives/260626/Additive Evidence Registry Memos.pdf" (owner-supplied)
  - "research/Evidence Registry/Additives/260626/Bari Evidence Registry Memos for Annatto Sulphites and Selected Emulsifiers.pdf" (owner-supplied, variant)
  - commission brief: orchestrator → AI researcher, 2026-06-26
---

# Additive Evidence Dossier — 260626 Batch (E160b · sulphites E220–E228 · emulsifier trio E435/E475/E477)

Three additives/families the D4 library had never assessed, commissioned after the E120 gap-scan
surfaced them on live shelves. Evidence supplied by the owner's AI researcher (2 PDFs). This dossier
transcribes it, records what was wired, and **flags three unverified citations** that gate the severe
tiers.

## What was DONE (reversible, in-lane, no tripwire)
- **Detector wired** in `03_operations/bsip2/proto_v0/src/ingredient_taxonomy.py` for all five canonicals:
  `annatto_bixin_norbixin` (E160b), `sulphite_family` (E220–E228), `polysorbate_60` (E435),
  `polyglycerol_esters` (E475), `pgms_propylene_glycol_esters` (E477).
- **Provably score-neutral**: every entry uses a non-scoring `additive_class`
  (`colorant_natural` / `preservative_sulphite` / `emulsifier_unscored_pending`) and
  `is_named_concern=False`. None equals one of the four ECS scoring branches
  (`emulsifier_concern/benign/medium/low`). Verified by 8 added selftest checks incl. explicit
  "outside every scoring branch" assertions; full selftest `ALL PASS`, 0 FAIL.

## What was deliberately NOT done (flagged, not built)
- **D4 tiers not finalized** — researcher proposals below are PENDING Nutrition co-sign.
- **Sulphites → SCORING not wired.** The proposed `confirmed-negative` is the **first-ever** at that
  tier and the additive is on **live juice / dried-fruit-bearing shelves**; making it move a grade is
  an **owner-gated scoring decision (tripwire #1)**, not done here.
- **Emulsifier trio → ECS scoring not wired.** Placing E435/E475/E477 in a real ECS class
  (`emulsifier_medium`/`concern`) would move **live cakes/cookies scores** — owner-gated, deferred.
- **No consumer copy shipped** — the Hebrew drafts in the PDFs stay drafts (two-gate required).

## CITATION INTEGRITY — C0 gate RUN 2026-06-26 (`verify_citations.py`, PubMed/CrossRef)
Nutrition flagged 3 IDs as "not in works-cited." The deterministic C0 gate then resolved every ID
against the live registries — and **clears most of them**: the worry was largely a false alarm.

| ID | Drives | C0 gate verdict (resolved title) |
|---|---|---|
| `DOI 10.2903/j.efsa.2022.7594` | sulphite `contested` | **GENUINE ✅** — resolves to *"Follow-up of the re-evaluation of sulfur dioxide (E220)…(E228)"*, EFSA Journal 2022. (Gate marked "MISMATCH" only as a context false-positive — the ID sits next to flag-prose in this table, not a clean sentence.) |
| `PMID 34320336` | E160b `likely-neutral` | **GENUINE ✅** — *"Annatto hypersensitivity… placebo-controlled oral challenge"* 2021. |
| `PMID 19772519` | E160b `likely-neutral` | **GENUINE ✅** — *"Allergy for cheese: IgE-mediated reaction from the natural dye annatto"* 2009. |
| `DOI 10.1016/S2213-8587(24)00086-X` (Lancet, HR 1.34 T2D) | E475/E477 | **REAL ✅ but mis-applied** — Research 2026-06-26: DOI resolves (PMID 38663950, NutriNet T2D, n=104,139); gate UNRESOLVED was a CrossRef encoding glitch on `(24)`. **BUT the paper does NOT individually name E475 or E477** (it names E407/E340/E472e/E331/E412/E414/E415). PLOS Med `1004570` (PMID 40198579, real) is mixture-level only. → **Pre-auth upgrade NOT triggered; E475/E477 stay `likely-neutral`.** |
| `PMC6899614` (E435 gut-barrier mechanism) | E435 `contested` | **REAL ✅ but WEAK/indirect** — Research 2026-06-26: real (PMID 31866761, FADiets) but it's a review/protocol paper naming only **polysorbate-80 (E433)**, NOT E435; E435 inherits by structural homology only. **E435's `contested` tier is now under Nutrition re-review** (see §3). |
| (E120 dossier, separate sweep) | E120 | **2/2 PASS ✅** — EFSA 2015 `10.2903/j.efsa.2015.4288` + `PMID 29705083`. |

**Net:** sulphite + annatto + E120 citations are verified genuine; only the Lancet/E475 DOI is
unresolved (and already neutralised by the down-rank). E435's mechanism rests on class-homology to
the already-`contested` E433 (operative ref `PMC6899614`/FADiets), independent of the Lancet ID.

---

## 1. E160b — Annatto (bixin / norbixin)

- **Researcher tier:** `likely-neutral` (parallel to E120 — rare IgE hypersensitivity to annatto
  protein/hapten, otherwise clean; **plant-derived → vegan-compatible**, unlike E120).
- **Identity:** EFSA 2016 split ADIs — bixin 6 mg/kg bw, **norbixin 0.3 mg/kg bw** (20× stricter;
  toddler 95th-pct over-exposure prompted EU 2020/771 split into E160b(i)/(ii)). Israel MoH caps:
  10 mg/kg margarine, 15 mg/kg ripened cheese.
- **scoring_effect (proposed):** nutrition_score no_change · additive_complexity mild_flag ·
  dietary_preference **none** · allergy_caution optional_contextual_rare.
- **Shelf:** ~26 products (cakes, cereals, cookies-coffee, hard cheeses).
- **Citations:** `10.2903/j.efsa.2016.4544` · `CELEX:32020R0771` · `PMID 34320336` · `PMID 19772519` (all corroborated).

## 2. Sulphite family — E220, E221, E222, E223, E224, E225, E226, E227, E228

- **Tier: `contested`** — Nutrition CO-SIGNED 2026-06-26, **DOWN-RANKED** from the researcher's
  proposed `confirmed-negative`. Reason: the confirmed-negative bar = population-level weight-of-
  evidence harm on the IARC/RCT standard (held by E249/E250 nitrites); an EFSA MOE breach +
  a subgroup allergen pathway clears `contested` but not that bar — and `confirmed-negative` would
  contradict the library's own E224 ruling (EV-102), which held the same EFSA-2022 basis at `contested`.
  `cosmetic_mup=False` (preservative).
- **Two harm pathways (both real, both `contested`-weight):** (a) **declared allergen** — sulphite-induced asthmatic bronchospasm,
  Israel SI 1145 mandates a bolded warning ≥10 mg/kg (confirmed pathway, not observational);
  (b) **systemic** — EFSA 2022 withdrew the group ADI, BMDL 38 mg SO₂-eq/kg, MOE < 80 (safe
  threshold) at **typical** dried-fruit/juice/wine intake.
- **scoring_effect (proposed):** nutrition_score no_change · additive_complexity **strong_flag** ·
  dietary_preference none · allergy_caution **declared_allergen**.
- **Shelf:** ~34 products (cakes, cookies-coffee, granola, bread, **juices**).
- **⚠ Citation:** headline EFSA-2022 DOI flagged above — reconcile before treating the tier as final.
- **Note vs library:** the E224-only mention attributed to EV-102 (the EHJ HTN paper) is a *different*
  basis; this is a family-level entry on the EFSA-2022/allergen basis.

## 3. Baked-goods emulsifier trio — E435 (polysorbate 60) · E475 (PGE) · E477 (PGMS)

- **ALL THREE → `likely-neutral`** (Nutrition CO-SIGNED 2026-06-26, re-ruled after Research verified
  the citations). **NONE are score-eligible.** `cosmetic_mup=True` for all three.
  - The researcher proposed all three `contested`. Verification collapsed that: the mechanism source
    `PMC6899614` (real) names only **E433**, not E435; and the Lancet T2D cohort (PMID 38663950, real)
    does **not** individually name E435, E475, or E477. Per the **E472e precedent** (class-homology
    without individual naming/substance-specific mechanism = `likely-neutral`, not `contested`), all
    three stay neutral. **E435 was down-ranked from the initial `contested`** once its mechanism basis
    was shown to name only its sibling E433.
  - **Reassess triggers:** E435 → any substance-specific human study that measures E435 individually
    (separate from E433); E475/E477 → confirmation that PLOS Med `10.1371/journal.pmed.1004570` names
    them individually (Research checked: it is mixture-level only, so currently NO).
- **EFSA classical view = safe** (E475 no-ADI, E477 25 mg/kg, E435 group 10 mg/kg).
- **Net for the what-if:** the trio contributes NOTHING to scoring → the scoring what-if is
  **sulphites-only.**
- **Dietary note:** fatty-acid source can be plant **or animal** → ambiguous for vegan/kosher/halal
  without certification (researcher proposes a dietary_preference caution — a *new un-built signal*,
  same status as E120's vegan flag, currently PARKED by owner).
- **scoring_effect (proposed):** nutrition_score no_change · additive_complexity strong_flag ·
  dietary_preference vegan/halal/kosher_caution (un-built) · allergy_caution none.
- **Shelf:** ~44 products (cakes, cookies-coffee).
- **⚠ Two citations flagged above. ⚠ ECS scoring-entry is owner-gated (would move live scores).**

---

## Sulphite scoring what-if — RESULTS (2026-06-26, no publish)

Artifact: `_sulphite_whatif_260626/sulphite_whatif_20260626T133404Z.json`. Engine files were modified
to run it, then **reverted to HEAD** (tree clean); the runner script + artifact are retained.

**Mechanics:** D4 penalty = 2 × (#score-eligible contested additives), so a sulphite declaration =
a flat **−2 points** per product (capped by D4_SCORE_CAP=8). Regression with flags off = byte-identical
(max delta 0.0).

**Impact across live shelves:**

| Shelf | Corpus | Sulphite carriers | Grade changes | Mean Δ |
|---|---|---|---|---|
| juices | 32 | 5 (15.6%) | 0 | −2.0 |
| cakes | 167 | 27 (16.2%) | 1 (D→E) | −1.93 |
| cookies_coffee | 209 | 30 (14.4%) | 2 (D→E) | −1.93 |
| cereals | 45 | 0 | — | — |
| **total** | **453** | **62** | **3** | — |

(bread + granola corpora unavailable at standard path — not scanned.) **Only 3 of 62 carriers cross a
grade boundary** (all D→E); the rest absorb −2 within grade; 2 are already at the cap (Δ 0).

**⚠ Material discovery — sulphites are ALREADY partially live.** `cookies_coffee` ships with
`BARI_D4_SCORE_V1=on` (TASK-393, 2026-06-26) and the pre-existing E224 entry is already score-eligible
(EV-102) → 2 cookies products are **already at E from sulphite on the live page**, independent of this
batch. So "should sulphites score?" is already answered YES on one live shelf. For juices/cakes it is
OFF (needs the master flag).

**⚠ Wiring caveat (for any future activation):** do NOT simply gate the existing live E224 entry behind
a new flag (the what-if's first wiring did this) — on the D4=on cookies shelf that would *revert* live
sulphite scoring. A clean activation adds the **expanded E220-family detection** (the live E224 has only
8 patterns and misses the common SO₂ form "דו תחמוצת הגופרית") as a proper family entry, decoupled from
the already-live E224 behaviour. Captured here as a design note for the D7 proposal.

## Activation decision (owner 2026-06-26): JUICES now, CAKES separate

The full D7 movement table (`_d4_activate_juices_cakes_260626/…135743Z.json`) showed that activating
D4 on **cakes** moves 80/167 products (48%) but **only 6 are sulphite-driven** — 74 are **E471** and
other additives the same master switch activates. Owner ruled:

- **Juices → PROCEED.** Turn D4 additive scoring on for juices. Impact: **6 products −2 within grade
  (5 sulphite, 1 E471), 0 grade changes.** Clean, sulphite-dominated. → D7 co-sign → owner final publish go.
- **Cakes → SEPARATE decision.** The cakes move is overwhelmingly an **E471 / full-D4 activation**, not
  a sulphite matter — and committed `cakes.json` has D4 **off**, so it would be a first-time full
  activation re-grading ~half the shelf. Pulled out to its own Nutrition+Product reviewed decision
  (NOT a rider on the sulphite go-ahead). Logged as a future item.
- **Cookies → unchanged** (sulphites already live there; the 10 newly-caught by expanded patterns are
  non-displayed corpus products, 0 committed-score changes).

Engine/config working-tree changes were **reverted** (tree clean); the package is preserved in the
artifact and re-applies cleanly for the juices publish.

## D7 co-sign — JUICES sulphite activation (2026-06-26): BOTH YES

- **Product: CO-SIGN YES (unconditional).** Declared allergen (SI 1145) + EFSA MOE; proportionate
  (0 grade changes); consistent with the live cookies precedent. Recommends clean family-entry wiring
  + both page gates before merge.
- **Nutrition: CO-SIGN YES (conditional).** Tier `contested` sound (two non-observational pathways);
  −2 proportionate; **accept the 1 E471 mover** (legitimately contested via EV-061 D7 2026-06-15, not a
  scope leak — do NOT add a sulphite-only shelf restriction); SO₂ pattern low false-positive risk.
  **Condition (D8 verification, not a D7 reopener):** before commit, prove the new E220-family entries
  do not shadow the live E224 — cookies_coffee re-run byte-identical + an explicit "E224 unchanged"
  preflight assertion.

→ Rule APPROVED. Remaining before publish: clean implementation + regen juices JSON + both page gates
+ the E224-isolation proof → then **owner final merge** (production publish stays owner-gated).

## Open items / routing

| # | Item | Owner | Status |
|---|---|---|---|
| 1 | Reconcile the 3 flagged citations | Nutrition | ✅ DONE 2026-06-26 — operative anchors: sulphites `PMC9685353`, E435 `PMC6899614`, E475/E477 candidate `10.1371/journal.pmed.1004570` (unconfirmed). Claims real, IDs corrected. |
| 2 | Co-sign D4 tiers | **Nutrition Agent** | ✅ DONE 2026-06-26 — E160b `likely-neutral` ✓; sulphites **`contested`** (down-ranked from confirmed-negative); E435 `contested` ✓; **E475/E477 `likely-neutral`** (down-ranked, w/ pre-auth reassess). 0 score moves. |
| 3 | `verify_citations.py` C0 gate | C0 gate | ✅ RUN 2026-06-26 — sulphite DOI + annatto PMIDs + E120 cites GENUINE; only Lancet/E475 DOI UNRESOLVED (already neutralised by down-rank). See citation section. |
| 4 | Verify Lancet DOI / whether PLOS Med `1004570` names E475/E477 individually → auto-upgrade to `contested` | **Research Agent** | DISPATCHED 2026-06-26 (pre-authorized reassess) |
| 5 | Scoring **what-if** — SULPHITES-ONLY | **Data Agent** | ✅ DONE 2026-06-26 — flat −2/product; 62 carriers across juices/cakes/cookies; **only 3 grade changes** (D→E); cereals 0; regression PASS; engine reverted (tree clean); NOT published. Results section above. |
| 5a | **Re-review E435 tier** | **Nutrition Agent** | ✅ DONE 2026-06-26 — E435 → `likely-neutral` (not score-eligible). Whole trio now neutral. |
| 5b | **Broader finding:** Lancet T2D PMID 38663950 individually names E412/E414/E415/E331/E340/E472e (some live at `functional`) | Nutrition | ✅ ASSESSED — **NOT a re-tiering trigger** (one cohort, no mechanism, strong UPF-confounding; guar/xanthan fibre evidence points opposite). Nutrition recommends a **watch-flag note** at next maintenance cycle, not a program. No published-score risk. |
| 6 | Product scope co-sign | Product Agent | ✅ DONE 2026-06-26 — **all six RETAIN** (sulphites flagged highest-maintenance but justified by juice-shelf exposure; E475/E477 retain w/ pre-auth reassess) |
| 7 | Two-gate (Content + Adversarial QA) on any Hebrew copy before a page | content gates | PENDING — not actionable yet (no page surfaces these) |
| 8 | Promote rows #38–#40 into live library + display config | Data Agent | PENDING (Product co-sign now clear; awaits owner's read of the what-if for the scoring entries) |
