(route: C3)

# P215 — C3 independent review: spine-conformance contract (is the gate checking the RIGHT things?)

Independent reviewer, NO repo access — facts below. We are building a gate that answers one
question: "Will this live food-comparison category actually re-flow when we flip a scoring
switch, or will it silently keep old scores while the rest of the shelf moves?" The owner's
real fear: ship a new category, be happy, then discover days later it doesn't conform to the
scoring spine. Judge whether the contract below is correct, complete, or missing a failure mode.

## How a score-flip actually works (verified from source)
- `spine_flip.py --set BARI_X=on` is the entry point. It calls `affected_set.py` (a shadow
  what-if diff), gets back `affected_shelves`, then loops **ONLY those shelves**
  (`spine_flip.py:391  for shelf in affected_shelves:`) and re-scores each via
  `rescore_all.py --shelf <stem>`.
- `affected_set.build_corpus_to_shelves_map()` decides `affected_shelves`. It maps a corpus to a
  shelf-config stem ONLY if the corpus is BOTH (a) registered in `shadow_registry_v1.json`
  (its `corpora[]` list, each with a `source` path) AND (b) resolvable to a config in
  `page_generator/configs/<stem>.json` by category-name match OR shared source-path OR a known alias.
- A config alone is NOT sufficient: `rescore_all.py` with no `--shelf` loops every config, but the
  flip path NEVER calls that — it always passes the specific affected shelves. So a category with a
  config but absent from `shadow_registry_v1.json` is INVISIBLE to the flip and keeps old scores.

## The contract our gate enforces, per category
HARD checks (fail = the category is silently stale on a real flip — block):
  1. `configs/<stem>.json` exists AND its corpus_dirs / run_products_dir resolve to existing dirs.
  2. The category's corpus resolves through the REAL function `affected_set.build_corpus_to_shelves_map()`
     to this config stem (we import and call the actual function the flip uses — not a re-implementation).
     This single check subsumes "registered in shadow_registry" + "mapping resolves".
TRACKED checks (fail = live/deploy hygiene problem, not a scoring-staleness problem — warn/soft):
  3. Frontend JSON exists and is the standard `{_meta, products}` shape (juices uses a bespoke FLAT
     schema → flagged, needs a manual loader override).
  4. Frontend wiring complete: route folder, registry entry, `ComparisonCategoryId` TS union member, sitemap path.
  5. Listed in `live_manifest.json` (the spine's machine-readable "what is live").
INTEGRITY:
  6. OFF (Open Food Facts) string count == 0 in the frontend JSON + corpus (hard project ban).

## Already-found reality (the gate's first --all run will report)
`cakes`, `cookies_coffee`, `brined_cheeses` are LIVE (have configs + frontend JSON + routes) but have
NO corpus entry in `shadow_registry_v1.json` → today a `spine_flip --set X=on` would re-flow every
other shelf and leave those three frozen at old scores, undetected.

## Questions
1. Is check #2 (resolve through the real `build_corpus_to_shelves_map`) truly the load-bearing
   re-flow guarantee, or is there ANOTHER way a flip silently skips / mis-scores a category that this
   contract misses? (e.g. frozen-invariant corpora, shared-source coupling where two shelves share one
   corpus dir, alias mismatches, a config that exists but points at a stale/empty corpus.)
2. Is anything OVER-checked — i.e. a check that will produce false "non-conforming" alarms on a category
   that is actually fine? Specifically: a category whose corpus is only reached via shared-source coupling
   (granola rides the cereals corpus) — will check #2 correctly pass it, or wrongly fail it?
3. Should "config exists but corpus is in shadow_registry as a DIFFERENT class (frozen/candidate/published)"
   be its own check? Does class matter for whether a flip re-flows it?
4. Biggest risk this gate introduces: false confidence (passes but still drifts) vs. false alarms (fails
   conforming categories and trains the owner to ignore it). Which is the bigger danger here and why?

For each: a clear recommendation + the single strongest reason. Flag anything mis-framed.
Evidence/reasoning only — you do not execute, write files, or close.
