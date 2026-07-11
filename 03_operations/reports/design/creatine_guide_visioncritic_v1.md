# Creatine Buying Guide — Design Vision-Critic (TASK-504 Wave 2)

Route reviewed: `/madrichim/creatine` (worktree `C:\bari_wt_t504\bari-web`, served at
`http://localhost:4700` via a pre-existing `next start -p 4700` process — this review did not
start or stop that server). Rendered and measured with Playwright (`bari-web/scripts/vision-in.mjs`
plus targeted custom capture scripts for guide-specific selectors), 375×812 first, then 1440×900.
`@axe-core/playwright` run against the live route for the WCAG floor. No code was edited — findings
only.

## Verdict: **GO-WITH-FIXES**

One HIGH-severity, screenshot-confirmed legibility bug (text-over-text collision in the expanded
third-party-verification bar at mobile width) blocks a clean GO. Everything else the delegation
asked me to check — 6-bar collapsed density, gauge-vs-caption-bar mix, currency rendering, the
no-mascot header, tier-pill placement, and the WCAG floor — passes.

---

## 1. Six bars display (collapsed + expanded) — PASS

Collapsed compact-badge-row (`GuideProductRow`, `guide-product-row.tsx:162-175`, `data-testid="guide-compact-badge-row"`)
wraps cleanly to 3 rows of 2 chips at 375px, no crowding, no clipped text:

- `frame__mobile__row0-collapsed-in-context.png` — Thorne row, 3-line badge wrap, tier pill
  "(3) מומלץ מאוד" undisturbed above it.
- `custom__mobile__03-first-tier-collapsed.png` — 3 consecutive rows, consistent wrap behavior.

At 1440px all 6 chips sit on one line (`custom__desktop__04-ils-collapsed.png`,
`custom__desktop__04-usd-collapsed.png`) — no reflow issue at either end of the viewport range.
Magnesium (4 bars, never wraps past 2 lines) never exercised this wrap path — this is a genuinely
new case, and it holds.

## 2. Gauge-bars vs fact-caption-bars — mostly PASS, one HIGH bug

Confirmed in code and on screen: `formAbsorption` gets a plain-text fact caption ("המוצר: מונוהידראט",
no track — `threshold-bar-row.tsx:217-222,358-361`, deliberate per the evidence co-sign banning a
form ranking). `safety` gets **no caption at all**, not even a fact-caption — plain chip only
(`creatine-guide-data.ts:236`, "safety: no benchmark entry"). `doseAdequacy`, `thirdPartyVerification`,
`priceFairness`, `labelTransparency` all render a track (gauge or ladder anatomy) + caption.

Visually (`safety__mobile__row0-full-detail.png`, full 6-bar stack for the Thorne row) the rhythm
reads fine block-to-block — each bar is separated by a hairline `border-t` regardless of its own
height, so a caption-only or chip-only block doesn't look "broken," just quieter. One LOW note:
the task brief describes "form **+ safety** bars are fact-captions" but the code only gives form an
actual caption; safety shows zero text (by design, per its own comment — a uniform PASS gauge would
"look like a broken control"). This is defensible, not a defect — flagging the discrepancy between
brief and implementation for the record, not as a blocker. Optional non-blocking polish: give safety
a one-line static caption ("אין סף עליון מבוסס — אחיד לכל המוצרים") for closer parity with form.

**HIGH — real bug:** the ladder-anatomy tick-label block and the caption paragraph beneath it
collide (text-over-text) at <768px whenever (a) a tick label wraps to 2 lines AND (b) the caption
text is also long. Root cause, `bari-web/src/components/guides/threshold-bar-row.tsx`:

- Lines 271–296: the tick-label container is `min-h-[26px]` but its children (`lines 277-295`) are
  `position: absolute`. An absolutely-positioned child cannot grow its parent's height, so when a
  tick label wraps to 2 lines (`CREATINE_THIRD_PARTY_LADDER`'s middle tier "מוצהר, טרם אומת מול מאגר"
  reliably wraps at a ~125px column width), the container still reports only 26px tall.
- Lines 350–357: the caption `<p className="mt-1 ...">` is the tick container's normal-flow sibling
  (mobile has no `md:flex`, so children stack vertically). It positions itself 4px below the
  container's *reported* 26px height — i.e. on top of the tick label's real second line.

