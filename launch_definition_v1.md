# Bari Launch Definition v1 — RATIFIED

**Task:** TASK-126 (Controller-ratified)
**Date:** 2026-06-01
**Status:** **RATIFIED as DEC-003** (`scope_definition`, DECIDED 2026-06-01). Amendments A (milk) + B (success indicators) incorporated.
**Purpose:** establish a single, testable finish line for "Bari launch" so the P1–P5 objectives have a fixed target and cannot creep.

> **Launch = Operational Readiness (§§2–6) AND Market-Facing Readiness (§6.5).** Both classes must pass; operational gates alone do not constitute launch.

> "Launch" here = the **public launch of the Bari comparison platform** as a credible consumer destination (the `hashvaot` hub + its categories + flagship intelligence content) — not an internal milestone. A category going LIVE in source (as hummus already has) is *necessary but not sufficient* for launch.

---

## 1. Launch criteria (overall gate)

Bari is **launched** when **all six dimensions below pass**, ratified by a launch decision (DEC-003), with:
- dashboard **GREEN, 0 drift**;
- **0 open P0/P1 defects**;
- `next build` clean, all static pages prerender;
- every dimension's owner has signed its row.

Launch is a **conjunction** — any single failing dimension holds launch.

## 2. Required categories

- **The 5 existing gen1 categories — maadanim, hummus, snacks, yogurts, bread — all LIVE on the v2 reference, score-frozen, and field-complete** (non-empty, product-specific reasoning fields for every displayed product).
- **milk** (gen0/LEGACY) — **DECIDED (Amendment A): launch as LEGACY; migrate post-launch (committed, not optional).** Rationale: milk has no comparison-shelf corpus (it is a bespoke `/blog` editorial analysis, 20 products) and requires a *double* migration — gen0→gen1 (MILK-001) to build a shelf corpus, *then* gen1→v2 — versus a single clean swap for the other five. Effort is disproportionate to its value, so it does not gate launch; but its gen0→gen1→v2 onboarding is a **committed post-launch workstream** (see P1 §128E, opens immediately after launch). The existing `/blog` milk-analysis stays live and LEGACY-labelled until then.
- **Wave 2 (cereals, tahini) is explicitly NOT required for launch.** Wave 2 is post-launch repeatability proof (P5). Launch is gated on *depth and credibility of the existing fleet*, not category count.

## 3. Required content

- **Methodology page live** — transparent signal taxonomy and "how Bari scores," no algorithm/weight exposure.
- **≥1 flagship intelligence article live** (the P4 pilot), with the corpus→article pipeline proven and traceable to a score-frozen corpus. The remaining 2 flagship articles **may trail launch**.
- **0 empty expansions** across all launch categories (already true for hummus; required fleet-wide).

## 4. Required platform capabilities

- **v2 reference Phase 1 shipped** on all 5 launch categories: dense row + density toggle, column-aligned metric block (**protein + additives**), strongest +/− on the collapsed row, restructured expansion, responsive table.
- **v2 navigation chrome (Phase 2)** — score-band rail, inline band dividers, header histogram — live on the launch hub categories.
- **Hashvaot hub live**; canonical routing stable; mobile + `lg` responsive; **SEO baseline generated** (`generate_seo.py`).
- **`base_pct` (Phase 3) is NOT required** for launch — it is externally blocked on a data pipeline (TASK-111) and must never gate launch.

## 5. Required BSIP maturity

- **BSIP2 = AUTHORITATIVE** for all 5 launch categories (already true on the dashboard).
- **Confidence accuracy gate passing** on all 5 (`verified` only when ≥3/6 nutrition fields **and** the ingredient field is a **real ingredient list** — not a scraped nutrition panel, marketing prose, or an allergen/handling sentence; else `partial`; null → `insufficient`). When the ingredient field fails the quality check, the row is `partial` **and** ingredient-derived positive signals (additive-free / NOVA / sweetener / protein-from-ingredients claims) are suppressed. Quality check is the shared validator `03_operations/bsip2/sprint1/ingredient_quality_gate.py` (`gate_confidence` / `assess_ingredients`). *Amended per TASK-129A (2026-06-01); supersedes the prior presence-only wording — origin `03_operations/bsip2/confidence_gate_fix_129a_v1.md`.*
- **Scores frozen per launch category** — no calibration in flight at launch.
- **Golden-products suite green**; known failure modes documented.
- **BSIP2 next-gen evolution is NOT required** for launch (post-launch, deferred slice of old O2).

