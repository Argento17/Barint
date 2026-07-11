# Magnesium Guide — Bar Revision Call v1 (TASK-504, Wave 1)

**Author:** Product Agent
**Scope:** Owner feedback on the rendered magnesium guide (golden guide, /madrichim/magnesium). Decision-only — no code, no rubric file edited. Proposals for the Nutrition co-signer and the orchestrator to route.
**Inputs read:** `01_framework/nutrition/supplement_guides_bar_rubric_v1.yaml`, `01_framework/product/supplement_guides_concrete_plan_v1.md`, `C:\bari_wt_t504\bari-web\src\lib\guides\magnesium-guide-data.ts`, `C:\bari_wt_t504\bari-web\src\lib\view-models\guide.ts`, `C:\bari_wt_t504\bari-web\src\components\shared\bar-state-badge.tsx`, `C:\bari_wt_t504\bari-web\src\lib\comparisons\creatine-page-data.ts` (premise check for the creatine counter-case).

---

## Premise check (Hard Rule 10, done before the calls below rest on it)

Ran a structural parse of every `bars()` call in `magnesium-guide-data.ts` (19 matches; 1 is the function signature, correctly excluded → n=18 products).

- `thirdPartyVerification`: **cannot_verify 18/18** (source: `magnesium-guide-data.ts`, parsed via `python3` regex over all `bars(...)` calls, this session).
- `priceFairness`: **cannot_verify 18/18** (same source, same method).
- Creatine counter-case confirmed real, not assumed: `creatine-page-data.ts` shows 7 rows with `"directory_verified"` (NSF registry match) vs. multiple `"manufacturer_stated"` rows for `thirdPartyVerification`, and populated `price_per_3g_label` values (e.g. `₪0.89`, `~$0.27`, `~$0.19–0.26`) for `priceFairness` — both bars carry real variance for creatine. The owner-feedback premise ("these two bars are dead specifically for magnesium, not universally") holds.
- Badge rendering confirmed: `bar-state-badge.tsx` renders only the state label (e.g. "לא ניתן לאמת"); the bar name and any note are folded into `aria-label`/`title` — screen-reader- and hover-only, not visibly persistent. This confirms owner complaint #2 as a real gap, not a perception issue.

---

## A. price_fairness bar — recommendation: **fast-follow acquisition, suppress the bar in the meantime**

**Call:** Israeli magnesium pricing collection is **NOT in scope for Wave 1**. It becomes a tracked fast-follow task (Data Agent scrape), opened this session as a named gap, not silently dropped. Until that data exists, **suppress the price_fairness badge from the per-product row** for this guide build (see rule in C) rather than render "cannot_verify" 18 times.

**Rationale:** This is a data-acquisition gap, not a rubric defect — the rubric's own math is sound and already proven on creatine. Blocking the golden-guide launch on a full pricing scrape recreates exactly the failure the plan already named and guarded against: the frozen-veg stall precedent (plan §7, red-team RT-A7 — "spec-then-stall"). The plan's own build-order mitigation is "ship in ONE build wave" — making Wave 1 wait on new data collection breaks that. Suppressing the dead badge is reversible and costs nothing; the pricing collection itself is real, tracked work with its own timeline, not a Wave-1 gate.

**Scope note tied to the owner's own strategy:** the owner's approved plan explicitly wants price differences shown (concrete plan §2, bar 4). Suppressing the bar is not shelving that ambition — it is refusing to fake it with 18 identical "cannot verify" pills while the real fix (collect the prices) is pending. Silence-with-a-stated-reason beats a decorative badge that says nothing 18 times.

---

## B. third_party_verification bar — recommendation: **suppress for this guide build, same rule as A, different underlying cause**

