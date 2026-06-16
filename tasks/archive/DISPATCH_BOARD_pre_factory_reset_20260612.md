# Bari — Live Board
*Updated by the orchestrator at every change · Last update: 2026-06-12 (P29 DISPATCHED — Copy Engine, native Content Agent background subagent; THE ROAD move 10 in flight) · Ctrl+Shift+V for the pretty view*

---

## 📬 Signals — your only job in this file
**When you send a prompt to an agent, put an `x` between the brackets on its line.
I see these states automatically with every message you send me.**
(Return blocks still get pasted into chat — I need their content, not just a signal.)

**Active prompts:**
- ✅ P29 → **C1-NATIVE (Content Agent)** — RETURNED + **orchestrator-VERIFIED against artifacts 2026-06-12 → CLOSED.** The Copy Engine is built (3 reusable scripts: build_copy_inputs.py / author_yogurts_v1.py / merge_copy.py) and run on yogurts. Verified: `yogurts_final_v1.json` = **0 PENDING_COPY**; gates **G1–G7 PASS** (report file read); **readability 616/616 is_clean**; 2 S blocks byte-verbatim; superlatives corpus-stat-grounded (3 granted). Output: `03_operations/page_generator/outputs/yogurts_final_v1.json` + `copy_sample_for_review.md`.
  - **Shared-instrument change verified legit:** agent narrowed `integrations/clients/hebrew_readability.py` `_SCORE_NUM` with a negative-lookahead so nutrition decimals ("10.5 גרם") don't false-positive as exposed score mechanics. Orchestrator re-tested the regex: real leaks (92.6/S, "score 92.6", 68.2, 72/B) STILL fire; unit-suffixed decimals don't. Surgical, not a gate-weakening. (Bug also affects the LIVE granola copy "12.1 ג' חלבון" — pre-existing false-positive, now fixed.)
  - 🔴 **BLOCKER confirmed real (Data/generator lane) → P37 dispatched:** the generator config wrongly excludes barcode **7290110565527** (דנונה PRO, 2nd S product) as "OFF contamination." Orchestrator-verified: shipcfg2 trace = `single_source_only`, protein **10.0**, **no** panel_source=OFF, grade **S 90.62** — CLEAN Shufersal. The OFF protein=20.0 / off_candidate_panel belongs to the separate **Yohananof duplicate**. Config conflated the two (RC1 inherited-ruling pattern) and dropped the barcode entirely → page shows **S=1 while narrative/caveat say S=2**. Copy for it is STAGED in authored_yogurts.json (merges on restore). Must fix before owner preview (ROAD move 13).
- ✅ P35 → **C2** — RETURNED + **orchestrator-VERIFIED against live artifacts 2026-06-12**. Map: **DIRTY 3** (yogurts v3 LIVE = 8 corpus-OFF + 7 image-OFF; cereals = 6 corpus-OFF still live; granola = 17 corpus-OFF) · **CLEAN 6** (bread, hummus, veg-spreads, snacks, cheese, milk) · **UNKNOWN 2** (butter, salty-snacks: no BSIP1 records). 🔴 **NEW LIVE BREACH:** the live yogurts v3 page serves 8 OFF products — board's prior "OFF-CLEAN verified" was about v4, NOT the v3 that's live. ⚠️ P36 auto-router CLOSED this on face value & missed both contradictions; return JSON counts also disagreed with its own (correct) report body. Report: `03_operations/off_sweep/off_sweep_v1.md`.
- [x] P36 → **C1-NATIVE** — RETURNED + orchestrator-verified ✅ CLOSED. **THE ROUTER IS LIVE:**
  `python 03_operations/router/dispatch.py P<N>` → opencode serve API → `opencode/deepseek-v4-flash-free`
  → return captured to `tasks/returns/P<N>_return.md` + git-delta + board auto-tick. Selftest PONG 19.5s;
  hash exact; dry-run on P35 re-run by orchestrator. (Note: `opencode run` hangs headless — HTTP serve API
  is the only viable path; binary path hardcoded with which-fallback.)
  **ROUTER LAW (post-P35 lesson, now stamped into every return file): router output = RETURNED-UNVERIFIED;
  the router never closes; orchestrator verifies every claim against artifacts before any CLOSED.**
