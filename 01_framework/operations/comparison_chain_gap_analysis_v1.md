# Comparison-Page Chain — Gap Analysis v1: Fixes · Enhancements · Efficiency · Additions

**Status:** owner deliverable (2026-06-11)
**Companion to:** `comparison_page_production_map_v1.md` (the phase letters 0, A–K below refer to that map)
**Method:** every finding is pinned to a repo artifact, task record, or live-verified fact — no generic process advice. Verified today: registry state in `tasks/` + `tasks/closed/`, TASK-245 close record (re-point is LIVE), yogurts OFF remediation brief, prod-sync decision brief, drafted CI workflows, factory artifact coverage.

**Context that frames everything:** the biggest structural defect — production serving from a repo 81 commits behind where all work happened — was found and **fixed today** (TASK-245: bari.digital now deploys from Barint master, 9/9 routes live-verified, 0 OFF refs). This analysis is about what that fix exposed and what remains.

---

## 1. FIXES — What Is Broken Right Now

Ordered by consumer impact. **P0 = consumers see it today. P1 = wrong but not yet visible. P2 = hygiene.**

### FIX-1 (P0) · The live yogurts page is the thin interim shelf — and the replacement is ready, parked behind 3 gates
- **What consumers see now:** yogurts v3 — 11 products, **0 of 11 with ingredient data**, all confidence partial/"under review," and a shelf with a high-protein bias (the mainstream plain/bio/Greek/flavored shelf is absent). A consumer looking for plain 3% yogurt sees a protein-product wall. (Source: `yogurts_off_remediation_decision_brief_v1.md` §2.)
- **Also live:** "NOVA" appears 9× in consumer-visible prose on this page — internal jargon the editorial law bans (logged at TASK-245 close as non-blocking).
- **The fix already exists:** run_yogurt_006 / v4 — 88 products, 0 errors, all red-team findings resolved (TASK-249/250, both RETURNED). It is held by exactly three gates: ① **your sign-off on Ruling 3** (two products change published grade: 35/D→35/E, 50/C→50/D — tripwire), ② Content Agent's ceiling-compression caveat copy, ③ QA baseline freeze on run_006.
- **Action:** this is the single highest-leverage consumer-facing move available — the work is done, only the gates remain. Your Ruling-3 decision is the critical path.

### FIX-2 (P1) · QA passed a corpus that red-team demolished — the QA gate tests traceability, not truth
- **Evidence:** run_yogurt_005 cleared QA, then red-team found ingredient text corrupted on **67 of 89 products** (website disclaimer text parsed as ingredients) plus a protein=190 g/100 g value no gate blocked. The QA protocol (`bari-qa-audit` skill) checks coverage, traceability, and version match — nothing in it checks whether parsed values are *plausible* or parsed text is *ingredients at all*.
- **Consequence:** truth-checking currently happens only at Phase F (red-team), the most expensive place to discover data corruption — after scoring, copy, and packaging (a full regeneration cycle; yogurt needed 6 runs).
- **The fix is half-built and stuck:** TASK-218 (systematic BSIP0 scrape QA standard) sits at **RETURNED, unclosed**. The yogurt remediation also built exactly the right machinery — `macros_plausible`, `ingredient_text_quality`, disclaimer-strip — but as **yogurt-specific builder code**, not shared pipeline infrastructure.
- **Action:** close TASK-218 and adopt it as a blocking Stage-B/C gate; lift the run_006 plausibility checks into the shared BSIP1 core so every category gets them for free.

### FIX-3 (P1) · Five RETURNED tasks are queued at the close gate — the chain's single-threaded bottleneck is verification
- **Queue today:** TASK-217 (juice NOVA-1 floor gate), TASK-218 (scrape QA standard), TASK-241 (salty 12-product rescue), TASK-249 + TASK-250 (yogurt v4). All carry finished work that is invisible to the roadmap until CC verifies and closes.
- **Why it matters:** the orchestration model is correct (no agent closes its own work) but close-verification is currently the slowest link — finished engine fixes and gates sit in limbo, and downstream tasks they `block` stay shut.
- **Action:** run a batch close-readiness session now; route the mechanical verification steps (file-exists, count-matches, grep-zero) to the cheap-LLM lane per CC v4.1 so CC judgment is spent only on judgment.

