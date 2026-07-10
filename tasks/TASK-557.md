---
id: TASK-557
title: Sweetener consumer guide (/madrichim) — evidence brief + build
owner: research-agent
status: BLOCKED
priority: MEDIUM
created_at: 2026-07-10
updated_at: 2026-07-10
depends_on: []
blocks: []
category_id: null
blocked_on: owner go-live decision (tripwire #2 — irreversible + consumer-facing). Copy is two-gate signed-off, rendered, and DOM-verified; page stays noindex until the owner flips it.
summary: >
  Owner-directed (2026-07-10). Build a consumer sweetener guide under /madrichim. Guide copy requires
  two-gate sign-off (Content + Adversarial QA) before owner review. No scoring change. Copy is COMPLETE
  and both gates have PASSED (v13); rendered page verified. Blocked only on the owner's go-live call.
---

# TASK-557 — Sweetener consumer guide (/madrichim) — evidence brief + build

## State (2026-07-10)

**Copy: DONE and two-gate signed off.** Live rendering verified. Blocked only on owner go-live.

### Deliverables (verified at artifact level)
- Consumer copy: `02_products/guides/sweetener_guide_he_draft_v1.md` (v13), sha256
  `811e6c22417bd1f6a2b07ab5d966b5d6033df46dd21df8f080158230d00fbaa6`. Consumer band between the
  `BARI:CONSUMER-COPY` sentinels.
- Fact base (the only permitted source): `01_framework/research/sweetener_guide_verified_facts_v1.md`.
- Frontend data: `bari-web/src/lib/guides/sweetener-guide-data.ts`, sha256
  `b13a39f0f0606a4ab3e4365b8307c219c3ebf8933a2c52fc54271a95fd32f877`. Byte-exact port of the v13 band
  (independently diffed: 7/7 sections, 27/27 paragraphs, 9/9 sources, 2/2 statutory strings).
- Page: `bari-web/src/app/madrichim/sweeteners/page.tsx`. `noindex`, off the `/madrichim` hub, off
  `sitemap.xml`. `next build` clean (306/306 static pages); DOM verified on a production server —
  all v13 strings present, all ten fixed defects absent, `noindex` present.

### Gate trail
- **Gate 1 (Content Agent):** authored v8→v13.
- **Gate 2 (Adversarial QA / Red-Team):** eleven passes. Final pass on v13 = PASS, 0 CRITICAL /
  0 HIGH / 0 MEDIUM.
- **Orchestrator independent checks:** hazard checker (0 fails, positive+negative controls live),
  byte-exact band↔.ts diff (0 fails), rendered-DOM assertion (all pass), git-tree integrity after a
  stash incident (no damage).
- Ten defects found and fixed across the loop; five originated with the orchestrator (fact base /
  brief), and were caught by the independent gate + checker. See the digest and
  [[false_inference_hides_in_bridges]], [[product_names_are_verbatim_strings]].

### Open, tracked separately (do NOT block go-live decision unless owner says so)
- **EXCEPTION-005** (draft, not committed): English Vancouver citations with DOIs render on a consumer
  page. Needs Product approval + a Design render-form call before it is anything but a draft.
- **TASK-562** (nutrition): is sucralose authorised in Israeli baked goods; does EFSA's dechlorination
  finding touch any scored product.
- **TASK-566** (data): `integrations/clients/http.py` shadows stdlib `http`; make gate callers fail loud.
- **TASK-572** (data): capture statutory label warnings (polyol >10%, aspartame/phenylalanine) at acquisition.
- **TASK-573** (data): expose USDA FDC Branded ingredient text for a US-shelf annotate-only comparison.

### Go-live (owner, tripwire #2)
Flipping `noindex`, adding to the `/madrichim` hub, and adding to `sitemap.xml` is the owner's call.
Nothing here ships to the public until then.
