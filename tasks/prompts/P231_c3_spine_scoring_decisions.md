(route: C3)

# P231 — C3 consult: 4 spine scoring-architecture decisions a red-team surfaced

Independent reviewer, no repo write access — facts below are verified against code this session.
These are JUDGMENT calls I deliberately will NOT autopilot (they change how scoring detects movement
or how scores are calibrated). For each: recommend the single best option + the strongest reason +
the main risk. Reasoning only; you don't implement or close.

Context: Bari food-scoring spine. A `spine_flip --set FLAG=on` runs `affected_set` (a shadow what-if
diff) to decide which shelves to rescore, then `rescore_all --shelf` does the real rescore. Some
categories are "shelf-relative": a product is scored vs the shelf's median/scale for a nutrient
(cakes=sugars_g, brined=sodium_mg, cheese=fat_saturated_g, hummus). Those median/scale values are
PINNED in each config and were computed over a curated enrollment subset (verified: recomputing
cheese's median from the raw corpus gives 5.4 vs the pinned 16.05 — a 3× shift that would corrupt
the shelf). `rescore_all.setup_shelf_stats()` injects the pinned stats; `shadow_backtest.score_corpus()`
does NOT (it only sets flags).

## DECISION 1 (RT-5) — shadow diff is blind to shelf-relative scoring
PROVEN this session: a real flip (`BARI_PALM_HYDRO_V1=on`) made `affected_set` report "cereals + hummus"
and OMIT cakes — even though cakes was the actual target — because the shadow diff scored cakes in
absolute mode (no shelf stats) and saw no movement. The flip would have SKIPPED cakes. (It happened to
be a no-op, but the omission was unreliable.) Options:
  (a) Inject the pinned shelf stats into `shadow_backtest.score_corpus` so the shadow path matches the
      real `rescore_all` path for shelf-relative shelves.
  (b) Force-include ALL shelf-relative shelves in `affected_set.affected_shelves` regardless of what the
      shadow diff reports (always rescore them on any flip).
  (c) Other.
Which is correct, and what breaks under each? (Note (a) makes shadow heavier but accurate; (b) is simple
but rescores shelf-relative shelves even for flags that can't touch them.)

## DECISION 2 (RT-7) — product expansion vs pinned shelf stats
When an existing live category gets MORE products scraped in, the pinned median/scale do NOT recompute,
so new products are scored against a stale shelf baseline. Options: keep pinned (deterministic but stale);
recalibrate on every expansion (recompute median/scale, accept score movement on existing products);
hybrid (recalibrate THEN surface the resulting movement for explicit review before publish). Also: should
there be a guardrail that warns when the corpus size has drifted >N% from the calibration date stored in
the config? What is the right policy, and what N?

## DECISION 3 (RT-3) — should the onboard gate verify scores reproduce?
`onboard_category.py` checks config/mapping/baseline/OFF but never verifies that the flags registered in
`shadow_registry_v1.json` actually REPRODUCE the live page's scores. A wrong registered flag passes the
gate, then a future flip rescores under the wrong flags. Should onboard run a `shadow_backtest`
reproduce-check (baseline diff == 0 moves) before declaring a category live-ready? Cost/benefit?

## DECISION 4 (RT-6) — shadow-registry single-source limitation
`cookies_coffee` is registered with 1 of its 2 config corpus dirs (shadow sees 61 of ~225 products);
`granola`'s registry source (`run_cereals_005`, 66) differs from its live traces (`run_cereals_008`).
So the shadow diff validates a partial/different corpus than what's live → can miss movement. Options:
extend the registry/shadow loader to accept multiple sources; merge into one BSIP1 dir per category;
or document + force-include these two. Best path given we want this right once?

For each decision: one clear recommendation, the single strongest reason, the main risk if wrong.
