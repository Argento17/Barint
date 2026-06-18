# Factory Run #7 (cookies-near-coffee) — Retrospective & Codification
**Date:** 2026-06-14 · **Author:** Orchestrator · **Task:** TASK-275 · **Run:** run_cookies_004 (58 products)

This is the honest after-action for the cookies-coffee page: what worked, what didn't, what we
learned, and what got codified vs. what is still open. Written in response to owner review
2026-06-14 (7 comments + A/B/C/D request).

---

## A) ROUTING

### What we did / where we delegated
- **C1-CURSOR (spec-complete code):** scraper, gen_frontend_json, render trio clone. Worked until it
  hit a hard **quota-out (exit 1 "out of usage")** mid-run → per lane law marked DOWN, re-routed to
  native C1 with no revision loop.
- **C1 native (Sonnet judgment):** methodology, corpus-filter ruling, copy authorship, red-team
  remediation, the EV-058 router decision. This carried the judgment-heavy spine.
- **C2 (DeepSeek, free grunt):** the E-modal diagnostic (binding-vs-string-presence cap audit),
  bulk plausibility checks. **C2's "25 binding red-labels" was RIGHT and my own "61 string-presence"
  was the wrong metric** — a lane I under-trusted at first and should have trusted earlier.
- **C3 (gpt-5.5 outside-family advisor):** bracketed the red-team (before AND after, per owner
  directive). C3 review #2 caught **new factual errors in untouched verdicts** (fabricated "pecan"
  source, a "sugar-free" cookie with 23g sugar). Advice-only; never closed.
- **Gemini:** turned out **read/plan-only** — `write_file`/`run_shell_command` returned
  "Unauthorized tool call". Usable for analysis/planning, NOT production. Re-routed its render task
  to C1-Frontend. Also **timed out (1800s)** on a 61-call sequential dual-extract.

### What we learned
1. **Lane outages are normal, not exceptional.** In one run: Cursor quota-out, Claude session cap
   (×2), Gemini write-block, Gemini timeout. The run survived only because each failure re-routed
   one lane up without a revision loop. **Resilience came from the fallback discipline, not from any
   single lane being up.**
2. **Gemini's real shape: an analyst, not an executor.** It plans and reads; it does not write files
   or run shell. Splitting "a big Cursor task across Gemini+Cursor+Sonnet" only works if Gemini's
   slice is *analysis/plan* and the *write* goes to Cursor or Sonnet.
3. **C2 is underused and more trustworthy than I treated it.** Mechanical audits (cap-firing
   distributions, string-vs-fired reconciliation, plausibility sweeps) are exactly its lane and it
   was correct against my own hand-count.
4. **C3-before-AND-after is not ceremony.** The second C3 pass found real, shipped-if-unchecked
   factual errors that the first pass and the red-team v1 both missed.

### Codified?
- **PARTIALLY.** EV-058 (biscuit router category) and the red-team scope ruling were codified in the
  methodology folder during the run. **The routing lessons above were NOT yet written into
  `lane_routing_rules_v1.md`.** → ACTION: add "Gemini = analyst/plan-only" and "lane-outage fallback
  is the expected path, log the split every report" to the lane law. (Owner memory already has
  `feedback_lane_routing_antilaziness`; this run is the confirming evidence.)

---

## B) SPINE

### What we did / where we delegated
- Fetched + confirmed the **golden brined page** as the structural reference before starting.
- Followed the factory spine end-to-end: broad scrape → corpus-filter narrow → score → invariants
  → generate JSON → milk-depth schema → copy → render trio + charts → Stage-9 red-team → local.
- **Strategy worked exactly as the owner specified:** scrape broad (129), narrow after BSIP0 (→58).

### What we learned
1. **The spine held.** Every stage produced its artifact; the golden playbook's hard rules (recharts
   not hand-SVG, grade never color-encoded, screenshot-and-look, capture the real build exit code)
   were followed and caught issues.
