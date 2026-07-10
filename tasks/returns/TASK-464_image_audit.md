# TASK-464 — Product-Image White-Background Audit

**Scope:** read-only. Zero git writes. Source of truth = `origin/master` — all 16 category JSONs
extracted via `git show origin/master:bari-web/src/data/comparisons/<file>` (identical file set /
version resolutions as `tasks/returns/TASK-461_fanout_audit.md`). All 580 products across the 16
live categories were audited. Images downloaded to scratchpad `images/` (580/580 succeeded, 0 dead).

**Scripts:** `download_images.py` (fetch), `classify_images_v2.py` (pixel classification — v2, see
methodology note below on why v1 was discarded). **Raw output:** `t464_image_metrics.json`.

---

## Step 1 — Rendering context: what "should blend" actually means here

Traced the full render path for every comparison-page product thumbnail:

- **Canonical thumbnail component:** `bari-web/src/components/comparisons/bari-product-thumbnail.tsx`
  (`BariProductThumbnail`). Used by **all 16 audited categories** via the single shared row renderer
  `bari-web/src/components/shared/comparison-row.tsx:186-190`.
- **The tile background is cream `#F7F7F2`, not white**, by design (`bari-product-thumbnail.tsx:48`):
  `border border-black/[0.06] bg-[#F7F7F2] shadow-sm`. A `blendWhite` prop exists
  (`bari-product-thumbnail.tsx:13,29,46-48`) that swaps the tile fill to pure white — **but it is wired
  to fire for exactly one category**: `comparison-row.tsx:189` → `blendWhite={category === "magnesium"}`.
  Magnesium is not one of the 16 audited comparison categories (it's the supplements page). **None of
  the 16 categories in scope receive `blendWhite` — every one of them renders product photos inside the
  default cream `#F7F7F2` tile.**
- **Page chrome around the tile:** outer page background `#EFEFEB` (light gray-beige) → white card panel
  (`comparison-page.tsx:245`, `bg-white`) → row background alternates `#FFFFFF` (odd) / `#FBFBF9` (even)
  per `globals.css:446-451`. So the tile itself sits on a background that is white or near-white
  already — the cream `#F7F7F2` fill is a deliberate ~3% off-white distinguishing frame (with a hairline
  border + soft shadow) so a contained product photo reads as "a photo in a frame," not "a floating box."
- **No second image slot exists.** The expansion panel (`expansion-section.tsx`) does not re-render the
  product photo — confirmed via grep, no `Thumbnail`/`imageUrl` reference in that file. One thumbnail
  slot per product, one component, one background token, project-wide (magnesium excepted).
- **Existing CSS mitigation:** `overflow-hidden rounded-2xl` on the tile (clips the image to match the
  frame's rounded corners) + `object-contain p-2` on the `<img>` (2px inset padding, contain-not-cover,
  so the photo never bleeds to the tile edge). **No `mix-blend-mode` anywhere in this component** — the
  only blending strategy is the cream-vs-white color proximity, not a CSS blend mode.

**What "blends" vs "visible box" means concretely:** because the tile is cream (not pure white) and the
row is white/near-white, *any* opaque product photo — regardless of its own background color — sits as a
padded, rounded, bordered, shadowed square inside a slightly-tinted frame. A pure-white product photo
background is barely distinguishable from the cream tile (soft mismatch, low severity). The visually
jarring case the owner is describing is most likely non-white opaque backgrounds (gray studio backdrops,
off-white with a color cast) that read as a **visibly separate colored square** against the row/tile, or
white-background photos that are large/high-contrast enough that the border + shadow reads as a "sticker"
rather than a photo. Both cases are driven entirely by **the source photo's own baked-in background**,
not by anything the frontend controls per-product — the frontend renders one uniform tile treatment
for all 16 categories.

---

## Step 2 — Methodology note (classifier v1 → v2)

First pass (`classify_images.py`, v1) sampled full edge-strips (top/bottom/left/right bands) for the
opaque/near-white test. This **catastrophically misclassified milk_v1 and juices_v3** (100% "opaque
non-white" in v1) because those two categories are photographed as **tall bottle/carton crops**
(avg height/width ≈ 2.5–2.8, vs ≈1.0 for every other category) where the product fills almost the
entire frame — the top/bottom "edge strip" catches cap/label pixels, not a background margin, so the
strip average is a blend of product-body colors, not the true canvas background.

**v2 fix** (`classify_images_v2.py`, the version whose output is authoritative here): samples only the
4 **corner patches** (reliable background even in a tight crop), takes their color consensus, and cross-
validates with a downscaled flood-fill from the border inward to estimate what fraction of the frame is
actually uniform background (`bg_flood_fraction` in the JSON) — flagging `tight_crop: true` when the
flood fill can't expand past ~15% of the image (i.e., the corner color is a small isolated patch, lower
classification confidence, mostly seen in milk/juices/cakes/cookies-coffee tight product-fills-frame
shots). This was verified by eye: a milk carton with a genuine white background sample
(`milk_7290000051352`) correctly classifies WHITE_BOX; a green goat-milk carton whose angled photo puts a
sliver of green carton in the top corners (`milk_7290102392094`) correctly classifies OTHER_OPAQUE, not
WHITE_BOX — the classifier is reading real corner content, not guessing.

**Classification categories (final, v2):**
- `BLENDS` — real alpha channel, ≥50% of corner pixels genuinely transparent.
- `WHITE_BOX` — opaque (no alpha, or alpha present but corners fully opaque), corner-consensus RGB all
  channels ≥240.
- `OTHER_OPAQUE` — opaque, corner-consensus below the white threshold (gray/tan/colored studio backdrop,
  or a tight crop where the corner itself shows product color).
- `DEAD` — download/decode failure. **0 of 580** in this audit — all images fetched cleanly.

---

## Overall corpus result (580 products, 16 categories)

| verdict | count | % of corpus |
|---|---|---|
| BLENDS (real transparency) | 318 | 54.8% |
| WHITE_BOX (opaque white/near-white bg) | 201 | 34.7% |
| OTHER_OPAQUE (opaque non-white bg) | 61 | 10.5% |
| DEAD | 0 | 0.0% |

**Over 45% of all product photos across the live site (262/580) are opaque with a hard rectangular
background** — the class of defect the owner is describing. Roughly 3 in 4 of those are white/near-white
(the specific "opaque white box" complaint); the rest are gray/tan/colored studio backdrops, which read
as an equally visible but differently-colored box.

**Provenance root cause, confirmed at the pixel level:** the corpus draws from two retailer image
pipelines with categorically different cutout behavior:

| source | n images | BLENDS | WHITE_BOX | OTHER_OPAQUE | blend rate |
|---|---|---|---|---|---|
| Cloudinary/Shufersal (`res.cloudinary.com/shufersal/...`) | 504 | 316 | 169 | 19 | 62.7% |
| Shufersal direct | 2 | 2 | 0 | 0 | 100% |
| Yochananof (`api.yochananof.co.il` / `yochananof.co.il`) | 74 | **0** | 32 | 42 | **0%** |

**Yochananof-sourced photos never blend — 0 of 74.** Every single one is a flat opaque JPG with a baked-
in background (white or a colored studio backdrop). This is a hard, structural, retailer-level pattern,
not per-product noise.

**Cloudinary/Shufersal is a genuinely mixed bag** — same CDN, same `.png` file format, same URL
pattern (`.../products_zoom/<code>_1.png`), yet **individual products differ in whether the PNG has a
real alpha cutout or is a flat opaque PNG with a white square baked in.** Verified directly: two hummus
products from the identical Cloudinary path pattern —
`SIZ44_Z_P_7290110564360_1.png` (`bsip1_7290110564360`) loads as PIL mode **RGB**, no alpha, opaque
white background start-to-finish (900×900) — vs
`bsip1_7296073725404`'s PNG, same pattern, loads as PIL mode **RGBA**, genuine transparent cutout. This
is the single most important finding: **the defect isn't "some categories are bad," it's "products
within the same category, from the same retailer, are inconsistently cut out."** That inconsistency is
exactly what produces the jarring effect the owner flagged — a shelf where most thumbnails float cleanly
and a few sit in visible white/gray boxes right next to them.

---

## Per-category table (ranked worst → best by WHITE_BOX rate)

| category | N | BLENDS | WHITE_BOX | OTHER_OPAQUE | blend% | white-box% | other-opaque% | total-fail% | consistency |
|---|---|---|---|---|---|---|---|---|---|
| **milk_v1** | 18 | 0 | 14 | 4 | 0.0% | **77.8%** | 22.2% | 100.0% | uniform-bad (Yochananof only) |
| **hummus_v5** | 57 | 16 | 40 | 1 | 28.1% | **70.2%** | 1.8% | 71.9% | **mixed — worst UX** |
| **juices_v3** | 17 | 0 | 9 | 8 | 0.0% | **52.9%** | 47.1% | 100.0% | uniform-bad (Yochananof only) |
| hard_cheeses_v4 | 31 | 11 | 16 | 4 | 35.5% | 51.6% | 12.9% | 64.5% | **mixed** |
| cheese_v5 | 47 | 23 | 24 | 0 | 48.9% | 51.1% | 0.0% | 51.1% | **mixed** |
| snacks_v5 | 21 | 11 | 10 | 0 | 52.4% | 47.6% | 0.0% | 47.6% | **mixed** |
| cereals_v2 | 20 | 11 | 9 | 0 | 55.0% | 45.0% | 0.0% | 45.0% | **mixed** |
| protein_combined_v2 | 32 | 19 | 13 | 0 | 59.4% | 40.6% | 0.0% | 40.6% | **mixed** |
| brined_cheeses_v2 | 36 | 24 | 12 | 0 | 66.7% | 33.3% | 0.0% | 33.3% | mixed (mostly clean) |
| chocolate_tablets_v1 | 35 | 25 | 10 | 0 | 71.4% | 28.6% | 0.0% | 28.6% | mixed (mostly clean) |
| crackers_v1 | 19 | 14 | 5 | 0 | 73.7% | 26.3% | 0.0% | 26.3% | mixed (mostly clean) |
| bread_v4 | 23 | 13 | 6 | 4 | 56.5% | 26.1% | 17.4% | 43.5% | **mixed** |
| cakes_hard_cookies_v1 | 62 | 35 | 14 | 13 | 56.5% | 22.6% | 21.0% | 43.5% | **mixed** |
| chocolate_bars_v1 | 23 | 19 | 4 | 0 | 82.6% | 17.4% | 0.0% | 17.4% | mostly clean |
| cookies_coffee_v2 | 117 | 76 | 14 | 27 | 65.0% | 12.0% | 23.1% | 35.0% | mixed (large N) |
| **granola_v2** | 22 | 21 | 1 | 0 | 95.5% | 4.5% | 0.0% | 4.5% | **cleanest category** |

"Consistency" column: **uniform-bad** = every product fails the same way (single retailer, no visual
inconsistency within the shelf, but 100% opaque); **mixed** = the category has both blending and
non-blending photos side by side — this is the worst experience because it's visually inconsistent row
to row, exactly the "some blend, some don't" pattern the owner's screenshots show.

### Worst offenders (concrete products, for spot-checking)

- **hummus_v5** (70% white-box, largest mixed category): `bsip1_7290110564360` (חומוס עשיר ב-40%
  טחינה), `bsip1_7290110579319` (חומוס גלילי), `bsip1_7290011800642` (סלט מטבוחה מרוקאית) — all opaque
  white PNGs from Cloudinary sitting next to correctly-cutout products in the same shelf.
- **milk_v1** (78% white-box, 100% opaque corpus-wide): `milk_7290000051352` (חלב מלא תנובה, "בטעם של
  פעם"), `milk_7290019790259`, `milk_7290114313865` — every milk photo (Yochananof-sourced) is a flat
  studio shot; none blend. Because 100% fail uniformly, the shelf itself doesn't look "broken" in
  isolation the way hummus does, but it never achieves the blended look either.
- **juices_v3** (100% opaque, split roughly evenly white vs colored-backdrop): `jc-003` (מיץ תפוזים
  ולנסיה, white bg), `jc-005`/`jc-011`/`jc-002` (gray-green backdrop, OTHER_OPAQUE) — same retailer,
  same product type, two different studio backdrop colors.
- **cheese_v5** (51% white-box): `bsip1_cheese_4127329` (קוטג' 5%), `bsip1_cheese_41445` (קוטג' 5%),
  `bsip1_cheese_474502` (גבינה לבנה 5%) — cottage-cheese tub photos, opaque white square, right next to
  blending competitors.
- **hard_cheeses_v4** (52% white-box + 13% other-opaque = 65% total fail): `bsip1_hardcheese_7290110324872`
  (גבינת גלבוע 5%), `HC-4137311`, `HC-52311`.

Full per-product verdicts (all 580, with RGB stats and reasoning) are in `t464_image_metrics.json`.

---

## Recommended fix path (ranked)

1. **Immediate, cheap, uniform — CSS containment fix (do this first, ships same day).** Since every
   category already renders through the single shared `BariProductThumbnail` component, add a **white
   chip mask**: change the default tile fill from cream `#F7F7F2` to pure white (i.e., extend the
   existing `blendWhite` behavior to be the default for all categories, not just magnesium — or simplify
   further and just delete the conditional, since cream-vs-white was never doing real work against
   opaque photos anyway). This does **not** fix `OTHER_OPAQUE` (gray/tan/colored backdrops — 61 products,
   10.5%) since no single fill color can match those, but it silently repairs all 201 `WHITE_BOX` cases
   for free — the photo's baked-in white square becomes indistinguishable from the tile itself. This is
   a **one-line class change**, zero data work, immediately removes the majority defect class (201/262
   = 77% of all opaque-background failures). Residual `OTHER_OPAQUE` cases would still show a visible
   colored box, but at 10.5% of the corpus (and 0% in 9 of the 16 categories) this is a much smaller,
   more tolerable residual.
2. **True fix — rembg cutout regeneration, targeted at the 262 opaque offenders.** Owner has `rembg`
   installed. Since this audit already identifies the exact 262 failing product IDs + local cached
   source images (`images/` in this scratchpad, filenames `<category>__<id>__<hash>.<ext>`), a follow-up
   task can run rembg over exactly that set (not all 580 — the 318 that already blend don't need
   touching) to produce real alpha-channel PNGs, replacing the `imageUrl` for those products only. This
   is the only fix that also solves `OTHER_OPAQUE` (colored backdrops), which the CSS fix cannot touch.
   Effort scales with 262 images, not 580.
3. **Per-retailer re-scrape (lowest priority, not recommended as primary path).** Since Yochananof is
   structurally 100% opaque (0/74 blend), a future BSIP0 re-scrape preferring Shufersal's cutout images
   over Yochananof's for any product available from both would raise the blend rate for milk/juices
   specifically — but per the scrape source-selection policy this must go through the standard
   cross-check waterfall, not be special-cased for image quality alone, and does not address the
   Cloudinary-internal inconsistency (the largest share of the problem) at all.

**Recommendation: do #1 immediately (near-zero cost, fixes 77% of the defect class uniformly across all
16 categories with one shared-component change), then queue #2 as a scoped follow-up task against the
262-item defect list this audit produced** (`t464_image_metrics.json`, filter `verdict != "BLENDS"`).
Do not pursue #3 unless #1+#2 leave a category still visibly broken after re-render.

---

## Categories: consistent vs mixed (mixed = worst UX, per task framing)

- **Uniform-bad (single retailer, 100% one failure mode, at least visually consistent shelf-to-shelf):**
  milk_v1, juices_v3.
- **Mixed (the worst pattern — some products blend, others sit in a visible box right next to them on
  the same shelf):** hummus_v5, hard_cheeses_v4, cheese_v5, snacks_v5, cereals_v2, protein_combined_v2,
  brined_cheeses_v2, chocolate_tablets_v1, crackers_v1, bread_v4, cakes_hard_cookies_v1,
  cookies_coffee_v2. That's **12 of 16 live categories** showing the inconsistent pattern.
- **Cleanest:** granola_v2 (95.5% blend rate, only 1 white-box product out of 22) and chocolate_bars_v1
  (82.6% blend rate).

No category is OFF-hosted (0 openfoodfacts hits across all 580 imageUrls — confirmed, not a provenance
breach).

## Caveats / limitations

- Classification is corner + flood-fill heuristic, not a full segmentation model — very rare edge cases
  (e.g. a product photographed on a white surface photographed at an angle that puts product in only 2
  of 4 corners) could be misclassified; the `tight_crop` flag in the JSON marks lower-confidence rows
  (49 of 580, concentrated in milk/juices/cakes/cookies-coffee) for manual spot-check if a tighter number
  is needed before shipping a fix.
- WHITE_THRESH=240 and NEAR_WHITE_RATIO=0.90 are reasonable but adjustable; a couple of `WHITE_BOX` calls
  sit at the boundary (near_white corner-consensus in the 240-250 range) — visually confirmed via direct
  image inspection (2 spot-checks) that the classifier's read matches what a human sees.
- This audit does not re-render the actual live pages (no screenshot/DOM check) — it validates the
  render **contract** (component code + tokens) and the **source images** independently, then reasons
  about how they compose. A visual DOM screenshot pass (Design Agent) would be the natural verification
  step before/after any fix ships.
