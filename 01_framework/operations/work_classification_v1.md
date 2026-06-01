# Work Classification — v1

**Status:** Active — **MANDATORY**
**Date:** 2026-05-31
**Scope:** All agents and the Central Controller, before any work begins
**Created by:** TASK-117 (Product Agent)
**Related:** [`registry_first_rule_v1.md`](./registry_first_rule_v1.md) · [`registry_protocol_v1.md`](./registry_protocol_v1.md)

> This is the gate **in front of** the task lifecycle. It decides whether a request becomes a tracked task at all. It adds no lifecycle states and does not redesign the registry.

---

## The distinction

Every incoming request is one of two kinds. Classify it **before** acting.

### Conversation Work
Handled directly in the conversation. **No TASK number. No registry entry. No dashboard entry.**

Typical examples:
- quick advice or a recommendation
- a clarification or explanation
- a prompt edit or wording tweak
- a minor copy fix
- a small one-off request
- a lightweight review or sanity check

If it's Conversation Work: just do it and answer. Do **not** mint a `TASK-XXX`, do **not** write to `C:\Bari\tasks\`, do **not** expect it on the dashboard.

### Registry Work
Tracked through the full lifecycle. **Gets a TASK number, lifecycle tracking, and dashboard visibility.**

A request is Registry Work if **any** of these hold:
- it is multi-step or spans more than one work session
- it produces a deliverable that will be **reviewed / accepted** (RETURNED → CLOSED)
- another task or agent **depends on** its outcome
- it changes shipped product, scoring, governance, or the dashboard itself
- the Central Controller **explicitly assigns it a `TASK-XXX`**

If it's Registry Work: register `C:\Bari\tasks\TASK-NNN.md` before starting (Registry Protocol v1), track it through the lifecycle, and it appears on the dashboard.

---

## Decision rule (fast path)

```
Does the request have / need a TASK-XXX, a reviewed deliverable,
a dependency, or a change to shipped/governed artifacts?
   ├── NO  → Conversation Work  → answer inline, no registry, no dashboard
   └── YES → Registry Work      → register TASK-NNN, track lifecycle, dashboard
```

When genuinely unsure, default to **Conversation Work** — keep the system lightweight. Promote to Registry Work only when one of the Registry Work conditions is actually met. Do not create tasks "just in case."

---

## Why this matters

The registry and dashboard are for **tracked** work. Minting a task for every clarification or copy tweak floods the registry, inflates the dashboard, and buries the work that genuinely needs review and acceptance. Conversation Work stays in the conversation; Registry Work stays in the registry. All agents apply this distinction.

---

*Work Classification v1 — Bari / 2026-05-31*
