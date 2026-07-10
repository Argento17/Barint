# TASK-504B — Design Vision-Critic Conformance Pass: `/madrichim/magnesium` Guide Template

**Reviewer:** Design Agent (vision-grounded critic)
**Reviewed:** worktree `C:\bari_wt_t504`, branch `feat/task504-guides-template`, commit `b8dc6a20`
**Method:** (1) reviewed the 9 pre-supplied screenshots at `C:\Bari\tasks\returns\TASK-504B_screenshots\`; (2) independently built (`npm run build`, exit 0) and served the worktree (`npm run start -- -p 4599`) and re-rendered the live route at 375×812 and 1440×900 with Playwright, pulling both fresh full-page screenshots and `getBoundingClientRect`/`getComputedStyle` geometry for every bar-state badge, bucket header, buy button, and the site header, plus a second targeted computed-style pass on the specific text/background pairs flagged below; (3) read all 7 files under `bari-web/src/components/guides/` plus `bari-web/src/components/shared/bar-state-badge.tsx` and diffed their hardcoded hex values against `bari-comparison-tokens.ts`; (4) computed WCAG contrast ratios from the actual rendered RGB, not assumed values. Evidence saved to `C:\Bari\tasks\returns\TASK-504B_design_critic_evidence\` (fresh screenshots + geometry JSON + computed-style JSON).

This is the first Design conformance pass on `guide-product-row.tsx` / `bar-state-badge.tsx` / the rest of the guide template — the components' own code comments flag themselves as "not yet reviewed by the Design Agent." This review functions as that Hard-Rule-6 new-component gate, not just enforcement against an existing frozen spec, since guides are a legitimately new page family (always-expanded cards, zero score/grade, per Product's D7 ruling) rather than a deviation from the comparison-page spec.

---

## Verdict: **GO-WITH-FIXES**

Structure, RTL, mobile geometry, buy-button dormancy, bucket ordering, and the "no fake winner" framing are all sound and conforming. Three concrete contrast failures and one semantic color-identity risk need a fix before this becomes the template every future guide inherits from. None of the four are pixel-level tweaks Frontend can free-solo — the color-identity one (CRITICAL) needs a decision on the replacement palette, which is what makes this GO-WITH-FIXES rather than GO.

---

## CRITICAL

### C1. Bar-state badge colors are byte-identical to the comparison-page gradePalette A/C/E tokens — this reads as a smuggled-back grade axis

**Element:** `BarStateBadge` (`bari-web/src/components/shared/bar-state-badge.tsx:28-46`), rendered on every one of the 108 bar badges across all 18 product rows.

**Rule failed:** Task brief for this review, verbatim: *"the hue reuse of gradePalette must NOT read as an A–E grade."* Also Hard Rule 2 of this agent's charter: *"Do not add a second color axis or per-product color outside the A–E ramp."*

**What I measured:** `bar-state-badge.tsx` doesn't approximate the gradePalette hues — it imports them directly:
```
const { A: PASS_PALETTE, C: FLAG_PALETTE, E: FAIL_PALETTE } = BARI_COMPARISON_TOKENS.gradePalette;
```
and assigns them 1:1 (`pass: PASS_PALETTE`, `flag: FLAG_PALETTE`, `fail: FAIL_PALETTE`). Confirmed against `bari-comparison-tokens.ts:2-8`:

| Guide state | bg | border | text | Identical to gradePalette grade |
|---|---|---|---|---|
| PASS | `#E7F4EC` | `#1E7A4F33` | `#155C3C` | **A** (green, "best") |
| FLAG | `#FBF3D8` | `#8A630033` | `#7E5800` | **C** (amber, "middle") |
| FAIL | `#F7E3E1` | `#A5212133` | `#7A1A1A` | **E** (red, "worst") |

