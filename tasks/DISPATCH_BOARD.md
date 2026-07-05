# Bari — Live Board

*Orchestrator's single live view. Compacted 2026-07-04 — prior append-log (2040 lines) archived at
`tasks/archive/DISPATCH_BOARD_pre_compaction_20260704.md` (2026-06-12 factory-reset log →
launch-sprint → cycle 1–6 all preserved there). The **registry (`tasks/TASK-*.md`) is the source of
truth**; this board is its view. Autonomy-default (`decision_authority_matrix_v1`); hard stops = the 5
tripwires, a consumer-facing deploy, an owner stop, or out-of-ready-work. WIP=2.*

**LIVE deploy target = `origin` = Argento17/Barint master (Vercel).** Push feature branches there; only
the owner merges consumer-facing PRs. `Argento17/bari` is DEAD — never push. `gh` may be absent in a
given session (was, 2026-07-04) — then the owner opens/merges PRs from the pushed branch in the UI.

---

## THE ROAD (2026-07-04)
**OWNER STRATEGY PIVOT (2026-07-04): supplements re-direction → TASK-504.** Ranking supplements is
retired as a product form (owner: creatine comparison "bad", magnesium ranking doubted too). New
top-level category **מדריכים (Guides)**: detailed guide + attribute-level verdicts (dose/form/
verification/price), unordered shortlist, worldwide-benchmark placement, pricing, plain buy button.
Supplements first; NO morph to other areas in v1. **Brief drafted → 4 consults running in parallel
(Product, Nutrition, Adversarial-QA strategy red-team, C3/P500) → synthesize concrete plan → owner.**
All creatine-thread work PARKED on owner stop (nothing pushed/merged; live site unchanged).
Launch-hardening (cycles 1–6) fully shipped. Nothing frozen; every live category re-flows on a switch.

