# TASK-476 Return — Product Agent Strategic Co-Sign on Bread/Crackers/Protein-Bars Re-flow

**Role boundary honored:** this is a judgment call on acceptability, sequencing, and
downstream requirement — not a re-derivation of numbers. Every figure below is cited
from `C:\Bari\tasks\returns\TASK-475_return.md` (the TASK-475 trace). I changed
nothing, ran no pipeline, spawned no sub-agents.

## Verdict: CO-SIGN

Re-flow bread, crackers, and protein-bars together, in one pass, now.

## Rationale (one paragraph, owner-readable)

The bug made 57 live products invisible to the engine's own additive/NOVA scrutiny —
not a scoring philosophy change, a data-visibility bug that let real ingredient signal
sit unread (TASK-475 root cause: `input_loader.py::get_ingredients()` never fell back
to the populated `ingredient_order`/`ingredients_text_he`). Every one of the 8 grade
movers goes down (TASK-475 counts: `grade_movers_direction: {down: 8, up: 0}` of 57),
because previously-hidden NOVA/additive signal now fires — that is the fix working as
intended, not a regression. This is exactly the class of correction the de-anchor /
honest-grades doctrine (`owner_s_grade_honesty_ruling`) and the missing-data-discard
rule already commit Bari to: don't let a data gap manufacture an inflated score. The
flagship bread product stays S-tier (94.8→90.8, TASK-475 line 114 context — no grade
change), and 49 of 57 products (86%) don't move grade at all (TASK-475 counts:
`grade_movers: {value: 8, denominator: 57}`). The optics cost is small and defensible —
8 products losing an undeserved letter grade is not a story that damages Bari;
publishing scores we know are wrong while a competent fix sits reviewed and ready would
be the actual reputational risk. Holding this to protect 8 products' current grade
optics would put system credibility behind product-count optics, which is backwards.

## Q1 — Strategic acceptability: CONFIRM GO

Correcting inflated scores downward when the underlying data-visibility bug is fixed
is not optional under Bari's own standing rules — it's the honest-grades and
de-anchor doctrine applied to a concrete case. No strategic concern raised. The
asymmetry (TASK-475: mean Δ −1.39, all 8 grade-line crossings downward, 34/57 products
negative vs 5/57 positive) is exactly what you'd expect from a visibility fix that
un-hides previously-unscored additive/processing penalties — it is not a sign the fix
is miscalibrated or punitive.

## Q2 — Scope / sequencing: re-flow all 3 together, no staging, no delist

- **All three in one pass.** They share one root cause and one fix
  (`input_loader.py` fallback). Staging bread+crackers now and protein-bars later
  would mean shipping a category (protein-bars) with a known-open scoring bug for no
  benefit — the fix is already validated end-to-end on all 57 products with 0 rescoring
  errors (TASK-475 counts: `rescoring_errors: {value: 0, denominator: 57}`).
- **Protein-bars being "only half-affected" (15/32) is not a reason to split it out** —
  it's a reason the category needs the same pass, since the other 17 already score
  correctly and would be untouched by the fix; splitting adds a second re-flow cycle
  and a second round of copy re-audit for no risk reduction.
- **No category should be delisted.** Nothing here indicates the underlying products
  are unsellable or the category thesis is wrong — this is a scoring-engine input bug,
  not a corpus-quality failure. Delisting would be a disproportionate response to a
  fixed plumbing defect.
