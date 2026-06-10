# Project Comp — Source Discovery Report v1

**Phase:** D0 — Source Discovery & Registry Build
**Owner:** Research Agent (evidence) + Marketing Agent (signal), joint
**Date:** 2026-06-10
**Scope:** Define the source universe Project Comp will monitor daily. **Not** a trend report. **No** scheduled run defined (Rule 10).
**Artifacts produced:**
- `source_registry_v1.yaml` — 48 verified active sources
- `source_candidates_v1.yaml` — 27 unverified/holding candidates
- `project_comp_watch_terms_v1.yaml` — 205 Hebrew+English watch terms (95 he + 110 en), 18 topic groups
- this report

**Core principle enforced throughout:** *influencers are signal, not evidence.* `credibility_weight` and `discourse_weight` are kept as separate axes; follower count is never treated as credibility (Rules 3 & 4).

---

## 1. Executive Summary

Project Comp's job is to watch the nutrition conversation — Israeli and global — and tell Bari what consumers, clinicians, regulators, and competitors are saying about food. D0 builds the **who/what to watch**, not the watching itself.

We verified **48 active sources** (22 Israeli/Hebrew, 26 English/global) as public and relevant via web search on 2026-06-10, and parked **27 candidates** that are plausible but unverified — most often because an exact, current handle/URL could not be confirmed, which Rule 9 says keeps them out of the live registry. We deliberately kept the registry **small and high-quality** over large and noisy (Rule 6): every active entry is a confirmed public page, and every viral-but-thin account was routed to candidates or tagged `misinformation_watch`.

The registry separates three things Bari must never conflate:
1. **Evidence** (regulators, academic public-health bodies, Examine, Cochrane) — `credibility:high`.
2. **Signal** (media desks, brands, big creators) — what the market is being told; often `discourse:high / credibility:low`.
3. **Misinformation patterns** (glucose-spike hype, seed-oil panic, EWG-style fear scoring) — tagged `misinformation_watch` so Bari can position against them, not absorb them.

**Verdict: PASS WITH FIXES.** The registry is strong enough to seed a first daily run. Two fixes should land before or alongside the scheduled task: (a) verify and promote the highest-value Israeli individual creators now sitting in candidates, and (b) decide the platform-access reality for Instagram/TikTok monitoring (see §7).

---

## 2. Source Mix

**By status**
| Status | Count |
|---|---|
| Active (registry) | 48 |
| Candidate | 27 |
| **Total mapped** | **75** |

**Active by language**
| Language | Count |
|---|---|
| Hebrew (he) | 21 |
| English (en) | 25 |
| Mixed | 2 |

**Active by market**
| Market | Count |
|---|---|
| Israel | 22 |
| US | 14 |
| Global | 6 |
| EU | 2 |
| UK | 2 |

**Active by source_type**
| source_type | Count |
|---|---|
| public_health | 9 |
| regulator | 7 |
| mainstream_health_media | 7 |
| licensed_dietitian | 4 |
| nutrition_blog | 4 |
| competitor | 5 |
| brand | 3 |
| doctor | 3 |
| fitness_nutrition | 2 |
| food_label_reviewer | 1 |
| retailer | 1 |

**Credibility × discourse (active) — the two-axis check**
- `credibility:high` sources: 17 (all evidence/regulatory/academic). These anchor truth.
- `discourse:high` sources: 12 (media, big creators, hot competitors). These anchor attention.
- The overlap (high/high) is small and deliberate — most high-reach sources are *medium-or-low* credibility, which is exactly the separation the brief demanded.

---

## 3. Top Israeli Source Clusters

