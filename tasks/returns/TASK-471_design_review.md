# TASK-471 Design Review — /p/[barcode] canonical product page + catalog barcode search

**Reviewer:** Design Agent (vision-grounded conformance critic)
**Method:** Read all 5 changed/new files; reviewed the 5 provided screenshots; rendered the page LIVE
(`next build` + `next start -p 3472`) and measured real DOM geometry, computed styles, and contrast
ratios via a Playwright script at 390px mobile (primary) and 1440px desktop, plus a 404 check on an
unknown barcode. Ran the existing `test:a11y` suite (covers `/` only — does not yet cover `/p/[barcode]`,
noted as a gap, not scored against this task).

## VERDICT: GO_WITH_FIXES

One CRITICAL-adjacent contrast bug newly introduced by this task (small, isolated, mechanical fix — one
color value on one element). Everything else — geometry, RTL, drift, structure — conforms. The OG image
degradation is a documented, deliberate, and acceptable tradeoff for this launch (see finding OG-1).

---

## Findings — introduced by TASK-471

### HIGH — H1: category-name link fails AA contrast (4.04:1 < 4.5:1 required)
**File:** `C:\Bari\bari-web\src\app\p\[barcode]\page.tsx` lines 135–141
**Element:** the `{row.categoryNameHe}` link ("לחם ומאפים") directly under the eyebrow label, above the H1
product name.

Measured live via Playwright at 390px:
```
categoryLink: color: rgb(31, 143, 106) [#1F8F6A], bg: rgb(255, 255, 255), fontSize: 12px, fontWeight: 700
computed contrast ratio: 4.04:1
```
WCAG 2.1 AA requires 4.5:1 for normal text, or 3:1 only for "large text" (≥18.66px/14pt normal, or
≥14px bold **at minimum 18.66px** — the common shorthand "14pt bold" translates to ~18.66px, which this
element does not reach at 12px). At 12px/700, this is normal-size text and needs 4.5:1. It measures
4.04:1 — a genuine AA fail, not a borderline rounding case.

**This is a newly-introduced usage, not a reused golden-page pattern.** I grepped every other use of
`#1F8F6A` in the codebase (81 files) — in `product-table.tsx`, the same color is used exclusively as a
40%-opacity focus ring (`focus:ring-[#1F8F6A]/40`), never as full-opacity small text. TASK-471 is the
first place this token is applied as link-text color at 12px, and it fails the floor the token was never
tested against in that role.

**Fix:** swap to `#167A58` (used two lines below for the brand name, measured 5.30:1 — passes) or to the
existing `--bari-green-deep` token already used elsewhere in `product-table.tsx` at 5.9:1+. Do not darken
`#1F8F6A` ad hoc — reuse an already-vetted token so this doesn't reintroduce drift on the next edit.

### MEDIUM — M1: OG image is Latin/numeric-only, no product name
**File:** `C:\Bari\bari-web\src\app\p\[barcode]\opengraph-image.tsx`
Confirmed by screenshot (`product_og_image.png`): shows "Bari" wordmark, score "95", "Grade A", and the
raw barcode digits — no Hebrew product name. The page's own `<title>`/`<meta>` (verified in
`generateMetadata`, page.tsx lines 58–64) IS correct Hebrew ("לחם טחינה פרוס — ברי").

**Assessment:** acceptable for this launch, not a blocker. Reasoning:
1. The degradation is documented in-file with the actual root cause (`ImageResponse`'s isolated renderer
   has no Hebrew-shaping font available in the repo — verified true, this is not a shortcut excuse).
2. The card still communicates the one thing that matters for a shared link in this consumer context —
   score + grade — correctly and legibly, in the correct grade-color-coded palette matching the live
   `ScoreChip`/`gradePalette` (checked: A→`#E7F4EC`/`#155C3C`/`#1F8F6A` in the OG file matches
   `BARI_COMPARISON_TOKENS.gradePalette.A` in intent).
3. Social-card no-show of the product name is a real but bounded loss (worse link-preview UX), not a
   correctness or trust problem (nothing false is shown, nothing is fabricated).
4. What would make this NO_GO: if the missing product name caused a wrong/misleading impression (it
   doesn't — barcode + score + grade is self-consistent) or if Hebrew came out as tofu/mojibake (it
   doesn't — it's cleanly omitted, not broken-rendered).

**Recommendation:** ship as-is for this pass. File a fast-follow ticket to source/vendor a single
embeddable Hebrew static font (e.g. a Heebo or Noto Sans Hebrew static .ttf) for `ImageResponse` — this is
a bounded, known fix, not a redesign. Until then, this is the correct degrade path per Hard Rule (avoid
broken glyphs over a clean fallback).

