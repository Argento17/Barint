# Bari Skills Changelog

**Document:** CHANGELOG.md
**Owner:** Frontend Architect
**Status:** ACTIVE
**Task:** TASK-050

---

## Versioning Rules

All Bari skills and persona files follow semantic versioning: `vMAJOR.MINOR.PATCH`

### Major version increment (`v1.x → v2.0`)

A major version increment is required when:
- A workflow stage is added, removed, or reordered in a skill
- A governance check is added or removed
- An owner changes
- A skill's activation scope changes materially (new trigger categories or removal of existing ones)
- A persona's decision rights or hard rules change
- A skill's output format changes in a breaking way (fields removed or renamed)

Major version changes require explicit approval from the skill owner and a corresponding entry in the skills registry.

### Minor version increment (`v1.0 → v1.1`)

A minor version increment is required when:
- Prompt wording is improved for clarity without changing behavior
- Examples are added or updated
- New trigger phrases are added without removing existing ones
- Output format adds new optional fields
- Interaction rules with other skills are clarified without changing responsibility boundaries
- Prohibited actions list is extended with new items

Minor version changes require owner review. A registry update is optional if the skill's core registration fields are unchanged.

### Patch version increment (`v1.0.0 → v1.0.1`)

A patch version increment is required when:
- Typos are corrected
- Formatting is fixed
- Markdown structure is tidied without content changes
- A broken link or path reference is corrected

Patch changes may be made without owner sign-off. A changelog entry is required.

---

## Changelog Entries

---

### 2026-05-31

#### Skills Registry v1.0 — Created (TASK-050)

**Type:** New document
**File:** `registry/skills_registry_v1.md`
**Author:** Frontend Architect

Formal skills registry established. Covers:
- 4 workflow skills (SKILL-001 through SKILL-004)
- 6 persona files (PERSONA-001 through PERSONA-006)

All assets registered at v1.0. Registry version: v1.0.

---

#### SKILL-001 bari-category-factory — v1.0 (TASK-050)

**Type:** Initial registration
**File:** `bari-category-factory/SKILL.md`
**Owner:** Data Architecture / Category Team

Initial registration of the category factory skill. Seven-stage pipeline: Shelf Mapping → Corpus Filter → BSIP0 Gate → BSIP1 Enrichment → QA Gate → BSIP2 Readiness → Frontend Packaging.

---

#### SKILL-002 bari-bsip2-scoring-governance — v1.0 (TASK-050)

**Type:** Initial registration
**File:** `bari-bsip2-scoring-governance/SKILL.md`
**Owner:** Scoring Governance Lead

Initial registration of the BSIP2 scoring governance skill. Five-check governance protocol: Evidence Registry Reference → Label Observability → Category Activation Scope → Rollback Plan → Rule Accumulation Prevention.

---

#### SKILL-003 bari-qa-audit — v1.0 (TASK-050)

**Type:** Initial registration
**File:** `bari-qa-audit/SKILL.md`
**Owner:** QA Lead

Initial registration of the QA audit skill. Six-stage protocol: QA Runner → Traceability → Hard Fails → Warnings → Baseline Freeze → Run Invalidation.

---

#### SKILL-004 bari-frontend-ui — v1.0 (TASK-050)

**Type:** Initial registration
**File:** `bari-frontend-ui/SKILL.md`
**Owner:** Frontend Architect

Initial registration of the frontend UI skill. Six-check compliance protocol: Comparison Structure → Data Traceability → RTL Layout → Accessibility → Component Consistency → Generic AI UI Prevention.

---

#### PERSONA-001 chief-nutrition-officer — v1.0 (TASK-050)

**Type:** Initial registration
**File:** `chief-nutrition-officer.md`
**Owner:** Chief Nutrition Officer

Initial registration. Primary workspace: `C:\Bari`.

---

#### PERSONA-002 frontend-architect — v1.0 (TASK-050)

**Type:** Initial registration
**File:** `frontend-architect.md`
**Owner:** Frontend Architect

Initial registration. Primary workspace: `C:\Users\HP\bari`.

---

#### PERSONA-003 head-of-product — v1.0 (TASK-050)

**Type:** Initial registration
**File:** `head-of-product.md`
**Owner:** Head of Product

Initial registration. Primary workspace: `C:\Bari`.

---

#### PERSONA-004 design-director — v1.0 (TASK-050)

**Type:** Initial registration
**File:** `design-director.md`
**Owner:** Design Director

Initial registration. Primary workspaces: `C:\Bari\01_framework\frontend\` (design specs) and `C:\Users\HP\bari` (rendered review).

---

#### PERSONA-005 research-analyst — v1.0 (TASK-050)

**Type:** Initial registration
**File:** `research-analyst.md`
**Owner:** Research Analyst

Initial registration. Primary workspace: `C:\Bari`.

---

#### PERSONA-006 qa-audit-lead — v1.0 (TASK-050)

**Type:** Initial registration
**File:** `qa-audit-lead.md`
**Owner:** QA & Audit Lead

Initial registration. Primary workspaces: both `C:\Bari` (data integrity) and `C:\Users\HP\bari` (rendered site).

---

## How to Add a Changelog Entry

When making any change to a skill or persona file, add an entry here following this format:

```
### YYYY-MM-DD

#### <SKILL-ID or PERSONA-ID> <skill-name> — <new version> (<task reference>)

**Type:** New document | Major update | Minor update | Patch
**File:** <relative path>
**Owner:** <owner>

<One paragraph describing what changed and why.>
```

Entries within a date are listed in the order: new documents first, major updates second, minor updates third, patches last.

---

*Bari Skills Changelog — TASK-050 — Frontend Architect — 2026-05-31*
