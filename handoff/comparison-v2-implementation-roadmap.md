# Comparison UI Reference v2 — Implementation Roadmap

**Task:** TASK-118 (Frontend Agent)
**Type:** Roadmap only — no implementation, no redesign, no production-code change.
**Date:** 2026-05-31

**Inputs consulted**
- `handoff/comparison-v2-spec.md` — accepted v2 direction (TASK-098); changes #1–#9, data contract, build sequencing.
- TASK-111 (registry, CLOSED) — data-dependency readiness review. Verdict: **READY_WITH_MODIFICATIONS** (`base_pct` needs a new main-ingredient extraction pipeline; confidence promotion needs a hummus re-audit).
- `docs/comparison_ui_reference_v1.md` (frozen) — current shelf reference (maadanim).
- `src/lib/comparisons/comparison-product.ts` — current `ComparisonProduct` VM.
- Command Center category states (`05_command_center/command_center.json`).

> **Input gap (flagged):** "TASK-106 decision" is listed as an input but is **not present** in the registry (`C:\Bari\tasks\`), the dashboard, `decisions/decisions.json`, or anywhere on disk. The locatable governing decisions are **TASK-098** (accepted v2 direction) and **DEC-002** (hummus go-live, DECIDED). This roadmap is built on those; if TASK-106 carries a constraint that supersedes them, it must be supplied before Phase 1 sign-off.

---

## 1. Governing principle

This is a **presentation/IA migration, not a corpus or scoring change.** Every v1 invariant carries forward unchanged: corpus owns order (no client re-sort), every product individually visible, pre-authored Hebrew verbatim, no algorithm exposure, interpretive-before-technical. The v2 spec touches layout and the view-model surface only.

**Hard process gate:** per the spec, v2 code "does **not** ship on frozen v1 without" a signed `comparison_ui_reference_v2.md`. Authoring + sign-off of that reference is therefore a Phase-1 prerequisite, not a Phase-1 deliverable.

---

## 2. Phase breakdown

### Phase 0 — v1-safe promotions (no v2 reference required)
Maps to the spec's "Pre-DEC002, v1-safe" bucket. Ships on the **frozen v1** shelf; needs no reference re-baseline.

| Item | Spec ref | Notes |
|------|----------|-------|
| Confidence promoted onto the collapsed row | #6 | Move confidence out of the 10px expansion footnote onto the row header. **Gated** on the accuracy re-audit (see Blockers). |
| Confidence accuracy gate | #6 | Apply `confidence_label_audit_v1` rule: `verified` only when ≥3/6 nutrition fields **and** ingredients present; else `partial`; null nutrition+ingredients → `insufficient`. |
| Category-level disclosure de-dup | #8 | Move category-wide gaps (fat note, relativity) to header/methodology; per-row `unknowns` becomes product-specific only. |
| Relativity tag | #8 | Category-level relativity disclosure in the header. |

*Why first:* zero reference risk, no QA re-baseline, and #6 forces the confidence re-audit that Phase 1 also depends on — so it retires a shared dependency early.

### Phase 1 — v2 core (the new reference)
Maps to the spec's "v2" bucket. **Blocked until `comparison_ui_reference_v2.md` is authored and signed**, and QA is re-baselined (v1's 375px-only snapshots are invalid).

| Item | Spec ref | Notes |
|------|----------|-------|
| Author `comparison_ui_reference_v2.md` | — | **Prerequisite gate.** Translate spec §Layout/§A11y into the binding reference. |
| Dense row by default + density toggle | #1 | Comfortable mode ≈ current v1 row metrics. |
| Column-aligned metric block | #2 | **Ships with 2 of 3 metrics: `protein_g` + `additive_count`.** `base_pct` is removed from Phase 1 (see §3 / §5). |
| Strongest +/− on the collapsed row | #5 | From `rowReason` (derived from `positiveSignals[0]`/`limitingFactors[0]`). |
| Expansion restructure | #7 | Confidence+source on top; nutrition at reason level; drop the 2nd "advanced" toggle; magnitude on limits. Keep label strings + section identity (`הקשר במדף` etc.). |
| Responsive table layout | #9 | Dense table-like from `lg`; single-column rows on mobile; ends the 375px desktop frame. |

### Phase 2 — navigation chrome (depends on Phase 1 layout)
Side affordances over the v2 list. No new section *above* the shelf.

| Item | Spec ref | Notes |
|------|----------|-------|
| Score-band jump rail (80+/70s/60s/50s/<50) | #3 | Sticky side rail; click = scroll only; hidden < 680px; bands derived from `score`, contiguous in corpus order. |
| Inline band dividers | #4 | Pure in-list visual separators; do not regroup or reorder. |
| Score-distribution histogram (header) | spec §Layout | Static, read-only; highlights dominant band. |

*Why after Phase 1:* the rail and dividers attach to the v2 row/band geometry; building them first would couple to layout that isn't fixed yet.

### Phase 3 — `base_pct` completion (deferred / externally blocked)
Re-opens the metric block once the data exists.

| Item | Spec ref | Notes |
|------|----------|-------|
| Main-ingredient extraction pipeline | TASK-111 | Data-side deliverable; **not owned by Frontend.** Produces `base_pct` per product, deterministically, category-scoped. |
| Add `base_pct` third bar to metric block | #2 | UI is a small additive change once the field lands; re-baseline metric-column snapshots. |

---

## 3. Required identifications

### 3a. Immediate implementation items (no new data, no external blocker)
- **#8** category-disclosure de-dup + relativity tag (Phase 0) — uses existing header/methodology surfaces.
- **#1** dense row + density toggle (Phase 1, once reference is signed) — pure layout.
- **#5 / `rowReason`** — derivable from existing `positiveSignals`/`limitingFactors`.
- **#7** expansion restructure — reorders existing fields; no new data.
- **#9** responsive layout — CSS/layout; no new data.
- **`additive_count`** — *safely derivable* from `ingredients_he` via a deterministic additive lexicon. Display-only; **not** a score input. (Implementable now; needs an authored derivation rule, not a pipeline.)
- **#3 / #4 / histogram** — all derive from existing `score`.

### 3b. VM dependencies (`ComparisonProduct` / `BariProductVM`)
Current VM (`comparison-product.ts`) exposes `score`, `grade`, `insight_line`, `ingredients_he`, `nutrition{energy_kcal, protein_g, sugar_g, fat_g, fiber_g, sodium_mg}`, `confidence_level: "full"|"partial"|"insufficient"`.

| New/changed field | Status | Action |
|-------------------|--------|--------|
| `metrics.protein_g` | **Exists** (in `nutrition`) | Surface as first-class metric (display scale 0–20). |
| `metrics.additive_count` | **Derivable** | Add derived field from `ingredients_he` (pips 0–5; good ≤1, poor ≥4). |
| `metrics.base_pct` | **Requires new pipeline** | **Defer to Phase 3.** Not derivable from current label data. |
| `metrics.sodium_mg` / `energy_kcal` | **Exists** | Expansion-only; carry through. |
| `rowReason{positive, limiting}` | **Derivable** | Short form from `positiveSignals[0]`/`limitingFactors[0]`. |
| `confidence` enum reconciliation | **Mismatch** | Spec wants `"verified"|"partial"|"insufficient"`; VM currently has `"full"|…`. Rename `full → verified` and apply the accuracy gate (#6). |

**Null rule (applies to every metric):** render `"—"`, never `0`. Two products with `additive_count` 1 vs 2 must remain visually distinguishable — that distinguishability *is* the differentiator.

### 3c. Blockers
1. **`base_pct` main-ingredient extraction pipeline** — not built/funded (TASK-111). Blocks the 3rd metric bar only → handled by removing `base_pct` from Phase 1 and deferring to Phase 3. **Owner: Data Agent.**
2. **`comparison_ui_reference_v2.md` sign-off** — process gate; v2 code cannot ship on frozen v1 without it. Blocks all of Phase 1+. **Owner: Frontend + design/product sign-off.**
3. **Confidence accuracy re-audit (hummus)** — required before confidence promotion (#6) per `confidence_label_audit_v1` (TASK-111). Blocks Phase 0 #6. **Owner: Data/QA.**
4. **QA re-baseline** — v1's 375px-only snapshots are invalid for v2; new baselines at mobile + `lg` required before Phase 1 ships. **Owner: QA.**
5. **TASK-106 input not locatable** — see header flag. Soft blocker on Phase-1 sign-off until confirmed that TASK-098/DEC-002 are the governing decisions.

### 3d. Items removed from Phase 1
- **`base_pct`** (the main-ingredient % bar, change #2's third metric) — removed from Phase 1, deferred to Phase 3, because it depends on a new extraction pipeline that does not exist (TASK-111). Phase-1 metric block ships with **protein + additives** only; the column is designed to accept a third bar later without re-layout.
- No other spec item is dropped. Everything in TASK-098's "Explicitly rejected" list (clustered groups, alternative sort modes, hiding/pagination) stays out of scope entirely — not "removed from Phase 1," but never in any phase.

---

## 4. Category migration order

Current shelf categories run on the **gen1** v1 architecture except milk (gen0) and two unbuilt categories. v2 migration sequence:

| Order | Category | Current state | Rationale |
|-------|----------|---------------|-----------|
| **1 (pilot)** | **hummus** | LIVE, gen1, 69 prod | Spec's named source of truth (`bari.digital/hashvaot/hummus` + the `ui_kits/web` prototype). Confidence re-audit is hummus-scoped anyway. See §5. |
| 2 | maadanim | LIVE, gen1, 90 prod | The **frozen v1 reference** — re-baseline the reference category onto v2 second, so the new reference is proven on the source-of-truth first. |
| 3 | snacks | LIVE, gen1, 53 prod | Clean gen1 swap; mid-size corpus. |
| 4 | yogurts | LIVE, gen1, 45 prod | Clean gen1 swap. |
| 5 | bread | LIVE, gen1, 80 prod | Clean gen1 swap; largest live corpus — good late-stage stress test for bands/rail/histogram. |
| 6 | milk | LEGACY, **gen0**, 20 prod | Higher effort: carries a gen0→gen1 migration (MILK-001) *before* it can take v2. Sequence its gen0→gen1→v2 jump after the gen1 fleet is on v2. |
| n/a | breakfast-cereals, tahini | NOT_STARTED | Born on v2 — build directly to the v2 reference when their corpora exist; no migration step. |

Migration is per-route and reversible behind the layout switch; the metric block degrades cleanly (`"—"`) on any category whose corpus lacks a given field.

---

## 5. Recommended pilot: **hummus**

**Recommendation: pilot v2 on `hummus` (`/hashvaot/hummus`).**

Rationale:
- It is the **spec's source of truth** — the `ui_kits/web/index.html` prototype was authored against hummus, so v2 is already visually validated there.
- The confidence re-audit (Blocker #3) is **hummus-scoped** per TASK-111, so it is on the critical path for hummus regardless — piloting here retires that dependency rather than adding a new one.
- Corpus size (69) is large enough to exercise the score-band rail, dividers, and histogram, yet small enough for a tight QA re-baseline.
- Its known data caveats (**HUM-001** fat suppressed, **HUM-002** sugar absent) **do not touch the Phase-1 metric block** (protein + additives) — fat/sugar are expansion-only or absent, so they don't gate the pilot.

**Pilot exit criteria:** v2 reference signed; metric block renders protein + additives with correct `"—"` null states; confidence accuracy gate passing on the re-audited hummus corpus; rail jump lands on the correct first row of each band; filtered views preserve corpus order; no product removed from the DOM by any control; fresh mobile + `lg` QA baselines captured. Only then promote maadanim (order 2).

---

## 6. Roadmap at a glance

```
Phase 0  v1-safe        #6 confidence promote+gate · #8 disclosure de-dup · relativity
         (no ref change) └─ requires: hummus confidence re-audit (Blocker #3)

   ── gate: author + sign comparison_ui_reference_v2.md (Blocker #2) ──
   ── gate: QA re-baseline mobile + lg (Blocker #4) ──

Phase 1  v2 core         #1 density · #2 metric block (protein+additives ONLY) ·
                         #5 rowReason · #7 expansion · #9 responsive table
         VM work:        + metrics{protein_g, additive_count} · rowReason ·
                         confidence enum reconcile (full→verified)
         PILOT: hummus → then maadanim → snacks → yogurts → bread

Phase 2  nav chrome      #3 band rail · #4 dividers · header histogram

Phase 3  base_pct        [Data] main-ingredient extraction pipeline (Blocker #1)
         (deferred)      → add 3rd metric bar (#2 completion) → re-baseline
```

---

*Roadmap only. No production code modified; no redesign performed.*
