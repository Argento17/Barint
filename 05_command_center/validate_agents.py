#!/usr/bin/env python3
"""
Agent Registry Schema Validator
================================
Validates every .claude/agents/*.md file against the required schema.
Fails with a non-zero exit code if any agent file is malformed.

Usage:
    python validate_agents.py          # full report
    python validate_agents.py --strict # exit 1 on any warning too
    python validate_agents.py --json   # machine-readable output

Called by generate_dashboard.py (advisory) and available as a standalone CI check.
"""

import sys
import re
import json
import argparse
from pathlib import Path

try:
    import yaml
except ImportError:
    raise SystemExit("PyYAML required: C:\\Bari\\.venv\\Scripts\\python.exe -m pip install pyyaml")

# ── Schema ───────────────────────────────────────────────────────────────────

REQUIRED_FRONTMATTER = {
    "name":    str,
    "description": str,
    "version": (str, int, float),
}

OPTIONAL_FRONTMATTER = {
    "successor-to": str,
    "changelog":    list,
}

REQUIRED_SECTIONS = [
    "## Mission",
    "## Workspace",
    "## Responsibilities",
    "## Does Not Own",
    "## Hard Rules",
    "## Autonomy Mandate",
    "## Escalation Rules",
]

REQUIRED_BODY_FIELDS = [
    "## Inputs",
    "## Outputs",
]

VALID_OWNERS = {
    "product-agent", "nutrition-agent", "research-agent", "data-agent",
    "frontend-agent", "design-agent", "qa-agent", "content-agent",
    "marketing-agent", "cc-agent", "red-team-agent",
}

CHANGELOG_ENTRY_KEYS = {"version", "date", "summary"}

# ── Parser ────────────────────────────────────────────────────────────────────

def parse_agent_file(path: Path) -> tuple[dict | None, str]:
    raw = path.read_text(encoding="utf-8")
    m = re.match(r"(?s)^---\s*\n(.*?)\n---\s*\n(.*)", raw)
    if not m:
        return None, raw
    try:
        fm = yaml.safe_load(m.group(1))
    except yaml.YAMLError as e:
        return None, raw
    if not isinstance(fm, dict):
        return None, raw
    return fm, m.group(2)


def validate_agent(path: Path) -> list[dict]:
    """Returns a list of findings: {level: error|warning|ok, field: str, message: str}"""
    findings = []

    def err(field, msg):
        findings.append({"level": "error", "field": field, "message": msg})

    def warn(field, msg):
        findings.append({"level": "warning", "field": field, "message": msg})

    fm, body = parse_agent_file(path)

    if fm is None:
        err("frontmatter", "Could not parse YAML frontmatter block")
        return findings

    # Required frontmatter fields
    for key, typ in REQUIRED_FRONTMATTER.items():
        if key not in fm:
            err(key, f"Required frontmatter field '{key}' is missing")
        elif not isinstance(fm[key], typ if isinstance(typ, tuple) else (typ,)):
            err(key, f"Field '{key}' must be type {typ.__name__ if not isinstance(typ, tuple) else '/'.join(t.__name__ for t in typ)}, got {type(fm[key]).__name__}")
        elif key in ("name", "description") and not str(fm[key]).strip():
            err(key, f"Field '{key}' must not be empty")

    # Version must be parseable as semver (at minimum X.Y)
    ver = str(fm.get("version", "")).strip()
    if ver and not re.match(r"^\d+\.\d+", ver):
        warn("version", f"Version '{ver}' is not semver (expected X.Y or X.Y.Z)")

    # Changelog — optional but validated if present
    cl = fm.get("changelog")
    if cl is not None:
        if not isinstance(cl, list):
            err("changelog", "changelog must be a YAML list of entries")
        else:
            for i, entry in enumerate(cl):
                if not isinstance(entry, dict):
                    err("changelog", f"changelog[{i}] must be a mapping")
                    continue
                missing = CHANGELOG_ENTRY_KEYS - entry.keys()
                if missing:
                    warn("changelog", f"changelog[{i}] missing keys: {sorted(missing)}")
    else:
        warn("changelog", "No changelog section — add changelog: [] to frontmatter (see agent_router_v1.md §Versioning)")

    # Required body sections
    for section in REQUIRED_SECTIONS:
        if section not in body:
            err("body", f"Required section '{section}' not found in agent body")

    # Recommended body fields
    for field in REQUIRED_BODY_FIELDS:
        if field not in body:
            warn("body", f"Recommended section '{field}' not found")

    # Description quality: must be >= 30 chars (meaningful dispatch trigger)
    desc = str(fm.get("description", "")).strip()
    if len(desc) < 30:
        warn("description", f"Description is very short ({len(desc)} chars) — dispatch matching may be imprecise")

    # Check for routing ambiguity keywords across agents (done at aggregate level below)

    return findings


