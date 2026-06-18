# P83 — Cookies render trio + index card (route: C1-GEMINI)

**Task:** TASK-275. **Lane:** C1-GEMINI (C1-CURSOR + C1-Sonnet capped). Spec-complete: clone the brined
golden render trio for cookies, swapping only the data source + names + scoped styles. **You must WRITE
files** — if your file-write tool is blocked, say so explicitly in the return (do not fabricate success).

## Goal: a building, viewable local page at `/hashvaot/cookies-coffee`
Mirror the brined golden FILE-FOR-FILE (copy structure, swap brined→cookies):

| Clone FROM (brined golden) | TO (cookies) |
|---|---|
| `bari-web/src/lib/comparisons/brined-cheeses-page-data.ts` | `bari-web/src/lib/comparisons/cookies-coffee-page-data.ts` |
| `bari-web/src/components/comparisons/brined-cheeses-comparison-page.tsx` | `bari-web/src/components/comparisons/cookies-coffee-comparison-page.tsx` |
| `bari-web/src/app/hashvaot/brined-cheeses/page.tsx` | `bari-web/src/app/hashvaot/cookies-coffee/page.tsx` |
| `bari-web/src/components/hashvaot/featured-brined-cheeses-intelligence-card.tsx` | `bari-web/src/components/hashvaot/featured-cookies-coffee-intelligence-card.tsx` |

Data source: `bari-web/src/data/comparisons/cookies_coffee_frontend_v1.json` (already exists, 61 products,
scored+copy). Wire it exactly as the brined page wires `brined_cheeses_frontend_v2.json`.
Also add the cookies index card to `bari-web/src/app/hashvaot/page.tsx` (mirror the brined entry) so the
page is discoverable.

## Rules (do NOT improvise — clone the golden)
- Swap ONLY: import paths, the JSON data file, the route slug (`cookies-coffee`), Hebrew titles/labels, and
  scope any page-local CSS to a `.cc-page` block (do NOT edit shared components — they must not regress for
  other categories).
- Do NOT invent UI. Do NOT add charts in this task (charts are a separate step). Do NOT touch scores/copy in
  the JSON. No new dependencies.
- imageUrl must render (mirror brined's image wiring). Additives dropdown populated from `d4_additives`.
  Category-caveat box present (text already in the JSON page-shell).

## Build gate (capture the REAL exit code — do NOT pipe to tail)
`cd bari-web && npm run build > build_cookies.log 2>&1; echo "EXIT:$?"` — must be EXIT:0 and the
`/hashvaot/cookies-coffee` route must appear in the build output. Paste the real exit code + the route line.

## Return
Return contract: task=P83, proposed_status=RETURNED, artifacts (the 4 new files + the modified hashvaot
page.tsx, each +sha256), counts (files created, build exit code, route present yes/no, shared-components
untouched yes/no), commands_run (the build with its real EXIT code), not_done, self_check. If file-write was
blocked, report that honestly in not_done. Propose RETURNED — do NOT close. The orchestrator re-runs the
build AND screenshots the page (pixel review is not delegated).
