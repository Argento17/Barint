# Bari Strategic Objectives — Validation & Approved Roadmap v1

**Task:** TASK-126 (Command Center / Central Controller)
**Type:** Strategic validation + roadmap. Recommendation pending Controller acceptance.
**Date:** 2026-06-01
**North star (from brief):** highest-value path to **Bari launch**.

> **Status of this document:** This is the Command Center's *recommended* objective
> structure. It becomes the **approved** roadmap only when the Central Controller
> accepts TASK-126. Until then the five proposed objectives remain unratified.

> **v1.1 (2026-06-01) — Controller feedback incorporated.** Direction approved.
> O5 removal, P1/P2/P3 structure ratified. Two changes from feedback: (a) **Wave 2
> challenge accepted** — the flat 4→2 reduction is withdrawn and replaced with an
> instrumented, gated target of **4** (see §2 O4 and §8); (b) **Launch Definition v1**
> proposed (`launch_definition_v1.md`) and a **registry structure** for P1–P5 added (§9).

---

## 0. Inputs consulted (authoritative)

- Registry `C:\Bari\tasks\` — 52 tasks; dashboard clean (0 drift) after TASK-125 remediation.
- **DEC-002** — Hummus v1 `GO_LIVE_APPROVED`, recorded LIVE 2026-05-31 (`hummus_v1_release_summary_v1.md`).
- **TASK-098** — accepted Comparison v2 direction; **TASK-118** — v2 implementation roadmap; **TASK-111** — data readiness `READY_WITH_MODIFICATIONS`; **TASK-123** — v2 sign-off package.
- `category_scaling_readiness_v1.md` — operating-model scaling verdict (the Wave-2 blocker).
- Dashboard category states (generate_dashboard.py, 2026-06-01):

| Category | bsip2 | dataset | website | launch |
|---|---|---|---|---|
| maadanim | AUTHORITATIVE | DEPLOYED | LIVE | LIVE *(frozen v1 reference)* |
| hummus | AUTHORITATIVE | DEPLOYED | LIVE | LIVE *(DEC-002; chosen v2 pilot)* |
| snacks | AUTHORITATIVE | DEPLOYED | LIVE | LIVE |
| yogurts | AUTHORITATIVE | DEPLOYED | LIVE | LIVE |
| bread | AUTHORITATIVE | DEPLOYED | LIVE | LIVE *(reasoning-field gaps noted)* |
| milk | AUTHORITATIVE | DEPLOYED | **LEGACY (gen0)** | LIVE |
| breakfast-cereals | NOT_STARTED | NOT_BUILT | NOT_STARTED | **QUEUED** |
| tahini | NOT_STARTED | NOT_BUILT | NOT_STARTED | NOT_STARTED |

---

## 1. Executive recommendation

**The five proposed objectives are directionally right but mis-framed, mis-sequenced, and double-counted. Two are partly already done, one is missing entirely, and the riskiest one is scheduled too early.** Adopting them as-written would put a scoring re-calibration, a new presentation layer, a content push, and four new categories all in flight at once — maximizing rework and QA-baseline churn at precisely the moment the operating model is already showing drift (TASK-125 just remediated 18 phantom tasks).

Concretely:

- **Objective 1 ("Comparison Platform V1")** is the right center of gravity but **wrongly labelled**. V1 is the *frozen* shelf; the org has already DECIDED to move to **v2** (TASK-098). Re-name and re-scope it to **v2 completion of the existing fleet** — that is the single highest-value path to a credible launch.
- **Objective 5 ("Hummus Production Verdict")** is **largely redundant** — hummus v1 is already `GO_LIVE_APPROVED` (DEC-002) and LIVE. The only live question is the **v2-pilot exit verdict**, which belongs inside Objective 1, not as a standalone objective.
- **Objective 2 ("BSIP0–BSIP2 Evolution")** is **too broad and dangerous to run whole during launch**. Split it: keep the launch-gating **calibration + confidence** slice; **defer BSIP2 next-gen** to post-launch.
- **Objective 4 ("Comparison Wave 2")** is the **riskiest and is sequenced too early**. `category_scaling_readiness_v1` explicitly rules the operating model **NOT ready for Category #5** until hardening lands. Gate Wave 2 behind that.
- **Objective 3 ("Intelligence Articles")** is valid but **strictly downstream** of 1+2 (articles consume publication-ready, score-frozen corpora). Sequence it after the first pilot category is frozen; prove with one article before committing to three.
- **Missing objective (must add):** **Operating-Model Hardening** — automated corpus validation, a category-module contract, route/status governance, and a deprecation policy. It is the prerequisite for Wave 2 and is currently nobody's objective. *Justification for a new workstream:* it is already specified by `category_scaling_readiness_v1`; we are naming existing required work, not inventing scope.

**Bottom line:** ship v2 across what we already have, freeze scores per category as we go, harden the factory, *then* expand. Launch on depth and credibility, not on category count.

---

## 2. Per-objective verdict

### Objective 1 — "Comparison Platform V1" → **REFRAME + KEEP (P1)**
**Verdict:** Re-name to **"Comparison Platform v2 Completion (existing fleet)."**
- "Complete all existing categories to a consumer- and publication-ready standard" is right, but five categories are already LIVE and the accepted forward standard is **v2**, not V1. As written the objective conflates "finish V1" with "ship v2."
- It also silently owns the hard process gate (author + sign `comparison_ui_reference_v2.md`) and the QA re-baseline — surface those as explicit prerequisite milestones, not buried blockers.
- Absorbs the live remnant of Objective 5 (the v2-pilot exit verdict on hummus).
- **Split note:** `base_pct` (3rd metric bar) is externally blocked on a data pipeline (TASK-111); keep it carved out to Phase 3 so it never gates launch.

### Objective 2 — "BSIP0–BSIP2 Evolution" → **SPLIT (P2 launch slice + deferred next-gen)**
**Verdict:** One objective spanning ingest (BSIP0), production scoring (BSIP1), and next-gen scoring (BSIP2) is too broad and competes with O1 for the same QA/reviewer capacity.
- **Keep (P2):** the **calibration + confidence** slice that is *already* on the launch critical path — the hummus confidence accuracy re-audit (a v2 Phase-0 blocker) plus calibration of observed weaknesses. **Freeze scores per launch category once calibrated.**
- **Defer (post-launch):** BSIP2 next-gen evolution and "future-category readiness." It already has its own roadmaps (`bsip2-improvement-roadmap-v1`, `bsip2_upgrade_roadmap_v1`); running it during launch invalidates QA baselines and any published explanations/articles mid-flight.

### Objective 3 — "Intelligence Articles" → **KEEP, RESEQUENCE (P4)**
**Verdict:** Valid distribution/credibility play (precedent exists: the milk-analysis article + `comparison-intelligence-hero`). But articles are downstream artifacts of publication-ready, score-frozen corpora.
- Do **not** commit to 3 up front. **Pilot one** article off the first v2-complete, score-frozen category (hummus or maadanim) to prove the corpus→article pipeline, then scale to 3.
- Hard dependency: only build on categories that have passed O2's score-freeze, or articles will need re-issuing when scores move.

### Objective 4 — "Comparison Wave 2 (4 families; cereals first)" → **DEFER + GATE (P5); target stays 4**
**Verdict (revised per Controller challenge):** the flat 4→2 reduction is **withdrawn**. The validation objective of Wave 2 is to prove Bari can **repeatably execute the full category pipeline** — the *number* is not the objective, the **invariance of marginal cost** is. Keep the **target at 4**, executed as an **instrumented, gated cohort** (see §8 for the full rationale and gate). Still defer behind O1 (v2 reference signed) and P3 (hardening), because committing 4-wide before the hardened pipeline is proven would scale a bespoke effort rather than amortize it.
- `category_scaling_readiness_v1`: the operating model is **NOT ready for Category #5** until automated corpus validation, a category-module contract, route/status governance, and a deprecation policy exist.
- Partially pre-staged already: **breakfast-cereals is QUEUED** and **tahini NOT_STARTED** in the dashboard — not net-new discovery.
- **Structure:** Cat 1 (cereals) = instrumented reference run on the hardened pipeline → Cat 2 (tahini) → **gate G-W2A** (re-execution confirmed) → Cats 3 & 4. **Repeatability is formally "proven" at completion of Cat 3** (trend across 3 points); **Cat 4 confirms throughput.**

### Objective 5 — "Hummus Production Verdict" → **REMOVE (fold into O1)**
**Verdict:** Redundant as written. Hummus v1 is already `GO_LIVE_APPROVED` (DEC-002, 2026-05-31), recorded LIVE, all launch-gating tasks (TASK-086/087A–C/089/090) CLOSED. Carrying a closed decision as an open objective re-litigates settled work.
- The **only** still-live verdict is hummus's readiness as the **v2 pilot** and the pilot **exit gate** — that lives inside O1.

---

## 3. Overlaps & redundancies (resolve before approval)

| Overlap | Resolution |
|---|---|
| O5 (hummus verdict) vs **DEC-002** (already decided + LIVE) | Remove O5; keep only the v2-pilot exit gate inside O1. |
| O1 "V1" framing vs **accepted v2 direction** (TASK-098) | Re-label O1 to v2 completion; V1 is frozen, not a forward objective. |
| O1 "publication-ready" vs O3 (articles) | Sequence: O3 *consumes* O1's publication-ready output. Not parallel. |
| O2 confidence re-audit vs O1 Phase-0 blocker (#6) | **Same piece of work claimed twice.** Assign once to O2's calibration slice; O1 consumes it. |
| O4 cereals vs dashboard (cereals already QUEUED, tahini staged) | Wave 2 is partly pre-staged; treat as gated expansion, not discovery. |

---

## 4. Approved objective roadmap (recommended)

> Prerequisite milestone (inside O1, blocks all v2 work): **author + sign `comparison_ui_reference_v2.md`; QA re-baseline at mobile + `lg`; hummus confidence re-audit.**

| # | Objective | Action | Owner (proposed) | Gated by |
|---|---|---|---|---|
| **P1** | **Comparison Platform v2 Completion (existing fleet)** | Reframe of O1 | frontend-agent (+ design/product sign-off) | v2 reference sign-off; QA re-baseline |
| **P2** | **BSIP Calibration & Confidence (launch slice)** | Split from O2; **freeze scores per launch category** | nutrition-agent / data-agent | — (feeds P1) |
| **P3** | **Operating-Model Hardening** | **NEW** (specified by scaling-readiness audit) | data-agent / qa-agent | — (gate for P5) |
| **P4** | **Bari Intelligence Articles** | Keep O3; pilot 1 → scale to 3 | content-agent | P1 + P2 (score-frozen category) |
| **P5** | **Comparison Wave 2 (target 4, gated cohort)** | Defer O4; instrumented 1→2→gate→3→4 | frontend + data | P1 (v2 ref) + P3 (hardening) |
| **Deferred** | **BSIP2 Next-Gen Evolution & future-category readiness** | Split from O2 | (post-launch) | after launch |

### Recommended sequencing (one screen)

```
PREREQ   author+sign comparison_ui_reference_v2.md · QA re-baseline · hummus confidence re-audit
            │
