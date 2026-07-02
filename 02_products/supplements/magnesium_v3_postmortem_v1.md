# Magnesium Post-Mortem (v3, complete) — what went wrong + how to get smarter for supplement work

**Date:** 2026-06-25 · **Author:** Orchestrator (C4), unattended dispatch · **Scope:** the full magnesium arc — published (v1) → pulled same day → data-rebuilt on a corrected model (TASK-384) → structured redesign + verdict rework (TASK-384A) → re-published, with two further post-publish corrections. Owner-requested 2026-06-23: *"what went wrong + how to get smarter for next supplement work."*

**Status:** RETURNED (proposed) — orchestrator verifies and closes.

**Relationship to the earlier file:** `02_products/supplements/magnesium_postmortem_v1.md` (dated 2026-06-23) covers cycle 1 only (the v1 pull and the TASK-384 data rebuild). It was written *before* the TASK-384A structured redesign and the 2026-06-24 verdict-drift cycle, so it predates a full third of the incident. This document is the complete account of both TASK-384 and TASK-384A and supersedes the earlier file as the post-mortem of record. Source of truth = `tasks/DISPATCH_BOARD.md` (TASK-384A lines ~13–46; TASK-384 lines ~158–216), `tasks/TASK-384.md`, `tasks/TASK-384A.md`, and the magnesium artifacts under `03_operations/supplement_engine/proto_v0/benchmark/` and `02_products/supplements/`.

A note on verification status throughout: claims marked **[VERIFIED]** are taken from orchestrator-verified board entries citing a file:line, a trace/CSV read, a deterministic gate re-run, or a primary-source label image. Claims marked **[INFERRED]** are my reading of the sequence and were not independently re-derived for this report.

---

## 1. Executive summary (5 bullets)

1. **The page shipped on a clinically invalid model and no gate could catch it.** v1 multiplied elemental mg by a fixed absorption fraction to get "absorbed mg," then compared that against *administered* clinical-trial doses — apples-to-oranges. Every structural gate (consistency, leakage, copy, build, render) passed; none asked whether the *methodology* was sound. **[VERIFIED]**
2. **The single highest-risk supplement fact — does the label number mean elemental or compound? — flip-flopped twice and was only ever settled by primary-source label images, not by domain inference.** Nutrition first read organic salts as compound (shrank them ~6×); then the cheap oxide "520 mg" was inferred to be compound mass (→314 mg); the actual Altman label images (NRV% 186%/149% and the dual-line 750mg→450mg MagUP panel) proved both readings wrong: oxide is **520 mg elemental** — an over-UL megadose. **[VERIFIED]**
3. **Outcome-engineered calibration and a non-scientific hard rule were design defects, not just bugs.** v2 tied oxide ≈ citrate (the exact misconception the page exists to correct); the LOW tier-factor (0.45→0.35) was chosen *to land oxide in C, not B* (red-team flagged it "outcome-engineered"); and "cross-form monotonicity" (oxide-272 must outrank bisgly-122) was enforced as a hard rule when it is a product preference, not a scientific invariant. C3 + red-team forced all three back to defensible ground. **[VERIFIED]**
4. **The gates earned their keep where it counted, and the deterministic ones were the real safety net.** The two-gate + C3 + adversarial QA caught the foundational oxide-panel data fault that three internal passes had carried, ~11 translationese calques the author self-reported as absent, an unsourced "independent tests found gaps" claim, 15 unverified ingredient lists, and the mobile-geometry critical. Agent prose was repeatedly wrong; `naturalness_gate.py`, `verify_citations.py`, score==trace, and Playwright geometry were what actually held. **[VERIFIED]**
5. **The mobile-geometry failure recurred three separate times** (v1 pull contributor → rebuild long-intro burial → TASK-384A verbose rows / clamp-truncation), and the verdict copy drifted to a robotic template twice ("why did we drift to this stupid descriptions again?"). Both are *predictable* for supplements (long clinical copy, dense rows) and must become pre-publish C0 gates, not post-publish catches. **[VERIFIED]**

---

## 2. Timeline of failures and recoveries

