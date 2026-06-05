---
name: supplement-engine-sie-task171
description: "Supplement Intelligence Engine (SIE, TASK-171) — sibling-to-BSIP2 supplement scorer; MVP scope, 5-dimension model, Phase-0 methodology D7 co-signed"
metadata: 
  node_type: memory
  type: project
  originSessionId: 1720bf8b-87ff-4466-87b6-e6af36780d71
---

**SIE = Supplement Intelligence Engine (TASK-171)** — a NEW scoring engine for supplements,
**sibling to BSIP2, explicitly NOT "BSIP2.1."** Owner-initiated 2026-06-03. A supplement is a
different object than a food: the unit is the **(active, dose, form, evidence) tuple**, NOT a
per-100g panel — none of BSIP2's 10 food dimensions transfer. Decision: **shared BSIP0/BSIP1
acquisition plumbing, forked scoring brain.** Placement (sibling tree):
`01_framework/supplement_framework/`, `02_products/supplements/`,
`03_operations/supplement_engine/proto_v0/` (own constants, own grade thresholds, own golden
corpus, own `SUPP-EV-###` registry → frozen food invariants structurally untouchable).

**Score answers "is this worth taking, as sold?"** (claim-specific, not active-generic: same
creatine scores A for strength, Insufficient for "fat burning"). **5 dimensions:** Evidence
Strength (gate) · Dose Adequacy (gate; fairy-dust detection) · Form & Bioavailability (elemental-
vs-absorbed split) · Formulation Honesty (proprietary-blend hidden-dose cap) · Safety Ceiling
(UL veto). Combination = weighted blend + caps/floors/vetoes (BSIP2 shape). Grade letters S–E
**redefined for supplements** (E = "not worth taking as sold", NOT "unhealthy"). Reusable backbone
= per-active **Evidence Dossier** (YAML: effective_dose, form_ladder, UL, claim tiers, citations;
born `verification_status: candidate`).

**MVP = prove the engine before category coverage** (owner directive). Minimal **5-active stress
set** (the floor — each leads one dimension, every dim gets a PASS+FAIL pole): **creatine** (Dose +
Safety PASS control), **magnesium** (Form: oxide vs glycinate), **vitamin D3** (Safety: UL veto),
**caffeine** (Honesty: proprietary blend), **ashwagandha KSM-66** (Evidence: contested/botanical).
MVP inputs = 5 dossiers + ~12-product constructed golden corpus; **ZERO Israeli scrape** needed.
Classification: MVP(5) · Phase2(iron, zinc, B12, omega-3, calcium, vit C, whey, melatonin, collagen,
curcumin) · Advanced(pre-workout stacks, probiotics/CFU, greens, adaptogen blends, hormone/weight-loss).

**Sources verified 2026-06-03:** reference brain fully live — `dsld` (doses, US-generic), `literature`
(evidence tiers), `pubchem` (form identity), `il_gov_data` (Israeli importer legitimacy), OFF. **One
gap:** the Israeli supplement SHELF (BSIP0-S corpus) — supplements sell at Super-Pharm/iHerb-IL/
pharmacies, NOT the food retailers `il_prices` covers → deferred to Phase 3 (engine-first de-risks it).
**EDPG firewall holds:** external sources calibrate/justify rules (w/ SUPP-EV cite); engine reads
in-house labels + dossier only. Related: [[external_integration_layer_task170]], [[bsip2_evidence_registry_v1]].

**v1.1 amendment (2026-06-03, owner-approved, Product re-ratified):** (1) MVP Evidence probe
**swapped ashwagandha → omega-3 (EPA/DHA)** — ashwagandha's contested-botanical/standardization
difficulty IS the machinery MVP defers (incoherent probe); omega-3 isolates Evidence better (same
molecule/form, Strong-for-triglycerides / Weak-for-"brain&mood") + adds the "1,000mg fish oil hides
low EPA/DHA" Dose+Honesty trap; ashwagandha→Phase 2. (2) **Dossier maintenance, NOT scoring, named
the dominant operational risk** (stale dossier = silent misrank): added §5.1 lifecycle model (stable-
vs-drift fields, staleness DETECTION not auto-update, change-control, lean on NIH ODS/EFSA re-sync);
**Product owns a maintenance-cost go/no-go gate** before any scale-up.