P1  ───────┴─ v2 completion: pilot HUMMUS → maadanim → snacks → yogurts → bread → milk(gen0→gen1→v2)
P2  ───────── BSIP calibration+confidence  →  FREEZE scores per category as P1 lands each one
                                              │
P4                                            └─ Intelligence Articles: 1 pilot article → scale to 3
P3  ───────── Operating-Model Hardening (parallel infra track)
                                              │
P5                                            └─ Wave 2 (target 4): cereals → tahini → [gate] → 3 → 4; after P1 ref + P3
Deferred ─── BSIP2 next-gen evolution (post-launch)
```

---

## 5. Success criteria (exit gates)

**P1 — v2 completion**
- `comparison_ui_reference_v2.md` authored and signed; fresh QA baselines at mobile + `lg`.
- All 5 gen1 categories render the v2 reference (density, metric block protein+additives, rowReason, restructured expansion, responsive table); milk migrated gen0→gen1→v2.
- Null rule holds (`"—"`, never `0`); corpus order preserved under every control; no product removed from the DOM.
- Hummus v2-pilot exit criteria (per TASK-118 §5) all pass.

**P2 — BSIP calibration & confidence**
- Confidence accuracy gate passing (`verified` only when ≥3/6 nutrition fields **and** ingredients present) on each launch category.
- Documented calibration of the observed weaknesses; golden-product suite green.
- **Per-category score freeze recorded** before that category feeds P4/launch.

**P3 — Operating-model hardening**
- A single `validate-corpus` command in `package.json` enforcing v2 field-completeness (incl. bread's missing `limitingFactors`); CI-or-convention gate documented.
- Category-module contract (one self-contained module per category); deprecation policy for old generators; clean committed baseline for production comparison assets; route/status governance explicit.

**P4 — Intelligence articles**
- 1 pilot article shipped from a score-frozen category, traceable to corpus; then 3 flagship articles total, each citing frozen scores + methodology, no algorithm exposure.

**P5 — Wave 2 (target 4, gated)**
- All families born directly on the signed v2 reference and passing P3's `validate-corpus`; LIVE with no regression.
- **Repeatability instrumented** per category: marginal effort (hours/elapsed), defect-escape rate (caught by `validate-corpus` vs. found late), contract-deviation count, rework cycles.
- **Gate G-W2A** (after Cat 2): marginal cost ≤ Cat 1, zero novel firefights, defects caught pre-launch → release Cats 3–4.
- **"Repeatability proven" milestone = completion of Cat 3** (cost trend established); **Cat 4 = throughput confirmed.**

---

## 6. Risks & dependencies

1. **Concurrency / rework (highest):** calibrating scores while migrating presentation and publishing articles invalidates QA baselines and published content mid-flight. **Mitigation:** per-category score-freeze (P2) before P1 finalizes that category and before any P4 article uses it.
2. **Hard process gate:** no v2 code ships on frozen v1 without a signed `comparison_ui_reference_v2.md` (TASK-118). Blocks all of P1+.
3. **External data blocker:** `base_pct` main-ingredient pipeline isn't built (TASK-111, Data Agent). Kept out of the launch path (Phase 3) so it cannot gate launch.
4. **Operating-model drift:** manual QA, doc/count drift (snacks lineage audit; hummus N1 hardcoded `"69"/"59"` copy constants), and registry drift under load (TASK-125 remediated 18 phantoms). **Mitigation:** P3 before P5.
5. **Capacity contention + acceptance bandwidth:** five parallel objectives exceed the dashboard's `task_capacity: 3` and the single Central-Controller acceptance lane. The sequencing above keeps ≤2–3 objectives hot at once.
6. **Launch definition gap:** the brief's north star is "launch," but no objective defines what launch *is* (public GTM / hub / SEO — `04_growth/growth_strategy_v1.md`, `generate_seo.py` exist). **Recommendation:** the Controller ratifies a launch definition so P-level success criteria trace to it; otherwise "launch-ready" stays subjective.

---

## 7. Decision requested of the Central Controller

Accept TASK-126 to ratify: (a) reframe O1 → v2 completion; (b) split O2 (keep calibration, defer BSIP2); (c) keep+resequence O3; (d) defer O4, **target 4 as a gated cohort** (§8); (e) remove O5 (fold into O1); (f) **add P3 Operating-Model Hardening**; (g) **Launch Definition v1** (`launch_definition_v1.md`, recommend DEC-003); and (h) the P1–P5 sequence and success criteria above. On acceptance this document is the authoritative Bari objective roadmap and each P-objective is opened per §9 (`new_task.py`).

---

## 8. Wave 2 — response to the Controller's challenge

**Direct answer up front: the challenge is correct and the flat 4→2 reduction is withdrawn. The target stays 4.** Below, the three questions answered honestly.

### 8.1 Was the recommendation strategic or capacity-driven?
**Capacity/sequencing-driven, and I mis-expressed it as final scope.** The legitimate concern was *commitment timing* — committing to 4 categories before the hardened pipeline (P3) is proven risks running a bespoke effort four times instead of proving a repeatable process. That is an argument for **gating**, not for a smaller target. Conflating "how many we commit to up front" with "how many we run before re-checking" was the error. The strategic objective you state — *prove repeatable execution of the full pipeline* — actually argues **for** 4, not against it.

### 8.2 What validation objective is satisfied with 2 but not 4?
Treat "repeatable" as a measurable claim about the **marginal cost curve** of the pipeline (corpus build → BSIP scoring → v2 frontend → QA/`validate-corpus` → launch), not as a category count:

| Count | What it proves | What it does **not** prove |
|---|---|---|
| **1** | The pipeline *can* run end-to-end | Nothing about repeatability (could be bespoke/hero effort) |
| **2** | Re-execution: category #1 was **not bespoke**; the process ran a second time | A **trend** — two points can't distinguish "repeatable" from "lucky twice"; no marginal-cost slope |
| **3** | **Repeatability** — three points establish a cost/variance **trend** (the classic "do it three times before you call it a process") | Throughput / concurrency |
| **4** | **Scalable throughput** — categories can run in a cohort without serializing on one specialist | — |

So **2 is the floor for *existence* of repeatability, not proof of *predictable, scalable* repeatability.** There is **no evidence** that 2 is sufficient for the latter — `category_scaling_readiness_v1` speaks to operating-model risk at Category #5/#10, not to a magic number of 2. Hence 2 should be the **gate-opening minimum**, not the target.

### 8.3 Revised structure (keeps target 4, controls the risk)
```
Cat 1  cereals   — instrumented reference run on the hardened (P3) pipeline → sets baseline cost
Cat 2  tahini    — repeat
   └─ GATE G-W2A: marginal cost ≤ Cat 1 · 0 novel firefights · defects caught by
                  validate-corpus pre-launch · ≤N contract deviations  → release Cats 3–4
