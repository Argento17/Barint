"""TASK-505 — Dependency & security maintenance report (READ-ONLY).

Aggregates:
  - bari-web:  npm audit --json  +  npm outdated --json
  - Python:    pip list --outdated --format=json  +  pip-audit --format=json (optional)

into a single markdown report at:
  03_operations/maintenance/reports/deps_report_<YYYY-MM-DD>.md

This script only READS and reports. It never modifies package.json, lockfiles,
requirements, or installed packages. Triage is propose-only; humans/PR flow apply.

Usage:  python 03_operations/maintenance/deps_report.py
Exit code: 0 if the report was written, 1 on internal failure.
"""

import json
import subprocess
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(r"C:\Bari")
WEB_DIR = REPO_ROOT / "bari-web"
REPORTS_DIR = REPO_ROOT / "03_operations" / "maintenance" / "reports"

SEVERITY_ORDER = ["critical", "high", "moderate", "low", "info"]

# Packages whose MAJOR bumps require the Frontend Agent (per skill triage rules).
FRONTEND_GATED = {"next", "react", "react-dom", "@playwright/test", "playwright"}


def run_cmd(cmd, cwd=None, timeout=300):
    """Run a command, tolerating non-zero exit codes (npm audit exits non-zero
    when vulnerabilities exist — that's data, not a crash). Returns
    (stdout, stderr, returncode) or (None, error_message, None) if the tool
    could not be executed at all."""
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(cwd) if cwd else None,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            shell=True,  # resolves npm.cmd / pip on Windows PATH
        )
        return proc.stdout, proc.stderr, proc.returncode
    except subprocess.TimeoutExpired:
        return None, f"TIMEOUT after {timeout}s: {cmd}", None
    except OSError as exc:
        return None, f"could not execute: {exc}", None


def parse_json(text):
    if not text or not text.strip():
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


# ---------------------------------------------------------------- npm audit
def collect_npm_audit():
    """Returns (vulns:list[dict], meta:str). Each vuln:
    {name, severity, range, fixed_in, direct, via}"""
    stdout, stderr, rc = run_cmd("npm audit --json", cwd=WEB_DIR)
    if stdout is None:
        return None, f"npm audit FAILED to run: {stderr}"
    data = parse_json(stdout)
    if data is None:
        return None, f"npm audit produced unparseable output (rc={rc}): {(stderr or stdout or '')[:300]}"

    vulns = []
    for name, v in (data.get("vulnerabilities") or {}).items():
        fix = v.get("fixAvailable")
        if fix is True:
            fixed_in = "fix available (npm audit fix)"
        elif isinstance(fix, dict):
            fixed_in = f"{fix.get('name', name)}@{fix.get('version', '?')}" + (
                " (SEMVER-MAJOR)" if fix.get("isSemVerMajor") else ""
            )
        else:
            fixed_in = "no fix available"
        via_titles = [x.get("title") for x in v.get("via", []) if isinstance(x, dict) and x.get("title")]
        vulns.append({
            "name": name,
            "severity": (v.get("severity") or "info").lower(),
            "range": v.get("range", "?"),
            "fixed_in": fixed_in,
            "direct": bool(v.get("isDirect")),
            "via": "; ".join(via_titles) or "(transitive)",
        })
    totals = (data.get("metadata") or {}).get("vulnerabilities") or {}
    meta = f"npm audit rc={rc}; totals: " + ", ".join(
        f"{s}={totals.get(s, 0)}" for s in SEVERITY_ORDER if s in totals
    ) if totals else f"npm audit rc={rc}; no vulnerability metadata"
    vulns.sort(key=lambda x: SEVERITY_ORDER.index(x["severity"]) if x["severity"] in SEVERITY_ORDER else 99)
    return vulns, meta


# ------------------------------------------------------------- npm outdated
def collect_npm_outdated():
    """Returns (majors:list, minors:list, meta:str). Each entry:
    {name, current, wanted, latest}"""
    stdout, stderr, rc = run_cmd("npm outdated --json", cwd=WEB_DIR)
    if stdout is None:
        return None, None, f"npm outdated FAILED to run: {stderr}"
    data = parse_json(stdout)
    if data is None:
        if rc == 0 and not (stdout or "").strip():
            return [], [], "npm outdated rc=0; everything up to date"
        return None, None, f"npm outdated produced unparseable output (rc={rc}): {(stderr or stdout or '')[:300]}"

    majors, minors = [], []
    for name, info in data.items():
        entry = {
            "name": name,
            "current": info.get("current", "MISSING"),
            "wanted": info.get("wanted", "?"),
            "latest": info.get("latest", "?"),
        }
        cur_major = str(entry["current"]).lstrip("v").split(".")[0]
        lat_major = str(entry["latest"]).lstrip("v").split(".")[0]
        if cur_major.isdigit() and lat_major.isdigit() and int(lat_major) > int(cur_major):
            majors.append(entry)
        else:
            minors.append(entry)
    meta = f"npm outdated rc={rc}; {len(majors)} major, {len(minors)} minor/patch"
    return majors, minors, meta


