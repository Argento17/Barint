---
id: TASK-477
title: Protein-bars corpus conformance + lineage cleanup (blocks protein rescore)
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-07-03
closed_at: 2026-07-03
close_reason: "SHIPPED LIVE PR #66 (merged 4d93de56). Corpus cleaned (live scores were never tainted, 33/33 traced; stray run_maadanim dupes → TASK-409). Ingredient-handoff fix re-measured on clean corpus = 13 movers (3 C→D via PROTEIN_BAR_MALTITOL_TIER1, flagship holds B). Nutrition+Product co-sign GREEN; two-gate content (Sonnet ×2 + Adversarial QA); full 13-mover red-team Track-V all PASS (scores reproduce 32/32, grades correct, 19 non-movers byte-identical, superlatives rank-checked, OFF 0); EXCEPTION-002 filed; surgical patch barcode-verified. Last unclean live category — all live categories now verified/traceable. Follow-up tickets owed (see body)."
depends_on: [TASK-409]
blocks: []
category_id: protein-bars
summary: >
  Split out of TASK-476 rescore. Protein-bars is NON-CONFORMING: config _reproduce_note says generate_page.py incompatible; no standard BSIP1 trace dir; corpus pointer lands on a dir with zero bsip1 files; 7/15 REAL_LOSS rows in TASK-476 scope_scan point at STRAY WRONG-CATEGORY BSIP1 records -> rescore movers unstable (8/7/8 across runs; a new mover appeared, a predicted one vanished). Its LIVE scores may also be on contaminated corpus. FIX: clean protein-bars corpus lineage to true live records, conform to the uniform generate_page path (or document the exception), re-measure the ingredient-handoff impact on the CLEAN corpus, re-cosign, then rescore. Bread+crackers ship WITHOUT it (TASK-476 split).
---

# TASK-477 — Protein-bars corpus conformance + lineage cleanup (blocks protein rescore)

## Phase 1 (Data, worktree C:\bari_wt_t477, commit 91011f73) — DIAGNOSE + CLEAN + MEASURE, orchestrator-noted
- **True corpus:** `02_products/snack_bars/protein_combined_corpus_task365_33_20260621_fix.json` (33 products, sha469c650… matches config pin). NO BSIP1 trace dir — scored INLINE from the flat corpus JSON (config discloses this). Live shows 32/33 (1 granola curated out). `rerank_table_rescore.json` matches corpus 1:1.
- **Contamination scoped + NOT live-tainting:** stray `run_maadanim_001` (deli/appetizers run) holds 5/33 corpus barcodes as DUPLICATE records (overlapping "protein" search query), 0 numeric divergence. Live scores never read a BSIP1 dir → **live scores CLEAN, 33/33 traced.** Stray-collision = future barcode-glob tooling risk → routed to TASK-409.
- **Stable re-measure (ran 2×, byte-identical — replaces 8/7/8):** 19/32 unchanged, **13/32 move — 3 grade C→D (all PROTEIN_BAR_MALTITOL_TIER1 cap), 10 score-only**, all DOWN (de-inflation, bread/crackers class). Flagship 7290017516295 68.6/B +0.7 holds B.
- **Recommendation:** document protein-bars as a conformance EXCEPTION (inline flat-corpus scoring, no BSIP1 dir), not force-conform.

## Gate: CO-SIGN on the clean 13-mover set.
- **Product = CO-SIGN-WITH-CONDITIONS (a003ab26, GREEN):** ship now as surgical numbers-patch (bread/crackers shape); framing risk LOW (3 C→D all = PROTEIN_BAR_MALTITOL_TIER1, a published category finding, defensible); accept conformance EXCEPTION but **Exception Registry entry REQUIRED before/with the PR** (per EXCEPTION-001 precedent). Verified corpus sha + 0-extra/0-missing + JSON==prose. **Required downstream gates:** (1) content two-gate on the 3 grade-mover rows (rowVerdict/insightLine must reflect D not stale C); (2) full red-team on ALL 13 movers; (3) Exception Registry entry filed; (4) owner PR. Flagship 68.6→69.3 holds B. Post-rescore grade dist B1/C23/D8.
- **Nutrition = CO-SIGN (a3f5d047, GREEN):** independently read raw `ingredients_full` for all 3 grade-movers — maltitol explicitly + repeatedly declared in each (7290015130028, 7290019401049, 7290019401018); traced cap to source (POLYOL_TIER_1_TOKENS constants.py:1840 + PROTEIN_BAR_MALTITOL_TIER1 cap=62 score_engine.py:3799, EV-PBAR-001); re-derived scores itself for 2 score-only movers (full driver traces); direction all-grade-movers-down = correct de-inflation; `git diff origin/master...HEAD --stat` = 0 scoring-file change (pure plumbing, no philosophy). 0 unjustifiable movers. Conditions match Product (exception registry + 13-mover red-team + rerank grade-floor bug follow-up).
- **✅ BOTH CO-SIGNS GREEN.**

