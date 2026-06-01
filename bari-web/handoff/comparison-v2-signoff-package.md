# Comparison UI Reference v2 — Sign-off Package

**Task:** TASK-123 (Frontend Agent)
**Type:** Sign-off / advisory only — no implementation, no production-code change, no redesign.
**Date:** 2026-05-31
**Verdict:** **READY WITH MODIFICATIONS** (see §6).

---

## Inputs consulted

- `handoff/comparison-v2-spec.md` — accepted v2 direction (TASK-098): changes #1–#9, the `BariProductVM` data contract, layout rules, build sequencing.
- **TASK-111** (registry, CLOSED) — data-dependency readiness review. Verdict: **READY_WITH_MODIFICATIONS** (`base_pct` needs a new main-ingredient extraction pipeline; confidence promotion needs a hummus re-audit).
- `handoff/comparison-v2-implementation-roadmap.md` — TASK-118 (registry, CLOSED): four-phase plan, VM dependencies, blocker list, category migration order, hummus pilot.
- `docs/comparison_ui_reference_v1.md` (frozen) — the current binding shelf reference (maadanim).
- Current comparison pages on disk: `/hashvaot/{hummus, maadanim, snacks, yogurts, bread, vegetable-spreads, ...}` + `milk-comparison` (gen0) — all running the **v1** architecture.

### Input discrepancies surfaced (not silently resolved)