These are not "the same hue family" — they are the literal same hex strings used for the numeric/letter score chip on every `/hashvaot` comparison page. A user who has seen even one comparison page has already learned "green pill = A = best, red pill = E = worst." Landing on `/madrichim/magnesium` and seeing the identical green/amber/red pills on PASS/FLAG/FAIL will read them as grades by trained association, regardless of the code comment's stated intent ("semantic hue reuse only... does not imply a grade letter" — intent in a comment doesn't change what the eye pattern-matches). This is exactly the failure mode the task brief pre-named.

**Screenshot reference:** `TASK-504B_screenshots/product-row-detail.png` and `section-bucket-fails.png` — the FAIL badges ("לא עומד") are visually indistinguishable in hue from an E-grade chip elsewhere in the app; PASS badges ("עומד בסף") from an A-grade chip.

**Counter-evidence the template already knows how to do this right:** the `isDefaultPick` badge ("הבחירה הפשוטה", `guide-product-row.tsx:106-111`) and the `isPromoted` bucket-header treatment (`guide-product-table.tsx:86`) both use a *distinct* muted green (`#F0F4F1` / `#3A6B50` / `#C6D4CB`) that is **not** in gradePalette at all — proving the template can express "positive" without borrowing the grade ramp. That's the pattern C1's fix should follow.