### MEDIUM — M2: no automated a11y/visual-regression coverage yet for `/p/[barcode]`
`e2e/a11y.spec.ts` and `e2e/visual.spec.ts` (checked via `grep` on their route lists implicitly — the
a11y run only exercised `/`) do not appear to include the new route. This means the CRITICAL contrast bug
above (H1) was only caught because this review rendered the page live — it would NOT have been caught by
CI. Recommend Frontend Agent add `/p/[barcode]` (a representative real barcode) to both suites' route
lists before go-live closes, so this class of bug is caught by machine next time, not by a human eyeballing
a screenshot.

---

## Findings — pre-existing / systemic (not introduced by TASK-471, flagged for completeness only)

### PRE-EXISTING — P1: grade-color-coded ScoreChip / InventoryGradeChip
`ScoreChip` (`src/components/shared/score-chip.tsx`) is used verbatim on the new page (page.tsx line 165)
with no modification. Per Score Presentation v1 memory, grade color-encoding is "forbidden" — but per this
task's explicit instruction and the owner directive (2026-06-03, `gradePalette`), this is now the shipped,
approved shape of the component across every live page. TASK-471 did not introduce this pattern; it reused
the existing shared component unchanged. No new finding to raise against this task specifically — the
system-wide status of that directive is a Product/owner-level question, not a TASK-471 defect.

### PRE-EXISTING — P2: cookie-consent banner overlaps page content on mobile
Measured live at 390×844: the consent banner (`src/components/shared/consent-manager.tsx` /
`cookie-notice.tsx`) occupies `top:720 bottom:844` (124px, ~15% of viewport height) and sits fixed over the
bottom of the visible content — in this case over the "אנרגיה / חלבון" nutrition value cards on first
paint, before dismissal. Confirmed via grep that this component is site-wide (`layout.tsx`,
`site-footer.tsx`, applies to `/`, `/catalog`, all `/hashvaot/*`, and now `/p/*` identically) — not
something this task added or changed. Flagging only because it is visible in the delivered
`product_page_mobile_390.png` screenshot and a reviewer seeing it fresh could mistake it for a new-page
bug. No action requested of this task; if it's worth fixing, it's a global consent-banner ticket, not a
TASK-471 scope item.

### PRE-EXISTING — P3: `MethodologyFooter` renders 11px / `#6B7070`, not the frozen spec's 12px / `#AAAAAA`
Measured live: `fontSize: 11px`, `color: rgb(107, 112, 112)` (`#6B7070`) on `#F7F7F2` background
(contrast 4.68:1 — passes AA, incidentally). The Gen 1 frozen constraint table in this agent's own brief
says "12px / `#AAAAAA`". `MethodologyFooter` is a single shared component already used by every golden
comparison page — TASK-471 imports it unmodified (`page.tsx` line 31, 203). This is a codebase-wide,
long-standing deviation from the literal memory text, not something this task touched or regressed. Not
scored against TASK-471; noting only so it isn't misattributed here.

---

## Conformance checklist results (measured, not asserted)

| # | Check | Method | Result |
|---|---|---|---|
| 1 | Mobile 390px zero horizontal scroll | Playwright: `document.documentElement.scrollWidth` vs `clientWidth` at 390px viewport | **PASS** — `scrollWidth=390, clientWidth=390`, 0 elements found with `right>390` or `left<0` across the full DOM |
| 2 | RTL correctness | Playwright: `dir` attribute + back-link text order | **PASS** — `dir="rtl"` on content wrapper; back-link renders `→ חזרה ללחם ומאפים` (arrow visually leads, text follows, correct RTL mirror); no LTR leakage observed in screenshots |
| 3 | WCAG contrast (page text) | Playwright computed-style extraction + manual relative-luminance contrast calc on 6 text/bg pairs | **5 PASS, 1 FAIL** — see H1 above. rowVerdict 12.54:1, muted labels 5.99:1, brand name 5.30:1, H1 18.58:1, methodology line 4.68:1 all pass; category link 4.04:1 fails |
| 4 | Design-token adherence | Read `page.tsx` inline styles against known tokens (`--fg3`, `--hairline`, `--shadow-card`, `--surface-neutral`) | **PASS with 1 flag** — page correctly uses CSS custom-property tokens with fallbacks throughout (`var(--fg3, #5E6560)` etc.), matching the catalog/table convention; the one hardcoded `#1F8F6A` at H1 above is the flagged exception |
| 5 | Visual language match | Screenshot comparison against `catalog_row_product_links.png` / `product_page_desktop.png` | **PASS** — rounded-18px white cards, hairline border (`rgba(17,19,24,0.08)`), `--shadow-card` all match the catalog/comparison golden pages; no novel layout introduced |
| 6 | Score presentation | Component reuse check | **PASS (as reused)** — `ScoreChip` used verbatim, numeric+grade only, no strength label text added; confidence states come from `detail.confidence` unmodified. Color-coded bg is pre-existing systemic (P1), not new |
| 7 | Drift/leakage | Grep for BSIP/NOVA/pillar/dimension/D1-D7 in rendered-string locations across the 2 new page files | **PASS** — 0 hits in rendered text; the one `glassBox` hit is a prop name passthrough, not rendered copy, same pattern the catalog page already uses |
| 8 | OG image | Screenshot + code read | **ACCEPTABLE DEGRADE, not blocking** — see M1 |
| — | Unknown barcode → 404 | Playwright: `goto` unregistered barcode, check response status | **PASS** — `status: 404`, no fabricated page (per `dynamicParams = false` + `notFound()`) |

