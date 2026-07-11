# Magnesium Guide — Per-Bar Threshold Infographic — Visual Spec v1

**Component:** NEW canonical component — `ThresholdBarRow` (guide surface only, not `/hashvaot`)
**Route reviewed live:** `http://localhost:4700/madrichim/magnesium` (worktree `C:\bari_wt_t504\bari-web`, TASK-504)
**Author:** Design Agent — spec only. No production code touched.
**Status:** Awaiting Frontend Agent implementation + this agent's post-build conformance pass (plan §6 gate, referenced in `guide-product-row.tsx` header comment).
**Decision right:** D11/D12 — this spec is the approval Frontend needs before building. Do not build a variant.

---

## 0. What I actually saw (evidence, not assertion)

Rendered at 375×812 (mobile) and 1440×900 (desktop), screenshots + DOM geometry pulled via Playwright against the live worktree route.

**Finding A (the real bug, worse than "no threshold marker"):** the six bar-state badges on every product row have **no visible bar-name label at all.** Measured `aria-label` on each badge is `"מינון: עם דגל"`, `"צורה וספיגה: עומד בסף"`, etc. — but the **rendered text node only shows the state word** (`עם דגל` / `עומד בסף` / `לא ניתן לאמת`). The bar identity exists only in the accessibility tree, invisible to a sighted user. Screenshot `mag-mobile-table.png`: two rows of pastel pills, zero pill carries a visible name. A sighted reader can only recover "which pill is dose" by memorizing badge order — which is exactly the owner's complaint, not a milder version of it.

**Finding B:** `product.benchmark` (`magnesium-guide-data.ts:85-101`) is a **single field per product**, wired to the dose bar only (or swapped to the UL line via `ulBenchmark()` for the four oxide products where safety is the deciding fact — see file header note). Screenshot `mag-mobile-table.png` / `mag-row-10.png` confirm: one benchmark caption line renders under the badge row (`טווח המינון היעיל: 300 מ"ג יסודי ליום ומעלה · המוצר: 136 מ"ג`), the other 3–5 bars get nothing beyond their bare pill. This matches the owner's "you don't know what it refers to" verbatim.

**Finding C:** the promoted bucket header ("הרשימה המעשית להתחיל ממנה (5)", desktop screenshot `mag-desktop-table.png`) is a title + count in a green box with no sub-line explaining the qualification rule. A reader cannot tell from the header alone whether "practical list" means "these are good" or "these are the least-bad." The actual rule ("לא נכשלים באף סף, אבל לפחות אחד מסומן כחלקי או לא ניתן לאימות") already exists verbatim in `headlineFinding.body[2]` but is buried three paragraphs above the table, not attached to the header itself.

**Finding D (precedent already exists — reuse it):** `bari-comparison-tokens.ts:98-112` (`GRADE_DOT_POSITION` / `gradeDotOffset`) already ships a colorblind-safe percentage-position marker along a graded accent bar, used on `ScoreChip` (`score-chip.tsx:54-63`) — a small white dot placed at `top: gradeDotOffset(palette.dot)` along a 5-zone vertical strip. This is the frozen system's own precedent for "marker positioned by percentage along a graded range." The spec below is that same mechanism rotated horizontal and re-scaled to a real numeric domain — **not a new visual language.**

**Finding E:** `GUIDE_BAR_TONE` (`bar-state-badge.tsx:35-43`) already carries a dedicated, WCAG-AA-checked, guide-only 4-tone palette (teal/indigo/berry/gray) deliberately shifted off `gradePalette` so guides never read as a second grade axis. Every color used below is drawn from this existing palette — no new hue is introduced anywhere in this spec.

---

## 1. Scope

Per-bar threshold display for the **four discriminating bars** — `doseAdequacy`, `formAbsorption`, `safety`, `labelTransparency` — per the parallel Product decision to suppress `thirdPartyVerification` and `priceFairness` (uniformly `cannot_verify` for every one of the 18 magnesium products; zero discriminating signal). If Product reverses that suppression, this same anatomy extends to those two bars unchanged — `thirdPartyVerification` is a 2-tier ladder (directory-confirmed / manufacturer-stated), `priceFairness` is a continuous-scale gauge (₪/effective-mg vs market median) — but that is out of scope until Product confirms.

Two anatomies cover all four bars:

