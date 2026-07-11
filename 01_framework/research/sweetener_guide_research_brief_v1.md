---
document: sweetener_guide_research_brief_v1
task: TASK-557
owner: research-agent
requested_by: owner (2026-07-10)
status: BRIEF — evidence pull not yet run
consumes: EV-004 (allulose), EV-005 (polyol osmotic threshold), EV-017 (sweetener gut dysbiosis)
produces: evidence table only — NO consumer copy, NO tier proposals, NO scoring change
gates_required: two-gate content sign-off (Content Agent + Adversarial QA/Red-Team) before any owner review
---

# Sweetener Consumer Guide — Research Brief v1

**Purpose.** Assemble the evidence base for a consumer-facing sweetener guide under `/madrichim`.
This brief commissions **evidence only**. Consumer copy is authored later by the Content Agent and
must clear the Adversarial QA / Red-Team gate before it reaches the owner.

---

## Premise corrections (do not inherit the pitch's assumptions)

1. **The Israeli sweetened-beverage tax was REPEALED in March 2023.** The guide pitch described a
   "post-sugar-tax reformulation wave." There is no active tax. Whether reformulation persisted
   after repeal is an open question (see Q-D), not a premise. Do not assert it.
2. **EV-017 is stale against the engine.** It states "current BSIP2 treats all non-caloric
   sweeteners as neutral." The engine already applies a Tier A/B/C sweetener penalty
   (`constants.py:285-287`) plus polyol tier penalties. Describe the engine, never the EV, if the
   guide references what Bari does.
3. **EV-017 files erythritol as "neutral."** That predates the 2023 cardiovascular/thrombosis
   signal. Treat erythritol's tier as an open question, not settled.

---

## Q-A IS ANSWERED — measured in-house 2026-07-10 (do not re-run; build on it)

Corpus scan over `02_products/`, deduped to distinct `(category, product)` records carrying
ingredient text. **Denominator: 1,922 products. 119 (6.2%) carry any sweetener.**

| Sweetener | Products | % corpus | Concentrated in |
|---|---|---|---|
| maltitol (E965) | 57 | 3.0% | snack_bars (33), chocolate (8), cookies_coffee (8) |
| sucralose (E955) | 54 | 2.8% | snack_bars (25), yogurt (18) |
| sorbitol (E420) | 29 | 1.5% | cakes_hard_cookies (14), snack_bars (12) |
| stevia (E960) | 18 | 0.9% | snack_bars (5), cereals (4), chocolate (4) |
| acesulfame-K (E950) | 15 | 0.8% | yogurt (14) |
| erythritol (E968) | 11 | 0.6% | snack_bars (4) |
| xylitol (E967) | 6 | 0.3% | snack_bars (5) |
| isomalt (E953) | 2 | 0.1% | cookies_coffee |
| monk fruit | 2 | 0.1% | — |
| **saccharin (E954)** | **0** | 0.0% | absent |
| **aspartame (E951)** | **0** | 0.0% | absent |
| **allulose** | **0** | 0.0% | absent |

Family roll-up (deduped across members): polyols **85** (4.4%), synthetic high-intensity **55**
(2.9%), plant-derived **20** (1.0%).

**Consequences that reorder this brief:**
- **EV-004 (allulose) has zero shelf relevance.** Allulose appears on no product Bari has scored. It
  cannot anchor or lead the guide. Keep as reference; flag EV-004 for a staleness note.
- **Aspartame and saccharin are absent.** The two most publicly feared sweeteners are on none of
  these shelves. EV-017 names saccharin as a high-risk sweetener; saccharin has zero presence, so
  only the **sucralose** arm of EV-017 has shelf relevance.
- **EV-005 (polyol osmotic threshold) is the highest-value EV, not EV-004.** Polyols dominate at 85
  products, led by **maltitol (57)** — the most common sweetener on the shelf and the one with the
  least public discussion.
- Erythritol is a **minor** shelf presence (11), despite carrying the loudest recent headline.

### Q-A residual (still open)
- **Israeli regulatory status of allulose.** Israel MoH has published a D-allulose novel-food
  guidance (`gov.il`, `fcs-35388024-d-allulose`); the PDF returned HTTP 403 to automated fetch and is
  **unverified by primary read**. The EU has **not** authorised allulose: EFSA (June 2025,
  DOI `10.2903/j.efsa.2025.9468`) concluded safety "cannot be established" because the applicant did
  not supply requested data. Confirm the Israeli position by primary read. Low priority — shelf
  presence is zero either way.
- Monk fruit (mogroside V) regulatory status in Israel.

### Q-B — Per-sweetener evidence
**Priority order follows the measured shelf, not fame.** Depth required, most first:
**maltitol, sucralose, sorbitol, stevia, acesulfame-K, erythritol, xylitol.** Then, briefly:
isomalt, monk fruit. Aspartame, saccharin and allulose get a short "why it is not here" note only.

**Scope narrowed by owner ruling 2026-07-10.** The guide is descriptive: what a person is consuming,
where it appears, and what the evidence says with its caveats. It gives no advice and no personal
threshold. This **demotes the maltitol dose question from blocking to valuable.** The guide can
explain the mandatory polyol laxative warning that Israeli labels already carry, without telling any
individual how many grams they may eat.