1. **Institutional / regulatory anchor** — MoH Efshari Bari (il-001), MoH Food Control (il-002), the national nutrition DB (il-003, *directional only*), PAN Israel physicians' org (il-004), Israeli Pediatric Association (il-005). This is the credible Hebrew backbone and the source of the 2020 warning-label thresholds Bari already reasons about.
2. **Mass-reach media desks** — Ynet Health (il-008), Mako healthy-nutrition (il-009), Haaretz Food (il-010), Walla kids-nutrition (il-011), Ynet Food (il-021). `discourse:high / credibility:medium` — the earliest read on what goes mainstream in Hebrew.
3. **Licensed dietitians / educators with public sites** — Karen Ann (il-012), Dganit Ein Bar / label literacy (il-013), Mutarli non-diet (il-014), Daat HaGuf (il-015). Practitioner voices, not evidence; Ein Bar's label-reading focus is the closest fit to Bari's own mission.
4. **HMO public-health content** — Clalit (il-006), Leumit (il-007). Institutional consumer education with enormous reach.
5. **Brands + retailer (signal/category)** — Tnuva (il-017), Strauss (il-018), Tivall/plant-based (il-019), Shufersal (il-020, already the BSIP0 scrape backbone). Watch the high-protein-dairy marketing wave and clean-label reformulation.

---

## 4. Top English / Global Source Clusters

1. **Direct competitors** — Yuka (gl-001), Open Food Facts (gl-002), Fooducate (gl-003), EWG Food Scores (gl-004), ZOE (gl-005). The scoring-app landscape Bari competes in. EWG is double-tagged `misinformation_watch` for hazard-not-dose scoring; Fooducate is the closest letter-grade analog.
2. **High-credibility evidence** — Examine (gl-006), Harvard Nutrition Source (gl-007), Marion Nestle (gl-009), Cochrane (gl-024), plus the already-integrated data layers DSLD (gl-025) and PubChem (gl-026). These adjudicate contested claims.
3. **Regulators** — WHO (gl-010), EFSA (gl-011), US FDA (gl-012). EFSA is the spine for additive/emulsifier/dye/sweetener risk — directly feeding BSIP2 additive evidence.
4. **Food-policy & industry commentary** — FoodNavigator (gl-015), STAT (gl-016), plus the RD-newsletter counter-voices The Nutrition Tea (gl-017) and Abbie Attwood (gl-018) that argue *against* UPF-panic — a useful corrective for Bari's framing.
5. **Major social creators (signal, scrutinized)** — Glucose Goddess (gl-021, hype), Layne Norton (gl-022, evidence-leaning counter-voice), Mark Hyman (gl-023, seed-oil/clean-label hype), and NutritionFacts (gl-008, plant-based-biased but citation-heavy). Mainstream explainers Healthline (gl-019) and Verywell (gl-020) are kept to two, on purpose (Rule 8).

---

## 5. Known Gaps / Sources Needing Manual Review

1. **Israeli individual creators are under-represented in the *active* set.** High-profile figures (e.g. Maya Roseman, cand-001) and the fastest-growing IL diet creators (cand-003) sit in candidates because an exact, current public handle could not be confirmed at D0. **Action:** verify handles, then promote the credible ones — this is the single biggest registry improvement available.
2. **No Hebrew-language independent evidence aggregator exists** (cand-026, a gap marker, not a source). There is no Israeli "Examine." This is both a monitoring gap *and* a genuine market void Bari could fill.
3. **TikTok and public Facebook are unmapped** (cand-011, cand-012). These are primary IL misinformation/parenting vectors but raise access and (for FB) privacy limits — public pages only; **private groups are hard-excluded (Rule 2).**
4. **Diffuse movements need concrete anchors** — MAHA food-policy (cand-021) and the GLP-1 nutrition cluster (cand-027) are real and loud but have no single source; each needs 1–2 named public anchors before it can be a registry entry.
5. **Primary literature should route to the existing integration client, not be re-monitored here** (cand-020) — coordinate with the Research literature client to avoid duplication.
6. **Maccabi HMO** (cand-007) is missing only a confirmed landing URL to complete the HMO set.

---

## 6. Recommended Active Registry Size for the First Daily Run

**Start the first run on a focused subset of ~28–32 of the 48 active sources, not all 48.** Rationale: a daily run should prove signal quality before scaling breadth (Rule 6).

