# P13 (v2 — supersedes the cap version) → Nutrition Agent — adjudicate the yogurt S-grades on merits

**Owner ruling 2026-06-12:** engine-recognized S grades are NOT suppressed. No blanket
A-ceiling. The gate is your audit + a very good explanation.

```
P13 / TASK-249 — S-grade audit: are 92.6/S and 90.6/S defensible, and if so, explain them.

CONTEXT: Under the exact ship flags, run_yogurt_006_shipcfg yields two S-grades:
- 7290112336712  דנונה פרו 21 חלבון 0%   92.6/S
- 7290110565527  דנונה PRO 20g 1.5%      90.6/S
Both scored via base dimensions; the 169D trim never applied because their names
lack יוגורט so the fermentation path never fired. OWNER RULING: if the engine
honestly recognizes S, Bari shows S. Your job is to determine whether these
scores are HONEST (then explain them) or ARTIFACTS (then fix the artifact —
never the framing). Evidence: 02_products/yogurt_system/bsip2_outputs/
run_yogurt_006_shipcfg/products/<pid>/bsip2_trace.json and reports/
run_yogurt_006_shipcfg_run_record.json.

DO:
1. FULL TRACE AUDIT of both products, dimension by dimension: protein scale
   contribution, nutrient density, processing (NOVA + caps), additives/
   sweeteners (these are flavored protein products — verify sweetener caps and
   additive penalties fired correctly against the BSIP1 ingredient data),
   TASK-250 confidence effects, and every cap/floor considered-but-not-applied.
   The question: does 92.6 survive scrutiny as "the best dairy products Bari has
   scored," or is a component misfiring?
2. THE MISSING-BONUS ASYMMETRY: these products never got fermentation-bonus
   ELIGIBILITY ASSESSED (is_yogurt name gate failed). Check their labels/
   ingredients: are they cultured? If yes, the honest score might be HIGHER
   (+8 eligible) — or the name gate needs widening. Rule on it; don't leave the
   asymmetry standing silently.
3. SHELF QUESTION: do dairy_protein products belong on the yogurt comparison
   shelf? If your answer is no, that's a shelf-composition recommendation
   (Product co-sign needed), not a scoring change — state it separately.
4. VERDICT, one of:
   a. HONEST S → write the "very good explanation" the owner requires:
      (i) a consumer-grade Hebrew explanation for the page (what S means, why
      THIS product earns it, what separates it from the A bio-yogurts — entailed
      by the trace, rubric rules apply); (ii) a methodology note for the
      category caveat. No engine change; shipcfg becomes the final run.
   b. ARTIFACT → name the exact misfiring component, propose the fix under full
      governance (EV entry, flag scope, flag-OFF byte-identity) and run the
      Shadow backtest (shadow_backtest.py diff) — acceptance: only the affected
      products move, frozen corpora untouched, attach the report. Then re-run
      batch_run_yogurt_006_shipcfg.py into run_yogurt_006_shipcfg2/.
   Mixed verdicts (one honest, one artifact) are allowed.
5. Either way: state what happens to the 169D trim's narrow scope (it still caps
   ferm-stacking S-grades) — keep/adjust, with reasoning. And note the
   trim/fermentation coupling status (03_operations/shadow/README.md "Known
   engine couplings").

RULES: do NOT add caps/ceilings to enforce zero-S — that path is closed by owner
ruling. Any engine change = governance + Shadow, no exceptions. No data
invention; label evidence only from the BSIP1 corpus (no Open Food Facts, ever).

RETURN BLOCK: per-product verdict (honest/artifact) with the dimension table;
the consumer explanation drafts (if honest); fix spec + Shadow report (if
artifact); fermentation-eligibility ruling; shelf recommendation; 169D trim
disposition. Propose RETURNED.
```
