# TASK-568 Return — Derived views: featured-card stats generated from comparison JSON at build time

## Summary

**Phase 1 (scoping, delivered first):** audited 6 `/hashvaot` featured cards (cheese,
protein-bars, juices, breakfast-cereals, granola, magnesium — chosen for spread). Wrote
`01_framework/frontend/derived_views_scoping_v1.md` classifying every field as data / copy /
design, designing the shared derived-stats shape, and designing the parity-check fixture.
Key discovery: `ComparisonIntelligenceHero`'s `insightLines`/`showInsights` props have been
**dead code since 2026-07-01** (owner review #6 removed the "תובנות מרכזיות" callout; the prop
is still accepted but never rendered) — cutting real scope, since per-product insight-line
derivation is not needed for the visible surface. The only fields that actually reach the DOM
are `badge`, `categoryTags`, `title`, `description`, `stats[]`, `updatedLabel`.

**Phase 2 (pilot, in worktree `C:/bari_wt_568`, branch `task568-derived-cards`, based on
`origin/master` per the delegation spec):** built `src/lib/derived/comparison-card-stats.ts` —
one pure function (`deriveComparisonCardStats`) that computes `productCount`, `scoredCount`,
per-grade counts, `ceilingGrade` (best grade actually present), `scoreLow/High/Spread`, and
`updatedLabel` from a product array + a `generated` date, plus a generic `deriveMetricRange`
helper. Converted 3 pilot cards (cheese, protein-bars, granola) to call it instead of hand-typed
literals / duplicated inline `.filter()`/`Math.round(Math.max...)` logic. Added
`scripts/validate-card-stats.mjs` (`npm run validate-card-stats`) — a parity fixture that
re-derives stats straight from the raw comparison JSON via the real shared module (not a
reimplementation), matching this repo's existing `validate-corpus.mjs` convention (plain Node,
exit-coded, zero new dependency).

## IMPORTANT — no drift discrepancy ships in this PR (read before treating this as a bug fix)

Phase 1's audit was read against the local `task506` branch and found two real hardcoded-vs-JSON
mismatches: protein-bars showed `"25–34"` g protein/100g when the JSON's actual range is
`25–36`, and granola showed `47` "נקודות פער" when the JSON's actual score spread was `~38`.
**By the time the worktree was created off `origin/master` (as the delegation spec requires),
both had already been independently hand-fixed upstream** — protein-bars now reads `"25–36"`
and granola now *computes* its spread inline (`Math.round(Math.max(...) - Math.min(...))`)
instead of hardcoding it. This is disclosed prominently per the task's own instruction ("flag it
prominently... each one is exactly the drift this task exists to catch") — it confirms the
failure class TASK-568 targets is real (two numbers went stale in production and needed manual
catches, with no gate to prevent a third), but it means **this PR's converted cards are
byte-identical in every displayed stat, before and after** (verified by construction: the
pre-existing inline computations and the new shared-module computation run the identical
arithmetic over the identical arrays). See `derived_views_scoping_v1.md` §7 for the full
before/after. The deliverable here is architectural (one shared source of truth, duplication
removed) — not a live-bug fix.

One item from the original scoping audit remains genuinely unfixed and out of this pilot's
scope: magnesium's `updatedLabel="עודכן יוני 2026"` is still a hardcoded literal with **no
underlying JSON `generated` field to derive it from** — `magnesium-page-data.ts` is a fully
hand-authored TS array that bypasses `loadComparisonCorpus` entirely (a structural gap, not a
card bug; flagged as a Data Agent follow-up in the scoping doc §1/§6).

## Files changed (worktree `C:/bari_wt_568`, branch `task568-derived-cards`)

- `bari-web/src/lib/derived/comparison-card-stats.ts` (new) — the shared derivation module.
- `bari-web/scripts/validate-card-stats.mjs` (new) — the parity fixture.
- `bari-web/package.json` — added `"validate-card-stats": "node scripts/validate-card-stats.mjs"`.
- `bari-web/src/components/hashvaot/featured-cheese-intelligence-card.tsx` — converted to
  `deriveComparisonCardStats`.