# ── Coverage check ────────────────────────────────────────────────────────────

EXPECTED_DOMAINS = {
    "product strategy": ["product-agent"],
    "nutrition / scoring": ["nutrition-agent"],
    "research / evidence": ["research-agent"],
    "data pipeline": ["data-agent"],
    "frontend / UI": ["frontend-agent"],
    "design / UX": ["design-agent"],
    "QA / verification": ["qa-agent"],
    "content / copy": ["content-agent"],
    "marketing / SEO": ["marketing-agent"],
    "command center / registry": ["cc-agent"],
    "challenge / red-team": ["red-team-agent"],
}


def check_coverage(agent_names: set[str]) -> list[dict]:
    gaps = []
    for domain, owners in EXPECTED_DOMAINS.items():
        missing = [o for o in owners if o not in agent_names]
        if missing:
            gaps.append({
                "domain": domain,
                "expected_owner": owners,
                "status": "MISSING",
                "message": f"No agent file found for domain '{domain}' (expected: {owners})",
            })
    return gaps


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Validate Bari agent registry schema")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as errors")
    parser.add_argument("--json", action="store_true", dest="as_json", help="Output JSON")
    args = parser.parse_args()

    agents_dir = Path(r"C:\Bari\.claude\agents")
    if not agents_dir.exists():
        print(f"ERROR: agents dir not found: {agents_dir}", file=sys.stderr)
        sys.exit(1)

    agent_files = sorted(agents_dir.glob("*.md"))
    if not agent_files:
        print("ERROR: no agent files found", file=sys.stderr)
        sys.exit(1)

    results = {}
    agent_names = set()
    all_errors = 0
    all_warnings = 0

    for f in agent_files:
        findings = validate_agent(f)
        results[f.name] = findings
        errors   = [x for x in findings if x["level"] == "error"]
        warnings = [x for x in findings if x["level"] == "warning"]
        all_errors   += len(errors)
        all_warnings += len(warnings)
        # extract agent slug from filename
        agent_names.add(f.stem)

    coverage_gaps = check_coverage(agent_names)

    if args.as_json:
        print(json.dumps({
            "agents": results,
            "coverage_gaps": coverage_gaps,
            "summary": {"errors": all_errors, "warnings": all_warnings, "coverage_gaps": len(coverage_gaps)},
        }, indent=2, ensure_ascii=False))
    else:
        print(f"\n{'='*60}")
        print(f"  Bari Agent Registry Validation — {len(agent_files)} agents")
        print(f"{'='*60}\n")

        for fname, findings in results.items():
            errors   = [x for x in findings if x["level"] == "error"]
            warnings = [x for x in findings if x["level"] == "warning"]
            status = "PASS" if not errors and not warnings else ("WARN" if not errors else "FAIL")
            print(f"  [{status:4}]  {fname}")
            for f in findings:
                sym = "  ERROR" if f["level"] == "error" else "   WARN"
                print(f"            {sym}  [{f['field']}]  {f['message']}")

        if coverage_gaps:
            print(f"\n  Coverage Gaps ({len(coverage_gaps)}):")
            for g in coverage_gaps:
                print(f"    MISSING  {g['domain']}: {g['message']}")

        print(f"\n  Summary: {all_errors} errors, {all_warnings} warnings, {len(coverage_gaps)} coverage gaps")
        if all_errors == 0 and (not args.strict or all_warnings == 0):
            print("  Status: CLEAN\n")
        else:
            print("  Status: NEEDS ATTENTION\n")

    exit_code = 0
    if all_errors > 0:
        exit_code = 1
    elif args.strict and all_warnings > 0:
        exit_code = 1
    elif len(coverage_gaps) > 0:
        exit_code = 1
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