# ------------------------------------------------------------ pip outdated
def collect_pip_outdated():
    stdout, stderr, rc = run_cmd(f'"{sys.executable}" -m pip list --outdated --format=json --disable-pip-version-check')
    if stdout is None:
        return None, None, f"pip list --outdated FAILED to run: {stderr}"
    data = parse_json(stdout)
    if data is None:
        return None, None, f"pip list --outdated produced unparseable output (rc={rc})"

    majors, minors = [], []
    for pkg in data:
        entry = {
            "name": pkg.get("name", "?"),
            "current": pkg.get("version", "?"),
            "wanted": pkg.get("latest_version", "?"),
            "latest": pkg.get("latest_version", "?"),
        }
        cur_major = str(entry["current"]).split(".")[0]
        lat_major = str(entry["latest"]).split(".")[0]
        if cur_major.isdigit() and lat_major.isdigit() and int(lat_major) > int(cur_major):
            majors.append(entry)
        else:
            minors.append(entry)
    meta = f"pip list --outdated rc={rc}; {len(majors)} major, {len(minors)} minor/patch"
    return majors, minors, meta


# -------------------------------------------------------------- pip-audit
def collect_pip_audit():
    """Returns (vulns:list|None, meta:str). Not-installed is reported, not fatal."""
    try:
        stdout, stderr, rc = run_cmd(f'"{sys.executable}" -m pip_audit --format=json --progress-spinner=off', timeout=420)
        if stdout is None:
            return None, f"pip-audit FAILED to run: {stderr}"
        if rc is not None and "No module named" in (stderr or ""):
            return None, "pip-audit NOT INSTALLED (pip install pip-audit to enable Python CVE scanning)"
        data = parse_json(stdout)
        if data is None:
            return None, f"pip-audit output unparseable (rc={rc}): {(stderr or stdout or '')[:300]}"
        deps = data.get("dependencies", data) if isinstance(data, dict) else data
        vulns = []
        for dep in deps or []:
            for v in dep.get("vulns", []):
                vulns.append({
                    "name": dep.get("name", "?"),
                    "severity": "unknown",
                    "range": dep.get("version", "?"),
                    "fixed_in": ", ".join(v.get("fix_versions") or []) or "no fix listed",
                    "direct": True,
                    "via": v.get("id", "?"),
                })
        return vulns, f"pip-audit rc={rc}; {len(vulns)} vulnerabilities"
    except Exception as exc:  # honest degradation, never crash the report
        return None, f"pip-audit NOT INSTALLED or errored: {exc}"


# ----------------------------------------------------------------- triage
def build_triage(npm_vulns, npm_majors, npm_minors, pip_vulns):
    """Propose-only triage rows: (package, ecosystem, action, reason)."""
    rows = []
    for v in npm_vulns or []:
        if v["severity"] in ("critical", "high"):
            action = "patch now" if "SEMVER-MAJOR" not in v["fixed_in"] and v["fixed_in"] != "no fix available" else "propose major"
            if v["fixed_in"] == "no fix available":
                action = "ignore-with-reason"
                reason = f"{v['severity']} but no fix released yet; re-check next run ({v['via'][:80]})"
            else:
                reason = f"{v['severity']} vulnerability; fix: {v['fixed_in']}"
        elif v["severity"] == "moderate":
            action = "batch"
            reason = f"moderate vulnerability; fix: {v['fixed_in']}"
        else:
            action = "ignore-with-reason"
            reason = f"low/info severity; batch with next routine update ({v['fixed_in']})"
        rows.append((v["name"], "npm", action, reason))

    vuln_names = {v["name"] for v in (npm_vulns or [])}
    for m in npm_majors or []:
        gate = " — REQUIRES Frontend Agent" if m["name"] in FRONTEND_GATED else ""
        rows.append((m["name"], "npm", "propose major",
                     f"{m['current']} -> {m['latest']} breaking-risk; needs migration notes{gate}"))
    if npm_minors:
        clean = [m["name"] for m in npm_minors if m["name"] not in vuln_names]
        if clean:
            rows.append((", ".join(clean[:15]) + (" …" if len(clean) > 15 else ""), "npm", "batch",
                         f"{len(clean)} minor/patch bumps; low-risk batch behind build+e2e green"))
    for v in pip_vulns or []:
        rows.append((v["name"], "pip", "patch now", f"advisory {v['via']}; fix: {v['fixed_in']}"))
    return rows


