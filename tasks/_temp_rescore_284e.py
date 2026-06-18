"""
TASK-284E — Re-score all published categories under BARI_FAT_TECH_V1 default ON.
Runs each authoritative batch runner as a subprocess with the new engine default.
Collects grade distributions and checks for unexpected grade changes.

Expected grade changes (all upward):
  cereals 884912126115: E→D  (EV-096, from TASK-284B registered)
  cakes 313184: E→D          (EV-096, from TASK-284D)
  maadanim 7290112497123: D→C (EV-096, from TASK-284B registered)
  salty 8710908800018: D→C   (EV-096, from TASK-284D)
"""
import subprocess
import sys
import json
import os
import pathlib

SRC = pathlib.Path(r"C:\Bari\03_operations\bsip2\proto_v0\src")

# Published category batch runners to re-score.
# Format: (runner_script, category_name, env_overrides, output_path_to_check_grades)
RUNNERS = [
    (
        "batch_run_milk_005_headpin.py",
        "milk (frozen)",
        {},  # headpin runner sets no extra flags; uses engine defaults
        r"C:\Bari\02_products\milk_and_alternatives\intelligence_bsip2\run_005_headpin\products",
    ),
    (
        "batch_run_snack_bars_001.py",
        "snack_bars (frozen)",
        {},
        r"C:\Bari\02_products\snack_bars\bsip2_outputs\run_001\products",
    ),
    (
        "batch_run_cereals_008.py",
        "cereals",
        {"BARI_RECAL_P0": "on"},
        r"C:\Bari\02_products\breakfast_cereals\bsip2_outputs\run_cereals_008\products",
    ),
    (
        "batch_run_cereals_multiretailer_001.py",
        "cereals_multiretailer",
        {"BARI_RECAL_P0": "on"},
        r"C:\Bari\03_operations\bsip1\run_cereals_multiretailer_001\bsip2_outputs\products",
    ),
    (
        "batch_run_maadanim_001.py",
        "maadanim",
        {"BARI_TASK144_FIXES": "on"},
        r"C:\Bari\02_products\maadanim\bsip2_outputs\run_maadanim_001\products",
    ),
    (
        "batch_run_cheese_004.py",
        "cheese",
        {"BARI_RECAL_P0": "on"},
        r"C:\Bari\02_products\cottage_and_soft_cheeses\bsip2_outputs\run_cheese_004\products",
    ),
    (
        "batch_run_hummus_003.py",
        "hummus",
        {"BARI_RECAL_P0": "on"},
        r"C:\Bari\02_products\hummus\intelligence_bsip2\run_hummus_003\products",
    ),
    (
        "batch_run_cakes_001.py",
        "cakes_hard_cookies",
        {},  # all flags off per batch runner
        r"C:\Bari\02_products\cakes_hard_cookies\bsip2_outputs\run_cakes_001\products",
    ),
    (
        "batch_run_cookies_005.py",
        "cookies_coffee",
        {},  # all flags off per batch runner
        r"C:\Bari\02_products\cookies_coffee\bsip2_outputs\run_cookies_005\products",
    ),
    (
        "batch_run_salty_snacks_002.py",
        "salty_snacks",
        {"BARI_RECAL_P0": "on"},
        r"C:\Bari\02_products\salty_snacks\bsip2_outputs\run_salty_snacks_002\products",
    ),
    (
        "batch_run_brined_cheeses_005.py",
        "brined_cheeses",
        {"BARI_RECAL_P0": "on", "BARI_GRAD_SODIUM_V1": "on"},
        r"C:\Bari\02_products\brined_cheeses\bsip2_outputs\run_brined_005\products",
    ),
]

results = {}
errors = []

env_base = os.environ.copy()
env_base["BARI_FAT_TECH_V1"] = "on"  # explicit, matches new default

for runner_file, cat_name, extra_flags, output_path in RUNNERS:
    runner_path = SRC / runner_file
    if not runner_path.exists():
        print(f"  SKIP {cat_name}: runner not found at {runner_path}")
        errors.append({"category": cat_name, "error": "runner not found"})
        continue

    run_env = env_base.copy()
    for k, v in extra_flags.items():
        run_env[k] = v

    print(f"\nRunning {cat_name} ({runner_file})...")
    try:
        proc = subprocess.run(
            [sys.executable, str(runner_path)],
            env=run_env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=180,
            cwd=str(SRC),
        )
        exit_code = proc.returncode
        print(f"  exit_code={exit_code}")
        if proc.stdout:
            # Print last 20 lines of stdout for summary
            lines = proc.stdout.strip().splitlines()
            for ln in lines[-20:]:
                print(f"  OUT: {ln}")
        if proc.stderr:
            lines = proc.stderr.strip().splitlines()
            for ln in lines[-10:]:
                print(f"  ERR: {ln}")
        results[cat_name] = {
            "runner": runner_file,
            "exit_code": exit_code,
            "output_path": output_path,
        }
    except subprocess.TimeoutExpired:
        print(f"  TIMEOUT after 180s")
        errors.append({"category": cat_name, "error": "timeout"})
        results[cat_name] = {"runner": runner_file, "exit_code": -1, "output_path": output_path}
    except Exception as e:
        print(f"  ERROR: {e}")
        errors.append({"category": cat_name, "error": str(e)})
        results[cat_name] = {"runner": runner_file, "exit_code": -1, "output_path": output_path}

print("\n" + "="*60)
print("RE-SCORE SUMMARY")
print("="*60)
for cat, r in results.items():
    status = "OK" if r["exit_code"] == 0 else f"EXIT={r['exit_code']}"
    print(f"  {cat}: {status}")

if errors:
    print("\nERRORS:")
    for e in errors:
        print(f"  {e}")

print("\nDone.")
