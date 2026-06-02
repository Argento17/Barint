# Hand-off — Cheese run_cheese_003 → LIVE promotion (CC do-next #4)

**Sequence:** independent of TASK-143; runs after TASK-142 CLOSED (already CLOSED 2026-06-02).
**Created:** 2026-06-02 by data-agent. **Owner:** product-agent / Central Controller → then data-agent.

---

Promote cheese-spreads run_cheese_003 to LIVE. TASK-142 is CLOSED; Nutrition signed APPROVED-FOR-PUBLICATION. This promotion is the separate Product/Controller act that was explicitly NOT a close gate. There is currently no live cheese-spreads page, so this CREATES one.

Read:
- C:\Bari\02_products\cheese_spreads\factory_run_003\frontend_package.json (52/59 display-approved; authoritative=false, promoted_to_frontend=false)
- C:\Bari\02_products\cheese_spreads\factory_run_003\NUTRITION_SIGNOFF_VERDICT.md (approval + 2 display conditions)
- C:\Bari\02_products\cheese_spreads\factory_run_003\bsip2_readiness_checklist.json

Product/Controller decision:
1. Approve flipping authoritative=true / promoted_to_frontend=true on factory_run_003/frontend_package.json.
2. Confirm the two Nutrition display conditions ship with the page: (a) labaneh pool n=1 presented standalone, no intra-pool ranking; (b) the two PO-approved Sec 6.4 disclosure notes (category-wide sodium/sat-fat; pool-specific reduced-fat reformulation) are rendered.
3. Confirm the 7 withholds stay withheld (1 misroute goat cheese, 1 A-ceiling טבורוג 5%, 5 transparency-tier partial-panel SKUs).

On approval, hand to Data:
- Flip the two flags; build the live cheese-spreads comparison JSON into C:\Bari\bari-web\src\data\comparisons\ matching the canonical (מעדנים) page schema + a new /hashvaot route; wire the 2 disclosure notes; run tsc + confirm the route builds.
- Return files changed, tsc/route result, and a "cheese-spreads live" note.

Guard: engine UNMODIFIED; no published/frozen score changes; only display_approved=true products render.
