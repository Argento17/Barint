# Magnesium Buying Guide — Threshold Infographic — Vision-Critic Pass v1

**Route reviewed:** `http://localhost:4700/madrichim/magnesium` (worktree `C:\bari_wt_t504\bari-web`, TASK-504C)
**Method:** live Playwright render, `npm run vision-in` (mobile 375×812 + geometry) + ad-hoc axe-core scan + ad-hoc
targeted element crops (mobile 375×812 @2x, desktop 1280×720/900 @1.5–2x) + `sharp` pixel sampling of the new
mascot asset + computed WCAG contrast ratios from the actual rendered hex values. No production code touched
or edited by this pass.
**Reviewer:** Design Agent — Vision-Critic gate, post-build conformance pass against
`03_operations/reports/design/magnesium_guide_threshold_infographic_spec_v1.md`.
**Scope note:** copy text (bucket sub-captions, `// TODO CONTENT (two-gate)` placeholders) is explicitly
IGNORED per the task brief — this pass judges layout, geometry, contrast, and RTL/state conformance only.

---

## 0. What changed since spec v1 — confirmed by measurement

| Spec ask | Status | Evidence |
|---|---|---|
| Visible bar-name label on every badge (Finding A) | **RESOLVED** | `row1-mobile.png` — "מינון" / "צורה וספיגה" / "בטיחות" / "שקיפות תווית" all render as visible 11px bold text beside each badge |
| Threshold gauge (dose, safety) with zones + dividers + marker | **IMPLEMENTED, conforms** | `row1-mobile.png`, `row-oxide-clamp-mobile.png` |
| Threshold ladder (form, transparency) with tiers + caret | **IMPLEMENTED, conforms** | `row1-mobile.png` |
| Honest CANNOT_VERIFY fallback (no fabricated position) | **IMPLEMENTED, conforms — both anatomies** | `row-triomag-mobile.png` |
| Suppression of thirdPartyVerification/priceFairness | **CONFIRMED** — every row shows exactly 4 bar rows, never 6 | all product-row screenshots |
| Bucket sub-caption slot | **IMPLEMENTED, correct position** (below header pill, above product list) | `bucket-header-top-crop.png` |
| Lumo hero mascot | **IMPLEMENTED, but see Finding H1** | `header-full-mobile.png`, `header-full-desktop.png` |
| Ladder sublabel contrast fix (#8A9089→#4E5663) | **VERIFIED, passes AA everywhere** | computed, see §3 |
| Desktop side-by-side gauge layout (spec §4) | **NOT implemented — see Finding H2** | `row1-desktop.png` |

---

## 1. Findings

### HIGH — H1: Lumo hero mascot ships without alpha transparency, produces a measurable halo

**File:** `bari-web/public/mascots/mascot-mg-magnesium-guide.webp`, consumed in
`src/components/guides/guide-buying-rule.tsx:51-62`

Pixel-sampled the actual asset with `sharp`: `hasAlpha: false`, corner/edge pixels all `rgb(254,254,254)` —
a flat rectangular image with a solid near-white background baked in, no cutout.

The **Character Bible** (`01_framework/brand/bari_character_bible_v1.md:90-94`) states the two currently-live
LUMO/OLI assets ship with "backgrounds keyed to transparent, cropped to figure" — this is the established
practice this new asset was built to match, and it does not:

```
90 ## Live usage so far (2026-07-01)
91 - **LUMO (leaf)** — /hashvaot comparisons index header ...
93 - Optimized assets: .../mascot-leaf.png, .../mascot-olive.png
94   (backgrounds keyed to transparent, cropped to figure).
```

Measured the actual color delta against both containers the image sits in:
- vs. header bg `#FCFCF9` (measured via `getComputedStyle`): `rgb(254,254,254)` vs `rgb(252,252,249)` — small
  but non-zero delta (2,2,5 per channel).
- vs. page body bg `#F7F7F2` (visible around the header at wider viewports): delta (7,7,12) per channel.

This is **visually confirmed**, not theoretical: `header-full-desktop.png` shows a discernible rectangular
edge around the mascot graphic against the page's warmer off-white — most visible at the 288×230 desktop
render size, where the image sits on a much larger expanse of exposed background than on mobile. Frontend's
"no clash" claim is not supported by the pixel evidence.

**Fix:** re-export/matte `mascot-mg-magnesium-guide.webp` with a true alpha channel, cropped tight to the
figure+prop group, matching the treatment already used for `mascot-leaf.png` / `mascot-olive.png`. This is
an asset-pipeline fix, not a component-code fix — no change needed in `guide-buying-rule.tsx` itself.

### HIGH — H2: Desktop gauge anatomy renders full-row-width, not the spec'd capped side-by-side layout

**File:** `src/components/guides/threshold-bar-row.tsx` (`ThresholdGauge`, `ThresholdBarRow`) — spec
§4 desktop requirement (gauge capped `max-width: 260px`, sharing a row with its caption via `flex`) was not
implemented. Confirmed via task brief and independently via render.

`row1-desktop.png` (1280px viewport) shows the gauge track stretching the full ~1150px content-column
width as a single thin 6px line, with the `0 / 150 (חצי סף) / 300 (הסף)` tick labels spread far apart across
that width. At this scale the gauge reads as a sparse, low-information-density line rather than a
quick-scan indicator — a materially worse "read at a glance" experience than the same gauge at mobile
width, where the track and its zones/marker occupy the eye's full attention span in ~240px.

Note the scope of this finding: the **ladder** anatomy (form/transparency) is not affected — its three
solid tier blocks still fill the full row width meaningfully and read fine at desktop size
(`row1-desktop.png`, second bar). This is specific to the gauge anatomy's thin-line geometry.

**Fix:** implement spec §4's desktop layout — bar-name+badge on one line, gauge capped at `max-width: 260px`
sharing a flex row with the caption text, exactly as specified. Not a blocker for a mobile-first ship
(mobile is the comprehension-critical surface per `bari_phase_status`), but should land before desktop
traffic is treated as a fully-supported surface for this component.

### MEDIUM — M1: Pre-existing axe "aria-prohibited-attr" (serious) on the thumbnail fallback — real, in-scope for a quick fix, not introduced by this diff

**File:** `src/components/guides/guide-product-row.tsx:52-56` (the no-image `GuideProductThumbnail` fallback)

Live axe scan (`@axe-core/playwright`, `wcag2a`+`wcag2aa` tags) against the running route returns exactly
**1 serious violation at both viewports**:

```
[serious] aria-prohibited-attr: Elements must only use permitted ARIA attributes (1 nodes)
html: <div class="relative size-14 shrink-0 overflow-hidden rounded-2xl border border-black/[0.06]
       bg-white shadow-sm" aria-label="ביסגליצינט 600 כמוסות">
message: aria-label attribute cannot be used on a div with no valid role attribute.
```

This is real (confirmed by the tool, not asserted) and is genuinely **pre-existing** — this exact
thumbnail-fallback component was not touched by the TASK-504C threshold-infographic diff. Flagging per the
task's explicit ask to re-check it, and because the fix is trivial and zero-risk: the very same file's
sibling component, `BarStateBadge` (`src/components/shared/bar-state-badge.tsx:72-74`), already does this
correctly with `role="img"` + `aria-label`. Recommend Frontend add `role="img"` to the fallback `<div>` in
the same or next PR — it is the one console-visible axe failure on this route today and the fix pattern
already exists one file away.

### MEDIUM — M2: Ladder non-current-tier label contrast passes with zero margin

**File:** `src/components/guides/threshold-bar-row.tsx:216-220` (`ThresholdLadder`, non-current tier label)

Computed (relative-luminance WCAG formula, not eyeballed): `#6B7070` at 10px bold on the neutral
non-current-tier background `#F3F4F2` measures **4.56:1** — clears the 4.5:1 AA floor for normal text (10px
bold does not qualify for the 3:1 large-text exemption), but by only 0.06. This is a pass today, not a
finding that blocks shipping, but it has no headroom: any future palette nudge to either `#6B7070` or
`#F3F4F2` could silently drop it below AA with nothing currently pinned to this exact pairing. Recommend
Frontend add this pairing to whatever fixture/test already covers the ladder-sublabel fix (`#4E5663`), so a
future token change doesn't regress it unnoticed.

For contrast, every other text/background pairing measured on the new component **clears AA comfortably**
(see §3 below) — this is the one fragile-but-passing case.

---

## 2. Confirmed-good (measured, not asserted — no action needed)

- **Bar-name labels** now visible next to every badge at 375px (`row1-mobile.png`) — spec Finding A resolved.
- **Zone tints + mandatory divider lines**: verified in code (`magnesium-guide-data.ts:97-114`) and on
  screen — dose gauge dividers both `solid` (150, 300); safety gauge divider `dashed` at the 250 EFSA
  soft-caution line and `solid` at the 350 hard UL line, exactly per spec §2. Visible in `row1-mobile.png`
  and `row-oxide-clamp-mobile.png`.
- **CANNOT_VERIFY honesty**: confirmed via the TRIOMAG row (`row-triomag-mobile.png`, product index 17/18,
  all four bars cannot_verify) — gauge renders a hollow dashed ring fixed at the track midpoint (no
  fabricated position), ladder renders all three tiers neutral with no fill/caret. Matches spec §2/§3
  exactly, and the owner's explicit "keep it honest" ask.
- **Clamp + "+" glyph**: confirmed via the 520mg oxide product row (`row-oxide-clamp-mobile.png`) — dose
  marker clamps at the domain end colored teal (+, pass, since 520mg clears the 300mg floor), safety marker
  clamps at the domain end colored berry (+, fail, since 520mg exceeds the 350mg UL). Colors correctly track
  each bar's own independent state, never a shared/borrowed color.
- **Suppression**: every product row (checked across `row1`, `row-triomag`, `row-oxide-clamp`) shows exactly
  4 `ThresholdBarRow` blocks — thirdPartyVerification/priceFairness never render, per spec §1/§4.
- **`dir="ltr"` gauge/ladder forcing inside the RTL page**: renders correctly — numeric 0→high reads
  conventionally left-to-right inside each gauge/ladder, bar-name/badge/caption stay `dir="rtl"` around it,
  no mirrored or garbled bidi text anywhere observed. The ladder's left=worst/right=best convention
  (dir=ltr) is applied consistently to both anatomies as spec'd. (Native-Hebrew-reader comprehension
  read-through remains outstanding per the spec's own §7.4 flag — this pass confirms it renders without
  technical breakage, not that it's the optimal mental model for a Hebrew reader.)
- **Hero block size on mobile**: image+eyebrow+h1 span ≈227px (`y:89` to `y:316` from
  `madrichim-magnesium__mobile.geometry.json`) — under the 280px comparison-page hero precedent, does not
  excessively push the six-card buying-rule grid down.
- **Bucket sub-caption position**: renders directly below the bucket header pill, above the product list,
  per spec §5 (`bucket-header-top-crop.png`, verified against the raw DOM via `outerHTML` dump — my first
  visual read of the low-res full-page screenshot had this backwards; the tight, upscaled crop plus a DOM
  dump both confirm the order is correct).

---

## 3. Contrast — computed, not eyeballed

Relative-luminance WCAG ratio computed directly from the hex values Frontend used (script run against the
literal `GUIDE_BAR_TONE` / gauge / ladder colors in the codebase):

| Pairing | Ratio | Verdict |
|---|---|---|
| Ladder sublabel `#4E5663` / neutral `#F3F4F2` | 6.71:1 | PASS |
| Ladder sublabel `#4E5663` / pass-tint `#E2F2EF` | 6.41:1 | PASS |
| Ladder sublabel `#4E5663` / flag-tint `#EAEDF8` | 6.34:1 | PASS |
| Ladder sublabel `#4E5663` / fail-tint `#F8E7EF` | 6.23:1 | PASS |
| Gauge tick label `#6B7070` / row bg `#FFFFFF` | 5.03:1 | PASS (this is the tick labels' real background — they sit in a row below the track, not on the zone tint itself; resolves the spec's own §7.3 uncertainty) |
| Gauge tick label `#6B7070` / zebra row bg `#F9F9F9` | ~4.98:1 | PASS |
| Caption `#4E5663` / white row bg | 7.41:1 | PASS |
| Bucket sub-caption `#6E756D` / white | 4.74:1 | PASS |
| Ladder non-current tier label `#6B7070` / `#F3F4F2` | 4.56:1 | PASS (zero margin — see M2) |

Axe-core (`wcag2a`+`wcag2aa`) live scan: **1 serious violation total, both viewports** — M1 above (thumbnail
fallback). Zero contrast violations reported by axe on this route.

---

## 4. GO / GO-WITH-FIXES / NO-GO

**GO-WITH-FIXES.**

Ship mobile now — it is the comprehension-critical surface (`bari_phase_status`), every spec-mandated
behavior (visible bar identity, honest cannot_verify fallback, clamp handling, suppression, contrast)
measures correctly there, and there are zero CRITICAL findings. Before treating desktop as a fully
supported surface, land H2 (capped-width side-by-side gauge layout). Land H1 (re-export the mascot asset
with real alpha transparency) before this page goes in front of the owner or into any screenshot-based
review — it's a one-file asset fix, not a code change, and cheap to do now. M1 and M2 are low-risk,
low-effort riders that should travel with whichever PR picks up H1/H2, not separate blockers.

---

## Return Contract

```json
{
  "artifacts": [
    { "path": "C:\\Bari\\03_operations\\reports\\design\\magnesium_guide_revision_visioncritic_v1.md", "sha256": "41490679d4138e60b4ccea3abc45097a46bf44ce13269c31aa2b759e83a92341 (self-hash of the pre-this-edit save; exact self-reference is not computable without a second pass — content unchanged except this line since that hash was taken)" },
    { "path": "C:\\Users\\HP\\AppData\\Local\\Temp\\claude\\c--Bari\\b0971aeb-0178-4845-a428-689223cdc9d0\\scratchpad\\mag-visioncritic\\madrichim-magnesium__mobile.png", "sha256": "27b47fb0ea2c9cd099f56b94ba564a840ce71c7fa8a36ec95caece361a8b92fd" },
    { "path": "C:\\Users\\HP\\AppData\\Local\\Temp\\claude\\c--Bari\\b0971aeb-0178-4845-a428-689223cdc9d0\\scratchpad\\mag-visioncritic\\madrichim-magnesium__desktop.png", "sha256": "6eaf1063c91b209b49b6910cba52808efc216ac7f3a38f2a91db752ed529eb9c" },
    { "path": "C:\\Users\\HP\\AppData\\Local\\Temp\\claude\\c--Bari\\b0971aeb-0178-4845-a428-689223cdc9d0\\scratchpad\\mag-visioncritic\\row1-mobile.png", "sha256": "73a69a54f802b2739994852a2767367e1eb55a76a93696b7d99e562e4941bc9c" },
    { "path": "C:\\Users\\HP\\AppData\\Local\\Temp\\claude\\c--Bari\\b0971aeb-0178-4845-a428-689223cdc9d0\\scratchpad\\mag-visioncritic\\row-cannotverify-mobile.png", "sha256": "f1da5a2a878a20f67e6e47eeeacd413ce75a8e8e5ac4294466aefc0971df6458" },
    { "path": "C:\\Users\\HP\\AppData\\Local\\Temp\\claude\\c--Bari\\b0971aeb-0178-4845-a428-689223cdc9d0\\scratchpad\\mag-visioncritic\\row-triomag-mobile.png", "sha256": "1d918ed8eb59b92eb152fbaf03311c563b6a89c72f906bfa702c064a8f9251a8" },
    { "path": "C:\\Users\\HP\\AppData\\Local\\Temp\\claude\\c--Bari\\b0971aeb-0178-4845-a428-689223cdc9d0\\scratchpad\\mag-visioncritic\\row-oxide-clamp-mobile.png", "sha256": "63b55aaa58c4f869198e5ba78fb80ab6d0137c679e626b711e5757fd7e0d5e20" },
    { "path": "C:\\Users\\HP\\AppData\\Local\\Temp\\claude\\c--Bari\\b0971aeb-0178-4845-a428-689223cdc9d0\\scratchpad\\mag-visioncritic\\header-full-mobile.png", "sha256": "15e061fae80188f305f2a1282ebae7a78302a79af871572605f12d89941a34e3" },
    { "path": "C:\\Users\\HP\\AppData\\Local\\Temp\\claude\\c--Bari\\b0971aeb-0178-4845-a428-689223cdc9d0\\scratchpad\\mag-visioncritic\\header-full-desktop.png", "sha256": "6de7f1c441ef79490133e77674f1f3cac830a2bace04558b9dc511bee4668419" },
    { "path": "C:\\Users\\HP\\AppData\\Local\\Temp\\claude\\c--Bari\\b0971aeb-0178-4845-a428-689223cdc9d0\\scratchpad\\mag-visioncritic\\hero-image-zoom-mobile.png", "sha256": "70f23a23fb1790adfa4cef7dc11b469f9197f2d1981f348ae6cc33c3866c05b8" },
    { "path": "C:\\Users\\HP\\AppData\\Local\\Temp\\claude\\c--Bari\\b0971aeb-0178-4845-a428-689223cdc9d0\\scratchpad\\mag-visioncritic\\row1-desktop.png", "sha256": "e264612287ba0b2060a9804ddc11162df98e385cc5f7ae129b612d5b338a5cf1" },
    { "path": "C:\\Users\\HP\\AppData\\Local\\Temp\\claude\\c--Bari\\b0971aeb-0178-4845-a428-689223cdc9d0\\scratchpad\\mag-visioncritic\\bucket-header-top-crop.png", "sha256": "f833227ed830ffe34ce1e2c2fd8e986244411e659e52f3997c25907b1e79adc5" },
    { "path": "C:\\Users\\HP\\AppData\\Local\\Temp\\claude\\c--Bari\\b0971aeb-0178-4845-a428-689223cdc9d0\\scratchpad\\mag-visioncritic\\axe-mobile.json", "sha256": "bbf8bf330abe1a106015e654f9e6aa8d024a975407c6127450f54897c0772f9a" },
    { "path": "C:\\Users\\HP\\AppData\\Local\\Temp\\claude\\c--Bari\\b0971aeb-0178-4845-a428-689223cdc9d0\\scratchpad\\mag-visioncritic\\axe-desktop.json", "sha256": "bbf8bf330abe1a106015e654f9e6aa8d024a975407c6127450f54897c0772f9a" },
    { "path": "C:\\Users\\HP\\AppData\\Local\\Temp\\claude\\c--Bari\\b0971aeb-0178-4845-a428-689223cdc9d0\\scratchpad\\mag-visioncritic\\madrichim-magnesium__mobile.geometry.json", "sha256": "e4d5fc8f152c73e0ede41ffcb1d6605eef39c72a6e02b4fb19168aa59240c209" },
    { "path": "C:\\Users\\HP\\AppData\\Local\\Temp\\claude\\c--Bari\\b0971aeb-0178-4845-a428-689223cdc9d0\\scratchpad\\mag-visioncritic\\madrichim-magnesium__desktop.geometry.json", "sha256": "44aff8725e8f27ab3ab25194e71972132fd966a50e4b1b55368dbcaae16ab57c" }
  ],
  "counts": {
    "viewports_reviewed": 2,
    "products_reviewed_by_name": 3,
    "products_in_dataset": 18,
    "findings_critical": 0,
    "findings_high": 2,
    "findings_medium": 2,
    "findings_low_or_confirmed_good": 9,
    "axe_serious_or_critical_violations": 1,
    "axe_violations_total_mobile": 1,
    "axe_violations_total_desktop": 1,
    "contrast_pairings_computed": 9,
    "contrast_pairings_failing_aa": 0,
    "contrast_pairings_passing_with_under_0.1_margin": 1
  },
  "commands_run": [
    { "command": "npm run vision-in -- --route /madrichim/magnesium --base http://localhost:4700 --viewport mobile --selectors <guide-specific testids>", "exit_code": 0 },
    { "command": "npm run vision-in -- --route /madrichim/magnesium --base http://localhost:4700 --viewport desktop --selectors <guide-specific testids>", "exit_code": 0 },
    { "command": "node <ad-hoc script>: AxeBuilder(wcag2a,wcag2aa).analyze() against localhost:4700/madrichim/magnesium, mobile+desktop", "exit_code": 0 },
    { "command": "node <ad-hoc script>: targeted element .screenshot() crops (hero, row1, row2, TRIOMAG cannot_verify row, 520mg oxide clamp row, bucket header)", "exit_code": 0 },
    { "command": "node <ad-hoc script>: sharp pixel-sample of mascot-mg-magnesium-guide.webp corners/edges", "exit_code": 0 },
    { "command": "node <ad-hoc script>: computed WCAG relative-luminance contrast ratios for 9 gauge/ladder text-on-background pairings", "exit_code": 0 },
    { "command": "node <ad-hoc script>: DOM outerHTML/children dump of guide-bucket-passes_with_flag and guide-product-table to resolve bucket-header/subcaption visual-order question", "exit_code": 0 }
  ],
  "not_done": [
    "npm run test:visual and npm run test:a11y (the committed suites) were NOT run against this route — it is not in either suite's route list yet (a11y.spec.ts ROUTES does not include /madrichim/magnesium). This pass used ad-hoc axe/Playwright scripts against the same libraries instead; recommend adding /madrichim/magnesium to e2e/a11y.spec.ts's ROUTES and a guide route to visual.spec.ts's baseline set as a follow-up, separate from this content-in-flight build.",
    "Native-Hebrew-reader screen-reader/comprehension read-through of the dir=ltr gauge convention (spec §7.4) — this pass confirms it renders without technical/bidi breakage, not that it is the most intuitive mental model for a Hebrew-only reader; that confirmation pass is still outstanding.",
    "Desktop viewport captured at 1280x720/900 (vision-in.mjs's built-in desktop size), not literally 1440x900 as the task text suggested — the gauge full-width-sparseness finding (H2) would be equally or more visible at 1440px, not less, so this does not change the verdict, but noting the exact viewport used for the record.",
    "Bucket sub-caption and suppressed-bars-disclosure COPY was not evaluated (placeholder `// TODO CONTENT (two-gate)` text throughout) — explicitly out of scope per the task brief; Content Agent + two-gate sign-off still owns that copy before ship."
  ],
  "acceptance_test": "GO-WITH-FIXES: ship mobile now (zero CRITICAL findings, all spec-mandated behaviors — visible bar identity, honest cannot_verify fallback for both anatomies, clamp+\"+\" handling, bar suppression, RTL dir=ltr gauge rendering, ladder-sublabel contrast fix — measured and confirmed conformant). Before wide/desktop rollout: fix H1 (re-export mascot-mg-magnesium-guide.webp with real alpha transparency, matching mascot-leaf.png/mascot-olive.png precedent) and H2 (implement spec §4's capped-width side-by-side desktop gauge layout). M1 (add role=\"img\" to the thumbnail fallback div) and M2 (pin the 4.56:1 ladder-tier-label contrast pairing in a fixture) should ride along with whichever PR picks up H1/H2."
}
```