- `bari-web/src/components/hashvaot/featured-protein-bars-intelligence-card.tsx` — converted;
  also replaced the hardcoded `"25–36"` and `"B"` literals with `deriveMetricRange` /
  `stats.ceilingGrade` (values unchanged, now future-proof against re-score).
- `bari-web/src/components/hashvaot/featured-granola-intelligence-card.tsx` — converted; removed
  the duplicated inline `Math.round(Math.max(...) - Math.min(...))` and `.filter()` logic.

No copy strings, images, or design tokens were touched. `insightLines` arrays in all three cards
are untouched (dead code — see above). 13 of the ~18 hashvaot featured cards remain unconverted
(explicitly out of this pilot's 2-3 card scope).

## Verification

- `npm ci` — clean install in the worktree (973 packages).
- `npx tsc --noEmit` — 0 errors.
- `npm run lint` — 0 errors, 19 pre-existing warnings (none in touched files; confirmed via
  `git diff` — no touched file appears in the warning list).
- `npm run build` — succeeded, all 305 static pages + all `/hashvaot/*` dynamic routes compiled,
  including the 3 converted cards' import graph.
- `npm run validate-card-stats` — exit 0, prints derived stats for all 3 pilot categories
  straight from the raw JSON (cheese: 47 products/47 scored/2×A; protein-bars: 32
  products/ceilingGrade B/scoreSpread 26; granola: 22 products/scoreSpread 37) — matches what
  each converted card now renders, by construction (same function, same input array).
- Live-render curl/browser check was not performed (background dev-server launch was denied by
  the sandbox in this session) — `next build`'s successful compilation of every `/hashvaot/*`
  route plus the parity script's independent numeric confirmation is the verification actually
  performed; flagging this gap rather than claiming a browser-verified render.

## Not done (explicitly out of Phase 2's 2-3 card pilot scope)

- The other ~13 hashvaot featured cards (juices, breakfast-cereals, magnesium, brined-cheeses,
  hard-cheeses, hummus, milk, snacks, chocolate-bars/tablets, cakes, cookies-coffee, crackers,
  yogurt, yogurt-drinks, bread-lite) are not converted.
- `magnesium-page-data.ts`'s structural gap (no `loadComparisonCorpus`, no JSON `generated`
  field) is not fixed — flagged as a Data Agent follow-up.
- The sibling drift risk in `src/lib/home/homepage-carousel-data.ts` (`HOMEPAGE_CAROUSEL_CARDS`
  — fully hand-typed leader-product scores/names for the actual homepage carousel + duel, e.g.
  bread `89 מול 60`) is documented (scoping doc §3) but not touched — the delegation spec scoped
  Phase 2 explicitly to the `hashvaot/featured-*-intelligence-card.tsx` files.
- The parity script's "grep the card source for a disagreeing literal" hardening (so an
  un-converted card fails the gate) is designed but not built — noted as a TODO in the script.
- Workflow files (`barint_ci` / GitHub Actions) are not touched, per the hard constraint —
  `npm run validate-card-stats` is invocable but not wired into CI.
- `supermarket/page.tsx`'s `granolaDescription`/`cerealsDescription` prose (two-gate content)
  still embeds numbers that may disagree with current JSON (e.g. `"פער של 47 נקודות"`) — flagged
  for Content Agent, not touched (copy carve-out).

## PR

Pushed `task568-derived-cards` to `origin`. Create PR at:
https://github.com/Argento17/Barint/pull/new/task568-derived-cards

