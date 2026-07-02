# P297 / TASK-380 — hard-cheeses sat-fat relief rule, independent CHALLENGE (route: C3)

You are an independent challenger (ChatGPT). Advice only — you do NOT build, do NOT edit files, do NOT close anything. Evidence-based reasoning only; flag where you are uncertain. This is a tripwire-1 (scoring-philosophy) fork, so your challenge is a mandatory gate before it can advance.

## Context
Bari scores Israeli supermarket products 0–100 / A–E on nutritional architecture. The hard-cheeses ("גבינות קשות") shelf has ~30 products. The page is LIVE with distribution **A:2 / B:23 / C:3 / D:2**.

**Two verified problems with that live distribution:**
1. **It is an artifact.** 27 of 30 products were scored with `fat_saturated_g = NULL` (no sat-fat value parsed), which the pre-correction engine treated favorably (fat_quality defaulted to 50) — inflating grades. The 2 current A-grades are 640–659 mg-sodium standard cheeses whose A is an artifact of sat-fat being read as ~0.
2. **The honest re-score collapses to D.** When sat-fat inference is restored (EV-099: sat_fat ≈ 0.62 × total_fat for cheese), hard cheese's high saturated fat (~18–22 g/100g) trips the Israeli regulatory "red label" sat-fat cap. Combined with a sodium red label, two red labels → a hard cap → almost the entire shelf clusters at D. Those caps were designed for engineered foods (added palm oil, margarine, cream), not intrinsic dairy fat.

## Proposed fix (the thing you must challenge)
A flag `BARI_HC_DAIRY_SATFAT_V1` (default OFF). For products passing a predicate — NOVA proxy ≤2 AND ≤6 clean ingredients AND not "processed" subpool AND sodium <850 mg/100g AND no engineered-fat markers (palm oil / margarine / coconut oil / added cream / butter-as-ingredient / emulsifying salts) — it:
1. Excludes the sat-fat red label from the "≥2 reformulable red labels" cap count (a single sodium red label still applies);
2. Suppresses the fat+sodium hyper-palatability combo penalty;
3. Reduces an R5 "seed penalty" 5→0 (endemic dairy fat is not an engineering choice);
4. **PRESERVES** the sat-fat penalty in the fat-quality dimension (sat-fat is still a real nutrient concern — relief is only about the binary cap, not about pretending sat-fat is zero);
5. **RETAINS** the sat-fat inference (0.62 × fat) — non-negotiable.
Non-relieved guardrails: sodium ≥850 → no relief; NOVA >2 → blocked; processed subpool → disqualified; kcal ≥380 → score capped at 67 (top of C); engineered-fat ingredients → disqualified.

Evidence basis (EV-104): cheese-matrix RCTs showing fermented-cheese sat-fat attenuates LDL vs butter at equal intake (Kay 2024 PMID 39133879; Thorning 2017 PMID 28615384; Lordan 2019 PMID 31022985); NOVA definition (Monteiro 2019 PMID 31122155); USDA FDC SR Legacy sat-fat fractions 0.62–0.66. (Full-text verification of the RCTs is still pending.)

Nutrition's **band-estimate** projection of the flag ON: **A:1 / B:11 / C:17 / D:1** (NOT yet an engine re-run; ±5 pts).

## Your challenge — argue BOTH directions, then give a verdict
1. **Is the relief scientifically defensible?** The dairy-matrix / fermented-cheese LDL literature is the load-bearing claim. Is it strong enough to justify exempting cheese sat-fat from the binary cap — or is that over-reading a modest, contested effect? Where is the evidence weakest?
2. **Over-correction risk.** Hard cheese is calorie-dense (~350–400 kcal/100g) and sodium-dense. After relief, the shelf runs B:11/C:17. Is that honest, or does it tell a consumer a high-sat-fat, high-sodium food is "good"? Is the kcal≥380→cap-67 and sodium-850 backstop the right line, or too lax/too strict? What's the defensible ceiling for a standard 28%-fat, 640mg-sodium cheese — B or C?
3. **Loophole / gaming.** Can a manufacturer engineer a processed/blended cheese to pass the predicate (≤6 ingredients, NOVA≤2 proxy, sodium<850) yet be nutritionally poor? Name concrete failure cases. Are the engineered-fat guards (palm/margarine/coconut/added-cream/emulsifying-salts) complete — what's missing?
4. **Coherence / publishability.** Can every resulting grade be publicly defended? Is moving the 2 current A's to C, and most B's to C, the *right* direction (correcting the NULL-sat-fat artifact) — and does the relief keep the ranking honest relative to the genuinely-processed cheeses that correctly stay at D?

## Return format
Argue both directions per question, then a one-paragraph VERDICT: is the direction right, are the guardrails sufficient, and list any REQUIRED changes before this should go to owner go-live (as you did for the snacks rule). Evidence-only; name your uncertainty. You do not close or build.
