---
id: TASK-171
title: Supplement Intelligence Engine (SIE) - MVP
owner: nutrition-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-06-03
closed_at: 2026-06-03
cc_reviewed: true
depends_on: []
blocks: []
category_id: null
roadmap_impact: true
work_type: objective
drift_ack: "Umbrella objective CLOSED 2026-06-03 — all sub-tasks 171A–L closed; engine banked as a proven asset, acquisition experiment closed, no launch (D10/D1 not made)."
banked_asset:
  one_liner: "Supplement Intelligence Engine (SIE) — sibling scorer to BSIP2 for supplements; 5 dims, 15 cited dossiers, golden 17/17, validated on real Israeli SKUs."
  why_parked: "Engine proven; the wall is panel acquisition — Israeli shelf is local-brand-dominated and only ~6.8% reachable by scraping (171J). Reviving is a business-development question (manufacturer data feed), not engineering."
  revival_gate: "A manufacturer/importer data feed (BD), then EDPG candidate→promote (D3/D4) + QA freeze on real panels + a separate launch decision (D10/D1)."
  reference: "03_operations/supplement_engine/SIE_ASSET_AND_CLOSURE.md"
  banked_at: "2026-06-03"
summary: >
  Sibling scoring engine to BSIP2 for supplements (different object: active/dose/form/evidence tuple, not a per-100g panel). MVP proves a 5-dimension scorer (Evidence Strength, Dose Adequacy, Form/Bioavailability, Formulation Honesty, Safety Ceiling) on a minimal 5-active stress set before any category expansion.
---

# TASK-171 — Supplement Intelligence Engine (SIE) - MVP

**CLOSED 2026-06-03 — engine PROVEN & BANKED as an asset; acquisition experiment CLOSED; NOT launched.**
Outcome: a strong, self-explaining, cheap-to-maintain (~30–33 h/yr) supplement engine — 15 actives, methodology
v1.3 (D7 co-signed), golden corpus 17/17, validated on real Israeli SKUs — parked because the Israeli shelf can't
be acquired economically by scraping (measured ~6.8% reachable, 171J), not because the engine fell short. Reviving
it is a business-development question (manufacturer data feed), not engineering. All candidate; nothing shipped;
D10/D1 not made; food invariants untouched. **Canonical record: `03_operations/supplement_engine/SIE_ASSET_AND_CLOSURE.md`.**
Sub-tasks 171A (methodology) · 171B (5 dossiers) · 171C (engine+golden) · 171D (Israeli corpus/acquisition) ·
171E (claim-resolution v1.3) · 171F (coverage analysis) · 171G (plumbing) · 171H (→15 actives) · 171I (acquisition
scoping) · 171J (MVP build+measure) · 171K (Hebrew claim-vocab fix) · 171L (archive+close) — all CLOSED.

---

**Status:** Phase 0 COMPLETE (D7 co-signed). Phase 1 authorized, pending owner go. No engine code yet.

## v1.1 amendment (2026-06-03, owner-approved, Product RE-RATIFIED)
Two scope refinements that *tighten* the MVP (no change to the 5-dimension model):
- **Evidence probe swapped ashwagandha → omega-3 (EPA/DHA).** Ashwagandha's core difficulty (contested botanical evidence + extract standardization) is exactly the machinery MVP defers — incoherent probe. Omega-3 isolates Evidence better (same molecule/form: Strong-for-TG, Weak-for-"brain & mood") and adds the "1,000 mg fish oil" mass-honesty trap. Ashwagandha + botanical subsystem → Phase 2.
- **Dossier lifecycle/maintenance model added** (`methodology_v1.md` §5.1). Names dossier maintenance — not scoring — as the dominant operational risk (stale dossier = silent misrank). Stable-vs-drift fields, staleness *detection* not auto-update, change-control, lean on NIH ODS/EFSA. **Product owns a maintenance-cost go/no-go gate**: MVP must measure per-dossier build+maintenance cost (drift-vs-stable author-hours, re-verification cadence, authority-leverage ratio, per-active variance) before any scale-up.

