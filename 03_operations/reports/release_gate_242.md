# Release Gate — TASK-242 Emergency Production Integrity Release

- **Branch:** `release/prod-integrity-242` (cut from production `master` @ `8eacb083`)
- **Built in:** isolated git worktree `C:\Bari-rel-242` (active working tree untouched)
- **Date:** 2026-06-11
- **Agent:** orchestrator + qa-agent · **Reviewers (sign-off pending):** data-agent, frontend-agent
- **Verdict:** **PASS WITH FIXES**

---

## 1. Scope — exact file list (34 files, all release-scope)

### Salty-snacks v4 (item 1) + sodium-metric dependency chain
- `M bari-web/src/lib/comparisons/salty-snacks-page-data.ts` — import v3 → **v4**, map `sodium_mg`, hero/methodology 54 → 29
- `A bari-web/src/data/comparisons/salty_snacks_frontend_v4.json` — 29 real products
- `M bari-web/src/components/comparisons/salty-snacks-comparison-page.tsx` — sodium bar
- `M bari-web/src/app/hashvaot/salty-snacks/page.tsx` — meta count 54 → 29
- `M bari-web/src/components/shared/comparison-metric-column.tsx` — `SODIUM_METRIC` + `formatMetricValue` (dep of v4)
- `M bari-web/src/lib/view-models/index.ts` — `+ sodium_mg?` on `BariProductMetricsVM` (dep of v4)

### OFF ban enforcement (item 2)
- `M CLAUDE.md` — project-wide OFF hard rule
- `M integrations/clients/open_food_facts.py` — **hard-disabled**: `OFF_DISABLED=True`, every entry point raises `OffDisabledError`

### Registry reconciliation (item 3)
- `A tasks/TASK-242.md` (this release) · `A tasks/TASK-237.md` · `A tasks/TASK-238.md`
- `A tasks/TASK-241.md` — **reconciled**: stale "OFF stays LOCAL / TASK-238 retracted" framing marked SUPERSEDED (project-wide ban wins; salty complies)

### De-OFF contaminated live JSONs (item 4) — 39 OFF image URLs → `null`
- `M bari-web/src/data/comparisons/hard_cheeses_frontend_v2.json` (15)
- `M bari-web/src/data/comparisons/granola_frontend_v1.json` (9)
- `M bari-web/src/data/comparisons/cereals_frontend_v2.json` (8)
- `M bari-web/src/data/comparisons/yogurts_frontend_v3.json` (7)

### Remove frozen-vegetables route (item 5) — 7 files + 2 shared de-wirings
- `D` route page, comparison-page, intelligence-card, page-data, shelf-filters, registry category, frontend JSON
- `M bari-web/src/lib/comparisons/registry/index.ts` + `registry/types.ts` — id + import removed
- `M bari-web/src/app/hashvaot/page.tsx` — featured card + href + description removed

### Remove dead/leaky JSONs (item 7)
- `D crackers_staged_v1.json`, `olive_oil_frontend_v1.json`, `archive/cereals_frontend_v1.json`, `archive/juices_frontend_v1.json`, `archive/salty_snacks_frontend_v1.json`, `salty_snacks_frontend_v2.json`, `salty_snacks_frontend_v3.json`

### Image first-paint (item 8 — clean + isolated only)
- `M bari-web/src/components/comparisons/bari-product-thumbnail.tsx` — additive `eager` prop, defaults `false`, backward-compatible

**Excluded (architecture backlog, stays on branches):** category copy-polish (bread/butter JSONs), shared-component refactors (`comparison-row`, `comparison-table`, `corpus.ts`), evals / project-comp / governance backlog.

---

## 2. Validation report

