# P506 / C3 challenge — is suppressing a uniformly-unverifiable bar honest? (route: C3)

**Repo:** C:\Bari (Agent OS root). **Task:** TASK-504 (Supplement Guides / מדריכים, Wave 1 — magnesium golden guide refinement).
**Role:** C3 = independent challenge/consult. You do NOT build, edit, or close. Advice only. Challenge hard, then state a clear support / support-with-changes / oppose verdict.

## Read first (absolute paths)
- Product's decision report (the proposal you are challenging): `C:\Bari\03_operations\reports\product\magnesium_guide_bar_revision_call_v1.md`
- Rubric config being amended: `C:\Bari\01_framework\nutrition\supplement_guides_bar_rubric_v1.yaml` (HARD RULE 1 anti-drift invariant; the third_party_verification + price_fairness bar definitions; bucket_logic).
- Approved plan: `C:\Bari\01_framework\product\supplement_guides_concrete_plan_v1.md`.

## The verified situation
On the magnesium buying guide, two of the six per-product bars are `cannot_verify` for 100% of the 18 products:
- **price_fairness** — zero price data collected for magnesium (a Bari data-collection gap).
- **third_party_verification** — zero Israeli magnesium brands make any cert claim at all (a market fact, not a collection gap).
The owner saw the rendered page and called these two bars "completely meaningless." Product proposes a `display_suppression_rule`: when a bar is uniformly the same state across the displayed corpus, do not RENDER it for that guide (display-only; the bucket computation still evaluates all 6 bars, so the "0/18 clear every bar" finding is preserved; re-evaluated per build; the same two bars still render for creatine, where they discriminate). An on-page disclosure line would state the bar was not assessed and why.

## The fork you must challenge (honest-vs-artifact)
Is suppressing a bar that is uniformly unverifiable HONEST, or does it hide from the consumer that Bari either did not collect the data (price) or that the category lacks it (third-party)? Specifically challenge:
1. **The two cases are NOT symmetric** — price is Bari's own uncollected data; third-party is a real market absence. Product gives them the same suppress ACTION with different disclosure TEXT. Is same-action-different-text sufficient, or does suppressing the price bar let Bari off the hook for work the owner's own strategy said to do ("show pricing differences")? Where is the line between the missing-data-discard doctrine ("unknown is acceptable, never punish") and hiding non-work?
2. **Does an on-page disclosure line actually reach the reader**, or is a removed bar simply invisible in a way a greyed-out "not assessed" bar would not be? Which is more honest to a mobile reader scanning fast?
3. **Anti-drift / precedent risk:** does a per-guide "hide bars that don't discriminate" rule set a precedent that could later be abused to hide an INCONVENIENT bar (e.g. one where many products FAIL) under the same "low signal" cover? Propose the guardrail that prevents that, or argue it can't be prevented.
4. **Trigger correctness:** is "100% identical state across the displayed corpus" the right trigger, or should it be narrower (e.g. only suppress on uniform CANNOT-VERIFY, never on uniform PASS/FAIL, since uniform FAIL is itself a finding)?

## Return format
Write your challenge to `C:\Bari\tasks\returns\P506_return.md`: verdict (support / support-with-changes / oppose) up top, then the four points each with a concrete recommendation, then any guardrail wording you'd add to the rubric rule. End with the machine-readable return contract JSON (`01_framework\operations\return_contract_v1.md`). Do not edit any file other than your return.