Recommended first-run subset:
- **All 7 regulators + 9 public-health** bodies (evidence floor) — but poll these **weekly**, not daily; they change slowly.
- **All 5 competitors** (daily — they move fast and matter most to positioning).
- **The 7 media desks + 2 RD newsletters** (daily — this is where discourse breaks).
- **3–4 highest-signal creators** (gl-021, gl-022, gl-023, + one IL creator once promoted).
- **Brands/retailer** (weekly — reformulation/marketing shifts are not daily events).

So: **daily core ≈ 18–20 fast-moving sources** (competitors + media + top creators), with the **evidence/regulator/brand tail (~28) on a weekly cadence**. This keeps the daily run sharp and cheap while preserving full coverage on a slower loop.

---

## 7. Risks

1. **Influencer noise.** The loudest sources are the least reliable. *Mitigation:* the two-axis model (`credibility` vs `discourse`) is enforced in every record; `misinformation_watch` is a first-class `bari_use`; no creator enters as `evidence_reference`.
2. **Unverifiable claims.** Creators state opinion as fact. *Mitigation:* Rule 4 is structural — creator content is `consumer_signal`/`misinformation_watch` only; claims get adjudicated against gl-006/gl-024/regulators before they ever touch Bari reasoning.
3. **Platform access limitations.** Instagram/TikTok have no clean public API; scraping logged-in/private content is forbidden (Rule 2). *Mitigation:* candidates flag this explicitly; the first run leans on **web/RSS-accessible** sources (media, blogs, newsletters, regulators) and treats social as a manual/periodic sweep until an access method is decided. **This is the main open dependency before the scheduled task.**
4. **Hebrew search blind spots.** Hebrew nutrition discourse is harder to surface than English; D0 search confirmed institutions and media easily but struggled to pin individual creator handles. *Mitigation:* mandatory IL coverage was met at the institutional/media tier (22 active); the creator tier is staged in candidates with explicit `verify_action`s rather than guessed at.
5. **Bias inheritance.** Several credible sources carry directional bias (PAN/NutritionFacts plant-based; anti-diet RD newsletters; pro-protein fitness voices). *Mitigation:* biases are named in each record's `notes`, and opposing wings are both included so Bari reads the debate, not one side.
6. **Self-reference / name collision.** A third-party "Chef Bari" blog (cand-008) shares our brand name — flagged to verify it is unrelated before any monitoring.

---

## 8. Recommendation

### Verdict: **PASS WITH FIXES**

The source universe is well-formed, honestly verified, and correctly separates credibility from virality. It meets every minimum target:

| Target | Required | Delivered |
|---|---|---|
| Israeli/Hebrew sources | 20–40 | **22 active** (+ IL candidates) |
| English/global sources | 20–40 | **26 active** |
| Candidate sources | 20–50 | **27** |
| Watch terms (he+en) | 30–80 | **205** (95 he + 110 en) across 18 groups |

**Fixes to land before/with the scheduled task (none are blockers for design, all are quick):**
1. Verify + promote the top Israeli individual creators from candidates (cand-001, cand-003, cand-005) — closes the biggest gap (§5.1).
2. Confirm canonical URLs for the strong global candidates (cand-023 USDA guidelines, cand-007 Maccabi) and promote.
3. **Decide the social-monitoring access model** (§7.3) — this determines whether Instagram/TikTok sources are daily-automated or manual-periodic. This is the one real dependency.

### Can the Project Comp daily scheduled task now be defined?

**Yes — readiness is met, but do not create it in this phase (Rule 10).** D0's mandate was source discovery only. The registry, candidates, and watch terms are sufficient to define a daily run on the §6 subset. Defining the schedule is the **next phase (D1)** and should begin only after fix #3 (social-access model) is decided, since it changes the run's source list and cadence.

**No scoring changes proposed. No Bari content created. No trend report written. No scheduled task defined.** — per the D0 boundary.

---
---

# D0b Addendum — Israeli Creator / Influencer Source Layer