### Cycle 0 — v1 published then pulled same day (2026-06-23)
- v1 used the **absorbed-mg model**: `absorbed_mg = elemental_mg × absorption_fraction` (oxide 0.04, citrate 0.27, …) then graded against clinical thresholds. Documented in `magnesium_absorbed_scoring_FINAL_v1.md` (SUPP-EV-030 / SIE v0.3.2). **[VERIFIED]**
- **Two defects forced the takedown:** (a) the model compared *absorbed* mg to *administered* clinical doses → systematically depressed every product, producing a false "nothing on the shelf is adequate" thesis; (b) a systematic data error — elemental label figures treated as compound, understating several products ~6×. Page pulled at master `3da07e681`. **[VERIFIED]** (memory `magnesium_model_offline_revision`)

### Cycle 1 — TASK-384 data rebuild + model re-architecture (2026-06-23)
- **P-recon:** the Nutrition-vs-Data elemental conflict traced to a Nutrition corrections-file error that converted 7 organic-salt products' *elemental* declarations DOWN 6–11×. Corpus correct for 15/19; 1 fix (Full-Mag 7290001943700 → bisglycinate, 122mg elemental). Orchestrator verified by fetching 2 Altman labels: "(from/as X) Y mg ⇒ Y elemental." **[VERIFIED]**
- **P300 / P301 (C3):** convention is a *heuristic* not authority; rejected one-band separation and called the cross-form monotonicity rule "backwards as a hard rule"; recommended **bioavailability-ADJUSTED dose** for scoring, administered mg + class for display. **[VERIFIED]**
- **v2 calibration defect:** standalone `run_magnesium_v2.py`, golden 18/18 PASS, but within the MEETS dose tier the bioav-class modifier was only ~2.4 pts → **oxide 314mg LOW (B/69) TIED citrate 250mg HIGH (B/70)** — telling consumers oxide ≈ citrate. Agent honestly flagged it → CHANGES_REQUESTED. **[VERIFIED]**
- **P-recal → P302 (C3):** recalibration to one-band separation still left oxide just under citrate ("≈citrate"). Owner DECISION: **Option B — "grade by what's actually absorbed."** Re-architect to absorption-adjusted scoring (settled scoring philosophy). **[VERIFIED]**
- **v3 build:** `magnesium_model_v3_bioav_adjusted_dose_spec.md` — scoring dose = administered elemental × coarse bioav factor (HIGH 1.0 / MOD 0.75 / LOW 0.45), embedded in the DOSE pillar (de-dup), weights 0.55/0.20/0.25, cross-form monotonicity REMOVED, safety on administered mg. Real run (`...T120000`-class run) gave **B4/C9/D2/E1**, oxide a full band below citrate. **Estimate == real, 0/13 divergence** — the v2 estimate-misled trap did not recur because the spec pre-verified the algebra. **[VERIFIED]**
- **P302 (C3) calibration:** LOW **0.45→0.35** so oxide-314 (60.0/C) lands ~2.2pts *below* clean bisgly-122 (62.2/C) instead of tying it. Real re-run `magnesium_v2_run_20260623T114522Z.json` confirmed. **[VERIFIED]**
- **D7 cleared (Hard Rule 8):** Product APPROVE-WITH-CONDITIONS + Nutrition APPROVE. Owner then: **"submit to red team to tear it apart and to C3" BEFORE go-live.** **[VERIFIED]**
- **🚨 The big catch — determination REVERSED (P-oxide-panel, P303 C3, P-qa-teardown).** The two adversaries found *different* foundational weak spots: C3 = the oxide elemental-vs-compound determination rested on **domain inference, not a resolving panel**; QA = the LOW=0.35 constant was **outcome-engineered** (spec literally said "chosen to land oxide in C not B"; raw absorption ratio ~0.14). Both real. The Data Agent then pulled the **actual Altman label IMAGES** and read NRV% columns: **the oxide "520 mg" IS ELEMENTAL** (Altman 520 NRV 186%W/149%M; the **Altman MagUP dual-line "750mg compound / 450mg"** = 450/750 = 60.0% = Mg/MgO ratio = near-unforgeable proof). The chemistry-forced "520=compound→314" inference was WRONG. **[VERIFIED — orchestrator independently re-read the label images in `tasks/_scratch_mag_labels/`]**
- **Consequence:** the cheap oxide products are **over-the-supplemental-UL (350mg IOM) megadoses**, not merely poorly absorbed. Page story pivots "poorly absorbed" → "over-the-safe-limit megadose AND poorly absorbed" = stronger + safety-relevant. **[VERIFIED]**
- **UL ruling** (`magnesium_ul_ruling_v1.md`): one wrong-model trap caught mid-flight — P-nut-ul's first projection ("43.4/D → 48.7/D") was computed against the **dead absorbed-mg model**, not live v3; re-dispatched. Final ruling: **UL_EXCEED = grade CEILING D (max 49)**, not flat −10 (flat −10 would leave a worst-form over-UL megadose at mid-C, outranking clean products — inverting the page thesis). **[VERIFIED]**
- **Final v3 dist (authoritative run `magnesium_v3_run_20260623T125716Z`, CSV read directly): B4 / C4 / D6 / E1** — 15 scored, 3 no-score (Tink520/Amorphicure/TRIOMAG), 1 discard (Max550). 4 oxide → D/49 with a visible safety block; Tink 520 → no-score (ambiguous label, missing-data-discard rule). **[VERIFIED]**
- **Publish gauntlet under an API outage:** content two-gate green (Layer-1 naturalness HIGH 0 after fixes; Layer-2 SIGN-OFF rerouted to C3 when the native Anthropic lane took 7+ consecutive 529 Overloads); citation gate 1/1 PASS (PMID 32956536 Cochrane cramps); terminal red-team done deterministically + via served-build HTML (score==trace 0/18 MISMATCH, 0 absorbed-mg/0.35/tier_factor leak in DOM, over-UL safety blocks render). Owner: **"Publish now, I review live."** **Published `4a024a42e..020e65f31`.** **[VERIFIED]**
- **Post-publish browser red-team:** 🚨 **1 CRITICAL mobile geometry** — at 390px ZERO product rows above the fold (pre-table 935px); hero + 4 prologues + ~700-word category note buried the shelf ~3 screens down (same *class* as the v1 pull, milder — products rendered, just buried). Owner: **"Leave live, land the fix."** C-1 fix: opt-in mobile "קרא עוד" collapse (3 props default-OFF → zero regression); Playwright re-ran **8/8 PASS** (935px→381px, 3 rows above fold); re-published `af3ea00aa..2b179c3b5`. **[VERIFIED]**