1. **"TASK-119 readiness assessment" — does not exist.** The brief names TASK-119 as an input, but there is **no TASK-119** in the authoritative registry (`C:\Bari\tasks\`), the dashboard, or `decisions.json`. The actual readiness assessment in this workstream is **TASK-111** (verdict READY_WITH_MODIFICATIONS), which is what this sign-off is built on. Per the Registry First Rule, the registry is authoritative and the conflict is surfaced rather than reconciled from memory. **If TASK-119 is a distinct artifact, it must be supplied before final sign-off.**
2. **"TASK-106 decision" — not locatable.** Inherited from the roadmap (TASK-118 header flag): TASK-106 is referenced as a governing input but is absent from the registry, dashboard, and `decisions/decisions.json`. The locatable governing decisions are **TASK-098** (accepted v2 direction) and **DEC-002** (hummus go-live). This sign-off is built on those; an unconfirmed TASK-106 remains an open condition (§5, §6).

---

## 1. What this document is

This package **freezes the V2 reference at the specification / decomposition level** and records the go/no-go verdict for implementation. It is the consolidation point where the accepted direction (TASK-098), the data-readiness verdict (TASK-111), and the phased roadmap (TASK-118) are confirmed to be mutually consistent and locked.

It is **not**:

- the binding `comparison_ui_reference_v2.md` engineering reference — authoring that remains a **Phase-1 prerequisite gate** (Blocker #2 in the roadmap), not part of this sign-off;
- a redesign or any change to layout decisions already accepted in TASK-098;
- a production-code change. No `src/**` file is touched.

**Scope guardrail (carried verbatim from v1 and TASK-098):** V2 is a **presentation / IA migration only**. It changes layout and the view-model *surface*; it never changes corpus content, product order, or scoring. Every v1 invariant below is preserved.

---

## 2. The frozen V2 reference — invariants carried from v1

These are **locked** and non-negotiable in V2 (from `comparison_ui_reference_v1.md` and the spec's "Non-negotiable invariants"):

1. **Corpus owns order.** Rows render in `BariProductVM[]` array order (score-desc, insufficient last). No client re-sort. Filters subset and **preserve relative order**.
2. **Every product individually visible.** No clustering, no collapse-by-default, no hiding. Insufficient-data products render a "—" no-score state.
3. **Pre-authored Hebrew, verbatim.** No runtime copy generation; expansion fields render from the VM.
4. **No algorithm exposure.** No BSIP / NOVA / caps / dimension language in user-facing strings.
5. **Interpretive-before-technical** hierarchy preserved inside the expansion (reasoning first; nutrition/ingredients muted below the hairline).
6. **Section identity preserved.** Expansion labels keep their strings and identity (esp. **הקשר במדף**).

Everything in §3 changes presentation/IA **on top of** these invariants — never order or corpus content.

---

## 3. Explicit confirmations (frozen V2 elements)

Each element below is **CONFIRMED — FROZEN** for V2 unless explicitly marked otherwise. "Spec ref" points to the change number in `comparison-v2-spec.md`.

### 3.1 Density model — CONFIRMED (FROZEN)
*Spec #1.*
- **Dense row by default**, with a **density toggle** offering `compact` / `comfortable`.
- `comfortable` mode ≈ current v1 row metrics (thumb 60px, relaxed padding); `compact` is the new default (thumb 44px).
- Density is a presentation toggle only — it does not change corpus, order, or which rows render.

### 3.2 Metric block — CONFIRMED (FROZEN) with a launch-scope modification
*Spec #2; modification per TASK-111 + TASK-118 §3d.*
- **Column-aligned metric block per row** on shared, **category-scoped** scales, in a fixed-width column (~188px) so values align vertically across rows — that vertical alignment **is** the differentiator.
- **V2 launch ships 2 of 3 metrics: `protein_g` + `additive_count`.**
  - `protein_g` — bar scale 0–20 g (good ≥10, poor <5). **Exists** in `nutrition`; surfaced as a first-class metric.
  - `additive_count` — pips 0–5 (good ≤1, poor ≥4). **Safely derivable** from `ingredients_he` via a deterministic additive lexicon. Display-only; **not** a score input.
- **`base_pct` (main-ingredient %) is EXCLUDED from V2 launch and deferred to Phase 3** — it requires a new main-ingredient extraction pipeline that does not exist (TASK-111, Data Agent). The metric column is designed to accept the third bar later **without re-layout**.
- **Null rule (every metric):** render `"—"`, never `0`. Two products with `additive_count` 1 vs 2 must remain visually distinguishable.
- Metrics are **display-only**, derived deterministically from existing label data; they are **not** new score inputs.

### 3.3 Confidence placement — CONFIRMED (FROZEN), gated
*Spec #6; gate per TASK-111 / `confidence_label_audit_v1`.*
- **Confidence is promoted onto the collapsed row header**, out of the 10px expansion footnote.
- **Accuracy-gated:** `verified` only when ≥3/6 nutrition fields **and** ingredients present; else `partial`; null nutrition + ingredients → `insufficient` (no score).
- **VM enum reconciliation required:** current VM exposes `confidence_level: "full" | "partial" | "insufficient"`; spec wants `"verified" | "partial" | "insufficient"`. **Rename `full → verified`** and apply the gate.
- **Gate:** confidence promotion must not ship until the **hummus confidence re-audit** passes (Blocker #3). This is a Phase-0, v1-safe promotion — it does **not** require the v2 reference.

### 3.4 Disclosures — CONFIRMED (FROZEN)
*Spec #8.*
- **Category-level disclosures are stated once** in the header / methodology (e.g. the fat note, the relativity tag) — **not** repeated per row.
- **Per-row `unknowns` becomes product-specific only.** Category-wide gaps move out of the row.
- This is a Phase-0, v1-safe change (no v2 reference required); it uses existing header/methodology surfaces.

### 3.5 Expansion layout — CONFIRMED (FROZEN)
*Spec #7.*
- **Confidence + source at the top** of the expansion.
- **Nutrition surfaces at reason level**; the **second "advanced" toggle is dropped**.
- **Magnitude shown on limiting factors.**
- **Label strings and section identity are preserved** (interpretive blocks → hairline → technical block; **הקשר במדף** unchanged).
- Interpretive-before-technical hierarchy (v1 invariant) is retained.
- **Expand behavior:** do **not** `scrollIntoView` on expand (it yanks long lists); multiple rows may be open simultaneously. Only the band rail scrolls, on explicit click (see 3.7).

### 3.6 Responsive behavior — CONFIRMED (FROZEN)
*Spec #9.*
- **Dense table-like layout from `lg`**; **single-column rows on mobile**.
- **Ends the 375px desktop phone-frame** (v1 item 10) and the hummus-vs-others 375px drift.
- **Mobile parity = same IA, narrower** — identical information architecture, not a reduced one.
- **QA consequence:** v1's 375px-only snapshots are **invalid** for V2; baselines must be re-captured at **mobile + `lg`** (Blocker #4) before Phase 1 ships.

### 3.7 Score-band rail — CONFIRMED (FROZEN)
*Spec #3 (rail) + #4 (dividers).*
- **Sticky side rail** with bands **80+ / 70s / 60s / 50s / <50**; positioned **inline-end (RTL)**; **hidden < 680px**.
- Each band shows **label + count + a proportion bar** tinted by band (green → amber as score drops).
- Bands are **derived from `score`**, contiguous in corpus order; **click = scroll only** (`scrollTo(firstRowOfBand, -offset)`). The rail **never reorders or regroups** rows.
- **Inline band dividers (#4)** are pure in-list visual separators; they **do not regroup or reorder** rows. This stays within the "no new section *above* the shelf" invariant — the rail is a side affordance and dividers are in-list.
- Plus **strongest +/− on the collapsed row (#5):** short-form `rowReason{positive, limiting}`, derived from `positiveSignals[0]` / `limitingFactors[0]`. Derivable from existing data.

### 3.8 Histogram — CONFIRMED (FROZEN)
*Spec §Layout.*
- **Score-distribution histogram in the header** (buckets 40–47 … 80+), **highlighting the dominant cluster band**.
- **Static, read-only.** Derived from existing `score`. Not interactive, not a control, does not filter or reorder.

### 3.9 Items intentionally excluded — CONFIRMED
Two distinct exclusion classes:

**A. Excluded from V2 entirely (TASK-098 "Explicitly rejected" — never in any phase):**
- Clustered / equivalent-product groups.
- Alternative sort modes (protein / additives / "Bari" views) — corpus owns order.
- Any hiding or pagination-by-default.
- `scrollIntoView`-on-expand (replaced by explicit rail-only scroll).

**B. Excluded from V2 *launch*, deferred (not rejected):**
- **`base_pct`** (third metric bar) → **Phase 3**, blocked on the main-ingredient extraction pipeline (TASK-111, Data Agent). The metric column is built to admit it later without re-layout.

---

## 4. V2 element → phase / readiness map

| Element | Spec # | Status | Phase | Data readiness (TASK-111) |
|---|---|---|---|---|
| Confidence promotion + accuracy gate | #6 | Frozen, gated | 0 (v1-safe) | Exists; needs enum rename + hummus re-audit |
| Category-disclosure de-dup + relativity | #8 | Frozen | 0 (v1-safe) | Uses existing surfaces |
| Density model | #1 | Frozen | 1 | Pure layout |
| Metric block (protein + additives) | #2 | Frozen (2 of 3) | 1 | protein exists; additives derivable |
| Strongest +/− on row (`rowReason`) | #5 | Frozen | 1 | Derivable |
| Expansion restructure | #7 | Frozen | 1 | Reorders existing fields |
| Responsive table | #9 | Frozen | 1 | CSS/layout |
| Score-band rail | #3 | Frozen | 2 | Derived from `score` |
| Inline band dividers | #4 | Frozen | 2 | Derived from `score` |
| Histogram | §Layout | Frozen | 2 | Derived from `score` |
| `base_pct` third bar | #2 | **Deferred** | 3 | **Requires new pipeline** |

**Pilot:** hummus (`/hashvaot/hummus`) — spec source of truth; confidence re-audit is hummus-scoped; corpus (69) exercises rail/dividers/histogram; HUM-001/HUM-002 caveats don't touch the protein+additives block. Migration order after pilot: maadanim → snacks → yogurts → bread → milk (gen0→gen1 first).

---

## 5. Unresolved decisions

These are open at sign-off. None invalidates the V2 *definition*; each is a precondition on *implementation* of the phase noted.

1. **TASK-106 input not locatable** *(soft blocker on Phase-1 sign-off).* Confirm that **TASK-098 + DEC-002** are the governing decisions, or supply TASK-106 if it carries a superseding constraint. **Owner: Central Controller / Product.**
2. **"TASK-119 readiness assessment" naming gap.** The brief's named input does not exist; this sign-off used **TASK-111**. Confirm TASK-111 is the intended source, or supply TASK-119. **Owner: Central Controller.**
3. **Binding `comparison_ui_reference_v2.md` not yet authored** *(hard Phase-1 gate).* V2 code "does not ship on frozen v1 without" it. This sign-off freezes the decisions; the binding reference must still be **authored and signed**. **Owner: Frontend + design/product sign-off.**
4. **Hummus confidence re-audit not yet run** *(gates Phase 0 #6).* Required by `confidence_label_audit_v1` before confidence promotion. **Owner: Data / QA.**
5. **QA re-baseline not yet captured** *(gates Phase 1).* New mobile + `lg` snapshots required; v1's 375px-only baselines are invalid. **Owner: QA.**
6. **`base_pct` extraction pipeline not built/funded** *(gates Phase 3 only).* Does **not** block V2 launch — handled by deferral. **Owner: Data Agent.**

---

## 6. Readiness verdict

### **READY WITH MODIFICATIONS**

**Rationale.** The V2 direction is accepted (TASK-098); all nine presentation/IA changes are internally consistent, decompose cleanly into the four-phase roadmap (TASK-118), and every data dependency is classified (TASK-111). The package is therefore not **NOT READY**. It is not **READY FOR IMPLEMENTATION** without conditions, because two governing inputs are unconfirmed (TASK-106, TASK-119) and the binding reference is unauthored. The honest position — matching TASK-111's own `READY_WITH_MODIFICATIONS` — is **READY WITH MODIFICATIONS**.

**The modifications / conditions attached to this sign-off:**

1. **Metric block ships 2 of 3 at launch** — protein + additives; `base_pct` deferred to Phase 3. (Locked.)
2. **Confidence promotion is gated** on the VM enum rename (`full → verified`) **and** the hummus re-audit. (Phase 0.)
3. **The binding `comparison_ui_reference_v2.md` must be authored and signed before any Phase-1 code.** This package authorizes that authoring; it does not substitute for it.
4. **QA must re-baseline at mobile + `lg`** before Phase 1 ships.
5. **TASK-106 must be confirmed-or-supplied, and the TASK-119/TASK-111 naming gap resolved,** before final Phase-1 sign-off.

**Implementation start authorized for Phase 0 (v1-safe)** — confidence promotion+gate and disclosure de-dup — once the hummus re-audit (condition 2) clears. Phases 1–2 unlock on conditions 3–5. Phase 3 unlocks on the data pipeline (condition 6).

---

*Sign-off package only. No production code modified; no redesign performed. The binding `comparison_ui_reference_v2.md` remains to be authored as a Phase-1 prerequisite.*
