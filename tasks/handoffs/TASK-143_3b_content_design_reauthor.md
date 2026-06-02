# Hand-off — TASK-143 step 3b → Content Agent + Design Agent (re-author)

**Sequence:** AFTER 3a is APPROVED. **Created:** 2026-06-02 by data-agent (CC do-next #3).
**Owner:** content-agent + design-agent · **Prereq:** 3a (Product go-live) approved, incl. soy/coconut ruling.

---

TASK-143 (yogurts) shelf re-author. Product Owner has approved the go-live for the calibrated run_yogurt_004 shelf (A→B downward correction; see their ruling on the soy/coconut rows). Re-author the consumer-facing layer to the new B-capped shelf BEFORE Data swaps the live JSON.

Inputs:
- New machine grades/scores: C:\Bari\02_products\yogurt_system\reports\run_yogurt_004_run_summary.json
- BSIP2 traces (drivers per product): C:\Bari\02_products\yogurt_system\bsip2_outputs\run_yogurt_004\products\**\bsip2_trace.json
- Delta vs the current live shelf: C:\Bari\02_products\yogurt_system\reports\reconciliation_143_run_yogurt_004_findings.md
- Current live shelf (structure + tone to match): C:\Bari\bari-web\src\data\comparisons\yogurts_frontend_v1.json

Do:
1. Rewrite every insightLine + the prologue to the NEW scores. Hard rule: no line may reference an old grade, old score, a point-gap, or an "A"/"top" framing that the corrected shelf no longer supports (this is the editorial-drift trap that bit maadanim/hummus at swap time — TASK-149/150). Every claim must trace to a run_yogurt_004 value.
2. Apply the Product Owner's ruling on the soy/coconut rows (drop / separate plant pool / defer).
3. Honor the score-presentation rules (numeric/grade only; verified/partial/insufficient; no חזק/בינוני/חלש labels; no color encoding).
4. Run the 15–20s first-time-mobile comprehension self-test and report the result.

Return the re-authored insight lines + prologue (Hebrew, RTL) ready for Data to fold into the v2 frontend JSON, plus a one-line confirmation that no line references stale scores. Do NOT touch the live JSON — Data does the swap (3c).