Confirmed by screenshot on two different products (not a one-off):
- `zoom__thirdparty-caption-thorne.png` / `safety__mobile__row0-full-detail.png` — Thorne,
  caption "המוצר: אומת מול מאגר (NSF, id 1204244)" visibly overlapping "מוצהר, טרם אומת מול מאגר".
- `zoom2__mobile__thirdparty-momentous.png` — Momentous, same collision with a different id.
- Confirmed **absent on desktop** (`zoom2__desktop__thirdparty-thorne.png`) — at ≥768px
  `md:flex md:items-center md:gap-3` (line 350) puts the track and caption side by side instead of
  stacked, so the vertical collision has no path to occur there. This is mobile-only, and mobile is
  the primary comprehension surface (Hard Rule 7).
- Not reproduced on the `labelTransparency` ladder for the same product (`zoom2__mobile__label-transparency-thorne.png`)
  — its captions are short, so no wrap-on-wrap collision, even though its tick labels also wrap.

Scope: I directly screenshot-confirmed the collision on 2/31 products. The shared root cause
(fixed-height absolutely-positioned tick container + long caption) is a property of the component,
not the data, so it will reproduce on every product whose `thirdPartyValueLabel` is long enough to
wrap — by grep, 22 of 31 products carry a caption longer than the short "לא נמצאה טענה" (Informed
Sport/Choice, NSF id, iTested, HASTA variants: `creatine-guide-data.ts:263-696`). I have **not**
screenshotted all 22 — treat "22/31 at risk" as a code-derived estimate, "2/31 visually confirmed"
as the hard number.

**Fix direction (Frontend):** give the tick-label container a height that actually reserves space
for a 2-line wrap at its own font-size/line-height (11px / 1.4 ≈ 15.4px/line → 2 lines ≈ 31px content
+ existing `mt-0.5` ⇒ raise `min-h-[26px]` to roughly `min-h-[34px]`, or compute it from
`multilineTicks` more precisely), or stop absolutely-positioning the tick spans so the container's
own height reflects its content instead of a hardcoded guess. Either fix is scoped to
`threshold-bar-row.tsx:273`; no data change needed.

## 3. Currencies — PASS (with one MEDIUM cosmetic bidi bug)

₪ renders correctly for the 18 Israeli-shelf products and $ for the 13 worldwide products
(`creatine-guide-data.ts:264-698`), and the price-gauge ratio is genuinely currency-agnostic —
each price is divided by its own-currency median (₪0.89 / $0.225, lines 181-182, 203-205) before
being placed on the shared `CREATINE_PRICE_GAUGE`, so ₪ and $ products land correctly on the same
0–2.5× track without mixing currencies. Confirmed visually: `zoom__price-caption-thorne.png` (USD,
gauge + caption), `custom__mobile__04-ils-collapsed.png`/`04-usd-collapsed.png` (both currencies'
collapsed rows).

**MEDIUM — bidi reorder:** every USD product whose `priceValueLabel` carries the "~" (approximate)
prefix renders with the tilde moved to *after* the price instead of before it. DOM/logical order is
`"~$0.27 ל-3 גרם"` (`threshold-bar-row.tsx:321`, and the same string ported verbatim into
`oneLinerHe` in `creatine-guide-data.ts`); the browser paints it `"$0.27~ ל-3 גרם"`. Confirmed on
both surfaces and both viewports:
- `zoom__price-caption-thorne.png` (mobile, expanded gauge caption)
- `zoom3__desktop__price-thorne.png` (desktop, same caption, no overlap present — so this is an
  independent bidi issue, not a symptom of the §2 overlap bug)
This is the classic bidi-neutral-character problem: `~` has no strong direction, sits between an
RTL run and an embedded LTR numeral+currency run, and the algorithm can attach it to either side.
By grep, 9 of 31 products carry a "~$" price label (`grep -c '"~\$' creatine-guide-data.ts` → 9);
all 9 are affected on every render of that string (one-liner + gauge caption). ₪ prices never use
"~", so Israeli-shelf products are unaffected.

**Fix direction (Frontend):** wrap the currency+number fragment in a bidi isolate so the algorithm
can't detach the leading mark — `<bdi dir="ltr">{valueLabel}</bdi>` around the `caption`/`oneLinerHe`
segment that contains "~$X", or a narrower fix scoped to just the "~$X" substring. Not a copy-wording
issue (I did not critique `oneLinerHe`'s wording per the task's instruction) — this is a rendering/
RTL-correctness defect in how the existing, correct string gets painted.

