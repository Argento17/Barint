# Hand-off — TASK-143 step 3a → Product Agent (go-live decision)

**Sequence:** run FIRST (gates 3b and 3c). **Created:** 2026-06-02 by data-agent (CC do-next #3).
**Owner:** product-agent · **Prereq:** none (TASK-143 data cycle is RETURNED & clean).

---

TASK-143 (yogurts) go-live decision. The data cycle is done and clean (run_yogurt_004, engine 0.4.1 UNMODIFIED, COV-006 0.0% implausible). Your decision gates the live shelf swap that retires DEC-005 — it overwrites a live page and is hard to reverse, so this is your call to make explicitly.

Read before deciding:
- C:\Bari\02_products\yogurt_system\reports\reconciliation_143_run_yogurt_004_findings.md
- C:\Bari\02_products\yogurt_system\reports\run_yogurt_004_qa_gate.json
- Live shelf being replaced: C:\Bari\bari-web\src\data\comparisons\yogurts_frontend_v1.json (DEC-005, 13 manual products)

What you are approving or rejecting:
1. Retire DEC-005 (the manual yogurt shelf) and replace it with the calibrated machine shelf from run_yogurt_004.
2. Accept the downward correction: the live manual shelf shows 5 A's (top 88/A); the machine caps the cleanest plain bio yogurts at ~75/B and reaches NO A (max 78.7/B). The A-ceiling ruling (139A) does not restore A on real data. The shelf becomes less flattering but truthful.
3. Rule on the two non-dairy live rows (yog-009 קוקוס / yog-010 סויה) the dairy_protein run does not cover 1:1: (a) drop them from the v2 shelf, (b) keep as a separate plant pool, or (c) defer to a future plant-cheese/yogurt task. State which.

Return: APPROVED-FOR-GO-LIVE (with your ruling on item 3) or CHANGES_REQUESTED with reasons. Do not edit code or data — this is a decision. On approval, Content+Design re-author next (3b), then Data executes the swap (3c).
