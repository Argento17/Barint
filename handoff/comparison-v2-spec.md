# Comparison UI — v2 direction spec (accepted v-next-2)

**Status:** Accepted direction (TASK-098). Engineering-facing translation of the `ui_kits/web/index.html` prototype into build decisions. This is the basis for a `comparison_ui_reference_v2.md`; it does **not** ship on frozen v1 without that reference.

**Source of truth:** `bari.digital/hashvaot/hummus` (live) + this prototype. Reference v1 = `comparison_ui_reference_v1.md` (frozen). DEC-002 gating = `Bari TASK-091 DEC-002 Decision.html`.

---

## Non-negotiable invariants (carried from v1)

1. **Corpus owns order.** Rows render in `BariProductVM[]` array order (score-desc, insufficient last). No client re-sort. Filters subset and **preserve relative order**.
2. **Every product individually visible.** No clustering, no collapse-by-default, no hiding. Insufficient-data products render with a "—" no-score state.
3. **Pre-authored Hebrew, verbatim.** No runtime copy generation. Expansion fields render from the VM.
4. **No algorithm exposure.** No BSIP/NOVA/caps/dimension language in user-facing strings.
5. **Interpretive-before-technical** hierarchy preserved inside the expansion.

Everything below changes **presentation/IA**, never order or corpus content.

---

## What changes vs v1 (and why it needs a v2 reference)

| # | Change | Frozen-v1 clause it touches | Rule for v2 |
|---|---|---|---|
| 1 | **Dense row by default** + density toggle (compact/comfortable) | ProductRow layout | New row spec; comfortable mode ≈ current v1 row metrics |
| 2 | **Column-aligned metric block** per row (protein · additives · base %) on shared scales | ProductRow layout | Requires VM to expose `protein_g`, `additive_count`, `base_pct` as first-class fields (see Data) |
| 3 | **Score-band jump rail** (80+/70s/60s/50s/<50) | new chrome (no new section *above* shelf — rail is a side affordance, not a section) | Bands derived from `score`; contiguous in corpus order; click = scroll only |
| 4 | **Inline band dividers** in the list | "no new sections above the shelf" — these are *in-list* dividers, allowed | Pure visual separators; do not regroup or reorder rows |
| 5 | **Strongest +/− on the collapsed row** | row header (insightLine slot) | Derive from `positiveSignals[0]` / `limitingFactors[0]`; short form |
| 6 | **Confidence promoted onto the row** | row header | Move confidence out of the 10px expansion footnote; gate accuracy per `confidence_label_audit_v1` |
| 7 | **Expansion: confidence+source top; nutrition at reason level (drop 2nd "advanced" toggle); magnitude on limits** | fixed expansion order | New expansion spec; keep label strings + section identity (`הקשר במדף` etc.) |
| 8 | **Category-level disclosures once** (fat note, relativity) in header, not per row | expansion `unknowns` content | Move category-wide gaps to header/methodology; per-row `unknowns` = product-specific only |
| 9 | **Responsive width** — dense table-like layout from `lg`, single-column rows on mobile; ends the hummus-vs-others 375px drift | item 10 "375px desktop frame" | Explicit v2 responsive system; mobile parity = same IA, narrower |

**Explicitly rejected** (per TASK-098, do not implement): clustered/equivalent-product groups; alternative sort modes (protein/additives/Bari views); any hiding or pagination-by-default.

---

## Data contract additions (`BariProductVM`)

The aligned metric block and pips need structured fields the current VM hides inside prose:

```
score: number | null
grade: "A"|"B"|"C"|"D"|"E" | null
confidence: "verified" | "partial" | "insufficient"   // accuracy-gated (audit rule)
metrics: {
  protein_g:   number | null,   // bar scale 0–20
  additive_count: number | null,// pips 0–5; good ≤1, poor ≥4
  base_pct:    number | null,   // main-ingredient %, bar 0–100
  sodium_mg:   number | null,   // expansion only
  energy_kcal: number | null,   // expansion only
}
rowReason: { positive: string | null, limiting: string | null }  // short, for collapsed row
```

- `metrics` are display-only, derived deterministically from existing label data; **not** new score inputs.
- Where a field is null, render "—" (never zero). Two products with `additive_count` 1 vs 2 must be visually distinguishable — that is the differentiation mechanism.
- `confidence`: apply the audit rule — `verified` only when ≥3/6 nutrition fields **and** ingredients present; else `partial`; null nutrition+ingredients → `insufficient` (no score).

---

## Layout rules

- **Row grid (compact):** `rank | thumb(44) | name+reason(1fr) | metricBlock(~188px fixed) | grade+conf+chevron`. Fixed metric column = vertical alignment across rows (the differentiator). Comfortable mode widens thumb to 60 and relaxes padding.
- **Band rail:** sticky, side (inline-end on RTL), hidden < 680px. Each band shows label + count + a proportion bar tinted by band (green→amber as score drops). Click → `scrollTo(firstRowOfBand, -offset)`.
- **Metric scales (shared, category-scoped):** protein 0–20 g; additives 0–5 pips; base 0–100 %. Color: protein good ≥10 / poor <5; additives good ≤1 / poor ≥4. Keep neutral grey otherwise — limits are information, not alarms.
- **Histogram (header):** score distribution buckets (40–47 … 80+), highlighting the dominant cluster band. Static, read-only.

## Accessibility / RTL

- Rail and pips need `aria-label`s ("חלבון 7.9 גרם", "2 תוספי מזון"). Pips are decorative; the numeric `mv` is the source of truth.
- Expand/collapse via row button; multiple rows may be open. Do **not** use `scrollIntoView` on expand (it yanks long lists); only the rail scrolls, on explicit click.
- All logical properties (`inset-inline`, `ms/me`); grade letter + number both announced.

## Build sequencing (maps to DEC-002 decision)

- **Pre-DEC002 (v1-safe, no reference change):** #6 confidence promotion + accuracy gate (A1/A2 in the decision doc), #8 category-disclosure de-dup, relativity tag.
- **v2 (this spec):** #1 density, #2 metric block, #3 rail, #4 dividers, #7 expansion restructure, #9 responsive table. Requires `comparison_ui_reference_v2.md` sign-off and re-baselined QA (375px snapshots obsolete).

## QA notes

- Re-capture baselines at mobile + `lg` (v1's 375px-only snapshots are invalid for v2).
- Assert: filtered views preserve corpus order; rail jump lands on the correct first row; null metrics render "—"; no product is removed from the DOM by any control.
