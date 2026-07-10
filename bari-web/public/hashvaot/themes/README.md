# /hashvaot Theme Images — Process Reference

This folder holds the stock category photos rendered on the `/hashvaot` index cards. One `.jpg` per category. This document records how to correctly add a new one.

---

## When this is needed

Each `/hashvaot` index card renders a stock category photo via `theme={{ photo: "/hashvaot/themes/{slug}.jpg" }}` in its component at `src/components/hashvaot/featured-{category}-intelligence-card.tsx`. If the referenced file is missing from this folder, the card renders blank.

Symptom: "some cards have no photo on /hashvaot."

---

## Diagnosis

Cross-reference the `photo:` path each `featured-*-intelligence-card.tsx` references against the files actually present in this folder. Any referenced filename with no corresponding file = a blank card to fix. The filename in the component and the file in this folder **must match exactly** (case-sensitive).

---

## Image spec

Match the look of the existing themes (`hard-cheeses.jpg`, `cheese.jpg`, `hummus.jpg`).

| Property | Requirement |
|---|---|
| Subject | Stock GENERAL CATEGORY mood shot — an appetizing photo of the food category, not a specific product, brand, or package |
| Dimensions | 900×600 px, landscape 3:2 JPEG |
| Why 3:2 | Cards use `object-cover`; 3:2 crops cleanly. A few legacy themes vary (e.g. `juices.jpg` is 800×1200), but **900×600 is the target for all new files** |
| Style | Editorial food photography: soft natural light, neutral/wood/linen/stone surfaces |
| Hard prohibitions | No text, no logos, no brand packaging or labels, no people or hands, no watermarks |

---

## Sourcing

**Default — free-license stock photography (Unsplash License).** Free for commercial use, no attribution required. This is what was used for the three photos added on 2026-06-18 and is the preferred method — real photos avoid the artificial look of AI generation.

**AI generation is a fallback only** if no suitable free-license stock exists AND the owner explicitly approves. Owner concern on record: AI food photos can look artificial.

**Never use Open Food Facts or any product-image source.** These are generic category mood photos, never product shots.

---

## Shared-tree hazard (critical — read before sourcing via any cloud CLI)

Cloud CLIs (Grok, Cursor, Gemini) bulk-upload the repo and run `git stash -u` on the whole shared tree when invoked with `cwd=C:\Bari`. This will wipe untracked files across the entire monorepo.

**Safe procedure:**
1. Download or generate the image into an isolated temp directory **outside** `C:\Bari`.
2. Inspect and approve the image there.
3. Copy **only** the final `.jpg` into this folder (`C:\Bari\bari-web\public\hashvaot\themes\`).
4. Run `git status --short` immediately after. Confirm: only additions, zero deletions.

---

## Verify before deploy

1. Open the file and confirm it is a valid JPEG at approximately 900×600 px.
2. Visually inspect: appetizing, on-style, none of the prohibited elements present.
3. `git status --short` — only the new theme file(s) added, nothing deleted tree-wide.
4. Commit **only the specific image files** — never `git add -A` (the tree is shared). Push to `origin/master`; Vercel auto-deploys.
5. After ~1–2 min build + CDN propagation, confirm the live URL `https://bari.digital/hashvaot/themes/{slug}.jpg` returns a valid JPEG (not a 404). Ask the owner to hard-refresh if they cached the blank state.

---

## Files added 2026-06-18

| File | Source | Dimensions | Size |
|---|---|---|---|
| `brined-cheeses.jpg` | Unsplash | 900×600 | ~96 KB (98,014 bytes) |
| `cakes-hard-cookies.jpg` | Unsplash | 900×600 | ~86 KB (87,667 bytes) |
| `cookies-coffee.jpg` | Unsplash | 900×600 | ~58 KB (59,615 bytes) |

## Files added 2026-07-09

| File | Source | Dimensions | Size |
|---|---|---|---|
| `yogurt-drinks.jpg` | Unsplash `photo-1650265929240`, **hand-cropped** (see below) | 900×600 | ~52 KB (53,712 bytes) |

`yogurt.jpg` (strawberry jars) had been shared by BOTH yogurt cards. Owner ruling 2026-07-09:
the strawberry jars read as **dense/spoonable** yogurt, so `yogurt.jpg` stays on the spoonable
card (`/hashvaot/yogurt`), and the **drinks** card is the one that needed a distinct photo —
now `yogurt-drinks.jpg` (a drinkable yogurt in a glass, matching "משקאות יוגורט לשתייה").

### Cropping matters more than you'd think — two traps hit here

1. **The card shows only the horizontal CENTRE ~56% of the file.** `ComparisonIntelligenceHero`
   paints the photo into a portrait box (`w-[60%]`, `background-size: cover`, `position: center`).
   For a 900×600 file that means **only x ∈ [198, 702] is ever visible.** Put the subject there or
   it will be cropped away. The source's straight 3:2 auto-crop put the glass off-centre and the
   card rendered the background plate instead.
2. **The photo sits behind a light gradient at `opacity: 0.62`, so low-contrast images wash out
   to nothing.** A white drink on white linen rendered as a near-blank card. Match the profile of
   a theme that reads well — measure the visible band, don't eyeball the whole file:

   | | contrast (L stddev) | luminance | saturation |
   |---|---|---|---|
   | `yogurt.jpg` (reads well) | 49.8 | 201 | 42 |
   | first drinks crop (washed out) | 33.9 | 199 | 39 |
   | shipped `yogurt-drinks.jpg` | 48.9 | 178 | 54 |

   Rule of thumb: **visible-band contrast ≥ 45 and luminance ≥ 165.** The shipped crop centres the
   glass and pulls the kiwi in as a colour anchor. The source's bright-yellow backdrop was cropped
   out entirely (all other themes are neutral linen/marble/stone).

Candidates rejected during sourcing, as a record of the prohibitions in action: one had visible
branded packaging + text (hard prohibition); one had granola as the dominant subject (granola is
its own category card); one was a dark moody fermentation jar (off-style — all themes are light,
and a jar is not a drink); one showed bottles on a blue cloth outdoors (not editorial). Five
further candidates passed the contrast screen but were all **dark** (luminance 91–128) and would
have clashed with the light card family.
