---
id: TASK-588
title: Catalog-registry alignment: register all live categories + CI parity gate
owner: frontend-agent
status: RETURNED
priority: HIGH
created_at: 2026-07-10
depends_on: []
blocks: []
category_id: null
summary: >
  Owner-approved 2026-07-10. Catalog registry covers only 7 of ~20 live categories; everything since (yogurt, juices, chocolates, cookies, protein bars, cheese trio, milk) is invisible in /catalog. Register every live category whose data matches the registry contract (Hebrew names REUSED from existing signed-off page data, zero new consumer strings), add a CI parity check (registry ids vs served comparison JSONs), Stage 13 checkbox. BUILD-HEAVY: Codex gpt-5.6-sol in worktree.
---

# TASK-588 — Catalog-registry alignment: register all live categories + CI parity gate

## Verification record (orchestrator, 2026-07-10)

- Lane: BUILD-HEAVY Codex gpt-5.6-sol, worktree C:/bari_wt_587, branch `task588-catalog-registry`.
  Lane history: attempt 1 failed (driver kwarg `cwd`→`worktree`), attempt 2 failed (multi-line prompt
  truncated by .cmd shim — Codex correctly refused; fixed via stdin, merged to master b5524728),
  attempt 3 SUCCEEDED. Codex committed into a fallback git-dir (sandbox blocked the worktree's
  external .git pointer); orchestrator delivered the identical tree as e1b25d19 on the real branch.
- C0 `validate_return.py`: PASS (17/17 sha256, C7 clean, counts with denominators, distribution marker).
- Independent re-runs by orchestrator in the worktree: `validate-catalog-parity` 18/18 green;
  `tsc --noEmit` exit 0.
- Copy law check: 11 new registry files contain ZERO Hebrew literals — every `nameHe` references an
  existing exported hero eyebrow (values read from served JSONs: יוגורט מוצק, משקאות יוגורט,
  חלב ותחליפים, עוגות, מיצים ומשקאות פירות, גבינות מלוחות, גבינות קשות וצהובות, חטיפי שוקולד,
  טבלאות שוקולד, עוגיות לקפה, חטיפי חלבון ועוגיות חלבון). Cakes metadata strings verified
  byte-identical to `src/app/hashvaot/cakes/page.tsx` metadata.
- CI gate wired: `validate-catalog-parity` npm script + barint_ci.yml step (matches card-stats style).
- Registered 11/11 candidates, skipped 0. Registry now 18/18 live product-comparison routes.

**Awaiting: owner Speed-2 merge (consumer-visible — /catalog gains 11 categories).**
PR: https://github.com/Argento17/Barint/pull/new/task588-catalog-registry
Close after the owner merges.
