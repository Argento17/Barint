# P76 — Cookies-near-coffee: milk-quality Hebrew copy (route: C1 / Content)

**Task:** TASK-275. **Lane:** C1 Content Agent — editorial judgment (Bari voice, honest framing). Scores
are LOCKED = `run_cookies_003`. C1-CURSOR is down; this is C1 native regardless (copy is always C1).

## Deliverable
`02_products/cookies_coffee/cookies_coffee_copy_v1.json` — mirror the structure of the golden
`02_products/brined_cheeses/brined_cheeses_copy_v2_draft.json`. Keyed by barcode:
- per product (all 61 in run_cookies_003): **`insightLine`** + **`rowVerdict`** (the 2-line interpretive
  verdict: standing → real driver → catch → earned grade; NOT a restatement of the columns).
- page shell: hero, 3 prologue sentences, methodology lines, **category caveat** (the yellow הערת קטגוריה box).

## Ground truth (read first — every claim traces to these; no fabrication)
- Scores/grades: `02_products/cookies_coffee/bsip2_outputs/run_cookies_003/` (traces + run_record).
- Methodology + framing: `02_products/cookies_coffee/methodology/cookies_coffee_scoring_interpretation_v1.md`
  + `cookies_coffee_routing_ruling_v1.md` (the C-ceiling ruling).
- The golden voice bar: `02_products/brined_cheeses/brined_cheeses_copy_v2_draft.json` + the milk page (content gold standard).

## The honest framing (NON-NEGOTIABLE — this is a C-ceiling indulgence shelf)
- **Real distribution: 0 A, 0 B, 9 C, 22 D, 30 E. Top product = 63/C.** The page is "least-bad", NOT
  "healthy cookies". An A/B does not exist here; **C is the ceiling** = the least-bad biscuits.
- Thesis (the page's spine): the real difference is **fat type (butter vs palm/hydrogenated) + sugar level
  + additive/processing load**, NOT "which cookie is healthy". Sodium is NOT the story (low across the shelf).
- Prologue: a human opening + the honest analytical read + a few REAL run stats (the 0-A/0-B/C-ceiling fact;
  most of the shelf crosses the 17.5g sugar + 5g sat-fat red lines). One line of genuine sentiment. Readable,
  not a stat dump. Do NOT demoralize — frame as practical harm-reduction ("if you're buying biscuits anyway…").
- Category caveat: explicit — all processed sweet biscuits; A/B not achievable; C = least-bad; drivers = fat
  type / sugar / additives; sodium not the story.

## Editorial law (hard)
- **Brand in every product title** (`<name> — <brand>`). No internal tokens in consumer copy (run ids,
  bc-/EV-/flag ids, NOVA/cap names — banned). No grade/score number inside description prose (grade is the
  badge only). rowVerdict differentiated per product (no templated repetition).
- Ground EVERY claim against the trace + the REAL parsed ingredients/nutrition. No invented products,
  brands, numbers, or health claims. OFF ban absolute (no external data).
- Run the leakage/readability gate (`integrations/clients/hebrew_readability.py`) on every consumer string;
  ≤1 em-dash per sentence; report it clean.
- Watch-items to handle honestly in copy: the 2 peanut-butter cookies (high protein — describe truthfully,
  don't imply "healthy"); choc-chip biscuits (in-scope, describe as biscuit-with-chips).

## Return
End with the return contract: task=P76, proposed_status=RETURNED, artifact (copy_v1.json + sha256), counts
(products with insightLine+rowVerdict = 61/61, prologue/methodology/caveat present, readability clean,
fabrication=0, internal-token leakage=0), not_done, self_check. Propose RETURNED — do NOT close. The
orchestrator reads every consumer string before ship (hard gate) + C3 fresh-eyes follows.
