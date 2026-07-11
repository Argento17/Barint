---
id: TASK-268
title: Spine Stage 8: render_local_page — auto-wire every shelf run into a viewable bari-web page (terminal layer)
owner: frontend-agent
status: CLOSED
closed_at: 2026-07-11
close_reason: "DONE-IN-FACT - 03_operations/spine/pipeline_e2e.py exists (asserted) incl. render stage; TASK-321 sweep generalized the factory. Per ghost triage 2026-07-11 (tasks/reports/ghost_triage_2026-07-11.md); orchestrator mechanically asserted the cited artifacts before closing."
priority: HIGH
created_at: 2026-06-13
depends_on: [TASK-266]
blocks: []
category_id: null
summary: >
  Owner directive 2026-06-13: the locally-viewable comparison page is the FINAL LAYER of the engine/spine — auto-produced for every shelf, never asked for. Add Stage 8 render_local_page to 03_operations/spine/pipeline_e2e.py (after Stage 7 merge_copy_and_gate): take the gated page JSON + authored copy → emit the bari-web trio (data/comparisons/<cat>_frontend.json + lib/comparisons/<cat>-page-data.ts + components/comparisons/<cat>-comparison-page.tsx + app/hashvaot/<cat>/page.tsx) following the hard-cheeses pattern, typed + re-runnable + hash-skip + lineage like other stages, npm run build as the stage gate. GENERALIZE the P49 manual prototype (brined cheese) into this reusable stage. Local render only — deploy stays a separate owner-gated step.
---

# TASK-268 — Spine Stage 8: render_local_page — auto-wire every shelf run into a viewable bari-web page (terminal layer)

## Why this is now a SPEED blocker (not just tidiness)
Brined retrospective (`01_framework/operations/brined_session_retrospective_v1.md`): the brined page
was hand-built, so EVERY re-render was a bespoke C1-CURSOR dispatch with a hand-written spec (P49,
P50, P53, P54). That per-change bespoke render is the main wall-clock sink. A one-command Stage-8
render turns each re-render from a 3-4 min dispatch into a seconds-long script call, compounding on
every future shelf. **Promoted from tidiness → speed-critical; do before the next shelf run.**

## OWNER CHALLENGE (2026-06-13) — parallelize across the THREE C1-grade lanes
The orchestrator over-used the **metered Claude C1** lane (4/4 judgment agents on native Claude this
session) when **C1 is a THREE-lane PARALLEL tier**, two of them flat-rate:
- **C1 (native Claude subagents)** — reserve for work needing Bari persona/memory/governance mid-task.
- **C1-CURSOR** (flat-rate) — spec-complete code/file edits.
- **C1-GEMINI** (flat-rate, LIVE + verified P47, `dispatch.py --selftest-gemini` PASS) — **was used
  ZERO times this session.** C1-grade judgment/investigation with repo access.

**The rule to bake in:** up to **3 C1-grade tasks run in PARALLEL, one per lane**, before any second
task is queued on the metered Claude lane. Distribute independent judgment/investigation work across
Claude-C1 + Gemini + Cursor concurrently; default to the flat-rate lanes and keep metered Claude C1
for what only it can do. A ledger where C1-GEMINI and C1-CURSOR sit dark while Claude C1 carries 4
serial agents is itself a routing-failure signal (same class as the prior 100%-C1 collapse).

**Acceptance addition:** Stage 8 must be lane-agnostic (any C1 executor can run it from the spec), and
the retrospective's render→red-team→consolidate→render macro + parallel-by-default (incl. the 3-lane
C1 tier) must be reflected in `lane_routing_rules_v1.md`.

## OWNER PAGE-REVIEW additions (2026-06-13, brined) — these become render-STANDARD, every page
The render stage must produce these automatically (not hand-added per page):
- **Category card on the `/hashvaot` index** (`bari-web/src/app/hashvaot/page.tsx`). Every rendered
  shelf auto-registers a card on the index — owner found brined live at its route but ABSENT from the
  index. No page is "rendered" until it's discoverable from the index.
- **Category hero image, auto-extracted + planted.** The pipeline picks a representative category
  image from the scrape and wires it into the page — agents do this automatically, not the owner.
- **Additives dropdown is a comparison-page STANDARD** (the data-driven "תוספים זוהו" component with
  per-E-number expandable cards — already renders elsewhere). The brined page only carried a thin
  "preservative" limiting-factor. Stage 8 must populate the additives data array (E-number, name,
  technical role, plain-Hebrew description) from the parsed ingredients and wire the dropdown. The
  milk page lacking it is NOT the standard — the standard is: every comparison page has it.
- These three + the category caveat box are part of the render contract / its build gate.

<!-- scope/deliverable: generalize P49 manual prototype into the reusable typed Stage 8. -->

## RENDER-WIRING BUG found in brined review (2026-06-13) — must be in the standard
- The brined frontend JSON carries `imageUrl` for all 48 (real, barcode-matched, whitelisted), but
  `brined-cheeses-page-data.ts` does NOT map it into the row VM the way `milk-comparison-page-data.ts`
  does (`imageUrl: product.image_url`). Images therefore DON'T RENDER in-browser → owner perceived
  products as "made up." Real data, broken presentation.
- **Stage 8 must wire imageUrl into the row VM for every page.** **Stage 9 gate must check images
  RENDER (in-page), not merely resolve (HTTP 200)** — the orchestrator's earlier 48/48-resolve check
  passed while images were not displaying. Resolution != rendering.

## OWNER 10/10 review (2026-06-13) — more render-standard items
- **Brand name in EVERY product title** from the scrape `brand` field (e.g. "…5% — גד"). No-brand titles read as fabricated; surface real provenance. All 48 brined had a brand in scrape.
- **Additives dropdown reuse `AdditivePanel.tsx`** (exists, used on butter/hummus/milk) — populate per product from parsed E-numbers + Nutrition's E-number→description map. Replace the bare "תוספות מזוהות: preservative" line.
- **Banned-token gate** on consumer copy must reject internal run names (`run_\d+`, `bc-\d+`) — a Content pass leaked "run_005" to the page.

## GOLDEN EXAMPLE COMPLETE (2026-06-13) — owner-ratified
The **brined-cheeses page is the golden example** ("save it as golden example… initiate another shelf soon"). Built + verified to zero-CRITICAL: corrected copy (36 products, real brands, no internal tokens), 3 recharts data-journalism charts (sodium×grade / protein×fat / calories×score, hollow-point, grade never color-encoded), additives dropdown, brand-in-title, images render, products sorted by score desc, all 36 confidence=verified (expected-null sugar/fiber fixed). Build REAL_EXIT:0; rendered + screenshot-reviewed at desktop+mobile.
- **The full repeatable process is documented:** `01_framework/operations/golden_comparison_page_playbook_v1.md` (scrape→corpus→score→copy→render→charts→hygiene→verify + hard rules + the failures-to-skip). Memory: `golden_comparison_page_brined`.
- **Remaining (keep this task open):** generalize the manual golden instance into the one-command `render_local_page` spine stage — parameterize the chart component (derive captions; clean-detection must exclude stabilizers not just preservatives), templatize the render trio, fold the verify/screenshot gate into the build. Until then the playbook is the manual procedure.
- **NOT deployed** — local render only; deploy stays owner-gated.
