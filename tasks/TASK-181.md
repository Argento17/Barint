---
id: TASK-181
title: "Glass Box — Evidence-Aware Engine Evolution (program-of-record; continues TASK-179)"
owner: nutrition-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-06-04
depends_on: []
supersedes: TASK-179
blocks: []
category_id: null
roadmap_impact: true
work_type: objective
summary: >
  Glass Box program-of-record, promoted 2026-06-04 to succeed TASK-179 (CLOSED — W0–W2 delivered:
  six-dimension contract, D5/D6 transparency+confidence LIVE, W1.5 DIAAS signal, W2 additive prototype
  + panel LIVE on hummus/maadanim). This umbrella carries the program forward: W3 (current — scale the
  D4 additive library) · W4 (D3 de-moralization, spec ready) · W5 (publish methodology + NDA packet).
  Current wave W3 expands the D4 library from the 24-row prototype to the full shelf-frequent set,
  bulk-imports + curates EFSA/JECFA/FDA evaluations, tiers each additive, and stands up a
  maintenance-cadence protocol (the named dominant risk). ANNOTATE-ONLY: D4 does NOT enter the headline
  grade; OFF = byte-identical; score-integration is a separate future owner-gated decision
  (frozen-invariant tripwire). W3 children: 181A Research · 181B Nutrition tiers · 181C Product
  maintenance gate · 181D Data wire. W2 demand gate was bypassed by owner override (see Provenance).
---

# TASK-181 — Glass Box: Evidence-Aware Engine Evolution (program-of-record)

**Promoted to program-of-record 2026-06-04**, continuing **TASK-179** (CLOSED — W0–W2 delivered).
TASK-179's A–Z sub-letters were exhausted; this umbrella succeeds it and carries the remaining waves.
Origin, six-dimension contract, and W0–W2 delivery history live in TASK-179 + `01_framework/glass_box/`.

## Wave status
- **W0–W2 — DELIVERED** (under TASK-179, CLOSED): six-dimension contract (`six_dimension_contract_v1.md`,
  DEC-006) · D5 transparency + D6 confidence LIVE (`BARI_GLASSBOX_D5D6`) · W1.5 DIAAS signal
  (`BARI_GLASSBOX_W15`) · W2 additive prototype (20 dossiers) + AdditivePanel LIVE on hummus + maadanim.
- **W3 — CURRENT (this umbrella):** scale the D4 additive library — 181A/B/C/D below.
- **W4 — READY:** D3 de-moralization. Spec complete + Product D7 co-signed (`d3_demoralization_spec_v1.md`,
  authored under TASK-179Z); draft EV-042 pending filing at W4 open. Opens on owner go.
- **W5 — BACKLOG:** publish public methodology page + NDA materials packet + consumer additive UI polish.

## Provenance — the W2 demand gate was bypassed
W3 was designed (per TASK-179 umbrella + `glass_box_engine_program_task179` memory) as the
**expensive, maintenance-heavy bet, gated on proven consumer demand**. The W2 engagement gate
(`TASK-179X`) was **closed by owner override on 2026-06-04 without engagement data** — no moderated
sessions were run, none of the three thresholds (5/8 unprompted opens · 8/12 comprehension · 20%
live panel-open rate) were measured. W3 therefore proceeds on **owner product judgment, not measured
engagement**. This is recorded so the decision to scale carries its full context.

## Scope (annotate-only)
1. **Expand the D4 library** from the 24-row prototype (`additive_prototype_set_v1.md`) to the full
   set of additives observed on the displayed Israeli shelves. **Classify shelf-present additives,
   not the full E-number space** (standing guardrail).
2. **Wire evidence sources** — bulk-import + curate EFSA OpenFoodTox, JECFA, FDA additive evaluations
   (import-and-curate, not live-per-product).
3. **Tier** each additive on the 6-tier evidence model; file evidence-registry entries.
4. **Maintenance-cadence protocol** + Product go/no-go gate — the program's **named dominant risk**.