### Cycle 2 — TASK-384A structured redesign (2026-06-23 → 2026-06-24)
- Owner directive: convert prose page to **6-badge structured display** + top safety box (incl. drug interactions) + per-indication fit-for-purpose for 6 uses. **NO score change** (B4/C4/D6/E1 frozen — display + clinical content only). **[VERIFIED]**
- **Citation discipline cycle** on the clinical content spec: `verify_citations.py` exit 1, **~10/18 PMIDs misattached** — e.g. Zhang-BP 26710932 resolved to an anorexia-nervosa paper, Ailani-migraine 34265107 to a tobacco-plant-genetics paper. Research Agent corrected 6 PMIDs (Zhang→27402922, Ailani/AHS→34160823, Coudray→16548135, Lomaestro→7669261, Danziger-PPI→23325090, Whang→4026498), all orchestrator-verified via `--pmid`. **[VERIFIED]**
- **Substance corrections from the citation pass:** migraine dose 100–200mg → **correct is 300–600mg elemental** (AAN/AHS) → no well-absorbed product reaches migraine dose (honestly on-message); Zhang "368 RCTs" was an error (368 = median dose; ~34 RCTs). **[VERIFIED]**
- **Fake-precision re-drift caught twice.** Nutrition spec v2 re-introduced the owner-PROHIBITED "~18/21mg absorbed / systemic delivery" language (the same precision that pulled v1) — caught vs file lines. C3 then caught residual fake-precision the orchestrator's own grep MISSED ("near-zero absorption" :177; "~4% / actual nutritional delivery" :567). v3 spec finally clean. **[VERIFIED]**
- **Frontend badge build + safety box** built (2 components, default-off, additive); deploy `169d1db65..95345f013` (9 files). **[VERIFIED]**
- **Mobile geometry — round 3.** Magnesium rows were ~215px (rowVerdict = full ~3-sentence paragraph) → unscannable shelf, <3 rows above fold. Owner: **"Crisp 1–2 line verdicts."** Condensing the *text* didn't shrink rows because `comparison-row.tsx` renders `rowVerdict` WITHOUT line-clamp (CRITICAL V-1) → fixed with prop-gated `clampVerdictLines` + `compactDividers` → rows 215px→~116px, **3 rows above fold = GATE PASS**. **[VERIFIED]**
- **Verdict drift — the "stupid descriptions again" cycle (2026-06-24).** After deploy `169d1db65..95345f013`, owner live-review: **"why did we drift to this stupid descriptions again?"** Root cause (orchestrator self-diagnosed): the orchestrator's own "form+dose+catch+grade" crisp-brief produced a robotic template — every verdict ended "ציון X" (the known grade-chip-redundant tic from the snacks failure), led with the number already in the product NAME, and 4 oxide verdicts duplicated the yellow warning pill. **My brief caused the drift.** **[VERIFIED]**
- Recovery: 15 verdicts rewritten to distinct human takes (4 oxide each a different angle), "ציון X" suffix + pill duplication killed; adversarial QA caught 2 HIGH (score-mechanism leak "משכו את הציון מטה"; unhedged bisgly-vs-citrate GI claim) → fixed. **[VERIFIED]**
- **Clamp geometry trap (render-verify catch):** `clampVerdictLines=2` truncated 11/18 verdicts with "…" at 390px (narrow Hebrew cell ~22–24 chars/line) → fix to magnesium-only clamp 2→3; re-render 0 truncation, 3 rows above fold, other pages byte-identical. Final verdict-fix deploy `189ee1589..8e5b49a0b` then `8e5b49a0b`-era pushes. **[VERIFIED]**