### FIX-4 (P1) · Known engine defects, all registered, none landed
| Defect | Task | State | Risk |
|---|---|---|---|
| Fermentation keyword bonus **uncapped** (yogurt TRIM Path A gap) | TASK-246 | IN_PROGRESS | A product can ride keyword stuffing toward A/S |
| **Absence-as-zero**: a missing nutrient field scores as 0 cross-category | TASK-236 | **BLOCKED** | Systematically punishes honest missing data — contradicts "unknown is acceptable" |
| Juice NOVA-1 floor fires for reconstituted-from-concentrate | TASK-217 | RETURNED | Reconstituted juice gets a whole-food floor it didn't earn |
| Router v2 has **no bread/cracker archetype**; seed-topped bread routes as whole-food-fat | scoring.md known gaps | unowned | Misrouting = wrong calorie-density table = wrong score |
- **Action:** TASK-236 deserves priority — it is a *philosophical* defect (the engine's data-honesty principle violated by the engine itself), and it touches every category's confidence story.

### FIX-5 (P2) · Registry/reality drift — the dashboard overstates what's still open
- TASK-237 (salty OFF re-source) is IN_PROGRESS, but salty v4 with 29 real products **shipped to production today** under TASK-245 — 237 is done-in-fact, open-on-paper.
- Memory drift: the memory index still says "TASK-189 open — granola sodium gap"; TASK-189 **closed 2026-06-05** with the `BARI_SODIUM_CEREAL` flag implemented.
- Four blog tasks (TASK-203–206) have sat IN_PROGRESS since their opening; either dispatch or park them explicitly.
- **Action:** one CC drift sweep closes all of this in an hour.

### FIX-6 (P2) · "NOVA" jargon ruling pending on two more live pages
- Maadanim (86 hits) and hummus (70 hits) show "NOVA" in metric cells — possibly the designed column, possibly the same leak as yogurts. Routed at TASK-245 close for an editorial ruling that hasn't happened.
- **Action:** Content Agent ruling: designed column = keep + document as exception; leak = template fix.

---

## 2. ENHANCEMENTS — What Works but Could Be Better

### ENH-1 · Generalize the yogurt honesty gates to every category
The disclaimer-strip, `macros_plausible`, and `ingredient_text_quality` machinery (run_006) is the best data-quality work in the pipeline — and it protects exactly one category. Lift into `03_operations/bsip1/core/` so phases C/H apply it everywhere. The shared `bsip0_gate.py` + 30 tests already exist (untracked) — finish, commit, wire.

### ENH-2 · Finish the verdict-copy standard rollout (8 categories pending)
The standard is ruled (verdicts name calorie density + the real fired driver; sodium = displayed fact only, never an unfired "driver") but is **live in new categories only**. Eight legacy comparison pages still carry pre-standard verdicts. One Content Agent pass per category; no data changes.

### ENH-3 · Image story after de-OFF
The OFF purge correctly nulled contaminated images — which means several live categories now show placeholders. Backfill ran for butter/granola/cereals (TASK-208, TASK-243 closed). Worth one QA sweep: per live category, % products with a real scrape-sourced image, and a stated SLA ("no category launches under X% image coverage; placeholders are acceptable, OFF never").

### ENH-4 · Wire the two finished-but-idle quality frameworks into the chain
- **Hebrew Golden Eval framework** (TASK-220, built): run it as an automatic Phase-G gate on every copy batch — it directly mechanizes the read-every-string rule that currently depends on discipline.
- **LLM observability event schema** (TASK-219, built): emit events from pipeline runs so "what ran, when, with which config hash" stops living only in per-run report files.

### ENH-5 · Red-team earlier *and* at the end, not just at the end
Keep Phase F as the full adversarial audit, but add a **30-minute "data sanity" red-team pass right after BSIP1** (before any scoring): sample 10 products, read raw ingredient text vs parsed output, check macro plausibility. Run_005's disaster would have been caught there for the cost of one agent-hour instead of a full regen cycle.

---

## 3. EFFICIENCY — Same Quality, Less Time and Cost

### EFF-1 · Shift truth checks left (the 6-run lesson)
Yogurt's cost structure: errors injected at Phase B/C were discovered at Phase F, forcing B→F reruns. Every plausibility assertion moved from F to C converts a multi-session regen into a minutes-level parse fix. This is FIX-2/ENH-1/ENH-5 viewed as an efficiency case: **the same checks, earlier, are ~10× cheaper.**

### EFF-2 · Commit the drafted CI — it's written and has never run
`.github/workflows/barint_ci.yml` already defines the right gate set (next build + lint + corpus validation + BSIP0 nutrition tests + 64 enricher tests + router & golden-corpus regressions + BSIP0 gate tests) — but the folder is **untracked**; no PR has ever been CI-checked. Committing it makes every frozen-invariant and build gate automatic instead of a manual checklist item. **Add one missing job: the OFF-string sweep** (grep for `openfoodfacts|off_api` across `bari-web/src/data/` — today that check is manual at Phase J).

### EFF-3 · Finish the shared packaging core (TASK-233F)
10 category generators still await migration to the shared core. Today each category has a bespoke builder (`build_yogurts_frontend_v4.py`, `_v006.py`, …) — every honesty gate, assertion, and format change must be re-implemented per category, which is exactly how yogurt-only safeguards happen. One core = write once, every category inherits.

### EFF-4 · Reconcile the factory skill with practice
The skill mandates per-stage artifacts (`shelf_map.json`, `bsip0_gate_result.json`, `qa_gate_result.json`…). Reality: only 4 categories have them (cereals, cheese_spreads, juices, hard_cheeses); yogurt — the newest, most scrutinized run — produced none. Two honest options: have the shared runner **emit them automatically** (preferred — zero marginal effort once EFF-3 lands), or trim the skill to the artifacts that earn their keep. A spec that the flagship run ignores trains agents to ignore the spec.

### EFF-5 · Unblock the close gate (cheap-LLM verification lane)
Per FIX-3: mechanical claim-verification (file exists, counts match, grep clean, build green) is zero-judgment work — route it to the Stupid-LLM lane with idiot-proofed prompts; CC reviews the evidence table and spends judgment only on judgment calls. Target: RETURNED→CLOSED in hours, not days.

### EFF-6 · Run copy and packaging in parallel after score freeze
Phases G (copy) and H (packaging) are serial today but share only one dependency: frozen scores + traces. Once QA freezes the baseline, dispatch Content and Data in parallel; H consumes G's strings at the end. Saves roughly one session per category.

### EFF-7 · Name the Shufersal-VPN dependency as an operational gate
Yogurt re-acquisition waited on Israeli-IP VPN availability — an undocumented, ad-hoc bottleneck for every future scrape. Cheap fix: a scrape-window runbook (when VPN is up, which scrapes queue, who flips it) so Phase B never silently stalls.

---

## 4. ADDITIONS — What Doesn't Exist Yet

### Must-have

**ADD-1 · Post-deploy production smoke test (automated).**
The prod/local split survived for months because *nothing watched the live site*. TASK-245 fixed the topology and CC live-verified the flip manually — but there is still no recurring check. Minimum viable: a scheduled job hitting every `/hashvaot/*` route asserting HTTP 200, 0 OFF refs, and the expected data-version marker per page. This is the **regression alarm for the entire class of "what's actually live?" failures.**

**ADD-2 · Live-state manifest (route → data version → run ID → baseline).**
Gap 2 of the prod-sync brief was precisely this absence: nobody could enumerate what would ship at re-point without hand-diffing repos. A small machine-readable manifest, updated by the packaging step and verified by the smoke test, makes "what is live?" a lookup instead of an investigation — and gives ADD-1 its expected values.

**ADD-3 · Adopt the BSIP0 scrape QA standard as a blocking gate.**
TASK-218's deliverable, closed and wired into Phase B for every future scrape (= the institutional form of FIX-2). The chain's weakest link is between retailer HTML and BSIP1 — it deserves a standing gate, not per-category heroics.

**ADD-4 · Data-freshness policy per category.**
Pages show "updated" lines, but no policy says when a category *must* re-verify (prices change, recalls happen, reformulations ship). Even a coarse rule — "re-scrape + re-verify every N months; show the date honestly; stale categories get a banner" — converts an unbounded liability into a scheduled cost. Frozen invariants already require re-verification on every rescore; this extends the discipline to corpus age.

### Nice-to-have

**ADD-5 · Consumer analytics loop.** The phase metric ("mobile user understands the shelf in 15–20 seconds") is unmeasured in production. Lightweight privacy-sane analytics (route traffic, scroll depth, filter usage) would let Product sequence the category roadmap on demand instead of intuition.

**ADD-6 · Editorial regression suite.** Banned-phrase + jargon linter (the 9 banned phrases, "NOVA", score-presentation rules) run automatically over every frontend JSON + page copy at build time. FIX-6 would have been impossible to ship.

**ADD-7 · Price display.** The `il_prices` read-only client exists (TASK-170). Price-per-100g next to scores is a major consumer-value add — and a new honesty surface (stale prices), so it needs its own freshness rule. Post-launch, Product-gated.

**ADD-8 · Category health dashboard.** One generated page off the registry + manifest: per category — corpus age, last run ID, gates passed, live version, open findings. The command center tracks *tasks*; nothing tracks *categories* as first-class objects.

**ADD-9 · Cross-market disclosure (Wave 3 backlog, already scoped).** US/EU vs Israeli label gaps, D5 annotate-only, never a score move. Parked correctly; listed here so it isn't lost.

---

## 5. If You Only Do Five Things

| # | Action | Type | Why first |
|---|---|---|---|
| 1 | **Rule on yogurt Ruling 3** → ship v4 (88 products) over the thin 11-product live shelf | FIX-1 | Biggest consumer-facing improvement; work already done; you are the critical path |
| 2 | **Batch-close the RETURNED queue** (217/218/241/249/250) with the cheap-verification lane | FIX-3 + EFF-5 | Unlocks everything queued behind finished work |
| 3 | **Commit the CI workflows + add the OFF-sweep job** | EFF-2 | One commit; converts 5 manual gates into automatic ones forever |
| 4 | **Stand up the post-deploy smoke test + live-state manifest** | ADD-1 + ADD-2 | Closes the failure class that produced the worst defect in project history |
| 5 | **Generalize the yogurt honesty gates into shared BSIP1 + adopt TASK-218** | ENH-1 + ADD-3 | Makes the 6-run yogurt lesson permanent for every future category |

---

*Companion map: `comparison_page_production_map_v1.md`. All task states verified against `C:\Bari\tasks\` on 2026-06-11.*