## Hard boundary — no score movement in W3
D4 **does not enter the headline grade** in W3. This stays **annotate-only / candidate**: OFF =
byte-identical; published `score`/`grade`/`gate`/`glassBox` fields are untouched. Letting additives
move the grade is a **separate, future, owner-gated decision** (frozen-invariant tripwire #1 — it
re-scores every pilot category and needs explicit owner sign-off). Do not fold score-integration
into this wave.

## Sub-tasks
- **TASK-181A** (Research, **CLOSED 2026-06-04**) — `additive_library_expanded_v1.md`: 36 additives (20 carried + 16 new), EFSA/JECFA/FDA evidence, 9 EVIDENCE-GAPs, no tiers. Flagged: displayed bread shelf has 0 additives; EFSA/JECFA numeric-ADI wiring gap → 181C.
- **TASK-181B** (Nutrition, **CLOSED 2026-06-04**) — `additive_tiered_library_v1.md` + EV-043: 36 additives tiered 19/7/5/3/1/0/1. Product D7 CO-SIGNED. Annotate-only.
- **TASK-181C** (Product, **CLOSED 2026-06-04**) — `additive_library_maintenance_protocol_v1.md`: cadence + go/no-go FREEZE gate + demand-revisit checkpoint; EFSA-import DEFERred; carried the 181B co-sign.
- **TASK-181D** (Data, **CLOSED 2026-06-04**) — detector 20→35 keys (36 additives); pilot JSONs regenerated (hummus 56/64 · maadanim 74/84 · bread 17/24); OFF 0-diff + 0 score/grade deltas; matcher digit-boundary guard added (no-invent).
- **TASK-181E** (Content, **CLOSED 2026-06-04**) — 14/14 Hebrew `explanation_he` authored (w2_additive_copy_v1.md W3 addendum) + CC re-wired all 14 into the pilot JSONs (+94 explanation_he filled; OFF 0-diff; 0 score-delta).

## W3 status — COMPLETE 2026-06-04
All five sub-tasks CLOSED: 181A (Research library) · 181B (Nutrition tiers) · 181C (Product maintenance) · 181D (Data wire) · 181E (Hebrew copy + re-wire). The full 36-additive D4 library is tiered, evidence-registered (EV-043), Hebrew-copied, and wired live (annotate-only, behind `BARI_GLASSBOX_W2`, OFF byte-identical, no grade movement).