## 6. Required QA threshold

- **`validate-corpus` (P3) green** on all 5 launch categories — enforces v2 field-completeness (incl. closing bread's `limitingFactors` gap).
- **Fresh QA baselines at mobile + `lg`** for all 5 (v1's 375px-only snapshots retired).
- **Corpus order preserved** under every control; **no product removed from the DOM** by any filter.
- **0 open P0/P1**; carry-forward items (e.g. hummus N1 hardcoded `"69"/"59"` copy constants) either fixed or explicitly accepted in writing.
- No regression to any sibling category on `next build`.

---

## 6.5 Launch Success Indicators — market-facing readiness (Amendment B)

Operational readiness (§§2–6) proves the platform is *built correctly*. These indicators prove it is *launched into the market* — outcome/market-facing signals, distinct from internal gates:

| Indicator | Met when |
|---|---|
| **Comparison pages publicly available** | All 5 launch categories reachable at public, indexable `/hashvaot/*` URLs (not behind a flag); robots/sitemap allow indexing. |
| **First flagship article published** | The P4 pilot article is publicly live and linked from the hub. |
| **Category coverage achieved** | 5/5 gen1 categories LIVE on v2; milk LEGACY-labelled (per Amendment A). |
| **User feedback collection active** | A live mechanism to capture user feedback on comparison pages (feedback control / form), with submissions reaching a monitored destination. |
| **Discoverability baseline live** | SEO baseline generated and deployed (`generate_seo.py`); hub indexed. |
| **Measurement active** | Analytics in place so post-launch outcomes (traffic, engagement, feedback volume) are observable from day one. |

These are **launch-completion** indicators, not pre-launch gates beyond what §§2–6 require: they confirm the platform is publicly usable and measurable, not merely deployable.

---

## 7. Explicitly NOT gating launch (anti-creep guardrails)

To prevent objective creep, launch is **not** held on any of:

| Item | Why excluded | Where it lives |
|---|---|---|
| Wave 2 categories (cereals, tahini, +2) | Post-launch repeatability proof | P5 |
| `base_pct` 3rd metric bar | Externally blocked data pipeline | P1 Phase 3 |
| BSIP2 next-gen evolution | Post-launch scoring R&D | deferred O2 slice |
| All 3 flagship articles | 1 pilot suffices for launch credibility | P4 |
| milk v2 migration | LEGACY-labelled at launch; migration **committed post-launch** (not optional) | P1 §128E (post-launch) |

Anything proposed as a launch blocker that is not in §§2–6 must be raised as an explicit DEC before it can move the finish line.

---

## 8. Dimension → owning objective (traceability)

| Launch dimension | Delivered by |
|---|---|
| §2 categories on v2, field-complete | **P1** |
| §3 content (methodology + pilot article) | **P4** (+ P1 for expansions) |
| §4 platform capabilities (v2 Phase 1+2, hub, SEO) | **P1** |
| §5 BSIP maturity (confidence gate, score-freeze) | **P2** |
| §6 QA threshold (validate-corpus, baselines) | **P3** |

Each P-objective's success criteria **inherit** from the rows it owns here, so closing the objectives mechanically advances the launch gate.

---

## 9. Ratification

**Ratified as DEC-003** (`scope_definition`, `DECIDED` 2026-06-01) by the Central Controller. P1–P5 success criteria cite the Launch-Definition dimension each owns (§8), so "launch-ready" is objectively checkable rather than subjective. Amendments A (milk: LEGACY at launch, committed post-launch migration) and B (Launch Success Indicators, §6.5) are part of the ratified definition.
