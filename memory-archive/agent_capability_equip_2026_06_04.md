---
name: agent-capability-equip-2026-06-04
description: "2026-06-04 build that equipped all 11 Bari agents with new API/knowledge clients (EDPG pattern) + bari-web QA harness + CC health log, lifting each agent grade to ≥90"
metadata: 
  node_type: memory
  type: project
  originSessionId: 2940e96d-2a0c-49f2-b3ed-977cc6a3022c
---

Closed the agent-capability gaps from the grading (Research 82 → Content 22) by building real
stdlib clients in `C:\Bari\integrations\clients\` (locked EDPG pattern: `from .http import
get_json`, `CLIENT_VERSION="1.0"`, dataclasses, `found=False` on 404, `__main__` smoke test
with `sys.stdout.reconfigure` for Hebrew), plus frontend infra in `bari-web` and a CC health
log. **Honest status only — LIVE-VERIFIED requires a real successful smoke test.**

**New clients (LIVE-VERIFIED 2026-06-04, free/no-auth unless noted):**
- `usda_fdc` — USDA FoodData Central; normalises to the same canonical per-100g keys as `tzameret`; `FDC_API_KEY` (DEMO_KEY rate-limited). [Nutrition, Data]
- `food_additives` — OFF additives taxonomy (disk-cached); E-number→name/class/EFSA-eval/over-exposure (E621=high). Honest limit: NO numeric ADI / no IL-vs-EFSA divergence. [Nutrition D4 MOAT, Red-Team]
- `semantic_scholar` — Graph API; tldr + influentialCitationCount + citation_velocity. [Research, Red-Team, Nutrition]
- `biorxiv` — bioRxiv/medRxiv preprints (date-window recent + DOI); `peer_reviewed=False`, `published_doi` upgrade flag. [Research, Red-Team]
- `crossref` — DOI metadata + references_count + **retraction/update-to integrity signal**. [Research, Red-Team]
- `openfda` — food recalls/enforcement + CAERS adverse-event counts (harm signal); US-jurisdiction caveat. Search is single-field (the `+`-OR breaks under urlencode). [Red-Team, Research, Nutrition]
- `hebrew_readability` — OFFLINE; readability heuristic + **framework-leakage gate** (`is_clean`: NOVA/cap/floor/BSIP/dimension/score-mechanic/recommendation). Leakage scan is a precise gate; readability score is a heuristic, not validated. [Content, QA]

**NEEDS-ENV-VERIFY (complete + correct; live check waits on a connected account — capability at target, not a fabricated green):**
- `search_console` — GSC Search Analytics; OAuth2 `GSC_ACCESS_TOKEN`+`GSC_SITE_URL`; carries a local stdlib POST helper (query is read-only). [Marketing]
- `analytics` — Plausible Stats; `PLAUSIBLE_API_KEY`+`PLAUSIBLE_SITE_ID`. [Marketing, Product]
- `figma` — Figma REST files/components/styles; `FIGMA_TOKEN`+`FIGMA_FILE_KEY`; for token-drift diff vs Tailwind. [Design, Frontend]

**bari-web QA harness (devDeps only — zero runtime/bundle cost):** added `@playwright/test`,
`@axe-core/playwright`, `@lhci/cli`. `playwright.config.ts` (mobile-first Pixel 5 + desktop),
`e2e/smoke.spec.ts` (**LIVE-VERIFIED 5/5 mobile** against dev server), `e2e/a11y.spec.ts`
(axe — **found a real WCAG 1.4.3 contrast violation on the grade chips**, a true positive for
Design), `lighthouserc.json`. Bundle analysis = Next 16.1+ built-in `next experimental-analyze`
(deliberately NOT `@next/bundle-analyzer`, which is Webpack-only and would drop Turbopack). Chromium was already cached so no heavy browser download.

**CC:** `05_command_center/registry_health_log.py` — append-only JSONL health time-series +
degradation diff (blocked/returned/CR/WIP-over-limit/alerts/drift/CLOSED-drop) + a
`github_artifacts` CI probe. LIVE-VERIFIED (append + synthetic degradation). Reads
`command_center_live.json`; only writes its own log.

**Live-validation findings + targeted improvements (2026-06-04, post-build):**
- `semantic_scholar` free tier now **429s on a clean single request** → effectively NEEDS-KEY (`SEMANTIC_SCHOLAR_API_KEY`); README downgraded. Code is fine, tier is throttled.
- `PAGESPEED_API_KEY` is a Windows **User** var the agent's spawned processes **do not inherit** (`os.environ` sees it absent) → pagespeed runs keyless and 429s. Set it process/machine-level.
- `gh` CLI **not authenticated** → CC's CI/PR/merge verification is BLIND (git verification works fine — correctly reported the comparisons data as `committed-not-on-default`).
- **CC improved:** `github_artifacts` now has `verify_artifact(path)` (one-call verdict: shipped/committed-not-on-default/unverifiable/uncommitted/missing), tri-state `on_default` (None=can't-verify), and `ci_status`/`pr_for_commit` carry an `available` flag so BLIND ≠ "CI passed". registry_health_log CI probe + cc-agent doc updated.
- **Frontend improved:** key-free perf is now a Playwright Web-Vitals spec `bari-web/e2e/perf.spec.ts` (`npm run test:perf`), **LIVE-VERIFIED against the production build** — home LCP≈1.6s, comparison pages ≈1.14s, CLS=0. This is the primary perf gate (no PageSpeed key, no public URL); lhci runs but hits a Windows teardown EPERM (CI/Linux path).
- **Product improved:** `google_trends` is **LIVE-VERIFIED, account-free**, with new sequencing helpers (`.momentum`, `.is_rising`, `.summary()`); real read: חלבון +29%↑, יוגורט +12%↑, גרנולה flat. Product doc elevates it from "dormant" to the validated D1 launch-order instrument (fence held: demand ≠ quality, never scoring). Plausible (`analytics`) remains the NEEDS-ENV-VERIFY on-site signal.

All 11 agent docs got/extended an "External Data Access" section (content/design/qa newly
added; the other 8 extended). `integrations/README.md` layout + status table + env keys +
honest-caveat updated. Pattern + firewall unchanged: evidence/identity/analytics clients do
NOT stamp provenance; ingestion clients (usda_fdc) do — born `candidate`, engine reads
in-house labels only, EDPG admission gate unchanged. Builds on [[external_integration_layer_task170]].