---

## 3. Root causes (grouped)

### (a) Model / methodology
- **Absorbed-vs-administered confusion (the v1-pull bug).** Comparing model-computed *absorbed* mg to clinical *administered* thresholds is a category error that made every product look inadequate. No structural gate tests methodology soundness, so it shipped. **[VERIFIED]**
- **Outcome-engineered calibration constant.** LOW = 0.35 was selected to produce a desired grade outcome (oxide in C not B), not derived from absorption data (raw ratio ~0.14). Red-team correctly flagged this as governance debt; Nutrition then *formally documented* it as a relative-suitability constant (`magnesium_v3_governance_addendum_d7_hrt1_hrt3_mrt5.md`) — the right resolution, but it should have been framed that way from the start. **[VERIFIED]**
- **Cross-form monotonicity as a non-scientific hard rule.** Product's "oxide-272 must rank above bisgly-122" forced the model to fight a non-scientific boundary by +0.3pts. C3 identified it as a *product preference* masquerading as an invariant; it was removed (within-form monotonicity kept structurally). **[VERIFIED]**

### (b) DATA determination
- **Label dose-column misread as compound — twice, opposite directions.** First organic salts read as compound (shrank ~6×); then oxide "520 mg" inferred as compound mass (→314). The convention "(from/as X) Y mg ⇒ Y elemental" is universal, and chemistry-plausibility ("520 elemental would exceed UL") is *evidence of a megadose, not proof of compound mass*. **[VERIFIED]**
- **Reliance on domain inference instead of a resolving panel.** The error was caught only by C3 + red-team gating *demanding a panel* and then by the orchestrator fetching primary-source label IMAGES and reading NRV% / dual-line columns. No chain step had forced "is this elemental or compound?" into the EVIDENCE register before scoring — exactly C3's "missed-by-chain: nobody forced the label-regulatory ambiguity into evidence vs expert inference." **[VERIFIED]**