| Anatomy | Bars | Why |
|---|---|---|
| **Threshold Gauge** (continuous scale) | `doseAdequacy`, `safety` | Both are a real mg number compared against a numeric line (300mg floor; 250/350mg bands) |
| **Threshold Ladder** (discrete tier) | `formAbsorption`, `labelTransparency` | Both are an ordinal category (absorption tier; disclosure tier), not a number — a numeric gauge would fabricate false precision |

---

## 2. Anatomy — Threshold Gauge (dose, safety)

```
מינון                                                    ⬤ עם דגל
┌──────────────────────────────────────────────────────────────┐
│ ░░░░░░░░░░░░░|▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒|●▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ │  ← track, dir="ltr" forced
└──────────────────────────────────────────────────────────────┘
  0                150 (חצי סף)          300 (הסף)
  המוצר: 250 מ״ג · לא מגיע לסף המלא (300 מ״ג)
```

- **Track:** height 6px, `border-radius: var(--radius-pill)` (9999px, existing token), background `#EDEFEC` (neutral, matches row/card grays already in `colors_and_type.css`).
- **Zone fill (informational, always renders — it's the fixed external standard, true regardless of this product):** three contiguous segments tinted with the *background* tone of the matching `GUIDE_BAR_TONE` entry at low opacity, **plus a 1px solid divider line at every zone boundary** — the divider is mandatory, not optional, so zone edges read in grayscale/color-blind simulation, not by hue alone (WCAG 1.4.1 — never color-only). Dose zones: `0–150mg` fail-tint, `150–300mg` flag-tint, `300mg–domain-max` pass-tint. Safety zones: `0–250mg` pass-tint, `250–350mg` flag-tint (EFSA soft caution line, **dashed** divider — advisory, not a fail), `350mg–domain-max` fail-tint (UL line, **solid** divider — hard boundary).
- **Domain + overflow rule:** dose gauge domain is `0–360mg` (60mg headroom past the 300mg floor so the pass zone reads as a real zone, not a sliver). Products above 360mg (the four 450–520mg oxide products) **clamp the marker at the domain's end** with a small `+` glyph beside it — do not stretch the domain to fit outliers, or the 250–300 range these bars exist to communicate becomes visually meaningless. The exact value stays in the caption text regardless of clamp. Safety gauge domain is `0–400mg` for the same reason (350mg UL + headroom).
- **Product marker:** a filled circle, 10px diameter, 2px white border (for contrast against the tinted zone under it), color = the *text* tone of the bar's current `GUIDE_BAR_TONE` state (so a FLAG dose bar gets the indigo `#2E3C86` marker, a FAIL gets berry `#84184F`, matching the badge beside it — one color vocabulary, not two). Positioned via `left`/`right` percentage exactly like `gradeDotOffset()` — same mechanism, new domain math (`clamp(value, 0, domainMax) / domainMax * 100%`).
- **Tick labels:** 11px (matches existing badge font-size — already contrast-verified in this codebase, do not go smaller), color `#6B7070`, positioned under each zone boundary tick, plus `0` at the start. Do not label every mg value — only the meaningful anchors (150/300 for dose; 250/350 for safety).
- **Caption line (replaces today's single `benchmark` text, now local to each gauge):** 12px, `#4E5663`, format `המוצר: {productValueLabel} · {short verdict clause}` — the verdict clause is Content's existing per-bar `note` field (`GuideBarResult.note`), rendered verbatim, never invented here.
- **Bidi handling (RTL risk — flag for Frontend + QA):** the gauge track itself must be wrapped in a `dir="ltr"` element so the numeric scale reads conventionally low-to-high left-to-right, matching how virtually every numeric axis (charts, sliders, dose lines) renders even inside RTL pages — mirroring it (high-to-low left-to-right) to "match" page direction would be a novel, unfamiliar convention with no existing Bari precedent. The bar-name label, state badge, and caption text around the gauge stay `dir="rtl"` as normal. **This is a judgment call, not a frozen fact — Frontend should confirm with one native-Hebrew-reader pass before shipping**, since gauge-direction-in-an-RTL-context is a genuine ambiguity zone this agent cannot resolve by measurement alone.

### Gauge — state-by-state rendering

| State | Marker | Caption |
|---|---|---|
| **PASS** (e.g. dose 250mg → wait, 250 is FLAG not PASS in this data; illustrative: a hypothetical 320mg product) | Filled teal dot inside the pass-tint zone | `המוצר: 320 מ״ג · עומד בסף המלא` |
| **FLAG** (dose 250mg, SupHerb Citrate+B6, row 1) | Filled indigo dot inside the flag-tint zone, sitting near the 300 boundary | `המוצר: 250 מ״ג · מתחת לסף (300 מ״ג), מעל מחצית הסף` |
| **FAIL** (dose 76mg, Nutricare Taurate) | Filled berry dot deep inside the fail-tint zone, near the 0 end | `המוצר: 76 מ״ג · משמעותית מתחת למחצית הסף` |
| **FAIL, over-UL** (safety, 520mg oxide products) | Filled berry dot **clamped at the domain end + `+`** | `המוצר: 520 מ״ג · חוצה את הסף הבטיחותי (350 מ״ג)` |
| **CANNOT_VERIFY** (dose, TRIOMAG / Tink 520 / Amorphicure) | **No marker rendered at all.** Track still shows the three tinted zones (the standard is a fact independent of this product) but with a dashed-outline placeholder ring (hollow, gray `#4E5663`, matching the badge's hollow-dot convention in `bar-state-badge.tsx:112-119`) fixed at the gauge's midpoint, never implying a real position | `המוצר: לא ניתן לאימות · {note, e.g. "מינון לכמוסה בלי מספר כמוסות ליום"}` |

The CANNOT_VERIFY row is the one the owner explicitly called out ("keep it honest, no fake position") — the placeholder ring is deliberately mid-track and hollow so it cannot be misread as a real low/mid/high value; it is a "we don't know" glyph, not a "medium" glyph.

---

## 3. Anatomy — Threshold Ladder (form, label transparency)

```
צורה וספיגה                                              ⬤ עומד בסף
┌───────────┬───────────┬───────────┐
│  נמוכה    │  בינונית   │ ▓▓גבוהה▓▓ │  ← dir="ltr", current tier filled + ▲ caret above it
│ אוקסיד/   │ מלאט/טאוראט│ ציטראט/   │
│ קרבונט    │ /הידרוקסיד │ ביסגליצינט│
└───────────┴───────────┴───────────┘
המוצר: ציטראט · קבוצת הספיגה הגבוהה
```

- **Track:** 3 equal-width segments in a single connected pill/rail, `border-radius: var(--radius-pill)` on the outer corners only, 1px dividers between segments (same divider discipline as the gauge — never color-only).
- **Segment fill:** the product's current tier segment fills with the bar's state-tone background (`GUIDE_BAR_TONE[state].bg`); the other two segments stay neutral (`#F3F4F2`, the existing `cannot_verify` gray — reused here as "not this tier," not as a state).
- **Caret marker:** a small filled triangle (▲, 6px) above the current-tier segment, colored to the state's text tone — this is the ladder's equivalent of the gauge's dot, and doubles the signal (fill + caret) so tier identity survives even if segment-fill contrast is marginal on a given screen.
- **Segment sub-label:** 10px, `#6B7070`, listing the 2–3 chemical forms that live in that tier (already fully enumerated in `magnesium-guide-data.ts` educationSpine "הצורות הכימיות, מוסבר שוב בקצרה" — port those groupings verbatim, do not re-derive).
- **Direction:** left = worst tier, right = best tier is **wrong** for a `dir="ltr"` internal convention — to stay consistent with the gauge above (low value at the LTR-left, high/good value at the LTR-right), the ladder uses the same left→right = worse→better ordering. State it once, apply identically to both anatomies so a reader only learns the convention once.

### Ladder — state-by-state rendering

| State | Rendering |
|---|---|
| **PASS** (form, e.g. Nutricare WELL — bisglycinate) | High tier segment filled teal, caret teal, caption `המוצר: ביסגליצינט · קבוצת הספיגה הגבוהה` |
| **FLAG** (form, e.g. NT L.C. — hydroxide) | Medium tier filled indigo, caret indigo, caption names the tier + the specific form |
| **FAIL** (form, e.g. any 520mg oxide product) | Low tier filled berry, caret berry, caption `המוצר: אוקסיד · קבוצת הספיגה הנמוכה ביותר` |
| **CANNOT_VERIFY** (form, TRIOMAG — undisclosed 3-form blend) | **All three segments stay neutral gray, no fill, no caret anywhere.** Caption swaps to the existing `note`: `לא ניתן לקבוע רמת ספיגה · תערובת לא-גלויה` |

Label-transparency ladder uses the identical structure with 3 tiers = `גלוי במלואו` / `חלקי` / `לא גלוי כלל` instead of absorption tiers — same fill/caret/caption rules, same CANNOT_VERIFY fallback (only relevant if a labelTransparency bar is ever itself unverifiable, which the current 18-product dataset does not exhibit — `labelTransparency` is always pass/flag/fail in the live data).

---

## 4. Per-bar row assembly (both anatomies share this frame)

Replaces the current flat 6-badge-wrap grid (`guide-product-row.tsx:126-139`) with **one stacked row per discriminating bar**, in `GUIDE_BAR_ORDER` sequence (dose → form → safety → transparency, skipping the two suppressed bars):

```
┌─ bar row ───────────────────────────────────────────────┐
│ {GUIDE_BAR_LABELS_HE[bar]}                {StateBadge}   │  ← 11px semibold label, badge unchanged
│ {gauge or ladder, full available width}                  │  ← 6-8px gap above/below
│ {caption line}                                           │  ← 12px, #4E5663
└───────────────────────────────────────────────────────────┘
   12px gap between bar rows
```

- **Mobile (≤767px):** stacked as drawn above. Measured available width for the content column after the 56px thumbnail + 12px gap + 2×16px row padding + 2×16px section padding is **~243px** at 375 viewport — the gauge/ladder must fit inside this, so keep it edge-to-edge of the text column, no side margins of its own.
- **Desktop (≥768px):** bar-name + badge stay on one line; gauge/ladder + caption move to sharing a row (`flex`, gauge fixed max-width 260px so it doesn't stretch thin across the ~1052px available column measured on the live 1440px render, caption text flows in the remaining space at its start side).
- **If a bar must still render as `cannot_verify`** and is one of the two *suppressed* bars (`thirdPartyVerification`, `priceFairness`) that Product is hiding entirely: **do not render the row at all** — that is the suppression, not a fallback state. The fallback rendering in §2/§3 above is only for a discriminating bar (dose/form/safety/transparency) landing on `cannot_verify` for an individual product (TRIOMAG, the two undisclosed-dose Tink/Amorphicure rows), which still must render honestly, never be hidden.

---

## 5. Bucket header pattern (owner fix #3)

Current (`guide-product-table.tsx:81-108`): mono-uppercase label + `(count)` + rule, optionally boxed green when promoted. Screenshot `mag-desktop-table.png` confirms the promoted header ("הרשימה המעשית להתחיל ממנה (5)") carries no explanation of the qualification rule.

**Fix — add a mandatory sub-caption slot under every bucket header**, 12px, `#6E756D` (methodology-adjacent tone, not attention-grabbing), one line, stating the bucket's actual qualification rule in plain words:

```
┌─────────────────────────────────────────┐
│ הרשימה המעשית להתחיל ממנה          (5)   │  ← existing header, unchanged
│ לא נכשלים באף סף, אבל לפחות אחד מסומן    │  ← NEW sub-caption, 12px
│ כחלקי או לא ניתן לאימות                  │
└─────────────────────────────────────────┘
```

- **Content discipline:** this sub-caption is a **content slot, not Design-authored copy.** For the `passes_with_flag`/promoted case the exact sentence already exists verbatim in `headlineFinding.body[2]` (`magnesium-guide-data.ts:371`) — reuse that fragment, do not re-derive. For `fails` and `cannot_assess`, no equivalent one-liner exists yet in the gate-1-approved copy doc; **Content Agent must author these two, through the standard two-gate sign-off**, before Frontend wires them in. Do not ship a Design- or Frontend-invented placeholder as final copy.
- **Structural requirement regardless of final wording:** every bucket — not just the promoted one — gets this sub-caption line. An un-promoted "לא עובר (11)" header with no sub-line has the exact same "clean label, no reference" problem the owner flagged for the bars; the fix is symmetric.
- **`clears_all` bucket:** currently never renders on the magnesium page (0/18 clear all six — `headlineFinding` note, `magnesium-guide-data.ts:20`), but the sub-caption pattern must still be defined for it now so the component doesn't need a second design pass the day a product clears all bars: `"עומד בכל שישה הספים בלי יוצא מן הכלל."`

---

## 6. Tokens / geometry reference (cite, don't invent)

| Element | Value | Source |
|---|---|---|
| Track radius | `9999px` | `--radius-pill`, `colors_and_type.css:64` |
| Card/row radius | `18px` (`rounded-2xl`) | already used in `guide-product-row.tsx:83`, do not change |
| Badge font-size | `11px` | `bar-state-badge.tsx:88` — reused verbatim for bar-name label and tick labels, do not go smaller |
| Caption font-size | `12px`, `#4E5663` | matches existing `product.oneLinerHe` treatment style family (`guide-product-row.tsx:144-151`) |
| Bucket sub-caption | `12px`, `#6E756D` | adjacent to the existing methodology tone (`#666C67`/`#AAAAAA` family per frozen Methodology spec) — not identical, deliberately slightly darker since this sits inside interactive content, not the page-level methodology footer |
| Marker-position mechanism | percentage `left`/`right` + `transform: translateY(-50%)` equivalent | precedent: `gradeDotOffset()`, `bari-comparison-tokens.ts:110-112`, consumed in `score-chip.tsx:54-63` |
| State colors (marker, caret, segment fill) | `GUIDE_BAR_TONE` — teal `#0B5D52`/`#E2F2EF`, indigo `#2E3C86`/`#EAEDF8`, berry `#84184F`/`#F8E7EF`, gray `#4E5663`/`#F3F4F2` | `bar-state-badge.tsx:35-43` — reused exactly, no new hex introduced |

---

## 7. WCAG / RTL risk register for Frontend

1. **Zone-boundary color-only risk (WCAG 1.4.1):** mandatory 1px divider lines at every zone boundary, independent of tint hue — spec'd in §2, do not drop this as a "nice to have."
2. **Marker-only-by-color risk:** the marker/caret always pairs with a shape difference too (filled circle vs hollow ring for cannot_verify; caret present/absent for the ladder) — never rely on the teal/indigo/berry/gray distinction alone, consistent with the existing badge's filled/hollow dot convention.
3. **Tick-label contrast:** verify `#6B7070` on the `#EDEFEC` track background and on each zone tint clears 4.5:1 (small text) at implementation time — the tone was chosen to match existing values but the *combination* against a tinted zone specifically hasn't been axe-tested yet; run `npm run test:a11y` after build, this spec does not substitute for that measurement.
4. **RTL gauge-direction ambiguity (flagged above, §2):** forcing `dir="ltr"` on the numeric gauge internals inside an otherwise RTL row is the right call by precedent (no existing Bari component mirrors numeric scales for RTL) but has not been screen-reader-tested; Frontend should get one native-Hebrew read-through before this ships, and this agent will re-render and re-measure post-build regardless.
5. **Accessible name completeness:** the bar-name label becoming visible text (§4) does not remove the need for `BarStateBadge`'s existing `aria-label` construction (`barLabel`) — keep both; a screen-reader user should still hear "מינון: עם דגל" as one phrase, not rely on adjacent-DOM-node inference.
6. **Do not let this migrate into `/hashvaot`.** This component is guide-surface-only (`GuideProductVM`, no score/grade). Nothing here should be read as license to add threshold gauges to the canonical A–E comparison rows — that surface stays frozen per the golden-page reference (`golden_comparison_page_brined`).

---

## 8. Explicit non-goals (conformance discipline)

- No numeric score or letter grade introduced anywhere in this component — bars stay PASS/FLAG/FAIL/CANNOT_VERIFY, gauges/ladders visualize *where a raw measured value sits against an external standard*, they never compute or imply a rolled-up score.
- No new color hue — every color cited above already exists in `GUIDE_BAR_TONE` or `gradePalette`-adjacent-but-distinct guide tokens.
- No product-vs-product comparison — every marker/caret is product-vs-EXTERNAL-STANDARD only, preserving the `GuideBenchmarkPlacement` contract's existing rule (`view-models/guide.ts:93-106`, red-team RT-A3). The VM contract needs to change from one `benchmark: GuideBenchmarkPlacement | null` field per product to one per discriminating bar (e.g. `benchmarks: Partial<Record<GuideBarKey, GuideBenchmarkPlacement>>`) — that VM/type change is Frontend's implementation call to make correctly, not re-specified here, but flagging it since today's singular field cannot carry 4 independent benchmarks as-is.

---

## Return Contract

```json
{
  "artifacts": [
    {
      "path": "C:\\Bari\\03_operations\\reports\\design\\magnesium_guide_threshold_infographic_spec_v1.md",
      "sha256": "1b6da50422ab4ddc422c1b3065a5f429ca3b4c832a4bfd2ad7f44abb425781c"
    },
    {
      "path": "C:\\Users\\HP\\AppData\\Local\\Temp\\claude\\c--Bari\\b0971aeb-0178-4845-a428-689223cdc9d0\\scratchpad\\mag-mobile-table.png",
      "sha256": "N/A - transient evidence screenshot, not a committed artifact"
    },
    {
      "path": "C:\\Users\\HP\\AppData\\Local\\Temp\\claude\\c--Bari\\b0971aeb-0178-4845-a428-689223cdc9d0\\scratchpad\\mag-desktop-table.png",
      "sha256": "N/A - transient evidence screenshot, not a committed artifact"
    },
    {
      "path": "C:\\Users\\HP\\AppData\\Local\\Temp\\claude\\c--Bari\\b0971aeb-0178-4845-a428-689223cdc9d0\\scratchpad\\mag-row-10.png",
      "sha256": "N/A - transient evidence screenshot, not a committed artifact"
    },
    {
      "path": "C:\\Users\\HP\\AppData\\Local\\Temp\\claude\\c--Bari\\b0971aeb-0178-4845-a428-689223cdc9d0\\scratchpad\\mag-cannot-bucket.png",
      "sha256": "N/A - transient evidence screenshot, not a committed artifact"
    }
  ],
  "counts": {
    "bars_in_scope_for_threshold_display": 4,
    "bars_suppressed_pending_product_decision": 2,
    "products_reviewed_in_dataset": 18,
    "anatomies_specified": 2,
    "bar_states_covered_per_anatomy": 4,
    "screenshots_captured": 8,
    "viewports_reviewed": 2
  },
  "commands_run": [
    {
      "command": "node scripts/design-agent-shot.mjs (ad hoc Playwright script, mobile+desktop screenshots + getBoundingClientRect geometry against http://localhost:4700/madrichim/magnesium)",
      "exit_code": 0
    },
    {
      "command": "node scripts/design-agent-shot2.mjs (targeted row/bucket screenshots: oxide-520 UL rows, TRIOMAG cannot_verify row, fails/cannot_assess bucket headers)",
      "exit_code": 0
    }
  ],
  "not_done": [
    "No axe/WCAG scan run against this spec's proposed markup (it doesn't exist yet) — Frontend must run npm run test:a11y after implementation, this spec's contrast citations are carried from already-shipped tokens (BarStateBadge), not independently re-measured on the new gauge/ladder combinations",
    "Bucket sub-caption copy for 'fails' and 'cannot_assess' buckets is NOT authored here (content slot only, per lane law) — routes to Content Agent + two-gate sign-off before Frontend wires it in",
    "GuideBenchmarkPlacement VM needs to move from one-field-per-product to one-per-bar (noted in §8) — this is Frontend's type-design call, not fully specified field-by-field here",
    "No static HTML/CSS mock file produced — the ASCII diagrams + exact token citations in this spec were judged sufficient for Frontend to build from; can produce a static mock on request if Frontend needs one before starting",
    "RTL gauge-direction convention (dir=ltr internals) is this agent's recommendation by precedent-absence, not a owner-confirmed or native-speaker-tested decision — flagged explicitly in §2 and §7.4, needs one confirmation pass"
  ],
  "acceptance_test": "Frontend implements ThresholdBarRow for the 4 discriminating bars per this spec; Design Agent re-renders /madrichim/magnesium at 375px + desktop via the same vision-in method, confirms: (1) every bar row shows a visible bar-name label, (2) every discriminating bar (not just dose) shows a threshold gauge or ladder with correct zone/tier rendering, (3) CANNOT_VERIFY bars show the honest no-marker/no-fill fallback with zero fabricated position, (4) bucket headers carry the sub-caption slot, (5) npm run test:a11y and npm run test:visual both pass with new baselines attached before/after at 375px and desktop."
}
```