## W4 — D3 de-moralization (OPENED 2026-06-04)
Reframe D3 from a deterministic NOVA-class→penalty mapping to a probabilistic, confidence-scaled
population-level signal. Spec = `d3_demoralization_spec_v1.md` (TASK-179Z; Section 3 consumer
framing Product-co-signed). **Unlike W3, W4 MOVES THE GRADE when ON** — so the build ships behind
`BARI_GLASSBOX_W4` (OFF = byte-identical), and the **flag-flip to ON is a SEPARATE frozen-invariant
owner gate (tripwire #1)**; these tasks build it OFF-identical + produce the score-impact analysis
for that owner decision. They do not flip it live.
- **TASK-181F** (Nutrition, **CLOSED 2026-06-04**) — **EV-042 filed** (registry L982–1003) binding confidence criteria (§2.3), confidence_scale 1.0/0.70/0.40 (§2.5), population_correlation 0.05/0.15/0.40/0.75 (§2.4); **both D7 co-signs complete** (Nutrition + Product). Rule adopted on paper, behind the flag, OFF.
- **TASK-181G** (Data, **CLOSED 2026-06-04**) — D3 reframe built behind `BARI_GLASSBOX_W4` (default OFF). OFF byte-identity verified 0-diff (342 products); engine-only change, frozen tables + published data untouched; built to EV-042. 4 build decisions routed to 181H.
- **TASK-181H** (QA, **RETURNED — CC gate PASS, with a MATERIAL FINDING**) — OFF 0-diff re-verified; frozen invariants HOLD when ON (milk 85/A, snack 70/B). **Finding: W4-ON is net-downward — 17 grade moves DOWN vs 3 UP** (the co-signed pull-to-neutral lowers NOVA-1/2/3 above-neutral scores; "less punitive" only holds for NOVA-4). 2 unbound magnitudes (D6 deduction=10, cap-scaling) need Nutrition sign-off. **Decision-relevant for go-live — held pending owner direction.**
- **TASK-181I** (Frontend/Design, **RETURNED — CC gate PASS — CLOSEABLE, held**) — D3 signal surfaced as a calm drilldown line behind `NEXT_PUBLIC_GLASSBOX_W4` (default OFF); OFF visually unchanged (10/10 smoke); build/lint/tsc clean; preview at `/dev/glass-box-preview`. Independent of the 181H finding.

## W4 status — BUILD COMPLETE, GO-LIVE BLOCKED (expert review done 2026-06-04)
181F (rule/EV-042) + 181G (engine) CLOSED; 181H (QA) + 181I (display) deliverables verified (RETURNED, held). Capability built, safe OFF. 181H finding: W4-ON is net-downward (17 grade moves down / 3 up).

**Nutrition + Product reviewed the finding (owner request 2026-06-04) — they AGREE:**
- The rule's behaviour is **correct, keep it** — uncertainty must pull toward neutral in BOTH directions (softens unverifiable harsh scores AND trims unverifiable good scores); narrowing to "only soften penalties" would re-introduce the over-confidence the reframe exists to remove. The downward pull is principled *because* confidence is keyed to label/evidence quality, not to the processing class.
- The real defect is the **"less punitive" wording** — true only for NOVA-4; on a high-side shelf it's net-downward. Reword EV-042 to "pull-to-neutral in both directions — less *confident*, not less *punitive*" (cheap, reversible doc edit).
- **2 unbound magnitudes need Nutrition sign-off before any flip:** (a) D6 low-confidence deduction = 10 pts, but Nutrition says apply to the LOW band ONLY (medium already pays via the 0.70 scale — else double-count); (b) the Data-derived cap-scaling formula must be written out + EV-042-signed, not relied on as a default.
- **Product recommends: ship ON, but staged (pilot hummus/maadanim first) + a visible dated consumer methodology note (Content authors), AFTER the reword. No silent flip; don't park (wastes a cheap, integrity-positive capability); don't split the engine across categories.** The 179X demand debt doesn't really apply to D3 (it's a formula, ~no maintenance) — it keeps blocking the additive-library scale-out, not this.

**The flag-flip itself remains the owner's call (tripwire #1).** Prep before flip = reword EV-042 + Nutrition signs the 2 magnitudes (all reversible, nothing live).

### Medium-band challenge (owner, 2026-06-04) — Nutrition + Product reviewed; both CONCEDE the owner is right
Owner accepted LOW-band shrinkage as valid; challenged the MEDIUM band as too aggressive (medium scale 0.70). Decisive fact: **all 20 grade moves are medium-band; the low band crossed ZERO grade lines** — so the entire net-downward shelf effect is the medium band.
- **Nutrition (concede):** 0.70 overreaches — it taxes the resolved 90% of a legible label for an unresolved 10%, re-introducing a processing penalty via the back door (collides with G-002). Refinement — **the current "medium" band is doing two jobs and should be split:** (1) **critical-path medium** (the unknown could flip the processing verdict — unnamed emulsifier/stabilizer that decides processed-vs-ultra, or D5 `severe`, or large unresolved fraction) → drops to LOW, moves the score (0.40) — the owner-accepted case; (2) **peripheral-gap medium** (visible signals already pin the read; one fuzzy term like "spices") → stays medium, **soften 0.70→~0.90 (nudge not haircut), route the doubt to D6/confidence**. Honors Bari's "unknown reduces confidence first, not quality first." Strong on direction; magnitudes (0.90, D6 size) are calibration vs the shelf distribution.
- **Product (concede):** the medium grade movement isn't worth it — a small local doubt expressed as a full B→C drop is an "unexplained markdown"; the honest signal belongs on the confidence axis at its true (quiet) volume. Softening medium dissolves the entire net-downward optics, keeps the honest low-end behavior, and makes go-live *easier* (the consumer methodology note drops from mandatory to optional). Reserving real movement for the low band is quiet-in-practice, not timid-in-principle (low band will move grades on a genuinely opaque future shelf).

