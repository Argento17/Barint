# Comparison UI Reference v2

**Type:** Binding engineering reference (authoritative). This is the implementation
reference for **TASK-128** (Comparison Platform v2 Completion).
**Status:** Authored — Phase-1 prerequisite gate (Blocker #2 / sign-off condition 3).
**Authored by:** frontend-agent under **TASK-128A**, 2026-06-01.
**Supersedes for v2 routes:** `comparison_ui_reference_v1.md` (frozen; remains the
binding reference for any route still on v1 until that route is migrated).

**Governing chain (do not re-litigate here):**

- `handoff/comparison-v2-spec.md` — accepted v2 direction (**TASK-098**); changes #1–#9, data contract, layout rules.
- `handoff/comparison-v2-implementation-roadmap.md` — **TASK-118** (CLOSED); four-phase plan, VM deps, migration order, hummus pilot.
- `handoff/comparison-v2-signoff-package.md` — **TASK-123** (CLOSED); freezes the decisions, verdict **READY WITH MODIFICATIONS**.
- **TASK-111** (CLOSED) — data-dependency readiness: **READY_WITH_MODIFICATIONS** (`base_pct` needs a new pipeline; confidence promotion needs a hummus re-audit).
- **DEC-002** — hummus GO_LIVE_APPROVED. **DEC-003** — Launch Definition v1.

This document is the **single source of truth for building v2**. Where the spec
described *intent*, this reference states the *binding decision*. Conflicts resolve
in favor of this document; anything not stated here defers to v1.

> **Open conditions inherited from sign-off (do not block authoring; gate ship):**
> (1) **TASK-106** governing input not locatable — confirm TASK-098 + DEC-002 govern, or supply it before final Phase-1 sign-off. (2) The "TASK-119 readiness assessment" naming gap — TASK-111 is the source used. (3) Hummus confidence re-audit must pass before #6 ships. (4) QA must re-baseline at mobile + `lg` before Phase 1 ships. These are owner-assigned in §10.

---

## 0. Scope guardrail (read first)

**V2 is a presentation / IA migration only.** It changes layout and the
**view-model surface**; it **never** changes corpus content, product order, or
scoring. The metric block, confidence label, and rowReason are **display-only**,
derived deterministically from existing label data — **never new score inputs**.

---

## 1. Non-negotiable invariants (carried from v1 — LOCKED)

These carry forward unchanged. Everything in §3–§9 layers on top of them.

1. **Corpus owns order.** Rows render in `BariProductVM[]` array order (score-desc, insufficient last). No client re-sort. Filters subset and **preserve relative order**.
2. **Every product individually visible.** No clustering, no collapse-by-default, no hiding, no pagination-by-default. Insufficient-data products render a `"—"` no-score state.
3. **Pre-authored Hebrew, verbatim.** No runtime / LLM copy generation. Expansion fields render from the VM.
4. **No algorithm exposure.** No BSIP / NOVA / caps / dimension / routing language in user-facing strings.
5. **Interpretive-before-technical** hierarchy preserved inside the expansion (reasoning first; nutrition/ingredients muted below the hairline).
6. **Section identity preserved.** Expansion labels keep their strings and identity — especially **הקשר במדף** (not "בהשוואה לגרסה אחרת").
7. **Calm editorial tokens.** Off-white / graphite / emerald palette; no neon/cyber/wellness-blog tone. Metric color is information, not alarm (§4).

---

## 2. Data contract (`BariProductVM` / `ComparisonProduct`)

The aligned metric block, promoted confidence, and rowReason need structured fields
the current VM hides inside prose. Current VM
(`src/lib/comparisons/comparison-product.ts`) exposes: `id`, `name_he`,
`image_url`, `score`, `grade`, `insight_line`, `ingredients_he`,
`nutrition{energy_kcal, protein_g, sugar_g, fat_g, fiber_g, sodium_mg}`,
`confidence_level: "full" | "partial" | "insufficient"`.

### 2.1 Target v2 surface

```ts
score: number | null;
grade: BariGrade | null;                       // "A".."E"
confidence: "verified" | "partial" | "insufficient";   // RENAMED from confidence_level; accuracy-gated (§5)

metrics: {
  protein_g:      number | null;   // bar 0–20 g   — Phase 1 (exists in nutrition)
  additive_count: number | null;   // pips 0–5     — Phase 1 (derived, §4.2)
  base_pct:       number | null;   // bar 0–100 %  — DEFERRED to Phase 3 (§8)
  sodium_mg:      number | null;   // expansion only (exists)
  energy_kcal:    number | null;   // expansion only (exists)
};

rowReason: { positive: string | null; limiting: string | null };  // short, collapsed row (§3.3)
```

### 2.2 Field actions

| Field | Status | Action |
|---|---|---|
| `metrics.protein_g` | Exists (in `nutrition`) | Surface as first-class metric; display scale 0–20. |
| `metrics.additive_count` | Derivable | Add derived field from `ingredients_he` via the deterministic additive lexicon (§4.2). Pips 0–5; good ≤1, poor ≥4. Display-only. |
| `metrics.base_pct` | **Requires new pipeline** | **DEFER to Phase 3.** Not derivable from current label data (TASK-111, Data Agent). |
| `metrics.sodium_mg` / `energy_kcal` | Exists | Expansion-only; carry through. |
| `rowReason.{positive, limiting}` | Derivable | Short form from `positiveSignals[0]` / `limitingFactors[0]`. |
| `confidence` enum | **Mismatch** | **Rename `confidence_level: "full" → confidence: "verified"`**; keep `"partial"` / `"insufficient"`; apply the §5 gate. Update every consumer; no shim left in the VM surface. |

### 2.3 Null rule (applies to every metric — LOCKED)

Render **`"—"`, never `0`.** Two products with `additive_count` 1 vs 2 must remain
**visually distinguishable** — that distinguishability *is* the differentiator.
The numeric value is the source of truth; pips/bars are decorative.

---

## 3. Row layout (Phase 1, spec #1)

### 3.1 Density model — FROZEN

- **Dense row is the default.** A **density toggle** offers `compact` / `comfortable`.
- `compact` (default): thumb **44px**, tight padding.
- `comfortable`: thumb **60px**, relaxed padding ≈ current v1 row metrics.
- Density is presentation only — it does **not** change corpus, order, or which rows render. Persist the user's choice client-side; default `compact`.

### 3.2 Row grid (compact) — FROZEN

RTL logical layout, inline-start → inline-end:

```
rank | thumb(44) | name + reason (1fr) | metricBlock(~188px fixed) | grade + conf + chevron
```

- The **metric column is fixed width (~188px)** so values align vertically across
  rows. **That vertical alignment is the differentiator** — do not let it collapse
  to content width.
- `comfortable` mode widens the thumb to 60 and relaxes padding; the metric column
  stays fixed-width.
- Grade letter + score chip and the confidence indicator and chevron are grouped
  together at the inline-end (mirrors v1's "chevron beside score chip").

### 3.3 Collapsed-row reason — FROZEN (spec #5)

- Show **strongest +/−** beneath the name from `rowReason`:
  `positive` ← `positiveSignals[0]`, `limiting` ← `limitingFactors[0]`, short form.
- If both null, the reason slot collapses (no empty space), same as v1's hidden
  `insightLine` slot.

---

## 4. Metric block (Phase 1, spec #2) — FROZEN with launch-scope modification

**Column-aligned metric block per row** on shared, **category-scoped** scales, in
the fixed ~188px column.

### 4.1 What ships at launch — 2 of 3 metrics

| Metric | Display | Scale | "Good" / "Poor" thresholds | Source |
|---|---|---|---|---|
| `protein_g` | horizontal bar | 0–20 g | good ≥10, poor <5 | exists in `nutrition` |
| `additive_count` | 0–5 pips | 0–5 | good ≤1, poor ≥4 | derived (§4.2) |
| ~~`base_pct`~~ | (bar 0–100 %) | — | — | **DEFERRED → Phase 3 (§8)** |

- **`base_pct` (main-ingredient %) is EXCLUDED from v2 launch.** It requires a new
  main-ingredient extraction pipeline that does not exist (TASK-111, Data Agent).
- **The metric column MUST be built to accept the third bar later without
  re-layout** — reserve the slot; do not center the two-metric layout in a way that
  shifts when a third is added.

### 4.2 `additive_count` derivation (binding)

- Derived deterministically from `ingredients_he` against a **fixed additive
  lexicon** (committed in-repo, category-agnostic). Display-only; **not** a score input.
- Count distinct matched additive tokens; clamp display to 0–5 pips (value >5 still
  renders 5 pips but the `aria-label` states the true count).
- Missing/empty `ingredients_he` → `additive_count = null` → render `"—"` (never 0).
- The lexicon and matching rule are an authored derivation rule, not a pipeline; land
  them with Phase 1.

### 4.3 Color & scale rules — FROZEN

- Scales are **category-scoped** and shared across all rows in a category.
- Color: **good** (emerald) / **poor** (muted amber) at the thresholds above;
  **neutral grey otherwise**. Limits are information, not alarms — no red.
- Null → `"—"` per §2.3.

---

## 5. Confidence display (Phase 0 / v1-safe, spec #6) — FROZEN, gated

- **Confidence is promoted onto the collapsed row header**, out of the 10px
  expansion footnote. It appears with the grade/score chip group at the inline-end.
- **Accuracy gate (binding):** `verified` only when **≥3/6 nutrition fields present
  AND ingredients present**; else `partial`; null nutrition + ingredients →
  `insufficient` (no score). Rule per `confidence_label_audit_v1`.
- **VM enum rename:** `confidence_level: "full"` → `confidence: "verified"` (§2.2).
- **Ship gate:** confidence promotion must **not** ship until the **hummus
  confidence re-audit** passes (Blocker #3, §10). This is a **Phase-0, v1-safe**
  change — it does **not** require this v2 reference and may land on the frozen v1
  shelf ahead of Phase 1.
- Confidence label strings remain pre-authored (`expansion.confidenceLabel`); the
  row shows the state, the expansion top still carries source/label (§7).

---

## 6. Disclosure handling (Phase 0 / v1-safe, spec #8) — FROZEN

- **Category-level disclosures are stated once** in the **header / methodology**
  (e.g. the fat note, the relativity tag) — **not** repeated per row.
- **Per-row `unknowns` becomes product-specific only.** Category-wide gaps move out
  of the row into the header/methodology surfaces (existing surfaces; no new
  section above the shelf).
- This is a **Phase-0, v1-safe** change (no v2 reference required); it retires
  duplicated copy and uses surfaces that already exist.

---

## 7. Expansion behavior (Phase 1, spec #7) — FROZEN

- **Confidence + source at the top** of the expansion.
- **Nutrition surfaces at reason level**; the **second "advanced" toggle is
  dropped** (one disclosure, not two).
- **Magnitude shown on limiting factors** (e.g. how much, not just that it limits).
- **Label strings and section identity preserved** — interpretive blocks → hairline
  → technical block; **הקשר במדף** unchanged. Section order stays:
  positive → limiting → bottom line → shelf context → hairline → technical
  (nutrition grid, ingredients, confidence/source).
- **Expand interaction (changed from v1):**
  - **Do NOT `scrollIntoView` on expand** — it yanks long lists. (v1 did; v2
    removes it. Only the band rail scrolls, on explicit click — §9.2.)
  - **Multiple rows may be open simultaneously.** Expand/collapse is a per-row
    toggle button.
  - Initial state: do not force-open on load for dense lists (v1's
    `initialExpandedProductId` behavior is dropped under v2 density; rows open on
    user action).

---

## 8. Phase 1 vs deferred — EXPLICIT

### 8.1 In Phase 1 (this reference authorizes build once gated)

- #1 Density model + toggle (§3.1)
- #2 Metric block — **protein + additives ONLY** (§4)
- #5 Strongest +/− on the collapsed row via `rowReason` (§3.3)
- #7 Expansion restructure (§7)
- #9 Responsive table layout (§9.1, §9.3 dense-from-`lg` + mobile single-column)
- VM work: `metrics.{protein_g, additive_count}`, `rowReason`, `confidence` enum reconcile (`full → verified`)

### 8.2 Phase 0 (v1-safe — may ship before Phase 1, no v2 ref needed)

- #6 Confidence promotion + accuracy gate (§5) — **gated on hummus re-audit**
- #8 Category-disclosure de-dup + relativity tag (§6)

### 8.3 Phase 2 (navigation chrome — depends on Phase-1 row/band geometry)

- #3 Score-band rail (§9.2)
- #4 Inline band dividers (§9.2)
- Header score-distribution histogram (§9.4)

*Why after Phase 1: the rail/dividers/histogram attach to v2 row/band geometry;
building them before the layout is fixed would couple to a moving target.*

### 8.4 Deferred to Phase 3 (externally blocked — does NOT gate launch)

- **`base_pct`** third metric bar (#2 completion) — blocked on the main-ingredient
  extraction pipeline (TASK-111, **Data Agent**). The metric column is built to
  admit it without re-layout (§4.1). Per DEC-003, `base_pct` does **not** gate launch.

### 8.5 Rejected — NEVER in any phase (TASK-098 "Explicitly rejected")

- Clustered / equivalent-product groups.
- Alternative sort modes (protein / additives / "Bari" views) — corpus owns order.
- Any hiding or pagination-by-default.
- `scrollIntoView`-on-expand (replaced by explicit rail-only scroll, §7/§9.2).

---

## 9. Responsive behavior

### 9.1 Responsive system (Phase 1, spec #9) — FROZEN

- **Dense, table-like layout from `lg`**; **single-column rows on mobile**.
- **Ends the 375px desktop phone-frame** (v1 item 10) and the hummus-vs-others
  375px drift. The v2 shelf is allowed to use real desktop width — this is the one
  v1 invariant v2 explicitly **replaces** (a new reference version was the
  precondition; this is it).
- **Mobile parity = same IA, narrower.** Identical information architecture, not a
  reduced one. Same rows, same metric block (stacked within the narrower row), same
  expansion content.

### 9.2 Mobile behavior — FROZEN

- **Single-column rows.** The fixed metric column collapses to a stacked metric
  group within the row; protein bar + additive pips remain present and aligned
  within the row.
- **Band rail hidden < 680px** (§9.3). Inline band dividers (Phase 2) still render
  on mobile as in-list separators.
- No horizontal scroll; no phone-frame chrome (no `max-w-[375px]`, no rounded
  frame/shadow on the shelf).
- Expand interaction per §7 (no `scrollIntoView`; multiple open allowed).

### 9.3 Desktop behavior — FROZEN (layout) / Phase 2 (chrome)

- **Dense table-like grid from `lg`** with the fixed ~188px metric column aligned
  across rows (§3.2). This is the Phase-1 desktop layout.
- **Score-band jump rail (Phase 2, spec #3):** sticky **side** rail, positioned
  **inline-end (RTL)**, **hidden < 680px**. Bands **80+ / 70s / 60s / 50s / <50**,
  derived from `score`, contiguous in corpus order. Each band shows **label + count
  + a proportion bar** tinted by band (green → amber as score drops).
  **Click = scroll only** (`scrollTo(firstRowOfBand, -offset)`). The rail **never
  reorders or regroups** rows; it is a side affordance, not a section above the shelf.
- **Inline band dividers (Phase 2, spec #4):** pure in-list visual separators; they
  **do not regroup or reorder** rows. Allowed within the "no new section above the
  shelf" invariant because they are in-list.

### 9.4 Header histogram (Phase 2, spec §Layout) — FROZEN

- **Score-distribution histogram in the header** (buckets 40–47 … 80+),
  **highlighting the dominant cluster band**.
- **Static, read-only.** Derived from existing `score`. Not interactive, does not
  filter or reorder.

---

## 10. Accessibility / RTL — FROZEN

- All logical properties (`inset-inline`, `ms`/`me`); no physical left/right.
- **Metric `aria-label`s** carry the numeric truth: e.g. `"חלבון 7.9 גרם"`,
  `"2 תוספי מזון"`. Pips/bars are decorative; the numeric value is authoritative.
- **Rail `aria-label`s** state band + count; rail items are buttons (scroll action).
- **Grade announced as letter + number** both.
- Expand/collapse is a real button per row; respect `prefers-reduced-motion`.
- Do **not** use `scrollIntoView` on expand (§7). Only the rail scrolls, on explicit
  click.

---

## 11. Migration & pilot (from TASK-118)

Per-route and reversible behind the layout switch; the metric block degrades cleanly
to `"—"` on any category whose corpus lacks a field.

| Order | Category | State | Note |
|---|---|---|---|
| 1 (pilot) | **hummus** | LIVE gen1, 69 prod | Spec source of truth; confidence re-audit is hummus-scoped; HUM-001 (fat suppressed) / HUM-002 (sugar absent) don't touch the protein+additives block. |
| 2 | maadanim | LIVE gen1, 90 prod | The frozen v1 reference category — re-baseline onto v2 second. |
| 3 | snacks | LIVE gen1, 53 prod | Clean gen1 swap. |
| 4 | yogurts | LIVE gen1, 45 prod | Clean gen1 swap. |
| 5 | bread | LIVE gen1, 80 prod | Largest live corpus — late-stage stress test for bands/rail/histogram. |
| 6 | milk | LEGACY gen0, 20 prod | Carries gen0→gen1 (MILK-001) before v2; sequence after the gen1 fleet (TASK-128E, post-launch per DEC-003 Amendment A). |
| n/a | breakfast-cereals, tahini | NOT_STARTED | Born on v2 — build directly to this reference; no migration step. |

**Pilot exit criteria (hummus):** v2 reference signed; metric block renders protein +
additives with correct `"—"` null states; confidence accuracy gate passing on the
re-audited hummus corpus; rail jump lands on the correct first row of each band;
filtered views preserve corpus order; no product removed from the DOM by any control;
fresh **mobile + `lg`** QA baselines captured. Only then promote maadanim (order 2).

---

## 12. Open conditions & owners (gate ship, not authoring)

| # | Condition | Gates | Owner |
|---|---|---|---|
| 1 | **TASK-106** input not locatable — confirm TASK-098 + DEC-002 govern, or supply it | Final Phase-1 sign-off | Central Controller / Product |
| 2 | TASK-119/TASK-111 naming gap (TASK-111 used) | Final Phase-1 sign-off | Central Controller |
| 3 | Hummus confidence re-audit | Phase 0 #6 (§5) | Data / QA |
| 4 | QA re-baseline at mobile + `lg` (v1's 375px snapshots invalid) | Phase 1 ship | QA |
| 5 | `base_pct` extraction pipeline | Phase 3 only (not launch) | Data Agent |

---

## 13. QA / acceptance — binding assertions

Before any v2 route ships, QA must assert:

- [ ] Filtered views **preserve corpus order**; no client re-sort.
- [ ] No product is **removed from the DOM** by any control (filter, density, rail).
- [ ] Null metrics render **`"—"`, never `0`**; `additive_count` 1 vs 2 visually distinct.
- [ ] Confidence gate: `verified` only with ≥3/6 nutrition + ingredients; else `partial`/`insufficient`.
- [ ] Expansion: confidence+source on top; one disclosure (no 2nd advanced toggle); `הקשר במדף` label intact; **no `scrollIntoView` on expand**; multiple rows open OK.
- [ ] Responsive: dense from `lg`, single-column on mobile, **no 375px frame**; same IA both widths.
- [ ] (Phase 2) Rail hidden < 680px; **click = scroll only**, lands on the correct first row of each band; dividers do not reorder.
- [ ] Fresh baselines captured at **mobile + `lg`**; v1 375px-only snapshots retired.
- [ ] `npm run lint` + `npm run build` clean.

---

## 14. Sign-off

| Role | Owner | Status |
|---|---|---|
| Authoring (this reference) | frontend-agent (TASK-128A) | **Signed — authored 2026-06-01** |
| Design / Product countersign | design-agent / product-agent | Pending |
| Controller acceptance (closes TASK-128A; opens Phase 1 build) | Central Controller | Pending |

This document **satisfies the authoring half** of TASK-128's prerequisite gate
(roadmap Blocker #2 / sign-off condition 3). The **sign half** (design/product
countersign + Controller acceptance) plus open conditions §12 must clear before
Phase-1 code begins. Phase 0 (§8.2) may proceed independently once condition 3 clears.

---

*Binding reference. Layout and view-model surface only — no corpus, order, or scoring
change. Anything unstated here defers to `comparison_ui_reference_v1.md`.*