Cat 3  (TBD)     — completion = "REPEATABILITY PROVEN" (3-point trend)
Cat 4  (TBD)     — completion = "THROUGHPUT CONFIRMED" (cohort/parallel)
```
**Instrumentation captured per category** (this is what makes the claim auditable rather than asserted): marginal effort (person-hours + elapsed), defect-escape rate (caught automatically vs. found late), category-module contract deviations, rework cycles. The gate is a real go/no-go: if Cat 2's marginal cost is *not* ≤ Cat 1, the answer is "the pipeline isn't repeatable yet — fix P3," not "ship two more anyway."

This satisfies your objective better than a flat 2 (which would have *under-committed* and never demonstrated the trend), while preserving the risk control that motivated the original hedge.

---

## 9. Recommended registry structure for P1–P5 (post-ratification)

Model each P-objective as **one objective task** with **lettered sub-tasks** (`new_task.py --parent`), sequencing encoded via `depends_on`/`blocks`. **Open objective tasks at ratification; open each sub-task only when its work begins** (Task Creation Protocol — register at open). Respect `task_capacity: 3` — keep ≤3 objectives `IN_PROGRESS`; the launch-critical trio **P1+P2+P3** runs first, P4/P5 open as they retire.

**Ratify first (before workstreams):** Launch Definition v1 → **DEC-003** (`scope_definition`). P-objective success criteria then cite the Launch-Definition dimension they own (§8 of `launch_definition_v1.md`).

| Obj | Proposed id | Title | Owner | Priority | depends_on |
|---|---|---|---|---|---|
| P1 | TASK-128 | Comparison Platform v2 Completion (existing fleet) | frontend-agent | **CRITICAL** | TASK-129A |
| P2 | TASK-129 | BSIP Calibration & Confidence (launch slice) | nutrition-agent / data-agent | HIGH | — |
| P3 | TASK-130 | Operating-Model Hardening | data-agent / qa-agent | HIGH | — |
| P4 | TASK-131 | Bari Intelligence Articles | content-agent | MEDIUM | TASK-128, TASK-129 |
| P5 | TASK-132 | Comparison Wave 2 (target 4, gated) | frontend + data | MEDIUM | TASK-128, TASK-130 |
| (deferred) | — | BSIP2 Next-Gen Evolution | — | — | open post-launch |

**Sub-task skeleton (open on demand):**
- **TASK-128** P1: `A` author+sign `comparison_ui_reference_v2.md` (prereq gate) · `B` QA re-baseline mobile+`lg` · `C` hummus v2 pilot + exit verdict · `D` maadanim→snacks→yogurts→bread migration · `E` milk gen0→gen1→v2 *or* legacy-label decision.
- **TASK-129** P2: `A` hummus confidence re-audit *(blocks 128A / Phase-0 #6)* · `B` observed-weakness calibration · `C` per-category score-freeze sign-offs.
- **TASK-130** P3: `A` `validate-corpus` command (+ close bread `limitingFactors` gap) · `B` category-module contract · `C` route/status governance + deprecation policy · `D` clean committed baseline.
- **TASK-131** P4: `A` pilot article (score-frozen category) · `B` scale to 3 flagship.
- **TASK-132** P5: `A` cereals (instrumented reference) · `B` tahini → **gate G-W2A** · `C` Cat 3 ("repeatability proven") · `D` Cat 4 ("throughput confirmed").

**Key dependency edges to set in frontmatter:** `TASK-129A blocks TASK-128` (confidence re-audit gates v2 Phase-0 #6); `TASK-131 depends_on [TASK-128, TASK-129]`; `TASK-132 depends_on [TASK-128, TASK-130]`.

*Note:* ids 128–132 assume no tasks are opened between now and ratification; `new_task.py` auto-allocates `max+1`, so confirm the next free id at open time.