- ⏭️ P34 (C1, queued): fixture library formalized + red-team file-check gate line in run_gates.py.
- Closed this wave: P27 (generator — orchestrator re-ran it independently: 80 products, G1–G7 PASS, boundary policy picked up = the "missing file" was P33/P27 timing, not a bug) · P32 · P33.
- **P30 CANCELLED** — confidence mapping was built into the generator (P27 deliverable 2.4) and passed gating; a separate prompt would duplicate it.

**THE ROAD (TASK-257, moves 1→16; orchestrator holds this line, no detours):**
1. ~P25 returns → verify schema vs the 3 live JSONs (spot-check fields).~ ✅ Done 2026-06-12 —
   **orchestrator-verified:** required-set holds across all 60 granola+snacks products, 0 violations.
   **Contract decision:** generator targets the MODERN canonical schema (granola/snacks/yogurts shape);
   milk = LEGACY format → quality-reference only, stays quarantined (legacy-isolation policy, frozen scores).
2. ~P26 returns → I RE-RUN the gates myself: must FAIL on bad v4 (images+scope), must NOT false-positive on granola (Hebrew-regex risk: מ"ג/לל"ג).~ ✅ Done 2026-06-12 —
   **orchestrator-verified:** G2+G3 both fire on v4 (6 images, 70 unexplained). Hebrew-regex PASS on granola (G5 fails on real TASK-198 score drift, not regex noise).
   **Bonus signal from granola run:** G3 FAIL (sub-pool split not declared in _meta) · G5: 1 grade inflation (7290014471436 shows D, trace=E) · G6: 'חלבון נמוך' ×9 + sodium causal framing ×3 in live copy.
   **Schema debt flagged (pre-Phase-1):** P25 schema has float-vs-integer score type drift + missing comparisonContext + undocumented extension fields (_subpool, _isChildrens). Schema must be updated to match the canonical format before the generator can self-gate (G1).
