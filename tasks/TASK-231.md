---
id: TASK-231
title: "Salty-snacks v4 data remediation — dedup Bamba/brand normalization, fix garbled+English ingredients, recover Apropo sodium, fix NOVA field/copy contradiction, regenerate v4"
owner: data-agent
status: BLOCKED
priority: HIGH
created_at: 2026-06-10
depends_on: [TASK-228, TASK-230]
blocks: [TASK-232]
roadmap_impact: true
work_type: data-remediation
block_reason: "Waits on TASK-230 (Content corrected copy templates) so the regeneration applies clean copy, not the current leaky/recommendation templates."
---

# TASK-231 — Salty-snacks v4 data remediation

Owner review of shipped v4 found data defects. All in
`bari-web/src/data/comparisons/salty_snacks_frontend_v4.json` (built by
`03_operations/bsip0/scrape/salty_snacks_real/03_build_frontend_v4.py`).

## Confirmed data defects (with evidence)

1. **Duplicate Bamba — 8 SKUs.** `במבה יום הולדת`, `במבה מארז 10*25`, `במבה קלאסי`, 3× `במבה ביסלי מיקס`,
   `במבה במילוי קרם נוגט`, `במבה מתוקה`. Owner: "take out multiple Bamba — leave one from each brand."
   Dedup to one canonical Bamba (classic) per brand; keep genuinely distinct products only if
   editorially justified, but no near-duplicate SKU clutter.
2. **Brand field garbage.** Same Bamba shows brand as `Osem`, `אסם`, `اوسم` (Arabic), `Some`, `Same`.
   Normalize to one canonical brand string per manufacturer across the whole corpus.
3. **Garbled ingredients.** `במבה יום הולדת 80 גרם` ingredients = `"םרי וייו ןוימיוc, ימ1 63 םמיי ת 1 )..."`
   — corrupted/reversed RTL parse. Fix the parse or omit the field (never ship garbled text).
4. **English ingredients.** `פריכיות תירס עם סויה וזרעי פשתן` ingredients = `"Maize (89%), Linseed (6%),
   Soy (2%), Chia Seeds (1%)..."` (OFF returned English). Confirm it's the OFF source; provide
   Hebrew, or omit ingredients and mark the product panel-only — don't ship English on a Hebrew page.
5. **Missing sodium on a salty snack.** `אפרופו 50 ג'` has `sodium: null`. Owner: "it's a really
   salty snack." Recover the real sodium (OFF / label) or mark the gap honestly; don't leave a
   salty snack with an empty sodium bar if a real value exists.
6. **NOVA field vs copy contradiction.** `פריכיות תירס...` has `novaGroup: 3` but its limitingFactors
   copy says "NOVA 4". Fix the source so the processing classification and the (de-leaked) copy agree.

## Scope
- Apply 1–6 to the corpus/build inputs. Re-run the build applying the **TASK-230 corrected copy
  templates** (no NOVA/leakage, no recommendations, reworded confidence label).
- Re-verify: every imageUrl still HTTP 200; sodium/fiber still populated where real; tsc + build clean.
- Do NOT change scoring logic. NOVA *correctness* questions (is X really ultra-processed?) and the
  protein-reward question route to Nutrition (TASK-229), not here — here only fix the field/copy
  contradiction and the data parse.

## Acceptance criteria
- [ ] Bamba deduped to canonical set; brand field normalized corpus-wide
- [ ] No garbled and no English ingredient strings shipped (Hebrew or omitted+panel-only)
- [ ] Apropo sodium recovered or honestly marked
- [ ] novaGroup ↔ copy consistent; corrected copy templates applied
- [ ] imageUrl 200 preserved; sodium/fiber bars still populate; tsc + build clean
- [ ] New corpus shipped (v4 updated or v5); page wired; product count + grade dist reported

## QA audit additions (TASK-232 FAIL, 2026-06-10)

- **120 score-mechanic leaks (BIG, was missed):** every `insightLine` ends `"הציון 77/B משקף…"` and
  every `bottomLine` embeds `(77/B)` — grade mechanic in prose (banned). Plus raw unrounded macros
  as TEXT in positiveSignals (×21) / limitingFactors (×13), e.g. `"15.0 גרם חלבון ל-100 גרם"`. When
  applying the TASK-230 templates, ensure NO `"X/Y"` grade and NO raw decimals in any consumer
  string; re-run `hebrew_readability.is_clean` = True on all. (Gate now flags "עדיף לבחור" too.)
- **Brand normalization specifics:** `Some` (8851016002685), `Salty`, `اوسم` (Arabic); split
  spellings: אסם×10 vs `Osem`×7, פיטנס vs `Fitness`, קליק vs `Click`, תפוצ'יפס(U+05F3) vs
  תפוצ׳יפס(U+05F4); 3 empty brand. Normalize to one canonical per maker.
- **Bamba — QA correction (Hard Rule 4):** the 8 Bamba products are NOT duplicate SKUs (distinct
  barcodes/variants). Not a dedup *bug* — but owner asked to cut the clutter; reduce to ~1–2
  canonical Bamba (balance call: 8/47 = 17% one brand-family).
- **VERIFY the beet-cracker trans value:** `7290112968807` scores 0/E via a hard trans-fat veto
  (`fat_trans_g = 2.33`). Implausible for a whole-grain beet cracker with no hydrogenated oil —
  CHECK the source OFF panel. If bad, correct it; re-scoring likely resolves the 0/E with NO scoring
  change. If real, routes to Nutrition (TASK-229).
- **Route metadata 54→47 already fixed** by orchestrator in `app/hashvaot/salty-snacks/page.tsx`.

## Return block
Report: final product count after dedup, brand normalization map, ingredients fixed/omitted,
Apropo sodium outcome, beet-cracker trans verification result, and confirmation copy is
leakage-clean (is_clean True on all consumer strings, no "X/Y" grades or raw decimals) +
recommendation-free.