2. **One spine gap surfaced: the page-data ↔ JSON divergence.** Page shell (hero/prologue/
   methodology) was hardcoded in `cookies-coffee-page-data.ts` AND present in the JSON `page_copy` —
   they could drift. Root-fixed by reading the shell FROM the JSON. **This should be the spine
   default for every category, not a cookies one-off.**
3. **The spine's weakest link is upstream of itself: ingredient parsing (see D).** The spine assumes
   BSIP1 hands BSIP2 a clean ingredient list. For 16/58 products it handed a single truncated token.
   The spine has no gate that catches "scored an indulgence cookie on 1 ingredient."

### Codified?
- **PARTIALLY.** The page-data→JSON refactor is done for cookies and noted as a follow-up to
  generalize. **Not yet a spine law.** → ACTION: promote "page shell reads from JSON page_copy" to
  the golden playbook, and add an **ingredient-sufficiency gate** to the spine (below).

---

## C) PROCESS

### What we did / where we delegated
- Verify-before-close at every seam: each return treated as RETURNED-UNVERIFIED; claims checked
  against artifacts at file:line. This caught **several false self-reported counts** (my own
  string-presence error; a 59-vs-58 trace miscount that stalled a red-team).
- Two adversarial gates (red-team + C3), red-team v1 BLOCKED with 2 CRITICAL → remediated → v2
  zero-CRITICAL.

### What we learned
1. **Verify-before-close earned its keep** — but **my verification tooling was the bottleneck.**
   Repeated barcode-keying and encoding (cp1252) errors in quick checks produced false alarms I then
   had to walk back. The discipline was right; the execution was sloppy.
2. **A cosmetic mismatch can stall a gate.** The red-team watchdog hung 600s investigating a
   59-vs-58 trace count that was just a stale excluded trace. **Housekeeping (move excluded traces
   OUT of the run dir) is a pre-gate step, not an in-gate discovery.**
3. **"Done" was declared at the wrong altitude.** The page passed both gates and was called
   owner-ready — yet owner review immediately found substantive nutrition-reasoning gaps (מחמאה,
   additive depth, calorie/sat-fat treatment) that **neither gate was scoped to test.** The gates
   checked *propagation and fabrication*, not *scoring-philosophy adequacy*.

### Codified?
- **PARTIALLY.** The red-team scope ruling was codified. **The biggest process lesson — that our
  gates don't test scoring-philosophy adequacy — is NOT codified.** → ACTION: add a
  "nutrition-adequacy" lens to the red-team scope (does the engine actually *see and reason about*
  the ingredients a human notices?), distinct from propagation QA.

---

## D) LESSONS / MISTAKES TO CODIFY

### D1. **Ingredient truncation — 16/58 products scored additive-blind (CRITICAL, real)**
- **Fact (trace-derived):** 16 of 58 traces have `ingredient_count == 1`, with `ingredient_list`
  = the first fragment before the first "(", e.g. `["קמח חיטה ("]`. The full ingredient string
  exists in BSIP1 (it renders correctly on the page) — so this is a **BSIP1→BSIP2 parser bug**, not
  a scrape gap. **Divergence: the page displays full ingredients; the engine scored one token.**
- **Blast radius:** the entire L3 additive/PHVO/sweetener/seed-oil/whole-grain layer ran on one
  token for these 16. Corpus-wide: `has_phvo` fired **0/58**, `sweetener_detected` **7/58**,
  `additive_marker>0` **29/58** — all undercounts.