**Still the most useful open question:** the evidence on **maltitol** — the most common sweetener on
Bari's shelf — for osmotic/GI tolerance, its dose threshold, its glycemic response relative to
sugar, and how it compares with erythritol on tolerability. Public discussion of sweeteners almost
never names maltitol. Answer it if the evidence exists; record "not established" if it does not.

For each of: maltitol (E965), sucralose (E955), sorbitol (E420), steviol glycosides (E960),
acesulfame-K (E950), erythritol (E968), xylitol (E967), isomalt (E953), monk fruit:
- Current regulatory status and ADI: EFSA, JECFA, Israeli MoH. Note any divergence between them.
- Human interventional evidence (RCTs) on glucose tolerance and microbiome. Distinguish RCT from
  observational, and note responder heterogeneity where reported.
- **The erythritol/xylitol cardiovascular signal.** Witkowski et al., *Nature Medicine* 2023
  (DOI `10.1038/s41591-023-02223-9`, PMID `36849732`), and the 2024 xylitol follow-up.
  **Pre-established, do not re-derive:** the paper's US (n=2,149) and European (n=833) validation
  cohorts are *internal to the same paper and research group* — that is internal validation, and it
  is **not** independent replication by another group. Confirm or refute that framing.
  **The decisive caveat:** plasma erythritol is substantially produced **endogenously** via the
  pentose phosphate pathway, and rises with hyperglycaemia and oxidative stress. Plasma level
  therefore may not reflect *dietary* intake at all, and may be a **marker of** cardiometabolic
  disease rather than a cause of it (Mellor, Sanders, via Science Media Centre; see also
  *Frontiers in Nutrition* 2023 on plasma erythritol vs dietary intake). Establish how strongly the
  literature supports this. **FDA, EFSA, and national authorities have not changed their erythritol
  assessments in response to Witkowski** — verify and cite this.
  Then answer: is a person eating a sweetened product exposed to anything the study actually measured?
- **The aspartame case.** IARC classified it 2B (2023) while JECFA reaffirmed the ADI in the same
  week. This is the canonical consumer-confusion object. Establish exactly what each body said and
  what the two statements do and do not mean together.
- What has changed since EV-004, EV-005, and EV-017 were filed?

### Q-C — Consumer confusion (validate the pitch's core claim)
- Is there evidence that Israeli consumers genuinely confuse stevia / sucralose / erythritol?
  Hebrew search queries, rising-query data, published survey work. If the confusion cannot be
  evidenced, say so — the guide's premise weakens and we should know before building.

### Q-D — The reformulation claim
- Did the 2023 repeal reverse reformulation, or did reformulated (sweetener-containing) variants
  persist on Israeli shelves? Cite retail or industry data, or return "not established."

### Q-E — Label derivability
- Which of the distinctions above are visible on an Israeli label at all? A distinction that cannot
  be read off a label cannot drive anything Bari publishes per-product. Mark each finding
  `label-derivable: yes/no`.

---

## Hard constraints (violating any of these invalidates the return)

- **Open Food Facts is banned.** Any field, any purpose, forever. Unknown is acceptable; OFF is not.
- **Every claim carries a primary citation** (DOI or PMID). The return is run through
  `03_operations/validators/verify_citations.py`. Agent-supplied identifiers are **not trusted** —
  a fabricated or mismatched PMID fails the return outright.
- **Missing data is discarded, never substituted.** If a value is not found in one pass, the field is
  NULL. Do not fill it from a secondary source.
- **Do not write consumer copy.** Do not draft headlines, insight lines, or explanations.
- **Do not propose tiers, scores, or penalties.** Anything that would move a published score is a
  D6/D7 matter and an owner tripwire. Flag it; do not act on it.
- **Never expose internal vocabulary.** The words `contested`, `likely-neutral`, `confirmed-negative`,
  NOVA, BSIP, cap, floor, and structural_class are internal data-state. They must not appear in
  anything a consumer will read. Consumer copy narrating data-state is the standing owner ruling
  (2026-07-08) and the most serious copy failure on record.
- **No health claims and no alarm framing.** Bari scores nutritional architecture; it does not advise
  on health outcomes. DEC-006's alarm-framing prohibition binds every tier.
- **Separate verified from believed.** State how each fact was verified. Where evidence conflicts,
  present the conflict; do not resolve it by picking a side.

---

## Deliverable

1. **Evidence table**, one row per sweetener: Hebrew name, E-number, regulatory status (EFSA / JECFA /
   Israeli MoH), ADI, human-evidence summary, evidence strength (Strong / Moderate / Weak /
   Insufficient), `label-derivable` yes/no, primary citations.
2. **Gating answer to Q-A** on allulose and monk fruit availability in Israel, stated up front.
3. **Contradiction log:** every place the evidence conflicts, including conflicts with EV-004/005/017.
4. **"What we cannot say"** section: the claims the evidence does not support. This section is
   mandatory and is the most important part of the return.
5. Return Contract JSON per `01_framework/operations/return_contract_v1.md`.

## Explicitly out of scope

Guide structure, page design, route wiring, Hebrew copy, tier assignment, and any scoring change.
Those follow the evidence; they are not part of this pull.