- **Launch-timing:** these are live categories, not a pending launch — "launch
  sequencing" doesn't apply here in the D1 sense. The only timing consideration is
  standard: fix → re-flow → re-audit copy → both gates + red-team → owner deploy
  decision. No reason to delay once Nutrition Agent has signed off on the fix itself
  (this co-sign covers product/scope; per Hard Rule 8 the scoring-rule
  implementation still needs Nutrition Agent's own sign-off if not already given).

## Q3 — Consumer-facing consequence: guardrail affirmed

Confirmed and binding, not optional: since this changes published grades on live
categories, every score-dependent copy string (verdicts, insight lines, expansion text
that names a grade, score, or "A"/"B"/"C" band) for the 8 grade-movers — and ideally all
57 re-scored products, since near-miss point changes can make an existing verdict read
oddly even without a grade-line crossing — must be re-audited before deploy. TASK-475
itself flags a live landmine here: protein-bars carries an `OLD_CAVEAT` "no ingredients
found" string (`02_products/snack_bars/staging/run_pb_standard_20260625_062614/fix_ingredients.py`,
per TASK-475's "What could NOT be measured" section) that will be factually false the
moment ingredient visibility is restored — that copy must be caught and rewritten, not
left stale. Per standing hard rules: both page gates (`validate_comparison_page.py`
7/7 and `run_gates.py` G1–G8) and the two-gate content sign-off (Content Agent +
Adversarial QA/Red-Team) must pass before this reaches the owner for the go-live
decision. I am affirming this requirement, not executing it — routing to Nutrition
Agent (fix sign-off), Data Agent (implementation), Content Agent + Adversarial QA
Agent (copy re-audit + two-gate), and the orchestrator (dispatch, gate verification,
close) is the orchestrator's call to sequence.

## Router_v2 delta (Finding 1)

**Verdict: CO-SIGN**

**What I did and did not verify.** I have not independently read `router_v2.py`, the
REQ-362-R2 threshold, or re-derived the 13→18 miscount — those are Nutrition's
independent code-read, not mine, and I am not re-deriving them (Hard Rule 9/10: a
number I haven't traced myself I attribute to its source, not restate as verified).
What I *am* ruling on is the shape of the change, which is unambiguous from the
description and consistent with what Nutrition confirmed: a single-consumer counting
function fed a routing decision, it undercounted on one product, got corrected, and the
correction points at the same fixed counting logic already covered by this co-sign.

**Why this doesn't need a fresh strategic review.** A product moving *scoring tables*
(bread vs. protein-bar/granola matrix) is a bigger structural change in the abstract
than a product moving *grade*, so it's fair to ask the question. But three things
collapse it back into the already-approved scope rather than opening a new one:

1. **Same root cause, same fix vector.** This is not a second bug — it's the same
   ingredient-counting defect this task already exists to correct, surfacing in a
   second call site (routing) instead of scoring. Co-signing "fix the counter" already
   implied fixing every place that counter feeds a decision. Treating the router path
   as a separate approval would be gating the same fix twice.
2. **Direction is corrective, not novel.** The bread was misrouted into the wrong
   table and scored *worse* than it should have (mis-route risked dropping it to A);
   the fix keeps it at its correct S. That's the fix protecting the flagship product's
   correct grade, not moving it — there is no new downward surprise to weigh.
3. **Blast radius and mechanism are both bounded.** One product, one deterministic
   threshold check, one confirmed single downstream consumer (per Nutrition's
   independent verification as relayed) — this is a narrow plumbing correction, not a
   new scoring rule, new weight, or new category boundary. It doesn't change what
   "protein-bar matrix" or "bread" means; it changes which one a single miscounted
   product correctly falls into.

**Does a product moving between scoring tables ever raise a strategic concern on its
own?** Yes, in general — reclassifying products across category boundaries is exactly
the kind of change that *should* stop and get a fresh look, because it can look like
quietly gaming a product's outcome by choosing a friendlier rubric. That is not what
this is: the classification was wrong due to a counting bug, not chosen, and the
correction is auditable to a single fixed function with one consumer. If a second
product outside this 57-item set were ever found to reclassify as a side effect of
this fix, that would need its own fresh premise check before folding into this
co-sign — it is not automatically covered.

**Scope-expansion accounting (Hard Rule 2):** nothing is added to scope that isn't
already inside it. This doesn't touch products outside the already-approved 57, doesn't
add a new category, and doesn't change what gets re-flowed (still bread + crackers +
protein-bars, together, no delist — unchanged from my original co-sign). Total grade
movers goes from 8 to 7 (per the coordinator's relay of the corrected TASK-475 count),
still all downward — I have not independently re-verified that 8→7 revision myself and
attribute it to whoever re-ran the trace; if the registry needs it as a hard number, it
should be re-confirmed against an updated TASK-475-family artifact before it's quoted
as fact elsewhere.

## Not done (out of my lane)

- Did not implement or approve the code fix — that's Nutrition Agent sign-off (D7
  co-sign still required per Hard Rule 8) + Data Agent implementation (D8).
- Did not dispatch, sequence, or close any task — orchestrator's lane.
- Did not audit or rewrite any copy — Content Agent + Adversarial QA Agent's lane.
- Did not re-verify TASK-475's numbers independently — cited as-is per the trace
  discipline; if the owner wants independent verification, that's an Adversarial QA
  Agent audit, not a Product Agent re-derivation.

---

```json
{
  "task": "TASK-476",
  "proposed_status": "RETURNED",
  "artifacts": [
    {
      "path": "C:\\Bari\\tasks\\returns\\TASK-476_product_cosign.md",
      "sha256": "cf3fb7178f792c7b792bea0329ba9dad16d7cb16215be97b634ec274a1477281 (hash of this file as of its last save before this JSON edit; self-referential hash is necessarily approximate, same limitation TASK-475 disclosed)"
    },
    {
      "path": "C:\\Bari\\tasks\\returns\\TASK-475_return.md",
      "sha256": "input_only_not_produced_by_this_task_see_note"
    }
  ],
  "counts": {
    "grade_movers": { "value": 8, "denominator": 57, "source": "TASK-475_return.md counts.grade_movers" },
    "grade_movers_direction_down": { "value": 8, "denominator": 8, "source": "TASK-475_return.md counts.grade_movers_direction" },
    "grade_movers_direction_up": { "value": 0, "denominator": 8, "source": "TASK-475_return.md counts.grade_movers_direction" },
    "products_unchanged_grade": { "value": 49, "denominator": 57, "source": "derived: 57 - grade_movers(8), TASK-475_return.md" },
    "mean_delta": { "value": -1.39, "source": "TASK-475_return.md counts.delta_distribution.mean" },
    "rescoring_errors": { "value": 0, "denominator": 57, "source": "TASK-475_return.md counts.rescoring_errors" },
    "real_loss_by_category": { "bread": 23, "crackers": 19, "protein_bars": 15, "source": "TASK-475_return.md counts.real_loss_by_category" }
  },
  "commands_run": [
    { "cmd": "Read C:\\Bari\\tasks\\returns\\TASK-475_return.md", "exit_code": 0 },
    { "cmd": "powershell Get-FileHash TASK-475_return.md (sanity check only, not cited as this task's artifact hash)", "exit_code": 0 }
  ],
  "not_done": [
    "No independent re-verification of TASK-475 figures performed (cited as-is per trace discipline; re-verification would be an Adversarial QA Agent audit, not Product's lane).",
    "No code fix, dispatch, sequencing, or copy audit performed (Nutrition/Data/Content/Adversarial-QA/orchestrator lanes respectively).",
    "sha256 recorded above is of the pre-edit file content (approximate, same self-reference limitation TASK-475 disclosed); orchestrator should re-hash the final committed file if an exact digest is required for the registry."
  ],
  "self_check": {
    "acceptance_test": "Co-sign verdict rendered on all 3 required questions (strategic acceptability, scope/sequencing, consumer-facing consequence), every cited number traced to TASK-475_return.md counts block, no numbers invented, no sub-agents spawned, no pipeline/code/copy changed: PASS",
    "guardrails_respected": {
      "numbers_fabricated": 0,
      "published_files_modified": 0,
      "subagents_spawned": 0,
      "unilateral_scoring_approval": false,
      "nutrition_cosign_still_required_per_hard_rule_8": true
    }
  }
}
```
