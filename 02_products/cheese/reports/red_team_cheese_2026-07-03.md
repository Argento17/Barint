# Adversarial QA Report — cheese_v5 copy overhaul (TASK-461 Phase-2 #1)
Date: 2026-07-02  Challenger: adversarial-qa-agent (Opus, independent lane)
Scope: 47 products, cheese_frontend_v5.json (insightLine + rowVerdict re-author)
Candidate: cheese_v5_copy_overhaul.json  sha256 0a490cc5…cabf4ab (matches spec)
Baseline: origin/master blob deec2e91… → my extraction cc10d803… (== orchestrator's extraction, independence confirmed)

## VERDICT: GO_WITH_FIXES (0 CRITICAL / 0 HIGH / 3 MEDIUM)
Track V fully GREEN on data/isolation/truth/hygiene. Track C: every one of 47 blocks
delivers a defensible engine opinion. No launch blocker. The three MEDIUM items are
gate-tooling / editorial-provenance notes, none of which is a copy defect.

================================================================
## TRACK V — VERIFICATION (deterministic)

### V1. Field isolation — PASS
Exactly {insightLine, rowVerdict} changed, 47/47 products. _meta, page_copy, and every
other product field (score/grade/rank/confidence/nutrition/ingredients/d4_additives/
imageUrl/barcode) byte-identical to origin/master. Non-product top-level keys identical.
Command: qa2_isolation.py → changed fields tally {'rowVerdict':47,'insightLine':47}; ISOLATION CLEAN True.

### V2. Claim-by-claim truth audit — PASS (all 47 read against engine ground-truth)
Every orchestrator hotspot re-derived from my own rank tables:

| # | Product | Claim | Verified |
|---|---|---|---|
| a | Tvorog 6040619 | protein 17g = MAX of all 47 (2nd=11.5) | TRUE |
| a | Tvorog | 30mg Na = shelf MIN; nearest 190 = ×6.33 → "פי שישה" | TRUE (rounds honestly) |
| b | Cottage1% 758681 | least fat (1.0) + least kcal (62) of 47 | TRUE (both are the min) |
| b | Cottage1% | "חלבון מהגבוהים" = rank 2/47 protein | TRUE |
| b | Cottage1% | "הפער ממשי" 86.6 vs 81.3 = +5.3 (largest top gap) | TRUE |
| d | Goat 065467 | "מנצח את כל ממרחי השמנת" 68.3 > max cream 56.3 | TRUE |
| e | Zaatar 3075850 | 558mg Na = shelf MAX; "מהעשירים בחלבון" = rank 7/47 (11g) | TRUE / defensible |
| f | 18% 502541 | label 18% but panel fat = 22g | TRUE |
| f | 18% 502541 | E407+E466 together = ONLY product on shelf | TRUE (unique) |
| g | Olives5% 635116 | 2.8g protein = category MIN | TRUE |
| h | Onion-jam 635383 | closes table; gap to 2nd-last = 10.4 = largest adjacent gap on shelf | TRUE |

Ingredient percentages (i) — all 6 match the parsed ingredient string:
gorgonzola 10%, olives 14%, jalapeño base 96%, garlic-dill 98%+1.4%/0.14%("אחוז וחצי"),
onion-jam 20% ("חמישית"), caramelized-onion 9.0%. PASS.

Twin/family numeric identity (j) — all TRUE:
- Tnuva 5% cottage ×3 (4127329/41445/7290110321277): identical 77.9 / 11 / 5 / 95 / 350 → "אותה גבינה בדיוק" honest.
- Tara lavane ×4 (474502/945481/393268/311472): identical 75.7 / 8.1 / 5 / 97 / 190; the +D/calcium variant (393268) & mehadrin (311472) genuinely score identical → "אינה מזיזה את התוצאה" TRUE.
- Ski pair (2824183/2824640): identical 71.6 → "זהה עד הפסיק האחרון" TRUE.
- 9% mehadrin pair (4127336/41452): identical 73.6 → TRUE.
- Napoleon 25% family (5 prods): 42.3–43.4, max spread 1.1pt < 2pt tie rule → "ההבדלים זניחים" honest.

Partial-panel disclosure (k) — PASS. 19/47 products are confidence=partial, all with the
SAME two nulls (sugar, fiber); each carries confidence_label_he "ניתוח חלקי" + a tooltip
rendered by a SEPARATE UI field (not the copy). No partial product asserts a sugar/fiber
value it lacks. No full-confidence product carries a false partial hedge. (The "סיבי הדרים"
in whipped-25% is the ingredient *citrus fibers*, not a fiber nutrition claim.)

Truth-defect fixes (l) — all 3 CONFIRMED against production:
- 7290119375219 (bagel-spice): OLD copy claimed קנולה; ingredient list has NONE → NEW copy correctly drops it.
- 7290019635116 (olives 5%): OLD copy claimed קנולה; ingredient list has NONE → NEW copy correctly drops it.
- 7290114311472 (#10 mehadrin): OLD copy claimed "הסיווג מוריד את הציון" yet it scores 75.7 = IDENTICAL to NOVA-2 siblings; the classification does NOT lower the score. NEW copy correctly says "הציון יוצא אותו ציון". FALSE claim removed.
- The 3 products NEW copy DOES cite canola (herbs-25% 936604, onion 342102, salsa 635581) all genuinely contain קנולה in ingredients. TRUE.

### V3. Hygiene — PASS
- Em/en dashes: 0 / 94 strings.
- Banned engine vocab (חציון/חיסרון/מדד עיבוד/תקרת עיבוד/רמת אמון/פרמטר/NOVA/BSIP/cap/floor/matrix/pillar/dimension/routing/"NN נקודות"): 0 real. (4 "נובה" substring hits are all inside the brand תנובה/Tnuva — false positives, disambiguated by preceding ת.)
- Antithesis "לא…אלא": 0.
- Opening-3-words uniqueness: 47/47 unique on insightLine AND 47/47 unique on rowVerdict.
- OFF refs: 0. Empty fields: 0.
- hebrew_readability leakage gate: 90/94 is_clean pass; the 4 fails are the identical
  תנובה/Tnuva brand substring collision — MEDIUM-1 below. With the brand masked, 0/94
  real leaks remain (proven by re-run). No genuine framework leak.

### V4. Consistency — PASS
No two products claim the same crown for the same metric. "שיא הקטגוריה" appears twice but
for different true peaks (sodium 558 max on 3075850; fat 30 max on 7290011499624). "הכי מעט"
twice for different metrics (least fat+kcal vs least protein-among-lavane). Rank-1 cottage
= "המנצח" (overall), rank-2 tvorog = "אלוף החלבון" (protein-specific) — two non-conflicting
crowns; the dual-champ risk is handled cleanly.

================================================================
## TRACK C — CHALLENGE (can each block be publicly defended?)

Every block leads with the engine's OPINION (stance + real driver), not a number recitation.
Numbers appear only where the number IS the story (shelf-max sodium 558, protein 17, ×6 salt
gap, 22g-vs-18% label gap, 10.4 last-place gap, ingredient %). Confidence honest. Hebrew
natural and non-templated. Proportionality respected: the 35/46 sub-2pt ties are presented
AS ties ("אותה גבינה בדיוק", "ההבדלים זניחים", "אין כאן שום דרמה"); the 4 big gaps each carry
a stated mechanism.

D-tier spread family (ranks 31–47) — PASS the stamped-verdict test. They share a true common
driver (fat-dense / low-protein), and the copy differentiates by HONEST angle, not a repeated
sentence: gorgonzola=10% real cheese; jalapeño=96% base + garnish; garlic-dill=1.5% seasoning
/ 98% base; salsa=industrial (canola+flavour); onion-jam=20% jam w/ cocoa powder; 30%=fattest
& densest; whipped=air in texture, fat in panel. Reads as a family with individual faces.

Assessment of all 47: JUSTIFIED (not merely plausible). No potentially-incorrect line found.

### Three weakest lines (for fan-out learning — NOT defects):
1. **Zaatar labneh 3075850** insightLine "לבנה עם שני פרצופים" (a labneh with two faces) —
   the "two faces" device is a touch literary; the claim under it (max sodium + rank-7 protein)
   is true, but "מהעשירים בחלבון" at rank 7/47 is the softest superlative on the page (defensible
   but the loosest "among the richest" on the shelf). Fan-out: reserve "among the richest" for top-5.
2. **Goat spread 3523230065467** "ממרח עיזים צרפתי" — "French" is true by BRAND (Soignon/סואניון)
   but is not in the name/ingredient fields; it rests on brand knowledge, not parsed label data.
   Editorially fine; note for the trace-grounding rule that provenance adjectives lean on brand.
3. **Cottage 3% 4127077** insightLine "שביל הזהב של הקוטג'ים" (the golden path) — pure positioning,
   no independent driver of its own beyond "between #1 and the 5%s"; weakest in information density,
   though accurate. Acceptable as a mid-shelf connective line.

================================================================
## FINDINGS BY SEVERITY

### CRITICAL — none.
### HIGH — none.
### MEDIUM (document / route, none block launch):
- **MED-1 (tooling, routes to: adversarial-qa fixture owner / data-agent):** hebrew_readability
  gate returns is_clean=FALSE on 4 strings solely because its substring matcher flags 'נובה'
  inside brand תנובה (Tnuva). Not a copy defect (proven: brand-masked re-run = 0 leaks). The
  gate needs a brand-allowlist / word-boundary fix before it is trusted as a hard go-live gate
  on any dairy category, or it will false-FAIL every Tnuva product forever.
- **MED-2 (editorial, routes to: content-agent):** "French" (צרפתי) on the goat spread is brand-
  derived, not label-derived. True (Soignon), but flag the pattern: provenance adjectives that
  aren't in the parsed name/ingredient string should be tagged as brand-knowledge in fan-out.
- **MED-3 (editorial, routes to: content-agent):** 13 of 19 partial-confidence products do not
  narrate the partial scan in copy (6 do). This is honest today (the confidence chip discloses
  it separately, and no partial line over-claims sugar/fiber), so it is NOT a Hard-Rule-12/13
  violation — but the inconsistency (some hedge in-copy, some rely on the chip) is worth a house
  rule for the fan-out: decide once whether the partial hedge belongs in copy or the chip.

================================================================
## RANK TABLES (from origin/master, my derivation)
Protein (g,/100g): MAX 6040619=17.0 | 758681=11.5 | cottages/lavane 11.0 | … MIN 635116=2.8
Fat: MIN 758681=1.0, 4127077=3.0 | MAX 499624=30.0 (13 products at 25.0)
Kcal: MIN 758681=62 | MAX 499624=302
Sodium: MIN 6040619=30 | 190-band (4 lavane) | MAX 3075850=558 (481, 480 next)
Sugar: non-null 28/47; MAX 342102=5.4; 19 nulls
Additive count: MAX 3 (56272, 194246, 375219, 6492852, 502541, 139278, 499624, 635383); MIN 0
Confidence: partial 19 / full 28. NOVA: 2→13, 3→29, 4→5.
Score: min 23.8 max 86.6 median 62.0 stdev 15.19; grades A2/B19/C9/D15/E2; most-common 75.7(×4).
Adjacent gaps (46): sub-2pt ties 35, ≥5pt big gaps 4 (all narrated).

Contested-additive ("שנוי במחלוקת") usage: 6 products, ALL genuinely carry an engine-`contested`
additive (E466 CMC or E407 carrageenan): 56272, 194246, 375219, 6492852, 504378, 342102. Zero
misapplications. Per Bari's own ECS/d4 data both E466 and E407 are tier=contested, so the phrase
is defensible on the engine's own stance in every instance. Not over-templated (6/47, each tied
to a real contested additive — a finding-count, not a filler phrase).