**Convergence:** soften/ split the medium band so peripheral-gap products barely move on quality (doubt → D6), reserve real score+grade movement for critical-path/low. Implementing = a scoring-rule change → **revised/superseding EV-042 + both D7 co-signs (Nutrition + Product)** + Data re-derivation; flag stays OFF, trips no tripwire.

### W4 REWORK — owner ADOPTED 2026-06-04
Owner directive: split medium-certainty into **MATERIAL uncertainty** (the unknown could change the processing read → may shrink the score, low-band treatment) vs **NON-MATERIAL uncertainty** (visible signals already pin the read → affects **confidence/D6 ONLY**, the score does not move). Rework chain opened:
- **TASK-181J** (Nutrition, **CLOSED 2026-06-04**) — revised EV-042 in place: material/non-material test (M1–M4), medium-material 0.70 / medium-non-material 1.0 (no D3 move), D6 routing (−5 / −10, max-combined), bound cap-scaling, "less punitive" retired. **Both D7 co-signs in** (Nutrition + Product). Baseline preserved.
- **TASK-181K** (Data, **CLOSED 2026-06-04**) — split re-implemented behind `BARI_GLASSBOX_W4`, OFF byte-identical (0-diff 342); ON smoke confirms medium-non-material no longer moves D3 (hummus 3/3 + maadanim 25/25 now zero D3 movement). 3 impl details flagged for 181L.
- **TASK-181L** (QA, **RETURNED — CC gate PASS, with 3 findings**) — OFF safety re-verified independently (0-diff); frozen invariants hold. **Before/after: 17-down/3-up → 17-down/0-up — NOT flat.** The rework worked at the D3 layer (non-material → 0 D3 move) but the 17 downgrades survive because they were never D3-driven. **F1:** materiality degenerate (0/342 material when D5D6 OFF — the split is inert offline). **F2 (the real driver):** the HP NOVA-weight de-amplification (separate co-signed mechanism) is what moves the shelf — NOVA-3 now takes full hyper-palatability penalty (×0.5→×1.0). **F3:** the −5 dent flips 3 products to insufficient_data at the confidence boundary.

**W4 status — rework landed but did NOT flatten the shelf; the real lever is elsewhere.** Closed: 181F·181G·181H·181I·181J·181K. 181L returned with the finding that the downgrades come from the HP de-amplification, not the medium-band uncertainty rule we reworked.

### Owner decision 2026-06-04 — KEEP the HP de-amplification (F2), pressure-test it first
Owner decided to **KEEP** the HP NOVA-weight de-amplification (accept the ~17 downgrades as honest — the foods genuinely carry the fat+salt/fat+sugar combos; W4 stops discounting that penalty by processing class). Owner asked to **pressure-test the keep decision** with Nutrition + Product before it's locked.

