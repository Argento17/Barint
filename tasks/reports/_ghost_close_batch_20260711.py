# One-shot close batch for the 2026-07-11 ghost triage (unattended 3AM run).
# Evidence: tasks/reports/ghost_triage_2026-07-11.md + orchestrator artifact assertions
# (24/25 mechanical checks OK; cereals route confirmed at breakfast-cereals/).
import re, shutil, sys
from pathlib import Path

TASKS = Path(r"C:\Bari\tasks")
CLOSED = TASKS / "closed"
SUFFIX = (" Per ghost triage 2026-07-11 (tasks/reports/ghost_triage_2026-07-11.md); "
          "orchestrator mechanically asserted the cited artifacts before closing.")

REASONS = {
 "233F": "SUPERSEDED - frontend_core.py never materialized (asserted absent); generate_page.py (TASK-257/268) is the canonical generator; TASK-321 sweep complete 2026-06-18.",
 "237": "SUPERSEDED - snacks OFF removal executed via the project-wide ban + TASK-360/362 rebuild; snacks_frontend_v5.json is the live artifact (asserted).",
 "241": "SUPERSEDED - reconciled 2026-06-11; TASK-360/362 snacks corpus rebuild absorbed the rescue scope; snacks_frontend_v5.json live (asserted).",
 "250": "SUPERSEDED - phase 2 complete per task body; TASK-515/543 spoonable/drinkable rebuild replaced run_yogurt_006; yogurt_spoonable/drinkable_frontend_v1.json live (asserted).",
 "256": "SUPERSEDED - TASK-515/543 yogurt split replaced the shipcfg2 relaunch chain; yogurt_spoonable/drinkable_frontend_v1.json live (asserted).",
 "257": "DONE-IN-FACT - generate_page.py exists (asserted) and is the production generator; TASK-321 conformance sweep complete 2026-06-18.",
 "266": "DONE-IN-FACT - brined_cheeses_frontend_v2.json + /hashvaot/brined-cheeses route exist (asserted); page live; all pipeline stages complete per task body.",
 "268": "DONE-IN-FACT - 03_operations/spine/pipeline_e2e.py exists (asserted) incl. render stage; TASK-321 sweep generalized the factory.",
 "275": "SUPERSEDED - cookies_coffee_frontend_v2.json live (asserted); parked 2026-06-14, scoring issues routed to de-anchor program (TASK-395+).",
 "286": "SUPERSEDED - TASK-412/380 delivered the hard-cheeses rework via governed sat-fat carve-out; hard_cheeses_frontend_v4.json + route live (asserted); NOVA-1 rule not needed.",
 "311": "DONE-IN-FACT - all 7 re-baselined pages live on origin/master (granola/juices/breakfast-cereals routes asserted); pre-push gate satisfied by the push; category-level red-team backfill tracked in TASK-474.",
 "314": "DONE-IN-FACT - reconciliation complete per task body; Argento17/Barint master = live Vercel deploy source (standing deploy topology); all live routes on origin/master.",
 "321": "DONE-IN-FACT - task body declares SWEEP COMPLETE 2026-06-18; conformance.py exists (asserted); 16/16 re-flow verified in later spine work (board 2026-06-18).",
 "321C": "SUPERSEDED - TASK-515/543 yogurt split replaced the run_yogurt_shelfrel_v2 conformance config; new-architecture pages live (asserted).",
 "321D": "DONE-IN-FACT - milk_frontend_v1.json exists at bari-web/src/data/comparisons/ (asserted); extraction branch pushed per task body (cad0732c).",
 "321E": "DONE-IN-FACT - orchestrator verified copy complete 2026-06-17 per task body; cheese_frontend_v4.json live (asserted).",
 "321F": "SUPERSEDED - TASK-515/543 yogurt split replaced the 83-product corpus; new spoonable/drinkable copy authored for the live architecture (asserted).",
 "321G": "DONE-IN-FACT - 4 legacy routes deleted (commit beabcef8 per task body); /compare/bread-comparison asserted absent.",
 "321H": "SUPERSEDED - TASK-515/543 split replaced the 321H conformance approach; live yogurt served via the new architecture (asserted).",
 "331": "SUPERSEDED - TASK-564/569/574/581 schema overhaul (board-verified closes) removed the v3 deep-dive fields from production; scope obsolete.",
 "332": "OBSOLETE - TASK-574 stripped the v3 deep-dive fields from all served JSONs; the architectural direction reversed (strip, not render); deep-dive render is not part of the page contract.",
 "357": "DONE-IN-FACT - snacks_frontend_v5.json + /hashvaot/snacks route exist (asserted); migration completed via TASK-362/de-anchor sweep.",
 "358": "SUPERSEDED - TASK-569/581 built the canonical TS contract + ajv gate (18/18 PASS, board-verified); conformance.py exists (asserted).",
 "360": "DONE-IN-FACT - snacks_frontend_v5.json exists with gates_report (asserted); snacks corpus rebuilt and re-scored.",
 "362": "DONE-IN-FACT - snacks_frontend_v5.json exists (asserted); legacy routes purged per TASK-321 wave; BSIP0 hardening continued in TASK-582/590.",
 "362A": "DONE-IN-FACT - protein_combined_frontend_v2.json + /hashvaot/protein-bars route exist (asserted); split completed.",
 "380": "DONE-IN-FACT - hard_cheeses_frontend_v4.json + route live (asserted); full rework completed via TASK-412.",
 "384": "DONE-IN-FACT - magnesium page live (asserted /madrichim/magnesium route; TASK-577/580/587 v3.x closes on board); data rebuild published; post-publish items resolved in TASK-577/587.",
 "384A": "DONE-IN-FACT - TASK-577 (v3) and TASK-587 (v3.2) CLOSED per board; the structured redesign is the live page (asserted route).",
 "385": "DONE-IN-FACT - granola_frontend_v2.json + /hashvaot/granola route exist (asserted); rework completed.",
 "412": "DONE-IN-FACT - hard_cheeses_frontend_v4.json + route live (asserted); governed sat-fat carve-out + Tom's Voice copy deployed.",
 "447": "DONE-IN-FACT - read-only capability audit completed; evidence = its downstream action tasks exist in the registry (TASK-446/451/453 asserted), each citing the audit's findings.",
}

done, errors = [], []
for tid, reason in REASONS.items():
    src = TASKS / f"TASK-{tid}.md"
    dst = CLOSED / f"TASK-{tid}.md"
    if not src.exists():
        errors.append(f"TASK-{tid}: source missing"); continue
    if dst.exists():
        errors.append(f"TASK-{tid}: dst exists"); continue
    text = src.read_text(encoding="utf-8")
    m = re.search(r"^status:\s*(\S+)\s*$", text, flags=re.M)
    if not m:
        errors.append(f"TASK-{tid}: no status line"); continue
    old_status = m.group(1)
    full_reason = (reason + SUFFIX).replace('"', "'")
    replacement = (f"status: CLOSED\nclosed_at: 2026-07-11\n"
                   f"close_reason: \"{full_reason}\"")
    text = text[:m.start()] + replacement + text[m.end():]
    src.write_text(text, encoding="utf-8")
    shutil.move(str(src), str(dst))
    done.append(f"TASK-{tid} (was {old_status})")

print(f"closed {len(done)}: " + ", ".join(done))
if errors:
    print("ERRORS:"); [print(" ", e) for e in errors]
    sys.exit(1)
