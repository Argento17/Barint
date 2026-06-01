# Bari Legacy Migration Criteria — v1

**Status:** Active  
**Date:** 2026-05-28  
**Scope:** `milk-comparison-page.tsx`, `bread-comparison-dashboard.tsx`, `src/components/snack/`  
**Companion:** `legacy_isolation_policy_v1.md` — defines what migration means and its eligibility criteria

---

## How This Document Works

`legacy_isolation_policy_v1.md` defines when a legacy page is *eligible* for migration (5 criteria, all required). This document defines what *triggers* migration consideration in the first place.

Triggers are separated into two classes:

- **Mandatory triggers** — when one of these is present, migration is required. The page cannot remain legacy.
- **Elective triggers** — when one of these is present, migration becomes eligible but is not forced. A decision is made.

A trigger does not mean migration begins immediately. It means migration enters the queue and the eligibility criteria in `legacy_isolation_policy_v1.md` are evaluated.

---

## Mandatory Migration Triggers

These conditions require migration. A legacy page that exhibits a mandatory trigger cannot receive further additive changes — it must be migrated or taken offline.

---

### 1. Mobile Auto-Fail Condition

**Trigger:** The page fails any of the 10 auto-fail conditions in `mobile_geometry_checklist_v1.md` on the primary viewport (375×812px).

The 10 auto-fail conditions are:
1. Hero total height > 300px
2. Pre-table height > 480px
3. Zero product rows visible on initial load
4. Score chip not visible without scrolling
5. Section heading between prologue and first product row
6. Score chip uses color encoding
7. Filter panel open by default on page load
8. Framework term in consumer-facing content (NOVA, cap, BSIP, routing)
9. Expanded row opens as modal or new screen
10. Methodology has a section heading

If any auto-fail condition is triggered by a rendering change, browser update, or data change that was not present at the time of original build — the page requires migration, not a patch.

**Exception:** if the auto-fail condition existed at original build time and has been present since launch without user impact, it is a known legacy debt — not a new trigger. Document it and leave as-is until an elective trigger arises.

---

### 2. Ontology Leakage Escalation

**Trigger:** A framework term appears in consumer-facing rendered content that was not present at original build time, as a result of a data change, content update, or pipeline output change.

Examples:
- A new product's `name_he` or `why_featured_he` field contains "NOVA4", "BSIP", or a structural class label
- A pipeline field rename propagates a technical term into a previously clean display string
- A content editor adds a framework term to an editorial copy field

**Not a trigger:** framework terms that were present at original build time (e.g., `SnackShelfStatBar` "NOVA4%" — this is known Gen 0 debt, not new leakage).

**Rationale:** new ontology leakage is a live correctness failure. A patch that removes one leaked term while leaving the underlying Gen 0 component intact only defers the problem. Migration removes the leakage structurally.

---

### 3. Component Incompatibility

**Trigger:** A shared canonical component (`src/components/shared/`) cannot be used in a feature that a legacy page requires, because the legacy page's architecture prevents the shared component from being composed into it without a destructive change.

This trigger fires when:
- A shared component's interface and the legacy page's data shape are incompatible and cannot be bridged by a data adapter alone
- A canonical layout behavior (inline expansion, sticky filter) conflicts with the legacy page's structural assumptions (e.g., it uses a sheet overlay that prevents inline expansion from rendering correctly)

**Not a trigger:** a canonical component that simply looks different from the legacy equivalent — visual difference is not incompatibility.

---

### 4. Major Redesign

**Trigger:** A deliberate decision to change the visual architecture, layout, or interaction model of the page — not a data update, not a copy update, not a bug fix.

Examples:
- Adding a filter dimension that requires the sticky filter button pattern
- Changing the product list from card grid to row list
- Replacing the hero with a compact version

A major redesign that begins on a legacy page without migration is a scope creep event. When a page requires a structural change of this magnitude, it migrates rather than receiving a destructive patch.

---

### 5. Dashboard Drift Event

**Trigger:** A new Gen 0 pattern is added to a legacy page — a chart, a new aggregate stat, a second tooltip, a new dimension bar, or any pattern listed as prohibited in `architecture_generations_registry_v1.md`.

Dashboard drift means the Gen 0 debt is actively growing. A page in which Gen 0 debt is growing is not stable legacy — it is regressing. Migration stops the regression by replacing the page with the canonical architecture.