## ✅ TASK-507 explore-next module (2026-07-04, marketing-driven) — CLOSED, PR open for owner merge (@ c67c5c7a)
GA4 (7d): hub-entry sessions (/, /hashvaot index, /catalog) browse 7–19 pages; leaf-entry (where all
social/paid traffic lands) = **1.0 pages/session** → paid clicks dead-end. Data-driven "עוד השוואות"
related-comparisons module added to the bottom of all 17 leaf /hashvaot pages (+1 blog demo). Worktree
`C:\bari-task507`, branch `frontend/task507-explore-next` (head 5d92a45d), PUSHED to origin (PR not opened —
gh absent; owner opens from compare URL). **Orchestrator verified:** diff additive (0 deletions → freeze
intact), snacks label correct (חטיפי דגנים, not stale registry nameHe), manifest data-driven + current-excluded.
**GATE RESULTS:** Content gate-1 ✅ SIGNED OFF ("עוד השוואות" unchanged; snacks label correct) — but caught a
2nd undeclared consumer string: card CTA "לכל ההשוואות" (to ALL comparisons) mislinks to a single category →
fix to "להשוואה". · Adversarial QA ⚠️ **CONDITIONAL PASS, 1 HIGH blocker (HIGH-1):** wiring `category` into
bread/cheese/crackers/milk pages (for the module) silently flows into product-row EXPANSION → bread & cheese
nutrition-bar scales + good/warn colors CHANGE (cheese protein goodAbove 8→20 flips green→grey). "Purely
additive/0-deletions" claim FALSE — additive diff, semantic side-effect via prop-flow. Orchestrator's own
numstat check was fooled; render-gate caught it. · Design conformance — STILL RUNNING.
**FIX PLAN (batched, one cycle):** decouple module category from the table prop (restore prior DEFAULT expansion,
reversible, zero consumer change) + CTA "לכל ההשוואות"→"להשוואה" + any Design findings + Product curation
(below) → back to Frontend Agent → re-gate QA. Ships only after clean re-gate → owner merges PR.
**Product decisions ✅ (in-lane, no tripwire):** D1 — exclude supplements from food cross-links STRUCTURALLY via
a `shelf` field (draw cards from same shelf only); reuses existing metadata, self-applies to creatine/future
shelves; supplements shelf = magnesium-only today → its page renders 0 cards / hides (must NOT fall back to food).
D2 — ship alphabetical + shelf-scope + a ~10-line "max 1 per `family`" cap (cheese family = cheese/brined/hard);
NO relevance graph (anti-overbuild). Follow-up flagged: /madrichim explore-next heading will need its own Content
gate when guides get the module.
**FULL FIX PACKAGE (defined, batched → Frontend Agent in ONE cycle):** (1) decouple module category from the table
prop [HIGH-1] (2) CTA לכל ההשוואות→להשוואה [content] (3) shelf-scoping + 0-card/hide on empty pool [Product D1]
(4) family de-dup cap [Product D2] (5) + Design findings once in.
**Design conformance ✅ CONFORMS:** 0 new WCAG fails, correct RTL, all tokens trace real (heading #4E5663=6.42:1,
CTA #167A58=5.30:1, accent used only as decorative underline), golden-page = "not drift" (follows SharePageButton
precedent, ruled explicitly). Non-blocking: (a) lazy-load images render blank in zero-scroll screenshots → force
scroll before refreshing test:visual baselines; (b) no :active/img-error fallback (minor). Confirmed the pre-existing
category-hero WCAG defect is LIVE + gate-red → TASK-510.
**CLOSED 2026-07-04** (registry `tasks/closed/TASK-507.md`): fix package landed + re-gated; orchestrator
independently confirmed 0 category-prop diff vs origin/master on all 4 formerly-wired files; suite green
(20/20 spec, 10/10 smoke, 0 new a11y). Branch `frontend/task507-explore-next` @ c67c5c7a pushed — **PR awaits
OWNER merge** (consumer-facing deploy, tripwire #2). Spin-offs: TASK-508/509/510.

## ✅ TASK-510 category-hero eyebrow contrast — CLOSED 2026-07-05 (tasks/closed/TASK-510.md)
category-hero.tsx:28 eyebrow → `text-[#176F53]` (6.113:1, was 2.981:1). Commit `2e216193` (worktree
`C:\bari_wt_t510`, `fix/task510-hero-contrast`). Verified: 1-line diff, mobile a11y 4/4 exit 0, tsc/lint 0,
C0 PASS. **Branch NOT pushed — queued for supervised morning.** Residual desktop a11y red = PRE-EXISTING
sibling defects (not introduced) → **TASK-512**.

## 🟡 TASK-512 residual WCAG a11y debt — frontend-agent, MEDIUM (2026-07-05)
Surfaced by TASK-510 (pre-existing on origin/master, confirmed by 510's 1-line diff). Carousel category chips
#1F8F6A/#E8F5EF 3.6:1 + rank number chips #7a817c 3.85-3.99:1 + 5 remaining `text-[#1F8F6A]/80` eyebrows
(hashvaot index:26, newsletter:27, demo:799+808, hashvaot-category-landing:35). Same darkening pattern; own PR.
Not yet dispatched (queued — bundle with TASK-494 blog-contrast morning kick).

## ✅ TASK-508 registry drift: snacks nameHe stale — CLOSED 2026-07-05 (tasks/closed/TASK-508.md)
snacks.ts:11 nameHe 'חטיפים מלוחים'→'חטיפי דגנים', commit `2c27c68c` (worktree `C:\bari_wt_t508`, branch
`fix/task508-registry-namehe` off origin/master). Audit: 7/7 registry categories checked, drift 1/7 (snacks
only), 0 remaining 'מלוחים'. C0 PASS; orchestrator eyeballed the 1-file/1-line diff. **Branch NOT pushed —
push+PR queued for supervised morning.**

## ✅ TASK-509 dormant nutrition-config on expansions — CLOSED 2026-07-05 (tasks/closed/TASK-509.md)
Nutrition verdict: **DEFAULT rendering is a latent display bug on all 4 pages, not intended.** Cheese protein
goodAbove=20 vs DEFAULT 8 (fresh cheese flips green→grey); crackers config absent; milk servingLabel wrong
("ל-100 גרם" for a per-100ml product) + unreachable via missing alias; all 4 pages pass `category=` 0×.
Orchestrator independently confirmed each claim at expansion-section.tsx. C0 PASS. Memo:
`03_operations/reports/nutrition/task509_expansion_config_recommendation_v1.md`.
→ **Implementation spun off as TASK-511 (BLOCKED).**

## 🟡 TASK-511 activate category expansion configs (bread/cheese/crackers/milk) — nutrition-agent, MEDIUM, BLOCKED
The TASK-509 fix: pass `category=` on each page + add `milk-comparison→milk` alias + author a NEW crackers
config. BLOCKED on Nutrition+Product D7 co-sign (new crackers thresholds) + Design render re-verify (milk bars
change substantially). Own PR, never piggybacked. Display-only, no published-score change.

## ✅ TASK-505 Agent OS upgrade (2026-07-04) — CLOSED (all 12 workstreams verified; tasks/closed/TASK-505.md)
Full implementation of the skills/agents audit (owner: "every single suggestion"). All 6 subagent
returns verified against artifacts; working-tree only, nothing committed (owner controls the commit).
Follow-ups routed in the task file: Design (72px-cap vs rowVerdict reality), Frontend (quarantine
violation + methodology color divergence + missing StickyFilterButton), QA (fixture library MISSING),
deps triage (hono/tmp high), owner unlocks (ANTHROPIC_API_KEY secret, GSC OAuth, pip-audit).
**Done inline:** 13 third_party skills un-nested to `.claude/skills/` (were UNDISCOVERABLE — nesting bug);
OFF-ban violations purged from nutrition/research/frontend agent files; frontend ScoreChip law fixed to
gradePalette; conformance milk carve-out retired; category-factory de-staled (red-team-agent → Adversarial
QA, stage order); QA pin sonnet→opus (per critic_lane_opus_and_c3); telemetry §8 skill-edit proposals;
loop-first autonomy codified (/orchestrate §Loop autonomy + CLAUDE.md, owner directive 2026-07-04);
hooks: `guard-off-ban.ps1` (tested: blocks OFF adds) + `guard-two-gate-commit.ps1` (tested: blocks
comparison-JSON commits without `tasks/signoffs/<json>.ok`); CI: `bari_page_gates.yml` (conformance +
OFF census) + `security_review.yml` (needs ANTHROPIC_API_KEY secret to activate).
**Dispatched (6 parallel subagents):** S1 marketing-agent v2 + `bari-seo` skill (+retire old seo-audit) ·
S2 bari-frontend-ui rewrite vs golden template · S3 bari-qa-audit refresh vs real gate scripts ·
S4 Hebrew copy eval harness (03_operations/evals/copy_evals) · S5 Design vision-in loop
(bari-web scripts/vision-in.mjs) · S6 deps/security maintenance lane (03_operations/maintenance + /deps skill).
**Note:** two-gate hook will require sign-off markers for the 4 currently-modified comparison JSONs
(cookies_coffee/hard_cheeses/juices/milk) at their next commit — intended behavior under the descriptions freeze.

## ✅ Recently shipped (live on origin/master)
- **TASK-492A — seed-oils evidence blog** `/blog/seed-oils` (PR #83, f/live-verified). Revised: recharts
  cookies chart + claims-vs-evidence table. Two-gate; gate-2 caught+fixed 2 CRITICALs (RT-1 seed-oil-penalty
  overclaim vs co-sign §2; RT-2 brand typo). CLOSED.
- **TASK-499 — SEO crawl-hygiene** (PR #84). Sitemap adds /nagisut,/cookies,/disclaimer + false-noindex
  comments fixed on 5 legal pages; internal-linking audited (17 /hashvaot pages already reachable). CLOSED.
- **Cycle 1–6 batch (2026-07-03), all merged:** consumer #67 crackers · #69 carbs/satFat honesty · #70
  cookies+granola · #72 milk phrasing · #76 hard_cheeses brands; copy overhaul #44/#51/#53 (14 comparison
  pages); mascots #54; footer community band #52; protein-bars rescore #66; internal #62/#73/#74/#75/#77/#78;
  analytics #82. No wrong published scores found in the 6-page red-team backfill. Detail in the archive.

## 🟢 TASK-515 (+515A) YOGURT — TWO comparison pages off ONE scrape (owner 2026-07-05) — Stage 0 RUNNING
Owner redirect off TASK-504A: cottage IS in-corpus but skyr/Greek/protein-yogurt are NOT → build a real **yogurt**
category (the honest high-protein-dairy surface). **Scope expanded (owner, same day): TWO pages off one BSIP0 scrape
for efficiency —** TASK-515 **spoonable yogurt** + **TASK-515A yogurt DRINKS** (drinkable/beverage). Shared Stage 0;
pipeline forks at corpus-filter into two subpools → two configs → two copies → two gates → two red-teams. Unblocks 504A.
**Pipeline (sequential, /build-page skill):** 0 BSIP0 (shared) → 1 BSIP1 → 2 BSIP2 → 3 generate_page → 4 two-gate copy →
5 D4 → 6 FAQ → 7 validate_comparison_page → 8 render → 9 red-team (≤3 rounds). Each page go-live = tripwire 2 (owner merge).
**Stage 0 DISPATCHED** → Data Agent (a8613a8…): **≥3 retailers HARD (owner: not Shufersal-only)** —
Shufersal/Victory/Yochananof/Rami-Levy, cross-check nutrition, document blocked, per-100(g/ml) plausibility gate,
OFF-banned, discard rule, validator 6/6. **Tag each SKU by subpool (spoonable vs drinkable); report counts separately.**
Boundary flags (kefir/labneh/cottage-dedup) → Nutrition/Product ruling at corpus filter, informed by real Stage-0 counts.
**Stage 0 PARTIAL (a8613a8 resumed):** Shufersal 129 (106 spoonable/23 drinkable) · Yohananof 8 (thin — verifying real
vs scraper gap; replaced a prior OFF-paneled scraper = OFF caught) · Victory in-progress (Cloudflare bot-wall, headed
Playwright works, slow) · Rami-Levy blocked (documented). **≥3 HINGES ON VICTORY** (only 2 fully done; if Victory
fails → ≥3-not-met = owner blocker to surface). Labneh keyword-collision (לבנה vs לאבנה) caught+fixed. Every SKU tagged
subpool + kefir/labneh edge flag. **Plausibility → Nutrition ✅ RULED (a1a40b1, verified):** cheese DAIRY_SOLID (20g) false-rejects yogurt (authoritative
gate passed only 45/147). Ruling (doc `01_framework/governance/yogurt_plausibility_floor_ruling_v1.json`, grounded in
live USDA FDC + Codex STAN 243): TWO new additive FoodClasses — **DAIRY_SEMISOLID** (spoonable, floor 8.0g, kcal 30–250)
+ **DAIRY_CULTURED_DRINK** (drinkable, floor 4.0g, kcal 20–150); **labneh→existing DAIRY_SOLID** (cheese); discard
<5.0/<2.0g. Orchestrator-verified: ruling artifact exists + `plausibility_gate.py` byte-untouched by Nutrition (clean
lane discipline). **Stage 0 FINALIZED (verified) — ⚠️ ≥3 NOT MET (2/3):** Shufersal 119 + Yohananof 7 = **126 survivors (103 spoonable/
23 drinkable)**. Victory FAILED (0/15 — candidate discovery grabbed cloudfront BANNER images not the product grid;
35-min box). Rami-Levy blocked (Nuxt shell, feed DNS-dead; re-probe doc'd). Gate patch orchestrator-VERIFIED cheese-safe
(DAIRY_SOLID floor 20.0 + kcal (40,450) byte-intact; 2 new classes 8.0/4.0 added). Corpus artifact = 126 confirmed.
Validator exit 1 (WARN: Victory HEAD false-neg + product-identity recheck deferred). Cross-check: 6 multi-source SKUs,
**4 disagree >15%** incl. a systematic **Yohananof sugar low-read** (3 SKUs) = suspected parser bug. Kefir: 0 real
products survived (only a DIY starter) → kefir ruling has no data. 3 low-fat (5%) labneh newly fail (routed to cheese
floor 20g) → open Nutrition Q.
**REMEDIATION RETURNED (verified) — 🔴 WALL: ≥3 STILL NOT MET, Victory diagnosed INTRACTABLE.** 3 architecturally
distinct rebuilds all dead-ended (promo-carousel not search; search autocomplete never activates; product grids render
empty even on a milk-category CONTROL — site-wide, not yogurt). Rami-Levy blocked. So only 2 of the canonical 4 retailers
are reachable. **WIN:** Yohananof sugar-parser bug FOUND+FIXED (teaspoon-of-sugar row bled into grams field via naive
"sugar" substring; verified vs live pages, 1 corrected + 3 →honest-NULL) → cross-check disagreements 4→2. Tree-safe
(only bsip0_nutrition.py + plausibility_gate.py + 3 new scraper files; bsip2 mods = pre-existing ambient, NOT this agent;
no scoring touched — orchestrator-verified). Corpus 126 (121 Shufersal/5 Yohananof). Validator exit 1 (WARN).
**→ OWNER OVERRIDE 2026-07-05 (supersedes park + the ≥3 rule):** "ignore [the scraper fix]... build the pages with the
data you obtained." **≥3 WAIVED for this build** — proceed on 2 sources (Shufersal 119 + Yohananof) / 126-survivor
corpus. Scraper-fix prompt preserved at `tasks/prompts/yogurt_bsip0_scraper_fix_PROMPT.md` for a future ≥3 pass.
TASK-515 + 515A UN-PARKED → IN_PROGRESS. **Pipeline RESUMED at Stage 1.**
**Reversible scope defaults (logged):** labneh (4) EXCLUDED (Nutrition = cheese/DAIRY_SOLID); kefir moot (0); cottage
excluded if present (scored elsewhere). Two pages by subpool: 515 spoonable (~103) / 515A drinkable (~23).
**Stage 1 BSIP1 ✅ DONE + orchestrator-VERIFIED (a027001):** 122 enriched (126 − 4 labneh; cottage/kefir confirmed 0),
**99 spoonable / 23 drinkable**, reused shared `ingredient_enricher` (uniform-baseline). Coverage: name 122/122, ingredients
119/122 (3 nulled = marketing-copy-as-ingredients, discard-rule good), core-nutrition 122/122, images 117/122. 122 files
confirmed on disk. NOVA assigned DESCRIPTIVE-only (must not enter scoring w/o co-sign). Artifacts under
`02_products/yogurt_system/bsip1_task515/`.
**Stage 2 methodology ✅ RULED (Nutrition a38d246):** **TWO separate shelf-relative pools** (spoonable 99 ≠ drinkable 23;
precedent = EV-089 vs EV-090 cheese subpools in dairy_protein) · all 122 → existing `dairy_protein` (no new category) ·
same dimension set both pools · per-100g uniform (matches milk) · NOVA descriptive-only. Mechanism NOT new (no D7 for the
mapping) BUT new shelf-rel CONSTANTS need EV-### + D6/D7 co-sign BEFORE go-live. Flags: old EV-088 sugar constants STALE
(recompute from new corpus); n=23 drinkable may fail the low-variance guard → flag not force.
**Stage 2 BSIP2 ✅ RAN + VERIFIED (ac25f4f):** 99+23 scored through the UNCHANGED engine (score_engine + constants
0-diff = tripwire-1 safe; router_v2/input_loader diffs are pre-existing ambient). Spoonable grades A10/B41/C24/D22/S2;
drinkable B5/C13/D4/E1. Spoonable sugar shelf-rel PASS (median 4.7, scale 4.6); **drinkable variance guard FAILED as
predicted (scale 1.63 < 3.0, n=23) → sugar shelf-stat left UNSET (not forced), absolute floor active.** Fermentation 0
genuine misfires. EV-105 constants = proposal only.
**Router gap → FIXED + re-scored v2 ✅ VERIFIED (Data a814ce9):** root cause = classify_category short-circuits Stage-1
anchor before Stage-5 overrides. 18 in-scope cultured brands re-routed (Actimel/Activia/Danone/Yoplait/Müller Active) via
additive barcode-overrides + 3 Stage-1 anchors; 2 soy DISCARDED; ambient router diff untouched. **TRIPWIRE-1 PROOF: 213/213
live-corpus products unchanged (0 reroute, 0 collision), score_engine+constants 0-diff** (orchestrator-confirmed). v2:
120 scored, dairy_protein 117/120. **Spoonable n=96** (A11/B39/C23/D20/S3, median 67.6) — CLEAN. **Drinkable n=24**
(B5/C14/D5, median 57.35).
**Nutrition cluster ✅ RULED (ac10c29) — path CLEARED, NO owner escalation:** (1) drinkable sugar absolute-basis is
HONEST (yogurts cluster ~5g → shelf-rel would manufacture false differentiation, "clustering is honest") → ship w/ a
yellow caveat box (Nutrition D13-authored Hebrew copy). (2) **R7 fermentation "misfire" = FALSE ALARM in the AUDIT
SCRIPT, not an engine bug** — all 19 trace to correct pre-existing behavior (Path-A already credited / flavor-excluded /
NOVA-4 gated); NO engine change, NO tripwire. (3) EXCLUDE tzatziki (no culture) + 2 chocolate-yogurts (scored under
confectionery lens per Rule 3) from display → **shipping pools spoonable 94 / drinkable 23**; Rule-3-narrowing → Product
D7 (non-blocking). (4) EV-105v2 spoonable **D6-APPROVED** (median 4.85/IQR 4.6/n82); drinkable stays unset. Condition:
recompute on the 94/23 shipping pools.
**Stage 2 FINAL rescore ✅ DONE + VERIFIED (Data a534adc):** shipping corpus **94 spoonable / 23 drinkable** (117; 2 soy +
3 Nutrition-excluded), router 117/117 clean, trace dirs 94+23 on disk, engine/constants/router 0-diff (tripwire-safe).
EV-105v2-FINAL: spoonable median 4.65/IQR 4.6/n80 guard PASS (D6-approved); drinkable guard FAIL → sugar unset (honest).
Grades: spoonable A11/B38/C23/D20/S2 (median 66.4); drinkable B5/C13/D5 (median 57.7). Drinkable-caveat noted for Content.
Traces at `02_products/yogurt_system/bsip2_task515_v3/`. **SCORING PHASE COMPLETE.**
**Product D7 ✅ CO-SIGNED (ab6fd95, premise-checked):** spoonable approved outright; drinkable unset/absolute-floor
approved, CONDITIONED on the D13 sugar-caveat box shipping (go-live gate); Rule-3-narrowing = don't pursue now (2-SKU
gain vs TASK-394's 16-shelf/572-product cost — future backlog); two-page split confirmed (n=23 within live precedent
juices17/milk18/cereals20/snacks21/bread23). **SCORING+GOVERNANCE PHASE COMPLETE, both pages D6+D7 co-signed, 0 owner
escalation, 0 engine bleed.**
**D8-persist + generate ×2 ✅ DONE + VERIFIED (Data a0c9e4d):** co-signed SUGAR_SHELF_REL_YOGURT_SPOONABLE persisted to
constants.py (36 ins / **0 del**; grep proves unused by score_engine → can't move scores; regression 11 PASS/1 pre-existing
WARN unchanged — tripwire-1 SAFE) + EV-105v2 registry entry. Configs `page_generator/configs/yogurt_{spoonable,drinkable}.json`.
**Two frontend JSONs generated** at `02_products/yogurt_system/bsip2_task515_v3/frontend_out/`: **yogurt_spoonable_frontend_v1.json
(94/94)** + **yogurt_drinkable_frontend_v1.json (23/23)** — every copy field PENDING_COPY, OFF=0/0, count 94+23=117.
Drinkable self-gate 8/8 PASS; spoonable G1-G6 PASS + **G8 FAIL on 1 product** (barcode 7290116936581, nutrition text bled
into ingredients — pre-existing BSIP1 scrape defect → BSIP1 re-parse or exclude before its copy). Images: spoonable 90/94
(4 missing → "data could not be retrieved" / self-host follow-up), drinkable 23/23. Not committed.

### ⏸️ CHECKPOINT — DATA/SCORING/GENERATION PHASE COMPLETE; COPY+RENDER phase = fresh session (CLAUDE.md "fresh chat per phase")
Both yogurt pages exist as fully-scored, co-signed, tripwire-safe frontend JSON with placeholder copy. **RESUME (via /roadmap):**
(1) fix/exclude the G8 spoonable product 7290116936581 + acquire the 4 self-hosted images; (2) **TWO-GATE COPY ×2** — Content
authors Hebrew (insightLine/rowVerdict/consumerTakeaway/expansion + hero/prologue/category-notes) → Adversarial QA gate; the
**drinkable page MUST carry the D13 sugar-caveat box** (Product go-live condition); (3) D4 additive wiring; (4) FAQ schema ×2;
(5) `validate_comparison_page.py` ×2 (hard battery); (6) render locally + (7) terminal red-team (≤3 rounds); (8) OWNER merge ×2
(tripwire 2). Backlog (non-blocking): Rule-3-narrowing future task; drinkable-caveat copy already D13-approved (attach at build).
**LOOP CONTINUES → next ROAD move = TASK-504 Wave 1 (magnesium guide).** Board line "Wave 1 starting — author copy" is
STALE: content/tier/slot copy + QA red-team + Product tier + Design specs already exist as artifacts. **Recon DISPATCHED**
→ Explore (a4c2c21, read-only): reconcile true state (authored? both gates signed? EFSA-2021 fabrication purged?
bisglycinate hedged? integrated into /madrichim/magnesium or copy-in-reports-only?) → real next action, no re-authoring.
**Deferred to corpus-filter (needs final ≥3 corpus):** kefir (needs a dedicated query pass — 0 data now) + labneh
disposition + cottage-dedup + drinkable-n viability → Product ruling.

## ✅ TASK-518 BSIP0 retailer fleet — CLOSED 2026-07-05 (tasks/closed/TASK-518.md): FLEET = 4 READY
**Owner final fleet: Shufersal · Hazi Hinam · Yohananof · Tiv Taam (owner re-added Tiv Taam as the 4th;
"4 is enough for now").** All 4 verified by butter smoke probes; Yohananof + Tiv Taam RE-PROBED FRESH by the
orchestrator on owner request (other chats' agents struggled to reach them): Tiv Taam 30 disc/25 scraped/
23-25 parse/22-25 gate (identical to prior run); Yohananof 19 disc/16 scraped/16-16 parse (its raw 4/16 gate
= probe-harness FoodClass artifact — butter passed as `dairy_solid` w/ 450-kcal cheese cap vs real butter
~730-750 kcal; parses correct; pass the right class per category in real runs). **Reach guidance for other
agents: do NOT raw-HTTP these sites — yochananof = Cloudflare false-DOWN; use the engines
`yohananof/acquire_yohananof.py` · `tiv_taam/acquire_tivtaam.py` · `hazi_hinam/acquire_hazi_hinam.py`.**
Set aside/blocked (documented in the closed task): Victory+Carrefour (self-point WAF; Tiv-Taam-proven API
pattern = future retry), Super Yuda (Radware edge ACL; owner-browser test = future option), Rami-Levy (HAR),
Osher Ad (no online store). Wolt/Yango rejected (aggregator provenance / market exit); Super-Pharm reserved
as supplements-only source. All engines/probes uncommitted under `03_operations/bsip0/scrape/`. Prior-return detail:

### (superseded target detail) 4/5-6 READY, was BLOCKED on WAF cool-down (2026-07-05, orchestrator-verified)
Owner: "I want 5-6 retailers BSIP0 ready, right now there's only 1 essentially." Infrastructure ONLY — no
category builds (TASK-515/515A untouched). **P518 returned; orchestrator verified every claim against the raw
probe JSONs (recounts match exactly), OFF census 0 on all new engines, `_shared/` yogurt gate/parser fixes
preserved, scope confined to `03_operations/bsip0/scrape/`.** READY = **Shufersal** (22/22 butter probe) ·
**Yohananof FIXED** (root cause: EAN discovery regex `_(\d{13})_` needed underscores BOTH sides → dropped
702/900 candidates; now lookaround; new `yohananof/acquire_yohananof.py`) · **Hazi Hinam NEW** (clean JSON API,
no WAF; 27/28) · **Tiv Taam NEW** (self-point `v2/retailers` API, WAF-free copy, inline per-100g nutrition;
25/30). BLOCKED: **Victory + Carrefour** — hard self-point.com WAF block (rate-limit tripped mid-session);
next = retry the Tiv-Taam-proven API pattern from a fresh session/IP after cool-down. **Rami-Levy** — needs
real HAR capture (re-probe doc'd). **Osher Ad NOT VIABLE** (no online store — drop from candidates).
All uncommitted (3 engines + `_smoke_probes/`). Registry: TASK-518 BLOCKED w/ resume condition.

## ✅ TASK-504 supplements re-direction — CLOSED 2026-07-05 (owner "close this project")
Both guides BUILT + Adversarial QA gate-2 GO (local, noindex), committed 8277450c on
`feat/task504-guides-template` @ worktree `C:\bari_wt_t504` (NOT pushed). Final model = A/B/C/D BANDS
(owner "revert to ABCD, bands not per-product") + GATE-EXCL-1 / split_v2 (dual-keyed, in
`supplement_guides_bar_rubric_v1.yaml`). Creatine 26-in-Israel (12 shelf + 14 import) + 13 benchmark →
A:0/B:13/C:8/D:3/CA:2; magnesium relabeled 2/3/12/1. PARKED for owner's future public flip: migration PR
(301s /hashvaot→/madrichim + sitemap = deploy tripwire), per-product real descriptions (freeze) + full
creatine gate-2, minor residuals. Full record: memory `supplements-guides-redirection`; `tasks/closed/TASK-504.md`.
(TASK-504A dairy pilot is SEPARATE, still open.)

<!-- superseded history (archived) -->
## 🟢 TASK-504 supplements re-direction — OWNER APPROVED → EXECUTING (Wave 0 done, Wave 1 starting)
- Plan (approved contract): `01_framework/product/supplement_guides_concrete_plan_v1.md`. Naming: **מדריכים**
  hub + "איך לבחור X" pages. Magnesium numeric score/rank come DOWN; form-tiers+UL flags survive as bar-states.
- **Wave 0 COMPLETE:** Nutrition rubric `supplement_guides_bar_rubric_v1.yaml` (6 bars, deterministic, 49/49
  classify, anti-drift no-composite) · Research magnesium-citation verify (bisglycinate NOT co-equal w/ citrate,
  hedged; UL 350/250 ok; **live "EFSA 2021" ×4 fabrication → must-fix in guide, not carried**) · Frontend
  template spike (commit 35545218, worktree t504: typed contract, 4-state bar primitive, /madrichim scaffold,
  buy-button data-separated, migration-TODO).
- **Product D7 co-sign GRANTED + empty-shortlist RESOLVED (no owner escalation — 0 tripwires):** validation
  found **0 Israeli products clear all 6 bars** → when clears-all empty, guide leads honest headline + promotes
  existing `passes_with_flag` bucket as practical shortlist (magnesium 5/18, creatine-IL 11/18); default-pick
  = one per currency pool (magnesium+creatine-IL none today; creatine-WW = BPN labeled worldwide-reference-pick);
  FAIL→fails-before-cannot-assess confirmed; nano-liposomal claims OUT of v1; 3 data/copy corrections mandatory.
  D7 pending Nutrition final ack of conditions (folds at Wave-1 gate). Owner FYI given: magnesium headline will
  be "no IL product clears every bar — closest + what's missing."
- **Wave 1 (magnesium guide) — RECONCILED 2026-07-05 (Explore a4c2c21); board line was STALE.** Copy is AUTHORED +
  INTEGRATED into a built noindex `/madrichim/magnesium` page on worktree `bari_wt_t504` (branch feat/task504-guides-
  template; NOT on master). Wave-0 must-fixes VERIFIED clean in copy: EFSA-2021 fabrication purged (2001/2015 only),
  bisglycinate hedged, no "דירוג". Gate status SPLIT: slot copy ✅ both gates (QA GO); tier copy = Content-only, QA
  verdict of record **NO-GO** (RT-8, fixed-in-copy-not-re-gated); full-body copy = **no gate-2 at all**.
  **🔴 GLITCH (raised) — uncommitted WIP reintroduces BANNED forms off-contract:** "קבוצה A/B/C/D" grade-letter bands
  (guide-band-letter.tsx) + within-tier derived sort (guide-product-table.tsx:81-85) violate plan:74-75 + Product §7
  (:219-222); data file falsely claims "both gates passed" on NO-GO tier copy. No exception, no two-gate.
  **→ Product ✅ RULED (a) REVERT (aee1565, all 8 files premise-checked):** A–D bands violate TWO separately-adjudicated
  bans (grade-letter form + within-tier derived sort), no exception, no stated user problem → in-lane enforcement, NO
  tripwire, NO owner escalation for the design. False "both gates passed" = separate data-integrity defect, correct
  regardless. **Frontend revert DONE + orchestrator-VERIFIED (a383359):** deleted guide-band-letter.tsx + band mapping
  (guide.ts:407-412) + table band render + within-tier sort (recommendedBandSortKey) → restore 4 named tiers unordered;
  grep-verified 0 banned patterns; 4 named tiers restored unordered; tsc/lint/next-build green (267pp); 3 false comments
  corrected (RESIDUAL 533/537 tier Slot 3/4 still "FINAL COPY" → folded into QA). noindex stays; no commit.
  **QA content gate-2 ✅ RETURNED (acba292, instrument-backed is_clean over 64 strings):** tier copy v3 = **GO** (RT-8
  RESOLVED, 11/11 clean) · full-body = **NO-GO**, sole blocker **RT-9** = 3 strings fail is_clean on substring "מומלץ"
  (recommendation detector over-firing on legit "the recommended upper limit"/"recommended for attention"; same false-
  pos class as RT-5). Wave-0 fixes all PASS (no EFSA-2021, bisglycinate hedged, no grade-letters). 7 comments to correct.
  +**RT-12** (MEDIUM, nutrition): rubric `safety` boundary off-by-one at 250mg. **Fix = REWORD not weaken-gate.**
  **Content reword ✅ DONE + orchestrator-VERIFIED (a82926):** 3 strings reworded ("המצריך תשומת לב"/"הסף העליון
  שנקבע"), "מומלץ" gone from all body/spine consumer strings (grep-confirmed; only L530 comment + sanctioned tier
  label remain), 350/250 + IOM/EFSA-2001/2015 preserved → RT-9 RESOLVED (is_clean 3/3). 8 comments corrected + header
  kept honest (not-launch-ready). TWO 2ndary items surfaced → QA reconfirm (acba292 resumed): (i) authoritative is_clean
  re-run; (ii) grammar-gate is_clean=False on "המכון הלאומי לבריאות האמריקאי" (594/621) — pre-existing medium-conf
  noun_adj_gender_mismatch, likely DictaBERT false-pos; rule if it reds the go-live battery → reword vs exempt; (iii)
  persist a real gate-2 GO record.
  **QA reconfirm ✅ DONE (acba292, verified) — CONTENT TWO-GATE CLEARED:** body GO + tier GO; RT-9 3/3 is_clean; grammar
  flag ruled a DictaBERT FALSE-POS NOT in the go-live battery (run_gates.py + validate_comparison_page.py have 0
  grammar refs → cannot red go-live), ship as-is. Gate-2 record persisted `03_operations/reports/qa/
  magnesium_guide_content_gate2_v1.md`. **C3 dose_adequacy (P508, Jul-4) = AFFIRM** w/ guardrail: dose-only מומלץ rows
  must keep the under-dose caveat visible (Frontend to honor).
  **⏸️ CHECKPOINT — content/gating PHASE COMPLETE; finalization phase = fresh session (per CLAUDE.md "fresh chat per
  phase").** REMAINING to owner-ready (ordered): (1) Frontend cleanup batch — repoint 6 gate-status comments to the
  persisted gate-2 record + fix stale "body[3] UNCHANGED" comment (RT-10/11) + honor P508 מומלץ-caveat guardrail;
  (2) Product D7 rubric finalize (rubric still PROPOSED) INCL the RT-12 2-line operator fix; (3) Nutrition D7
  display_suppression_rule co-sign ("not obtained"); (4) Design vision-critic on the built page; (5) C0 build + sitemap;
  (6) commit worktree bari_wt_t504; (7) OWNER index/robots flip = tripwire 2. Resume via /roadmap.
  **Nutrition RT-12 ✅ RULED (ab9a273):** 250mg = FLAG correct (matches shipped HRT-3 D7 2026-06-23, live in
  magnesium-page-data.ts); rubric TEXT off-by-one only → fix `supplement_guides_bar_rubric_v1.yaml:349-350` to
  PASS "< 250" / FLAG ">= 250 to <= 350". ZERO data/copy/score effect (2 products stay FLAG). Rubric still PROPOSED
  pending Product D7 → **RT-12 2-line fix FOLDED into the D7 rubric finalization** (no standalone dispatch).
  After Content: I re-run is_clean + QA reconfirm 3 reworded strings → body GO → then C3 dose_adequacy + Product/Nutrition
  D7 (rubric finalize incl RT-12) + suppression_rule → commit + Design vision-critic + C0 → owner index-flip (tripwire 2).
  **Ordered path to owner-ready:** revert → QA v3 re-gate tier copy (close RT-8 NO-GO) + gate-2 the full-body copy →
  C3 dose_adequacy_sole_caveat + Nutrition D7 display_suppression_rule → commit + Design vision-critic + C0 → owner
  index-flip (consumer deploy = tripwire 2). Then Wave 2 creatine, Wave 3 hub+migration PR.

## 🟢 TASK-504A — GLP-1 / suppressed-appetite DAIRY guide (מדריך pilot) — owner GO 2026-07-05, EXECUTING
Assessment (Research+Product parallel) → owner approved the **guide angle, not a badge**. One /madrichim page
reusing LIVE `milk_and_alternatives` scores through a protein-density + nutrient-density-per-calorie lens for
suppressed-appetite eating (GLP-1 mainstreaming: Wegovy in IL 2026 basket for teens 12–18; 100k+ Maccabi on GLP-1
'25). **Hard constraints:** NO "GLP-1 friendly" badge, NO drug named as a product qualifier, NO scoring change
(guardrails_v2 Lens 2 + Anti-Immunity Rule). Science anchor = lean-mass loss 25–39% of weight lost → protein
≥1.2 g/kg confident; nausea/fiber/hydration = hedge/omit (Insufficient tier).
**Nutrition GATE ✅ RETURNED — pilot LIVES, reshaped (safety valve fired):** `satiety_support` bar DROPPED
(admittedly-gameable proxy, can't be honestly caveated for a "help me eat on suppressed appetite" page). **3 honest
bars, fields traced to score_engine.py:** protein density from RAW `protein_g`÷`energy_kcal` (NOT the nutrient_density
dimension score — calibrated for cross-cat ranking, misrepresents milk at 3.4g→~23/100) · added sugar via
`added_sugar_sources_count` (NOT sugars_g/lactose) · sodium (bands provisional, pending full-corpus stats). Spine
tier-gated: STRONG lean-mass/protein (PMID 41877354/42036071/40445127) but NEVER per-product "prevents muscle loss";
fiber/nausea/hydration OMITTED not hedged (teen-12–18 audience → implied-medical-advice risk). Do NOT build a protein-
QUALITY bar from the DIAAS factor (frozen-invariant tripwire).
**Data Agent ✅ RETURNED** — 18-product live shelf dataset at `02_products/milk_and_alternatives/guides/
task504a_dairy_satiety_shortlist_v1.json` (sha 8fc488e1…), per-100ml basis asserted, score/grade byte-checked 18/18,
satiety dropped, raw protein_g+energy_kcal+added_sugar_sources_count exposed, sodium NULL on 2/18 (kept null, no OFF).
**SCOPE FORK → Product ✅ RULED (c, corrected) — caught an orchestrator premise error:** my brief claimed "~nothing
clears pass"; Product recomputed per-product from the artifact → **5/18 (28%) clear ≥6 g protein/100kcal** (whole milk
=4.93, not ~5.5). Real cluster = 2 fortified cow's milks (יטבתה 1% 7.91, טרה lactose-free 10.16) + 3 unsweetened soy
(Tnuva Alt ×2 10.31, Alpro 7.17). **Ruling: build on the 5-tier, NO new scrape, but RENAME "dairy"→"milk & plant-milk
protein density"** (3 of 5 winners are soy — a "dairy" title misdescribes its own evidence).
**Gating pre-checks before Content drafts:** Nutrition (a1c5cc4…) ✅ RULED **(b) mix dairy+soy OK but guide MUST carry a
protein-QUALITY caveat** — density is honest, but the lean-mass claim runs on leucine; dairy leucine-richer per g
(~9.5–11% vs soy 7.5–8%; DIAAS ~1.0–1.45 vs 0.84–0.98) → dairy edges ahead on muscle-signaling, soy stays (good, not
poor). Precision: don't imply plant milks broadly shine — only soy passes; almond/oat/rice = low tail. No score/co-sign.
· Adversarial QA (abbd12f…) ✅ **FAIL as claim base — 3 CRITICALs, structural (not copy):** RT-1 the protein-per-kcal
bar is really a LOW-CALORIE filter — goat + whole milk (A/85, 3.4g protein) shown as losers while a D-grade sweetened
soy drink "wins" on identical protein, differing only by fat; RT-2 GLP-1/medication frame over-claims authority a
milk-drink shelf can't carry (the actual high-protein dairy — skyr/cottage/quark/Greek — is NOT scored) = owner
tripwire if drug-frame kept; RT-3 orchestrator shorthand errors caught (Alpro barista NOT "unsweetened" = added sugar;
יטבתה NOT "protein-fortified" = ordinary 3.4g milk protein, passes only on low fat). +RT-4/5/6 HIGH.
**PILOT BLOCKED on owner strategic call (2026-07-05):** milk-shelf GLP-1 guide can't ship honestly; honest version needs
a high-protein-dairy corpus we don't have (= new program, tripwire 3) + medication frame (tripwire 2). Orchestrator rec =
SHELVE + bank the assessment, revisit with a proper skyr/cottage/Greek corpus when prioritized; do NOT ship milk compromise.
Content never dispatched (held throughout). Escalated to owner as ONE digest w/ recommendation.
**Spin-off:** TASK-513 (literature.py wrong-DOI citation-integrity bug, owner data-agent, HIGH) — surfaced by the
assessment's Research lane; threatens C0 citation gate. **DISPATCHED 2026-07-05** → P513.
C1-CURSOR REFUSED (dirty tree wipe hazard) → rerouted C1-Sonnet shared-tree scoped touch-only.
**✅ CLOSED 2026-07-05 (tasks/closed/TASK-513.md)** — orchestrator-verified: root cause = recursive `.//ArticleIdList`
descending into ReferenceList (last-match-wins → cited paper's DOI); fix = `_article_doi()` direct-child parse
(literature.py:84/91, never ReferenceList). Ran pytest MYSELF → 6/6 PASS; `git diff --stat` scope clean (literature.py
28+/4− + 2 new test files, nothing else, uncommitted). Local only — push batched with supervised morning (like 508/510).

## ⏸️ PARKED on owner stop (creatine thread — nothing pushed/merged, live site unchanged)
- **TASK-492B blog** `/blog/functional-dairy`: gate-1 authored+committed `68381ebb` (worktree t492b); gate-2
  red-team was killed mid-run on the stop. Substance likely survives the pivot (it's a dose-honesty blog, not
  a comparison) but re-gate + re-frame check AFTER TASK-504 settles (it links /hashvaot/creatine).
- **TASK-503 hub card**: built+committed `6b936782` (worktree t503), gate returned **NO-GO** (RT-1 CRITICAL:
  card blurb lacked Content-Agent sign-off — one-signature ship attempt; +2 HIGH: count-scope coincidence in
  card stats, missing theme photo). MOOT in current form anyway — the supplements hub card concept is
  superseded by the guides hub. Fold findings into the TASK-504 build.
- **/hashvaot/creatine + /hashvaot/magnesium stay live as-is** until the guides migration plan lands (no
  interim changes).

## ✅ Also shipped this session
- **TASK-492C — creatine comparison page `/hashvaot/creatine` LIVE** (PR #86 → d9005328, owner-merged +
  live-verified: 18 IL + 13 worldwide, grade-free, "5 מדינות" correct). Full evidence pipeline + two-gate;
  red-team caught+fixed RT-1 CRITICAL (cert count) + region-count nit, all re-verified. CLOSED.
- **TASK-502 — UPF evidence blog** (Hebrew explainer, Lancet Nov-2025 3-paper series). Angle locked:
  *UPF alarm real but NOVA category is blunt → Bari scores mechanism (additive/fat/process), not the label.*
  HARD: attribute all advocacy/medical/policy claims (never assert "cigarettes=UPF" equivalence); C0
  `verify_citations.py`; full two-gate (Content + Adversarial QA/Red-Team). **BOTH content gates GREEN:**
  Nutrition verified 4/4 citations (Lancet ×3 + Milbank, real PMIDs) + locked positioning (red-label overclaim
  caught → omitted; angle carried by emulsifier+fat-tech which ARE live). Content draft v2 (Marketing lane);
  red-team v1 NO_GO → fixed → v2 **GO**. Owner approved copy + 4 infographics. Frontend build → Design critic
  PASS_WITH_FINDINGS (fixed) + LUMO hero → QA render-gate GO_WITH_FINDINGS → microcopy two-gated.
  **CLOSED 2026-07-04, owner-merged: `/blog/ultra-processed-food` LIVE on origin/master** (feat/task502-upf-blog,
  a488ebeb + 0c88cc9e; registry `tasks/closed/TASK-502.md`).

## 🟠 Ready / queued
- **TASK-492B — creatine/functional-dairy blog.** Framework ruling done (`functional_dose_ingredient_ruling_v1`);
  scrape shows on-shelf dairy creatine = Yoplait GO (2 SKUs, **both undisclosed dose**; Tnuva GO = collagen,
  not creatine). Honest blog story ready to author (undisclosed-dose = can't verify a meaningful dose) → two-gate.
- **TASK-494 — blog-template WCAG-AA contrast — ✅ CLOSED 2026-07-05** (tasks/closed/TASK-494.md). Colors
  #7A817C→#5C635E (6.17:1), #7A9450→#4A5E26 (7.19:1) + blog-tokens.ts. One CHANGES_REQUESTED round: orchestrator
  caught a UTF-8 BOM on all 46 files (Next.js "use client" risk) → fix commit `e4434a0b` re-saved UTF-8-no-BOM.
  Verified: C0 PASS, 0/46 BOM, 0 old hexes, all 47 files blog-scoped, tsc/lint 0. NOT pushed — queued for morning.
- **TASK-495 — EV-017 flag-vs-score review — ✅ CLOSED 2026-07-05** (tasks/closed/TASK-495.md). PROPOSE-only:
  KEEP should_affect_score_now=false. DOI dep verified (PMID 42347889, 21 RCTs, 0 retractions); meta is
  CLASS-level + tier-silent → can't license the sucralose/saccharin-vs-stevia tier move; class-scoring would
  wrongly penalize stevia/monk-fruit. No tripwire (status quo). Follow-up: retire stale grounds-language →
  **TASK-514** (Nutrition lane, no D7, no score).
- **TASK-501 — cookies 117-vs-119 live count** (BLOCKED/surfaced): page_copy says 119/E:83, product array is
  117/E:81; live /hashvaot/cookies-coffee renders stale count (blog's 117 is correct). Needs clean worktree
  (main-tree copy has unrelated drift) + own gate + owner merge.
- **TASK-500 — batch-rescore robustness — ✅ CLOSED 2026-07-05** (tasks/closed/TASK-500.md). Per-shelf
  subprocess isolation (new `_score_shelf_worker.py`); commit `83f12228` (worktree `C:\bari_wt_t500`).
  Verified neutral: C0 PASS, diff = 2 harness .py only (no scoring-logic change), worker uses real
  score_engine → batch==isolated by construction, sentinel 5718038 back to 22.0/E, worktree clean of JSON.
  **NOT pushed — internal-fix merge queued for supervised morning.**
- **Sitemap-completeness micro-pass:** several live blog routes absent from ALL_INDEXABLE_PATHS (/blog/seed-oils,
  hummus, lechem, bread-everyday|standouts|wellness-gap, yogurt). In 499's spirit; own small audit.

## 🔴 Held for owner
- **TASK-473 — 10 FB/IG social posts** (Marketing Agent) + **Item 8 marketing week-1** (owner's hands: group
  recon, admin DMs, WhatsApp Channel, finding-posts, $150 search). Checklist delivered
  (`tasks/reports/marketing_week1_launch_checklist.md`).
- **Hummus brand name-token extraction** — source-empty; orch rec = don't invent. bread/crackers brands stay
  honest-null.
- **Gen-Z homepage redesign** — owner-confirmed live; docs in `project_gen_z/` preserved via PR #55; confirm
  #55 merged before the stale `feature/homepage-mascots` branch is ever dropped / local reset.

## ⚠️ Registry-hygiene debt (owed, needs supervised sweep — do NOT mass-close unverified)
- Census 2026-07-04: **96 IN_PROGRESS** (mostly stale June-era), **9 unverified RETURNED**, 15 BLOCKED, 11
  CLOSED-not-yet-archived. Owed: a supervised reconciliation sweep (verify each against artifacts → close or
  re-activate). ~10 stale git worktrees to prune (t461*, deanchor, p277, phase2, task395…).
- **NEW tooling nit (2026-07-05, flagged by Content a82926, low-pri, has workaround):** `integrations/clients/http.py`
  shadows Python's stdlib `http` package when that directory is added directly to `sys.path` → breaks transformers/httpx
  imports (hebrew_grammar_gate). Workaround = import via the `integrations.clients` package path. Fix owner = integration-client lane.
- Known tooling nits: validate_return.py fence-regex mis-pairs when a ```diff block precedes the ```json
  contract; return-contract key-drift across agents (enforce return_contract_v1 keys in authoring template).