**Date:** 2026-06-10 · **Addressed to:** Research + Marketing + QA (handled inline, all three lenses applied) · **Trigger:** D0 closure blocker — Israeli individual creators under-represented in the active set (D0 §5.1).

## D0b.1 What changed

| | D0 | After D0b |
|---|---|---|
| Israeli active sources | 22 | **31** (+9 verified creators) |
| Global active sources | 26 | 26 (unchanged) |
| Total active | 48 | **57** |
| Candidate entries | 27 | **44** (+17 IL creators; cand-001 promoted → tombstone) |

**Deliverable answers:**
- **Israeli creators added to ACTIVE registry: 9** → il-023 Maya Roseman, il-024 Omer Miller, il-025 Gal Rubinstein ("תזונה שפויה"), il-026 Dr. Olga Raz, il-027 Proteins.co.il, il-028 TBM Academy (Tal Ben Moshe), il-029 Zvia (label reader), il-030 Ruti Fink (podcast), il-031 Sigal Belzer (kids).
- **Israeli creators kept as CANDIDATES: 17** (cand-028…cand-044), incl. the highest-value lead **Matan HaBar / מתן הבר** (food technologist exposing label truths — Bari's exact niche) held only because his exact handle never resolved to a live profile.

## D0b.2 Promotion standard applied (QA lens — no guessed handles)

A creator went **active only if** a public URL/handle was seen *resolving as an actual result link* (own site / Substack / podcast / `instagram.com/<handle>`) **and** the source runs an ongoing public content stream. Two honest consequences:
- **Handles seen only inside a search-engine summary** (e.g. `@rutifink`, `@amitganornutrition`, `@netta_kailler_nutrition`) were **not** promoted — they sit in candidates marked *confirm-before-use* (cand-032/035/036). Ruti Fink is active via her **verified podcast URL**, not via the unconfirmed handle.
- **Verified-URL clinic sites with no evident content stream** (Anat Tavor, Heli Maman) were kept as candidates, because a clinic homepage is not a *discourse* source to monitor. Sigal Belzer is the one kids active, flagged as clinic-oriented.

**Vocab note (QA):** one controlled-vocabulary value, `food_culture`, was added for figures like Omer Miller who fit no original `source_type`. It is signal-only — `credibility:low` for nutrition by default, never `evidence_reference`. Documented in `source_registry_v1.yaml` meta.

## D0b.3 Credibility ≠ virality — worked examples

**High-discourse / low-credibility (track as SIGNAL + `misinformation_watch`, never evidence):**
- **il-024 Omer Miller** — ~380K reach, but a chef on a personal keto diet, not a clinician. Pure consumer signal.
- **il-023 Maya Roseman** — `discourse:high`; credibility only `medium` despite a PhD, because she is a popularizer (verify specific claims).
- **cand-037 Carnitosis / ketosis.co.il** & **cand-038 carbfree.co.il** — IL carnivore/keto + low-carb advocacy; ideology-driven hype nodes.
- **cand-028 Matan HaBar** — `discourse:high`, but a food-industry insider POV that can cut both ways → claims need cross-checking.

**High-credibility / medium-discourse (practitioner voices, evidence-adjacent but still not primary evidence):**
- **il-026 Dr. Olga Raz** — veteran ex-Ichilov clinical dietitian; closest of the creator tier to evidence-adjacent.
- **il-028 TBM Academy** — explicitly science-based, debunks social-media nutrition myths (also a `misinformation_watch` lens).
- **il-025 Gal Rubinstein** & **il-029 Zvia** — licensed dietitians; Zvia's label-reading content is the tightest topical fit to Bari.

## D0b.4 Coverage by creator type (the 9 required categories)

| Required type | Active | Candidate | Status |
|---|---|---|---|
| 1 Nutrition IG creators | Roseman, Rubinstein | Liya Noga, Amit Ganor*, Netta Kailler* | OK |
| 2 RD / clinical nutritionists w/ social | Roseman, Rubinstein, Raz, Belzer | Tavor, Maman, Tirtza Shani | Strong |
| 3 Doctors on nutrition/metabolism/obesity | — | Obesity Society (cand-042); **individual = GAP (cand-043)** | **Weak — gap** |
| 4 Food-label / supermarket reviewers | Zvia (il-029) | **Matan HaBar (cand-028, top lead)** | OK, pending top promote |
| 5 Fitness + nutrition | Proteins.co.il, TBM Academy | — | Strong |
| 6 Kids-food / parenting | Belzer (il-031) | Tavor, Maman, Tirtza Shani | OK but clinic-heavy |
| 7 Food-culture figures | Omer Miller (il-024) | Oz Telem, Dor Vanger, Gold Rita | OK |
| 8 Brand/product commentators | (D0: Tnuva/Strauss/Tivall) | Matan HaBar doubles here | OK |
| 9 Misinformation / hype-watch | — | Carnitosis, carbfree, Ilana Muhlstein | OK (all candidate) |

\* handle from search summary only — confirm before use.

## D0b.5 Remaining gaps

1. **No individual Israeli doctor-nutrition creator verified** (cand-043, gap marker). Search surfaced institutions (obesity society, cand-042) but no physician running a public nutrition/metabolism feed. **Highest-priority discovery gap.**
2. **Matan HaBar's exact handle unresolved** (cand-028) — the single best fit, blocked only on handle verification. One manual lookup likely promotes him.
3. **Kids-food has no true social INFLUENCER** — only clinic dietitians. The active kids slot (Belzer) is service-oriented.
4. **Hebrew "accounts to follow" lists are culinary, not nutrition** — WebFetch of the Ynet and Mako lists returned recipe/food-styling creators (e.g. pasta, desserts), confirming a structural Hebrew blind spot: nutrition/label creators don't surface through mainstream food-curation lists and need targeted discovery.
5. **Audio (podcasts) and IG can't be auto-scraped** — il-030, cand-033/034 are manual-sweep; reinforces the D0 §7.3 social-access dependency.

## D0b.6 Verdict & recommendation

### **PASS WITH FIXES**

The Israeli creator layer is now real, verified, and honestly tiered: 9 active creators spanning 8 of 9 required types, with credibility and discourse kept on separate axes and every viral-thin account routed to `consumer_signal`/`misinformation_watch`, never to evidence.

**Fixes (quick, non-blocking for D1 design):**
1. **Promote Matan HaBar (cand-028)** once his handle is confirmed — top single improvement.
2. **Close the doctor gap (cand-043)** with one targeted search for an IL physician nutrition creator.
3. **Confirm the three summary-only handles** (cand-032/035/036) before any monitoring.

### Can D0 now close and D1 (scheduled-run design) begin?

**Yes.** The original closure blocker — thin Israeli creator coverage — is resolved (22 → 31 IL active; creator layer present across nearly all required types). The remaining items are *refinements tracked in candidates*, not gaps in the registry's fitness for a first run. **D0 can close; D1 may begin.** The one true cross-phase dependency is unchanged from D0 §7.3 — **decide the social-monitoring access model** (auto vs. manual sweep for IG/podcasts) before finalizing the D1 run's source list and cadence.

**Boundary held:** public sources only; no guessed handles; no scoring change; no Bari content; no trend report; no scheduled task created (Rule 10).

---
---

# D0c Addendum — US / European Creator Layer (+ owner-flagged IL adds)

**Date:** 2026-06-10 · **Trigger:** owner request to (a) add Yaniv Salman to the IL layer and (b) build the same creator/influencer layer for US/European sources (examples cited: Itay "Scheter", Andrew Huberman).

## D0c.1 What changed

| | After D0b | After D0c |
|---|---|---|
| Israeli active | 31 | **32** (+Yaniv Salman, il-032) |
| Global active | 26 | **34** (+8 creators, gl-027…034) |
| Total active | 57 | **66** |
| Candidate entries | 44 | **47** (cand-045/046/047; cand-014/015/022 → tombstones) |

**Global active market mix now:** US 19 · UK 5 · global 8 · EU 2.

## D0c.2 Creators added to ACTIVE (all handles verified as live profile links)

**Israel (1):**
- **il-032 Yaniv Salman** — primary handle confirmed **@yanivsalman120** (disambiguated 2026-06-10: a nutrition post on proper fruit-washing + consistent IG/TikTok/YouTube presence). @yan_sal_ left unused; a same-name *musician* excluded. `fitness_nutrition`, `credibility:LOW` until credentials confirmed, `discourse:high` → SIGNAL + `misinformation_watch`.

**US / European (8):**
| id | Creator | Handle | Market | Cred / Disc | Why |
|---|---|---|---|---|---|
| gl-027 | Andrew Huberman | @hubermanlab | US | low / high | owner-cited; huge reach, contested nutrition claims → signal + misinfo-watch |
| gl-028 | Prof. Tim Spector | @tim.spector | UK | med / high | ZOE co-founder; top UPF/microbiome communicator (distinct from gl-005 platform) |
| gl-029 | Prof. Giles Yeo | @gilesyeo | UK | **high** / med | Cambridge geneticist; rigorous diet/UPF myth-busting |
| gl-030 | Steph Grasso, RD | @stephgrassodietitian | US | med / high | ~2.4M, evidence-based debunking |
| gl-031 | Dr. Jessica Knurick, PhD RDN | @drjessicaknurick | US | **high** / high | leading evidence-based MAHA/food-policy critic — best US model for Bari's voice |
| gl-032 | Abbey Sharp, RD | @abbeyskitchen | global | med / high | anti-diet, fad-debunking podcast |
| gl-033 | Graeme Tomlinson "The Fitness Chef" | @thefitnesschef_ | UK | med / high | **tightest parallel to Bari** — exposes misleading "healthy" label/marketing spin |
| gl-034 | Itay **Shechter** "GFBEEF" | @gfbeef | US | low / high | owner-cited; ~802K exposing additives/processed food — same hook, appeal-to-nature risk → misinfo-watch |

**Two owner-name corrections (verified):** "Itay Scheter" → **Itay Shechter** (@gfbeef); Andrew Huberman was already a candidate (cand-014) and is now promoted.

## D0c.3 Credibility ≠ virality — how the global layer is tiered

The global creator layer deliberately **over-indexes on the evidence-based / myth-busting wing** (Yeo, Knurick, Grasso, Sharp, Tomlinson) because those are the models for Bari's own voice — then balances them with named high-reach/low-credibility hype (Huberman gl-027, Glucose Goddess gl-021, Hyman gl-023, Shechter gl-034, biohacker cluster cand-047). Two academics carry `credibility:high` (Yeo, Knurick); no creator is `evidence_reference`-only without also being a credentialed academic/clinician. Owner-cited high-reach names (Huberman, Shechter, Yaniv Salman) are tagged `misinformation_watch` precisely because reach ≠ reliability.

## D0c.4 Tombstones (promotion bookkeeping, QA)

cand-014 (Huberman → gl-027), cand-015 (Tim Spector → gl-028), and cand-022 (RD cluster → split into gl-031 Knurick + gl-032 Sharp) are set to `status: exclude` with pointers, so nothing is double-counted or re-monitored as a duplicate.

## D0c.5 Remaining gaps (updated)

1. **Continental-Europe (non-English) — DEFERRED by owner** (cand-046, 2026-06-10: "English only for now"). "European" coverage = **UK/English by design** for D1; continental-EU (DE/FR/ES) is explicitly out of scope and tombstoned so it isn't silently reopened.
2. Carried from D0b: IL individual **doctor**-creator (cand-043) and **Matan HaBar's** handle (cand-028) still open.
3. ~~Yaniv Salman primary-handle~~ — **RESOLVED**: @yanivsalman120 (il-032).

## D0c.6 Verdict & recommendation

### **PASS WITH FIXES**

The US/European creator layer now mirrors the Israeli one: 8 verified active creators spanning evidence-based RDs (US), academic communicators (UK), a label/marketing-truth coach (UK, closest to Bari), and named hype accounts — with the owner's specific adds (Huberman, Shechter, Yaniv Salman) placed and correctly tiered as signal, not evidence.

**Fixes (quick, non-blocking):** Yaniv Salman handle resolved (@yanivsalman120) and continental-EU deferred (English-only) per owner 2026-06-10 — both closed. Remaining open items are the prior D0b fixes (Matan HaBar handle, IL doctor-creator gap).

### D0 closure / D1 status
**Unchanged and reinforced: D0 can close, D1 may begin.** The creator layer is now strong in both markets (66 active sources). The single cross-phase dependency remains the **social-monitoring access model** (D0 §7.3) — and D0c *raises its weight*, since the global layer is now almost entirely Instagram, which cannot be auto-scraped. That decision (automated vs. manual-sweep for IG) should be settled as the first step of D1.

**Boundary held:** public sources only; no guessed handles (Yaniv Salman's two-profile ambiguity left open rather than guessed); no scoring change; no Bari content; no trend report; no scheduled task created.

---
---

# D1 Readiness Note — Daily Run Design

**Date:** 2026-06-10 · **Phase:** D1 (design only — run still not created). Accepts the D0 state: 66 active sources (32 IL / 34 global), 42 live candidates + 5 tombstones, watch terms validated, English-only global scope.

## D1 deliverables produced
- `project_comp_daily_run_prompt_v1.md` — the evening agent's operational prompt (role, inputs, source tiering, method, the 7 hard rules, self-check).
- `project_comp_schedule_spec_v1.md` — cron `30 20 * * *` Asia/Jerusalem; output paths; manual social-sweep cadence (IL 2×/wk, global weekly, candidates weekly) as **reminders, not scrapers**; failure handling; pre-flight checklist.
- `project_comp_output_template_v1.md` — the dated report: a mandatory **`## Context`** opening block (coverage checked vs not_checked, social mode, limitations, proposed registry changes) + 9 sections (exec summary · consumer concerns · competitor/creator moves · misinformation watch · category opportunities · content opportunities · scoring/methodology watchlist · source log · **Bari Assignment Queue**), with C/D separation baked into every creator/competitor line.
  - The **Bari Assignment Queue** is the operational closer: every actionable signal → exactly one primary owner (from 10 allowed agents) + ≤2 reviewers + action + priority + evidence status + next artifact + gate. Routing is enforced — scoring→research/nutrition first, consumer content→content+nutrition before publication, category→product before BSIP0, misinformation = signal-not-evidence; no-action → owner `none`/`monitor`.

## How the locked decisions are honored
- **Social-access = manual-periodic:** automated daily scope is `platform: web` only; every `instagram`/`tiktok` source is stamped `not_checked (last swept …)` — never fetched, never silently dropped (Rule 5).
- **Influencers = signal:** credibility and discourse are separate required fields in §3/§4 of every report; the misinformation watch is descriptive surveillance, and any counter-position is a gated §9 proposal.
- **Frozen invariants protected:** scoring/methodology items are watchlist *questions for Nutrition/Product*, never changes (tripwire #1). Project Comp proposes; it ships nothing — no scores, copy, claims, or registry edits.
- **English-only global:** continental-EU deferred (cand-046 tombstone); the run's global tier is UK/English.

## Open items (all minor, owner-side, non-blocking for design)
1. Confirm run time/timezone (default 20:30 Asia/Jerusalem).
2. Assign the **human owner** of the manual social sweeps (the automated run cannot do them).
3. Decide whether the optional sweep **reminder** crons are wanted.
4. Output dirs created on first run (`reports/comp/daily/`, `.../social_sweep/`).

## Verdict: **PASS WITH FIXES**
The daily run is fully specified and every locked decision is reflected. The "fixes" are the four
owner-side pre-flight confirmations above (§4 of the schedule spec) — none require more design.
**The scheduled daily run can be created** once those are confirmed. Per CLAUDE.md, creating a
recurring autonomous run is a program-start = **owner trigger**; Project Comp does not self-create it.
