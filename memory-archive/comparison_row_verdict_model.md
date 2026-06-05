---
name: comparison-row-verdict-model
description: Bari comparison-page row = a 2-line interpretive VERDICT (not a terse tag); dropdown = full analysis + nutrition
metadata: 
  node_type: memory
  type: project
  originSessionId: b6225074-158c-4f75-b996-399c426d91ef
---

The Bari comparison-page **collapsed row description** is a **2-line interpretive VERDICT** written as a real human assessment by the Content writer: STANDING in the category → WHY (the real drivers) → the CATCH → the **earned grade** ("עוצר ב-B כי…"). It must be **differentiated per product** (no shared sentence skeleton; lead from whatever is genuinely distinctive about each one) and reader-first. The **dropdown/expansion** shows the full analysis (מה עובד / מה מגביל / בשורה תחתונה) + real nutrition values + ingredients — that was already built in `expansion-section.tsx`.

**Mechanism:** the verdict text is authored into each product's `insightLine` in `bari-web/src/data/comparisons/*.json`, and the page-data enrichers route it to `rowVerdict` (the multi-line slot) — `comparison-row.tsx` renders `rowVerdict` first; its `line-clamp` was removed (TASK-168F) so the full verdict shows and the row grows to fit. Standard: `01_framework/editorial/row_description_standard_v1.md` (v2 verdict model). Per-category truth limits: `01_framework/editorial/row_description_grounding_v1.md` (e.g. hummus: no fat/sugar; cheese: sodium/sat-fat outside score so high≠healthy; snacks: nutrition all-null, only trace ingredient figures; bread: no energy/sugar/fat, sourdough only where signal asserts; yogurts: sugar only where non-null, ceiling B).

**Why:** the owner (2026-06-02, TASK-168) rejected terse one-line tags as "mechanical" AND rejected a full page redesign as over-build — Product showed the rest of the Gen-1 page is validated; the real gap was that the strong verdict field was never authored at scale. Approved on the **maadanim pilot**, then rolled out to hummus/cheese/yogurts/snacks/bread. Owner has per-product comments to apply in a later refinement pass.

**How to apply:** when writing/reviewing comparison row copy, write the verdict, not a label; differentiate genuinely; ground every claim in the product's real data (no invention); keep ~2 lines. Don't reintroduce the +/− tags or terse one-liners. Relates to [[bari_insight_line_spec_v1]], [[bari_comparison_template_v1]], [[feedback_plain_english]].