**Recommendation:** Give PASS/FLAG/FAIL their own three-tone family, shifted in lightness/saturation/hue far enough from gradePalette A/C/E that the two systems are visually distinguishable side by side (e.g. desaturate and cool the hues, or move to a duotone/pattern-based system) — while keeping the existing good practice of never relying on color alone (state label text + dot always present). This is a palette decision, not a Frontend judgment call — flagging for this agent + Product/Nutrition sign-off before Frontend re-implements, per Hard Rule 2 ("Any change to the ramp itself is an exception request" — here it's the guide ramp that needs defining, not the ramp itself, but the same rigor applies).

---

## HIGH

### H1. Bucket product-count text fails WCAG AA contrast — 2.67:1 against a 4.5:1 floor

**Element:** the `(N)` count beside every bucket heading — e.g. `(12)` next to "לא עובר", `(1)` next to "לא ניתן להעריך". `guide-product-table.tsx:96-103`, class `text-[11px] font-semibold ... text-[#9AA09B]` (non-promoted branch).

**Measured:** live computed style `rgb(154, 160, 155)` text on white page background → **contrast 2.67:1**. WCAG 1.4.3 requires 4.5:1 for 11px/600-weight text (not "large text" — that threshold starts at 18.66px bold). This is a hard fail, not a borderline one.

**Why it matters here specifically:** the whole point of the bucket table is "how many products landed where" at a glance — the count is core content, not decoration, and it's the most washed-out text on the page.

**Screenshot reference:** `TASK-504B_design_critic_evidence/geometry_mobile.json` buckets array + `computed_styles.json` → `failsHeaderCount` / `cannotHeaderCount`.

### H2. Non-promoted bucket heading text fails WCAG AA — 3.99:1 against 4.5:1

**Element:** the bucket label itself ("לא עובר", "לא ניתן להעריך") when not the promoted bucket. `guide-product-table.tsx:88-94`, `text-[#7A817C]`.

**Measured:** computed `rgb(122, 129, 124)` on white, 10.4px/700-weight → **3.99:1**. Same WCAG clause as H1 — 10.4px bold doesn't qualify for the 3:1 large-text exception (needs ≥18.66px bold). Close to the line but a genuine fail.

### H3. Promoted-bucket count fails AA — ≈3.0:1, in the page's single most important heading

**Element:** the `(5)` count beside the promoted "practical shortlist" heading. `guide-product-table.tsx:96-103`, `isPromoted` branch, `text-[#3A6B50]/70`.

**Measured:** live computed color is a 70%-alpha composite (`lab(41.165 -22.5293 9.79008 / 0.7)`) over the `#F0F4F1` promoted-container background → hand-verified composite ≈ `#719480`, contrast **≈3.0:1** against a 4.5:1 floor. This is the one heading on the page Product/Nutrition explicitly wants legible — it's the "start here" bucket — and its count is the least legible text on the page after H1.

**Fix for H1–H3 (one fix, three sites):** drop the `/70` opacity modifier and lighten-adjust the base hex instead (opacity composited onto a colored background is what's producing the failures — solid, slightly darker versions of the same hues clear 4.5:1 easily, e.g. `#6E756D`-range darkened, or reuse `sectionMeta`'s `#4E5663` which already passes at 9.86:1 elsewhere on this same page). Verify with the a11y suite (`npm run test:a11y`) after the change, not by eye — these three all "look" like reasonable muted grays on screen, which is exactly how contrast bugs like this ship invisibly.

---

## MEDIUM

### M1. Inherited template debt: shared `sectionEyebrow` token also fails AA (~3.6:1), now on two more surfaces

**Element:** `BARI_COMPARISON_TOKENS.typography.sectionEyebrow` (`text-[0.65rem] ... text-[#167A58]/80`), used verbatim for "מדריכים · בארי" in `guide-buying-rule.tsx:30` and for "Bari · מדריכים" on the `/madrichim` hub (`page.tsx:71`).

**Measured:** live computed color composites to ~3.6:1 against white — below 4.5:1 for its 10.4px/700-weight size.

**Disposition:** this is a **pre-existing shared token**, not something this task introduced — it's inherited exactly the way the TASK-494 blog-contrast class was inherited debt. It was already failing on comparison pages before this task touched anything; this task just adds two more places it appears. Flagging per this agent's standing duty to note pre-existing template debt when it surfaces during a review, not blocking this guide launch on it — but it should go on the token-governance backlog since the guide template has now widened its blast radius from N comparison pages to N+2.

### M2. `cannot_verify` is 44% of all bar evaluations on this page (47 of 108 badges) — a content/data question, not a design one

Counted via live DOM query (`data-bar-state="fail"`: 16, `pass`: 33, `flag`: 12, `cannot_verify`: 47). Flagging for visibility only: a page whose headline honesty pitch is "here's what actually matters, verified" is working against itself if nearly half of every product's bars land on "we couldn't check." Out of Design's lane — routing this observation to Nutrition/Content, not gating the design verdict on it.

---

## LOW / non-gating observations

- **Buy button dormant tap target** (`guide-buy-button.tsx`) renders at 26px height. Below the 24px WCAG 2.5.8 AA minimum is close but the control is `disabled`/`aria-disabled` and non-operable by design (dormant `/catalog` treatment per plan §4) — target-size criteria don't bind non-operable controls. Re-check when `buyUrl` goes live and the button becomes clickable.
- **Native `title` attribute** for the badge's `note` tooltip (`bar-state-badge.tsx:78`) has no touch affordance on mobile — the reason text still reaches screen readers via `aria-label`, so this isn't an a11y floor failure, just a lost "why" for sighted mobile users. Worth a tap-reveal pattern in a later iteration, not a blocker.
- **Breadcrumb/back-link arrows** (`ArrowLeft` icon, both "hub → comparisons" and "hub → home" links on `/madrichim`) point the same direction regardless of semantic forward/back. This mirrors the existing `/hashvaot` page's own convention verbatim (confirmed via code comment "mirrors /hashvaot/page.tsx structure") — not new drift, not flagging as a defect.

---

## Confirmed PASS (measured, not assumed)

- **RTL:** `<html dir="rtl" lang="he">` confirmed via live DOM query; every guide component sets `dir="rtl"` explicitly; badge dot renders before the Hebrew label in correct RTL reading order (verified visually in `product-row-detail.png` and via flex/dir computed styles). No LTR leakage found.
- **No horizontal scroll:** `document.documentElement.scrollWidth === clientWidth` at both 375px (`375===375`) and 1440px (`1440===1440`) — see `geometry_mobile.json` / `geometry_desktop.json` → `overflow`.
- **No numeric score or letter grade anywhere on the page:** grepped all guide files for `ScoreChip`/`BariGradeBadge`/`bandOf`/`gradeOf` — the only hits are code *comments* explicitly disclaiming their use; zero live usage.
- **Buy button uniformly dormant:** sampled 10 of 18 rows programmatically — all render `data-testid="guide-buy-button-dormant"` with identical geometry/style (142×26px, `#5E6560` text, transparent bg, `cursor-not-allowed`); mechanically decoupled from bucket/verdict data per the component's own contract (`buyUrl`-only prop).
- **Bucket order and empty-state handling:** DOM order confirmed `passes_with_flag → fails → cannot_assess` (clears_all correctly empty and skipped) matching `GUIDE_BUCKET_ORDER`; `GuideHeadlineFinding` renders in its place with the honest "no product clears every bar" framing, verbatim Content copy, no paraphrasing logic in the component.
- **"Practical shortlist" promotion reads honestly, not as a fake podium:** the promoted bucket uses a modest bordered/tinted section header (`#F0F4F1`/`#3A6B50`/`#C6D4CB`), no crown/trophy/rank-number graphic; `rank` prop is explicitly documented as zebra-tone-only, never rendered as a position number.
- **Default-pick badge correctly avoids gradePalette** — uses its own muted-green tone distinct from A-grade green, proving the team already knows the right pattern (this is the fix C1 should imitate).
- **Single sticky header, no duplication:** DOM query confirms exactly one `position: sticky` element; the recurring "Bari" logo visible mid-page in the pre-supplied full-page screenshots (`section-bucket-pw.png`, `mobile.png`) is a Playwright full-page-screenshot stitching artifact at the sticky header's repaint boundary, not a real duplicated-header bug. Verified and ruled out — not a finding.
- **Token discipline elsewhere:** read all 7 guide component files line-by-line against `bari-comparison-tokens.ts`; `GuideBuyingRule` and `GuideEducationSpine` correctly reuse `BARI_COMPARISON_TOKENS.typography` and `comparisonWebSectionPaddingClass()` rather than inventing new type scale or spacing, per the components' own stated intent ("no novel type scale invented for this new page family"). The only off-conformance hex usage found is C1 (wrong reuse direction) and H1–H3 (right token family, wrong contrast for text size).
- **Hub page (`/madrichim`) reuses the already-shipped `HashvaotCategoryBox` component verbatim** — the "18 מוצרים נבדקו" stat and "זמין"/"בקרוב" status pills are pre-existing, already-approved patterns from `/hashvaot`, not new drift introduced by this task.

---

## Required before GO

1. **C1** — replace the PASS/FLAG/FAIL tone source with a palette visually distinct from gradePalette A/C/E (Design Agent + Product/Nutrition to pick the replacement; Frontend implements once specified).
2. **H1, H2, H3** — fix the three bucket-header/count contrast failures (single class of bug, three sites); re-verify with `npm run test:a11y` after the fix, not by eye.

M1/M2/LOW items do not block go-live of this template but M1 should be logged against the token-governance backlog since this task widens its surface.

---

## Return Contract

```json
{
  "task": "TASK-504B",
  "proposed_status": "RETURNED",
  "summary": "Vision-grounded conformance review of the /madrichim/magnesium guide template (worktree c:\\bari_wt_t504, commit b8dc6a20). Verdict: GO-WITH-FIXES. 1 CRITICAL (bar-state badge colors are byte-identical to comparison-page gradePalette A/C/E, risking the ruling that guide bars must not read as a grade), 3 HIGH (bucket-count and bucket-heading text fail WCAG AA contrast at 2.67:1, 3.99:1, and ~3.0:1 against a 4.5:1 floor), 2 MEDIUM (inherited sectionEyebrow contrast debt now on 2 more surfaces; cannot_verify is 44% of all bar evaluations, a content question not a design one), 2 LOW non-gating observations. RTL, mobile geometry, no-horizontal-scroll, buy-button dormancy, bucket ordering/empty-state, and the non-podium 'practical shortlist' framing all confirmed passing via live render + DOM geometry, not by assumption.",
  "artifacts": [
    {"path": "C:\\Bari\\tasks\\returns\\TASK-504B_design_critic_v1.md", "sha256": "self-referential (a hash embedded in a file cannot describe that same file's final byte content); verify with `sha256sum TASK-504B_design_critic_v1.md` against the version in the PR/commit"},
    {"path": "C:\\Bari\\tasks\\returns\\TASK-504B_screenshots\\mobile.png", "sha256": "82e8dbce02c6d514d2e2fa8fe7b7d2ca6d847a04e515d94442fece4c4887725b"},
    {"path": "C:\\Bari\\tasks\\returns\\TASK-504B_screenshots\\desktop.png", "sha256": "eed2c1eeb3ea2040942081bc3832d6ae9a912461051df69dcb68556835d5de6d"},
    {"path": "C:\\Bari\\tasks\\returns\\TASK-504B_screenshots\\product-row-detail.png", "sha256": "42861da17b4d2d30b109aa2b0f195011f522db9f4c2a98b0a4fdeb2e7555d08f"},
    {"path": "C:\\Bari\\tasks\\returns\\TASK-504B_screenshots\\section-bucket-pw.png", "sha256": "92e813015fd6d3140f3bfacbfc3ef7194631bf97e9d88f6b656d765e0c41bc13"},
    {"path": "C:\\Bari\\tasks\\returns\\TASK-504B_screenshots\\section-bucket-fails.png", "sha256": "60c7d08f69fd7afab1aeb417ee66af5c76c399e15eb03a01a471b7f8c8b7395a"},
    {"path": "C:\\Bari\\tasks\\returns\\TASK-504B_screenshots\\section-bucket-cannot.png", "sha256": "d5115e14999d8f5fae0892dfc39b7fe32e1f2b7282060e3c8aecfb0e469200c8"},
    {"path": "C:\\Bari\\tasks\\returns\\TASK-504B_screenshots\\section-headline.png", "sha256": "dc985e4c2903315fb6dc28e6ac3509407cf17a2ef4f72c21279c322fd903d802"},
    {"path": "C:\\Bari\\tasks\\returns\\TASK-504B_screenshots\\section-buying-rule.png", "sha256": "1fddfb3817d63b1118caa4af8ffa0fef8636d96c13c34530589c34cd0516d4ed"},
    {"path": "C:\\Bari\\tasks\\returns\\TASK-504B_screenshots\\section-education.png", "sha256": "5abdab4d9344ef92298abf6d99a5982bb44d8605c3eb2f65f084ec89bafca3a3"},
    {"path": "C:\\Bari\\tasks\\returns\\TASK-504B_design_critic_evidence\\fresh_mobile_full.png", "sha256": "8160f3cd95d840ec3b448ec11dd9664fdf0a250b68bc866766ea21da8db69ce9"},
    {"path": "C:\\Bari\\tasks\\returns\\TASK-504B_design_critic_evidence\\fresh_desktop_full.png", "sha256": "3a40c2a46ef84fbc8d757d377c0cb4504f05f89d5249e45415ea58f491d86cb0"},
    {"path": "C:\\Bari\\tasks\\returns\\TASK-504B_design_critic_evidence\\desktop_top_crop.png", "sha256": "f6361464115c5996e0981b354fcbdb7b1317dd7c89221fae939bbca5ede3a63b"},
    {"path": "C:\\Bari\\tasks\\returns\\TASK-504B_design_critic_evidence\\hub_mobile.png", "sha256": "8cb0a42c95b9469a9d0d2279de92ddee2663449c05f57f0b0bf9a9f34b4c4c54"},
    {"path": "C:\\Bari\\tasks\\returns\\TASK-504B_design_critic_evidence\\geometry_mobile.json", "sha256": "b2dbaf4a0ae80dbf3cfe373c22c1e502cc293baa20c582d94ae8f207f66f4ac0"},
    {"path": "C:\\Bari\\tasks\\returns\\TASK-504B_design_critic_evidence\\geometry_desktop.json", "sha256": "2525520c09752f504c5e3689e317414bdedd12cf311e9a6a92fa72dd2ea8e354"},
    {"path": "C:\\Bari\\tasks\\returns\\TASK-504B_design_critic_evidence\\computed_styles.json", "sha256": "a78c134c4241c3fc6d8552ae57bda8071b1908b58ad27d6fa82462a50e4a5183"}
  ],
  "counts": {
    "findings_critical": 1,
    "findings_high": 3,
    "findings_medium": 2,
    "findings_low_nongating": 2,
    "findings_denominator": "all findings raised in this review, out of 7 guide component files + 1 shared badge component + 1 hub page fully read",
    "bar_state_badges_on_page": 108,
    "bar_state_badges_denominator": "18 product rows x 6 bars per GUIDE_BAR_ORDER, counted via live DOM query on data-bar-state attribute",
    "bar_state_distribution": {"pass": 33, "flag": 12, "fail": 16, "cannot_verify": 47},
    "bar_state_distribution_denominator": "counted out of the 108 total badges above",
    "product_rows_on_page": 18,
    "product_rows_denominator": "data-testid=guide-product-row count via live DOM query",
    "buckets_rendered": 3,
    "buckets_denominator": "out of 4 possible GUIDE_BUCKET_ORDER entries; clears_all correctly empty/hidden this run",
    "contrast_failures_found": 3,
    "contrast_failures_denominator": "out of 17 text/background pairs sampled across the guide page components",
    "viewports_rendered": 2,
    "viewports_denominator": "375x812 mobile + 1440x900 desktop, both fresh Playwright renders plus the 9 pre-supplied screenshots reviewed"
  },
  "commands_run": [
    {"command": "npm run build (in C:\\bari_wt_t504\\bari-web)", "exit_code": 0},
    {"command": "npm run start -- -p 4599 (background, C:\\bari_wt_t504\\bari-web)", "exit_code": "n/a (long-running, stopped via TaskStop after captures)"},
    {"command": "node _design_capture.mjs (Playwright screenshot + geometry, mobile+desktop)", "exit_code": 0},
    {"command": "node _design_capture2.mjs (Playwright computed-style pass on flagged text/bg pairs)", "exit_code": 0},
    {"command": "node _design_crop.mjs (header crops + /madrichim hub render)", "exit_code": 0},
    {"command": "node _design_fail_check.mjs (FAIL-state computed style + bar-state distribution count)", "exit_code": 0},
    {"command": "grep -rn ScoreChip|BariGradeBadge|gradeOf|bandOf src/components/guides/ src/app/madrichim/", "exit_code": 0, "result": "0 live usages, comment-only references"},
    {"command": "sha256sum on all 9 pre-supplied screenshots + 7 fresh evidence artifacts", "exit_code": 0}
  ],
  "not_done": [
    "Did not run npm run test:a11y / npm run test:visual / npm run lhci in the worktree — this review used direct Playwright + computed-style + manual WCAG contrast-formula verification instead, which is a valid substitute per the agent's Instruments table but is a different evidence trail than the named LIVE suites; recommend Frontend also run test:a11y after the H1-H3 fix so axe independently confirms the contrast fix at the exact rendered DOM (not just the corrected hex math).",
    "Did not review the /madrichim/creatine guide (not yet built per the worktree's own migration-TODO comments) or the Wave 3 migration itself (redirects, sitemap moves) — out of this task's stated scope (magnesium guide + its template).",
    "Did not review keyboard-only navigation / focus-visible states on the guide page (tab order through buy buttons, badge tooltips) — flagged as a gap, not performed, since the task brief scoped this pass to token/contrast/RTL/geometry/bar-state/buy-button/drift, not full keyboard-interaction audit.",
    "cannot_verify data-completeness (M2) routed to Nutrition/Content as a note; did not investigate the underlying data pipeline reason for the 44% rate — out of Design's lane."
  ],
  "acceptance_test_result": "NOT MET as-is for a straight GO: 1 CRITICAL + 3 HIGH findings block clean go-live of this template. GO-WITH-FIXES: the structural/RTL/geometry/state-completeness/honesty-framing acceptance criteria for the guide template are MET (verified via live render + DOM geometry, not assumed); the color-identity and contrast acceptance criteria are NOT MET and require the fixes listed under 'Required before GO' before this template is inherited by future guides."
}
```
