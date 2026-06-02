# Hand-off — TASK-143 step 3c → Data Agent (build + live swap)

**Sequence:** LAST. Execute ONLY after 3a (Product go-live) AND 3b (Content/Design re-author) are both in hand.
**Created:** 2026-06-02 by data-agent (CC do-next #3). **Owner:** data-agent.

---

TASK-143 (yogurts) live swap — execute ONLY after Product go-live (3a) AND Content/Design re-author (3b) are both in hand. Engine stays UNMODIFIED; no score changes.

Do:
1. Build the run_yogurt_004 frontend package from the traces (mirror the existing yogurts_frontend_v1.json schema: _meta + products[{id,name,imageUrl,score,grade,confidence,insightLine,_cluster,expansion}]). Source scores/grades from run_yogurt_004; source insightLine/prologue from the 3b re-author; apply the 3a soy/coconut ruling. Write it as yogurts_frontend_v2.json under 02_products/yogurt_system/ first (factory artifact).
2. Reconcile-check: every displayed score/grade matches a run_yogurt_004 trace; no orphan ids; Hebrew coverage 100%; no stale-score lines (grep the insightLines against old values).
3. Swap live: copy to C:\Bari\bari-web\src\data\comparisons\yogurts_frontend_v1.json (or v2 + repoint the page import — match how maadanim/hummus were shipped), run tsc, confirm the /hashvaot/yogurts route builds clean.
4. Retire DEC-005: record the retirement in the decision log and update TASK-143 with a "live swap shipped" note.

Return: files changed, tsc result, route-build confirmation, the DEC-005 retirement record, and propose TASK-143 RETURNED → ready for Controller CLOSED. Guard: if either 3a or 3b is missing, STOP and report — do not swap.
