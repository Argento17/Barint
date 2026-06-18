"""
DISABLED — Open Food Facts (OFF) pipeline removed (TASK-238 / TASK-248).

Original purpose: BSIP1 builder for the multi-retailer cereals acquisition (TASK-184) —
built BSIP1 records from the il_prices + Open Food Facts candidate panels produced by
01_acquire_multiretailer.py, stamping provenance as an OFF candidate.

OFF is BANNED project-wide (owner hard rule, TASK-238). The upstream acquisition
(01_acquire_multiretailer.py) is disabled, so there is no OFF-sourced raw to build from.
"Unknown is acceptable; OFF is not." Re-enable only under a future explicit written
owner policy (and only against a direct-scrape source, never OFF).
"""
raise RuntimeError(
    "DISABLED (TASK-238/248): 02_build_bsip1_multiretailer.py built from Open Food Facts "
    "candidate panels, which are banned project-wide. No OFF code path may run."
)
