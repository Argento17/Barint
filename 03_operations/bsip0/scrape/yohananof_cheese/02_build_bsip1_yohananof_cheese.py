"""
DISABLED — Open Food Facts (OFF) pipeline removed (TASK-238 / TASK-248).

Original purpose: BSIP1 Builder for Yohananof Cheese (TASK-210 Phase B) — built BSIP1
records from yohananof_cheese_bsip0_raw_*.json (il_prices + Open Food Facts candidate
panels), reusing the run_cheese_003 _curate() logic.

OFF is BANNED project-wide (owner hard rule, TASK-238). The upstream acquisition
(01_acquire_yohananof_cheese.py) is disabled, so there is no OFF-sourced raw to build
from. "Unknown is acceptable; OFF is not." Re-enable only under a future explicit written
owner policy (and only against a direct-scrape source, never OFF).
"""
raise RuntimeError(
    "DISABLED (TASK-238/248): 02_build_bsip1_yohananof_cheese.py built from Open Food "
    "Facts candidate panels, which are banned project-wide. No OFF code path may run."
)
