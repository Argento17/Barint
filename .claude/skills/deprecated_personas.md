# Deprecated Persona Files — Bari

**Status:** ACTIVE RETIREMENT PLAN
**Published:** 2026-05-31
**Task:** TASK-049E
**Owner:** Product Agent + Frontend Agent

This document formally retires the legacy persona architecture and maps each deprecated persona to its successor agent definition file.

---

## Retirement Statement

The six legacy persona files listed below are **deprecated as of 2026-05-31**. They must not be used for any new work. They are retained in the repository for historical reference only and may be deleted after a 30-day grace period (2026-07-01) unless an active dependency is discovered.

The Agent Architecture defined in `C:\Bari\.claude\agents\` is now the single source of truth for all agent behavior.

---

## Persona → Agent Migration Map

| Deprecated Persona File | Successor Agent File | Migration Status |
|---|---|---|
| `skills/head-of-product.md` | `agents/product-agent.md` | COMPLETE |
| `skills/chief-nutrition-officer.md` | `agents/nutrition-agent.md` | COMPLETE |
| `skills/research-analyst.md` | `agents/research-agent.md` | COMPLETE |
| `skills/frontend-architect.md` | `agents/frontend-agent.md` | COMPLETE |
| `skills/design-director.md` | `agents/design-agent.md` | COMPLETE |
| `skills/qa-audit-lead.md` | `agents/qa-agent.md` | COMPLETE |

---

## What Was Migrated

### head-of-product.md → product-agent.md

| Content Type | Migrated | Notes |
|---|---|---|
| Role definition and workspace map | ✓ | |
| Responsibilities | ✓ | |
| Does Not Own | ✓ | |
| Decision Rights | ✓ | Expanded with full D1–D16 matrix entries |
| Expected Outputs | ✓ | Renamed to Outputs |
| Hard Rules | ✓ | All 7 rules migrated verbatim; Rule 8 added (scoring rule joint approval) |
| Interaction Rules with Other Bari Skills | ✓ | Updated terminology: Skills → Agents |
| Default Response Style | ✓ | |
| Requires consultation / Cannot override | ✓ | Absorbed into Decision Rights and Escalation Rules |
| New in v2 | — | Inputs, Core/Supporting/Optional/Restricted Skills, Escalation Rules |

### chief-nutrition-officer.md → nutrition-agent.md

| Content Type | Migrated | Notes |
|---|---|---|
| Role definition and workspace map | ✓ | |
| Responsibilities | ✓ | |
| Does Not Own | ✓ | |
| Decision Rights | ✓ | Expanded with full D1–D16 matrix entries |
| Expected Outputs | ✓ | |
| Hard Rules | ✓ | All 7 rules migrated verbatim; Rule 8 added (joint scoring approval) |
| Interaction Rules | ✓ | Terminology updated |
| Default Response Style | ✓ | |
| New in v2 | — | Inputs, Core/Supporting/Optional/Restricted Skills, Escalation Rules |

### research-analyst.md → research-agent.md

| Content Type | Migrated | Notes |
|---|---|---|
| Role definition and workspace map | ✓ | |
| Responsibilities | ✓ | |
| Does Not Own | ✓ | |
| Evidence Tier Classification | ✓ | Migrated verbatim — critical taxonomy |
| Decision Rights | ✓ | Expanded |
| Expected Outputs | ✓ | |
| Source Hierarchy | ✓ | Migrated verbatim |
| Hard Rules | ✓ | All 7 migrated verbatim; Rule 8 added (no open-ended research) |
| Interaction Rules | ✓ | Terminology updated |
| Default Response Style | ✓ | |
| New in v2 | — | Inputs, Core/Supporting/Optional/Restricted Skills, Escalation Rules |

### frontend-architect.md → frontend-agent.md

| Content Type | Migrated | Notes |
|---|---|---|
| Role definition and workspace map | ✓ | Both repo paths preserved |
| Key paths (src/ structure) | ✓ | Migrated verbatim |
| Responsibilities | ✓ | |
| Does Not Own | ✓ | |
| Canonical Component Rules | ✓ | Migrated verbatim — frozen constraints |
| Legacy quarantine list | ✓ | Migrated verbatim |
| Decision Rights | ✓ | Expanded with D15 infrastructure ownership |
| Expected Outputs | ✓ | |
| Hard Rules | ✓ | All 7 migrated verbatim; Rule 8 (no component without spec) and Rule 9 (skill installation review) added |
| Interaction Rules | ✓ | Terminology updated |
| Default Response Style | ✓ | |
| New in v2 | — | Inputs, Core/Supporting/Optional/Restricted Skills, Escalation Rules |

### design-director.md → design-agent.md

| Content Type | Migrated | Notes |
|---|---|---|
| Role definition and workspace map | ✓ | |
| Responsibilities | ✓ | |
| Does Not Own | ✓ | |
| Gen 1 Design Constraints | ✓ | Migrated verbatim — frozen |
| Drift Detection criteria | ✓ | Migrated verbatim — critical |
| Decision Rights | ✓ | Expanded |
| Expected Outputs | ✓ | |
| Hard Rules | ✓ | All 7 migrated verbatim; Rule 8 (no build without spec) added |
| Interaction Rules | ✓ | Terminology updated |
| Default Response Style | ✓ | |
| New in v2 | — | Inputs, Core/Supporting/Optional/Restricted Skills, Escalation Rules |

### qa-audit-lead.md → qa-agent.md

| Content Type | Migrated | Notes |
|---|---|---|
| Role definition and workspace map | ✓ | Both repos preserved |
| Responsibilities | ✓ | |
| Does Not Own | ✓ | |
| All 4 checklists | ✓ | Migrated verbatim — operational |
| Decision Rights | ✓ | Expanded; D9 authority clarified |
| Expected Outputs | ✓ | |
| Hard Rules | ✓ | All 7 migrated verbatim; Rule 8 (no baseline freeze over hard fails) added |
| Interaction Rules | ✓ | Terminology updated |
| Default Response Style | ✓ | |
| New in v2 | — | Inputs, Core/Supporting/Optional/Restricted Skills, Escalation Rules |

---

## What Was Not Migrated

The following persona content was intentionally excluded from the agent definitions:

| Content | Reason |
|---|---|
| Persona "you are X" framing | Replaced by Mission statement |
| "Requires consultation" and "Cannot override" decision right subsections | Absorbed into unified Decision Rights table using D1–D16 from `decision_rights_matrix.md` |
| Redundant repository map repetition in every file | Single canonical workspace table per agent |
| "When to Use — invoke this skill when" sections | Replaced by the `description` YAML frontmatter (Claude Code skill trigger) |

---

## Conflicts Discovered During Migration

No policy conflicts were discovered. All hard rules, decision rights, and responsibilities from the persona files are consistent with `agent_os_v1.md`, `capability_stack_matrix.md`, and `decision_rights_matrix.md`.

Two gaps were identified and filled:

| Gap | Resolution |
|---|---|
| Persona files had no explicit skill assignments | Each agent definition now includes Core/Supporting/Optional/Restricted skill tiers from `capability_stack_matrix.md` |
| Persona files had no escalation rules as a distinct section | Each agent definition now has an Escalation Rules section derived from `agent_os_v1.md` |

---

## Deprecation Schedule

| Date | Action |
|---|---|
| 2026-05-31 | All persona files marked deprecated (this document) |
| 2026-05-31 | All agent definition files created and validated |
| 2026-07-01 | Grace period ends — persona files may be deleted if no active dependencies |

**Before deletion:** Verify no Claude Code project-level configuration references persona files by name in hooks, settings, or CLAUDE.md files.

---

## Deprecated File Headers

The following header must be added to each deprecated persona file. This marks them as non-authoritative for Claude Code discovery:

```markdown
> **DEPRECATED — 2026-05-31**
> This persona file has been superseded by the Agent Architecture.
> Successor: `C:\Bari\.claude\agents\[successor-agent].md`
> Do not use this file for new work. See `deprecated_personas.md` for migration details.
```
