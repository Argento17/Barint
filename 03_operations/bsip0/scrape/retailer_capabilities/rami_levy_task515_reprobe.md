# Rami Levy re-probe — TASK-515 (yogurt), 2026-07-05

**Verdict: still BLOCKED.** Consistent with every prior probe (2026-06-05, 06-07,
06-20). Attempted per the BSIP0 source-selection policy (probe every run, never
assume last run's reachability table).

## What was tried this run

1. **Price-transparency feed** (the preferred structured path):
   - `https://prices.rami-levy.co.il/` → `ConnectionError` (DNS/TCP failure, no route)
   - `https://url.retail.publishedprices.co.il/login` (Cerberus successor guess) → `ConnectionError` (DNS failure)
   - `matrixcatalog.co.il` (suggested alternative in `rami_levy.yaml`) → `SSLError` (SSL EOF, no valid handshake)
   - `il_prices` client registry (`integrations/source_registry.py`): `rami_levi` is registered
     with `il_prices_chain_id=None, il_prices_kind=None` — confirmed, no known feed to query.

2. **Storefront** — NEW finding this run: `https://www.rami-levy.co.il` (note the
   hyphen; `rami_levy.yaml`'s `https://www.ramilevi.co.il` — no hyphen — does not
   resolve at all) returns HTTP 200 via plain `requests`, and even a guessed
   search-results URL returns 200. This is DIFFERENT from the 2026-06-07 assessment
   ("login-gated JavaScript SPA, no public API"). However:
   - The search-results page is a Nuxt.js SSR shell with **zero product markup**
     server-side (0 occurrences of "יוגורט", 0 `data-product` attributes) — results
     are fetched client-side after hydration.
   - Three guessed client API endpoints (`/api/search`, `/api/items/search`,
     `/apps/RamiLevi/api/search`) returned either 404 or `["Internal Server Error"]`
     — the real API contract could not be reverse-engineered from static probing
     alone (likely needs a session/store-context cookie or a POST body, not
     discoverable without a browser HAR capture).

## Why this doesn't change the GO/NO-GO for TASK-515

The hard requirement is **≥3 reachable retailers**; Shufersal + Victory + Yohananof
satisfy that. Rami Levy is being **documented, not silently skipped**, per the
scrape-source-selection policy. Cracking the Nuxt client API would need a real
browser session (HAR capture + replay) — a genuine follow-up task, not a same-run
fix, and out of proportion for a 4th source when the composition/cross-check gates
are already satisfied by three.

## Recommendation

Open a dedicated follow-up (suggest TASK-516 or fold into a future BSIP0
infra task): capture a real Playwright session against
`www.rami-levy.co.il/he/online/market/search-results`, inspect the Network tab for
the actual XHR the Nuxt app fires post-hydration, and replay that endpoint directly
via `requests` with the correct headers/cookies. Do NOT attempt Rami Levy via
Open Food Facts pairing under any circumstance (project-wide OFF ban).
