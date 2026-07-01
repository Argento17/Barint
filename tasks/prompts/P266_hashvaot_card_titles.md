# P266 / /hashvaot index card titles — remove numbers, apply approved key-insight titles (route: C1-CURSOR)

Repo C:\Bari, site under bari-web (local == origin/master). TASK-426. STAGING ONLY — no commit/push/deploy. Touch ONLY the `bari-web/src/components/hashvaot/featured-*-intelligence-card*.tsx` components. NO scores/data/JSON changes.

## Problem
The /hashvaot INDEX page cards render titles HARDCODED in `featured-<category>-intelligence-card.tsx` (and one `-lite` variant for bread), e.g. `featured-granola-intelligence-card.tsx:39` → `title="גרנולה ומוזלי: 53 מוצרים, פער של 47 נקודות"`. These were NOT updated when the comparison-page hero titles were rewritten, so the live index still shows OLD titles WITH NUMBERS (owner: "let's not mention numbers" + some counts are stale/wrong, e.g. granola "53" but the category has 22, cereals "37" but 20).

## Do — for EVERY featured card component (find them all: `ls bari-web/src/components/hashvaot/featured-*-intelligence-card*.tsx`)
1. Read the APPROVED new hero title for that card's category from `bari-web/src/data/site-content/comparison-pages.json` (the `hero.title` field per category — these passed the QA gate). Set the card's hardcoded `title=` to that approved title (or a faithful card-length version that preserves its key insight and voice — but NEVER re-introduce numbers).
2. Remove ALL Arabic numerals (0-9) from the card `title` AND from any `subtitle`/`description`/`insight` prose in that component (e.g. "פער של 47 נקודות", "53 מוצרים"). Keep the sentence natural after removal.
3. Map by category slug: granola, breakfast-cereals(דגני בוקר), cheese(גבינה לבנה), chocolate-bars, chocolate-tablets, hard-cheeses(גבינה צהובה), hummus, juices, milk, protein-bars, snacks, bread(-lite), brined-cheeses, cakes-hard-cookies, cookies-coffee. magnesium is a supplement — leave its title as-is unless it contains a bare product-count number.
4. Do NOT touch the structured STAT ROW numbers if they are a separate metadata component (e.g. "38 פרמטרים בהשוואה") — but REPORT every place a number still appears (title/subtitle/stat) so the orchestrator can decide. Titles and prose sentences must be number-free.

## Voice guards (content_voice/tom_bari_voice/ files 2/5/7)
No E-codes/code-tokens, no numbers in titles/prose, no info-dumping, on Tom-Bari voice. Titles must match the approved comparison-pages.json versions in spirit.

## Verify + report
- For each card component: old title → new title, and confirm 0 digits remain in title + subtitle prose.
- List every featured card file changed. Run `npm run build` (bari-web) and report exit code + that /hashvaot compiles.
- Report any remaining numeric content in stat-row metadata (not changed) for owner review.

End with the return contract (01_framework/operations/return_contract_v1.md); status RETURNED, not CLOSED.