| Gate | Result | Evidence |
|---|---|---|
| git diff = only release-scope files | **PASS** | 34 files, enumerated above |
| `tsc --noEmit` | **PASS** | exit 0 (after closing sodium-metric dep chain) |
| `next build` | **PASS** | 2026-06-11 orchestrator re-run in the worktree with a REAL `npm install` (972 pkgs, no junction): `tsc --noEmit` exit 0, `next build` exit 0, all routes prerendered — `/hashvaot/salty-snacks` present, `/hashvaot/frozen-vegetables` ABSENT from the route manifest. |
| frontend JSON validator | **PASS** | every `comparisons/*.json` parses |
| OFF grep across production data (`bari-web/src/data`) | **PASS** | **0** hits (was **39**) |
| frozen-vegetables route removed | **PASS** | 0 files on disk, route dir GONE, 0 code refs, registry id removed, tsc clean |
| salty page imports v4 not v3 | **PASS** | `import ... salty_snacks_frontend_v4.json` |
| no fake barcodes / dead image hosts in salty | **PASS** | 29 real EANs, single real host `api.yochananof.co.il`; the lone Calbee `8851016002685` is prose-only (0 live products) |
| no full-data confidence where panel missing (salty) | **PASS** | 0 inflated; confidence ∈ {partial, verified}, all verified rows have panels |
| no full-data confidence where panel missing (snacks — item 6, staged 2026-06-11) | **PASS** | data-agent reviewer confirmed the inflation set = exactly snk-003/007/009/020 (all-null panels + full-gap unknowns, shipped `verified`) and ruled a copy-free extraction ISOLATABLE. 4-row × 4-field hotfix applied on master's bytes (verified→partial, canonical `missing_nutrition` label/tooltip/sub_reason from `confidence_annotation.py:43-44`; `expansion.confidenceLabel` deliberately untouched = not a copy edit). Post-patch: 0 verified rows corpus-wide; 18 products intact; JSON parses. Structural fix (DA-013 `annotate_fallback` re-derive + LIVE_FILES staleness) remains **TASK-244**. |
| OFF grep pattern definition (reviewer finding A) | **NOTE** | The OFF gate pattern is pinned to `openfoodfacts` host/URL strings — under it, prod data = 0 hits. Salty v4 `_meta.dropped_products[].reason` contains 9 literal "OFF" tokens that are all NEGATIONS ("NOT backfilled from OFF") — anti-provenance metadata, not contamination. Optional fast-follow: reword to "any external aggregator". |
| post-merge production URL verification | **PENDING** | forward step — see §4 |

---

## 3. Fixes required before / right after merge (why PASS WITH FIXES)

1. ~~**`next build` green in a real checkout**~~ — **RESOLVED 2026-06-11**: real `npm install` + build in the worktree, exit 0 (see §2). Former merge blocker cleared.
1b. **Orchestrator verification fixups landed as `243b9f8b`** (post-initial-report): (a) the branch had staged the STALE RETRACTED/CLOSED revision of `tasks/TASK-238.md`, contradicting §3.4 and scope item 3 — replaced with the reinstated project-wide-ban record (IN_PROGRESS) + a TASK-242 remediation-status block; (b) the CLAUDE.md OFF-ban Hard rule was MISSING from the branch (scope item 2 was only half-shipped: client stub yes, constitutional rule no) — added; (c) gate #8 re-worded to its honest salty-only scope. TASK-243 (image backfill) + TASK-244 (snacks confidence structural fix) are now REGISTERED in the live registry, not prose proposals.
2. **Real-image backfill for the 39 nulled images** — de-OFF was done honestly by NULLing OFF images on hard_cheeses/granola/cereals/yogurts; those products now render the Bari placeholder card ("unknown is acceptable; OFF is not"). This is a **visual regression** to be closed by sourcing real retailer images. *data-agent — proposed follow-up TASK-243.* Not a merge blocker (placeholder is rule-compliant); ship-and-backfill.
3. ~~**Snacks confidence (item 6) — reviewer-gated.**~~ — **RESOLVED 2026-06-11**: data-agent confirmed the exact inflation set (4 rows) and the copy-free extraction; the 4-field hotfix is STAGED in this release (see §2). The data-agent explicitly warned against cherry-picking the `salty-snacks-v4` branch copy of `snacks_frontend_v2.json` (it rewrites bottomLine/comparisonContext on all 18 products and does NOT fix the confidence fields) — the staged patch is fresh, applied to master's bytes. Structural DA-013 fix + the pre-existing bottomLine score-drift on these rows (53/28/47/33 vs 55/27/48/32, on master today) = **TASK-244**.
4. **TASK-238** stays `IN_PROGRESS`; orchestrator closes it after post-merge prod verification confirms 0 OFF live.

---

## 4. Preview URL & production verification

- **Preview URL:** generated on deploy of `release/prod-integrity-242` (Vercel preview) — confirm `next build` (§3.1) first.
- **Post-merge production verification checklist (run against the LIVE site, not local):**
  - [ ] `/hashvaot/salty-snacks` shows 29 products, sodium bar renders, hero = "…רק חטיף אורז מלא בלי מלח מגיע ל-A"
  - [ ] `/hashvaot/frozen-vegetables` returns **404** (route gone); `/hashvaot` index has no frozen-veg card
  - [ ] View-source / network on hard_cheeses, granola, breakfast-cereals, yogurts → **no `images.openfoodfacts.org`** requests; nulled products show Bari placeholder
  - [ ] No salty image 404s; all thumbnails resolve to `api.yochananof.co.il`
  - [ ] No console/render errors on the four de-OFF'd pages or salty
  - [ ] Confirm removed JSONs (v2/v3 salty, olive_oil, crackers_staged) are not fetched

---

## 5. Authority note
The **merge to production master + deploy** is irreversible and consumer-facing (decision tripwire #2). Orchestrator stages + gates (this report); **owner authorizes the merge/deploy.** Do not self-close TASK-242 — orchestrator records CLOSED only after the §4 production checklist passes.
