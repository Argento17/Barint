---
id: TASK-499
title: SEO crawl-hygiene: internal-linking pass for /hashvaot comparison pages + legal-page sitemap/comment fixes
owner: frontend-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-07-03
close_reason: "MERGED LIVE 2026-07-04 (PR #84 → origin/master f498ae28). Verified: origin/master sitemap-paths.ts contains /nagisut,/cookies,/disclaimer (4 legal paths total); 0 false 'stays noindexed' comments remain on the 5 legal pages. Part A (internal-linking) audited = all 17 /hashvaot pages already reachable via SSR anchors (no orphans, no change). Original -clean branch conflicted after master moved (PR #82/#83); orchestrator cherry-picked the verified commit onto current master (clean, byte-identical diff 6 files +13/-5) → seo/crawl-hygiene-task499-v2 → owner merged. Follow-up logged: several live blog routes still absent from sitemap (own micro-pass)."
depends_on: []
blocks: []
category_id: null
summary: >
  GSC discovered-not-indexed remediation (bari.digital). Primary: ensure all 17 hashvaot comparison pages are linked from the /hashvaot hub and homepage so Google prioritizes them. Secondary hygiene: add nagisut/cookies/disclaimer to the sitemap (live, indexable, real content, currently footer-only); correct the false 'stays noindexed' code comments on the 5 legal pages (they emit no robots override and are indexable). No content/copy or scoring changes. Ships as PR.
---

# TASK-499 — SEO crawl-hygiene: internal-linking pass for /hashvaot comparison pages + legal-page sitemap/comment fixes

<!-- opened with new_task.py; fill in context / scope / the deliverable -->

## Orchestrator verification (2026-07-04) — VERIFIED COMPLETE, awaiting owner PR/merge

Deliverable landed as ONE clean commit `aaa4b021` on top of current `origin/master`, pushed to
`origin/seo/crawl-hygiene-task499-clean`. (The local branch `seo/crawl-hygiene-task499` holds a
messier duplicate `1d4490e2` on a stale base — NOT the deliverable; ignore it.)

Verified against DoD:
- **Part A (primary, internal-linking):** commit documents an audit finding — all 17 /hashvaot
  comparison pages already reachable via real SSR anchors (home → /hashvaot →
  supermarket/supplements → page; 4 also linked from the homepage carousel). No orphans, no change
  needed. Honest "audited, nothing to fix" — correct outcome, not a skipped step.
- **Part B (secondary, hygiene):** `/nagisut`, `/cookies`, `/disclaimer` added to
  `ALL_INDEXABLE_PATHS` (sitemap-paths.ts); false `(page stays noindexed)` comments corrected on
  all 5 legal pages (they set no robots override, inherit index:true from root layout).
- Scope clean: 6 files, +13/−5, comment + string-array only. No content/copy, no scoring, no
  behavior change beyond sitemap membership.

Consumer-facing (sitemap membership changes crawl surface) → **owner merges** (tripwire-2).
Status held IN_PROGRESS pending that merge. `gh` is not installed this session, so the orchestrator
cannot open the PR — owner opens+merges `seo/crawl-hygiene-task499-clean`, or restores `gh`.
CLOSE on owner merge.