**v1.2 amendment (Product re-ratified) + Phase 2:** added (a) **Dose short-circuit** (Evidence=Insufficient
→ Dose N/A, dropped from blend denominator, never positive credit off market prevalence); (b) **failure-
attribution explanation layer** — engine emits machine "why" = the BINDING CONSTRAINT (cap/veto that bound
the grade, or dominant-limiting-dimension if blend-bound), NOT lowest sub-score; structured trace; inherits
BSIP2 explanation discipline + No-Necessity firewall; machine-why=Phase2, Hebrew prose=Phase4; (c) golden-
corpus **attribution axis** = 3 failure archetypes. **Standing Safety meta-rule (FLAG-2, D7 co-signed):**
hard veto reserved for TOXICITY ceilings; reversible self-limiting tolerance (GI/osmotic, e.g. Mg EFSA-250)
→ graded Safety NOTE, not veto (veto rests on toxicity bound NIH-350) — supersedes prior "most-conservative-
governs-veto"; reversibility classification is dossier-level Nutrition-owned cited, engine never infers it.

**v1.3 claim-resolution amendment (TASK-171E, CLOSED — the most important design correction):** the Phase-3
real-data PoC exposed that the engine was scoring Evidence off **legally-coerced vague label wording, not the
substance** — a perfect magnesium (good form, honest, safe) scored E because its label said "supports bone
health" (the compliant default) instead of citing the BP trial. Fix (owner posture: **MODERATE / "fair but
skeptical"**): a vague structure/function claim **RESOLVES** to the active's cited studied endpoints via an
authored dossier **`structure_function_umbrella`** map (frozen exact key-lookup, NO NLP/inference on score
path); Evidence scores the best mapped tier; Insufficient→E ceiling fires ONLY when nothing maps (snake oil);
over-specific lies ("clinically proven to cure X") caught by §2.4 Honesty + resolve to the real (Weak) tier.
Magnesium umbrella authored from live literature: heart→BP=Moderate, bone/muscle→Weak, **nerve→does NOT map
(cited refusal — proves edges, not a loophole)**. Nutrition D6 + Product D7 co-signed; Data implemented (engine
0.2.0). **17/17 fixtures incl. 3 fairness fixtures (R1 vague-evidenced→B > R3 lie→D > R2 snake-oil→E); magnesium
PoC E/34→B/77.3.** Brand stance crystallized: **"punish over-promise, not compliance."** Still candidate;
SUPP-EV-006 should_affect_score_now flip + QA re-validation carried-forward before E→B is authoritative.

**Owner chose (2026-06-03) bounded widen to 15 + plumbing + real corpus.** Done & CLOSED: **171G acquisition
plumbing** (Super-Pharm catalog reader + iHerb panel-extract + barcode bridge in `integrations/clients/`;
live catalog read; bridge correctly rejects ships-to-IL-only US brands); **171H dossier expansion 5→15**
(+vit C, zinc, iron, calcium, folic acid, B12, melatonin, biotin, vit E, CoQ10; dropped collagen; DEFERRED
multivitamin+probiotics+B-complex to hard-gate; 16 dossiers load clean, golden 17/17, every umbrella populated
w/ cited refusals — biotin all-null→E, B12 nerve→Strong vs Mg nerve→null; **maintenance ~30–33 h/yr@15 VALIDATED**;
⚠️ first-pass had ~15 mis-PMIDs self-caught → needs a "PMID title-check" sweep step); **171F coverage analysis**
(15 actives ≈ 40–55% shelf, biggest sellers = hardest to score). **171D Step-2 addressable mapping (live, no
firecrawl):** 204 real SKUs sampled → **56.4% addressable** by the 15 actives (confirms estimate); BUT **THE
BINDING CONSTRAINT IS NOW THE LOCAL-BRAND PANEL GAP** — only **20% of addressable SKUs are global brands
(iHerb-panel-gettable); 80% are local-only (Altman/Life/SupHerb/Tink) with no iHerb panel → only ~11% of the
real shelf scoreable TODAY** without a Super-Pharm-PDP/brand-site/OCR panel-source build. creatine/CoQ10/melatonin=0
on the pharmacy shelf (sports/iHerb channel, keep them). Constraint is NOT the engine (excellent) or active
coverage (~56%) — it's **panel acquisition for the local-brand-dominated shelf.** Corpus run also gated on
**firecrawl scrape permission** (denied in build session).

