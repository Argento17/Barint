---
name: bari-snack-bar-blog-v1
description: "Snack bar editorial investigation v1 — 2 Cursor-ready handoffs; Article 1 everyday/cereal/granola, Article 2 protein/wellness/natural; bar-native decomposition (5 dims); date bar 70/B is the category outlier; protein bars 45-47/D; BSIP2 re-run required before Cursor build"
metadata: 
  node_type: memory
  type: project
  originSessionId: 8af7e0b5-ff02-43a8-b8df-e8e443e61a10
---

Built 2026-05-27. Master document at `C:\Bari\02_products\snack_bars\snack_bar_blog_v1.md`.
Dataset: run_snack_bars_synthesis_001 — 53 products, Yohananof, May 2026.
Architecture: mirrors bread_blog_v3.md + refinement_v1.md.

**Why:** Previous snack bar work predates the stabilized editorial architecture. This starts from scratch using the milk/bread investigation model.

**How to apply:** These are the active Cursor implementation handoffs for snack bars. All future snack bar content references this document. Requires BSIP2 re-run before implementation.

## Two Articles

**Article 1: "החטיפים שרוב ישראל קונה"** — /snack-bars/everyday
- Editorial spine: 59% of the shelf is NOVA4; every NOVA4 product scored D or E
- Key finding: "Fitness" and "Energy" branding found on products in 17–46 range
- Key contrast: קראנצ'י שיבולת שועל ודבש (53/C, NOVA3) vs. פיטנס בר גרנולה שוקולד מריר (17/E, NOVA4)
- Components: SnackBarShelfMap (processing depth × sweetener architecture), BarCompositionBreakdown (5 bar-native dimensions), 2 comparison pairs

**Article 2: "פרוטאין, 'טבעי', פיטנס: מה הרכיבים הראו"** — /snack-bars/wellness
- Editorial spine: Only B in entire dataset = 4-ingredient date bar (70/B). All protein bars = D (45–47). 23-point gap.
- Key finding: Name-composition misalignment in all three wellness positioning types (protein/natural/fitness)
- Key contrast: חטיף תמרים במילוי חמאת שקדים (70/B, NOVA2, 4 ingredients) vs. Nature Valley Protein (47/D, NOVA4, 15+ ingredients)
- Components: SnackBarWellnessMap (simplicity × positioning), ThreeMisalignmentBreakdown (protein/natural/fitness gaps), 3 comparison pairs

## Bar-Native Decomposition (5 Dimensions)

1. מקור הבסיס — structural base (whole food / processed / engineered)
2. ארכיטקטורת הסוכר — sweetener architecture (single source / multiple added)
3. עומק העיבוד — processing depth (NOVA2/3/4)
4. עומס התוספות — additive load (0–2 / 3–4 / 5+)
5. יחסיות ההצגה — name-composition alignment

## Key Dataset Facts

- Score range: 13.4 (E) to 70 (B)
- No A grades. One B: date bar.
- NOVA4 = 59% of shelf. All NOVA4 = D or E.
- Protein bars (Nature Valley): 45–47/D
- Date bars (NOVA2): 55–70/B–C
- "Fitness" branded products: 17–46 range (D–E mostly)
- "Energy" branded products: 18–31/E

## Pre-Implementation Requirements

- BSIP2 re-run needed: ingredients_raw currently empty in BSIP1 source
- Granola routing needs stabilization (granola_bar archetype gap)
- Frontend dataset JSON must be generated (matching bread format)

[[bari-bread-blog-v3]]
[[bsip2-snack-bars-001]]
[[bari-bread-refinement-v1]]
