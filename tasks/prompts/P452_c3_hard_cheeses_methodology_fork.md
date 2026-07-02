# P452 / C3 challenge: hard_cheeses traceability methodology fork — port TASK-380 sat-fat penalty vs re-score on main engine (route: C3)

META (read first): You are C3 (independent challenge / red-team). Give evidence and a reasoned recommendation-challenge ONLY — you do NOT decide, build, or close. Output is advice to the orchestrator. No code. Cite reasoning. Keep it tight.

## Situation (verified facts)
Bari scores food products 0–100 with letter grades. The live hard-cheeses comparison page ("v3") was scored by a **forked copy of the scoring engine** in an external scratch dir (`C:\bari_hc380`), via a run named `run_hc_dairy_satfat_v1_001`, applying a strong **saturated-fat penalty** specific to hard cheeses. This was deliberate TASK-380 work (Nutrition-driven).

The problem: the **main engine cannot reproduce v3**. Feeding the main engine v3's exact flags (`BARI_HC_DAIRY_SATFAT_V1=on`, `BARI_REDLABEL_V1=off`, shelf-relative on saturated fat, median 18.0 / scale 1.4) and the same corpus, products v3 scores at **39/D come out ~73/B (+34)**. So the forked engine's sat-fat penalty is far harsher than the main engine's `BARI_HC_DAIRY_SATFAT_V1` flag of the same name. The forked methodology was never merged into the main engine.

Goal: make hard_cheeses **clean + traceable** (every published score must re-derive from the committed main engine + config + corpus). Owner has authorized score movements.

## The fork (challenge my recommendation)
- **(A) Port the TASK-380 forked sat-fat penalty into the MAIN engine, then re-derive.** Preserves the live scoring *intent* (hard cheeses penalized hard for saturated fat) and makes it reproducible. My recommendation.
- **(B) Re-score hard_cheeses with the main engine as-is** (its existing, gentler `BARI_HC_DAIRY_SATFAT_V1`). Fast and traceable, but scores jump ~+34 (39/D → ~73/B), effectively undoing TASK-380's intent.

## Your challenge (answer these)
1. Is (A) actually right, or am I preserving an under-documented forked penalty whose magnitude was never independently validated? What evidence would justify the forked penalty's harshness vs the main engine's gentler one?
2. **Cross-category risk of (A):** porting a hard-cheese sat-fat penalty into the SHARED main engine — what's the risk it perturbs other dairy shelves (cheese spreads, brined cheeses, milk, butter) that the main engine also scores? How should that be bounded/tested before adopting?
3. Is the strong saturated-fat penalty for hard cheeses **scientifically defensible** as a category-specific lever, or is it double-counting (sat fat already enters via fat_quality / shelf-relative)? 
4. Is there a **third option** I'm missing (e.g., quarantine hard_cheeses as a documented non-standard shelf; or adopt the main-engine score with a transparent methodology note)?
5. Net recommendation: A, B, or a third path — with the single most important risk to watch.

Return evidence + a clear challenge verdict. Do not write code or make the final call.