def md_table(headers, rows):
    if not rows:
        return "_None found._\n"
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(c).replace("|", "\\|").replace("\n", " ") for c in r) + " |")
    return "\n".join(out) + "\n"


def main():
    today = date.today().isoformat()
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORTS_DIR / f"deps_report_{today}.md"

    print(f"[deps_report] collecting — npm cwd={WEB_DIR}")
    npm_vulns, audit_meta = collect_npm_audit()
    npm_majors, npm_minors, outdated_meta = collect_npm_outdated()
    pip_majors, pip_minors, pip_meta = collect_pip_outdated()
    pip_vulns, pip_audit_meta = collect_pip_audit()

    triage = build_triage(npm_vulns, npm_majors, npm_minors, pip_vulns)

    n_vulns = len(npm_vulns or []) + len(pip_vulns or [])
    n_majors = len(npm_majors or []) + len(pip_majors or [])
    n_minors = len(npm_minors or []) + len(pip_minors or [])

    lines = [
        f"# Dependency & Security Report — {today}",
        "",
        "> READ-ONLY report (TASK-505 maintenance lane). Nothing was modified.",
        "> Triage actions are PROPOSALS — apply via normal PR flow with build + e2e green.",
        "",
        "## Summary",
        f"- Security vulnerabilities: **{n_vulns}** ({audit_meta}; {pip_audit_meta})",
        f"- Outdated majors (breaking-risk): **{n_majors}**",
        f"- Outdated minors/patches (batch candidates): **{n_minors}**",
        f"- Tool status: {outdated_meta}; {pip_meta}",
        "",
        "## 1. Security vulnerabilities (by severity)",
        "",
        "### npm (bari-web)",
        md_table(
            ["Package", "Severity", "Vulnerable range", "Fixed in", "Direct?", "Advisory"],
            [(v["name"], v["severity"], v["range"], v["fixed_in"], "yes" if v["direct"] else "no", v["via"][:120])
             for v in (npm_vulns or [])],
        ) if npm_vulns is not None else f"_UNAVAILABLE — {audit_meta}_\n",
        "### Python (pip-audit)",
        md_table(
            ["Package", "Installed", "Fixed in", "Advisory"],
            [(v["name"], v["range"], v["fixed_in"], v["via"]) for v in (pip_vulns or [])],
        ) if pip_vulns is not None else f"_{pip_audit_meta}_\n",
        "## 2. Outdated majors (breaking-risk — propose-only, never applied unattended)",
        "",
        "### npm (bari-web)",
        md_table(["Package", "Current", "Wanted", "Latest"],
                 [(m["name"], m["current"], m["wanted"], m["latest"]) for m in (npm_majors or [])])
        if npm_majors is not None else f"_UNAVAILABLE — {outdated_meta}_\n",
        "### Python",
        md_table(["Package", "Current", "Latest"],
                 [(m["name"], m["current"], m["latest"]) for m in (pip_majors or [])])
        if pip_majors is not None else f"_UNAVAILABLE — {pip_meta}_\n",
        "## 3. Outdated minors/patches (low-risk batch candidates)",
        "",
        "### npm (bari-web)",
        md_table(["Package", "Current", "Wanted", "Latest"],
                 [(m["name"], m["current"], m["wanted"], m["latest"]) for m in (npm_minors or [])])
        if npm_minors is not None else f"_UNAVAILABLE — {outdated_meta}_\n",
        "### Python",
        md_table(["Package", "Current", "Latest"],
                 [(m["name"], m["current"], m["latest"]) for m in (pip_minors or [])])
        if pip_minors is not None else f"_UNAVAILABLE — {pip_meta}_\n",
        "## 4. Triage recommendations (propose-only)",
        "",
        md_table(["Package", "Ecosystem", "Action", "Reason"], triage),
        "",
        "---",
        "_Generated by `03_operations/maintenance/deps_report.py`. "
        "Rules: security patches within same major -> normal PR flow (build + e2e green); "
        "majors -> propose with migration notes; next/react/playwright majors -> Frontend Agent; "
        "never auto-merge; never touch the deploy repo directly._",
    ]

    report_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"[deps_report] wrote {report_path}")
    print(f"[deps_report] SUMMARY: vulns={n_vulns} majors={n_majors} minors={n_minors}")
    print(f"[deps_report]   {audit_meta}")
    print(f"[deps_report]   {outdated_meta}")
    print(f"[deps_report]   {pip_meta}")
    print(f"[deps_report]   {pip_audit_meta}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        print(f"[deps_report] FATAL: {exc}", file=sys.stderr)
        sys.exit(1)