```json
{
  "task": "TASK-568",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": "C:/Bari/01_framework/frontend/derived_views_scoping_v1.md", "action": "created", "sha256": "99a20bd1ef3606f5263c03ad12cc2330743d5afa5307f3dceb50d8c595cdcf02"},
    {"path": "bari-web/src/lib/derived/comparison-card-stats.ts", "action": "created", "sha256": "ce8f8b68dbf00567ad8398d322aa1d6e459432e49cd37b1d8f4b72d6f81bbdf4"},
    {"path": "bari-web/scripts/validate-card-stats.mjs", "action": "created", "sha256": "4ee491e26ca81463528df1a530c36320a2ace92db381b184f34958f69ec82385"},
    {"path": "bari-web/package.json", "action": "modified", "sha256": "8f81b660a92cca5882ba1fc259ce3acafec848e73ee9e586d185aca3088bd356"},
    {"path": "bari-web/src/components/hashvaot/featured-cheese-intelligence-card.tsx", "action": "modified", "sha256": "71d1557a73ab82d53554b86d256b6f608e084cf3634b00985e232bde6255f749"},
    {"path": "bari-web/src/components/hashvaot/featured-protein-bars-intelligence-card.tsx", "action": "modified", "sha256": "3f1199a337c0b03a08f5805ba784408570827cae9928b6dcc3696604a37ccd7d"},
    {"path": "bari-web/src/components/hashvaot/featured-granola-intelligence-card.tsx", "action": "modified", "sha256": "fbb30871447751c9c5c0aa0b57064850c2184f8ffc67193acf41adcdd8bb168e"}
  ],
  "counts": {
    "pilot_cards_converted": "3/3 (scope: cheese, protein-bars, granola per delegation spec 2-3 cards)",
    "featured_cards_total_unconverted": "13/16 remaining (bari-web/src/components/hashvaot/featured-*-intelligence-card.tsx, ls count)",
    "cards_audited_in_scoping": "6/6 (cheese, protein-bars, juices, breakfast-cereals, granola, magnesium — derived_views_scoping_v1.md §1)",
    "drift_discrepancies_found_at_scoping_time": "2/2 (protein-bars protein-range 25-34-vs-25-36, granola score-spread 47-vs-38; both independently pre-fixed on origin/master before implementation, see return body IMPORTANT section)",
    "lint_errors": "0/0 (npm run lint, touched files)",
    "tsc_errors": "0/0 (npx tsc --noEmit)",
    "build_routes_compiled": "305 static + all /hashvaot/* dynamic routes (npm run build, exit 0)",
    "parity_script_categories_passing": "3/3 (npm run validate-card-stats, exit 0)"
  },
  "commands_run": [
    {"cmd": "npm ci", "exit_code": 0},
    {"cmd": "npx tsc --noEmit", "exit_code": 0},
    {"cmd": "npm run lint", "exit_code": 0},
    {"cmd": "npm run build", "exit_code": 0},
    {"cmd": "npm run validate-card-stats", "exit_code": 0},
    {"cmd": "git push -u origin task568-derived-cards", "exit_code": 0}
  ],
  "not_done": [
    "13 of ~16-18 hashvaot featured cards not converted (out of 2-3 card pilot scope)",
    "magnesium updatedLabel drift not fixed (no JSON generated field to derive from — Data Agent follow-up)",
    "homepage-carousel-data.ts (HOMEPAGE_CAROUSEL_CARDS, the actual 'homepage carousel + featured duel' the task title names) not converted — Phase 2 delegation text scoped to hashvaot cards only; flagged as follow-up",
    "parity script's static-source-literal-grep hardening not built (TODO comment left in script)",
    "barint_ci workflow not wired to run validate-card-stats (workflow files intentionally not touched)",
    "supermarket/page.tsx prose numbers (e.g. granola '47 points' in the description paragraph) not corrected — copy carve-out, flagged for Content Agent",
    "live browser/curl render verification not performed (background server denied by sandbox); relied on next build compile success + parity script instead"
  ],
  "self_check": "Acceptance test: 'npm run build && npm run lint && npm run validate-card-stats all exit 0, and every pilot card's stats prop reads from deriveComparisonCardStats/deriveMetricRange with no hand-typed literal remaining for productCount/scoredCount/gradeCounts/ceilingGrade/scoreSpread/updatedLabel.' Observed: all three commands exited 0 (see commands_run); read back all 3 converted card files after editing and confirmed no residual hardcoded stat literals for those fields (categoryTags/badge/title copy literals intentionally untouched per the copy carve-out)."
}
```