**Call:** Suppress the per-product badge for this bar in this guide build, under the same corpus-uniformity trigger as A — but the *disclosure text* must say something different, because the underlying fact is different. For magnesium, no product in the 18-product corpus makes a certification claim at all (the guide's own copy already states this: "אף מותג מגנזיום במדף לא פרסם טענה כזו כלל" — this is a market fact, not a Bari collection gap). For price, the data exists in principle and Bari hasn't collected it yet. Conflating the two in copy would misattribute a market-structure fact as a Bari data gap (the same distinction the rubric itself already draws for `label_transparency` vs. Bari-sourcing gaps).

**The rule that decides render vs. suppress (applies to both A and B identically):** stated in C below — it is corpus-uniformity-driven, not a hardcoded per-bar or per-guide exclusion. This matters because the same bar (`third_party_verification`) discriminates for creatine (7/N directory-verified) and must stay fully rendered there. A rule that says "don't show third-party-verification for supplements" would be wrong; the rule has to say "don't show a badge that carries the identical state for every displayed product in *this* guide, this build."

---

## C. The render/suppress rule (rubric-governance addition — proposed text)

Proposed insertion into `supplement_guides_bar_rubric_v1.yaml`, as a new top-level section (`display_suppression_rule`), written in the file's own style:

```
display_suppression_rule:
  trigger: >
    At guide-build time, for each of the 6 bars independently: if that bar's computed
    state is IDENTICAL for every product in the guide's currently displayed corpus
    (100% — not "mostly" or "90%+"), the per-product BADGE for that bar is not rendered
    in the product table/rows for this guide's build.
  why_100_percent_only: >
    A partial-uniformity bar (even 17/18 identical) still carries real signal for the
    non-matching product — suppressing it would hide the one actionable finding. Only
    total uniformity carries zero per-product discriminating information.
  what_still_happens_when_suppressed:
    - "The bar's STATE is still computed and still feeds bucket_logic exactly as before —
       this is a DISPLAY rule only, never a computation rule. Bucket math (clears_all /
       passes_with_flag / fails / cannot_assess) is unchanged and continues to evaluate
       all 6 bars. This preserves the honest '0/18 clear every bar' finding without
       having to touch, re-derive, or re-approve the bucket logic itself."
    - "The bar is NOT deleted from the buying-rule explanation layer (layer 1) — the
       reader still learns what the bar checks and why it matters."
    - "A single, guide-level disclosure line states plainly: which bar(s) were
       suppressed, the count (e.g. '18/18'), and WHY — split into the two honest
       reasons distinguished above: 'not yet collected' (a Bari data gap, e.g. price)
       vs. 'no claims exist in this market to check' (a corpus fact, e.g. certification
       claims). This line is Content-authored and goes through the same two-gate
       sign-off as any other consumer-facing string — this config states the rule, not
       the shipped wording."
  re-evaluated_per_build: >
    This is computed fresh at every guide build from the live corpus, per the standing
    re-flow doctrine ("nothing is frozen"). It is NOT a hardcoded exclusion list keyed
    to a bar name or a guide slug. The same bar renders normally wherever it
    discriminates (e.g. third_party_verification and price_fairness both render fully
    on the creatine guide, where they carry real variance).
  honesty_constraint: >
    A suppressed bar is disclosed, never silently vanished. "Not assessed this round"
    must be stated in guide-level copy near the product table, not just buried in an
    upstream paragraph the reader may have scrolled past.
```

**Anti-drift invariant check (Hard Rule 1 of the rubric):** compliant. No numeric aggregate, no bar-state combining, no new 5th state. This is a presentation-layer rule that changes which badges render; the bucket computation itself is explicitly untouched, which is the more conservative and lower-risk option than trimming the bar count used in bucket math (a subset-bucket redefinition would itself be a scoring-presentation logic change needing its own fresh D6/D7 pass — I am deliberately not proposing that).

**Missing-data-discard doctrine check:** compliant. That doctrine governs how missing data affects a *product's* standing (never punish/cap); it says nothing about display deduplication of an identically-repeated state across an entire table. No product's bucket outcome, bar-state, or copy changes under this rule — only the redundant per-row badge disappears in favor of one clear guide-level statement.

**Nutrition D7 co-sign required:** yes, flagged explicitly. This is a new addition to a rubric config whose own governing text (`supplement_guides_bar_rubric_v1.yaml` meta block) states it is "PROPOSED — Product Agent D7 co-sign required," and the config's own enforcement clause requires "a fresh Product + Nutrition D6/D7 review" for any new rule layered on top of it. Route to Nutrition Agent for co-sign on: (1) the 100%-only threshold, (2) that suppression-without-recomputation is the scientifically honest reading of "not applicable this round" vs. a deduction, (3) the exact two-reason disclosure split (collection gap vs. market-absence) doesn't overstate or understate either case.

---

## D. Bucket header replacement

**Current:** `הרשימה המעשית להתחיל ממנה` ("the practical list to start from") — used as `promotedShortlistLabel` in `magnesium-guide-data.ts` line 380, and repeated as the section heading directly above the product table.

**Problem:** it reads as an endorsement ("start from here") without stating the actual inclusion criterion. The correct explanation already exists one paragraph earlier in `headlineFinding.body[2]` ("חמישה מוצרים עוברים עם דגל, כלומר אף סף לא נכשל אצלם, אבל לפחות אחד מסומן כחלקי או לא ניתן לאימות") — but a reader scrolling to the table sees only the promoted label again, disconnected from that sentence.

**Recommendation:** replace the header with one that states the criterion inline, so it stands on its own without requiring the reader to have retained the earlier paragraph:

> **"5 מוצרים בלי כישלון בשום סף (כל אחד עם דגל אחד לפחות)"**
> (5 products with no failure on any threshold — each still carries at least one flag)

**Why this framing:** states the actual bucket-membership rule ("no FAIL bar") as the headline fact instead of an implied recommendation; states the caveat ("still has ≥1 flag") in the same breath so it can't be read as an endorsement; carries the number (5) per the standing consumer-translation-label convention; uses no "X, not Y" antithesis; uses a parenthetical instead of an em dash. This is a **direction recommendation**, not final shippable copy — it still requires Content Agent authorship/polish and two-gate sign-off (Content + Adversarial QA) before it reaches the page, per the standing content sign-off hard rule. I am not authoring final consumer copy here; I am correcting the *comprehension defect* the owner named.

---

## Out of scope for this call (flagged, not resolved)

- **Infographics** (owner ask #4): a Design/Frontend visual-execution request, not a bar-rubric or bucket-language decision. Recommend routing to the Design Agent as a fast-follow visual pass on the existing (post-fix) bar/bucket structure — do not fold into this rubric-governance change, to avoid scope creep on a decision that's supposed to be a targeted refinement, not a redesign.
- **Persistent, non-hover bar-context on the badge itself** (the deeper fix behind owner complaint #2, beyond the two dead bars) — a Frontend/Design component change to `bar-state-badge.tsx` (e.g., a visible micro-label or always-on caption instead of aria/title-only). I'm flagging the defect and its evidence (component read above); the component-level fix is Frontend's to implement and Design's to approve, not mine to spec here.

## Scope risk

1. If A's fast-follow pricing collection slips and someone later tries to gate golden-guide launch on it, that recreates the frozen-veg stall (RT-A7) the plan explicitly built around. Track it as its own ticket with its own owner (Data Agent), not a go-live blocker.
2. If the render/suppress rule in C is implemented as a hardcoded "hide price+cert for magnesium" special case instead of the corpus-uniformity check, it silently breaks the moment magnesium pricing data lands (bar would need to un-suppress) and it never generalizes to creatine or future guides. The rule must be re-evaluated per build, not hand-coded per guide.
3. Nutrition D7 co-sign on C is a real gate, not a formality — do not ship the suppression behavior before that sign-off lands, per Hard Rule 8 (scoring/rubric-adjacent approval requires both Product and Nutrition).

---

```json
{
  "task": "TASK-504-magnesium-guide-bar-revision",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": "03_operations/reports/product/magnesium_guide_bar_revision_call_v1.md", "action": "created", "sha256": "5efe3eba34580b005f41b34cbbd57b81d9ff9797a8143c9f2a8c0b811b5ead5f (hash of pre-edit content; this JSON edit changes the final byte content — orchestrator's validate_return.py re-hashes the committed file at close, per its own C0 gate)"}
  ],
  "counts": {
    "third_party_verification_cannot_verify": "18/18 (source: C:\\bari_wt_t504\\bari-web\\src\\lib\\guides\\magnesium-guide-data.ts, parsed via python3 regex over all bars() calls, this session)",
    "price_fairness_cannot_verify": "18/18 (same source, same method)",
    "creatine_directory_verified_rows": "7 rows found (source: grep over C:\\bari_wt_t504\\bari-web\\src\\lib\\comparisons\\creatine-page-data.ts, string 'directory_verified', this session) — cited as evidence the same bar discriminates for creatine, not a full corpus n"
  },
  "commands_run": [
    {"cmd": "python3 -c \"parse bars() calls in magnesium-guide-data.ts and Counter() third/price args\"", "exit_code": 0},
    {"cmd": "grep -oP 'bars\\([^)]*\\)' src/lib/guides/magnesium-guide-data.ts | ... | uniq -c (initial single-line pass, undercounted due to multiline formatting, superseded by the python3 regex pass above)", "exit_code": 0}
  ],
  "not_done": [
    "No code, rubric YAML, or copy file was edited — this is a decision report only, per the task's explicit instruction.",
    "Nutrition D7 co-sign on the render/suppress rule (C) has not been obtained — flagged as required, not sought in this pass.",
    "Final consumer-facing bucket header copy (D) not authored to ship standard — direction only; Content Agent authorship + two-gate sign-off still required.",
    "Infographics request (owner item 4) and persistent badge-context component fix not scoped — explicitly named as out-of-scope fast-follows, routed to Design/Frontend."
  ],
  "self_check": "Acceptance test: every quantitative claim in this report cites a named artifact/command (Hard Rule 9) and the price/cert premise was verified against the live worktree file before the calls rested on it (Hard Rule 10). Observed: both counts (18/18, 18/18) reproduced via an independent parse; creatine counter-case confirmed via grep before being used to justify the corpus-uniformity (not bar-identity) framing of the rule in C."
}
```