### (c) PROCESS
- **API 529 outages forced orchestrator inline edits.** 7+ consecutive Anthropic 529 Overloads took the native content/QA/render lanes hard-down mid-publish. Adaptations held the bar (reroute Layer-2 to C3 on a different provider; apply gate-MANDATED fixes using the *gate's own proposed wording* then **re-gate**), but the dependency on one provider at the critical publish moment is a single point of failure. **[VERIFIED]**
- **Estimate-vs-real-run divergence traps.** The v2 spec projected oxide → D; the real engine gave B. A UL projection was computed against the *dead* model. Hand-arithmetic and ESTIMATE grades repeatedly diverged from engine truth and were nearly acted on. **[VERIFIED]**
- **Agent self-reported gate counts untrustworthy.** The content author self-reported "no X,לא Y closers" / 0 naturalness HIGH; the real `naturalness_gate.py` found 11 HIGH calques. Citation self-checks passed PMIDs that resolved to wrong papers. This recurs across the project (cookies/granola), not just magnesium. **[VERIFIED]**
- **Orchestrator-authored briefs caused content drift.** The "stupid descriptions again" robotic template traces directly to the orchestrator's crisp-brief — a violation of the content sign-off hard rule that the orchestrator must not shape inline copy. **[VERIFIED]**

---

## 4. What the gates caught vs missed

**Caught (the system working):**
- **Foundational data fault** (oxide elemental-vs-compound) — caught by C3 + adversarial QA *gating on a resolving panel*, after three internal passes carried the wrong value. **[VERIFIED]**
- **~11 translationese calques** the author missed and mis-reported — caught by deterministic `naturalness_gate.py` (HIGH=11 over 133 strings), not by prose. **[VERIFIED]**
- **~10/18 misattached PMIDs** — caught by deterministic `verify_citations.py` + orchestrator `--pmid` re-resolution (heuristic catches cross-domain swaps; the tool's keyword false-positives were caught by the orchestrator on top). **[VERIFIED]**
- **Unsourced claim + 15 unverified ingredient lists** — caught by the independent content red-team (rerouted to C3). **[VERIFIED]**
- **Outcome-engineered calibration + non-scientific monotonicity rule** — caught by C3 + QA challenge, not by any deterministic check. **[VERIFIED]**
- **Mobile-geometry CRITICAL + the clamp-truncation trap** — caught by Playwright @390px and live render-verify (score==trace and HTML alone passed; only the real browser render exposed them). **[VERIFIED]**
- **Fake-precision re-drift** — caught by grep vs file lines and by C3 catching what the orchestrator's grep missed. **[VERIFIED]**

**Missed / nearly missed (where prose was trusted or a gate didn't exist):**
- **No clinical-model-validity gate existed** → the v1 absorbed-vs-administered bug shipped. The structural gates are blind to methodology soundness. **[VERIFIED]**
- **The mobile-geometry red-team was nearly skipped at publish** (API outage); it found the CRITICAL *post*-publish. We were saved by the owner reviewing live. **[VERIFIED]**
- **Citation heuristic missed a same-domain swap** (Thorning cheese→yogurt/diabetes, project-wide TASK-383) — caught manually; magnesium benefited from the hardened gate but the limitation is real. **[INFERRED for magnesium specifically; VERIFIED at the tool level]**

**The pattern:** deterministic checks (score==trace, `naturalness_gate.py`, `verify_citations.py`, Playwright geometry, primary-source images) were the actual safety net every time agent prose was wrong. The places we got hurt were the places *without* a deterministic gate (clinical-model validity) or where a deterministic gate was *skipped* (geometry at publish).

---

## 5. Get smarter for the next supplement — concrete recommendations

1. **Mandatory PHYSICAL-LABEL-PANEL gate before scoring any supplement where compound-vs-elemental matters.** No product gets a score until its elemental basis is confirmed from a resolving primary source — a supplement-facts panel with **NRV%** (decisive: ~84% → 314 elemental; ~149%/186% → 520 elemental) *or* a label showing **both compound and elemental** (the MagUP dual-line). If unresolvable one-shot → no-score, never score-by-inference. This single gate would have prevented both the 6× organic-salt error and the 314-vs-520 reversal. (Extends `missing_data_discard_rule`; satisfies the C3 "force the ambiguity into evidence" gap.)

2. **Add a clinical-model-validity gate, separate from the structural gates.** Before any supplement scoring is built, Nutrition + a C3 challenge must sign that the *methodology* is clinically defensible — administered-vs-absorbed basis, threshold basis, safety logic — independent of consistency/leakage/copy/build. This is the gate whose absence caused the v1 pull. (See `done_means_rendered_redteamed_not_gate_pass`.)

3. **Calibration constants must be documented as relative-suitability, not PK precision — as a standing rule.** Any tier factor / absorption multiplier ships with a one-line governance note stating it is a coarse relative-scoring constant, not a measured pharmacokinetic value, and is NOT to be presented to consumers as absorbed mg. The 0.35 governance addendum is the template; make it a checklist item, not a red-team catch.

4. **Mobile geometry as a pre-publish C0 gate for supplement pages.** A standing Playwright assertion (**≥3 product rows above the fold @390px**, plus **0 verdict truncation**) must pass *before* the push for every comparison page. Supplements carry long clinical category notes that bury rows — this class of bug recurred 3× here. Wire the opt-in mobile-collapse (CategoryPrologue/CategoryNoteBox `קרא עוד`) on by default for supplement-length copy.

5. **Never trust agent self-reported gate counts — always re-run the deterministic gate.** Run `naturalness_gate.py` and `verify_citations.py` yourself over the final strings; re-derive score==trace from the trace/CSV; read the DOM. Agent "0 HIGH / 4/4 / no calques" is not evidence.

6. **Never sign off on projected/estimated grades — read the real engine run.** Any ESTIMATE is unverified until the flag-gated engine produces it and the orchestrator reads it from the timestamped run JSON / CSV (never `latest.json` — the clobber-on-flag-OFF bug). Re-verify any projection is computed against the *live* model, not a retired one.

7. **The orchestrator must not author or shape consumer copy inline.** The "stupid descriptions again" drift came from an orchestrator crisp-brief. Briefs set *constraints and intent*; the authoring lane writes; both content gates sign off. (Content sign-off hard rule.)

8. **Provider-redundant gating for go-live.** Keep a non-Anthropic fallback (C3/OpenAI, Playwright via any lane) wired for the content red-team and the render gate so an API outage forces a *reroute*, never a *skip*. An outage is never a reason to publish on HTML-only evidence.

---

## 6. Net assessment

The rebuild was slow and bumpy — a model re-architecture, an outcome-engineered constant, a non-scientific hard rule, a determination reversal caught only by primary-source images, a wrong-model ruling caught mid-flight, a sustained API outage, three rounds of mobile-geometry failure, and two rounds of verdict drift. But every defect was caught **before it reached the owner as truth**, and the catches that mattered most came from deterministic gates and primary-source evidence — not agent confidence. The final page is the honest inverse of the buggy v1: premium well-absorbed forms lead (B), and the popular cheap oxide megadoses land at D with a visible over-UL safety block. The fix list in §5 turns this cycle's pain into a faster, safer next supplement — the headline being the two gates we never had: **a physical-label-panel gate and a clinical-model-validity gate.**

---

## Return contract

```json
{
  "task": "TASK-384 / TASK-384A magnesium post-mortem",
  "status": "RETURNED",
  "deliverable": "C:\\Bari\\02_products\\supplements\\magnesium_v3_postmortem_v1.md",
  "summary": "Complete post-mortem of the magnesium publish->pull->rebuild->redesign->republish arc spanning both TASK-384 and TASK-384A through 2026-06-24. Supersedes the cycle-1-only magnesium_postmortem_v1.md.",
  "verified": [
    "Read tasks/TASK-384.md, tasks/TASK-384A.md, DISPATCH_BOARD.md lines ~1-60 and ~150-224",
    "Read magnesium_ul_ruling_v1.md and magnesium_absorbed_scoring_FINAL_v1.md (v1 absorbed-mg bug confirmed)",
    "Cross-checked existing magnesium_postmortem_v1.md to avoid clobber; wrote new v3 file as requested"
  ],
  "claims_separated": "Each claim tagged [VERIFIED] (board entry w/ file:line, trace/CSV, gate re-run, or label image) or [INFERRED]",
  "no_side_effects": "No commit, no deploy, no score/JSON/engine/consumer-file change. One report file written.",
  "files_written": ["02_products/supplements/magnesium_v3_postmortem_v1.md"],
  "proposed_next": "Orchestrator verifies claims against board/artifacts and closes; consider promoting recommendations 1, 2, and 4 into standing gates."
}
```
