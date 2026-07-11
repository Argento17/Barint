---
name: deps
description: Dependency & security maintenance lane (TASK-505) — run the read-only deps report, triage vulnerabilities and outdated packages, and propose (never auto-apply) updates. Use weekly, before any release, and after any security advisory.
---

# Dependency & Security Maintenance Lane

Minimal, honest maintenance lane: **report + triage, never auto-update.** The
report script only reads; every change ships through the normal PR flow.

## When to run

1. **Weekly routine** — once a week as part of orchestrator hygiene.
2. **Before any release / go-live** — a category launch or deploy PR is not
   ready if a critical/high npm vulnerability is unreviewed.
3. **After any security advisory** — GitHub Dependabot alert, npm advisory,
   CVE mentioned anywhere touching our stack (Next.js, React, Playwright,
   sharp, etc.).

## The command

```
python C:\Bari\03_operations\maintenance\deps_report.py
```

- Aggregates `npm audit` + `npm outdated` (cwd = `C:\bari\bari-web`) and
  `pip list --outdated` + `pip-audit` (if installed) into one markdown report.
- Output: `C:\Bari\03_operations\maintenance\reports\deps_report_<YYYY-MM-DD>.md`
- The script is READ-ONLY. It never modifies `package.json`, lockfiles,
  requirements, or installed packages. Non-zero `npm audit` exit codes are
  data (vulns exist), not failures.
- If `pip-audit` is not installed the report says NOT INSTALLED honestly;
  it does not fail.

## Triage rules

| Situation | Action |
|---|---|
| Security patch available **within the same major** | Apply via normal PR flow. PR merges only with `npm run build` AND `npm run test:e2e` green. |
| Fix requires a **major** bump (SEMVER-MAJOR) | **Propose-only.** Write migration notes (breaking changes, affected code paths). Never applied unattended. |
| Major bump touches **next / react / react-dom / playwright / @playwright/test** | Requires the **Frontend Agent** to own the migration — never done as a mechanical bump. |
| Moderate-severity vuln, fix available | Batch into the next routine update PR. |
| Low/info severity, or no fix released | Ignore-with-reason in the report; re-check next weekly run. |
| Minor/patch outdated (no vuln) | Low-risk batch candidate — one batch PR, build + e2e green required. |
| Python package vuln (pip-audit) | Patch now via PR; verify affected pipeline scripts still run. |

Escalation: none of this reaches the owner unless a tripwire fires (e.g., a
vulnerability forces an irreversible consumer-facing change). Default is
autonomous triage + PR, logged in the registry if tracked.

## Output contract

Every run of this skill returns:

1. **Report path** — the `deps_report_<date>.md` file written.
2. **Top-3 actions** — the three highest-priority triage rows (security first,
   then majors, then batch), each as: package → action → one-line reason.
3. Honest tool status — anything that was UNAVAILABLE or NOT INSTALLED.

## Never rules (hard)

- **Never auto-merge** a dependency PR. A human-reviewable PR is the ceiling
  of autonomy for this lane.
- **Never update a lockfile without running `npm run build` + `npm run test:e2e`**
  and confirming both green in the PR.
- **Never touch the deploy repo directly** (LIVE = Argento17/Barint master via
  Vercel). All changes go through branch → PR on the monorepo; nothing is
  pushed to production remotes from this lane.
- Never let the report script (or this lane) modify `package.json`, lockfiles,
  or installed packages as part of "reporting" — reading and writing are
  separate steps, and writing is always a PR.
