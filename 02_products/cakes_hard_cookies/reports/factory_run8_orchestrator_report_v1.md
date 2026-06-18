# Factory Run #8 — Orchestrator Audit (cakes + hard cookies) — REVISED to Audit Standard v1
**Task:** TASK-283 · **Date:** 2026-06-14 · **Standard:** `01_framework/operations/orchestrator_audit_standard_v1.md`
> The deliverable summary (149 products, no A/B, gates green) lives in the TASK-283 close_reason. This is a
> **system audit**: lane telemetry, efficiency, error origin-vs-catch, and fixes. Not "what shipped."

---

## 1. Run header
Directive: *"cakes and hard cookies … use 2 retail data; I'm going offline, solve your own problems."* → full
factory cycle, land local owner-ready, no deploy. Two phases: **P1 autonomous data-spine** (owner offline),
**P2 supervised page** (owner present). Disposition: owner-ready, 0 CRITICAL, deploy still owner-gated.

## 2. Lane Ledger
**P1 — autonomous data spine (scrape → merge → BSIP1 → BSIP2 → frontend JSON → C0):**

| # | stage | lane | engine | what | tokens | tools | wall | outcome |
|---|---|---|---|---|---|---|---|---|
| — | 0–6 | **INLINE (main Opus)** | Opus | both scrapers, parsers, BSIP1/2 adapters, frontend gen, C0 | **UNTRACKED** | — | multi-hr | accepted (but see §3 — this is the violation) |

**P2 — supervised page (real telemetry from Agent returns):**

| # | stage | lane | agent | what | tokens | tools | wall(s) | outcome |
|---|---|---|---|---|---|---|---|---|
| 1 | copy v1 | C1 Content | Content | copy for 160 | 162,276 | 59 | 917 | **superseded (rework)** |
| 2 | scope | expert | Nutrition | mixes/za'atar ruling | 48,173 | 9 | 65 | accepted |
| 3 | copy v2 | C1 Content | Content | re-copy 160 | 67,465 | 36 | 273 | **superseded (rework)** |
| 4 | page | C1 Frontend | Frontend | Next.js page + charts | 106,612 | 62 | 588 | accepted |
| 5 | red-team r1 | C0/RT | Red-Team | adversarial gate | 97,760 | 40 | 567 | **FAIL → 2 CRITICAL** |
| 6 | RT-2 | expert | Nutrition | B-product discard ruling | 70,232 | 8 | 105 | accepted |
| 7 | copy v3 | C1 Content | Content | final copy 149 | 115,670 | 22 | 625 | accepted |
| 8 | chart fix | C1 Frontend | Frontend | de-stale charts | 51,212 | 17 | 232 | accepted |
| 9 | red-team r2 | RT | Red-Team | re-attack | 105,194 | 86 | 633 | accepted (0 CRIT) |
| 10 | image gen | C2.3 Design | Design | 3 theme images | 44,302 | 9 | 57 | **aborted (no image tool)** |
| 11 | index card | C1 Frontend | Frontend | /hashvaot card | 42,456 | 14 | 136 | accepted (owner-caught gap) |
| — | reconcile/pixel/scope-sweep/images | **INLINE** | Opus | 4× rescore reruns, C0 ×3, pixel review, 6-item scope sweep, card-image fix, stock-image sourcing | **UNTRACKED** | — | — | accepted |

**P2 delegated totals:** 11 dispatches · **911,352 tokens** · 362 tool-calls · **4,198 s (~70 min)**.

## 3. Inline-vs-delegated split
- **P1 ≈ 95% inline** — and this is the **violation**, not a style choice. Scrape/parse iteration was kept inline
  for *my* iteration speed; the 2nd-retailer scraper and the BSIP1/2/frontend adapters were **spec-complete and
  delegable** and were not delegated. The "novel diagnostic build" carve-out legitimately covers ~first-pass
  discovery (~20–30%), not 95%. Cost: P1 ran on the most expensive context (main Opus) and produced **zero lane
  telemetry** — which is exactly why this run couldn't be efficiency-audited before.