- **The #1 product on the page (540160, 63.1/C, the shelf "winner") is one of the 16.** Its additive
  profile was never actually evaluated. (It is genuinely clean, but the engine didn't establish that.)
- **Command:** `for f in run_cookies_004/products/*/bsip2_trace.json; do jq '.L1_observed_signals.ingredient_count' $f; done | sort | uniq -c`
- **Codify:** add an **ingredient-sufficiency gate** — if `ingredient_count==1` AND the raw BSIP1
  string contains ≥2 commas, FLAG (re-parse or mark low-confidence), never silently score. This is
  a data-integrity gate, not a scoring change.

### D2. **מחמאה / hardened-fat blindness (HIGH, real methodology gap)**
- **Fact:** at least 2 products (ביסקוטי 7290017898506; the cashew biscotti) list
  `מחמאה (שומנים מוקשים מן הצומח)` = imitation butter / hardened vegetable fat. `has_phvo` fired
  **0/58**. The ביסקוטי scored `fat_quality: 87` and `additive_quality: 100` — i.e. the engine
  rated its fat as *high quality* while the label declares hardened vegetable fat.
- **Two causes stack:** (a) truncation (D1) hid the ingredient entirely; (b) **even un-truncated, the
  PHVO detector (EV-050) markers are singular `שומן/שמן צמחי מוקשה` and would NOT match the plural
  `שומנים מוקשים מן הצומח`, and `מחמאה` is not a recognized term at all.** The engine has no concept
  of מחמאה as a distinct cheap-fat ingredient.
- **Codify:** this is Nutrition Agent's lane (dispatched 2026-06-14). Needs: (1) PHVO marker set
  widened to catch `שומנים מוקשים`, `מן הצומח` hardened constructions, and `מחמאה`; (2) a
  methodology stance on imitation butter (owner: "severely punish"); (3) a research note on what
  מחמאה actually is and why it's worse than חמאה. Any score-moving change → tripwire-1 (rescore +
  bleed + invariants gate before publish).

### D3. **Gates test propagation, not nutrition adequacy (process)** — see C3. Codify a
  nutrition-adequacy lens distinct from propagation QA.

### D4. **My verification execution was error-prone (self).** Barcode-keying on a dict, string-
  presence ≠ cap-fired, cp1252 stdout on Hebrew. Codify: quick-check scripts force `encoding=utf-8`
  + `PYTHONUTF8=1`, key on the dict key, and read the `fired` boolean, never string presence.

### D6. **Additive severity is known in DISPLAY but discarded at SCORING (HIGH, real, owner-found 2026-06-14)**
- **Fact:** additive descriptions come from a curated static table `ADDITIVE_DB` in
  `gen_frontend_json.py` (NOT per-product generation → no fabrication risk). Entries are factually
  accurate (E150D = Class IV sulfite-ammonia caramel, 4-MEI byproduct; E322 = benign lecithin).
- **Two gaps:** (a) each `ADDITIVE_DB` entry carries a `tier` field
  (`functional/likely-neutral/dose-dependent/contested`) — but that tier drives only the **display
  badge**; the **score engine never reads it.** The engine's additive logic *counts* markers
  (`ADDITIVE_MARKERS_3_PLUS→cap72`, `5_PLUS→cap60`), so E150D (contested colorant) and E500 (benign
  leavening) move the score **identically.** We hold severity knowledge and throw it away at scoring.
  (b) No **category-rarity** model — the table is a flat glossary; it cannot say "E150D is unusual
  for a biscuit" (the owner's exact "from all the biscuits I've seen, THIS one…" standard).
- **Display entries are also thin** — E150D omits Prop 65 / IARC 2B weight.
- **Codify:** fold into the Nutrition additive-depth ruling (running) — wire `tier` into scoring as
  severity-weighted (not counted) additive quality, add per-category additive frequency, deepen the
  high-signal entries. Score-moving → tripwire-1.

### D5. **Calories are in the model but flat within this shelf (informational, not a bug).**
  `calorie_density` is 15% weight, but biscuits cluster ~415–540 kcal and mostly sit at the 50
  baseline; the HIGH_CAL caps require pairing with sugar/low-satiety. So calorie density is a weak
  *differentiator* here (correct — they're all calorie-dense). Sat-fat, by contrast, IS handled at
  three levels (red-label cap 55, the 2-red-label cap 45, fat_quality dimension, HP_FAT_SUGAR combo).