## Phase progress
- ✅ **Phase 0** (TASK-171A, CLOSED) — `methodology_v1.md` v1.0 → **v1.1** authored + D7 CO-SIGNED, then RE-RATIFIED (Nutrition + Product) after the v1.1 amendment.
- ✅ **Phase 1** (TASK-171B, CLOSED) — 5 Evidence Dossiers built (Research) + all tiers D6/D7 CO-SIGNED (Nutrition); SUPP-EV registry created; lifecycle model instantiated; build-cost report = **conditional GO** for scale-up. All `candidate` / non-score-affecting.
- ✅ **Phase 2** (TASK-171C, CLOSED) — engine prototype built (Data) + D8-VERIFIED (Nutrition) + FLAG-2 D7 co-signed (Product). **14/14 golden fixtures pass grade + binding-constraint; inverted-E pair proven distinct.** Dose short-circuit, binding-constraint attribution, caps/vetoes all implemented to v1.2 spec. Standing Safety meta-rule added (veto=toxicity only; reversible-tolerance→note). All candidate/calibration-pending; nothing ships. See accumulating scope below (now largely realized).
- ⏳ **Phase 3** (TASK-171D, IN_PROGRESS) — Israeli corpus. **Step 1 probe + 5-SKU PoC DONE.** Owner chose **bounded widen to 15 + plumbing + real corpus**:
  - ✅ **Acquisition plumbing** (TASK-171G, CLOSED) — Super-Pharm catalog reader + iHerb panel-extract + barcode bridge; live catalog read (176 supplements/store, 924 stores); bridge correctly rejects ships-to-IL-only US brands; ~40–60% complete-label first pass. ⚠️ local brands (Altman/SupHerb) need a non-iHerb panel source; ⚠️ live run needs firecrawl scrape permission.
  - ✅ **Dossier expansion → 15 actives** (TASK-171H, CLOSED) — +vit C, zinc, iron, calcium, folic acid, B12, melatonin, biotin, vit E, CoQ10. 16 dossiers load clean, golden 17/17, coverage ~40–55%, maintenance ~30–33 h/yr (validated). ⚠️ a real ~15-mis-PMID first-pass error (self-caught) → "PMID title-check" sweep step needed.
  - ✅ **Thin live proof** (TASK-171D Step 3) — global-brand SKUs scored end-to-end LIVE: **Solgar Omega→C/60.5** (real panel; "Heart Healthy"→contested CV endpoint), **Solgar Zinc→B/68.4**. Pipeline PROVEN on real Israeli SKUs. **But: iHerb yields only ~2–4 SKUs** (the "~23" was an importer-field over-count; Israeli-pack barcodes differ from iHerb-US). **iHerb is NOT a breadth source.**
  - ✅ **Acquisition scoped** (TASK-171I, CLOSED) — Super-Pharm PDP panels ≈0%; **unlock = Israeli 3rd-party vitamin e-tailers** (one generic adapter, ~75–85% addressable); OCR = fallback; Life house-brand residue (~18%) needs a manufacturer feed. **Cost: ~8–10 day MVP / ~15–19 day full → ~42–48% net shelf** (from ~11% today). Product rec: **BUILD phased** (8–10d MVP as a measurement instrument → run real corpus → then decide launch).
  - ✅ **MVP acquisition built + corpus MEASURED** (TASK-171J, CLOSED) — adapters (3rd-party e-tailer + Altman + resolver) built; ran on 118 addressable SKUs. **⚠️ MEASURED YIELD = 6.8% (8/118), NOT the projected ~31–37%** — local-brand panel sources resolve almost nothing at scale. Engine scored every real product correctly (Altman Vit D→S/91.2 clean win; 450mg-oxide mag→E safety veto; biotin cosmetic→E). 2nd finding: **claim-umbrella vocab incomplete for real Hebrew labels** (fatigue/absorption claims don't map → unfair E; Nutrition D6 fix).
  - ⏳ **RE-DECISION (owner):** the measurement weakened the build case (~7% reachable, not ~half-shelf). Options: iterate acquisition (more sources + Hebrew claim-vocab fix) + re-measure · pursue manufacturer-feed/BD path · pause. Engine proven; reachable corpus currently ~7%. Go-live = separate D10/D1; nothing shipped.
- **v1.3 claim-resolution amendment** (TASK-171E, CLOSED) — surfaced by the PoC: the engine was scoring Evidence off *legally-coerced vague label wording*, flooring honest products. Fix (owner posture: **moderate**): vague structure/function claims **resolve** to the active's cited studied endpoints via a dossier umbrella-map; Insufficient→E only when nothing maps; over-promises caught by Honesty. Nutrition D6 + Product D7 co-signed; Data implemented; **17/17 fixtures, magnesium E/34→B/77.3.** Brand stance: "punish over-promise, not compliance."
- ⬜ **Phase 4** — frontend category page (separate verdict model) + consumer Hebrew explanation prose. *Go-live = separate D10/D1, not yet decided.*

## Phase 2 scope — accumulating requirements (captured pre-build, from owner challenges 2026-06-03)
Surfaced while pressure-testing the engine's *attribution* (can it tell apart, and explain, different failure modes). Fold into the Phase-2 spec + a small co-signed methodology addendum before building:
1. **Dose short-circuit rule.** If Evidence tier = Insufficient, Dose Adequacy is **N/A — never positive credit** (a no-evidence active must not read "well-dosed" off `market_range_dsld`; keeps attribution honest). Methodology §2.2/§3 addition.
2. **Failure-attribution explanation layer (machine "why").** The engine must emit *why* a product failed = the **binding constraint** (the cap/veto that actually bound the grade under most-restrictive-wins), not merely the lowest sub-score. Inherits BSIP2's explanation discipline (grounded-in-real-trace, dominant-driver/anti-attribution rules, banned-phrase list) + the No-Necessity firewall. Machine-readable "why" = **Phase 2**; consumer Hebrew prose = **Phase 4**.
3. **Golden corpus gains the attribution axis** — three named failure archetypes the engine must both *distinguish* (signature) and *explain* (binding "why"), beyond the per-dimension anchors:
   - **Good active / wasted** (fairy-dust, e.g. 1 g creatine) → **D**; "sound active, a fifth of the studied dose."
   - **Bad active / excellent product** (no-evidence active, impeccably made) → **E** (evidence ceiling); "well-made, no reliable evidence it does this." Ev LOW · delivery HIGH.
   - **Good active / dangerous product** (extreme dose, e.g. 50,000 IU D3 daily) → **E** (safety floor); "active is sound, the dose is unsafe." Ev HIGH · Safety VETO.
   *Note:* the bottom two are **both E with inverted signatures** — the decisive test that the explanation layer attributes correctly (must say "nothing behind it" vs "unsafe dose," never confuse them).

## Why a separate engine (not BSIP2.1)
A supplement is a different object of analysis than a food. BSIP2 scores the nutritional
architecture of a matrix eaten for calories/macros (NOVA, matrix integrity, hyper-palatability,
fat/glycemic quality). A supplement is scored on: *does it deliver an evidence-backed active, at
an effective dose, in an absorbable form, honestly labeled, safely?* None of BSIP2's 10 dimensions
transfer; the unit of analysis is the **(active, dose, form, evidence) tuple**, not a per-100g panel.
"BSIP2.1" is rejected — it would invite shared constants / golden corpus / risk to the frozen food
invariants. Decision: **shared BSIP0/BSIP1 plumbing, forked scoring brain.**

Placement (sibling to BSIP2):
- `01_framework/supplement_framework/` — methodology, dimensions, grade semantics, scope
- `02_products/supplements/` — corpus (category-first)
- `03_operations/supplement_engine/proto_v0/` — own constants + scorer + dossier loader; `evidence_dossiers/`

## Scoring model — 5 dimensions
Grade answers **"is this worth taking, as sold?"**
1. **Evidence Strength** — credible evidence the active does what the product implies (Strong/Moderate/Weak/Insufficient; via `literature`).
2. **Dose Adequacy** — per-serving dose at/above clinically effective dose vs fairy-dusted/underdosed (`dsld` × literature).
3. **Form & Bioavailability** — absorbable form vs cheap/poor form (`pubchem` × evidence).
4. **Formulation Honesty** — proprietary blends hiding doses, claim-vs-substance gap, filler/additive burden.
5. **Safety Ceiling** — exceeds tolerable upper limit, risky/banned active, unjustified mega-dosing.

Reusable backbone = per-active **Evidence Dossier** (effective-dose range, evidence tier, best/worst
forms, upper limit, common label claims). Built once; every SKU with that active reuses it.

## MVP scope (owner directive 2026-06-03: prove the engine before expanding coverage)

**Minimal 5-active stress set** — fewest actives where every dimension has both a PASS and a FAIL anchor.
Each active leads one dimension; together they span the full evidence spectrum (Creatine doubles as the
Safety PASS control). 4 actives is below the floor (drops the botanical/standardization subsystem and the
proprietary-blend machinery — both load-bearing).

| Active | Lead dimension | PASS anchor | FAIL anchor |
|---|---|---|---|
| Creatine monohydrate | Dose Adequacy | 5 g monohydrate | 1 g creatine HCl sub-dose |
| Magnesium | Form & Bioavailability | glycinate / citrate | oxide as "high elemental Mg" |
| Vitamin D3 | Safety Ceiling | 1,000–2,000 IU D3 | 50,000 IU/day, or D2 |
| Caffeine | Formulation Honesty | labeled 200 mg | hidden in proprietary blend |
| Omega-3 (EPA/DHA) | Evidence Strength | EPA/DHA for triglyceride lowering (Strong) | same omega-3 for broad "brain & mood" claim (Weak/Insufficient) |

**MVP inputs:** 5 dossiers + a ~12-product golden corpus (the PASS/FAIL anchors, ~2–3 constructed SKUs
per active). Zero Israeli scrape required — engine is validated entirely on the live reference layer.

### Classification
- **MVP:** creatine · magnesium · vitamin D3 · caffeine · **omega-3 (EPA/DHA)**.
- **Phase 2 (harden + common shelf):** **ashwagandha + the botanical/standardization subsystem** *(deferred from MVP — belongs with the contested-evidence machinery it needs)*, iron *(necessity/contraindication — the angle MVP under-tests — + toxicity)*, zinc, B12 *(form depth)*, calcium, vitamin C, whey *(amino-spiking)*, melatonin *(~10× over-dosing)*, collagen, curcumin/turmeric.
- **Advanced (deferred — each needs machinery MVP lacks):** full pre-workouts / sports stacks *(blend-level dose attribution)*; probiotics *(CFU viability + strain-specificity + shelf-stability)*; greens/detox powders; mushroom/adaptogen/nootropic blends; hormone-adjacent & weight-loss *(safety + regulatory-risk handling)*.

## Sources (verified 2026-06-03)
Reference brain fully covered & live: `dsld` (actives + dose ranges, US-generic), `literature`
(PubMed/EuropePMC/OpenAlex/ClinicalTrials → evidence tier), `pubchem` (form identity), `il_gov_data`
(Israeli importer/legitimacy), `open_food_facts` (some barcodes). **One gap:** the Israeli supplement
*shelf* (BSIP0-S corpus) — supplements sell at Super-Pharm/iHerb-IL/pharmacies, not the food retailers
`il_prices` covers. Engine-first strategy de-risks this: scrape is Phase 3, nothing blocks on it.
EDPG firewall holds — DSLD/literature *calibrate* rules; the engine reads in-house labels only.

## Phases
- **Phase 0** — governance & scope doc (`supplement_framework/methodology_v1.md`); Nutrition + Product D7 co-sign. No code.
- **Phase 1** — 5 Evidence Dossiers (Nutrition + Research).
- **Phase 2** — engine prototype + 12-anchor golden-corpus validation. *(Proves the engine.)*
- **Phase 3** — Israeli corpus (BSIP0-S scrape) + QA freeze.
- **Phase 4** — frontend category page (separate verdict model from food comparison pages).

## Governance
Nutrition + Product D7 co-sign on scoring rules; new `SUPP-EV-###` evidence registry; EDPG firewall;
food invariants structurally untouchable (separate engine). `roadmap_impact: true` → CC close-gate applies.
