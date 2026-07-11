---
id: TASK-275
title: Factory run #7: cookies-near-coffee (עוגיות לקפה) subcategory page — broad cookie scrape, narrow to coffee-biscuit shelf
owner: orchestrator
status: CLOSED
closed_at: 2026-07-11
close_reason: "SUPERSEDED - cookies_coffee_frontend_v2.json live (asserted); parked 2026-06-14, scoring issues routed to de-anchor program (TASK-395+). Per ghost triage 2026-07-11 (tasks/reports/ghost_triage_2026-07-11.md); orchestrator mechanically asserted the cited artifacts before closing."
priority: HIGH
created_at: 2026-06-13
depends_on: []
blocks: []
category_id: cookies-coffee
summary: >
  Factory run #7 (golden brined playbook + Spine). Sub-category within cookies: the biscuit eaten with coffee (Lotus/speculoos, petit beurre, tea/marie, butter cookies, biscotti). Strategy: scrape a BROAD cookie radius at BSIP0, then narrow to coffee-cookies at corpus-filter (discard rule + methodology scope). Stages: scrape->corpus filter->score->invariants->generate->milk-depth schema->milk-quality copy->prologue charts->gates->red-team. OFF-banned. NO DEPLOY without owner.
---

# TASK-275 — Factory run #7: cookies-near-coffee (עוגיות לקפה) subcategory page — broad cookie scrape, narrow to coffee-biscuit shelf

## ⏸ PARKED pending a Bari-wide scoring project — 2026-06-14

Owner reviewed the local page 2026-06-14 and decided the scoring rework it surfaced is **bigger than
cookies → a new Bari-wide project** (owner to open). **No cookies-level rescore.** The design agent
was stopped. TASK-275 holds; it does NOT carry the scoring changes.

**Findings handed off as INPUTS to the Bari-wide project** (not executed here):
1. **Red-label de-anchor** (standing directive, memory `redlabel_deanchor_directive`): binary
   Israeli red-label caps → category-relative/continuous. Machinery exists behind `BARI_REDLABEL_V1`
   (currently dairy-scoped). Brined graduated-sodium (`graduated_sodium_d7_design_v1.md`) is the blueprint.
2. **Fat-source severity (מחמאה/מרגרינה)** + additive depth: engine blind to hardened veg-fat
   (`has_phvo` 0/58); additive `tier` is display-only (not scored). → `methodology/cookies_coffee_additive_depth_ruling_v1.md`.
3. **Ingredient truncation** (data bug): 16/58 traces scored on a 1-ingredient list → additive/PHVO blind.
- Run-7 retrospective (routing/spine/process/lessons): `reports/factory_run7_retrospective_v1.md`.

**SPLIT (owner 2026-06-14):** #1 red-label de-anchor → deferred to the Bari-wide project. **#2
fat-source severity (מחמאה/מרגרינה) + #3 truncation fix → PROCEEDING now** (separable; don't touch
red-label averaging). In flight: Data Agent on a branch — Fix A (truncation parser), Fix B (widen
`_PHVO_MARKERS`: מחמאה/מרגרינה/שומנים מוקשים), Fix C (`fat_quality` ceiling 40 when has_phvo — a
dimension drop, NOT a new cap). Gated: rescore cookies→run_005 + delta, frozen milk byte-identical
0/20, 342 invariants, no published run re-run (מרגרינה in cereal/snack stays latent). Product co-sign
+ owner delta review before any page regen/publish.