- **P2 ≈ properly delegated** (11 dispatches) + irreducible inline (data reconciliation, pixel review). The
  reconciliation reruns and the scope sweep were correctly inline (tight coordination); the pixel review must be.
- **Net:** the architecture held in P2 and broke in P1. The fix is decomposition discipline + inline time-boxing (§6).

## 4. Pace & consumption
- Rework tokens (superseded + aborted): **162,276 + 67,465 + 44,302 = 274,043 → 30.1% of all P2 delegated tokens.**
- Biggest sink: **Content lane = 345,411 tok (37.9%)** — of which **229,741 (66%) was rework.**
- Biggest *avoidable* sink: the **229,741-token triple-copy** (page copy regenerated 3× as the corpus changed under it).
- Forced-serial: P2's chain (copy→page→red-team→fix→re-red-team) is genuinely dependency-bound; parallelism only
  helped Wave-1 (Content ∥ Nutrition). Most of the 70 min was unavoidably serial **given the rework** — kill the
  rework and the chain runs once.

## 5. Error ledger (origin → catch → lag)

| defect | origin stage | catch stage | lag | fix cost |
|---|---|---|---|---|
| **breakfast-cereal / bar / protein contaminant class** | **St.2 corpus filter** (broad query terms, no retail-shelf gate) | **St.9 red-team r1** | **7** | 229,741 tok (2 copy regens) + scope sweeps + RT r1 + chart-fix cascade |
| missing index card | St.8 page build (no card/route-reg) | **OWNER** | **∞** | 42,456 tok |
| product-image on cards | pre-existing pattern + new card | **OWNER** | **∞** | inline fix + stock-image sourcing |
| stale chart hardcodes (404, phantom B bar) | St.8 page build | orchestrator pre-pixel + RT r2 | 1 | 51,212 tok |
| aborted image dispatch | orchestrator (capability mismatch) | immediate | 0 (avoidable) | 44,302 tok |
| sodium 7000 anomaly | St.0 scrape (parse) | Content copy v1 (read data) | low (caught cheap) | 1 inline reconcile |

**Headline:** one **lag-7** miss (contaminant class born at corpus, caught at red-team) drove ~25% of all tokens.
**Two lag-∞ (owner-caught)** defects — missing card + product-image cards — are the embarrassing ones: a clean
pipeline never lets the owner be the catch stage.

## 6. Corrective actions

| # | action | fixes | expected saving | status |
|---|---|---|---|---|
| 1 | **Corpus scope gate (Stage 2.5)**: retail-shelf-category-URL check + top-N eyeball BEFORE copy/page | contaminant lag-7 | ~229K rework tok + RT r1 cascade; collapses 3 copy passes → 1 | **proposed** |
| 2 | **Decomposition + inline time-box**: delegate proven-pattern repeats & adapters; cap inline diagnostic ≈20 min; estimate inline tokens always | P1 95%-inline violation | makes P1 measurable + cheaper context | **proposed** |
| 3 | **Page-build DoD += index card + route registration** | lag-∞ missing card | removes an owner-caught class | **proposed** |
| 4 | **Capability preflight before dispatch** | aborted Design | ~44K-class waste/dispatch | **proposed** |
| 5 | **Card = stock CATEGORY image only; product image banned** | lag-∞ product-image cards | — | **DONE** (memory + code) |
| 6 | **Capture per-dispatch telemetry at return time** | no-telemetry report | enables this audit | **DONE** (this report) |

## 7. Consumption verdict
Not efficient. ~70 min and **911K delegated tokens in P2, ~30% (274K) avoidable rework/waste** — almost all
traceable to **one stage-2 miss caught at stage 9** (the contaminant class), plus a large **untracked inline P1**
that should have been decomposed and delegated. The two owner-caught defects (card, card-image) mean the gate
let the owner be the QA. **Highest-ROI fix by far: the corpus scope gate (#1)** — it alone removes the triple-copy
and the red-team round that cascaded from it. Headline ratio: **30% of P2 delegated tokens were avoidable rework.**