**Pressure-test result (2026-06-04) — BOTH CONFIRM KEEP, both land on the SAME one required pre-flip fix:**
- **Nutrition (confirm-keep):** full-magnitude HP is the *more* defensible state — it stops discounting a **directly-observed** fat+salt/fat+sugar combo by NOVA class (a proxy that merely predicted it = "invented certainty" via the back door). Went looking for the counter (NOVA-3 fat may be "structural" in whole foods) and resolved it: that's a **matrix** question → use the matrix/whole-food lever per-category on evidence, NOT a blanket NOVA-keyed HP discount. No new double-count (D3 doesn't move for these products; HP gates on macros, not NOVA). Watch-item (log, don't fix): HP-full-magnitude × the untouched NOVA-reading WFI dimension — revisit when WFI gets its own de-moralization (§4.2).
- **Product (confirm-keep):** cleaner shopper story than the uncertainty one — *"this hummus is fat+salt heavy; we stopped discounting that for processed-but-natural-looking foods"* = anti-health-halo = integrity. Same staged + dated-note plan; reframe the note from confidence-hedge to principle; name the driving combo on affected rows so no drop looks arbitrary.
- **REQUIRED PRE-FLIP FIX (both, independently) — F3:** a non-material −5 confidence dent must NOT be the term that flips a scored product into `insufficient_data` (it currently does, for 3 maadanim — breaches the "confidence dent, never a grade cut" co-sign basis). Fix = **guard the gate** (keep the −5 magnitude — it's correctly anchored at half the D5 partial −10; fix the boundary so the dent reduces displayed confidence within the graded band but can't cross the data-sufficiency label). Data implements; Nutrition + Product D7 co-sign the guard.
- **F1 (log/fix, not a go-live blocker for this decision):** materiality split is inert when D5D6 OFF (0/342 material) — make D5D6 a hard precondition or build an offline token resolver so the medium-material path isn't dead code.

**Net: KEEP confirmed by both. One required fix (F3 gate-guard) before any flip; F1 a correctness cleanup. Then go-live (staged + note) is the separate owner tripwire-1 call.** Flag still OFF.

### Owner: methodology findings ACCEPTED; W4 GO authorized (conditional) 2026-06-04
Owner accepted the pressure-test findings (KEEP HP de-amplification confirmed). Opened **TASK-181M** — "Prevent non-material confidence dents from independently triggering insufficient_data" (the F3 gate-guard, Data; keep the −5, fix the boundary; re-validate). **Owner GO for W4 go-live is authorized CONDITIONAL on 181M landing + re-validation passing.** Scope kept to the one F3 task per owner; F1 stays a logged correctness item (not in this task). At the GO checkpoint (after 181M passes), CC executes the flag-flip per owner authorization — confirming with the owner the methodology-note + staging (Product's "no silent flip" condition) since the flip is consumer-facing/irreversible.

**TASK-181M CLOSED 2026-06-04 (CC gate PASS).** F3 boundary clamp landed + re-validated: 3 maadanim back to graded D, exactly 3 rescues / 0 other diffs, genuine data-poor still reach insufficient_data, OFF 0-diff, frozen invariants hold. **All owner go-live conditions are now MET.** At the GO checkpoint — the only open item is Product's "no silent flip" condition (a dated methodology note shipping with the flip). The flag-flip moves real grades on the live pilot shelf (hummus + maadanim; ~17 honest downgrades) = consumer-facing/irreversible = owner's tripwire-1 call, already authorized; CC confirms the note decision with the owner, then executes.
Flag stays OFF throughout; live flip remains a separate owner go-live decision. 181F/181G/181H/181I outputs stand; this revises the medium-band behaviour they were built on.
- **TASK-181H** (QA, BLOCKED on 181G) — OFF byte-identity (0-diff golden/frozen) + the ON score-impact analysis for the owner go-live decision; confirm frozen invariants don't breach.
- **TASK-181I** (Frontend/Design, BLOCKED on 181G) — surface d3_processing_signal + note_he on the professional/consumer surface (view-model); behind the flag, no live exposure pre-go-live.

**W4 end condition:** 181F–181I CLOSED → W4 build done + OFF-identical + score-impact analysis in hand. The **live grade move is a separate owner go-live decision** (like W1's flag flip). Then W5 (publish methodology + NDA + UI polish) is the last wave.

## W3 end condition
W3 closes when 181A–181D are all CLOSED and the maintenance protocol (181C) is signed. Score-integration,
if pursued, opens as a separate owner-gated task — not part of W3.

## Guardrails
Every tier cites an evidence-registry entry (`bari-bsip2-scoring-governance`). Nutrition + Product
co-sign tiers. OFF byte-identity proven by QA. `roadmap_impact: true` → CC close-gate applies.
Frozen invariants (milk run_005_headpin / snack 70/B / bread provenance) untouched. Nothing ships without owner go.
