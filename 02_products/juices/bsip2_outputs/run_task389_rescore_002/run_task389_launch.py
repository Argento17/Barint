# -*- coding: utf-8 -*-
"""
Launcher for TASK-389 run_002 — sets all env vars BEFORE spawning the batch script
as a fresh subprocess, guaranteeing env-before-import for all engine modules.
"""
import os, sys, subprocess, pathlib

# ── Set all flags in this process env ─────────────────────────────────────────
FLAGS = {
    "BARI_SHELF_RELATIVE_V1": "on",
    "BARI_FAT_TECH_V1": "on",
    "BARI_RECAL_P0": "on",
    "BARI_TASK144_FIXES": "off",
    "BARI_SODIUM_SHELF_RELATIVE_V1": "off",
    "BARI_DAIRY_PROTEIN_REWEIGHT_V1": "off",
    "BARI_REDLABEL_V1": "off",
    "BARI_SODIUM_CEREAL": "off",
    "BARI_GRAD_SODIUM_V1": "off",
}

env = os.environ.copy()
for k, v in FLAGS.items():
    env[k] = v

print("Launcher: env flags set:", flush=True)
for k, v in FLAGS.items():
    print(f"  {k}={v}", flush=True)

batch_script = pathlib.Path(__file__).parent / "batch_run_002.py"
print(f"\nLauncher: spawning {batch_script} as subprocess...\n", flush=True)

result = subprocess.run(
    [sys.executable, str(batch_script)],
    env=env,
    cwd=str(pathlib.Path(__file__).parent),
)

print(f"\nLauncher: subprocess exit code = {result.returncode}", flush=True)
sys.exit(result.returncode)