**Thin live proof (171D Step 3, firecrawl LIVE):** global-brand SKUs scored end-to-end — **Solgar Omega→C/60.5**
(real barcode-matched iHerb panel; "Heart Healthy" resolved to the CONTESTED CV-events endpoint → engine refuses
a contested claim → C; calibration Q: should vague "heart healthy" pin to contested-CV or omega-3's Strong
triglyceride tier? → Nutrition D6), **Solgar Zinc→B/68.4.** Pipeline PROVEN on real Israeli SKUs. **BUT iHerb is
NOT a breadth source:** real yield was ~2–4 SKUs — the "~23 global-brand" was an importer-field over-count
(אמברוזיה/סולגר distributes BOTH global Solgar AND local SupHerb), and Israeli-pack barcodes differ from iHerb-US
(halves even genuine Solgar). **A real Israeli corpus REQUIRES a dedicated local-brand/local-pack panel source
(Super-Pharm PDPs / brand sites / OCR) — that build is the make-or-break for the category, NOT the engine.**

**MVP acquisition build + corpus MEASURED (TASK-171J, owner GO'd the 8–10d MVP; built il_supplement_panels.py +
il_panel_resolver.py, ran 118 addressable SKUs):** ⚠️ **MEASURED YIELD = 6.8% (8/118), NOT the projected
~31–37%** — local-brand e-tailer/brand-site sources resolve almost nothing at scale (probe's 75–85% was hand-
picked-optimistic). Engine scored every real product correctly: **Altman Vit D-1000→S/91.2 (clean win)**, Altman
Magnesium Balance 450mg oxide→E/20 (safety veto fires on real over-dose), Altman Biotin→E/34 (cosmetic Insuff),
TINC Mag Malate + SupHerb Mag Bisglycinate→E/34 (claim didn't map). **2nd finding: claim-umbrella vocab incomplete
for real HEBREW labels** — "עייפות/fatigue", "ספיגה/absorption" don't map though magnesium-fatigue is EFSA-authorized
→ unfair E → Nutrition D6 calibration task (expand each dossier's structure_function_umbrella to real Hebrew claim
vocab). Caveat: 6.8% is a floor (1st run, session-limit-cut, no tuning).

**FINAL — TASK-171 CLOSED 2026-06-03: engine PROVEN & BANKED as an asset; acquisition experiment CLOSED; NOT
launched** (owner directive: stop, no more engineering sprints). The engine is strong, self-explaining, cheap
(~30–33 h/yr), 15 actives, methodology v1.3, golden 17/17, validated on real Israeli SKUs — parked because the
Israeli shelf can't be acquired economically by **scraping** (measured ~6.8% reachable, 171J), NOT because the
engine fell short. Reviving = a **business-development question (manufacturer/importer data feed), not engineering.**
Owner-approved wind-down done: (1) **Hebrew claim-vocab fix** (171K — ~46 cited EFSA/Hebrew umbrella mappings;
+ a one-line tokenizer fix `[^a-z0-9֐-׿]+` so Hebrew survives tokenization; magnesium עייפות→Moderate verified,
golden 17/17 held); (2)+(3) **archived + experiment closed** → canonical record
`03_operations/supplement_engine/SIE_ASSET_AND_CLOSURE.md`. Carried-forward IF revived: manufacturer-feed BD path;
score-path-creating items (v1.3 claim-resolution live use, tokenizer change, the 3 first-authored umbrellas D3/
creatine/omega-3) need Product D7 + golden re-validation before any SHIP; all UL numbers NEEDS-ENV-VERIFY. All
candidate; nothing shipped; D10/D1 not made; separate tree; food invariants untouched. Sub-tasks 171A–171L all CLOSED.

**Phases:** 0 (✅171A) · 1 (✅171B) · 2 (✅171C) · **3 Israeli corpus (171D — plumbing✅171G + 15 actives✅171H +
catalog mapped + thin live proof✅; full corpus = owner business-case decision on the local-brand panel build)** · 4 frontend.
**Phase 3 probe answered "do we have the APIs?":** catalog/barcode (Super-Pharm price-transparency feed, LIVE no
login) + identity (il_gov_data imported_foods) + panel-extract (iHerb via firecrawl, 5/5) all reachable; the
missing piece is a **~2–3.5 day build (Super-Pharm reader + iHerb panel pipeline + barcode bridge), NOT an API**;
OFF supplement coverage 0/4. **5 real Israeli SKUs scored end-to-end** (`02_products/supplements/poc_real_skus/`):
creatine S, caffeine A, omega-3 D, magnesium B (post-v1.3), D3 E (5000IU>UL veto). **Two strategic findings:**
(1) real ceiling = engine ACTIVE-COVERAGE (5 dossiers; real shelf is mostly multivit/probiotic/herbal we can't
score), NOT acquisition; (2) the claim-as-worded problem (→ resolved by v1.3). **Business thesis still unproven**
(maintenance cost + coverage + launch D10/D1) even though scoring thesis is proven. Owner fork pending: build
5-active corpus / widen coverage / pause.
**Phase 2 done:** engine built at `03_operations/supplement_engine/proto_v0/src/` (constants/dossier_loader/
supplement_label/score_engine/trace_writer) + golden_corpus (11 §6 anchors + 3 archetypes) + run_golden_
validation.py + reports. Data built → Nutrition D8-VERIFIED (impl matches v1.2 spec, no deviations; fixed a
real bug: Safety now compares UL on same elemental+per-day basis) → Product D7 co-signed FLAG-2. **14/14
fixtures pass grade AND binding-constraint; inverted-E pair (no-evidence cap_1 vs dangerous veto_safety)
proven NEVER confused.** All numbers CALIBRATION-PENDING; nothing ships; separate tree (no BSIP2 imports).
Carried-forward (non-blockers): FLAG-3 safety-neutral blend value→SUPP-EV-006; primary UL numbers still
NEEDS-ENV-VERIFY before any value moves a published score.
**Phase 1 done:** Research built 5 dossiers (live pubchem/literature/dsld; 21 lit queries, 118 papers)
→ `03_operations/supplement_engine/proto_v0/evidence_dossiers/*.yaml` + `_build_cost_report.md` +
`evidence_registry/supp_evidence_registry_v1.md` (SUPP-EV-001–005). Nutrition D6/D7 co-signed all 12
claim tiers (creatine strength=Strong/fatloss=Insufficient; Mg BP=Moderate/sleep=Weak; D3 status=Strong/
bone=Moderate/broad=Weak; caffeine ergogenic=Strong/alert=Moderate; omega-3 TG=Strong/brain&mood=Weak/
**CV-events=contested→deferred**). **UL governance meta-rule:** veto at most-credible *tolerance/hazard*
threshold → Mg EFSA-250 governs, omega-3 EFSA-5g governs (FDA-3g = NOTE band only, it's GRAS not a
tolerance ceiling), caffeine 400/200-preg, D3 4000IU. omega-3 has a `conflation_firewall` (broad
brain/mood Weak does NOT inherit clinical-MDD evidence). All dossiers `candidate`/`should_affect_score_now:
false`; UL primary numbers still NEEDS-ENV-VERIFY. Build-cost = **conditional GO** for scale (authority-
leverage ≈0.375; dominant risk = silent staleness on a contested active, omega-3 = canary).
**D7 authorizes through Phase 1 only — supplement category go-live is a separate D10/D1, NOT decided.**
TASK-171 parent has `drift_ack` (umbrella; deliverables belong to closed sub-tasks).
Phase-0 doc: `01_framework/supplement_framework/methodology_v1.md` (has `## Invariants` block —
**SIE Invariant 1 No-Necessity Rule**: never scores/implies whether a person *needs* an active, keeps
Bari out of medical-advice territory). `roadmap_impact: true`.
