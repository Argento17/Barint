(route: C3)

# P211 — C3 independent review: new-category route scaffolder (don't-overdo-it check)

Independent reviewer, NO repo access — facts below. The owner's explicit constraint was
"don't overdo it." Judge whether this tool is correctly scoped, over-built, or under-built.

## Context
Bari = food-scoring monorepo + Next.js site. Onboarding a new /hashvaot comparison category
currently needs hand-wiring ~4 frontend files + 3 patch points (registry import+entry, a
TypeScript union, sitemap line). Scoring/page-generation already conform automatically via a
config + the shared pipeline; only the frontend route wiring is manual. A scaffolder was built:

`python 03_operations/page_generator/scaffold_category.py --category <slug> [--json <file>]`

It emits the STRUCTURAL skeleton for a new category that already has a spine config + a generated
frontend JSON:
- `<slug>-page-data.ts` (loads the frontend JSON; hero/prologue/methodology/categoryNote exported
  as TODO placeholder constants marked `// TODO(content): author Hebrew copy`)
- `<slug>-comparison-page.tsx` (thin wrapper delegating to the EXISTING shared `ComparisonPage`
  component; filters/metrics left as `// TODO(filters)` placeholder)
- `app/hashvaot/<slug>/page.tsx` route
- `registry/categories/<slug>.ts`
- applies the 3 patches (registry index, ComparisonCategoryId union, sitemap)

Deliberately does NOT: auto-write Hebrew copy (Content-Agent/Sonnet's job), invent per-category
filters, create new shared components, add gates, or touch scoring/engine/config code.
Verified: it scaffolds a throwaway test category and `npm run build` passes TypeScript; one file
added to the repo.

## Known residuals it does NOT solve (the builder flagged these)
1. Loader filename convention is split repo-wide (`-page-data.ts` ×9 vs `-comparison-page-data.ts`
   ×3); scaffolder standardizes on the dominant `-page-data.ts`, leaving 3 legacy files inconsistent.
2. Juices uses a bespoke flat JSON schema (no `_meta` wrapper) + inline normalization; a new
   category with that shape needs a manual override in its page-data file.
3. Metadata export pattern is inconsistent (some export a `*ComparisonMetadata` const, some inline
   the route metadata); scaffolder uses the exported-const pattern.

## Questions
1. Is this the right scope for "don't overdo it," or is it over/under-built? Specifically: is leaving
   copy + filters as TODO placeholders the correct boundary, or should it do more / less?
2. Of the 3 residuals, which (if any) is worth fixing now vs. leaving — given new categories are
   coming soon and the goal is lean, repeatable onboarding (not a perfect framework)?
3. Biggest risk this scaffolder introduces (e.g., silently drifting from the real pattern, masking
   the juices-style schema mismatch, encouraging copy-paste of stale placeholders)?

For each: a clear recommendation + the single strongest reason. Flag anything mis-framed.
Evidence/reasoning only — you do not execute or close.
