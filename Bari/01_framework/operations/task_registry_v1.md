> ⛔ **FROZEN — NON-AUTHORITATIVE (since 2026-05-31, TASK-117).**
> This markdown registry is **no longer a source of truth**. The single authoritative
> registry is **`C:\Bari\tasks\`** (one `TASK-NNN.md` per task; state in YAML frontmatter),
> rendered by the live Command Center. Do **not** edit or consult this file for current
> task state — it is retained only as a historical snapshot. Governance now lives in
> `C:\Bari\01_framework\operations\` (work_classification / registry_first_rule / registry_protocol).

# Bari Task Registry — v1 (FROZEN SNAPSHOT)

**Status:** Frozen historical snapshot — superseded by `C:\Bari\tasks\`
**Date:** 2026-05-31
**Scope:** All active agent work across Frontend, Content, and Data agents
**Authority:** ~~source of truth~~ — **superseded.** Authoritative registry is `C:\Bari\tasks\`.

---

## Purpose

The task registry is the single operational log of active and recently closed agent tasks. Command Center reads this document to surface which agents have running work and what that work is. A task absent from this registry is invisible to Command Center regardless of actual in-progress state.

Tasks are registered here when they begin. They are marked CLOSED when the output is accepted. Historical closed tasks are preserved for traceability.

State reporting follows [`registry_protocol_v1.md`](./registry_protocol_v1.md) (Registry Protocol v1, mandatory): every agent return ends with a `Registry Update (proposed)` block; the Central Controller is the sole writer of state and the only role that can record `CLOSED`.

---

## Active Tasks

### TASK-100 — Vegetable Spreads Frontend Page

**Status:** ACTIVE  
**Agent:** Frontend Agent  
**Date opened:** 2026-05-31  
**Scope:** Separate vegetable spreads (matbucha, eggplant, roasted pepper) from the hummus comparison page and create a dedicated vegetable-spreads comparison page.

**Context:**  
Hummus v1 launched at `/hashvaot/hummus` containing 59 products: 36 legume-family spreads (hummus, masabacha) and 23 vegetable-family spreads (matbucha ×11, eggplant ×7, pepper ×5). EXCEPTION-002 established a distinct weight vector for the vegetable family. A dedicated page surfaces these as a coherent consumer category with appropriate methodology.

**Deliverables:**
- New route `/hashvaot/vegetable-spreads`
- Registry entry in `src/lib/comparisons/registry/categories/`
- Corpus scoped to vegetable-family subtypes only
- Page wired to existing `ComparisonShelfPage` template

**Blockers:** None registered.

---

### TASK-101 — Vegetable Spreads Content and Methodology Copy

**Status:** ACTIVE  
**Agent:** Content Agent  
**Date opened:** 2026-05-31  
**Scope:** Write the vegetable-spreads category methodology explanation and intro copy for the new comparison page.

**Context:**  
Vegetable spreads (matbucha, eggplant, roasted pepper) score under EXCEPTION-002 weight vectors — protein signal is de-weighted, glycemic and additive quality are up-weighted. Consumer-facing copy must reflect this without surfacing internal weight constants or framework vocabulary (ontology-leakage policy applies).

**Deliverables:**
- Category eyebrow label and headline (Hebrew)
- `methodologyLines` copy explaining what the page scores and how it differs from hummus
- Hero intro paragraph scoped to vegetable-condiment consumer use cases

**Blockers:** TASK-100 corpus definition must be confirmed before hero stats can be derived.

---

### TASK-102 — Category-Boundary Review Across Comparison Pages

**Status:** ACTIVE  
**Agent:** Data Agent  
**Date opened:** 2026-05-31  
**Scope:** Audit category boundaries across all active comparison pages to ensure no product appears in more than one page and that boundary rules are documented.

**Context:**  
The vegetable-spreads split from hummus creates a boundary between `/hashvaot/hummus` and `/hashvaot/vegetable-spreads`. This review confirms the boundary is clean, that the hummus corpus retains only legume-family products after the split, and that any other pages with mixed-category corpora are identified.

**Deliverables:**
- Category-boundary audit report listing all affected pages and any cross-page product overlaps
- Confirmed exclusion sets for hummus post-split
- Flag any other comparison pages where similar boundary issues exist

**Blockers:** None registered.

---

### TASK-114 — Implement Registry Protocol v1 across Agent OS

**Status:** RETURNED — awaiting Central Controller acceptance
**Agent:** Product Agent
**Date opened:** 2026-05-31
**Scope:** Create a mandatory Registry Protocol defining task lifecycle states, the required agent return format, and the Central Controller acceptance/rejection formats — eliminating dashboard drift from unreported task state.

**Context:**
Agents returned deliverables without structured state, leaving tasks `IN_PROGRESS` after completion and forcing the Central Controller to reconstruct state manually. Registry Protocol v1 makes a `Registry Update (proposed)` block mandatory on every return and fixes closure authority with the Central Controller.

**Deliverables:**
- `registry_protocol_v1.md` (lifecycle, mandatory protocol, ownership, examples)
- Lifecycle-state vocabulary + protocol pointer added to this registry

**Blockers:** None registered.

---

### TASK-115 — Command Center Support for Registry Protocol v1

**Status:** RETURNED — awaiting Central Controller acceptance
**Agent:** Frontend Agent
**Date opened:** 2026-05-31
**Scope:** Make the Command Center route Registry Protocol v1 lifecycle states into operational sections (Active Work / Awaiting Review / Blockers / Changes Requested), excluding CLOSED from operational sections. No dashboard redesign, no new lifecycle model, no change to Bari category/product logic.

**Context:**
Command Center existed only as a wireframe concept (`visual_wireframe_v1.md` §5) with no code. This task adds a state→section routing contract and a self-contained reference dashboard that reads this registry as its single source of truth.

**Deliverables:**
- `command_center_registry_support_v1.md` (state→section model, read contract, chip conventions)
- `command-center/index.html` (dependency-free reference dashboard)

**Blockers:** None registered.

---

## Recently Closed Tasks (Post-Hummus v1 Launch)

| Task | Scope | Agent | Closed |
|------|-------|-------|--------|
| TASK-086 | Remove per-grade boilerplate; product-specific explanation arrays | CE | 2026-05-31 |
| TASK-087A | Category-boundary decision for non-spread chickpea products | CE | 2026-05-31 |
| TASK-087B | Implement combined exclusion set (NOVA-1 + non-spread = 10 IDs) | CE | 2026-05-31 |
| TASK-087C | Hero/display counts derived from rendered products | CE | 2026-05-31 |
| TASK-089 | BSIP2 spread-subtype calibration assessment | CE | 2026-05-31 |
| TASK-089A | Quantified proposal for vegetable vector weights | CE | 2026-05-31 |
| TASK-091 | Nutrition review of proposed subtype weights | CE | 2026-05-31 |
| TASK-094 | Revised methodology incorporating TASK-091 requirements | CE | 2026-05-31 |
| TASK-095 | Implement EXCEPTION-002 subtype weights in score_engine.py | CE | 2026-05-31 |
| TASK-090 | Final acceptance QA — verdict READY_FOR_DEC002 | CE | 2026-05-31 |
| TASK-116 | Registry First Rule across Agent OS (rule + Agent OS guidance + process docs) | Product Agent | 2026-05-31 |

---

## Lifecycle States

Per [`registry_protocol_v1.md`](./registry_protocol_v1.md):

| State | Meaning | Set by |
|-------|---------|--------|
| `IN_PROGRESS` | Agent actively working | Central Controller |
| `BLOCKED` | Waiting on a named dependency | Central Controller (from agent proposal) |
| `RETURNED` | Work delivered, awaiting review | Central Controller (from agent proposal) |
| `CHANGES_REQUESTED` | Returned for rework → resumes as `IN_PROGRESS` | Central Controller |
| `CLOSED` | Accepted and complete (Active → Closed table) | **Central Controller only** |

Agents may propose `RETURNED` or `BLOCKED` in their return block; they may never propose `CLOSED` or `ACCEPTED`.

---

## Governance

- **Registry first:** Any task-management request (status/close/accept/reject/block/resume/reopen) is answered by consulting this registry, not conversation memory. This registry is authoritative. See [`registry_first_rule_v1.md`](./registry_first_rule_v1.md).
- **Opening a task:** Record it here before beginning work. An unregistered task is invisible to Command Center.
- **Reporting state:** Every agent return ends with a `Registry Update (proposed)` block (Registry Protocol v1). A return without one is treated as still `IN_PROGRESS`.
- **Closing a task:** Only the Central Controller records `CLOSED`. Move it from Active to the closed table with the close date and final agent.
- **Scope discipline:** Task entries describe deliverables, not implementation steps. Steps belong in handoff docs or individual task briefs.
- **Task numbering:** Sequential from TASK-001. TASK-103 is the Product Agent task that created this registry. The next task opened after this registry is created should be TASK-104 or higher.

---

*Task Registry v1 — Bari / 2026-05-31*