**How to identify:** compare the page's current component tree against its state at its original build. Any Gen 0 pattern not present at original build constitutes drift.

---

## Elective Migration Triggers

These conditions make a legacy page eligible for migration but do not require it. A decision is made based on available capacity and the eligibility criteria.

---

### 6. Filter Rewrite

**Trigger:** The category requires a filter change — adding a dimension, changing dimension values, or changing the filter's interaction model — that cannot be done additively.

A filter rewrite on a legacy page is a good natural migration point because:
- It requires touching the filter component, which is a direct Gen 0 pattern replacement
- The canonical StickyFilterButton pattern resolves the same need with the correct architecture

Migration is elected, not mandatory. If the filter change is minor and purely additive (relabeling a filter option), it does not trigger migration.

---

### 7. Major Content Refresh

**Trigger:** The category data is substantially refreshed — new products, new scores, new insight lines — in a volume that requires rebuilding the data adapter or editorial content files.

A major content refresh is a natural migration point because:
- The data adapter rebuild is the same work regardless of whether it targets the legacy or canonical component interface
- Building to the canonical interface during a refresh has near-zero additional cost compared to building to the legacy interface

Migration is elected. If the content refresh is incremental (updating a few product entries), it does not trigger migration.

---

### 8. Canonical Precedent Established (Passive Trigger)

**Trigger:** The first canonical category (מעדנים) has been live in production and its shared components have been validated. This makes all legacy pages eligible under eligibility criterion #1 in `legacy_isolation_policy_v1.md`.

This is a passive trigger — it does not initiate migration immediately. It means the eligibility gate has opened. Migration for a specific legacy page still requires a decision and the remaining 4 eligibility criteria.

---

## Leave-As-Is Conditions

The following conditions require the legacy page to be left untouched, regardless of how much technical debt it carries.

| Condition | Rule |
|---|---|
| No mandatory trigger is present | Leave as-is. Additive changes only. |
| Canonical precedent does not exist (מעדנים not live) | Leave as-is. Eligibility criterion #1 is not met. |
| Active editorial content update is in progress | Leave as-is until the update is complete. Do not begin migration during a content cycle. |
| The legacy page has known Gen 0 violations that predate the canonical spec | Leave as-is. Known debt from before the spec existed is not a trigger — it is documented legacy status. |
| A migration would require URL or routing changes | Leave as-is until routing impact is scoped separately. Migration does not change routes. |
| The migration scope cannot be bounded to the component tree | Leave as-is. If migration requires touching data, routing, or types beyond the legacy page's own files, the scope has not been properly bounded. Scope the migration and return. |
| The legacy page is the only active page for that category | Leave as-is unless a mandatory trigger is present. Removing or breaking the only page for a category is a user-facing regression. |

---

## Decision Matrix

| Trigger present | Mandatory trigger? | Eligibility met? | Action |
|---|---|---|---|
| Mobile auto-fail (new) | Yes | Yes | Migrate |
| Mobile auto-fail (new) | Yes | No | Block additive changes; work toward eligibility |
| Ontology leakage (new) | Yes | Yes | Migrate |
| Ontology leakage (new) | Yes | No | Hotfix the specific leaked term only; work toward eligibility |
| Component incompatibility | Yes | Yes | Migrate |
| Component incompatibility | Yes | No | Do not build the feature on the legacy page; wait for eligibility |
| Major redesign | Yes | Yes | Migrate |
| Major redesign | Yes | No | Defer the redesign until eligible |
| Dashboard drift event | Yes | Yes | Migrate |
| Dashboard drift event | Yes | No | Revert the drift; do not patch on top of it |
| Filter rewrite (elective) | No | Yes | Migration eligible — decide |
| Major content refresh (elective) | No | Yes | Migration eligible — decide |
| No trigger | — | — | Leave as-is |

---

## What Migration Is Not

- Migration is not an opportunity to redesign the category editorial content
- Migration is not an opportunity to change the URL or route
- Migration is not a refactor of the data pipeline
- Migration is not adding features the canonical architecture does not support
- Migration is not a gradual incremental update — the legacy component tree is replaced, not evolved

Migration has one output: a page that uses the canonical component set (`src/components/shared/`) and passes the full `mobile_geometry_checklist_v1.md` and `frontend_integration_checklist_v1.md` Section 3 audit.

---

*This document is updated when a new legacy page is added to scope or when experience from the first migration reveals criteria that were over- or under-specified.*