**Engine fixes VERIFIED + owner-authorized to merge & rebuild (2026-06-14).** Orchestrator verified:
3 diffs correct; frozen milk 0/20 has_phvo, top 85/A held (byte-identical by construction; Fix-A
cookies-only, B/C has_phvo-gated); run_005 = C5/D22/E31, 25 moved, 4 grade changes (all downward —
honest: truncation was inflating #1 540160 63→51 and spelt #27 37/D→29/E). Owner chose "merge fixes
AND rebuild page now" (ship honest page on run_005; de-anchor later). Product co-sign logged as
OWNER-AUTHORIZED (owner > D7). Branch `task-275-engine-fixes-abc` (commit 10ca9738).

**Rebuild pipeline (in flight):** Data regen structural from run_005 + preserve copy + stale-copy
manifest → Content remediates (4 grade verdicts + prologue 7→5 C + NAME the מרגרינה/מחמאה on has_phvo
products = delivers owner comment #7) → orchestrator rebuild+gate (score==trace, OFF=0, build) →
Red-Team + C3 bracket → local deploy. Milk traces NEVER staged.

**Cookies page status:** rebuilding on run_005. Polish (#5/#6) folds into this cycle. NOT for deploy
until red-team clears.

## ✅ PAGE OWNER-READY (LOCAL) on run_005 — 2026-06-14 (zero CRITICAL; survived red-team + 3 C3 passes)

**Final corpus: 56 products, C5 / D21 / E30, score==trace 0, OFF 0, images 56/56, 0 rendered PENDING.**
- **2 data discards** (missing-data rule): 7290013453631 (ingredient field = marketing blurb → false
  has_phvo) + 7290017962108 (scrape grabbed another product's cranberry data on a "vanilla pecan").
- **Polish:** story-driven de-anchored intro (#6, proportional-consumption); charts redesigned to the
  brined-golden bar (#5); 13 has_phvo verdicts NAME the מרגרינה/מחמאה (#7 delivered), label-faithful.
- **Adversarial:** C3-before (P98, 0 CRIT) → Red-Team (BLOCKED 2 CRIT+4 HIGH, all closed) → C3-after
  (P100, 2 NEW CRIT: bottomLine PENDING render leak + broader truncation + SEO-FAQ "healthiest" — all
  closed) → C3-final (P102: all CLOSED bar trailing-comma cosmetics → fixed, 0 suspect endings).
- Gates caught orchestrator misses: rank-change copy staleness, discard count-propagation, RT-9 wrong-
  layer (bottomLine renders via shared ExpansionSection), PHVO naive-substring false-positive on
  negation/marketing text.
- Local view: `cd bari-web && npm run start` → `/hashvaot/cookies-coffee`. **NO PROD DEPLOY w/o owner.**
- **Open follow-ups (non-blocking):** (a) PHVO matching should scope to parsed list + handle negation;
  (b) display-ingredient truncation/marketing-bleed = generator/bsip0 sanitization gap (fixed here from
  traces, not yet systematic); (c) red-label de-anchor → Bari-wide project.

## ~~★ PAGE OWNER-READY (LOCAL) — 2026-06-14~~ (SUPERSEDED — see PARKED above)

**Authoritative scoring run:** `run_cookies_004` (58 products). Distribution **A:0 B:0 C:7 D:22 E:29**, max
63.1/C — an honest least-bad, C-ceiling indulgence shelf (snack-bar-precedent shape, one notch lower).

**Pipeline (all orchestrator-verified at each seam):**
- P64 broad BSIP0 scrape (129, OFF=0) → P67 corpus filter (narrow) → P88 red-team scope ruling (drops) → **58**.
- P65 methodology + P66/P72 C3 premise/collapse reads → engine-natural C-ceiling (no tripwire).
- EV-058 `biscuit` router category (P73 Nutrition + P74 Product D7) — added for taxonomy/coherence, caps
  intact, **0 published-score movement** (bleed-sim 0, invariants 342, proven across P75/P75b/P89).
- P76/P82/P90/P94 milk-quality Hebrew copy (C3-gated; least-bad framing, honest disclosures).
- P77/P85/P86/P91/P95 render trio + index card + sugar×sat-fat prologue charts (recharts, grade never colored).
- **Stage-9 Red-Team: P87 BLOCKED (2 CRITICAL) → remediated → P92b re-gate CONDITIONAL PASS, ZERO CRITICAL.**
  **C3 review #2 (P93): ZERO CRITICAL.** All HIGH/MED (incl. 6 false NOVA-2 signals, 3 verdict factual errors,
  chart-title, provenance) fixed + verified.
- Deterministic gate (orchestrator): build EXIT:0, score==trace 58/58, OFF=0, images resolve 58/58, 0 PENDING.

**Local view:** `cd bari-web && npm run start` → `localhost:<port>/hashvaot/cookies-coffee`.
**NO PRODUCTION DEPLOY without owner** (tripwire-2 — owner's separate consumer-facing call).

**Open factory follow-ups (non-blocking, noted for the machine):** (a) gen_frontend_json.py NOVA-2/minimal-
processing suppression implemented but not full-regen'd (JSON handles the live page); (b) 4 dead page-data.ts
fallback strings (don't render) — cleanup; (c) page-data→JSON page_copy refactor done for cookies, generalize
to all categories; (d) EV-058 oat re-route needs a multi-term router match (abbreviated "ש.שועל" + cereal-
anchor precedence) — separate P-spec if oat biscuits recur.

<!-- opened with new_task.py -->