---

## Recommendation

**GO_WITH_FIXES.** Ship blocked only on H1 (one-line color-token swap, `#1F8F6A` → `#167A58` or an
already-vetted ≥4.5:1 green token, on `page.tsx` line ~138–140). Everything else — the geometry, RTL,
structure, drift-freedom, and the OG degrade decision — conforms and is launch-ready. Route the H1 fix to
the Frontend Agent as a small, scoped patch; re-render and re-measure that one element's contrast before
closing (do not re-run the full review — this is a single isolated value).

M2 (add `/p/[barcode]` to the `a11y`/`visual` suites) is a fast-follow, not a go-live blocker, but should
be opened as a tracked follow-up so this bug class is machine-caught next time.

---

```json
{
  "task": "TASK-471",
  "proposed_status": "RETURNED",
  "artifacts": [
    {
      "path": "C:\\Bari\\tasks\\returns\\TASK-471_design_review.md",
      "sha256": "405daf4a7afdba4029b9a396c456f405e13434d5ea04c8890fac43fcb51c7632"
    }
  ],
  "counts": {
    "files_reviewed": 5,
    "screenshots_reviewed_provided": 5,
    "screenshots_captured_live": 2,
    "conformance_checks_run": 8,
    "conformance_checks_passed": 7,
    "conformance_checks_failed": 1,
    "findings_total": 5,
    "findings_high_introduced_by_task": 1,
    "findings_medium_introduced_by_task": 2,
    "findings_preexisting_systemic": 3,
    "findings_critical": 0,
    "text_bg_contrast_pairs_measured": 6,
    "text_bg_contrast_pairs_passed": 5,
    "text_bg_contrast_pairs_failed": 1,
    "mobile_horizontal_overflow_elements_found": 0,
    "unknown_barcode_status_code": 404
  },
  "commands_run": [
    { "cmd": "npx next build", "exit_code": 0, "cwd": "C:\\Bari\\bari-web" },
    { "cmd": "npx next start -p 3472", "exit_code": "backgrounded, stopped after measurement (server process terminated cleanly via TaskStop)", "cwd": "C:\\Bari\\bari-web" },
    { "cmd": "node measure_tmp_design_review.js (Playwright script; copied into bari-web tree to resolve node_modules, deleted after run)", "exit_code": 0, "cwd": "C:\\Bari\\bari-web" },
    { "cmd": "npx playwright test e2e/a11y.spec.ts --reporter=list", "exit_code": 1, "cwd": "C:\\Bari\\bari-web", "note": "2 failures, both on route '/', both pre-existing (granola card contrast, unrelated to TASK-471; /p/[barcode] not yet in this suite's route list — see finding M2)" }
  ],
  "not_done": [
    "Did not run npm run test:visual (screenshot-diff) against /p/[barcode] — no committed baseline exists yet for this brand-new route, so there is nothing to diff against; recommend Frontend Agent capture the first baseline once H1 is fixed.",
    "Did not independently re-verify score/grade/nutrition VALUES against the underlying corpus JSON — out of this agent's lane (display-only conformance review, not data verification); Adversarial QA / Data Agent lane.",
    "Did not test additional barcodes beyond 7290016245325 (the one specified) plus one deliberately-unknown barcode for the 404 check — a broader sample across categories (e.g. a product with null imageUrl, null brand, empty expansion) was not spot-checked live; recommend at least one empty-state barcode (no image, no brand) be visually confirmed before go-live given the letter-tile fallback and BrandTag-suppression logic both branch on nullable fields."
  ],
  "self_check": {
    "confirms_render_was_seen_before_verdict": true,
    "confirms_geometry_measured_not_asserted": true,
    "confirms_contrast_measured_not_asserted": true,
    "confirms_introduced_vs_preexisting_separated": true,
    "confirms_no_fix_applied_by_this_agent": true,
    "confirms_no_close_authority_exercised": true
  }
}
```
