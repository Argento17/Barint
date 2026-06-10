#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_llm_import_tripwire.py — Deliverable 3 (TASK-BARI-PROMPT-REGISTRY-CI-EVAL-V1)

Enforces the `llm-import-tripwire` rule from prompt_registry_v1.yaml:

  FAIL if any anthropic / openai / litellm SDK import appears ANYWHERE outside
  `.venv/` UNLESS that import site is registered in prompt_registry_v1.yaml with
  model_boundary: runtime_api AND status: production AND a reviewer.

This prevents a future live LLM call from silently bypassing the prompt registry.
Bari makes ZERO programmatic LLM calls today, so the expected match set is EMPTY.

Exit 0 = no unregistered matches. Non-zero = unregistered LLM import found.
"""
import sys, io, re
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

try:
    import yaml
except ImportError:
    print("PyYAML required"); sys.exit(2)

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
REGISTRY = REPO / "01_framework" / "operations" / "prompt_registry_v1.yaml"

SKIP_DIRS = {".venv", "node_modules", ".git", ".next", "dist", "build",
             "__pycache__", ".pytest_cache", "out", ".turbo"}

PY_PATTERNS = [
    re.compile(r"^\s*import\s+(anthropic|openai|litellm)\b"),
    re.compile(r"^\s*from\s+(anthropic|openai|litellm)\b"),
]
TS_PATTERNS = [
    re.compile(r"""from\s+['"]@anthropic-ai/"""),
    re.compile(r"""from\s+['"]openai['"]"""),
    re.compile(r"""require\(\s*['"](openai|@anthropic-ai/[^'"]+|litellm)['"]\s*\)"""),
]
EXTS = {".py": PY_PATTERNS, ".ts": TS_PATTERNS, ".tsx": TS_PATTERNS,
        ".js": TS_PATTERNS, ".jsx": TS_PATTERNS, ".mjs": TS_PATTERNS}


def registered_runtime_api_files():
    """Files explicitly allowed to hold a live LLM import (none expected in v1)."""
    if not REGISTRY.exists():
        return set()
    doc = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    allow = set()
    for s in doc.get("surfaces", []):
        if s.get("model_boundary") == "runtime_api" and s.get("status") == "production" and s.get("reviewer"):
            sf = s.get("source_file", "")
            allow.add(sf)
    return allow


def scan():
    hits = []
    for path in REPO.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        pats = EXTS.get(path.suffix)
        if not pats:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            for pat in pats:
                if pat.search(line):
                    hits.append((str(path.relative_to(REPO)).replace("\\", "/"), i, line.strip()))
    return hits


def main():
    allow = registered_runtime_api_files()
    hits = scan()
    unregistered = [h for h in hits if h[0] not in allow]
    print(f"registered runtime_api files (allowed): {sorted(allow) or 'none'}")
    print(f"LLM SDK import matches outside .venv: {len(hits)}")
    for f, ln, src in hits:
        status = "ALLOWED(registered)" if f in allow else "UNREGISTERED"
        print(f"  [{status}] {f}:{ln}  {src}")
    print("-" * 50)
    if unregistered:
        print(f"FAIL: {len(unregistered)} unregistered LLM import(s) outside .venv. "
              f"Register as runtime_api + reviewer in prompt_registry_v1.yaml or remove.")
        return 1
    print("PASS: zero unregistered LLM SDK imports outside .venv (expected).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