3. (No stall risk: P26 runs without P25's schema — gate 1 skips gracefully.)
4. Micro-ruling needed during Phase 1: grade-boundary policy floor-vs-round (the Great Grains E/D bug). Default = floor; ratify with Nutrition. Blocks gate 5 consistency only.
5. ~Draft P27 (C1): generate_page.py — self-gating.~ ✅ Drafted — **P28 MERGED INTO P27** (configs + generator are one feedback loop; the schema-v2 fix from P26's debt finding is Deliverable 0 of P27).
6. ~Draft P28 (C2)~ — merged into move 5.
7. ~P27/P28 return → ACCEPTANCE: regenerate granola + snacks from sources, diff vs live.~ ✅ Done 2026-06-12 — orchestrator-verified: 0 GAP items in both diffs.
8. ~Expected fight: diff ≠ 0...~ ✅ Done — granola: 18 LIVE_DEBT (10 off_banned + 8 subpool mismatch), 1 NEW; snacks: 10 grade LIVE_DEBT (stale pre-headpin). No GAP = generator is complete for non-copy fields.
9. ~Yogurts through the generator → ~80 products, 100% images, strings PENDING. No page touched.~ ✅ Done — 80 products, 80/80 images (100%), PENDING_COPY throughout.
   **⚠️ Note on barcode 7290000408316:** clean Shufersal corpus record EXISTS → included in the 80 (correct). The "dropped product" was a Yohananof-only gap. Config exclusion entry should be removed.
   **⚠️ Yogurts grade change:** 1×A→S promotion (engine-recognized S, correct per owner_s_grade_honesty_ruling); 3×A→B corrections (floor policy). Expected.
10. ~Draft P29 (C1): copy engine (trace-driver lines, standalone rule) + P30 (C2): confidence mapping.~ ✅ Done 2026-06-12 — **P29 CLOSED, orchestrator-verified** (0 PENDING, G1–G7 PASS, readability 616/616). P30 was CANCELLED (built into generator). The Copy Engine is a reusable 3-script machine.
11. ~P29 returns → claim gate (auto) + editorial sample.~ ✅ Done 2026-06-12 — claim gate auto **G6 PASS**; orchestrator editorial read of the seeded 10-card sample = **PASS, no revision loop spent**. Verified: standalone rule holds, grade-in-prose=badge, sodium/fat are facts-only (goat card pins B on protein not נתרן), real-driver named (additives/sugar-sources/list-length), superlatives correctly scoped (exclusive reserved, plural used elsewhere), no framework leakage, no "חלבון נמוך" bare dismissal. Quality matches the row-verdict model.
    **🔴 GATING move 13 — IN FLIGHT (P38):**
    - **P37 (C1, Data Agent) — RETURNED BLOCKED + orchestrator-VERIFIED.** Data/config portion CORRECT: removed the 7290110565527 exclusion → generated page 81 / **S=2** / restored record S,90.6,protein 10.0,shufersal,**zero OFF** (grep-confirmed). Block was real: P29's staged S card was INCOMPLETE (only expansion+rowVerdict; missing insightLine + s_grade_explanation) → merge_copy crashed. **Bonus finding (orchestrator-verified):** the SAME RC1 conflation wrongly excludes **6 MORE clean Shufersal products** (7290102394081/C, 7290102399819/D, 7290107936309/B, 7290110328764/C, 7290112330352/B, 7290116934402/C) — each has a clean shipcfg2 record (single_source_only, zero OFF) + an OFF Yohananof twin that is NOT in any loaded dir. Machine page was showing **81 while 87 clean products exist** — the exact "shown < scored" pattern that killed the last launch.
    - **P38 (C1, Content Agent) — RETURNED + orchestrator-VERIFIED against artifacts → CLOSED 2026-06-12.** The machine yogurts page is **COMPLETE: 87 products / S=2 / 0 PENDING_COPY / 0 OFF markers (final page + 6 restored traces independently grep-verified) / all 7 restored grades = clean Shufersal / gates G1–G7 PASS / readability 675/675**. 6 new B/C/D cards passed orchestrator editorial read (standalone, grade=badge, fat fact-only, real drivers, cap_misclaim products claim no cap, no superlative over-claim, no leakage). S explanation for 7290110565527 byte-verbatim (371 chars, source-matched). Output: `03_operations/page_generator/outputs/yogurts_final_v1.json`. **close_reason:** every claim verified at file:line; OFF-ban satisfied; full clean set restored. *Note for owner: both S explanations use Nutrition-approved relational framing (approved artifact, not a defect) — a fully-standalone rewrite would need Nutrition re-approval.*
    - 🟢 **MACHINE OUTPUT READY for move 13.** The page generator (TASK-257) has now mechanically produced a complete, gated, OFF-clean 87-product yogurts page from sources — proving the program's core thesis. Next: **P31 (preview wiring + parity) → then the OWNER side-by-side (move 13, tripwire 2).**
12. ~P31 (C2): preview wiring + parity report.~ ✅ PARITY DONE 2026-06-12 (orchestrator, data-level). **Machine 87 (S2·A10·B32·C19·D23·E1, 100% images, 0 OFF) vs live v3 19 (A7·B9·C2·D1, 18/19 images, 15 OFF markers incl. 7 displayed openfoodfacts.org image URLs).** Machine page is more complete AND OFF-clean; live v3 is in active OFF-ban breach. **Rendered frontend preview NOT built autonomously** — it's frontend integration adjacent to the consumer-facing swap + the audit's RC5 warns against another confidence-cascade build before owner sight. Held for owner direction.
13. ⛔ **OWNER WALL (move 13, tripwire 2 — his call alone):** side-by-side yogurts machine-page vs live v3 → swap or fix-loop. **Awaiting owner:** (a) build a non-published rendered preview for visual judgment then decide swap, or (b) other direction. Note: swapping also resolves the live v3 OFF breach.
14. Phase 4: cereals through the machine (clean 26-corpus; it needs re-ship anyway) → proves "second category in ≤1 day".
15. Runbook + retire hand-assembly permanently (board law: pages only from the generator).
16. Then substrate upgrades, in order: datastore port (#8) → DAG framework (#7) → extraction+dual-extractor (#1/Phase 5) → card #2 in Shadow (parallel anytime).

**Closed & verified this session** (prompt files in `tasks\prompts\_done\`):
P5 · P6 · P9 · P10 · P11 · P12 · P13 · P14 · P15 · P16 · P17 · P18 · P19 · P20 · P21 · P22 · P23 · P24 · P25 · P26 · P32 · P33 · **P27** · **P35** · **P29**.

**🔴 SYSTEMIC — P35 SWEEP COMPLETE (2026-06-12, definitive):**

| Category | Live? | OFF-fed | Image-OFF | Verdict | Action |
|---|---|---|---|---|---|
| granola | YES | 17/42 | 0 | DIRTY | Purge 17 → 25 products |
| breakfast-cereals | YES | 6/26 | 0 | DIRTY | Second purge → 20 products |
| yogurts (v3) | NOT YET | 8/19 | 7/19 | DIRTY | Generator output replaces v3 |
| bread | YES | 0/19 | 0 | CLEAN | — |
| hummus | YES | 0/64 | 0 | CLEAN | — |
| vegetable-spreads | YES | 0/64 | 0 | CLEAN | — |
| snacks | YES | 0/18 | 0 | CLEAN | — |
| cheese | YES | 0/45 | 0 | CLEAN | — |
| milk (legacy) | YES | 0/18 | 0 | CLEAN | — |
| butter | YES | 0 (no BSIP1) | 0 | UNKNOWN | No BSIP1 run exists |
| salty-snacks | YES | 0 (no BSIP1) | 0 | UNKNOWN | Self-declared clean; unverifiable |

**Total confirmed OFF-fed on live site: 23 products** (17 granola + 6 cereals; yogurts v3 not deployed)
**Total image-OFF: 0 live** (7 in yogurts v3, not deployed)
**Artifact:** `03_operations/off_sweep/off_sweep_v1.md`

**✅ PURGE PREPARED in working tree (2026-06-12, orchestrator):** granola `42→25` (17 OFF barcodes removed) and cereals `26→20` (6 OFF barcodes removed). Both files re-validated: valid JSON, 0 leaked barcodes, **0 OFF markers in live product records**. Removed barcodes documented in each `_meta.excluded_off_products` (BSIP source retained). **NOT deployed — awaiting owner deploy to bari.digital (tripwire 2, consumer-facing).** Copy still references old counts → reconcile in the P29 wave (cosmetic; not a rule breach).
**⚠️ Interim note:** copy in cereals-page-data.ts / granola-page-data.ts still cites 26 / 42 — fix in P29 copy pass, not blocking the data deploy.

**Open follow-ups (non-blocking):**
- **FLAG-A** (Data lane) — mango −4.0 unexplained penalty delta; trace-explainability, not a score error (see Yogurts section).
- **Dropped product** 7290000408316 — not recovered by P6; needs targeted Yohananof fetch or delisted-confirm.
- **Cereals R-15** — §9 display_values fallback to live-frontend nutrition (sugar/sat-fat 0/34 from run_cereals_005 gap); TASK-254/Nutrition call.
- **Roadmap (offered, not logged):** dual-extractor consensus → Phase-5; queryable datastore → Spine.

---

## 🚨 Yogurts relaunch — REGRESSION CAUGHT AT PREVIEW → REVERTED (TASK-256)

**Owner rejected the v4 preview (2/10 vs the 8/10 page it replaced):** 17 products shown while
**87 were scored**, 6 images dropped (5 existed in BOTH v3 and BSIP1), weak relational copy.
**Reverted in commit `4e2ec1a3`** — the good v3 page (19 products, real images, original copy)
is restored and committed. Nothing was ever published.

**Full root-cause audit (owner-ordered):** `02_products/yogurt_system/yogurt_relaunch_failure_audit_v1.md`
- RC1: 17-product scope was inherited spec, never challenged — the P19 prompt itself said "over 87" one line above.
- RC2: builder silently dropped images present in its own sources; return block never reported image coverage.
- RC3: claim gate proves truth, nothing proved value; the weak relational framing was instructed by the orchestrator's own brief.
- RC4: every verification checked spec-compliance, not "better than the live page" — self-referential loop.
- RC5: 11 green checkmarks in a row = confidence cascade; nobody reviewed the assembled page as a product.
**The only gate that worked: owner preview before publish.**

**5 permanent fixes adopted** (in the audit): Page Parity Gate (side-by-side vs live, blocking) ·
scope assertions w/ owner sign-off on >20% deltas · field-coverage reporting in return blocks ·
editorial quality review distinct from claim gate · inherited rulings expire.

**OWNER RULING (supersedes the rebuild plan): NO manual rebuild. This was goal drift.**
The owner never asked for a scoring/relaunch exercise — the intent was a SYSTEMATIC, AUTOMATED
process. The S=2 finding became a program orbiting 2 products; that program is dead. The v3 page
stays until the **pipeline** can regenerate it mechanically: scrape (raw store LIVE) → extraction
(Phase 5) → score (Spine DAG) → **frontend JSON as a generated view** (gap-analysis card #8) →
automated gates (parity, field coverage, claim gate in build) + dual-extractor trust (card #1).
A generator doesn't forget images or products — hand-built prompts do. All scoring assets
(87-product run, S=2 audit) remain as pipeline inputs. Memory: `owner_systematic_not_artisanal`.

**Open follow-up (NON-blocking, Data lane): FLAG-A** — mango (7290116934402) trace shows a −4.0
delta (score_after_cap 68 → score_after_penalty 64) with no named penalty rule in exposed fields.
Score 64 is frozen/consistent (v4=shipcfg2) and the copy is honest — this is a trace-explainability
gap, not a score error. Resolve before we ever surface per-product score breakdowns publicly.

One product (7290000408316) stays dropped — **P6 swept the Yohananof yogurt shelf (101 barcodes) but did NOT capture this one.** Recovering it needs a targeted fetch by URL/barcode (or confirm it's delisted). NOT a launch blocker — we ship 17 without it.

**🔴 CORRECTION (P35, 2026-06-12) — the OFF-CLEAN claim was about v4, NOT the live page:** the
prior "all 17 shufersal, zero OFF markers in v4" verification was run on **yogurts_frontend_v4.json**.
But page-data imports **v3**, and `yogurts_frontend_v3.json` (19 products, LIVE NOW) carries a
**Yohananof OFF pool**: 8 products scored from OFF panels (`run_yogurt_yohananof_001`) + 7 with
`images.openfoodfacts.org` image URLs displayed. **Verified by direct grep + JSON parse of the live file.**
This is a LIVE breach of the OFF hard rule (TASK-238). Remediation required before any further yogurts work.
(Also: barcode 7290107936309 appears twice — clean shufersal yog-007 AND an OFF Yohananof "Greek yogurt" dup.)
**⚠️ PRE-PUBLISH cosmetic:** 6/17 have no image incl. the S product `7290110565527` (90.6/S). Owner
decision: publish with placeholders, or source those images from the Shufersal/banked scrape first (no OFF).

---

## 👉 Next moves — THE PROGRAM IS NOW TASK-257: THE PAGE GENERATOR

Owner intent (anchor): *"a machine that takes a shelf and turns it into a well-explained,
complete, no-errors page — like milk, granola, snacks — quickly and efficiently."*

| Phase | What | Route | State |
|---|---|---|---|
| 0a | Output contract from the 3 working pages | **C2** | **P25 RETURNED ✅** |
| 0b | 7-gate suite as code (coverage/scope/OFF/grade/copy/parity) | **C1** | **P26 ready — send** |
| 1 | `generate_page.py` — data → complete frontend JSON, validated by re-generating granola/snacks ≈0-diff | C1 (+C2 configs) | next, after 0 |
| 2 | Copy engine from trace drivers + auto claim-gate | C1 (+C2 mapping) | after 1 |
| 3 | Preview + parity gate + owner side-by-side | C2 | after 2 |
| 4 | Second category + runbook | C1/C2 | after 3 |
| 5 | Extraction from raw store + dual-extractor (full chain) | backlog | raw store already LIVE |

Pilot data = yogurts (87 scored, 100% images in BSIP1 — nothing new to scrape or score).
The yogurt v3 page stays live until the MACHINE's output beats it at the parity gate + owner approval.

---

## ⚠️ Live-site / other category state

- **Cereals — QA audit DONE (`cereals_qa_report_v1.md`) → ✅ AMENDMENTS APPLIED 2026-06-12** (nothing was
  publicly published — preview-only; no fire). Build-verifying.
  - **⚠️ C1 (OFF blocker) PARTIALLY RESOLVED (P35 correction 2026-06-12):** 8 explicit OFF products moved to `_meta.excluded_off_products` (34→26). BUT P35 sweep found **6 MORE products in the live 26 via `run_cereals_carrefour_001`** with `panel_source=open_food_facts` in BSIP1 — scored from OFF nutrition, images clean. Barcodes: 7290017325910, 7290116535371, 7290112494351, 7290112495228, 8445290964595, 884912126115. **Cereals C1 is NOT fully resolved. Second purge required: 26→20 products.** Owner deployment decision needed.
  - **✅ H3 (grade defect) FIXED:** Great Grains Dates → **34/E** (was 35/D; engine grade_estimate=E).
    *Note for Nutrition:* the global round-vs-floor-at-grade-boundary policy is still open (I floored this one).
  - **✅ H2 (promo-as-ingredients) NEUTRALIZED:** Lion/Nesquik/Cini Minis ingredient field set to null →
    honest "data could not be retrieved" instead of marketing text. (Real fix = re-scrape, Data, later.)
  - **✅ Copy reconciled:** all count/retailer refs updated for 26 products (dist B:3/C:9/D:12/E:2,
    whole-grain claim 18, children 4, Shufersal-only) across cereals-page-data.ts + featured card (had stale 37) + hashvaot index.
  - **H1 (stale deploy):** moot — not published; merge/deploy is owner's call whenever.
  - Engine sound; 33/34 propagate correctly. M3 (cosmetic OCR/promo tails on ~12) left as non-blocking.
- **9 cereal products, small score drift** — regenerate copy+score together at next cereals
  re-ship (with TASK-189 sodium rule).
- **Branch hygiene (pre-existing, not P23):** `.next/types/validator.ts` TSC errors reference
  deleted maadanim/preview pages. `next build` is clean (stale generated types). Clear `.next` +
  re-confirm tsc before go-live; not blocking now.

---

## 🏭 Live on bari.digital

Milk · Bread · Snack bars · Cereals · Hummus · Salty snacks · Juices ·
Hard cheeses · Butter · Granola · Vegetable spreads
**Yogurts: candidate (3 steps out). Maadanim: purged.**

---

## 🗺️ Programs (platform work — NOT the yogurt launch; yogurts is just the first to exercise them)

| Program | Where it stands |
|---|---|
| **Shadow** — engine safety net | Merged. First real engine change arms the approved baseline. **Card #2 (property-based engine invariants) homes here — independent track, spec on request.** |
| **Spine** — pipeline backbone (cards #7+#8 are its roadmap) | Core merged. **TASK-257 = Spine's QA+package stages:** P26 gates = the DAG's QA node (#7); P27 generator = "frontend JSON as generated view" (#8, file-substrate first; P25 contract = future table schema). Datastore + DAG-framework = substrate swaps once stages exist as typed callables. |
| **Claim gate** — copy can't lie | Rubric v2 law; first production run passed (P17). Phase 2 = wire into build step. |
| **Living shelf** — auto-scrape & expand | Shufersal unblocked (no proxy spend); 89 expansion candidates banked; replay proof honest now (P20: 31/53); **Yohananof scraper LIVE (P6): 106 yogurt pages banked on VM**; Tiv Taam = validation leg. **Next: Phase 5 = offline BSIP0 extraction over the banked raw pages.** |
| **Page Generator** (TASK-257) — **THE program** | Phase 0 prompts ready (P25→C2, P26→C1). Shelf → complete gated page, mechanically. All other programs feed it: raw store = input, Spine = backbone, claim gate = gate 6, Shadow = score safety. |