## 4. No hero mascot — PASS

`heroImage: null` (`creatine-guide-data.ts:721`, no creatine mascot asset exists yet). The header
degrades exactly as designed — no leftover `#FEFEFE` band, no empty gap, no orphaned container:
plain eyebrow ("מדריכים · בארי") + H1 ("איך לבחור קריאטין") + the 6 buying-rule cards, immediately.
Reads as an intentional, finished editorial header at both sizes:
- `custom__mobile__01-header.png` — single-column card stack, clean.
- `custom__desktop__01-header.png` — 3-column card grid (2 rows of 3), clean.

(One vision-in instrument note, not a page defect: my first capture of the 6-card list appeared to
show only 5 cards — that was the site's cookie-consent banner, a `position: fixed` overlay,
compositing over the bottom of a tall stitched element screenshot. Confirmed false alarm after
dismissing the banner and re-measuring — `header[data-testid='guide-buying-rule'] ul > li'` count = 6
on both viewports. Recorded here so the next reviewer doesn't re-chase it.)

## 5. Tier headers + cannot-assess placement — PASS

Colored pills confirmed for `very_recommended` (green, Check icon, "(3) מומלץ מאוד" —
`custom__mobile__03-first-tier-collapsed.png`) and `cannot_assess` (gray, HelpCircle icon,
"(1) לא ניתן להעריך", rendered in its own section **after** the 4 ranked tiers, never folded into
לא מומלץ — `custom__mobile__06-cannot-assess.png`, matches `guide-product-table.tsx:243-272`). Did
not independently screenshot the `recommended`/`good`/`not_recommended` pills this pass, but their
tone values are the same shared `GUIDE_BAR_TONE`/`TIER_TONE` map already measured for magnesium
(`guide-product-table.tsx:42-51`, contrast ratios documented in-code: 6.73:1 / 5.42:1 / 5.56:1 /
6.29:1 / 6.71:1, all clear AA) — no new palette introduced for creatine.

## 6. WCAG AA / RTL / mobile — PASS

`@axe-core/playwright` (`wcag2a` + `wcag2aa` tags) against `/madrichim/creatine` at 375×812 with 3
product rows expanded (so gauge/caption/ladder markup was in the DOM for the scan, not just the
collapsed state): **0 violations of any severity** (0 serious/critical, 0 minor/moderate). This
route is not yet in the committed `e2e/a11y.spec.ts` `ROUTES` list — I ran axe directly against the
live page rather than editing that spec (not my lane); recommend Frontend add
`/madrichim/creatine` (and `/madrichim/magnesium`) to that list so this becomes a standing gate
rather than a one-off manual run.

`dir="rtl"` confirmed set correctly throughout via `vision-in.mjs` geometry capture (hero-header,
hero-title, and the product-table wrapper all report `"direction": "rtl"`). No horizontal overflow
observed at 375px in any captured frame.

## Observation (out of my lane, routing not critiquing)

Every one of the 31 products' collapsed "price + buy" line reads "מחיר לא זמין" / dormant "בקרוב"
buy button (`pricing: null`, `buyUrl: null` hardcoded in every `buildProduct()` call,
`creatine-guide-data.ts:238-239`) — the real per-3g price only appears once a row is expanded. This
matches the project-wide dormant-`buyUrl` pattern (TASK-427) so it is not a rendering defect, but it
does mean the always-visible layer never shows a shoppable price. That is a product/data-wiring
question (does the affiliate-link wave populate `pricing` before go-live, or is price meant to live
only in the expanded gauge caption?), not a layout defect — noting it for Product/Frontend rather
than holding the design verdict on it.

## Screenshots (evidence, not committed — `.vision-in`-style scratch output)

All under `C:\Users\HP\AppData\Local\Temp\claude\c--Bari\b0971aeb-0178-4845-a428-689223cdc9d0\scratchpad\creatine-vision\`:
`madrichim-creatine__mobile.png`, `madrichim-creatine__desktop.png` (full-page baselines),
`custom__{mobile,desktop}__01-header.png` / `02-buyingrule-cards.png` / `03-first-tier-collapsed.png`
/ `04-{ils,usd}-collapsed.png` / `05-{ils,usd}-expanded.png` / `06-cannot-assess.png`,
`frame__mobile__row0-collapsed-in-context.png`, `frame__{mobile,desktop}__usd-row0-expanded-in-context.png`,
`zoom__thirdparty-caption-thorne.png`, `zoom__price-caption-thorne.png`, `zoom__oneliner-thorne.png`,
`zoom2__{mobile,desktop}__{label-transparency,thirdparty}-thorne.png`, `zoom2__mobile__thirdparty-momentous.png`,
`zoom3__desktop__{price,oneliner}-thorne.png`, `safety__{mobile,desktop}__row0-full-detail.png`.

## Not done / gaps

- Did not screenshot all 22 at-risk products for the §2 overlap bug — root cause + 2 confirmed
  reproductions is the evidence; exhaustive per-product capture was out of scope for a format review.
- Did not independently screenshot the `recommended`/`good`/`not_recommended` tier pills (relied on
  shared, already-measured token table).
- Did not run `npm run test:visual` (screenshot-diff) — this is a new route with no committed
  baseline yet; nothing to diff against. First baseline should be captured once §2/§3 are fixed.
- Did not add `/madrichim/creatine` to `e2e/a11y.spec.ts` (not my lane — recommending Frontend do it).

```json
{
  "task": "TASK-504-W2-design-visioncritic",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": "03_operations/reports/design/creatine_guide_visioncritic_v1.md", "action": "created", "sha256": "62802e7136511d583b7ac3cbf2b99a8d5249280b83e1942cb2d39320e00e9408"}
  ],
  "counts": {
    "products_total": "31/31 (creatine-guide-data.ts products array)",
    "products_with_tilde_price_bug": "9/31 (grep -c '\"~\\$' creatine-guide-data.ts)",
    "products_with_overlap_confirmed_by_screenshot": "2/31 (Thorne, Momentous)",
    "products_at_risk_of_overlap_by_code_estimate": "22/31 (thirdPartyValueLabel longer than the short 'לא נמצאה טענה' caption, grep-derived, not individually screenshotted)",
    "axe_violations_serious_or_critical": "0/0 (@axe-core/playwright, wcag2a+wcag2aa, 375px, 3 rows expanded)",
    "axe_violations_total": "0/0 (same run)",
    "buying_rule_cards_rendered": "6/6 (header[data-testid='guide-buying-rule'] ul > li, both viewports)"
  },
  "commands_run": [
    {"cmd": "node scripts/vision-in.mjs --route /madrichim/creatine --base http://localhost:4700 --viewport both", "exit_code": 0},
    {"cmd": "node scripts/_tmp_vision_creatine_custom.mjs (targeted guide-selector screenshots, deleted after use)", "exit_code": 0},
    {"cmd": "node scripts/_tmp_vision_creatine_rows.mjs (single-frame resting-scroll captures, deleted after use)", "exit_code": 0},
    {"cmd": "node scripts/_tmp_vision_creatine_zoom*.mjs (zoomed bar-level crops + DOM text extraction, deleted after use)", "exit_code": 0},
    {"cmd": "node scripts/_tmp_vision_creatine_axe.mjs (@axe-core/playwright scan, deleted after use)", "exit_code": 0},
    {"cmd": "grep -c '\"~\\$' src/lib/guides/creatine-guide-data.ts", "exit_code": 0},
    {"cmd": "grep -n 'thirdPartyValueLabel:' src/lib/guides/creatine-guide-data.ts", "exit_code": 0}
  ],
  "not_done": [
    "Did not screenshot all 22 code-estimated at-risk products for the overlap bug (2 confirmed by direct screenshot)",
    "Did not independently re-verify recommended/good/not_recommended tier-pill contrast (relied on shared documented token measurements)",
    "Did not run npm run test:visual (no committed baseline exists yet for this new route)",
    "Did not add /madrichim/creatine to e2e/a11y.spec.ts ROUTES (routing to Frontend, not my lane)",
    "Did not edit any code (Design Agent is a critic on this task, per the delegation)"
  ],
  "self_check": "Acceptance test = 'GO / GO-WITH-FIXES / NO-GO on the FORMAT, backed by screenshot + geometry evidence, no code edits.' Result: GO-WITH-FIXES, blocked on one HIGH (threshold-bar-row.tsx:273 tick-container height causing caption/tick-label text overlap at <768px) and one MEDIUM (threshold-bar-row.tsx:321 bidi tilde reorder on '~$X' captions) — both screenshot-confirmed with file:line root cause; everything else in the 6-point checklist passed with cited evidence."
}
```