## Phase 2 — surgical patch ASSEMBLED (Data, commit 72f3ce9f) + orchestrator-VERIFIED
- 13 movers patched (score/grade/rank) in `protein_combined_frontend_v2.json`; 3 grade C→D (7290015130028 49.7/D r25, 7290019401049 49.5/D r26, 7290019401018 48.9/D r27). Flagship 69.3/B r1.
- **Orchestrator BARCODE-KEYED verify: 0 curated-copy changes** across all 32 products (rowVerdict/insightLine/positiveSignals/limitingFactors/comparisonContext/bottomLine byte-identical per barcode; the alarming line-diff = pure rank-reorder artifact of the sorted array, NOT copy edits). Grade dist B1/C23/D8 ✓. 3 movers keep OLD C-tier copy = PENDING_COPY (correct).
- **EXCEPTION-002 filed** (01_framework/governance/exception_registry_v1.md): protein-bars inline flat-corpus scoring, no BSIP1 dir, harness-reproduced.
- Gates: no NEW failures (pre-existing G1 schema + G5 no-trace only, byte-identical to origin run); G4/G6/G8 PASS.
## Phase 2b — 3 grade-mover rows RE-AUTHORED (Content/Sonnet, commit b94a130a) + orchestrator-VERIFIED
- Each of the 3 rewritten to reflect D honestly, driver-named from its own trace: 7290015130028 (maltitol + 3-family isolate-stacking + 9.9g satfat/low fiber); 7290019401049 (maltitol + glycerol + 362kcal/long list); 7290019401018 (maltitol + glycerol; kept real low-sodium 92mg positive without letting it soften). Author caught+fixed 1 draft antithesis pre-commit.
- **Orchestrator-verified delta:** touched EXACTLY the 3 movers' rowVerdict+insightLine (6 fields), 0 score/grade/rank change; 0 antithesis/0 em-dash in new strings; PENDING_COPY now []. Did NOT fabricate the "copper colorant" (correctly belongs to a different product 7290019766025, out of scope).
## Phase 2c — Adversarial QA + full red-team (a93dc0e8) = GO-WITH-FIXES
- **Track V ALL PASS:** score-vs-trace 32/32 reproduce (harness, sha-verified corpus), 13-mover diff == gate_b exactly; grade-boundary 49.7/49.5/48.9 correctly D; surgical integrity barcode-keyed (exactly 13 movers' numbers + 3 movers' copy, 19 non-movers byte-identical); superlatives ALL rank-checked TRUE (9.9g satfat 3rd-highest/32, 2.3g fiber 3rd-lowest, 92mg sodium 3rd-lowest); OFF 0; EXCEPTION-002 well-formed (4 questions answered, harness substitute, tripwire kept). Content claims all DEFENSIBLE vs trace.
- **RT-H1 (HIGH) = FALSE ALARM / RESOLVED:** QA flagged "no separate Content Agent artifact, all commits same lane" → but the copy WAS authored by a separate Sonnet content lane (agent af531d9c), NOT inline by Opus. QA inferred from git attribution (repo convention = owner acct + Claude co-author on ALL agent commits). Two-gate IS satisfied (Content Sonnet author + this Adversarial QA gate). Note on PR.
- **RT-M1 (MEDIUM, REAL) → fix round (content author resumed):** 2 residual antithesis via `ולא` (no comma, missed by the author's comma-regex) — 7290019401049 "חלבון מבודד ולא ממזון שלם" + 7290019401018 "...הנדסת מזון ולא על מרכיבים שלמים". Reword to positive declaratives. + RT-M2 stale `_meta.deployment_note` (references non-existent v1 file) → fix. + check 3 movers' expansion for D-contradiction.
- **RT-M3/M4 non-blocking (pre-existing):** 3 movers' expansion em-dashes (systemic, same class as milk product-row) + G1 schema FAIL (byte-identical on origin, stale schema). Backlog.
## Phase 2c fix (content author resumed, commit 399bd69b + gate-report 2884c568) + orchestrator-VERIFIED → SHIPPED PR #66
- RT-M1 fixed: 7290019401049 "חלבון מבודד ולא ממזון שלם" → "...ותערובת מהונדסת"; 7290019401018 "לא מפצה... ולא על מרכיבים שלמים" → "נקודת אור אמיתית בלוח שכולו נשען על הנדסת מזון ורכיבים מבודדים" (positive, kept low-sodium point). RT-M2 deployment_note fixed. Expansion reviewed = D-consistent, no change.
- **Orchestrator-verified:** delta = only the 2 rowVerdicts + _meta.deployment_note; 0 antithesis(all forms)/0 em-dash in all 3 movers' rowVerdict+insightLine; tree clean.
- **ALL GATES SATISFIED:** Nutrition+Product co-sign GREEN; two-gate content (Sonnet author ×2 + Adversarial QA); full 13-mover red-team Track-V all PASS; EXCEPTION-002 filed; surgical integrity barcode-keyed. RT-H1 = false alarm (separate Sonnet content lane, git attribution artifact).
- **SHIPPED → PR #66** https://github.com/Argento17/Barint/pull/66 (consumer rescore = owner merge). CLOSE on merge; prune C:\bari_wt_t477.
- **Follow-up tickets owed (non-blocking):** (1) rerank_table_rescore.json grade-floor tie-bug (2 barcodes, live already correct); (2) protein-bars expansion em-dash cleanup (systemic, w/ milk product-row); (3) G1 schema staleness; (4) TASK-409 run_maadanim stray-collision; (5) content authoring-template: antithesis scan must cover ALL לא/אלא forms not comma-only (3rd recurrence).

## Follow-ups (flagged, non-blocking)
- **Grade-boundary tie-grouping bug:** `rerank_table_rescore.json` mislabels 2 sub-floor products (7290019766230, 7290019401544, score<50) as C — but the LIVE frontend already shows the policy-correct D, so consumer site is NOT wrong. Fix the intermediate artifact separately → new ticket.
- **Exception Registry entry** for protein-bars non-conformance — governance filing (bari_exception_registry).
- **TASK-409 corpus-hygiene:** run_maadanim_001 stray-collision root cause.
