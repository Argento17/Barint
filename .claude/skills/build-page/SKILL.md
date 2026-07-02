---
name: build-page
description: Build one Bari comparison page end to end — the WHOLE cycle from BSIP0 data acquisition (scrape) through BSIP1 enrich, BSIP2 score, page generation, two-gate copy, validation, render, and terminal red-team. Use to build or rebuild a single category page from scratch.
---

# /build-page — Full single-category cycle (BSIP0 → live page)

**Owner lane:** Orchestrator drives; Data / Nutrition / Content / Frontend / Adversarial-QA
own their stages. This is the page-centric driver for ONE category; for the multi-category
gate contracts see `bari-category-factory`. The tweak that makes this skill distinct: **it
starts at BSIP0 (the scrape), not at an existing corpus.**

## Use this when
- "Build the <category> page", "rebuild <category> from scratch", "do the whole cycle for <category>".

## Stages (in order — do not skip, do not reorder)

### 0. BSIP0 — data acquisition (the scrape) ⟵ included on purpose
- **Source selection (HARD):** never default to one retailer. Attempt
  **Shufersal → Victory → Yochananof → Rami-Levy**, use the reachable ones, cross-check
  nutrition across sources. Per-env reachability differs (document blocked retailers, never
  silently skip). Policy: `03_operations/bsip0/scrape/retailer_capabilities/SOURCE_SELECTION_POLICY.md`.
- Per-category scrapers live under `03_operations/bsip0/scrape/<retailer>_<category>/`; follow
  `03_operations/bsip0/scrape/BSIP0_PLAYBOOK.md`.
- **OFF IS BANNED — project-wide, every field, forever.** Ingredients + nutrition come ONLY
  from the direct product scrape. If a field isn't parsed it is NULL and the page says
  "data could not be retrieved." Any OFF dependency is a launch blocker. (The BSIP0 README's
  "OFF enrichment" line is stale and overridden by this rule.)
- **Per-100g plausibility gate** is mandatory (snacks shipped per-serving-as-per-100g — never again).
- Gate: pass all 6 checks in `03_operations/bsip0/validators/bsip0_qa_validator.py` (the single
  source of truth). **Missing-data discard rule:** if a product's data isn't found one-shot,
  discard it — never punish/cap, never over-invest in re-sourcing.
- Output: one raw JSON per retailer per run; never modified after the gate passes.

### 1. BSIP1 — enrichment
Attribute extraction, `ingredients_text_he`, label assignment, comparison-dimension selection.
Validate coverage threshold. (Raw-vs-prepared boundary = tahini+sodium+energy, never protein.)

### 2. BSIP2 — scoring traces
Score every product; one trace dir per run under the corpus. This is the universe `generate_page` walks.

### 3. Generate the page
```
python 03_operations/page_generator/generate_page.py --config <category_config.json> --out <out.json>
```
Walks BSIP2 traces, looks up barcodes in BSIP1, applies OFF ban + subpool filter + dedup +
exclusions. All copy fields emit `PENDING_COPY`.

### 4. Copy — TWO-GATE sign-off (HARD RULE)
Every consumer-facing string is a *draft* until **both** the Content Agent **and** the
Adversarial-QA / Red-Team gate sign off. The orchestrator must NOT author copy inline.
Authoring engine is lane-agnostic (Sonnet / Cursor / Grok). Apply via:
```
python 03_operations/page_generator/copy_stage.py --staging <out.json> --live <baseline.json> --shelf <name>
```
Stale-copy flag fires on score moves past threshold — re-author those.

### 5. D4 additive wiring
Per `bari-category-factory` Stage 8 (`wire_d4_<category>.py`, copy from `w2_additive_copy_v1.md`;
assert score/grade/glassBox byte-identical after writing).

### 6. FAQ schema
```
python 03_operations/seo/generate_faq_schema.py --input <frontend.json> --category-he "<שם>" --url <canonical> --out <faq.json>
```
Copy to `bari-web/src/data/seo/<category>_faq_schema.json` and inject into the route.

### 7. Validate (hard gate battery)
```
python 03_operations/spine/validate_comparison_page.py --json <frontend.json> --traces <run_dir/products> --http
```
Hard exits: score==trace · OFF=0 · 0 PENDING in any rendered field · count consistency ·
ingredient sanity (no truncation / marketing bleed) · every product has a resolvable imageUrl.

### 8. Render locally
Render the page in `bari-web` (restart the dev server — Next.js caches JSON imports).
**Done = rendered + red-teamed, not gate-pass.** A 200 on an image URL ≠ it displays.

### 9. Terminal red-team + C3 bracket (capped loop, net-correction tracked)
`C3-before → Red-Team (re-run on the live page) → C3-after → loop if any new CRITICAL`.
Owner-ready only at **zero open CRITICAL**. Critic LLM lane = **Opus 4.8**; **C3 is an
additive cross-family scan with NO veto** (it proposes findings the critic adjudicates;
the gate stays gates-green + zero-open-CRITICAL). See adversarial-qa-agent.md §C3.

**Loop cap (HARD — deterministic, not a prose rule).** At most **3 red-team rounds**.
Log every round to the net-correction ledger; the ledger enforces the cap:
```
python 03_operations/page_generator/gates/redteam_loop_ledger.py --page <frontend.json> \
    --round N --criticals-open A --criticals-resolved B \
    --copy-fields-changed C --regressions D
```
- **Cap / non-convergence → escalate, never loop (exit 2).** A 4th round, or the 3rd
  round still carrying an open CRITICAL, stops the loop: route the open CRITICALs to the
  owning agent and surface to the orchestrator. Never spin indefinitely.
- **Net correction = resolved − regressions (exit 1 if negative).** A round that breaks
  more previously-clean copy than it fixes FAILs — revert that round's copy churn before
  continuing. The loop drives CRITICALs to zero; it never churns already-clean copy.

Emit the orchestrator after-action report (use the `telemetry` skill) and **attach the
`_redteam_ledger.json`** as the per-round evidence of net correction.

## Never
- Never use OFF. Never ship copy without both gates. Never call a page done before render +
  red-team. Never auto-deploy (owner-gated migration).

## Related
`bari-category-factory` (full gate contracts), `corpus`, `rescore`, `bari-qa-audit`, `telemetry`.
