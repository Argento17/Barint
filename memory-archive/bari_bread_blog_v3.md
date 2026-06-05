---
name: bari-bread-blog-v3
description: "Bread blog reset v3: 2 Cursor-ready implementation handoffs replacing the failed 3-article system; milk comparison as golden standard; investigation-first architecture; real product data from bread_retail_002"
metadata: 
  node_type: memory
  type: project
  originSessionId: 0992f16e-b33f-475c-a0cf-6a0c70b3da1d
---

Built 2026-05-27. Master document at `C:\Bari\02_products\bread_retail_002\bread_blog_v3.md`.
Replaces: `blog_handoffs_v2.md`
Dataset: `real_bread_retail_002_v2_frontend_dataset.json`

**Why:** The v2 system failed structurally (fragmented comparison cards, no editorial spine, vague score causality). Reset around milk comparison golden standard: one coherent investigation per article, products as evidence inside the narrative.

**How to apply:** These are the active Cursor implementation handoffs for bread. Any future bread content changes reference this document.

## Two Articles

**Article 1: "הלחם שאתה קונה בכל שבוע"** — /bread/everyday
- Editorial spine: Ingredient list position explained most of the score gap, not the product name
- Key finding: Simple whole-grain compositions outscored complex enriched ones
- Key contrast: לחם שיפון קל (75/B, 12.4g matrix fiber) vs. לחמניות לס קיטו (not scored, 17.4g added fiber)
- 4 InsightCards, BreadEverydayMap (grain structure × fiber source), CompositionBreakdown (5 dimensions), 2 comparison pairs

**Article 2: "מה שכתוב לא תמיד מה שיש"** — /bread/wellness
- Editorial spine: Wellness segment showed widest divergence — driven by fermentation naming, כוסמין qualifier, fiber source
- Key finding: 13 "מחמצת" products had industrial yeast as primary leavener; highest score (82/A) went to cracker not bread
- Key contrast: לחם שיפון קל (75/B, fermentation_real=true) vs. לחם מחמצת שיפון (74/B, fermentation_real=false, same score)
- 5 InsightCards, BreadWellnessMap (grain verification × fermentation), ThreeGapBreakdown (3 named gaps), 3 comparison pairs

## New Components (must be built by Cursor)

1. BreadEverydayMap — scatter/cluster, grain structure × fiber source axes
2. BreadWellnessMap — scatter/cluster, grain verification × fermentation axes; Cluster C annotation required
3. CompositionBreakdown — 5-row section explaining observable score dimensions (Article 1)
4. ThreeGapBreakdown — 3-panel section showing fermentation/spelt/fiber gaps (Article 2)
5. ProductComparisonMatrix — table + prose, NOT card duels

## Critical Rules

- Score=40 for insufficient products is a technical floor, NOT a real score. Display "לא נוקד"
- displayable=false → show "—" not a number
- Fermentation mismatch products are documented as a pattern, not accused as fraudulent
- No recommendation language anywhere. One footer disclaimer per article. Zero body disclaimers.

[[bari-assertive-writing-v1]]
[[bsip2-bread-retail-002-frontend]]
