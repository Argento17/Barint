---
name: bari-category-caveat-standard
description: "The cheese-style \"הערת קטגוריה\" caveat box is now the required standard on every comparison page (owner directive 2026-06-02)"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: ea7007fb-62f6-4f59-8848-cda2436ef7a6
---

The cheese-style **"הערת קטגוריה"** yellow caveat box is now the STANDARD on every Bari comparison page, not a cheese one-off. Owner directive (2026-06-02): "this is a brilliant caveat which really helps the reader understand the scoring. I expect this to be the standard for all comparisons." Shipped to all 8 live categories under TASK-157 (CLOSED).

**Why:** the caveat names a real, category-specific scoring nuance that helps a reader interpret the score for THAT shelf (e.g. snacks "best is B, no A"; bread "fermentation read from ingredients not branding"; maadanim "'דיאט' can mean sweeteners + stabilizers"). It is the transparency doctrine made consumer-facing.

**How to apply:**
- Render through the shared `categoryNote` slot in `comparison-page.tsx` — do NOT fork per-page markup. Feed it from each category's `src/lib/comparisons/<cat>-page-data.ts` constant; cheese feeds from `cheese_frontend_v1.json` `_meta.disclosures`.
- Format = cheese gold standard: bold header line `הערת קטגוריה — <subject>` + 1–2 short paragraphs, blocks joined by `\n\n`.
- Each caveat MUST be grounded in that category's actual engine behavior — verify with Nutrition, don't copy another category's disclosure blindly. (Maadanim originally inherited cheese's "sodium/sat-fat NOT scored" line, which was FALSE — the maadanim engine penalizes both; Nutrition corrected it.)
- **Cross-page divergence is allowed when each statement is truthful for its own data** (cheese "not scored" because its run lacks the data; maadanim "penalized" because it has it). Anchor the divergence with a shared lead clause so it reads as intentional, not an error: `"הציון מודד את מה שהתווית והנתונים מאפשרים בכל קטגוריה בנפרד; ..."` (Product positioning ruling, TASK-157).
- Editorial voice: insight-first, framework-invisible, no apology, no prohibited tokens (נקי/בריא except in negation). See [[bari_insight_line_spec_v1]], [[bari_assertive_writing_v1]], [[bari_editorial_intelligence_v1]].
